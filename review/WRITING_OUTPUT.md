# Writing Output Section — Four-Axis Review

## Data (WritingOutputAnthropic)

```
WritingOutputAnthropic
  .tool_name            ToolName/SnakeString (scalar)
  .invocation_variant   InvocationVariant (enum/gate)
  .invocation_display   InvocationDisplay (scalar)
  .name_needed          OutputToolNameNeeded/Boolean (scalar)
  .name_pattern         FilenameTemplate (scalar, optional)
  .batch_size           OutputToolBatchSize/Integer (scalar, optional)
  .schema_path          OutputToolSchemaXAbs (scalar, optional)
  .file_path            PathAbsolute (scalar, optional)
  .directory_path       PathAbsolute (scalar, optional)
```

Agent-builder: this section is only rendered when `has_output_tool = true`. For agent-builder, `has_output_tool = false` so this section is likely skipped.

## Content (WritingOutputContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"Output Mechanics"` |
| ✅ | 2 | `transition_preamble` | StringProse | `_preamble` | preamble | `"After processing input according to the instructions above, write your results using the following output tool."` |
| ✅ | 3 | `tool_mandate_preamble` | StringProse | `_preamble` | preamble | `"Output flows through one channel: the tool specified here. You do not write files directly. You do not choose alternative tools. You invoke this tool — no exceptions."` |
| ✅ | 4 | `invocation_preamble` | StringProse | `_preamble` | preamble | `"Your invocation template (copy exactly, substituting only the marked placeholders):"` |
| ✅ | 5 | `tool_identity_label_template` | StringTemplate | `_label_template` | body | `"Your output tool is: \`{{TOOL_NAME}}\`"` |
| ✅ | 6 | `heredoc_explanation_postscript` | StringProse | `_postscript` | body | `"This uses heredoc syntax to pass multi-line JSON to the tool. The EOF markers delimit the content block."` |

## Structure (WritingOutputStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `transition_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 2 | `tool_mandate_preamble_visible` | Boolean | `true` | → content #3 |
| ✅ | 3 | `heredoc_explanation_postscript_visible` | Boolean | `false` | → content #6 |

## Display (WritingOutputDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 2 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Output Mechanics"

PREAMBLE:
  ✅ transition_preamble                   "After processing input according to the instructions above..."
                                             [visible: transition_preamble_visible = true]
  ✅ tool_mandate_preamble                 "Output flows through one channel: the tool specified here..."
                                             [visible: tool_mandate_preamble_visible = true]
  ✅ invocation_preamble                   "Your invocation template (copy exactly, substituting only the marked placeholders):"
                                             [visible: implicit — no toggle, always renders]

BODY:
  [SCALAR] tool_name                       → interpolated into tool_identity_label_template
  ✅ tool_identity_label_template          "Your output tool is: `{{TOOL_NAME}}`"
                                             NOTE: uses UPPERCASE {{TOOL_NAME}} — check if data field is lowercase tool_name

  [GATE] invocation_variant                → GATE: selects which invocation template to render
  ❌ invocation_display                    InvocationDisplay scalar — the pre-formatted invocation block
                                             no content template renders it; it IS the content to render
  ❌ name_needed                           OutputToolNameNeeded/Boolean — controls name rendering
                                             no structure toggle or content field references it
  ❌ name_pattern                          FilenameTemplate scalar — no content template
  ❌ batch_size                            OutputToolBatchSize/Integer scalar — no content template
  ❌ schema_path                           OutputToolSchemaXAbs scalar — no content template
  ❌ file_path                             PathAbsolute scalar — no content template
  ❌ directory_path                        PathAbsolute scalar — no content template

  heredoc_explanation_postscript           "This uses heredoc syntax to pass multi-line JSON to the tool..."
                                             [visible: heredoc_explanation_postscript_visible = false]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: `tool_identity_label_template` uses `{{TOOL_NAME}}` — uppercase vs lowercase

Content template uses `{{TOOL_NAME}}` (uppercase). Data field is `tool_name` (lowercase). Template interpolation must handle case-insensitive matching, or the placeholder will not resolve. Need to confirm whether the template engine normalizes placeholder keys.

### ❌ ISSUE 2: `invocation_display` has no content template — it IS the content

`invocation_display` is the pre-formatted invocation block (the actual tool call syntax). It is not a gate — it is a scalar that needs to be rendered as-is (likely in a code fence). There is no content template that handles passthrough rendering of this field. This is the most critical missing piece of this section.

**Fix required:** A content passthrough mechanism for `invocation_display`, rendered as a code block. Or a `_body` content field that templates around it.

### ❌ ISSUE 3: `name_needed`, `name_pattern`, `batch_size`, `schema_path`, `file_path`, `directory_path` have no content templates

Six data fields exist with no corresponding content templates. These conditionally rendered fields need content templates and structure visibility toggles before they can render.

**Fix required:** Define content templates and structure visibility gates for each optional field. At minimum: `name_pattern`, `batch_size`, `schema_path`.

### ⚠️ ISSUE 4: `invocation_variant` gate logic not implemented

`invocation_variant` controls which form of invocation block renders (e.g., heredoc vs inline vs schema-embedded). The engine has no logic to select between invocation forms based on this gate value.

### ⚠️ ISSUE 5: Section-level skip not wired to `has_output_tool`

This section should only render when `has_output_tool = true` on the CriticalRules model. There is no cross-section visibility mechanism in the engine — the section would render even when there is no output tool.
