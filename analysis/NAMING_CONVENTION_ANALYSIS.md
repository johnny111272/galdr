# Naming Convention Analysis: Cross-Axis Field Matching

Analysis of whether field names across the four axes (data, content, structure, display) can be mechanically matched by a composition engine.

---

## 1. Intended Naming Convention (from Design Docs)

TOML_ARCHITECTURE.md establishes the following conventions:

- **Content fields** use positional suffixes: `_heading`, `_preamble`, `_label`, `_postscript`, `_transition`. These encode WHERE the prose appears relative to data.
- **Structure fields** use `_visible` suffix for boolean toggles, `_variant` suffix for variant selectors, and `_override` suffix for data overrides.
- **Display fields** use `_format` suffix for list formatting enums and `_format_threshold` for count-based switching.
- **Data fields** use domain-specific names with NO positional suffixes.

The **intended cross-reference** mechanism is a shared "trunk" (root name). The worked example in the doc shows:

| Axis | Field | Trunk |
|---|---|---|
| content | `expertise_label` | `expertise` |
| content | `expertise_is_strictly_limited_postscript` | `expertise_is_strictly_limited` |
| data | `role_expertise` | ??? |
| structure | `expertise_is_strictly_limited_postscript_visible` | `expertise_is_strictly_limited` |
| display | `expertise_format` | `expertise` |

The trunk word "expertise" connects content and display. But the data field is `role_expertise`, not `expertise`. The `role_` prefix breaks mechanical matching.

---

## 2. Section-by-Section Field Alignment

### IDENTITY

#### Data fields (IdentityAnthropic):
| Data Field | Type | Used As |
|---|---|---|
| `title` | AgentTitle (scalar) | Template placeholder `{{title}}` |
| `description` | AgentDescription (scalar) | Template placeholder (frontmatter, not identity section) |
| `role_identity` | StringText (scalar) | Template placeholder `{{role_identity}}` |
| `role_responsibility` | RoleResponsibility (scalar) | Template placeholder `{{role_responsibility}}` |
| `model` | AnthropicModel (enum) | Not used in identity content |
| `role_description` | RoleDescription (scalar, optional) | No direct content reference; rendered as prose block |
| `role_expertise` | RoleExpertise (LIST, optional) | Rendered as list entries |

#### Content fields (IdentityContent):
| Content Field | Trunk | References Data |
|---|---|---|
| `heading` | (section heading) | `{{title}}` |
| `declaration` | `declaration` | `{{role_identity}}` |
| `declaration_heuristic_postscript` | `declaration_heuristic` | `{{role_identity}}` |
| `responsibility_label` | `responsibility` | `{{role_responsibility}}` |
| `expertise_label` | `expertise` | (introduces role_expertise list) |
| `expertise_is_strictly_limited_postscript` | `expertise_is_strictly_limited` | (references expertise list) |
| `closing_identity_reminder` | `closing_identity_reminder` | `{{role_identity}}` |

#### Structure fields (IdentityStructure):
| Structure Field | Trunk |
|---|---|
| `field_ordering` | (section-level) |
| `fuse_declaration_and_role_description` | `declaration` + `role_description` |
| `expertise_is_strictly_limited_postscript_visible` | `expertise_is_strictly_limited_postscript` |
| `closing_identity_reminder_visible` | `closing_identity_reminder` |
| `bold_contrast_phrase_from_role_description_visible` | `role_description` |

#### Display fields (IdentityDisplay):
| Display Field | Trunk |
|---|---|
| `expertise_format` | `expertise` |
| `expertise_format_threshold` | `expertise` |
| `responsibility_format` | `responsibility` |
| `responsibility_format_threshold` | `responsibility` |

#### Alignment Analysis:

**CLEAN alignments (trunk matches across axes):**
- `closing_identity_reminder`: content `closing_identity_reminder` <-> structure `closing_identity_reminder_visible`. Clean.
- `expertise_is_strictly_limited_postscript`: content field <-> structure `_visible` toggle. Clean.

