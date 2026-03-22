# TOML Architecture: Agent Control Surface Configuration

Design document for the TOML files that configure agent prompt rendering.

---

## File Architecture

Four files. Three base files define the default agent. One override file defines the delta.

### structure.toml

Stable configuration. Shared across all variants. Never copied for experiments.

Contains:
- Section ordering (`section_order` array with standalone sections and groups)
- Per-section visibility toggles (boolean: show/hide optional fragments)
- Per-section `divider_above` overrides (when a section needs non-default entrance)
- Structural variant selectors (e.g., `field_ordering = "identity_first"`)
- Global defaults (default divider, etc.)

Does NOT contain prose, templates, or format enums.

### content.toml

The variant surface. This is what gets copied/overridden for behavioral experiments.

Contains:
- Text blobs — pure prose, no `{{DATA}}` references
- Template blobs — prose with `{{DATA}}` holes
- Variant sub-tables — `[section.{name}_variant]` tables whose keys are mutually exclusive prose alternatives selected by a structure.toml selector of the same name

Scalar fields are strings. Variant sub-tables contain string values keyed by variant name. Visibility is controlled by structure.toml toggles, not by empty strings in content.

### display.toml

Format selectors. Orthogonal to prose changes.

Contains:
- Format enums dispatching to renderer functions (e.g., `"bulleted"`, `"inline"`, `"path_first"`)
- Threshold tuples for count-based format switching
- Joiner strings for array inline rendering

### override.toml

Deltas on top of the base three. Contains fields from ANY of the other files.

Load order: structure → content → display → override (override replaces matching fields).

Purpose: experiment with specific knobs without copying entire files. The override IS the experiment description — read it and see exactly what's different.

May evolve into CLI field access: `galdr render --set content.identity.declaration="..."` or `galdr sweep --field display.identity.expertise_format --values bulleted,inline,numbered`.

---

## Universal Block Assembly Order

Every rendered block follows the same positional sequence:

```
heading → preamble → label → entries → postscript
```

Not every block has all five elements — most skip some. But when elements exist, they appear in this order. The suffixes in content.toml field names map directly to position:

| Suffix | Position | Purpose | Example |
|---|---|---|---|
| `_heading` | First | Names the block. Rendered as H2/H3. | `context_required_heading = "Required Reading"` |
| `_preamble` | After heading | Sets context before any data. Frames how to process what follows. | `context_required_preamble = "These are not reference materials..."` |
| `_label` | Before data | Immediately introduces a data field or list. | `expertise_label = "**Your judgment is authoritative in:**"` |
| (entries) | Middle | The data itself — array items, field values, template expansions. | `context_entry = "**{{context_label}}**: Read..."` |
| `_postscript` | After data | Reinforces, constrains, or summarizes what was just presented. | `expertise_postscript = "Your expertise is strictly limited to the areas listed above."` |
| `_transition` | Between blocks | Marks a cognitive shift from one block to the next. | `knowledge_data_transition = "With this knowledge internalized..."` |

This sequence applies at two levels:

**Section level** — the section itself has a heading, optional preamble, sub-blocks, and optional postscript.

**Sub-block level** — within a section, each data group (context_required, parameters, etc.) follows the same heading → preamble → label → entries → postscript pattern.

### Why Position Signifiers Matter

LLMs editing content.toml will pattern-match on field names. An LLM seeing `_postscript` will write text that references what came before ("the areas listed above"). An LLM seeing `_preamble` will write text that sets up what follows ("the following documents"). The field name steers the language without the LLM needing to understand the rendering pipeline.

Wrong name → wrong language → broken rendering. `expertise_is_strictly_limited` might produce "the following areas:" placed after the list. `expertise_postscript` will produce "the areas listed above" — correctly aligned.

---

## Content Primitives

### Text Blobs

Pure prose. No data references. Swappable.

```toml
expertise_postscript = "Your expertise is strictly limited to the areas listed above."
```

### Template Blobs

Prose with `{{DATA}}` holes. The template is the knob; the data is fixed.

```toml
declaration = "You are a {{role_identity}}."
responsibility_label = "**Scope:** {{role_responsibility}}"
```

