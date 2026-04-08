# Output-Driven Knobs v3

Derived by examining the rendered outputs and working backwards to every piece of non-data text and every formatting decision. Two agents examined: `agent-builder` (no output tool) and `interview-enrich-create-summary` (has output tool). All section headings, labels, templates, structural elements, and display decisions catalogued below.

---

## Method

For each section: quote the non-data text verbatim, tag its category, identify the display mode for arrays, note differences between agents, flag non-obvious decisions.

Categories: `heading`, `label`, `template`, `prose`, `footer`, `separator`, `structural`

---

## FRONTMATTER

Rendered as YAML frontmatter block delimited by `---`.

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `---` (opening) | structural | Code fence variant — YAML block delimiter |
| `---` (closing) | structural | Pair with opening |
| `name:` | label | YAML key |
| `description:` | label | YAML key |
| `tools:` | label | YAML key |
| `model:` | label | YAML key |
| `permissionMode:` | label | YAML key |
| `hooks:` | label | YAML key |
| `PreToolUse:` | label | YAML key, hardcoded hook phase name |
| `- matcher:` | label | YAML key |
| `hooks:` | label | YAML key (nested) |
| `- type: command` | label | YAML key + value |
| `command:` | label | YAML key |

### Display Decisions

- `tools` array: rendered `inline` with `, ` separator (e.g., `"Bash, Glob, Grep, Read"`)
- Hook `matcher` field: tools rendered `inline` with `|` separator (e.g., `Glob|Grep|Read`)
- Hook paths: rendered as one long comma-separated string in the command value, no line breaks

### Knobs Required

- `tools_separator` — `, ` vs other separators
- `hook_matcher_separator` — `|` between tool names in matcher
- The hook block rendering is entirely structural — the YAML schema is fixed, not parameterized through style/display

### Notes

- The frontmatter is YAML, not markdown. Its "style" is the YAML key names themselves, which are dictated by the Claude Code agent spec. These are not style knobs — they are required field names. Only the inline rendering of arrays within YAML values is a display knob.
- `hook_intercept_subagent_tool` and `hook_intercept_subagent_bash` are tool invocation templates. These appear in the `command:` value. They are generated from security boundary data — the rendering template is a knob.

---

## IDENTITY (rendered at top of body, before first HR)

### Rendered output (agent-builder)

```
# Agent Builder

**Purpose:** Creates new agent TOML definitions and include files from requirements and preparation packages, producing complete definitions ready for the pipeline.

You are a definition author.

You create agent definitions from requirements. You translate domain knowledge into structured TOML fields, bland instruction steps, and boringly correct calibration examples. Your definitions are data forms, not prose documents. Every field has a purpose, every instruction step captures one judgment task, and everything else is left for the template system to generate.

**Your responsibility:** Read the preparation package, design the agent's role and instruction steps, create calibration examples, write guardrails and criteria, set security grants, validate conditional rules, and produce a complete TOML definition with include files.

**Expertise:** agent definition architecture, domain knowledge extraction, calibration example design, minimum permission security modeling
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `# {title}` | heading | H1, interpolated with `title` field |
| `**Purpose:**` | label | Bold label preceding `description` |
| `You are a {role_identity}.` | template | Sentence wrapping `role_identity` |
| `**Your responsibility:**` | label | Bold label preceding `role_responsibility` |
| `**Expertise:**` | label | Bold label preceding `role_expertise` array |

### Display Decisions

- `role_expertise` array: `inline` with `, ` separator
- `role_description`: rendered as bare paragraph (no label, no bold)
- `role_identity`: embedded in sentence template, not rendered as standalone field
- `description` vs `role_description`: `description` gets the `**Purpose:**` label; `role_description` is unlabeled prose

### Differences Between Agents

None — both render identically with the same non-data text. `role_identity` differs in value but template is the same.

### Non-Obvious Decisions

- `description` and `role_description` are separate fields in the data. `description` appears first under `**Purpose:**`. `role_description` appears below as an unlabeled paragraph. This ordering (description → role_identity sentence → role_description → responsibility → expertise) is a style decision encoded nowhere explicit.
- `role_identity` is the only field not rendered standalone — it is always embedded in the sentence template `"You are a {role_identity}."` This is the one template in the identity section.
- `title` is used for the H1 heading. In the data, `title` and `name` exist in both `[identity]` and `[frontmatter]` — the heading uses `identity.title`.

### Knobs Required

- `heading_level` — currently H1 (fossil, should be configurable)
- `purpose_label` — `"**Purpose:**"` (bold formatting + text)
- `role_template` — `"You are a {role_identity}."` (full sentence template)
- `responsibility_label` — `"**Your responsibility:**"`
- `expertise_label` — `"**Expertise:**"`
- `expertise_separator` — `", "` (display)
- `expertise_display` — `"inline"` (display mode)

---

## SECURITY BOUNDARY

### Rendered output (agent-builder)

```
## Security Boundary

This agent operates under `bypassPermissions` with hook-based restrictions.

The following operations are allowed — everything else is blocked by the system.

**Glob, Grep, Read, find:** `./definitions/agents/agent-template.toml`
**Glob, Grep, Read, find:** `./definitions/audit/`
...

Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Security Boundary` | heading | H2 (fossil — heading_level knob) |
| `This agent operates under \`bypassPermissions\` with hook-based restrictions.` | prose | Preamble; `bypassPermissions` is data (permission_mode field) embedded in prose template |
| `The following operations are allowed — everything else is blocked by the system.` | prose | Grants intro |
| `Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.` | prose | Boundary warning / footer |

### Entry Template (per display entry)

Each `[[security_boundary.display]]` entry renders as:

```
**{tools_joined}:** `{path}`
```

