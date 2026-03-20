# TOML Extraction Audit

## Summary

The 13 extraction files are largely consistent with the architecture doc. Naming conventions are followed with discipline across most sections. The findings below are genuine convention violations and cross-section inconsistencies, not design disagreements. The most impactful issue is inconsistent position-signifier usage on content fields that have matching `_visible` toggles.

## Findings

### [CONVENTION]: `expertise_is_strictly_limited` content field missing position signifier

- **Where**: IDENTITY content.toml, field `expertise_is_strictly_limited`
- **Convention violated**: Universal Block Assembly Order (position signifiers). The architecture doc states field names MUST encode position. This field is a postscript (it says "the areas listed above"), but the content field name is `expertise_is_strictly_limited` while the structure toggle is `expertise_is_strictly_limited_visible`. The architecture doc's own worked example calls the content field `expertise_is_strictly_limited_postscript`.
- **Specific**: IDENTITY content.toml has `expertise_is_strictly_limited = "Your expertise is strictly limited to the areas listed above."` The architecture doc worked example (line 349) shows this as `expertise_is_strictly_limited_postscript`. The extraction drops the `_postscript` suffix.
- **Fix**: Rename to `expertise_is_strictly_limited_postscript` in IDENTITY content.toml to match the architecture doc worked example.

### [MISMATCH]: `input_completeness_assertion_visible` toggle has no matching content field name

- **Where**: INPUT structure.toml field `input_completeness_assertion_visible`, INPUT content.toml field `input_completeness_postscript`
- **Convention violated**: Visibility toggle naming. Architecture doc: "The shared root name creates obvious cross-reference." The structure field root is `input_completeness_assertion`, but the content field root is `input_completeness` with a `_postscript` suffix.
- **Specific**: `input_completeness_assertion_visible` should match a content field with root `input_completeness_assertion`. The actual content field is `input_completeness_postscript`. These share no root name.
- **Fix**: Either rename the structure toggle to `input_completeness_postscript_visible` (matching the content field), or rename the content field to `input_completeness_assertion_postscript` (preserving both the root match and the position signifier).

### [MISMATCH]: `readiness_checkpoint_visible` toggle vs `readiness_checkpoint_postscript` content field

- **Where**: INPUT structure.toml field `readiness_checkpoint_visible`, INPUT content.toml field `readiness_checkpoint_postscript`
- **Convention violated**: Visibility toggle naming. The architecture doc convention: structure has `X_visible`, content has `X`. Here structure has `readiness_checkpoint_visible` but content has `readiness_checkpoint_postscript` -- the content root name is `readiness_checkpoint_postscript`, not `readiness_checkpoint`.
- **Specific**: The `_visible` suffix applies to a root name. If the content field is `readiness_checkpoint_postscript`, the toggle should be `readiness_checkpoint_postscript_visible`. If the toggle is `readiness_checkpoint_visible`, the content field should be `readiness_checkpoint`.
- **Fix**: Rename toggle to `readiness_checkpoint_postscript_visible` to match the content field's full root name.

### [CONVENTION]: `section_preamble_visible` toggle vs `section_preamble` content field -- inconsistent use across sections

- **Where**: INPUT, EXAMPLES, SECURITY_BOUNDARY all use `section_preamble_visible` / `section_preamble`. ANTI_PATTERNS and FAILURE_CRITERIA use `preamble_visible` / `preamble`. CONSTRAINTS uses `preamble_visible` / `preamble_standalone` (variant pattern).
- **Convention violated**: Cross-section consistency. The architecture doc says "field names must be self-documenting without context from other files." Both `preamble_visible` and `section_preamble_visible` appear across different sections for the same concept (section-level preamble text).
- **Specific**: INPUT, EXAMPLES, SECURITY_BOUNDARY: `section_preamble_visible` + `section_preamble`. ANTI_PATTERNS: `preamble_visible` + `preamble`. FAILURE_CRITERIA: `preamble_visible` + `preamble_obligation`/`preamble_permission` (variant). CONSTRAINTS: `preamble_visible` + `preamble_standalone`/`preamble_references_*` (variant). INSTRUCTIONS: no `preamble_visible` at all (preamble components have individual toggles).
- **Fix**: Pick one convention for section-level preamble naming. `preamble_visible` + `preamble` is shorter. `section_preamble_visible` + `section_preamble` is more self-documenting per the architecture doc's own guidance. Apply whichever is chosen uniformly to INPUT, EXAMPLES, SECURITY_BOUNDARY, ANTI_PATTERNS, FAILURE_CRITERIA, and CONSTRAINTS.

