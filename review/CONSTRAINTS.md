# Constraints Section — Four-Axis Review

## Data (Constraints)

```
Constraints
  └─ rules: list of GuardrailsConstraint (scalar prose — RootModel[StringProse])
```

Agent-builder has 10 constraint rules. Each is a `RootModel[str]` — unwrapped to a plain string.

## Content (ConstraintsContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | TitleString | `section_start` | heading | `"Constraints"` |
| ✅ | 2 | `constraint_count_heading_template` | StringTemplate | `_heading_template` | body | `"You have {{COUNT}} operational constraints:"` — body sub-heading wrapping rules list count |
| ✅ | 3 | `constraints_are_not_steps_preamble` | StringProse | `_preamble` | preamble | `"Constraints are not steps — they are conditions that must hold true at all times..."` |
| ✅ | 4 | `hierarchy_tier_comparison_preamble` | StringProse | `_preamble` | preamble | `"These constraints are binding operational rules — less severe than critical rules..."` |
| ✅ | 5 | `hierarchy_three_tier_explanation_preamble` | StringProse | `_preamble` | preamble | `"You operate under three tiers of behavioral rules: critical rules (hard failures)..."` |
| ✅ | 6 | `section_preamble_variant` | BaseModel | `_preamble_variant` | preamble | `{standalone: "...", references_instructions: "...", references_critical_rules: "..."}` |
| ✅ | 7 | `no_inferred_constraints_preamble_variant_template` | BaseModel | `_preamble_variant_template` | preamble | `{light: "These are your operational constraints.", explicit: "These {{COUNT}} rules are exhaustive..."}` |
| ✅ | 8 | `compliance_reminder_closing_variant_template` | BaseModel | `_closing_variant_template` | closing | `{evaluation_warning: "Every constraint above is auditable...", simultaneity: "All {{COUNT}} constraints..."}` |

## Structure (ConstraintsStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `pre_section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `pre_max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ⚠️ | 3 | `section_preamble_visible` | Boolean | `true` | → content #6 — not wired to variant |
| ✅ | 4 | `constraints_are_not_steps_preamble_visible` | Boolean | `true` | → content #3 |
| ⚠️ | 5 | `no_inferred_constraints_preamble_visible` | Boolean | `true` | → content #7 — not wired to variant |
| ⚠️ | 6 | `compliance_reminder_closing_visible` | Boolean | `true` | → content #8 — not wired to variant |
| ✅ | 7 | `constraint_count_heading_visible` | Boolean | `true` | → content #2 |
| ✅ | 8 | `hierarchy_tier_comparison_preamble_visible` | Boolean | `true` | → content #4 |
| ✅ | 9 | `hierarchy_three_tier_explanation_preamble_visible` | Boolean | `true` | → content #5 |
| ✅ | 10 | `section_preamble_selector` | ConstraintsSectionPreambleSelector | `"standalone"` | → selects key in content #6 |
| ✅ | 11 | `compliance_reminder_closing_selector` | ConstraintsComplianceReminderClosingSelector | `"evaluation_warning"` | → selects key in content #8 |
| ✅ | 12 | `no_inferred_constraints_preamble_selector` | ConstraintsNoInferredConstraintsPreambleSelector | `"light"` | → selects key in content #7 |

## Display (ConstraintsDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `rules_format` | UnionFormatOrPair | `["bulleted", "numbered"]` | threshold-based list format — not wired |
| ⚠️ | 2 | `rules_format_threshold` | Integer | `6` | switch to numbered above 6 items — not wired |
| ⚠️ | 3 | `compliance_reminder_closing_visibility_threshold` | Integer | `6` | show closing above 6 items — not wired |
| ⚠️ | 4 | `constraint_count_heading_visibility_threshold` | Integer | `6` | show count heading above 6 items — not wired |
| ⚠️ | 5 | `rules_polarity_normalization` | ConstraintsRulesPolarityNormalization | `"preserve_voice"` | MUST/MUST-NOT handling — not wired |
| ⚠️ | 6 | `rules_polarity_grouping_threshold` | Integer | `11` | group positive/negative at 11+ items — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Constraints"

PREAMBLE:
  ✅ constraints_are_not_steps_preamble    "Constraints are not steps — they are conditions..."
                                             [visible: constraints_are_not_steps_preamble_visible = true]
  ✅ hierarchy_tier_comparison_preamble    "These constraints are binding operational rules..."
                                             [visible: hierarchy_tier_comparison_preamble_visible = true]
  ✅ hierarchy_three_tier_explanation_preamble  "You operate under three tiers..."
                                             [visible: hierarchy_three_tier_explanation_preamble_visible = true]
  ⚠️ section_preamble_variant             {variant: "standalone" → "These constraints govern your execution..."}
                                             [visible: section_preamble_visible = true — not wired to variant]
  ⚠️ no_inferred_constraints_preamble_variant_template  {variant: "light" → "These are your operational constraints."}
                                             [visible: no_inferred_constraints_preamble_visible = true — not wired to variant]

BODY:
  [constraint_count_heading]
    ✅ constraint_count_heading_template   "You have {{COUNT}} operational constraints:" (body sub-heading)
                                             [visible: constraint_count_heading_visible = true]
                                             ⚠️ threshold: constraint_count_heading_visibility_threshold = 6 — not wired

  [rules]
    For each GuardrailsConstraint (RootModel[str]):
      .root                                → unwrapped prose string
      ⚠️ format: rules_format = ["bulleted", "numbered"], threshold = 6 — not wired

CLOSING:
  ⚠️ compliance_reminder_closing_variant_template  {variant: "evaluation_warning" → "Every constraint above is auditable..."}
                                             [visible: compliance_reminder_closing_visible = true — not wired to variant]
                                             ⚠️ threshold: compliance_reminder_closing_visibility_threshold = 6 — not wired
```

---

## Issues

### ⚠️ ISSUE 1: `pre_section_visible` master toggle not checked by engine

The master `pre_section_visible = true` toggle exists in structure but the engine does not check it before rendering the section. This would be a section-skip decision handled at the orchestrate level.

### ⚠️ ISSUE 2: Variant visibility gates not connected to variant selectors

`section_preamble_visible`, `no_inferred_constraints_preamble_visible`, and `compliance_reminder_closing_visible` are separate from their variant selectors (`section_preamble_selector`, `no_inferred_constraints_preamble_selector`, `compliance_reminder_closing_selector`). The engine needs to: (a) check the visibility gate, (b) use the variant selector to pick the correct string from the content table. These two steps are not yet connected.

### ⚠️ ISSUE 3: Display thresholds not wired

`rules_format_threshold`, `constraint_count_heading_visibility_threshold`, `compliance_reminder_closing_visibility_threshold`, and `rules_polarity_grouping_threshold` all require counting the rules list at render time and making conditional decisions. None are wired.

### ⚠️ ISSUE 4: `rules_polarity_normalization` not wired

Display control for MUST/MUST-NOT polarity treatment (`"preserve_voice"`) is not read by the engine.
