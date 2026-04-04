# Naming Alignment Plan: Cross-Axis Mechanical Matching

## Purpose

Make field names mechanically matchable across all four axes (data, content, structure, display) so the galdr composition engine can derive cross-axis connections from field names alone — no heuristics, no mapping tables.

## The Mechanical Matching Rule

```
content:   {trunk}_label           → data:      {trunk}
content:   {trunk}_postscript      → structure: {trunk}_postscript_visible
display:   {trunk}_format          → data:      {trunk}  (the list it formats)
display:   {trunk}_format_threshold → pairs with {trunk}_format
structure: {field_name}_visible     → content:   {field_name}
```

Strip the positional suffix from a content field name → get the trunk → trunk maps to the data field and display format field. Template placeholders (`{{name}}`) use direct name lookup against data fields.

---

## Required Changes

### Group 1: Identity Content/Display — Add `role_` Prefix to Match Data

Data model uses `role_expertise` and `role_responsibility`. Content and display drop the `role_` prefix. Fix: add `role_` to content and display fields so the trunk matches data. The data model is the source of truth (comes from the pipeline) — other axes align to it.

**Verdandi source:** agent-output YAML, identity content and display fields

| Axis | Current | Rename To | Trunk |
|------|---------|-----------|-------|
| content | `expertise_label` | `role_expertise_label` | `role_expertise` |
| content | `expertise_is_strictly_limited_postscript` | `role_expertise_is_strictly_limited_postscript` | `role_expertise` |
| structure | `expertise_is_strictly_limited_postscript_visible` | `role_expertise_is_strictly_limited_postscript_visible` | `role_expertise` |
| display | `expertise_format` | `role_expertise_format` | `role_expertise` |
| display | `expertise_format_threshold` | `role_expertise_format_threshold` | `role_expertise` |
| content | `responsibility_label` | `role_responsibility_label` | `role_responsibility` |
| display | `responsibility_format` | `role_responsibility_format` | `role_responsibility` |
| display | `responsibility_format_threshold` | `role_responsibility_format_threshold` | `role_responsibility` |

**Data model stays unchanged.** No pipeline cascade. No agent definition TOML changes.

**Cascade:** Verdandi agent-output YAML → Draupnir schemas → Nornir output gates → Galdr generated models + `extracted/content.toml` + `extracted/display.toml`

---

### Group 2: Constraints Display — Match Data Field Name

Data calls the list `rules`. Display calls the format `enumeration_format`. No shared trunk.

**Verdandi source:** agent-output YAML, constraints display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| `enumeration_format` | `rules_format` | data: `rules` |
| `enumeration_format_threshold` | `rules_format_threshold` | pairs with `rules_format` |

**Cascade:** Verdandi YAML → Draupnir schemas → Nornir gates (output gates) → Galdr generated models + `extracted/display.toml`

---

### Group 3: Anti-Patterns Display — Match Data Field Name

Data calls the list `patterns`. Display calls the format `pattern_list_format`. Trunk mismatch (`patterns` vs `pattern_list`).

**Verdandi source:** agent-output YAML, anti_patterns display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| `pattern_list_format` | `patterns_format` | data: `patterns` |

**Cascade:** Same as Group 2.

---

### Group 4: Examples Content/Display — Match Data Field Name

Data calls the field `example_heading`. Content calls it `entry_heading`. Display calls it `entry_heading_format`.

**Verdandi source:** agent-output YAML, examples content and display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| content: `entry_heading` | `example_heading` | data: `example_heading` (in ExampleEntry) |
| display: `entry_heading_format` | `example_heading_format` | content: `example_heading` |
| display: `entry_body_container` | `example_body_container` | consistency with `example_` prefix |
| display: `entry_separator` | `example_separator` | consistency |

**Cascade:** Same as Group 2.

---

### Group 5: Instructions Vocabulary — Align Content/Structure/Display to Data Trunk

Data uses `instruction_mode` with values `deterministic`/`probabilistic`. Content/structure/display wholesale renamed this to `exact_vs_judgment`/`exact`/`judgment` — a divergence that breaks trunk matching. Field names are flags that connect axes, not rendering vocabulary.

