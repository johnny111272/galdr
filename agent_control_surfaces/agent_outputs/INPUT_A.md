# Input Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The input section configures the agent's understanding of WHERE ITS WORK COMES FROM. This is not a metadata block about data formats. It is the agent's origin story for the current invocation -- the answer to "what was I given, what do I know, and what should I expect when I open the file?"

After reading this section, the agent should have internalized:

1. **What arrives at its doorstep.** A tempfile containing data in a specific format (text or jsonl). This is the raw material. The agent must understand what it will encounter when it reads that file -- not just "a file path" but "a file containing stripped interview exchanges, one JSON object per line, with fields: exchange, agent, user." The description and format fields together create an expectation that shapes how the agent approaches its first instruction step.

2. **What it must already know before it begins.** The context_required documents are prerequisite knowledge. They are not reference materials to consult during work -- they are foundational understanding the agent must absorb BEFORE processing its input. An agent-builder that has not internalized "bland is correct" will write florid definitions. An agent-builder that has not read the template will invent field names. The context_required array is a reading list that must be completed before the first instruction step can execute meaningfully.

3. **How it was invoked.** The parameters tell the agent what arguments it received. A tempfile path, a uid string. These are not just "inputs" -- they are the specific handles the agent uses to locate its data and construct its outputs. The parameter interface is the contract between the dispatcher and the agent: "I gave you these things, use them."

4. **What it should NOT expect.** The absence of context_required (as in the summarizer) tells the agent something critical: you need no external knowledge. Your world is entirely inside the tempfile. Do not go looking for reference materials. Do not try to learn about the domain from other files. Everything you need is in your input. This is a confinement signal as important as the security boundary -- it constrains the agent's information-seeking behavior.

5. **The shape of its task.** A text format with 7 context documents and 1 parameter signals a broad, knowledge-intensive, creative task. A jsonl format with 0 context documents and 2 parameters signals a tight, mechanical, batch-processing task. The input section's SHAPE -- not just its content -- telegraphs what kind of work follows.

### The knowledge-vs-data distinction

The most consequential design choice in this section is how to frame the relationship between context_required (knowledge the agent must internalize) and the tempfile (data the agent must process). These are fundamentally different kinds of input:

**The tempfile is work.** It contains the material the agent transforms. The agent's instructions operate on this data. The output is derived from this data. This is the "what" of the agent's task.

**The context_required documents are wisdom.** They contain principles, patterns, reference structures, and domain knowledge that shape HOW the agent processes the data. They are not processed -- they are absorbed. The agent does not transform the template reference into output. The agent uses the template reference to make correct decisions while transforming the preparation package into output.

If the section presents both as "your inputs" without distinction, the agent may treat context documents like additional data to process, or treat the tempfile like another document to read and absorb. The section must establish a clear cognitive separation: "Here is what you know. Here is what you work on."

### The zero-context case

When context_required is absent (the summarizer), the section's character changes entirely. It becomes purely about the data channel: what format, what fields, what parameters. There is no knowledge-loading preamble, no reading list, no prerequisite understanding. The agent is a pure processor: data in, transformed data out.

This creates a fundamental conditional branch. An input section with context_required is saying: "Before you begin, you must understand these things." An input section without context_required is saying: "You already know everything you need. Here is your data."

---

## FIELD: delivery
TYPE: string (currently always "tempfile")
OPTIONAL: no
VALUES: "tempfile" / "tempfile"

### What the agent needs to understand

The delivery mechanism tells the agent HOW its data arrives. Both agents receive their data via a tempfile -- a temporary file written by the dispatcher before the agent starts. The agent reads this file as its first act.

This field is structurally invariant in the current system (always "tempfile"), but it matters because it tells the agent its data is ephemeral -- written for this invocation, consumed during this invocation, not a persistent artifact. The agent should not worry about the file's lifecycle, should not try to preserve it, and should not reference it in its output as a durable path.

### Fragments

**delivery_declaration**
- Alternative A: `Your input arrives as a tempfile.` -- simple declarative, names the mechanism
- Alternative B: `The dispatcher provides your input as a temporary file at the path specified below.` -- explains the mechanism and points to the parameter
- Alternative C: No explicit delivery mention -- the parameters section names a "tempfile" parameter, which is self-explanatory. Naming the delivery mechanism separately adds redundant information.
- Alternative D: `Input delivery: tempfile` -- terse metadata line, treating delivery as a configuration parameter
- PURPOSE: Tells the agent how to expect its data. If delivery could vary (tempfile vs. stdin vs. inline), this would be critical. Since it is always tempfile, the question is whether it needs to be stated at all or whether the parameter definition is sufficient.
- HYPOTHESIS: Explicitly naming the delivery mechanism may help the agent form a clear operational model: "Step 1: read the tempfile." Omitting it (C) relies on the parameter named "tempfile" to carry the delivery semantics, which it probably does for any capable model. The terse metadata form (D) signals "this is infrastructure" and may be skimmed. The explanatory form (B) creates the clearest operational picture but adds length. Test: does explicit delivery naming affect how reliably agents find and read their input, or is the parameter definition sufficient?
- STABILITY: structural -- this is invariant in the current system and may not even need rendering

---

## FIELD: description
TYPE: string
OPTIONAL: no
VALUES: "Preparation package containing requirements, domain analysis, data shapes, and schema references" / "Stripped interview exchanges with exchange number, agent question, and user response -- no learned, threads, or insight fields"

### What the agent needs to understand

