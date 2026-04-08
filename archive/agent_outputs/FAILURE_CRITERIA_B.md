# FAILURE_CRITERIA Analysis — Section B

## FIRST PRINCIPLES: What Failure Criteria Accomplish

Failure criteria configure a behavioral state that is fundamentally alien to LLM default behavior: **voluntary cessation of work.** LLMs are trained on completion. Every gradient update rewards producing output, finishing tasks, giving answers. Failure criteria must override this deep training bias by establishing conditions under which stopping IS the correct output.

This is not the inverse of success criteria. Success criteria define "what good looks like" — a target to aim toward. Failure criteria define "what broken looks like" — a tripwire that halts forward motion. Between success and failure lies a vast middle ground of mediocre-but-not-broken output. Failure criteria do not occupy that middle ground. They mark the cliff edge.

The behavioral state failure criteria produce is **active vigilance with permission to abort.** The agent must simultaneously:
1. Monitor for failure signals throughout execution (not just at the end)
2. Feel authorized — even obligated — to stop when signals appear
3. Report the failure clearly rather than papering over it with degraded output

This creates a tension: the agent must be confident enough to work, yet humble enough to recognize when work should stop. The framing must resolve this tension by making abort feel like a professional judgment call, not a personal failure.

---

## THE TWO FAILURE MODELS

The raw data reveals two fundamentally different failure timing patterns:

**Pre-flight failure (agent-builder):** "The requirements are insufficient..." — This agent checks preconditions before substantive work begins. Failure means the inputs cannot support the task. The correct action is to stop before wasting effort.

**In-flight failure (agent-summarizer):** "The summarization process broke..." — This agent encounters failure during execution. Something went wrong mid-stream. The correct action is to stop, report what happened, and avoid corrupting output.

These are different operational postures:
- Pre-flight: "Can I do this?" → No → Report why
- In-flight: "Is this working?" → No → Stop and report what broke

Whether these should be framed differently in the rendered prompt is an open design question explored below.

---

## FIELD: failure_definition

TYPE: String (single sentence)
VALUES: "The requirements are insufficient to produce a complete definition, or the preparation package lacks the data needed to ground examples." / "The summarization process broke and output could not be completed — input unreadable, output records could not be written, or unrecoverable error."

### What the agent needs to understand

The failure_definition is the **category label** for a class of failure. It names the kind of broken. Unlike success_definition (which names what "done right" looks like), failure_definition names what "gone wrong" looks like. It answers: "What general condition am I watching for?"

The definition serves as the agent's mental model for a failure mode. When it reads "the summarization process broke," it creates a category in working memory: PROCESS BREAKAGE. The evidence items then populate that category with specific detection signals. Without the definition, evidence items are disconnected symptoms. With it, they form a coherent failure narrative.

Critically, the definition also establishes **scope of failure.** Builder's definition scopes failure to input insufficiency — it does not cover "I made a bad definition." Summarizer's definition scopes failure to process breakage — it does not cover "the summaries are mediocre." This scoping prevents the agent from catastrophizing every imperfection into a failure state.

### Fragments

**Failure Category Framing**

- Alternative A: "**Abort condition:** {failure_definition}"
  - Mechanical, clinical. Positions failure as a system state, not a judgment on the agent.
- Alternative B: "**Recognize this failure mode:** {failure_definition}"
  - Positions the agent as a diagnostician. Failure is something to identify, not something that happens to you.
- Alternative C: "**Stop work if you determine:** {failure_definition}"
  - Direct imperative. Makes the abort action explicit in the framing itself.
- Alternative D: "**This work cannot succeed when:** {failure_definition}"
  - Reframes failure as impossibility rather than inadequacy. The agent is not failing; the conditions make success impossible.