Where `tools_joined` is the tools array joined inline with `, `. This is a compound template: bold label containing the tools list, followed by backtick-wrapped path.

### Display Decisions

- `security_boundary.display` array: `sequential` — each entry on its own line, no blank lines between entries
- Per-entry `tools` array: `inline` with `, ` separator, rendered inside bold
- `path` field: wrapped in backticks (structural/template decision)
- `tools` rendered as `**{tools}:**` — tools are the label, path is the value (inverted from a typical key: value pattern)

### Differences Between Agents

- `interview-enrich-create-summary` has no `[[security_boundary.display]]` entries (no tool grants listed) — the entire grants block is absent
- The section still appears (or would appear) with the prose preamble — unclear if section is dropped entirely when no entries exist

### Non-Obvious Decisions

- Tools and path are combined into a single line where tools act as the label. This is not obvious — an alternative would be `path: tools` or separate paragraphs.
- `permission_mode` from frontmatter is embedded in the preamble prose. This crosses section boundaries — the style template references data from `frontmatter`, not from `security_boundary`. This is a cross-section data reference.
- `workspace_path` is on `[security_boundary]` but is NOT rendered in the body — it is used only in hook generation (frontmatter). It is a pipeline control, not a display field. Worth noting as established fact.

### Knobs Required

- `heading` — `"Security Boundary"`
- `heading_level` — currently H2
- `preamble` — `"This agent operates under \`{permission_mode}\` with hook-based restrictions."` (template, crosses into frontmatter data)
- `grants_intro` — `"The following operations are allowed — everything else is blocked by the system."`
- `entry_template` — `"**{tools}:** \`{path}\`"` (per-entry template combining tools and path)
- `tools_separator` — `", "` (within entry template)
- `entries_display` — `"sequential"` (one per line, no blank lines)
- `boundary_warning` — `"Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."`

---

## INPUT

### Rendered output (agent-builder)

```
## Input

Preparation package containing requirements, domain analysis, data shapes, and schema references

The dispatcher provides:
- tempfile (path): Path to the preparation package

**Required context:**
- **Agent Template Reference:** `/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-template.toml`
- **Definition System Architecture:** `/Users/johnny/.ai/spaces/bragi/definitions/prompts/agent-definition-mindset/one-definition-many-agents.md`
...
```

### Rendered output (interview-enrich-create-summary)

```
## Input

Stripped interview exchanges with exchange number, agent question, and user response — no learned, threads, or insight fields

The dispatcher provides:
- tempfile (path): Path to the JSONL tempfile containing stripped interview exchanges
- uid (string): Interview identifier used for output filename construction
```

Note: no `**Required context:**` block — interview-enrich-create-summary has no `context_required` entries.

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Input` | heading | H2 (fossil) |
| `The dispatcher provides:` | prose | Intro to parameters list |
| `**Required context:**` | label | Bold label, only appears when context_required is non-empty |

### Parameter Entry Template

```
- {param_name} ({param_type}): {param_description}
```

Each parameter renders as a bulleted item combining three fields. Optional parameters would need an additional suffix (e.g., `(optional)` after param_type — not yet seen in rendered output but referenced in AGENT_BUILD_SYSTEM.md example).

### Context Entry Template

```
- **{context_label}:** `{context_path}`
```

Bold label followed by backtick-wrapped path.

### Display Decisions

- `parameters` array: `bulleted` — `- ` prefix per item
- `context_required` array: `bulleted` — `- ` prefix per item
- `context_available` array: not seen in these agents (would also be bulleted per display spec)
- Parameters block omitted entirely when empty (not visible here — both agents have parameters)
- Context block omitted entirely when no context entries

### Differences Between Agents

- agent-builder: 1 parameter, 7 context_required entries
- interview-enrich-create-summary: 2 parameters, 0 context entries → `**Required context:**` block absent entirely
- Format of delivery is shown in section description (text vs jsonl) but `delivery` field itself (`tempfile`) is reflected in the prose `"The dispatcher provides:"` rather than rendered explicitly

### Non-Obvious Decisions

- `delivery` field value (`tempfile`) is not rendered as a standalone label — it is implied by the section heading and `"The dispatcher provides:"` prose. The actual delivery mechanism is surfaced structurally, not as data.
- `format` field (text/jsonl) is not rendered in this section. It appears only in the dispatcher skill. This is intentional by design.
- `input_schema` is not present in either agent's data — when present, it would require an `schema_intro` prose and entry template.

### Knobs Required

- `heading` — `"Input"`
- `heading_level` — currently H2
- `parameters_intro` — `"The dispatcher provides:"`
- `param_entry_template` — `"{param_name} ({param_type}): {param_description}"` (combined field template)
- `optional_suffix` — suffix to append to param_type for optional params (e.g., `", optional"`)
- `parameters_display` — `"bulleted"`
- `context_required_label` — `"**Required context:**"`
- `context_required_display` — `"bulleted"`
- `context_entry_template` — `"**{context_label}:** \`{context_path}\`"`
- `context_available_label` — (parallel to context_required_label, not yet seen)
- `context_available_display` — `"bulleted"` (per design spec)
- `schema_intro` — for input_schema display (not yet exercised)

---

## INSTRUCTIONS (rendered as "Processing")

### Rendered output (agent-builder, first two steps shown)

```
## Processing

Read the preparation package from the tempfile path. Read all context_required documents (mindset documents and agent-template.toml). The template defines every valid field, its type, its constraints, and its conditional dependencies.

Identify the agent's core domain from the requirements. What does this agent judge, assess, evaluate, or transform? What mental model should it hold? What expertise does it need?

