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
| ✅ | 1 | `heading` | TitleString | `heading` | heading | `"Constraints"` |
| ✅ | 2 | `constraint_count_heading` | StringTemplate | `_heading` | heading | `"You have {{COUNT}} operational constraints:"` |
| ✅ | 3 | `constraints_are_not_steps_preamble` | StringProse | `_preamble` | preamble | `"Constraints are not steps — they are conditions that must hold true at all times..."` |
| ✅ | 4 | `hierarchy_tier_comparison_preamble` | StringProse | `_preamble` | preamble | `"These constraints are binding operational rules — less severe than critical rules..."` |
| ✅ | 5 | `hierarchy_three_tier_explanation_preamble` | StringProse | `_preamble` | preamble | `"You operate under three tiers of behavioral rules: critical rules (hard failures)..."` |
| ✅ | 6 | `section_preamble_p_variant` | BaseModel | `_p_variant` | preamble | `{standalone: "...", references_instructions: "...", references_critical_rules: "..."}` |
| ✅ | 7 | `no_inferred_constraints_p_variant` | BaseModel | `_p_variant` | preamble | `{light: "These are your operational constraints.", explicit: "These {{COUNT}} rules are exhaustive..."}` |
| ✅ | 8 | `closing_compliance_reminder_c_variant` | BaseModel | `_c_variant` | closing | `{evaluation_warning: "Every constraint above is auditable...", simultaneity: "All {{COUNT}} constraints..."}` |

## Structure (ConstraintsStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ⚠️ | 3 | `section_preamble_visible` | Boolean | `true` | → content #6 — not wired to variant |
| ✅ | 4 | `constraints_are_not_steps_preamble_visible` | Boolean | `true` | → content #3 |
| ⚠️ | 5 | `no_inferred_constraints_visible` | Boolean | `true` | → content #7 — not wired to variant |
| ⚠️ | 6 | `closing_compliance_reminder_visible` | Boolean | `true` | → content #8 — not wired to variant |
| ✅ | 7 | `constraint_count_heading_visible` | Boolean | `true` | → content #2 |
| ✅ | 8 | `hierarchy_tier_comparison_preamble_visible` | Boolean | `true` | → content #4 |
| ✅ | 9 | `hierarchy_three_tier_explanation_preamble_visible` | Boolean | `true` | → content #5 |
| ✅ | 10 | `section_preamble_p_variant` | ConstraintsSectionPreamblePVariant | `"standalone"` | → selects key in content #6 |
| ✅ | 11 | `closing_compliance_reminder_c_variant` | ConstraintsClosingComplianceReminderCVariant | `"evaluation_warning"` | → selects key in content #8 |
| ✅ | 12 | `no_inferred_constraints_p_variant` | ConstraintsNoInferredConstraintsPVariant | `"light"` | → selects key in content #7 |

## Display (ConstraintsDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `rules_format` | UnionFormatOrPair | `["bulleted", "numbered"]` | threshold-based list format — not wired |
| ⚠️ | 2 | `rules_format_threshold` | Integer | `6` | switch to numbered above 6 items — not wired |
| ⚠️ | 3 | `closing_compliance_reminder_visibility_threshold` | Integer | `6` | show closing above 6 items — not wired |
| ⚠️ | 4 | `constraint_count_heading_visibility_threshold` | Integer | `6` | show count heading above 6 items — not wired |
| ⚠️ | 5 | `must_vs_must_not_normalization` | ConstraintsMustVsMustNotNormalization | `"preserve_voice"` | MUST/MUST-NOT handling — not wired |
| ⚠️ | 6 | `polarity_grouping_activation_threshold` | Integer | `11` | group positive/negative at 11+ items — not wired |

---

## Rendering Order