The description tells the agent WHAT is in the tempfile before it reads the tempfile. This is a preview -- a mental model the agent builds before encountering the actual data. The description shapes expectations: the builder expects a "preparation package" (a structured bundle of heterogeneous materials), while the summarizer expects "stripped interview exchanges" (a homogeneous sequence of records).

Critically, the summarizer's description includes a negative boundary: "no learned, threads, or insight fields." This tells the agent not just what IS present, but what is ABSENT -- and that the absence is deliberate. This negative description is an anti-hallucination measure: it prevents the agent from inventing or seeking data that was intentionally excluded.

### Fragments

**input_description_presentation**
- Alternative A: `**Input:** {description}` -- bold label, description as inline text. Simple presentation that names what follows.
- Alternative B: `You will receive: {description}` -- second-person future tense, framing the description as a preview of what the agent will encounter
- Alternative C: `Your data: {description}` -- possessive framing that creates ownership. "Your data" implies responsibility for it.
- Alternative D: Woven into a sentence with format: `Your input is a {format} file containing {description}.` -- integrates description with format into a single coherent preview
- Alternative E: No label at all -- the description rendered as the opening sentence of the section, establishing the data context before any structural elements: `{description}. This arrives as a {format} tempfile at the path given below.`
- PURPOSE: Creates the agent's first mental model of its input data. The framing controls whether the agent approaches the data as something to receive passively ("Input:"), something to expect actively ("You will receive"), or something it owns ("Your data").
- HYPOTHESIS: "You will receive" (B) creates temporal expectation -- the agent knows it has not yet seen the data but will. This may improve the agent's approach to its first instruction step (reading the file). "Your data" (C) creates ownership, which may increase careful handling. Integrated presentation (D) is the most information-dense -- the agent learns description AND format in one sentence. Label-free opening (E) establishes the data context as the primary frame for the entire section. Test: does integrated presentation (D) produce better first-step execution than separated fields? Does the possessive framing (C) reduce careless data handling?
- STABILITY: formatting (label choice) + experimental (framing strategy)

**negative_boundary_in_description**
- Alternative A: Render the description as-is, letting the negative boundary ("no learned, threads, or insight fields") pass through naturally as part of the description text
- Alternative B: Split the description into positive and negative parts: `Contains: exchange number, agent question, user response. Excluded: learned, threads, insight fields.` -- explicit structural separation of what's present from what's absent
- Alternative C: Elevate the negative boundary to a separate warning: `{positive description}. WARNING: Fields learned, threads, and insight have been deliberately stripped. Do not attempt to access them.` -- the absence is highlighted as a deliberate design decision
- Alternative D: For descriptions without negative boundaries (builder), render nothing extra. For descriptions with them (summarizer), add the warning. This creates a conditional branch.
- PURPOSE: Controls how strongly the agent registers the deliberate absence of fields. The summarizer's description includes a negative boundary that, if missed, could cause the agent to hallucinate missing fields or seek external data.
- HYPOTHESIS: Passing through naturally (A) relies on the agent noticing the negative clause in a longer sentence -- it may be overlooked. Structural separation (B) makes the absence impossible to miss. Elevating to a warning (C) treats the absence as a safety concern. The warning form is strongest but may be excessive for capable models. Test: do agents that receive a structurally separated negative boundary produce fewer hallucinated-field errors?
- STABILITY: experimental (framing strength) + conditional (only applies when description contains negative boundaries)

---

## FIELD: format
TYPE: string (enum: "text" | "jsonl" | others possible)
OPTIONAL: no
VALUES: "text" / "jsonl"

### What the agent needs to understand

The format tells the agent what structure to expect inside the tempfile. This is a parsing directive -- it controls the agent's first mechanical interaction with its data.

"text" means: the file is a free-form text document. Read it as prose. The structure is embedded in the content, not in the format.

"jsonl" means: the file is a sequence of JSON objects, one per line. Each line is independently parseable. The structure is rigid and predictable. This also implies batch processing -- each line is one unit of work.

The format field has outsized behavioral influence because it determines whether the agent approaches its input as a document to comprehend (text) or as a dataset to iterate (jsonl). These are fundamentally different cognitive modes. A document-comprehension mode allows the agent to build holistic understanding. A dataset-iteration mode focuses the agent on per-record processing.

### Fragments

**format_declaration**
- Alternative A: `Format: {format}` -- terse metadata. The agent sees "jsonl" as a label.
- Alternative B: `The input file is in {format} format.` -- declarative sentence. Slightly more natural than a label.
- Alternative C: Format-specific prose that explains what the format means operationally:
  - For "text": `The input is a text document. Read it as a whole to build understanding before proceeding.`
  - For "jsonl": `The input is a JSONL file -- one JSON object per line. Each line is one work unit to be processed in sequence.`
- Alternative D: Format integrated into the description (see input_description_presentation Alternative D above). No separate format declaration.
- Alternative E: No explicit format declaration. The description already implies the format: "stripped interview exchanges" strongly implies structured records, "preparation package" strongly implies text. The format field adds no information the agent cannot infer.
- PURPOSE: Sets the agent's parsing expectations. An agent that knows it is reading JSONL will approach the file differently than one that knows it is reading text.
- HYPOTHESIS: Terse metadata (A) is skimmable -- the agent may note "jsonl" without deeply processing what it means for its approach. Format-specific operational prose (C) directly configures the agent's reading strategy: "read as a whole" vs. "process each line." This could have significant behavioral impact -- it pre-configures the agent's first instruction step. Integrated presentation (D) avoids redundancy but may lose the operational guidance. Test: does operational format prose (C) improve first-step execution quality? Does it reduce parsing errors for JSONL agents?
- STABILITY: formatting (declaration style) + experimental (operational prose) + conditional (prose varies by format value)