Write the role fields: role_identity (2-3 words), role_description (what it does and why, written as direct address), role_responsibility (the specific deliverable), role_expertise (3-4 domain skills).

Role text should be bland and precise. No aspirational language. No "you will excel at." State what the agent does.
...
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Processing` | heading | H2 — note: NOT "Instructions". The heading differs from the section name. This is a style knob. |

### Display Decisions

- `steps` array: `sequential` — each step text is a paragraph (or multi-paragraph block) separated by blank lines
- `instruction_mode` field: NOT RENDERED — this is the known bug. Mode (`deterministic`/`probabilistic`) does not appear in the output. In the rebuild it MUST be rendered.
- Steps are not numbered, not bulleted — raw paragraphs concatenated with blank lines

### Differences Between Agents

No structural difference — both use sequential paragraph rendering. interview-enrich-create-summary has 5 steps, agent-builder has 7. Both render identically in structure.

### instruction_mode Rendering (Required in Rebuild)

This is a bug in the current renderer. `instruction_mode` must be rendered. Options (to be decided):
- Prefix label: `[DETERMINISTIC]` or `[PROBABILISTIC]` before each step text
- Inline badge: `**Deterministic:**` or `**Probabilistic:**`
- Numbered with mode: `1. [deterministic] Read the input...`

The knob `mode_label_deterministic` and `mode_label_probabilistic` need to exist in style. The knob `steps_display` controls whether steps are numbered, bulleted, or sequential. A per-step mode label knob controls how the mode appears within each step.

### Non-Obvious Decisions

- The section heading is `"Processing"` not `"Instructions"`. This diverges from the section name in the data model (`instructions`). The heading is therefore a pure style knob — the data section is always `instructions`, the heading displayed is configurable.
- Multi-paragraph step texts (instruction_text with embedded newlines) render as-is inside the sequential output. No wrapping or stripping of internal structure.

### Knobs Required

- `heading` — `"Processing"` (not "Instructions" — pure style)
- `heading_level` — currently H2
- `steps_display` — `"sequential"` (paragraphs separated by blank lines)
- `mode_label_deterministic` — e.g., `"[DETERMINISTIC]"` or `""` (empty = not rendered, bug state)
- `mode_label_probabilistic` — e.g., `"[PROBABILISTIC]"` or `""`
- `mode_label_position` — where mode label appears: `"prefix"`, `"inline"`, `"badge"`

---

## EXAMPLES

### Rendered output (agent-builder)

```
## Examples

### Definition Design

#### Designing Instruction Steps From Requirements

Requirement: "The agent should assess each truth entry against quality dimensions and produce a QC report."
...

#### Minimum Required Permissions

The agent reads input from a tempfile and writes JSONL output to ./truth/quarantine/.
...
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Examples` | heading | H2 (section heading) |
| `### {example_group_name}` | heading | H3 (group heading) — conditional on `example_display_headings = true` |
| `#### {example_heading}` | heading | H4 (entry heading) — conditional on `example_display_headings = true` |

### Display Decisions

- `groups` array: `sequential` — each group separated by blank lines (implicitly, since entries flow beneath headings)
- `example_entries` array within group: `sequential` — each entry text block follows its H4 heading
- `example_text` field: rendered verbatim (multi-line, preserving internal formatting)
- When `example_display_headings = false`: headings suppressed, entries rendered as sequential text blocks

### Differences Between Agents

Both agents have `example_display_headings = true`. Structural difference: agent-builder has 1 group with 2 entries; interview-enrich-create-summary has 1 group with 5 entries.

### Non-Obvious Decisions

- Heading level hierarchy (H2 → H3 → H4) is a consequence of the section being at H2, groups at H3, entries at H4. If section moves to H1, groups shift to H2, entries to H3. The heading level is relative, not absolute.
- `example_display_headings` is a per-group boolean field in the data — not a display TOML knob. This means it is a data-driven conditional, not a style/display override. The style TOML would control the heading templates, but visibility is data-controlled.

### Knobs Required

- `heading` — `"Examples"`
- `heading_level` — currently H2
- `group_heading_level` — currently H3 (or relative: section + 1)
- `entry_heading_level` — currently H4 (or relative: section + 2)
- `groups_display` — `"sequential"`
- `entries_display` — `"sequential"`
- `group_heading_template` — `"### {example_group_name}"` (when headings enabled)
- `entry_heading_template` — `"#### {example_heading}"` (when headings enabled)

---

## OUTPUT

### Rendered output (agent-builder)

```
## Output

**Output directory:** `/Users/johnny/.ai/spaces/bragi/definitions`

TOML definition file with include references, plus separate include files for instructions, examples, guardrails, and criteria

Write the main definition to definitions/agents/{agent-name}.toml and include files to definitions/prompts/{agent-name}/.
```

### Rendered output (interview-enrich-create-summary)

```
## Output

**Schema:** `/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json`
**Output directory:** `/Users/johnny/.ai/spaces/bragi/interview/interviews`

One contextual summary record per input exchange with exchange number and one-sentence summary
```