- PURPOSE: Establish the failure definition as a named, bounded category that the agent monitors for, while making abort feel like correct professional behavior rather than task abandonment.
- HYPOTHESIS: Alternative D ("cannot succeed when") will produce the best abort behavior because it externalizes failure — the agent is not broken, the situation is broken. This removes the completion-bias pressure because the agent is not "giving up," it is recognizing impossibility. Alternative A may be too clinical and get glossed over. Alternative B is good but passive. Alternative C is direct but may trigger the "I should try harder" instinct.
- STABILITY: HIGH for definition content (it names a real failure mode that is either present or not). MEDIUM for framing choice (the same definition with different framing will produce meaningfully different abort thresholds — too gentle and the agent pushes through failures, too harsh and it aborts on minor issues).

---

## FIELD: failure_evidence

TYPE: Array of strings (detection signals)
VALUES: 3 items (builder) / 4 items (summarizer)

### What the agent needs to understand

Evidence items are **specific, observable signals** that indicate the failure_definition condition is present. They are detection criteria, not consequences. The agent should be scanning for these signals, and when one is detected, it triggers evaluation of whether the failure_definition applies.

The relationship between definition and evidence is: definition = the disease, evidence = the symptoms. You do not diagnose the disease abstractly; you detect symptoms and conclude the disease is present.

Importantly, evidence items have different temporal characteristics:
- Builder evidence is **checkable upfront:** "Requirements do not specify..." / "No sample data found..." / "Required fields cannot be determined..." — All of these can be evaluated before substantive work begins.
- Summarizer evidence is **discovered during execution:** "Any exchange skipped..." / "Output count does not match..." / "Input could not be read..." / "Schema validation failure..." — These emerge as work progresses.

This temporal difference matters for how the agent processes evidence: upfront-checkable evidence should be evaluated as a pre-flight checklist, while execution-discovered evidence should be monitored as ongoing watchpoints.

### Fragments

**Evidence List Introduction**

- Alternative A: "Watch for these signals:\n{evidence_list}"
  - Positions evidence as ongoing monitoring targets. Implies vigilance throughout.
- Alternative B: "Any of the following indicates this failure:\n{evidence_list}"
  - Logical framing. Any single signal is sufficient to trigger the failure category.
- Alternative C: "You MUST abort if you observe:\n{evidence_list}"
  - Obligation framing. Makes abort mandatory, not optional, upon detection.
- Alternative D: "Symptoms that confirm this failure mode:\n{evidence_list}"
  - Diagnostic framing. Evidence confirms a diagnosis, agent is the diagnostician.
- Alternative E: "Before continuing, verify none of these apply:\n{evidence_list}" (pre-flight only) / "During processing, stop if any of these occur:\n{evidence_list}" (in-flight only)
  - Temporally split framing. Different introduction for pre-flight vs in-flight evidence.

- PURPOSE: Establish evidence items as detection signals that the agent actively monitors, with clear behavioral consequence (abort) upon detection.
- HYPOTHESIS: Alternative C ("MUST abort") provides the strongest behavioral signal but risks over-triggering on ambiguous cases. Alternative B ("any of the following indicates") is precise and logical — it establishes that evidence items are individually sufficient, which is important because the agent might otherwise wait for multiple signals. Alternative E is the most precise but requires the renderer to distinguish pre-flight from in-flight failure, adding complexity. Alternative A is natural but weak — "watch for" does not clearly state what to DO when a signal is detected.
- STABILITY: HIGH for evidence content (these are specific, falsifiable conditions). MEDIUM-LOW for framing (the same evidence with obligation vs permission framing will produce very different abort thresholds). The framing must thread the needle: too permissive and the agent ignores signals, too mandatory and ambiguous cases cause premature abort.

**Evidence Item Formatting**

- Alternative A: Bulleted list, bare text: "- {evidence_item}"
  - Clean, scannable. Each item is a standalone signal.
- Alternative B: Numbered list: "1. {evidence_item}"
  - Implies ordering or priority, which may not be intended.
