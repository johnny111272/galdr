# WRITING_OUTPUT Section Analysis

## OVERVIEW

The `writing_output` section is the most operationally rigid section in the entire agent prompt. It is a behavioral programming block that transforms the agent from a general-purpose language model into a disciplined batch-processing worker with a precise, non-negotiable output ritual. Its presence or absence is the single biggest fork in how an agent's operational identity is constructed.

When present, this section answers: "You will write output THIS way, using THIS tool, in THIS format, at THIS rhythm." When absent, the agent falls back to standard file-manipulation tools with no prescribed ceremony — a fundamentally different operational mode.

The key behavioral insight: this section doesn't just tell the agent what tool to use. It installs a **processing cadence**. Batch discipline means the agent must hold state across multiple processed items, accumulate results, and flush at intervals. This is a radically different cognitive posture than process-one-write-one. The agent must plan ahead, maintain a mental buffer, and respect a rhythm imposed externally.

---

## STRUCTURAL: SECTION CONDITIONALITY

The entire `writing_output` section is conditional on `has_output_tool = true`. This is not a field-level conditional — the entire section appears or disappears as a unit. Agent 1 (agent-builder) has NO `writing_output` section. Agent 2 (interview-enrich-create-summary) has it fully populated.

### What the agent needs to understand

The agent needs to know whether it has a prescribed output tool or not. When the section is present, the agent must treat it as the ONLY acceptable output mechanism — no fallback to Write or Bash for data output. When absent, the agent uses standard file tools with no special ceremony. The template system must handle both modes cleanly: either the entire output-tool instruction block renders, or it is completely omitted with no orphaned references.

### Fragments

**section_present_gate**
- Alternative A: "You have a dedicated output tool. ALL processed output MUST be written using this tool. Do not use Write, Bash, or any other file tool for data output."
- Alternative B: "Your output is written through a specialized validated writer. The invocation pattern below is your ONLY permitted output method. Using any other tool to write output data is a violation."
- Alternative C: "A custom output tool has been configured for this task. Every record you produce goes through this tool — no exceptions, no alternatives, no 'just this once' with a different method."
- PURPOSE: Establish that the output tool is not a suggestion but the exclusive output channel.
- HYPOTHESIS: Alternative C's conversational anti-escape-hatch tone ("no 'just this once'") may be more effective at preventing the model from reasoning its way into using a different tool. Alternative A is cleanest. Alternative B introduces "validated writer" framing which connects to schema validation.
- STABILITY: High. The binary present/absent gate is structural — every output-tool agent needs this framing.

**section_absent_fallback**
- Alternative A: (Simply omit the entire output-tool instruction block. No mention of output tools at all.)
- Alternative B: "You write output using standard file tools (Write, Bash). No special output tool is configured for this task."
- Alternative C: "Output files are written directly. Use the file tools available to you."
- PURPOSE: Handle the non-output-tool case. The question is whether silence (omission) or explicit acknowledgment of standard mode is better.
- HYPOTHESIS: Alternative A (pure omission) is likely best. Mentioning the absence of an output tool draws attention to a concept the agent doesn't need. Alternative B is useful only if the template needs to be self-documenting. Alternative C is too vague.
- STABILITY: High. But the design choice (omit vs. mention) has downstream effects on template complexity.

---

## FIELD: tool_name
TYPE: string (exact identifier)
VALUES: (absent) / "append_interview_summaries_record"

### What the agent needs to understand

This is the precise, character-exact name of the tool the agent must invoke. It is not a description — it is an identifier that must be reproduced without modification. The agent must treat this as a literal string, not interpret or abbreviate it.

### Fragments

**tool_identity**
- Alternative A: "Your output tool is `append_interview_summaries_record`."
- Alternative B: "Write all output records using the tool named `append_interview_summaries_record`. This name is exact — do not abbreviate, modify, or paraphrase it."
- Alternative C: "Output tool: `append_interview_summaries_record`"
- PURPOSE: Introduce the tool by its exact name so the agent can reference it in invocations.
- HYPOTHESIS: Alternative B's explicit "do not abbreviate" warning may be unnecessary — models generally reproduce tool names faithfully. Alternative C is minimal and works well when followed immediately by the invocation display. Alternative A is clean middle ground.
- STABILITY: High. The tool name is always a single literal string. The only variation across agents is the string value itself.