**BROKEN alignments:**
- **`expertise` trunk**: content has `expertise_label`, display has `expertise_format`, but data has `role_expertise`. The `role_` prefix prevents matching.
- **`responsibility` trunk**: content has `responsibility_label`, display has `responsibility_format`, but data has `role_responsibility`. Same problem.
- **`declaration` trunk**: content has `declaration` and `declaration_heuristic_postscript`. Data placeholder is `{{role_identity}}`. The data field name (`role_identity`) shares no trunk with `declaration`.
- **`title` trunk**: content heading uses `{{title}}`, data field is `title`. This one works but `title` is a section heading, not a sub-block concept.
- **`role_description` trunk**: structure has `fuse_declaration_and_role_description` and `bold_contrast_phrase_from_role_description_visible`. Data has `role_description`. Content has no explicit field. The `role_` prefix is IN the structure field here, which is inconsistent with the content/display fields that use bare `expertise`/`responsibility`.

### SECURITY_BOUNDARY

#### Data fields (SecurityBoundaryAnthropic):
| Data Field | Type |
|---|---|
| `workspace_path` | PathExistsAbsolute (scalar) |
| `display` | DisplayEntries (LIST of DisplayEntry, optional) |

#### Content fields (SecurityBoundaryContent):
| Content Field | Trunk |
|---|---|
| `filesystem_map_intro` | `filesystem_map_intro` |
| `section_closing` | `section_closing` |
| `compound_entry_template` | `compound_entry` |
| `grouped_tool_header` | `grouped_tool` |
| `framing_variant` | (shared variant: heading, workspace_path_declaration, section_preamble) |

#### Structure fields (SecurityBoundaryStructure):
| Structure Field | Trunk |
|---|---|
| `fuse_workspace_path_and_resolver` | `workspace_path` |
| `filesystem_map_intro_visible` | `filesystem_map_intro` |
| `section_preamble_visible` | `section_preamble` |
| `section_closing_visible` | `section_closing` |
| `tool_names_visible` | `tool_names` |
| `framing_variant` | `framing_variant` |

#### Display fields (SecurityBoundaryDisplay):
| Display Field | Trunk |
|---|---|
| `path_style` | `path` |
| `uniform_toolset_format` | `uniform_toolset` |
| `heterogeneous_toolset_format` | `heterogeneous_toolset` |
| `filesystem_map_intro_visibility_threshold` | `filesystem_map_intro` |
| `entry_list_format` | `entry_list` |

#### Alignment Analysis:
- `filesystem_map_intro`: content <-> structure `_visible` <-> display `_visibility_threshold`. **Clean.**
- `section_closing`: content <-> structure `_visible`. **Clean.**
- `workspace_path`: data `workspace_path` <-> structure `fuse_workspace_path_and_resolver`. **Clean.**
- `display` (data field for the list of entries): no matching trunk in content. The content fields that wrap display entries are `compound_entry_template` and `grouped_tool_header`. **No trunk match** -- the data field is called `display`, the content fields reference "entry" and "tool."
- `framing_variant`: structure selector <-> content variant table. **Clean.**

### CRITICAL_RULES

#### Data fields (CriticalRules):
| Data Field | Type |
|---|---|
| `has_output_tool` | Boolean (scalar) |
| `tool_name` | ToolName (scalar, optional) |
| `name_needed` | OutputToolNameNeeded (scalar, optional) |
| `batch_size` | OutputToolBatchSize (scalar, optional) |

#### Content fields (CriticalRulesContent):
| Content Field | References Data |
|---|---|
| `heading` | (none) |
| `authority_preamble` | (none) |
| `workspace_confinement` | `{{workspace_path}}` |
| `output_tool_exclusivity` | `{{tool_name}}` |
| `batch_discipline` | `{{batch_size}}`, `{{tool_name}}` |
| `fail_fast` | (none) |
| `input_is_your_only_source` | (none) |
| `no_invention` | (none) |
| `discipline_over_helpfulness` | (none) |
| `rule_count_awareness_prelude` | `{{rule_count}}` (computed) |