Note: interview-enrich-create-summary has no `name_instruction` (file name is template-based, not free text), so that line is absent.

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Output` | heading | H2 |
| `**Schema:**` | label | Bold label for `schema_path`, only present when schema exists |
| `**Output directory:**` | label | Bold label for `output_directory` |
| `**Output file:**` | label | For known file name (not seen here) |

### Display Decisions

- `schema_path`: rendered as bold label + backtick-wrapped path, one line
- `output_directory`: rendered as bold label + backtick-wrapped path, one line
- `description`: rendered as unlabeled paragraph after the path lines
- `name_instruction`: rendered as unlabeled paragraph after description (when present)
- `name_template`: NOT rendered in body — interview-enrich-create-summary has a template but it is not shown here (it appears in dispatcher skill)
- `output_format` (`text`/`jsonl`): NOT rendered — pipeline control, by design

### Differences Between Agents

- agent-builder: has `output_directory` + `description` + `name_instruction`; no `schema_path`
- interview-enrich-create-summary: has `schema_path` + `output_directory` + `description`; no `name_instruction`

### Conditional Rendering

- `schema_path` → renders `**Schema:**` line only when present
- `output_directory` → renders `**Output directory:**` line only when present
- `name_instruction` → renders as trailing paragraph only when present
- `name_template` → not rendered in agent body (only in dispatcher)

### Non-Obvious Decisions

- The description field appears AFTER the path metadata lines, not before. This is a non-obvious ordering choice — description-first would be equally valid.
- `name_instruction` is free prose while `name_template` is a structured pattern. They both exist because some agents know their output file name structure, others give prose instructions. The free prose is rendered; the template is used by the dispatcher.

### Knobs Required

- `heading` — `"Output"`
- `heading_level` — currently H2
- `schema_label` — `"**Schema:**"` (conditional)
- `directory_label` — `"**Output directory:**"`
- `file_label` — `"**Output file:**"` (for known file name, not seen here)
- `path_format` — backtick wrapping (structural template)
- Field ordering within section (description before or after paths)

---

## WRITING OUTPUT

Only present when `has_output_tool = true`. Absent entirely for agent-builder.

### Rendered output (interview-enrich-create-summary)

```
## Writing Output (MANDATORY)

```
append_interview_summaries_record {name} <<'EOF'
{json_data}
EOF
```
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Writing Output (MANDATORY)` | heading | H2 with `(MANDATORY)` suffix — the suffix is a style knob |
| Opening ` ``` ` | structural | Code fence (no language tag) |
| Closing ` ``` ` | structural | Code fence |

### Invocation Display

The entire content inside the code fence is the `invocation_display` field value from `[writing_output]`. This is raw data — but it is a template: `{name}` and `{json_data}` are placeholders, not actual field references from the data model. The `invocation_display` field itself is the pre-formatted template string.

### Display Decisions

- Entire section is a code fence wrapping the `invocation_display` value
- No labels, no structured rendering — the field renders verbatim

### Conditional Presence

- Section appears only when `critical_rules.has_output_tool = true`
- The `writing_output` section of the data model feeds this

### Non-Obvious Decisions

- The heading suffix `(MANDATORY)` is not derived from data — it is static style text appended to the heading. It is a style knob.
- The code fence has no language tag — just triple backticks. An alternative would be `bash` or `shell` for syntax highlighting.
- `{name}` and `{json_data}` in the invocation_display are not Galdr template variables — they are placeholders for the executing agent, passed through verbatim.

### Knobs Required

- `heading` — `"Writing Output"`
- `heading_suffix` — `"(MANDATORY)"` (appended to heading when has_output_tool = true)
- `heading_level` — currently H2
- `code_fence_lang` — `""` (empty) or `"bash"`

---

## CONSTRAINTS

### Rendered output (agent-builder)

```
### Constraints

- Use ONLY field names from agent-template.toml — the TOML section provides the namespace, field names are short and unqualified.
- Validate ALL 18 conditional field rules before writing any output.
...
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `### Constraints` | heading | H3 — note the LEVEL difference vs other sections which are H2. This is a fossil. |

### Display Decisions

- `rules` array: `bulleted` — `- ` prefix per item

### Differences Between Agents

No structural difference. Both use bulleted list.

### Non-Obvious Decisions

- `Constraints` is H3 while most other sections are H2. This is identified as a fossil in the brief — heading_level is a knob.

### Knobs Required

- `heading` — `"Constraints"`
- `heading_level` — currently H3 (fossil, should be H2 or configurable)
- `rules_display` — `"bulleted"`

---

## ANTI-PATTERNS

### Rendered output (agent-builder)

```
### Anti-Patterns

- Do not write verbose instruction text when a dull fact would suffice — state what to do, name the outputs, specify criteria.
...
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `### Anti-Patterns` | heading | H3 (fossil) |

### Display Decisions

- `patterns` array: `bulleted` — `- ` prefix per item

### Knobs Required

- `heading` — `"Anti-Patterns"`
- `heading_level` — currently H3 (fossil)
- `patterns_display` — `"bulleted"`

---

## SUCCESS CRITERIA

### Rendered output (agent-builder)

```
### Success Criteria

A complete TOML definition and include files have been written that fully specify the agent described in the requirements.

Evidence:
- Every requirement maps to either a named field or a probabilistic instruction step.
- No instruction step contains operational content (tool invocation, batch rules, file paths).
...
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `### Success Criteria` | heading | H3 (fossil) |
| `Evidence:` | label | Appears before evidence bulleted list |

### Item Template

Each criterion renders as:
1. `success_definition` as unlabeled paragraph
2. `Evidence:` label
3. `success_evidence` array as bulleted list

When multiple criteria exist, they appear as sequential blocks.

### Display Decisions

- `criteria` array: `sequential` — each criterion block separated by blank line
- `success_evidence` array (per criterion): `bulleted`

### Differences Between Agents

No structural difference. Both have 1 criterion. Multiple criteria would produce sequential blocks.

### Non-Obvious Decisions

- `success_definition` has no label — it renders as a bare paragraph. The label `Evidence:` appears above the evidence list. This is an asymmetry — definition unlabeled, evidence labeled.
- `Evidence:` uses a plain colon (not bold) — differs from other labels in the document that use `**bold:**` formatting.

### Knobs Required