---

## FIELD: invocation_display
TYPE: multiline string (literal code template)
VALUES: (absent) / heredoc invocation pattern

### What the agent needs to understand

This is the single most critical field in the section. It is a literal command template that the agent must reproduce precisely when writing output. It contains heredoc syntax (`<<'EOF'`), a tool name, an optional name parameter, and a data placeholder (`{json_data}`). The agent must understand that this is not pseudocode or a description — it is the exact command shape it must produce, with only the placeholders substituted.

The heredoc pattern (`<<'EOF' ... EOF`) is a shell construct that passes multi-line data to a command. The agent must reproduce this syntax exactly, including the single quotes around EOF (which prevent variable expansion in shell) and the closing EOF on its own line.

### Fragments

**invocation_frame**
- Alternative A: "When writing output, use exactly this invocation pattern:\n```\nappend_interview_summaries_record {name} <<'EOF'\n{json_data}\nEOF\n```\nSubstitute `{name}` with the constructed filename and `{json_data}` with your JSON records."
- Alternative B: "Your output invocation is a heredoc command. Reproduce this pattern exactly — it is not pseudocode, it is the literal command shape:\n```\nappend_interview_summaries_record {name} <<'EOF'\n{json_data}\nEOF\n```\nReplace only the `{name}` and `{json_data}` placeholders. Everything else is literal."
- Alternative C: "Output command template (reproduce exactly, substituting only placeholders):\n```\nappend_interview_summaries_record {name} <<'EOF'\n{json_data}\nEOF\n```"
- Alternative D: "Each batch of records is written using a heredoc invocation. The tool receives the filename as an argument and the JSON data via stdin through the heredoc:\n```\nappend_interview_summaries_record {name} <<'EOF'\n{json_data}\nEOF\n```\nThis is the EXACT syntax. Do not restructure, reorder, or reformulate this command."
- PURPOSE: Install the invocation pattern as a rigid template the agent will reproduce mechanically.
- HYPOTHESIS: Alternative B's "it is not pseudocode" warning directly addresses the primary failure mode — models treating code blocks as illustrative rather than prescriptive. Alternative D explains the mechanics (stdin, heredoc) which may help the agent reason about edge cases. Alternative C is minimal and may work if the surrounding context is strong enough. Alternative A is clear but may not be forceful enough about literalness.
- STABILITY: Medium-high. The invocation_display value varies per agent, but the framing around "reproduce this exactly" is universal for all output-tool agents.

**heredoc_explanation**
- Alternative A: (No explanation — assume the model understands heredoc syntax.)
- Alternative B: "The `<<'EOF'` syntax passes everything between the opening and closing `EOF` markers as input to the command. The single quotes prevent shell interpolation."
- Alternative C: "This uses heredoc syntax to pass JSON data to the tool. The data goes between `<<'EOF'` and the closing `EOF` on its own line."
- PURPOSE: Ensure the agent understands the mechanical syntax it must reproduce.
- HYPOTHESIS: Alternative A is likely sufficient — modern LLMs understand heredoc syntax. Explanation is only needed if agents are observed mangling the syntax. Alternative B is technically precise but the shell interpolation detail is irrelevant in an LLM context. Alternative C focuses on what matters (data goes between markers).
- STABILITY: Low. This is explanatory scaffolding that may be unnecessary. Good candidate for removal if testing shows agents handle heredocs correctly without explanation.

---

## FIELD: batch_size
TYPE: integer
VALUES: (absent) / 20

### What the agent needs to understand

Batch size fundamentally changes the agent's processing rhythm. Instead of processing one item and immediately writing it, the agent must process multiple items, accumulate their results in memory, and write them together in a single invocation. This creates a buffer-and-flush cadence.

The behavioral implications are significant:
1. The agent must maintain a mental count of accumulated records.
2. The agent must know when to flush (every N records, and at the end of processing).
3. The final batch may be smaller than batch_size — the agent must handle remainders.
4. If the agent processes 47 items with batch_size=20, it writes 3 invocations: 20 + 20 + 7.

### Fragments

