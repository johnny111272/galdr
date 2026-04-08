# RETURN_FORMAT Section Analysis

## What This Section Accomplishes

Return format is the agent's **completion protocol**. It answers three questions simultaneously:

1. **What states can I end in?** (the exit codes)
2. **What must I report in each state?** (the payload)
3. **Who am I talking to when I'm done?** (the audience — a dispatcher, not a human)

This makes it fundamentally different from every other section. Every other section programs how the agent *works*. This section programs how the agent *stops working and reports*. It is the transition point where the agent ceases to be an autonomous actor and becomes a message sender in a larger system.

The behavioral effect is profound: an agent that understands its completion protocol works *toward defined endpoints* rather than drifting toward an open-ended sense of "done enough." It creates goal-directedness by defining what the finish line looks like in machine-parseable terms.

There is a second, subtler effect. An agent that knows it must report FAILURE with a structured reason is an agent that has *permission to fail cleanly*. Without explicit failure protocol, agents tend to hedge, partially succeed, or narrate problems rather than declaring a terminal state. The return format section is what gives the agent the vocabulary — and therefore the behavioral license — to stop and say "this broke, here's why."

---

## FIELD: mode

TYPE: enum (string)
VALUES: `"status"` / `"status"`

### What the agent needs to understand

The `mode` field selects the return protocol class. Both agents use `"status"`, which means: your primary output goes to files; your return value is a brief structured signal for the dispatcher. The agent is not returning its work product — it is returning a *report about* its work product.

This distinction matters because it tells the agent where its output lives. In status mode, the return message is metadata, not content. The agent should not try to cram its actual work into the return. It should write output to the designated locations and then send a terse signal.

Other plausible mode values (not observed but architecturally implied): `"content"` (return the work product itself), `"delegated"` (output already handled, just signal completion), `"streaming"` (output is incremental, return signals final state). The existence of the field implies the system was designed to support multiple return paradigms.

### Fragments

**mode_framing — How the mode value is introduced to the agent**

- Alternative A: "Your return mode is `status`. This means your actual output is written to files. Your return value is a brief status signal for the dispatcher — not the work product itself."
- Alternative B: "Return mode: status. Write all output to designated files. Return only a completion signal with summary metrics."
- Alternative C: "You operate in status-return mode. The dispatcher expects a machine-parseable completion signal, not your output content. Output goes to files; the return channel carries only status."
- Alternative D: "When you finish, you report status — not content. Your work is in the files you wrote. Your return message tells the dispatcher whether it worked and gives key metrics."

- PURPOSE: Prevent the agent from conflating "return" with "output." Without this framing, agents tend to dump their work product into the return, producing verbose responses that are neither good output nor good status signals. The framing creates a clean separation between the output channel (files) and the control channel (return).
- HYPOTHESIS: Explicitly naming the two channels (output = files, return = status signal) will produce more concise, machine-friendly return messages than simply saying "return SUCCESS." The agent needs to understand *why* its return should be terse — because its work lives elsewhere.
- STABILITY: High. The mode value is a system-level protocol decision. It does not vary with agent content or task complexity. If the mode is status, the framing is the same regardless of what the agent does. Only changes if new return modes are added to the system.

---

## FIELD: status_instruction

TYPE: free-form text (pre-authored per agent)
VALUES: Agent 1: "Return SUCCESS with the agent name, number of instruction steps, and number of include files. Return ABORT with a structured fault list if the requirements are insufficient. Return FAILURE if source materials cannot be read." / Agent 2: "Return SUCCESS when all exchange summaries are written and validated. Include interview uid, exchanges processed count, and output path. If any record fails validation and cannot be fixed, return FAILURE with clear reason."

### What the agent needs to understand

This is the per-agent protocol specification. It defines exactly which terminal states exist, what payload accompanies each state, and under what conditions each state triggers. This is the most behaviorally consequential part of return_format because it is what the agent actually *does* when it finishes.

Key structural observations:

1. **Terminal states are agent-specific.** Agent 1 has three (SUCCESS, ABORT, FAILURE). Agent 2 has two (SUCCESS, FAILURE). The number and meaning of states varies by task type.

2. **ABORT vs FAILURE is a meaningful distinction.** ABORT = "I examined the input and determined I cannot/should not proceed" (pre-execution rejection). FAILURE = "I attempted execution and it broke" (mid-execution breakdown). Not every agent needs ABORT. Agents with strict input requirements (builder) need it. Agents that process batches (summarizer) tend to either succeed or fail — there is no "I looked at the batch and decided not to start."

