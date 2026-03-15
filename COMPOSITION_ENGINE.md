# Galdr Composition Engine

Galdr is a universal agent composer. It takes frozen content from an upstream pipeline and composes it into deployable agent prompts using configurable rendering.

---

## Inputs

1. **Vendor render TOML** (e.g., `anthropic_render.toml`) — frozen content from upstream pipeline (Regin). Read-only. Never modified by Galdr.
2. **Recipe TOML** — composition config: module list with ordering, variant per module, per-module parameters. Controls the structure of the prompt.
3. **Style TOML** — tone config: heading text, framing text, warning text per module. Controls the voice of the prompt.

Content is frozen. Recipe and style are the independent variables. Changing one does not affect the others.

## Outputs

1. **Agent prompt** (`.md`) — deployable agent markdown file
2. **Dispatcher skill** (`SKILL.md`) — deployable dispatcher skill (when vendor render includes a dispatcher section)

---

## The Four Knobs

| Knob | What it controls | Where it lives |
|------|-----------------|----------------|
| **Order + skips** | Which modules render, in what sequence | Recipe: module list (order IS config, presence IS config) |
| **Display structure** | Bullets, numbered, prose, table, compact | Recipe: `variant` field per module |
| **Flavor/tone** | Headings, framing prose, emphasis, warnings | Style: per-module entries |
| **Special settings** | max_entries, display_headings, field visibility | Recipe: per-module params (data provides smart defaults) |

---

## 14 Modules

Each module is an independent rendering unit with its own data packet, config, and style entry.

| Module | Data shape | Optional | Locked position |
|--------|-----------|----------|-----------------|
| `frontmatter` | structured YAML fields | no | first (machine-parsed) |
| `identity` | key-value fields (title, role, expertise) | no | no |
| `security_boundary` | structured entries (path + tools) | yes | no |
| `input` | key-value + parameter list + context lists | no | no |
| `instructions` | list of steps (mode + text) | no | no |
| `examples` | nested: groups → entries (heading + text) | yes | no |
| `output` | key-value fields (format, paths, naming) | no | no |
| `writing_output` | invocation string | yes | no |
| `constraints` | list of strings | yes | no |
| `anti_patterns` | list of strings | yes | no |
| `success_criteria` | list of {definition, evidence[]} | yes | no |
| `failure_criteria` | list of {definition, evidence[]} | yes | no |
| `return_format` | mode + instruction strings | no | no |
| `critical_rules` | conditional fields (tool name, batch size) | no | no |

`frontmatter` must be first because the machine parser reads it before the LLM sees the prompt. All other modules are freely reorderable by recipe.

---

## Rendering Primitives

Small pure functions. Each takes typed data and returns a markdown string. No IO, no side effects, no dependencies beyond Python stdlib.

**List renderers:**
- `list_as_bullets(items: list[str]) -> str`
- `list_as_numbered(items: list[str]) -> str`
- `list_as_prose(items: list[str]) -> str`

**Structured renderers:**
- `structured_entries(entries: list[{definition, evidence}], evidence_mode) -> str`
- `field_set(fields: list[{label, value}], mode) -> str`
- `code_block(content: str) -> str`

**Assembly:**
- `heading(level: int, text: str) -> str`
- `section_frame(heading, framing, warning, content) -> str`

`section_frame` is the universal wrapper. Every module passes through it. It handles: heading (from style), optional framing text (from style, if enabled in config), optional warning text (from style, if enabled in config), then the rendered content from the appropriate primitive.

---

## Recipe Format

```toml
name = "standard-v1"
style = "default"

[[modules]]
section = "frontmatter"

[[modules]]
section = "identity"

[[modules]]
section = "security_boundary"

[[modules]]
section = "input"

[[modules]]
section = "instructions"
variant = "numbered"

[[modules]]
section = "examples"
# max_entries and display_headings come from data defaults

[[modules]]
section = "output"

[[modules]]
section = "writing_output"

[[modules]]
section = "constraints"
variant = "bullets"
framing = true

[[modules]]
section = "anti_patterns"
variant = "bullets"
framing = true

[[modules]]
section = "success_criteria"
variant = "standard"

[[modules]]
section = "failure_criteria"
variant = "standard"

[[modules]]
section = "return_format"

[[modules]]
section = "critical_rules"
variant = "numbered"
framing = true
```

