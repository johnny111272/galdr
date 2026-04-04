# Cross-Axis Naming Inventory

Generated: 2026-04-02

Audit of field name alignment across the four Pydantic model axes:

| Axis | File | Root model |
|------|------|------------|
| DATA | `src/galdr/structure/gen/anthropic_render.py` | `AgentAnthropicRender` |
| CONTENT | `src/galdr/structure/gen/output_content.py` | `AgentOutputContent` |
| STRUCTURE | `src/galdr/structure/gen/output_structure.py` | `AgentOutputStructure` |
| DISPLAY | `src/galdr/structure/gen/output_display.py` | `AgentOutputDisplay` |

Naming convention per axis:
- DATA: bare field names (the trunk)
- CONTENT: `*_label`, `*_postscript`, `*_heading`, template fields, variant sub-models
- STRUCTURE: `*_visible`, `*_variant`, `*_override`, enum selectors
- DISPLAY: `*_format`, `*_threshold`, `*_style`, enum selectors

---

## Legend

- **ALIGNED** -- trunk name matches across all axes that reference this concept
- **MISMATCH** -- trunk name diverges across axes
- **ORPHAN** -- concept appears in only one axis
- **MISSING** -- a logical pairing is absent (e.g., data list exists but no display format)

---

## 1. identity

### DATA (`IdentityAnthropic`)

| # | Field | Type |
|---|-------|------|
| 1 | `title` | AgentTitle |
| 2 | `description` | AgentDescription |
| 3 | `role_identity` | StringText |
| 4 | `role_responsibility` | RoleResponsibility |
| 5 | `model` | AnthropicModel |
| 6 | `role_description` | RoleDescription (optional) |
| 7 | `role_expertise` | RoleExpertise (optional, list) |

### CONTENT (`IdentityContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringTemplate ({{title}}) |
| 2 | `declaration` | StringTemplate ({{role_identity}}) |
| 3 | `declaration_heuristic_postscript` | StringTemplate ({{role_identity}}) |
| 4 | `responsibility_label` | StringTemplate ({{role_responsibility}}) |
| 5 | `expertise_label` | StringText |
| 6 | `expertise_is_strictly_limited_postscript` | StringProse |
| 7 | `closing_identity_reminder` | StringTemplate ({{role_identity}}) |

### STRUCTURE (`IdentityStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `field_ordering` | IdentityFieldOrdering enum |
| 2 | `fuse_declaration_and_role_description` | Boolean |
| 3 | `expertise_is_strictly_limited_postscript_visible` | Boolean |
| 4 | `closing_identity_reminder_visible` | Boolean |
| 5 | `bold_contrast_phrase_from_role_description_visible` | Boolean |

### DISPLAY (`IdentityDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `expertise_format` | UnionFormatOrPair |
| 2 | `expertise_format_threshold` | Integer |
| 3 | `responsibility_format` | UnionFormatOrPair |
| 4 | `responsibility_format_threshold` | Integer |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| title | `title` | `heading` ({{title}}) | -- | -- | ALIGNED (content refs data via placeholder) |
| role_identity | `role_identity` | `declaration` ({{role_identity}}), `declaration_heuristic_postscript`, `closing_identity_reminder` | `closing_identity_reminder_visible` | -- | ALIGNED |
| role_responsibility | `role_responsibility` | `responsibility_label` ({{role_responsibility}}) | -- | `responsibility_format`, `responsibility_format_threshold` | ALIGNED |
| role_description | `role_description` | -- | `fuse_declaration_and_role_description`, `bold_contrast_phrase_from_role_description_visible` | -- | ALIGNED |
| role_expertise | `role_expertise` (list) | `expertise_label`, `expertise_is_strictly_limited_postscript` | `expertise_is_strictly_limited_postscript_visible` | `expertise_format`, `expertise_format_threshold` | **MISMATCH**: data says `role_expertise`, content/structure/display drop the `role_` prefix and use just `expertise_*` |
| description | `description` | -- | -- | -- | ORPHAN in DATA (also in frontmatter, not rendered by content/structure/display) |
| model | `model` | -- | -- | -- | ORPHAN in DATA (frontmatter concern, not a body section field) |
| declaration | -- | `declaration`, `declaration_heuristic_postscript` | `fuse_declaration_and_role_description` | -- | ORPHAN in CONTENT (no data field named `declaration`; the concept is derived from `role_identity`) |
| field_ordering | -- | -- | `field_ordering` | -- | ORPHAN in STRUCTURE |
| bold_contrast_phrase | -- | -- | `bold_contrast_phrase_from_role_description_visible` | -- | ORPHAN in STRUCTURE (no content template, no display format) |

### Flags

1. **MISMATCH: `role_expertise` vs `expertise_*`** -- DATA uses `role_expertise`; CONTENT uses `expertise_label` / `expertise_is_strictly_limited_postscript`; STRUCTURE uses `expertise_is_strictly_limited_postscript_visible`; DISPLAY uses `expertise_format` / `expertise_format_threshold`. The `role_` prefix is dropped in all non-data axes.
2. **MISSING**: `role_description` has no content template (no `role_description_label` or similar). It is referenced by structure toggles but rendered without dedicated content prose.
3. **MISSING**: `declaration_heuristic_postscript` in CONTENT has no corresponding structure visibility toggle (`declaration_heuristic_postscript_visible` does not exist).

---

## 2. security_boundary

### DATA (`SecurityBoundaryAnthropic`)

| # | Field | Type |
|---|-------|------|
| 1 | `workspace_path` | PathExistsAbsolute |
| 2 | `display` | DisplayEntries (optional, list of DisplayEntry) |

`DisplayEntry` sub-fields: `path` (DisplayPath), `tools` (DisplayToolsCommands)

### CONTENT (`SecurityBoundaryContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `filesystem_map_intro` | StringText |
| 2 | `section_closing` | StringProse |
| 3 | `compound_entry_template` | StringTemplate ({{PATH}}, {{TOOLS}}) |
| 4 | `grouped_tool_header` | StringTemplate ({{TOOLS}}) |
| 5 | `framing_variant` | FramingVariantContent (sub-model with heading, workspace_path_declaration, section_preamble -- each has territory/environmental/cage) |

### STRUCTURE (`SecurityBoundaryStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `fuse_workspace_path_and_resolver` | Boolean |
| 2 | `filesystem_map_intro_visible` | Boolean |
| 3 | `section_preamble_visible` | Boolean |
| 4 | `section_closing_visible` | Boolean |
| 5 | `tool_names_visible` | Boolean |
| 6 | `framing_variant` | SecurityBoundaryFramingVariant enum |

