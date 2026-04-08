# OUTPUT SECTION ANALYSIS — Surface B

## FIRST PRINCIPLES: What Does Output Accomplish?

The output section answers a single question the agent must resolve before it can do useful work: **What am I producing?**

This is distinct from every other section:
- **Instructions** tell the agent what to DO (process, transform, analyze).
- **Success/failure criteria** tell the agent what GOOD and BAD look like after the fact.
- **Writing_output** tells the agent HOW to physically write (tool, frequency, batch size).
- **Output** tells the agent what the DELIVERABLE IS — its shape, its location, its name, and whether its structure is specified or described.

Without output, the agent has a process with no artifact. It knows how to think but not what to emit. Output is the agent's mental model of its own product.

The critical design tension: output must be specific enough that the agent knows exactly what to produce, but must not bleed into HOW to produce it (that's instructions) or HOW to write it (that's writing_output). Output is a **specification of the artifact**, not a specification of the process.

---

## FIELD: description

TYPE: string (free-form prose)
VALUES: `"TOML definition file with include references, plus separate include files for instructions, examples, guardrails, and criteria"` / `"One contextual summary record per input exchange with exchange number and one-sentence summary"`

### What the agent needs to understand

Description is the agent's **mental image of what it is building**. Before format, before filename, before schema — the agent needs a plain-language understanding of the deliverable. This is the "elevator pitch" of the output: if you had to explain to someone what this agent produces in one sentence, this is it.

Agent 1's description is structurally complex — multiple files, a main file plus satellite files, with a specific relationship between them (include references). Agent 2's description is structurally simple — one record per input unit, with two named fields. The description carries **structural topology** (one file vs. many, flat vs. hierarchical) and **content preview** (what the records contain, what the files contain).

Description serves as the agent's **grounding anchor**. When instructions get complex and the agent is deep in processing, the description is what it returns to: "Am I producing the thing I'm supposed to produce?"

### Fragments

**output_description_frame**
- Alternative A: `"You will produce: {description}"`
- Alternative B: `"Your deliverable is {description}."`
- Alternative C: `"The output of your work is {description}."`
- Alternative D: `"What you are building: {description}"`
- PURPOSE: Establish the agent's mental model of its product before any structural details. This is the conceptual anchor.
- HYPOTHESIS: Framing as "you will produce" (future action) vs "your deliverable is" (noun definition) vs "what you are building" (active construction) may affect whether the agent treats output as a checklist item, a specification, or an ongoing creative target. Noun-definition framing ("your deliverable is") may produce more consistent structural adherence because it treats the output as a fixed specification rather than a suggestion.
- STABILITY: High. Every agent has a description. The frame is invariant across all agents. Only the interpolated content changes.

---

## FIELD: format

TYPE: string enum (observed: `"text"`, `"jsonl"`)
VALUES: `"text"` / `"jsonl"`

### What the agent needs to understand

Format tells the agent the **serialization contract** of its output. This is not cosmetic — it determines whether the output is machine-parseable, whether records are delimited, whether structure is enforced syntactically.

`"text"` means the agent is producing human-readable content where the structure is semantic, not syntactic. TOML, Markdown, prose — the format is loose and the agent has latitude in how it organizes content within files.

`"jsonl"` means the agent is producing machine-parseable records, one per line, where each line must be valid JSON conforming to a schema. The format is strict and the agent has zero latitude in serialization.

Format has a **cross-section dependency with writing_output**: the writing tool and write frequency must be compatible with the format. JSONL implies append-per-record semantics. Text implies write-once or write-and-replace semantics.

Format also has a **conditional relationship with schema**: JSONL outputs almost always have schemas. Text outputs rarely do (though they could). The presence of format="jsonl" raises the expectation of schema_path.

### Fragments

**output_format_declaration**
- Alternative A: `"Output format: {format}"`
- Alternative B: `"Each output must be valid {format}."`
- Alternative C: `"You are writing {format} output."`
- Alternative D: `"Format: {format}. Every record you emit must conform to this format."`
- PURPOSE: Establish the serialization contract. The agent must know that format is a hard constraint, not a suggestion.
- HYPOTHESIS: Terse declaration ("Output format: jsonl") may be sufficient for simple formats but insufficient for formats with implications (jsonl implies one-record-per-line, valid JSON per line, no trailing commas, no multi-line records). Explicit constraint language ("every record must conform") may reduce format violations at the cost of verbosity.
- STABILITY: High. Every agent has a format. The fragment is invariant; only the value changes.

