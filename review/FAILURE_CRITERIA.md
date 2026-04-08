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
| ✅ | 1 | `heading` | StringText | `heading` | heading | `"Abort Conditions"` |
| ✅ | 2 | `any_one_triggers_abort_preamble` | StringProse | `_preamble` | preamble | `"Any ONE of the following failure modes is sufficient to trigger abort."` |
| ✅ | 3 | `abort_stance_preamble_p_variant` | BaseModel | `_p_variant` | preamble | `{obligation: "The following conditions make valid output impossible...", permission: "Not every task can be completed..."}` |
| ✅ | 4 | `evidence_intro` | StringProse | `_intro` | body | `"Any of the following indicates this failure — one signal is sufficient:"` |
| ✅ | 5 | `abort_stance_definition_label_b_variant` | BaseModel | `_b_variant` | body | `{obligation: "Halt condition:", permission: "This work cannot succeed when:"}` |
| ✅ | 6 | `cite_definition_and_evidence_postscript` | StringProse | `_postscript` | body | `"Each failure mode has a definition (what went wrong) and evidence (how you detect it)..."` |
| ✅ | 7 | `check_before_and_during_postscript` | StringProse | `_postscript` | body | `"Check what you can before starting. Monitor the rest throughout."` |

## Structure (FailureCriteriaStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ⚠️ | 3 | `abort_stance_preamble_visible` | Boolean | `true` | → content #3 — not wired to variant |
| ✅ | 4 | `cite_definition_and_evidence_postscript_visible` | Boolean | `false` | → content #6 |
| ✅ | 5 | `check_before_and_during_postscript_visible` | Boolean | `false` | → content #7 |
| ✅ | 6 | `abort_stance_preamble_p_variant` | FailureCriteriaAbortStanceVariant | `"obligation"` | → selects key in content #3 |
| ✅ | 7 | `abort_stance_definition_label_b_variant` | FailureCriteriaAbortStanceVariant | `"obligation"` | → selects key in content #5 |

## Display (FailureCriteriaDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `evidence_format` | ListFormat | `"bare"` | evidence list rendering style — not wired |

---

## Rendering Order

```
HEADING:
  ✅ heading                               "Abort Conditions"

PREAMBLE:
  ✅ any_one_triggers_abort_preamble       "Any ONE of the following failure modes is sufficient to trigger abort."
                                             [visible: implicit — always visible, no toggle]
  ⚠️ abort_stance_preamble_p_variant       {variant: "obligation" → "The following conditions make valid output impossible..."}
                                             [visible: abort_stance_preamble_visible = true — not wired to variant]

BODY:
  For each FailureItem:
    .failure_definition                    → scalar string (FailureDefinition)
    .failure_evidence                      → list of StringProse scalars

    ⚠️ abort_stance_definition_label_b_variant  {variant: "obligation" → "Halt condition:"}
                                             label before failure_definition — per-item decoration, not wired
    evidence_intro                         "Any of the following indicates this failure — one signal is sufficient:"
                                             [visible: implicit — renders per-item before evidence list]
    ⚠️ evidence list                       renders failure_evidence items
                                             [display: evidence_format = "bare" — not wired]

  cite_definition_and_evidence_postscript  "Each failure mode has a definition..."
                                             [visible: cite_definition_and_evidence_postscript_visible = false]
  check_before_and_during_postscript       "Check what you can before starting..."
                                             [visible: check_before_and_during_postscript_visible = false]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: Per-item `_b_variant` label not wired for per-item rendering

`abort_stance_definition_label_b_variant` is a body-slot variant table that provides the label rendered before each `failure_definition`. It is correctly classified by suffix (`_b_variant`) but the engine does not apply it as a per-item decoration template. Requires a per-item decoration mechanism in the composition engine.

### ⚠️ ISSUE 2: `abort_stance_preamble_visible` not connected to variant selector

`abort_stance_preamble_visible` (Boolean gate) and `abort_stance_preamble_p_variant` (variant key) are separate but both must be consulted together: check visibility, then select variant. Currently not wired.

### ⚠️ ISSUE 3: `evidence_format = "bare"` not wired

Display control for evidence list format (`"bare"`) is not read by the engine. Items render with hardcoded bullet formatting.

### ⚠️ ISSUE 4: `evidence_intro` placement is per-item, not section-level

`evidence_intro` has `_intro` suffix — classified as body slot. But it renders once per failure item, before that item's evidence list, not once per section. The engine renders body-slot content once. If multiple failure items exist, the intro would be misplaced.

### ⚠️ ISSUE 5: `section_visible` master toggle not checked by engine

Same as other sections — section-skip decision not implemented at orchestrate level.

---

## Renames Needed

No scalar content fields contain `{{placeholders}}` and no trunk mismatches exist. Variant tables (`abort_stance_preamble_p_variant`, `abort_stance_definition_label_b_variant`) contain only plain prose alternatives — no `_template` suffix needed.

### Variant naming (`_variant` as modifier, `_selector` in structure)

Content: drop slot letter from `_x_variant` — the positional suffix before `_variant` determines the slot.

- `abort_stance_preamble_p_variant` → `abort_stance_preamble_variant` — drop `_p`; slot determined by `_preamble`
- `abort_stance_definition_label_b_variant` → `abort_stance_definition_label_variant` — drop `_b`; slot determined by `_label`

Structure: the two abort_stance variants switch together (both driven by the same `obligation`/`permission` choice). Replace the two per-slot selectors with a single shared selector.

- Remove `abort_stance_preamble_p_variant` (selector for preamble slot)
- Remove `abort_stance_definition_label_b_variant` (selector for label slot)
- Add `abort_stance_selector` — single selector drives both content fields; default value `"obligation"`