### DISPLAY (`SecurityBoundaryDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `path_style` | SecurityBoundaryPathStyle enum |
| 2 | `uniform_toolset_format` | SecurityBoundaryUniformToolsetFormat enum |
| 3 | `heterogeneous_toolset_format` | SecurityBoundaryHeterogeneousToolsetFormat enum |
| 4 | `filesystem_map_intro_visibility_threshold` | Integer |
| 5 | `entry_list_format` | SecurityBoundaryEntryListFormat enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| workspace_path | `workspace_path` | `framing_variant.workspace_path_declaration.*` | `fuse_workspace_path_and_resolver` | -- | ALIGNED |
| display (entries) | `display` (list) | `compound_entry_template`, `grouped_tool_header` | `tool_names_visible` | `entry_list_format` | ALIGNED (different facets of same concept) |
| filesystem_map_intro | -- | `filesystem_map_intro` | `filesystem_map_intro_visible` | `filesystem_map_intro_visibility_threshold` | ALIGNED (no data field, content-only concept) |
| section_closing | -- | `section_closing` | `section_closing_visible` | -- | ALIGNED |
| section_preamble | -- | `framing_variant.section_preamble.*` | `section_preamble_visible` | -- | ALIGNED |
| framing_variant | -- | `framing_variant` (sub-model) | `framing_variant` (enum selector) | -- | ALIGNED |
| path_style | -- | -- | -- | `path_style` | ORPHAN in DISPLAY (purely visual, no data/content/structure counterpart -- acceptable) |
| uniform_toolset_format | -- | `grouped_tool_header` | -- | `uniform_toolset_format` | ALIGNED (content provides the template, display selects the mode) |
| heterogeneous_toolset_format | -- | `compound_entry_template` | -- | `heterogeneous_toolset_format` | ALIGNED |
| path/tools (per entry) | `DisplayEntry.path`, `DisplayEntry.tools` | `compound_entry_template` {{PATH}}, {{TOOLS}} | `tool_names_visible` | `path_style`, toolset formats | ALIGNED |

### Flags

1. **MISSING**: `display` (entries) in DATA is a list but there is no corresponding display `*_format` for the overall list itself. The `entry_list_format` covers marker style (bullet/numbered/dash) which is adequate.
2. Content `heading` for this section lives inside `framing_variant.heading.*`, which is structurally different from other sections that have a top-level `heading` field. Naming is consistent but location pattern deviates.

---

## 3. critical_rules

### DATA (`CriticalRules`)

| # | Field | Type |
|---|-------|------|
| 1 | `has_output_tool` | Boolean |
| 2 | `tool_name` | ToolName (optional) |
| 3 | `name_needed` | OutputToolNameNeeded (optional) |
| 4 | `batch_size` | OutputToolBatchSize (optional) |

### CONTENT (`CriticalRulesContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `authority_preamble` | StringProse |
| 3 | `workspace_confinement` | StringTemplate ({{workspace_path}}) |
| 4 | `output_tool_exclusivity` | StringTemplate ({{tool_name}}) |
| 5 | `batch_discipline` | StringTemplate ({{batch_size}}, {{tool_name}}) |
| 6 | `fail_fast` | StringProse |
| 7 | `input_is_your_only_source` | StringProse |
| 8 | `no_invention` | StringProse |
| 9 | `discipline_over_helpfulness` | StringProse |
| 10 | `rule_count_awareness_prelude` | StringTemplate ({{rule_count}}) |

### STRUCTURE (`CriticalRulesStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `authority_preamble_visible` | Boolean |
| 2 | `rule_count_awareness_prelude_visible` | VisibilityMode |
| 3 | `rule_count_awareness_prelude_auto_threshold` | Integer |
| 4 | `workspace_confinement_visible` | Boolean |
| 5 | `fail_fast_visible` | Boolean |
| 6 | `input_is_your_only_source_visible` | Boolean |
| 7 | `no_invention_visible` | Boolean |
| 8 | `output_tool_exclusivity_visible` | Boolean |
| 9 | `batch_discipline_visible` | Boolean |
| 10 | `discipline_over_helpfulness_visible` | Boolean |
| 11 | `rule_presentation` | CriticalRulesRulePresentation enum |
| 12 | `internal_hierarchy` | CriticalRulesInternalHierarchy enum |

### DISPLAY (`CriticalRulesDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `workspace_path_format` | InlineFormat enum |
| 2 | `tool_name_format` | InlineFormat enum |
| 3 | `tool_name_repetition` | CriticalRulesToolNameRepetition enum |
| 4 | `batch_size_format` | InlineFormat enum |
| 5 | `rule_separator` | CriticalRulesRuleSeparator enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| workspace_path | (from security_boundary data) | `workspace_confinement` ({{workspace_path}}) | `workspace_confinement_visible` | `workspace_path_format` | **MISMATCH**: content/structure use `workspace_confinement` but display uses `workspace_path_format`. The data trunk is `workspace_path`, the content rule name is `workspace_confinement`, the display format name is `workspace_path_format`. Two different naming axes. |
| tool_name | `tool_name` | `output_tool_exclusivity` ({{tool_name}}) | `output_tool_exclusivity_visible` | `tool_name_format`, `tool_name_repetition` | **MISMATCH**: data/display share `tool_name` trunk, but content/structure use `output_tool_exclusivity` for the rule. The rule concept vs the data value have different names -- this is intentional (rule name vs data field) but creates divergence. |
| batch_size | `batch_size` | `batch_discipline` ({{batch_size}}) | `batch_discipline_visible` | `batch_size_format` | **MISMATCH**: same pattern as above -- data/display use `batch_size`, content/structure use `batch_discipline` for the rule. |
| has_output_tool | `has_output_tool` | -- | -- | -- | ORPHAN in DATA (gate flag, not rendered directly) |
| name_needed | `name_needed` | -- | -- | -- | ORPHAN in DATA (used in writing_output, not critical_rules rendering) |
| authority_preamble | -- | `authority_preamble` | `authority_preamble_visible` | -- | ALIGNED |
| fail_fast | -- | `fail_fast` | `fail_fast_visible` | -- | ALIGNED |
| input_is_your_only_source | -- | `input_is_your_only_source` | `input_is_your_only_source_visible` | -- | ALIGNED |
| no_invention | -- | `no_invention` | `no_invention_visible` | -- | ALIGNED |
| discipline_over_helpfulness | -- | `discipline_over_helpfulness` | `discipline_over_helpfulness_visible` | -- | ALIGNED |
| rule_count_awareness_prelude | -- | `rule_count_awareness_prelude` ({{rule_count}}) | `rule_count_awareness_prelude_visible`, `rule_count_awareness_prelude_auto_threshold` | -- | ALIGNED |
| rule_presentation | -- | -- | `rule_presentation` | -- | ORPHAN in STRUCTURE |
| internal_hierarchy | -- | -- | `internal_hierarchy` | -- | ORPHAN in STRUCTURE |
| rule_separator | -- | -- | -- | `rule_separator` | ORPHAN in DISPLAY |