3. **Payloads are specific.** SUCCESS for builder = name + step count + include count. SUCCESS for summarizer = uid + exchange count + output path. These are not generic — they are the exact metrics the dispatcher needs to verify the work or route it downstream.

4. **The instruction is pre-authored, not generated.** The agent definition author wrote this text. The template's job is to present it with appropriate protocol framing, not to rewrite it.

### Fragments

**protocol_preamble — Framing that establishes "this is protocol, not suggestion"**

- Alternative A: "The following defines your return protocol. These are machine-parsed signals — use the exact tokens specified. Do not paraphrase, narrate, or wrap them in conversational language."
- Alternative B: "COMPLETION PROTOCOL: Your return message is parsed by the dispatcher. Use the exact state tokens below. Include the specified metrics. No additional prose."
- Alternative C: "When you complete, you send a structured return signal. The dispatcher reads this programmatically. Return exactly what is specified — the tokens SUCCESS, FAILURE, and ABORT are protocol keywords, not casual language."
- Alternative D: "Your final output is a protocol message. The state tokens (SUCCESS, FAILURE, ABORT) are machine-readable signals consumed by the dispatch system. Emit them exactly as specified with the required payload fields. Do not embellish."

- PURPOSE: Prevent the agent from treating the return as conversational prose. Without protocol framing, agents write things like "I've successfully completed the task! Here's what I did..." instead of "SUCCESS: agent-builder, 12 steps, 4 includes." The preamble shifts the agent's mental model from "writing a response" to "sending a signal."
- HYPOTHESIS: Explicit mention of machine parsing and exact tokens will produce more consistent, parseable returns than simply presenting the status_instruction alone. The agent needs to understand it is writing to a machine, not a person.
- STABILITY: High. This framing applies to all agents in status mode. The specific tokens may vary per agent, but the "this is protocol" framing is universal to the mode.

**state_token_presentation — How the actual states and payloads are presented**

- Alternative A: Present the status_instruction verbatim as a quoted block, preceded by "Your return states:" — trusting the pre-authored text to be sufficient.
- Alternative B: Parse the status_instruction into a structured format — one state per line, condition and payload separated. E.g., `SUCCESS: [condition] → [payload fields]` / `FAILURE: [condition] → [payload fields]`.
- Alternative C: Present the status_instruction verbatim but append a synthetic example of each state's expected output format, derived from the instruction text.
- Alternative D: Present the status_instruction verbatim, then add a single-line "Format: STATE_TOKEN: metric1, metric2, metric3" template showing the expected shape without inventing specific values.

- PURPOSE: The status_instruction is pre-authored and may vary in quality and structure. The question is whether the template should add formatting assistance or trust the authored text. Over-formatting risks rigidity; under-formatting risks ambiguous returns.
- HYPOTHESIS: Alternative A (verbatim) is safest for stability — the definition author knows what they want. Alternative D (verbatim + shape hint) adds marginal formatting guidance without rewriting the instruction. Alternative B (parsed) risks misinterpreting the authored intent. Alternative C (examples) risks the template inventing incorrect examples.
- STABILITY: The status_instruction itself is per-agent and authored externally — HIGH variance in content but the *presentation mechanism* should be stable. The template fragment wrapping it should be invariant; only the content changes.

**abort_distinction — Whether to explicitly teach the ABORT vs FAILURE difference**

- Alternative A: "ABORT means you stopped before performing work because the inputs were insufficient or invalid. FAILURE means you attempted work and encountered an unrecoverable error. These are different states — do not conflate them."
- Alternative B: "Three terminal states: SUCCESS (work completed), ABORT (work not attempted — input insufficient), FAILURE (work attempted but broke). Choose the state that matches what happened."
- Alternative C: No explicit teaching — the status_instruction already specifies when each applies. Trust the authored text.
- Alternative D: "If you determine the inputs are insufficient before beginning work, return ABORT — not FAILURE. FAILURE is reserved for errors during execution. This distinction matters for the dispatcher's retry and routing logic."

- PURPOSE: The ABORT/FAILURE distinction is semantically meaningful for dispatch routing. An ABORT means "don't retry, fix the inputs." A FAILURE means "might be transient, or might need investigation." Conflating them produces incorrect dispatch behavior.
- HYPOTHESIS: Agents without explicit instruction tend to use FAILURE for everything, including input rejection. Teaching the distinction produces cleaner dispatch signals. However, this is only relevant when ABORT is a defined state — it should be conditional.
- STABILITY: Low for presence (only applies to agents with ABORT), high for content (the distinction is system-level, not per-agent). This is a **conditional fragment** — emitted only when the status_instruction contains ABORT.

