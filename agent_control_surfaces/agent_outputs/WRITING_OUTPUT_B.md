# WRITING_OUTPUT Section Analysis

## FIRST PRINCIPLES

### What This Section Accomplishes

The `writing_output` section is the **mechanical instruction set** for agents that have a dedicated output tool. It answers a single question with zero ambiguity: "How exactly do you invoke the tool that writes your results?"

This is fundamentally different from every other section in the composition system. Other sections shape judgment, priorities, processing approach. This section shapes **motor behavior** — the precise keystrokes, the exact syntax, the literal characters the agent must produce. It is a recipe, not a philosophy.

### Why It Is Conditional

The section's conditionality on `has_output_tool = true` creates a **binary behavioral fork**:

- **When absent**: The agent writes output using standard filesystem tools (Write, Edit). The agent chooses filenames, formats, locations. Output behavior is governed by general instructions and guardrails.
- **When present**: The agent MUST use the named tool. No alternatives. The tool handles validation, append semantics, schema enforcement. The agent's job is to produce correct invocations — nothing else.

This fork is the sharpest behavioral division in the entire system. An agent with `writing_output` has its output behavior fully prescribed. An agent without it has output behavior that emerges from instruction interpretation.

### The Behavioral Effect of Exact Templates

The `invocation_display` field contains a literal code block — not a description of how to invoke, but the exact characters to reproduce. This has a specific cognitive effect on the LLM agent: it converts output writing from a **generative task** (figure out the right command) to a **substitution task** (fill in the blanks in this template). This dramatically reduces error surface. The agent cannot invent novel invocation syntax because the correct syntax is provided verbatim.

### How Batch Discipline Changes Processing

`batch_size = 20` transforms the agent from a one-at-a-time processor into a **batch accumulator**. This changes the processing rhythm fundamentally:

- Without batching: process one input, write one output, repeat.
- With batching: process up to 20 inputs, accumulate results in memory, write all 20 in a single tool invocation, then proceed.

Batching affects quality because it forces the agent to **hold state** — to maintain a working set of processed results before committing them. This creates natural checkpoints and makes the agent's processing more deliberate. It also reduces tool invocation overhead, which matters for throughput.

---

## SECTION-LEVEL STRUCTURAL ANALYSIS

### STRUCTURAL: Section Presence Gate

The entire `writing_output` section is gated on `has_output_tool = true`. This is the most important structural fact about it.

**What the agent needs to understand**: When this section exists, it is MANDATORY. The agent must use the specified tool. When it does not exist, the agent uses standard tools and this entire behavioral module is inactive.

#### Fragments

**presence_mandate**
- Alternative A: "You have a dedicated output tool. Every result you produce MUST be written using this tool. Standard file operations are not permitted for output."
- Alternative B: "Your output is written through a specialized tool described below. This tool is not optional — it is the only authorized method for writing your results."
- Alternative C: "The following tool is your output mechanism. Using any other method to write results is a violation. All output goes through this tool, every time, no exceptions."
- Alternative D: "Output flows through one channel: the tool specified here. You do not write files directly. You do not choose alternative tools. You invoke this tool."
- PURPOSE: Establish that the tool is mandatory, not a convenience option. Agents must not fall back to Write/Edit for output.
- HYPOTHESIS: Without explicit mandate language, agents will sometimes use standard tools when the dedicated tool would require more effort (e.g., handling validation errors). The mandate prevents this escape hatch.
- STABILITY: LOCKED. The mandate is binary — use the tool or don't. There is no soft version of this.

**absence_explanation**
- Alternative A: (No text — simply omit the section entirely for non-output-tool agents)
- Alternative B: "You write output using standard file tools. No dedicated output tool is configured for this agent."
- Alternative C: (Handled by conditional rendering — section not emitted, no explanation needed)
- PURPOSE: Determine whether non-output-tool agents need to be told they DON'T have an output tool, or whether silence is sufficient.
- HYPOTHESIS: Silence is sufficient. An agent that has never been told about an output tool will not look for one. Explicit "you don't have this" statements waste tokens and create confusion.
- STABILITY: STABLE toward Alternative A/C. Omission is cleaner than negation.

