# DISPATCHER Section Analysis — Control Surface Design

## Fundamental Nature: The Dispatch Instruction as Caller Programming

The dispatcher section is architecturally unique. Every other section renders INTO the agent's prompt — programming the agent's behavior. The dispatcher renders into a SKILL.md file — programming the CALLER's behavior regarding this agent. This is meta-architecture: the dispatcher section is an initialization document for the caller's interaction with the agent, which means it faces every problem the agent prompt itself faces (clarity, unambiguity, completeness) but for a different audience with different needs.

The caller may be an LLM autonomously dispatching agents. The dispatch instruction must therefore be as rigorous as an agent prompt: it is effectively a mini-prompt that teaches the caller a single skill (how to invoke this specific agent).

---

## Field-by-Field Analysis

### `agent_name`

**Raw data:**
- Agent 1: `"agent-builder"`
- Agent 2: `"interview-enrich-create-summary"`

**Purpose:** Machine-readable identifier used in the actual Task tool invocation. The caller needs this exact string to construct the dispatch call.

**Hypothesis:** This is a pure identifier — it appears verbatim in the rendered SKILL.md as the agent reference. It is not a display name; it is the invocation handle.

**Stability:** LOCKED. The agent_name is a foreign key into the agent registry. Changing it would break all callers that reference this agent.

**Rendering fragments:**

Fragment A — Section header identity:
```
# Agent: agent-builder
```

Fragment B — Invocation reference:
```
Invoke using skill: `agent-builder`
```

Fragment C — Combined:
```
# Dispatch: agent-builder
Skill name for Task tool invocation: `agent-builder`
```

**Design decision:** The name must appear both as document identity (so the caller can find/recognize the instruction) and as the literal invocation string (so the caller can construct the call). These are distinct uses of the same value.

---

### `agent_description`

**Raw data:**
- Agent 1: `"Creates new agent TOML definitions and include files from requirements and preparation packages, producing complete definitions ready for the pipeline."`
- Agent 2: `"Reads stripped interview exchanges sequentially and produces one-sentence contextual summaries capturing what each exchange signifies given all prior conversation."`

**Purpose:** Tells the caller WHEN to dispatch this agent. This is the decision-support text — given a task, the caller reads this to determine whether this agent is the right tool.

**Hypothesis:** This is the "job posting" for the agent. It answers: "What does this agent do?" The caller uses it for routing decisions. It should be concrete enough that a caller can match incoming work to this agent without ambiguity.

**Stability:** MEDIUM. The description tracks the agent's actual capability. It changes when the agent's scope changes, but should be stable within a version.

**Cross-section mirror:** This is likely identical or nearly identical to the agent's own identity description. The agent knows what it does; the caller also needs to know what it does. The question is whether the dispatcher description should be identical (single source) or tailored (caller-optimized phrasing).

**Rendering fragments:**

Fragment A — Purpose statement:
```
## Purpose
Creates new agent TOML definitions and include files from requirements
and preparation packages, producing complete definitions ready for the pipeline.
```

Fragment B — When-to-use framing:
```
## When to Dispatch
Use this agent when you have a preparation package containing requirements,
domain analysis, data shapes, and schema references that need to be converted
into a complete agent TOML definition with include files.
```

Fragment C — Capability summary:
```
## What This Agent Does
Creates new agent TOML definitions and include files from requirements
and preparation packages, producing complete definitions ready for the pipeline.

Dispatch this agent when you need to convert a preparation package into
a pipeline-ready agent definition.
```

**Design tension:** Fragment A is a label. Fragment B is decision support (tells the caller the triggering condition). Fragment C combines both. For an LLM caller, Fragment B or C is far more useful — it answers "should I dispatch this?" not just "what is this?"

---

### `dispatch_mode`

**Raw data:**
- Agent 1: `"full"`
- Agent 2: `"full"`

**Purpose:** Indicates how completely the agent handles its task. "full" means the agent takes input and produces complete output — no partial delegation, no continuation needed.

**Hypothesis:** This field distinguishes agents that do complete work from agents that might do partial work requiring caller follow-up. Both examples are "full," suggesting this is the common case. Other possible values might include "partial" (agent does a step, caller continues) or "advisory" (agent produces recommendations, caller acts).

