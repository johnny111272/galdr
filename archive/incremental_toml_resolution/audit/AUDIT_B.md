# TOML Extraction Audit

## Summary

Most sections follow the architecture doc conventions correctly. The primary issues are naming mismatches between structure `_visible` toggles and their corresponding content fields, variant selectors that don't follow the documented `{concept}_variant` -> `{concept}_{value}` mapping pattern, phantom fields (variant selectors with no content entries, visible toggles with no content fields), and one threshold naming violation.

## Findings

### [MISMATCH]: INSTRUCTIONS `section_closer_visible` does not match content field `section_closer_guardrail`

- **Where**: INSTRUCTIONS section, structure.toml `section_closer_visible`, content.toml `section_closer_guardrail`
- **Convention violated**: "The shared root name creates obvious cross-reference" (Naming Conventions, Visibility Toggles Use `_visible` Suffix). Structure field `section_closer_visible` implies content field `section_closer`. Content field is `section_closer_guardrail`.
- **Specific**: Structure has `section_closer_visible`, content has `section_closer_guardrail`. Root names differ: `section_closer` vs `section_closer_guardrail`.
- **Fix**: Either rename structure to `section_closer_guardrail_visible` or rename content to `section_closer`.

### [MISMATCH]: INSTRUCTIONS `instructions_preamble_no_extra_operations_visible` does not match content field `instructions_preamble_no_extra_operations_postscript`

- **Where**: INSTRUCTIONS section, structure.toml `instructions_preamble_no_extra_operations_visible`, content.toml `instructions_preamble_no_extra_operations_postscript`
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- "The structure field is `closing_identity_reminder_visible` (boolean). The content field is `closing_identity_reminder` (string)." The content field root must match the structure field root (before `_visible`).
- **Specific**: Stripping `_visible` from structure gives `instructions_preamble_no_extra_operations`. Content field is `instructions_preamble_no_extra_operations_postscript`. The `_postscript` position signifier is in content but absent from structure.
- **Fix**: Rename structure to `instructions_preamble_no_extra_operations_postscript_visible`, or rename content to `instructions_preamble_no_extra_operations`.

### [MISMATCH]: INSTRUCTIONS `signal_at_mode_change_boundaries_visible` does not match content fields `signal_at_mode_change_to_exact` / `signal_at_mode_change_to_judgment`

- **Where**: INSTRUCTIONS section, structure.toml `signal_at_mode_change_boundaries_visible`, content.toml `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment`
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- shared root name must create obvious cross-reference. Also, the two content fields imply a variant pattern (keyed by mode type), but there is no `_variant` selector in structure.toml.
- **Specific**: Structure root is `signal_at_mode_change_boundaries`. Content roots are `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment`. No shared root name. No variant selector governs which content field is used.
- **Fix**: Either (a) add a variant selector and rename, e.g., structure gets `signal_at_mode_change_variant = "..."` with content fields `signal_at_mode_change_exact` / `signal_at_mode_change_judgment`, or (b) the toggle controls both fields as a pair (renderer emits both when visible), in which case the structure toggle should use a root that encompasses both, and the content fields should share that root with distinguishing suffixes.

### [MISMATCH]: EXAMPLES `section_preamble_visible` does not match content field `preamble`

- **Where**: EXAMPLES section, structure.toml `section_preamble_visible`, content.toml `preamble`
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- shared root name creates obvious cross-reference.
- **Specific**: Structure root is `section_preamble`. Content field is `preamble`. Reader of structure.toml looking for the content match would search for `section_preamble` and not find it.
- **Fix**: Either rename structure to `preamble_visible` or rename content to `section_preamble`. Note: CONSTRAINTS and ANTI_PATTERNS both use `preamble_visible`/`preamble` consistently, while INPUT and SECURITY_BOUNDARY use `section_preamble_visible`/`section_preamble` consistently. EXAMPLES mixes the two patterns.

### [MISMATCH]: FAILURE_CRITERIA `preamble_visible` does not match content fields `abort_stance_preamble_obligation` / `abort_stance_preamble_permission`

