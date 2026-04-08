# RETURN FORMAT — Control Surface Analysis

## First Principles: What Does This Section Actually Do?

The return format section is not merely "how to format output." It is the agent's **completion contract** — the behavioral specification that defines what "done" means, what the dispatcher expects to parse, and critically, what mental model of accountability the agent carries throughout execution.

This section programs two distinct behaviors:

1. **Protocol compliance** — The agent must understand that SUCCESS, FAILURE, and ABORT are machine-parsed tokens in a dispatch protocol, not conversational status words. The difference between "I succeeded" and "SUCCESS" is the difference between prose and protocol. The dispatcher is not reading for comprehension — it is pattern-matching on tokens.

2. **Completion orientation** — By defining what the agent reports at the end, the section retroactively shapes how the agent approaches the entire task. An agent that knows it must report "exchanges processed count" will naturally track that count during execution. An agent that knows ABORT is a valid state will feel licensed to stop early when inputs are insufficient, rather than fabricating output to avoid failure. The return format defines the destination, and the destination shapes the journey.

The behavioral consequence of placing this section last is that it becomes the agent's final mental frame before execution. This is not accidental — it means the agent's most recent instruction when it begins working is "here is what you will report and how." This creates a persistent orientation toward the defined completion states throughout the work.

---

## FIELD: mode

TYPE: enum (observed value: "status"; hypothesized values: "full", "structured", others)
VALUES: "status" / "status"

### What the agent needs to understand

The `mode` field tells the agent the **channel semantics** of its return. In `status` mode, the agent's return to the dispatcher is a brief signal with key metrics — the substantive output goes to files. The return is a summary for the orchestration layer, not the deliverable itself. This distinction matters because it prevents the agent from dumping full output into its return message (which would be wasteful and potentially break dispatch parsing) while also preventing the agent from thinking the return IS the output (which would cause it to skip file writes).

The agent must understand: "Your work products go to files. Your return goes to the dispatcher. These are different channels with different audiences."

### Fragments

**mode_channel_framing**
- Alternative A: "Return a brief status signal to the dispatcher. Your substantive output goes to the files specified in your output instructions — the return is a summary for orchestration, not the deliverable."
- Alternative B: "Your return is a dispatch signal, not your output. Write your work products to the designated files. Return only a status token with key metrics to the dispatcher."
- Alternative C: "The dispatcher expects a status signal, not your full output. File writes are your deliverables. The return channel carries only a token and summary metrics."
- PURPOSE: Separate the return channel from the output channel in the agent's mental model. Without this, agents conflate "what I return" with "what I produce."
- HYPOTHESIS: Agents that understand the two-channel model (files for output, return for signal) will reliably write files AND return clean status tokens. Agents without this framing may either skip file writes (thinking the return IS the output) or return verbose content (thinking the dispatcher wants the full result).
- STABILITY: High. The two-channel model is structural to how dispatch works. Every status-mode agent needs this framing regardless of task domain.

**mode_audience_distinction**
- Alternative A: "The dispatcher reads your return programmatically. It parses tokens, not prose. Your files are read by humans or downstream agents. Write accordingly for each audience."
- Alternative B: "Two audiences receive your work: the dispatcher (which parses your return token) and the consumer (which reads your output files). Format each for its audience."
- Alternative C: "Your return is machine-parsed by the dispatch layer. Your file output is consumed by humans or other agents. These are different audiences with different needs."
- PURPOSE: Reinforce that the return is machine-consumed. This nudges the agent away from conversational returns ("I've completed the task successfully!") toward protocol-compliant returns ("SUCCESS: agent-builder, 12 steps, 3 includes").
- HYPOTHESIS: Explicitly naming the dispatcher as a machine parser will produce cleaner, more parseable returns. Without this, agents default to conversational tone in returns because LLMs default to human-facing prose.
- STABILITY: High. The machine-audience framing is invariant across all status-mode agents.

---

## FIELD: status_instruction