- `heading` — `"Success Criteria"`
- `heading_level` — currently H3 (fossil)
- `criteria_display` — `"sequential"`
- `evidence_label` — `"Evidence:"` (plain text, not bold — different from other labels)
- `evidence_display` — `"bulleted"`
- `definition_label` — `""` (empty — definition renders unlabeled)

---

## FAILURE CRITERIA

Structurally identical to Success Criteria.

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `### Failure Criteria` | heading | H3 (fossil) |
| `Evidence:` | label | Same as success criteria |

### Knobs Required

- `heading` — `"Failure Criteria"`
- `heading_level` — currently H3 (fossil)
- `criteria_display` — `"sequential"`
- `evidence_label` — `"Evidence:"`
- `evidence_display` — `"bulleted"`
- `definition_label` — `""` (empty)

---

## RETURN FORMAT

### Rendered output (both agents)

```
## Return Format

On success:
```
SUCCESS
```

On failure:
```
FAILURE: <reason>
```

Return SUCCESS with the agent name, number of instruction steps, and number of include files. Return ABORT with a structured fault list if the requirements are insufficient. Return FAILURE if source materials cannot be read.
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `## Return Format` | heading | H2 |
| `On success:` | label | Appears before success code fence |
| `On failure:` | label | Appears before failure code fence |
| ` ``` ` / ` ``` ` pairs (×2) | structural | Code fences wrapping status examples |
| `SUCCESS` | structural | Static success example text (not from data) |
| `FAILURE: <reason>` | structural | Static failure example text (not from data) |

### Display Decisions

- `mode` field (`"status"`): drives which example blocks appear
- When mode is `"status"`: success block + failure block both rendered with static example text
- `status_instruction` field: rendered as trailing paragraph after the code fence blocks
- `metrics_instruction` and `output_instruction` fields: not present in these agents; would render as additional paragraphs when mode includes those

### Differences Between Agents

Both have `mode = "status"`. The `status_instruction` text differs but the template structure is identical.

### Non-Obvious Decisions

- `SUCCESS` and `FAILURE: <reason>` inside the code fences are STATIC TEXT in the style, not derived from data. The data only has `mode = "status"` and the `status_instruction` prose. The renderer constructs the example blocks from the mode value.
- The instruction text (`status_instruction`) appears AFTER the code fences, not before them. Again a non-obvious ordering choice.

### Knobs Required

- `heading` — `"Return Format"`
- `heading_level` — currently H2
- `success_label` — `"On success:"`
- `failure_label` — `"On failure:"`
- `success_example` — `"SUCCESS"` (static example text when mode=status)
- `failure_example` — `"FAILURE: <reason>"` (static example text when mode=status)
- `code_fence_lang` — `""` (empty)
- `metrics_label` — for metrics mode (not yet seen)
- `output_label` — for output mode (not yet seen)

---

## CRITICAL RULES

This is the most style-heavy section. The two agents differ significantly here.

### Rendered output (agent-builder, no output tool, 3 rules)

```
## Critical Rules

1. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
2. **Stay in scope** — process only what you were given, nothing more
3. **No invention** — if the data doesn't support it, don't produce it
```

### Rendered output (interview-enrich-create-summary, has output tool, 6 rules)

```
## Critical Rules

1. **Use append_interview_summaries_record for all output** — never write files directly, never use a different write tool
2. **Batch discipline** — process exactly 20 records per batch (last batch may be smaller)
3. **Write after every batch** — do not accumulate records in memory across batches
4. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
5. **Stay in scope** — process only what you were given, nothing more
6. **No invention** — if the data doesn't support it, don't produce it
```

### Non-Data Text (in both)

The generic rules (items 1-3 in agent-builder, items 4-6 in interview-enrich-create-summary) are ENTIRELY STATIC STYLE TEXT — they contain no data field values:

| Rule text | Category | Source |
|-----------|----------|--------|
| `**Fail fast** — if something is wrong, FAILURE immediately with clear reason` | prose | Static style |
| `**Stay in scope** — process only what you were given, nothing more` | prose | Static style |
| `**No invention** — if the data doesn't support it, don't produce it` | prose | Static style |

### Non-Data Text (output-tool-specific rules, interview-enrich-create-summary only)

These rules contain data values embedded in templates:

| Rule text | Data fields used |
|-----------|-----------------|
| `**Use {tool_name} for all output** — never write files directly, never use a different write tool` | `critical_rules.tool_name` |
| `**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)` | `critical_rules.batch_size` |
| `**Write after every batch** — do not accumulate records in memory across batches` | (static, implies batch_size context) |

### Display Decisions

- All rules: `numbered` — `{i}. ` prefix
- Within each rule: bold short label (`**{label}**`) + em-dash + explanation text
- Output-tool rules appear FIRST (before generic rules) when has_output_tool = true

### Rule Entry Template

```
{i}. **{rule_label}** — {rule_explanation}
```

This is a compound template where the bold label and the explanation are two distinct parts of a structured rule, not a flat string. But currently `critical_rules` data only has `tool_name`, `batch_size`, and `has_output_tool` — the rule text is constructed from those values using style templates, not stored as free text in the data.

### Conditional Presence of Rules

When `has_output_tool = true`:
- Rule 1: tool-name rule (template: `"Use {tool_name} for all output — never write files directly, never use a different write tool"`)
- Rule 2: batch discipline rule (template: `"process exactly {batch_size} records per batch (last batch may be smaller)"`)
- Rule 3: write-after-batch rule (static)

When `has_output_tool = false`:
- Rules 1-3 above are absent

In both cases, the generic rules (`fail_fast`, `stay_in_scope`, `no_invention`) always appear.

### Non-Obvious Decisions

