# DISPATCHER Section — Control Surface Analysis

## Fundamental Nature: A Different Rendering Target

The dispatcher section is categorically distinct from every other section in the agent definition system. All other sections render INTO the agent prompt — they shape what the agent sees when it starts working. The dispatcher section renders into a SEPARATE DOCUMENT: the SKILL.md file that teaches a PARENT agent (or human operator) how to invoke this agent.

This means the dispatcher is an INTERFACE SPECIFICATION. Its audience is external callers, not the agent itself. Every design decision must be evaluated from the caller's perspective: "Can I correctly dispatch this agent given only the information in this section?"

---

## Field-by-Field Analysis

### `agent_name`

**Raw data:**
- Agent 1: `"agent-builder"`
- Agent 2: `"interview-enrich-create-summary"`

**Purpose:** Provides the exact identifier the caller uses when constructing the Task tool invocation. This is the `subagent_type` parameter — the machine-readable key that the dispatch system resolves to the correct agent prompt.

**Hypothesis:** This is a REFERENCE field, not a declaration. The agent_name here must exactly match the agent's canonical name as defined in its own definition. It exists in the dispatcher because the caller needs it without having to look it up elsewhere.

**Stability:** RIGID. This is a lookup key. If it doesn't match the actual agent definition filename/identifier, dispatch fails. No flexibility in representation.

**Fragment candidates:**

Fragment A — Bare identity:
```
agent_name → string
```
One atomic field. The dispatch target identifier.

Fragment B — Qualified identity:
```
agent_name → string
agent_version → string (optional)
```
Allows version-pinned dispatch. But no version data appears in the raw data, so this is speculative.

**Recommendation:** Fragment A. The raw data shows a single string with no versioning. Adding version would be inventing structure not present in the data.

---

### `agent_description`

**Raw data:**
- Agent 1: `"Creates new agent TOML definitions and include files from requirements and preparation packages, producing complete definitions ready for the pipeline."`
- Agent 2: `"Reads stripped interview exchanges sequentially and produces one-sentence contextual summaries capturing what each exchange signifies given all prior conversation."`

**Purpose:** Tells the CALLER what this agent does so they can decide WHEN to dispatch it. This is decision-support prose — the caller reads this to determine if this is the right agent for their current task.

**Hypothesis:** This is the same conceptual content as identity.description or frontmatter.description in other sections, but re-expressed for the caller's decision-making context. It answers "what does this agent do?" from the outside, not "who are you?" from the inside.

**Cross-section relationship:** This DUPLICATES information from the agent's own identity/description fields. The question is whether it should be a COPY of those fields, a REFERENCE to them, or independently authored for the caller's perspective.

**Stability:** MODERATE. The content carries the same semantic payload as other description fields but serves a different audience (caller vs agent). The phrasing could legitimately differ to optimize for each audience, or could be forced to match for consistency.

**Fragment candidates:**

Fragment A — Independent prose field:
```
agent_description → string (authored specifically for the caller)
```
Allows the description to be tuned for dispatch decision-making. "What does this agent do?" phrased for the person choosing whether to invoke it.

Fragment B — Reference to canonical description:
```
agent_description → reference to identity.description
```
Single source of truth. No divergence possible. But the caller-facing phrasing may suffer from being written for a different audience.

Fragment C — Layered description:
```
agent_description → string (short, one-line, for listing/scanning)
agent_description_detail → string (optional, longer, for understanding before dispatch)
```
Supports both scanning (which agent do I need?) and understanding (what exactly will it do?).

**Recommendation:** The raw data shows a single string that reads naturally as "what this agent does" from an external perspective. Fragment A is what exists. Fragment C is what might emerge if dispatch instructions need both terse and detailed descriptions, but there's no evidence of that need yet.

---

### `dispatch_mode`

**Raw data:**
- Agent 1: `"full"`
- Agent 2: `"full"`

**Purpose:** Tells the caller HOW to deliver the workload. "full" means send everything at once — the agent receives the complete input in a single invocation.

