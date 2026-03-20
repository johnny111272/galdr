# Output-Driven Knob Inventory v2

**Method:** Read actual rendered outputs, diff against input TOML, catalog every non-data element.
**Sources:** agent-builder (no output tool) vs interview-enrich-create-summary (has output tool)

---

## Section Inventory

Sections visible in the rendered agent outputs, in render order:

1. frontmatter (YAML block)
2. identity
3. security_boundary
4. input
5. processing (instructions)
6. examples
7. output
8. writing_output (conditional — only when has_output_tool=true)
9. guardrails (wraps constraints + anti_patterns together)
10. return_format
11. critical_rules

Sections present in data but not appearing as distinct rendered sections:
- `constraints` and `anti_patterns` render as **subsections inside a single `## Guardrails` section**
- `success_criteria` and `failure_criteria` render as **subsections inside `## Return Format`**, not as standalone sections
- `dispatcher` feeds the skill/dispatcher render path, not the agent prompt path

---

## Section-by-Section Analysis

### 1. FRONTMATTER

**Format:** YAML front matter block delimited by `---` markers.

**Structure:**
```
---
name: "{name}"
description: "{description}"
tools: "{tool1}, {tool2}, ..."
model: "{model}"
permissionMode: "{permission_mode}"
hooks:
  PreToolUse:
  - matcher: {tool_list}
    hooks:
    - type: command
      command: {hook_command}
---
```

**Style knobs (non-data text):**
- YAML key names: `name`, `description`, `tools`, `model`, `permissionMode`, `hooks`, `PreToolUse`, `matcher`, `type`, `command` — these are structural labels, not data
- The `---` delimiters (opening and closing)
- The YAML key `type: command` is a fixed structural string, not from the data model

**Display knobs:**
- `tools` array rendered as inline comma-separated string (not bulleted, not YAML list)
- hooks structure: the nesting of `PreToolUse` > array of matcher blocks is a fixed structural template

**Notes:**
- Tools list uses inline display with `, ` separator
- The YAML frontmatter block is the only section that does NOT use markdown headings
- hooks rendering is a sub-template: the command string is assembled from hook data, not just emitted

---

### 2. IDENTITY

**Rendered output (agent-builder):**
```
# Agent Builder

**Purpose:** Creates new agent TOML definitions and include files...

You are a definition author.

You create agent definitions from requirements...

**Your responsibility:** Read the preparation package...

**Expertise:** agent definition architecture, domain knowledge extraction, calibration example design, minimum permission security modeling
```

**Rendered output (interview-enrich-create-summary):**
```
# Interview Enrich Create Summary

**Purpose:** Reads stripped interview exchanges sequentially...

You are a contextual interview summarizer.

The meaning of an exchange depends on the conversation before it...

**Your responsibility:** Read stripped interview exchanges in order...

**Expertise:** contextual meaning extraction from sequential dialogue, source quality marker decontamination, significance calibration between content density and conversational weight
```

**Style knobs:**
- `# {title}` — H1 heading using `identity.title` field (NOT `identity.name`)
- `**Purpose:**` — bold label for the description field
- `You are a {role_identity}.` — template sentence; `role_identity` is data
- The blank line between identity sentence and role_description (structural separator)
- `**Your responsibility:**` — bold label for `role_responsibility`
- `**Expertise:**` — bold label for `role_expertise`

**Display knobs:**
- `role_description`: scalar text rendered as paragraph (sequential)
- `role_expertise`: array rendered as **inline** with `, ` separator
- blank line between role_identity sentence and role_description: structural

**Current heading level:** H1

---

### 3. SECURITY BOUNDARY

**Rendered output (agent-builder):**
```
## Security Boundary

This agent operates under `bypassPermissions` with hook-based restrictions.

The following operations are allowed — everything else is blocked by the system.

**Glob, Grep, Read, find:** `./definitions/agents/agent-template.toml`
**Glob, Grep, Read, find:** `./definitions/audit/`
...

Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.
```