### Flags

1. **MISMATCH: `workspace_confinement` vs `workspace_path_format`** -- The critical_rules section has a RULE called `workspace_confinement` (content/structure) but the display format for the DATA VALUE is `workspace_path_format`. This is a content-rule-name vs data-value-format divergence. Arguably intentional but creates ambiguity.
2. **MISMATCH: `output_tool_exclusivity` vs `tool_name_format`** -- Same pattern: rule name in content/structure vs data value format in display.
3. **MISMATCH: `batch_discipline` vs `batch_size_format`** -- Same pattern.
4. Note: These mismatches follow a consistent pattern where content names the RULE and display names the DATA VALUE. This may be by design but should be documented.

---

## 4. input

### DATA (`Input`)

| # | Field | Type |
|---|-------|------|
| 1 | `description` | InputDescription |
| 2 | `format` | DispatchInputFormat enum |
| 3 | `delivery` | DispatchInputDelivery enum |
| 4 | `input_schema` | PathExistsAbsolute (optional) |
| 5 | `parameters` | DispatchParameters (optional, list) |
| 6 | `context` | ContextResources (optional, sub-model with context_required, context_available) |

### CONTENT

No `InputContent` model exists.

### STRUCTURE

No `InputStructure` model exists.

### DISPLAY

No `InputDisplay` model exists.

### Flags

1. **ORPHAN SECTION**: The `input` section exists in DATA but has no CONTENT, STRUCTURE, or DISPLAY counterpart in any of the three output models. This section apparently does not participate in the content/structure/display composition pipeline (it may be rendered by a different mechanism or its rendering is hardcoded).

---

## 5. instructions

### DATA (`Instructions`)

| # | Field | Type |
|---|-------|------|
| 1 | `steps` | ExecutionInstructions (list of InstructionStep) |

`InstructionStep` sub-fields: `instruction_mode` (InstructionMode enum), `instruction_text` (StringMarkdown)

### CONTENT (`InstructionsContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `instructions_preamble_step_count` | StringTemplate ({{step_count}}) |
| 2 | `instructions_preamble_no_add_skip_reorder` | StringProse |
| 3 | `instructions_preamble_exact_vs_judgment_preview` | StringProse |
| 4 | `instructions_preamble_no_extra_operations` | StringProse |
| 5 | `step_header_exact` | StringTemplate ({{step_n}}, {{step_total}}) |
| 6 | `step_header_judgment` | StringTemplate ({{step_n}}, {{step_total}}) |
| 7 | `step_header_exact_n_only` | StringTemplate ({{step_n}}) |
| 8 | `step_header_judgment_n_only` | StringTemplate ({{step_n}}) |
| 9 | `exact_vs_judgment_body_prefix_exact` | StringText |
| 10 | `exact_vs_judgment_body_prefix_judgment` | StringText |
| 11 | `signal_at_mode_change_to_exact` | StringProse |
| 12 | `signal_at_mode_change_to_judgment` | StringProse |
| 13 | `step_done_when_suffix` | StringTemplate ({{completion_condition}}) |
| 14 | `cross_step_dependency_phrases` | StringTemplate ({{dependency_steps}}) |
| 15 | `halfway_point_reminder` | StringTemplate ({{midpoint}}, {{midpoint_next}}, {{step_total}}) |
| 16 | `section_closer_guardrail` | StringTemplate ({{step_count}}) |
| 17 | `section_closer_exact_vs_judgment_recap` | StringTemplate ({{mode_recap_text}}) |
| 18 | `exact_vs_judgment_explanation_mixed` | StringProse |
| 19 | `exact_vs_judgment_explanation_uniform_exact` | StringProse |
| 20 | `exact_vs_judgment_explanation_uniform_judgment` | StringProse |
| 21 | `heading_variant` | InstructionsHeadingVariant sub-model (default, procedure, steps_with_count) |

### STRUCTURE (`InstructionsStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading_variant` | InstructionsHeadingVariant enum |
| 2 | `exact_vs_judgment_explanation_visible` | VisibilityMode |
| 3 | `exact_vs_judgment_marker_placement` | enum |
| 4 | `signal_at_mode_change_visible` | Boolean |
| 5 | `instructions_preamble_step_count_visible` | Boolean |
| 6 | `instructions_preamble_no_add_skip_reorder_visible` | Boolean |
| 7 | `instructions_preamble_exact_vs_judgment_preview_visible` | Boolean |
| 8 | `instructions_preamble_no_extra_operations_visible` | Boolean |
| 9 | `step_index_tracking` | InstructionsStepIndexTracking enum |
| 10 | `step_done_when_suffix_visible` | Boolean |
| 11 | `section_closer_guardrail_visible` | Boolean |
| 12 | `section_closer_exact_vs_judgment_recap_visible` | Boolean |
| 13 | `cross_step_dependency_phrases_visible` | Boolean |
| 14 | `halfway_point_reminder_visible` | Boolean |
| 15 | `structural_complexity_override` | enum |