**batch_discipline**
- Alternative A: "Write output in batches of 20 records per invocation. Accumulate processed records and invoke the output tool every 20 records. Write any remaining records in a final smaller batch."
- Alternative B: "Batch discipline: process records and accumulate results. Every 20 records, invoke the output tool to write the batch. After processing all input, write any remaining records as a final batch. Never write single records individually."
- Alternative C: "Your output rhythm is batched. Accumulate 20 processed records, then write them in a single tool invocation. Continue until all input is processed. The final invocation may contain fewer than 20 records — that is expected."
- Alternative D: "Output is batched at 20 records per write. This means you do NOT write after each record. You process, accumulate, and write in groups of 20. The last group may be smaller. This batching is mandatory — do not write records one at a time."
- PURPOSE: Install batch accumulation behavior and prevent the one-at-a-time write pattern.
- HYPOTHESIS: Alternative D explicitly names and prohibits the failure mode (writing one at a time), which is the most likely deviation. Alternative C's "output rhythm" framing is elegant and may create a stronger mental model. Alternative B's "batch discipline" label creates a named concept the agent can reference. Alternative A is functional but bland.
- STABILITY: High. Batch discipline framing is needed for every output-tool agent. The number changes but the concept is universal.

**batch_remainder**
- Alternative A: "The final batch may contain fewer than 20 records. Write it normally."
- Alternative B: "After processing all input, flush any remaining records regardless of count."
- Alternative C: "Do not wait for a full batch at the end of processing. Write whatever remains."
- PURPOSE: Prevent the agent from holding back the final partial batch.
- HYPOTHESIS: Alternative C directly addresses the failure mode (waiting for a full batch that will never come). Alternative B's "flush" terminology is precise. Alternative A is simplest. This may be combinable with the main batch_discipline fragment rather than standing alone.
- STABILITY: High. Every batched agent faces the remainder problem.

---

## FIELD: directory_path
TYPE: string (absolute filesystem path)
VALUES: (absent) / "/Users/johnny/.ai/spaces/bragi/interview/interviews"

### What the agent needs to understand

This is the directory where output files are written. The output tool handles the actual file writing, but the agent needs to know the directory for two reasons: (1) understanding where its output lands in the filesystem, and (2) the tool may require it as context or for error messages.

### Fragments

**output_location**
- Alternative A: "Output files are written to: `/Users/johnny/.ai/spaces/bragi/interview/interviews`"
- Alternative B: "Your output directory is `/Users/johnny/.ai/spaces/bragi/interview/interviews`. The output tool writes files here — you do not need to create or manage the directory."
- Alternative C: "Output destination: `/Users/johnny/.ai/spaces/bragi/interview/interviews/`\nThe output tool handles file creation in this directory."
- PURPOSE: Inform the agent where output lands. Secondary: prevent the agent from trying to mkdir or manage the directory itself.
- HYPOTHESIS: Alternative B's "you do not need to create or manage" prevents a common LLM behavior of trying to ensure directories exist before writing. Alternative A is bare-minimum. Alternative C is concise with a useful addendum.
- STABILITY: High. Every output-tool agent has a directory path. The framing is universal; only the path value changes.

---

## FIELD: name_needed
TYPE: boolean
VALUES: (absent) / true

### What the agent needs to understand

When true, the agent must construct a filename and pass it to the output tool. This is not optional — the tool requires a name argument. The filename is constructed from the `name_pattern` template.

### Fragments

This field's behavioral effect is expressed through the `name_pattern` and `invocation_display` fragments rather than standalone. It acts as a gate: when true, the name_pattern and name-related invocation fragments are included. When false, the invocation pattern omits the name argument.

**name_required_gate**
- Alternative A: "You must provide a filename with each invocation."
- Alternative B: "Each output invocation requires a filename argument constructed from the naming pattern below."
- Alternative C: (Express this implicitly through the invocation_display which shows the `{name}` parameter.)
- PURPOSE: Signal that filename construction is mandatory.
- HYPOTHESIS: Alternative C (implicit via invocation template) may be sufficient — the invocation_display already shows `{name}` as a required parameter. Explicit statement is only needed if agents are observed omitting the name. Alternative B connects to the name_pattern, creating a forward reference.
- STABILITY: Medium. The gate itself is stable but its expression may be subsumed by other fragments.

