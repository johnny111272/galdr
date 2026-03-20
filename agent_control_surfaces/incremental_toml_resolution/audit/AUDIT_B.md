# TOML Extraction Audit

## Summary

The 13 extractions are largely well-structured with consistent use of the guardrails family pattern (`section_visible` + `max_entries_rendered`) and correct threshold suffix usage in display.toml. However, there are systematic naming mismatches in the `_variant` pattern -- several selectors use root names that do not match their content field roots, and two variant selectors have no content fields at all. The `_visible` / content field name-matching convention is violated in a few places. These issues would force special-casing in any schema that tries to mechanically validate structure-to-content cross-references.

## Findings

### [CONVENTION]: IDENTITY content field missing `_postscript` position suffix
- **Where**: IDENTITY content.toml, `expertise_is_strictly_limited`
- **Convention violated**: Position signifier naming (architecture doc: field names MUST encode position relative to data they reference)
- **Specific**: The architecture doc's own worked example uses `expertise_is_strictly_limited_postscript` for this field. The extraction drops the suffix to just `expertise_is_strictly_limited`. This text renders AFTER the expertise list ("the areas listed above"), making `_postscript` the correct position signifier.
- **Fix**: Rename to `expertise_is_strictly_limited_postscript`. Structure toggle becomes `expertise_is_strictly_limited_postscript_visible` (or keep current structure name and accept a root-name mismatch, which is worse).

### [MISMATCH]: INPUT `input_completeness_assertion_visible` does not share root with content field
- **Where**: INPUT structure.toml `input_completeness_assertion_visible`, content.toml `input_completeness_postscript`
- **Convention violated**: Shared root name creates obvious cross-reference (architecture doc visibility toggle section)
- **Specific**: Structure root is `input_completeness_assertion`. Content root is `input_completeness` (with `_postscript` suffix). The word `assertion` exists only in structure and cannot be found in content.
- **Fix**: Either rename structure field to `input_completeness_postscript_visible` or rename content field to `input_completeness_assertion_postscript`. The former is simpler.

### [CONVENTION]: INSTRUCTIONS `heading_variant = "default"` has no matching `heading_default` content field
- **Where**: INSTRUCTIONS structure.toml `heading_variant`, content.toml `heading`
- **Convention violated**: Variant pattern -- "the enum value in structure matches a content field suffix" (architecture doc)
- **Specific**: Variant values are `"default"`, `"procedure"`, `"steps_with_count"`. Content fields are `heading` (bare), `heading_procedure`, `heading_steps_with_count`. The value `"default"` should map to `heading_default`, but maps to the unsuffixed `heading`. The other two values correctly map to suffixed fields.
- **Fix**: Rename `heading` to `heading_default` in content.toml.

### [MISMATCH]: SUCCESS_CRITERIA content fields include `_variant` in name, breaking root-name convention
- **Where**: SUCCESS_CRITERIA content.toml `definition_framing_variant_declarative_assertion`, `definition_framing_variant_conditional_gate`, `definition_framing_variant_completion_identity`
- **Convention violated**: Variant pattern -- structure has `{concept}_variant`, content has `{concept}_{value}` (not `{concept}_variant_{value}`)
- **Specific**: Architecture doc example: structure `preamble_variant = "standalone"`, content `preamble_standalone`. Here: structure `definition_framing_variant = "declarative_assertion"`, content `definition_framing_variant_declarative_assertion`. The `_variant` suffix leaked into the content field name.
- **Fix**: Rename to `definition_framing_declarative_assertion`, `definition_framing_conditional_gate`, `definition_framing_completion_identity`.

### [MISMATCH]: SUCCESS_CRITERIA `evidence_framing_variant` root does not match content field root `evidence_preamble`
- **Where**: SUCCESS_CRITERIA structure.toml `evidence_framing_variant`, content.toml `evidence_preamble_properties` / `evidence_preamble_verification_checklist` / `evidence_preamble_quality_signals`
- **Convention violated**: Variant pattern -- structure selector root and content field root must match
- **Specific**: Structure selector root is `evidence_framing`. Content field root is `evidence_preamble`. A naive reader sees `evidence_framing_variant = "properties"` and looks for `evidence_framing_properties` in content -- it does not exist.
- **Fix**: Either rename structure to `evidence_preamble_variant` or rename content fields to `evidence_framing_properties`, etc.

### [MISMATCH]: FAILURE_CRITERIA `abort_stance_variant` root does not match any content field root
- **Where**: FAILURE_CRITERIA structure.toml `abort_stance_variant = "obligation"`, content.toml `preamble_obligation`, `preamble_permission`, `definition_label_obligation`, `definition_label_permission`
- **Convention violated**: Variant pattern -- structure selector root and content field root must match
- **Specific**: The selector `abort_stance_variant` drives two independent content field pairs: `preamble_{value}` and `definition_label_{value}`. Neither root matches `abort_stance`. A reader cannot find the content fields from the selector name.
- **Fix**: Split into two selectors (`preamble_variant` and `definition_label_variant`) whose roots match their content fields, or rename the content fields to use `abort_stance` as root (e.g., `abort_stance_preamble_obligation`). The former is more consistent with the one-selector-one-content-set pattern.