**Rendered output (interview-enrich-create-summary):**
The security_boundary section is **absent** from interview-enrich-create-summary's rendered output. This agent has no `security_boundary.display` entries in its TOML.

**Style knobs:**
- `## Security Boundary` — H2 section heading
- `This agent operates under \`bypassPermissions\` with hook-based restrictions.` — fixed prose preamble (note: `bypassPermissions` is actually from frontmatter data; this sentence is a template: `"This agent operates under \`{permission_mode}\` with hook-based restrictions."`)
- `The following operations are allowed — everything else is blocked by the system.` — fixed grants intro prose
- `**{tools_joined}:** \`{path}\`` — per-entry template; tools array joined with `, ` separator, path as inline code
- `Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.` — fixed boundary warning prose (closing footer)

**Display knobs:**
- Each display entry rendered as `**{tool1}, {tool2}, ...:** \`{path}\`` — tools inline, path as code span
- Entries rendered sequentially (one per line, no extra blank lines between them)
- `workspace_path` is the anchor for resolving relative paths in display entries — it is NOT rendered as text

**Conditional rendering:** This section only renders if `security_boundary.display` is non-empty.

**Current heading level:** H2

---

### 4. INPUT

**Rendered output (agent-builder):**
```
## Input

Preparation package containing requirements, domain analysis, data shapes, and schema references

The dispatcher provides:
- tempfile (path): Path to the preparation package

**Required context:**
- **Agent Template Reference:** `/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-template.toml`
- **Definition System Architecture:** `/Users/johnny/.ai/spaces/bragi/...`
...
```