TYPE: free-form text (pre-authored per agent definition)
VALUES:
- Agent 1: "Return SUCCESS with the agent name, number of instruction steps, and number of include files. Return ABORT with a structured fault list if the requirements are insufficient. Return FAILURE if source materials cannot be read."
- Agent 2: "Return SUCCESS when all exchange summaries are written and validated. Include interview uid, exchanges processed count, and output path. If any record fails validation and cannot be fixed, return FAILURE with clear reason."

### What the agent needs to understand

The status_instruction is the agent-specific completion contract. It tells the agent exactly what to return in each terminal state, including what metrics to report and under what conditions each state applies. This is the most task-specific part of the return format — while `mode` is structural, `status_instruction` is authored by the agent designer to match the task's specific completion semantics.

The agent must understand three things about this field:
1. The tokens (SUCCESS, FAILURE, ABORT) are protocol — they are the first thing the dispatcher looks for.
2. The metrics listed with each token are required, not suggestions.
3. The conditions for each state are deterministic — the agent should not choose between states based on preference but based on which condition was met.

### Fragments

**protocol_token_framing**
- Alternative A: "The following tokens are dispatch protocol — SUCCESS, FAILURE, and ABORT are machine-parsed signals. Begin your return with exactly one of these tokens. They are not conversational; they are protocol."
- Alternative B: "Your return must begin with a protocol token: SUCCESS, FAILURE, or ABORT. The dispatch layer parses this token programmatically. Do not paraphrase, reword, or embed these tokens in prose — they must appear as the first word of your return."
- Alternative C: "Dispatch protocol requires your return to lead with exactly one of: SUCCESS, FAILURE, ABORT. These are not descriptive words — they are parsed signals. The token must be unambiguous and appear first."
- Alternative D: "Return protocol: your first word must be one of SUCCESS, FAILURE, or ABORT. This is a machine-parsed token. Everything after the token is the status detail."
- PURPOSE: Prevent the agent from returning conversational completions like "I have successfully completed..." instead of "SUCCESS: ...". The token must be unambiguous and positionally fixed for reliable dispatch parsing.
- HYPOTHESIS: Without explicit protocol framing, LLMs will embed status in conversational prose approximately 60-80% of the time. Explicit "this is protocol, not prose" framing should push compliance above 95%. The positional instruction ("first word") is critical — without it, agents may write "The result is SUCCESS" which is harder to parse.
- STABILITY: Very high. This framing is invariant across all agents using status mode. The specific tokens may evolve, but the need to frame them as protocol is permanent.

**status_instruction_presentation**
- Alternative A: "Here is your completion contract:\n\n{status_instruction}"
- Alternative B: "Report your completion as follows:\n\n{status_instruction}"
- Alternative C: "When your work is complete, return to the dispatcher:\n\n{status_instruction}"
- Alternative D: "Your dispatch return specification:\n\n{status_instruction}"
- PURPOSE: Frame the status_instruction content as authoritative specification, not suggestion. The phrasing before the injected text sets the agent's interpretive stance.
- HYPOTHESIS: "Completion contract" (A) may over-formalize and cause the agent to treat it as legal text rather than operational spec. "Report as follows" (B) is direct and imperative. "When your work is complete" (C) ties it to a temporal moment, which may help placement. "Dispatch return specification" (D) is the most precise about what it is but may be jargon-heavy.
- STABILITY: Medium. The framing words matter less than the protocol token framing above. This is presentational rather than behavioral.

**metrics_obligation**
- Alternative A: "The metrics listed with each token are required. Include all specified values in your return — they are not optional detail."
- Alternative B: "Each return state specifies required metrics. Your return must include every listed value. Missing metrics are a protocol violation."
- Alternative C: "Report all metrics specified for your return state. The dispatcher and downstream processes depend on these values being present."
- PURPOSE: Prevent the agent from returning bare tokens ("SUCCESS") without the required metrics. The status_instruction specifies metrics (agent name, counts, paths, uids) that downstream processes need.
- HYPOTHESIS: Without explicit obligation framing, agents will sometimes return bare SUCCESS tokens when the work felt straightforward, omitting metrics they consider obvious. "Protocol violation" language (B) is strongest but may be over-threatening. "Downstream processes depend on" (C) explains the WHY, which may be more effective than pure obligation.
- STABILITY: High. Every status_instruction includes metrics, and every agent needs to know they are required.