---

## FIELD: context_required (array of label+path pairs)
TYPE: array of objects, each with context_label (string) and context_path (string, absolute path)
OPTIONAL: yes (present in builder with 7 entries, absent in summarizer)
VALUES: 7 entries for agent-builder / absent for interview-summary

### What the agent needs to understand

This is the most architecturally distinctive feature of the input section. The context_required array is a reading list -- documents the agent MUST read and internalize before it begins processing its tempfile data. These are not input data. They are prerequisite knowledge.

Each entry has two components:
- **context_label**: A human-readable name for the document ("Agent Template Reference", "Bland Is Correct"). This tells the agent what the document IS, which shapes how the agent reads and applies it.
- **context_path**: The absolute filesystem path to the document. This is the handle the agent uses to actually read the file.

The builder's 7 context documents form a coherent domain education:
1. Agent Template Reference -- the structural specification
2. Definition System Architecture -- the philosophical framework
3. What Definitions Capture -- the scope definition
4. Bland Is Correct -- the quality standard
5. Minimum Required Permissions -- the security principle
6. AgentDispatcher Definition -- the output target understanding
7. Includes Paths -- the file organization convention

These are not arbitrary reference materials. They are a curated curriculum. The ORDER may matter -- the template reference provides structural grounding, the architecture document provides philosophical context, and the remaining documents refine the agent's understanding in specific dimensions.

When context_required is absent (summarizer), the agent needs no external knowledge. Its entire world is the tempfile. This is a profound behavioral difference: the builder must become educated before working, while the summarizer must work immediately.

### Fragments

**context_section_heading**
- Alternative A: `### Required Reading` -- frames the context documents as mandatory study material
- Alternative B: `### Prerequisites` -- frames them as conditions that must be met before work begins
- Alternative C: `### Domain Knowledge` -- frames them as knowledge the agent needs for this specific task
- Alternative D: `### Before You Begin` -- temporal framing that explicitly sequences reading before work
- Alternative E: No sub-heading -- the context list appears within the broader input section without its own header
- PURPOSE: Labels the context_required block. The label choice frames how the agent perceives these documents -- as study material, prerequisites, knowledge, or temporal constraints.
- HYPOTHESIS: "Required Reading" (A) is the strongest framing -- it evokes educational obligation. The agent approaches each document as something to learn. "Prerequisites" (B) is more clinical -- conditions to satisfy, potentially reducing engagement depth. "Before You Begin" (D) is temporal -- it tells the agent WHEN to read, not how to read. "Domain Knowledge" (C) tells the agent WHY these documents matter. Test: does "Required Reading" produce deeper engagement with context documents than "Prerequisites"? Does temporal framing ("Before You Begin") improve the likelihood that the agent reads all documents before starting?
- STABILITY: experimental -- label choice directly affects how thoroughly the agent processes these documents

**context_preamble**
- Alternative A: No preamble -- heading followed directly by the document list
- Alternative B: `Read and internalize the following documents before processing your input. These establish the principles and reference structures your work depends on.` -- explicit instruction to internalize, with explanation of purpose
- Alternative C: `The following documents contain knowledge essential to your task. Read each one completely.` -- instruction plus importance signal
- Alternative D: `Your work quality depends on understanding these documents. Do not begin processing until you have read all of them.` -- stakes framing plus temporal constraint
- Alternative E: `These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting. After reading them, you should not need to re-read them.` -- explicitly distinguishes between "reference" and "prerequisite" modes
- PURPOSE: Tells the agent HOW to approach the context documents. Without a preamble, the agent may skim them, read them partially, or treat them as reference materials to check during work rather than knowledge to absorb upfront.
- HYPOTHESIS: The most critical distinction is between "reference" (consult during work) and "prerequisite" (absorb before work). Alternative E makes this distinction explicit, which may produce different reading behavior. Alternative D adds stakes ("your work quality depends on...") which may increase reading thoroughness but also increase anxiety. Alternative B is the most balanced -- instruction plus purpose. Test: does explicitly distinguishing "absorb before starting" from "consult during work" affect how agents use context documents? Do agents that receive the stakes framing (D) produce higher-quality output?
- STABILITY: experimental -- this preamble directly configures the agent's knowledge-acquisition behavior

**context_entry_template (compound: label + path)**
- Alternative A: Bulleted list with label as text and path in parentheses:
  ```
  - Agent Template Reference (/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-template.toml)
  - Definition System Architecture (/Users/johnny/.ai/spaces/bragi/definitions/prompts/.../one-definition-many-agents.md)
  ```
- Alternative B: Numbered list (implies reading order):
  ```
  1. Agent Template Reference — /path/to/file
  2. Definition System Architecture — /path/to/file
  ```
- Alternative C: Label as bold text, path on next line or as code:
  ```
  **Agent Template Reference**
  `/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-template.toml`
  ```
- Alternative D: Label only, with instruction to use Read tool. Path embedded but de-emphasized:
  ```
  - **Agent Template Reference**: Read this file — `agent-template.toml`
  ```
  (full path available but presented as a relative or shortened form)
- Alternative E: Table format:
  ```
  | Document | Path |
  |---|---|
  | Agent Template Reference | /path/to/agent-template.toml |
  ```