### DISPLAY (`InstructionsDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `step_header_format` | HeadingFormat enum |
| 2 | `step_body_container` | BodyContainer enum |
| 3 | `scaffolding_tier_lightweight_activation_threshold` | Integer |
| 4 | `scaffolding_tier_standard_activation_threshold` | Integer |
| 5 | `exact_vs_judgment_recap_format` | enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| steps | `steps` (list) | step_header_*, body prefix templates | `step_index_tracking` | `step_header_format`, `step_body_container` | ALIGNED (trunk is `step`) |
| instruction_mode | `instruction_mode` per step | `exact_vs_judgment_*` (multiple) | `exact_vs_judgment_*` (multiple) | `exact_vs_judgment_recap_format` | **MISMATCH**: DATA uses `instruction_mode` with values `deterministic`/`probabilistic`; content/structure/display use `exact_vs_judgment` terminology. The enum values `deterministic`/`probabilistic` map to `exact`/`judgment` in the rendering layer. |
| instruction_text | `instruction_text` per step | -- | -- | -- | DATA only (rendered directly, no content wrapper) |
| heading_variant | -- | `heading_variant` (sub-model) | `heading_variant` (enum selector) | -- | ALIGNED |
| preamble_step_count | -- | `instructions_preamble_step_count` | `instructions_preamble_step_count_visible` | -- | ALIGNED |
| preamble_no_add_skip_reorder | -- | `instructions_preamble_no_add_skip_reorder` | `instructions_preamble_no_add_skip_reorder_visible` | -- | ALIGNED |
| preamble_exact_vs_judgment_preview | -- | `instructions_preamble_exact_vs_judgment_preview` | `instructions_preamble_exact_vs_judgment_preview_visible` | -- | ALIGNED |
| preamble_no_extra_operations | -- | `instructions_preamble_no_extra_operations` | `instructions_preamble_no_extra_operations_visible` | -- | ALIGNED |
| signal_at_mode_change | -- | `signal_at_mode_change_to_exact`, `signal_at_mode_change_to_judgment` | `signal_at_mode_change_visible` | -- | ALIGNED |
| step_done_when_suffix | -- | `step_done_when_suffix` | `step_done_when_suffix_visible` | -- | ALIGNED |
| cross_step_dependency_phrases | -- | `cross_step_dependency_phrases` | `cross_step_dependency_phrases_visible` | -- | ALIGNED |
| halfway_point_reminder | -- | `halfway_point_reminder` | `halfway_point_reminder_visible` | -- | ALIGNED |
| section_closer_guardrail | -- | `section_closer_guardrail` | `section_closer_guardrail_visible` | -- | ALIGNED |
| section_closer_exact_vs_judgment_recap | -- | `section_closer_exact_vs_judgment_recap` | `section_closer_exact_vs_judgment_recap_visible` | `exact_vs_judgment_recap_format` | ALIGNED |
| structural_complexity_override | -- | -- | `structural_complexity_override` | `scaffolding_tier_*_activation_threshold` (x2) | **MISMATCH**: structure uses `structural_complexity_override`, display uses `scaffolding_tier_*`. Different naming for same concept. |
| exact_vs_judgment_marker_placement | -- | body prefix fields | `exact_vs_judgment_marker_placement` | -- | ALIGNED |

### Flags

1. **MISMATCH: `instruction_mode` (deterministic/probabilistic) vs `exact_vs_judgment`** -- DATA enum values and content/structure/display terminology diverge. The mapping is deterministic=exact, probabilistic=judgment but these are different words for the same concept.
2. **MISMATCH: `structural_complexity_override` vs `scaffolding_tier_*`** -- Structure and display use different trunk names for the same tiering mechanism.

---

## 6. examples

### DATA (`Examples`)

| # | Field | Type |
|---|-------|------|
| 1 | `groups` | ExecutionExamples (list of ExampleGroup) |

`ExampleGroup` sub-fields: `example_group_name`, `example_display_headings`, `examples_max_number`, `example_entries` (list of ExampleEntry: `example_heading`, `example_text`)

### CONTENT (`ExamplesContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `section_preamble` | StringProse |
| 3 | `group_framing_sentence` | StringTemplate ({{example_group_name}}) |
| 4 | `entry_heading` | StringTemplate ({{example_heading}}) |

### STRUCTURE (`ExamplesStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `section_preamble_visible` | Boolean |
| 2 | `suppress_lone_group_heading` | Boolean |
| 3 | `example_display_headings_override` | Boolean |
| 4 | `examples_max_number_override` | Boolean |
| 5 | `group_framing_sentence_visible` | Boolean |
| 6 | `example_display_headings` | Boolean (optional, override value) |
| 7 | `examples_max_number` | Integer (optional, override value) |

### DISPLAY (`ExamplesDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `entry_heading_format` | HeadingFormat enum |
| 2 | `entry_body_container` | BodyContainer enum |
| 3 | `entry_separator` | SeparatorStyle enum |
| 4 | `multi_group_separator` | SeparatorStyle enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| groups | `groups` (list) | `group_framing_sentence` | `suppress_lone_group_heading` | `multi_group_separator` | ALIGNED |
| example_group_name | `example_group_name` | `group_framing_sentence` ({{example_group_name}}) | -- | -- | ALIGNED |
| example_display_headings | `example_display_headings` (per-group) | `entry_heading` template | `example_display_headings_override`, `example_display_headings` (override value) | `entry_heading_format` | **MISMATCH**: data uses `example_display_headings`, display uses `entry_heading_format`. The trunk shifts from `example_display_headings` to `entry_heading`. |
| examples_max_number | `examples_max_number` (per-group) | -- | `examples_max_number_override`, `examples_max_number` (override value) | -- | ALIGNED |
| example_heading | `example_heading` (per-entry) | `entry_heading` ({{example_heading}}) | -- | `entry_heading_format` | **MISMATCH**: data uses `example_heading`, content/display use `entry_heading`. |
| example_text | `example_text` (per-entry) | -- | -- | `entry_body_container` | ALIGNED (display refers to body container, reasonable) |
| example_entries | `example_entries` (list per-group) | -- | -- | `entry_separator` | ALIGNED |
| section_preamble | -- | `section_preamble` | `section_preamble_visible` | -- | ALIGNED |
| group_framing_sentence | -- | `group_framing_sentence` | `group_framing_sentence_visible` | -- | ALIGNED |

### Flags

1. **MISMATCH: `example_heading` vs `entry_heading`** -- DATA names the field `example_heading` (per entry) and `example_display_headings` (per group toggle); content and display shift to `entry_heading` / `entry_heading_format`. The trunk changes from `example_heading` to `entry_heading`.

---

## 7. output

### DATA (`Output`)

| # | Field | Type |
|---|-------|------|
| 1 | `description` | OutputDescription |
| 2 | `format` | OutputFormatKind enum |
| 3 | `name_known` | OutputNameKnown enum |
| 4 | `schema_path` | PathExistsAbsolute (optional) |
| 5 | `output_file` | PathAbsolute (optional) |
| 6 | `output_directory` | PathAbsolute (optional) |
| 7 | `name_template` | FilenameTemplate (optional) |
| 8 | `name_instruction` | StringProse (optional) |
| 9 | `schema_embed` | Boolean (optional) |