**Hypothesis:** The alternative to "full" would be "batch" or "streaming" — modes where the caller splits input and sends chunks. With only two data points and both showing "full", the alternative modes are implied by the field's existence but not demonstrated.

**Stability:** HIGH for the field's existence; UNCERTAIN for the enum values. Both examples show "full" so we can't observe the behavioral difference that other modes would create in the rendered dispatch instructions.

**Fragment candidates:**

Fragment A — Simple enum:
```
dispatch_mode → enum { "full", "batch" }
```
Binary: either send everything or split it up.

Fragment B — Richer delivery model:
```
dispatch_mode → enum { "full", "batch", "streaming" }
batch_size → integer (only when dispatch_mode = "batch")
```
Adds streaming for long-running progressive work. Batch carries a companion field.

Fragment C — Dispatch mode as a compound:
```
dispatch_mode → "full" | { mode: "batch", size: integer, overlap: integer }
```
Batch mode carries its own configuration as a nested structure.

**Recommendation:** Fragment A captures what the raw data shows. The existence of a mode field implies at least two values, and "batch" is the obvious counterpart to "full". But we only see "full" — designing the batch case would be speculative.

---

### `background_mode`

**Raw data:**
- Agent 1: `"allowed"` (creative task, up to 6 parallel agents)
- Agent 2: `"forbidden"` (sequential processing, exactly 1 agent)

**Purpose:** Tells the caller whether they MAY dispatch this agent as a background task. This directly affects the caller's dispatch lifecycle management: background agents run concurrently while the caller does other work; foreground agents block until completion.

**Hypothesis:** This is a CONSTRAINT on the caller, not a preference. "forbidden" means the agent REQUIRES foreground attention — perhaps because it needs interactive feedback, or because its output must be consumed immediately, or because its work is sequentially dependent on real-time state. "allowed" means the agent can safely run unsupervised.

**Cross-section relationship:** background_mode interacts strongly with max_agents. If max_agents > 1 and background_mode = "forbidden", the caller must run multiple foreground agents sequentially (or the combination is invalid). If background_mode = "allowed" and max_agents > 1, the caller can fan out.

**Stability:** HIGH. The enum values are clearly binary and the semantic distinction is fundamental to dispatch behavior.

**Fragment candidates:**

Fragment A — Binary enum:
```
background_mode → enum { "allowed", "forbidden" }
```
Clean, matches raw data exactly.

Fragment B — Ternary enum:
```
background_mode → enum { "required", "allowed", "forbidden" }
```
Adds "required" for agents that MUST run in background (perhaps long-running tasks that would block the caller unnecessarily).

Fragment C — Preference with override:
```
background_mode → enum { "allowed", "forbidden" }
background_preference → enum { "background", "foreground" } (optional, when mode = "allowed")
```
When allowed, suggests whether the caller SHOULD default to background or foreground.

**Recommendation:** Fragment A. The raw data shows a clean binary. Fragment B's "required" is interesting but speculative — no data point demonstrates it. Fragment C adds complexity without demonstrated need.

---

### `input_delivery`

**Raw data:**
- Agent 1: `"tempfile"`
- Agent 2: `"tempfile"`

**Purpose:** Tells the caller HOW to physically deliver input to the agent. "tempfile" means: write the input to a temporary file, then pass the file path as a parameter.

**Hypothesis:** The alternative to tempfile would be "inline" (pass input directly in the task prompt) or "directory" (point to a directory of files). Tempfile exists because some inputs are too large for inline delivery, or because the agent's prompt template expects a file path.

**Stability:** HIGH for the field's existence. Both examples show tempfile, so like dispatch_mode, the alternatives are implied but not demonstrated.

**Fragment candidates:**

Fragment A — Simple enum:
```
input_delivery → enum { "tempfile", "inline", "directory" }
```
Three delivery mechanisms covering the obvious cases.

Fragment B — Delivery with format coupling:
```
input_delivery → enum { "tempfile", "inline" }
```
Just two modes. Directory would be a special case of tempfile (the path points to a directory).

