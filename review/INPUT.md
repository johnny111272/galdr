# Input Section — Four-Axis Review

## Data (Input)

```
Input
  .description          InputDescription (scalar)
  .format               DispatchInputFormat (enum/gate)
  .delivery             DispatchInputDelivery (enum/gate)
  .input_schema         PathExistsAbsolute (scalar, optional)
  .parameters           list of ParameterItem (optional)
       .param_name          SnakeString
       .param_type          ParamType
       .param_required      Boolean
       .param_description   ParamDescription (optional)
  .context_required     list of ContextItem (optional, NESTED BaseModel — currently skipped)
       .context_label       TitleString
       .context_path        PathAbsolute
  .context_available    list of ContextItem (optional, NESTED BaseModel — currently skipped)
```

Agent-builder: `format = "text"`, `delivery = "tempfile"`, 1 parameter, context fields are nested BaseModel (skipped by engine).

## Content (InputContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | TitleString | `section_start` | heading | `"Input"` |
| ✅ | 2 | `section_preamble` | StringProse | `_preamble` | preamble | `"Before processing your input, you must read and internalize several reference documents..."` |
| ✅ | 3 | `context_required_heading` | StringText | `_heading` | body | `"Required Reading"` (sub-heading within `[context]` body trunk) |
| ✅ | 4 | `context_required_intro` | StringProse | `_intro` | body | `"These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting."` |
| ✅ | 5 | `context_required_entry_template` | StringTemplate | `_entry_template` | body | `"**{{context_label}}**: Read \`{{context_path}}\`"` |
| ✅ | 6 | `context_available_heading` | StringText | `_heading` | body | `"Available Resources"` (sub-heading within `[context]` body trunk) |
| ✅ | 7 | `parameters_transition` | StringProse | `_transition` | body | `"With this knowledge internalized, here is your input data:"` |
| ✅ | 8 | `parameters_heading` | TitleString | `_heading` | body | `"Parameters"` (sub-heading within `[parameters]` body trunk) |
| ✅ | 9 | `parameters_entry_template` | StringTemplate | `_entry_template` | body | `` "`{{param_name}}` ({{param_type}}): {{param_description}}" `` |
| ✅ | 10 | `description_format_template` | StringTemplate | `_template` | body | `"Your input is a {{format}} file containing {{description}}."` |
| ✅ | 11 | `input_completeness_postscript` | StringProse | `_postscript` | body | `"Your input and required reading together constitute your complete input. Do not seek additional sources."` |
| ✅ | 12 | `schema_label_template` | StringTemplate | `_label_template` | body | `` "Input validates against: `{{input_schema}}`" `` |

## Structure (InputStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `section_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 2 | `context_required_intro_visible` | Boolean | `true` | → content #4 |
| ✅ | 3 | `parameters_transition_visible` | Boolean | `true` | → content #7 |
| ✅ | 4 | `input_completeness_postscript_visible` | Boolean | `false` | → content #11 |
| ✅ | 5 | `schema_label_visible` | Boolean | `true` | → content #12 |
| ✅ | 6 | `parameters_heading_visible` | VisibilityMode | `"auto"` | → content #8 (auto = show when parameters count ≥ threshold) |
| ✅ | 7 | `parameters_heading_auto_threshold` | Integer | `2` | threshold for above |

## Display (InputDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `context_required_format` | ListFormat | `"numbered"` | context_required list format — not wired |
| ⚠️ | 2 | `context_available_format` | ListFormat | `"bulleted"` | context_available list format — not wired |
| ⚠️ | 3 | `parameters_format` | UnionFormatOrPair | `["bulleted", "prose"]` | threshold-based parameter list format — not wired |
| ⚠️ | 4 | `parameters_format_threshold` | Integer | `2` | switch to prose below 2 items — not wired |
| ⚠️ | 5 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 6 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Input"

