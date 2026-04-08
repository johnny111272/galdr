# RETURN_FORMAT -- Control Surface Synthesis

## Section Purpose

Return format is the agent's **completion protocol** -- the behavioral specification that defines what "done" means in machine-parseable terms. It answers three questions: what states can I end in (exit codes), what must I report in each state (payload), and who receives this (a dispatcher, not a human). Both analyses converge strongly on this framing.

This section programs two distinct behaviors. First, **protocol compliance**: SUCCESS, FAILURE, and ABORT are machine-parsed tokens in a dispatch protocol, not conversational status words. Second, **completion orientation**: by defining what the agent reports at the end, the section retroactively shapes how the agent approaches the entire task. An agent that knows it must report "exchanges processed count" will naturally maintain that counter during execution. The return format is a mission briefing disguised as a reporting requirement.

Its placement near the end of the prompt is deliberate and both analyses agree it is correct. The completion model occupies the agent's most recent working memory when execution begins, creating persistent orientation toward defined terminal states.

## Fragment Catalog

### mode_framing
- CONVERGED: Both agree mode="status" means a two-channel model -- output goes to files, return carries only a terse signal to the dispatcher. This separation must be made explicit or agents will conflate output with return.
- DIVERGED: A emphasizes the audience distinction (machine vs human consumers) as a separate fragment; B treats audience as embedded within mode framing.
- ALTERNATIVES:
  - A: "Your return mode is status. Your work products go to files. Your return goes to the dispatcher as a brief status signal -- not the deliverable." -- Direct, two-sentence separation of channels.
  - B: "You operate in status-return mode. The dispatcher expects a machine-parseable completion signal, not your output content. Output goes to files; the return channel carries only status." -- Adds machine-parsing context upfront.
- HYPOTHESIS: Explicitly naming two channels (output = files, return = status signal) prevents agents from either skipping file writes or returning verbose content. Without this, agents conflate "what I return" with "what I produce."
- STABILITY: structural
- CONDITIONAL: Only applies when mode="status". Other modes (hypothetical "content", "delegated") would need entirely different framing. Only "status" is currently observed.

### protocol_preamble
- CONVERGED: Both analyses rank this as the single highest-priority fragment. Tokens must be framed as machine-parsed protocol, not conversational language. First-position requirement is critical for reliable dispatch parsing.
- DIVERGED: Minimal. Both produce nearly identical alternatives with consistent rationale.
- ALTERNATIVES:
  - A: "Your return must begin with a protocol token: SUCCESS, FAILURE, or ABORT. The dispatch layer parses this token programmatically. Do not paraphrase or embed in prose -- it must appear as the first word." -- Explicit positional instruction.
  - B: "COMPLETION PROTOCOL: Your return message is parsed by the dispatcher. Use the exact state tokens below. Include specified metrics. No additional prose." -- Terse, imperative, header-style.
- HYPOTHESIS: Without explicit protocol framing, LLMs embed status in conversational prose the majority of the time. Explicit "this is protocol, not prose" framing with positional instruction ("first word") should push compliance above 95%.
- STABILITY: structural
- CONDITIONAL: Token list adjusts based on whether ABORT is present in status_instruction (two vs three tokens).

### status_instruction_presentation
- CONVERGED: Both agree the status_instruction is pre-authored by the definition author and should be presented verbatim. The template adds framing around it, never rewrites it.
- DIVERGED: A offers four framing labels ("completion contract", "report as follows", etc.); B focuses on whether to add structural scaffolding (parsed format, examples, shape hints) around the verbatim text.
- ALTERNATIVES:
  - A: Present verbatim, preceded by "Report your completion as follows:" -- Direct imperative, minimal framing.
  - B: Present verbatim, then append a single-line format template: "Format: STATE_TOKEN: metric1, metric2, metric3" -- Adds shape hint without inventing values.
  - C: Present verbatim as quoted block, preceded by "Your return states:" -- Lightest touch, trusts authored text fully.
- HYPOTHESIS: The framing label matters less than the protocol_preamble that precedes it. "Completion contract" may over-formalize; "report as follows" is direct. Adding a shape hint (B) provides marginal formatting guidance without overriding authored intent.
- STABILITY: formatting
- CONDITIONAL: none

### metrics_obligation
- CONVERGED: Both agree agents will sometimes return bare tokens without required metrics. Both agree the metrics are required, not suggestions.
- DIVERGED: A treats this as a standalone fragment with three alternatives. B embeds metric obligation within protocol_preamble ("include the specified metrics") and within the accuracy clause.
- ALTERNATIVES:
  - A: "Report all metrics specified for your return state. The dispatcher and downstream processes depend on these values being present." -- Explains WHY, which may be more effective than pure obligation.
  - B: "Each return state specifies required metrics. Missing metrics are a protocol violation." -- Strongest obligation language.