- PURPOSE: Presents each context document as a unit the agent must engage with. The compound nature (label + path) means the template must decide which component is primary -- does the agent see the LABEL first (and understand WHAT the document is) or the PATH first (and know WHERE to find it)?
- HYPOTHESIS: Label-first presentation (A, B, D) helps the agent understand what each document contains before locating it. This creates expectation -- the agent reads "Bland Is Correct" and already has a hypothesis about what the document will say. Numbered list (B) implies that reading order matters, which may cause the agent to read more carefully in sequence rather than cherry-picking interesting documents. Path-first or table format (E) treats the list as a data table, which may produce more mechanical reading (locate, open, skim, next). Bold labels with de-emphasized paths (D) most strongly foregrounds the document's purpose. Test: does numbered ordering produce more sequential, thorough reading? Does label-first presentation improve comprehension compared to path-first?
- STABILITY: formatting (list style, path display) + structural (ordering implication)

**context_reading_order**
- Alternative A: No order specified -- the list is rendered in whatever order it appears in the data. The agent reads in whatever order it prefers.
- Alternative B: Numbered list implies data order is the intended reading order (template first, specifics after)
- Alternative C: Explicit ordering instruction: `Read these in the order listed. Earlier documents provide context for later ones.` -- establishes that order is intentional, not arbitrary
- Alternative D: Grouped by type: structural references first, philosophical documents second, specific guidelines third. Sub-headings within the list.
- PURPOSE: Controls whether the agent perceives the context list as ordered (curriculum with dependencies) or unordered (a set of reference documents).
- HYPOTHESIS: For the builder's 7 documents, order may genuinely matter -- reading "What Definitions Capture" before "Agent Template Reference" means the agent encounters the conceptual framework before the structural specification, potentially causing misunderstanding. Reading the template first grounds the agent in concrete structure, then the philosophical documents refine that understanding. If the list is unordered, the agent may read the most interesting-sounding document first (likely "Bland Is Correct" due to its unusual name), which is not the best starting point. Test: does explicit ordering produce better knowledge integration than unordered presentation?
- STABILITY: structural (whether to order at all) + experimental (the specific ordering strategy)

**context_absent_handling**
- Alternative A: When context_required is absent, render nothing -- the input section simply has no context block. The absence speaks for itself.
- Alternative B: Explicit absence declaration: `This agent requires no external knowledge beyond its instructions.` -- positively states that no reading is needed
- Alternative C: Implicit through section structure -- if there is no context_required heading or list, the agent never encounters the concept of "prerequisite knowledge" and naturally operates as a pure processor
- Alternative D: Conditional preamble: if context_required is absent, the input section opens differently -- perhaps with a directness that signals "you have everything you need already"
- PURPOSE: Handles the zero-context case. The summarizer has no context documents, which means it should NOT be primed to go looking for reference materials. The question is whether the absence of a reading list is sufficient to prevent information-seeking behavior, or whether the section needs to explicitly state "you need nothing else."
- HYPOTHESIS: Silent absence (A/C) may be sufficient for a well-defined task like summarization -- the agent's instructions are self-contained and the tempfile has all needed data. Explicit absence (B) adds a line that may feel odd ("this agent requires no external knowledge" -- why mention it if it does not apply?). But for agents that could plausibly benefit from external knowledge, explicit absence prevents time-wasting exploration. Test: do agents without context_required ever attempt to read external files? If so, does explicit "no external knowledge needed" reduce that behavior?
- STABILITY: conditional (only relevant when context_required is absent) + experimental (whether to state or leave silent)

---

## FIELD: parameters (array of compound entries)
TYPE: array of objects, each with param_name (string), param_description (string), param_type (string enum), param_required (boolean)
OPTIONAL: no (at minimum, tempfile parameter is always present)
VALUES: 1 parameter for agent-builder (tempfile path) / 2 parameters for interview-summary (tempfile path + uid string)

### What the agent needs to understand

The parameters define the agent's invocation interface -- the specific values passed to it by the dispatcher. This is the "function signature" of the agent. Each parameter is a named, typed, described value that the agent can reference during execution.

The builder receives only a tempfile path. The summarizer receives a tempfile path AND a uid string (used for output filename construction). This difference matters: the builder's output naming is entirely up to the agent's judgment (name_known = "unknown"), while the summarizer's output naming is partially determined by the uid parameter (name_known = "partially").

Parameters serve a dual purpose:
1. **Operational:** The agent uses these values to locate data and construct paths. The tempfile parameter tells it where to read. The uid parameter tells it what to name the output.
2. **Contractual:** The parameters are the dispatcher's promise. "I gave you a tempfile at this path" is a guarantee the agent can rely on. The agent should not validate the parameter's existence -- it should trust it.

### Fragments

**parameters_section_heading**
- Alternative A: `### Parameters` -- neutral technical label
- Alternative B: `### What You Received` -- second-person framing that tells the agent these are its possessions
- Alternative C: `### Invocation Arguments` -- technical framing aligned with the dispatch system
- Alternative D: No heading -- parameters presented inline within the input section, perhaps after the description: `{description}. You received: tempfile (path to input), uid (interview identifier).`
- PURPOSE: Labels the parameter block. The choice controls whether the agent sees parameters as technical metadata, possessions, or arguments.
- HYPOTHESIS: "Parameters" (A) is the most neutral and familiar to any model trained on software documentation. "What You Received" (B) creates ownership and grounds the parameters in the current invocation -- these are not abstract interface definitions, they are ACTUAL VALUES the agent has RIGHT NOW. "Invocation Arguments" (C) aligns with the dispatch infrastructure but may feel distant. Inline presentation (D) avoids structural overhead for small parameter lists. Test: does "What You Received" framing cause the agent to use parameters more confidently than "Parameters" framing?
- STABILITY: formatting (label choice) + structural (whether to have a separate heading at all)