**Principle:** Data model is source of truth. Content/structure/display field names align to it. The rendered prose INSIDE the content fields can say "exact"/"judgment" — that's a content authoring choice, not a naming concern.

**Verdandi source:** agent-output YAML, instructions content/structure/display fields

| Axis | Current | Rename To |
|------|---------|-----------|
| content | `step_header_exact` | `step_header_deterministic` |
| content | `step_header_judgment` | `step_header_probabilistic` |
| content | `step_header_exact_n_only` | `step_header_deterministic_n_only` |
| content | `step_header_judgment_n_only` | `step_header_probabilistic_n_only` |
| content | `exact_vs_judgment_body_prefix_exact` | `instruction_mode_body_prefix_deterministic` |
| content | `exact_vs_judgment_body_prefix_judgment` | `instruction_mode_body_prefix_probabilistic` |
| content | `exact_vs_judgment_explanation_mixed` | `instruction_mode_explanation_mixed` |
| content | `exact_vs_judgment_explanation_uniform_exact` | `instruction_mode_explanation_uniform_deterministic` |
| content | `exact_vs_judgment_explanation_uniform_judgment` | `instruction_mode_explanation_uniform_probabilistic` |
| content | `signal_at_mode_change_to_exact` | `signal_at_mode_change_to_deterministic` |
| content | `signal_at_mode_change_to_judgment` | `signal_at_mode_change_to_probabilistic` |
| content | `section_closer_exact_vs_judgment_recap` | `section_closer_instruction_mode_recap` |
| structure | `exact_vs_judgment_explanation_visible` | `instruction_mode_explanation_visible` |
| structure | `exact_vs_judgment_marker_placement` | `instruction_mode_marker_placement` |
| structure | `instructions_preamble_exact_vs_judgment_preview_visible` | `instructions_preamble_instruction_mode_preview_visible` |
| structure | `section_closer_exact_vs_judgment_recap_visible` | `section_closer_instruction_mode_recap_visible` |
| display | `exact_vs_judgment_recap_format` | `instruction_mode_recap_format` |

**Data model stays unchanged.** No pipeline cascade. No agent definition TOML changes.

**Cascade:** Verdandi agent-output YAML → Draupnir schemas → Nornir output gates → Galdr generated models + `extracted/content.toml` + `extracted/structure.toml`

---

### ~~Group 6: Scaffolding Terminology~~ — NOT A MISMATCH

`structural_complexity_override` (structure) and `scaffolding_tier_*_activation_threshold` (display) are different concepts in different axes. Structure says WHICH tier. Display says WHAT COUNTS trigger each tier in auto mode. Names are correct for what they describe. No rename needed.

---

## Additional Schema Changes

### `role_responsibility` — Change from Scalar to List

**DECIDED:** `role_responsibility` becomes a list type in the data model. Currently typed as single `RoleResponsibility` (StringProse) but display already has `role_responsibility_format` with threshold-based switching, which only makes sense for lists. Current usage confirms agents can have multiple responsibility statements.

**Verdandi source:** agent-builder YAML, identity section — change `role_responsibility` from atom to array type.

**Cascade:** This one touches the data model → full pipeline cascade: Verdandi agent-builder → Draupnir → Nornir gates → Regin models + pipeline code → all agent definition TOMLs → Galdr models.

---

### Input Section — Add to All Three Output Schemas

**DECIDED:** The input section exists in the data model but was never extracted to the output schemas during the three-axis split. Must be added to content, structure, and display.

**Verdandi source:** agent-output YAML — add `input` section to all three output schemas.

#### Content fields to add (`InputContent`):

| Field | Type | Notes |
|-------|------|-------|
| `heading` | StringText | Default: "Input" |
| `section_preamble` | StringProse | Conditional on context_required presence. "Before processing your input, you must read and internalize several reference documents." |
| `description_format_template` | StringTemplate | `"Your input is a {{format}} file containing {{description}}."` — integrated presentation |
| `context_required_heading` | StringText | "Required Reading" — sub-block heading |
| `context_required_preamble` | StringProse | "These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting." |
| `context_entry_template` | StringTemplate | `"**{{context_label}}**: Read {{context_path}}"` |
| `context_available_heading` | StringText | Sub-block heading for optional context |
| `knowledge_data_transition` | StringProse | "With this knowledge internalized, here is your input data:" |
| `parameters_heading` | StringText | "Parameters" |
| `parameter_entry_template` | StringTemplate | `` "`{{param_name}}` ({{param_type}}): {{param_description}}" `` |
| `input_completeness_postscript` | StringProse | "Your input and required reading together constitute your complete input. Do not seek additional sources." |
| `schema_intro` | StringTemplate | `"Input validates against: {{input_schema}}"` |

