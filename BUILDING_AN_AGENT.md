# Building an Agent with Galdr

Galdr is the final stage of the bragi agent pipeline. It takes an `anthropic_render.toml` file and renders it into a deployable `.claude/agents/{name}.md` file.

## Prerequisites

An `anthropic_render.toml` file. This file is produced by the upstream pipeline stages (draupnir + regin) and lives at:

```
definitions/agents/{agent-name}/anthropic_render.toml
```

The file is TOML, validated against `schemas/agent-anthropic-render.schema.json` by a compiled Rust/PyO3 gate. Python never reads the TOML directly and never does schema validation.

## Running Galdr

```bash
# Render to definitions/staging/{agent-name}.md (default)
cd tools/galdr
uv run python -m galdr.cli path/to/anthropic_render.toml

# Render to a specific output path
uv run python -m galdr.cli path/to/anthropic_render.toml -o path/to/output.md

# Preview to stdout without writing
uv run python -m galdr.cli path/to/anthropic_render.toml --check
```

Workspace root is auto-detected by walking parent directories until finding `schemas/` + `definitions/` as siblings. Override with `--workspace`.

---

## Sections

Every rendered agent prompt is assembled from independent sections. Each section has its own Jinja2 template and its own data packet extracted from the `anthropic_render.toml` input. Sections never reach across each other's data.

### Frontmatter

YAML metadata block consumed by Claude Code's agent system, not by the LLM.

| Field | Source |
|-------|--------|
| `name` | Agent display name |
| `description` | One-line purpose |
| `tools` | Comma-separated tool list (Read, Write, Bash, etc.) |
| `model` | Resolved model name (haiku, sonnet, opus) |
| `permissionMode` | Always `bypassPermissions` |
| `hooks` | PreToolUse hook commands per tool matcher |

Hooks are the security enforcement mechanism. Each hook maps a tool (Read, Write, Bash, etc.) to a validation command that checks whether the agent's file access stays within its declared boundaries.

**Always present.** Not reorderable (must be first).

### Identity

The opening section. Establishes who the agent is and what it does.

| Field | Purpose |
|-------|---------|
| `title` | H1 heading |
| `description` | One-line purpose statement ("Purpose: ...") |
| `role_identity` | What the agent is ("semantic quality assessor") |
| `role_description` | Expanded context (nullable) |
| `role_expertise` | Skill areas as comma-separated list (nullable) |
| `role_responsibility` | Core mandate sentence |

**Always present.** Not reorderable (must follow frontmatter).

### Security Boundary

Tells the agent what file operations are permitted. Agents run under `bypassPermissions` with hook enforcement. This section documents the allowed operations so the agent does not waste turns attempting blocked actions.

| Field | Purpose |
|-------|---------|
| `has_grants` | Whether any explicit grants exist |
| `display` | Array of `{path, tools}` entries showing what is allowed where |

Each display entry is a workspace-relative path paired with the tools/commands permitted there. Example: `Read: ./schemas` means the Read tool is allowed on files under `schemas/`.

**Present when `has_grants` is true.** Reorderable.

### Input

Describes what the agent receives and how.

| Field | Purpose |
|-------|---------|
| `description` | What the input contains ("JSONL tempfile of embedding targets") |
| `format` | Data format (text, json, jsonl) |
| `delivery` | How the input arrives (tempfile, inline, file, directory) |
| `input_schema` | Path to schema the input validates against (nullable) |
| `parameters` | Dispatcher-provided parameters with name, type, required (nullable) |
| `context_required` | Reference resources the agent must read (nullable) |
| `context_available` | Reference resources available but not mandatory (nullable) |

**Always present.** Reorderable.

### Instructions (rendered as "Processing")

The core work definition. Contains ordered steps that tell the agent what to do.

| Field | Purpose |
|-------|---------|
| `steps` | Array of `{mode, text}` entries |

Each step has a `mode` (deterministic or probabilistic) and `text` (the actual instruction content). The text often contains its own markdown headings. The template renders each step's text in order without adding structure — instruction structure is author-controlled.

`mode` is carried in the data for future template sophistication (framing deterministic steps more imperatively) but is not used in v1 rendering.

**Always present.** Reorderable.

### Examples

Concrete demonstrations of expected behavior. Organized into named groups.

| Field | Purpose |
|-------|---------|
| `groups` | Array of example groups |

Each group has:
- `group_name` — heading text ("Good Rewrites", "Bad Rewrites")
- `display_headings` — whether individual entry headings are shown
- `max_entries` — cap on entries rendered from this group (nullable)
- `entries` — array of `{heading, text}` examples

**Optional.** Reorderable.

### Output

Describes what the agent produces.

| Field | Purpose |
|-------|---------|
| `description` | What the output contains |
| `format` | Output format (text, json, jsonl, markdown) |
| `name_known` | Whether the output filename is known (known, partially, unknown) |
| `name_instruction` | How to determine the filename when not fully known (nullable) |
| `schema_path` | Path to output schema (nullable) |
| `file_path` | Exact output file when known (nullable) |
| `directory_path` | Output directory when file not fully known (nullable) |

**Always present.** Reorderable.

### Writing Output