### CONTENT (`OutputContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `output_description` | StringTemplate ({{DESCRIPTION}}) |
| 3 | `format_declaration` | StringTemplate ({{FORMAT}}) |
| 4 | `schema_embedded_preamble` | StringProse |
| 5 | `schema_reference` | StringTemplate ({{SCHEMA_PATH}}) |
| 6 | `directory_location_variant` | OutputDirectoryLocationVariant sub-model (standard, with_boundary) |

### STRUCTURE (`OutputStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `schema_embed` | Boolean |
| 2 | `directory_location_variant` | OutputDirectoryLocationVariant enum |

### DISPLAY

No `OutputDisplay` model exists. The output section is absent from `AgentOutputDisplay`.

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| description | `description` | `output_description` ({{DESCRIPTION}}) | -- | -- | **MISMATCH**: data uses `description`, content prefixes with `output_` to get `output_description`. |
| format | `format` | `format_declaration` ({{FORMAT}}) | -- | -- | ALIGNED (content wraps with `_declaration` suffix) |
| schema_path | `schema_path` | `schema_reference` ({{SCHEMA_PATH}}), `schema_embedded_preamble` | -- | -- | ALIGNED (content provides both modes) |
| schema_embed | `schema_embed` | -- | `schema_embed` | -- | ALIGNED |
| output_file | `output_file` | -- | -- | -- | ORPHAN in DATA |
| output_directory | `output_directory` | `directory_location_variant.*` ({{OUTPUT_DIRECTORY}}) | `directory_location_variant` | -- | ALIGNED |
| name_known | `name_known` | -- | -- | -- | ORPHAN in DATA |
| name_template | `name_template` | -- | -- | -- | ORPHAN in DATA |
| name_instruction | `name_instruction` | -- | -- | -- | ORPHAN in DATA |
| directory_location_variant | -- | `directory_location_variant` (sub-model) | `directory_location_variant` (enum) | -- | ALIGNED |

### Flags

1. **MISMATCH: `description` vs `output_description`** -- DATA field is `description`; content field is `output_description`. The content field adds an `output_` prefix to disambiguate (since `description` is generic).
2. **MISSING DISPLAY**: The output section has no display model at all. No formatting controls for any output fields.

---

## 8. writing_output

### DATA (`WritingOutputAnthropic`)

| # | Field | Type |
|---|-------|------|
| 1 | `tool_name` | ToolName |
| 2 | `invocation_variant` | InvocationVariant enum |
| 3 | `invocation_display` | InvocationDisplay (string) |
| 4 | `name_needed` | OutputToolNameNeeded |
| 5 | `name_pattern` | FilenameTemplate (optional) |
| 6 | `batch_size` | OutputToolBatchSize (optional) |
| 7 | `schema_path` | OutputToolSchemaXAbs (optional) |
| 8 | `file_path` | PathAbsolute (optional) |
| 9 | `directory_path` | PathAbsolute (optional) |

### CONTENT (`WritingOutputContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `transition_preamble` | StringProse |
| 3 | `tool_mandate` | StringProse |
| 4 | `tool_identity_label` | StringTemplate ({{TOOL_NAME}}) |
| 5 | `invocation_preamble` | StringProse |
| 6 | `heredoc_explanation` | StringProse |

### STRUCTURE (`WritingOutputStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `transition_preamble_visible` | Boolean |
| 2 | `tool_mandate_visible` | Boolean |
| 3 | `heredoc_explanation_visible` | Boolean |

### DISPLAY

No `WritingOutputDisplay` model exists. The writing_output section is absent from `AgentOutputDisplay`.

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| tool_name | `tool_name` | `tool_identity_label` ({{TOOL_NAME}}) | -- | -- | **MISMATCH**: data uses `tool_name`, content uses `tool_identity_label`. |
| invocation_display | `invocation_display` | `invocation_preamble` | -- | -- | ALIGNED (different roles: data holds the rendered heredoc, content holds the introductory prose) |
| invocation_variant | `invocation_variant` | -- | -- | -- | ORPHAN in DATA |
| name_needed | `name_needed` | -- | -- | -- | ORPHAN in DATA |
| name_pattern | `name_pattern` | -- | -- | -- | ORPHAN in DATA |
| batch_size | `batch_size` | -- | -- | -- | ORPHAN in DATA |
| schema_path | `schema_path` | -- | -- | -- | ORPHAN in DATA |
| file_path | `file_path` | -- | -- | -- | ORPHAN in DATA |
| directory_path | `directory_path` | -- | -- | -- | ORPHAN in DATA |
| transition_preamble | -- | `transition_preamble` | `transition_preamble_visible` | -- | ALIGNED |
| tool_mandate | -- | `tool_mandate` | `tool_mandate_visible` | -- | ALIGNED |
| heredoc_explanation | -- | `heredoc_explanation` | `heredoc_explanation_visible` | -- | ALIGNED |

### Flags

1. **MISMATCH: `tool_name` vs `tool_identity_label`** -- DATA says `tool_name`, content says `tool_identity_label`. Trunk differs.
2. **MISSING DISPLAY**: No display model for writing_output. No formatting controls.
3. Many DATA fields are orphans (name_needed, name_pattern, batch_size, schema_path, file_path, directory_path). These are consumed by the template engine directly from data and don't go through the content/structure/display pipeline.

---

## 9. constraints

### DATA (`Constraints`)

| # | Field | Type |
|---|-------|------|
| 1 | `rules` | GuardrailsConstraints (list of GuardrailsConstraint) |

### CONTENT (`ConstraintsContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `constraints_are_not_steps` | StringProse |
| 3 | `constraint_count_heading` | StringTemplate ({{constraint_count}}) |
| 4 | `hierarchy_tier_comparison` | StringProse |
| 5 | `hierarchy_three_tier_explanation` | StringProse |
| 6 | `section_preamble_variant` | sub-model (standalone, references_instructions, references_critical_rules) |
| 7 | `closing_compliance_reminder_variant` | sub-model (evaluation_warning, simultaneity) |
| 8 | `no_inferred_constraints_variant` | sub-model (light, explicit) |

