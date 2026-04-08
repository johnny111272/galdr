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
| ✅ | 1 | `heading` | StringText | `heading` | heading | `"What You Produce"` |
| ✅ | 2 | `output_description_declaration` | StringTemplate | `_declaration` | body | `"You produce: {{DESCRIPTION}}"` |
| ✅ | 3 | `format_declaration` | StringTemplate | `_declaration` | body | `"Output format: {{FORMAT}}"` |
| ✅ | 4 | `schema_embedded_preamble` | StringProse | `_preamble` | preamble | `"The following JSON Schema defines your output structure. Every record you produce must validate against it."` |
| ✅ | 5 | `schema_reference_label` | StringTemplate | `_label` | body | `"Your output must conform to the JSON Schema at {{SCHEMA_PATH}}. You MUST read this schema and conform your output to it."` |
| ✅ | 6 | `directory_location_b_variant` | BaseModel | `_b_variant` | body | `{standard: "All output files are written under: {{OUTPUT_DIRECTORY}}", with_boundary: "Your output location is {{OUTPUT_DIRECTORY}}..."}` |

## Structure (OutputStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `schema_embed` | Boolean | `false` | gates schema_embedded_preamble + embedded schema block |
| ✅ | 2 | `directory_location_b_variant` | OutputDirectoryLocationBVariant | `"standard"` | → selects key in content #6 |

## Display (OutputDisplay)

No display fields for this section in `display.toml`.

---

## Rendering Order

```
HEADING:
  ✅ heading                               "What You Produce"

PREAMBLE:
  ✅ schema_embedded_preamble              "The following JSON Schema defines your output structure..."
                                             [visible: schema_embed = false → HIDDEN]
                                             [gate: only renders when schema_embed = true]

BODY:
  [SCALAR] description                     → interpolated into output_description_declaration
  [GATE] format                            → interpolated into format_declaration
  [GATE] name_known                        → GATE: drives name-related content selection
  [GATE] schema_embed                      → GATE: controls schema embedding

  ✅ output_description_declaration        "You produce: {{DESCRIPTION}}"
                                             interpolates .description
  ✅ format_declaration                    "Output format: {{FORMAT}}"
                                             interpolates .format

  [SCALAR] schema_path                     → interpolated into schema_reference_label (when present)
  ✅ schema_reference_label                "Your output must conform to the JSON Schema at {{SCHEMA_PATH}}..."
                                             [conditional: schema_path must be present]

  [SCALAR] output_directory                → interpolated into directory_location_b_variant
  ✅ directory_location_b_variant          {variant: "standard" → "All output files are written under: {{OUTPUT_DIRECTORY}}"}
                                             [conditional: output_directory must be present]

  ❌ output_file                           PathAbsolute scalar — no content template references it
  ❌ name_template                         FilenameTemplate scalar — no content template references it
  ❌ name_instruction                      StringProse scalar — no content template references it
  ❌ name_known                            OutputNameKnown gate — controls name rendering but no content handles it

CLOSING:
  (none)
```

---

## Issues

### ❌ ISSUE 1: `output_file`, `name_template`, `name_instruction` have no content templates

Three data scalars are present in the model with no corresponding content templates. `name_instruction` for agent-builder contains a detailed multi-path output instruction that would be critical in a rendered prompt — but there is no content field with a suffix to render it through.

**Fix required:** Content templates needed. For `name_instruction` — a passthrough `_body` field or `_declaration` template. For `name_template` and `output_file` — conditional content labels with appropriate templates.

### ❌ ISSUE 2: `name_known` gate has no rendering logic

`name_known` is an enum gate with values like `"unknown"`. It should control whether `name_template`, `name_instruction`, or neither renders. No structure toggle exists for this conditional and the engine has no logic to handle it.

**Fix required:** Structure visibility toggles linked to `name_known` value, or engine-side conditional rendering based on the gate.

### ⚠️ ISSUE 3: `schema_embed` gate needs engine support

Structure field `schema_embed = false` gates the `schema_embedded_preamble` and should also gate the rendering of an embedded schema block. The engine does not yet implement schema embedding.

### ⚠️ ISSUE 4: `directory_location_b_variant` needs conditional — only when `output_directory` present

The directory variant should only render when `output_directory` is present. The engine needs to check field presence before rendering optional-conditional content. Currently not implemented.

---

## Renames Needed

### Template suffix (`_template` as final suffix)

- `output_description_declaration` → `output_description_declaration_template` — contains `{{DESCRIPTION}}`
- `format_declaration` → `format_declaration_template` — contains `{{FORMAT}}`
- `schema_reference_label` → `schema_reference_label_template` — contains `{{SCHEMA_PATH}}`

### Variant templates (at least one alternative contains `{{...}}`)

- `directory_location_b_variant` → `directory_location_b_variant_template` — both alternatives contain `{{OUTPUT_DIRECTORY}}`

### Variant naming (`_variant` as modifier, `_selector` in structure)

Content: drop slot letter from `_x_variant` — the positional suffix before `_variant` determines the slot.

- `directory_location_b_variant` → `directory_location_declaration_variant` — drop `_b`, add `_declaration` (bare `directory_location` has no recognized positional suffix); also has `_template` from above, so combined rename is `directory_location_declaration_variant_template`

Structure: rename `_variant` selectors to `_selector`. Selector trunk matches the shared trunk across all content variant fields for this choice (only one variant field here, so trunk = content trunk `directory_location`).

- `directory_location_b_variant` → `directory_location_selector`
