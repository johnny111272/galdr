# Galdr — Context Refresh Protocol

## STOP. Read this before writing any code.

You are working on a composition engine that combines gate-validated agent data with prose, structure, and display configuration to produce deployable markdown prompts. You have context from a compaction summary or from earlier in this session. **You are almost certainly wrong about the details.**

After compaction, you have section names and a vague sense of "combine data with templates." You lose the four-axis independence requirement, the v2 zone architecture rules, the gate IO boundary, the import direction constraints, and the specific ways this project diverges from how you'd normally write Python. You will produce output that looks right, runs, and silently violates the architecture.

**This has happened before.** Previous sessions in this project have:

- Built a 14-class OOP inheritance hierarchy (`SectionStyle → IdentityStyle → ...`) inside what was supposed to be a functional architecture — entire renderer had to be scrapped
- Used `dict[str, Any]` for gate output instead of `GateResult.model_validate()` — broke the type-safety chain at the exact point it matters most
- Created a `reshape_style_toml()` function in `functions/pure/` that took and returned `dict[str, Any]` — a pure function with `Any` is nonsensical
- Organized code by consumer ("used by pipeline", "used by loader") instead of by function type ("string operations", "unwrap operations")
- Entangled the four input axes by putting content decisions in the data model — destroying the benchmarking matrix that is galdr's entire purpose

None of them felt uncertain while doing it.

**The test:** Can you state what the four input axes are, which ones the author controls vs which ones the pipeline produces, and why entangling any two of them is a structural failure? Can you draw the v2 zone architecture from memory — which zones exist, which can import from which, and what the level hierarchy is? If not, read the recovery sources below before proceeding.

---

## You Will Get These Things Wrong

### Entangling the Four Axes
**Detection:** If you find yourself putting a heading string, a list format choice, or a visibility toggle inside the data model... or reading a structure toggle from the content config... or anything that makes one axis depend on another...
**Why it's wrong:** Galdr exists to multiply one agent definition across content × structure × display variants for benchmarking. If axes are entangled, swapping one changes the others. The benchmarking matrix collapses. Data (from pipeline, frozen) × Structure (what to include) × Content (how to word it) × Display (how to format it) — four independent inputs, four independent TOML files.
**Recovery:** Read `AGENT_BUILD_SYSTEM.md` — the "Four Input Axes" section defines the boundaries.

### Putting IO in Python Code
**Detection:** If you find `Path.read_text()`, `open()`, `write()`, or any filesystem access in logic code...
**Why it's wrong:** Gates handle ALL file IO. Input gates read TOML and return validated JSON. Output gates take JSON and write validated TOML/markdown. Python between gates transforms typed data. The only IO in galdr Python is gate invocation (in `logic/impure/`) — never raw filesystem calls.
**Recovery:** Read regin's `logic/impure/gates/primitive.py` and `simple.py` — that is the pattern.

### Violating the V2 Zone Architecture
**Detection:** If you find yourself importing from `pure/` into `transform/`, or from `impure/` into `pure/`, or doing same-level imports within a zone, or putting a module-level constant in a logic file...
**Why it's wrong:** The v2 zone architecture is enforced by gleipnir. Two orthogonal axes: zone matrix (which zones can see which) and level matrix (imports go UP only, never down, never sideways). Pure is walled — cannot see impure or transform. Transform is fully isolated — no edges to/from pure or impure. Only orchestrate sees all three. Same-level imports are banned — this is the primary anti-monolith binding.
**Recovery:** Read `~/.ai/smidja/nornir/core/gleipnir_core/V2_ZONE_ARCHITECTURE.md` — the two-axis intersection table is the complete import law.

### Organizing Code by Consumer Instead of Function Type
**Detection:** If you create a module called `pipeline_helpers.py`, `render_utils.py`, `loader_support.py`, or anything named after WHO uses the code rather than WHAT the code does...
**Why it's wrong:** Code is organized by what it IS, not who calls it. String manipulation goes in `logic/pure/string/`, unwrapping goes in `logic/pure/unwrap/`, gate calls go in `logic/impure/gates/`. When looking for a function, you think "what does it do?" not "who uses it?" This is how the mental map works — import paths tell you what guarantees you get.
**Recovery:** Read `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_NAMING_IS_INSTRUCTION.md` and look at draupnir/regin file trees for examples.