- Alternative C: Conditional formatting: "- IF {evidence_item} THEN this failure applies"
  - Makes the logical structure explicit: each item is a conditional trigger.
- Alternative D: Signal notation: "- SIGNAL: {evidence_item}"
  - Labels each item explicitly as a detection signal, reinforcing the monitoring posture.

- PURPOSE: Present individual evidence items in a format that reinforces their role as independently sufficient detection signals.
- HYPOTHESIS: Alternative A (bulleted, bare) is likely sufficient. The context established by the list introduction carries the semantic weight. Alternative C (conditional) is the most precise but adds verbosity that may dilute scanning behavior. Alternative D (signal notation) adds useful labeling at minimal cost.
- STABILITY: HIGH. Formatting is cosmetic once the introduction establishes the right mental model.

---

## STRUCTURAL: Section Header and Framing

### What the agent needs to understand

The section header establishes the agent's entire orientation toward this content. It must accomplish three things simultaneously:
1. Signal that this content defines STOP conditions (not quality targets)
2. Create permission/obligation to abort (overcoming completion bias)
3. Distinguish this from success criteria, constraints, and rules

### Fragments

**Section Title**

- Alternative A: "## Failure Criteria"
  - Direct, matches the field name. But "failure" may trigger avoidance behavior — the agent does not want to think about failure.
- Alternative B: "## When to Stop"
  - Action-oriented. Reframes failure as a decision point rather than an outcome.
- Alternative C: "## Abort Conditions"
  - Technical, precise. This is systems language — abort is a defined operation, not an emotional state.
- Alternative D: "## Recognizing Broken Input or Process"
  - Diagnostic framing. Positions the agent as someone who recognizes problems, not someone who fails.
- Alternative E: "## Conditions That Prevent Success"
  - Inverts the framing: these are not YOUR failures, they are conditions that make success impossible regardless of effort.

- PURPOSE: Establish the behavioral frame for all content that follows. The title primes how every subsequent line is interpreted.
- HYPOTHESIS: Alternative E ("Conditions That Prevent Success") is the strongest candidate because it externalizes failure and removes the completion-bias pressure. The agent is not failing; it is recognizing that external conditions have made success impossible. Alternative C ("Abort Conditions") is precise and professional but may feel cold. Alternative B ("When to Stop") is clear but lacks the externalization that helps override completion bias. Alternative A is functional but the word "failure" creates resistance to engagement.
- STABILITY: HIGH impact on downstream interpretation. This is a load-bearing naming decision. The wrong title can undermine carefully crafted evidence and definition framing.

**Section Preamble**

- Alternative A: "Stopping work is the correct response when these conditions are met. Producing output despite these conditions would be worse than reporting the failure."
  - Explicitly validates stopping. Directly addresses the completion-bias concern by framing continued work as the WRONG choice.
- Alternative B: "The following conditions make successful completion impossible. If you detect any of these, report the failure rather than producing degraded output."
  - Impossibility framing + explicit instruction to report rather than degrade.
- Alternative C: "Not every task can be completed. These conditions indicate that this task cannot produce valid output, and attempting to force output would violate quality standards."
  - Normalizes incompletability. Links forced output to quality violation, which leverages the agent's desire to maintain quality.
- Alternative D: (No preamble — let definitions and evidence speak for themselves.)
  - Minimal approach. Avoids over-explaining. But loses the opportunity to prime the abort-is-correct mindset.

- PURPOSE: Override the LLM's default completion bias by explicitly establishing that stopping is a valid, correct, and sometimes obligatory action.
- HYPOTHESIS: Alternative A is the most direct and may be the most effective. It names the tension ("stopping work") and resolves it ("is the correct response"). Alternative C is sophisticated — it normalizes failure and links forced output to quality violation, which is a powerful motivator. Alternative D risks the agent treating failure criteria as informational rather than actionable if there is no explicit instruction to act on them. Alternative B is clean and precise but may not fully override completion bias because it does not address the emotional/behavioral component.
- STABILITY: MEDIUM-HIGH. The preamble is important for first-time processing but may be skimmed on re-reads. Its effects are priming effects — they shape interpretation of what follows but are not referenced back to directly.