#### Structure fields (CriticalRulesStructure):
| Structure Field | Trunk |
|---|---|
| `authority_preamble_visible` | `authority_preamble` |
| `rule_count_awareness_prelude_visible` | `rule_count_awareness_prelude` |
| `rule_count_awareness_prelude_auto_threshold` | `rule_count_awareness_prelude` |
| `workspace_confinement_visible` | `workspace_confinement` |
| `fail_fast_visible` | `fail_fast` |
| `input_is_your_only_source_visible` | `input_is_your_only_source` |
| `no_invention_visible` | `no_invention` |
| `output_tool_exclusivity_visible` | `output_tool_exclusivity` |
| `batch_discipline_visible` | `batch_discipline` |
| `discipline_over_helpfulness_visible` | `discipline_over_helpfulness` |
| `rule_presentation` | (section-level) |
| `internal_hierarchy` | (section-level) |

#### Alignment Analysis:
Critical rules content fields are designed prose fragments, not data-wrapping templates. Each content field has a matching structure `_visible` toggle with the same trunk. **All content-structure pairs are clean.** Data fields are referenced only inside `{{placeholders}}` -- there is no trunk-based matching needed because the composition engine resolves placeholders, not field-to-field pairing.

Display fields control inline formatting of the data values themselves (`workspace_path_format`, `tool_name_format`, `batch_size_format`). These use the **data field name** as trunk: `workspace_path`, `tool_name`, `batch_size`. **Clean match to data field names.**

### INSTRUCTIONS

#### Data fields (Instructions):
| Data Field | Type |
|---|---|
| `steps` | ExecutionInstructions (LIST of InstructionStep) |

Each InstructionStep has: `instruction_mode` (enum), `instruction_text` (markdown).

#### Alignment Analysis:
Instructions is a hybrid section. The data is a list of steps. Content fields are step header templates and preamble components. There is no per-step data-content trunk matching -- the engine iterates the list and applies templates. **No trunk-matching problem.** Computed values (`step_count`, `step_n`, `step_total`, `midpoint`) are derived at render time.

### EXAMPLES

#### Data fields (Examples):
| Data Field | Type |
|---|---|
| `groups` | ExecutionExamples (LIST of ExampleGroup) |

Each ExampleGroup has: `example_group_name`, `example_display_headings`, `examples_max_number`, `example_entries` (LIST of ExampleEntry with `example_heading`, `example_text`).

#### Alignment Analysis:
Examples data has `example_display_headings` and `examples_max_number`. Structure has `example_display_headings_override`, `examples_max_number_override`, `example_display_headings`, `examples_max_number`. Content has `entry_heading` template with `{{example_heading}}`. Display has `entry_heading_format`.

The content field is `entry_heading` but the data field is `example_heading`. The display field is `entry_heading_format`. Content and display align on trunk `entry_heading`, but data uses `example_heading`. **Mismatch.**

### GUARDRAILS FAMILY (constraints, anti_patterns, success_criteria, failure_criteria)

#### Constraints:
- Data: `rules` (LIST of GuardrailsConstraint)
- Content: `heading`, `constraints_are_not_steps`, `constraint_count_heading`, `hierarchy_tier_comparison`, `hierarchy_three_tier_explanation`, plus 3 variant tables
- Structure: `section_visible`, `max_entries_rendered`, plus visibility toggles and variant selectors
- Display: `enumeration_format`, `enumeration_format_threshold`, plus thresholds and normalization

Data field is `rules`. Display field trunk is `enumeration`. Content field trunk is `constraint_count` for the count heading. **No trunk alignment** between data `rules` and display `enumeration_format`.

#### Anti-Patterns:
- Data: `patterns` (LIST of GuardrailsAntiPattern)
- Display: `pattern_list_format`

Data trunk: `patterns`. Display trunk: `pattern_list`. **Partial match** -- `pattern` is shared but not exact.

#### Success Criteria:
- Data: `criteria` (LIST of SuccessItem, each with `success_definition` + `success_evidence` LIST)
- Display: `evidence_format`, `evidence_format_threshold`

The display field governs the evidence sub-list format with trunk `evidence`. The data sub-field is `success_evidence`. **Partial match** -- `evidence` is shared.