### STRUCTURE (`ConstraintsStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `section_visible` | Boolean |
| 2 | `max_entries_rendered` | Integer |
| 3 | `section_preamble_visible` | Boolean |
| 4 | `constraints_are_not_steps_visible` | Boolean |
| 5 | `no_inferred_constraints_visible` | Boolean |
| 6 | `closing_compliance_reminder_visible` | Boolean |
| 7 | `constraint_count_heading_visible` | Boolean |
| 8 | `section_preamble_variant` | enum (optional) |
| 9 | `closing_compliance_reminder_variant` | enum (optional) |
| 10 | `no_inferred_constraints_variant` | enum (optional) |

### DISPLAY (`ConstraintsDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `enumeration_format` | UnionFormatOrPair |
| 2 | `enumeration_format_threshold` | Integer |
| 3 | `closing_compliance_reminder_visibility_threshold` | Integer |
| 4 | `constraint_count_heading_visibility_threshold` | Integer |
| 5 | `must_vs_must_not_normalization` | enum |
| 6 | `polarity_grouping_activation_threshold` | Integer |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| rules | `rules` (list) | -- | `max_entries_rendered` | `enumeration_format`, `enumeration_format_threshold` | **MISMATCH**: data calls the list `rules`; display calls the format `enumeration_format` (not `rules_format`). No trunk alignment. |
| constraints_are_not_steps | -- | `constraints_are_not_steps` | `constraints_are_not_steps_visible` | -- | ALIGNED |
| constraint_count_heading | -- | `constraint_count_heading` | `constraint_count_heading_visible` | `constraint_count_heading_visibility_threshold` | ALIGNED |
| section_preamble_variant | -- | `section_preamble_variant` (sub-model) | `section_preamble_variant` (enum), `section_preamble_visible` | -- | ALIGNED |
| closing_compliance_reminder | -- | `closing_compliance_reminder_variant` (sub-model) | `closing_compliance_reminder_visible`, `closing_compliance_reminder_variant` (enum) | `closing_compliance_reminder_visibility_threshold` | ALIGNED |
| no_inferred_constraints | -- | `no_inferred_constraints_variant` (sub-model) | `no_inferred_constraints_visible`, `no_inferred_constraints_variant` (enum) | -- | ALIGNED |
| hierarchy_tier_comparison | -- | `hierarchy_tier_comparison` | -- | -- | ORPHAN in CONTENT (no structure visibility toggle) |
| hierarchy_three_tier_explanation | -- | `hierarchy_three_tier_explanation` | -- | -- | ORPHAN in CONTENT (no structure visibility toggle) |
| must_vs_must_not_normalization | -- | -- | -- | `must_vs_must_not_normalization` | ORPHAN in DISPLAY |
| polarity_grouping_activation_threshold | -- | -- | -- | `polarity_grouping_activation_threshold` | ORPHAN in DISPLAY |

### Flags

1. **MISMATCH: `rules` vs `enumeration_format`** -- DATA calls the constraint list `rules`; display calls the format `enumeration_format`. No shared trunk. Should be `rules_format` or data should be `constraints` to match `enumeration`.
2. **ORPHAN**: `hierarchy_tier_comparison` and `hierarchy_three_tier_explanation` in CONTENT have no STRUCTURE visibility toggles. They will always render or require hardcoded logic.
3. **ORPHAN**: `must_vs_must_not_normalization` and `polarity_grouping_activation_threshold` in DISPLAY have no content or structure counterparts. They are display-only transforms.

---

## 10. anti_patterns

### DATA (`AntiPatterns`)

| # | Field | Type |
|---|-------|------|
| 1 | `patterns` | GuardrailsAntiPatterns (list of GuardrailsAntiPattern) |

### CONTENT (`AntiPatternsContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `section_preamble` | StringProse |
| 3 | `constraints_vs_anti_patterns_distinction` | StringProse |

### STRUCTURE (`AntiPatternsStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `section_visible` | Boolean |
| 2 | `max_entries_rendered` | Integer |
| 3 | `section_preamble_visible` | Boolean |
| 4 | `constraints_vs_anti_patterns_distinction_visible` | Boolean |

### DISPLAY (`AntiPatternsDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `pattern_list_format` | AntiPatternsPatternListFormat enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| patterns | `patterns` (list) | -- | `max_entries_rendered` | `pattern_list_format` | **MISMATCH**: data says `patterns`, display says `pattern_list_format` (singular `pattern`). Minor singular/plural divergence. |
| section_preamble | -- | `section_preamble` | `section_preamble_visible` | -- | ALIGNED |
| constraints_vs_anti_patterns_distinction | -- | `constraints_vs_anti_patterns_distinction` | `constraints_vs_anti_patterns_distinction_visible` | -- | ALIGNED |

### Flags

1. **Minor MISMATCH: `patterns` vs `pattern_list_format`** -- Data uses plural `patterns`, display uses singular `pattern_list_format`. Convention inconsistency.

---

## 11. success_criteria

### DATA (`SuccessCriteria`)

| # | Field | Type |
|---|-------|------|
| 1 | `criteria` | SuccessCriteria1 (list of SuccessItem) |

`SuccessItem` sub-fields: `success_definition` (SuccessDefinition), `success_evidence` (SuccessEvidence, list of StringProse)

### CONTENT (`SuccessCriteriaContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `verification_guidance_suffix` | StringProse |
| 3 | `success_failure_independence_statement` | StringProse |
| 4 | `multi_criteria_transition` | StringText |
| 5 | `definition_framing_variant` | sub-model (declarative_assertion, conditional_gate, completion_identity) |
| 6 | `evidence_framing_variant` | sub-model (properties, verification_checklist, quality_signals) |
| 7 | `definition_to_evidence_transition_variant` | sub-model (goal_then_criteria, proof, dual_presentation) |

### STRUCTURE (`SuccessCriteriaStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `section_visible` | Boolean |
| 2 | `max_entries_rendered` | Integer |
| 3 | `definition_framing_variant` | enum |
| 4 | `evidence_framing_variant` | enum |
| 5 | `definition_to_evidence_transition_variant` | enum |
| 6 | `evidence_type_handling` | enum |
| 7 | `output_vs_agent_voice` | enum |
| 8 | `success_failure_independence_statement_visible` | Boolean |
| 9 | `verification_guidance_suffix_visible` | Boolean |
| 10 | `multi_criteria_relationship` | enum |