### [MISMATCH]: SECURITY_BOUNDARY `section_closing_visible` toggle vs `section_closing` content -- missing position signifier

- **Where**: SECURITY_BOUNDARY structure.toml `section_closing_visible`, content.toml `section_closing`
- **Convention violated**: Position signifiers. The architecture doc says field names MUST encode position. `section_closing` is a postscript (rendered after entries). A reader encountering `section_closing` in content.toml cannot distinguish position from the name alone.
- **Specific**: `section_closing = "If your task requires access to a path not listed above, report this in your return status."` -- this text references "above", confirming it is a postscript.
- **Fix**: Rename to `section_closing_postscript` and `section_closing_postscript_visible`. Or, if the pattern is to match the `section_preamble`/`section_closing` symmetry, document this as a position-pair convention.

### [INCONSISTENCY]: `_variant` selector naming inconsistency across sections

- **Where**: CONSTRAINTS, FAILURE_CRITERIA, SUCCESS_CRITERIA, SECURITY_BOUNDARY, INSTRUCTIONS
- **Convention violated**: Architecture doc pattern 3 (`_variant`): "structure has `{concept}_variant = "{value}"`, content has `{concept}_{value} = "..."`"
- **Specific**:
  - CONSTRAINTS: `preamble_variant = "standalone"` maps to `preamble_standalone`, `preamble_references_instructions`, `preamble_references_critical_rules` -- correct.
  - CONSTRAINTS: `closing_compliance_reminder_variant = "evaluation_warning"` maps to `closing_compliance_reminder_evaluation_warning`, `closing_compliance_reminder_simultaneity` -- correct.
  - FAILURE_CRITERIA: `abort_stance_variant = "obligation"` maps to `preamble_obligation`, `preamble_permission` -- **broken**. The structure concept is `abort_stance` but the content fields use `preamble_` prefix. The content should be `abort_stance_obligation` / `abort_stance_permission`, or the variant selector should be `preamble_variant`.
  - FAILURE_CRITERIA: Same issue with `definition_label_obligation` / `definition_label_permission` -- these are keyed by the same variant but use `definition_label_` prefix instead of `abort_stance_`.
  - SECURITY_BOUNDARY: `framing_paradigm = "territory"` maps to `heading_territory`, `workspace_path_declaration_territory`, `section_preamble_territory` -- **inconsistent with pattern**. The architecture doc says content fields should be `{concept}_{value}`. Here the concept is `framing_paradigm` but the content fields use their own concept names (`heading_`, `workspace_path_declaration_`, `section_preamble_`) with the variant value as suffix. This works but differs from the documented pattern where ONE variant selector maps to ONE content field.
- **Fix**:
  - FAILURE_CRITERIA: Either rename `abort_stance_variant` to split into `preamble_variant` and `definition_label_variant`, or rename the content fields to `abort_stance_preamble_obligation`, `abort_stance_preamble_permission`, `abort_stance_definition_label_obligation`, `abort_stance_definition_label_permission`. The current state has a variant selector that doesn't predict its content field names.
  - SECURITY_BOUNDARY: The one-to-many pattern (one variant selector drives multiple content fields) needs to be acknowledged as an extension of the architecture doc's one-to-one example, or each affected content field should have its own variant selector.

### [CONVENTION]: `heading_variant` in INSTRUCTIONS structure.toml but content variants use `heading_` prefix

