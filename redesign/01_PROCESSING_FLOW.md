# Processing Flow

## The Four Stages

The composition engine processes each section through four stages. Each stage makes the problem smaller.

### Stage 1: Chunk

Take all four axes for one section. Sort every field into one of four buffer slots (heading, preamble, body, closing) based on its terminal suffix. No processing, no rendering — just sorting.

**Why this matters:** After chunking, the heading fields can't interfere with the body fields. The preamble can't mix with the closing. Each slot is an independent, smaller problem. We've gone from "figure out everything about this section" to "figure out this one slot."

### Stage 2: Gather

For each output point within a slot, collect everything that affects it into one bundle. A body data field gets its matched content decorations, its visibility toggle, its variant selector, its display format — all gathered together before any processing happens.

**Why this matters:** After gathering, each bundle is self-contained. Everything needed to resolve and render that one output point is in one place. No more scanning across axes during rendering. The resolver just opens the bundle and works with what's inside.

### Stage 3: Resolve + Render

Feed each bundle through the hourglass resolver-renderer. The wide input end takes everything from the bundle. The narrow middle resolves: is it visible? which variant? interpolate placeholders? what format? The wide output end routes to the appropriate renderer based on what the resolution produced.

**Why this matters:** The resolver handles one bundle at a time. It doesn't know about sections, slots, or other bundles. Every bundle goes through the same resolution steps. The rendering differs per type — plain text just passes through, a simple list gets formatted, a compound structure goes to a specialized renderer — but the resolution is uniform.

### Stage 4: Buffer

Append each rendered text to its buffer slot. When all slots are done, join them in order: heading, preamble, body, closing. That's the section output.

**Why this matters:** The buffer just collects strings. It doesn't process. The ordering was determined in Stage 1 (which slot) and Stage 2 (which position within the slot). By this point, everything is rendered text.

## Key Properties

- **No rendering before Stage 3.** Stages 1 and 2 sort and gather. If the gathering is wrong, you can inspect it before any rendering happens.
- **Each stage reduces the problem.** Four axes → four slots → individual bundles → rendered text.
- **The resolver is uniform.** Same steps for every bundle. Different renderers for different output types, but the resolution is one path.
- **Stages 1 and 2 may combine** in implementation — chunking naturally involves gathering. But conceptually they're separate concerns: where does it go (chunking) vs what does it need (gathering).