**Stability:** HIGH. The dispatch mode is a fundamental architectural property of how the agent relates to the caller's workflow.

**Rendering fragment:**

Fragment A — Implicit (full mode as default, only render non-full):
```
(no rendering — "full" is the assumed default)
```

Fragment B — Explicit lifecycle note:
```
## Dispatch Lifecycle
This agent handles the complete task. No follow-up dispatch is needed
after successful completion.
```

Fragment C — Constraint form:
```
Dispatch mode: full — agent produces complete output, no continuation required.
```

**Design decision:** If "full" is the overwhelmingly common case, rendering it adds noise. If other modes exist, the absence of a mode note implies "full." This is a classic default-vs-explicit tension.

---

### `background_mode`

**Raw data:**
- Agent 1: `"allowed"` (agent-builder)
- Agent 2: `"forbidden"` (interview-enrich-create-summary)

**Purpose:** Tells the caller whether this agent CAN be dispatched as a background task. This is a critical dispatch constraint — it determines whether the caller can fire-and-forget or must wait.

**Hypothesis:** "forbidden" means the agent MUST run in the foreground — the caller must wait for completion before proceeding. This could be because the agent's output is needed immediately for the next step, or because the agent requires interactive resources. "allowed" means the caller MAY dispatch to background but is not required to.

**Stability:** HIGH. Background capability is an architectural property tied to the agent's resource usage patterns and output delivery mechanism.

**Rendering fragments:**

Fragment A — Constraint statement:
```
Background execution: ALLOWED — this agent may be dispatched as a background task.
```
```
Background execution: FORBIDDEN — this agent MUST run in the foreground.
Wait for completion before proceeding.
```

Fragment B — Integrated into invocation instructions:
```
## Invocation
You MAY dispatch this agent in the background using `run_in_background: true`.
```
```
## Invocation
You MUST dispatch this agent in the foreground. Do NOT use background execution.
```

Fragment C — Lifecycle-oriented:
```
## Execution Model
This agent supports background execution. You can dispatch it and continue
with other work. Check for completion before using results.
```
```
## Execution Model
This agent requires foreground execution. You must wait for it to complete
before continuing. Do not dispatch other work that depends on its output.
```

**Design tension:** Fragment A states a fact. Fragment B integrates it into the how-to. Fragment C explains the operational implication. For an LLM caller, Fragment C is most useful because it tells the caller what to DO differently based on this constraint. Fragment B is most actionable if the caller is constructing a literal tool call.

---

### `max_agents`

**Raw data:**
- Agent 1: `6` (agent-builder)
- Agent 2: `1` (interview-enrich-create-summary)

**Purpose:** The maximum number of parallel instances of this agent the caller should dispatch simultaneously. This is a concurrency constraint.

**Hypothesis:** max_agents=1 means strictly sequential — only one instance at a time. This implies the agent either has ordering requirements (summary agent reads "sequentially") or resource constraints. max_agents=6 means the caller can batch-dispatch up to 6 parallel instances for throughput.

**Stability:** MEDIUM. The max changes based on resource constraints, ordering requirements, and operational tuning. The structural presence of the field is stable; the value may be adjusted.

**Rendering fragments:**

Fragment A — Simple constraint:
```
Maximum parallel agents: 6
```
```
Maximum parallel agents: 1 (sequential only)
```

Fragment B — Operational guidance:
```
## Parallelism
You may dispatch up to 6 instances of this agent simultaneously.
When processing multiple preparation packages, batch them into groups of 6.
```
```
## Parallelism
This agent processes input sequentially. Dispatch exactly one instance at a time.
Do not batch or parallelize.
```

Fragment C — Combined with background:
```
## Dispatch Constraints
- Background: allowed
- Max parallel: 6
- Strategy: batch inputs into groups of up to 6, dispatch as background tasks,
  collect results when all complete.
```
```
## Dispatch Constraints
- Background: forbidden
- Max parallel: 1
- Strategy: dispatch one instance, wait for completion, then proceed.
```

