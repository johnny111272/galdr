# TOML Extraction Audit

## Summary

The 13 extractions are largely consistent with the architecture doc conventions. Most `_visible` toggles have matching content fields, most `_variant` selectors follow the `{concept}_{value}` content naming pattern, and threshold suffixes are correctly applied throughout. However, there are several naming mismatches between structure and content fields, two phantom variant selectors with no content counterparts, and one misplaced field.

## Findings

### [MISMATCH]: `framing_variant` in SECURITY_BOUNDARY drives content fields with different concept prefixes

- **Where**: SECURITY_BOUNDARY section, structure.toml `framing_variant`, content.toml `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory` (and their `_environmental`/`_cage` siblings)
- **Convention violated**: Variant selector pattern (architecture doc, "Field Interface Patterns" section 3): structure has `{concept}_variant = "{value}"`, content has `{concept}_{value} = "..."`. The concept in the selector name must be the concept prefix in the content fields.
- **Specific**: Structure declares `framing_variant = "territory"`. A naive reader would look for `framing_territory` in content.toml. Instead, the variant value `territory` is suffixed onto three different concept prefixes: `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory`. The one-to-many mapping from a single variant selector to multiple content field families has no precedent in the architecture doc.
- **Fix**: Either (a) split into three variant selectors (`heading_variant`, `workspace_path_declaration_variant`, `section_preamble_variant`) so each follows the `{concept}_variant` -> `{concept}_{value}` convention, or (b) document the one-to-many variant pattern as an explicit extension of the convention in the architecture doc.

### [MISMATCH]: `abort_stance_variant` in FAILURE_CRITERIA has same one-to-many problem

- **Where**: FAILURE_CRITERIA section, structure.toml `abort_stance_variant`, content.toml `abort_stance_preamble_obligation`, `abort_stance_preamble_permission`, `abort_stance_definition_label_obligation`, `abort_stance_definition_label_permission`
- **Convention violated**: Same variant selector pattern as above.
- **Specific**: Structure declares `abort_stance_variant = "obligation"`. Content fields are `abort_stance_preamble_{value}` and `abort_stance_definition_label_{value}` -- two content field families keyed by one variant selector. The concept prefix in the content fields (`abort_stance_preamble`, `abort_stance_definition_label`) does not match the concept in the selector (`abort_stance`).
- **Fix**: Same options as SECURITY_BOUNDARY: split into `abort_stance_preamble_variant` and `abort_stance_definition_label_variant`, or document the one-to-many pattern.

### [MISMATCH]: `preamble_visible` in FAILURE_CRITERIA does not match content field root

- **Where**: FAILURE_CRITERIA section, structure.toml `preamble_visible`, content.toml `abort_stance_preamble_obligation` / `abort_stance_preamble_permission`
- **Convention violated**: Visibility toggle naming (architecture doc, "Visibility Toggles Use `_visible` Suffix"): "The shared root name creates obvious cross-reference."
- **Specific**: Structure toggle is `preamble_visible`. Content fields are `abort_stance_preamble_obligation` and `abort_stance_preamble_permission`. The root `preamble` does not match `abort_stance_preamble`. A reader of structure.toml sees `preamble_visible` and looks for `preamble` (or `preamble_{variant}`) in content.toml. They will not find it -- the content fields have the `abort_stance_` prefix.
- **Fix**: Rename structure toggle to `abort_stance_preamble_visible` to match the content field root, consistent with the `_visible` cross-reference convention.

### [MISMATCH]: `instructions_preamble_no_extra_operations_visible` does not match content field

- **Where**: INSTRUCTIONS section, structure.toml `instructions_preamble_no_extra_operations_visible`, content.toml `instructions_preamble_no_extra_operations_postscript`
- **Convention violated**: Visibility toggle naming: "The structure field is `X_visible` (boolean). The content field is `X` (string). The shared root name creates obvious cross-reference."
- **Specific**: Structure root is `instructions_preamble_no_extra_operations`. Content field is `instructions_preamble_no_extra_operations_postscript` (appends `_postscript`). The root names differ.
- **Fix**: Either rename the structure toggle to `instructions_preamble_no_extra_operations_postscript_visible`, or rename the content field to `instructions_preamble_no_extra_operations` (dropping the `_postscript` suffix). The `_postscript` suffix carries position signifier value per the architecture doc, so the structure toggle should incorporate it.