**parameter_entry_template (compound: name + description + type + required)**
- Alternative A: Bulleted list with all fields inline:
  ```
  - `tempfile` (path, required): Path to the JSONL tempfile containing stripped interview exchanges
  - `uid` (string, required): Interview identifier used for output filename construction
  ```
- Alternative B: Bold name with description, type in parenthetical:
  ```
  **tempfile** — Path to the preparation package (type: path, required)
  ```
- Alternative C: Definition list style:
  ```
  tempfile
  : Path to the preparation package. Type: path. Required.
  ```
- Alternative D: Natural prose integrating all parameters:
  ```
  You receive a tempfile path pointing to the JSONL input, and a uid string identifying the interview for output filename construction.
  ```
- Alternative E: Table format:
  ```
  | Name | Type | Description |
  |---|---|---|
  | tempfile | path | Path to the JSONL tempfile... |
  | uid | string | Interview identifier... |
  ```
- PURPOSE: Presents each parameter as a usable handle. The agent needs to know the name (for reference), the type (for correct usage), and the description (for understanding what the value represents).
- HYPOTHESIS: Code-formatted names (A, E) signal to the agent that these are literal identifiers to use in tool invocations or path construction. Bold names (B) make the parameter name visually prominent but do not signal "this is a literal string." Prose integration (D) is the most natural but may make individual parameters harder to reference back to. Table format (E) is the most information-dense and scannable but may feel like a specification document rather than an instruction. For agents with only 1 parameter, any format works. For agents with 3+ parameters, table or bulleted formats become important for scannability. Test: does code-formatted parameter names reduce errors where the agent uses the wrong parameter name?
- STABILITY: formatting (list/table/prose style)

**parameter_type_rendering**
- Alternative A: Show the type as a label: `(path)`, `(string)` -- metadata that categorizes the parameter
- Alternative B: Show the type as operational guidance: `(this is a filesystem path -- use it in Read tool calls)`, `(this is a string value -- use it in filename construction)` -- type translated to behavioral guidance
- Alternative C: Omit the type -- the description already implies it. "Path to the JSONL tempfile" clearly implies a path type. "Interview identifier" clearly implies a string.
- Alternative D: Type shown only when non-obvious. A "path" parameter named "tempfile" with a description mentioning "path" does not need a type label. A "string" parameter named "uid" with a description about "identifier" might benefit from explicit typing.
- PURPOSE: Controls whether the agent thinks about parameter types abstractly (A), operationally (B), or not at all (C).
- HYPOTHESIS: Abstract types (A) add precision but may not change behavior -- an agent already knows a path is a path from the description. Operational guidance (B) connects the type to the agent's actual tool usage, which may reduce errors ("use it in Read tool calls" is more actionable than "type: path"). Omission (C) reduces clutter for simple cases. Test: does operational type guidance (B) reduce tool-invocation errors compared to abstract type labels (A)?
- STABILITY: formatting + conditional (based on how obvious the type is from context)

**parameter_required_rendering**
- Alternative A: Show required status: `(required)` -- explicit label
- Alternative B: Omit required status when all parameters are required -- if every parameter is required, the label adds no discriminating information
- Alternative C: Show required status ONLY when some parameters are optional -- the label becomes meaningful only when it distinguishes required from optional
- Alternative D: Instead of labeling, use phrasing: `You MUST use the tempfile parameter...` vs `You MAY use the optional xyz parameter...` -- required/optional expressed through prose rather than labels
- PURPOSE: Communicates whether the agent can ignore a parameter. In the current data, all parameters are required, making the label informational but non-discriminating.
- HYPOTHESIS: When all parameters are required, the "required" label is noise -- it does not distinguish any parameter from any other. In this case, omission (B) is cleaner. If future agents have optional parameters, the label becomes critical for preventing the agent from ignoring an optional parameter it should use, or relying on an optional parameter that might not be present. Test: in a mixed required/optional parameter set, does explicit labeling reduce errors compared to prose-based distinction?
- STABILITY: conditional (depends on whether any parameters are optional) + formatting

---

## STRUCTURAL: section_heading
TYPE: n/a

### What the agent needs to understand

The input section heading tells the agent it is about to learn where its work comes from. The heading primes the agent for a specific kind of information: data sources, formats, prerequisites, parameters.

### Fragments

**section_heading_text**
- Alternative A: `## Input` -- neutral, minimal. Tells the agent this section is about input.
- Alternative B: `## Your Input` -- possessive, personal. The agent is receiving something.
- Alternative C: `## What You Receive` -- active, present-tense. Frames input as a current event.
- Alternative D: `## Data and Context` -- names the two sub-blocks (data tempfile and context documents) in the heading itself, previewing the section's internal structure
- Alternative E: `## Starting Materials` -- metaphorical. Frames input as raw materials for construction, which may be apt for the builder but odd for the summarizer.
- PURPOSE: Sets the agent's expectation for what follows. The heading is the first signal about the section's content.
- HYPOTHESIS: "Input" (A) is the most neutral and familiar. "Your Input" (B) creates ownership. "What You Receive" (C) is the most active -- it implies the agent was just handed something. "Data and Context" (D) previews the section's two-part structure, which may help the agent organize its reading. Test: does a heading that previews the section structure (D) improve comprehension of the knowledge-vs-data distinction?
- STABILITY: structural (heading presence/level) + experimental (heading text)

