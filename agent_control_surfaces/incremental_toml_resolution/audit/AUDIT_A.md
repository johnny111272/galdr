# TOML Extraction Audit

## Summary

The 13 extractions are largely consistent with the architecture doc conventions. The major pattern violations cluster around three issues: visibility toggle names that don't match their content field counterparts (broken cross-reference), variant selectors that don't follow the `{concept}_variant` naming convention, and a handful of phantom fields (structure toggles with no content, or content variants with no structure selector).

## Findings

### [MISMATCH]: INSTRUCTIONS `instructions_preamble_no_extra_operations_visible` vs `instructions_preamble_no_extra_operations_postscript`
- **Where**: INSTRUCTIONS, structure.toml `instructions_preamble_no_extra_operations_visible`, content.toml `instructions_preamble_no_extra_operations_postscript`
- **Convention violated**: "The shared root name creates obvious cross-reference" and "The structure field is `{name}_visible` (boolean). The content field is `{name}` (string)."
- **Specific**: Structure toggle root is `instructions_preamble_no_extra_operations`. Content field adds `_postscript` suffix: `instructions_preamble_no_extra_operations_postscript`. A reader of structure.toml looking for the content counterpart by stripping `_visible` finds nothing.
- **Fix**: Either rename structure to `instructions_preamble_no_extra_operations_postscript_visible` or rename content to `instructions_preamble_no_extra_operations`.

### [MISMATCH]: FAILURE_CRITERIA `preamble_visible` vs `abort_stance_preamble_{value}`
- **Where**: FAILURE_CRITERIA, structure.toml `preamble_visible`, content.toml `abort_stance_preamble_obligation` / `abort_stance_preamble_permission`
- **Convention violated**: "The shared root name creates obvious cross-reference." For visibility toggles on variant-selected content, the toggle root must match the content field family root.
- **Specific**: Structure toggle is `preamble_visible`, implying a content field named `preamble`. Content fields are `abort_stance_preamble_obligation` and `abort_stance_preamble_permission`, keyed by `abort_stance_variant`. The root `preamble` doesn't match the content root `abort_stance_preamble`.
- **Fix**: Rename structure toggle to `abort_stance_preamble_visible`.

### [MISMATCH]: FAILURE_CRITERIA `cite_definition_and_evidence_visible` vs `cite_definition_and_evidence_postscript`
- **Where**: FAILURE_CRITERIA, structure.toml `cite_definition_and_evidence_visible`, content.toml `cite_definition_and_evidence_postscript`
- **Convention violated**: Same root-name cross-reference rule as above.
- **Specific**: Structure root is `cite_definition_and_evidence`. Content field appends `_postscript`: `cite_definition_and_evidence_postscript`.
- **Fix**: Either rename structure to `cite_definition_and_evidence_postscript_visible` or rename content to `cite_definition_and_evidence`.

### [MISMATCH]: EXAMPLES `section_preamble_visible` vs `preamble`
- **Where**: EXAMPLES, structure.toml `section_preamble_visible`, content.toml `preamble`
- **Convention violated**: Shared root name cross-reference.
- **Specific**: Structure root is `section_preamble`. Content field is `preamble`. Stripping `_visible` from the structure field yields `section_preamble`, which does not match `preamble`.
- **Fix**: Either rename structure to `preamble_visible` or rename content to `section_preamble`.

### [MISMATCH]: INSTRUCTIONS `section_closer_visible` vs `section_closer_guardrail`
- **Where**: INSTRUCTIONS, structure.toml `section_closer_visible`, content.toml `section_closer_guardrail`
- **Convention violated**: Shared root name cross-reference.
- **Specific**: Structure root is `section_closer`. Content field is `section_closer_guardrail`. If `guardrail` is a variant, there should be a `section_closer_variant` selector. If it's just a descriptor, the content field should be `section_closer`.
- **Fix**: If single variant: rename content to `section_closer`. If multiple variants intended: add `section_closer_variant` to structure and name content fields `section_closer_{value}`.

### [CONVENTION]: CONSTRAINTS `closing_compliance_reminder_variant` value `"simultaneity_reminder"` vs content field suffix `simultaneity`
- **Where**: CONSTRAINTS, structure.toml `closing_compliance_reminder_variant = "evaluation_warning" | "simultaneity_reminder"`, content.toml `closing_compliance_reminder_simultaneity`
- **Convention violated**: "The enum value in structure matches a content field suffix."
- **Specific**: Variant value `"simultaneity_reminder"` does not match content field suffix `simultaneity`. Content field is `closing_compliance_reminder_simultaneity`, not `closing_compliance_reminder_simultaneity_reminder`.
- **Fix**: Either change the variant value to `"simultaneity"` or rename the content field to `closing_compliance_reminder_simultaneity_reminder`.

### [CONVENTION]: SECURITY_BOUNDARY `framing_variant` does not follow `{concept}_variant` naming
- **Where**: SECURITY_BOUNDARY, structure.toml `framing_variant`, content.toml `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory` (and corresponding `_environmental`, `_cage` variants)
- **Convention violated**: "_variant — Content Variant Selection" pattern: "structure has `{concept}_variant`, content has `{concept}_{value}`." The concept in the selector name should match the content field prefix.
- **Specific**: `framing_variant` drives three different content field families (`heading_*`, `workspace_path_declaration_*`, `section_preamble_*`). None of these families have the prefix `framing`. A reader of structure.toml cannot determine from the field name which content fields this selector controls.
- **Fix**: Either (a) split into three selectors (`heading_variant`, `workspace_path_declaration_variant`, `section_preamble_variant`) all constrained to the same enum, or (b) document this as a "shared selector" pattern exception in the architecture doc. Option (a) is verbose but schema-derivable; option (b) requires a new pattern.

