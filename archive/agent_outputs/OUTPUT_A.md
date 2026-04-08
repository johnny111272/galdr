# OUTPUT SECTION — Control Surface Analysis

## SECTION PHILOSOPHY

The output section answers a single question the agent must internalize before it begins work: **What am I building?**

This is not the same as "what am I doing" (instructions), "what does good look like" (success criteria), or "how do I write it" (writing_output). The output section is the agent's mental model of its **deliverable as an artifact** — its shape, its location, its naming, its structural contract. An agent that deeply understands its output will make better decisions throughout its entire run, because every intermediate step is implicitly shaped by knowing what the end product must be.

The output section is the most heavily conditional section in the agent definition. The `name_known` three-way branch alone produces three fundamentally different section shapes. Add the optional schema fields and you get a section that can range from three fields (known name, no schema, simple format) to seven or more fields (unknown name with instruction, schema-validated, templated). This conditionality is not accidental — it reflects the genuine variance in what "output" means across different agent types.

---

## FIELD: description
TYPE: string (free prose)
VALUES: `"TOML definition file with include references, plus separate include files for instructions, examples, guardrails, and criteria"` / `"One contextual summary record per input exchange with exchange number and one-sentence summary"`

### What the agent needs to understand

This is the agent's primary mental model of what it produces. It must be concrete enough that the agent could describe its output to someone who has never seen one. The description is not a format specification — it is a conceptual portrait of the deliverable. The builder's description tells it "you produce a main file plus satellite files." The summarizer's description tells it "you produce one record per input unit with specific fields." Both descriptions carry structural information implicitly: the builder knows it produces multiple files, the summarizer knows it produces multiple records in one file.

The description field carries more weight when no schema is present. For the builder (no schema), the description IS the primary output specification. For the summarizer (schema present), the description is a human-readable summary that orients the agent before it encounters the formal schema. This asymmetry means the description must be self-sufficient for unschemaed agents and complementary for schemaed agents.

### Fragments

**output_description_framing**
- Alternative A: "You produce: {description}"
- Alternative B: "Your deliverable is {description}."
- Alternative C: "The output of your work is {description}."
- Alternative D: "What you are building: {description}"
- PURPOSE: Frame the description so the agent internalizes it as identity-level knowledge about its purpose, not just metadata it has been told. The framing verb matters — "produce" implies manufacturing, "deliverable" implies a handoff, "output" is neutral, "building" implies construction.
- HYPOTHESIS: "You produce" is the most direct and least ambiguous. "Your deliverable" adds a connotation of something being handed to a consumer, which may help agents that produce artifacts consumed by other agents. "What you are building" is the most identity-forming but may be too casual for batch-processing agents.
- STABILITY: HIGH. This is a simple frame around a variable. The description field itself varies wildly between agents, but the framing is stable.

**output_description_sufficiency_cue** (conditional: only when schema_path is absent)
- Alternative A: "This description is your complete output specification. There is no formal schema — use this description to determine the structure, content, and completeness of each output artifact."
- Alternative B: "No schema governs this output. The description above is your authoritative guide to what the output must contain and how it should be structured."
- Alternative C: "Your output is description-driven, not schema-driven. The description above defines what complete and correct output looks like."
- PURPOSE: When no schema exists, the agent must understand that the description is load-bearing — it is not a casual summary but the primary specification. Without this cue, agents may treat the description as optional context and hallucinate structure.
- HYPOTHESIS: Making the absence of schema explicit (Alternative B) is more informative than just elevating the description (Alternative A). The agent needs to know BOTH that there is no schema AND that the description fills that role. Alternative C introduces vocabulary ("description-driven vs schema-driven") that may help the agent categorize its output behavior.
- STABILITY: MEDIUM. This fragment exists only for unschemaed agents. Its necessity depends on whether schema absence is common or rare across the agent population.

---

## FIELD: format
TYPE: string enum
VALUES: `"text"` / `"jsonl"`

### What the agent needs to understand

The format tells the agent the structural grammar of its output. "text" means the agent produces human-readable content with agent-determined internal structure. "jsonl" means the agent produces machine-parseable records, one per line, conforming to a predictable shape. This distinction affects everything: how the agent thinks about completeness (all sections present vs all records emitted), how it handles errors (malformed prose vs invalid JSON), and how it relates to downstream consumers (humans reading vs pipelines parsing).

Format also creates expectations about atomicity. A text output is typically one conceptual unit (a document, a definition file). A jsonl output is typically many atomic records. This affects how the agent thinks about progress and partial output.

### Fragments

