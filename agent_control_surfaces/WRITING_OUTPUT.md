# WRITING_OUTPUT -- Control Surface Synthesis

## Section Purpose

The `writing_output` section is the most mechanically rigid section in the agent prompt composition system. It converts output writing from a generative task (figure out how to write) into a substitution task (fill in the blanks). Every other section shapes judgment and reasoning; this section shapes motor behavior -- the exact characters the agent must produce.

The section is binary: gated entirely on `has_output_tool = true`, it either renders in full or is completely absent. When present, it installs three things: (1) a mandatory tool with no alternatives, (2) a literal invocation template the agent reproduces mechanically, and (3) a batch accumulation rhythm that changes processing cadence from write-per-item to accumulate-and-flush. When absent, output behavior emerges from instructions, permissions, and guardrails with no special ceremony.

The key non-obvious behavioral effect: `batch_size` forces the agent to hold state across multiple items, creating a consistency window where it can cross-reference and normalize before committing. This is a quality lever disguised as a throughput optimization.

## Fragment Catalog

### presence_mandate
- CONVERGED: Both agree the section demands explicit, emphatic language establishing the tool as the ONLY output channel. Both agree the mandate must prevent fallback to Write/Edit/Bash.
- DIVERGED: None.
- ALTERNATIVES:
  - A: "You have a dedicated output tool. Every result you produce MUST be written using this tool. Standard file operations are not permitted for output." -- Clean, direct, minimal.
  - B: "Output flows through one channel: the tool specified here. You do not write files directly. You do not choose alternative tools. You invoke this tool." -- Rhythmic repetition hammers exclusivity.
  - C: "A custom output tool has been configured for this task. Every record goes through this tool -- no exceptions, no alternatives, no 'just this once' with a different method." -- Conversational anti-escape-hatch tone.
- HYPOTHESIS: Escape-hatch prevention is the critical behavioral target. Agents reason their way into using standard tools when the dedicated tool throws validation errors. Anti-escape language (B or C) directly addresses this.
- STABILITY: structural
- CONDITIONAL: `has_output_tool = true` gates entire section.

### absence_handling
- CONVERGED: Both strongly agree: emit nothing. Silence is the correct signal. Mentioning the absence of an output tool wastes tokens and draws attention to a concept the agent does not need.
- DIVERGED: None.
- ALTERNATIVES:
  - A: (Omit entire section. No text, no header, no explanation.)
- HYPOTHESIS: An agent that has never been told about an output tool will not look for one.
- STABILITY: structural
- CONDITIONAL: `has_output_tool = false` -- emit nothing.

### tool_identity
- CONVERGED: Both agree on minimal framing. The tool name is a literal string. It also appears in `invocation_display`, so this fragment serves as a semantic anchor giving the agent a named concept.
- DIVERGED: Whether to warn against abbreviation. A considers it potentially unnecessary; B treats it as implicit.
- ALTERNATIVES:
  - A: "Your output tool is `append_interview_summaries_record`." -- Clean anchor statement.
  - B: "Tool: `append_interview_summaries_record` -- this is the only tool you use for writing output." -- Combines identity with mandate reinforcement.
- HYPOTHESIS: Warning against abbreviation is unnecessary; models reproduce tool names faithfully. The fragment's real job is semantic anchoring.
- STABILITY: structural
- CONDITIONAL: none (always present when section renders).

### invocation_template
- CONVERGED: Both agree this is the single most critical field. Both emphasize: it is code to copy, not prose to interpret. Both flag the primary failure mode as agents treating the template as illustrative rather than prescriptive.
- DIVERGED: Whether to explain heredoc mechanics. A offers detailed explanation options; B leans toward omission, noting explanation may suggest the syntax is tricky and invite tinkering.
- ALTERNATIVES:
  - A: "Use this exact invocation pattern. The only parts you change are the placeholders -- `{name}` becomes the filename, `{json_data}` becomes your output. Reproduce all other characters exactly:" -- Explicit "exactly" framing.
  - B: "Your invocation template (copy exactly, substituting only the marked placeholders):" -- Minimal, lets the code block speak.
  - C: "Every write follows this pattern precisely. `{name}` and `{json_data}` are variables you fill in. The heredoc syntax, tool name, and structure are fixed:" -- Names what is fixed vs. variable.