### Floating Code to Higher Levels Than Needed
**Detection:** If a CC=1 function lives in `composed.py`, or a CC=2 function lives in `assembled.py`...
**Why it's wrong:** The gravity rule: code must live at the LOWEST level it legally can. `primitive.py` = CC=1, `simple.py` = CC=1-3, `dispatch.py` = CC=1-2, `composed.py` = CC=4-8, `assembled.py` = CC=1-2. Floating everything to `composed/` where constraints are loosest is the default LLM behavior. Gleipnir enforces gravity — CC below the level's minimum is a violation.
**Recovery:** Read V2_ZONE_ARCHITECTURE.md "Cyclomatic Complexity Enforcement" and "The Gravity Rule."

### Building Monolithic Render Functions
**Detection:** If a single function checks visibility, selects variants, interpolates templates, formats lists, AND assembles markdown...
**Why it's wrong:** Each of those is a separate concern at a different level. Visibility checking is a primitive (CC=1). Variant selection is simple (CC=2-3). Template interpolation is a primitive. List formatting is simple. Assembly is composed. A monolith that does all of them will exceed CC limits and violate level placement. Find the functional primitive — what is the ONE thing?
**Recovery:** Read `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_HEMINGWAY_CODING.md` — the "Break It Down" section.

### Modifying Generated Files
**Detection:** If you open any file in `structure/gen/` to edit it...
**Why it's wrong:** Files in `structure/gen/` are generated by `generate_structures.py` from JSON Schemas. Manual edits are silently overwritten on next generation. Hand-authored models live in `structure/model/` and `structure/config/`.
**Recovery:** Change source → run draupnir → run `generate_structures.py`.

### Whack-a-Mole Error Fixing
**Detection:** If you're fixing errors one by one, error count is going UP, you're adding `# type: ignore`, or touching the same file repeatedly...
**Why it's wrong:** Scattered errors = architectural problem, not syntax problems. Error clusters by type reveal WHAT is broken. Error clusters by location reveal WHERE. STOP. Read ALL errors. Find the pattern. Secure the boundary. Errors disappear.
**Recovery:** Read `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_REFACTORING_DISCIPLINE.md`.

### Writing Per-Section Code
**Detection:** If you're creating `compose_identity()`, `render_constraints()`, or ANY function named after a specific section...
**Why it's wrong:** The engine is GENERIC. One `compose_section()` processes all sections. Section-specific knowledge lives in the models and TOML, not in code. The field name suffixes (`_heading`, `_preamble`, `_label`, `_postscript`) encode position. The five operations (visibility gate, text passthrough, template interpolation, variant selection, list formatting) handle every field type. There is no per-section code. This mistake has been made twice before — once with OOP classes, once with per-section composer functions.
**Recovery:** Read `COMPOSITION_ENGINE_DESIGN.md` — especially "Core Principle" and "What the Engine Code Looks Like."

### Using the Old Code as Reference
**Detection:** If you're looking at git history for the deleted `functions/` directory, or referencing `styles/default.toml` as a current format...
**Why it's wrong:** The old renderer was OOP disguised as functional code — it was scrapped entirely. `styles/default.toml` is the OLD pre-split format (combined content/structure/display). The current architecture uses three separate TOML files. Nothing in the old code is normative.
**Recovery:** Read `AGENT_BUILD_SYSTEM.md` for the current design. Read draupnir and regin source code for v2 zone patterns.

---

## Recovery Sources