---

## STRUCTURAL: Pre-Flight vs In-Flight Failure Distinction

### What the agent needs to understand

The two agents demonstrate fundamentally different failure timing:
- Builder checks conditions BEFORE substantive work (pre-flight)
- Summarizer detects failures DURING execution (in-flight)

Should the rendering system distinguish these? Or treat all failure criteria uniformly?

### Fragments

**Unified Treatment**

- Alternative A: Render all failure criteria identically regardless of timing. Let the evidence items themselves signal whether they are pre-flight or in-flight checkable.
  - Simpler rendering. Evidence items are self-describing ("requirements do not specify" is obviously pre-flight, "exchange skipped" is obviously in-flight).
- Alternative B: Add a timing annotation to each failure_criteria entry (e.g., `timing = "pre-flight"` or `timing = "in-flight"`) and render differently.
  - More precise but adds schema complexity. The renderer must handle two modes.

**Split Treatment**

- Alternative C: "Before beginning work, verify:" (pre-flight section) + "During execution, watch for:" (in-flight section) — split within the rendered output.
  - Most precise behavioral instruction. Different timing = different monitoring posture.
- Alternative D: Render pre-flight as a checklist ("Confirm before proceeding:") and in-flight as watchpoints ("Monitor during execution:").
  - Different formatting for different behavioral requirements: checklist vs monitoring.

- PURPOSE: Determine whether the failure criteria rendering should account for temporal differences in when failures are detectable.
- HYPOTHESIS: Alternative A (unified) is the pragmatic choice. The evidence items are self-describing, and adding timing annotations increases schema complexity for minimal behavioral gain. The agent can infer from "requirements do not specify" that this is checkable upfront. However, if testing shows agents fail to check pre-flight conditions before starting work, Alternative C or D becomes necessary. This is a candidate for A/B testing.
- STABILITY: LOW — this is a design decision that should be revisited based on observed agent behavior. Start unified, add temporal distinction if agents demonstrate timing-blind failure detection.

---

## STRUCTURAL: Relationship Between Failure Criteria and Return Format

### What the agent needs to understand

Failure criteria define WHEN to abort. Return format defines HOW to report. These are tightly coupled: a failure criterion without a corresponding return path is a dead end. The agent detects failure but does not know what to do about it.

### Fragments

**Explicit Cross-Reference**

- Alternative A: "When a failure condition is met, report it using the failure return format described in [return section]."
  - Direct pointer. Agent knows where to look for reporting instructions.
- Alternative B: Include a brief inline instruction: "When a failure condition is met, set status to FAILURE and include the specific evidence signal in your report."
  - Self-contained. Agent does not need to cross-reference another section.
- Alternative C: No cross-reference. Assume the agent will connect failure detection to failure reporting through the return format section.
  - Minimal. Relies on the agent's ability to compose instructions from separate sections.

- PURPOSE: Ensure failure detection leads to proper failure reporting, not to silence or degraded output.
- HYPOTHESIS: Alternative B is the safest choice. It gives the agent enough information to act correctly even if it does not perfectly recall the return format section. Alternative A is cleaner but requires the agent to hold a cross-reference in working memory. Alternative C is risky — the gap between "I detected failure" and "here is how to report it" is where agents are most likely to fall back to completion behavior (producing something, anything, rather than reporting nothing).
- STABILITY: HIGH — this cross-reference is structurally important regardless of how failure criteria or return format are individually rendered.

---

## STRUCTURAL: Single vs Multiple Failure Criteria Entries

### What the agent needs to understand

Both agents have exactly one failure_criteria entry. But the schema allows multiple. How should multiple entries be rendered?

