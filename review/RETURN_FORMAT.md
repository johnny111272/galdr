# Return Format Section — Four-Axis Review

## Data (ReturnFormat)

```
ReturnFormat
  .mode                  ReturnMode (enum/gate)
  .return_schema         PathExistsAbsolute (scalar, optional)
  .status_instruction    StringProse (scalar, optional)
  .metrics_instruction   StringProse (scalar, optional)
  .output_instruction    StringProse (scalar, optional)
```

Agent-builder: `mode = "status"`, `status_instruction` present (return SUCCESS with agent name, step count, include file count). `return_schema`, `metrics_instruction`, `output_instruction` absent.

## Content (ReturnFormatContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"Return Protocol"` |
| ✅ | 2 | `files_vs_status_explanation_preamble` | StringProse | `_preamble` | preamble | `"Your return mode is status. Your work products go to files. Your return goes to the dispatcher as a brief status signal — not the deliverable."` |
| ✅ | 3 | `token_must_be_first_word_preamble` | StringProse | `_preamble` | preamble | `"Your return must begin with a protocol token. The dispatch layer parses this token programmatically. Do not paraphrase or embed in prose — it must appear as the first word."` |
| ✅ | 4 | `token_must_be_first_word_tokens_three_preamble` | StringProse | `_preamble` | preamble | `"Three terminal states: SUCCESS, FAILURE, or ABORT."` |
| ✅ | 5 | `token_must_be_first_word_tokens_two_preamble` | StringProse | `_preamble` | preamble | `"Two terminal states: SUCCESS or FAILURE."` |
| ✅ | 6 | `abort_vs_failure_distinction_preamble` | StringProse | `_preamble` | preamble | `"ABORT means you determined the work should not be attempted — inputs insufficient, prerequisites missing..."` |
| ✅ | 7 | `honest_failure_over_dubious_success_preamble` | StringProse | `_preamble` | preamble | `"An honest FAILURE is better than a dubious SUCCESS. If your work did not meet success conditions, return FAILURE..."` |
| ✅ | 8 | `failure_cross_reference_preamble` | StringProse | `_preamble` | preamble | `"The conditions for failure are defined in your failure criteria. Here, you learn how to report failure to the dispatcher."` |
| ✅ | 9 | `report_completion_label` | StringText | `_label` | body | `"Report your completion as follows:"` |
| ✅ | 10 | `report_all_metrics_postscript` | StringProse | `_postscript` | body | `"Report all metrics specified for your return state. The dispatcher and downstream processes depend on these values being present."` |
| ✅ | 11 | `track_metrics_as_you_work_postscript` | StringProse | `_postscript` | body | `"Your return requirements imply tracking requirements. If you must report a count, maintain that count as you work..."` |
| ✅ | 12 | `track_metrics_as_you_work_antidrift_postscript` | StringProse | `_postscript` | body | `"The dispatcher is waiting for your return signal. When you reach a terminal state, report it immediately..."` |
| ✅ | 13 | `do_not_fabricate_metrics_postscript` | StringProse | `_postscript` | body | `"Report actual metrics from your execution. Do not fabricate values to match the expected format."` |

## Structure (ReturnFormatStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `files_vs_status_explanation_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 2 | `token_must_be_first_word_preamble_visible` | Boolean | `true` | → content #3 |
| ✅ | 3 | `report_all_metrics_postscript_visible` | Boolean | `true` | → content #10 |
| ✅ | 4 | `abort_vs_failure_distinction_preamble_visible` | Boolean | `true` | → content #6 |
| ✅ | 5 | `honest_failure_over_dubious_success_preamble_visible` | Boolean | `true` | → content #7 |
| ✅ | 6 | `track_metrics_as_you_work_postscript_visible` | Boolean | `true` | → content #11 |
| ✅ | 7 | `do_not_fabricate_metrics_postscript_visible` | Boolean | `true` | → content #13 |
| ✅ | 8 | `failure_cross_reference_preamble_visible` | Boolean | `false` | → content #8 |

## Display (ReturnFormatDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 2 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Return Protocol"

