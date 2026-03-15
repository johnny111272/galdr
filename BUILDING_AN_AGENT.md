# Building an Agent with Galdr

Galdr is the universal agent composer. It takes a vendor-specific render TOML (e.g., `anthropic_render.toml`) and composes it into a deployable agent prompt and companion dispatcher skill.

Galdr is vendor-agnostic. The composition system — modules, recipes, styles — works identically regardless of which vendor format produced the content. Resin level 7 produces a `universal_render.toml` (vendor-agnostic), level 8 fans out for per-vendor resolution. Anthropic is the first implemented target. The architecture supports additional vendor targets without changing the composition layer.

## Three Axes

Agent rendering has three independent concerns:

1. **Content** — vendor render TOML (e.g., `anthropic_render.toml`) — what the agent knows, does, and produces. This comes from the upstream pipeline (regin) and is never modified by Galdr.
2. **Composition** — recipe TOML — which modules to include, what order, which structural variant of each module. Controls the shape of the prompt.
3. **Style** — style TOML — framing language, section headings, tone. Controls how each section is introduced to the LLM.

Content is frozen. Composition and style are the independent variables. Changing one does not affect the others. The recipe and style layer do not know or care which vendor produced the content.

---

## Why Composability Matters

The entire reason for building a template system instead of string concatenation is empirical optimization. Given one vendor render TOML:

- Produce N different agent prompts by varying composition and style
- Run all N against the same benchmark dataset with the same rubric
- Measure which prompt structure produces the best agent behavior for the task
- Iterate on the winning composition

This only works if the content is identical across variants and only the template composition varies. If content and structure are entangled, the experiment is contaminated and results are incomparable.

---

## Modules

Every section of the agent prompt is an independent **module**. Each module is a self-contained Jinja2 template that renders one section from its own data packet. Modules never reach across each other's data.

### Module Directory

```
templates/modules/
  frontmatter/
    standard.md.j2
  identity/
    standard.md.j2
  security_boundary/
    standard.md.j2
  input/
    standard.md.j2
  instructions/
    standard.md.j2
  examples/
    standard.md.j2
    compact.md.j2
  output/
    standard.md.j2
  writing_output/
    standard.md.j2
  constraints/
    bullets.md.j2
    prose.md.j2
    numbered.md.j2
  anti_patterns/
    bullets.md.j2
    stern.md.j2
  return_format/
    standard.md.j2
  critical_rules/
    standard.md.j2
```

Each module directory contains one or more **variants** — different structural approaches to rendering the same data. A recipe selects which variant to use for each module. If no variant is specified, the engine falls back to the default for that module.

### Naming Convention

`{section}/{variant-name}.md.j2`

Variant names describe the structural approach:

- `bullets` — bullet list
- `prose` — paragraph text with framing
- `numbered` — numbered list
- `stern` — bullet list with failure-oriented framing
- `compact` — minimal rendering, fewer headings, limited entries
- `standard` — the default rendering for this module

Room for further specialization: `prose-collaborative`, `bullets-minimal`, etc.

### Module Independence

Constraints and anti-patterns are **separate modules**, not subsections of a combined guardrails module. This allows:

- Placing them adjacent or apart in the prompt
- Using different structural variants for each (constraints as numbered, anti-patterns as prose)
- Including one without the other
- Testing whether proximity to instructions vs examples affects behavior

Any two modules that have distinct semantic purposes should be separate modules, even if they are often rendered together.

---

## Recipes

A recipe is a TOML file that declares the composition: which modules, what order, which variant, and per-module parameters.

```toml
name = "prose-verbose-v1"
style = "stern"

[[modules]]
section = "frontmatter"

[[modules]]
section = "identity"

[[modules]]
section = "constraints"
variant = "prose"

[[modules]]
section = "input"

[[modules]]
section = "instructions"

[[modules]]
section = "examples"
max_entries = 3
display_headings = true

[[modules]]
section = "anti_patterns"
variant = "stern"

[[modules]]
section = "output"

[[modules]]
section = "writing_output"

[[modules]]
section = "return_format"

[[modules]]
section = "critical_rules"
```

### Recipe Fields

| Field | Scope | Purpose |
|-------|-------|---------|
| `name` | recipe | Human-readable identifier, used in output filenames |
| `style` | recipe | Which style TOML to load for framing language |
| `section` | per-module | Which module to render |
| `variant` | per-module | Which template variant (omit for default) |
| `max_entries` | per-module | Cap on rendered entries (examples) |
| `display_headings` | per-module | Show/hide per-entry headings (examples) |

Per-module parameters override any defaults from the data. The data carries `display_headings` and `examples_max_number` from the definition — the recipe can override them per composition.

### Locked Positions

Three sections have fixed positions that recipes must respect:

| Section | Position | Why |
|---------|----------|-----|
| `frontmatter` | first | YAML block parsed by Claude Code before the LLM sees the prompt |
| `identity` | second | Establishes who the agent is before any task content |
| `critical_rules` | last | Recency bias — the last thing read carries extra weight |

Everything between identity and critical_rules is freely reorderable.

---

## Styles

A style is a TOML file that provides framing language and headings for every module in a particular tone.