**Design tension:** max_agents interacts strongly with background_mode. Together they define the dispatch STRATEGY. Fragment C shows that rendering them together produces more useful caller guidance than rendering them separately. This suggests these fields form a natural group.

**Emergent grouping:** `background_mode` + `max_agents` = **dispatch strategy**. These two fields together answer "how do I manage the lifecycle of dispatching this agent?" They should probably render as a unified block.

---

### `input_delivery`

**Raw data:**
- Agent 1: `"tempfile"`
- Agent 2: `"tempfile"`

**Purpose:** Tells the caller HOW to deliver input data to the agent. "tempfile" means the caller writes data to a temporary file and passes the path as a parameter.

**Hypothesis:** This is the input delivery mechanism. Both agents use tempfile, suggesting this is the primary (possibly only) delivery method. Other conceivable methods: inline (pass data as string parameter), stdin (pipe), reference (pass path to existing file).

**Stability:** HIGH for the field's existence. The delivery mechanism is a fundamental interface contract. The value "tempfile" appears to be a strong convention.

**Rendering fragments:**

Fragment A — Preparation instruction:
```
## Input Preparation
1. Write your input data to a temporary file
2. Pass the file path as the `tempfile` parameter
```

Fragment B — Detailed with format:
```
## Input Preparation
1. Prepare input as text format
2. Write to a temporary file (e.g., /tmp/agent-builder-input.txt)
3. Pass the absolute file path as the `tempfile` parameter
```

Fragment C — Integrated with format and description:
```
## Input
**What to prepare:** Preparation package containing requirements, domain analysis,
data shapes, and schema references
**Format:** text
**Delivery:** Write to a temporary file, pass path as `tempfile` parameter
```

**Design decision:** The delivery mechanism is tightly coupled with input_format and input_description — together they answer "what do I prepare, in what format, and how do I hand it over?" Fragment C shows the natural grouping.

---

### `input_format`

**Raw data:**
- Agent 1: `"text"`
- Agent 2: `"jsonl"`

**Purpose:** Tells the caller what format the input data must be in when written to the delivery mechanism (tempfile).

**Hypothesis:** This constrains the caller's data preparation step. "text" is unstructured — the caller writes whatever text is appropriate. "jsonl" is structured — the caller must produce newline-delimited JSON records conforming to an expected schema.

**Stability:** HIGH. The input format is a core interface contract. Changing it breaks all callers.

**Rendering fragments:**

Fragment A — Format specification:
```
Input format: text
```
```
Input format: JSONL (one JSON object per line)
```

Fragment B — With preparation guidance:
```
Write the preparation package as plain text to the tempfile.
```
```
Write stripped interview exchanges as JSONL to the tempfile.
Each line must be a valid JSON object containing the exchange data.
```

Fragment C — With schema hint:
```
Input format: JSONL
Each line: a JSON object with exchange_number, agent_question, and user_response fields.
```

**Design tension:** For structured formats (jsonl, json), the caller needs to know the SCHEMA of the records, not just the container format. input_format says "jsonl" but that's insufficient — the caller needs to know what fields each record contains. input_description partially covers this ("stripped interview exchanges with exchange number, agent question, and user response") but in prose form, not schema form.

---

### `input_description`

**Raw data:**
- Agent 1: `"Preparation package containing requirements, domain analysis, data shapes, and schema references"`
- Agent 2: `"Stripped interview exchanges with exchange number, agent question, and user response — no learned, threads, or insight fields"`

**Purpose:** Tells the caller WHAT the input data should contain — the semantic description of expected input content.

**Hypothesis:** This is the caller's guide to input preparation. It describes what data to gather/construct before dispatching. For the summary agent, it also specifies what to EXCLUDE ("no learned, threads, or insight fields"), which is a stripping instruction for the caller.

**Stability:** MEDIUM. Changes when the agent's input requirements change, but should be stable within a version.

**Rendering fragments:**

Fragment A — Descriptive paragraph:
```
Prepare stripped interview exchanges with exchange number, agent question,
and user response. Do NOT include learned, threads, or insight fields.
```

Fragment B — Structured requirements:
```
## Input Requirements
- Content: stripped interview exchanges
- Must include: exchange number, agent question, user response
- Must exclude: learned, threads, insight fields
- Format: JSONL (one exchange per line)
```