PREAMBLE:
  ✅ files_vs_status_explanation_preamble  "Your return mode is status. Your work products go to files..."
                                             [visible: files_vs_status_explanation_preamble_visible = true]
  ✅ token_must_be_first_word_preamble     "Your return must begin with a protocol token..."
                                             [visible: token_must_be_first_word_preamble_visible = true]

  ⚠️ token_must_be_first_word_tokens_three_preamble  "Three terminal states: SUCCESS, FAILURE, or ABORT."
  ⚠️ token_must_be_first_word_tokens_two_preamble    "Two terminal states: SUCCESS or FAILURE."
                                             [gate: mode drives which one renders — ABORT available or not]
                                             [both classified as _preamble — engine renders both, should render only one]

  ✅ abort_vs_failure_distinction_preamble "ABORT means you determined the work should not be attempted..."
                                             [visible: abort_vs_failure_distinction_preamble_visible = true]
  ✅ honest_failure_over_dubious_success_preamble  "An honest FAILURE is better than a dubious SUCCESS..."
                                             [visible: honest_failure_over_dubious_success_preamble_visible = true]
  ✅ failure_cross_reference_preamble      "The conditions for failure are defined in your failure criteria..."
                                             [visible: failure_cross_reference_preamble_visible = false]

BODY:
  [GATE] mode                              → GATE: drives token count content selection and return block format
  ✅ report_completion_label               "Report your completion as follows:"

  ❌ return_schema                         PathExistsAbsolute scalar — no content template
  ❌ status_instruction                    StringProse scalar — the actual per-agent return instruction
                                             most important field in this section; no content template renders it
  ❌ metrics_instruction                   StringProse scalar — no content template
  ❌ output_instruction                    StringProse scalar — no content template

  ✅ report_all_metrics_postscript         "Report all metrics specified for your return state..."
                                             [visible: report_all_metrics_postscript_visible = true]
  ✅ track_metrics_as_you_work_postscript  "Your return requirements imply tracking requirements..."
                                             [visible: track_metrics_as_you_work_postscript_visible = true]
  ✅ track_metrics_as_you_work_antidrift_postscript  "The dispatcher is waiting for your return signal..."
                                             [visible: implicit — no structure toggle, always renders when reached]
  ✅ do_not_fabricate_metrics_postscript   "Report actual metrics from your execution..."
                                             [visible: do_not_fabricate_metrics_postscript_visible = true]

CLOSING:
  (none)
```

---

## Issues

### ❌ ISSUE 1: `status_instruction`, `metrics_instruction`, `output_instruction` have no content templates

The per-agent return instructions are the most critical content in this section — they tell the agent exactly what to return. For agent-builder, `status_instruction` contains specific metric reporting requirements. There is no content template to render any of these scalar fields.

**Fix required:** A passthrough content field (e.g., `status_instruction_body`) or direct passthrough mechanism for scalar string fields that are already formatted prose.

### ❌ ISSUE 2: `return_schema` has no content template

`return_schema` is an optional path scalar. When present, it should render as a schema reference label. No content template exists.

**Fix required:** A schema reference content field similar to `schema_reference_label_template` in the output section.

### ⚠️ ISSUE 3: Two mutually exclusive `_preamble` token-count fields both render

`token_must_be_first_word_tokens_three_preamble` and `token_must_be_first_word_tokens_two_preamble` are both in the preamble slot. Only one should render based on whether ABORT is a valid return state (driven by `mode` or another gate). Engine currently has no mechanism to select between two content fields in the same slot based on a gate value — both would render.

**Fix required:** Either (a) structure visibility toggles for each (`tokens_three_visible`, `tokens_two_visible`) with agent-specific values, or (b) merge into a single `_preamble_variant` table keyed on mode.

### ⚠️ ISSUE 4: `track_metrics_as_you_work_antidrift_postscript` has no structure toggle

Unlike all other postscripts in this section, `track_metrics_as_you_work_antidrift_postscript` has no corresponding structure visibility toggle. It will always render when reached. Inconsistent with the pattern of the rest of the section.
