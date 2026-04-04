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

### Group 6: Instructions Display — Align Scaffolding Terminology

Structure uses `structural_complexity_override`. Display uses `scaffolding_tier_*_activation_threshold`.

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| structure: `structural_complexity_override` | `scaffolding_tier` | display: `scaffolding_tier_*_activation_threshold` |

OR:

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| display: `scaffolding_tier_lightweight_activation_threshold` | `structural_complexity_lightweight_threshold` | structure: `structural_complexity_override` |
| display: `scaffolding_tier_standard_activation_threshold` | `structural_complexity_standard_threshold` | structure: `structural_complexity_override` |

**Recommendation:** Rename structure field to `scaffolding_tier` — shorter, and `scaffolding_tier` is the more descriptive name for what it does.

**Cascade:** Verdandi YAML → schemas → gates → Galdr models + `extracted/structure.toml`

---

## Issues to Decide (Not Renames)

### `role_responsibility` Scalar-vs-List Anomaly

`role_responsibility` is typed as a single `RoleResponsibility` (StringProse) — a scalar. But display has `responsibility_format` with threshold-based switching, which only makes sense for lists.

**Options:**
1. Make `responsibility` a list type in verdandi (allows multiple responsibility statements)
2. Remove `responsibility_format` and `responsibility_format_threshold` from display (accept it's always scalar)
3. Keep both — the engine renders a single-item list using the format (works but odd)

**Recommendation:** Decide based on whether agents will ever have multiple responsibility statements. If yes, make it a list. If no, remove the display format fields.

### Input Section — No Content/Structure/Display Models

The `input` section exists in the data model but has no content, structure, or display counterpart. It doesn't participate in the composition pipeline.

**Options:**
1. Add input to all three output schemas (full composition pipeline participation)
2. Keep input as a data-only section with hardcoded rendering (simpler but inconsistent)
3. Defer — handle after the engine works for the other 12 sections

**Recommendation:** Option 3. Get the engine working first. Input can be added later.

### Content Fields Missing `_visible` Toggles

8 content fields have no corresponding structure `_visible` toggle:

| Section | Content Field | Always Renders? |
|---------|--------------|----------------|
| identity | `declaration_heuristic_postscript` | Currently yes |
| constraints | `hierarchy_tier_comparison` | Currently yes |
| constraints | `hierarchy_three_tier_explanation` | Currently yes |
| failure_criteria | `any_one_triggers_abort` | Currently yes |
| return_format | `report_completion_label` | Currently yes |
| return_format | `token_must_be_first_word_tokens_three` | Data-gated (3 tokens) |
| return_format | `token_must_be_first_word_tokens_two` | Data-gated (2 tokens) |
| examples | `group_framing_sentence` | Has toggle ✓ (was missing from count) |

**Recommendation:** Add `_visible` toggles for the first 5. The token fields are data-gated (mutually exclusive based on whether ABORT is a valid token), not visibility-toggled. Defer or handle as part of the input section work.

---

## Implementation Order

**All groups are verdandi agent-output only.** No agent-builder changes. No pipeline cascade. No agent definition TOML changes.

Groups 1-6 can be done in any order or all at once — they're all in the same verdandi project (agent-output YAML sources).

After all verdandi changes: Draupnir (agent-output schemas) → Nornir output gates → Galdr `generate_structures.py` → update `extracted/*.toml` files.

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