**output_format_declaration**
- Alternative A: "Output format: {format}"
- Alternative B: "You write {format} output."
- Alternative C: "Your output is formatted as {format}."
- PURPOSE: Declare the format so the agent knows the grammar it must conform to. This is mechanical but foundational — every output decision flows through format awareness.
- HYPOTHESIS: The terse label style (Alternative A) may be sufficient since format is a simple enum. The sentence styles (B, C) integrate format into the agent's self-model. For a control surface that will be rendered into prose, B or C fit more naturally.
- STABILITY: HIGH. Format is a simple declaration. The only variance is the enum value itself.

**output_format_implication** (conditional: varies by format value)
- For `text`:
  - Alternative A: "Your output is free-form text. You determine the internal structure based on your instructions and the nature of the content."
  - Alternative B: "Text output means you control the structure. Organize the content as the task requires — the format imposes no structural constraints beyond what your instructions specify."
  - Alternative C: "As a text-format output, your deliverable is a document whose internal organization you design."
- For `jsonl`:
  - Alternative A: "Your output is JSONL — one JSON object per line. Each line must be a complete, valid JSON object. Do not emit partial records or multi-line JSON."
  - Alternative B: "JSONL format: each output record is a self-contained JSON object on its own line. Every line must parse independently."
  - Alternative C: "You produce newline-delimited JSON. Each line is one record. Records must be valid JSON — no trailing commas, no comments, no multi-line formatting."
- PURPOSE: The format name alone ("text", "jsonl") is not enough. The agent needs to understand what the format MEANS for its behavior. Text agents need to know they have structural freedom. JSONL agents need to know about line-level atomicity and validity.
- HYPOTHESIS: For JSONL, being explicit about per-line validity (Alternative A or C) prevents the most common failure mode: agents that emit pretty-printed JSON instead of single-line records. For text, the key insight is that the agent has structural authority (Alternative B communicates this most clearly).
- STABILITY: MEDIUM-HIGH. The format-specific implications are stable per format value, but the set of supported formats may expand (json, toml, csv, markdown).

---

## FIELD: name_known
TYPE: string enum ("unknown" | "partially" | "known")
VALUES: `"unknown"` / `"partially"`

### What the agent needs to understand

This is the section's primary branch point. `name_known` determines how the agent relates to its output filename — whether it must invent it, fill in a template, or simply use a fixed name. Each branch creates a fundamentally different cognitive experience:

- **unknown**: The agent must determine the output filename at runtime based on its understanding of the task. This requires judgment. The agent must read `name_instruction` to understand the naming convention, then apply it to the specific input. This is the highest-autonomy branch.
- **partially**: The agent receives a template with placeholders. It must extract values from its context to fill the template. This requires pattern matching — understanding what `{interview-id}` refers to in the input data. This is medium autonomy.
- **known**: The filename is fixed. The agent writes to exactly this file. Zero naming autonomy. This is the simplest branch but may not appear in the current data.

The branch also affects error modes: an "unknown" agent can produce badly-named files, a "partially" agent can fill templates incorrectly, a "known" agent cannot get the name wrong.

### Fragments

**output_naming_branch_unknown**
- Alternative A: "You determine the output filename. {name_instruction}"
- Alternative B: "The output filename is not predetermined — you must derive it from the task context. Naming guidance: {name_instruction}"
- Alternative C: "Output naming is your responsibility. Follow this convention: {name_instruction}"
- PURPOSE: Tell the agent it has naming authority and give it the convention to follow. The agent must understand this is a creative/judgmental act, not a mechanical one.
- HYPOTHESIS: Alternative B is most informative — it explains WHY the agent is naming (not predetermined) and frames the instruction as guidance rather than a rigid rule. Alternative C is most directive, which may be better for agents that should not get creative with naming.
- STABILITY: HIGH within this branch. The instruction content varies but the frame is stable.

**output_naming_branch_partial**
- Alternative A: "Output filename template: `{name_template}`. Replace placeholders with values from your input context."
- Alternative B: "Your output filename follows the pattern `{name_template}`. Fill in the bracketed placeholders using the corresponding values from your input data."
- Alternative C: "Name your output file by applying this template: `{name_template}`. Each `{placeholder}` corresponds to a field in your input — substitute the actual values."
- PURPOSE: Give the agent a template and tell it how to use it. The agent must understand that placeholders are not literal — they must be resolved from context.
- HYPOTHESIS: Being explicit about what placeholders mean (Alternative B: "bracketed placeholders" + "corresponding values") reduces the risk of agents treating the template as a literal filename. Alternative C's "substitute the actual values" is the most unambiguous instruction.
- STABILITY: HIGH within this branch. Template syntax is stable; only the template content varies.

