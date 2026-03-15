# Galdr Quickstart

Galdr is the final stage of the bragi agent pipeline. It takes an `anthropic_render.toml` file — the fully resolved, Anthropic-specific render data — and produces two deployable artifacts:

- **Agent prompt** — `.claude/agents/{name}.md`
- **Dispatcher skill** — `.claude/skills/dispatch-{name}/SKILL.md`

Both are rendered from the same input file. The agent prompt is the instruction set the LLM executes. The dispatcher skill is the orchestration script a human invokes via `/dispatch-{name}` to feed work to that agent.

---

## How to Run

```bash
cd /Users/johnny/.ai/spaces/bragi/tools/galdr

# Render agent + dispatcher to definitions/staging/
uv run python -m galdr.cli path/to/anthropic_render.toml

# Render agent only (skip dispatcher)
uv run python -m galdr.cli path/to/anthropic_render.toml --agent-only

# Preview to stdout without writing
uv run python -m galdr.cli path/to/anthropic_render.toml --check

# Render to a specific agent output path
uv run python -m galdr.cli path/to/anthropic_render.toml -o path/to/output.md

# Override workspace root (auto-detected if omitted)
uv run python -m galdr.cli path/to/anthropic_render.toml --workspace /path/to/bragi
```

**Entry point:** defined in `pyproject.toml` as `galdr = "galdr.cli:main"`.

**Running guardrails:**
```bash
cd /Users/johnny/.ai/spaces/bragi/tools/galdr
uv run pytest tests/test_guardrails.py   # Gleipnir structural checks — run FREQUENTLY
```

---

## Input / Output

**Reads:**
- `definitions/agents/{agent-name}/anthropic_render.toml` — the fully resolved render data, validated by a Nornir gate against `schemas/agent-anthropic-render.schema.json`

**Produces:**
- `definitions/staging/{agent-name}.md` — the rendered agent prompt
- `definitions/staging/dispatch-{agent-name}/SKILL.md` — the rendered dispatcher skill (when the TOML has a `[dispatcher]` section)

Workspace root is auto-detected by walking parent directories until finding `schemas/` + `definitions/` as siblings.

---

## Architecture

### Pipeline

```
anthropic_render.toml
  → gate_anthropic_render_input (Rust/PyO3: reads TOML, validates schema, returns JSON)
    → Pydantic models (frozen, generated from schema)
      → reshape functions (pure: explicit field selection per section)
        → RenderContext (frozen Pydantic model with all section contexts)
          → Jinja2 variant template (agent) + skill template (dispatcher)
            → rendered markdown strings
              → writer (writes to disk)
```

Key principle: **boilerplate lives in templates, not in definition data.** The definition carries only the raw content insertions each section needs. Standard language ("This agent operates under bypassPermissions...") is baked into templates.

### Two-Boundary IO Design

IO exists in exactly four files. Everything else is pure computation.

```
IMPURE: gates.py     — imports and calls Nornir PyO3 gate modules
        loader.py    — calls the gate, returns validated JSON string
        engine.py    — loads Jinja2 templates from disk, renders to string
        writer.py    — writes rendered strings to disk

PURE:   context.py   — builds RenderContext from validated JSON
        reshape_*.py — maps schema model fields to template context fields
        unwrap.py    — unwraps RootModel/Enum wrappers to plain scalars
```

### Source Layout

```
src/galdr/
  cli.py                                # CLI: parse args, dispatch to pipeline
  structures/                           # Frozen Pydantic models (data only, zero methods)
    anthropic_render.py                 # Schema models (generated from JSON Schema)
    template_context.py                 # Template context models (what templates see)
    gate_types.py                       # Gate result model
    errors.py                           # GateValidationError
  functions/
    pure/                               # No IO, no side effects
      context.py                        # build_render_context: JSON → RenderContext
      reshape_frontmatter.py            # Frontmatter section reshape
      reshape_identity.py               # Identity section reshape
      reshape_security_boundary.py      # Security boundary reshape
      reshape_input.py                  # Input section reshape (parameter renames)
      reshape_instructions.py           # Instructions reshape
      reshape_examples.py               # Examples reshape
      reshape_output.py                 # Output section reshape
      reshape_writing_output.py         # Writing output reshape
      reshape_guardrails.py             # Constraints + anti-patterns reshape
      reshape_return_format.py          # Return format reshape
      reshape_critical_rules.py         # Critical rules reshape
      reshape_dispatcher.py             # Dispatcher section reshape
      unwrap.py                         # RootModel/Enum → plain scalar
    impure/                             # File IO only
      gates.py                          # Gate module loader (ONLY importlib user)
      loader.py                         # TOML → validated JSON via gate
      engine.py                         # Jinja2 environment + render functions
      paths.py                          # Output path derivation
      writer.py                         # Write rendered markdown to disk
      pipeline.py                       # Orchestration: load → context → render → write
  templates/
    sections/                           # Per-section Jinja2 templates (11 sections)
      frontmatter.md.j2
      identity.md.j2
      security_boundary.md.j2
      input.md.j2
      instructions.md.j2
      examples.md.j2
      output.md.j2
      writing_output.md.j2
      guardrails.md.j2
      return_format.md.j2
      critical_rules.md.j2
    variants/                           # Agent variant templates (section ordering)
      standard_v1.md.j2
    skills/                             # Dispatcher skill templates
      dispatch_v1.md.j2
```

---

## The Reshape Pattern

Every section has its own `reshape_*.py` file. The reshape function:

1. Takes the schema model (from `structures/anthropic_render.py`)
2. Calls `unwrap()` on every RootModel/Enum field to get plain scalars
3. Renames fields to template-friendly names (e.g., `param_name` → `name`)
4. Returns a frozen context model (from `structures/template_context.py`)
5. Makes every field selection visible — no silent dropping, no JSON roundtrips

All reshape functions are composed in `context.py:build_render_context()`, which produces the single `RenderContext` that templates consume.

---

## Agent Sections

Every rendered agent prompt is assembled from independent sections. Each section has its own Jinja2 template and its own data packet. Sections never reach across each other's data.

| Section | Template | Required | Locked Position |
|---------|----------|----------|-----------------|
| frontmatter | `frontmatter.md.j2` | always | first |
| identity | `identity.md.j2` | always | second |
| security_boundary | `security_boundary.md.j2` | when has_grants | — |
| input | `input.md.j2` | always | — |
| instructions | `instructions.md.j2` | always | — |
| examples | `examples.md.j2` | when present | — |
| output | `output.md.j2` | always | — |
| writing_output | `writing_output.md.j2` | when custom output tool exists | — |
| guardrails | `guardrails.md.j2` | when constraints or anti_patterns exist | — |
| return_format | `return_format.md.j2` | always | — |
| critical_rules | `critical_rules.md.j2` | always | last |

Sections between identity and critical_rules can be reordered via variant templates.

For full section documentation: `BUILDING_AN_AGENT.md`

---

## Dispatcher Skills

A dispatcher is a skill (`.claude/skills/dispatch-{name}/SKILL.md`) that orchestrates agent work. It does three things:

1. **Orchestrate** — route user intent to the right agent with the right input
2. **Batch split** — divide work into chunks using `split_jsonl_batches` (batch mode only)
3. **Scope discovery** — when no args given, read filesystem state and present options via AskUserQuestion

The dispatcher template (`skills/dispatch_v1.md.j2`) renders from the same `RenderContext` as the agent, accessing `dispatcher`, `identity`, `input`, and `output` contexts.

For full dispatcher documentation: `BUILDING_A_DISPATCHER.md`

---

## Section Reordering and A/B Testing

Section order is controlled by the **variant template**. Each variant is a Jinja2 file in `templates/variants/` that includes section templates in a specific order. To test a different order, create a new variant.

Three positions are locked:
- **frontmatter** — first (YAML block parsed by Claude Code before the LLM sees the prompt)
- **identity** — second (establishes who the agent is before any task content)
- **critical_rules** — last (recency bias means the last thing read carries extra weight)

Everything between is reorderable. Create a new variant by copying `standard_v1.md.j2`, reordering the `{% include %}` lines, and updating `engine.py` to select it.

---

## Where Things Live

| Resource | Path |
|----------|------|
| Galdr source | `tools/galdr/src/galdr/` |
| Templates | `tools/galdr/src/galdr/templates/` |
| Agent definitions (input) | `definitions/agents/{name}/anthropic_render.toml` |
| Rendered output (staging) | `definitions/staging/` |
| Anthropic render schema | `schemas/agent-anthropic-render.schema.json` |
| Schema models (generated) | `tools/galdr/src/galdr/structures/anthropic_render.py` |
| Gate module | `~/.ai/tools/lib/gate_anthropic_render_input.so` |
| Section guide | `tools/galdr/BUILDING_AN_AGENT.md` |
| Dispatcher guide | `tools/galdr/BUILDING_A_DISPATCHER.md` |
| Custom write tools | `tools/galdr/CUSTOM_WRITE_TOOL.md` |

---

## Upstream Dependencies

| Dependency | Purpose |
|------------|---------|
| `gate_anthropic_render_input` | Nornir PyO3 gate — reads TOML, validates against schema, returns JSON |
| `schemas/agent-anthropic-render.schema.json` | Schema the gate validates against (produced by draupnir) |
| `anthropic_render.toml` files | Produced by regin (the anthropic resolver, pipeline stage 8) |

---

## What NOT to Do

1. **Do not read TOML directly in Python.** The Nornir gate handles TOML parsing and schema validation. Galdr receives validated JSON. If you're importing `toml` or `tomllib`, you're bypassing the gate.

2. **Do not validate data in Python.** The gate validates against the JSON Schema. The Pydantic models provide typed access. There is no third layer of validation needed.

3. **Do not put IO outside the impure boundary.** `gates.py`, `loader.py`, `engine.py`, and `writer.py` are the only files that touch the filesystem or import external modules. Reshape functions and context building are pure.

4. **Do not inline boilerplate in definition data.** Standard language belongs in templates. The definition carries only the raw content insertions each section needs. If you're adding "This agent operates under..." to the TOML, it goes in the template instead.

5. **Do not silently drop fields in reshape functions.** Every field selection must be visible. If a field exists in the schema model and isn't in the template context, the reshape function is the place where that decision is documented.

6. **Do not use `cross_boundary()` within galdr.** That was a previous mistake. It silently drops fields on name mismatches with no error. Reshape functions handle field mapping explicitly.

7. **Do not modify `anthropic_render.py` to add custom fields.** This file is generated from the JSON Schema via `datamodel-codegen`. Changes belong in the schema (verdandi → draupnir → schema → codegen → models). Manual edits to fix codegen issues (like `oneOf` union collapse) are the exception.

---

## Key Design Principles

- **Gate validates, Pydantic types, templates render** — three layers, no overlap
- **Reshape is the explicit mapping layer** — schema field names to template field names, every selection visible
- **Templates own boilerplate** — standard language, formatting, section structure
- **Frozen models everywhere** — `ConfigDict(frozen=True)` on every model
- **One reshape function per section** — small, single-purpose, composable
- **Variant templates control ordering** — swap section order without touching data or reshape logic