- **Where**: INSTRUCTIONS structure.toml `heading_variant = "default"`, content.toml `heading`, `heading_procedure`, `heading_steps_with_count`
- **Convention violated**: Pattern 3 (`_variant`): content fields should be `{concept}_{value}`. The default variant maps to `heading` (no suffix), while others map to `heading_procedure` and `heading_steps_with_count`.
- **Specific**: For variant value `"default"`, the content field is `heading` (no `_default` suffix). For `"procedure"`, it is `heading_procedure`. For `"steps_with_count"`, it is `heading_steps_with_count`. The architecture doc pattern says `{concept}_{value}` -- the default case breaks this by having no value suffix.
- **Fix**: Either rename the default content field to `heading_default` for consistency, or document that the default variant value is an implicit bare-name convention (content field = concept name without suffix).

### [INCONSISTENCY]: `evidence_format` field naming differs between SUCCESS_CRITERIA and FAILURE_CRITERIA

- **Where**: SUCCESS_CRITERIA display.toml `evidence_format` + `evidence_format_threshold`. FAILURE_CRITERIA display.toml `evidence_item_format`.
- **Convention violated**: Cross-section consistency. Both sections render evidence lists. SUCCESS_CRITERIA uses `evidence_format` (matching the architecture doc `_format` pattern with threshold). FAILURE_CRITERIA uses `evidence_item_format` (different naming, no threshold, plain string).
- **Specific**: SUCCESS_CRITERIA: `evidence_format = ["bulleted", "numbered"]`, `evidence_format_threshold = 5`. FAILURE_CRITERIA: `evidence_item_format = "bare"`. The `_item_` insertion in the FAILURE_CRITERIA name breaks the naming parallel.
- **Fix**: Rename FAILURE_CRITERIA's field to `evidence_format = "bare"` for cross-section consistency. If the `_item_` qualifier is meaningful (distinguishing from something else in the section), document why.

### [MISMATCH]: CONSTRAINTS `no_inferred_constraints_variant` selector maps to content fields with `no_inferred_constraints_` prefix correctly, but toggle is `no_inferred_constraints_visible`

- **Where**: CONSTRAINTS structure.toml has both `no_inferred_constraints_visible = false` and `no_inferred_constraints_variant = "light"`. Content has `no_inferred_constraints_light` and `no_inferred_constraints_explicit`.
- **Convention violated**: None strictly -- but this is a potential confusion point. The `_visible` toggle and the `_variant` selector share the same root `no_inferred_constraints`. When `_visible = false`, the variant selector is irrelevant. This is fine. But a reader might wonder whether `no_inferred_constraints_light` is the content field for the visibility toggle or for the variant selector. The architecture doc examples always show a `_visible` toggle mapping to a content field without a variant suffix (e.g., `closing_identity_reminder_visible` -> `closing_identity_reminder`).
- **Specific**: This combines two patterns on the same root: `_visible` (pattern 1) and `_variant` (pattern 3). The architecture doc doesn't explicitly address this combination.
- **Fix**: No rename needed, but the schema documentation should acknowledge that `_visible` + `_variant` can coexist on the same root, with `_visible` as the gate and `_variant` as the selector within.

### [CONVENTION]: `filesystem_map_intro_visibility_threshold` uses `_visibility_threshold` but lives in display.toml -- ambiguous ownership

- **Where**: SECURITY_BOUNDARY display.toml `filesystem_map_intro_visibility_threshold = 4`, structure.toml `filesystem_map_intro_visible = true`
- **Convention violated**: Architecture doc threshold types section: "`_visibility_threshold` -- controls whether a fragment appears at a certain count. Lives in display.toml when count-driven, structure.toml when data-driven." This is count-driven so display.toml is correct. However, the interaction is unusual: the display threshold can suppress a fragment even when the structure toggle enables it. The SECURITY_BOUNDARY decisions section acknowledges this ("below threshold, intro suppressed regardless of toggle") but this two-file interaction for a single fragment's visibility creates a non-obvious override.
- **Specific**: `filesystem_map_intro_visible = true` (structure) can be overridden by `filesystem_map_intro_visibility_threshold = 4` (display) when entry count is below 4. The threshold effectively negates the toggle in some conditions.
- **Fix**: This is architecturally correct per the threshold types documentation. No rename needed. Noting it because the cross-file interaction should be captured in the schema's documentation to prevent confusion during editing.
