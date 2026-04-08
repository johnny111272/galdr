# Intermediate Container

## Purpose

The intermediate container sits between chunking/gathering and rendering. It holds unrendered bundles sorted by slot. Each bundle carries everything needed to resolve and render one output point — but nothing has been rendered yet.

**Why not go straight to rendering?** Because you can inspect the intermediate state. When the output is wrong, you can check: did the bundle get the right data? The right content? The right visibility toggle? If the bundle is wrong, the problem is in chunking/gathering. If the bundle is right, the problem is in the resolver/renderer. This isolation makes debugging tractable.

## Structure

Four arrays — one per buffer slot: heading, preamble, body, closing. Each entry is a bundle.

## What a Bundle Carries

Each bundle represents one output point. It needs to carry:

- Where it came from — data field, content field, or both
- The raw data value (if data-driven) — scalar, list, or compound items
- The raw content text (if content-driven) — before interpolation
- The variant sub-table and selector (if a variant)
- The visibility state from the structure toggle
- The display format and threshold (if a list)
- The data shape — so the resolver knows which renderer to route to

The exact model will be determined by what chunking actually produces. The key constraint: a bundle must be self-contained. The resolver should not need to look outside the bundle to do its job.

## What a Bundle Does NOT Carry

- Rendered text — that's the resolver's output, not the bundle's content
- References to other bundles — bundles are independent
- Section-level context — each bundle resolves on its own

## Open Design Questions

- Should the bundle carry raw Pydantic field values, or already-unwrapped data? Raw preserves type information for the resolver. Unwrapped is simpler but loses the ability to inspect annotation types.
- For compound lists (D1/D2/E), is it one bundle per list or one per item? Probably per list — the specialized renderer handles iteration internally.