PREAMBLE:
  ✅ section_preamble                      "Before processing your input, you must read and internalize..."
                                             [visible: section_preamble_visible = true]

BODY:
  [description]
    [GATE] format                          → interpolated into description_format_template
    [GATE] delivery                        → used for conditional rendering of delivery-mode-specific content
    ✅ description_format_template         "Your input is a {{format}} file containing {{description}}."
                                             interpolates .format and .description

  [parameters]
    ✅ parameters_transition               "With this knowledge internalized, here is your input data:"
                                             [visible: parameters_transition_visible = true]
    ✅ parameters_heading                  "Parameters" (sub-heading)
                                             [visible: parameters_heading_visible = "auto", threshold = 2]
    [LIST] parameters                      For each ParameterItem:
      .param_name                          → interpolated into parameters_entry_template
      .param_type                          → interpolated into parameters_entry_template
      .param_description                   → interpolated into parameters_entry_template
      ⚠️ parameters_entry_template         "`{{param_name}}` ({{param_type}}): {{param_description}}"
                                             per-item template — interpolation with per-item data not wired
      ⚠️ format                            [display: parameters_format = ["bulleted", "prose"], threshold = 2]

  [context]
    ✅ context_required_heading            "Required Reading" (sub-heading)
                                             [renders only if context_required data is present]
    ✅ context_required_intro              "These are not reference materials to consult during work..."
                                             [visible: context_required_intro_visible = true]
                                             [renders only if context_required data is present]
    [NESTED] context_required              ⚠️ SKIPPED — nested BaseModel, engine cannot traverse
      Would render: context_required_entry_template per item
                                             [display: context_required_format = "numbered"]
    ✅ context_available_heading           "Available Resources" (sub-heading)
                                             [renders only if context_available data is present]
    [NESTED] context_available             ⚠️ SKIPPED — nested BaseModel, engine cannot traverse

  [input_completeness_postscript]
    ✅ input_completeness_postscript       "Your input and required reading together constitute your complete input."
                                             [visible: input_completeness_postscript_visible = false]

  [schema_label]
    [SCALAR] input_schema                  → interpolated into schema_label_template
    ✅ schema_label_template               "Input validates against: `{{input_schema}}`"
                                             [visible: schema_label_visible = true]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: `context_required` and `context_available` are NESTED BaseModel — skipped entirely

Both context fields hold `list of ContextItem` where `ContextItem` is a nested BaseModel (not a `RootModel`). The data unwrap only handles scalar fields and `RootModel` lists. The entire context rendering path is skipped — `context_required_entry_template` is never used, `context_required_heading` and `context_required_intro` are orphaned content.

**Fix required:** Either (a) add nested BaseModel traversal to the engine, or (b) define ContextItem as `RootModel[str]` with a pre-formatted string. Option (b) is simpler but moves formatting logic into the data.

### ⚠️ ISSUE 2: `parameters_entry_template` needs per-item interpolation

`parameters_entry_template` uses `{{param_name}}`, `{{param_type}}`, `{{param_description}}` — all per-item fields from `ParameterItem`. The engine does not yet support per-item template interpolation (the template is a body-slot content field, but its placeholders resolve from item fields, not section-level data). Each ParameterItem would need its own interpolation pass.

### ⚠️ ISSUE 3: `context_required_entry_template` same problem as parameters_entry_template

`context_required_entry_template` uses `{{context_label}}` and `{{context_path}}` — per-item ContextItem fields. Same per-item interpolation issue as above, compounded by the nested BaseModel issue.

### ⚠️ ISSUE 4: All display list format controls not wired

`context_required_format`, `context_available_format`, `parameters_format`, and `parameters_format_threshold` are not read. List rendering uses hardcoded defaults.

### ⚠️ ISSUE 5: `parameters_heading_visible = "auto"` — auto logic not implemented

The auto threshold checks `len(parameters) >= threshold`. The engine does not perform this count.