---

## FIELD: tool_name

TYPE: string (tool binary name)
VALUES: absent (agent-builder) / `"append_interview_summaries_record"` (interview-enrich-create-summary)

### What the agent needs to understand

This is the exact name of the binary/tool the agent will invoke. It is a literal identifier — not a description, not a category. The agent must reproduce this name exactly in every invocation.

### Fragments

**tool_identity**
- Alternative A: "Your output tool is `append_interview_summaries_record`."
- Alternative B: "Write all results using the tool: `append_interview_summaries_record`"
- Alternative C: "Tool: `append_interview_summaries_record` — this is the only tool you use for writing output."
- PURPOSE: Introduce the tool by exact name so the agent can reference it in invocations.
- HYPOTHESIS: The tool name appears in `invocation_display` already, so this field's primary role is as a **semantic anchor** — giving the agent a named concept to associate with the invocation template. Without it, the template is an anonymous code block.
- STABILITY: LOCKED. The name is a literal. Only the framing prose varies.

**Cross-section dependency**: `critical_rules` in the rules section reinforces tool usage mandate. The tool name here must match the tool name referenced there.

---

## FIELD: invocation_display

TYPE: multi-line string (literal code template with placeholders)
VALUES: absent (agent-builder) / heredoc template (interview-enrich-create-summary)

```
append_interview_summaries_record {name} <<'EOF'
{json_data}
EOF
```

### What the agent needs to understand

This is the **exact syntax** to reproduce. The placeholders `{name}` and `{json_data}` are the only parts the agent fills in — everything else is literal. The heredoc syntax (`<<'EOF'` ... `EOF`) is a shell construct that passes multi-line content to the tool.

This is the most mechanical field in the entire composition system. It requires zero interpretation and maximum fidelity.

### Fragments

**template_introduction**
- Alternative A: "Invoke the tool exactly as shown. Replace `{name}` with the output filename and `{json_data}` with the JSON content. Everything else is literal:"
- Alternative B: "Use this exact invocation pattern. The only parts you change are the placeholders — `{name}` becomes the filename, `{json_data}` becomes your output. Reproduce all other characters exactly:"
- Alternative C: "Your invocation template (copy exactly, substituting only the marked placeholders):"
- Alternative D: "Every write follows this pattern precisely. `{name}` and `{json_data}` are variables you fill in. The heredoc syntax, tool name, and structure are fixed:"
- PURPOSE: Frame the template as a literal to copy, not a suggestion to adapt.
- HYPOTHESIS: LLM agents are prone to "improving" code they're shown — adding flags, changing syntax, reformatting. Explicit "exactly as shown" language suppresses this tendency.
- STABILITY: MEDIUM-HIGH. The intent (exact reproduction) is locked. The framing words can vary.

**heredoc_explanation**
- Alternative A: (No explanation — assume the agent understands heredoc syntax)
- Alternative B: "The `<<'EOF'` syntax passes everything between `<<'EOF'` and the closing `EOF` as input to the tool. Single quotes around EOF prevent variable expansion."
- Alternative C: "This uses heredoc syntax to pass multi-line JSON to the tool. The `EOF` markers delimit the content block."
- Alternative D: "Heredoc format: everything between the opening `<<'EOF'` and the closing `EOF` on its own line is passed as the tool's input data."
- PURPOSE: Determine whether heredoc syntax needs explanation or can be assumed.
- HYPOTHESIS: LLM agents understand heredoc syntax from training data. Explicit explanation is unnecessary and may even be counterproductive (suggesting the syntax is unusual or tricky). However, a minimal note prevents rare failures where the agent closes the heredoc incorrectly.
- STABILITY: LOW. This is a judgment call about how much the agent already knows. Could go either way.

