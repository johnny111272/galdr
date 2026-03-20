# TOML Extraction Audit

## Summary

The 13 extractions are largely coherent and follow the architecture doc's patterns. The main systemic issue is inconsistent application of the `_variant` naming convention -- several sections use the variant pattern (structure enum selects among content alternatives) but deviate from the documented `{concept}_variant` / `{concept}_{value}` naming. There are also a few structure-content root name mismatches on `_visible` toggles.

## Findings

### [MISMATCH]: INSTRUCTIONS heading variant content field missing default suffix

- **Where**: INSTRUCTIONS, structure `heading_variant = "default"`, content `heading`
- **Convention violated**: Variant pattern -- structure `{concept}_variant = "{value}"` maps to content `{concept}_{value}`
- **Specific**: Structure has `heading_variant = "default"`. Content has `heading = "Instructions"` but should have `heading_default = "Instructions"`. The other two variants (`heading_procedure`, `heading_steps_with_count`) follow the convention. The default variant does not.
- **Fix**: Rename content field `heading` to `heading_default`

### [MISMATCH]: SUCCESS_CRITERIA definition_framing content fields include `_variant` in name

- **Where**: SUCCESS_CRITERIA, structure `definition_framing_variant`, content `definition_framing_variant_*`
- **Convention violated**: Variant pattern -- content fields should be `{concept}_{value}`, not `{concept}_variant_{value}`
- **Specific**: Structure has `definition_framing_variant = "declarative_assertion"`. Content has `definition_framing_variant_declarative_assertion`, `definition_framing_variant_conditional_gate`, `definition_framing_variant_completion_identity`. Per the convention (as demonstrated in CONSTRAINTS `preamble_variant` / `preamble_standalone`), these should be `definition_framing_declarative_assertion`, `definition_framing_conditional_gate`, `definition_framing_completion_identity`.
- **Fix**: Remove `_variant` from all three content field names

### [MISMATCH]: SUCCESS_CRITERIA evidence_framing content fields use different root than selector

- **Where**: SUCCESS_CRITERIA, structure `evidence_framing_variant`, content `evidence_preamble_*`
- **Convention violated**: Variant pattern -- content field root must match structure selector root
- **Specific**: Structure selector root is `evidence_framing`. Content fields are `evidence_preamble_properties`, `evidence_preamble_verification_checklist`, `evidence_preamble_quality_signals`. Root is `evidence_preamble`, not `evidence_framing`. A reader of structure.toml seeing `evidence_framing_variant` would look for content fields starting with `evidence_framing_` and find nothing.
- **Fix**: Either rename content fields to `evidence_framing_properties`, `evidence_framing_verification_checklist`, `evidence_framing_quality_signals` OR rename structure selector to `evidence_preamble_variant`

### [MISMATCH]: FAILURE_CRITERIA abort_stance_variant content fields use unrelated roots

- **Where**: FAILURE_CRITERIA, structure `abort_stance_variant`, content `preamble_*` and `definition_label_*`
- **Convention violated**: Variant pattern -- content field root must match structure selector root
- **Specific**: Structure has `abort_stance_variant = "obligation" | "permission"`. Content has `preamble_obligation`, `preamble_permission`, `definition_label_obligation`, `definition_label_permission`. None of these share the `abort_stance` root. This is a one-to-many variant (one selector drives multiple content field families), which the architecture doc's variant pattern does not accommodate. A reader of structure.toml cannot find the corresponding content fields by root name matching.
- **Fix**: Either split into two selectors (`preamble_variant` and `definition_label_variant`), or rename content fields to include the selector root (`abort_stance_preamble_obligation`, `abort_stance_definition_label_obligation`, etc.)

### [MISMATCH]: CONSTRAINTS closing_compliance_reminder variant value does not match content suffix

- **Where**: CONSTRAINTS, structure `closing_compliance_reminder_variant`, content `closing_compliance_reminder_simultaneity`
- **Convention violated**: Variant pattern -- enum value in structure matches content field suffix exactly
- **Specific**: Structure has `closing_compliance_reminder_variant = "evaluation_warning" | "simultaneity_reminder"`. Content has `closing_compliance_reminder_evaluation_warning` (correct) and `closing_compliance_reminder_simultaneity` (incorrect -- should be `closing_compliance_reminder_simultaneity_reminder` to match the enum value `"simultaneity_reminder"`).
- **Fix**: Either rename content field to `closing_compliance_reminder_simultaneity_reminder` OR change the enum value to `"simultaneity"` in structure.toml

### [MISMATCH]: INPUT input_completeness_assertion_visible has no matching content root

- **Where**: INPUT, structure `input_completeness_assertion_visible`, content `input_completeness_postscript`
- **Convention violated**: Visibility toggle -- structure `X_visible` maps to content `X` (shared root name)
- **Specific**: Structure toggle root is `input_completeness_assertion`. Content field root is `input_completeness` (with `_postscript` position signifier). The roots diverge: `input_completeness_assertion` vs `input_completeness`.
- **Fix**: Either rename structure field to `input_completeness_postscript_visible` or rename content field to `input_completeness_assertion_postscript`

### [CONVENTION]: EXAMPLES suppress_lone_group_heading_visible inverts _visible semantics

- **Where**: EXAMPLES, structure `suppress_lone_group_heading_visible = true`
- **Convention violated**: `_visible = true` means "show this fragment" per architecture doc convention
- **Specific**: `suppress_lone_group_heading_visible = true` means "suppress the group heading" -- i.e., true = hide, not show. This inverts the universal `_visible` semantics where true = render. A reader of structure.toml seeing `_visible = true` expects the fragment to appear.
- **Fix**: Rename to `lone_group_heading_visible = false` (invert the boolean) or use a different mechanism entirely (e.g., `lone_group_heading_promotion = true`)

### [INCONSISTENCY]: SECURITY_BOUNDARY framing_paradigm acts as variant without _variant suffix

- **Where**: SECURITY_BOUNDARY, structure `framing_paradigm`, content `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory`, etc.
- **Convention violated**: Interface pattern 3 -- variant selectors use `_variant` suffix
- **Specific**: `framing_paradigm` in structure selects among content alternatives (`heading_territory` / `heading_environmental` / `heading_cage`, etc.). This IS the variant pattern -- one structure enum, multiple content alternatives keyed by value. But it lacks the `_variant` suffix and drives multiple content field families from a single selector. CRITICAL_RULES `rule_presentation` and `internal_hierarchy` are documented as "plain enums" because they don't drive content field selection. `framing_paradigm` does drive content field selection.
- **Fix**: Document as a recognized "multi-family variant" pattern (one selector driving heading, workspace_path_declaration, and section_preamble simultaneously), or split into three independent `_variant` selectors

### [INCONSISTENCY]: OUTPUT directory_location has two content variants with no structure selector

- **Where**: OUTPUT content.toml, `directory_location` and `directory_location_with_boundary`
- **Convention violated**: Every content variant set needs a structure selector to choose among them
- **Specific**: Two content alternatives exist (`directory_location` and `directory_location_with_boundary`) but no structure.toml selector controls which one renders. The decisions text says "Selection mechanism TBD." This is a phantom variant -- content fields exist for two options but there is no structure knob to choose between them.
- **Fix**: Add a structure selector (e.g., `directory_location_variant = "standard" | "with_boundary"`) and rename content fields to match the convention (`directory_location_standard`, `directory_location_with_boundary`)