#### Failure Criteria:
- Data: `criteria` (LIST of FailureItem, each with `failure_definition` + `failure_evidence` LIST)
- Display: `evidence_format`

Same pattern as success criteria. Trunk `evidence` shared. **Partial match.**

### OUTPUT

- Data: `description` (scalar), `format` (enum), `name_known` (enum), `schema_path` (scalar), `output_file` (scalar), `output_directory` (scalar), `name_template` (scalar), `name_instruction` (scalar), `schema_embed` (boolean)
- Content: `heading`, `output_description` template (uses `{{DESCRIPTION}}`), `format_declaration` (uses `{{FORMAT}}`), `schema_embedded_preamble`, `schema_reference` (uses `{{SCHEMA_PATH}}`), `directory_location_variant`
- Structure: `schema_embed`, `directory_location_variant`

Content field `output_description` references data field `description` via `{{DESCRIPTION}}`. Trunk mismatch: content uses `output_description`, data uses `description`. The content field had to add the `output_` prefix for disambiguation since `description` is too generic.

### WRITING_OUTPUT

- Data: `tool_name`, `invocation_variant`, `invocation_display`, `name_needed`, `name_pattern`, `batch_size`, `schema_path`, `file_path`, `directory_path`
- Content: `heading`, `transition_preamble`, `tool_mandate`, `tool_identity_label` (uses `{{TOOL_NAME}}`), `invocation_preamble`, `heredoc_explanation`
- Structure: `transition_preamble_visible`, `tool_mandate_visible`, `heredoc_explanation_visible`

Content-structure pairs are clean (`transition_preamble`, `tool_mandate`, `heredoc_explanation`).

### RETURN_FORMAT

- Data: `mode` (enum), `return_schema` (scalar), `status_instruction` (scalar), `metrics_instruction` (scalar), `output_instruction` (scalar)
- Content: many prose fields
- Structure: visibility toggles for each content field

Content-structure pairs are clean (shared trunks with `_visible` suffix).

### INPUT

Input section has no content, structure, or display model -- it is not present in the output_content, output_structure, or output_display models. Input rendering is currently handled differently (possibly entirely data-driven or not yet extracted to the control surface architecture).

---

## 3. Specific Renames for Mechanical Matchability

### Identity Data Fields

These are the critical renames. The data model uses `role_` prefixes that break trunk matching.

| Current Data Field | Rename To | Rationale |
|---|---|---|
| `role_expertise` | `expertise` | Matches content `expertise_label`, display `expertise_format` |
| `role_responsibility` | `responsibility` | Matches content `responsibility_label`, display `responsibility_format` |
| `role_identity` | `identity_declaration_value` OR keep as-is | This is a template placeholder `{{role_identity}}` used inside content `declaration`. The trunk is `declaration`, not `identity`. But renaming this is complex -- see discussion below. |
| `role_description` | `description_extended` OR keep as-is | Used in structure `fuse_declaration_and_role_description` and `bold_contrast_phrase_from_role_description_visible`. If renamed, structure fields need updating too. |

**Recommended approach**: Rename `role_expertise` to `expertise` and `role_responsibility` to `responsibility`. These are the two fields where trunk matching is needed for list formatting. Leave `role_identity` and `role_description` as-is because they are scalar template placeholders referenced by `{{name}}` syntax, not by trunk matching.

### Guardrails Data Fields

| Current Data Field | Rename To | Rationale |
|---|---|---|
| Constraints: `rules` | `constraints` | Matches section name. Display could then use `constraints_format`. |
| Anti-Patterns: `patterns` | `anti_patterns` | Matches section name. Display `pattern_list_format` would become `anti_patterns_format`. |
| SuccessCriteria: `criteria` | `success_criteria` OR keep `criteria` | Inner field names `success_definition` and `success_evidence` already carry the section prefix. |
| FailureCriteria: `criteria` | `failure_criteria` OR keep `criteria` | Same as above. |

### Display Field Renames (if data fields are NOT renamed)

If data field names cannot change (schema stability), the display fields could be renamed instead:

| Current Display Field | Rename To | Rationale |
|---|---|---|
| Constraints: `enumeration_format` | `rules_format` | Match data `rules` |
| Anti-Patterns: `pattern_list_format` | `patterns_format` | Match data `patterns` |

### Examples Data/Content Alignment

| Field | Current | Rename To |
|---|---|---|
| Content: `entry_heading` | `entry_heading` | `example_heading` (match data) |
| Display: `entry_heading_format` | `entry_heading_format` | `example_heading_format` (match data) |

OR rename data field `example_heading` to `entry_heading`.

---

## 4. Field Classification: Scalars (Template Placeholders) vs Lists (Need Formatting)

### IDENTITY

| Data Field | Classification | How Used |
|---|---|---|
| `title` | **SCALAR/TEMPLATE** | `{{title}}` in heading template |
| `description` | **SCALAR/TEMPLATE** | Used in frontmatter, not in identity section rendering |
| `role_identity` | **SCALAR/TEMPLATE** | `{{role_identity}}` in declaration, postscript, reminder |
| `role_responsibility` | **SCALAR/TEMPLATE** (but see note) | `{{role_responsibility}}` in responsibility_label. Display has `responsibility_format`, suggesting this CAN be a list in some agents. Ambiguous. |
| `model` | **SCALAR/ENUM** | Not rendered in identity section |
| `role_description` | **SCALAR/PROSE** | Rendered as a prose block, no template wrapping |
| `role_expertise` | **LIST** | Rendered as formatted list (bulleted/inline/etc.) |

Note: `role_responsibility` is typed as `RoleResponsibility` (a single StringProse), but display has `responsibility_format` with threshold-based switching. This suggests the engine may split a single prose value into multiple items, OR the schema will evolve to allow a list here. Currently it is a scalar with a display format field -- this is a **design inconsistency**.

### SECURITY_BOUNDARY

| Data Field | Classification |
|---|---|
| `workspace_path` | **SCALAR/TEMPLATE** -- used in `{{WORKSPACE_PATH}}` |
| `display` | **LIST** -- security grant entries rendered as formatted list |

### CRITICAL_RULES

| Data Field | Classification |
|---|---|
| `has_output_tool` | **SCALAR/BOOLEAN** -- data gate, not rendered as text |
| `tool_name` | **SCALAR/TEMPLATE** -- `{{tool_name}}` in rule templates |
| `name_needed` | **SCALAR/BOOLEAN** -- data gate |
| `batch_size` | **SCALAR/TEMPLATE** -- `{{batch_size}}` in batch_discipline |

### INSTRUCTIONS

| Data Field | Classification |
|---|---|
| `steps` | **LIST** -- iterated, each step rendered with templates |

### EXAMPLES

| Data Field | Classification |
|---|---|
| `groups` | **LIST OF LISTS** -- groups contain entries |

### CONSTRAINTS

| Data Field | Classification |
|---|---|
| `rules` | **LIST** -- rendered as formatted constraint list |

### ANTI_PATTERNS

| Data Field | Classification |
|---|---|
| `patterns` | **LIST** -- rendered as formatted pattern list |

### SUCCESS_CRITERIA

| Data Field | Classification |
|---|---|
| `criteria` | **LIST** -- each item contains `success_definition` (scalar) + `success_evidence` (LIST) |

### FAILURE_CRITERIA

| Data Field | Classification |
|---|---|
| `criteria` | **LIST** -- each item contains `failure_definition` (scalar) + `failure_evidence` (LIST) |

### OUTPUT

| Data Field | Classification |
|---|---|
| `description` | **SCALAR/TEMPLATE** -- `{{DESCRIPTION}}` |
| `format` | **SCALAR/TEMPLATE** -- `{{FORMAT}}` |
| `name_known` | **SCALAR/ENUM** -- branches rendering logic |
| `schema_path` | **SCALAR/TEMPLATE** -- `{{SCHEMA_PATH}}` |
| `output_file` | **SCALAR** -- rendered when present |
| `output_directory` | **SCALAR/TEMPLATE** -- `{{OUTPUT_DIRECTORY}}` |
| `name_template` | **SCALAR** -- rendered when present |
| `name_instruction` | **SCALAR** -- rendered when present |
| `schema_embed` | **SCALAR/BOOLEAN** -- branches rendering |