---

## STRUCTURAL: section_architecture (ordering of sub-blocks)
TYPE: n/a

### What the agent needs to understand

The input section has three distinct sub-blocks: (1) top-level metadata (delivery, description, format), (2) context_required (reading list), and (3) parameters (invocation arguments). The order in which these appear shapes the agent's mental model of its input.

### Fragments

**sub_block_ordering**
- Alternative A: Description/format first -> context_required -> parameters. This is "what am I working with?" -> "what do I need to know?" -> "where do I find it?" The agent builds a preview of its data, learns the prerequisite knowledge, then gets the handles to locate everything.
- Alternative B: Context_required first -> description/format -> parameters. This is "learn this first" -> "here's what you'll process" -> "here's where to find it." The agent acquires knowledge before even knowing what its data looks like, which means it reads context documents through a general lens rather than a task-specific one.
- Alternative C: Parameters first -> description/format -> context_required. This is "here's what you were given" -> "here's what it contains" -> "here's what you need to know." The agent starts with concrete handles, builds a data preview, then acquires knowledge. Most operational, least pedagogical.
- Alternative D: Everything integrated into a single narrative flow: `You receive a tempfile at {path} containing {description} in {format} format. Before processing it, read the following documents: {context list}. You also receive a {param2_name} for {param2_description}.`
- PURPOSE: Controls the cognitive sequence of the agent's input acquisition. Which mental model forms first?
- HYPOTHESIS: Description-first (A) is the most natural reading sequence -- "what is this about?" before "what do I need?" before "how do I access it?" Context-first (B) may produce better knowledge integration because the agent reads prerequisite documents without preconceptions about the data. Parameters-first (C) is most operational but least conceptual. Integrated narrative (D) avoids structural overhead entirely but may be hard to scan for specific information. Test: does context-first ordering produce better knowledge application than description-first? Does integrated narrative produce better or worse comprehension than structured sub-blocks?
- STABILITY: structural -- this is an architectural decision about information sequencing

---

## STRUCTURAL: section_preamble
TYPE: n/a

### What the agent needs to understand

Before the first sub-block, the agent may need framing that establishes the section's purpose and internal structure. The current defective system has no preamble.

### Fragments

**input_section_intro**
- Alternative A: No preamble -- the section opens directly with the description field or context_required block
- Alternative B: `This section describes what you receive and what you must know before starting.` -- brief structural guide that previews the two sub-blocks
- Alternative C: `Your work begins with input. Understand what you have, learn what you need to know, and then proceed to your instructions.` -- temporal framing that sequences the agent's first actions
- Alternative D: Different preambles based on context_required presence:
  - With context: `Before processing your input, you must read and internalize several reference documents. Your input data and prerequisite knowledge are described below.`
  - Without context: `Your input is described below. No additional knowledge is required.`
- PURPOSE: Sets expectations for the section. In a section with complex internal structure (description + 7 context documents + parameters), a preamble helps the agent organize its reading. In a simple section (description + 2 parameters), a preamble may be unnecessary overhead.
- HYPOTHESIS: Conditional preambles (D) handle the structural variation between rich-context and no-context agents. The with-context preamble explicitly names the knowledge-acquisition requirement, which primes the agent for thorough reading. The without-context preamble closes off information-seeking behavior. Fixed preambles (B, C) may be appropriate for the general case but suboptimal for either extreme. Test: does a conditional preamble that names "prerequisite knowledge" for context-heavy agents improve reading thoroughness?
- STABILITY: experimental (preamble content) + conditional (presence and content based on context_required)

---

## STRUCTURAL: knowledge_data_separator
TYPE: n/a

### What the agent needs to understand

When context_required is present, the section contains two cognitively different kinds of material: knowledge (context documents) and data (tempfile + parameters). These should be visually and conceptually separated so the agent does not confuse "things to learn" with "things to process."

### Fragments

**separator_between_context_and_data**
- Alternative A: `---` horizontal rule between the context_required block and the description/parameters block -- strong visual break, no prose
- Alternative B: A transition sentence: `With this knowledge internalized, your input data is:` -- explicit cognitive transition from learning mode to operating mode
- Alternative C: Sub-headings that name each block: `### Prerequisite Knowledge` followed by context list, then `### Input Data` followed by description and parameters
- Alternative D: No separator -- context_required and parameters appear in the same list or flow. The agent must distinguish them by content rather than structure.
- Alternative E: When context_required is absent, no separator is needed (there is nothing to separate). This makes the separator a conditional fragment.
- PURPOSE: Prevents the agent from conflating prerequisite knowledge with input data. Without separation, an agent might treat context documents as additional input to process, or treat the tempfile as another document to learn from.
- HYPOTHESIS: The transition sentence (B) is the strongest separator because it explicitly names the cognitive shift: "you have learned, now you operate." The horizontal rule (A) signals "new topic" without explaining the shift. Sub-headings (C) provide the clearest structural organization but may feel heavy for a section with only 2-3 items. No separator (D) risks the conflation described above. Test: does a cognitive transition sentence reduce cases where agents treat context documents as data to process?
- STABILITY: structural (whether to separate) + conditional (only when context_required exists) + experimental (the transition phrasing)

---

## STRUCTURAL: section_closer
TYPE: n/a