- The rule list mixes data-driven rules (first N) with fully static rules (last 3). The ordering — output tool rules before generic rules — is a style convention.
- The rule structure (bold short label + em-dash + explanation) is a compound template pattern, not a flat string render. The bold label and explanation text are stylistic components.
- The number of critical rules and their position in the list changes based on data conditionals. This is the most complex conditional rendering in the system.
- `name_needed` from `critical_rules` is not separately rendered — it drives the invocation variant in writing_output but has no standalone display.

### Knobs Required

- `heading` — `"Critical Rules"`
- `heading_level` — currently H2
- `rules_display` — `"numbered"`
- Rule templates (output-tool conditional group):
  - `output_tool_rule_template` — `"Use {tool_name} for all output — never write files directly, never use a different write tool"`
  - `batch_discipline_rule_template` — `"process exactly {batch_size} records per batch (last batch may be smaller)"`
  - `write_after_batch_rule` — `"Write after every batch — do not accumulate records in memory across batches"` (static)
- Generic rule static text:
  - `fail_fast_rule` — `"Fail fast — if something is wrong, FAILURE immediately with clear reason"`
  - `stay_in_scope_rule` — `"Stay in scope — process only what you were given, nothing more"`
  - `no_invention_rule` — `"No invention — if the data doesn't support it, don't produce it"`
- Rule entry structure:
  - `rule_label_bold` — whether the short label is bold (`true` = `**{label}**`)
  - `rule_separator` — `" — "` (em-dash with spaces, between label and explanation)
- Ordering knob: output-tool rules before or after generic rules

---

## SECTION SEPARATORS

Between sections, `---` (horizontal rule) appears consistently throughout both rendered outputs.

### Pattern

```
[section content]

---

## [Next Section Heading]
```

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `---` | separator | Horizontal rule between every major section |

### Differences Between Agents

Identical in both.

### Non-Obvious Decisions

- The `---` appears between ALL major sections but NOT between subsections (e.g., not between Constraints and Anti-Patterns within the guardrails block, not between Success Criteria and Failure Criteria). Actually — looking at the output: there IS a `---` between Constraints and Anti-Patterns, and between Success/Failure Criteria. Each named subsection has its own `---`.
- The section heading immediately follows the `---` with no blank line between them (the blank line appears before the `---`, not after it).

### Knobs Required

- `section_separator` — `"---"` vs `""` (none) vs other separators
- `separator_position` — before section heading, after section content

---

## DISPATCHER SKILL (separate output path)

### Structure

```
---
[YAML frontmatter]
---

# Dispatch: {agent_name_title_case}

**Agent:** `{agent_name}`
**Execution: FULL — single agent, all input at once**

---

## Paths

| Label | Path |
|-------|------|
| {context_label} | `{context_path}` |
...
| Output directory | `{output_directory}` |

---

## With Arguments

When the user provides specific targets:

1. Validate the targets exist
2. Prepare input ({input_format} format)
3. Dispatch directly — skip scope discovery

---

## No Arguments — Scope Discovery

**MANDATORY: Every step requires actual tool calls. Never use cached or remembered state.**

When the user provides no arguments:

1. **Assess state** — Read the filesystem to determine what work exists, what is already done, and what is stale
2. **Present options** — Use AskUserQuestion to present sensible choices to the user
3. **Prepare input** — Based on user selection, prepare the {input_format} input and write to a tempfile
4. Proceed to dispatch

---

## Dispatch

Launch ALL Agent tool calls in a **SINGLE message** for foreground parallel execution.

**Do NOT use `run_in_background`.** Foreground parallel returns all results in one response.

Each Agent call:
- `subagent_type`: `{agent_name}`
- `prompt`: Path to the input tempfile + `{extra_params}`
Tempfiles survive agent failure — failed batches can be redispatched without regenerating input.

---

## Post-Dispatch

1. Collect all agent results
2. Report aggregate summary (status format)
3. If any agents failed, offer to redispatch the failed batches

---

## Rules

1. **Task prompt is thin.** `subagent_type` + input path + parameters. The agent already knows its job.
2. **Foreground parallel.** All Agent calls in a single message. No background dispatch.
3. **Tempfiles survive failure.** Never clean up tempfiles automatically.
4. **State is never cached.** Every filesystem check is a real tool call.
5. **User-invoked only.** This skill runs only when explicitly requested.
```

### YAML Frontmatter Fields

| Field | Value source |
|-------|-------------|
| `name:` | `dispatch-{agent_name}` (template) |
| `description:` | `dispatcher.agent_description` |
| `argument-hint:` | joined `dispatcher.parameters[].param_name` values |
| `disable-model-invocation:` | `true` (static) |

### Non-Data Text