**output_naming_branch_known** (hypothetical — not in current data)
- Alternative A: "Output filename: `{name_literal}`. Write to exactly this file."
- Alternative B: "Your output file is `{name_literal}`. This name is fixed — do not modify it."
- Alternative C: "Write your output to `{name_literal}` — this is the exact filename, not a template."
- PURPOSE: Remove all ambiguity. The agent writes to this file, period. The "not a template" clarification (Alternative C) prevents agents from looking for placeholders that don't exist.
- HYPOTHESIS: The simplest branch needs the least prose. Alternative A is sufficient. Alternative C adds value if agents have been trained on enough template examples that they might misinterpret a literal name.
- STABILITY: HIGH. This is the most stable branch — it's just a constant.

---

## FIELD: name_instruction
TYPE: string (free prose, conditional on name_known="unknown")
VALUES: `"Write the main definition to definitions/agents/{agent-name}.toml and include files to definitions/prompts/{agent-name}/."` / absent

### What the agent needs to understand

This is the naming convention the agent must follow when it determines filenames at runtime. It is inherently more complex than a template because it may describe multiple output files, directory structures, and naming patterns that require interpretation. The builder's instruction describes a main file PLUS satellite files in a different directory — the agent must understand it produces a file tree, not a single file.

The instruction is prose, not a formal pattern. This means the agent must parse natural language to understand the naming convention. This is deliberate — the naming logic for "unknown" agents is often too complex for a simple template.

### Fragments

This field is consumed directly by the naming branch fragment above. It does not need its own framing — it IS the content that the branch fragment wraps. The branch fragment provides the frame; this field provides the substance.

**No additional fragments needed.** The `output_naming_branch_unknown` fragment already incorporates `{name_instruction}` by reference.

### Cross-section dependency

- Depends on `name_known = "unknown"` — this field is ONLY present when the agent determines naming.
- The instruction may reference paths relative to `output_directory`, creating an implicit dependency on that field.
- The instruction may describe multiple files, which interacts with `writing_output` mechanics (how does the agent write multiple files using its output tool?).

---

## FIELD: name_template
TYPE: string (template with placeholders, conditional on name_known="partially")
VALUES: absent / `"{interview-id}.summaries.jsonl"`

### What the agent needs to understand

The template is a filename pattern with `{placeholder}` tokens that the agent must resolve from its input context. The agent needs to understand two things: (1) the syntactic convention (`{...}` means "replace this"), and (2) where to find the replacement values (input data, context, task parameters).

The template also implicitly communicates output structure. `{interview-id}.summaries.jsonl` tells the agent that there is one output file per interview, that the file contains summaries, and that it is JSONL format (reinforcing the `format` field).

### Fragments

Consumed by `output_naming_branch_partial` above. The template itself is the variable content; the branch fragment provides the frame.

### Cross-section dependency

- Depends on `name_known = "partially"`.
- Placeholder values must exist in the agent's input context. This creates a dependency on the `input` section — whatever `{interview-id}` is, the input section must make it available.
- The resolved template combines with `output_directory` to form the full output path.

---

## FIELD: output_directory
TYPE: string (absolute path)
VALUES: `"/Users/johnny/.ai/spaces/bragi/definitions"` / `"/Users/johnny/.ai/spaces/bragi/interview/interviews"`

### What the agent needs to understand

This is the root directory where all output goes. Combined with the resolved filename (from whichever naming branch applies), it forms the complete output path. The agent must understand that this directory is its designated output location — it should not write files outside this directory unless explicitly instructed.

The output directory also implicitly communicates the agent's role in the larger system. Writing to `definitions/` means you are producing definitions. Writing to `interview/interviews/` means you are producing interview artifacts. The path is informational as well as functional.

### Fragments

**output_directory_declaration**
- Alternative A: "Output directory: `{output_directory}`"
- Alternative B: "Write your output to `{output_directory}`."
- Alternative C: "Your output files go in `{output_directory}`. All filenames are relative to this directory."
- Alternative D: "Base output path: `{output_directory}`. Combine this with your output filename to determine the full path."
- PURPOSE: Tell the agent where to write. The key nuance is whether to be explicit about the directory being a base that combines with the filename (Alternative C, D) or to treat it as a simple location (A, B).
- HYPOTHESIS: Alternative C is the most useful — it both declares the directory AND clarifies the relationship between directory and filename. Alternative D is more mechanical but makes the composition explicit. For agents that produce multiple files in subdirectories (like the builder), the "relative to this directory" framing (Alternative C) is essential.
- STABILITY: HIGH. The declaration frame is stable; only the path value varies.

