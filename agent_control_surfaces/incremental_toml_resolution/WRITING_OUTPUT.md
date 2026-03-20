# WRITING_OUTPUT -- TOML Extraction

## structure.toml

```toml
[writing_output]
# Transition sentence connecting from instructions to this section
transition_preamble_visible = true

# Tool exclusivity mandate prose
tool_mandate_visible = true

# Heredoc syntax explanation (off by default — only if agents mangle heredoc)
heredoc_explanation_visible = false
```

**Decisions:**

- `has_output_tool` gates the entire section in code. Not a structure toggle — silence for absence.
- `name_needed`, `schema_path` presence, `batch_size > 1` are all data conditions evaluated by the renderer. Not toggles.
- `tool_mandate_visible`: The only high-leverage prose fragment. Everything else is data or code conditionals.

## content.toml

```toml
[writing_output]
heading = "Output Mechanics"

transition_preamble = "After processing input according to the instructions above, write your results using the following output tool."

tool_mandate = "Output flows through one channel: the tool specified here. You do not write files directly. You do not choose alternative tools. You invoke this tool — no exceptions."

tool_identity_label = "Your output tool is: `{{TOOL_NAME}}`"

invocation_preamble = "Your invocation template (copy exactly, substituting only the marked placeholders):"

heredoc_explanation = "This uses heredoc syntax to pass multi-line JSON to the tool. The EOF markers delimit the content block."
```

**Decisions:**

- `tool_mandate`: Highest-priority prose. Anti-escape-hatch tone.
- `invocation_preamble`: "copy exactly" is the critical instruction. The template itself is data from tool_registry.

## display.toml

```toml
[writing_output]
# No display knobs for this section.
```

## Excluded (invariant rules / bare data)

- **Invocation code block**: Immutable data from tool_registry.toml. Injected verbatim as fenced code block.
- **Sub-block ordering**: transition → mandate → tool identity → invocation → batch → naming → schema → recovery. Invariant.
- **Batch discipline**: Renders when batch_size > 1. Text is data-conditional, not a knob.
- **Name construction**: Renders when name_needed = true. Placeholder mapping derived from invocation template.
- **Schema validation + recovery**: Renders when schema_path exists. "Tool validates, agent fixes" is invariant.
- **Output location**: Data pass-through. Directory path rendered as-is.
- **Silent record-dropping prohibition**: Invariant. Never configurable.