### WRITING_OUTPUT

| Data Field | Classification |
|---|---|
| `tool_name` | **SCALAR/TEMPLATE** -- `{{TOOL_NAME}}` |
| `invocation_variant` | **SCALAR/ENUM** -- branches rendering |
| `invocation_display` | **SCALAR/PROSE** -- rendered as code block |
| `name_needed` | **SCALAR/BOOLEAN** -- branches rendering |
| `name_pattern` | **SCALAR** -- rendered when present |
| `batch_size` | **SCALAR** -- rendered when present |
| `schema_path` | **SCALAR** -- rendered when present |
| `file_path` | **SCALAR** -- rendered when present |
| `directory_path` | **SCALAR** -- rendered when present |

### RETURN_FORMAT

| Data Field | Classification |
|---|---|
| `mode` | **SCALAR/ENUM** -- drives which instruction blocks render |
| `return_schema` | **SCALAR** -- embedded or referenced |
| `status_instruction` | **SCALAR/PROSE** -- rendered when mode includes status |
| `metrics_instruction` | **SCALAR/PROSE** -- rendered when mode includes metrics |
| `output_instruction` | **SCALAR/PROSE** -- rendered when mode includes output |

---

## 5. List Fields vs Display Format Coverage

### Fields that are LISTS and need formatting:

| Section | Data List Field | Display Format Field | Covered? |
|---|---|---|---|
| Identity | `role_expertise` | `expertise_format` + threshold | YES (trunk mismatch: `role_expertise` vs `expertise`) |
| Identity | `role_responsibility` (scalar but has format) | `responsibility_format` + threshold | ANOMALOUS -- data is scalar, display treats as list |
| Security Boundary | `display` (entries) | `entry_list_format`, `uniform_toolset_format`, `heterogeneous_toolset_format` | YES (no trunk alignment, but covered) |
| Instructions | `steps` | `step_header_format`, `step_body_container` | YES (per-item rendering, not list format) |
| Examples | `groups[].example_entries` | `entry_heading_format`, `entry_body_container`, `entry_separator` | YES |
| Constraints | `rules` | `enumeration_format` + threshold | YES (trunk mismatch: `rules` vs `enumeration`) |
| Anti-Patterns | `patterns` | `pattern_list_format` | YES (trunk mismatch: `patterns` vs `pattern_list`) |
| Success Criteria | `criteria[].success_evidence` | `evidence_format` + threshold | YES (partial trunk: `success_evidence` vs `evidence`) |
| Failure Criteria | `criteria[].failure_evidence` | `evidence_format` | YES (partial trunk: `failure_evidence` vs `evidence`) |

### Missing display format fields:

**None are truly missing.** Every list has a format control. But the trunk names do not align mechanically in several cases.

### `role_responsibility` anomaly:

`role_responsibility` is defined as a single `RoleResponsibility` (StringProse) -- a scalar. But display has `responsibility_format` with threshold-based switching. Either:
1. The schema will evolve to make responsibility a list, OR
2. The display field is preemptive (designed for a future list type), OR
3. The engine splits a single prose string into sub-items

This needs resolution. If responsibility stays scalar, `responsibility_format` and `responsibility_format_threshold` in display are dead fields.

---

## 6. Proposed Mechanical Matching Rule

### The Rule

Given a content field name like `expertise_label`, the composition engine derives sibling fields as follows:

```
CONTENT field:  {trunk}_{position_suffix}
                e.g., expertise_label

DATA field:     {trunk}
                e.g., expertise

DISPLAY field:  {trunk}_format
                e.g., expertise_format

STRUCTURE field (visibility): {content_field_name}_visible
                e.g., expertise_label_visible (if toggled)
                OR {trunk}_{position_suffix}_visible for postscripts
```

### Derivation Steps

