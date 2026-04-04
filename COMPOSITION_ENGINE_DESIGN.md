# Composition Engine Design

## What This Document Is

The authoritative design spec for galdr's composition engine — the code that takes four typed inputs and produces markdown. This document exists because previous sessions lost this understanding during compaction and rebuilt the wrong thing (per-section OOP classes, per-section composer functions). **The engine is generic. It does not know sections.**

**If you are about to write section-specific code, STOP and re-read this document.**

Source documents this design distills:
- `agent_control_surfaces/TOML_ARCHITECTURE.md` — field naming, assembly order, interface patterns
- `agent_control_surfaces/CROSS_SECTION_PATTERNS.md` — rendering conditionals, format knobs, structural variants
- `AGENT_BUILD_SYSTEM.md` — four axes, section inventory, benchmarking matrix

---

## Core Principle

**One generic engine processes all sections.** Section-specific knowledge lives in the data models and TOML files, not in code. The engine reads field names, checks types, and applies the appropriate operation. It never asks "which section am I in?"

---

## The Four Inputs

Every section receives four typed chunks — one from each axis. The engine extracts the section's chunk from each top-level model:

```
data      = AgentAnthropicRender.{section}     # what to say (from pipeline)
structure = AgentOutputStructure.{section}      # what to include (toggles, selectors)
content   = AgentOutputContent.{section}        # how to word it (templates, prose, variants)
display   = AgentOutputDisplay.{section}        # how to format it (list styles, thresholds)
```

These four chunks are independent. The engine never reads a content field to make a structure decision. The engine never reads a display field to determine visibility.

---

## Universal Block Assembly Order

Every rendered block follows the same positional sequence:

```
heading → preamble → label → entries → postscript
```

Not every block has all five elements — most skip some. But when elements exist, they appear in this order. Content field name suffixes encode position:

| Suffix | Position | What the author writes |
|--------|----------|----------------------|
| `_heading` | First | "Names the block" |
| `_preamble` | After heading | "The following...", "Below you will find..." |
| `_label` | Before data | "Your X:", "The following X:" |
| *(entries)* | Middle | The data itself |
| `_postscript` | After data | "The areas listed above...", "As stated above..." |
| `_transition` | Between blocks | Marks a cognitive shift |

This applies at two levels: the section itself, and sub-blocks within a section.

---

## The Five Operations

The engine has exactly five operations. Every field in every section is handled by one of these. The operation is determined by the field's type and naming convention, not by which section it belongs to.

### 1. Visibility Gate (`_visible` suffix in structure)

Check whether a fragment renders. Three forms:

- **Simple boolean:** `preamble_visible = true` → render or skip
- **Auto with count threshold:** `visible = "auto"` + `auto_threshold = 5` → render when count exceeds threshold
- **Auto with data condition:** `visible = "auto"` → render when a binary data condition is met (e.g., mixed instruction modes)

### 2. Text Passthrough

Plain prose string from content. No placeholders. Render as-is. Gated by its `_visible` toggle if one exists.

Example: `expertise_is_strictly_limited_postscript = "Your expertise is strictly limited to the areas listed above."`

### 3. Template Interpolation

Prose string from content containing `{{placeholder}}` markers. Replace markers with data field values. The data values come from unwrapping RootModel `.root` fields.

Example: `declaration = "You are a {{role_identity}}."` → data provides `role_identity`

### 4. Variant Selection (`_variant` suffix in structure)

Structure has a selector enum. Content has a sub-table with keys matching the enum values. The selector picks which prose alternative renders.

For shared variants (one selector drives multiple content families), the sub-table contains sub-sub-tables for each governed family, all looked up with the same key.

Example:
- Structure: `framing_variant = "territory"`
- Content: `[security_boundary.framing_variant.heading]` → `territory = "Your Workspace"`

### 5. List Formatting (display)

Data provides a list of items. Display provides a format enum (or threshold pair). The engine resolves the format, then renders the list.

- Plain format: `evidence_format = "bare"` → always this format
- Threshold pair: `expertise_format = ["bulleted", "inline"]` + `threshold = 3` → bulleted above 3, inline at or below

---

## Data Gates (Code, Not TOML)