**completion_as_goal — Framing that orients the agent toward defined endpoints**

- Alternative A: "Everything above defines your work. This section defines what 'done' looks like. You are working toward one of the states defined below."
- Alternative B: "Your task is complete when you can emit one of the following return states with accurate metrics. Work toward that endpoint."
- Alternative C: No explicit completion framing — the return format's position at the end of the prompt is itself the signal.
- Alternative D: "The dispatcher is waiting for your return signal. When you reach a terminal state — whether success or failure — report it immediately with the specified payload. Do not continue work after reaching a terminal state."

- PURPOSE: Give the agent a concrete sense of "done" rather than an open-ended sense of "keep working until it feels finished." This is especially important for batch tasks where the agent might process items indefinitely without a clear stopping point.
- HYPOTHESIS: Explicit completion framing reduces over-work (agents continuing to polish after the task is done) and under-reporting (agents reaching a terminal state but not declaring it). Alternative D adds the "stop when done" instruction which prevents post-completion drift.
- STABILITY: Medium. The concept is universal, but whether it is needed depends on task type. Batch tasks benefit more than single-output tasks. Could be stable as a default fragment that is always included — the cost of including it when unnecessary is low.

---

## STRUCTURAL: section_position

### What the agent needs to understand

Return format appears at or near the end of the agent prompt. This is the last behavioral instruction before execution begins. The question is whether this position is correct, or whether return format should appear earlier to orient the agent's work.

### Fragments

**position_rationale — Whether to address why this comes last**

- Alternative A: Place return format last and add no comment. The position speaks for itself — "this is the last thing you read before you start working, so it defines what you're working toward."
- Alternative B: Place return format last with explicit framing: "Now that you understand your task, here is how you report completion."
- Alternative C: Place return format EARLY (after role, before instructions) with framing: "Before you begin, understand what 'done' looks like. You are working toward one of these terminal states." Then repeat the states briefly at the end as a reminder.
- Alternative D: Place return format last but open with a forward reference early in the prompt: "You will receive your completion protocol at the end of these instructions. Your work targets a defined terminal state."

- PURPOSE: Position affects behavioral weight. Instructions at the end of a prompt benefit from recency — they are fresh in the context window when generation begins. Instructions at the beginning benefit from primacy — they frame all subsequent processing. Return format is both protocol (favoring end — precise, fresh) and goal-orientation (favoring beginning — frames the work).
- HYPOTHESIS: Alternative B (last, with transition framing) is the most practical. It preserves recency for protocol precision while the transition sentence ("now that you understand your task") links it to everything above. Alternative C (early + late) is theoretically strongest but doubles the section's token cost and introduces repetition. Alternative D (forward reference) is a middle ground that may not justify its complexity.
- STABILITY: High. Position is a template-level decision, not a per-agent decision. Once chosen, it applies to all agents.

---

## STRUCTURAL: section_header

### What the agent needs to understand

The section header signals what kind of content follows. For return format, the header needs to communicate "this is protocol, not more task instructions."

### Fragments

**header_text — The section heading itself**

- Alternative A: `## Return Format`
- Alternative B: `## Completion Protocol`
- Alternative C: `## Return Protocol`
- Alternative D: `## How to Report Completion`
- Alternative E: `## Terminal States`

- PURPOSE: Set the agent's expectation for what follows. "Return Format" is descriptive but generic. "Completion Protocol" signals formality and machine-parseable structure. "Terminal States" is precise but jargon-heavy.
- HYPOTHESIS: "Completion Protocol" or "Return Protocol" best communicate the dual nature: this is about completion (goal-orientation) AND it is protocol (machine-precise). "Return Format" is adequate but undersells the behavioral significance. "How to Report Completion" is too conversational for protocol content.
- STABILITY: High. Header is a template-level decision. Once chosen, it is the same for all agents.

---

## Cross-Section Dependencies

### return_format <-> failure_criteria
Failure criteria define WHEN to fail. Return format defines HOW to report the failure. These are complementary: failure_criteria says "if validation fails on a record, that is a failure condition." Return format says "when you hit a failure condition, return FAILURE with the reason." An agent missing either half will either fail silently (no return protocol) or report failures that were never defined as failure conditions (no failure criteria).