### Array Display (handled by display.toml, not content)

When data is a list, the display file controls HOW it renders. There is no content template for bare array items — if there's nothing to adjust, there's no TOML entry. The renderer just outputs the data.

---

## Naming Conventions

### Position Signifiers

Field names MUST encode position relative to the data they reference. This prevents prose-position misalignment. LLMs editing these files pattern-match on names — the name steers the language.

- `_preamble` — text BEFORE a block, setting context. Author will write "the following...", "below you will find..."
- `_postscript` — text AFTER a block, reinforcing or constraining. Author will write "the areas listed above...", "as stated above..."
- `_label` — immediately before data, introducing it. Author will write "Your X:", "The following X:"

Example: `expertise_postscript` → author writes "the areas listed above." If this were just `expertise_is_strictly_limited`, an author might write "the following areas:" and the renderer would place it after the list — broken.

### Descriptive Over Convenient

Each file is read in isolation. Field names must be self-documenting without context from other files.

Bad: `closer = false`
Good: `closing_identity_reminder_visible = false`

A reader of structure.toml sees `closing_identity_reminder_visible = false` and knows exactly what's being toggled without opening content.toml.

### Visibility Toggles Use `_visible` Suffix

Every boolean in structure.toml that controls whether a fragment renders uses the `_visible` suffix. This makes the field's purpose unambiguous when reading structure.toml in isolation.

```toml
# structure.toml
[identity]
closing_identity_reminder_visible = false

# content.toml
[identity]
closing_identity_reminder = "Remember: you are a {{role_identity}}."
```

The structure field is `closing_identity_reminder_visible` (boolean). The content field is `closing_identity_reminder` (string). The shared root name creates obvious cross-reference. The `_visible` suffix prevents confusion — without it, `closing_identity_reminder = false` could mean "the reinforcement text is false" rather than "don't show it."

---

## Field Interface Patterns

Five patterns, each identified by suffix. A naive reader encountering any field can identify the pattern from its name.

### 1. `_visible` — Fragment Visibility

Controls whether a prose fragment renders. Two forms:

**Simple toggle:**
```toml
preamble_visible = true
```

**Auto with count threshold** — renderer decides based on a count:
```toml
rule_count_awareness_prelude_visible = "auto"   # "auto" | "always" | "never"
rule_count_awareness_prelude_auto_threshold = 5
```
`"auto"` applies the threshold. `"always"` and `"never"` override it.

**Auto with data condition** — renderer decides based on a boolean data property, not a count:
```toml
exact_vs_judgment_explanation_visible = "auto"  # "auto" (render when mixed modes) | "always" | "never"
```
No `_auto_threshold` — the auto condition is binary (e.g., "are instruction modes mixed?"), not count-based. The field comment documents what "auto" means. When the auto condition is a data property rather than a count, a numeric threshold is semantically inappropriate and is omitted.

### 2. `_override` — Data Override

The definition data carries a value. The rendering layer can substitute it.

`_override = false` → data passes through unchanged. `_override = true` → use the sibling value instead.

```toml
example_display_headings_override = false
example_display_headings = true                # only applies when override = true

examples_max_number_override = false
examples_max_number = 0                        # 0 = no truncation, N = cap. Only when override = true
```

The sibling value matches the data's type. No mixed-type fields, no string sentinels.

### 3. `_variant` — Content Variant Selection

Selects among named prose alternatives in content.toml. The alternatives live in a **sub-table** named after the variant selector. The sub-table's keys ARE the allowed enum values — self-documenting, no comments needed, and the schema derives the enum directly from the keys.

```toml
# structure.toml
section_preamble_variant = "standalone"   # enum values derived from content sub-table keys

# content.toml
[constraints.section_preamble_variant]
standalone = "These constraints govern your execution..."
references_instructions = "While executing your instructions..."
references_critical_rules = "These constraints are binding operational rules..."
```

The structure selector name matches the content sub-table name. An LLM reading content.toml sees a table called `section_preamble_variant` and immediately knows these are mutually exclusive alternatives — the table structure makes it impossible to misread as separate fields that all render.

#### Shared Variants