- **Where**: FAILURE_CRITERIA section, structure.toml `preamble_visible`, content.toml `abort_stance_preamble_obligation` and `abort_stance_preamble_permission`
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- shared root name. Also, `_variant` pattern (Field Interface Patterns, section 3).
- **Specific**: Structure toggle is `preamble_visible` (root: `preamble`). Content fields are `abort_stance_preamble_obligation` and `abort_stance_preamble_permission` (root: `abort_stance_preamble`). The `abort_stance_variant` selects between them, but the visible toggle name doesn't reflect the actual content field name it governs. Stripping `_visible` from `preamble_visible` gives `preamble`, not `abort_stance_preamble`.
- **Fix**: Rename structure toggle to `abort_stance_preamble_visible` to match the content field root.

### [MISMATCH]: FAILURE_CRITERIA `cite_definition_and_evidence_visible` does not match content field `cite_definition_and_evidence_postscript`

- **Where**: FAILURE_CRITERIA section, structure.toml `cite_definition_and_evidence_visible`, content.toml `cite_definition_and_evidence_postscript`
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- content field root must match structure field root.
- **Specific**: Structure root is `cite_definition_and_evidence`. Content field is `cite_definition_and_evidence_postscript`. The `_postscript` position signifier is in content but absent from structure.
- **Fix**: Rename structure to `cite_definition_and_evidence_postscript_visible`.

### [MISMATCH]: CONSTRAINTS `closing_compliance_reminder_variant` value `"simultaneity_reminder"` does not match content field suffix `_simultaneity`

- **Where**: CONSTRAINTS section, structure.toml `closing_compliance_reminder_variant = "evaluation_warning" | "simultaneity_reminder"`, content.toml `closing_compliance_reminder_simultaneity`
- **Convention violated**: `_variant` Content Variant Selection (Field Interface Patterns, section 3) -- "The enum value in structure matches a content field suffix."
- **Specific**: Variant value is `"simultaneity_reminder"`. Expected content field: `closing_compliance_reminder_simultaneity_reminder`. Actual content field: `closing_compliance_reminder_simultaneity`. The `_evaluation_warning` variant matches correctly (`closing_compliance_reminder_evaluation_warning`), but `_simultaneity_reminder` does not match `_simultaneity`.
- **Fix**: Either rename content field to `closing_compliance_reminder_simultaneity_reminder`, or rename the variant value to `"simultaneity"`.

### [CONVENTION]: SECURITY_BOUNDARY `framing_variant` is a cross-cutting variant that doesn't follow the `{concept}_variant` -> `{concept}_{value}` convention

- **Where**: SECURITY_BOUNDARY section, structure.toml `framing_variant`, content.toml `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory` (and other variant suffixes)
- **Convention violated**: `_variant` Content Variant Selection (Field Interface Patterns, section 3) -- "The enum value in structure matches a content field suffix." Convention shows `preamble_variant = "standalone"` mapping to `preamble_standalone`. The concept name in the variant selector should be the prefix of the content fields.
- **Specific**: `framing_variant = "territory"` controls three different content field families: `heading_*`, `workspace_path_declaration_*`, `section_preamble_*`. None of these share the prefix `framing_`. A reader of structure.toml seeing `framing_variant` cannot predict which content fields it governs.
- **Fix**: Either (a) split into per-field variants: `heading_variant`, `workspace_path_declaration_variant`, `section_preamble_variant` (all set to the same value by default, independently overridable), or (b) document the cross-cutting variant as a named exception to the convention with a comment naming all governed fields.

### [CONVENTION]: FAILURE_CRITERIA `abort_stance_variant` governs multiple content field families without following `{concept}_variant` -> `{concept}_{value}`

- **Where**: FAILURE_CRITERIA section, structure.toml `abort_stance_variant`, content.toml `abort_stance_preamble_obligation`, `abort_stance_preamble_permission`, `abort_stance_definition_label_obligation`, `abort_stance_definition_label_permission`
- **Convention violated**: Same as SECURITY_BOUNDARY above. `abort_stance_variant = "obligation"` maps to `abort_stance_preamble_obligation` and `abort_stance_definition_label_obligation` -- not `abort_stance_obligation`.
- **Specific**: The variant controls two distinct content field families: `abort_stance_preamble_*` and `abort_stance_definition_label_*`. The convention expects `abort_stance_obligation` as the content field name.
- **Fix**: Same options as SECURITY_BOUNDARY -- split into per-field variants or document as named exception.