1. **Strip the positional suffix** from the content field name to get the trunk:
   - Known suffixes: `_heading`, `_preamble`, `_label`, `_postscript`, `_transition`, `_template`, `_closing`
   - `expertise_label` -> trunk = `expertise`
   - `expertise_is_strictly_limited_postscript` -> trunk = `expertise_is_strictly_limited`

2. **Data field** = trunk (exact match):
   - Trunk `expertise` -> data field `expertise`
   - Trunk `responsibility` -> data field `responsibility`

3. **Display format field** = `{trunk}_format`:
   - Trunk `expertise` -> display field `expertise_format`

4. **Display threshold field** = `{trunk}_format_threshold`:
   - Trunk `expertise` -> display field `expertise_format_threshold`

5. **Structure visibility toggle** = `{full_content_field_name}_visible`:
   - Content field `expertise_is_strictly_limited_postscript` -> structure field `expertise_is_strictly_limited_postscript_visible`

### When the Rule Does NOT Apply

- **Template placeholders** (`{{role_identity}}`): These reference data fields by explicit name inside the template string. The engine resolves them by string interpolation, not by trunk matching. No rename needed.
- **Designed prose** (critical rules content fields like `workspace_confinement`, `fail_fast`): These are hand-authored prose, not data-wrapping. Their structure pairing is the `_visible` toggle on the full field name.
- **Variant selectors**: Structure `framing_variant` -> content `framing_variant` sub-table. Matched by exact name, not trunk derivation.
- **Section-level fields**: `heading`, `section_preamble`, `section_closing` are section-level concepts, not data-wrapping.

### Required Renames to Make the Rule Work

For the rule above to function mechanically, these renames are needed:

**Data model (anthropic_render.py):**
1. `role_expertise` -> `expertise` (in IdentityAnthropic)
2. `role_responsibility` -> `responsibility` (in IdentityAnthropic) -- only if it becomes a list

**Display model (output_display.py):**
3. Constraints: `enumeration_format` -> `rules_format` (match data `rules`)
4. Constraints: `enumeration_format_threshold` -> `rules_format_threshold`
5. Anti-Patterns: `pattern_list_format` -> `patterns_format` (match data `patterns`)

**Content model (output_content.py):**
6. Examples: `entry_heading` -> `example_heading` (match data field in ExampleEntry)

**Display model (output_display.py):**
7. Examples: `entry_heading_format` -> `example_heading_format` (match data)

OR alternatively, if the data model is the source of truth and harder to change, rename ALL other axes to match the data. But the data names (`role_expertise`, `role_responsibility`) are the least natural trunks -- they contain domain context (`role_`) that the other axes do not need.

### Template Placeholder Convention

For scalar data fields consumed via `{{placeholder}}`, the placeholder name MUST match the data field name exactly:
- `{{title}}` -> data field `title`
- `{{role_identity}}` -> data field `role_identity`
- `{{workspace_path}}` -> data field `workspace_path`
- `{{tool_name}}` -> data field `tool_name`
- `{{batch_size}}` -> data field `batch_size`

These are resolved by direct name lookup, not trunk derivation. The composition engine needs two distinct resolution paths:
1. **Trunk matching** for list data -> content label -> display format connections
2. **Direct name matching** for `{{placeholder}}` -> scalar data field lookups

---

## Summary of Findings

1. **Content <-> Structure matching is already clean.** Every content field that has a visibility toggle uses the exact content field name with `_visible` appended.

2. **Content <-> Display matching is mostly clean** where the trunk convention is followed (identity `expertise`, `responsibility`).

3. **Data <-> Content/Display matching is broken** in the identity section due to `role_` prefixes on data fields.

4. **Guardrails data field names diverge from display field names** (`rules` vs `enumeration`, `patterns` vs `pattern_list`).

5. **The `role_responsibility` scalar-vs-list ambiguity** needs resolution before the engine can reliably determine whether to apply list formatting.

6. **Two resolution mechanisms are needed**: trunk-based matching for list-wrapping compositions, and direct name lookup for template placeholder interpolation. These are fundamentally different operations and should not be conflated.
