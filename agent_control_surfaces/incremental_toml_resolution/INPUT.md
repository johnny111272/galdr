# INPUT — TOML Extraction

## structure.toml

```toml
[input]
section_preamble_visible = true
input_completeness_postscript_visible = true
readiness_checkpoint_postscript_visible = true
context_entry_presentation = "list"
parameter_presentation = "list"
```

**Decisions:**

- `section_preamble_visible`: Data-gated (context_required must exist) AND structure-toggled. Both must be true.
- `readiness_checkpoint_postscript_visible`: High-leverage for context-heavy agents, omittable for simple agents.

## content.toml

```toml
[input]
heading = "Input"
section_preamble = "Before processing your input, you must read and internalize several reference documents. Your input data and prerequisite knowledge are described below."
input_description = "Your input is a {{format}} file containing {{description}}."
context_required_heading = "Required Reading"
context_required_preamble = "These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting."
context_entry = "**{{context_label}}**: Read `{{context_path}}`"
knowledge_data_transition = "With this knowledge internalized, here is your input data:"
input_completeness_postscript = "Your tempfile and required reading together constitute your complete input. Do not seek additional sources."
readiness_checkpoint_postscript = "Confirm you have: (1) your input data at the tempfile path, (2) knowledge from all required reading. Now proceed."
```

**Decisions:**

- `heading`: Alternatives: "What You Receive", "Data and Context".
- `context_required_heading`: "Required Reading" over "Before You Begin" — communicates WHAT and HOW, not just WHEN.
- `context_required_preamble`: Explicitly dismisses wrong mental model ("not reference materials to consult").
- `knowledge_data_transition`: Cognitive shift between context entries and input data. Position is between the two blocks.

## display.toml

```toml
[input]
context_entry_format = ["numbered", "bulleted"]
context_entry_format_threshold = 4
parameter_format = ["bulleted", "prose"]
parameter_format_threshold = 3
```

**Decisions:**

- `context_entry_format`: Numbered above 4 implies reading order for large sets.

## Excluded (invariant rules / bare data)

- **Sub-block ordering**: description/format → context_required → parameters. Invariant.
- **Delivery**: Always tempfile. Integrated into `input_description` template.
- **Format-specific operational prose**: "read holistically" vs "process per-record" — open design question, deferred. May become conditional content field keyed on format.