**Rendered output (interview-enrich-create-summary):**
```
## Input

Stripped interview exchanges with exchange number, agent question, and user response — no learned, threads, or insight fields

The dispatcher provides:
- tempfile (path): Path to the JSONL tempfile containing stripped interview exchanges
- uid (string): Interview identifier used for output filename construction
```
(No context section — no `context_required` entries in this agent's input)

**Style knobs:**
- `## Input` — H2 section heading
- `The dispatcher provides:` — fixed prose intro for parameters list
- `**Required context:**` — bold label for context_required block (only appears when context_required is non-empty)
- Per-parameter format: `- {param_name} ({param_type}): {param_description}` — template with embedded type annotation and separator text `: `
- Per-context format: `- **{context_label}:** \`{context_path}\`` — template with bold label and inline code path

**Display knobs:**
- `input.description`: scalar text rendered as paragraph (no label)
- `parameters`: bulleted list with inline type annotation template
- `context_required`: bulleted list with bold-label inline-code-path template
- `context_available`: (not seen in these two agents — would use same bulleted pattern)

**Conditional rendering:**
- `**Required context:**` block only appears if `context_required` is non-empty
- Parameters section (with intro prose) only appears if parameters exist

**Current heading level:** H2

---

### 5. PROCESSING (Instructions)

**Rendered output (agent-builder):**
```
## Processing

Read the preparation package from the tempfile path. Read all context_required documents...

Identify the agent's core domain from the requirements...

Design the instruction steps...

...

Map all structured fields from the requirements...
```

**Rendered output (interview-enrich-create-summary):**
```
## Processing

Read the input tempfile. Each line is a JSON object...

For each exchange, write one sentence...

...
```

**Style knobs:**
- `## Processing` — H2 section heading
- No step labels, numbers, or mode labels appear in the current rendered output (instruction_mode is NOT currently rendered — this is the confirmed bug)
- Steps separated by blank lines (sequential display)

**Display knobs:**
- `instructions.steps`: sequential (blank-line-separated paragraphs, no numbering, no bullets)
- `instruction_mode` per step: currently dropped entirely — **rebuild required knob: mode display**

**REQUIRED KNOB — instruction_mode rendering:**
The rebuild must render instruction_mode. Preferred format: group steps by mode, or prefix each step with a mode label. Options include:
- Inline prefix: `[deterministic]` or `[probabilistic]` before step text
- Grouped: all deterministic steps under a subheading, then probabilistic
- Annotated: bold mode label as first line of each step block
This is a design decision for the rebuild — catalog the knob, specify the options.

**Current heading level:** H2

---

### 6. EXAMPLES

**Rendered output (agent-builder):**
```
## Examples

### Definition Design

#### Designing Instruction Steps From Requirements

Requirement: "The agent should assess..."
...

#### Minimum Required Permissions

The agent reads input from a tempfile...
```

**Rendered output (interview-enrich-create-summary):**
```
## Examples

### Contextual Summaries

#### Standard substantive exchange

Exchange 5 user text: "So I started..."
...

#### Thin content with rich context
...
```

**Style knobs:**
- `## Examples` — H2 section heading
- `### {example_group_name}` — H3 group heading (data: `example_group_name`)
- `#### {example_heading}` — H4 entry heading (data: `example_heading`)

**Display knobs:**
- Groups: sequential (each group separated by... nothing visible, just sequential layout)
- Entries within group: sequential (each entry separated by blank line + H4 heading)
- Example text (`example_text`): rendered as-is (raw text block, no wrapping, preserves internal newlines)
- `example_display_headings = true` controls whether H4 headings appear per entry

**Heading level hierarchy:** H2 > H3 (group) > H4 (entry)
- All these are knobs: section heading level drives the group/entry levels relative to it

**Conditional rendering:**
- When `example_display_headings = false`, individual entry headings are suppressed (group heading still renders)

---

### 7. OUTPUT

**Rendered output (agent-builder):**
```
## Output

**Output directory:** `/Users/johnny/.ai/spaces/bragi/definitions`

TOML definition file with include references, plus separate include files for instructions, examples, guardrails, and criteria

Write the main definition to definitions/agents/{agent-name}.toml and include files to definitions/prompts/{agent-name}/.
```

**Rendered output (interview-enrich-create-summary):**
```
## Output

**Schema:** `/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json`
**Output directory:** `/Users/johnny/.ai/spaces/bragi/interview/interviews`

One contextual summary record per input exchange with exchange number and one-sentence summary
```

**Style knobs:**
- `## Output` — H2 section heading
- `**Schema:**` — bold label for `output.schema_path` (only appears when schema_path present)
- `**Output directory:**` — bold label for `output.output_directory`
- No label for `output.description` — rendered as plain paragraph

**Display knobs:**
- `output.schema_path`: inline code span (when present)
- `output.output_directory`: inline code span
- `output.description`: scalar paragraph, no label
- `output.name_instruction` (agent-builder): rendered as plain paragraph below description (no label)
- Labels+values rendered on consecutive lines (not a table)

**Conditional rendering:**
- `**Schema:**` line only appears when `schema_path` is present (interview-enrich-create-summary has it; agent-builder does not)
- `output.name_instruction` only appears when present (agent-builder has it; interview-enrich-create-summary uses `name_template` instead, which does not appear here — name_template feeds writing_output section)

---

### 8. WRITING OUTPUT (conditional section)

**Only appears in interview-enrich-create-summary (has_output_tool=true).**
**Absent from agent-builder (has_output_tool=false).**

**Rendered output (interview-enrich-create-summary):**
```
## Writing Output (MANDATORY)

```
append_interview_summaries_record {name} <<'EOF'
{json_data}
EOF
```
```

**Style knobs:**
- `## Writing Output (MANDATORY)` — H2 section heading; the `(MANDATORY)` qualifier is a style choice
- The code fence (triple backtick) wrapping the invocation template
- No surrounding prose — the invocation display is rendered directly inside a code fence

**Display knobs:**
- `writing_output.invocation_display`: rendered verbatim inside a triple-backtick code fence
- Code fence has no language specifier (unlabeled fence)

**Conditional rendering:** This entire section only appears when `critical_rules.has_output_tool = true`

---

### 9. GUARDRAILS (wraps constraints + anti_patterns)

**Rendered output (agent-builder):**
```
### Constraints

- Use ONLY field names from agent-template.toml...
- Validate ALL 18 conditional field rules...
...

---

### Anti-Patterns

- Do not write verbose instruction text...
...

---
```

**Rendered output (interview-enrich-create-summary):**
```
## Guardrails

### Constraints

- MUST process exchanges in order...
...

### Anti-Patterns

- Do not classify importance...
...

---
```

**IMPORTANT STRUCTURAL DIFFERENCE:**
- In **agent-builder**, there is NO `## Guardrails` parent heading. Constraints and Anti-Patterns appear as H3 headings hanging directly after the `---` separator that follows the Output section. This appears to be a rendering artifact.
- In **interview-enrich-create-summary**, there IS a `## Guardrails` parent heading, with `### Constraints` and `### Anti-Patterns` as children.

The difference arises because in agent-builder the guardrails appear AFTER the output section's `---` separator, while in interview-enrich-create-summary the Writing Output section introduces a new `## Guardrails` heading. This is inconsistent in the current implementation and should be unified in the rebuild.

**Style knobs:**
- `## Guardrails` — H2 parent heading (present in interview-enrich-create-summary, absent/inconsistent in agent-builder)
- `### Constraints` — H3 subsection heading
- `### Anti-Patterns` — H3 subsection heading
- `---` horizontal rule separator after each subsection

**Display knobs:**
- `constraints.rules`: bulleted list (`- {rule}`)
- `anti_patterns.patterns`: bulleted list (`- {pattern}`)

**NOTE on heading levels:** H3 for both constraints and anti_patterns subsections is a fossil of a parent `## Guardrails` section that existed previously. In the current output the parent heading is inconsistently present. In the rebuild, heading levels should be configurable per section (the `heading_level` knob applies here).

**Current heading levels:** H3 (subsections), H2 (parent — inconsistent)

---

### 10. RETURN FORMAT

**Rendered output (agent-builder):**
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

Return SUCCESS with the agent name, number of instruction steps, and number of include files...

---

### Success Criteria

A complete TOML definition and include files have been written...

Evidence:
- Every requirement maps to either a named field...
...

---

### Failure Criteria

The requirements are insufficient to produce a complete definition...

Evidence:
- Requirements do not specify what the agent judges...
...

---
```

**Rendered output (interview-enrich-create-summary):**
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

Return SUCCESS when all exchange summaries are written...

### Success Criteria

Every input exchange has been contextually summarized...

Evidence:
- Output record count equals input record count.
...

### Failure Criteria

The summarization process broke...

Evidence:
- Any exchange skipped without a summary being written.
...

---
```

**Style knobs:**
- `## Return Format` — H2 section heading
- `On success:` — fixed prose label before success code fence
- `On failure:` — fixed prose label before failure code fence
- ` ``` ` fences wrapping SUCCESS and FAILURE: templates
- `SUCCESS` — fixed literal string inside success code fence
- `FAILURE: <reason>` — fixed literal string template inside failure code fence; `<reason>` is a placeholder, not data
- No label for `status_instruction` text — rendered as plain paragraph below the code fences
- `### Success Criteria` — H3 subsection heading
- `### Failure Criteria` — H3 subsection heading
- `Evidence:` — fixed prose label before evidence list (no bold in agent-builder; bold styling would be a style knob)

**Display knobs:**
- `success_criteria[].success_definition`: scalar paragraph (no label, becomes the opening line of the subsection)
- `success_criteria[].success_evidence`: bulleted list under `Evidence:` label
- `failure_criteria[].failure_definition`: scalar paragraph
- `failure_criteria[].failure_evidence`: bulleted list under `Evidence:` label
- `return_format.status_instruction`: scalar paragraph (no label)
- Code fences for SUCCESS/FAILURE literals: structural display choice

**Separator behavior:**
- agent-builder: `---` between success and failure criteria blocks
- interview-enrich-create-summary: no `---` between them (only final `---` after failure)
This inconsistency is a rendering artifact; the rebuild should make separator placement a configurable knob.

**Current heading levels:** H2 (section), H3 (subsections)

---

### 11. CRITICAL RULES

**Rendered output (agent-builder) — has_output_tool=false:**
```
## Critical Rules

1. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
2. **Stay in scope** — process only what you were given, nothing more
3. **No invention** — if the data doesn't support it, don't produce it
```
(3 rules — generic only)

**Rendered output (interview-enrich-create-summary) — has_output_tool=true, tool_name="append_interview_summaries_record", batch_size=20:**
```
## Critical Rules

1. **Use append_interview_summaries_record for all output** — never write files directly, never use a different write tool
2. **Batch discipline** — process exactly 20 records per batch (last batch may be smaller)
3. **Write after every batch** — do not accumulate records in memory across batches
4. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
5. **Stay in scope** — process only what you were given, nothing more
6. **No invention** — if the data doesn't support it, don't produce it
```
(6 rules — 3 tool-specific prepended + 3 generic appended)

**THIS IS THE MOST STYLE-HEAVY SECTION.** The rules are entirely composed from style templates interpolated with data values.

**Style knobs — generic rules (always present, 3 rules):**
- `**Fail fast** — if something is wrong, FAILURE immediately with clear reason`
- `**Stay in scope** — process only what you were given, nothing more`
- `**No invention** — if the data doesn't support it, don't produce it`

These are FIXED STYLE TEXT. They do not come from any field in the TOML. They are always appended.

**Style knobs — tool-specific rules (conditional on has_output_tool=true):**
Rule 1 template: `**Use {tool_name} for all output** — never write files directly, never use a different write tool`
- `{tool_name}` interpolated from `critical_rules.tool_name`

Rule 2 template: `**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)`
- `{batch_size}` interpolated from `critical_rules.batch_size`

Rule 3 template: `**Write after every batch** — do not accumulate records in memory across batches`
- This is FIXED STYLE TEXT (no interpolation despite appearing with the tool rules)

**Style knobs — structural:**
- `## Critical Rules` — H2 section heading
- Rule format: `{i}. **{short_label}** — {description_text}` — numbered list with bold label + em-dash + prose
- Tool-specific rules are PREPENDED (numbered 1-3), generic rules are APPENDED (numbered 4-6 when tool rules present, or 1-3 when absent)

**Display knobs:**
- Rules: numbered list (`{i}. ...`)
- Bold rule labels with em-dash separator: `**label** — text`

**Conditional rendering matrix:**
```
has_output_tool=false:
  → 3 generic rules (numbered 1-3)

has_output_tool=true:
  → 3 tool-specific rules using tool_name + batch_size (numbered 1-3)
  → 3 generic rules (numbered 4-6)
```

**Data fields consumed:**
- `critical_rules.has_output_tool` — controls conditional branch
- `critical_rules.tool_name` — interpolated into rule 1 template
- `critical_rules.batch_size` — interpolated into rule 2 template
- `critical_rules.name_needed` — (present in TOML, not visible in rendered output; may control rule 3 or future knobs)
- `critical_rules.workspace_path` — anchors security_boundary, NOT rendered here

**Current heading level:** H2

---

## Dispatcher / Skill Output Analysis

### SKILL.md structure (both agents)

**Rendered output (dispatch-agent-builder):**
```yaml
---
name: dispatch-agent-builder
description: {agent_description}
argument-hint: "{param_names}"
disable-model-invocation: true
---

# Dispatch: {agent_name_display}

**Agent:** `{agent_name}`
**Execution: FULL — single agent, all input at once**

---

## Paths
| Label | Path |
|-------|------|
| {label} | `{path}` |
...

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
1. **Assess state** — Read the filesystem...
2. **Present options** — Use AskUserQuestion...
3. **Prepare input** — Based on user selection, prepare the {input_format} input and write to a tempfile
4. Proceed to dispatch

---

## Dispatch
Launch ALL Agent tool calls in a **SINGLE message** for foreground parallel execution.
**Do NOT use `run_in_background`.** Foreground parallel returns all results in one response.
Each Agent call:
- `subagent_type`: `{agent_name}`
- `prompt`: Path to the input tempfile{param_additions}
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

**Differences between the two dispatcher outputs:**

1. `argument-hint`: agent-builder has `"tempfile"`, interview-enrich-create-summary has `"tempfile uid"` — derived from parameter names
2. `**Execution:**` line: agent-builder uses `FULL — single agent, all input at once` (no colon after bold), interview-enrich-create-summary uses `FULL — single agent, all input at once` (with colon after bold label). Minor inconsistency.
3. `## Paths` table: agent-builder includes 8 entries (7 context paths + output directory), interview-enrich-create-summary includes 2 entries (schema + output directory). Paths table is fully data-driven.
4. `Prepare input ({input_format} format)`: agent-builder shows `text format`, interview-enrich-create-summary shows `jsonl format` — `{input_format}` interpolated from dispatcher data
5. `prompt` line in Dispatch section: agent-builder has `Path to the input tempfile`, interview-enrich-create-summary has `Path to the input tempfile + \`uid\`` — extra parameters listed after tempfile

**Dispatcher style knobs (heavily templated):**
- YAML frontmatter structure: `name`, `description`, `argument-hint`, `disable-model-invocation` — all key names are fixed style
- `# Dispatch: {agent_name_display}` — H1 heading template
- `**Agent:** \`{agent_name}\`` — bold label + inline code template
- `**Execution:** {execution_mode_text}` — bold label; execution_mode_text is derived from dispatch_mode field
- `## Paths` — H2 heading
- Paths table header: `| Label | Path |` / `|-------|------|` — fixed structural
- `## With Arguments` — H2 heading (fixed)
- "When the user provides specific targets:" — fixed prose
- Steps 1-3 under With Arguments — largely fixed with `{input_format}` interpolation
- `## No Arguments — Scope Discovery` — H2 heading (fixed)
- `**MANDATORY: Every step requires actual tool calls. Never use cached or remembered state.**` — fixed bold prose
- Steps 1-4 under No Arguments — largely fixed with `{input_format}` interpolation
- `## Dispatch` — H2 heading (fixed)
- "Launch ALL Agent tool calls..." — fixed prose
- `**Do NOT use \`run_in_background\`.**` — fixed bold prose
- "Each Agent call:" — fixed label
- "`subagent_type`: `{agent_name}`" — template
- "`prompt`: Path to the input tempfile{...}" — template with conditional parameter additions
- "Tempfiles survive agent failure..." — fixed prose
- `## Post-Dispatch` — H2 heading (fixed)
- Steps 1-3 — fixed prose
- `## Rules` — H2 heading (fixed)
- All 5 rules — fixed style text (no data interpolation)

**Dispatcher is almost entirely fixed-structure.** The data-driven parts are:
- `name` (agent_name with dispatch- prefix)
- `description`
- `argument-hint` (derived from parameter names)
- Paths table content
- `{input_format}` interpolations
- `{agent_name}` in subagent_type
- Extra parameter additions in prompt line

---

## Complete Knob Catalog

### Style Knobs

| Section | Knob Name | Current Value |
|---------|-----------|---------------|
| global | separator | `---` (horizontal rule between major sections) |
| frontmatter | yaml_key_name_tools | `tools` |
| frontmatter | yaml_key_name_model | `model` |
| frontmatter | yaml_key_name_permission | `permissionMode` |
| identity | section_heading | `# Agent Builder` (H1, uses title field) |
| identity | purpose_label | `**Purpose:**` |
| identity | role_template | `You are a {role_identity}.` |
| identity | responsibility_label | `**Your responsibility:**` |
| identity | expertise_label | `**Expertise:**` |
| security_boundary | section_heading | `## Security Boundary` (H2) |
| security_boundary | preamble | `This agent operates under \`{permission_mode}\` with hook-based restrictions.` |
| security_boundary | grants_intro | `The following operations are allowed — everything else is blocked by the system.` |
| security_boundary | entry_template | `**{tools_inline}:** \`{path}\`` |
| security_boundary | boundary_warning | `Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.` |
| input | section_heading | `## Input` (H2) |
| input | parameters_intro | `The dispatcher provides:` |
| input | parameter_template | `- {param_name} ({param_type}): {param_description}` |
| input | context_required_label | `**Required context:**` |
| input | context_entry_template | `- **{context_label}:** \`{context_path}\`` |
| instructions | section_heading | `## Processing` (H2) |
| instructions | mode_display | (currently omitted — required rebuild knob) |
| examples | section_heading | `## Examples` (H2) |
| examples | group_heading_level | H3 (relative to section H2) |
| examples | entry_heading_level | H4 (relative to group H3) |
| output | section_heading | `## Output` (H2) |
| output | schema_label | `**Schema:**` |
| output | directory_label | `**Output directory:**` |
| writing_output | section_heading | `## Writing Output (MANDATORY)` (H2) |
| writing_output | code_fence_language | (none — unlabeled fence) |
| guardrails | parent_heading | `## Guardrails` (H2, currently inconsistent) |
| guardrails | constraints_heading | `### Constraints` (H3) |
| guardrails | anti_patterns_heading | `### Anti-Patterns` (H3) |
| return_format | section_heading | `## Return Format` (H2) |
| return_format | success_label | `On success:` |
| return_format | failure_label | `On failure:` |
| return_format | success_literal | `SUCCESS` |
| return_format | failure_literal | `FAILURE: <reason>` |
| return_format | success_criteria_heading | `### Success Criteria` (H3) |
| return_format | failure_criteria_heading | `### Failure Criteria` (H3) |
| return_format | evidence_label | `Evidence:` |
| critical_rules | section_heading | `## Critical Rules` (H2) |
| critical_rules | rule_format | `{i}. **{label}** — {text}` |
| critical_rules | tool_rule_1_template | `**Use {tool_name} for all output** — never write files directly, never use a different write tool` |
| critical_rules | tool_rule_2_template | `**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)` |
| critical_rules | tool_rule_3_fixed | `**Write after every batch** — do not accumulate records in memory across batches` |
| critical_rules | generic_rule_1 | `**Fail fast** — if something is wrong, FAILURE immediately with clear reason` |
| critical_rules | generic_rule_2 | `**Stay in scope** — process only what you were given, nothing more` |
| critical_rules | generic_rule_3 | `**No invention** — if the data doesn't support it, don't produce it` |

### Display Knobs

| Section | Field | Current Display Mode | Separator |
|---------|-------|---------------------|-----------|
| frontmatter | tools | inline | `, ` |
| identity | role_expertise | inline | `, ` |
| identity | role_description | scalar paragraph | — |
| input | parameters | bulleted | — |
| input | context_required | bulleted | — |
| instructions | steps | sequential (blank-line-separated) | blank line |
| examples | groups | sequential | — |
| examples | entries_per_group | sequential | — |
| examples | example_text | verbatim block | — |
| output | schema_path | inline code span | — |
| output | output_directory | inline code span | — |
| writing_output | invocation_display | verbatim inside code fence | — |
| constraints | rules | bulleted | — |
| anti_patterns | patterns | bulleted | — |
| success_criteria | criteria | sequential | — |
| success_criteria | evidence | bulleted | — |
| failure_criteria | criteria | sequential | — |
| failure_criteria | evidence | bulleted | — |
| return_format | code_fences | triple-backtick | — |
| critical_rules | rules | numbered | — |
| security_boundary | entries | sequential (one per line) | — |
| security_boundary | tools_per_entry | inline | `, ` |

### Structural / Separator Knobs

| Element | Current Behavior |
|---------|-----------------|
| Section separator | `---` (HR) appears after most sections |
| Within-guardrails separator | `---` after constraints, after anti_patterns |
| Within-return_format separator | `---` after success_criteria in agent-builder; inconsistent in interview-enrich-create-summary |
| Code fence language tag | Empty (no language specifier) on return_format and writing_output fences |
| Blank line after `---` | Present throughout |

### Conditional Rendering Knobs

| Section | Condition | Gate Field |
|---------|-----------|------------|
| security_boundary | only if display entries exist | `security_boundary.display` non-empty |
| input context block | only if context_required exists | `input.context.context_required` non-empty |
| output schema line | only if schema_path present | `output.schema_path` present |
| output name_instruction | only if name_instruction present | `output.name_instruction` present |
| writing_output section | only when has_output_tool=true | `critical_rules.has_output_tool` |
| critical_rules tool rules | only when has_output_tool=true | `critical_rules.has_output_tool` |
| critical_rules batch rule | only when has_output_tool=true | `critical_rules.has_output_tool` (batch_size interpolated) |

### Heading Level Summary

| Section | Current Level | Note |
|---------|--------------|-------|
| identity | H1 | Uses `title` field |
| security_boundary | H2 | |
| input | H2 | |
| processing (instructions) | H2 | Section heading is "Processing" not "Instructions" |
| examples | H2 | |
| examples > group | H3 | |
| examples > entry | H4 | |
| output | H2 | |
| writing_output | H2 | |
| guardrails (parent) | H2 | Currently inconsistent — present in one, absent in other |
| constraints | H3 | Fossil of parent category — heading_level should be a knob |
| anti_patterns | H3 | Same |
| return_format | H2 | |
| success_criteria | H3 | Child of return_format |
| failure_criteria | H3 | Child of return_format |
| critical_rules | H2 | |

All heading levels should be configurable. The H3 for constraints/anti_patterns/success_criteria/failure_criteria are fossils from a parent-category structure that no longer exists. The rebuild treats `heading_level` as a per-section style knob.

---

## Fields Serving Non-Rendering Purposes

These fields appear in anthropic_render.toml but are NOT rendered directly. Each serves a specific pipeline or conditional purpose:

| Field | Purpose |
|-------|---------|
| `output.format` | Pipeline control — consumed before rendering to route dispatcher path |
| `input.format` | Feeds dispatcher input preparation, not agent prompt |
| `input.delivery` | Feeds dispatcher tempfile handling, not agent prompt |
| `output.name_known` | Conditional gate controlling which output name fields appear |
| `critical_rules.has_output_tool` | Conditional gate for writing_output section and tool-specific critical rules |
| `critical_rules.name_needed` | Controls name parameter handling in invocation (not yet visible in rendered output) |
| `critical_rules.workspace_path` | Anchors relative path resolution in security_boundary display |
| `dispatcher.*` | Feeds skill/dispatcher render path entirely (not agent prompt) |
| `frontmatter.hooks.*` | Rendered in YAML frontmatter as structured hook configuration |
| `writing_output.invocation_variant` | Controls which invocation template variant is selected |
| `writing_output.name_pattern` | Used to construct invocation display, not rendered standalone |
| `writing_output.schema_path` | Used in invocation, also appears in output section as schema label |

---

## Known Rendering Bugs (to fix in rebuild)

1. **instruction_mode dropped entirely** — Steps render without any mode annotation. The rebuild must render instruction_mode. Knob: mode display format (inline prefix, grouped, annotated).

2. **Guardrails parent heading inconsistency** — agent-builder has no `## Guardrails` heading; constraints and anti_patterns appear as orphaned H3s. interview-enrich-create-summary has the parent. The rebuild must consistently render the parent heading.

3. **Success/failure criteria placement inconsistency** — agent-builder puts success/failure criteria inside return_format section (after code fences). interview-enrich-create-summary does the same. This is consistent. But separator behavior between success and failure blocks differs. Make separator placement a knob.

4. **Execution heading colon inconsistency** — dispatcher: agent-builder has `**Execution: FULL...`** (colon inside bold), interview-enrich-create-summary has `**Execution:** FULL...` (colon outside bold, then plain text). Normalize in rebuild.