### [CONVENTION]: SUCCESS_CRITERIA `evidence_type_handling_variant` and `output_vs_agent_voice_variant` have no content field counterparts
- **Where**: SUCCESS_CRITERIA, structure.toml `evidence_type_handling_variant` and `output_vs_agent_voice_variant`
- **Convention violated**: "_variant — Content Variant Selection: Selects among named prose alternatives in content.toml." The architecture doc defines variant selectors as choosing between content.toml prose alternatives.
- **Specific**: `evidence_type_handling_variant = "graduated_language" | "undifferentiated"` has no content fields `evidence_type_handling_graduated_language` or `evidence_type_handling_undifferentiated`. Same for `output_vs_agent_voice_variant = "output_centric" | "agent_centric"` — no matching content fields. These selectors control renderer behavior, not prose selection.
- **Fix**: These are plain enums controlling rendering behavior, not variant selectors. Remove the `_variant` suffix: `evidence_type_handling = "graduated_language"` and `output_vs_agent_voice = "output_centric"`. The `_variant` suffix per the architecture doc specifically means "selects among named prose alternatives in content.toml."

### [CONVENTION]: OUTPUT has two `directory_location` content variants with no structure selector
- **Where**: OUTPUT, content.toml `directory_location` and `directory_location_with_boundary`
- **Convention violated**: "_variant — Content Variant Selection" pattern requires a structure.toml selector to choose between named alternatives.
- **Specific**: Two content alternatives exist (`directory_location` and `directory_location_with_boundary`) but no `directory_location_variant` selector in structure.toml. The extraction notes "Selection mechanism TBD."
- **Fix**: Add `directory_location_variant = "standard" | "with_boundary"` to structure.toml. Rename content fields to `directory_location_standard` and `directory_location_with_boundary` to match the pattern.

### [CONVENTION]: INSTRUCTIONS `signal_at_mode_change_boundaries_visible` root name doesn't match content fields
- **Where**: INSTRUCTIONS, structure.toml `signal_at_mode_change_boundaries_visible`, content.toml `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment`
- **Convention violated**: Shared root name cross-reference.
- **Specific**: Structure root (after stripping `_visible`) is `signal_at_mode_change_boundaries`. Content fields are `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment`. The roots don't match. These are two directional variants, both controlled by a single visibility toggle.
- **Fix**: Rename structure to `signal_at_mode_change_visible`. Content fields `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment` share root `signal_at_mode_change`, which would match.

### [CONVENTION]: INSTRUCTIONS phantom toggles with no content counterparts
- **Where**: INSTRUCTIONS, structure.toml `cross_step_dependency_phrases_visible` and `step_body_container_visible`
- **Convention violated**: "_visible — Fragment Visibility: Controls whether a prose fragment renders." The `_visible` suffix means there should be a corresponding prose fragment.
- **Specific**: `cross_step_dependency_phrases_visible` has no content field named `cross_step_dependency_phrases`. `step_body_container_visible` has no content field — the extraction decisions suggest this is a rendering behavior toggle, not a prose fragment.
- **Fix**: For `cross_step_dependency_phrases_visible`: add matching content field or remove toggle if the prose doesn't exist yet. For `step_body_container_visible`: this controls rendering structure, not prose — rename to remove `_visible` suffix (e.g., `step_body_container = true`) or move to display.toml as `step_body_container`.

### [CONVENTION]: EXAMPLES phantom toggle `group_framing_sentence_visible` with no content counterpart
- **Where**: EXAMPLES, structure.toml `group_framing_sentence_visible`
- **Convention violated**: `_visible` toggle implies a content field exists.
- **Specific**: No content field `group_framing_sentence` exists in EXAMPLES content.toml.
- **Fix**: Add `group_framing_sentence` to content.toml, or remove the toggle if the prose is not yet designed.

### [MISPLACED]: SECURITY_BOUNDARY `tool_names_visible` may belong in display.toml
- **Where**: SECURITY_BOUNDARY, structure.toml `tool_names_visible`
- **Convention violated**: structure.toml "Does NOT contain prose, templates, or format enums." The `_visible` suffix in structure is for "whether a prose fragment renders." This toggle controls whether tool name data appears alongside path data — a display concern, not a prose fragment visibility concern.
- **Specific**: `tool_names_visible` controls whether tool names render in security boundary entries. Tool names are data, not prose. This is more analogous to a display format selector (show/hide a data column).
- **Fix**: Move to display.toml. Consider renaming to `tool_names_display = "visible" | "hidden"` or similar display-oriented naming.

### [INCONSISTENCY]: INSTRUCTIONS `scaffolding_tier_boundary_lightweight` / `scaffolding_tier_boundary_standard` threshold naming
- **Where**: INSTRUCTIONS, display.toml `scaffolding_tier_boundary_lightweight = 3` and `scaffolding_tier_boundary_standard = 7`
- **Convention violated**: Threshold types documentation specifies four threshold suffixes: `_format_threshold`, `_visibility_threshold`, `_activation_threshold`, `_auto_threshold`. These thresholds don't use any of the four documented suffixes.
- **Specific**: These are activation thresholds that determine which scaffolding tier applies. They should use `_activation_threshold` per the architecture doc: "triggers a behavioral feature."
- **Fix**: Rename to `scaffolding_tier_lightweight_activation_threshold = 3` and `scaffolding_tier_standard_activation_threshold = 7`, or define a new threshold pattern and document it in the architecture doc.