### Fragments

**Multiple Entry Rendering**

- Alternative A: Each entry is a separate failure mode with its own definition and evidence. Render as separate blocks under a shared header.
  - Clean separation. Each failure mode is self-contained and independently triggered.
- Alternative B: Render as a numbered sequence of failure modes: "Failure Mode 1: ... Failure Mode 2: ..."
  - Implies ordering, which may or may not be meaningful.
- Alternative C: Render with explicit independence: "Any ONE of the following failure modes is sufficient to trigger abort:"
  - Makes the OR relationship explicit. The agent does not need all failure modes to be present.

- PURPOSE: Ensure agents correctly interpret multiple failure criteria as independently sufficient abort triggers, not as a cumulative threshold.
- HYPOTHESIS: Alternative C is the most behaviorally precise. Without the explicit "any one," agents may implicitly assume they need to see MULTIPLE failure modes before aborting, especially if they have been trained on threshold-based decision patterns. Alternative A is clean but leaves the independence implicit. Alternative B adds false ordering.
- STABILITY: MEDIUM — current data has only single entries, so this is speculative. But the design must accommodate the multi-entry case because the schema allows it.

---

## STRUCTURAL: Obligation vs Permission to Abort

### What the agent needs to understand

This is the deepest behavioral design question for failure criteria. Two mental models:

1. **Permission model:** "You MAY stop if these conditions are met." The agent is allowed to abort but retains judgment about whether to try harder.
2. **Obligation model:** "You MUST stop if these conditions are met." The agent is required to abort when conditions are detected. No judgment, no "trying harder."

### Fragments

**Abort Behavioral Stance**

- Alternative A: Pure obligation: "When any failure evidence is detected, you MUST stop work and report the failure. Do not attempt to work around these conditions."
  - Removes all ambiguity. Agent has no choice. But may cause premature abort on edge cases.
- Alternative B: Qualified obligation: "When failure evidence is clearly present, stop work and report. If evidence is ambiguous, note the concern and proceed with caution."
  - Allows judgment for ambiguous cases. But "ambiguous" is itself ambiguous — agents may classify most evidence as ambiguous to avoid aborting.
- Alternative C: Strong permission: "These conditions indicate that continuing work will not produce valid output. When you detect them, the correct action is to stop and report."
  - Positions abort as correct without making it mandatory. The agent is guided to the right choice without being commanded.
- Alternative D: Consequence framing: "Continuing past these failure conditions produces output that will be rejected. Stopping and reporting saves effort and prevents invalid output from entering the pipeline."
  - Appeals to outcome. The agent stops not because it is told to, but because continuing is wasteful.

- PURPOSE: Determine the abort threshold — how easily should the agent trigger failure mode?
- HYPOTHESIS: Alternative A (pure obligation) is correct for tight batch tasks (summarizer) where failure conditions are binary and unambiguous. Alternative C (strong permission) is better for broad creative tasks (builder) where some failure conditions (e.g., "requirements are insufficient") involve genuine judgment. The optimal choice may depend on agent type, which means this could be a conditional rendering decision based on agent metadata. Alternative D is appealing but may not be strong enough to override completion bias in practice.
- STABILITY: LOW — this is the highest-impact design variable in the failure criteria section. The wrong choice either produces agents that never abort (too permissive) or agents that abort too eagerly (too mandatory). This MUST be tested empirically.

---

## CROSS-SECTION DEPENDENCIES

### failure_criteria <-> success_criteria
- These define opposite poles but are NOT logical inverses. Success = quality threshold achieved. Failure = process broken or preconditions unmet. The gap between them is "mediocre but functional." Failure criteria should never reference success criteria language — they are independent evaluation axes.

### failure_criteria <-> guardrails (constraints + anti-patterns)
- Guardrails define how to work. Failure criteria define when NOT to work. A constraint violation during work is a guardrail issue. An unworkable input condition is a failure criteria issue. The boundary: "Can I do this task at all?" (failure criteria) vs "Am I doing this task correctly?" (guardrails).