Fragment C — Compound delivery:
```
input_delivery → { method: "tempfile" | "inline" | "directory", cleanup: "caller" | "agent" | "auto" }
```
Adds cleanup responsibility. Who deletes the tempfile?

**Recommendation:** Fragment A or B. The raw data only shows tempfile. The cleanup question (Fragment C) is operationally important but not present in the data — it may be handled by convention rather than declaration.

---

### `input_format`

**Raw data:**
- Agent 1: `"text"` (preparation package)
- Agent 2: `"jsonl"` (structured records)

**Purpose:** Tells the caller what format the input file must be in. The caller must prepare the input in this exact format before delivery.

**Hypothesis:** This is a CONTRACT field. The agent expects this format; delivering a different format will cause failure. It constrains the caller's input preparation step.

**Stability:** HIGH. Format is a mechanical requirement. The enum values are well-understood data formats.

**Fragment candidates:**

Fragment A — Simple enum:
```
input_format → enum { "text", "jsonl", "json", "toml", "csv" }
```
Covers common data formats.

Fragment B — Format with schema:
```
input_format → enum { "text", "jsonl", "json", "toml" }
input_schema → path (optional, when format is structured)
```
When format is jsonl/json, a schema reference tells the caller exactly what structure to produce.

Fragment C — Bare string:
```
input_format → string
```
No enum constraint. Freeform format declaration.

**Recommendation:** Fragment A captures what the raw data shows. Fragment B is compelling because structured formats (jsonl, json) benefit from schema references, but no schema paths appear in the raw data. The workspace's schema-first philosophy (schemas/*.schema.json) suggests Fragment B may be the right evolution, but it's not present yet.

---

### `input_description`

**Raw data:**
- Agent 1: `"Preparation package containing requirements, domain analysis, data shapes, and schema references"`
- Agent 2: `"Stripped interview exchanges with exchange number, agent question, and user response — no learned, threads, or insight fields"`

**Purpose:** Tells the caller WHAT to put in the input. This is semantic documentation — what the data represents, what fields to include, what to exclude.

**Hypothesis:** This is the most critical field for correct dispatch. A caller who gets the format right but the content wrong will produce a technically valid but semantically useless invocation. The description must be precise enough for an LLM caller to construct correct input autonomously.

**Stability:** MODERATE. The content is highly agent-specific. The field's existence is stable; its adequacy for autonomous dispatch is the design question.

**Fragment candidates:**

Fragment A — Single prose field:
```
input_description → string
```
Free-form description. Flexible, human-readable, but potentially ambiguous for LLM callers.

Fragment B — Structured input specification:
```
input_description → string (semantic description)
input_fields → array of { name, type, required, description } (when structured format)
```
Adds field-level documentation for structured formats. An LLM caller can mechanically construct correct records.

Fragment C — Example-augmented description:
```
input_description → string
input_example → string (optional, a concrete example of valid input)
```
Shows rather than tells. An LLM caller can pattern-match against the example.

**Recommendation:** Fragment A is what exists. Fragment B or C would improve autonomous dispatch reliability. Agent 2's description already reads like a field specification ("exchange number, agent question, and user response — no learned, threads, or insight fields") — it's trying to be Fragment B within the constraints of Fragment A.

---

### `max_agents`

**Raw data:**
- Agent 1: `6` (creative task, parallel work)
- Agent 2: `1` (sequential processing)

**Purpose:** Tells the caller the MAXIMUM number of concurrent instances they may dispatch. This is a hard ceiling, not a suggestion.

**Hypothesis:** max_agents encodes a fundamental constraint about the agent's work. max_agents=1 means the work is inherently sequential or requires exclusive access to something. max_agents>1 means the work can be parallelized — but the caller must handle work distribution.

**Cross-section interaction:** max_agents interacts with dispatch_mode and background_mode:
- max_agents=1 + background_mode="forbidden" → strictly sequential, foreground, single invocation
- max_agents=6 + background_mode="allowed" → fan-out pattern, caller manages parallel dispatch
- max_agents>1 + dispatch_mode="full" → each agent gets the full input? Or is the caller expected to partition?

