# Data Model Knobs v2 — Composition Engine Design Reference

**Purpose:** Exhaustive field inventory and style/display knob assignments for all 14 sections + dispatcher.
Each section entry lists every data field, its Python type, classification, and all knobs that serve a real rendering purpose.

**Axes:**
- **data** — field values from the validated Pydantic model (anthropic_render.toml)
- **style** — non-data text: labels, templates, prose, headings, footers, omit behavior
- **display** — how arrays/collections are formatted: mode, separator, item_template

**Corrections applied:** See task brief — no re-discovery of established decisions.

---

## Table of Contents

1. [frontmatter](#1-frontmatter)
2. [identity](#2-identity)
3. [security_boundary](#3-security_boundary)
4. [input](#4-input)
5. [instructions](#5-instructions)
6. [examples](#6-examples)
7. [output](#7-output)
8. [writing_output](#8-writing_output)
9. [constraints](#9-constraints)
10. [anti_patterns](#10-anti_patterns)
11. [success_criteria](#11-success_criteria)
12. [failure_criteria](#12-failure_criteria)
13. [return_format](#13-return_format)
14. [critical_rules](#14-critical_rules)
15. [dispatcher](#15-dispatcher-fixed-structure)

---

## 1. frontmatter

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `name` | `AgentTitle` (TitleString) | scalar, required | Human-readable title, e.g. "Agent Builder" |
| `description` | `AgentDescription` (StringProse) | scalar, required | One-line purpose statement |
| `model` | `AnthropicModel` (Enum: haiku/sonnet/opus/inherit) | scalar, required | Model tier |
| `permission_mode` | `PermissionMode` (Enum: bypassPermissions) | scalar, required | Currently only one value exists |
| `tools` | `FrontmatterTools` (list[PascalString]) | array, required, min 1 | Claude Code tool names |
| `hooks.output_tool` | `OutputToolName \| None` | scalar, optional | Resolved output tool binary name |
| `hooks.tool_entries` | `ToolPathEntries \| None` (list[ToolPathEntry]) | array of objects, optional | Per-tool path grants |
| `hooks.tool_entries[i].tool` | `ToolNameAnthropic` (Enum) | scalar | Read/Grep/Glob/Write/Edit/Bash |
| `hooks.tool_entries[i].paths` | `PathPrefixes` (list[PathAbsolute]) | array | Absolute path prefixes |
| `hooks.command_entries` | `CommandPathEntries \| None` (list[CommandPathEntry]) | array of objects, optional | Per-command path grants |
| `hooks.command_entries[i].command` | `CommandNameUnix` (Enum) | scalar | find/ls/du/wc/stat/diff/tree |
| `hooks.command_entries[i].paths` | `PathPrefixes` (list[PathAbsolute]) | array | Absolute path prefixes |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Agent Configuration" |
| `heading_level` | H level (default H2) |
| `name_label` | Label for name field, e.g. "Name:" or omit entirely |
| `description_label` | Label for description field, e.g. "Purpose:" |
| `model_label` | Label for model field, e.g. "Model:" |
| `permission_label` | Label for permission_mode field, e.g. "Permissions:" |
| `tools_label` | Label for tools array, e.g. "Tools:" |
| `hooks_heading` | Sub-heading for hooks block, e.g. "Hook Enforcement" |
| `hooks_omit_if_none` | Whether to suppress the hooks block entirely when all hook fields are null |
| `output_tool_label` | Label for output_tool, e.g. "Output Tool:" |
| `tool_entries_label` | Label for tool_entries block |
| `command_entries_label` | Label for command_entries block |
| `path_prefix_label` | Label/prefix for each path line, e.g. "  -" or blank |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `tools_mode` | `tools` array | bulleted / inline |
| `tools_separator` | `tools` when inline | e.g. `", "` |
| `tool_entries_mode` | `tool_entries` array | sequential / bulleted |
| `tool_entry_paths_mode` | paths within each tool_entry | bulleted / inline |
| `tool_entry_paths_separator` | paths when inline | e.g. `", "` |
| `command_entries_mode` | `command_entries` array | sequential / bulleted |
| `command_entry_paths_mode` | paths within each command_entry | bulleted / inline |

### Design Notes

- The frontmatter section renders as TOML/YAML frontmatter, not markdown prose. The style knobs above assume markdown rendering. If the output format is a TOML frontmatter block, the knobs collapse to structural delimiters only.
- `hooks` is a nested object. Three sub-fields are each independently optional. The section must handle all combinations: no hooks, only output_tool, only tool_entries, only command_entries, mixed.
- `permission_mode` currently has only one valid value (`bypassPermissions`). A style knob could suppress it entirely (it is always the same) or always render it for explicitness.
- `model` is an enum token. Style may want to map it to a display string: `opus` → "Claude Opus", etc. A `model_display_map` style knob handles this.

---

## 2. identity

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `title` | `AgentTitle` (TitleString) | scalar, required | Title Case, e.g. "Agent Builder" |
| `description` | `AgentDescription` (StringProse) | scalar, required | One-line purpose (same as frontmatter.description) |
| `role_identity` | `StringText` | scalar, required | Short noun phrase, e.g. "definition author" |
| `role_responsibility` | `RoleResponsibility` (StringProse) | scalar, required | One-sentence mandate |
| `model` | `AnthropicModel` (Enum) | scalar, required | Same as frontmatter.model |
| `role_description` | `RoleDescription \| None` (StringProse) | scalar, optional | Expanded role context |
| `role_expertise` | `RoleExpertise \| None` (list[StringText]) | array, optional | Domain skill phrases |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Role" or "Identity" |
| `heading_level` | H level (default H2) |
| `role_template` | f-string interpolating role_identity, e.g. `"You are a {role_identity}."` |
| `responsibility_label` | Label for role_responsibility, e.g. "Your responsibility:" or "Mandate:" |
| `description_label` | Label for role_description, e.g. "Context:" — omit if None |
| `expertise_label` | Label for role_expertise array, e.g. "Expertise:" — omit if None |
| `model_label` | Label for model field, e.g. "Model:" — may omit (duplicates frontmatter) |
| `model_display_map` | Map enum tokens to display strings: opus → "Claude Opus" |
| `description_omit` | Whether to suppress the description sub-field (it duplicates frontmatter.description) |
| `model_omit` | Whether to suppress the model sub-field (it duplicates frontmatter.model) |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `expertise_mode` | `role_expertise` array | bulleted / numbered / inline |
| `expertise_separator` | `role_expertise` when inline | e.g. `", "` |

### Design Notes

- `role_identity` feeds into `role_template` — it is not rendered standalone but is interpolated. The template IS the style knob.
- `role_description` is optional. When present it adds meaningful framing context. Omit behavior: skip the label and prose entirely.
- `description` and `model` duplicate frontmatter fields. Whether to render them here is a style decision exposed as omit knobs.

---

## 3. security_boundary

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `workspace_path` | `PathExistsAbsolute` | scalar, required | Absolute workspace root path |
| `display` | `DisplayEntries \| None` (list[DisplayEntry]) | array of objects, optional | Path+tools grant pairs |
| `display[i].path` | `DisplayPath` (PathRelative \| PathAbsolute) | scalar | Workspace-relative or absolute path |
| `display[i].tools` | `DisplayToolsCommands` (list[DisplayToolCommand]) | array | Tool/command names for this path |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Security Boundary" |
| `heading_level` | H level (default H2) |
| `preamble` | Prose sentence before the grant table, e.g. "This agent operates under `bypassPermissions` with hook-based path enforcement." |
| `grants_intro` | Intro text for the display entries block, e.g. "Allowed operations — everything else is blocked:" |
| `boundary_warning` | Footer warning text, e.g. "Do not attempt operations outside this boundary." |
| `workspace_label` | Label for workspace_path, e.g. "Workspace:" — render or omit |
| `workspace_omit` | Whether to suppress workspace_path display (it anchors the sandbox but may be obvious from paths) |
| `omit_if_no_display` | Whether to suppress the section entirely when display is null (no explicit grants) |
| `path_prefix` | Text prefix before each path, e.g. `- ` or blank |
| `tools_inline_separator` | Separator between tool names on one line, e.g. `", "` or `" | "` |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `entries_mode` | `display` array | sequential / bulleted — each entry is a path+tools line |
| `entry_item_template` | Each display entry | e.g. `"{path}: {tools}"` or a two-line format |
| `tools_in_entry_mode` | `display[i].tools` array | inline / bulleted |
| `tools_in_entry_separator` | Tools when inline | e.g. `", "` |

### Design Notes

- `workspace_path` is on `SecurityBoundaryAnthropic`, not `CriticalRules`. It anchors the sandbox root. Whether to show it in the rendered section is a style decision.
- When `display` is null, the section has no grant table. The preamble and warning may still be useful, or the whole section may be suppressed. `omit_if_no_display` handles this.
- The common display pattern is: one line per path, tools listed inline on the same line. A two-column table format is an alternative display mode.

---

## 4. input

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `description` | `InputDescription` (StringText) | scalar, required | Human-readable description of input data |
| `format` | `DispatchInputFormat` (Enum: jsonl/json/text) | scalar, required | Input data format |
| `delivery` | `DispatchInputDelivery` (Enum: tempfile/inline/file/directory) | scalar, required | How input reaches the agent |
| `input_schema` | `PathExistsAbsolute \| None` | scalar, optional | Schema path for input validation |
| `parameters` | `DispatchParameters \| None` (list[ParameterItem]) | array of objects, optional | Dispatcher-passed parameters |
| `parameters[i].param_name` | `SnakeString` | scalar, required | Parameter name |
| `parameters[i].param_type` | `ParamType` (Enum: path/string/integer/boolean) | scalar, required | Parameter type |
| `parameters[i].param_required` | `Boolean` | scalar, required | Whether required |
| `parameters[i].param_description` | `ParamDescription \| None` (StringText) | scalar, optional | Human-readable description |
| `context.context_required` | `ContextRequired \| None` (list[ContextItem]) | array of objects, optional | Required context resources |
| `context.context_available` | `ContextAvailable \| None` (list[ContextItem]) | array of objects, optional | Available (optional) context resources |
| `context[*][i].context_label` | `TitleString` | scalar, required | Display label for context resource |
| `context[*][i].context_path` | `PathAbsolute` | scalar, required | Absolute path to context resource |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Input" |
| `heading_level` | H level (default H2) |
| `description_label` | Label for description field, e.g. "Input:" or "You will receive:" |
| `format_label` | Label for format field, e.g. "Format:" — may omit if obvious from description |
| `delivery_label` | Label for delivery field, e.g. "Delivery:" |
| `format_display_map` | Map enum tokens to display strings: jsonl → "JSONL", text → "plain text" |
| `delivery_display_map` | Map enum tokens to display strings: tempfile → "tempfile path parameter", inline → "inline in this prompt" |
| `schema_label` | Label for input_schema path, e.g. "Input Schema:" |
| `schema_omit_if_none` | Whether to suppress schema line when null |
| `parameters_heading` | Sub-heading for parameters block, e.g. "Parameters" |
| `parameters_intro` | Intro prose before parameters list, e.g. "The dispatcher provides:" |
| `parameters_omit_if_none` | Whether to suppress parameters block when null |
| `param_required_suffix` | Text appended to required params, e.g. "(required)" |
| `param_optional_suffix` | Text appended to optional params, e.g. "(optional)" |
| `param_description_omit` | Whether to suppress param_description sub-field |
| `context_required_heading` | Sub-heading for required context, e.g. "Required Context" |
| `context_available_heading` | Sub-heading for available context, e.g. "Available Context" |
| `context_intro` | Intro prose for context block, e.g. "Load these resources before beginning:" |
| `context_omit_if_none` | Whether to suppress context blocks when null |
| `param_item_template` | f-string for each parameter line, e.g. `"- {param_name} ({param_type}): {param_description}"` |
| `context_item_template` | f-string for each context item, e.g. `"- {context_label}: {context_path}"` |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `parameters_mode` | `parameters` array | bulleted / numbered |
| `context_required_mode` | `context_required` array | bulleted / numbered |
| `context_available_mode` | `context_available` array | bulleted / numbered |

### Design Notes

- `format` and `delivery` are enum scalars. They describe mechanics, not agent behavior. Whether to render them depends on how self-describing the description field is. Omit knobs allow suppression.
- `parameters` and `context` are each independently optional. The section must handle: no parameters + no context, parameters only, context only, both.
- `context_required` vs `context_available` have different semantic weight — required items the agent must load, available items the agent may reference. The style may want separate headings and prose.
- `param_description` is optional per-item. When absent, the item renders with name and type only.

---

## 5. instructions

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `steps` | `ExecutionInstructions` (list[InstructionStep]) | array of objects, required, min 1 | Ordered processing steps |
| `steps[i].instruction_mode` | `InstructionMode` (Enum: deterministic/probabilistic) | scalar, required | Processing mode boundary |
| `steps[i].instruction_text` | `StringMarkdown` | scalar, required | Step content (markdown) |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Instructions" or "Processing Steps" |
| `heading_level` | H level (default H2) |
| `deterministic_label` | Badge/prefix for deterministic steps, e.g. "[DETERMINISTIC]" or "**Deterministic:**" |
| `probabilistic_label` | Badge/prefix for probabilistic steps, e.g. "[PROBABILISTIC]" or "**Judgment required:**" |
| `mode_label_omit` | Whether to suppress mode labels entirely (renders steps as plain sequence) |
| `mode_boundary_heading` | Whether to insert a heading when mode changes (e.g. "## Deterministic Steps" / "## Probabilistic Steps") |
| `mode_boundary_heading_deterministic` | Text for the deterministic boundary heading |
| `mode_boundary_heading_probabilistic` | Text for the probabilistic boundary heading |

**instruction_mode display format is the primary knob.** Four strategies:
1. **badge_prefix** — each step prefixed with its mode badge inline
2. **per_step_label** — each step has a sub-label showing mode
3. **grouped_by_mode** — steps grouped under mode boundary headings (shows transitions clearly)
4. **omit** — mode not rendered at all

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `steps_mode` | `steps` array | numbered / sequential / bulleted |
| `step_item_template` | Each step | controls how mode label and text are assembled per item |

### Design Notes

- `instruction_mode` MUST be rendered in some form — it is a boundary marker communicating deterministic vs probabilistic. The display format is the knob. See correction #3.
- `instruction_text` is `StringMarkdown` — it may contain nested markdown (headers, code blocks, lists). The display mode for steps should not wrap step text in markdown markers that would conflict with existing formatting.
- `numbered` mode for steps is the most common; sequence number helps the agent orient itself. `sequential` (blank-line separated blocks) is an alternative for long steps.
- **grouped_by_mode** is the preferred strategy when mode transitions matter — it shows the reader exactly where the agent switches from mechanical to judgmental work.

---

## 6. examples

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `groups` | `ExecutionExamples` (list[ExampleGroup]) | array of objects, required, min 1 | Example groups |
| `groups[i].example_group_name` | `ExampleGroupName` (TitleString) | scalar, required | Group name, used as H3 heading |
| `groups[i].example_display_headings` | `Boolean \| None` | scalar, optional, default False | Whether individual entries get H4 headings |
| `groups[i].examples_max_number` | `Integer \| None` | scalar, optional | Max examples to include from this group |
| `groups[i].example_entries` | `ExampleEntries` (list[ExampleEntry]) | array of objects, required, min 1 | Entries in this group |
| `groups[i].example_entries[j].example_heading` | `StringText` | scalar, required | Entry heading |
| `groups[i].example_entries[j].example_text` | `StringMarkdown` | scalar, required | Entry content (markdown) |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Examples" or "Calibration Examples" |
| `heading_level` | H level (default H2) |
| `group_heading_level` | H level for group headings (default H3) |
| `entry_heading_level` | H level for entry headings when example_display_headings=true (default H4) |
| `preamble` | Intro prose before all groups, e.g. "The following examples calibrate expected behavior:" |
| `entry_heading_omit_when_false` | When example_display_headings=false, suppress the entry heading entirely vs use it as bold inline label |
| `entry_heading_inline_label_template` | When headings suppressed, format heading as inline bold prefix: `"**{heading}:** "` |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `groups_mode` | `groups` array | sequential (standard) |
| `entries_mode` | `example_entries` within a group | sequential / numbered |
| `max_number_enforcement` | `examples_max_number` | how truncation is applied — first N / last N / evenly distributed |

### Design Notes

- `example_display_headings` is a per-group boolean that gates whether individual entry headings render. When false, the heading text is available but must be either suppressed or rendered as inline bold — a style decision.
- `examples_max_number` is a data field that controls truncation, not a style knob. The truncation strategy (first N vs other) is a display decision.
- `example_text` is `StringMarkdown` and likely contains structured content (GOOD/BAD/WHY patterns). Do not wrap in list markers.

---

## 7. output

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `description` | `OutputDescription` (StringText) | scalar, required | Human-readable output description |
| `format` | `OutputFormatKind` (Enum: jsonl/json/markdown/text) | scalar, required | Pipeline control — not agent-facing |
| `name_known` | `OutputNameKnown` (Enum: known/partially/unknown) | scalar, required | How well output filename is known |
| `schema_path` | `PathExistsAbsolute \| None` | scalar, optional | Output schema path |
| `output_file` | `PathAbsolute \| None` | scalar, optional | Exact output file path (when name_known=known) |
| `output_directory` | `PathAbsolute \| None` | scalar, optional | Output directory (when name_known=partially/unknown) |
| `name_template` | `FilenameTemplate \| None` | scalar, optional | Filename template with {placeholder} (when name_known=partially) |
| `name_instruction` | `StringProse \| None` | scalar, optional | Naming instruction (when name_known=unknown) |
| `schema_embed` | `Boolean \| None` | scalar, optional | Whether schema is embedded vs referenced |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Output" |
| `heading_level` | H level (default H2) |
| `description_label` | Label for description, e.g. "You will produce:" or "Output:" |
| `format_omit` | Whether to suppress format (it is pipeline control, not agent-facing — see correction #4) |
| `schema_label` | Label for schema_path, e.g. "Schema:" |
| `schema_omit_if_none` | Whether to suppress schema line when null |
| `output_file_label` | Label for output_file, e.g. "Write to:" |
| `output_directory_label` | Label for output_directory, e.g. "Output directory:" |
| `name_template_label` | Label for name_template, e.g. "Filename pattern:" |
| `name_instruction_label` | Label for name_instruction, e.g. "Filename instruction:" |
| `schema_embed_note` | Text to show when schema_embed=true, e.g. "(schema embedded below)" — or omit |

### Conditional Rendering

| Condition | Fields rendered |
|-----------|----------------|
| `name_known = known` | `output_file` present; `output_directory`, `name_template`, `name_instruction` absent |
| `name_known = partially` | `output_directory` + `name_template` present; `output_file`, `name_instruction` absent |
| `name_known = unknown` | `output_directory` + `name_instruction` present; `output_file`, `name_template` absent |
| `schema_embed = true` | Schema content is embedded; schema_path label may note this |
| `schema_embed = false/null` | Schema_path is a read-accessible reference |

### Design Notes

- `format` is a pipeline control field (correction #4). It should not be rendered in the agent-facing section. Include `format_omit = true` in the style default.
- `schema_embed` gates whether the schema file content appears inline. The section renderer needs to know whether to embed (requiring a file read during render) or just show the path. This is a data-driven behavior, not a style knob — the style knob is only the label/note shown either way.

---

## 8. writing_output

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `tool_name` | `ToolName` (SnakeString) | scalar, required | Resolved output tool name |
| `invocation_variant` | `InvocationVariant` (Enum: no-name/with-name) | scalar, required | Whether agent provides a name |
| `invocation_display` | `InvocationDisplay` (StringText) | scalar, required | Ready-to-use heredoc string |
| `name_needed` | `OutputToolNameNeeded` (Boolean) | scalar, required | Whether agent must provide a filename |
| `name_pattern` | `FilenameTemplate \| None` | scalar, optional | Naming pattern when name_needed=true |
| `batch_size` | `OutputToolBatchSize \| None` (Integer, default 20) | scalar, optional | Records per batch write |
| `schema_path` | `OutputToolSchemaXAbs \| None` | scalar, optional | Schema path for tool validation |
| `file_path` | `PathAbsolute \| None` | scalar, optional | Fixed output file path (no-name variant) |
| `directory_path` | `PathAbsolute \| None` | scalar, optional | Output directory (with-name variant) |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Writing Output" or "Output Tool" |
| `heading_level` | H level (default H2) |
| `preamble` | Intro prose, e.g. "Use this tool for all output writes:" |
| `tool_name_label` | Label for tool_name, e.g. "Tool:" |
| `invocation_label` | Label preceding the invocation_display block, e.g. "Invocation:" |
| `invocation_code_fence` | Whether to wrap invocation_display in a code fence (bash) |
| `name_pattern_label` | Label for name_pattern when name_needed=true, e.g. "Name pattern:" |
| `batch_size_label` | Label for batch_size, e.g. "Batch size:" |
| `schema_path_label` | Label for schema_path |
| `omit_if_null` | Whether to suppress the entire section when writing_output is null (section is optional at top level) |

### Conditional Rendering

| Condition | Fields rendered |
|-----------|----------------|
| `invocation_variant = no-name` | `file_path` present; `directory_path`, `name_pattern` absent |
| `invocation_variant = with-name` | `directory_path` + `name_pattern` (if partially known) present |
| `name_needed = false` | No name-generation instruction needed |
| `name_needed = true` | name_pattern shown with instruction to derive the name variable |

### Design Notes

- `invocation_display` is the pre-composed heredoc string. It is the primary agent-facing content of this section — the agent copies it verbatim. Style wraps it (label + code fence) but does not transform it.
- The entire `writing_output` section is nullable at the top-level model. When null, there is no custom output tool, and this section must be entirely suppressed (`omit_if_null`).
- `batch_size` has a default of 20 via `default_factory`. It is always present when writing_output is present.

---

## 9. constraints

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `rules` | `GuardrailsConstraints` (list[GuardrailsConstraint]) | array, required, min 1 | MUST/NEVER constraint rules |
| `rules[i]` | `GuardrailsConstraint` (StringProse) | scalar | Single constraint sentence |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Constraints" |
| `heading_level` | H level (default H3 — fossil; configurable in rebuild) |
| `preamble` | Intro prose before rules, e.g. "The following rules are absolute:" |
| `omit_if_null` | Whether to suppress section when constraints is null |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `rules_mode` | `rules` array | bulleted / numbered |

### Design Notes

- The heading_level is currently H3 (a fossil from when constraints lived under a parent "Guardrails" category). In the rebuild this is configurable via the `heading_level` knob.
- Section is nullable at the top level. `omit_if_null` should default to true.

---

## 10. anti_patterns

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `patterns` | `GuardrailsAntiPatterns` (list[GuardrailsAntiPattern]) | array, required, min 1 | Anti-pattern descriptions |
| `patterns[i]` | `GuardrailsAntiPattern` (StringProse) | scalar | Single anti-pattern sentence |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Anti-Patterns" or "Common Mistakes" |
| `heading_level` | H level (default H3 — fossil; configurable in rebuild) |
| `preamble` | Intro prose before patterns, e.g. "Avoid these failure modes:" |
| `omit_if_null` | Whether to suppress section when anti_patterns is null |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `patterns_mode` | `patterns` array | bulleted / numbered |

### Design Notes

- Mirrors `constraints` in structure. Same heading_level fossil issue; same configurable fix.
- Section is nullable at the top level.

---

## 11. success_criteria

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `criteria` | `SuccessCriteria1` (list[SuccessItem]) | array of objects, required, min 1 | Success criteria items |
| `criteria[i].success_definition` | `SuccessDefinition` (StringProse) | scalar, required | One-sentence success statement |
| `criteria[i].success_evidence` | `SuccessEvidence` (list[StringProse]) | array, required, min 1 | Observable evidence items |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Success Criteria" |
| `heading_level` | H level (default H3 — fossil; configurable in rebuild) |
| `preamble` | Intro prose before criteria |
| `definition_label` | Label for each success_definition, e.g. "Success:" or bold prefix |
| `evidence_label` | Label for evidence block, e.g. "Evidence:" |
| `omit_if_null` | Whether to suppress section when success_criteria is null |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `criteria_mode` | `criteria` array | sequential / numbered |
| `evidence_mode` | `success_evidence` within each item | bulleted / numbered |

### Design Notes

- Each item is a definition + evidence array. The definition is rendered first, then the evidence list under it. `sequential` mode for criteria with `bulleted` for evidence is the natural default.
- Section is nullable at the top level.

---

## 12. failure_criteria

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `criteria` | `FailureCriteria1` (list[FailureItem]) | array of objects, required, min 1 | Failure criteria items |
| `criteria[i].failure_definition` | `FailureDefinition` (StringProse) | scalar, required | One-sentence failure statement |
| `criteria[i].failure_evidence` | `FailureEvidence` (list[StringProse]) | array, required, min 1 | Observable evidence items |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Failure Criteria" |
| `heading_level` | H level (default H3 — fossil; configurable in rebuild) |
| `preamble` | Intro prose before criteria |
| `definition_label` | Label for each failure_definition, e.g. "Failure:" or bold prefix |
| `evidence_label` | Label for evidence block, e.g. "Evidence:" |
| `omit_if_null` | Whether to suppress section when failure_criteria is null |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `criteria_mode` | `criteria` array | sequential / numbered |
| `evidence_mode` | `failure_evidence` within each item | bulleted / numbered |

### Design Notes

- Structural mirror of `success_criteria`. All knob names and defaults are parallel.
- Section is nullable at the top level.

---

## 13. return_format

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `mode` | `ReturnMode` (Enum: status/status-metrics/metrics-output/output) | scalar, required | Return communication mode |
| `return_schema` | `PathExistsAbsolute \| None` | scalar, optional | Schema for structured return |
| `status_instruction` | `StringProse \| None` | scalar, optional | How to report status |
| `metrics_instruction` | `StringProse \| None` | scalar, optional | How to report metrics |
| `output_instruction` | `StringProse \| None` | scalar, optional | How to deliver output inline |

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Return Format" or "Reporting" |
| `heading_level` | H level (default H2) |
| `mode_label` | Label for mode field, e.g. "Return mode:" — may omit; mode is implied by which instruction fields render |
| `mode_display_map` | Map enum tokens to display strings: status → "STATUS only", status-metrics → "STATUS + METRICS" |
| `return_schema_label` | Label for return_schema path, e.g. "Return schema:" |
| `return_schema_omit_if_none` | Whether to suppress schema line when null |
| `status_label` | Label preceding status_instruction, e.g. "Status reporting:" |
| `metrics_label` | Label preceding metrics_instruction |
| `output_label` | Label preceding output_instruction |

### Conditional Rendering

| Condition | Fields rendered |
|-----------|----------------|
| `mode = status` | `status_instruction` rendered; metrics/output instructions absent |
| `mode = status-metrics` | `status_instruction` + `metrics_instruction` rendered |
| `mode = metrics-output` | `metrics_instruction` + `output_instruction` rendered |
| `mode = output` | `output_instruction` rendered |

The mode enum directly gates which instruction fields are rendered. Style only needs to provide labels for each possible instruction field.

### Design Notes

- `mode` gates which instructions are present. Since the instruction fields themselves carry the content, rendering mode as a standalone field is redundant. `mode_label` + `mode_display_map` provides the option but omitting it is a valid style choice.
- `return_schema` is nullable. When present, it should be embedded in the prompt (the schema content is agent-facing, not just a path reference). The section renderer needs to handle file embedding similar to `output.schema_embed`.

---

## 14. critical_rules

### Overview

This is the most style-heavy section. Almost all rendered content comes from style templates, not data fields. The data fields are triggers and interpolation values only.

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `has_output_tool` | `Boolean` | scalar, required | Gates which rules appear |
| `tool_name` | `ToolName \| None` (SnakeString) | scalar, optional | Interpolates into tool rule text |
| `name_needed` | `OutputToolNameNeeded \| None` (Boolean) | scalar, optional | Potential conditional |
| `batch_size` | `OutputToolBatchSize \| None` (Integer, default 20) | scalar, optional | Interpolates into batch rule text |

Note: `workspace_path` is on `SecurityBoundaryAnthropic`, not here. See correction #2.

### Style Knobs

| Knob | Purpose |
|------|---------|
| `heading` | Section heading text, e.g. "Critical Rules" |
| `heading_level` | H level (default H2) |
| `generic_rules` | List of rule text strings always rendered regardless of has_output_tool — e.g. "Fail fast — if something is wrong, return FAILURE immediately.", "Stay within scope — do not perform operations not described in these instructions.", "Do not invent data — if you cannot determine a value from the input, it is absent." |
| `tool_rule_template` | Rule text interpolating tool_name, e.g. `"Use {tool_name} for all output — never use Write, Edit, or Bash to write output directly."` |
| `batch_rule_template` | Rule text interpolating batch_size, e.g. `"Process exactly {batch_size} records per batch before invoking the output tool."` |
| `name_needed_rule` | Rule text when name_needed=true, e.g. "Determine the output filename before each write — use the name pattern to construct it from dispatch parameters." |
| `rules_mode` | Display mode: numbered / bulleted |

### Conditional Rendering Logic

```
if has_output_tool = true:
    render: tool_rule_template (interpolating tool_name)
    render: batch_rule_template (interpolating batch_size)
    if name_needed = true:
        render: name_needed_rule
    render: generic_rules

if has_output_tool = false:
    render: generic_rules only
```

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `rules_mode` | Combined rules list | numbered / bulleted |

### Design Notes

- `has_output_tool` is the primary gate. When false, only generic rules render. When true, tool + batch + optional name_needed rules prepend the generic rules.
- `tool_name` and `batch_size` are interpolation values only — they do not render standalone. They exist for self-sufficiency (no cross-section dependencies per correction #5).
- `name_needed` exists on the schema but is not currently wired (correction #1 note). It is a potential conditional for a name-generation reminder rule. Include `name_needed_rule` as an optional style knob that renders only when `has_output_tool=true` and `name_needed=true`.
- `workspace_path` from `SecurityBoundaryAnthropic` could optionally appear here as a security reminder rule. If desired, a style knob `workspace_rule_template` handles this: `"All file operations must be within the workspace: {workspace_path}."` — but workspace_path would need to be passed to this section container, which violates the no-cross-section-dependency principle. Either accept the dependency for this knob or make workspace_path a top-level pass-through to critical_rules.
- All rule text (generic, tool, batch, name_needed) lives in the style TOML, not in data. This means rule wording is a style variant choice — different style files can express the same rules with different tone (stern vs collaborative) without touching the data.

---

## 15. dispatcher (fixed structure, not recipe-driven)

### Fields

| Field | Python Type | Class | Notes |
|-------|-------------|-------|-------|
| `agent_name` | `AgentName` (kebab-case str) | scalar, required | Agent identifier |
| `agent_description` | `AgentDescription` (StringProse) | scalar, required | One-line purpose |
| `dispatch_mode` | `DispatchMode` (Enum: batch/full) | scalar, required | How work is fed to agent |
| `background_mode` | `DispatchBackgroundMode` (Enum: allowed/required/forbidden) | scalar, required | Execution lifecycle policy |
| `input_format` | `DispatchInputFormat` (Enum: jsonl/json/text) | scalar, required | Input data format |
| `input_delivery` | `DispatchInputDelivery` (Enum: tempfile/inline/file/directory) | scalar, required | How input reaches agent |
| `input_description` | `InputDescription` (StringText) | scalar, required | Human-readable input description |
| `output_format` | `OutputFormatKind` (Enum: jsonl/json/markdown/text) | scalar, required | Output format |
| `output_name_known` | `OutputNameKnown` (Enum: known/partially/unknown) | scalar, required | Output filename knowability |
| `return_mode` | `ReturnMode` (Enum: status/status-metrics/metrics-output/output) | scalar, required | Return communication mode |
| `max_agents` | `Integer \| None` (default 6) | scalar, optional | Max concurrent agent instances |
| `batch_size` | `DispatchBatchSize \| None` (tuple[Integer, Integer]) | scalar, optional | [min, max] records per batch chunk |
| `parameters` | `DispatchParameters \| None` (list[ParameterItem]) | array of objects, optional | Parameters passed to agent |

### Style Knobs

Per correction #7: dispatcher is fixed-structure. Style knobs are text substitution only — no section ordering or omission.

| Knob | Purpose |
|------|---------|
| `heading` | Dispatcher section heading, e.g. "Dispatcher Configuration" |
| `heading_level` | H level |
| `agent_name_label` | Label for agent_name |
| `description_label` | Label for agent_description |
| `dispatch_mode_label` | Label for dispatch_mode |
| `background_mode_label` | Label for background_mode |
| `input_format_label` | Label for input_format |
| `input_delivery_label` | Label for input_delivery |
| `input_description_label` | Label for input_description |
| `output_format_label` | Label for output_format |
| `output_name_known_label` | Label for output_name_known |
| `return_mode_label` | Label for return_mode |
| `max_agents_label` | Label for max_agents |
| `batch_size_label` | Label for batch_size (only when dispatch_mode=batch) |
| `parameters_heading` | Sub-heading for parameters block |
| `parameters_omit_if_none` | Whether to suppress parameters block when null |
| `param_item_template` | f-string for each parameter line |
| `dispatch_mode_display_map` | Map: batch → "Batch (chunked)", full → "Full (single invocation)" |
| `background_mode_display_map` | Map: allowed → "Allowed", required → "Required", forbidden → "Forbidden (foreground)" |

### Display Knobs

| Knob | Applies To | Purpose |
|------|-----------|---------|
| `parameters_mode` | `parameters` array | bulleted / numbered |

### Conditional Rendering

| Condition | Fields rendered |
|-----------|----------------|
| `dispatch_mode = batch` | `batch_size` rendered (required when batch) |
| `dispatch_mode = full` | `batch_size` absent |
| `parameters` is null | Parameters block suppressed |

### Design Notes

- Dispatcher feeds a separate skill generation path (per AGENT_BUILD_SYSTEM.md). Its rendered output is a dispatcher skill file, not the agent prompt. Style knobs here serve that output format.
- `batch_size` is a [min, max] tuple. The item_template for it should show both values: `"[{min}, {max}] records per batch"`.
- `parameters` mirrors the `input.parameters` array. The same `param_item_template` knob design applies.

---

## Cross-Cutting Notes

### Nullable Sections

Six sections are nullable at the top level of `AgentAnthropicRender`:
- `security_boundary` — null when no explicit grants
- `examples` — null when no examples defined
- `constraints` — null when no constraints defined
- `anti_patterns` — null when no anti-patterns defined
- `success_criteria` — null when no success criteria defined
- `failure_criteria` — null when no failure criteria defined
- `writing_output` — null when no custom output tool

Every style TOML must provide `omit_if_null = true` as the default for these sections. Recipe omission handles this at the recipe level; per-section omit handles it at the container level.

### Heading Levels — Fossil Correction

Current heading levels are fossils of a prior parent-category structure:
- H2: frontmatter, identity, security_boundary, input, instructions, examples, output, writing_output, return_format, critical_rules
- H3: constraints, anti_patterns, success_criteria, failure_criteria

In the rebuild, `heading_level` is a style knob on every section. The fossil defaults are preserved as style defaults but are overridable.

### Format Pipeline Control Fields

Two fields are pipeline control only and should default to `omit = true` in all style files:
- `output.format` — the write tool already embodies the format (correction #4)
- `dispatcher.output_format` — same reasoning applies to the dispatcher output

### instruction_mode Rendering — Required

`instruction_mode` on each `InstructionStep` MUST be rendered. The choice is which of the four display strategies to implement:
1. badge_prefix (inline per step)
2. per_step_label (sub-label per step)
3. grouped_by_mode (boundary headings — preferred)
4. omit (prohibited)

### Denormalized Fields in critical_rules

`tool_name`, `batch_size`, and `name_needed` on `CriticalRules` are denormalized copies from `writing_output`. They exist so the critical_rules section container is self-sufficient (correction #5). The style TOML rule templates consume them directly via interpolation — no cross-section lookup.
