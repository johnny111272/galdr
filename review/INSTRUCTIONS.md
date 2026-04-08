# Instructions Section — Four-Axis Review

## Data (Instructions)

```
Instructions
  └─ steps: list of InstructionStep
       .instruction_mode    InstructionMode (enum: deterministic/probabilistic)
       .instruction_text    StringMarkdown (scalar)
```

Agent-builder has 7 steps. Modes vary per step (mixed).

## Content (InstructionsContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `heading_variant_template` | BaseModel | `_variant_template` | heading | `{default: "Instructions", procedure: "Procedure", steps_with_count: "Steps ({{step_count}} total)"}` |
| ✅ | 2 | `step_count_preamble_template` | StringTemplate | `_preamble_template` | preamble | `"You will execute {{step_count}} steps."` |
| ✅ | 3 | `no_add_skip_reorder_preamble` | StringProse | `_preamble` | preamble | `"Do not add steps. Do not skip steps. Do not reorder steps."` |
| ✅ | 4 | `instruction_mode_preview_preamble` | StringProse | `_preamble` | preamble | `"Steps marked (exact) leave no room for interpretation..."` |
| ✅ | 5 | `no_extra_operations_preamble` | StringProse | `_preamble` | preamble | `"Each instruction step is a complete specification..."` |
| ✅ | 6 | `instruction_mode_explanation_preamble_variant` | BaseModel | `_preamble_variant` | preamble | `{mixed: "...", uniform_deterministic: "...", uniform_probabilistic: "..."}` |
| ✅ | 7 | `step_done_when_postscript_template` | StringTemplate | `_postscript_template` | body | `"Done when: {{completion_condition}}"` |
| ✅ | 8 | `cross_step_dependency_label_template` | StringTemplate | `_label_template` | body | `"Uses output from: {{dependency_steps}}"` |
| ✅ | 9 | `reminder_midpoint_preamble_template` | StringTemplate | `_preamble_template` | preamble | `"You are past the halfway point. Steps 1-{{midpoint}} established the foundation..."` |
| ✅ | 10 | `guardrail_closing_template` | StringTemplate | `_closing_template` | closing | `"These {{step_count}} steps constitute your complete task. Do not add additional steps."` |
| ✅ | 11 | `instruction_mode_recap_closing_template` | StringTemplate | `_closing_template` | closing | `"{{mode_recap_text}} There are no other steps."` |
| ✅ | 12 | `instruction_mode` | BaseModel (D1 table) | sub-table | body | `{header: {deterministic: "...", probabilistic: "..."}, header_n_only: {...}, body_prefix: {...}, signal_at_mode_change: {...}}` |

## Structure (InstructionsStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `heading_selector` | InstructionsHeadingSelector | `"default"` | → content #1 variant key |
| ⚠️ | 2 | `instruction_mode_explanation_visible` | VisibilityMode | `"auto"` | → content #6 (auto = render when mixed modes) — not implemented |
| ⚠️ | 3 | `instruction_mode_marker_placement` | InstructionsInstructionModeMarkerPlacement | `"header_fused"` | how mode tags appear per-step — not implemented |
| ⚠️ | 4 | `signal_at_mode_change_visible` | Boolean | `false` | → `instruction_mode.signal_at_mode_change` — not implemented |
| ✅ | 5 | `step_count_preamble_template_visible` | Boolean | `true` | → content #2 |
| ✅ | 6 | `no_add_skip_reorder_preamble_visible` | Boolean | `true` | → content #3 |
| ✅ | 7 | `instruction_mode_preview_preamble_visible` | Boolean | `true` | → content #4 |
| ✅ | 8 | `no_extra_operations_preamble_visible` | Boolean | `true` | → content #5 |
| ⚠️ | 9 | `step_index_tracking` | InstructionsStepIndexTracking | `"n_of_m"` | `n_only` vs `n_of_m` in step headers — not implemented |
| ✅ | 10 | `step_done_when_postscript_template_visible` | Boolean | `false` | → content #7 |
| ✅ | 11 | `guardrail_closing_template_visible` | Boolean | `true` | → content #10 |
| ✅ | 12 | `instruction_mode_recap_closing_template_visible` | Boolean | `false` | → content #11 |
| ✅ | 13 | `cross_step_dependency_label_template_visible` | Boolean | `false` | → content #8 |
| ✅ | 14 | `reminder_midpoint_preamble_template_visible` | Boolean | `false` | → content #9 |
| ⚠️ | 15 | `scaffolding_tier_override` | InstructionsScaffoldingTierOverride | `"auto"` | tier selection — not implemented |