This last question is unresolved. If dispatch_mode="full" and max_agents=6, does each of the 6 agents receive the same full input (redundant parallel processing), or does the caller split the input into 6 parts? The raw data doesn't clarify this.

**Stability:** HIGH for the field. The integer value is unambiguous.

**Fragment candidates:**

Fragment A — Simple integer:
```
max_agents → integer (minimum 1)
```
Clean, matches raw data.

Fragment B — Range:
```
min_agents → integer (minimum 1, default 1)
max_agents → integer (minimum 1)
```
Adds a floor. Some agents might require at least N parallel instances.

Fragment C — Concurrency model:
```
max_agents → integer
parallelism_model → enum { "independent", "partitioned", "redundant" }
```
Clarifies whether multiple agents work on independent partitions of the input, or all process the same input redundantly.

**Recommendation:** Fragment A matches the raw data. Fragment C addresses a genuine ambiguity (what does max_agents=6 mean with dispatch_mode="full"?) but introduces complexity not present in the data. The rendered dispatch instructions would need to resolve this ambiguity through prose, not schema.

---

### `output_format`

**Raw data:**
- Agent 1: `"text"` (definitions, creative output)
- Agent 2: `"jsonl"` (structured records)

**Purpose:** Tells the caller what format to expect from the agent's output. The caller must be prepared to consume this format.

**Stability:** HIGH. Mirrors input_format in structure.

**Fragment candidates:** Same as input_format. Fragment A (enum) is sufficient.

---

### `output_name_known`

**Raw data:**
- Agent 1: `"unknown"` (creative output, filenames unpredictable)
- Agent 2: `"partially"` (some filenames predictable from input parameters)

**Purpose:** Tells the caller whether they can PREDICT output filenames before dispatch. This affects post-dispatch handling: if filenames are known, the caller can pre-configure downstream processing. If unknown, the caller must discover filenames after completion.

**Hypothesis:** This is a ternary: "known" (caller knows exact filenames), "partially" (caller can predict some but not all), "unknown" (caller must discover all filenames post-completion). The "partially" case for Agent 2 likely means the uid parameter is used in filename construction — the caller can predict the pattern but not the exact names.

**Stability:** MODERATE. The field represents a real operational distinction, but the ternary values feel like they could collapse. "partially" is vague — how much can the caller predict?

**Fragment candidates:**

Fragment A — Ternary enum:
```
output_name_known → enum { "known", "partially", "unknown" }
```
Matches raw data exactly.

Fragment B — Known with pattern:
```
output_name_known → enum { "known", "partially", "unknown" }
output_name_pattern → string (optional, template showing how names are constructed)
```
When "partially" or "known", the pattern tells the caller how to predict filenames. E.g., `"{uid}_summaries.jsonl"`.

Fragment C — Binary with explanation:
```
output_name_predictable → boolean
output_name_notes → string (optional, when predictable, explains the pattern)
```
Collapses ternary to binary. Either you can predict or you can't. Notes explain partial cases.

**Recommendation:** Fragment A is what exists. Fragment B adds genuine value — when output_name_known is "partially", the caller needs to know WHICH parts are predictable. The pattern template would make this actionable. But it's not in the raw data.

---

### `return_mode`

**Raw data:**
- Agent 1: `"status"` (returns SUCCESS/FAILURE)
- Agent 2: `"status"` (returns SUCCESS/FAILURE)

**Purpose:** Tells the caller what the agent's return value represents. "status" means the agent returns a completion status (SUCCESS/FAILURE), not the content itself. The content is in the output files.

**Hypothesis:** The alternative to "status" would be "content" (the agent returns the actual output in its response) or "reference" (the agent returns a path to the output). "status" implies the caller must look elsewhere for the actual output.

**Cross-section relationship:** return_mode connects to the return section of the agent's own definition. It's the external-facing summary of what the agent's return behavior looks like to the caller.

**Stability:** HIGH for the field. Both examples show "status", so alternatives are inferred, not observed.