**output_format_implications** (conditional: when format has non-obvious constraints)
- Alternative A: `"JSONL means one valid JSON object per line. No multi-line records. No trailing commas. No array wrappers."`
- Alternative B: `"Each line of your output file is an independent JSON object. Lines are separated by newlines. The file is not itself a JSON array."`
- Alternative C: `"Write one JSON object per line. Each line must parse independently as valid JSON."`
- PURPOSE: Disambiguate format semantics that agents frequently get wrong. LLMs are notorious for producing JSON arrays when JSONL is requested, or adding trailing commas.
- HYPOTHESIS: Explicit negation ("no array wrappers", "no trailing commas") may be more effective than positive-only description because it directly blocks the most common failure modes.
- STABILITY: Medium. Only needed for formats with non-obvious constraints. Text format probably needs no implications fragment. JSONL almost certainly does. Future formats (CSV, YAML) would each need their own.

---

## FIELD: name_known

TYPE: string enum — `"unknown"` | `"partially"` | `"known"`
VALUES: `"unknown"` / `"partially"`

### What the agent needs to understand

This is the **three-way branching pivot** of the output section. It determines the agent's cognitive relationship to filename determination:

- **`"unknown"`**: The agent must DECIDE the filename. This is a creative/judgment act. The agent needs guidance (name_instruction) but ultimately exercises discretion. It must understand naming conventions, the content it's producing, and the organizational scheme of the output directory.

- **`"partially"`**: The agent must FILL IN a template. This is a substitution act. The agent knows the pattern but must resolve placeholders from its input or context. It must identify what values go in the template slots.

- **`"known"`**: The agent writes to a FIXED filename. This is a mechanical act. No decision, no substitution — just write to the specified path. (Not observed in these two agents but implied by the enum.)

The cognitive load decreases dramatically from unknown → partially → known. An agent with name_known="unknown" must carry a filename-determination subtask throughout its entire execution. An agent with name_known="known" never thinks about filenames at all.

### Fragments

**name_known is not directly rendered** — it is a branch selector. The fragment that renders depends on its value. See STRUCTURAL: name_known_branch below.

---

## FIELD: name_instruction

TYPE: string (free-form prose)
CONDITIONAL: Only present when name_known = "unknown"
VALUES: `"Write the main definition to definitions/agents/{agent-name}.toml and include files to definitions/prompts/{agent-name}/."` / (absent)

### What the agent needs to understand

When the agent must determine its own output filenames, name_instruction provides the **naming policy**. This is not a template — it's prose guidance that the agent must interpret and apply to its specific situation.

Agent 1's name_instruction is notably complex: it specifies TWO output paths (main definition + include files), each in a different subdirectory, with {agent-name} as a contextual placeholder the agent resolves from its task. This is more than a naming convention — it's a **file topology instruction** embedded in the output section.

This raises a design question: does name_instruction belong here, or does the multi-file topology belong in instructions? The answer is that output specifies WHAT is produced and WHERE it goes. The multi-file structure is a property of the output, not the process. Instructions would say "decompose the definition into includes" — output says "the result is a main file here and include files there."

### Fragments

**name_instruction_frame**
- Alternative A: `"Determine the output filename(s) as follows: {name_instruction}"`
- Alternative B: `"You must decide where to write your output. {name_instruction}"`
- Alternative C: `"Output location is not predetermined. Follow this naming guidance: {name_instruction}"`
- Alternative D: `"File naming: {name_instruction}"`
- PURPOSE: Signal to the agent that filename determination is its responsibility, then provide the policy.
- HYPOTHESIS: Explicitly marking the filename as "not predetermined" (Alternative C) may be important for agents that default to asking for a filename or producing output to stdout. The agent needs to understand that filename determination is part of its job, not an unresolved ambiguity.
- STABILITY: Low-medium. Only appears for name_known="unknown" agents. The framing may need to vary based on whether the instruction specifies one file or multiple files.

---

## FIELD: name_template

TYPE: string (template with placeholders)
CONDITIONAL: Only present when name_known = "partially"
VALUES: (absent) / `"{interview-id}.summaries.jsonl"`

### What the agent needs to understand

When the agent has a template, it must perform **placeholder resolution** — identifying what value goes into each `{placeholder}` from its input context. The cognitive task is recognition and substitution, not creative decision-making.

The template also carries **naming convention information** implicitly. `{interview-id}.summaries.jsonl` tells the agent: the file is named after the interview, it's specifically summaries (not transcripts, not decompositions), and it's JSONL. The extension in the template should be consistent with the format field — this is a latent consistency check.

### Fragments

