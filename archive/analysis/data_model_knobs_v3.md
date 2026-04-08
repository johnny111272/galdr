# Data Model Knobs v3

Control surfaces for each section container. For every field in every section: type classification, style controls (text that is not data), display controls (collection formatting), conditional gates, and non-obvious design decisions.

---

## Reading This Document

**Field classifications:**
- `scalar` — single value, renders as text
- `array` — collection, needs display mode
- `nested` — sub-object with its own fields
- `optional` — may be null/absent

**Style surface types:**
- `heading` — section title
- `heading_level` — H1/H2/H3/H4
- `label` — field prefix ("Purpose:", "Schema:")
- `template` — f-string wrapping data ("You are a {role_identity}.")
- `prose` — connective framing text ("The following operations are allowed...")
- `footer` — closing text ("Do not attempt operations outside this boundary.")
- `omit_behavior` — what renders when optional field is None

**Display surface types:**
- `mode` — bulleted / numbered / sequential / inline
- `separator` — for inline mode
- `item_template` — for structured items in arrays

---

## 1. frontmatter

**Purpose:** Agent metadata for the TOML frontmatter header. Not rendered as prose into the agent prompt — rendered as structured frontmatter fields and hook CLI commands.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `name` | AgentTitle (TitleString) | scalar |
| `description` | AgentDescription (StringProse) | scalar |
| `model` | AnthropicModel (enum) | scalar |
| `permission_mode` | PermissionMode (enum) | scalar, always `bypassPermissions` |
| `tools` | FrontmatterTools (list[PascalString]) | array |
| `hooks.output_tool` | OutputToolName | scalar, optional |
| `hooks.tool_entries` | list[ToolPathEntry] | array of nested, optional |
| `hooks.command_entries` | list[CommandPathEntry] | array of nested, optional |

### Style Controls

- `heading` — knob, but frontmatter renders before the prompt body; the heading is structural ("---\n{fields}\n---"), not a prose section title
- `tools_format` — how to join the tools list: comma-separated inline in TOML (`tools = ["Read", "Grep"]`) vs. one per line vs. prose sentence — this is a display choice that matters for readability in the rendered .md file
- `hooks_format` — how hook CLI commands are assembled: the style controls whether hook commands render as a comment block, a bash block, or inline in the frontmatter TOML
- `permission_mode_display` — `bypassPermissions` is always present; the knob is whether to display it verbatim, as a human-readable label ("Unrestricted with hook enforcement"), or omit from frontmatter prose
- `omit_behavior` for `hooks.output_tool` — when None, no output_tool hook line is emitted
- `omit_behavior` for `hooks.tool_entries` — when None, no tool hook lines are emitted
- `omit_behavior` for `hooks.command_entries` — when None, no command hook lines are emitted

### Display Controls

- `tools` array → `mode`: inline (comma-separated in TOML) is the natural form; no variant needed here since TOML frontmatter format is fixed
- `hooks.tool_entries` → each entry is `{tool}: {paths}` — the item_template and separator for the paths sub-list are knobs
- `hooks.command_entries` → same structure as tool_entries

### Conditionals

- `hooks.output_tool` present ↔ `has_output_tool = true` on critical_rules
- `hooks.tool_entries` present ↔ agent has tool-based grants
- `hooks.command_entries` present ↔ agent has Bash command grants

### Non-Obvious Design Decisions

1. Frontmatter is the only section that renders as structured data (TOML), not prose. Style controls here are about TOML formatting conventions, not prose framing. Whether this section goes through the same style/display machinery as prose sections is an open question — it may warrant a separate rendering path.
2. The `description` field appears in both `frontmatter` and `identity`. They are duplicated in the data model. Style controls must decide which one "wins" or whether both render in their respective sections independently.

---

## 2. identity

**Purpose:** Establishes who the agent is. The opening section of the agent prompt that sets role context.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `title` | AgentTitle (TitleString) | scalar |
| `description` | AgentDescription (StringProse) | scalar |
| `role_identity` | StringText | scalar |
| `role_responsibility` | RoleResponsibility (StringProse) | scalar |
| `model` | AnthropicModel (enum) | scalar |
| `role_description` | RoleDescription (StringProse) | scalar, optional |
| `role_expertise` | list[StringText] | array, optional |

### Style Controls

- `heading` — section title knob ("Identity", "Your Role", "Who You Are", or no heading at all)
- `heading_level` — H1 or H2 (identity is often the lead section; H1 is defensible)
- `role_identity_template` — wraps `role_identity` in a sentence: "You are a {role_identity}." or "As a {role_identity}, you..." — the template IS the style surface; bare role_identity string is never rendered alone
- `responsibility_label` — prefix label for `role_responsibility`: "Your responsibility:", "Mission:", "Primary obligation:", or no label (role_responsibility is a complete sentence that stands alone)
- `description_label` — prefix label for `role_description`: "Context:", "Background:", or no label
- `expertise_label` — prefix label for `role_expertise` array: "Expertise:", "Domain knowledge:", or no label
- `model_display` — whether and how to render `model`: verbatim ("claude-sonnet-4-6"), as tier label ("sonnet"), or omit entirely from prose (model is already in frontmatter, showing it again in identity is optional)
- `omit_behavior` for `role_description` — when None: no description block; when present: renders after role_identity sentence
- `omit_behavior` for `role_expertise` — when None: no expertise block; when present: renders as configured display mode

### Display Controls

- `role_expertise` → `mode` knob: inline ("Python, schema design, data validation") vs. bulleted list vs. omit entirely — inline is the natural form for short expertise phrases

