# Success Criteria Section — Four-Axis Review

## Data (SuccessCriteria)

```
SuccessCriteria
  └─ criteria: list of SuccessItem
       .success_definition    SuccessDefinition (scalar)
       .success_evidence      list of StringProse (scalar list)
```

Agent-builder has 1 SuccessItem. Each item has a definition string and a list of evidence strings.

## Content (SuccessCriteriaContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `heading` | StringText | `heading` | heading | `"Success Criteria"` |
| ✅ | 2 | `criteria_separator` | TitleString | `_separator` | body | `"Additionally"` |
| ✅ | 3 | `verification_guidance_postscript` | StringProse | `_postscript` | body | `"Some conditions above are mechanically verifiable; others require your judgment..."` |
| ✅ | 4 | `success_failure_independence_statement_postscript` | StringProse | `_postscript` | body | `"Success criteria define quality. Failure criteria define breakage. These are independent evaluations."` |
| ✅ | 5 | `definition_framing_b_variant` | BaseModel | `_b_variant` | body | `{declarative_assertion: "{{DEFINITION}}", conditional_gate: "...", completion_identity: "..."}` |
| ✅ | 6 | `evidence_framing_b_variant` | BaseModel | `_b_variant` | body | `{properties: "A successful output has these properties:", verification_checklist: "...", quality_signals: "..."}` |
| ✅ | 7 | `definition_to_evidence_transition_b_variant` | BaseModel | `_b_variant` | body | `{goal_then_criteria: "Meeting this standard means:", proof: "...", dual_presentation: "..."}` |

## Structure (SuccessCriteriaStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ✅ | 3 | `definition_framing_b_variant` | SuccessCriteriaDefinitionFramingBVariant | `"declarative_assertion"` | → selects key in content #5 |
| ✅ | 4 | `evidence_framing_b_variant` | SuccessCriteriaEvidenceFramingBVariant | `"properties"` | → selects key in content #6 |
| ✅ | 5 | `definition_to_evidence_transition_b_variant` | SuccessCriteriaDefinitionToEvidenceTransitionBVariant | `"goal_then_criteria"` | → selects key in content #7 |
| ⚠️ | 6 | `evidence_type_handling` | SuccessCriteriaEvidenceTypeHandling | `"undifferentiated"` | per-item evidence classification — not implemented |
| ⚠️ | 7 | `output_vs_agent_voice` | SuccessCriteriaOutputVsAgentVoice | `"output_centric"` | voice paradigm — not implemented |
| ✅ | 8 | `success_failure_independence_statement_postscript_visible` | Boolean | `true` | → content #4 |
| ✅ | 9 | `verification_guidance_postscript_visible` | Boolean | `false` | → content #3 |
| ⚠️ | 10 | `multi_criteria_relationship` | SuccessCriteriaMultiCriteriaRelationship | `"independent_blocks"` | how multiple criteria relate visually — not implemented |

## Display (SuccessCriteriaDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `evidence_format` | UnionFormatOrPair | `["bulleted", "numbered"]` | threshold-based evidence list format — not wired |
| ⚠️ | 2 | `evidence_format_threshold` | Integer | `5` | switch to numbered above 5 items — not wired |

---

## Rendering Order

```
HEADING:
  ✅ heading                               "Success Criteria"

BODY:
  For each SuccessItem:
    .success_definition                    → scalar string (SuccessDefinition)
    .success_evidence                      → list of StringProse scalars

    ⚠️ definition_framing_b_variant        {variant: "declarative_assertion" → "{{DEFINITION}}"}
                                             wraps success_definition — per-item rendering not yet wired
    ⚠️ definition_to_evidence_transition_b_variant  {variant: "goal_then_criteria" → "Meeting this standard means:"}
                                             transition between definition and evidence list — not wired
    ⚠️ evidence_framing_b_variant          {variant: "properties" → "A successful output has these properties:"}
                                             framing label before evidence list — not wired
    ⚠️ evidence list                       renders success_evidence items
                                             [display: evidence_format = ["bulleted", "numbered"], threshold = 5]

  criteria_separator                       "Additionally" — rendered between items when >1 criteria
                                             [visible: implicit — always rendered between items]

  verification_guidance_postscript         "Some conditions above are mechanically verifiable..."
                                             [visible: verification_guidance_postscript_visible = false]
  success_failure_independence_statement_postscript  "Success criteria define quality. Failure criteria define breakage..."
                                             [visible: success_failure_independence_statement_postscript_visible = true]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: Per-item `_b_variant` framing not wired for per-item rendering

The three `_b_variant` fields (`definition_framing_b_variant`, `definition_to_evidence_transition_b_variant`, `evidence_framing_b_variant`) are body-slot content that need to be applied per criteria item. They are classified correctly by suffix but the engine's per-item rendering loop does not yet use them as decoration templates around each item's data.

### ⚠️ ISSUE 2: `evidence_type_handling` and `output_vs_agent_voice` not implemented

Structure controls for evidence classification (`"undifferentiated"`) and voice paradigm (`"output_centric"`) exist but are not read.

### ⚠️ ISSUE 3: `multi_criteria_relationship` not implemented

`multi_criteria_relationship = "independent_blocks"` controls visual grouping when there are multiple criteria items. Not implemented.

### ⚠️ ISSUE 4: `evidence_format` display threshold not wired

Evidence list format switches between bulleted and numbered based on count vs threshold. Engine does not read the threshold.

### ⚠️ ISSUE 5: `section_visible` master toggle not checked by engine

Same as other sections — section-skip decision not implemented at orchestrate level.

---

## Renames Needed

### Variant templates (at least one alternative contains `{{...}}`)

- `definition_framing_b_variant` → `definition_framing_b_variant_template` — all alternatives contain `{{DEFINITION}}`

### Variant naming (`_variant` as modifier, `_selector` in structure)

Content: drop slot letter from `_x_variant`. Fix ambiguous names — `framing` has no recognized positional suffix after dropping `_b`, so add one.

- `definition_framing_b_variant` → `definition_declaration_variant` — drop `_b`, replace ambiguous `_framing` with `_declaration`; also has `_template` from above, so combined rename is `definition_declaration_variant_template`
- `evidence_framing_b_variant` → `evidence_intro_variant` — drop `_b`, replace ambiguous `_framing` with `_intro`
- `definition_to_evidence_transition_b_variant` → `definition_to_evidence_transition_variant` — drop `_b`; `_transition` is a recognized positional suffix

Structure: rename `_variant` selectors to `_selector`.

- `definition_framing_b_variant` → `definition_declaration_selector`
- `evidence_framing_b_variant` → `evidence_intro_selector`
- `definition_to_evidence_transition_b_variant` → `definition_to_evidence_transition_selector`