The mandatory write tool section. Present only when the agent uses a custom validated write tool (not Claude Code's built-in Write). Contains a pre-composed `invocation_display` — the complete bash heredoc command the agent copies to write output.

| Field | Purpose |
|-------|---------|
| `invocation_display` | Ready-to-use bash command block |

This block is composed upstream by the anthropic resolver (regin level 8) from enforcement fields. The template renders it as-is.

**Optional** (present only when custom output tool exists). Reorderable.

### Guardrails

Behavioral constraints and known mistakes to avoid. Two sources are merged into a single bullet list:

| Source | Purpose |
|--------|---------|
| `constraints` | MUST/NEVER rules ("MUST validate every record") |
| `anti_patterns` | Known failure modes ("Do not batch-summarize from memory") |

Both are arrays of plain strings rendered as bullet items.

**Optional** (present when either constraints or anti_patterns exist). Reorderable.

### Return Format

Defines how the agent signals completion.

| Field | Purpose |
|-------|---------|
| `mode` | Return type (status, status-metrics, metrics-output, output) |
| `status_instruction` | How to report status (nullable) |
| `metrics_instruction` | How to report metrics (nullable) |
| `output_instruction` | How to report output (nullable) |
| `success_criteria` | What constitutes success, with evidence items (nullable) |
| `failure_criteria` | What constitutes failure, with evidence items (nullable) |

When mode includes "status", the template renders the SUCCESS/FAILURE block.

**Always present.** Reorderable.

### Critical Rules

Final emphasis — the non-negotiable rules. Content varies based on whether the agent has a custom output tool:

| Field | Purpose |
|-------|---------|
| `has_output_tool` | Whether a custom write tool exists |
| `tool_name` | Name of the write tool (nullable) |
| `batch_size` | Records per batch for batch writers (nullable) |

When `has_output_tool` is true, rules include tool discipline and batch discipline. When false, rules are limited to fail-fast, stay-in-scope, and no-invention.

**Always present.** Not reorderable (must be last body section).

---

## Standard Template Order

The default variant (`standard_v1`) renders sections in this order:

```
1. frontmatter          (locked — must be first)
2. identity             (locked — must follow frontmatter)
   ---
3. security_boundary    (if has_grants)
   ---
4. input
   ---
5. instructions
   ---
6. examples             (if present)
   ---
7. output
   ---
8. writing_output       (if present)
   ---
9. guardrails           (if constraints or anti_patterns exist)
   ---
10. return_format
    ---
11. critical_rules      (locked — must be last)
```

Horizontal rules (`---`) separate sections visually.

---

## Section Reordering and A/B Testing

### How Ordering is Controlled

Section order is controlled by the **variant template**. Each variant is a Jinja2 file in `templates/variants/` that includes section templates in a specific order. To test a different order, create a new variant.

For example, `standard_v1.md.j2` includes sections in the order above. A hypothetical `examples_first_v1.md.j2` could move examples before instructions.

### Locked Positions

Three sections have fixed positions:

| Section | Position | Why |
|---------|----------|-----|
| frontmatter | First | YAML block parsed by Claude Code before the LLM sees the prompt |
| identity | Second | Establishes who the agent is before any task content |
| critical_rules | Last | Final emphasis — recency bias means the last thing read carries extra weight |

### Reorderable Sections

Everything between identity and critical_rules can be reordered:

- **security_boundary** — could move after input (learn what you can do after learning what you receive)
- **input** — could move before or after security boundary
- **instructions** — could move after examples (see examples before reading instructions)
- **examples** — could move before instructions (learn by example first)
- **output** — could move closer to writing_output
- **writing_output** — could follow immediately after output or after guardrails
- **guardrails** — could move before instructions (set constraints before giving directions)
- **return_format** — could move earlier if success/failure criteria are important context

### A/B Testing Surfaces

Beyond section order, templates expose these testing surfaces:

| Surface | What Varies | Where |
|---------|-------------|-------|
| Section order | Which information appears first | Variant template |
| Identity framing | "You are a..." vs "Your role is..." vs leading with responsibility | `identity.md.j2` |
| Guardrail separation | Constraints and anti-patterns as one list vs separate headed lists | `guardrails.md.j2` |
| Example count | How many examples rendered from a larger bank | `max_entries` in data |
| Example headings | Show/hide per-entry headings within groups | `display_headings` in data |
| Instruction framing | Deterministic steps as imperatives vs probabilistic as guidance | `instructions.md.j2` |

### Creating a New Variant

1. Copy `templates/variants/standard_v1.md.j2`
2. Reorder the `{% include %}` lines
3. Keep frontmatter first, identity second, critical_rules last
4. Name it descriptively: `guardrails_early_v1.md.j2`, `examples_first_v1.md.j2`
5. Update `engine.py` to select the variant (currently hardcoded to `standard_v1`)

---

## Pipeline Architecture

```
anthropic_render.toml
  → gate_anthropic_render_input (Rust/PyO3: reads TOML, validates schema, returns JSON)
    → Pydantic models (frozen, generated from schema)
      → reshape functions (pure: explicit field selection per section)
        → RenderContext (frozen Pydantic model with all section contexts)
          → Jinja2 variant template (includes section templates)
            → rendered markdown string
              → writer (writes to disk)
```

Key principle: **boilerplate lives in templates, not in definition data.** The definition carries only the raw content insertions each section needs. Standard language ("This agent operates under bypassPermissions...") is baked into templates.