A single variant selector may drive multiple content field families when those families always change together. The sub-table contains sub-sub-tables for each governed family:

```toml
# structure.toml
framing_variant = "territory"

# content.toml
[security_boundary.framing_variant.heading]
territory = "Your Workspace"
environmental = "Operating Environment"
cage = "Permitted Boundaries"

[security_boundary.framing_variant.workspace_path_declaration]
territory = "Your workspace is {{WORKSPACE_PATH}}..."
environmental = "You operate within {{WORKSPACE_PATH}}..."
cage = "You are confined to {{WORKSPACE_PATH}}..."

[security_boundary.framing_variant.section_preamble]
territory = "Within this workspace, you can access:"
environmental = "The following paths are available to you:"
cage = "You are permitted to access only the following paths:"
```

The variant value picks a key, looked up in every sub-table under the variant name. The sub-table names are the governed field families. All sub-tables must have the same keys.

### 4. `_format` + `_format_threshold` — Display Format

Controls HOW data renders (bullets, inline, numbered, etc). Lives in display.toml.

```toml
expertise_format = ["bulleted", "inline"]
expertise_format_threshold = 3
```

Tuple = conditional (above threshold, at-or-below). Plain string = always that format.

### 5. Plain Enums (no suffix convention)

Structure selectors that don't fit the above — presentation paradigms, organizational modes.

```toml
rule_presentation = "single_sentence"          # "single_sentence" | "heading_plus_body"
internal_hierarchy = "flat"                     # "flat" | "universal_then_output_tool"
```

These are rare and section-specific.

---

## Threshold Notation

Count-based format switches use a tuple convention: `[above_threshold_format, at_or_below_threshold_format]`.

```toml
expertise_format = ["bulleted", "inline"]
expertise_format_threshold = 3
```

Reads as: "bulleted above 3, inline at or below 3."

When there is no threshold — single format always applies — use a plain string:

```toml
expertise_format = "bulleted"
```

Type tells behavior: array = conditional switch, string = always this format.

---

## Section Ordering

The `section_order` array in structure.toml controls inter-section sequence.

Supports standalone sections and groups:

```toml
section_order = [
    "identity",
    "security_boundary",
    "critical_rules",
    "instructions",
    "examples",
    { group = "Guardrails", sections = ["constraints", "anti_patterns"] },
    "success_criteria",
    "failure_criteria",
    "output",
    "writing_output",
    "return_format",
]
```

- Standalone sections render at H2.
- Groups render the group name at H2, children at H3.
- Sections inside groups are still independently configured — they just render one heading level deeper.

### Per-Section Dividers

Global default `divider_above` applies to all sections. Per-section override when a section needs a different entrance (attention-grabbing fence for critical_rules, no divider for a section that flows from the previous one).

`divider_above` is per-section because each section controls its own entrance. When sections are reordered, the divider travels with the section.

Overuse of custom dividers reduces the effect. Most sections inherit the default.

Frontmatter's `---` is invariant (YAML format), not a rendering knob.

---

## Heading Levels

H1 is not used. Two reasons:
1. H1 with agent name creates "biographical document" framing — agents treat content as descriptive rather than prescriptive
2. H1 below H2 is semantically broken — reordering sections becomes fragile

All sections render at H2 (or H3 when inside a group). This is invariant — handled by the renderer, not configurable per section.

---

## Invariant Rendering Rules (Code, Not TOML)

These are universal behaviors baked into the renderer. They never vary. They are not knobs.

- **Silence for absence** — when optional data is absent, render nothing. Don't mention what isn't there.
- **Frontmatter delimiters** — `---` YAML boundaries are non-negotiable format.
- **Heading levels** — H2 for sections, H3 for grouped children. Always.
- **Embedded schema** — JSON code fence around schema content. Always `json` language tag.
- **Boolean gates** — `has_output_tool`, `context_required` presence, empty arrays. The renderer evaluates data properties and takes the appropriate path. Not configurable.

---

## Structural Variants vs Format Knobs

Two categories of variation with different cost profiles:

**Format knobs** (display.toml) — trivially dynamic. Renderer receives an enum and switches output. Cheap. Change freely.