Separate from visibility toggles. These are invariant rules baked into the engine:

- **Silence for absence** — when optional data is null/absent, render nothing
- **Boolean gates** — `has_output_tool = false` → skip output-tool rules entirely
- **Empty arrays** — no items → skip the list and its surrounding prose

Data gates fire before visibility toggles. If the data isn't there, the toggle is irrelevant.

---

## Section Ordering

`structure.section_order.order` — array of 13 section names. The engine iterates this array. For each section name:

1. Extract the four chunks (data, structure, content, display)
2. Check data gate (is the section's data present?)
3. Walk content fields in declaration order
4. Apply operations per field
5. Join fragments → section markdown

Sections render at H2. Heading level is invariant — not configurable.

---

## Dividers

Each section controls the divider ABOVE it. Global default divider applies unless the section has a per-section override in structure. When sections are reordered, the divider travels with the section.

---

## Special Cases (Exactly Two)

### Identity Field Ordering

Identity has two structural variants: `identity_first` and `responsibility_first`. These produce different field sequences. Rather than a dynamic reordering engine, this is handled by two model variants — the structure selector picks which model/order is used.

This is the ONLY section with intra-section field reordering.

### Frontmatter and Dispatcher

Frontmatter is pure serialization (data → YAML). No experimental fragments. Not a presentation concern.

Dispatcher programs the caller, not the agent. Different audience, different purpose. The dispatch strategy matrix (background_mode × max_agents) determines entirely different document shapes.

These two may not share the body-section engine. They have their own render paths.

---

## The Guardrails Family

Four sections get extra control surfaces:
- `section_visible` — master toggle (can hide entire section even when data exists)
- `max_entries_rendered` — truncation cap (0 = render all)

**Sections:** constraints, anti_patterns, success_criteria, failure_criteria

This enables combinatorial testing (all four, just two, top-N items) without changing data.

The other sections do NOT get these. They either render (data present) or don't (data absent).

---

## Processing Order

The engine processes content fields in **declaration order** — the order they appear in the Pydantic model. This is the model's field sequence, which was generated from the schema, which was generated from the verdandi YAML. The order in the model IS the render order.

This means: to change the rendering order of fragments within a section, you change the verdandi YAML field order. You do not write reordering code.

---

## What the Engine Code Looks Like

The engine is a small set of pure functions:

1. **Fragment classifier** — reads a content field's name and type, determines which operation to apply (text, template, variant selection)
2. **Visibility checker** — given a content field name, looks up the corresponding `_visible` toggle in structure
3. **Template interpolator** — `{{key}}` replacement (already built: `logic/pure/template/primitive.py`)
4. **List formatter** — resolve format from display, render items (already built: `logic/pure/render/`)
5. **Section walker** — iterates content fields in declaration order, applies the right operation for each, joins results
6. **Pipeline orchestrator** — loads all four inputs through gates, iterates section_order, calls section walker, joins sections with dividers, writes output

Items 1-4 are pure. Item 5 is pure (or transform if it does model-to-model conversion). Item 6 is orchestrate (it does IO via gates).

**There is no per-section code.** There is no `compose_identity()` or `compose_constraints()`. There is one `compose_section()` that works for any section.

---

## What's Already Built

| Module | Level | What |
|--------|-------|------|
| `logic/impure/gates/ffi.py` | ffi | `call_input_gate` — FFI boundary for Rust gates |
| `logic/impure/gates/simple.py` | simple | `validate_input` — gate call + ok-check |
| `logic/pure/template/primitive.py` | primitive | `interpolate` — `{{key}}` replacement |
| `logic/pure/render/primitive.py` | primitive | `heading`, `bold`, `backtick`, `bullet_item`, `numbered_item` |
| `logic/pure/render/simple.py` | simple | List renderers, `format_inline`, `format_heading` |
| `logic/pure/render/composed.py` | composed | `resolve_format`, `render_list` — threshold-based format dispatch |
| `logic/transform/codegen_clean/` | all | Post-codegen transforms for model generator |

**What's NOT built:**
- Fragment classifier
- Visibility checker
- Variant selector
- Data unwrapper (RootModel `.root` → plain values)
- Section walker
- Pipeline orchestrator
- CLI