### Conditionals

- `role_description` None → omit description block entirely
- `role_expertise` None → omit expertise block entirely
- If both optional fields are None, identity renders as: role_identity template + responsibility sentence only

### Non-Obvious Design Decisions

1. `title` and `description` also appear on `frontmatter`. Identity's `title` may serve as the H1 heading of the prompt (the display title), while `description` may serve as a sub-heading or opening sentence. The style controls must specify which field plays which role.
2. `model` on identity is the resolved model name (haiku/sonnet/opus/inherit). It almost certainly should not render as prose in the identity section — it belongs in frontmatter. Flag: this field should probably be consumed but not rendered by the identity container.
3. `role_identity_template` is the highest-impact style surface in the entire document. "You are a {role_identity}" vs. "You are an expert {role_identity}" vs. "Operating as a {role_identity}" meaningfully affects agent behavior. This is a primary benchmark axis.

---

## 3. security_boundary

**Purpose:** Declares what paths and tools the agent is permitted to access. Sets behavioral constraints via explicit enumeration.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `workspace_path` | PathExistsAbsolute | scalar |
| `display` | list[DisplayEntry] | array of nested, optional |
| `display[n].path` | DisplayPath (PathRelative or PathAbsolute) | scalar |
| `display[n].tools` | list[DisplayToolCommand] | array |

### Style Controls