- HYPOTHESIS: Explicit "exactly as shown" language suppresses the LLM tendency to "improve" code it is shown. The template itself is immutable data injected verbatim; surrounding prose contextualizes it.
- STABILITY: structural (framing) / the code block itself is immutable data, not a composable fragment.
- CONDITIONAL: none (always present when section renders).

### heredoc_explanation
- CONVERGED: Both agree this is low-stability scaffolding that is likely unnecessary. Modern LLMs understand heredoc syntax.
- DIVERGED: A offers a mid-weight explanation option; B leans harder toward omission, arguing explanation may be counterproductive.
- ALTERNATIVES:
  - A: (No explanation -- assume the agent understands heredoc syntax.)
  - B: "This uses heredoc syntax to pass multi-line JSON to the tool. The `EOF` markers delimit the content block." -- Minimal safety net.
- HYPOTHESIS: Omission is default. Include only if testing shows agents mangling heredoc syntax.
- STABILITY: experimental
- CONDITIONAL: none.

### placeholder_mapping
- CONVERGED: Both agree explicit mapping of placeholders to data sources is necessary. Both flag the `{name}` to filename and `{json_data}` to content mapping.
- DIVERGED: A folds this into invocation_frame; B breaks it out as a distinct fragment.
- ALTERNATIVES:
  - A: "`{name}` = output filename (from name_pattern). `{json_data}` = the JSON records for this batch." -- Terse key-value mapping.
  - B: "Replace `{name}` with the constructed filename and `{json_data}` with your JSON records, one complete JSON object per line." -- Combines mapping with format instruction.
- HYPOTHESIS: Separating mapping from format instruction is cleaner. Format belongs in json_format_in_heredoc.
- STABILITY: formatting
- CONDITIONAL: none.

### batch_discipline
- CONVERGED: Both agree batch discipline is mandatory, high-stability, and must prevent two failure modes: (1) writing after every single item, (2) accumulating ALL items before writing. Both agree the final-batch remainder must be explicitly handled.
- DIVERGED: Whether to mention the quality implication of batching. A sees a consistency window; B says keep it purely mechanical.
- ALTERNATIVES:
  - A: "You write in batches of 20. Process 20 inputs, construct 20 JSON records, write all 20 in one tool call, repeat until done. Final batch may be smaller." -- Step-by-step rhythm.
  - B: "Batch discipline: accumulate 20 processed records, then write them in a single tool invocation. After all input is processed, write any remaining records. Never write single records individually." -- Named concept with explicit prohibition.
  - C: "Your output rhythm is batched. Accumulate 20 processed records, then write them in a single tool invocation. Continue until all input is processed. The final invocation may contain fewer than 20 records -- that is expected." -- "Output rhythm" framing.
- HYPOTHESIS: Naming the prohibition ("never write single records individually") directly addresses the most common failure mode. The "output rhythm" framing from C creates a strong mental model. Combining both is strongest.
- STABILITY: structural
- CONDITIONAL: none (batch_size is always present when section renders, value varies).

### batch_remainder
- CONVERGED: Both agree final-batch handling is critical and must be explicit. Both identify the failure mode: waiting for a full batch that never comes.
- DIVERGED: Whether this stands alone or folds into batch_discipline.
- ALTERNATIVES:
  - A: "Do not wait for a full batch at the end of processing. Write whatever remains." -- Addresses the failure mode directly.
  - B: (Fold into batch_discipline: "...Final batch may be smaller.") -- Simpler, less fragmented.
- HYPOTHESIS: Folding into batch_discipline is cleaner. Separate fragment only if testing shows agents holding back remainders.
- STABILITY: structural (if standalone) / formatting (if folded)
- CONDITIONAL: none.