---

## FIELD: name_pattern
TYPE: string (template with placeholders)
VALUES: (absent) / "{interview-id}.summaries.jsonl"

### What the agent needs to understand

The agent must construct the output filename by substituting placeholders in this pattern with values from the input. This creates a cross-section dependency: the `{interview-id}` placeholder must be filled from the input section's `parameters.uid` field (or equivalent). The agent must:
1. Know the pattern.
2. Know where to get the substitution values.
3. Produce the correct filename for each input.

### Fragments

**name_construction**
- Alternative A: "Construct the output filename using the pattern: `{interview-id}.summaries.jsonl`\nReplace `{interview-id}` with the interview ID from your input."
- Alternative B: "Output filename pattern: `{interview-id}.summaries.jsonl`\nThe `{interview-id}` value comes from each input record's identifier. Each unique interview produces a separate output file."
- Alternative C: "Name your output files by substituting into this pattern:\n`{interview-id}.summaries.jsonl`\nThe interview ID is extracted from the input data. If processing interview `abc-123`, the output file is `abc-123.summaries.jsonl`."
- Alternative D: "Filename template: `{interview-id}.summaries.jsonl`\nSubstitute the interview identifier from the input. This means records from different interviews go to different files."
- PURPOSE: Teach the agent to construct filenames correctly and understand the cross-section dependency.
- HYPOTHESIS: Alternative C's concrete example (`abc-123` -> `abc-123.summaries.jsonl`) makes the substitution mechanical and unambiguous. Alternative D highlights the implication that different inputs may produce different filenames — important for batch processing where the agent might encounter multiple interviews. Alternative B's "each unique interview produces a separate output file" is the key insight for multi-input scenarios.
- STABILITY: Medium. The pattern varies across agents. The framing around substitution is reusable, but the cross-section mapping (which input field maps to which placeholder) is agent-specific.

**cross_section_mapping**
- Alternative A: "The `{interview-id}` in the filename pattern corresponds to the identifier field in your input records."
- Alternative B: "Input-to-output mapping: the interview ID from your input parameters becomes the `{interview-id}` in the output filename."
- Alternative C: (Express this implicitly — the agent should be able to infer the mapping from field names.)
- PURPOSE: Make the cross-section dependency explicit.
- HYPOTHESIS: Alternative C (implicit) is risky — the placeholder name `{interview-id}` and the input parameter name may not match exactly, and the agent must bridge that gap. Explicit mapping (A or B) is safer. Alternative A is more generalizable; Alternative B is more specific to this agent.
- STABILITY: Low-medium. The mapping is agent-specific. The need for SOME mapping statement is universal for name_needed=true agents, but the content varies entirely.

---

## FIELD: invocation_variant
TYPE: string (enum-like)
VALUES: (absent) / "with-name"

### What the agent needs to understand

This field indicates which invocation pattern shape to use. "with-name" means the tool invocation includes a filename argument. Other variants (e.g., a hypothetical "no-name" or "with-directory") would produce different invocation shapes. In practice, this field drives template selection — the invocation_display already reflects the chosen variant.

### Fragments

**variant_awareness**
- Alternative A: (Do not expose this to the agent. It is a template-selection field that has already been resolved into invocation_display.)
- Alternative B: "This tool uses the 'with-name' invocation pattern — you provide the filename as an argument to the tool."
- Alternative C: "Invocation style: named file. You specify which file to write to in the command."
- PURPOSE: Explain why the invocation looks the way it does.
- HYPOTHESIS: Alternative A is likely correct. The invocation_variant is a BUILD-TIME field that selects which invocation_display template to render. The agent doesn't need to know about variants — it just needs to follow the invocation_display. Exposing this field to the agent adds unnecessary conceptual overhead.
- STABILITY: N/A if we adopt Alternative A (do not render). If rendered, medium stability — the concept of invocation variants is universal but the explanation is per-variant.

---

## FIELD: schema_path
TYPE: string (absolute filesystem path)
VALUES: (absent) / "/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json"

### What the agent needs to understand

