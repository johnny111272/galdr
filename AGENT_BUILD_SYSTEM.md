# Agent Build System

## Purpose

One agent definition produces many agents. The composition engine takes a single validated data structure and multiplies it across style variants, display variants, and model configurations to produce a matrix of benchmarkable agent prompts.

This enables:
- Empirical optimization of prompt format through systematic benchmarking
- Regression testing when underlying LLM models are updated
- Auditable evidence that an agent meets quality and safety standards
- Reproducible agent configurations versioned as TOML files in git

---

## Pipeline

```
Verdandi → Draupnir → Nornir → Regin → Galdr
 (types)   (schemas)  (gates)  (resolver) (composer)
```

Everything upstream of Galdr exists to produce one clean, typed, gate-validated Pydantic model: the `anthropic_render` data structure. By the time data reaches Galdr, it has 14 top-level sections — each corresponding to one section of the final agent prompt.

Galdr's job is simple: combine data with style and display choices to produce markdown.

---

## Three Input Axes

Every rendered agent prompt is the product of three independent inputs:

| Axis | Source | Controls |
|------|--------|----------|
| **Data** | `anthropic_render.toml` | What to say — field values, paths, parameters, instructions |
| **Style** | `style/*.toml` | How to word it — labels, prose, templates, headings, framing |
| **Display** | `display/*.toml` | How to format it — list types, separators, structural layout |

These axes are orthogonal. Any style works with any display. Any combination works with any data.

---

## Data Axis

The data model is produced by the Regin pipeline and validated by a Nornir gate. It is a Pydantic model with 14 top-level sections:

| Section | Content |
|---------|---------|
| `frontmatter` | name, description, model, permission_mode, tools, hooks |
| `identity` | title, role_identity, role_description, role_expertise, role_responsibility |
| `security_boundary` | display entries (path + tools grants) |
| `input` | description, format, delivery, parameters, context, input_schema |
| `instructions` | steps (mode + text) |
| `examples` | groups → entries (heading + text) |
| `output` | description, format, schema_path, file/directory paths |
| `writing_output` | invocation_display |
| `constraints` | rules (string list) |
| `anti_patterns` | patterns (string list) |
| `success_criteria` | criteria → items (definition + evidence) |
| `failure_criteria` | criteria → items (definition + evidence) |
| `return_format` | mode, status/metrics/output instructions |
| `critical_rules` | has_output_tool, tool_name, batch_size |

Plus `dispatcher` which feeds a separate skill generation path.

No reshaping. The gate-validated Pydantic model IS the data. Field names are used directly.

---

## Style Axis

A style TOML defines every piece of text that appears in the rendered output that is not data. This includes:

- **Headings** — section and subsection titles
- **Labels** — field identifiers (`"Purpose"`, `"Schema"`, `"Evidence:"`)
- **Templates** — f-string patterns interpolated with data values (`"You are a {role_identity}."`)
- **Prose** — connective sentences that frame data (`"The dispatcher provides:"`)
- **Rules** — behavioral instruction text (`"Fail fast — if something is wrong, FAILURE immediately."`)

Each style TOML has the same 14 section names as the data model. The style for a section contains exactly the text fields needed to render that section.

```toml
# style/default.toml

[identity]
purpose_label = "Purpose"
role_template = "You are a {role_identity}."
responsibility_label = "Your responsibility"
expertise_label = "Expertise"

[input]
heading = "Input"
parameters_intro = "The dispatcher provides:"
schema_intro = "Input validates against:"
optional_suffix = "(optional)"

[security_boundary]
heading = "Security Boundary"
preamble = "This agent operates under `bypassPermissions` with hook-based restrictions."
grants_intro = "The following operations are allowed — everything else is blocked by the system."
boundary_warning = "Do not attempt operations outside this boundary."
```

Multiple styles can exist: `default.toml`, `stern.toml`, `collaborative.toml`, `concise.toml`. Each is a complete set of text for all 14 sections.

---

## Display Axis

A display TOML defines how collections (arrays) are formatted. Scalar fields render as text — display choices only apply to arrays.