**placeholder_mapping**
- Alternative A: "Replace `{name}` with the constructed filename. Replace `{json_data}` with the JSON record."
- Alternative B: "`{name}` = output filename (see name_pattern below). `{json_data}` = the JSON object you've constructed for this batch."
- Alternative C: "Placeholders: `{name}` maps to the filename from name_pattern. `{json_data}` maps to valid JSON matching the output schema."
- PURPOSE: Explicitly map each placeholder to its data source.
- HYPOTHESIS: Placeholder mapping is critical because the agent must know WHERE each value comes from — name from pattern construction, data from processing output. Without mapping, the agent might confuse which placeholder gets which value.
- STABILITY: MEDIUM. The mapping is fixed (name→filename, json_data→content), but the explanation style varies.

**Cross-section dependencies**:
- `name_pattern` → provides the template for constructing `{name}`
- `input.parameters` → provides the values (e.g., interview-id) used in name_pattern
- `schema_path` → the JSON in `{json_data}` must conform to this schema
- `invocation_variant` → determines whether `{name}` is needed (see below)

---

## FIELD: invocation_variant

TYPE: string enum
VALUES: absent (agent-builder) / `"with-name"` (interview-enrich-create-summary)

### What the agent needs to understand

This field signals which invocation shape to use. `"with-name"` means the tool requires a filename argument before the heredoc. Other variants (e.g., a hypothetical `"stdin-only"`) might not require a name argument.

### Fragments

**variant_explanation**
- Alternative A: (Implicit — the invocation_display already shows the shape, so variant is metadata for the renderer, not the agent)
- Alternative B: "This tool requires a filename argument before the data block."
- Alternative C: "Invocation shape: tool name, then filename, then heredoc data."
- PURPOSE: Determine whether the agent needs to understand the variant concept or whether it's purely a composition-system internal.
- HYPOTHESIS: The agent does NOT need to understand this field. It is metadata for the galdr renderer — telling it which invocation_display template to use. Once the template is rendered into the agent prompt, the variant field has served its purpose. The agent just follows the template.
- STABILITY: STABLE toward Alternative A. This is a renderer field, not an agent field.

---

## FIELD: batch_size

TYPE: integer
VALUES: absent (agent-builder) / `20` (interview-enrich-create-summary)

### What the agent needs to understand

Process up to 20 items, then write them all in one invocation. This is not a suggestion — it is the processing rhythm. The agent accumulates results and writes in batches.

### Fragments

**batch_discipline**
- Alternative A: "Process items in batches of 20. After processing 20 items (or reaching the end of input), write all results in a single tool invocation."
- Alternative B: "Accumulate up to 20 processed results before writing. Each tool invocation writes one batch. If fewer than 20 items remain, write what you have."
- Alternative C: "Batch size: 20. Process twenty items, write them together, then process the next twenty. Final batch may be smaller."
- Alternative D: "You write in batches of 20. This means: process 20 inputs → construct 20 JSON records → write all 20 in one tool call → repeat until done."
- PURPOSE: Establish the accumulate-then-write rhythm and handle the edge case (final batch < 20).
- HYPOTHESIS: Explicit batch discipline prevents two failure modes: (1) writing after every single item (inefficient, ignores batch_size), and (2) trying to accumulate ALL items before writing (risks context overflow on large inputs).
- STABILITY: HIGH. The number varies per agent, but the concept (accumulate N, write, repeat) is fixed.

**batch_quality_implication**
- Alternative A: (No mention — batch size is purely mechanical)
- Alternative B: "Batching lets you compare items within a batch for consistency before writing."
- Alternative C: "Writing in batches gives you a natural checkpoint — verify batch quality before committing."
- PURPOSE: Determine whether batching has quality implications worth mentioning or is purely mechanical.
- HYPOTHESIS: For tight batch tasks, batching IS purely mechanical. The quality mandate comes from other sections (critical_rules, instructions). Mentioning quality here dilutes the mechanical clarity of the batch discipline.
- STABILITY: STABLE toward Alternative A. Keep this section mechanical.

---

## FIELD: directory_path