### DISPLAY (`SuccessCriteriaDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `evidence_format` | UnionFormatOrPair |
| 2 | `evidence_format_threshold` | Integer |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| criteria | `criteria` (list) | `multi_criteria_transition` | `max_entries_rendered`, `multi_criteria_relationship` | -- | ALIGNED |
| success_definition | `success_definition` (per item) | `definition_framing_variant` | `definition_framing_variant` | -- | ALIGNED |
| success_evidence | `success_evidence` (list per item) | `evidence_framing_variant` | `evidence_framing_variant`, `evidence_type_handling` | `evidence_format`, `evidence_format_threshold` | ALIGNED |
| definition_to_evidence_transition | -- | `definition_to_evidence_transition_variant` | `definition_to_evidence_transition_variant` | -- | ALIGNED |
| verification_guidance_suffix | -- | `verification_guidance_suffix` | `verification_guidance_suffix_visible` | -- | ALIGNED |
| success_failure_independence_statement | -- | `success_failure_independence_statement` | `success_failure_independence_statement_visible` | -- | ALIGNED |
| evidence_type_handling | -- | -- | `evidence_type_handling` | -- | ORPHAN in STRUCTURE |
| output_vs_agent_voice | -- | -- | `output_vs_agent_voice` | -- | ORPHAN in STRUCTURE |

### Flags

No significant mismatches. This section is well-aligned. The `evidence_type_handling` and `output_vs_agent_voice` structure fields are render-time behavioral controls that don't map to specific content templates (they modify how existing content is applied).

---

## 12. failure_criteria

### DATA (`FailureCriteria`)

| # | Field | Type |
|---|-------|------|
| 1 | `criteria` | FailureCriteria1 (list of FailureItem) |

`FailureItem` sub-fields: `failure_definition` (FailureDefinition), `failure_evidence` (FailureEvidence, list of StringProse)

### CONTENT (`FailureCriteriaContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `any_one_triggers_abort` | StringProse |
| 3 | `evidence_preamble` | StringProse |
| 4 | `cite_definition_and_evidence_postscript` | StringProse |
| 5 | `check_before_and_during` | StringProse |
| 6 | `abort_stance_variant` | FailureCriteriaAbortStanceVariantContent sub-model (preamble: obligation/permission, definition_label: obligation/permission) |

### STRUCTURE (`FailureCriteriaStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `section_visible` | Boolean |
| 2 | `max_entries_rendered` | Integer |
| 3 | `abort_stance_preamble_visible` | Boolean |
| 4 | `cite_definition_and_evidence_postscript_visible` | Boolean |
| 5 | `check_before_and_during_visible` | Boolean |
| 6 | `abort_stance_variant` | enum (optional) |

### DISPLAY (`FailureCriteriaDisplay`)

| # | Field | Type |
|---|-------|------|
| 1 | `evidence_format` | ListFormat enum |

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| criteria | `criteria` (list) | -- | `max_entries_rendered` | -- | ALIGNED |
| failure_definition | `failure_definition` (per item) | `abort_stance_variant.definition_label.*` | -- | -- | ALIGNED (content provides the label for how definitions render) |
| failure_evidence | `failure_evidence` (list per item) | `evidence_preamble` | -- | `evidence_format` | ALIGNED |
| abort_stance | -- | `abort_stance_variant` (sub-model) | `abort_stance_preamble_visible`, `abort_stance_variant` (enum) | -- | ALIGNED |
| any_one_triggers_abort | -- | `any_one_triggers_abort` | -- | -- | ORPHAN in CONTENT (no structure visibility toggle) |
| cite_definition_and_evidence_postscript | -- | `cite_definition_and_evidence_postscript` | `cite_definition_and_evidence_postscript_visible` | -- | ALIGNED |
| check_before_and_during | -- | `check_before_and_during` | `check_before_and_during_visible` | -- | ALIGNED |

### Flags

1. **ORPHAN**: `any_one_triggers_abort` in CONTENT has no STRUCTURE visibility toggle. It always renders (or requires hardcoded logic).

---

## 13. return_format

### DATA (`ReturnFormat`)

| # | Field | Type |
|---|-------|------|
| 1 | `mode` | ReturnMode enum |
| 2 | `return_schema` | PathExistsAbsolute (optional) |
| 3 | `status_instruction` | StringProse (optional) |
| 4 | `metrics_instruction` | StringProse (optional) |
| 5 | `output_instruction` | StringProse (optional) |

### CONTENT (`ReturnFormatContent`)

| # | Field | Type |
|---|-------|------|
| 1 | `heading` | StringText |
| 2 | `files_vs_status_explanation_preamble` | StringProse |
| 3 | `token_must_be_first_word_preamble` | StringProse |
| 4 | `token_must_be_first_word_tokens_three` | StringProse |
| 5 | `token_must_be_first_word_tokens_two` | StringProse |
| 6 | `report_completion_label` | StringText |
| 7 | `report_all_metrics_postscript` | StringProse |
| 8 | `abort_vs_failure_distinction_preamble` | StringProse |
| 9 | `honest_failure_over_dubious_success_preamble` | StringProse |
| 10 | `track_metrics_as_you_work_postscript` | StringProse |
| 11 | `track_metrics_as_you_work_antidrift` | StringProse |
| 12 | `do_not_fabricate_metrics_postscript` | StringProse |
| 13 | `failure_cross_reference_preamble` | StringProse |

### STRUCTURE (`ReturnFormatStructure`)

| # | Field | Type |
|---|-------|------|
| 1 | `files_vs_status_explanation_preamble_visible` | Boolean |
| 2 | `token_must_be_first_word_preamble_visible` | Boolean |
| 3 | `report_all_metrics_postscript_visible` | Boolean |
| 4 | `abort_vs_failure_distinction_preamble_visible` | Boolean |
| 5 | `honest_failure_over_dubious_success_preamble_visible` | Boolean |
| 6 | `track_metrics_as_you_work_postscript_visible` | Boolean |
| 7 | `do_not_fabricate_metrics_postscript_visible` | Boolean |
| 8 | `failure_cross_reference_preamble_visible` | Boolean |

### DISPLAY

No `ReturnFormatDisplay` model exists. The return_format section is absent from `AgentOutputDisplay`.

### Cross-axis alignment