| Text | Category | Notes |
|------|----------|-------|
| `# Dispatch: {agent_name_display}` | heading | H1, title-cased agent name with "Dispatch: " prefix |
| `**Agent:** \`{agent_name}\`` | label + template | Bold label + backtick-wrapped agent name |
| `**Execution: FULL — single agent, all input at once**` | prose | Mode-dependent; "FULL" is derived from `dispatch_mode = "full"` |
| `## Paths` | heading | H2 |
| `| Label \| Path \|` | structural | Markdown table header |
| `\|-------\|------\|` | structural | Table separator |
| `\| {context_label} \| \`{context_path}\` \|` | template | Per context entry table row |
| `\| Output schema \| \`{schema_path}\` \|` | template | Conditional row (only interview-enrich has schema) |
| `\| Output directory \| \`{output_directory}\` \|` | template | When output_directory exists |
| `## With Arguments` | heading | H2 (static) |
| `When the user provides specific targets:` | prose | Static intro |
| `1. Validate the targets exist` | prose | Static numbered item |
| `2. Prepare input ({input_format} format)` | template | `input_format` interpolated |
| `3. Dispatch directly — skip scope discovery` | prose | Static |
| `## No Arguments — Scope Discovery` | heading | H2 (static) |
| `**MANDATORY: Every step requires actual tool calls. Never use cached or remembered state.**` | prose | Static (bold warning) |
| `When the user provides no arguments:` | prose | Static |
| `1. **Assess state** — ...` | prose | Static numbered item |
| `2. **Present options** — ...` | prose | Static numbered item |
| `3. **Prepare input** — Based on user selection, prepare the {input_format} input and write to a tempfile` | template | `input_format` interpolated |
| `4. Proceed to dispatch` | prose | Static |
| `## Dispatch` | heading | H2 (static) |
| `Launch ALL Agent tool calls in a **SINGLE message** for foreground parallel execution.` | prose | Static |
| `**Do NOT use \`run_in_background\`.**...` | prose | Static |
| `Each Agent call:` | prose | Static |
| `- \`subagent_type\`: \`{agent_name}\`` | template | agent_name interpolated |
| `- \`prompt\`: Path to the input tempfile + \`{extra_params}\`` | template | Conditional on extra parameters beyond tempfile |
| `Tempfiles survive agent failure...` | prose | Static |
| `## Post-Dispatch` | heading | H2 (static) |
| `1. Collect all agent results` | prose | Static |
| `2. Report aggregate summary (status format)` | prose | Static |
| `3. If any agents failed, offer to redispatch the failed batches` | prose | Static |
| `## Rules` | heading | H2 (static) |
| Rules 1-5 | prose | Static numbered rules |

### Differences Between Agents (Dispatcher)

- agent-builder: `argument-hint: "tempfile"` (one param)
- interview-enrich-create-summary: `argument-hint: "tempfile uid"` (two params, space-separated)
- agent-builder dispatcher: Paths table has 8 rows (7 context_required + 1 output_directory)
- interview-enrich-create-summary dispatcher: Paths table has 3 rows (output schema + output directory) — no context_required
- interview-enrich-create-summary dispatcher prompt line: `- \`prompt\`: Path to the input tempfile + \`uid\``
- agent-builder dispatcher prompt line: `- \`prompt\`: Path to the input tempfile` (no extra params)
- `Prepare input (jsonl format)` vs `Prepare input (text format)` — input_format interpolated

### Non-Obvious Decisions

- The dispatcher is almost entirely static prose with a few template interpolation points. The data axes (style/display) barely apply — it is more like a fixed template with slots.
- Context paths and output paths are combined into a single Paths table, even though they come from different parts of the data model (input.context vs output paths).
- `argument-hint` is derived by joining all dispatcher parameter names with spaces — not a rendered field, only frontmatter.
- `dispatch_mode = "full"` maps to the static text `"FULL — single agent, all input at once"`. Other modes would need different prose.
- The prompt line is conditional: if parameters beyond `tempfile` exist, they are listed after `+`. This is a template with a conditional suffix.

### Knobs Required (Dispatcher)

Since the dispatcher is heavily fixed-structure with few style variants, the knobs are primarily template slots:

- `skill_heading_prefix` — `"Dispatch: "` prefix before agent name
- `execution_mode_labels` — `dispatch_mode` value → display string mapping (e.g., `full` → `"FULL — single agent, all input at once"`)
- `paths_table_schema_label` — `"Output schema"` (static label for schema_path row)
- `paths_table_output_label` — `"Output directory"` (static label for output_directory row)
- `input_format_label` — used in "Prepare input ({input_format} format)" prose

---

## SUMMARY: ALL STYLE KNOBS BY SECTION

### Global

- `section_separator` — `"---"` between sections
- `heading_level_base` — base heading level for top-level sections (H2 in current output)

### frontmatter

- `tools_separator` — `", "` for inline tools array
- `hook_matcher_separator` — `"|"` for tool names in hook matcher

### identity

- `heading_level` — H1 for identity (anomalous)
- `purpose_label` — `"**Purpose:**"`
- `role_template` — `"You are a {role_identity}."`
- `responsibility_label` — `"**Your responsibility:**"`
- `expertise_label` — `"**Expertise:**"`
- `expertise_separator` — `", "`
- `expertise_display` — `"inline"`

### security_boundary

- `heading` — `"Security Boundary"`
- `heading_level` — H2
- `preamble` — `"This agent operates under \`{permission_mode}\` with hook-based restrictions."`
- `grants_intro` — `"The following operations are allowed — everything else is blocked by the system."`
- `entry_template` — `"**{tools}:** \`{path}\`"`
- `tools_separator` — `", "`
- `entries_display` — `"sequential"`
- `boundary_warning` — `"Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."`

### input

- `heading` — `"Input"`
- `heading_level` — H2
- `parameters_intro` — `"The dispatcher provides:"`
- `param_entry_template` — `"{param_name} ({param_type}): {param_description}"`
- `optional_suffix` — (not yet seen — for optional params)
- `parameters_display` — `"bulleted"`
- `context_required_label` — `"**Required context:**"`
- `context_required_display` — `"bulleted"`
- `context_entry_template` — `"**{context_label}:** \`{context_path}\`"`
- `context_available_label` — (parallel, not yet exercised)
- `context_available_display` — `"bulleted"`
- `schema_intro` — (for input_schema, not yet exercised)

### instructions

- `heading` — `"Processing"` (NOT "Instructions" — pure style)
- `heading_level` — H2
- `steps_display` — `"sequential"`
- `mode_label_deterministic` — `""` (bug state; must be non-empty in rebuild)
- `mode_label_probabilistic` — `""` (bug state)
- `mode_label_position` — `"prefix"` | `"inline"` | `"badge"`

### examples