**Fragment candidates:**

Fragment A — Simple enum:
```
return_mode → enum { "status", "content", "reference" }
```
Three obvious modes: just status, actual content, or a pointer to content.

Fragment B — Mode with structure:
```
return_mode → enum { "status", "content", "reference" }
return_status_values → array of string (when "status", the possible values)
```
Documents what status values to expect. E.g., ["SUCCESS", "FAILURE", "PARTIAL"].

**Recommendation:** Fragment A. Fragment B is useful but potentially over-specified — if all agents return SUCCESS/FAILURE, the values don't need per-agent documentation.

---

### `parameters` (Compound Array)

**Raw data:**

Agent 1:
```toml
[[dispatcher.parameters]]
param_description = "Path to the preparation package"
param_name = "tempfile"
param_required = true
param_type = "path"
```

Agent 2:
```toml
[[dispatcher.parameters]]
param_description = "Path to the JSONL tempfile containing stripped interview exchanges"
param_name = "tempfile"
param_required = true
param_type = "path"

[[dispatcher.parameters]]
param_description = "Interview identifier used for output filename construction"
param_name = "uid"
param_required = true
param_type = "string"
```

**Purpose:** Defines the INVOCATION SIGNATURE — the exact parameters the caller must provide when dispatching this agent. This is the most mechanically critical part of the dispatcher: if the caller gets parameters wrong, the invocation fails.

**Hypothesis:** Parameters are the dispatch contract. Each parameter has a name (the key to pass), a type (what kind of value), a description (what it means), and a required flag (whether omitting it is valid). This is essentially a function signature for the agent.

**Observations:**
- `param_name` is the key used in the invocation. "tempfile" appears in both agents as the standard input delivery parameter.
- `param_type` constrains the value. "path" means a filesystem path; "string" means arbitrary text.
- `param_required` is boolean. Both examples show only required=true parameters.
- `param_description` is caller-facing documentation explaining what to pass.
- Agent 1 has 1 parameter; Agent 2 has 2. The parameter count varies by agent.
- The "tempfile" parameter connects directly to input_delivery="tempfile" — it's the mechanism for the delivery method.

**Stability:** HIGH. Parameters are a well-understood concept. The four sub-fields (name, type, required, description) are the minimum viable parameter specification.

**Fragment candidates:**

Fragment A — Flat parameter tuple:
```
parameters → array of {
  param_name → string
  param_type → enum { "path", "string", "integer", "boolean" }
  param_required → boolean
  param_description → string
}
```
Matches raw data exactly. Simple, clear, sufficient.

Fragment B — Parameter with default:
```
parameters → array of {
  param_name → string
  param_type → enum { "path", "string", "integer", "boolean" }
  param_required → boolean
  param_default → any (optional, when required=false)
  param_description → string
}
```
Adds defaults for optional parameters. No optional parameters appear in the data, so this is forward-looking.

Fragment C — Parameter with validation:
```
parameters → array of {
  param_name → string
  param_type → enum { "path", "string", "integer", "boolean" }
  param_required → boolean
  param_description → string
  param_pattern → string (optional, regex validation for strings)
  param_must_exist → boolean (optional, for paths — must the file exist before dispatch?)
}
```
Adds validation hints. For path parameters, knowing whether the file must pre-exist is operationally important (tempfiles are created by the caller, so yes).

**Recommendation:** Fragment A captures the raw data. Fragment C's `param_must_exist` is genuinely useful for path parameters — the caller needs to know whether to create the file before dispatch (input tempfiles) or expect it after (output paths). But it's not in the data.

---

## Structural Analysis: How Fields Compose Into Dispatch Instructions

The dispatcher section is not just a bag of fields — it's a specification that renders into PROSE INSTRUCTIONS. The rendered SKILL.md must guide a caller through a dispatch sequence. The fields compose into these instruction phases:

### Phase 1: Decision — "Should I dispatch this agent?"
**Fields used:** agent_name, agent_description
**Rendered as:** A description block that helps the caller decide if this agent fits their current need.