- HYPOTHESIS: Without explicit obligation framing, agents return bare SUCCESS tokens when work felt straightforward, omitting metrics they consider obvious. Explaining downstream dependency (A) may outperform pure threat language (B).
- STABILITY: structural
- CONDITIONAL: Framing intensity may scale with metric complexity (1-2 metrics = lighter; 3+ metrics = stronger tracking instruction).

### abort_distinction
- CONVERGED: Both analyses agree on the semantic distinction (ABORT = pre-execution rejection, FAILURE = mid-execution breakdown), that it matters for dispatch routing, and that it must be conditional on ABORT being present in status_instruction.
- DIVERGED: Negligible. Both produce equivalent alternatives and identical conditional logic.
- ALTERNATIVES:
  - A: "ABORT means you determined the work should not be attempted -- inputs insufficient, prerequisites missing. ABORT is not failure. It is a responsible decision to stop before producing bad output." -- Frames ABORT as professional responsibility.
  - B: "Three terminal states: SUCCESS (work completed), ABORT (work not attempted -- input insufficient), FAILURE (work attempted but broke). Choose the state that matches what happened." -- Compact taxonomy.
- HYPOTHESIS: Without explicit distinction, agents default to FAILURE for all non-success states. Framing ABORT as "a responsible professional decision" (not a lesser failure) is critical for correct state selection.
- STABILITY: structural
- CONDITIONAL: **Emit only when status_instruction contains "ABORT".** Omit entirely for two-state agents. Mentioning ABORT to agents that cannot return it creates confusion and occasional inappropriate ABORT returns.

### failure_honesty
- CONVERGED: Both rank this as the second highest-priority fragment. Both identify the LLM success bias as a fundamental behavioral pattern that corrupts signal integrity. Both agree this fragment is universally needed.
- DIVERGED: A emphasizes "a clean FAILURE is more valuable than a SUCCESS with compromised output." B adds the concept of behavioral license -- the return format gives the agent "permission to fail cleanly."
- ALTERNATIVES:
  - A: "An honest FAILURE is better than a dubious SUCCESS. If your work did not meet success conditions, return FAILURE. The dispatch layer handles failure -- do not hide it." -- Appeals to signal integrity.
  - B: "FAILURE is a valid and expected return state. Do not salvage broken output to avoid returning FAILURE. A clean FAILURE with a clear reason is more valuable than a SUCCESS with compromised output." -- Grants explicit permission.
- HYPOTHESIS: This is one of the highest-impact fragments in the entire section. Without it, agents return SUCCESS with qualifications instead of clean FAILURE. Explicit permission and encouragement to fail honestly materially improves signal quality.
- STABILITY: structural
- CONDITIONAL: none (universal across all agents)

### retroactive_orientation
- CONVERGED: Both agree the return format retroactively shapes execution behavior. Both agree agents should track metrics during execution rather than reconstructing them afterward.
- DIVERGED: A presents three phrasing alternatives; B frames this as "completion_as_goal" with emphasis on preventing open-ended drift and post-completion continuation.
- ALTERNATIVES:
  - A: "Your return requirements imply tracking requirements. If you must report a count, maintain that count as you work. If you must report a path, know the path before you write." -- Concrete, operational.
  - B: "The dispatcher is waiting for your return signal. When you reach a terminal state, report it immediately with the specified payload. Do not continue work after reaching a terminal state." -- Adds anti-drift instruction.
- HYPOTHESIS: Without this framing, agents treat return format as afterthought and reconstruct metrics from memory, producing inaccurate counts and missing values. Alternative A improves metric accuracy; alternative B prevents post-completion drift. Both may be needed.
- STABILITY: formatting
- CONDITIONAL: B's anti-drift instruction is more valuable for batch tasks than single-output tasks.

### accuracy_clause
- CONVERGED: B explicitly recommends this; A implies it through the metrics_obligation fragment.
- DIVERGED: A does not surface this as a distinct fragment. B calls it out as a guardrails interaction point.
- ALTERNATIVES:
  - A: "Report actual metrics from your execution. Do not fabricate values to match the expected format." -- Two sentences, direct.
- HYPOTHESIS: Prevents agents from inventing plausible-looking return values when unsure of actual numbers. Low cost to include, meaningful downside protection.
- STABILITY: formatting
- CONDITIONAL: none

### failure_cross_reference
- CONVERGED: Both identify the failure_criteria <-> return_format dependency. Both agree failure conditions should not be repeated -- only referenced.
- DIVERGED: A offers an explicit bridging fragment and an "omit" option. B frames it as a design implication ("reference, don't repeat").
- ALTERNATIVES:
  - A: "The conditions for failure are defined in your failure criteria. Here, you learn how to report failure to the dispatcher." -- Explicit bridge.
  - B: Omit -- let the agent connect the sections implicitly. -- Trusts agent competence, avoids redundancy.