- `heading` — `"Examples"`
- `heading_level` — H2
- `group_heading_level` — H3
- `entry_heading_level` — H4
- `groups_display` — `"sequential"`
- `entries_display` — `"sequential"`

### output

- `heading` — `"Output"`
- `heading_level` — H2
- `schema_label` — `"**Schema:**"`
- `directory_label` — `"**Output directory:**"`
- `file_label` — `"**Output file:**"`

### writing_output

- `heading` — `"Writing Output"`
- `heading_suffix` — `"(MANDATORY)"`
- `heading_level` — H2
- `code_fence_lang` — `""`

### constraints

- `heading` — `"Constraints"`
- `heading_level` — H3 (fossil — should be configurable)
- `rules_display` — `"bulleted"`

### anti_patterns

- `heading` — `"Anti-Patterns"`
- `heading_level` — H3 (fossil)
- `patterns_display` — `"bulleted"`

### success_criteria

- `heading` — `"Success Criteria"`
- `heading_level` — H3 (fossil)
- `criteria_display` — `"sequential"`
- `definition_label` — `""` (unlabeled)
- `evidence_label` — `"Evidence:"` (plain, not bold)
- `evidence_display` — `"bulleted"`

### failure_criteria

- `heading` — `"Failure Criteria"`
- `heading_level` — H3 (fossil)
- `criteria_display` — `"sequential"`
- `definition_label` — `""` (unlabeled)
- `evidence_label` — `"Evidence:"`
- `evidence_display` — `"bulleted"`

### return_format

- `heading` — `"Return Format"`
- `heading_level` — H2
- `success_label` — `"On success:"`
- `failure_label` — `"On failure:"`
- `success_example` — `"SUCCESS"`
- `failure_example` — `"FAILURE: <reason>"`
- `code_fence_lang` — `""`

### critical_rules

- `heading` — `"Critical Rules"`
- `heading_level` — H2
- `rules_display` — `"numbered"`
- `output_tool_rule_template` — `"Use {tool_name} for all output — never write files directly, never use a different write tool"`
- `batch_discipline_rule_template` — `"process exactly {batch_size} records per batch (last batch may be smaller)"`
- `write_after_batch_rule` — static text
- `fail_fast_rule` — static text
- `stay_in_scope_rule` — static text
- `no_invention_rule` — static text
- `rule_label_bold` — `true`
- `rule_separator` — `" — "`
- Output-tool rules ordering: before or after generic rules

---

## REQUIRED BUT MISSING: instruction_mode

`instruction_mode` (`deterministic` | `probabilistic`) is a field on every `[[instructions.steps]]` item. It is NOT rendered in the current output. This is an identified bug. In the rebuild it MUST appear.

Required new knobs:

- `mode_label_deterministic` — display string for deterministic steps (e.g., `"[DETERMINISTIC]"`, `"Deterministic:"`, `""`)
- `mode_label_probabilistic` — display string for probabilistic steps
- `mode_label_position` — where the label appears relative to step text: `"prefix_line"` (own line before), `"inline_prefix"` (same line, before text), `"inline_badge"` (bold badge)
- `mode_label_format` — formatting applied to the label (plain, bold, bracketed)

---

## CROSS-SECTION DATA REFERENCES (Architectural Note)

One case identified where a section's style template references data from a DIFFERENT section:

- `security_boundary.preamble` references `frontmatter.permission_mode`

The template `"This agent operates under \`{permission_mode}\` with hook-based restrictions."` needs data from `frontmatter`, not from `security_boundary`. The container for `security_boundary` must receive permission_mode as an additional data input, OR the preamble template must be evaluated with a merged data context that includes frontmatter fields.

This is an architectural consideration for the container design — the three-axis model (data/style/display) assumes each container receives only its own section's data. Cross-section references break that assumption.

---

## CONDITIONAL RENDERING MATRIX

| Section | Appears when | Hidden when |
|---------|-------------|-------------|
| `security_boundary` grants block | display entries exist | No entries |
| `input.context_required` block | context_required non-empty | Empty list |
| `output.schema_label` line | schema_path present | Not present |
| `output.directory_label` line | output_directory present | Not present |
| `output.name_instruction` paragraph | name_instruction present | Not present |
| `writing_output` section | has_output_tool = true | has_output_tool = false |
| critical_rules output-tool rules (3) | has_output_tool = true | has_output_tool = false |
| dispatcher.paths schema row | output.schema_path present | Not present |

---

## NON-OBVIOUS DECISIONS SUMMARY

1. `identity` renders at H1 while all other body sections render at H2 or H3 — heading_level is a knob that fixes this
2. Section heading for `instructions` is `"Processing"` not `"Instructions"` — pure style, no relation to section name
3. `Constraints`, `Anti-Patterns`, `Success Criteria`, `Failure Criteria` render at H3 while their siblings are H2 — all fossils, heading_level is a knob
4. `success_definition` and `failure_definition` are unlabeled while `success_evidence` gets the `Evidence:` label — asymmetric labeling
5. `Evidence:` uses plain text, not bold — unlike all other labels which use `**bold:**`
6. In `security_boundary` entries, tools act as the label and path is the value — inverted from typical key:value
7. The `critical_rules` section mixes static prose rules with data-driven template rules — the most complex conditional block
8. `return_format` code fence examples (`SUCCESS`, `FAILURE: <reason>`) are static style text, not derived from data
9. `writing_output` heading has a static suffix `(MANDATORY)` not found in any other section heading
10. `security_boundary.preamble` crosses section boundaries by referencing `frontmatter.permission_mode`
11. Dispatcher is almost entirely static prose — the data/style/display three-axis model barely applies; it is better modeled as a fixed template with a small number of interpolation slots