- `heading` — knob: "Security Boundary", "Permissions", "Access Grants", "Allowed Operations"
- `heading_level` — H2 is the established convention
- `preamble` — prose before the entries: "This agent operates under `bypassPermissions` with hook-based restrictions." The hook model is the style surface; the data doesn't change, the explanation does
- `grants_intro` — prose introducing the entries: "The following operations are allowed — everything else is blocked by the system." vs. "Granted paths:" vs. no intro
- `boundary_warning` — footer prose: "Do not attempt operations outside this boundary." vs. "All other operations are denied." vs. omit
- `workspace_path_display` — whether to render `workspace_path` in the section (as a base path reference) or omit it (it's in critical_rules too); if rendered, the label knob ("Workspace:", "Base path:")
- `omit_behavior` for `display` — when None (no explicit grants beyond auto-derived): either render "No explicit grants — all access is auto-derived from IO fields" or omit the section entirely; this is a non-trivial design decision
- `path_format` — for display entries: render relative paths with or without the `./` prefix, use the absolute path if it was absolute
- `tools_label` — per-entry label: "Tools:", or rendered inline after the path without a label

### Display Controls

- `display` array → `mode` knob: sequential (one entry per line block) vs. bulleted (each entry is a `- path: tools` bullet) vs. compact table format
- `display[n].tools` → `mode` knob: inline comma-separated ("Read, Grep, find") vs. bulleted sub-list vs. space-separated — inline is the natural form
- `display[n].tools` → `separator`: ", " vs. " | " vs. " " for inline mode
- `item_template` — how each entry renders: "`{path}` — {tools}" vs. "- **{path}**: {tools}" vs. table row

### Conditionals

- `display` None → either omit section or render a "no explicit grants" message; style controls the omit_behavior
- When `display` entries are present, each entry always has both `path` and `tools` (non-optional within entry)

### Non-Obvious Design Decisions

1. `workspace_path` is on `SecurityBoundaryAnthropic`, not on `CriticalRules` (established). But it is duplicated — critical_rules has a separate `workspace_path` field (this is the established design). The security_boundary container does not need to render `workspace_path` — the critical_rules section owns that rendering. The security_boundary container renders only the `display` entries.
2. The section may be omitted entirely (no explicit grants at all for simple read-only agents). The style must define what "omit this section" means in the recipe — either remove from modules list or produce an empty string and filter.
3. Tools and commands (Unix shell commands like `find`, `ls`) are mixed in `display[n].tools`. Style must decide whether they render identically or with visual differentiation (e.g., `Bash:find` or just `find`).

---

## 4. input

**Purpose:** Describes what the agent receives: data format, delivery mechanism, schema, parameters, and context resources.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `description` | InputDescription (StringText) | scalar |
| `format` | DispatchInputFormat (enum: jsonl/json/text) | scalar |
| `delivery` | DispatchInputDelivery (enum: tempfile/inline/file/directory) | scalar |
| `input_schema` | PathExistsAbsolute | scalar, optional |
| `parameters` | list[ParameterItem] | array of nested, optional |
| `parameters[n].param_name` | SnakeString | scalar |
| `parameters[n].param_type` | ParamType (enum: path/string/integer/boolean) | scalar |
| `parameters[n].param_required` | Boolean | scalar |
| `parameters[n].param_description` | ParamDescription (StringText) | scalar, optional |
| `context.context_required` | list[ContextItem] | array of nested, optional |
| `context.context_available` | list[ContextItem] | array of nested, optional |
| `context[n].context_label` | TitleString | scalar |
| `context[n].context_path` | PathAbsolute | scalar |

### Style Controls

- `heading` — knob: "Input", "What You Receive", "Input Data"
- `heading_level` — H2
- `description_label` — label before description: "Input:" or no label (description is readable prose that stands alone)
- `format_label` — label before format value: "Format:", "Data format:", or rendered inline in description sentence
- `delivery_label` — label for delivery mode: "Delivery:", "Delivered via:", or inline; delivery enum values may need human-readable mappings ("tempfile" → "temporary file", "inline" → "embedded in prompt")
- `delivery_display_map` — style surface: maps enum values to human-readable strings for rendering
- `parameters_intro` — prose before parameters list: "The dispatcher provides:", "Parameters:", "You receive the following parameters:"
- `schema_intro` — prose before schema path: "Input validates against:", "Schema:", "Input schema:"
- `context_required_intro` — prose before required context: "Required context:", "You must read:", "Context (required):"
- `context_available_intro` — prose before available context: "Available context:", "You may read:", "Context (available):"
- `optional_suffix` — for optional parameters: "(optional)" appended to item, or no suffix
- `omit_behavior` for `input_schema` — when None: no schema block
- `omit_behavior` for `parameters` — when None: no parameters block
- `omit_behavior` for `context` — when None: no context block; when context is present but only one sub-list: render only that sub-list

### Display Controls

- `parameters` → `mode`: bulleted is the natural form; numbered is defensible for ordered parameters
- `parameters` → `item_template`: "`{param_name}` ({param_type}): {param_description}" vs. "- **{param_name}**: {param_description} [{param_type}]" vs. minimal "`{param_name}`" only
- `parameters` → `required_display`: whether to render `param_required` (show "required" / "optional" badge) or omit (all parameters listed are assumed required unless annotated)
- `context.context_required` → `mode`: bulleted list of label+path pairs is the natural form; sequential (one block per item) is an option for long descriptions
- `context.context_available` → same as context_required
- `context` → `item_template`: "**{context_label}**: `{context_path}`" vs. "- {context_label} ({context_path})" vs. just label with path rendered beneath

### Conditionals

- `parameters` None → omit parameters block
- `input_schema` None → omit schema block
- `context` None → omit context block
- `context.context_required` None → omit required sub-block
- `context.context_available` None → omit available sub-block
- `parameters[n].param_description` None → render parameter without description; template must handle absent description gracefully

### Non-Obvious Design Decisions

1. `format` and `delivery` are pipeline-mechanical enum values that need human-readable rendering. The style controls both the label and the display map from enum values to prose. "jsonl" may render as "JSONL" or "newline-delimited JSON"; "tempfile" may render as "temporary file path" — these are meaningful benchmark differences.
2. Context items contain both a label (human-readable) and a path (filesystem path). The question is whether the path renders verbatim (as a monospace path reference) or is suppressed in favor of just the label. For prompts, the label matters most — the path is the grant mechanism, already handled by hooks.
3. `param_required` Boolean on each parameter — whether to visually distinguish required vs. optional parameters is a style choice. If all parameters in the example data are required, this distinction may not matter yet.

---

## 5. instructions

**Purpose:** Ordered processing steps the agent executes. The core behavioral specification.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `steps` | list[InstructionStep] | array of nested |
| `steps[n].instruction_mode` | InstructionMode (enum: deterministic/probabilistic) | scalar |
| `steps[n].instruction_text` | StringMarkdown | scalar |

### Style Controls

- `heading` — knob: "Instructions", "Processing Steps", "How To Proceed", "Execution Steps"
- `heading_level` — H2
- `deterministic_marker` — how to signal deterministic mode: prefix badge ("[DETERMINISTIC]"), section group label ("Deterministic Steps"), per-step annotation, or no marker
- `probabilistic_marker` — how to signal probabilistic mode: prefix badge ("[PROBABILISTIC]"), group label, per-step annotation, or no marker
- `mode_grouping` — whether to group steps by mode (all deterministic together, all probabilistic together) vs. preserve original order with per-step mode markers — this is a major architectural choice
- `step_separator` — what separates steps in sequential rendering: blank line, horizontal rule, nothing
- `step_prefix_template` — how to prefix each step: "Step {n}:", "{n}.", no prefix, mode-badge prefix

### Display Controls

- `steps` → `mode`: **numbered** (1., 2., 3.) is the natural form and signals sequence; bulleted loses sequence information; sequential (paragraphs) works when steps are labeled differently
- `steps` → `mode` by mode-type: grouped display is an alternative axis — group all deterministic steps under "### Deterministic" and all probabilistic under "### Probabilistic", each group numbered independently
- `instruction_mode` → `rendering_strategy` — four options exist, each is a legitimate benchmark variant:
  1. Per-step badge prefix: "[D] 1. {text}" / "[P] 2. {text}"
  2. Grouped sections with sub-numbering: "### Deterministic\n1. {text}" / "### Probabilistic\n1. {text}"
  3. Per-step label paragraph: "**Step 1 (deterministic):**\n{text}"
  4. Mode-framed blocks: "> **DETERMINISTIC:** {text}" (blockquote variant)

### Conditionals

- All steps are required (list[InstructionStep] min_length=1, no optional steps)
- `instruction_mode` is always present on every step — it always gates rendering style, never rendering inclusion
- Mixed-mode sequences (deterministic then probabilistic then deterministic) are the common case; grouping mode would reorder presentation

### Non-Obvious Design Decisions

1. `instruction_mode` MUST be rendered — it is a boundary marker established as a key fact. The display format is the primary knob. The four strategies above represent genuinely different behavioral signals to the LLM. This is the highest-value display benchmark in the instructions section.
2. Grouping vs. preserving order is an architectural choice with LLM behavioral implications. Grouping by mode makes mode semantics clearer but breaks the natural flow of work. Preserving order with per-step markers maintains procedural coherence. Both are valid hypotheses.
3. The `instruction_text` is StringMarkdown — it may contain internal markdown (lists, code blocks, bold). The step container must pass through markdown formatting without double-processing it.

---

## 6. examples

**Purpose:** Calibration examples that show the agent what correct output looks like. Organized in groups, with optional per-example headings.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `groups` | list[ExampleGroup] | array of nested |
| `groups[n].example_group_name` | ExampleGroupName (TitleString) | scalar |
| `groups[n].example_display_headings` | Boolean | scalar, optional (default: false) |
| `groups[n].examples_max_number` | Integer | scalar, optional |
| `groups[n].example_entries` | list[ExampleEntry] | array of nested |
| `example_entries[n].example_heading` | StringText | scalar |
| `example_entries[n].example_text` | StringMarkdown | scalar |

### Style Controls

- `heading` — section heading: "Examples", "Calibration Examples", "Reference Examples"
- `heading_level` — H2 for the section; H3 for group names is the established convention
- `group_heading_level` — knob: H3 (established/fossil) vs. H2 — the "fossil" designation in the key facts means H3 is the existing behavior but not necessarily correct; this is a benchmark axis
- `entry_heading_level` — knob: H4 (established) when `example_display_headings` is true
- `entries_intro` — prose before entries within a group: no intro (group heading is sufficient) vs. minimal prose
- `omit_behavior` for `example_display_headings = false` — when false: entries render without H4 headings, as sequential blocks; when true: each entry gets an H4 heading from `example_heading`
- `omit_behavior` for `examples_max_number` — when None: all entries render; when present: truncate to max (style decides whether to signal truncation)
- `max_number_truncation_signal` — whether to render a note when examples are truncated: "(showing {n} of {total})" or silent truncation

### Display Controls

- `groups` → `mode`: sequential is the only sensible mode (groups are structural blocks, not list items); "bulleted groups" is nonsensical
- `example_entries` (within a group) → `mode`: sequential is the natural form when headings are shown; numbered list is an alternative when headings are hidden
- `example_text` renders as-is (StringMarkdown passthrough) — display mode does not apply to the text content itself

### Conditionals

- `examples` section is optional on AgentAnthropicRender — when None, omit section entirely
- `example_display_headings` default is false — most groups render entries without individual headings
- `examples_max_number` gates truncation: when present and list exceeds max, slice to first N entries

### Non-Obvious Design Decisions

1. `example_display_headings` is a data field (Boolean) that acts as a style control. It lives on the data model because it was captured at definition time. But it functions as a per-group display override. The question is whether the style TOML should be able to override this field's effect — "always show headings regardless of data" or "respect whatever the data says". Most likely: data field wins, style cannot override.
2. `examples_max_number` similarly is a data field that controls rendering quantity. It was captured during prompt reduction to stay within context limits. The composition engine must apply this before rendering.
3. The section is among the most markdown-heavy. Each `example_text` is StringMarkdown that may be multi-paragraph with code blocks, GOOD/BAD comparisons, etc. The container is essentially a passthrough for example text — the rendering work is structural framing, not prose generation.

---

## 7. output

**Purpose:** Describes what the agent produces: format, file location, naming rules, and optional schema.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `description` | OutputDescription (StringText) | scalar |
| `format` | OutputFormatKind (enum: jsonl/json/markdown/text) | scalar |
| `name_known` | OutputNameKnown (enum: known/partially/unknown) | scalar |
| `schema_path` | PathExistsAbsolute | scalar, optional |
| `output_file` | PathAbsolute | scalar, optional |
| `output_directory` | PathAbsolute | scalar, optional |
| `name_template` | FilenameTemplate | scalar, optional |
| `name_instruction` | StringProse | scalar, optional |
| `schema_embed` | Boolean | scalar, optional |

### Style Controls

- `heading` — knob: "Output", "What You Produce", "Output Format"
- `heading_level` — H2
- `description_label` — label before description: "Output:" or no label
- `format_label` — label before format enum: "Format:", "File format:", or inline in description
- `format_display_map` — maps enum values to human-readable: "jsonl" → "JSONL", "markdown" → "Markdown"
- `schema_label` — label before schema_path: "Schema:", "Validates against:", "Output schema:"
- `schema_embed_display` — when `schema_embed` is true: the schema content is embedded inline; when false: render the path with a "read on first invocation" note; when None: no schema rendering
- `output_file_label` — label: "Output file:", "Write to:", "Target file:"
- `output_directory_label` — label: "Output directory:", "Write to:", "Target directory:"
- `name_template_label` — label: "Filename pattern:", "Name template:", "Filename:"
- `name_instruction_label` — label: "Naming instruction:", "Filename:", "How to name output:"
- `name_known_display` — whether to render the `name_known` enum value at all (partially/known/unknown) vs. let the template/instruction fields implicitly communicate this
- `omit_behavior` for `schema_path` — when None: no schema block
- `omit_behavior` for `output_file` — when None and name_known="known": contradiction — gate enforcement handles this
- `omit_behavior` for `output_directory` — when None: no directory block
- `omit_behavior` for `name_template` — when None: no template block
- `omit_behavior` for `name_instruction` — when None: no naming instruction block

### Display Controls

- No arrays in output section — all fields are scalars or optional scalars
- `format` is a single enum value — inline rendering only

### Conditionals

- `output.format` is a pipeline control consumed before rendering — but it still appears in the output data model and may need to render for agent awareness
- `schema_embed = true` → embed schema content inline (Galdr reads the schema file at `schema_path` and inlines it)
- `schema_embed = false` or None → render `schema_path` as a read-access path reference
- `name_known = known` → `output_file` present, `output_directory` and `name_template` and `name_instruction` absent
- `name_known = partially` → `output_directory` and `name_template` present, `output_file` and `name_instruction` absent
- `name_known = unknown` → `output_directory` and `name_instruction` present, `output_file` and `name_template` absent
- `name_known` gates which path/naming fields are present — the container must handle all three branches

### Non-Obvious Design Decisions

1. `output.format` is described as "a pipeline control consumed before rendering — not agent-facing" in the key facts. However, the agent needs to know what format to write. The question is whether `output.format` should render in the output section (as "you produce JSONL") or be suppressed here because the `writing_output` invocation display makes it implicit. Both are defensible. The benchmark should test both.
2. `schema_embed` triggers Galdr reading the schema file and inlining it — this is a significant rendering behavior. The style controls whether embedded schema gets a code block fence, a heading, and introductory prose.
3. The `name_known` enum creates three structurally different output sections. A single item_template cannot cover all three. The container needs three template branches, each with its own label/prose controls.

---

## 8. writing_output

**Purpose:** The exact tool invocation pattern the agent must use when writing output. Only present when `has_output_tool = true`.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `tool_name` | ToolName (SnakeString) | scalar |
| `invocation_variant` | InvocationVariant (enum: no-name/with-name) | scalar |
| `invocation_display` | InvocationDisplay (StringText) | scalar — pre-composed bash heredoc |
| `name_needed` | OutputToolNameNeeded (Boolean) | scalar |
| `name_pattern` | FilenameTemplate | scalar, optional |
| `batch_size` | OutputToolBatchSize (Integer, default 20) | scalar |
| `schema_path` | OutputToolSchemaXAbs | scalar, optional |
| `file_path` | PathAbsolute | scalar, optional |
| `directory_path` | PathAbsolute | scalar, optional |

### Style Controls

- `heading` — knob: "Writing Output", "Output Tool", "How To Write Output"
- `heading_level` — H2
- `preamble` — prose before the invocation display: "Use the following tool to write each output record:" vs. "Write output using this command:" vs. no preamble
- `batch_size_prose` — how to render batch_size: "Invoke the tool every {batch_size} records." vs. "Batch size: {batch_size} records per call." vs. a full behavioral instruction sentence
- `name_pattern_label` — label for name_pattern when present: "Filename pattern:", "Output name template:"
- `name_needed_display` — whether to render name_needed as behavioral instruction ("Provide the output filename on each invocation") or let the invocation_display template make it implicit
- `schema_path_label` — label if schema_path renders separately from invocation_display: "Schema:", "Validates against:" — usually the invocation_display already incorporates schema handling
- `omit_behavior` for `name_pattern` — when None and invocation_variant=no-name: no pattern block
- `omit_behavior` for `schema_path` — when None: no schema block in this section (schema handling is embedded in invocation_display)
- `omit_behavior` for `file_path` — when None: use directory_path instead
- `omit_behavior` for `directory_path` — when None: use file_path instead
- `invocation_display_format` — the invocation_display is a pre-composed bash heredoc string; the style controls whether it renders in a code block fence (```bash) or as raw text

### Display Controls

- No arrays — all fields are scalars
- `invocation_display` is a pre-composed multi-line string; display mode is whether to wrap it in a code fence and what language tag to use

### Conditionals

- Entire section is optional (WritingOutputAnthropic | None) — absent when `has_output_tool = false`
- `name_pattern` present ↔ `invocation_variant = with-name`
- `file_path` present ↔ `name_known = known`
- `directory_path` present ↔ `name_known = partially` or `name_known = unknown`

### Non-Obvious Design Decisions

1. `invocation_display` is a pre-composed string that already embeds the tool name, heredoc syntax, and placeholder structure. The style knob is primarily about whether to wrap it in a code fence and what prose introduces it. The content itself is not a style surface — it is data.
2. `batch_size` appears on both `writing_output` and `critical_rules`. They are denormalized copies. The writing_output container renders the batch_size as behavioral context; the critical_rules section renders it as a hard rule. Style must not double-render a confusing duplicate — the recipe controls which section renders which aspect.
3. The section assumes `has_output_tool = true`. The recipe should not include this section when `has_output_tool = false`. This is a recipe-level gate, not a container-level conditional.

---

## 9. constraints

**Purpose:** MUST and NEVER rules the agent must follow. Behavioral boundaries.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `rules` | list[GuardrailsConstraint] (list[StringProse]) | array |

### Style Controls

- `heading` — knob: "Constraints", "Rules", "Behavioral Constraints", "MUST Follow"
- `heading_level` — H2 or H3; the key facts flag H3 as a fossil — H2 is correct going forward
- `intro_prose` — prose before the rules list: "You must follow these constraints:" vs. "The following rules apply:" vs. no intro (heading is sufficient)
- `footer_prose` — prose after the rules list: "Violating any constraint is a FAILURE." vs. no footer
- `omit_behavior` — entire section is optional; when None, omit entirely

### Display Controls

- `rules` → `mode`: bulleted is the natural form; numbered is an alternative that implies priority ordering; sequential (each rule as a paragraph) is an option for very long rules
- `rules` items are StringProse (complete sentences) — they render as-is without additional item_template wrapping beyond the list marker

### Conditionals

- Section is optional (Constraints | None on AgentAnthropicRender) — when None: omit entirely

### Non-Obvious Design Decisions

1. Heading level is flagged as H3 being a fossil. The benchmark should test H2 vs. H3 to determine whether heading level affects constraint adherence. H2 signals equal weight with other major sections; H3 signals subordination.
2. Rules are complete prose sentences — no label or template wrapping needed. The display mode (bulleted vs. numbered) is the primary knob.
3. The section has no sub-structure — it is a flat list of prose strings. Style and display controls are minimal compared to criteria sections.

---

## 10. anti_patterns

**Purpose:** Common mistakes the agent should avoid. Observed or anticipated failure modes.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `patterns` | list[GuardrailsAntiPattern] (list[StringProse]) | array |

### Style Controls

- `heading` — knob: "Anti-Patterns", "Common Mistakes", "What To Avoid", "Don't Do This"
- `heading_level` — H2 or H3; same fossil situation as constraints — H2 is correct going forward
- `intro_prose` — prose before the patterns list: "Avoid these known failure modes:" vs. no intro
- `footer_prose` — prose after: no standard footer for anti-patterns
- `omit_behavior` — entire section optional; when None, omit entirely

### Display Controls

- `patterns` → `mode`: bulleted is the natural form; numbered is an alternative
- Pattern items are StringProse complete sentences — render as-is

### Conditionals

- Section is optional (AntiPatterns | None) — when None: omit entirely

### Non-Obvious Design Decisions

1. Heading level fossil — same issue as constraints. H2 vs. H3 benchmark applies.
2. Anti-patterns and constraints are structurally identical (both are flat lists of StringProse). The style controls are the same; only the heading and framing prose differ. A shared list-section template could serve both, parameterized by heading and intro text.
3. The behavioral distinction between "constraint" (MUST/NEVER) and "anti-pattern" (common mistake) is carried by the content, not the structure. Style could reinforce this distinction with different intro language or markers.

---

## 11. success_criteria

**Purpose:** Defines what success means. Composed of one or more success items, each with a definition sentence and observable evidence bullets.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `criteria` | list[SuccessItem] | array of nested |
| `criteria[n].success_definition` | SuccessDefinition (StringProse) | scalar |
| `criteria[n].success_evidence` | list[StringProse] | array |

### Style Controls

- `heading` — knob: "Success Criteria", "What Success Looks Like", "Done When"
- `heading_level` — H2 or H3; same fossil flag as constraints — H2 going forward
- `intro_prose` — prose before criteria: no intro vs. "This agent succeeds when:" vs. minimal framing
- `definition_label` — label before each success_definition: "Success:" vs. no label (definition is a complete sentence that stands alone)
- `evidence_label` — label before evidence list: "Evidence:" vs. "Observable evidence:" vs. no label
- `omit_behavior` — entire section optional; when None: omit entirely

### Display Controls

- `criteria` → `mode`: sequential is the natural form (each criterion is a block of definition + evidence); numbered for multiple criteria; bulleted for a single-criterion list (unusual)
- `success_evidence` → `mode`: bulleted is the natural form for evidence items; numbered implies priority; inline would lose clarity
- `success_evidence` → `item_template`: no template needed — items are complete sentences

### Conditionals

- Section is optional (SuccessCriteria | None) — when None: omit entirely
- `success_evidence` has min_length=1 — always present on each SuccessItem, never None

### Non-Obvious Design Decisions

1. Heading level fossil — H2 going forward.
2. Multiple success criteria in `criteria` list are independent items. The display mode for `criteria` controls how they relate visually: sequential blocks (distinct) vs. numbered list (ordered priority). In practice, most agents have one success criterion.
3. The `success_definition` sentence and `evidence` list form a paired unit. Style must decide whether to render definition inline with a label, or as a heading for the evidence sub-list. Option A: "**Success:** {sentence}\n- {evidence}" vs. Option B: "#### {sentence}\n- {evidence}".

---

## 12. failure_criteria

**Purpose:** Defines what failure means (process failure, not data failure). Structurally identical to success_criteria with inverted semantics.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `criteria` | list[FailureItem] | array of nested |
| `criteria[n].failure_definition` | FailureDefinition (StringProse) | scalar |
| `criteria[n].failure_evidence` | list[StringProse] | array |

### Style Controls

- `heading` — knob: "Failure Criteria", "What Failure Looks Like", "Process Failure"
- `heading_level` — H2 or H3; fossil flag applies; H2 going forward
- `intro_prose` — "This agent has failed if:" vs. no intro
- `definition_label` — label: "Failure:" vs. no label
- `evidence_label` — "Evidence:" vs. no label
- `failure_distinction_prose` — optional prose establishing the process-vs-data distinction: "Failure refers to the processing pipeline, not the data quality." vs. omit (the definition sentence captures this)
- `omit_behavior` — entire section optional; when None: omit

### Display Controls

- `criteria` → `mode`: sequential (same reasoning as success_criteria)
- `failure_evidence` → `mode`: bulleted

### Conditionals

- Section is optional — when None: omit
- `failure_evidence` min_length=1 — always present

### Non-Obvious Design Decisions

1. Success and failure criteria are structurally identical. A single criteria-section template parameterized by polarity (success/failure) would serve both. The style knobs are the heading, intro prose, and definition/evidence labels.
2. The failure_definition has an embedded semantic constraint (process failure, not data failure) that a style could reinforce or not. The "failure distinction prose" control is for cases where the definition sentence alone may not signal this clearly enough.

---

## 13. return_format

**Purpose:** How the agent reports results: return mode, optional instructions for status/metrics/output, optional schema for structured returns.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `mode` | ReturnMode (enum: status/status-metrics/metrics-output/output) | scalar |
| `return_schema` | PathExistsAbsolute | scalar, optional |
| `status_instruction` | StringProse | scalar, optional |
| `metrics_instruction` | StringProse | scalar, optional |
| `output_instruction` | StringProse | scalar, optional |

### Style Controls

- `heading` — knob: "Return Format", "How To Respond", "Reporting", "Return"
- `heading_level` — H2
- `mode_label` — label before mode value: "Return mode:" or inline
- `mode_display_map` — maps enum to human-readable: "status" → "status only", "status-metrics" → "status with metrics", "metrics-output" → "metrics with output", "output" → "inline output"
- `status_label` — label before status_instruction: "Status:" or no label (instruction is complete prose)
- `metrics_label` — label before metrics_instruction: "Metrics:" or no label
- `output_label` — label before output_instruction: "Output:" or no label
- `schema_label` — label before return_schema path: "Return schema:", "Schema:"
- `schema_embed_behavior` — return_schema is always a path reference (no schema_embed flag on ReturnFormat); style decides whether to render the schema inline or as a path to read
- `omit_behavior` for `return_schema` — when None: no schema block
- `omit_behavior` for `status_instruction` — when None: no status block; instructions only render when `mode` includes their component
- `omit_behavior` for `metrics_instruction` — when None: no metrics block
- `omit_behavior` for `output_instruction` — when None: no output block

### Display Controls

- No arrays — all fields are scalars or optional scalars

### Conditionals

- `mode` determines which instruction fields are relevant:
  - `status` → `status_instruction` only (metrics and output absent)
  - `status-metrics` → `status_instruction` and `metrics_instruction`
  - `metrics-output` → `metrics_instruction` and `output_instruction`
  - `output` → `output_instruction` only
- `return_schema` is present when mode includes structured metrics or output; None for pure status return

### Non-Obvious Design Decisions

1. The `mode` enum has four values, each enabling different combinations of instruction fields. The container must render only the instructions relevant to the selected mode. Style controls whether the mode value itself is rendered (as a label or signal) or whether the instructions implicitly communicate the mode.
2. `return_schema` on ReturnFormat does not have a `schema_embed` flag (unlike `output.schema_embed`). If the return schema should be embedded inline, the container must make that decision from the style config alone, not from a data flag.
3. All instruction fields are StringProse — complete sentences that stand alone. The style choice is whether to prefix with a label or render as plain prose blocks.

---

## 14. critical_rules

**Purpose:** End-of-lifecycle synthesis section. Contains the most style-heavy rendering in the system. Data fields are conditionals and interpolation values; almost all rendered content comes from style templates.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `has_output_tool` | Boolean | scalar — primary conditional gate |
| `tool_name` | ToolName (SnakeString) | scalar, optional — present when `has_output_tool = true` |
| `name_needed` | OutputToolNameNeeded (Boolean) | scalar, optional — present when `has_output_tool = true` |
| `batch_size` | OutputToolBatchSize (Integer, default 20) | scalar |

### Style Controls

This section is almost entirely style. The data fields gate which rules render and provide interpolation values.

- `heading` — knob: "Critical Rules", "Operational Rules", "Non-Negotiable Rules"
- `heading_level` — H2
- `rules_mode` — how the rules render: numbered list (numbered is natural for rules with implied priority) vs. bulleted
- `workspace_path_rule` — template that renders workspace confinement rule using `workspace_path` (extracted from SecurityBoundaryAnthropic): "All file operations MUST remain within {workspace_path}." The workspace_path value is the interpolation; the rule text is pure style.
- `no_output_tool_rules` — list of style-defined rules rendered when `has_output_tool = false`: standard write discipline rules (use Write tool, etc.)
- `output_tool_base_rules` — list of style-defined rules rendered when `has_output_tool = true` (regardless of name_needed): rules about using `{tool_name}` exclusively
- `output_tool_named_rules` — additional rules rendered when `has_output_tool = true` AND `name_needed = true`: rules about providing the filename argument
- `output_tool_unnamed_rules` — rules rendered when `has_output_tool = true` AND `name_needed = false`: rules about not providing filename
- `batch_size_rule_template` — template: "Invoke the output tool every {batch_size} records." — rendered when `has_output_tool = true`; the integer value is the interpolation
- `fail_fast_rule` — fixed rule string: "Fail fast — if something is wrong, call FAILURE immediately." This is pure style with no data interpolation
- `no_partial_output_rule` — fixed rule: "Never produce partial output or abandon mid-batch." Pure style
- `tool_name_template` — inline template for rule sentences that reference the tool name: "Use {tool_name} for every write operation." vs. "Only invoke {tool_name} — never Write or Edit directly."
- `omit_behavior` for `tool_name` — when None (`has_output_tool = false`): tool-name-referencing rules do not render; replace with standard-write rules
- `omit_behavior` for `name_needed` — when None: name-related rules do not render

### Display Controls

- The rules list is generated by the style system, not directly from data — it is assembled from style templates with data interpolations
- `rules_mode`: numbered is natural (rules with implied priority ordering)
- No item_template needed — each rule is a complete sentence generated by the style

### Conditionals (the primary function of this section's data)

```
has_output_tool = false:
  → render: workspace rule, no-output-tool rules, fail-fast rule, no-partial-output rule

has_output_tool = true, name_needed = false:
  → render: workspace rule, output-tool-base rules (with tool_name interpolation),
            output-tool-unnamed rules, batch-size rule (with batch_size interpolation),
            fail-fast rule, no-partial-output rule

has_output_tool = true, name_needed = true:
  → render: workspace rule, output-tool-base rules (with tool_name interpolation),
            output-tool-named rules, batch-size rule (with batch_size interpolation),
            fail-fast rule, no-partial-output rule
```

### Non-Obvious Design Decisions

1. Critical_rules is the style-heaviest section. The data fields are almost entirely conditional gates and interpolation values. The actual rule text is defined in the style TOML, not in the data. This means the style TOML for this section is substantially larger than for other sections.
2. `workspace_path` is not a field on CriticalRules in the Pydantic model — it lives on SecurityBoundaryAnthropic. The container for critical_rules must receive workspace_path as an additional input, or the recipe must explicitly pass it. This is a design decision for the container interface: does critical_rules receive the full data model and extract workspace_path, or does the composition engine inject it?
3. `batch_size` has a default of 20 via `default_factory`. The container must handle the case where batch_size is present (even when `has_output_tool = false`) by suppressing the batch rule. The `has_output_tool` flag is the gate, not the presence of `batch_size`.
4. The style template for `tool_name_template` must gracefully handle snake_case tool names (e.g., `append_interview_summaries_record`). If the style renders the tool name in a sentence, it must not attempt to human-format it. Render verbatim in monospace: `{tool_name}`.

---

## 15. dispatcher

**Purpose:** Fixed-structure section that feeds a separate skill generation path. Not recipe-driven. Listed here for completeness.

### Fields

| Field | Type | Classification |
|-------|------|----------------|
| `agent_name` | AgentName (kebab-case str) | scalar |
| `agent_description` | AgentDescription (StringProse) | scalar |
| `dispatch_mode` | DispatchMode (enum: batch/full) | scalar |
| `background_mode` | DispatchBackgroundMode (enum: allowed/required/forbidden) | scalar |
| `input_format` | DispatchInputFormat (enum: jsonl/json/text) | scalar |
| `input_delivery` | DispatchInputDelivery (enum: tempfile/inline/file/directory) | scalar |
| `input_description` | InputDescription (StringText) | scalar |
| `output_format` | OutputFormatKind (enum: jsonl/json/markdown/text) | scalar |
| `output_name_known` | OutputNameKnown (enum: known/partially/unknown) | scalar |
| `return_mode` | ReturnMode (enum) | scalar |
| `max_agents` | Integer | scalar, optional (default 6) |
| `batch_size` | DispatchBatchSize (tuple[Integer, Integer]) | scalar, optional — present when `dispatch_mode = batch` |
| `parameters` | list[ParameterItem] | array of nested, optional |

### Style Controls

- Dispatcher is described as "fixed-structure, not recipe-driven" in the key facts. This means the dispatcher section has a fixed rendering format rather than configurable style/display knobs.
- `heading` — if dispatcher renders in the skill TOML, its heading structure follows the skill format, not the agent prompt format
- `description_label` — "Description:" for the skill file
- `mode_display_maps` — enum values need human-readable rendering in the skill file (same maps as input section)
- `parameters_intro` — same as input section parameters intro

### Display Controls

- `parameters` → `mode`: bulleted (same as input section)
- `parameters` → `item_template`: same as input section

### Conditionals

- `batch_size` present ↔ `dispatch_mode = batch`
- `parameters` optional — when None: no parameters block in skill

### Non-Obvious Design Decisions

1. Dispatcher generates a skill file, not an agent prompt section. Its rendering target is different from all other sections. The style/display machinery may be a separate renderer, not the same section container infrastructure.
2. `output_format` on dispatcher IS a pipeline control here too (like `output.format` on the agent side). Whether it renders in the skill file is an open question — the skill consumer may or may not need to know the agent's output format.
3. `max_agents` has a default of 6. When 6 is the value, the style must decide whether to render it verbatim or suppress the default (show only when non-default).

---

## Cross-Section Design Decisions

### Workspace Path Threading

`workspace_path` lives on `SecurityBoundaryAnthropic` but must render in `critical_rules`. The container interface must either:
- A. Pass the full `AgentAnthropicRender` model to every container and let each extract what it needs, or
- B. Have the composition engine extract `workspace_path` and inject it as an additional input to the `critical_rules` container

Option A is simpler but violates section isolation. Option B maintains isolation at the cost of explicit injection plumbing.

### Duplicate Fields

Several fields appear on multiple sections:
- `title` and `description` appear on both `frontmatter` and `identity` (identical values)
- `model` appears on both `frontmatter` and `identity`
- `batch_size` appears on both `critical_rules` and `writing_output`

The recipe controls which section renders each. Style must ensure the duplicate does not produce contradictory prose in the same rendered output.

### Optional Section Omission

The recipe drops sections not listed in its `modules`. But several sections are optionally null in the data model. When a section is listed in the recipe but its data is None, the container must return an empty string — the recipe iterates and silently omits zero-length outputs. This is the correct behavior; it does not require explicit recipe gates.

### Heading Level Fossil

Key facts establish that H3 on constraints/anti_patterns/success_criteria/failure_criteria is a fossil. The knob for all four sections should default to H2, with H3 available as a variant for benchmarking against the established behavior.

### Schema Embedding

Two sections have schema embedding behavior:
- `output` has `schema_embed` (Boolean field on data model) — data field controls embedding
- `writing_output` embeds the schema implicitly in `invocation_display` (pre-composed)
- `return_format` has `return_schema` but no `schema_embed` flag — style must decide whether to embed

The embedding decision for return_format is a non-obvious gap: the data model provides no control for it. Style config must supply the decision.

### Display Mode Defaults

When a display TOML omits a field, the container needs a fallback. Recommended defaults:
- List of strings → `bulleted`
- List of nested items → `sequential`
- Short string array (expertise) → `inline`
- Instruction steps → `numbered`
- Evidence lists → `bulleted`

These defaults should be baked into the container, not required from every display TOML variant.