| Concept | DATA | CONTENT | STRUCTURE | DISPLAY | Status |
|---------|------|---------|-----------|---------|--------|
| mode | `mode` | `token_must_be_first_word_tokens_three`, `token_must_be_first_word_tokens_two` | -- | -- | ALIGNED (content provides variants conditioned on mode) |
| return_schema | `return_schema` | -- | -- | -- | ORPHAN in DATA |
| status_instruction | `status_instruction` | -- | -- | -- | ORPHAN in DATA |
| metrics_instruction | `metrics_instruction` | -- | -- | -- | ORPHAN in DATA |
| output_instruction | `output_instruction` | -- | -- | -- | ORPHAN in DATA |
| files_vs_status_explanation_preamble | -- | `files_vs_status_explanation_preamble` | `files_vs_status_explanation_preamble_visible` | -- | ALIGNED |
| token_must_be_first_word_preamble | -- | `token_must_be_first_word_preamble` | `token_must_be_first_word_preamble_visible` | -- | ALIGNED |
| report_completion_label | -- | `report_completion_label` | -- | -- | ORPHAN in CONTENT (no structure visibility toggle) |
| report_all_metrics_postscript | -- | `report_all_metrics_postscript` | `report_all_metrics_postscript_visible` | -- | ALIGNED |
| abort_vs_failure_distinction_preamble | -- | `abort_vs_failure_distinction_preamble` | `abort_vs_failure_distinction_preamble_visible` | -- | ALIGNED |
| honest_failure_over_dubious_success_preamble | -- | `honest_failure_over_dubious_success_preamble` | `honest_failure_over_dubious_success_preamble_visible` | -- | ALIGNED |
| track_metrics_as_you_work_postscript | -- | `track_metrics_as_you_work_postscript` | `track_metrics_as_you_work_postscript_visible` | -- | ALIGNED |
| track_metrics_as_you_work_antidrift | -- | `track_metrics_as_you_work_antidrift` | -- | -- | ORPHAN in CONTENT (no structure visibility toggle) |
| do_not_fabricate_metrics_postscript | -- | `do_not_fabricate_metrics_postscript` | `do_not_fabricate_metrics_postscript_visible` | -- | ALIGNED |
| failure_cross_reference_preamble | -- | `failure_cross_reference_preamble` | `failure_cross_reference_preamble_visible` | -- | ALIGNED |

### Flags

1. **ORPHAN**: `report_completion_label` in CONTENT has no STRUCTURE visibility toggle.
2. **ORPHAN**: `track_metrics_as_you_work_antidrift` in CONTENT has no STRUCTURE visibility toggle.
3. **ORPHAN**: `token_must_be_first_word_tokens_three` and `token_must_be_first_word_tokens_two` in CONTENT have no STRUCTURE visibility toggles (they are selected by mode, not toggled).
4. **MISSING DISPLAY**: No display model for return_format. No formatting controls.
5. Many DATA fields are orphans (return_schema, status_instruction, metrics_instruction, output_instruction) -- these are inserted directly into the rendered prompt.

---

## Summary of Issues

### Sections missing from DISPLAY axis entirely

| Section | Has DISPLAY model? |
|---------|-------------------|
| input | No |
| output | No |
| writing_output | No |
| return_format | No |

### Sections missing from CONTENT/STRUCTURE axes entirely

| Section | Has CONTENT model? | Has STRUCTURE model? |
|---------|-------------------|---------------------|
| input | No | No |

### Trunk name mismatches

| # | Section | DATA trunk | Other-axis trunk | Axes affected | Severity |
|---|---------|-----------|-----------------|---------------|----------|
| 1 | identity | `role_expertise` | `expertise_*` | CONTENT, STRUCTURE, DISPLAY | Medium -- consistent `role_` prefix dropped |
| 2 | critical_rules | `workspace_path` (from security_boundary) | `workspace_confinement` (CONTENT/STRUCTURE) vs `workspace_path_format` (DISPLAY) | CONTENT, STRUCTURE, DISPLAY | Medium -- rule-name vs value-name split |
| 3 | critical_rules | `tool_name` | `output_tool_exclusivity` (CONTENT/STRUCTURE) vs `tool_name_format` (DISPLAY) | CONTENT, STRUCTURE, DISPLAY | Medium -- same pattern as above |
| 4 | critical_rules | `batch_size` | `batch_discipline` (CONTENT/STRUCTURE) vs `batch_size_format` (DISPLAY) | CONTENT, STRUCTURE, DISPLAY | Medium -- same pattern as above |
| 5 | instructions | `instruction_mode` (deterministic/probabilistic) | `exact_vs_judgment` | CONTENT, STRUCTURE, DISPLAY | High -- completely different vocabulary |
| 6 | instructions | -- | `structural_complexity_override` (STRUCTURE) vs `scaffolding_tier_*` (DISPLAY) | STRUCTURE, DISPLAY | Medium |
| 7 | examples | `example_heading` | `entry_heading` | CONTENT, DISPLAY | Medium |
| 8 | output | `description` | `output_description` | CONTENT | Low -- disambiguation prefix |
| 9 | writing_output | `tool_name` | `tool_identity_label` | CONTENT | Medium |
| 10 | constraints | `rules` | `enumeration_format` | DISPLAY | Medium -- no trunk overlap |
| 11 | anti_patterns | `patterns` (plural) | `pattern_list_format` (singular) | DISPLAY | Low -- singular vs plural |

### Content fields missing structure visibility toggles (always-render or hardcoded)

| # | Section | Content field | Has `_visible` in STRUCTURE? |
|---|---------|--------------|------------------------------|
| 1 | identity | `declaration_heuristic_postscript` | No |
| 2 | constraints | `hierarchy_tier_comparison` | No |
| 3 | constraints | `hierarchy_three_tier_explanation` | No |
| 4 | failure_criteria | `any_one_triggers_abort` | No |
| 5 | return_format | `report_completion_label` | No |
| 6 | return_format | `track_metrics_as_you_work_antidrift` | No |
| 7 | return_format | `token_must_be_first_word_tokens_three` | No |
| 8 | return_format | `token_must_be_first_word_tokens_two` | No |

### Data list fields missing display format controls

| # | Section | DATA list field | Has display `*_format`? |
|---|---------|----------------|------------------------|
| 1 | identity | `role_expertise` | Yes (`expertise_format`) |
| 2 | constraints | `rules` | Yes (`enumeration_format`) -- but mismatched trunk |
| 3 | anti_patterns | `patterns` | Yes (`pattern_list_format`) |
| 4 | success_criteria | `success_evidence` | Yes (`evidence_format`) |
| 5 | failure_criteria | `failure_evidence` | Yes (`evidence_format`) |
| 6 | examples | `example_entries` | Partial (has `entry_heading_format`, `entry_body_container`, `entry_separator`) |
| 7 | instructions | `steps` | Yes (`step_header_format`, `step_body_container`) |
| 8 | input | everything | No -- no display model at all |
| 9 | return_format | everything | No -- no display model at all |