### What the agent needs to understand

The input section ends and another section begins (typically instructions). The transition from "here is what you have" to "here is what you do" is one of the most important cognitive shifts in the entire prompt.

### Fragments

**section_transition**
- Alternative A: `---` divider only -- clean structural break
- Alternative B: A transition sentence that bridges input to instructions: `You now have your input and your knowledge. The following section tells you what to do with them.` -- explicit bridge
- Alternative C: No transition -- the input section's last element (final parameter or context document) is followed directly by the next section's heading
- Alternative D: A readiness checkpoint: `Confirm you have: (1) your input data at the tempfile path, (2) [if context_required] knowledge from all {N} reference documents. Now proceed.` -- forces the agent to mentally verify its input state before continuing
- PURPOSE: Controls the transition from input-understanding to task-execution. The input section configures the agent's starting state; the instructions section begins execution. The cleaner this transition, the more likely the agent enters the instructions section with a complete input model.
- HYPOTHESIS: The readiness checkpoint (D) is the strongest form -- it forces the agent to verify it has everything before proceeding. This may catch cases where an agent skipped a context document or missed a parameter. The bridge sentence (B) is softer -- it narratively transitions from "have" to "do." The bare divider (A) relies on the next section's heading to signal the shift. Test: does a readiness checkpoint reduce cases where agents begin processing before reading all context documents?
- STABILITY: experimental (transition content) + conditional (checkpoint content varies based on context_required presence)

---

## CROSS-FIELD DEPENDENCIES

### input.description / identity.description / frontmatter.description / dispatcher.input_description
The input description is distinct from the identity description. The identity description says what the agent DOES ("Creates new agent TOML definitions..."). The input description says what the agent RECEIVES ("Preparation package containing requirements..."). These are different fields with different values, but they are related -- the input description should be consistent with what the identity description says the agent processes.

### input.format / instructions.steps[0]
The first instruction step almost always references the input format. The builder's step 1: "Read the preparation package from the tempfile path." The summarizer's step 1: "Read the input tempfile. Each line is a JSON object..." The format field in the input section creates an expectation that the first instruction step must fulfill. If the input says "jsonl" but the first instruction says "read as text," the agent will be confused.

### input.context_required / security_boundary.display
The context documents in context_required must be readable by the agent. The security_boundary's display entries (path grants) must include paths that cover the context_required paths. For the builder, the context paths point to `definitions/agents/agent-template.toml` and `definitions/prompts/agent-definition-mindset/*.md` -- both covered by the security boundary's display entries for `./definitions/agents/` and `./definitions/prompts/`. If a context_required path fell outside the security boundary, the agent would be told to read a file it cannot access.

### input.parameters / dispatcher.parameters
The input parameters and dispatcher parameters are the same data in different rendering contexts. The input parameters tell the AGENT what it received. The dispatcher parameters tell the DISPATCHER what to pass. They must be identical.

### input.parameters.uid / output.name_template
For the summarizer, the uid parameter is used to construct the output filename via name_template = "{interview-id}.summaries.jsonl". The input section's uid parameter and the output section's name_template are linked -- the agent must understand that uid is not just metadata, it is a construction material for the output path.

---

## CROSS-SECTION DEPENDENCIES

### input -> instructions
The input section tells the agent what it has. The instructions section tells it what to do with it. The first instruction step typically references the input directly ("Read the input tempfile", "Read the preparation package from the tempfile path"). The input section must create a mental model that the first instruction step can reference without re-explaining.

### input -> identity
The identity section says what the agent IS. The input section says what the agent RECEIVES. For the builder, the identity says "definition author" and the input says "preparation package" -- these are coherent (an author receives source material). For the summarizer, the identity says "contextual interview summarizer" and the input says "stripped interview exchanges" -- also coherent. If the identity said "code reviewer" but the input said "interview exchanges," there would be dissonance.

### input.context_required -> security_boundary
As noted above, context_required paths must be within the security boundary's read grants. But there is a deeper connection: the context_required paths represent files the agent MUST read, while the security_boundary's display represents files the agent MAY read. Context_required is mandatory; security_boundary is permissive. The agent must read context_required documents as obligations, not as options.

### input -> critical_rules
For agents with output tools, the critical_rules section adds batch discipline rules that affect how the agent processes its input. The summarizer's batch_size = 20 means the input's JSONL records are processed in batches of 20. The input section describes the data; the critical_rules section adds processing constraints that modify HOW the data flows through the agent.

---

## CONDITIONAL BRANCHES

### Presence of context_required
This is the primary conditional branch. When present (builder), the section is dominated by a reading list that may be 7+ entries long. When absent (summarizer), the section is compact -- just description, format, and parameters. The section's visual weight, internal structure, and preamble should all vary based on this branch.

Specific changes when context_required is present:
- A reading-list sub-block with its own heading/preamble
- A separator between the reading list and the data description
- Possibly a readiness checkpoint before transition to instructions
- The section's overall length is 3-5x longer

Specific changes when context_required is absent:
- No reading-list block
- Possibly an explicit "no external knowledge needed" statement
- Shorter section with direct flow from description to parameters
- Simpler transition to instructions

### Number of parameters
The builder has 1 parameter. The summarizer has 2. Future agents could have 0 (if input is hardcoded) or 5+ (if the interface is complex). The parameter presentation strategy must scale:
- 1 parameter: inline presentation works, list format works, table is overkill
- 2-3 parameters: bulleted list is natural, table works, inline becomes crowded
- 4+ parameters: table becomes preferred for scannability