| Document | Path | What it tells you |
|----------|------|-------------------|
| **Agent Build System** | `AGENT_BUILD_SYSTEM.md` | Four input axes, section inventory, composition model, benchmarking matrix |
| **V2 Zone Architecture** | `~/.ai/smidja/nornir/core/gleipnir_core/V2_ZONE_ARCHITECTURE.md` | Zone/level import rules, CC bounds, gravity rule, gleipnir enforcement |
| **Hemingway Coding** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_HEMINGWAY_CODING.md` | Functional primitives, pure/impure separation, essence extraction |
| **Safety Taxonomy** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_SAFETY_TAXONOMY.md` | Import path IS the safety contract — four categories |
| **Naming Is Instruction** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_NAMING_IS_INSTRUCTION.md` | Names overpower instructions 200:1, compounding cascade |
| **IO Externalization** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_IO_EXTERNALIZATION.md` | Gates externalize IO — application is pure |
| **Errors Are Signal** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_ERRORS_ARE_SIGNAL.md` | Error clusters are diagnostic maps, never silence them |
| **Refactoring Discipline** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_REFACTORING_DISCIPLINE.md` | STOP before fixing, find the pattern, secure the boundary |
| **Economic Model** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_ECONOMIC_MODEL.md` | Gleipnir is pressure, not certification |
| **Context Exhaustion** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_CONTEXT_EXHAUSTION.md` | Confidence + speed = pattern matching, not thinking |
| **Regin source** | `~/.ai/smidja/regin/src/regin/` | Reference implementation — gate pattern, v2 zones, orchestrate wiring |
| **Draupnir source** | `~/.ai/smidja/draupnir/src/draupnir/` | Reference implementation — transform isolation, level progression |

---

## Architecture in One Paragraph

Galdr is the composition engine — the final stage of the agent build pipeline (Verdandi → Draupnir → Nornir → Regin → **Galdr**). It takes a single gate-validated `AgentAnthropicRender` Pydantic model (14 sections of agent data produced by Regin) and combines it with three independently-swappable control surfaces — Structure (what to include: visibility toggles, variant selectors, section ordering), Content (how to word it: headings, templates, prose fragments, variant alternatives), and Display (how to format it: list types, thresholds, separators, containers) — to produce a deployable agent prompt (.md) and a dispatcher skill (SKILL.md). The four axes are independent: one definition × N content variants × M structure variants × K display variants = a benchmarking matrix of agent configurations. Gates handle all file IO. Python between gates is pure computation on typed Pydantic models. The codebase follows gleipnir v2 zone architecture: `structure/` (data only), `logic/pure/` (deterministic), `logic/impure/` (IO via gates), `logic/transform/` (model-to-model, fully isolated), `logic/orchestrate/` (wiring only). Imports go UP through levels (primitive → simple → dispatch → composed → assembled → orchestrate → entry point), never down, never sideways. Code is organized by function type, not by consumer.

---

## MANDATORY: Run Guardrails Frequently

Run after EVERY significant change. Not after finishing a phase. After every file.

---

## Context Reminders for Long Sessions

After ANY compaction, ask yourself:

1. **Are the four axes independent?** Data from pipeline (frozen). Structure, content, display from separate TOML files. If I'm reading content config to make a structure decision, STOP.

2. **Do gates handle IO?** YES. Python never reads or writes files directly. If I'm writing `Path.read_text()` in logic code, STOP.

3. **Am I following v2 zone rules?** Pure can't see impure or transform. Transform can't see pure or impure. Only orchestrate sees all three. No same-level imports. No constants in logic zones. If I'm importing across these boundaries, STOP.

4. **Is code organized by function type?** String ops in string/, unwrap in unwrap/, gates in gates/. NOT by consumer. If I'm creating `pipeline_helpers.py`, STOP.

5. **Does each function do ONE thing?** If it checks visibility AND formats AND assembles — it's a monolith. Find the primitive. Decompose by level.

6. **Am I at the lowest legal level?** CC=1 belongs in primitive, not composed. Check the gravity rule.

7. **Am I reaching for `dict` or `Any`?** This is a CANARY. We pass typed frozen Pydantic models. The data model is generated and validated by gates. `Any` means the boundary is broken.

8. **Am I pattern matching or thinking?** If everything feels clear and fast, I'm probably pattern matching from training data. Slow down. This project diverges from standard patterns deliberately.

---
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- EVERYTHING ABOVE THIS LINE IS BEHAVIORAL (human-maintained, empirical) -->
<!-- EVERYTHING BELOW THIS LINE IS DYNAMIC ORIENTATION (agent-regenerated)  -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
---

## Dynamic Orientation

@./CONTEXT_MAP.md
