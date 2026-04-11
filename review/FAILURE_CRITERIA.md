# Failure Criteria Section — Four-Axis Review

## Data (FailureCriteria)

```
FailureCriteria
  └─ criteria: list of FailureItem
       .failure_definition    FailureDefinition (scalar)
       .failure_evidence      list of StringProse (scalar list)
```

Agent-builder has 1 FailureItem. Each item has a definition string and a list of evidence strings.

## Content (FailureCriteriaContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"Abort Conditions"` |
| ✅ | 2 | `any_one_triggers_abort_preamble` | StringProse | `_preamble` | preamble | `"Any ONE of the following failure modes is sufficient to trigger abort."` |
| ✅ | 3 | `abort_stance_preamble_variant` | BaseModel | `_preamble_variant` | preamble | `{obligation: "The following conditions make valid output impossible...", permission: "Not every task can be completed..."}` |
| ✅ | 4 | `evidence_intro` | StringProse | `_intro` | body | `"Any of the following indicates this failure — one signal is sufficient:"` |
| ✅ | 5 | `abort_stance_definition_label_variant` | BaseModel | `_label_variant` | body | `{obligation: "Halt condition:", permission: "This work cannot succeed when:"}` |
| ✅ | 6 | `cite_definition_and_evidence_postscript` | StringProse | `_postscript` | body | `"Each failure mode has a definition (what went wrong) and evidence (how you detect it)..."` |
| ✅ | 7 | `check_before_and_during_postscript` | StringProse | `_postscript` | body | `"Check what you can before starting. Monitor the rest throughout."` |

## Structure (FailureCriteriaStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `pre_section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `pre_max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ⚠️ | 3 | `abort_stance_preamble_visible` | Boolean | `true` | → content #3 — not wired to variant |
| ✅ | 4 | `cite_definition_and_evidence_postscript_visible` | Boolean | `false` | → content #6 |
| ✅ | 5 | `check_before_and_during_postscript_visible` | Boolean | `false` | → content #7 |
| ✅ | 6 | `abort_stance_selector` | FailureCriteriaAbortStanceVariant | `"obligation"` | → selects key in content #3 and content #5 |

## Display (FailureCriteriaDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `criteria_evidence_format` | ListFormat | `"bare"` | evidence list rendering style — not wired |
| ⚠️ | 2 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 3 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Abort Conditions"

PREAMBLE:
  ✅ any_one_triggers_abort_preamble       "Any ONE of the following failure modes is sufficient to trigger abort."
                                             [visible: implicit — always visible, no toggle]
  ⚠️ abort_stance_preamble_variant         {selector: "obligation" → "The following conditions make valid output impossible..."}
                                             [visible: abort_stance_preamble_visible = true — not wired to variant]

BODY:
  For each FailureItem:
    .failure_definition                    → scalar string (FailureDefinition)
    .failure_evidence                      → list of StringProse scalars

    ⚠️ abort_stance_definition_label_variant  {selector: "obligation" → "Halt condition:"}
                                             label before failure_definition — per-item decoration, not wired
    evidence_intro                         "Any of the following indicates this failure — one signal is sufficient:"
                                             [visible: implicit — renders per-item before evidence list]
    ⚠️ evidence list                       renders failure_evidence items
                                             [display: criteria_evidence_format = "bare" — not wired]

  cite_definition_and_evidence_postscript  "Each failure mode has a definition..."
                                             [visible: cite_definition_and_evidence_postscript_visible = false]
  check_before_and_during_postscript       "Check what you can before starting..."
                                             [visible: check_before_and_during_postscript_visible = false]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: Per-item label variant not wired for per-item rendering

`abort_stance_definition_label_variant` is a body-slot variant table that provides the label rendered before each `failure_definition`. It is correctly classified by suffix (`_label_variant`) but the engine does not apply it as a per-item decoration template. Requires a per-item decoration mechanism in the composition engine.

### ⚠️ ISSUE 2: `abort_stance_preamble_visible` not connected to variant selector

`abort_stance_preamble_visible` (Boolean gate) and `abort_stance_selector` (variant key) are separate but both must be consulted together: check visibility, then select variant. Currently not wired.

### ⚠️ ISSUE 3: `criteria_evidence_format = "bare"` not wired

Display control for evidence list format (`"bare"`) is not read by the engine. Items render with hardcoded bullet formatting.

### ⚠️ ISSUE 4: `evidence_intro` placement is per-item, not section-level

`evidence_intro` has `_intro` suffix — classified as body slot. But it renders once per failure item, before that item's evidence list, not once per section. The engine renders body-slot content once. If multiple failure items exist, the intro would be misplaced.

### ⚠️ ISSUE 5: `pre_section_visible` master toggle not checked by engine

Same as other sections — section-skip decision not implemented at orchestrate level.