#### Structure fields to add (`InputStructure`):

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `section_preamble_visible` | Boolean | true | Conditional — only renders when context_required present |
| `context_required_preamble_visible` | Boolean | true | |
| `knowledge_data_transition_visible` | Boolean | true | Only when context_required present |
| `input_completeness_postscript_visible` | Boolean | false | Experimental — off by default |
| `schema_intro_visible` | Boolean | true | Only when input_schema present |
| `parameters_heading_visible` | VisibilityMode | "auto" | Auto based on param count |
| `parameters_heading_auto_threshold` | Integer | 2 | Show heading when 3+ params |

#### Display fields to add (`InputDisplay`):

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `context_required_format` | ListFormat | "numbered" | Numbered implies reading order |
| `context_available_format` | ListFormat | "bulleted" | |
| `parameters_format` | UnionFormatOrPair | ["bulleted", "prose"] | Prose for 1-2, bullets for 3+ |
| `parameters_format_threshold` | Integer | 2 | |

**Cascade:** Verdandi agent-output YAML → Draupnir → Nornir output gates → Galdr generated models + new `[input]` sections in `extracted/content.toml`, `extracted/structure.toml`, `extracted/display.toml`.

---

### Content Fields Missing `_visible` Toggles

Add structure `_visible` toggles for content fields that currently always render:

| Section | Content Field | Toggle to Add |
|---------|--------------|---------------|
| identity | `declaration_heuristic_postscript` | `declaration_heuristic_postscript_visible` |
| constraints | `hierarchy_tier_comparison` | `hierarchy_tier_comparison_visible` |
| constraints | `hierarchy_three_tier_explanation` | `hierarchy_three_tier_explanation_visible` |
| failure_criteria | `any_one_triggers_abort` | `any_one_triggers_abort_visible` |
| return_format | `report_completion_label` | `report_completion_label_visible` |

The token fields (`token_must_be_first_word_tokens_three/two`) are data-gated (mutually exclusive based on ABORT token availability), not visibility-toggled. No toggle needed.

---

## Implementation Order

**Two cascades:**

**Cascade A — agent-output (Groups 1-5 renames + input section + missing toggles):**
All in verdandi agent-output YAML. No pipeline impact. No agent definition changes.
- Do all renames + input section addition + missing toggles in one pass
- Draupnir (agent-output schemas) → Nornir output gates → Galdr `generate_structures.py`
- Update `extracted/content.toml`, `extracted/structure.toml`, `extracted/display.toml`

**Cascade B — agent-builder (`role_responsibility` scalar→list):**
Touches the data model → full pipeline cascade.
- Verdandi agent-builder YAML → Draupnir → Nornir gates → Regin models + code → Agent definition TOMLs → Galdr models
- Can be done separately, before or after Cascade A

**Recommendation:** Do Cascade A first (all output-side changes in one pass). Then Cascade B (the one data model change).

---

## Verification

After the cascade completes:

```bash
# Verify galdr models regenerate
cd ~/.ai/smidja/galdr && uv run python src/galdr/generate_structures.py

# Verify gates accept updated TOMLs
uv run python -c "
import gate_output_structure_input, gate_output_content_input, gate_output_display_input
for gate, path in [
    (gate_output_structure_input, 'extracted/structure.toml'),
    (gate_output_content_input, 'extracted/content.toml'),
    (gate_output_display_input, 'extracted/display.toml'),
]:
    result = gate.validate(path)
    print(f'{path}: {\"ok\" if result[\"ok\"] else \"FAIL: \" + result[\"error\"][\"message\"][:100]}')
"
```

Then verify mechanical matching works by inspecting generated model field names across axes.