Four display modes:

| Mode | Format | Example |
|------|--------|---------|
| `bulleted` | `- {item}` | `- Validate input` |
| `numbered` | `{i}. {item}` | `1. Validate input` |
| `sequential` | `{item}\n\n{item}` | Paragraphs separated by blank lines |
| `inline` | `{item}{separator}{item}` | `Python, schema design, testing` |

Each display TOML has the same 14 section names. For each section, it specifies how each array field should render:

```toml
# display/standard.toml

[identity]
expertise = "inline"
expertise_separator = ", "

[instructions]
steps = "numbered"

[constraints]
rules = "bulleted"

[anti_patterns]
patterns = "bulleted"

[success_criteria]
items = "sequential"
evidence = "bulleted"

[failure_criteria]
items = "sequential"
evidence = "bulleted"

[input]
parameters = "bulleted"
context_required = "bulleted"
context_available = "bulleted"

[security_boundary]
entries = "sequential"

[critical_rules]
rules = "numbered"

[examples]
groups = "sequential"
entries = "sequential"
```

Multiple display variants can exist: `standard.toml`, `numbered.toml`, `compact.toml`, `prose.toml`.

---

## Recipe

A recipe TOML controls ordering, section inclusion, and per-section overrides:

```toml
name = "standard-v1"
style = "default"
display = "standard"

[[modules]]
section = "frontmatter"

[[modules]]
section = "identity"

[[modules]]
section = "instructions"

[[modules]]
section = "constraints"
display = "numbered"      # override display for this section only

[[modules]]
section = "return_format"
```

Sections not listed in the recipe are dropped. Order in the recipe is order in the output. Per-module `style` or `display` overrides allow fine-grained mixing.

---

## Section Containers

Each section has a container that receives three typed inputs and produces markdown:

```python
identity = Identity(
    data=data_model.identity,
    style=style_model.identity,
    display=display_model.identity,
)
output = identity.render()
```

The container's job is trivial:
1. Interpolate style templates with data values
2. Format arrays according to display settings
3. Return a markdown string

No reshaping. No variant branching. No lookup tables. The data is already typed, the style is already typed, the display is already typed. They click together by section name.

---

## Composition

The composition engine iterates through the recipe and assembles section outputs:

```
for each module in recipe.modules:
    data    = data_model.{module.section}
    style   = resolve_style(module, style_model)
    display = resolve_display(module, display_model)
    section = Container(data, style, display)
    output.append(section.render())
```

`resolve_style` and `resolve_display` check for per-module overrides in the recipe, falling back to the recipe-level defaults.

---

## Matrix Multiplication

The composition engine enables systematic benchmarking:

```
agent_definitions  ×  llm_models  ×  display_variants  ×  style_variants  =  benchmark_matrix
```

One agent definition with 3 models, 4 display variants, and 3 style variants produces 36 agent prompts. Run them all against representative test data with known expected outputs.

Select the highest performers. Version the winning configuration. Re-run when models update.

---

## Versioning and Reproducibility

Every input is a TOML file in git:

```
definition v3 + style v2 + display v1 + recipe v1 + model claude-opus-4-6
```

This fully specifies a reproducible agent configuration. No code changes to vary an agent. No hidden state. Change one file, re-run, diff the output.

---

## Regression Testing

When an underlying LLM model is updated:

1. Re-run the benchmark matrix with the new model
2. Compare results against the previous baseline
3. Identify any agents adversely affected by the upgrade
4. Adjust definitions or configurations as needed
5. Re-benchmark to verify fixes

This turns model upgrades from a hope-and-pray event into a measurable, auditable process.

---

## Auditability

For regulated industries with strict safety and audit requirements:

- **Definition**: declarative TOML describing the agent's role, permissions, instructions
- **Test data**: representative inputs with known correct outputs
- **Benchmark results**: performance across N configurations
- **Selected configuration**: which style, display, model, and why
- **Verification run**: results against held-out test data
- **Regression history**: benchmark results across model versions

Every piece is a versionable artifact. Every decision has evidence. The system produces not just agents, but proof that those agents work.
