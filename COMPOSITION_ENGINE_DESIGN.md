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
- Threshold pair: `role_expertise_format = ["bulleted", "inline"]` + `threshold = 3` → bulleted above 3, inline at or below

---

## Trunk Matching: How the Engine Finds Data for Content Fields

The naming alignment enables mechanical matching across axes. The engine never needs a mapping table.

**The `_label` suffix signals that data entries follow.** When the engine encounters a content field ending in `_label`:

1. Render the label text (or interpolate if it's a template)
2. Strip `_label` to get the **trunk** → e.g., `role_expertise_label` → trunk = `role_expertise`
3. Look up `data.{trunk}` → the data list (e.g., `data.role_expertise`)
4. Look up `display.{trunk}_format` → the format (e.g., `display.role_expertise_format`)
5. Look up `display.{trunk}_format_threshold` → threshold if format is a pair
6. Render the list using the resolved format
7. Continue to the next content field (typically `{trunk}_postscript`)

**Template placeholders use direct name lookup.** `{{role_identity}}` matches `data.role_identity` exactly. No trunk derivation needed.

**Visibility toggles use the full content field name.** `declaration_heuristic_postscript` → check `structure.declaration_heuristic_postscript_visible`.

**Variant selectors use the content sub-table name.** Content field is a BaseModel subclass (not a string type) → it's a variant sub-table. Look up the matching selector in structure by the same field name.

These four lookup mechanisms cover every cross-axis connection:

| Content field type | Mechanism | Example |
|-------------------|-----------|---------|
| StringTemplate | Direct placeholder lookup in data | `{{role_identity}}` → `data.role_identity` |
| StringText/StringProse | Check `_visible` in structure | `closing_identity_reminder` → `structure.closing_identity_reminder_visible` |
| `*_label` suffix | Strip suffix → trunk → `data.{trunk}` + `display.{trunk}_format` | `role_expertise_label` → `data.role_expertise` + `display.role_expertise_format` |
| BaseModel subclass | Variant sub-table → selector in structure by same name | `framing_variant` (content) → `structure.framing_variant` |

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

## Processing Order: Data Drives, Content Decorates

**The data model field order IS the rendering order.** The engine walks DATA fields in declaration order, not content fields. Content fields are decorations that attach to data fields via trunk naming. This is the fundamental architecture — getting it backwards (walking content, inserting data) was the mistake of two previous attempts.

For each section, the flow is:

```
1. SECTION DECORATION (top)
   - heading (from content — the one field named just "heading")
   - section-level preamble, explanatory prose, variant selections
   - (content fields whose trunk does NOT match any data field name)

2. DATA WALK (in data field declaration order)
   For each data field:
   a. Resolve overrides: check structure for {field}_override → if true, substitute
   b. Classify: gate (boolean/enum for branching) | scalar | list
   c. If gate → process logic, skip rendering
   d. Check visibility: structure.{trunk}_visible → skip if hidden
   e. Prepend decoration: content.{trunk}_heading, _preamble, _label → render before
   f. Render data:
      - Scalar in template → find content template with {{field_name}}, interpolate
      - Scalar no template → render as-is
      - List → find display.{trunk}_format (+threshold), format and render
   g. Append decoration: content.{trunk}_postscript → render after

3. SECTION DECORATION (bottom)
   - section-level closing prose, postscripts
   - (content fields whose trunk does NOT match any data field, with closing suffixes)
```

**How to tell section-level content from field-level content:** If a content field's trunk matches a data field name → field-level (attaches to that data field). If it doesn't match → section-level (renders before or after the data walk based on its suffix).

**Override resolution:** Structure can override data values via the `_override` pattern. When `structure.{field}_override = true`, the sibling value `structure.{field}` replaces `data.{field}`. This fires BEFORE classification and rendering.

**Guardrails family:** Four sections (constraints, anti_patterns, success_criteria, failure_criteria) have `section_visible` and `max_entries_rendered` in structure. These are section-level gates — check before any field processing. `section_visible = false` → skip entire section. `max_entries_rendered > 0` → truncate the data list before rendering.

To change the rendering order of data within a section, change the verdandi YAML field order in the data model. To change which prose decorates which field, change the content field's trunk name. No reordering code.

---

## What the Engine Code Looks Like

The engine is a small set of functions:

1. **Data field classifier** — given a data field's type, determines: gate | scalar | list (pure, primitive)
2. **Content matcher** — given a data field trunk, finds associated content decoration: heading, preamble, label, postscript. Also identifies section-level content (no data field match). (pure, simple)
3. **Override resolver** — checks structure for `_override` flags, substitutes values (pure, simple)
4. **Visibility checker** — looks up `_visible` toggle in structure (pure, primitive)
5. **Variant selector** — given a variant sub-table in content + selector in structure, picks the prose (pure, simple)
6. **Template interpolator** — `{{key}}` replacement (already built: `logic/pure/template/primitive.py`)
7. **List formatter** — resolve format from display, render items (already built: `logic/pure/render/`)
8. **Data unwrapper** — RootModel `.root` → plain values for template interpolation (transform, simple)
9. **Section walker** — the main loop: section decoration → data walk → section closing (pure, composed)
10. **Pipeline orchestrator** — loads all four inputs through gates, iterates section_order, calls section walker, joins sections with dividers, writes output (orchestrate)
11. **CLI** — thin typer wrapper (entry point)

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
- Data field classifier
- Content matcher
- Override resolver
- Visibility checker
- Variant selector
- Data unwrapper (RootModel `.root` → plain values)
- Section walker (the core loop)
- Pipeline orchestrator
- CLI
