# WRITING_OUTPUT -- TOML Extraction

## structure.toml

```toml
[writing_output]
has_output_tool = false
name_needed_visible = true
schema_validation_visible = true
heredoc_explanation_visible = false
```

**Decisions:**

- `has_output_tool` gates the entire section. When false, nothing renders -- no header, no mention. This is the master switch.
- `name_needed` controls whether name_pattern, name_construction, and the `{name}` placeholder appear in the invocation template. Currently always true when section renders; kept as a toggle for the hypothetical false case.
- `schema_validation` controls whether tool_validates_you_fix and validation_failure_recovery fragments render. Driven by presence of schema_path in the agent definition.
- `heredoc_explanation` defaults false. Both analyses lean toward omission. Toggle exists for testing if agents mangle heredoc syntax.

## content.toml

```toml
[writing_output]
heading = "Output Mechanics"

transition_preamble = "After processing input according to the instructions above, write your results using the following output tool."

only_this_tool_no_exceptions = "Output flows through one channel: the tool specified here. You do not write files directly. You do not choose alternative tools. You invoke this tool -- no exceptions, no 'just this once' with a different method."

tool_identity_label = "Your output tool is: `{{TOOL_NAME}}`"

invocation_preamble = "Your invocation template (copy exactly, substituting only the marked placeholders):"

placeholder_mapping = "`{name}` = output filename (constructed from name_pattern). `{json_data}` = your JSON records for this batch."

batch_discipline = "Your output rhythm is batched. Accumulate {{BATCH_SIZE}} processed records, then write them in a single tool invocation. Continue until all input is processed. The final invocation may contain fewer than {{BATCH_SIZE}} records -- that is expected. Never write single records individually."

output_location = "Your output tool writes to: `{{DIRECTORY_PATH}}`. The tool manages this directory -- you just invoke the tool."

name_construction = "Output filename = `{{NAME_PATTERN}}` where `{{PLACEHOLDER}}` comes from the input parameter `{{INPUT_FIELD}}`. Example: input {{INPUT_FIELD}} `abc-123` produces `abc-123.summaries.jsonl`."

json_format_in_heredoc = "Format your batch as JSONL: each record is a single-line JSON object, one per line. No trailing commas, no wrapping array."

tool_validates_you_fix = "Schema validation is handled by the tool, not by you. Records that fail validation are rejected. You are responsible for producing valid records. If the tool rejects a write, examine the error, fix the record, and retry."

validation_failure_recovery = "On validation failure: do not skip the record. Fix the structural error and resubmit. Do not proceed to the next batch with unwritten records. Never silently drop records that fail validation."

heredoc_explanation_text = "This uses heredoc syntax to pass multi-line JSON to the tool. The EOF markers delimit the content block."
```

**Decisions:**

- `only_this_tool_no_exceptions`: Highest-priority behavioral fragment. Anti-escape-hatch tone.
- `tool_validates_you_fix`: Critical for preventing ad-hoc validation logic. "Handled by the tool, not by you."
- `name_construction`: uid-to-interview-id mapping is the highest-risk cross-section dependency.
- `output_location`: "you just invoke the tool" prevents directory-management impulse.

## display.toml

```toml
[writing_output]
batch_size_threshold = 1
batch_size_format = ["batched", "single"]

json_format_example = "inline"
```

**Decisions:**

- `batch_size_format`: Threshold is on the data value (batch_size), not item count. "batched" when >1, "single" for degenerate case.

## Excluded (invariant rules / bare data)

- **Invocation code block**: Immutable data from tool_registry.toml. Injected verbatim as fenced code block.
- **Sub-block ordering**: transition → mandate → tool identity → invocation → placeholders → batch → location → naming → json format → schema → recovery. Invariant.
- **Silent record-dropping prohibition**: Invariant. Never configurable.
- **"Tool validates, agent fixes"**: Invariant rule. Content implements it but the split itself is not configurable.