---

## STRUCTURAL: The Three-State Protocol (SUCCESS / FAILURE / ABORT)

### What the agent needs to understand

The three terminal states are not a spectrum — they are categorically different conditions:

- **SUCCESS**: Work completed, output produced, metrics reportable. The contract is fulfilled.
- **FAILURE**: Work was attempted but something broke during execution. Partial output may exist. The contract was attempted but not fulfilled.
- **ABORT**: Work was NOT attempted because preconditions were not met. No output was produced. The contract was never entered.

The critical distinction is between FAILURE and ABORT. FAILURE means the agent tried and failed. ABORT means the agent determined that trying would be pointless or harmful (insufficient input, missing prerequisites, contradictory requirements). ABORT is not a failure — it is a responsible pre-flight check.

Not all agents use all three states. The builder uses SUCCESS/ABORT/FAILURE (three states). The summarizer uses SUCCESS/FAILURE (two states). The template must handle both cases — agents that can ABORT and agents that cannot.

### Fragments

**abort_distinction**
- Alternative A: "ABORT means you determined the work should not be attempted — inputs were insufficient, prerequisites missing, or requirements contradictory. ABORT is not failure. It is a responsible decision to stop before producing bad output."
- Alternative B: "If preconditions for your work are not met, return ABORT — not FAILURE. ABORT signals that you stopped before attempting the work because the attempt would be pointless. FAILURE signals that you attempted the work and it broke."
- Alternative C: "ABORT and FAILURE are different signals. ABORT: 'I examined the inputs and cannot proceed — no work was done.' FAILURE: 'I attempted the work and it did not succeed.' Choose the correct signal — the dispatcher handles them differently."
- Alternative D: "There is a difference between 'the inputs were wrong' (ABORT) and 'the execution broke' (FAILURE). Return the signal that matches what actually happened. The dispatcher routes these differently."
- PURPOSE: Prevent agents from returning FAILURE when they should return ABORT (or vice versa). The dispatch layer may handle these differently — ABORT might trigger input review while FAILURE triggers retry or escalation. Misclassification corrupts the dispatch response.
- HYPOTHESIS: Without explicit distinction framing, agents will default to FAILURE for all non-success states because FAILURE is the more familiar concept. ABORT requires understanding that "I stopped before working" is a valid and distinct outcome. The framing must make ABORT feel like a responsible professional decision, not a lesser form of failure.
- STABILITY: High for agents that have ABORT in their status_instruction. Not applicable to agents with only SUCCESS/FAILURE. The template needs a conditional branch here.

**two_vs_three_state (conditional)**
- When ABORT is present in status_instruction: Include the abort_distinction fragment.
- When ABORT is absent: Omit it entirely. Do not mention ABORT to an agent whose protocol does not include it — this would create confusion about whether ABORT is available as a return state.
- PURPOSE: Keep the protocol description honest to the agent's actual contract. Mentioning states the agent cannot return introduces ambiguity.
- HYPOTHESIS: Agents presented with three states when they only have two will occasionally return ABORT inappropriately, having been primed with the concept. Keep the state space clean.
- STABILITY: High. This is a structural conditional, not a phrasing choice.

---

## STRUCTURAL: Completion Model and Its Retroactive Effect

### What the agent needs to understand

Knowing what "done" looks like changes how the agent works, not just how it finishes. An agent that knows it must report "exchanges processed count" will naturally maintain a counter. An agent that knows ABORT is valid will evaluate inputs early rather than discovering problems mid-execution. The return format is not a postscript — it is a mission briefing disguised as a reporting requirement.

### Fragments