TYPE: string (absolute path)
VALUES: absent (agent-builder) / `"/Users/johnny/.ai/spaces/bragi/interview/interviews"` (interview-enrich-create-summary)

### What the agent needs to understand

This is where the output tool writes files. The agent doesn't navigate to this directory or manage it — the tool handles that. But the agent needs to know the path exists as context for understanding where its output lands.

### Fragments

**directory_context**
- Alternative A: "Output directory: `/Users/johnny/.ai/spaces/bragi/interview/interviews`"
- Alternative B: "Your output tool writes to: `/Users/johnny/.ai/spaces/bragi/interview/interviews`. The tool manages this directory — you just invoke the tool."
- Alternative C: "Files are written to the interviews directory. The tool handles path resolution."
- Alternative D: (Embed in invocation explanation rather than calling out separately)
- PURPOSE: Give the agent awareness of where output goes without implying it should manage the directory.
- HYPOTHESIS: The agent needs minimal awareness of directory_path. The tool handles pathing. Over-explaining the directory invites the agent to do its own path management (e.g., checking if the directory exists, constructing full paths manually). Brief mention is sufficient.
- STABILITY: MEDIUM. The path is literal and locked, but how much to emphasize it varies.

**Cross-section dependency**: The tool handles directory creation/management. The agent's `permissions` section would reference this path for write access. `security` section may reference it for allowed write paths.

---

## FIELD: name_needed

TYPE: boolean
VALUES: absent (agent-builder) / `true` (interview-enrich-create-summary)

### What the agent needs to understand

When `true`, the agent must construct a filename for each invocation. This filename comes from `name_pattern` with placeholders filled from input parameters.

### Fragments

**name_requirement**
- Alternative A: (Implicit — if name_pattern exists, a name is needed. No separate signal required.)
- Alternative B: "Each invocation requires a filename. Construct it from the pattern below."
- Alternative C: "You must provide a filename with every tool invocation."
- PURPOSE: Signal that filename construction is the agent's responsibility.
- HYPOTHESIS: Like `invocation_variant`, this field is primarily a renderer signal. The agent sees `{name}` in the invocation template and `name_pattern` below — that is sufficient to know a name is needed. The boolean is redundant for the agent.
- STABILITY: STABLE toward Alternative A. The template and pattern together make this self-evident.

---

## FIELD: name_pattern

TYPE: string (filename template with placeholders)
VALUES: absent (agent-builder) / `"{interview-id}.summaries.jsonl"` (interview-enrich-create-summary)

### What the agent needs to understand

This is the filename template. The placeholder `{interview-id}` must be replaced with the actual interview ID from the input. The result is the `{name}` value used in invocation_display.

### Fragments

**pattern_instruction**
- Alternative A: "Filename pattern: `{interview-id}.summaries.jsonl` — replace `{interview-id}` with the interview ID from the input."
- Alternative B: "Construct the output filename by replacing `{interview-id}` in `{interview-id}.summaries.jsonl` with the actual interview ID provided in your input."
- Alternative C: "Output filename = `{interview-id}.summaries.jsonl` where `{interview-id}` comes from the input parameter `uid`."
- Alternative D: "The filename follows the pattern `{interview-id}.summaries.jsonl`. The interview-id value comes from the input you receive."
- PURPOSE: Teach the agent to construct filenames from the pattern by substituting input values.
- HYPOTHESIS: The critical information is the mapping from input parameter to placeholder. Without explicit mapping, the agent might use the wrong input field or invent a filename.
- STABILITY: HIGH for the pattern itself. MEDIUM for how explicitly to map placeholders to input fields.

**Cross-section dependency**: This is the strongest cross-section link in writing_output.
- `input.parameters.uid` → provides the value for `{interview-id}`
- `invocation_display` → the constructed filename fills the `{name}` placeholder
- The mapping `uid → interview-id` is a SEMANTIC BRIDGE that must be explicit somewhere.