### output_location
- CONVERGED: Both agree on minimal mention. Both warn against over-explaining the directory, which invites the agent to manage it (mkdir, path checking).
- DIVERGED: None significant.
- ALTERNATIVES:
  - A: "Output directory: `/path/to/interviews`" -- Bare minimum.
  - B: "Your output tool writes to: `/path/to/interviews`. The tool manages this directory -- you just invoke the tool." -- Prevents directory management impulse.
- HYPOTHESIS: B's "you just invoke the tool" prevents a common LLM behavior of ensuring directories exist before writing.
- STABILITY: formatting
- CONDITIONAL: none.

### name_construction
- CONVERGED: Both agree the filename pattern is critical and the placeholder-to-input mapping is the highest-risk cross-section dependency. Both identify the `uid` vs `interview-id` naming mismatch as a key ambiguity point.
- DIVERGED: How explicitly to map. A offers a concrete example; B names the exact input field (`uid`).
- ALTERNATIVES:
  - A: "Filename pattern: `{interview-id}.summaries.jsonl` -- replace `{interview-id}` with the interview ID from your input." -- General.
  - B: "Output filename = `{interview-id}.summaries.jsonl` where `{interview-id}` comes from the input parameter `uid`." -- Names the exact field, bridges the naming gap.
  - C: "Construct the filename from the pattern `{interview-id}.summaries.jsonl`. The interview ID is extracted from the input data. Example: input uid `abc-123` produces `abc-123.summaries.jsonl`." -- Concrete example eliminates ambiguity.
- HYPOTHESIS: The `uid` to `interview-id` semantic bridge MUST be explicit. This is the highest-risk cross-section mapping in the entire section. Concrete examples (C) reduce error further.
- STABILITY: structural (need for bridge is locked; bridging language is formatting)
- CONDITIONAL: `name_needed = true`.

### json_format_in_heredoc
- CONVERGED: Both agree JSONL format specification is needed. A explicitly addresses this; B handles it implicitly through placeholder mapping.
- DIVERGED: A identifies this as a standalone fragment; B does not break it out.
- ALTERNATIVES:
  - A: "Format your batch as JSONL: each record is a single-line JSON object, one per line. No trailing commas, no wrapping array." -- Explicit prohibitions address common LLM mistakes.
  - B: "The data between the heredoc markers is JSONL -- one JSON object per line. Example:\n```\n{\"id\": \"...\", \"field\": \"value\"}\n{\"id\": \"...\", \"field\": \"other\"}\n```" -- Example eliminates ambiguity.
- HYPOTHESIS: Combining explicit prohibitions with a concrete example is strongest. This fragment is needed whenever the output tool expects JSONL (which is the current default).
- STABILITY: formatting
- CONDITIONAL: Output format is JSONL (driven by file extension in name_pattern).

### schema_validation_awareness
- CONVERGED: Both agree on the critical split: the tool validates, the agent handles failures. Both agree the agent must NOT do its own validation. Both agree silent record-dropping is the most dangerous failure mode.
- DIVERGED: None significant.
- ALTERNATIVES:
  - A: "The output tool validates each record against the schema. Validation failures mean your output has structural errors -- correct them and retry." -- Concise.
  - B: "Schema validation is handled by the tool, not by you. Records that fail validation are rejected. You are responsible for producing valid records. If the tool rejects a write, examine the error, fix the record, and retry." -- Explicit responsibility split.
- HYPOTHESIS: "Handled by the tool, not by you" is the critical framing. It prevents agents from building ad-hoc validation logic (a known LLM failure mode and a workspace-level violation).
- STABILITY: structural
- CONDITIONAL: `schema_path` is present.

### validation_failure_recovery
- CONVERGED: Both emphatically agree: never silently drop records. Fix and retry. This is locked.
- DIVERGED: None.
- ALTERNATIVES:
  - A: "On validation failure: do not skip the record. Fix the structural error and resubmit. Do not proceed to the next batch with unwritten records." -- Covers both skip and proceed-without failure modes.
  - B: "If the tool rejects a record, examine the validation error, fix the JSON, and retry. Never silently drop records that fail validation." -- Names the dangerous anti-pattern directly.