Fragment C — Checklist form:
```
## Input Checklist
[ ] Contains exchange_number for each exchange
[ ] Contains agent_question for each exchange
[ ] Contains user_response for each exchange
[ ] Does NOT contain learned field
[ ] Does NOT contain threads field
[ ] Does NOT contain insight field
[ ] Written as JSONL (one JSON object per line)
[ ] Saved to a temporary file
```

**Design tension:** Fragment A is natural language (easy to read, hard to verify). Fragment B is structured (scannable, verifiable). Fragment C is a checklist (most verifiable, most verbose). For an LLM caller, Fragment B hits the sweet spot — structured enough to be unambiguous, concise enough to not overwhelm.

**Emergent grouping:** `input_delivery` + `input_format` + `input_description` = **input specification**. These three fields together answer "what do I prepare, how do I format it, and how do I deliver it?" They form a natural rendering group.

---

### `parameters`

**Raw data — Agent 1:**
```toml
[[dispatcher.parameters]]
param_description = "Path to the preparation package"
param_name = "tempfile"
param_required = true
param_type = "path"
```

**Raw data — Agent 2:**
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

**Purpose:** Defines the exact parameters the caller must pass when invoking the agent via the Task tool. This is the invocation signature.

**Hypothesis:** Parameters are the literal arguments to the dispatch call. They define the interface contract at the invocation level. The `tempfile` parameter is universal (all tempfile-delivery agents have it). Additional parameters like `uid` carry metadata the agent needs but that isn't part of the input data itself.

**Stability:** HIGH. Parameters are the API contract. Adding parameters is backward-compatible (if optional); removing or renaming is breaking.

**Rendering fragments:**

Fragment A — Table format:
```
## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| tempfile | path | yes | Path to the JSONL tempfile containing stripped exchanges |
| uid | string | yes | Interview identifier used for output filename construction |
```

Fragment B — Invocation example:
```
## Invocation
Use the Task tool with skill `interview-enrich-create-summary`:

Arguments: tempfile=/path/to/exchanges.jsonl uid=interview-2024-001
```

Fragment C — Parameter documentation with invocation template:
```
## Parameters

**tempfile** (path, required)
Path to the JSONL tempfile containing stripped interview exchanges.

**uid** (string, required)
Interview identifier used for output filename construction.

## Example Invocation
Skill: interview-enrich-create-summary
Args: tempfile=/tmp/stripped_exchanges.jsonl uid=INT-2024-042
```

**Design tension:** The parameters serve dual purpose — they are documentation (what does each parameter mean?) AND invocation specification (how do I construct the call?). Fragment C serves both purposes. Fragment B is most actionable but lacks parameter detail. Fragment A is most scannable but doesn't show how to use the parameters in practice.

**Critical observation:** An LLM caller constructing a Task tool call needs to know the exact syntax. The rendering should include a concrete invocation template or example, not just parameter documentation.

---

### `output_format`

**Raw data:**
- Agent 1: `"text"`
- Agent 2: `"jsonl"`

**Purpose:** Tells the caller what format the agent's output will be in, so the caller knows how to parse/consume results.

**Hypothesis:** This is the output contract. The caller needs to know whether to expect structured data (jsonl, json) or unstructured text. This determines the caller's post-dispatch processing logic.

**Stability:** HIGH. Output format is a core interface contract.

**Rendering fragments:**

Fragment A — Simple statement:
```
Output format: JSONL
```

Fragment B — With consumption guidance:
```
## Output
The agent produces JSONL output. Each line is a valid JSON object
containing the enriched exchange with summary field added.
```

Fragment C — With handling instruction:
```
## Handling Results
The agent writes JSONL output. Parse each line as a JSON object.
Verify all lines are valid JSON before proceeding.
```

**Design tension:** output_format alone is insufficient for structured formats — the caller also needs to know the output schema (what fields? what types?). The current data doesn't include output schema information in the dispatcher section, which may be a gap or may be intentional (output schema documented elsewhere).

---

### `output_name_known`

**Raw data:**
- Agent 1: `"unknown"` (agent-builder)
- Agent 2: `"partially"` (interview-enrich-create-summary)