The output tool validates each record against this JSON Schema before writing. The agent does NOT perform validation itself — the tool does. But the agent needs to know:
1. That validation happens (so it understands why writes might fail).
2. What schema is being validated against (so it can produce conformant records).
3. What happens on validation failure (the tool rejects the write; the agent must fix and retry).

### Fragments

**schema_validation_awareness**
- Alternative A: "The output tool validates each record against the schema at `/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json` before writing. If validation fails, the write is rejected."
- Alternative B: "Your output records are validated against `summaries.schema.json` at write time. The tool enforces schema compliance — records that don't conform are rejected. Produce records that match the schema."
- Alternative C: "Schema enforcement: every record you write is validated against `/Users/johnny/.ai/spaces/bragi/schemas/summaries.schema.json`. The tool will reject non-conformant records. If a write fails due to schema validation, fix the record and retry."
- Alternative D: "Output validation is handled by the tool, not by you. The tool checks every record against the summaries schema. Your job is to produce conformant records. If the tool rejects a write, examine the error, fix the record, and retry the batch."
- PURPOSE: Set expectations about validation and error handling without making the agent think it should validate records itself.
- HYPOTHESIS: Alternative D's "handled by the tool, not by you" is the critical framing — it prevents the agent from building ad-hoc validation logic (a known LLM failure mode per workspace standards). Alternative C's retry instruction is important for error recovery. Alternative B is concise but lacks error handling guidance.
- STABILITY: High. Schema validation framing is needed for every output-tool agent. The schema path changes but the concept is universal.

**validation_failure_recovery**
- Alternative A: "If a write fails due to schema validation, examine the error message, correct the offending records, and retry the invocation."
- Alternative B: "On validation failure: read the error, fix the record(s), resubmit the batch. Do not skip failed records — fix them."
- Alternative C: "Schema validation errors mean your records don't match the expected format. Fix the issue and retry. Never silently drop records that fail validation."
- PURPOSE: Define error recovery behavior for validation failures.
- HYPOTHESIS: Alternative B's "do not skip failed records" and Alternative C's "never silently drop records" address the most dangerous failure mode — the agent quietly omitting records that don't validate. This is data loss. The retry instruction must be emphatic. Alternative A is procedurally correct but doesn't warn against the silent-drop failure.
- STABILITY: High. Error recovery framing is universal for all output-tool agents.

---

## STRUCTURAL: SECTION ORDERING AND INTEGRATION

### What the agent needs to understand