### [CONVENTION]: INSTRUCTIONS display.toml threshold fields `scaffolding_tier_boundary_lightweight` and `scaffolding_tier_boundary_standard` do not use any documented threshold suffix

- **Where**: INSTRUCTIONS display.toml, fields `scaffolding_tier_boundary_lightweight` and `scaffolding_tier_boundary_standard`
- **Convention violated**: Threshold Types section -- four documented suffixes: `_format_threshold`, `_visibility_threshold`, `_activation_threshold`, `_auto_threshold`. The `_boundary_` naming follows none of them.
- **Specific**: These fields define the step-count boundaries between scaffolding tiers (lightweight/standard/heavy). They are activation thresholds -- they trigger behavioral features at certain counts.
- **Fix**: Rename to `scaffolding_tier_lightweight_activation_threshold = 3` and `scaffolding_tier_standard_activation_threshold = 7`, or document `_boundary_` as a fifth threshold type.

### [INCONSISTENCY]: Preamble naming convention inconsistent across sections

- **Where**: CONSTRAINTS, ANTI_PATTERNS use `preamble_visible` / `preamble`. INPUT, SECURITY_BOUNDARY use `section_preamble_visible` / `section_preamble`. EXAMPLES uses `section_preamble_visible` / `preamble` (the mismatch noted above).
- **Convention violated**: Descriptive Over Convenient (Naming Conventions) -- "Each file is read in isolation. Field names must be self-documenting without context from other files."
- **Specific**: Two naming patterns for the same concept across sections: `preamble` and `section_preamble`. Both refer to the introductory prose block at the top of a section. The inconsistency prevents a schema from defining a single pattern for preamble fields.
- **Fix**: Converge on one pattern. `preamble` is shorter and already scoped by the TOML table name. `section_preamble` is redundant when inside `[constraints]` -- the section context is the table name.

### [PHANTOM]: SUCCESS_CRITERIA `evidence_type_handling_variant` and `output_vs_agent_voice_variant` have no corresponding content fields

- **Where**: SUCCESS_CRITERIA structure.toml, `evidence_type_handling_variant` and `output_vs_agent_voice_variant`
- **Convention violated**: `_variant` Content Variant Selection (Field Interface Patterns, section 3) -- variant selectors select among named prose alternatives in content.toml. These selectors have no content fields to select among.
- **Specific**: `evidence_type_handling_variant = "graduated_language" | "undifferentiated"` -- no content fields `evidence_type_handling_graduated_language` or `evidence_type_handling_undifferentiated` exist. Same for `output_vs_agent_voice_variant`.
- **Fix**: Either add the corresponding content fields, or if these are code-only behavioral switches (not selecting prose), remove the `_variant` suffix and use plain enums as documented in Field Interface Patterns section 5.

### [PHANTOM]: EXAMPLES `group_framing_sentence_visible` has no corresponding content field

- **Where**: EXAMPLES structure.toml `group_framing_sentence_visible`, no matching content field
- **Convention violated**: Visibility Toggles Use `_visible` Suffix -- structure toggle controls whether a prose fragment renders. The prose fragment must exist in content.toml.
- **Specific**: `group_framing_sentence_visible = false` in structure, but no `group_framing_sentence` in content.toml.
- **Fix**: Add `group_framing_sentence = "..."` to content.toml, or remove the structure toggle if the fragment doesn't exist yet.

### [PHANTOM]: INSTRUCTIONS `cross_step_dependency_phrases_visible` has no corresponding content field

- **Where**: INSTRUCTIONS structure.toml `cross_step_dependency_phrases_visible`, no matching content field
- **Convention violated**: Same as above -- visibility toggle with no content field.
- **Specific**: `cross_step_dependency_phrases_visible = false` in structure, but no `cross_step_dependency_phrases` in content.toml. The decisions text says this is "conditional on step count (7+)" but no content defines what these phrases actually say.
- **Fix**: Add content field(s), or remove the toggle if the feature is deferred.