**Purpose:** Tells the caller whether the output filename is predictable before dispatch.

**Hypothesis:** "unknown" means the caller cannot predict what the output file will be named — it must discover the output location from the agent's return status. "partially" means some part of the filename is predictable (e.g., it uses the uid parameter) but not entirely. This affects the caller's ability to plan file handling before dispatch.

**Stability:** MEDIUM. This is a convenience/planning property that may change as naming conventions evolve.

**Rendering fragments:**

Fragment A — Discovery instruction:
```
Output filename: unpredictable — check agent's return status for output location.
```
```
Output filename: partially predictable — incorporates the `uid` parameter.
Check agent's return status for exact path.
```

Fragment B — Operational guidance:
```
## Output Location
The output filename is not known in advance. After the agent completes,
read its return status to discover where output was written.
```
```
## Output Location
The output filename incorporates the `uid` parameter you provide.
After completion, check return status for the exact output path.
```

Fragment C — Conditional handling:
```
## After Dispatch
Do NOT assume you know the output path. The agent's completion status
will include the output location. Read it from there.
```

**Design decision:** This field is about post-dispatch workflow. It tells the caller what to expect AFTER the agent finishes. It groups naturally with output_format and return_mode.

---

### `return_mode`

**Raw data:**
- Agent 1: `"status"`
- Agent 2: `"status"`

**Purpose:** Tells the caller what kind of return to expect from the agent upon completion.

**Hypothesis:** "status" means the agent returns a status indicator (success/failure) rather than the output data itself. The actual output is in files, not in the return value. Other possible modes might include "content" (output returned directly) or "reference" (path to output returned).

**Stability:** HIGH. The return mode is a fundamental interface contract.

**Rendering fragments:**

Fragment A — Return specification:
```
Return: status only (success or failure). Output is written to files, not returned.
```

Fragment B — Handling instruction:
```
## Handling Completion
The agent returns a status message (success or failure).
- On success: output files are ready at the reported location
- On failure: check the status message for error details
```

Fragment C — Combined with output:
```
## Results
- Return: status (success/failure)
- Output: written to files (format: JSONL)
- Output location: check return status message
- On success: proceed with output files
- On failure: diagnose from status message, do not retry without investigation
```

**Emergent grouping:** `output_format` + `output_name_known` + `return_mode` = **result specification**. These three fields together answer "what comes back, where is it, and how do I find it?"

---

## Structural Analysis: Natural Groupings

The dispatcher fields form clear functional groups based on what question they answer for the caller:

### Group 1: Identity & Routing
**Question:** "What is this agent and when should I use it?"
**Fields:** `agent_name`, `agent_description`
**Caller action:** Decide whether to dispatch this agent for the current task.

### Group 2: Input Specification
**Question:** "What data do I need to prepare and how do I deliver it?"
**Fields:** `input_description`, `input_format`, `input_delivery`
**Caller action:** Gather/construct/format input data, write to delivery mechanism.

### Group 3: Invocation Interface
**Question:** "How do I actually call this agent?"
**Fields:** `parameters` (name, type, required, description)
**Caller action:** Construct the Task tool call with correct arguments.

### Group 4: Dispatch Strategy
**Question:** "How do I manage the execution lifecycle?"
**Fields:** `dispatch_mode`, `background_mode`, `max_agents`
**Caller action:** Decide foreground vs background, sequential vs parallel, batching strategy.

### Group 5: Result Handling
**Question:** "What comes back and how do I consume it?"
**Fields:** `output_format`, `output_name_known`, `return_mode`
**Caller action:** Parse output, locate files, handle success/failure.

---

## Cross-Section Mirrors

Several dispatcher fields mirror data from other agent sections:

| Dispatcher Field | Mirrors | Notes |
|---|---|---|
| `agent_description` | identity.description | Same or similar text. Single-source question: should dispatcher reference identity, or is the dispatcher description independently authored for the caller's perspective? |
| `parameters` | input section parameters | Overlap — the agent's input specification and the dispatcher's parameter list describe the same interface from different sides. |
| `output_name_known` | output.name_known | Direct mirror of output section property. |
| `output_format` | output.format or enforcement output format | Mirror of the agent's own output specification. |
| `return_mode` | return.mode | Direct mirror of return section. |