### Cross-section dependency

- Must be within `security_boundary.workspace_path`. The output directory is the agent's permitted write zone. If the security boundary restricts writes to a specific subtree, the output directory must be within it.
- Interacts with `name_instruction` (unknown branch) — the instruction may describe subdirectory structure relative to this directory.
- Interacts with `writing_output.tool_invocation` — the writing tool must be configured to write to paths within this directory.

---

## FIELD: schema_path
TYPE: string (absolute file path, conditional on schema validation being required)
VALUES: absent / `"/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json"`

### What the agent needs to understand

When present, this tells the agent that its output has a formal structural contract — a JSON Schema that defines exactly what valid output looks like. The agent must understand that its output will be validated against this schema, and non-conforming output is a failure.

The path itself may or may not be useful to the agent depending on `schema_embed`. If the schema is embedded in the prompt, the path is informational (the agent knows where the schema lives but doesn't need to read it). If the schema is not embedded, the path tells the agent where to find the schema if it has file-reading capabilities.

### Fragments

**output_schema_reference** (conditional: schema_path present, schema_embed=false or absent)
- Alternative A: "Your output must conform to the JSON Schema at `{schema_path}`."
- Alternative B: "Output is validated against `{schema_path}`. Read this schema to understand the required structure."
- Alternative C: "A JSON Schema governs your output format: `{schema_path}`. Your output must validate against this schema."
- PURPOSE: Tell the agent a schema exists and its output must conform. When the schema is not embedded, the path is the agent's primary reference.
- HYPOTHESIS: Alternative B is most actionable — it tells the agent to read the schema, which is what it should do when the schema is not embedded. Alternative A is a constraint statement; Alternative C is a governance statement. The right choice depends on whether the agent can actually read files.
- STABILITY: MEDIUM. This fragment only appears when schema exists but is not embedded — a specific conditional combination.

**output_schema_embedded_header** (conditional: schema_path present, schema_embed=true)
- Alternative A: "Your output must conform to this schema (source: `{schema_path}`):"
- Alternative B: "The following JSON Schema defines your output structure. Every record you produce must validate against it."
- Alternative C: "Output schema — your structural contract:"
- PURPOSE: Introduce the embedded schema content. The agent is about to see the actual schema; this fragment frames it. The source path (Alternative A) is informational — it tells the agent where the schema lives on disk even though the content is right here.
- HYPOTHESIS: Alternative B is the most informative — it names what the thing is (JSON Schema), what it defines (output structure), and what the constraint is (every record must validate). Alternative C is the tersest and treats the schema as self-explanatory. Alternative A preserves provenance.
- STABILITY: MEDIUM. Only appears when schema is both present and embedded.

---

## FIELD: schema_embed
TYPE: boolean
VALUES: absent / `true`

### What the agent needs to understand

This field is a rendering directive, not an agent-facing field. The agent never sees `schema_embed = true` — it sees either the embedded schema content or a path reference. The field controls which fragment is used during prompt rendering: if true, the schema content is included in the prompt; if false or absent, only the path is referenced.

### Fragments

**No agent-facing fragments.** This is a rendering-time control field. It determines which of the two schema fragments above (`output_schema_reference` vs `output_schema_embedded_header` + schema content) appears in the rendered prompt. The agent experiences the RESULT of this field, not the field itself.

### Rendering logic

```
if schema_path exists:
    if schema_embed == true:
        render output_schema_embedded_header
        render schema content (read from schema_path)
    else:
        render output_schema_reference
else:
    render nothing (or output_description_sufficiency_cue)
```

---

## STRUCTURAL: output_section_opening

### What the agent needs to understand

The output section needs an opening that shifts the agent's attention from "what am I doing" to "what am I producing." This transition is important because the output section is where the agent forms its mental model of its deliverable — and this model should be established early and firmly.

### Fragments

**output_section_header**
- Alternative A: "## What You Produce"
- Alternative B: "## Output Specification"
- Alternative C: "## Your Deliverable"
- Alternative D: "## Output"
- PURPOSE: Signal that we are now talking about the artifact the agent creates. The header sets tone: "What You Produce" is conversational and agent-centered, "Output Specification" is formal and document-like, "Your Deliverable" is personal and responsibility-oriented, "Output" is minimal.
- HYPOTHESIS: "What You Produce" (Alternative A) best frames the section as identity-level knowledge. "Output Specification" (Alternative B) is better for schema-heavy agents where the section is genuinely a spec. The right choice may depend on the agent's formality level.
- STABILITY: HIGH. This is a static structural element.

---

## STRUCTURAL: output_section_assembly_order

### What the agent needs to understand

The order in which output information is presented affects comprehension. The agent should first understand WHAT it produces (description), then WHERE it goes (directory + naming), then what STRUCTURAL CONTRACT governs it (schema, if any).

### Recommended assembly order

1. **Section header** — `output_section_header`
2. **Description** — `output_description_framing` with the description value
3. **Format** — `output_format_declaration` + `output_format_implication`
4. **Directory** — `output_directory_declaration`
5. **Naming** — appropriate `output_naming_branch_*` based on `name_known`
6. **Schema** (conditional) — `output_schema_reference` OR (`output_schema_embedded_header` + schema content)
7. **Description sufficiency cue** (conditional) — `output_description_sufficiency_cue` if no schema

### Rationale

The assembly order follows a narrative arc: what is it → what format → where does it go → what's it called → what must it conform to. This mirrors how a person would think about creating a deliverable: understand the thing, then understand the logistics, then understand the constraints.

Schema comes last because it is the most detailed element and should not interrupt the higher-level orientation. The description sufficiency cue is an alternative to schema — it occupies the same "structural contract" slot but communicates absence rather than presence.

---

## STRUCTURAL: conditional_branching_map

### Complete conditional logic for the output section

```
ALWAYS PRESENT:
  - description
  - format
  - output_directory
  - name_known

CONDITIONAL ON name_known:
  "unknown"   → name_instruction (required)
  "partially" → name_template (required)
  "known"     → name_literal (required, hypothesized — not in current data)

CONDITIONAL ON schema presence:
  schema_path present + schema_embed true  → embedded schema rendering
  schema_path present + schema_embed false → path reference rendering
  schema_path absent                       → description sufficiency cue

FRAGMENT SELECTION:
  output_naming_branch_{name_known value}
  output_schema_reference | output_schema_embedded_header | output_description_sufficiency_cue
```

### Cross-section dependencies (complete)

| This field | Depends on | Nature of dependency |
|---|---|---|
| `output_directory` | `security_boundary.workspace_path` | Must be within permitted write zone |
| `name_instruction` | `output_directory` | Paths in instruction are relative to directory |
| `name_template` | Input section fields | Placeholder values come from input context |
| `schema_path` | Schema files on disk | Schema must exist at this path for validation and embedding |
| `format` | `writing_output` section | Format determines applicable writing mechanics |
| `output_directory` | `writing_output.tool_invocation` | Writing tool must target this directory |
| `name_known` | Agent autonomy level | Unknown = high autonomy agents, known = constrained agents |
| `description` | `format` | Description should be consistent with declared format |

---

## STRUCTURAL: output_vs_writing_output_boundary

### The distinction that must be maintained

The **output** section answers: "What is the artifact?"
The **writing_output** section answers: "How do you physically write it?"

This boundary is critical and must not blur. The output section should never mention tool invocations, batch sizes, or write frequencies. The writing_output section should never redefine what the output IS — only how it gets written to disk.

**Where they connect:** The output section establishes format and location. The writing_output section provides the mechanics to realize that format at that location. The connection point is:
- `output.format` → `writing_output` knows what kind of data it is writing
- `output.output_directory` + resolved name → `writing_output.tool_invocation` targets this path
- `output.schema_path` → `writing_output` may invoke validated-write tools that check against this schema

**Fragments for this boundary:** None needed in the output section itself. The boundary is maintained by what the output section does NOT say, not by what it does say. The writing_output section may include a forward-reference ("Write your output as described above using...") but the output section should not reference writing mechanics.

---

## OPEN QUESTIONS

1. **Should `format` expand beyond text/jsonl?** Current data shows two values. Are there agents that produce `json` (single object), `toml`, `csv`, or `markdown`? Each would need its own `output_format_implication` fragment.

2. **Is `name_known = "known"` actually used?** The current data only shows `unknown` and `partially`. If `known` exists, it is the simplest branch. If it does not exist, the enum may effectively be binary.

3. **Multi-file output in the "unknown" branch.** The builder's `name_instruction` describes multiple files in multiple directories. How does this interact with `output_directory`? Is the directory a common ancestor, or does the instruction override it? This ambiguity needs resolution.

4. **Schema embedding mechanics.** When `schema_embed = true`, who reads the schema file and injects its content? This is a rendering-time concern, not an agent concern, but it affects how the prompt composition system works.

5. **Relationship between `description` and `schema`.** When both exist, do they ever conflict? The description says "one contextual summary record per input exchange" — does the schema enforce the one-per-exchange cardinality, or only the record structure? If the schema only validates structure, the description carries additional behavioral constraints that the schema cannot enforce.