### Phase 2: Input Preparation — "What do I need to prepare?"
**Fields used:** input_format, input_description, input_delivery, parameters
**Rendered as:** Step-by-step instructions for preparing the input. For tempfile delivery: create a tempfile, write data in the specified format, note the path. Parameter documentation tells the caller what else to gather.

### Phase 3: Invocation — "How do I call it?"
**Fields used:** agent_name, parameters, dispatch_mode, max_agents, background_mode
**Rendered as:** The actual Task tool invocation template. Shows the caller the exact tool call to make, with parameter placeholders.

### Phase 4: Lifecycle Management — "What happens during execution?"
**Fields used:** background_mode, max_agents
**Rendered as:** Instructions for managing the dispatch lifecycle. Background-allowed agents can be fire-and-forget (with later result collection). Foreground-forbidden agents must be waited on. Multi-agent dispatches need coordination logic.

### Phase 5: Result Handling — "What do I do when it finishes?"
**Fields used:** return_mode, output_format, output_name_known
**Rendered as:** Instructions for consuming the agent's output. Status return means check SUCCESS/FAILURE first. Known output names can be read immediately. Unknown names require discovery.

---

## Cross-Section Relationships

### Duplication with Identity/Frontmatter
- `agent_description` ≈ `identity.description` ≈ `frontmatter.description`
- These serve different audiences but carry the same semantic content. The design must decide: single source with rendering variants, or independent authoring per audience.

### Mirror of Input Section
- `input_format` mirrors the agent's own understanding of its input format
- `input_description` mirrors the agent's input documentation
- `parameters` mirrors the agent's parameter handling
- These MUST be consistent. The dispatcher tells the caller what to send; the input section tells the agent what to expect. Divergence = failure.

### Mirror of Output/Return Sections
- `output_format` mirrors the agent's output format
- `output_name_known` mirrors the agent's output naming behavior
- `return_mode` mirrors the agent's return format

### The Consistency Problem
Every mirrored field creates a consistency risk. If the dispatcher says input_format="jsonl" but the agent's input section expects "json", the invocation will fail. Options:
1. **Derived fields** — the dispatcher section is auto-generated from the agent's own sections (single source of truth)
2. **Validated consistency** — both are independently authored but validation catches divergence
3. **Accepted duplication** — both are independently authored and consistency is the author's responsibility

---

## Key Design Tensions

### Tension 1: Declarative Data vs. Rendered Prose

The dispatcher fields are declarative. But the output (SKILL.md) is prose instructions. Something must translate declarations into instructions. The rendering logic must:
- Convert `background_mode="forbidden"` into "Do NOT dispatch this agent in the background. Wait for completion."
- Convert `max_agents=6` into "You may dispatch up to 6 parallel instances."
- Convert parameter arrays into "Pass the following parameters:" formatted lists.

This rendering is non-trivial. Different field combinations produce qualitatively different instruction structures:
- Single-agent foreground dispatch: simple linear instructions
- Multi-agent background dispatch: loop/fan-out instructions with coordination
- Batch dispatch with partitioning: splitting logic instructions

### Tension 2: Sufficient Specification vs. Over-specification

How much must the dispatcher declare for correct dispatch? The raw data shows a lean specification. But correct autonomous dispatch may require:
- Error handling instructions (what if the agent fails?)
- Retry policy (should the caller retry on failure?)
- Timeout expectations (how long should the caller wait?)
- Output location (where does the agent write its output?)
- Cleanup responsibilities (who deletes tempfiles?)

None of these are in the raw data. Either they're handled by convention, or they're gaps.

### Tension 3: Caller Variability

The dispatcher targets "a parent agent or human operator." These are very different callers:
- An LLM caller needs mechanical precision: exact parameter names, exact tool call syntax
- A human caller needs conceptual understanding: what the agent does, what to expect
- The SKILL.md must serve both, which may mean layered information (quick-reference invocation template + detailed explanation)

---

## Structural Shape of the Section

The dispatcher section has a two-level structure:

**Level 1: Scalar fields** (11 fields)
```
agent_name          → string (identifier)
agent_description   → string (prose)
dispatch_mode       → enum (full | batch)
background_mode     → enum (allowed | forbidden)
input_delivery      → enum (tempfile | inline | ...)
input_format        → enum (text | jsonl | json | ...)
input_description   → string (prose)
max_agents          → integer (>= 1)
output_format       → enum (text | jsonl | json | ...)
output_name_known   → enum (known | partially | unknown)
return_mode         → enum (status | content | reference)
```

**Level 2: Parameter array** (0..N compound elements)
```
parameters → array of {
  param_name        → string
  param_type        → enum (path | string | integer | boolean)
  param_required    → boolean
  param_description → string
}
```

This is a flat section with one compound array. No nesting beyond the parameter elements. The structural complexity is LOW — the rendering complexity is where the real work lives.

---

## What Distinguishes Agent 1 from Agent 2

| Dimension | Agent 1 (agent-builder) | Agent 2 (interview-enrich-create-summary) |
|-----------|------------------------|------------------------------------------|
| Parallelism | Up to 6 agents | Exactly 1 agent |
| Background | Allowed | Forbidden |
| Input format | text (unstructured) | jsonl (structured records) |
| Parameters | 1 (tempfile path) | 2 (tempfile path + uid string) |
| Output predictability | Unknown | Partially known |
| Dispatch character | Fan-out creative work | Sequential precise processing |

These two agents represent opposite ends of a dispatch spectrum:
- **Agent 1** is a "scatter" dispatch: send preparation packages to multiple builders, let them work in background, collect results.
- **Agent 2** is a "pipeline" dispatch: send structured data to exactly one processor, wait for it to finish, use its output immediately.

The rendered SKILL.md for each would look very different:
- Agent 1's SKILL.md would include parallelization instructions, background management, result collection from multiple agents.
- Agent 2's SKILL.md would be linear: prepare input, invoke once, wait, collect output.

---

## Open Questions

1. **Where does the agent write its output?** Neither agent's dispatcher specifies an output path or directory. Is this passed as a parameter? Derived from input path? Fixed by convention?

2. **Who cleans up tempfiles?** The caller creates them, but who deletes them? This is an operational detail not captured in the data.

3. **What does max_agents mean with dispatch_mode="full"?** If each of 6 agents gets the "full" input, are they doing the same work redundantly? Or is "full" per-agent (each gets its own full workload, prepared separately by the caller)?

4. **How does "partially" known output names work?** Agent 2 says output names are "partially" known. The uid parameter is used for filename construction — but what's the template? The caller needs this to find the output.

5. **Is return_mode always "status"?** Both examples show status. If content return exists, how does it change the dispatch lifecycle?

6. **Retry and error handling?** Neither agent's dispatcher addresses failure recovery. Is this the caller's responsibility entirely, or should the dispatcher declare retry policy?

---

## Summary of Fragment Inventory

| Field | Recommended Fragment | Alternative Worth Considering |
|-------|---------------------|-------------------------------|
| agent_name | Bare string | None — this is a lookup key |
| agent_description | Independent prose string | Layered (short + detail) |
| dispatch_mode | Simple enum (full, batch) | With batch_size companion |
| background_mode | Binary enum (allowed, forbidden) | Ternary with "required" |
| input_delivery | Simple enum (tempfile, inline) | With cleanup responsibility |
| input_format | Simple enum | With schema reference |
| input_description | Single prose string | With field-level spec or example |
| max_agents | Simple integer | With parallelism model |
| output_format | Simple enum | Same as input_format |
| output_name_known | Ternary enum | With name pattern template |
| return_mode | Simple enum (status, content) | With expected status values |
| parameters | 4-field compound (name, type, required, description) | With default, pattern, must_exist |

The raw data supports lean fragments throughout. Every "alternative worth considering" adds genuine operational value but is not evidenced in the current data. The design question is: how much to invest in the dispatcher's expressiveness now vs. letting needs emerge from actual dispatch failures.