**Design question:** Should the dispatcher section OWN these values, or should it REFERENCE them from their home sections? Duplication creates drift risk. References create coupling. The dispatcher's unique nature (different rendering target) argues for ownership — the dispatcher is a self-contained interface specification that happens to describe the same agent from the outside.

**Counter-argument:** If description changes in identity but not in dispatcher, the caller gets stale information. A reference-and-override model might work: dispatcher inherits from home section unless explicitly overridden.

---

## Dispatch Strategy Matrix

The combination of `background_mode` and `max_agents` produces distinct dispatch strategies:

| background_mode | max_agents | Strategy | Example |
|---|---|---|---|
| forbidden | 1 | Sequential foreground | interview-enrich-create-summary |
| allowed | N>1 | Parallel background batching | agent-builder (6) |
| forbidden | N>1 | Sequential foreground batching | (not in data — hypothetical) |
| allowed | 1 | Single background | (not in data — hypothetical) |

Each strategy requires fundamentally different caller instructions:

**Sequential foreground (forbidden/1):**
```
Dispatch one instance. Wait for completion. Process result.
If multiple inputs, process them one at a time in order.
```

**Parallel background (allowed/N>1):**
```
Batch inputs into groups of up to N. Dispatch each as a background task.
Continue with other work. Collect results when all complete.
If more than N inputs, dispatch N, wait for some to complete, dispatch more.
```

**This matrix drives the overall structure of the rendered SKILL.md.** The dispatch strategy isn't just one section — it shapes the entire instruction document.

---

## Rendering Architecture: Two Fundamentally Different Documents

The data reveals that a single SKILL.md template cannot serve both dispatch patterns well. Consider:

**Single-agent sequential dispatch (summary agent):**
- Simple invocation: one call, wait, done
- No batching logic needed
- No result collection from multiple agents
- Emphasis on input preparation and result consumption

**Multi-agent parallel dispatch (builder agent):**
- Complex invocation: batch planning, parallel dispatch, lifecycle management
- Batching logic is the core complexity
- Result collection from multiple agents
- Emphasis on orchestration strategy

**Design options:**

Option A — Single template with conditional sections:
```
# Dispatch: {agent_name}
## Purpose (always)
## Input (always)
## Parameters (always)
## Invocation (always, but content varies by strategy)
## Batching (only if max_agents > 1)
## Background Management (only if background_mode = allowed)
## Result Handling (always, but varies)
```

Option B — Strategy-driven templates:
```
Template: sequential-foreground (forbidden/1)
Template: parallel-background (allowed/N)
Template: sequential-batch (forbidden/N)
Template: single-background (allowed/1)
```

Option C — Modular composition:
```
Base: identity + input + parameters + result
Addon: batching-strategy (if max_agents > 1)
Addon: background-lifecycle (if background_mode = allowed)
Addon: sequential-ordering (if max_agents = 1 and ordering matters)
```

**Hypothesis:** Option C aligns best with the composability principles of the broader system. The dispatch instruction is composed from modules based on the field values, just as the agent prompt is composed from sections.

---

## The `dispatch_mode = "full"` Question

Both agents have `dispatch_mode = "full"`. This raises questions:

1. What other values exist? If only "full" exists, the field is noise.
2. If "partial" exists, what does the caller do differently? (Follow-up dispatch? Manual completion?)
3. If "advisory" exists, the output is recommendations, not artifacts — fundamentally different result handling.

**Hypothesis:** dispatch_mode is a high-level contract that determines the entire shape of the caller's workflow around this agent. "full" means fire-and-consume. Other modes would require the SKILL.md to document a multi-step caller workflow.

**Stability:** The field's existence is HIGH (it's a fundamental architectural property). The value "full" being the only observed value makes its current utility LOW but its future utility potentially HIGH.

---

## Parameter Analysis: The Invocation Signature

### Universal parameter: `tempfile`

Both agents have a `tempfile` parameter of type `path`, required. This is the delivery mechanism handle — it connects `input_delivery = "tempfile"` to the actual invocation.