**retroactive_orientation**
- Alternative A: "Understand your completion states before you begin. The metrics you must report should inform how you track your progress throughout execution."
- Alternative B: "Read your return specification carefully — it defines what 'done' means. The metrics listed here should guide your tracking during execution, not be assembled retroactively at the end."
- Alternative C: "Your return requirements imply tracking requirements. If you must report a count, maintain that count as you work. If you must report a path, know the path before you write."
- PURPOSE: Transform the return format from a post-hoc reporting template into a pre-execution orientation. The agent should read this section and adjust its working approach to naturally produce the required metrics.
- HYPOTHESIS: Without this framing, agents treat return format as an afterthought — they do their work, then try to reconstruct the required metrics from memory. This leads to inaccurate counts and missing values. Explicit "track as you go" instruction should improve metric accuracy.
- STABILITY: Medium-high. The principle is stable but the specific phrasing may need tuning based on whether agents actually adjust their approach or just acknowledge the instruction.

---

## STRUCTURAL: Honest Failure Reporting

### What the agent needs to understand

The return format intersects with the agent's willingness to report failure honestly. LLMs have a strong default toward reporting success — they will salvage bad output, paper over errors, and return SUCCESS with caveats rather than return clean FAILURE. The return format section is the last opportunity to counteract this bias before execution begins.

### Fragments

**failure_honesty**
- Alternative A: "FAILURE is a valid and expected return state. Do not salvage broken output to avoid returning FAILURE. A clean FAILURE with a clear reason is more valuable to the dispatcher than a SUCCESS with compromised output."
- Alternative B: "Return FAILURE when the conditions for failure are met. Do not attempt to recover failing work into a marginal success. The dispatcher handles failure — your job is to report it accurately."
- Alternative C: "An honest FAILURE is better than a dubious SUCCESS. If your work did not meet the success conditions, return FAILURE. The dispatch layer is designed to handle failure — do not hide it."
- Alternative D: "The dispatcher expects honest signals. Returning SUCCESS when the work is compromised corrupts downstream processing. FAILURE with a clear reason allows the system to respond correctly."
- PURPOSE: Counteract the LLM's bias toward success-reporting. This is not about the agent's ego — it is about signal integrity in the dispatch system. A false SUCCESS is worse than a true FAILURE because it propagates bad data downstream.
- HYPOTHESIS: This is one of the highest-impact fragments in the entire return format section. Without it, agents will return SUCCESS with qualifications ("SUCCESS, though some records had issues...") instead of clean FAILURE. Explicit permission and encouragement to fail honestly should materially improve signal quality.
- STABILITY: Very high. The success bias is a fundamental LLM behavior pattern that exists across all agents and all tasks. This fragment is universally needed.

**failure_cross_reference**
- Alternative A: "Your failure criteria (defined earlier) specify WHEN to fail. This section specifies HOW to report that failure. Both apply."
- Alternative B: "The conditions for failure are defined in your failure criteria. Here, you learn how to report failure to the dispatcher. These are complementary — one defines the trigger, the other defines the signal."
- Alternative C: (omit — let the agent connect the sections implicitly)
- PURPOSE: Bridge between failure_criteria and return_format. Without this, the agent may treat them as disconnected — understanding when to fail but not connecting it to the return protocol, or understanding the return protocol but not connecting it to the earlier failure definitions.
- HYPOTHESIS: Explicit cross-reference is likely helpful but may be unnecessary if the agent is competent enough to connect the sections itself. The risk of omission (C) is that the agent treats failure_criteria as advisory and return_format as the real failure spec, or vice versa.
- STABILITY: Medium. This is a bridging fragment whose necessity depends on how well the overall prompt holds together. It may be redundant in well-structured prompts.

---

## STRUCTURAL: Placement and Rendering Order

### What the agent needs to understand

The return format appears near the end of the prompt. This is deliberate — it is the last behavioral instruction before execution, which means it occupies the agent's most recent working memory when work begins.

### Fragments

