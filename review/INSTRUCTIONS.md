# Instructions Section — Four-Axis Review

## Data (Instructions)

```
Instructions
  steps: list of InstructionStep
    .instruction_mode    InstructionMode (enum: deterministic/probabilistic)
    .instruction_text    StringMarkdown (scalar)
```

Agent-builder has 7 steps. Modes vary per step (mixed).

## Content (InstructionsContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `heading_variant_template` | BaseModel | `_variant_template` | heading | `{default: "Instructions", procedure: "Procedure", steps_with_count: "Steps ({{step_count}} total)"}` |
| ✅ | 2 | `highlight_step_count_preamble_template` | StringTemplate | `_preamble_template` | preamble | `"You will execute {{step_count}} steps."` |
| ✅ | 3 | `sequence_integrity_preamble` | StringProse | `_preamble` | preamble | `"Do not add steps. Do not skip steps. Do not reorder steps."` |
| ✅ | 4 | `follow_strictly_preamble` | StringProse | `_preamble` | preamble | `"Each instruction step is a complete specification..."` |
| ✅ | 6 | `instruction_mode_explanation_preamble_variant` | BaseModel | `_preamble_variant` | preamble | `{mixed: "...", uniform_deterministic: "...", uniform_probabilistic: "..."}` |
| ✅ | 7 | `reminder_midpoint_preamble_template` | StringTemplate | `_preamble_template` | preamble | `"You are past the halfway point..."` |
| ✅ | 8 | `step_header_template` | StringTemplate | `_template` | body | `"Step {{step_n}} of {{step_total}}."` |
| ✅ | 9 | `step_header_n_only_template` | StringTemplate | `_template` | body | `"Step {{step_n}}."` |
| ✅ | 10 | `step_mode_label_variant` | BaseModel | `_variant` | body | `{deterministic: "**EXACT**", probabilistic: "**JUDGMENT**"}` |
| ✅ | 11 | `step_done_when_postscript_template` | StringTemplate | `_postscript_template` | body | `"Done when: {{completion_condition}}"` |
| ✅ | 12 | `cross_step_dependency_label_template` | StringTemplate | `_label_template` | body | `"Uses output from: {{dependency_steps}}"` |
| ✅ | 13 | `follow_strictly_closing_template` | StringTemplate | `_closing_template` | closing | `"These {{step_count}} steps constitute your complete task. Do not add additional steps."` |
| ✅ | 14 | `instruction_mode_recap_closing_template` | StringTemplate | `_closing_template` | closing | `"{{mode_recap_text}} There are no other steps."` |

## Structure (InstructionsStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `heading_selector` | InstructionsHeadingSelector (enum) | `"default"` | → selects key in content #1 |
| ✅ | 2 | `instruction_mode_explanation_preamble_visible` | VisibilityMode | `"auto"` | → content #6 (auto = render when mixed modes) |
| ✅ | 3 | `highlight_step_count_preamble_template_visible` | Boolean | `true` | → content #2 |
| ✅ | 4 | `sequence_integrity_preamble_visible` | Boolean | `true` | → content #3 |
| ✅ | 5 | `follow_strictly_preamble_visible` | Boolean | `true` | → content #5 |
| ✅ | 6 | `step_index_tracking` | InstructionsStepIndexTracking (enum) | `"n_of_m"` | Selects `step_header_template` vs `step_header_n_only_template` |
| ✅ | 7 | `step_done_when_postscript_template_visible` | Boolean | `false` | → content #11 |
| ✅ | 8 | `follow_strictly_closing_template_visible` | Boolean | `true` | → content #13 |
| ✅ | 9 | `instruction_mode_recap_closing_template_visible` | Boolean | `false` | → content #14 |
| ✅ | 10 | `cross_step_dependency_label_template_visible` | Boolean | `false` | → content #12 |
| ✅ | 11 | `reminder_midpoint_preamble_template_visible` | Boolean | `false` | → content #7 |
| ⚠️ | 12 | `scaffolding_tier_override` | InstructionsScaffoldingTierOverride | `"auto"` | Meta-policy that computes visibility toggles from step count |