### failure_criteria <-> return_format
- Tightly coupled. Failure criteria trigger the failure return path. The return_format section must define what a failure report looks like. If failure criteria exist, the return format MUST have a failure reporting mechanism. This is a hard structural dependency.

### failure_criteria <-> execution_instructions
- Execution instructions define the work process. Failure criteria define when to exit that process early. The interaction: failure evidence detection should be woven into the execution flow, not relegated to a post-execution check. For pre-flight failures, this means step 1 of execution should be "verify failure conditions are not present." For in-flight failures, this means each execution step should have implicit failure monitoring.

### failure_criteria <-> role/identity
- The agent's role informs how it relates to failure. A "quality auditor" role makes failure detection feel natural (auditors find problems). A "builder" role makes failure detection feel like admission of defeat. The role framing can either reinforce or undermine the abort-is-correct message.

---

## CONDITIONAL BRANCHES

### Branch: Agent has no failure_criteria
- Some agents may not define failure criteria. This means either: (a) failure is not possible (unlikely), (b) failure conditions are implicit in other sections, or (c) the definition author chose not to specify them.
- Rendering: Omit the section entirely. Do NOT render a "no failure criteria defined" message — this would prime the agent to think about failure without giving it useful detection signals.

### Branch: Single failure entry vs multiple
- Single: Render directly under section header.
- Multiple: Render with explicit independence language ("any one of the following").
- The structural fragments above address this.

### Branch: Pre-flight vs in-flight failure (inferred from evidence content)
- If all evidence items are input-checkable: Consider rendering as a pre-flight checklist.
- If evidence items are execution-discoverable: Render as monitoring watchpoints.
- If mixed: Unified rendering with temporal self-description in evidence items.
- Decision: Start unified, split if testing shows timing-blind behavior.

### Branch: Tight batch task vs broad creative task
- Tight batch: Failure conditions are typically binary (input unreadable, count mismatch). Obligation framing works well.
- Broad creative: Failure conditions involve judgment (requirements "insufficient"). Permission framing with strong guidance works better.
- This suggests the abort behavioral stance (obligation vs permission) could be a conditional rendering parameter based on agent type or a metadata flag.

### Branch: Failure criteria with vs without return_format cross-reference
- With return_format: Include cross-reference to failure reporting mechanism.
- Without return_format: Failure criteria still function as abort triggers, but the agent may not know HOW to report. This is a schema design question: should failure_criteria require return_format to be defined?

---

## OPEN DESIGN QUESTIONS

1. **Should the schema include a timing field?** (`timing = "pre-flight" | "in-flight" | "any"`) This would allow the renderer to frame failure evidence differently based on when it is detectable. Current data suggests this is inferrable from evidence content, but explicit annotation would be more reliable.

2. **Should abort strength be configurable?** A field like `abort_strength = "mandatory" | "recommended"` would let definition authors control how aggressively the agent aborts. This addresses the obligation-vs-permission tension directly at the schema level.

3. **Should failure criteria be rendered near the TOP of the prompt?** Pre-flight failure criteria are most useful when checked early. Rendering them after execution instructions means the agent may begin work before encountering the abort conditions. Prompt placement is a rendering decision but has behavioral implications.

4. **What is the interaction between failure criteria and retry behavior?** The summarizer includes "Schema validation failure not resolved after retry" — this implies the agent should retry before aborting. Should retry-before-abort be a general pattern, or is it specific to certain evidence types? This may need a retry annotation on individual evidence items.

5. **Should failure evidence items have severity levels?** Some evidence ("input could not be read") is absolute — there is nothing to do. Other evidence ("requirements do not specify domain judgment") involves judgment about what "specify" means. Severity levels could distinguish binary signals from judgment-dependent signals, allowing the renderer to frame them differently.