```toml
# styles/stern.toml
name = "stern"

[constraints]
heading = "Constraints"
framing = "You must at all times stay within these boundaries:"

[anti_patterns]
heading = "Anti-Patterns"
framing = "If you display any of the below traits you are *actively failing*:"

[instructions]
heading = "Processing"
framing = ""

[examples]
heading = "Examples"
framing = "Study these carefully before beginning work:"

[critical_rules]
heading = "Critical Rules"
framing = "These are non-negotiable:"
```

```toml
# styles/collaborative.toml
name = "collaborative"

[constraints]
heading = "Boundaries"
framing = "Keep these constraints in mind as you work:"

[anti_patterns]
heading = "Common Mistakes"
framing = "Watch out for these — they are easy to fall into:"

[examples]
heading = "Examples"
framing = "Here are some examples to guide your approach:"

[critical_rules]
heading = "Final Reminders"
framing = "Before you begin, remember:"
```

The style is selected by the recipe's `style` field. Templates access style data as `{{ style.heading }}` and `{{ style.framing }}`.

### Style vs Variant

These are different concerns:

- **Variant** = structural choice — bullets, prose, numbered, compact
- **Style** = textual choice — headings, framing language, tone

A `prose` variant with a `stern` style produces different output than a `prose` variant with a `collaborative` style. The variant controls shape. The style controls voice.

---

## Running Galdr

```bash
cd tools/galdr

# Default recipe (backward compatible)
uv run python -m galdr.cli path/to/vendor_render.toml

# With a specific recipe
uv run python -m galdr.cli path/to/vendor_render.toml --recipe recipes/prose-verbose.toml

# Benchmark set: render all recipes in a directory
uv run python -m galdr.cli path/to/vendor_render.toml --recipe-batch recipes/benchmark-set/

# Preview to stdout
uv run python -m galdr.cli path/to/vendor_render.toml --recipe recipes/stern.toml --check
```

The input file can be any vendor render TOML (e.g., `anthropic_render.toml`). Output goes to `definitions/staging/`. When using `--recipe-batch`, each output is suffixed with the recipe name for disambiguation.

---

## Pipeline Architecture

```
vendor_render.toml     (content — e.g., anthropic_render.toml)
recipe.toml            (composition)
style.toml             (framing)
    │
    ▼
vendor gate (Rust/PyO3: reads TOML, validates against vendor schema, returns JSON)
    │
    ▼
Pydantic models (frozen, generated from schema)
    │
    ▼
reshape functions (pure: content → per-module data packets)
    │
    ▼
recipe engine (reads recipe, resolves module variants, loads style)
    │
    ▼
Jinja2 renders each module with its data packet + style context
    │
    ▼
assembled markdown string
    │
    ▼
writer (disk)
```

Key principle: **boilerplate lives in templates, not in definition data.** The definition carries only the raw content insertions each section needs. Standard language, framing, and section structure are owned by the template + style layer.

---

## Design Rules

1. **Content and composition are separate.** The vendor render TOML is never modified by Galdr. It is read-only input.
2. **Modules are independent.** Each module renders from its own data packet. No cross-module data access.
3. **Recipes are declarative.** A recipe is a TOML manifest, not executable code. The engine interprets it.
4. **Styles are complete.** A style file provides entries for every module. No partial styles.
5. **Per-module parameters override data defaults.** The recipe is the authority on composition choices.
6. **Locked positions are enforced.** The engine validates that frontmatter is first, identity is second, critical_rules is last.
7. **Gate validates, Pydantic types, templates render.** Three layers, no overlap.
8. **Reshape is the explicit mapping layer.** Schema field names to template field names, every selection visible.
9. **Frozen models everywhere.** `ConfigDict(frozen=True)` on every model.
10. **IO lives in impure boundary only.** `gates.py`, `loader.py`, `engine.py`, `writer.py` are the only files that touch the filesystem.

---

## What NOT to Do

1. **Do not read TOML directly in Python.** The Nornir gate handles TOML parsing and schema validation. Galdr receives validated JSON.
2. **Do not validate data in Python.** The gate validates against JSON Schema. Pydantic models provide typed access. No third layer.
3. **Do not put IO outside the impure boundary.** Four files touch the filesystem. Everything else is pure.
4. **Do not inline boilerplate in definition data.** Standard language belongs in templates and styles.
5. **Do not entangle content and composition.** If changing a template requires changing the TOML, the boundary is broken.
6. **Do not silently drop fields in reshape functions.** Every field the data carries must either flow through to the template context or be explicitly documented as unused.
7. **Do not fabricate data in Galdr.** Galdr renders what it receives. If data is missing, the upstream pipeline is responsible — Galdr does not invent defaults, derive fields, or compose strings.

---

## Current State

The module system, recipe engine, and style registry described above are the target architecture. The current implementation uses a single monolithic variant template (`standard_v1.md.j2`) with hardcoded section includes. Migration path:

1. Split existing section templates into module directories
2. Implement recipe loading and module resolution in the engine
3. Implement style loading and injection into template context
4. Create a default recipe that reproduces current `standard_v1` output
5. Build additional recipes and styles for benchmarking

The reshape functions, gate integration, and pure/impure boundary are already in place and do not change.
