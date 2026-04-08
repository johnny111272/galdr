# INPUT Section Analysis — Control Surface Design

## EXECUTIVE FRAME

The `input` section answers the agent's foundational question: **Where does my work come from?** It configures the agent's mental model of provenance — not what to do (that is execution), not what to produce (that is output), but what arrives at the threshold before work begins.

This section has two fundamentally different concerns masquerading as one block:

1. **The payload** — the data stream the agent processes (delivery, format, description, parameters)
2. **The preparation** — the knowledge the agent must absorb before touching the payload (context_required)

These are not the same thing. The payload is the assembly line. The preparation is the training the worker received before stepping onto the floor. Collapsing them into a single `[input]` block is an implementation convenience that the rendering layer must carefully decompose.

---

## TOP-LEVEL FIELDS

---

## FIELD: delivery
TYPE: string (enum-like)
OPTIONAL: no (present in both agents)
VALUES: "tempfile" / "tempfile"

### What the agent needs to understand

Delivery tells the agent the transport mechanism — HOW the data physically arrives. "tempfile" means a file on disk at a path that will be provided as a parameter. This is not about content; it is about logistics. The agent needs to know it will be reading from a file, not receiving inline content, not pulling from an API, not reading from stdin.

The behavioral implication is concrete: the agent must expect a file path, must read that file, and must not assume the file persists after the session. "Tempfile" carries the connotation of ephemerality — this was prepared for you, use it now, it will not be here tomorrow.

### Fragments

**delivery_mechanism**
- Alternative A: "Your input arrives as a temporary file. You will receive a file path — read it, process it, and do not assume it persists beyond this session."
- Alternative B: "Work material is delivered via tempfile. A path parameter points to this file. Read it as your primary data source."
- Alternative C: "You receive your input through a temporary file on disk. The file path is provided as a parameter at invocation."
- Alternative D: "A tempfile has been prepared containing your input data. You will be given its path. This file is ephemeral — it exists for this task only."
- PURPOSE: Establish the physical contract — the agent reads from a file at a given path.
- HYPOTHESIS: Delivery is likely always "tempfile" in the current system. If other delivery mechanisms emerge (inline, streaming, multi-file), this field becomes a dispatch point for very different behavioral framing. For now, it may be safe to treat as near-constant.
- STABILITY: Medium-high. The value is stable across both agents, but the field itself is architecturally load-bearing — if new delivery types appear, every fragment here changes fundamentally.

### Cross-section dependencies
- Links to `parameters` — the tempfile delivery implies at least one parameter of type "path" that points to the file.
- Links to `output.processing` — the delivery mechanism may mirror the output mechanism (tempfile in, file out).

---

## FIELD: description
TYPE: string (free text)
OPTIONAL: no (present in both agents)
VALUES: "Preparation package containing requirements, domain analysis, data shapes, and schema references" / "Stripped interview exchanges with exchange number, agent question, and user response — no learned, threads, or insight fields"

### What the agent needs to understand

Description is the agent's first mental model of what it will encounter. Before the agent reads a single byte of input, this field tells it what to expect — the shape, the content, the scope. It functions as a preview that calibrates expectations.

Notice the radical difference between the two agents: the builder's description is abstract and composite ("preparation package containing..."), while the summarizer's is concrete and structural ("stripped interview exchanges with exchange number, agent question, and user response"). The builder expects a heterogeneous bundle. The summarizer expects a homogeneous stream of records with known fields.

The description also carries negative information in the summarizer's case: "no learned, threads, or insight fields." This tells the agent what has been removed — what NOT to expect or look for. This is a critical behavioral cue: the absence is intentional, and the agent should not treat missing fields as errors.

### Fragments