## Display (InstructionsDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `step_header_format` | HeadingFormat | `"bold"` | bold vs H3 for step headers — not wired |
| ⚠️ | 2 | `step_body_container` | BodyContainer | `"none"` | none vs blockquote for step bodies — not wired |
| ⚠️ | 3 | `scaffolding_tier_lightweight_activation_threshold` | Integer | `3` | tier threshold — not wired |
| ⚠️ | 4 | `scaffolding_tier_standard_activation_threshold` | Integer | `7` | tier threshold — not wired |
| ⚠️ | 5 | `instruction_mode_recap_format` | InstructionsInstructionModeRecapFormat | `"prose"` | prose vs tabular recap — not wired |

---

## Rendering Order

```
HEADING:
  ✅ heading_variant_template               {selected by heading_selector = "default" → "Instructions"}

PREAMBLE:
  ✅ step_count_preamble_template           "You will execute {{step_count}} steps."
                                             [visible: step_count_preamble_template_visible = true]
  ✅ no_add_skip_reorder_preamble          "Do not add steps. Do not skip steps. Do not reorder steps."
                                             [visible: no_add_skip_reorder_preamble_visible = true]
  ✅ instruction_mode_preview_preamble     "Steps marked (exact) leave no room for interpretation..."
                                             [visible: instruction_mode_preview_preamble_visible = true]
  ✅ no_extra_operations_preamble          "Each instruction step is a complete specification..."
                                             [visible: no_extra_operations_preamble_visible = true]
  ⚠️ instruction_mode_explanation_preamble_variant  {variant selected by mode mix}
                                             [visible: instruction_mode_explanation_visible = "auto" — not implemented]
  ✅ reminder_midpoint_preamble_template   "You are past the halfway point. Steps 1-{{midpoint}}..."
                                             [visible: reminder_midpoint_preamble_template_visible = false]

BODY:
  For each InstructionStep:
    .instruction_mode                      → GATE: controls step header variant
    .instruction_text                      → render as markdown prose

    ⚠️ step header                         "**Step N of M (exact/judgment).**"
                                             [step_index_tracking = "n_of_m", instruction_mode_marker_placement = "header_fused"]
                                             [display: step_header_format = "bold"]
                                             [display: step_body_container = "none"]

  ✅ instruction_mode                      D1 table — step header templates (sub-table, no positional suffix)

  step_done_when_postscript_template       "Done when: {{completion_condition}}"
                                             [visible: step_done_when_postscript_template_visible = false]
  cross_step_dependency_label_template     "Uses output from: {{dependency_steps}}"
                                             [visible: cross_step_dependency_label_template_visible = false]

CLOSING:
  ✅ guardrail_closing_template            "These {{step_count}} steps constitute your complete task..."
                                             [visible: guardrail_closing_template_visible = true]
  ✅ instruction_mode_recap_closing_template  "{{mode_recap_text}} There are no other steps."
                                             [visible: instruction_mode_recap_closing_template_visible = false]
```

---

## Issues

### ⚠️ ISSUE 1: `instruction_mode` content table is a D1 sub-table — special handling needed

The `[instructions.instruction_mode]` TOML block is a D1 dispatch table — it holds per-mode step header templates (`header`, `header_n_only`, `body_prefix`, `signal_at_mode_change`). It has no positional suffix because it drives per-step rendering logic, not section-level content slots. Requires special handling in the composition engine (per-item decoration lookup).

### ⚠️ ISSUE 2: Per-step mode rendering entirely unimplemented

Step header format (`instruction_mode_marker_placement`, `step_index_tracking`, `step_header_format`, `step_body_container`) all control per-step rendering. The engine currently has no per-item decoration mechanism. This is the core of the instructions section and is not yet built.

### ⚠️ ISSUE 3: `instruction_mode_explanation_visible = "auto"` not implemented

The `"auto"` mode should render the explanation only when step modes are mixed. Requires inspecting the steps list. Not implemented.

### ⚠️ ISSUE 4: `scaffolding_tier_override` and display thresholds not wired

Scaffolding tier affects which preamble components render based on step count. Structure and display thresholds exist but are not read by the engine.