**Structural variants** (structure.toml) — field ordering, field grouping, fused vs discrete. Each variant is a separate Pydantic model. The model IS the specification — field order is defined by the model's field sequence.

Only IDENTITY has a meaningful structural variant (`field_ordering = "identity_first" | "responsibility_first"`). This is a unicorn — two models, not a configurable ordering system.

---

## Filtering Principle

If a fragment has no meaningful variation — if it's just rendering data as-is with no prose wrapping, no label, no framing — it does NOT get a TOML entry. The renderer just outputs the data.

Only things that VARY are knobs. Only knobs live in TOML.

---

## Worked Example: IDENTITY Section

### structure.toml — `[identity]`

```toml
[identity]
field_ordering = "identity_first"
fuse_declaration_and_role_description = false
expertise_is_strictly_limited_visible = true
closing_identity_reminder_visible = false
```

### content.toml — `[identity]`

```toml
[identity]
heading = "AGENT: {{title}}"
declaration = "You are a {{role_identity}}."
responsibility_label = "**Scope:** {{role_responsibility}}"
expertise_label = "**Your judgment is authoritative in:**"
expertise_is_strictly_limited_postscript = "Your expertise is strictly limited to the areas listed above."
closing_identity_reminder = "Remember: you are a {{role_identity}}."
```

### display.toml — `[identity]`

```toml
[identity]
expertise_format = ["bulleted", "inline"]
expertise_format_threshold = 3
responsibility_format = ["bulleted", "prose"]
responsibility_format_threshold = 3
```

### Example override.toml

```toml
[identity]
declaration = "You are a {{role_identity}} — not a debugger, not a reviewer, not a creative writer."
responsibility_label = "**You are done when:** {{role_responsibility}}"
expertise_label = "**Pay special attention to:**"
closing_identity_reminder_visible = true
```

Note: the override sets `closing_identity_reminder_visible = true` (structure concern — toggle visibility) without changing the text (content concern — stays as defined in content.toml). Override can contain fields from any of the three base files.

---

## Visibility Toggles vs Data Gates

A critical distinction. The renderer has two independent mechanisms that can prevent a fragment from rendering:

1. **Data gates** (code) — `has_output_tool`, `context_required` presence, empty arrays. The renderer checks data properties and silently omits fragments when the data isn't there. This is silence-for-absence. Not configurable.

2. **Visibility toggles** (structure.toml) — `_visible` booleans that let an author suppress a fragment even when the data IS present.

These are NOT redundant. A data gate says "this data doesn't exist, so there's nothing to render." A visibility toggle says "this data exists, but I don't want the boilerplate prose that wraps it."

**Example**: CRITICAL_RULES has `output_tool_exclusivity_visible = true` and `batch_discipline_visible = true`. The renderer also checks `has_output_tool` (data gate). Both mechanisms are needed:
- When `has_output_tool = false`: data gate suppresses everything. Toggle is irrelevant.
- When `has_output_tool = true`: data gate passes. Toggle controls whether the prose renders. You might want to test whether the exclusivity rule actually helps, or whether the tool enforcement (hooks) makes it unnecessary.

**Rule**: If the ONLY scenario is "data present → always render," there's no toggle. But if there's a legitimate reason to suppress prose when data is present (testing, simplification, section is already covered elsewhere), the toggle is justified.

### What Does NOT Need a `_visible` Toggle

**Variant content fields** — when a `_variant` selector chooses between prose alternatives, the individual content fields for each variant value do not get independent `_visible` toggles. Selecting the variant selects its prose. If you don't want the prose, change the variant or toggle the parent concept's visibility. Example: CONSTRAINTS `section_preamble_variant = "references_critical_rules"` renders `section_preamble_references_critical_rules` along with `hierarchy_tier_comparison` and `hierarchy_three_tier_explanation`. These are part of the variant's prose package, not independently togglable.

**Code-gated conditional content** — some content fields render only when a code-level data condition is met (e.g., task type, batch mode). The renderer decides inclusion based on the data, not a structure toggle. These fields note their condition in the decisions text. A `_visible` toggle is only needed if someone would want to suppress the field when the data condition IS met. If the only scenario is "condition met → render, condition not met → omit," no toggle.

