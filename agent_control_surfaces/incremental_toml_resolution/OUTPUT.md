# OUTPUT — TOML Extraction

## structure.toml

```toml
[output]
# Always-present toggles
no_schema_description_is_authoritative_visible = false   # true = render cue when no schema exists

# Variant selectors
name_known = "unknown"                     # "unknown" | "partially" | "known"
schema_embed = false                       # true = inline schema content; false = path reference only
```

**Decisions:**

- `name_known`: Primary branching axis — selects naming fragment and modulates directory framing intensity.
- `schema_embed`: Build-time rendering directive (agent never sees it). Selects inline schema vs path reference.

## content.toml

```toml
[output]
heading = "What You Produce"

output_description = "You produce: {{DESCRIPTION}}"
no_schema_description_is_authoritative = "No schema governs this output. The description above is your authoritative guide to structure and content."

format_declaration = "Output format: {{FORMAT}}"

directory_location = "All output files are written under: {{OUTPUT_DIRECTORY}}"
directory_location_with_boundary = "Your output location is {{OUTPUT_DIRECTORY}}. All files you create must be within this directory or its subdirectories."

naming_unknown = "The output filename is not predetermined — you must derive it from the task context. Naming guidance: {{NAME_INSTRUCTION}}"
naming_partial = "Your output filename follows the pattern {{NAME_TEMPLATE}}. Fill in the bracketed placeholders using the corresponding values from your input data."
naming_known = "Output filename: {{NAME_LITERAL}}. Write to exactly this file."

schema_embedded_preamble = "The following JSON Schema defines your output structure. Every record you produce must validate against it."
schema_reference = "Your output must conform to the JSON Schema at {{SCHEMA_PATH}}. You MUST read this schema and conform your output to it."

# Format-specific behavioral implications (keyed by format data value)
format_implications_jsonl = "JSONL means one valid JSON object per line. No multi-line records. No trailing commas. No array wrappers."
format_implications_text = "Text output means you control the structure. Organize the content as the task requires."
```

**Decisions:**

- `directory_location` vs `directory_location_with_boundary`: Code selects by `name_known`. "partially"/"known" gets standard (implied containment). "unknown" gets boundary enforcement (high-autonomy agents).
- `schema_reference`: Imperative "MUST read" — without embedding, agents demonstrably skip schema reading and work from description alone.
- `schema_embedded_preamble`: "must validate against it" — LLMs sometimes treat embedded JSON as informational.

## display.toml

```toml
[output]
# No display knobs identified for this section.
# Format implications moved to content.toml (they are behavioral prose, not format selectors).
# No threshold tuples needed. Output section has no count-dependent formatting.
# No joiner strings needed. Fragments are sequentially rendered, not list-joined.
```

## Excluded (invariant rules / bare data)

- **Assembly order**: description → format → directory → naming → schema. Invariant.
- **Output vs writing_output boundary**: Output never mentions tools, batch sizes, write frequency. Code-enforced.
