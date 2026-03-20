# OUTPUT — TOML Extraction

## structure.toml

```toml
[output]
# Variant selectors
schema_embed = false                       # true = inline schema content; false = path reference only
```

**Decisions:**

- `schema_embed`: Build-time rendering directive (agent never sees it). Selects inline schema vs path reference.

## content.toml

```toml
[output]
heading = "What You Produce"

output_description = "You produce: {{DESCRIPTION}}"

format_declaration = "Output format: {{FORMAT}}"

directory_location = "All output files are written under: {{OUTPUT_DIRECTORY}}"
directory_location_with_boundary = "Your output location is {{OUTPUT_DIRECTORY}}. All files you create must be within this directory or its subdirectories."

schema_embedded_preamble = "The following JSON Schema defines your output structure. Every record you produce must validate against it."
schema_reference = "Your output must conform to the JSON Schema at {{SCHEMA_PATH}}. You MUST read this schema and conform your output to it."
```

**Decisions:**

- `directory_location` vs `directory_location_with_boundary`: Two variants for different autonomy levels. Standard for most agents, boundary enforcement for high-autonomy agents. Selection mechanism TBD.
- `schema_reference`: Imperative "MUST read" — without embedding, agents demonstrably skip schema reading and work from description alone.
- `schema_embedded_preamble`: "must validate against it" — LLMs sometimes treat embedded JSON as informational.

## display.toml

```toml
[output]
# No display knobs for this section.
```

## Excluded (invariant rules / bare data)

- **Assembly order**: description → format → directory → schema. Invariant.
- **Output vs writing_output boundary**: Output describes what is produced and where. Writing_output describes how (tool, invocation, naming, batching). Code-enforced.