---

## Section Categories

Sections fall into distinct categories with different control surface needs.

### Guardrails Family (experimental playground)

**Sections**: anti_patterns, constraints, success_criteria, failure_criteria

These four sections are the primary experimental surface for testing how much behavioral scaffolding an agent needs. They ALL get:
- `section_visible` — master toggle to show/hide the entire section even when data exists
- `max_entries_rendered` — truncation cap (0 = render all) to test "top N items" without changing the underlying data

Why: You want to test combinations — success criteria only, constraints + anti_patterns only, all four, just two. You want to test whether 3 constraints work as well as 12. The data stays complete; the rendering layer controls what the agent sees.

The other 9 sections do NOT get `section_visible` or `max_entries_rendered`. They are structural sections that either render (data present) or don't (data absent).

### Critical Rules (boilerplate show/hide)

Critical rules is NOT a guardrails section. Each rule is a designed prose fragment in content.toml, not author data that passes through. The per-rule `_visible` toggles exist to test which boilerplate rules earn their place. Some rules may be redundant with system enforcement (hooks prevent tool bypass anyway). Toggles let you test that hypothesis.

### Mechanics Sections (data-driven, minimal knobs)

**Sections**: output, writing_output, return_format

These sections are primarily data-driven. The renderer checks data conditions and takes the appropriate path. The control surface is thin — mostly transition/framing prose and a few variant selectors. Content that just restates what the data provides or explains infrastructure the agent can't control does not get a TOML entry.

### Intentional Cross-Section Overlap

CRITICAL_RULES and WRITING_OUTPUT both assert tool exclusivity. This is intentional redundancy — critical_rules establishes the rule with hard-failure consequence, writing_output provides the mechanics. The CRITICAL_RULES version is terse ("this is the only correct tool"). The WRITING_OUTPUT version is operational ("here's how to invoke it").

INPUT's `input_completeness_postscript` ("do not seek additional sources") overlaps with CRITICAL_RULES' `input_is_your_only_source`. Same principle — input frames it as completeness, critical_rules frames it as prohibition. Different behavioral levers for the same underlying rule.

---

## Section Boundary Rules

Each section owns a specific concern. When in doubt about where a knob belongs:

- **OUTPUT** — what is produced, what format, where it goes, what schema governs it. Never mentions tools, batch sizes, or write mechanics.
- **WRITING_OUTPUT** — how to use the output tool. Invocation, batching, naming, validation. Only renders when `has_output_tool = true`.
- **CRITICAL_RULES** — hard rules with failure consequences. Short, terse, non-negotiable.
- **CONSTRAINTS** — ongoing compliance standards. Author data that passes through with framing prose.
- **ANTI_PATTERNS** — specific failure modes. Author data with "Do not X — Y" structure.
- **INPUT** — what the agent receives and prerequisite reading.
- **INSTRUCTIONS** — step-by-step execution with mode markers.
- **RETURN_FORMAT** — how to report completion status to the dispatcher.

---

## Threshold Types

Three distinct threshold purposes, named by suffix:

- **`_format_threshold`** — switches between display formats (e.g., bulleted vs numbered). Lives in display.toml.
- **`_visibility_threshold`** — controls whether a fragment appears at a certain count. Lives in display.toml when count-driven, structure.toml when data-driven.
- **`_activation_threshold`** — triggers a behavioral feature (e.g., polarity grouping at 11+ items). Lives in display.toml.
- **`_auto_threshold`** — governs the "auto" mode of an auto/always/never toggle. Lives in structure.toml next to the toggle.

---

## Cross-Section Data Flow

Same data values appear at multiple rendering sites. The pipeline duplicates values into every section that needs them. Each site renders the value with its own template for its own purpose. This is normal rendering — the source data is invariant.

Notable multi-site values:
- **workspace_path** → security_boundary (territory), critical_rules (prohibition)
- **tool_name** → critical_rules (exclusivity), writing_output (mechanics), security_boundary (grants)
- **description** → frontmatter (metadata), dispatcher (caller decision support). NOT in identity (catalog metadata, not agent-facing).
