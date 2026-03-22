# Galdr Quickstart

Galdr is the final stage of the bragi agent pipeline. It takes an `anthropic_render.toml` file — the fully resolved, Anthropic-specific render data — and composes it with style and display configuration to produce two deployable artifacts:

- **Agent prompt** — `definitions/staging/{name}.md`
- **Dispatcher skill** — `definitions/staging/dispatch-{name}/SKILL.md`

Both are rendered from the same input file. The agent prompt is the instruction set the LLM executes. The dispatcher skill is the orchestration script a human invokes via `/dispatch-{name}` to feed work to that agent.

For the full design rationale, see `AGENT_BUILD_SYSTEM.md`.

---

## How to Run

```bash
cd /Users/johnny/.ai/smidja/galdr

# Render agent + dispatcher to definitions/staging/
uv run galdr path/to/anthropic_render.toml

# Render agent only (skip dispatcher)
uv run galdr path/to/anthropic_render.toml --agent-only

# Preview to stdout without writing
uv run galdr path/to/anthropic_render.toml --check

# Render to a specific agent output path
uv run galdr path/to/anthropic_render.toml -o path/to/output.md

# With a specific recipe
uv run galdr path/to/anthropic_render.toml --recipe recipes/terse-v1.toml

# With a specific style
uv run galdr path/to/anthropic_render.toml --style styles/stern.toml

# Benchmark set: render all recipes in a directory
uv run galdr path/to/anthropic_render.toml --recipe-batch recipes/benchmark-set/

# Override workspace root (auto-detected if omitted)
uv run galdr path/to/anthropic_render.toml --workspace /path/to/bragi
```

**Running guardrails:**
```bash
uv run pytest tests/test_guardrails.py   # Gleipnir structural checks — run FREQUENTLY
```

---

## Full Pipeline (Regin → Galdr)

```bash
# Step 1: Run the agent through regin
cd /Users/johnny/.ai/smidja/regin
uv run regin /Users/johnny/.ai/spaces/bragi/definitions/agents/agent-builder.toml

# Step 2: Render with galdr
cd /Users/johnny/.ai/smidja/galdr
uv run galdr /Users/johnny/.ai/spaces/bragi/definitions/agents/agent-builder/anthropic_render.toml
```

---

## Three Input Axes

| Axis | Source | Controls |
|------|--------|----------|
| **Data** | `anthropic_render.toml` | What to say — content from the pipeline |
| **Style** | `styles/*.toml` | How to word it — labels, prose, templates, headings |
| **Display** | `display/*.toml` | How to format it — list types, separators, layout |

These are orthogonal. Any style works with any display. The recipe controls ordering, section inclusion, and per-section overrides.

---

## Input / Output

**Reads:**
- `definitions/agents/{name}/anthropic_render.toml` — validated by Nornir gate
- `recipes/*.toml` — composition ordering and overrides
- `styles/*.toml` — text configuration
- `display/*.toml` — formatting configuration

**Produces:**
- `definitions/staging/{name}.md` — the rendered agent prompt
- `definitions/staging/dispatch-{name}/SKILL.md` — the rendered dispatcher skill

---

## 14 Sections

The data model has 14 top-level sections, each mapping 1:1 to a recipe module:

| Section | Content | Optional |
|---------|---------|----------|
| `frontmatter` | name, description, model, tools, hooks | no |
| `identity` | title, role, expertise, responsibility | no |
| `security_boundary` | permission grants (path + tools) | yes |
| `input` | format, parameters, context, schema | no |
| `instructions` | processing steps | no |
| `examples` | grouped example entries | yes |
| `output` | format, schema, file paths | no |
| `writing_output` | write tool invocation | yes |
| `constraints` | behavioral rules | yes |
| `anti_patterns` | failure patterns | yes |
| `success_criteria` | success definitions + evidence | yes |
| `failure_criteria` | failure definitions + evidence | yes |
| `return_format` | SUCCESS/FAILURE protocol | no |
| `critical_rules` | non-negotiable rules | yes |

Plus `dispatcher` which feeds the skill generation path.

---

## Where Things Live

| Resource | Path |
|----------|------|
| Galdr source | `smidja/galdr/src/galdr/` |
| Agent definitions (input) | `definitions/agents/{name}/anthropic_render.toml` |
| Rendered output (staging) | `definitions/staging/` |
| Recipes | `smidja/galdr/recipes/` |
| Styles | `smidja/galdr/styles/` |
| Display variants | `smidja/galdr/display/` |
| Schemas | `smidja/galdr/schemas/` |
| Design spec | `smidja/galdr/AGENT_BUILD_SYSTEM.md` |
| Dispatcher guide | `smidja/galdr/BUILDING_A_DISPATCHER.md` |
| Custom write tools | `smidja/galdr/CUSTOM_WRITE_TOOL.md` |

---

## Upstream Dependencies

| Dependency | Purpose |
|------------|---------|
| Nornir gates | Rust/PyO3 modules — read TOML, validate against schema, return JSON |
| Regin | Pipeline that produces `anthropic_render.toml` (stages L0-L8) |
| Verdandi/Draupnir | Type system and schema generation for the data model |

---

## What NOT to Do

1. **Do not reshape data.** The gate-validated Pydantic model IS the data. Use field names directly.
2. **Do not read TOML directly in Python.** Nornir gates handle TOML parsing and schema validation.
3. **Do not validate data in Python.** Gates validate against JSON Schema. Pydantic provides typed access.
4. **Do not hardcode text in renderers.** Labels, prose, headings, rules — everything lives in style TOMLs.
5. **Do not put IO outside the impure boundary.** Gate calls and file writes are the only impure operations.
6. **Do not entangle axes.** Changing a style must never require changing the data or display.