**placeholder_to_parameter_mapping**
- Alternative A: "The `{interview-id}` in the filename pattern corresponds to the `uid` parameter from your input."
- Alternative B: "Map input parameter `uid` to the `{interview-id}` placeholder when constructing filenames."
- Alternative C: "Your input provides a `uid` field — this is the interview-id used in the filename."
- PURPOSE: Explicitly bridge the gap between input parameter naming and output placeholder naming.
- HYPOTHESIS: This mapping is CRITICAL. The input calls it `uid`. The pattern calls it `interview-id`. Without explicit bridging, the agent must infer the connection — which it might get wrong. This is a high-risk ambiguity point.
- STABILITY: LOCKED for the need to bridge. MEDIUM for the bridging language.

---

## FIELD: schema_path

TYPE: string (absolute path to JSON Schema file)
VALUES: absent (agent-builder) / `"/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json"` (interview-enrich-create-summary)

### What the agent needs to understand

The output tool validates every record against this schema before writing. If validation fails, the tool rejects the record. The agent must handle rejection by fixing the data, not by bypassing the tool.

### Fragments

**schema_awareness**
- Alternative A: "Your output is validated against `summaries.schema.json`. The tool rejects records that don't conform."
- Alternative B: "The tool validates each record against the schema at `schemas/summaries.schema.json`. If validation fails, the record is not written — fix the data and retry."
- Alternative C: "Schema validation happens at the tool level. Every record must conform to `summaries.schema.json`. Validation failures mean your output has structural errors — correct them."
- Alternative D: "The output tool enforces schema compliance. Records that fail validation are rejected. You are responsible for producing valid records."
- PURPOSE: Make the agent aware that validation is EXTERNAL (tool does it) but FAILURE HANDLING is INTERNAL (agent must respond to it).
- HYPOTHESIS: Agents need to understand two things: (1) the tool validates, so they don't need to do their own validation, and (2) when the tool rejects a record, they must fix the data. Without (2), agents may interpret a tool rejection as a system error and stop processing.
- STABILITY: HIGH. The split responsibility (tool validates, agent fixes) is invariant.

**failure_handling**
- Alternative A: "If the tool rejects a record, examine the validation error, fix the JSON, and retry the invocation."
- Alternative B: "Validation errors mean your output doesn't match the schema. Read the error message, correct the record, and write again."
- Alternative C: "On validation failure: do not skip the record. Fix the structural error and resubmit."
- Alternative D: "The tool will tell you what's wrong if validation fails. Fix it. Do not proceed to the next batch with unwritten records."
- PURPOSE: Prevent the agent from silently dropping records that fail validation.
- HYPOTHESIS: Silent record-dropping is the most dangerous failure mode. The agent processes an item, tries to write it, gets a validation error, and moves on without that record ever being written. Explicit "do not skip" language is essential.
- STABILITY: LOCKED. Never skip failed records.

---

## STRUCTURAL: Section Tone — Tutorial vs. Specification vs. Reference

### What the agent needs to understand

The `writing_output` section has a unique tonal challenge. It is the most mechanical section (favoring specification/reference) but also teaches a specific invocation pattern (favoring tutorial).

### Fragments

**section_framing_approach**
- Alternative A: SPECIFICATION tone — "You MUST invoke the tool as follows. The pattern is exact. Deviations are errors."
- Alternative B: REFERENCE tone — present the template and fields with minimal prose, trusting the agent to read and apply.
- Alternative C: TUTORIAL tone — "Here's how to write your output. First, construct the filename... Then, format the JSON... Finally, invoke the tool..."
- Alternative D: HYBRID — specification for the mandate and template, reference for the field values, brief tutorial only for the placeholder mapping.
- PURPOSE: Determine the right voice for a section that is simultaneously rigid (no interpretation) and instructional (must be understood to execute).
- HYPOTHESIS: Alternative D (hybrid) is optimal. The mandate needs specification weight ("you MUST"). The template needs reference clarity (just show it). The parameter-to-placeholder mapping needs tutorial explanation (because it bridges sections). Pure specification is too cold for the mapping explanation. Pure tutorial is too soft for the mandate.
- STABILITY: MEDIUM. The hybrid approach is likely correct, but the exact boundaries between tones are tunable.