- HYPOTHESIS: Explicit cross-reference is helpful but may be unnecessary in well-structured prompts. The risk of omission is that agents treat failure_criteria as advisory and return_format as the real failure spec.
- STABILITY: experimental
- CONDITIONAL: none

### section_header
- CONVERGED: Both prefer "Return Protocol" or "Completion Protocol" over "Return Format." Both agree the header primes interpretive stance and "Return Format" undersells behavioral significance.
- DIVERGED: A offers 4 alternatives; B offers 5 including "Terminal States" and "How to Report Completion."
- ALTERNATIVES:
  - A: "## Return Protocol" -- Primes protocol compliance from first words.
  - B: "## Completion Protocol" -- Signals both completion (goal-orientation) and protocol (machine-precision).
- HYPOTHESIS: Either outperforms "Return Format," which sounds like formatting instructions. Marginal difference between A and B.
- STABILITY: formatting
- CONDITIONAL: none

## Cross-Section Dependencies

Both analyses converge on the same dependency map:

| Dependency | Direction | Design Implication |
|---|---|---|
| failure_criteria -> return_format | Forward ref | Failure criteria define WHEN; return format defines HOW to report. Reference, do not repeat. |
| success_criteria -> return_format | Forward ref | SUCCESS metrics should align with success criteria. Dispatcher should verify fulfillment from return payload alone. |
| execution_instructions -> return_format | Sequential | Last execution instruction should flow naturally into return format. Transition framing bridges them. |
| output_spec -> return_format | Parallel | Output spec defines file destinations; return format defines status destination. Two-channel model depends on both. |
| guardrails -> return_format | Implicit | Guardrail violations may trigger FAILURE. Accuracy clause prevents fabricated metrics (guardrails interaction). |

B additionally identifies role -> return_format (creative roles may need stronger protocol framing than mechanical ones) but recommends consistent framing for all agents to avoid complexity.

## Conditional Branches

### ABORT present vs absent
- **Detection:** Parse status_instruction for uppercase "ABORT"
- **Present:** Include abort_distinction, list three terminal states in protocol_preamble
- **Absent:** Omit abort_distinction entirely, list two states only

### mode = "status" vs other
- **Detection:** Direct enum comparison on mode field
- **"status":** Full two-channel framing, terse signal instruction, metrics obligation
- **Other:** Entirely different framing needed (return IS the output). Only "status" currently observed.

### Metric complexity (A only)
- **Detection:** Count distinct metric references in status_instruction
- **Simple (1-2):** Light metrics_obligation framing
- **Complex (3+):** Stronger retroactive_orientation, explicit tracking instruction

### Batch vs single-output (B only)
- **Detection:** Implicit in status_instruction content or derivable from dispatch batch_size
- **Batch:** Stronger completion_as_goal framing, anti-drift instruction
- **Single-output:** ABORT more relevant, completion more naturally defined

## Open Design Questions

1. **Should mode_framing and audience_distinction be one fragment or two?** A separates them; B combines them. Combining is more compact; separating allows independent tuning.

2. **Transition sentence before the section -- include or omit?** B recommends "Now that you understand your task, here is your completion protocol." A does not address this explicitly. A transition bridges execution_instructions -> return_format but costs tokens.

3. **Shape hint after status_instruction -- include or omit?** B's Alternative D (single-line format template) adds marginal formatting guidance. Risk: becomes stale if status_instruction format varies. Benefit: reduces ambiguity in return structure.

4. **Accuracy clause -- standalone fragment or embedded in metrics_obligation?** B surfaces it explicitly; A implies it. Standalone is cleaner for conditional inclusion.

5. **Batch vs single-output branch -- worth implementing?** B identifies it but detection is indirect. The behavioral difference is real but the complexity cost may not justify a formal branch.

## Key Design Decisions

1. **Protocol framing is the highest-priority fragment.** Both analyses agree unanimously. Tokens must be understood as machine-parsed protocol, with explicit first-position instruction. Non-negotiable for status mode.

2. **Failure honesty is the second highest-priority fragment.** Both analyses agree. Counteracting LLM success bias is critical for dispatch signal integrity. Universal across all agents.

3. **Two-channel model must be explicit.** Without it, agents conflate output and return. Structural to status mode.

4. **ABORT distinction is conditional, not universal.** Only agents with ABORT in their protocol receive this framing. Including it for two-state agents causes inappropriate ABORT returns.

5. **Status_instruction is presented verbatim.** The template adds framing around it, never rewrites it. The definition author's intent is preserved.

6. **End-of-prompt placement is correct.** Recency effect means the completion model is the agent's freshest frame when execution begins. Both analyses agree this should not change.

7. **"Return Protocol" or "Completion Protocol" for header.** Either outperforms "Return Format." Both prime protocol compliance over formatting.