**Design implication:** The template should not repeat failure conditions in the return format section. It should reference them: "If you encounter a condition defined in your failure criteria, return FAILURE as specified below." This keeps failure definition in one place and return reporting in another.

### return_format <-> success_criteria
Similar complementary relationship. Success criteria define what "done correctly" means. Return format defines the SUCCESS payload. The metrics in the SUCCESS return (agent name, step count, include count) are the *evidence* that success criteria were met.

**Design implication:** SUCCESS metrics should align with success criteria — the dispatcher should be able to verify success criteria fulfillment from the return payload alone, or at least triage whether further verification is needed.

### return_format <-> execution_instructions
Execution instructions define the workflow. Return format defines the endpoint. These create a directed arc: "do this work, then report this way." The transition from "working" to "reporting" is managed by the return format section.

**Design implication:** The last execution instruction should naturally flow into the return format section. If the last instruction is "validate all outputs," the return format should follow immediately: "once validation is complete, report as follows."

### return_format <-> role
The role section defines who the agent is. Return format defines how that agent communicates completion to the system. An agent with a creative role (builder) may need more explicit protocol framing because its default mode is generative prose. An agent with a mechanical role (batch processor) may need less because it is already oriented toward structured output.

**Design implication:** Protocol framing intensity might be conditional on role type, but this adds complexity. A simpler approach: make protocol framing consistently explicit for all agents, accepting minor redundancy for mechanical roles.

### return_format <-> guardrails
Guardrails define what the agent must NOT do. Return format defines what the agent MUST do at completion. There is a potential interaction: a guardrail might say "never fabricate metrics" and the return format says "include these metrics." The agent needs to understand that return metrics must be accurate, not fabricated to match the expected format.

**Design implication:** Consider whether the protocol preamble should include a brief accuracy clause: "Report actual metrics from your execution. Do not fabricate values to match the expected format."

---

## Conditional Branches

### Branch: ABORT state present vs absent

**Condition:** The status_instruction text contains "ABORT" as a defined terminal state.

**When present (e.g., agent-builder):**
- Include the abort_distinction fragment explaining ABORT vs FAILURE
- The protocol preamble should list three states, not two
- The completion_as_goal fragment should acknowledge three possible endpoints

**When absent (e.g., interview-enrich-create-summary):**
- Omit the abort_distinction fragment entirely
- The protocol preamble lists two states
- Simpler completion model: either it worked or it didn't

**Detection:** Parse the status_instruction for the token "ABORT" (case-sensitive, as protocol tokens are uppercase).

### Branch: mode = "status" vs other modes

**Condition:** The mode field value.

**When mode = "status":**
- Include mode_framing explaining the output/signal channel separation
- Return is terse and structured
- Agent writes output to files, returns only status

**When mode = other (hypothetical):**
- Different framing needed — the return IS the output, or the return is delegated
- mode_framing fragment would need entirely different alternatives

**Current state:** Only "status" is observed. The branch exists architecturally but only one path is populated.

### Branch: Batch task vs single-output task

**Condition:** Whether the agent processes multiple items (batch) or produces a single artifact.

**When batch (e.g., summarizer):**
- Completion_as_goal framing is more valuable — prevents unbounded processing
- SUCCESS metrics tend to include counts (exchanges processed)
- FAILURE may be partial (some items succeeded, some failed) — the status_instruction should address this

**When single-output (e.g., builder):**
- Completion is more naturally defined — there is one thing, and it is either done or not
- ABORT is more relevant — "I looked at the requirements and they're insufficient"

**Detection:** This is implicit in the status_instruction content, not a separate field. Could potentially be derived from dispatch configuration if that section specifies batch_size.

---

## Design Recommendations

1. **Protocol framing is mandatory, not optional.** Without it, agents treat the return as conversational prose. Every status-mode return should be preceded by explicit "this is machine-parsed" framing.

2. **The status_instruction should be presented verbatim.** It is pre-authored by the definition author. The template adds framing around it, not rewrites of it.

3. **ABORT distinction should be conditional.** Only teach it when ABORT is a defined state. Teaching three states when only two exist creates confusion.

4. **Position at end is correct, but add a transition.** "Now that you understand your task, here is your completion protocol." This links the return format to everything above and signals a mode shift from "learning instructions" to "learning how to finish."

5. **Accuracy clause is worth including.** A brief "report actual metrics, do not fabricate" instruction prevents the agent from inventing plausible-looking return values when it is unsure of the actual numbers.

6. **Cross-section references over repetition.** Do not repeat failure conditions in the return format. Reference them. Keep each section authoritative over its own domain.