### [MISMATCH]: `section_closer_visible` in INSTRUCTIONS does not match content field

- **Where**: INSTRUCTIONS section, structure.toml `section_closer_visible`, content.toml `section_closer_guardrail`
- **Convention violated**: Same visibility toggle cross-reference convention.
- **Specific**: Structure root is `section_closer`. Content field is `section_closer_guardrail`. A reader of structure.toml sees `section_closer_visible` and expects `section_closer` in content.toml. The content field has an extra `_guardrail` suffix.
- **Fix**: Rename content field to `section_closer` to match the structure toggle root, or rename the structure toggle to `section_closer_guardrail_visible`.

### [MISMATCH]: `section_preamble_visible` in EXAMPLES does not match content field

- **Where**: EXAMPLES section, structure.toml `section_preamble_visible`, content.toml `preamble`
- **Convention violated**: Same visibility toggle cross-reference convention.
- **Specific**: Structure root is `section_preamble`. Content field is `preamble`. The names differ by the `section_` prefix. A reader of structure.toml sees `section_preamble_visible` and looks for `section_preamble` in content.toml.
- **Fix**: Either rename structure toggle to `preamble_visible` or rename content field to `section_preamble`. Choose whichever is consistent with how other sections name their preambles (INPUT uses `section_preamble` in both files; CONSTRAINTS uses `preamble` in both; ANTI_PATTERNS uses `preamble` in both). The inconsistency across sections is also noted below.

### [MISMATCH]: `signal_at_mode_change_boundaries_visible` in INSTRUCTIONS does not match content fields

- **Where**: INSTRUCTIONS section, structure.toml `signal_at_mode_change_boundaries_visible`, content.toml `signal_at_mode_change_to_exact` / `signal_at_mode_change_to_judgment`
- **Convention violated**: Same visibility toggle cross-reference convention.
- **Specific**: Structure root is `signal_at_mode_change_boundaries`. Content fields are `signal_at_mode_change_to_exact` and `signal_at_mode_change_to_judgment`. The shared prefix is `signal_at_mode_change` but structure appends `_boundaries` while content appends `_to_exact`/`_to_judgment`.
- **Fix**: Rename structure toggle to `signal_at_mode_change_visible` (drop `_boundaries`). The content fields then clearly extend the shared root with their data-conditional suffixes.

### [MISMATCH]: `cite_definition_and_evidence_visible` in FAILURE_CRITERIA does not match content field

- **Where**: FAILURE_CRITERIA section, structure.toml `cite_definition_and_evidence_visible`, content.toml `cite_definition_and_evidence_postscript`
- **Convention violated**: Same visibility toggle cross-reference convention.
- **Specific**: Structure root is `cite_definition_and_evidence`. Content field adds `_postscript`. The `_postscript` suffix carries position information per the architecture doc and should be in the shared root.
- **Fix**: Rename structure toggle to `cite_definition_and_evidence_postscript_visible`.

### [CONVENTION]: Two variant selectors in SUCCESS_CRITERIA have no content counterparts

- **Where**: SUCCESS_CRITERIA section, structure.toml `evidence_type_handling_variant` and `output_vs_agent_voice_variant`
- **Convention violated**: Variant selector pattern requires content fields `{concept}_{value}` for each possible value of `{concept}_variant`.
- **Specific**: `evidence_type_handling_variant = "undifferentiated"` has values `"graduated_language"` and `"undifferentiated"` but content.toml has no `evidence_type_handling_graduated_language` or `evidence_type_handling_undifferentiated` fields. Similarly, `output_vs_agent_voice_variant` with values `"output_centric"` and `"agent_centric"` has no `output_vs_agent_voice_output_centric` or `output_vs_agent_voice_agent_centric` content fields.
- **Fix**: Add the corresponding content fields, or if these variants control rendering behavior (code-level template selection) rather than prose selection, document them as plain enums and remove the `_variant` suffix.

### [CONVENTION]: `directory_location` and `directory_location_with_boundary` in OUTPUT have no structure selector