## Display (InstructionsDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `step_header_format` | HeadingFormat | `"bold"` | Step headers as bold/h3/h4 |
| ✅ | 2 | `step_body_container` | BodyContainer | `"none"` | Step body wrapping (none/blockquote) |
| ✅ | 3 | `step_mode_separator` | InlineSeparator (enum) | `"dash"` | Separator between mode label and step header (dash/colon/pipe/newline) |
| ✅ | 4 | `instruction_mode_restrict_to_transition` | Boolean | `false` | When true, suppress mode labels on consecutive same-mode steps |
| ⚠️ | 5 | `scaffolding_tier_lightweight_activation_threshold` | Integer | `3` | Step count threshold for lightweight tier |
| ⚠️ | 6 | `scaffolding_tier_standard_activation_threshold` | Integer | `7` | Step count threshold for standard tier |
| ✅ | 7 | `instruction_mode_recap_format` | InstructionModeRecapFormat | `"prose"` | Recap as prose/tabular |

---

## Rendering Order

```
HEADING:
  ✅ heading_variant_template               selected by heading_selector = "default" → "Instructions"

PREAMBLE:
  ✅ highlight_step_count_preamble_template "You will execute {{step_count}} steps."
                                             [visible: highlight_step_count_preamble_template_visible = true]
  ✅ sequence_integrity_preamble            "Do not add steps. Do not skip steps. Do not reorder steps."
                                             [visible: sequence_integrity_preamble_visible = true]
  ✅ follow_strictly_preamble              "Each instruction step is a complete specification..."
                                             [visible: follow_strictly_preamble_visible = true]
  ⚠️ instruction_mode_explanation_preamble_variant
                                             {selected by data condition: mixed/uniform modes}
                                             [visible: instruction_mode_explanation_preamble_visible = "auto"]
  ✅ reminder_midpoint_preamble_template   "You are past the halfway point..."
                                             [visible: reminder_midpoint_preamble_template_visible = false]

BODY:
  For each InstructionStep:
    MODE LABEL:  step_mode_label_variant     selected by step's instruction_mode enum
                                             [display: step_mode_separator = "dash"]
                                             [display: instruction_mode_restrict_to_transition = false]
    STEP HEADER: step_header_template        "Step {{step_n}} of {{step_total}}."
                                             [structure: step_index_tracking = "n_of_m"]
                                             [display: step_header_format = "bold"]
    STEP BODY:   instruction_text            rendered as markdown prose
                                             [display: step_body_container = "none"]

  step_done_when_postscript_template       "Done when: {{completion_condition}}"
                                             [visible: step_done_when_postscript_template_visible = false]
  cross_step_dependency_label_template     "Uses output from: {{dependency_steps}}"
                                             [visible: cross_step_dependency_label_template_visible = false]

CLOSING:
  ✅ follow_strictly_closing_template      "These {{step_count}} steps constitute your complete task..."
                                             [visible: follow_strictly_closing_template_visible = true]
  ✅ instruction_mode_recap_closing_template  "{{mode_recap_text}} There are no other steps."
                                             [visible: instruction_mode_recap_closing_template_visible = false]
```

---

## Issues

### ⚠️ ISSUE 1: `instruction_mode_explanation_preamble_variant` has no structure selector

Its variant key is computed from data (what modes are present in the steps), not from a structure selector. The engine needs to inspect the steps list to determine `mixed` vs `uniform_deterministic` vs `uniform_probabilistic`. No `_selector` field exists.

### ⚠️ ISSUE 2: `scaffolding_tier_override` is a meta-policy

A meta-control that computes which visibility toggles should be active based on step count and thresholds. Not directly processable by the generic engine — may need pre-processing that resolves the tier into individual toggle values before the engine runs.

### ⚠️ ISSUE 3: `step_index_tracking` selects between templates by non-matching names

`"n_of_m"` → use `step_header_template`, `"n_only"` → use `step_header_n_only_template`. The enum values don't match the content field names. The engine needs a mapping.

### ⚠️ ISSUE 4: Computed placeholders

`{{step_count}}`, `{{step_n}}`, `{{step_total}}`, `{{midpoint}}`, `{{completion_condition}}`, `{{dependency_steps}}`, `{{mode_recap_text}}` are all computed values, not data fields. The engine needs to generate these before interpolation.
