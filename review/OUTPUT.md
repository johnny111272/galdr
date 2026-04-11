# Output Section — Four-Axis Review

## Data (Output)

```
Output
  .description          OutputDescription (scalar)
  .format               OutputFormatKind (enum/gate)
  .name_known           OutputNameKnown (enum/gate)
  .schema_path          PathExistsAbsolute (scalar, optional)
  .output_file          PathAbsolute (scalar, optional)
  .output_directory     PathAbsolute (scalar, optional)
  .name_template        FilenameTemplate (scalar, optional)
  .name_instruction     StringProse (scalar, optional)
  .schema_embed         Boolean (gate, optional)
```

Agent-builder: `format = "text"`, `name_known = "unknown"`, `output_directory` present, `name_instruction` present. `schema_path`, `output_file`, `name_template` absent.

## Content (OutputContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"What You Produce"` |
| ✅ | 2 | `output_description_template` | StringTemplate | `_template` | body | `"You produce: {{DESCRIPTION}}"` |
| ✅ | 3 | `format_template` | StringTemplate | `_template` | body | `"Output format: {{FORMAT}}"` |
| ✅ | 4 | `schema_embed_intro` | StringProse | `_intro` | body | `"The following JSON Schema defines your output structure. Every record you produce must validate against it."` |
| ✅ | 5 | `schema_reference_label_template` | StringTemplate | `_label_template` | body | `"Your output must conform to the JSON Schema at {{SCHEMA_PATH}}. You MUST read this schema and conform your output to it."` |
| ✅ | 6 | `directory_location_variant_template` | BaseModel | `_variant_template` | body | `{standard: "All output files are written under: {{OUTPUT_DIRECTORY}}", with_boundary: "Your output location is {{OUTPUT_DIRECTORY}}..."}` |

## Structure (OutputStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `schema_embed` | Boolean | `false` | gates schema_embed_intro + embedded schema block |
| ✅ | 2 | `directory_location_selector` | OutputDirectoryLocationSelector | `"standard"` | → selects key in content #6 |

## Display (OutputDisplay)

No display fields for this section in `display.toml`.

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "What You Produce"

PREAMBLE:
  ✅ schema_embed_intro                    "The following JSON Schema defines your output structure..."
                                             [visible: schema_embed = false → HIDDEN]
                                             [gate: only renders when schema_embed = true]

BODY:
  [SCALAR] description                     → interpolated into output_description_template
  [GATE] format                            → interpolated into format_template
  [GATE] name_known                        → GATE: drives name-related content selection
  [GATE] schema_embed                      → GATE: controls schema embedding

  ✅ output_description_template           "You produce: {{DESCRIPTION}}"
                                             interpolates .description
  ✅ format_template                       "Output format: {{FORMAT}}"
                                             interpolates .format

  [SCALAR] schema_path                     → interpolated into schema_reference_label_template (when present)
  ✅ schema_reference_label_template       "Your output must conform to the JSON Schema at {{SCHEMA_PATH}}..."
                                             [conditional: schema_path must be present]

  [SCALAR] output_directory                → interpolated into directory_location_variant_template
  ✅ directory_location_variant_template   {selector: "standard" → "All output files are written under: {{OUTPUT_DIRECTORY}}"}
                                             [conditional: output_directory must be present]

  ❌ output_file                           PathAbsolute scalar — no content template references it
  ❌ name_template                         FilenameTemplate scalar — no content template references it
  ❌ name_instruction                      StringProse scalar — no content template renders it
  ❌ name_known                            OutputNameKnown gate — controls name rendering but no content handles it

CLOSING:
  (none)
```

---

## Issues

### ❌ ISSUE 1: `output_file`, `name_template`, `name_instruction` have no content templates

Three data scalars are present in the model with no corresponding content templates. `name_instruction` for agent-builder contains a detailed multi-path output instruction that would be critical in a rendered prompt — but there is no content field with a suffix to render it through.

**Fix required:** Content templates needed. For `name_instruction` — a passthrough `_body` field or `_template`. For `name_template` and `output_file` — conditional content labels with appropriate templates.

### ❌ ISSUE 2: `name_known` gate has no rendering logic

`name_known` is an enum gate with values like `"unknown"`. It should control whether `name_template`, `name_instruction`, or neither renders. No structure toggle exists for this conditional and the engine has no logic to handle it.

**Fix required:** Structure visibility toggles linked to `name_known` value, or engine-side conditional rendering based on the gate.

### ⚠️ ISSUE 3: `schema_embed` gate needs engine support

Structure field `schema_embed = false` gates the `schema_embed_intro` and should also gate the rendering of an embedded schema block. The engine does not yet implement schema embedding.

### ⚠️ ISSUE 4: `directory_location_variant_template` needs conditional — only when `output_directory` present

The directory variant should only render when `output_directory` is present. The engine needs to check field presence before rendering optional-conditional content. Currently not implemented.