### [CONVENTION]: SUCCESS_CRITERIA `evidence_type_handling_variant` and `output_vs_agent_voice_variant` have no content fields
- **Where**: SUCCESS_CRITERIA structure.toml
- **Convention violated**: Variant pattern -- "selects among named prose alternatives in content.toml" (architecture doc)
- **Specific**: `evidence_type_handling_variant = "undifferentiated"` and `output_vs_agent_voice_variant = "output_centric"` are labeled `_variant` but select renderer behavior, not content fields. No content.toml fields are keyed to these selectors.
- **Fix**: These are plain enums controlling renderer behavior, not content variant selectors. Drop the `_variant` suffix: `evidence_type_handling = "undifferentiated"`, `output_vs_agent_voice = "output_centric"`.

### [MISMATCH]: CONSTRAINTS `closing_compliance_reminder_variant` value does not match content suffix
- **Where**: CONSTRAINTS structure.toml `closing_compliance_reminder_variant = "evaluation_warning" | "simultaneity_reminder"`, content.toml `closing_compliance_reminder_simultaneity`
- **Convention violated**: Variant enum value matches content field suffix
- **Specific**: Variant value `"simultaneity_reminder"` should map to content field `closing_compliance_reminder_simultaneity_reminder`. The actual content field is `closing_compliance_reminder_simultaneity` -- the `_reminder` suffix is missing. The other variant value `"evaluation_warning"` correctly maps to `closing_compliance_reminder_evaluation_warning`.
- **Fix**: Either rename the content field to `closing_compliance_reminder_simultaneity_reminder` or change the variant value to `"simultaneity"`.

### [MISPLACED]: OUTPUT `schema_embed` is a variant selector disguised as a boolean
- **Where**: OUTPUT structure.toml `schema_embed = false`
- **Convention violated**: Variant selection uses `_variant` suffix with named values (architecture doc interface patterns)
- **Specific**: `schema_embed = false` selects between two content fields: `schema_embedded_preamble` (when true) and `schema_reference` (when false). This is functionally a variant selector with two modes, not a visibility toggle. A boolean in structure.toml that isn't a `_visible` toggle breaks the convention that booleans mean visibility.
- **Fix**: Rename to `schema_presentation_variant = "reference"` with values `"reference"` and `"embedded"`. Content fields become `schema_presentation_reference` and `schema_presentation_embedded` (or keep current content names and just fix the selector naming).

### [CONVENTION]: INSTRUCTIONS `section_closer_visible` does not cleanly map to content fields
- **Where**: INSTRUCTIONS structure.toml `section_closer_visible`, content.toml `section_closer_guardrail` and `section_closer_exact_vs_judgment_recap`
- **Convention violated**: `_visible` toggle shares root name with content field (architecture doc)
- **Specific**: Structure has `section_closer_visible` (root: `section_closer`). Content has `section_closer_guardrail` and `section_closer_exact_vs_judgment_recap`. Neither content field uses the bare root `section_closer`. The guardrail variant always renders when visible; the recap is independently toggled by `section_closer_exact_vs_judgment_recap_visible`. This means `section_closer_visible` is a master toggle for a sub-block, not a single-field visibility toggle -- but the naming makes it look like a single-field toggle with a phantom content field.
- **Fix**: Either add a bare `section_closer` content field that `section_closer_visible` directly controls, or rename to `section_closer_block_visible` to signal it's a block-level toggle.

### [CONVENTION]: EXAMPLES `group_framing_sentence_visible` has no content field
- **Where**: EXAMPLES structure.toml `group_framing_sentence_visible = false`
- **Convention violated**: `_visible` toggle should have a matching content field
- **Specific**: No `group_framing_sentence` field exists in content.toml. The toggle exists but there is nothing to toggle.
- **Fix**: Either add `group_framing_sentence` to content.toml or remove the toggle from structure.toml.

### [CONVENTION]: RETURN_FORMAT `track_metrics_as_you_work_antidrift` has no structure toggle
- **Where**: RETURN_FORMAT content.toml `track_metrics_as_you_work_antidrift`
- **Convention violated**: Content fields that are optional should have `_visible` toggles in structure (phantom content)
- **Specific**: `track_metrics_as_you_work_postscript` has a toggle (`track_metrics_as_you_work_postscript_visible`). Its sibling `track_metrics_as_you_work_antidrift` has no toggle. If antidrift always renders when postscript is visible, this should be documented as a coupled pair. If it can be independently suppressed, it needs its own toggle.
- **Fix**: Either add `track_metrics_as_you_work_antidrift_visible` to structure.toml, or document that antidrift renders whenever the postscript toggle is on.

### [INCONSISTENCY]: Single-selector multi-content-set pattern vs one-selector-one-set
- **Where**: SECURITY_BOUNDARY `framing_paradigm` drives heading + workspace_path_declaration + section_preamble. FAILURE_CRITERIA `abort_stance_variant` drives preamble + definition_label. CONSTRAINTS `preamble_variant` drives only preamble.
- **Convention violated**: Cross-section consistency in variant selector scope
- **Specific**: SECURITY_BOUNDARY uses one selector (`framing_paradigm`) to drive three content field sets -- heading, workspace_path_declaration, and section_preamble all have `_territory`/`_environmental`/`_cage` suffixes. FAILURE_CRITERIA uses one selector (`abort_stance_variant`) for two content field sets. CONSTRAINTS uses one selector per content field set. There is no documented convention for when a single selector should drive multiple content sets vs separate selectors per set.
- **Fix**: Establish a convention: either one-selector-multi-set is the standard (document it) or one-selector-one-set is the standard (split SECURITY_BOUNDARY and FAILURE_CRITERIA selectors). The former is more practical for paradigm-level shifts like framing.