The writing_output section should appear AFTER the input section (so the agent knows what it's processing before learning how to write output) and AFTER the execution instructions (so the agent knows what to DO with inputs before learning the output mechanics). It should appear BEFORE or ALONGSIDE critical_rules, which may reference the output tool.

### Fragments

**section_position**
- Alternative A: (Position the section after execution instructions, before critical rules. No explicit statement about ordering.)
- Alternative B: "After processing input according to the instructions above, write your results using the following output tool."
- Alternative C: "Output mechanics — how to write your results:"
- PURPOSE: Transition from "what to do" to "how to write results."
- HYPOTHESIS: Alternative B creates a narrative bridge — it connects the execution phase to the output phase. Alternative C is a clean section header. Alternative A relies on document structure alone. The transitional bridge (B) may help the agent understand that output writing is the FINAL step, not something interleaved with processing.
- STABILITY: High. The transition from processing to output is universal.

---

## STRUCTURAL: JSON DATA FORMAT WITHIN HEREDOC

### What the agent needs to understand

The `{json_data}` placeholder in the invocation_display must be replaced with actual JSON. For batch writes, this means multiple JSON records. The format within the heredoc depends on whether the output is JSONL (one JSON object per line) or a JSON array. Given the `.jsonl` extension in the name_pattern, the records should be JSONL format — one complete JSON object per line, no wrapping array.

### Fragments

**json_format_in_heredoc**
- Alternative A: "Replace `{json_data}` with your JSON records, one complete JSON object per line (JSONL format). Do not wrap records in an array."
- Alternative B: "The data between the heredoc markers is JSONL — one JSON object per line. Each line must be a complete, valid JSON object. No trailing commas, no wrapping array."
- Alternative C: "Format your batch as JSONL: each record is a single-line JSON object, one per line. Example with 2 records:\n```\n{\"id\": \"...\", \"field\": \"value\"}\n{\"id\": \"...\", \"field\": \"other\"}\n```"
- PURPOSE: Specify the exact data format within the heredoc to prevent the agent from producing invalid JSONL.
- HYPOTHESIS: Alternative C's concrete example eliminates ambiguity. Alternative B's explicit prohibitions (no trailing commas, no wrapping array) address common LLM mistakes. Alternative A is correct but may leave room for format errors. Combining B's prohibitions with C's example would be strongest.
- STABILITY: Medium-high. The JSONL format instruction is needed whenever the output tool expects JSONL. If an agent writes JSON arrays instead, this fragment would differ.

---

## STRUCTURAL: RELATIONSHIP TO CRITICAL_RULES

### What the agent needs to understand

The critical_rules section typically contains reinforcement of the output tool mandate — rules like "ALWAYS use append_interview_summaries_record for output" or "NEVER use Write/Bash for data output." The writing_output section provides the mechanics; critical_rules provides the enforcement. These sections must be consistent and mutually reinforcing.

### Fragments

**critical_rules_bridge**
- Alternative A: (No explicit bridge. Let critical_rules independently reinforce the output tool mandate.)
- Alternative B: "The output tool specified above is your ONLY permitted output method. This is reinforced in the critical rules section."
- Alternative C: "Deviation from this output method is prohibited. See critical rules."
- PURPOSE: Connect writing_output to critical_rules enforcement.
- HYPOTHESIS: Alternative A (no bridge) is likely best. The sections should be self-reinforcing through repetition, not through cross-references that create dependency. If the template system renders them in sequence, the agent absorbs both without needing a pointer from one to the other. Cross-references add fragility.
- STABILITY: Medium. The need for reinforcement is universal, but the mechanism (bridge vs. independent repetition) is a design choice.

---

## CROSS-SECTION DEPENDENCIES

1. **writing_output.name_pattern -> input.parameters**: The filename placeholder values come from input parameters. The template must ensure these are mappable.
2. **writing_output.tool_name -> critical_rules**: Critical rules reinforce mandatory use of this specific tool.
3. **writing_output.batch_size -> execution instructions**: Batch discipline affects how the agent structures its processing loop.
4. **writing_output presence -> has_output_tool**: The entire section's existence is gated by this boolean.
5. **writing_output.schema_path -> schemas/**: The schema must exist and be compatible with the records the execution instructions tell the agent to produce.
6. **writing_output.directory_path -> input.directory_path (potential)**: The output directory may or may not be the same as the input directory. The agent must not confuse them.

---

## DESIGN CONSIDERATIONS

### Mechanical vs. Behavioral

This section is unique in the prompt because it is primarily MECHANICAL — it's a code template the agent must reproduce. Most other sections are BEHAVIORAL — they shape how the agent thinks, reasons, and decides. The writing_output section must balance:
- Mechanical precision (reproduce this exact syntax)
- Behavioral integration (batch discipline, error recovery, schema awareness)

The mechanical parts should be presented as literal, non-negotiable templates. The behavioral parts should be presented as operational rules the agent internalizes.

### Conditional Rendering Complexity

The section's complete conditionality (present vs. absent) means the template system needs a clean gate. This is not a field-level conditional — the entire section either renders or doesn't. The template should NOT have an "else" branch that says "you don't have an output tool" — it should simply omit the section entirely. The absence of output-tool instructions naturally causes the agent to fall back on standard file tools.

### Batch Size as Cognitive Load Management

Batch discipline is not just an efficiency concern — it affects output quality. An agent that writes after every record has no opportunity to cross-reference, normalize, or ensure consistency across records. An agent that accumulates 20 records before writing has a "buffer" of recent records it can compare against. The batch_size implicitly creates a consistency window. This is a non-obvious behavioral effect worth preserving in the design.

### The Invocation Display as Executable Specification

The invocation_display is effectively an executable specification — it defines the contract between the agent and the tool. This is fundamentally different from prose instructions. The template system should treat it as a code block that is injected verbatim, not as text that is composed from fragments. The surrounding prose contextualizes and explains the code block, but the code block itself is immutable data, not composable prose.