**Observation:** The `tempfile` parameter is a STRUCTURAL consequence of `input_delivery = "tempfile"`. If delivery were "inline", there would be no tempfile parameter — the input would be a string parameter. This means the parameter list is partially DERIVED from other fields, not independently defined.

**Design question:** Should the tempfile parameter be auto-generated from `input_delivery = "tempfile"`, or explicitly declared? Auto-generation reduces redundancy but hides the interface. Explicit declaration is redundant but makes the invocation signature self-contained and inspectable.

**Hypothesis:** Explicit declaration is correct for the dispatcher because the SKILL.md must be self-contained — the caller should not need to understand the derivation rules to construct a correct invocation.

### Agent-specific parameters: `uid`

The summary agent has an additional `uid` parameter not present in the builder. This demonstrates that agents can have arbitrary additional parameters beyond the structural ones.

**Purpose of uid:** "Interview identifier used for output filename construction" — this is metadata that flows through the agent to affect output naming. The caller must provide it, but it doesn't affect input content.

**Design observation:** Parameters fall into two categories:
1. **Structural** (tempfile) — derived from delivery mechanism, universal
2. **Semantic** (uid) — agent-specific metadata required for processing

The rendering should probably distinguish these or at least ensure both are documented clearly enough that the caller knows what value to provide for each.

---

## Output Name Predictability

The `output_name_known` field has three observed values: "unknown", "partially", and (presumably) "known".

**Caller impact:**
- **known:** Caller can pre-plan file handling, check for output before agent reports completion
- **partially:** Caller can predict the pattern (e.g., `{uid}_summaries.jsonl`) but not the exact path
- **unknown:** Caller must wait for agent completion and read the output location from return status

**Rendering implication:** For "partially" and "unknown", the SKILL.md must include explicit instructions about how to discover the output location. For "known", the SKILL.md can include the exact output path template.

---

## Complete Rendering Hypothesis: SKILL.md Structure

Based on the analysis, a SKILL.md for a dispatcher renders these groups in order:

```
1. HEADER: Agent name + purpose (when to dispatch)
2. INPUT: What to prepare + format + delivery instructions
3. PARAMETERS: Complete invocation signature with types and descriptions
4. DISPATCH STRATEGY: Background/foreground + parallelism + batching guidance
5. INVOCATION EXAMPLE: Concrete Task tool call template
6. RESULT HANDLING: What to expect + where to find output + success/failure paths
```

**Key principle:** The document is ordered by the caller's workflow — decide, prepare, invoke, manage, consume. Each section maps to a phase of the caller's dispatch lifecycle.

**For sequential foreground (summary agent):**
Sections 4 and 5 are simple (one call, wait, done). The document emphasizes input preparation and result consumption.

**For parallel background (builder agent):**
Section 4 becomes the core complexity — batching strategy, lifecycle management, result collection. The document emphasizes orchestration.

---

## Open Design Questions

1. **Single source vs duplication for mirrored fields:** Should dispatcher own its description, or reference identity.description? Ownership is self-contained but risks drift. Reference is DRY but creates coupling across rendering targets.

2. **Structural parameter generation:** Should `tempfile` be auto-generated from `input_delivery`, or always explicitly declared? Self-containment argues for explicit; DRY argues for derived.

3. **Dispatch strategy as template selector vs conditional sections:** Does the strategy matrix (background x max_agents) select a template, or does a single template conditionally include sections?

4. **Output schema in dispatcher:** The current data includes output_format but no output schema. Should the dispatcher include schema information so the caller knows how to parse structured output?

5. **Error handling guidance:** The current data doesn't include failure modes or retry guidance. Should the dispatcher section include fields for error taxonomy and recovery instructions?

6. **The dispatch_mode question:** Is "full" the only mode, or are other modes planned? This affects whether dispatch_mode is structural or vestigial.

7. **Invocation syntax:** What is the exact Task tool syntax the caller uses? The rendering must produce a concrete, copy-pasteable invocation — but the exact syntax depends on the caller's tooling. Is the SKILL.md coupled to a specific invocation mechanism (Claude Code Task tool) or generic?