**name_template_frame**
- Alternative A: `"Output filename follows this template: {name_template}. Replace placeholders with values from your input context."`
- Alternative B: `"Write to: {name_template}, where {placeholder_list} are resolved from the input you receive."`
- Alternative C: `"Your output file is named by the pattern {name_template}. Resolve the placeholder(s) from context."`
- PURPOSE: Tell the agent to substitute, not invent. The template is authoritative; the agent fills slots.
- HYPOTHESIS: Explicitly naming the placeholders (Alternative B's {placeholder_list}) may reduce errors where the agent treats part of the literal filename as a placeholder or vice versa. But it requires extracting placeholder names from the template, which is a rendering-time computation.
- STABILITY: Medium. Only appears for name_known="partially" agents. The frame is stable but the need for placeholder enumeration may vary.

---

## FIELD: output_directory

TYPE: string (absolute path)
VALUES: `"/Users/johnny/.ai/spaces/bragi/definitions"` / `"/Users/johnny/.ai/spaces/bragi/interview/interviews"`

### What the agent needs to understand

Output_directory is the **root location** for the agent's deliverables. Combined with the filename (from name_instruction, name_template, or name_known="known"), this forms the complete output path.

This field has a **critical cross-section dependency** with the security boundary. The output_directory must fall within the workspace_path defined in the security section. If it doesn't, the agent would be instructed to write outside its security boundary — a configuration error, not a runtime decision.

For name_known="unknown" agents, output_directory constrains where the agent can create files. The agent doesn't get to write anywhere — only within this directory tree. For name_known="partially"/"known" agents, output_directory is combined with the resolved filename to produce the full path.

### Fragments

**output_directory_frame**
- Alternative A: `"Output directory: {output_directory}"`
- Alternative B: `"All output files are written under: {output_directory}"`
- Alternative C: `"Write your output to {output_directory}."`
- Alternative D: `"Your output location is {output_directory}. All files you create must be within this directory or its subdirectories."`
- PURPOSE: Establish the filesystem root for the agent's output. Combined with filename determination, this completes the "where does it go" specification.
- HYPOTHESIS: For name_known="unknown" agents, the boundary-enforcement framing (Alternative D: "must be within this directory or its subdirectories") may be important to prevent the agent from writing to arbitrary paths. For name_known="known"/"partially" agents, simple declaration is sufficient since the path is already determined.
- STABILITY: High. Every agent has an output_directory. The framing may vary slightly based on name_known value.

---

## FIELD: schema_path

TYPE: string (absolute path to JSON Schema file)
CONDITIONAL: Only present when the output has a schema
VALUES: (absent) / `"/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json"`

### What the agent needs to understand

Schema_path points to the **structural specification** of the output. When present, this is not advisory — it is the definitive contract for what each output record must contain and how fields must be typed.

The presence of a schema fundamentally changes the agent's output generation mode:
- **Without schema**: The agent works from description alone. It has latitude in structure. The description is the specification.
- **With schema**: The agent works from a formal specification. Every field, type, enum value, and required property is defined externally. The description becomes a summary; the schema is authoritative.

This creates a **specification hierarchy**: schema (when present) overrides description for structural details. Description provides semantic context that schema cannot (why fields exist, what they mean in context).

### Fragments

**schema_reference_frame**
- Alternative A: `"Your output must conform to the JSON Schema at: {schema_path}"`
- Alternative B: `"Output structure is defined by schema: {schema_path}. Every record you produce must validate against this schema."`
- Alternative C: `"A formal schema governs your output structure. Schema location: {schema_path}. Deviation from this schema is a failure condition."`
- PURPOSE: Establish the schema as authoritative and non-negotiable. The agent must understand that the schema is a hard constraint.
- HYPOTHESIS: Explicit failure-condition language (Alternative C) may reduce schema violations by framing deviation as failure rather than imprecision. However, this may overlap with success/failure criteria and should be coordinated to avoid redundancy.
- STABILITY: Medium. Only present for schema-bearing outputs. The frame is stable when present.

---

## FIELD: schema_embed

TYPE: boolean
CONDITIONAL: Only meaningful when schema_path is present
VALUES: (absent) / `true`

### What the agent needs to understand

Schema_embed controls whether the **schema content** appears inline in the agent's prompt or whether the agent only gets the path reference.

- **schema_embed = true**: The schema JSON is rendered directly into the prompt. The agent can see every field, type, constraint, and required property without needing to read the file. This is higher token cost but gives the agent immediate access to the specification.

- **schema_embed = false** (or absent): The agent gets only the path. It must read the schema file to know the exact specification, or work from the description alone and trust that its output will match.

This is a **prompt engineering tradeoff**: embedding increases prompt size but decreases the chance of schema violations because the agent has the specification in working memory. Not embedding saves tokens but adds a file-read step or increases violation risk.

### Fragments

**schema_embed_render** (conditional: schema_embed = true)
- Alternative A: `"The schema your output must conform to:\n\n{schema_content}"`
- Alternative B: `"Output schema (authoritative — all records must match):\n\n{schema_content}"`
- Alternative C: `"Here is the exact structure each output record must follow:\n\n{schema_content}\n\nEvery field marked 'required' must be present. Types must match exactly."`
- PURPOSE: When embedded, make the schema immediately visible and mark it as the authoritative specification.
- HYPOTHESIS: Adding interpretive guidance after the schema (Alternative C: "every field marked required must be present") may be redundant — the schema itself says this. But LLMs sometimes treat embedded JSON as "informational" rather than "normative," so explicit reinforcement may help. Testing needed.
- STABILITY: Medium. Only rendered when schema_embed=true. The framing question (how much interpretive guidance to add around raw schema) is a significant design decision.

**schema_path_only_render** (conditional: schema_embed = false or absent)
- Alternative A: `"Read the schema at {schema_path} before producing output."`
- Alternative B: `"Your output must conform to the schema defined at {schema_path}. Read this file to understand the required structure."`
- Alternative C: `"Schema reference: {schema_path}. You MUST read this schema and conform your output to it."`
- PURPOSE: When not embedded, ensure the agent knows it must actively read the schema rather than guessing at structure.
- HYPOTHESIS: Without embedding, there is a real risk the agent skips reading the schema and produces output based on description alone. Imperative language ("you MUST read") may be necessary to prevent this.
- STABILITY: Medium. Only rendered when schema exists but is not embedded. The strength of the "read this" directive is the key variable.

---

## STRUCTURAL: name_known_branch

This is the primary conditional structure in the output section. The value of name_known determines which filename-related fields appear and how they are framed.

### Branch Logic

```
if name_known == "unknown":
    render name_instruction_frame with name_instruction
elif name_known == "partially":
    render name_template_frame with name_template
elif name_known == "known":
    render name_known_frame with name_value (implied field, not observed)
```

### Fragments

**branch_unknown_composite**
- Alternative A: `"You determine the output filename(s). {name_instruction_frame}"`
- Alternative B: `"The output filename is not fixed — you must decide it based on the task. {name_instruction_frame}"`
- Alternative C: `"Output naming is your responsibility. {name_instruction_frame}"`
- PURPOSE: Frame the cognitive mode (you decide) before providing the naming policy.
- HYPOTHESIS: The "you decide" framing is important for agents that default to asking for clarification. It pre-empts uncertainty by making filename determination an explicit part of the agent's job description.
- STABILITY: Medium. Only for name_known="unknown" agents.

**branch_partially_composite**
- Alternative A: `"The output filename follows a template. {name_template_frame}"`
- Alternative B: `"Your output filename is derived from a pattern. {name_template_frame}"`
- Alternative C: `"Output filename: templated. {name_template_frame}"`
- PURPOSE: Frame the cognitive mode (fill in template) before providing the template.
- HYPOTHESIS: The "template" framing signals substitution, not invention. The agent should not deviate from the pattern — only resolve placeholders.
- STABILITY: Medium. Only for name_known="partially" agents.

**branch_known_composite** (inferred — not observed in data)
- Alternative A: `"The output filename is fixed: {name_value}"`
- Alternative B: `"Write to: {name_value}. This filename is exact and must not be modified."`
- Alternative C: `"Output file: {name_value}"`
- PURPOSE: Remove all ambiguity — the filename is determined, the agent just writes.
- HYPOTHESIS: Minimal framing is appropriate here. The agent has no decision to make. Over-explaining a fixed filename wastes tokens and may confuse.
- STABILITY: High (when it appears). The simplest branch.

---

## STRUCTURAL: schema_branch

The secondary conditional structure. Presence or absence of schema_path determines whether schema-related fragments render.

### Branch Logic

```
if schema_path exists:
    render schema_reference_frame
    if schema_embed == true:
        render schema_embed_render with schema_content
    else:
        render schema_path_only_render
else:
    (no schema fragments rendered)
    output structure is governed by description alone
```

### Fragments

**schema_absence_note** (conditional: no schema_path)
- Alternative A: (render nothing — absence is the default)
- Alternative B: `"Your output structure is defined by the description above. There is no formal schema."`
- Alternative C: `"No schema governs this output. Use the description as your structural guide."`
- PURPOSE: Should the absence of a schema be explicitly noted? Or is silence sufficient?
- HYPOTHESIS: For free-form text outputs, explicitly noting "no schema" may be unnecessary and even confusing. For structured outputs without schemas (if they exist), it might clarify that the agent has latitude. Silence is probably correct for text format; explicit noting may help for structured formats without schemas.
- STABILITY: Low. This is a design decision about whether to render anything at all. Likely resolved to "render nothing" for text formats.

---

## STRUCTURAL: output_section_ordering

The output section has a natural information hierarchy that determines rendering order.

### Ordering Logic

The agent needs information in this order:
1. **What am I producing?** (description) — conceptual anchor first
2. **What format?** (format + implications) — serialization contract
3. **Where does it go?** (output_directory) — filesystem root
4. **What's it called?** (name_known branch) — filename determination
5. **What's the exact structure?** (schema branch) — formal specification if present

This ordering follows a **zoom-in pattern**: concept → format → location → name → structure. Each step narrows the specification.

### Fragments

**output_section_header**
- Alternative A: `"## Output"`
- Alternative B: `"## What You Produce"`
- Alternative C: `"## Your Deliverable"`
- Alternative D: `"## Output Specification"`
- PURPOSE: Section header that frames the content. "Output" is terse and standard. "What You Produce" is agent-addressed and intentional. "Output Specification" is formal.
- HYPOTHESIS: Agent-addressed headers ("What You Produce") reinforce that this section is about the agent's responsibility, not just a data sheet. But consistency with other section headers matters more than individual optimization.
- STABILITY: High. Every agent has an output section. The header is invariant.

---

## CROSS-SECTION DEPENDENCIES

### output.format ↔ writing_output mechanics
The format field constrains what writing_output can specify. JSONL format implies append semantics, per-record writing, and line-delimited output. Text format implies write-once or full-file-replace semantics. The writing_output section must be compatible with the format declared here.

**Implication for rendering**: The output section should establish format before writing_output is rendered, so writing_output can reference the established format context.

### output.output_directory ↔ security_boundary.workspace_path
The output_directory must be within the security boundary. This is a validation constraint, not a rendering dependency — but if violated, it represents a configuration error that should be caught at build time, not runtime.

**Implication for rendering**: No direct rendering dependency. This is a build-time validation rule.

### output.schema_path ↔ success/failure criteria
Schema-bearing outputs typically have success criteria referencing schema compliance. The schema is defined in output; the requirement to comply is in success criteria. These must be consistent.

**Implication for rendering**: Success criteria should reference "the schema defined in the output section" rather than re-specifying the schema path, to avoid drift.

### output.name_known ↔ writing_output.file_path / writing_output.directory_path
The name determination strategy affects what writing_output knows about the target path. For name_known="known", writing_output can reference the exact file. For name_known="unknown", writing_output specifies the directory and the agent determines the file within it.

**Implication for rendering**: writing_output must be aware of the name_known value to correctly frame its path references.

### output.description ↔ instructions
The output description says WHAT is produced. Instructions say HOW to produce it. These must be complementary, not contradictory. If description says "one record per input exchange" and instructions say "batch all exchanges into a single summary," there's a conflict.

**Implication for rendering**: No direct rendering dependency, but a consistency validation opportunity.

---

## DESIGN TENSIONS AND OPEN QUESTIONS

### 1. Specification vs. Description framing
Should the output section be framed as a **specification** (formal, constraining, violation = failure) or a **description** (informative, guiding, deviation = acceptable)? Schema-bearing outputs naturally lean toward specification. Schema-absent outputs lean toward description. Should the framing adapt to schema presence?

### 2. Multi-file outputs in name_instruction
Agent 1's name_instruction specifies a multi-file topology. Is name_instruction the right place for this? Or should there be an explicit multi-file structure field? The current design overloads name_instruction with both naming policy AND file topology.

### 3. Schema embedding token cost
Schema_embed=true injects potentially large JSON into every prompt invocation. For batch agents processing hundreds of items, this cost is multiplied. Is the schema violation reduction worth the token cost? Could a middle ground exist (embed schema summary, reference for full schema)?

### 4. Format implications — render always or conditionally?
JSONL needs explicit implications (one object per line, no array wrapper). Text probably doesn't. Should format implications be conditional on format value, or always rendered? If conditional, the rendering logic needs format-specific knowledge.

### 5. The missing name_known="known" case
Neither example shows name_known="known". The design implies it exists (it's the simplest case: fixed filename, no agent decision). The fragments above are inferred. Real data would confirm or revise.