- HYPOTHESIS: Both failure modes (skip record, proceed without) must be explicitly prohibited. This is the highest-stakes behavioral instruction in the section.
- STABILITY: structural
- CONDITIONAL: none (always present when schema_path exists).

### section_transition
- CONVERGED: Both agree a transition from processing instructions to output mechanics is needed. Both consider pure omission (rely on document structure) vs. explicit bridge.
- DIVERGED: A leans toward explicit narrative bridge; B leans toward clean section header.
- ALTERNATIVES:
  - A: "After processing input according to the instructions above, write your results using the following output tool." -- Narrative bridge connecting execution to output.
  - B: "Output mechanics -- how to write your results:" -- Clean section header.
- HYPOTHESIS: The narrative bridge (A) helps the agent understand that output writing is the FINAL step, not interleaved with processing. Worth testing against the cleaner header.
- STABILITY: formatting
- CONDITIONAL: none.

## Cross-Section Dependencies

1. **name_pattern -> input.parameters**: `{interview-id}` placeholder maps to input `uid` field. HIGHEST RISK dependency. Naming mismatch requires explicit bridging in the prompt.
2. **tool_name -> critical_rules**: Critical rules reinforce mandatory tool usage. Tool name must match across both sections.
3. **batch_size -> execution instructions**: Batch discipline affects processing loop structure. Instructions should not re-specify the invocation template (drift risk).
4. **schema_path -> schemas/**: Schema must exist and be compatible with records the instructions tell the agent to produce.
5. **directory_path -> permissions/security**: Directory must appear in allowed write paths; schema_path must be readable.
6. **directory_path vs input.directory_path**: Output directory may differ from input directory. Agent must not confuse them.

## Conditional Branches

| Condition | Effect |
|---|---|
| `has_output_tool = false` | Entire section omitted. No header, no explanation, no mention. |
| `has_output_tool = true` | Full section renders with all applicable fields. |
| `name_needed = true` | name_pattern, name_construction, and cross-section mapping fragments render. `{name}` appears in invocation template. |
| `name_needed = false` (hypothetical) | name_pattern omitted. Invocation template adjusted to exclude `{name}`. |
| `invocation_variant` value | Selects which invocation_display template to render. Renderer concern only -- agent never sees this field. |

## Open Design Questions

1. **Batch quality implication**: A sees batch_size as creating a consistency window (quality lever). B says keep it purely mechanical. Should the prompt mention cross-referencing within batches, or does that dilute mechanical clarity?

2. **Heredoc explanation**: Include a minimal safety-net explanation, or trust that LLMs understand heredoc syntax? Both lean toward omission but neither commits fully.

3. **Section tone**: B proposes a hybrid tone (specification for mandate, reference for template, tutorial for placeholder mapping). A does not explicitly address tone. Is hybrid optimal, or does uniform specification tone work?

4. **Critical rules bridge**: Should writing_output explicitly reference critical_rules, or should the sections reinforce independently through repetition? Both lean toward independent reinforcement (no cross-reference) to avoid fragility.

5. **Renderer-only fields**: Both agree `invocation_variant` is a renderer field, not an agent field. A partially agrees on `name_needed`. Should both be formally classified as renderer-internal with no agent-facing fragments?

## Key Design Decisions

1. **DECIDED: Absence = silence.** Non-output-tool agents see nothing. No negation, no explanation.

2. **DECIDED: invocation_variant is renderer-internal.** The agent sees the rendered template, not the variant selector.

3. **DECIDED: Schema validation responsibility split.** Tool validates. Agent fixes failures. Agent never builds its own validation.

4. **DECIDED: Silent record-dropping is prohibited.** Fix and retry is the only acceptable failure recovery.

5. **DECIDED: invocation_display is immutable data.** It is injected verbatim as a code block, not composed from fragments. Surrounding prose contextualizes it.

6. **DECIDED: Cross-section parameter mapping must be explicit.** The `uid` to `interview-id` bridge cannot be left to inference.

7. **OPEN: Batch quality framing.** Consistency-window argument vs. pure mechanics. Defer to testing.

8. **OPEN: Heredoc explanation.** Default to omission; include only if failure testing warrants it.