**section_header**
- Alternative A: "## Return Protocol"
- Alternative B: "## Completion Contract"
- Alternative C: "## Dispatch Return"
- Alternative D: "## Return Format"
- PURPOSE: Set the interpretive frame for the section. "Return Protocol" emphasizes the machine-parsed nature. "Completion Contract" emphasizes the obligation. "Dispatch Return" emphasizes the audience. "Return Format" is neutral and descriptive.
- HYPOTHESIS: "Return Protocol" (A) best reinforces the protocol nature of the tokens and may prime the agent for protocol compliance. "Completion Contract" (B) may prime obligation but sounds legalistic. "Dispatch Return" (C) is precise about destination but may be unfamiliar. "Return Format" (D) is the weakest — it sounds like formatting instructions rather than behavioral specification.
- STABILITY: Medium. The header matters for framing but is not the primary behavioral driver. The content fragments carry more weight.

**section_placement**
- Current: Near end of prompt (after instructions, criteria, guardrails)
- Alternative placement: Before instructions (orient the agent to the destination before the journey)
- Assessment: End-of-prompt is correct for status-mode returns. The agent needs to understand what to do and what to avoid before it can meaningfully process what to report. Moving return format earlier would create forward references to failure states and metrics the agent has not yet learned about. The current placement also benefits from recency — the last thing the agent reads before execution is its completion model.
- STABILITY: High. End-of-prompt placement is correct and should not change.

---

## CONDITIONAL BRANCHES

### Branch 1: ABORT state present vs. absent
- **Condition:** ABORT appears in status_instruction
- **When present:** Include abort_distinction fragment, render three-state protocol description
- **When absent:** Omit ABORT entirely, render two-state protocol description (SUCCESS/FAILURE only)
- **Detection:** Parse status_instruction for the token "ABORT"

### Branch 2: mode = "status" vs. other modes
- **Condition:** mode field value
- **When "status":** Full protocol framing with token-first instruction, two-channel model (files + return), metrics obligation
- **When other (hypothetical "full" or "structured"):** Different framing would be needed — the return IS the output, not just a signal. Channel separation framing would not apply. This branch is theoretical based on current data.
- **Detection:** Direct enum comparison on mode field

### Branch 3: Metric complexity
- **Condition:** Number and type of metrics in status_instruction
- **Simple (1-2 metrics):** Light framing, metrics obligation may be implicit
- **Complex (3+ metrics, multiple states with different metrics):** Stronger tracking instruction, explicit retroactive_orientation fragment
- **Detection:** Count of distinct metric references in status_instruction

---

## CROSS-SECTION DEPENDENCIES

| Dependency | Direction | Nature |
|---|---|---|
| failure_criteria -> return_format | Forward reference | Failure criteria define WHEN; return format defines HOW to report. Agent must connect both. |
| success_criteria -> return_format | Forward reference | Success criteria define WHEN; return format defines HOW to report. The SUCCESS metrics should align with what success criteria measure. |
| instructions -> return_format | Implicit | Instructions describe the work; return format describes the reporting of completion. Metrics in return format should correspond to observable work outputs. |
| output_spec -> return_format | Parallel | Output spec defines where work products go (files). Return format defines where status goes (dispatcher). Two-channel model depends on both sections existing. |
| guardrails -> return_format | Implicit | Guardrails may produce failure conditions. Return format must accommodate reporting guardrail-triggered failures. |

---

## SUMMARY OF KEY DESIGN DECISIONS

1. **Protocol framing is non-negotiable.** The tokens must be understood as machine-parsed protocol, not conversational. This is the single highest-priority fragment in this section.

2. **Failure honesty framing is critical.** Counteracting the LLM success bias is the second highest-priority fragment. Without it, signal integrity in the dispatch system degrades.

3. **Two-channel model (files vs. return) must be explicit** for status mode. Without it, agents conflate output and return.

4. **ABORT distinction is important but conditional.** Only agents with ABORT in their protocol need this framing. Including it for two-state agents would be confusing.

5. **Retroactive orientation (track as you go) is a behavioral multiplier.** It transforms return format from postscript to pre-execution guidance. Medium-high priority.

6. **End-of-prompt placement is correct.** Recency effect means the completion model is the agent's freshest frame when execution begins.

7. **Section header "Return Protocol" best serves the behavioral goals** by priming protocol compliance from the first words of the section.