---

## STRUCTURAL: Conditional Rendering Logic

### What the agent needs to understand

This is a RENDERER concern, not an agent concern. But the analysis must document the conditional logic for the galdr composition system.

### Rendering Rules

1. If `has_output_tool = false`: emit NOTHING for writing_output. No section header, no explanation of absence.
2. If `has_output_tool = true`: emit the full section with all fields.
3. If `name_needed = false` (hypothetical): omit name_pattern and adjust invocation_display to exclude `{name}`.
4. If `invocation_variant = "stdin-only"` (hypothetical): adjust invocation_display template accordingly.

### Fragments

**conditional_rendering_note**
- Alternative A: (No fragment needed — this is purely internal to galdr)
- Alternative B: Document the rendering conditions in a galdr-internal comment block
- PURPOSE: Ensure the composition system knows when to emit this section.
- HYPOTHESIS: This belongs in galdr's rendering logic, not in the agent prompt. The agent never sees the conditional logic — it sees either a fully rendered section or nothing.
- STABILITY: LOCKED. Conditional rendering is a system concern.

---

## STRUCTURAL: Cross-Section Dependency Map

### writing_output → input

- `name_pattern.{interview-id}` ← `input.parameters.uid`
- This is the highest-risk cross-section dependency. Parameter naming mismatch (`uid` vs `interview-id`) requires explicit bridging.

### writing_output → critical_rules

- `critical_rules` reinforces the tool usage mandate. If writing_output says "use this tool" and critical_rules says "ALWAYS use the output tool," these must not contradict.
- critical_rules may reference `tool_name` by name.

### writing_output → instructions

- Processing instructions may reference batch_size implicitly ("process items in groups").
- Instructions should not re-specify the invocation template — that creates drift risk.

### writing_output → permissions/security

- `directory_path` must appear in allowed write paths.
- `schema_path` must be readable.

---

## STRUCTURAL: Absence Behavior for Non-Output-Tool Agents

### What the composition system needs to handle

Agent-builder has no `writing_output` section. It writes using standard tools (Write, Edit). Its output behavior is governed by:
- `instructions` (which tell it what files to create)
- `permissions` (which constrain where it can write)
- `guardrails` (which prevent certain write patterns)

There is NO need for the agent prompt to say "you don't have an output tool." The absence of the section IS the signal.

### Fragments

**absence_handling**
- Alternative A: Emit nothing. The agent's instructions and permissions govern writing behavior.
- Alternative B: Emit a brief note: "You write output using standard file tools as directed by your instructions."
- Alternative C: Emit nothing, but ensure instructions explicitly cover output writing mechanics.
- PURPOSE: Handle the case where writing_output is absent.
- HYPOTHESIS: Alternative A is correct for most cases. Alternative C is a safety net — if instructions don't cover writing mechanics, the agent has no guidance. But that's an instructions problem, not a writing_output problem.
- STABILITY: STABLE toward Alternative A.

---

## SUMMARY OF KEY FINDINGS

1. **Most mechanical section** in the composition system. Exact reproduction, not interpretation.
2. **Binary presence** — exists fully or not at all. No partial states.
3. **Template-as-specification** — invocation_display is code to copy, not prose to interpret.
4. **Batch discipline** changes processing rhythm from item-by-item to accumulate-and-write.
5. **Highest-risk cross-section dependency** is the parameter-to-placeholder mapping (uid → interview-id).
6. **Tone should be hybrid** — specification for mandate, reference for template, tutorial for mapping.
7. **Renderer fields** (invocation_variant, name_needed) serve galdr, not the agent. They should not appear in the final prompt.
8. **Failure handling** is critical — agents must fix and retry, never silently drop records.
9. **Absence requires no explanation** — non-output-tool agents simply don't see this section.
10. **Schema validation is external** — the tool validates, the agent handles failures. The agent does NOT do its own validation.