- **Where**: OUTPUT section, content.toml has `directory_location` and `directory_location_with_boundary`
- **Convention violated**: Variant selector pattern: when content has multiple named alternatives for the same concept, structure.toml must have a `{concept}_variant` selector to choose between them.
- **Specific**: Two content fields exist for directory location text but no `directory_location_variant` in structure.toml selects between them. The decisions note "Selection mechanism TBD."
- **Fix**: Add `directory_location_variant = "standard"  # "standard" | "with_boundary"` to structure.toml, and rename content fields to `directory_location_standard` and `directory_location_with_boundary` to follow the `{concept}_{value}` pattern.

### [MISPLACED]: `step_body_container_visible` in INSTRUCTIONS belongs in display.toml

- **Where**: INSTRUCTIONS section, structure.toml `step_body_container_visible`
- **Convention violated**: Architecture doc file architecture: structure.toml "Does NOT contain prose, templates, or format enums." Display.toml contains "Format enums dispatching to renderer functions." A body container (blockquote, code fence, bare) is a visual format decision.
- **Specific**: `step_body_container_visible = false` controls whether a visual wrapper (like a blockquote) surrounds step body text. EXAMPLES has the analogous `entry_body_container` correctly placed in display.toml. INSTRUCTIONS should follow the same pattern.
- **Fix**: Move the toggle to display.toml or consolidate with a `step_body_container` format enum in display.toml (where a value of `"none"` replaces the boolean toggle).

### [CONVENTION]: `must_vs_must_not_normalization` in CONSTRAINTS is a format concern in structure.toml

- **Where**: CONSTRAINTS section, structure.toml `must_vs_must_not_normalization = "preserve_voice" | "normalize_outliers" | "prefix_tags"`
- **Convention violated**: Architecture doc file architecture: display.toml contains "Format enums dispatching to renderer functions." This enum controls HOW constraint text renders (preserve original voice, normalize formatting, add MUST/MUST-NOT prefix tags). This is a display format decision, not a structural one.
- **Specific**: `must_vs_must_not_normalization` selects a rendering treatment applied to constraint text. It does not control what data is present or what prose fragments are included. It controls visual formatting of author data.
- **Fix**: Move to display.toml `[constraints]`.

### [INCONSISTENCY]: Preamble field naming varies across sections without documented reason

- **Where**: Multiple sections
- **Convention violated**: Architecture doc, "Descriptive Over Convenient": "Each file is read in isolation. Field names must be self-documenting without context from other files."
- **Specific**: The same concept (section preamble) uses different naming across sections:
  - INPUT: structure `section_preamble_visible`, content `section_preamble`
  - SECURITY_BOUNDARY: structure `section_preamble_visible`, content `section_preamble_{variant}`
  - EXAMPLES: structure `section_preamble_visible`, content `preamble`
  - CONSTRAINTS: structure `preamble_visible`, content `preamble_{variant}`
  - ANTI_PATTERNS: structure `preamble_visible`, content `preamble`
  - FAILURE_CRITERIA: structure `preamble_visible`, content `abort_stance_preamble_{variant}`

  Some use `section_preamble`, others use `preamble`, and FAILURE_CRITERIA uses a domain-specific prefix. This inconsistency means a schema cannot define a single pattern for section preamble toggles.
- **Fix**: Standardize on one naming convention for section-level preambles across all sections. Either always `section_preamble_visible`/`section_preamble` or always `preamble_visible`/`preamble`. FAILURE_CRITERIA should align with whichever is chosen.

### [CONVENTION]: `group_framing_sentence_visible` in EXAMPLES is a phantom toggle

- **Where**: EXAMPLES section, structure.toml `group_framing_sentence_visible = false`
- **Convention violated**: Visibility toggle convention: `_visible` fields should have matching content fields.
- **Specific**: Structure has `group_framing_sentence_visible = false` but content.toml has no `group_framing_sentence` field. If this toggle were enabled, there would be no prose to render.
- **Fix**: Add `group_framing_sentence` to content.toml, or remove the toggle from structure.toml if the feature is not yet designed.

### [CONVENTION]: `cross_step_dependency_phrases_visible` in INSTRUCTIONS is a phantom toggle

- **Where**: INSTRUCTIONS section, structure.toml `cross_step_dependency_phrases_visible = false`
- **Convention violated**: Same as above -- visibility toggle with no matching content field.
- **Specific**: Structure has the toggle but content.toml has no `cross_step_dependency_phrases` field or template.
- **Fix**: Add the content field(s), or remove the toggle if the feature is not yet designed.