**input_preview**
- Alternative A: "You will receive: {description}."
- Alternative B: "Your input data is: {description}."
- Alternative C: "The material you process is: {description}. Set your expectations accordingly before reading."
- Alternative D: "What arrives at your threshold: {description}."
- PURPOSE: Calibrate the agent's expectations before it encounters raw data.
- HYPOTHESIS: This field is always present and always free-text. The rendering challenge is that some descriptions are self-explanatory while others (like the builder's) benefit from being unpacked. The renderer should present this as-is and trust that the definition author wrote a good description.
- STABILITY: High. The field itself is stable. The content varies wildly per agent, but the rendering pattern (present the description) is constant.

### Cross-section dependencies
- Tightly coupled with `format` — the description tells you what the content IS, format tells you how it is ENCODED.
- Coupled with `context_required` — for the builder, the description says "preparation package" but the context_required says "also read these 7 reference documents." The description covers the payload; context_required covers the knowledge base.

---

## FIELD: format
TYPE: string (enum-like)
OPTIONAL: no (present in both agents)
VALUES: "text" / "jsonl"

### What the agent needs to understand

Format tells the agent the encoding of the payload. This has direct behavioral consequences:

- **"text"**: The input is unstructured or semi-structured prose/content. The agent reads it as a document. Parsing is conceptual, not mechanical.
- **"jsonl"**: The input is a stream of JSON objects, one per line. The agent reads it as structured records. Parsing is mechanical — each line is a discrete unit with known fields.

This field fundamentally shapes HOW the agent reads. A text-format agent approaches its input like reading a brief. A jsonl-format agent approaches its input like processing a queue. The cognitive stance is different.

### Fragments

**format_expectation**
- Alternative A: "The input is formatted as {format}."
- Alternative B: "Your input file is in {format} format. {'Each line is one JSON record — process them sequentially.' if jsonl else 'Read it as a continuous document.'}"
- Alternative C: "Input encoding: {format}. {'Expect one JSON object per line, each a discrete work unit.' if jsonl else 'Expect a cohesive document to be read holistically.'}"
- Alternative D: "The data arrives as {format}. {'This means structured records — each line stands alone as a complete data unit.' if jsonl else 'This means free-form content to be understood as a whole.'}"
- PURPOSE: Set the agent's parsing strategy — holistic reading vs. record-by-record processing.
- HYPOTHESIS: Format is a critical behavioral switch. The difference between text and jsonl is not cosmetic — it changes whether the agent thinks in terms of "the document says..." or "for each record...". This may warrant conditional rendering that provides format-specific behavioral guidance.
- STABILITY: High as a field. The enum of possible values may grow (toml, json, csv, markdown), but the rendering pattern (declare format + provide format-specific guidance) is stable.

### Cross-section dependencies
- Coupled with `description` — together they form the complete picture of "what is it" + "how is it encoded."
- Influences `execution` — a jsonl agent likely has per-record processing instructions; a text agent likely has holistic processing instructions.
- Influences `output` — jsonl input often implies structured output; text input may imply either.

---

## STRUCTURAL: context_required (array of context entries)

This is the most architecturally interesting part of the input section. It is an optional array, and its presence or absence creates a major conditional branch in rendering.

### What it IS

`context_required` is a reading list. It is a set of documents the agent must read and internalize BEFORE processing the payload. Each entry is a (label, path) pair — a human-readable name and a file path.

This is fundamentally different from the payload. The payload is what the agent transforms. The context is what the agent must KNOW to transform correctly. The builder agent cannot write a good agent definition without understanding the template, the architecture, the mindset documents. These are not inputs to be processed — they are knowledge to be absorbed.

### The conditional branch

- **Builder (7 entries)**: The agent has an extensive required reading list. It must absorb architectural knowledge, design philosophy, templates, and patterns before it can do creative work.
- **Summarizer (0 entries)**: The agent needs no external knowledge. Everything it needs is in the payload itself. Its task is self-contained.

This is not a minor variation — it represents two fundamentally different agent archetypes:
1. **Knowledge-dependent agents**: Need external context to do their work correctly. The context shapes judgment.
2. **Self-contained agents**: The payload contains everything. The task is mechanical or narrowly scoped enough that no external knowledge is needed.

### Rendering implications

When context_required is present, the rendered prompt must:
1. Establish that there IS required reading
2. Present each document with its label and path
3. Instruct the agent to read and internalize these before proceeding
4. Frame them appropriately (reference materials, not additional inputs to process)

When context_required is absent, the rendered prompt must:
1. NOT mention required reading at all (not "you have no required reading" — just silence)
2. Proceed directly to payload description

---

## FIELD: context_required[].context_label
TYPE: string (free text)
OPTIONAL: no (required within each context entry)
VALUES: "Agent Template Reference", "Definition System Architecture", "What Definitions Capture", "Bland Is Correct", "Minimum Required Permissions", "AgentDispatcher Definition", "Includes Paths" / (none — summarizer has no context_required)

### What the agent needs to understand

The label is the human-readable name for a reference document. It tells the agent WHAT this document is about before the agent reads it. Labels like "Bland Is Correct" and "Minimum Required Permissions" are not just names — they are conceptual anchors that prime the agent for what it will find.

Labels serve a dual purpose: they help the agent locate the right document, and they help the agent understand WHY this document is on the reading list. "Agent Template Reference" tells the agent: you need this because you will be producing something that follows this template.

### Fragments

**context_label_presentation**
- Alternative A: "- **{context_label}**: `{context_path}`"
- Alternative B: "Read **{context_label}** at `{context_path}`"
- Alternative C: "- {context_label} (located at `{context_path}`)"
- Alternative D: "**{context_label}** — reference document at `{context_path}`. Read and internalize before proceeding."
- PURPOSE: Present each required reading item with enough context for the agent to understand its role.
- HYPOTHESIS: The label is the more important element for the agent's understanding; the path is the more important element for the agent's action. Both must be present, but the label should lead.
- STABILITY: High. The pattern of (label, path) pairs is stable. The specific labels vary per agent but the rendering template is constant.

---

## FIELD: context_required[].context_path
TYPE: string (absolute file path)
OPTIONAL: no (required within each context entry)
VALUES: various absolute paths under /Users/johnny/.ai/spaces/bragi/definitions/ / (none)

### What the agent needs to understand

The path is the actionable element — this is what the agent uses to actually READ the document. It must be an absolute path (the agent cannot resolve relative paths reliably). The path is a concrete instruction: go here, read this.

### Fragments

**context_path_instruction**
- Alternative A: "Read the file at `{context_path}`."
- Alternative B: "`{context_path}`"
- Alternative C: "Located at: `{context_path}` — read this file in full."
- PURPOSE: Provide the agent with the exact location to read.
- HYPOTHESIS: Paths should be presented verbatim — no summarization, no abbreviation. The agent needs the exact string to use in a Read tool call.
- STABILITY: Very high. Paths are data, not prose. The rendering is mechanical.

### Cross-section dependencies
- Paths link to the `security.paths` section — context_required paths should be included in allowed_read paths. If they are not, the agent cannot fulfill its reading list.
- Paths may link to `includes` — some agents may have includes that overlap with context_required, but the semantics differ (includes are injected into the prompt; context_required is a reading instruction).

---

## STRUCTURAL: context_required as a whole block

### Fragments for the block envelope

**reading_list_header (when context_required is non-empty)**
- Alternative A: "Before processing your input, you must read and internalize the following reference materials:"
- Alternative B: "Required reading — absorb these documents before beginning work:"
- Alternative C: "You have {n} reference documents to read before you begin. These shape your understanding of how to approach this task:"
- Alternative D: "The following documents are prerequisites. Read each one fully — they provide the architectural knowledge and design philosophy you need:"
- Alternative E: "Your preparation includes reading these reference materials. They are not part of your input data — they are the knowledge foundation for your work:"
- PURPOSE: Frame the reading list as prerequisite knowledge, distinct from the payload.
- HYPOTHESIS: The framing matters. These must not be confused with "additional inputs to process." They are knowledge the agent absorbs to do its job well. The language should convey "internalize" not "process."
- STABILITY: High. The need to frame a reading list is constant whenever context_required is non-empty.

**reading_list_absent (when context_required is empty)**
- Alternative A: (silence — do not mention it)
- Alternative B: (silence)
- Alternative C: (silence)
- PURPOSE: Absence should be invisible. Do not say "you have no required reading." Just move on.
- HYPOTHESIS: Mentioning the absence of something creates noise. The agent does not need to know about a feature it does not use.
- STABILITY: Very high. Silence is always the right choice for absent optional blocks.

---

## STRUCTURAL: parameters (array of parameter entries)

### What it IS

Parameters define the invocation interface — what arguments the dispatcher passes to the agent at launch time. Each parameter has a name, type, description, and required flag.

Parameters are the mechanical handoff. They are not about meaning — they are about plumbing. "Here is the path to your tempfile" is a parameter. "Here is the UID for output naming" is a parameter. They are the variables that get substituted into the agent's runtime context.

### Observations across agents

- **Builder (1 param)**: Just the tempfile path. Simple invocation — one file, one job.
- **Summarizer (2 params)**: Tempfile path plus a UID. The UID is metadata that flows through to output — it does not affect processing, it affects naming.

Parameters are the narrowest part of the input section. They are purely mechanical. But they still need to be presented clearly because the agent must know what values it has available.

---

## FIELD: parameters[].param_name
TYPE: string (identifier)
OPTIONAL: no
VALUES: "tempfile" / "tempfile", "uid"

### What the agent needs to understand

The parameter name is the identifier the agent uses to reference this value. "tempfile" means "the path I was given to my input file." "uid" means "the identifier I was given for this work unit."

### Fragments

**parameter_declaration**
- Alternative A: "- `{param_name}` ({param_type}): {param_description}"
- Alternative B: "**{param_name}** — {param_description} (type: {param_type}, required: {param_required})"
- Alternative C: "Parameter `{param_name}`: {param_description}. Type: {param_type}."
- Alternative D: "You receive `{param_name}` as a {param_type} — {param_description}."
- PURPOSE: Declare the parameter with enough information for the agent to use it correctly.
- HYPOTHESIS: Parameters are best presented in a compact, scannable format. They are reference material, not narrative.
- STABILITY: Very high. Parameter declaration is mechanical.

---

## FIELD: parameters[].param_type
TYPE: string (enum-like)
OPTIONAL: no
VALUES: "path" / "path", "string"

### What the agent needs to understand

Type tells the agent what kind of value to expect. "path" means a file system path — the agent can read from it. "string" means an opaque string value — the agent uses it as-is (for naming, for matching, for passing through).

### Fragments

(Covered within parameter_declaration above — type is presented inline with the parameter, not as a standalone element.)

- PURPOSE: Type is metadata on the parameter, not a standalone behavioral concern.
- HYPOTHESIS: Type rarely needs its own rendering fragment. It is always presented as part of the parameter declaration.
- STABILITY: Very high.

---

## FIELD: parameters[].param_description
TYPE: string (free text)
OPTIONAL: no
VALUES: "Path to the preparation package" / "Path to the JSONL tempfile containing stripped interview exchanges", "Interview identifier used for output filename construction"

### What the agent needs to understand

The description tells the agent what this parameter represents in the context of this specific task. It bridges the gap between the abstract (a path parameter) and the concrete (the path to YOUR preparation package for THIS task).

### Fragments

(Covered within parameter_declaration above.)

- PURPOSE: Contextualize the parameter for this specific agent's task.
- HYPOTHESIS: Descriptions should be presented verbatim from the definition. They were written by the definition author with specific intent.
- STABILITY: Very high.

---

## FIELD: parameters[].param_required
TYPE: boolean
OPTIONAL: no
VALUES: true / true, true

### What the agent needs to understand

Whether this parameter must be provided. In the current data, all parameters are required. If optional parameters exist, the agent needs to know what happens when they are absent (default behavior).

### Fragments

**required_indicator**
- Alternative A: "(required)" / "(optional)"
- Alternative B: "This parameter is always provided." / "This parameter may not be provided. If absent, {default_behavior}."
- Alternative C: Implicit — if all are required, do not mention it. Only call out optionality when it exists.
- PURPOSE: Set expectations about parameter availability.
- HYPOTHESIS: If all parameters in a given agent are required, the required flag adds noise. It may be better to only render required/optional distinctions when there is actual variation. However, for safety, always marking required is defensible.
- STABILITY: High. The field is stable. The rendering decision (always show vs. show only when mixed) is a design choice.

---

## STRUCTURAL: Ordering — context_required before or after parameters?

### Analysis

This is a genuine design decision with behavioral implications.

**Case for context_required FIRST:**
- The reading list is prerequisite knowledge. The agent should absorb it BEFORE it even thinks about the payload.
- Conceptually: "First, learn what you need to know. Then, here is what you will process."
- This mirrors how a human would onboard: read the background materials, then look at the work.

**Case for parameters FIRST:**
- Parameters tell the agent what it HAS. They are the concrete handoff.
- The agent needs to know "I have a tempfile at path X and a UID of Y" before it can make sense of anything else.
- Pragmatically: the agent reads the tempfile to get its payload, and it may need to read context_required documents too — knowing what files it has helps frame the reading list.

**Case for: description + format FIRST, then context_required, then parameters:**
- Lead with WHAT the input is (description + format) — this sets the mental model.
- Then provide the knowledge base (context_required) — this prepares the agent.
- Then provide the mechanics (parameters) — this gives the agent the concrete values.
- This follows: what → why/how to think about it → where to find it.

### Fragments

**ordering_strategy_A (context first)**
- "Before you begin, read and absorb the following reference materials. [...context_required...] Your input data: [...description, format, parameters...]"

**ordering_strategy_B (parameters first)**
- "You receive the following parameters: [...parameters...] Your input is {description} in {format} format. Required reading before processing: [...context_required...]"

**ordering_strategy_C (description → context → parameters)**
- "You will process {description}, delivered as {format}. First, read these reference materials: [...context_required...] Your invocation parameters: [...parameters...]"

- PURPOSE: Establish the cognitive flow of the input section.
- HYPOTHESIS: Strategy C (description → context → parameters) is the strongest because it follows the natural information hierarchy: what am I working with → what do I need to know → what are my concrete handles. This mirrors how a new employee would be briefed: "Your job is X. Here is the background reading. Here are the files on your desk."
- STABILITY: Medium. This is a design decision that may evolve as more agents are observed. The ordering should be consistent across all agents once chosen.

---

## STRUCTURAL: Conditional branching — with vs. without context_required

### Analysis

The presence or absence of context_required creates two distinct rendering paths:

**Path A: context_required present (Builder pattern)**
```
[Description of what input is]
[Format declaration]
[Reading list with N entries]
[Parameters]
```

The rendered section is substantial. The agent has both payload awareness and knowledge preparation. The cognitive load is higher — the agent must read multiple documents, internalize them, and THEN process the payload with that knowledge applied.

**Path B: context_required absent (Summarizer pattern)**
```
[Description of what input is]
[Format declaration]
[Parameters]
```

The rendered section is lean. The agent has only payload awareness. The task is self-contained. The cognitive load is lower — everything the agent needs is in the payload itself.

### Fragments

**conditional_rendering_note**
- The renderer must check: does `context_required` exist and have entries?
  - YES: Render the full reading list block between description/format and parameters.
  - NO: Skip the reading list block entirely. Do not render an empty section or a "no required reading" message.
- PURPOSE: Keep the rendered prompt clean and relevant to the specific agent.
- HYPOTHESIS: This is the primary conditional branch in the input section. Other fields (delivery, description, format, parameters) are always present. Only context_required is truly optional.
- STABILITY: Very high. The conditional is binary and clean.

---

## STRUCTURAL: The compound entry template for context_required

### Analysis

Each context_required entry is a (label, path) pair. When rendering multiple entries, the renderer needs a template for individual entries AND an envelope for the collection.

### Fragments

**single_entry_template**
- Alternative A: "- **{context_label}**: Read `{context_path}`"
- Alternative B: "- **{context_label}** (`{context_path}`)"
- Alternative C: "- {context_label} — `{context_path}`"
- Alternative D: "1. **{context_label}**: `{context_path}`"

**collection_envelope**
- Alternative A: Bulleted list (unordered — reading order does not matter)
- Alternative B: Numbered list (ordered — suggests a reading sequence)
- Alternative C: Bulleted list with a note: "Read these in any order, but read all of them before proceeding."

- PURPOSE: Present multiple reading items in a scannable, actionable format.
- HYPOTHESIS: Bulleted list (Alternative A or C) is preferable unless the definition author explicitly orders the context entries. Numbered lists imply sequence where none may be intended. However, the builder's list has a natural progression (template → architecture → philosophy → specifics) that might benefit from numbering.
- STABILITY: High. The template pattern is stable; the choice between ordered/unordered is a one-time design decision.

---

## STRUCTURAL: The overall input section envelope

### Fragments

**section_header**
- Alternative A: "## Input" (minimal)
- Alternative B: "## What You Receive" (behavioral)
- Alternative C: "## Your Input" (possessive, establishes ownership)
- Alternative D: (no header — the input description flows from the role/task section)

**section_opening**
- Alternative A: "Your work begins with the following input:"
- Alternative B: "You receive input data to process. Here is what to expect:"
- Alternative C: "Here is what arrives at your workstation:"
- Alternative D: (no opening — jump directly to description)

- PURPOSE: Frame the transition into the input section.
- HYPOTHESIS: Minimal framing is best. The input section should not be ceremonial. A short header and immediate content is more effective than elaborate transitions. The agent is being briefed, not entertained.
- STABILITY: Medium-high. The framing style is a global design decision.

---

## CROSS-SECTION DEPENDENCY MAP

| Input Field | Depends On | Depended On By |
|---|---|---|
| delivery | — | parameters (tempfile delivery implies path parameter) |
| description | — | execution (what the agent processes) |
| format | — | execution (how the agent parses), output (structural correspondence) |
| context_required | security.paths.allowed_read (must include these paths) | execution (knowledge applied during processing) |
| context_required | includes (may overlap but different semantics) | — |
| parameters | delivery (path param matches delivery mechanism) | execution (values referenced during processing), output (uid used in naming) |
| parameters.uid | — | output (filename construction) |

---

## DESIGN RECOMMENDATIONS

1. **Render order**: description + format → context_required (if present) → parameters. This follows the cognitive hierarchy: what → knowledge → mechanics.

2. **context_required framing**: Present as "required reading" or "reference materials," never as "additional inputs." The distinction between payload and knowledge is critical.

3. **Silence for absence**: When context_required is empty, emit nothing. No "you have no required reading" messages.

4. **Format-conditional guidance**: Consider emitting a brief format-specific behavioral note. "jsonl" implies per-record processing; "text" implies holistic reading. This may belong in execution rather than input, but the seed is planted here.

5. **Parameters as reference table**: Parameters are best rendered in a compact, scannable format — they are looked up, not read narratively.

6. **The tempfile parameter is special**: When delivery is "tempfile" and a parameter named "tempfile" exists, these are the same concept. The renderer should not present them as two unrelated things. Consider: "Your input arrives as a temporary file. The path is provided as the `tempfile` parameter."

7. **context_required count as a complexity signal**: An agent with 7 required reading documents is doing fundamentally different cognitive work than an agent with 0. This is not just a rendering concern — it signals the type of agent (knowledge-dependent vs. self-contained). The rendering should acknowledge this implicitly through the weight given to the reading list section.