```
HEADING:
  ✅ heading                               "Constraints"
  ✅ constraint_count_heading              "You have {{COUNT}} operational constraints:"
                                             [visible: constraint_count_heading_visible = true]
                                             ⚠️ threshold: constraint_count_heading_visibility_threshold = 6 — not wired

PREAMBLE:
  ✅ constraints_are_not_steps_preamble    "Constraints are not steps — they are conditions..."
                                             [visible: constraints_are_not_steps_preamble_visible = true]
  ✅ hierarchy_tier_comparison_preamble    "These constraints are binding operational rules..."
                                             [visible: hierarchy_tier_comparison_preamble_visible = true]
  ✅ hierarchy_three_tier_explanation_preamble  "You operate under three tiers..."
                                             [visible: hierarchy_three_tier_explanation_preamble_visible = true]
  ⚠️ section_preamble_p_variant           {variant: "standalone" → "These constraints govern your execution..."}
                                             [visible: section_preamble_visible = true — not wired to variant]
  ⚠️ no_inferred_constraints_p_variant    {variant: "light" → "These are your operational constraints."}
                                             [visible: no_inferred_constraints_visible = true — not wired to variant]

BODY:
  For each GuardrailsConstraint (RootModel[str]):
    .root                                  → unwrapped prose string
    ⚠️ format: rules_format = ["bulleted", "numbered"], threshold = 6 — not wired

CLOSING:
  ⚠️ closing_compliance_reminder_c_variant  {variant: "evaluation_warning" → "Every constraint above is auditable..."}
                                             [visible: closing_compliance_reminder_visible = true — not wired to variant]
                                             ⚠️ threshold: closing_compliance_reminder_visibility_threshold = 6 — not wired
```

---

## Issues

### ⚠️ ISSUE 1: `section_visible` master toggle not checked by engine

The master `section_visible = true` toggle exists in structure but the engine does not check it before rendering the section. This would be a section-skip decision handled at the orchestrate level.

### ⚠️ ISSUE 2: Variant visibility gates not connected to variant selectors

`section_preamble_visible`, `no_inferred_constraints_visible`, and `closing_compliance_reminder_visible` are separate from their variant selectors (`section_preamble_p_variant`, `no_inferred_constraints_p_variant`, `closing_compliance_reminder_c_variant`). The engine needs to: (a) check the visibility gate, (b) use the variant selector to pick the correct string from the content table. These two steps are not yet connected.

### ⚠️ ISSUE 3: Display thresholds not wired

`rules_format_threshold`, `constraint_count_heading_visibility_threshold`, `closing_compliance_reminder_visibility_threshold`, and `polarity_grouping_activation_threshold` all require counting the rules list at render time and making conditional decisions. None are wired.

### ⚠️ ISSUE 4: `must_vs_must_not_normalization` not wired

Display control for MUST/MUST-NOT polarity treatment (`"preserve_voice"`) is not read by the engine.

---

## Renames Needed

### Template suffix (`_template` as final suffix)

- `constraint_count_heading` → `constraint_count_heading_template` — contains `{{COUNT}}`

### Variant templates (at least one alternative contains `{{...}}`)

- `closing_compliance_reminder_c_variant` → `closing_compliance_reminder_c_variant_template` — `simultaneity` alternative contains `{{COUNT}}`
- `no_inferred_constraints_p_variant` → `no_inferred_constraints_p_variant_template` — `explicit` alternative contains `{{COUNT}}`

### Variant naming (`_variant` as modifier, `_selector` in structure)

Content: drop slot letter from `_x_variant` — the positional suffix before `_variant` determines the slot. Fix ambiguous names by adding a recognized positional suffix where needed.

- `section_preamble_p_variant` → `section_preamble_variant` — drop `_p`; slot determined by `_preamble`
- `closing_compliance_reminder_c_variant` → `compliance_reminder_closing_variant` — drop `_c`, shorten trunk, add `_closing`; also has `_template` from above, so combined rename is `compliance_reminder_closing_variant_template`
- `no_inferred_constraints_p_variant` → `no_inferred_constraints_preamble_variant` — drop `_p`, add `_preamble` for disambiguation; also has `_template` from above, so combined rename is `no_inferred_constraints_preamble_variant_template`

Structure: rename `_variant` selectors to `_selector`.

- `section_preamble_p_variant` → `section_preamble_selector`
- `closing_compliance_reminder_c_variant` → `compliance_reminder_closing_selector`
- `no_inferred_constraints_p_variant` → `no_inferred_constraints_preamble_selector`