**Recipe fields:**

| Field | Scope | Purpose |
|-------|-------|---------|
| `name` | recipe | Identifier, used in output filenames for batch mode |
| `style` | recipe | Which style TOML to load |
| `section` | per-module | Which module to render |
| `variant` | per-module | Rendering mode (omit for default) |
| `framing` | per-module | Include style's framing text (default: data-driven) |
| `warning` | per-module | Include style's warning text (default: false) |
| `fields` | per-module | Ordered list of fields to render (omit for all) |
| `max_entries` | examples | Cap on rendered entries per group |
| `display_headings` | examples | Toggle per-entry headings |

---

## Style Format

```toml
name = "default"

[frontmatter]
# no style — machine-parsed

[identity]
heading = ""
framing = ""

[security_boundary]
heading = "Security Boundary"
framing = ""

[input]
heading = "Input"
framing = ""

[instructions]
heading = "Processing"
framing = ""

[examples]
heading = "Examples"
framing = ""

[output]
heading = "Output"
framing = ""

[writing_output]
heading = "Writing Output (MANDATORY)"
framing = ""

[constraints]
heading = "Constraints"
framing = "You must at all times stay within these boundaries:"
warning = "Violation of any constraint is immediate failure."

[anti_patterns]
heading = "Anti-Patterns"
framing = "If you display any of the below traits you are *actively failing*:"
warning = ""

[success_criteria]
heading = "Success Criteria"
framing = ""
warning = ""

[failure_criteria]
heading = "Failure Criteria"
framing = ""
warning = ""

[return_format]
heading = "Return Format"
framing = ""

[critical_rules]
heading = "Critical Rules"
framing = "These are non-negotiable:"
warning = ""
```

---

## Engine Flow

```
vendor_render.toml
    |
    v
gate (Rust/PyO3) --> JSON --> Pydantic model --> reshape --> section data packets
                                                               |
recipe (TOML or built-in default) --> RecipeConfig             |
style  (TOML or built-in default) --> StyleConfig              |
                                                               |
                     composition engine <----- all three ------+
                          |
                          |  for each module in recipe:
                          |    1. look up section data (skip if None and optional)
                          |    2. look up module config from recipe
                          |    3. look up module style
                          |    4. select rendering primitive (variant + data shape)
                          |    5. render content
                          |    6. wrap in section_frame
                          |    7. collect
                          |
                          v
                     join with separators
                          |
                          v
                     markdown string --> writer --> disk
```

---

## What Changes

**Stays as-is:**
- Gate (Rust/PyO3) — TOML parsing and schema validation
- Pydantic models (AgentAnthropicRender) — typed access to validated data
- Reshape functions — schema field names to clean context names
- Context models (RenderContext) — typed data packets per section
- Writer — disk output
- Dispatcher rendering — separate, mechanical (keeps its own renderer)
- CLI entry point — gains new flags at L2+

**Removed:**
- Jinja2 dependency
- `templates/` directory (all `.md.j2` files)
- `engine.py` FileSystemLoader / Environment setup
- `variants/standard_v1.md.j2` master template

**New:**
- Rendering primitives (`render_primitives.py`) — pure functions
- Section renderers (`render_sections.py`) — per-module rendering logic
- Recipe model (`RecipeConfig`, `ModuleConfig`)
- Style model (`StyleConfig`, `StyleEntry`)
- Composition engine (`compose.py`) — pure function: context + recipe + style -> markdown
- Built-in default recipe (reproduces current output)
- Built-in default style (reproduces current headings/framing)