### Format value
The format field changes the agent's parsing expectations:
- "text": the agent reads the tempfile as a document, comprehending it holistically
- "jsonl": the agent reads the tempfile as a dataset, processing records sequentially

This may affect the description's framing -- a text description might benefit from "read and understand this document" language, while a jsonl description might benefit from "process these records in order" language.

### Relationship between format and context_required
The builder is text-format WITH context_required. The summarizer is jsonl-format WITHOUT context_required. This correlation makes intuitive sense (broad creative tasks need knowledge; tight batch tasks do not), but it is not a rule. An agent could be jsonl-format WITH context_required (a batch processor that needs reference schemas) or text-format WITHOUT context_required (a text transformer that needs no external knowledge). The section design must handle all four combinations.

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### input_shape_signal
Nothing in the current system tells the agent what KIND of task its input implies. But the input's shape IS a strong task-type signal:
- Text format + many context documents + 1 parameter = broad, knowledge-intensive, creative task
- JSONL format + no context documents + 2+ parameters = tight, mechanical, batch task

A fragment could make this signal explicit:
- `This is a knowledge-intensive task. Your input is a preparation package requiring domain understanding to process correctly.`
- `This is a batch processing task. Your input is a sequence of records to process uniformly.`

**PURPOSE:** Pre-configures the agent's cognitive mode for the entire session. A knowledge-intensive signal primes for depth. A batch-processing signal primes for consistency and throughput.

**HYPOTHESIS:** Making the task type explicit may improve the agent's pacing and resource allocation. An agent primed for "batch processing" may maintain more consistent quality across records. An agent primed for "knowledge-intensive" may invest more in comprehending context documents. However, this signal may also be redundant with the identity section's role_description, which already configures cognitive stance. Test: does an explicit task-type signal in the input section produce measurably different behavior than relying on the identity section alone?

**STABILITY:** experimental -- this fragment type does not exist and its interaction with identity configuration is unknown

### input_completeness_assertion
Nothing currently tells the agent whether its input is COMPLETE -- whether the tempfile contains everything it needs, or whether it might need to seek additional data. For the summarizer, the input is definitively complete (all exchanges in the tempfile, nothing else needed). For the builder, the input is the preparation package, but the agent also reads 7 context documents -- so the "complete input" is actually the union of tempfile + context.

- Alternative A: `Your tempfile and required reading together constitute your complete input. Everything you need is provided. Do not seek additional sources.`
- Alternative B: `The tempfile contains your working data. The required reading contains your domain knowledge. Together, they are everything you need.`
- Alternative C: No completeness assertion -- the agent infers completeness from the absence of any instruction to seek more data.

**PURPOSE:** Prevents the agent from spending time searching for additional context, seeking clarification, or hedging about insufficient information. This is particularly important for autonomous dispatched agents that cannot ask follow-up questions.

**HYPOTHESIS:** Autonomous agents that receive a completeness assertion may be less likely to waste output tokens on caveats like "I would need more information to..." or "Without access to..." An explicit "everything is provided" statement may also reduce the builder agent's temptation to explore beyond its 7 context documents. Test: does a completeness assertion reduce caveat-hedging in agent output?

**STABILITY:** experimental

### parameter_usage_hint
Nothing currently connects parameters to their usage site. The tempfile parameter is used in the first instruction step. The uid parameter is used in output filename construction. But nothing in the input section tells the agent WHERE each parameter will matter.

- Alternative A: `tempfile — used in Step 1 to locate your input data`; `uid — used in output to construct the filename`
- Alternative B: No usage hints -- the instructions and output sections reference parameters when needed. Forward-referencing from the input section creates coupling.
- Alternative C: A general statement: `These parameters will be referenced in your instructions and output sections. Remember their values.`

**PURPOSE:** Helps the agent maintain parameter values in working memory by connecting them to future usage.

**HYPOTHESIS:** For agents with 1-2 parameters, usage hints may be unnecessary -- the agent can hold these values easily. For agents with 4+ parameters, knowing which parameters matter for which steps may reduce "lost parameter" errors where the agent forgets a parameter exists. However, forward-referencing creates coupling between the input section and later sections, which complicates independent section rendering. Test: for agents with 3+ parameters, do usage hints reduce parameter-forgetting errors?

**STABILITY:** conditional (useful only for multi-parameter agents) + experimental

### context_document_purpose_annotations
The context_label field provides a name for each document, but not an explanation of WHY the agent needs it. The builder's context documents have labels like "Bland Is Correct" -- evocative but not explanatory. A purpose annotation would tell the agent what to look for in each document:

- `Agent Template Reference — the structural specification you must conform to`
- `Bland Is Correct — the quality standard for your writing style`
- `Minimum Required Permissions — the security principle governing your permission grants`

**PURPOSE:** Directs the agent's reading attention. Without annotations, the agent reads each document with general attention. With annotations, the agent reads each document looking for specific knowledge to extract.

**HYPOTHESIS:** Purpose annotations may significantly improve knowledge extraction from context documents. An agent that reads "Bland Is Correct" knowing it contains "the quality standard for your writing style" will extract and internalize the relevant principles more effectively than one that reads the same document with only the title to guide it. However, annotations also risk biasing the reading -- the agent may only extract what the annotation said to look for, missing other relevant content. Test: do purpose annotations improve the application of context document knowledge in agent output?

**STABILITY:** experimental -- high potential leverage, but requires careful annotation design to avoid narrowing the agent's reading