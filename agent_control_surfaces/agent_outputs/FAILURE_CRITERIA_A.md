# FAILURE_CRITERIA — Control Surface Analysis

## Preamble: What Failure Criteria Actually Do

Failure criteria configure the agent's **abort circuitry**. They are not the inverse of success criteria. Success criteria define a target state the agent verifies after work is done. Failure criteria define conditions the agent must detect **as they arise** and respond to by halting — not by trying harder, not by producing partial output, not by degrading gracefully. Halting.

This is a fundamentally adversarial instruction to give an LLM. Language models are completion machines. Their training reward comes from producing helpful, thorough responses. Telling a model to stop producing output and report a failure state goes against the grain of its optimization surface. The framing of failure criteria must therefore accomplish something unusual: it must make aborting feel like the **correct, professional, responsible** action — not a failure of the agent, but a successful detection of a broken precondition.

The behavioral state this section produces is **armed vigilance with a license to halt**. The agent enters execution knowing that certain observable conditions constitute abort triggers, and that detecting and reporting these conditions is itself a form of correct operation. The agent is not "failing" when it aborts — it is succeeding at a different task: the task of not producing garbage.

---

## STRUCTURAL: Section Framing

### What the agent needs to understand

The agent must understand three things before it encounters any specific criteria:
1. These are not warnings — they are halt conditions.
2. Detecting a halt condition and reporting it IS successful behavior.
3. Continuing past a halt condition produces output that is worse than no output.

The framing must reposition "abort" from "I failed at my task" to "I correctly identified that this task cannot produce valid output under current conditions." This is the single most important behavioral calibration in the section.

### Fragments

**section_header**
- Alternative A: `## Failure Criteria`
- Alternative B: `## Abort Conditions`
- Alternative C: `## Halt Triggers`
- Alternative D: `## When to Stop`
- PURPOSE: Name the section in a way that signals its behavioral function.
- HYPOTHESIS: "Failure Criteria" is the most semantically precise but carries connotations of agent inadequacy. "Abort Conditions" is operationally clearer — it frames these as environmental/input states, not agent performance. "Halt Triggers" is the most mechanical, reducing emotional loading. "When to Stop" is the most direct but may feel informal for a structured prompt.
- STABILITY: HIGH. The name propagates through agent self-understanding. A name that implies agent failure will make the agent reluctant to invoke these criteria. A name that implies correct detection behavior will make it more willing.

**section_preamble**
- Alternative A: `Detecting any of these conditions and halting is correct behavior. Continuing past them produces invalid output. If you observe these conditions, stop work and report the failure — this is not a failure on your part, it is a successful detection of conditions that prevent valid output.`
- Alternative B: `The following conditions make valid output impossible. When detected, halt immediately and report. An agent that detects a halt condition and stops is performing correctly. An agent that ignores a halt condition and produces output anyway has failed.`
- Alternative C: `These are not aspirational warnings. Each condition below is an observable state that, when true, means the task cannot succeed. Your responsibility is detection and reporting, not remediation. Do not attempt to work around these conditions.`
- Alternative D: `You have a license to halt. The conditions below define when exercising that license is mandatory. Output produced after a halt condition is detected is worse than no output — it is confidently wrong output that downstream consumers will trust.`
- PURPOSE: Override the model's completion bias. Make halting feel like the professional choice.
- HYPOTHESIS: The core tension is between the model's training (complete the task) and the desired behavior (abort the task). The preamble must resolve this tension by redefining what "completing the task" means when halt conditions are present. Alternative A is empathetic and direct. Alternative B is more structured and creates a clear inversion (halting = success, continuing = failure). Alternative C emphasizes non-remediation — critical because models will try to "fix" problems rather than report them. Alternative D introduces the "license to halt" framing which is psychologically potent — it grants permission rather than imposing obligation.
- STABILITY: CRITICAL. Without this framing, models will systematically underweight failure criteria and attempt to produce output regardless. The specific wording matters less than the behavioral reframe being present and unambiguous.

**temporal_model_framing**
- Alternative A: (No explicit temporal framing — let each criterion's definition imply when to check.)
- Alternative B: `Some conditions are detectable before work begins (insufficient input). Others emerge during execution (process breakage). Check pre-flight conditions first — if they fail, do not begin work.`
- Alternative C: `Evaluate these conditions continuously. Some will be apparent immediately; others may only surface during processing. The moment any condition becomes true, halt.`
- PURPOSE: Address the pre-flight vs in-flight distinction observed in the raw data. The builder's failure is detectable before work starts; the summarizer's failure emerges during processing.
- HYPOTHESIS: Alternative A is cleanest but loses the behavioral distinction — an agent may start work on an insufficient input and only realize later it should have stopped. Alternative B makes the pre-flight/in-flight distinction explicit, which helps the agent prioritize early checks. Alternative C treats all conditions as continuous monitoring, which is simpler but may cause unnecessary overhead for pre-flight checks.
- STABILITY: MEDIUM. The temporal model matters more for complex agents (builder) than simple ones (summarizer). For batch processors, all conditions are effectively in-flight. For creative/analytical agents, pre-flight checks prevent wasted work. This may need to be conditional on agent type.

---

## STRUCTURAL: criteria Array Wrapper

### What the agent needs to understand

The criteria array is a list of distinct failure modes. Each entry is independent — any single criterion being met is sufficient to trigger a halt. The agent needs to understand that these are OR-connected, not AND-connected.

### Fragments

**criteria_logical_relationship**
- Alternative A: (Implicit — each criterion stands alone, no explicit connective language.)
- Alternative B: `Each criterion below is independently sufficient to trigger a halt. If ANY single criterion is met, stop.`
- Alternative C: `These are independent halt conditions. You do not need to observe all of them — any one is enough.`
- PURPOSE: Clarify that failure criteria are disjunctive. One criterion met = halt.
- HYPOTHESIS: This is probably obvious from context but worth being explicit about. Models sometimes treat lists as checklists (all must be true) rather than trigger sets (any one is sufficient). Alternative A risks this misinterpretation. Alternatives B and C are functionally equivalent; B is more imperative, C is more explanatory.
- STABILITY: MEDIUM. For agents with a single failure criterion, this is irrelevant. For agents with multiple, it prevents a dangerous misreading where the agent waits for "enough" failures before halting.

---

## FIELD: failure_definition

TYPE: String (one per criteria entry)
VALUES: "The requirements are insufficient to produce a complete definition, or the preparation package lacks the data needed to ground examples." / "The summarization process broke and output could not be completed — input unreadable, output records could not be written, or unrecoverable error."

### What the agent needs to understand

The `failure_definition` is the **named failure mode** — a human-readable description of a category of failure. It is NOT the detection mechanism (that's what evidence is for). It is the high-level characterization of what went wrong, suitable for inclusion in a failure report.

Structurally, the definition serves as:
1. A cognitive anchor — the agent reads this and forms a mental model of what this failure "looks like."
2. A reporting label — when the agent halts, it can reference this definition as the reason.
3. A severity signal — the definition implies whether this is "bad input" (external fault) or "broken process" (execution fault).

Examining the two values:
- Builder: "requirements are insufficient" — this is an INPUT QUALITY judgment. The agent is told that sometimes the input simply isn't good enough to produce output. This is a pre-flight abort.
- Summarizer: "summarization process broke" — this is a PROCESS INTEGRITY judgment. The agent is told that sometimes the machinery fails during execution. This is an in-flight abort.

These represent two fundamental failure archetypes:
1. **Input insufficiency** — the task is impossible given the input.
2. **Process breakage** — the task should be possible but something went wrong during execution.

### Fragments

**definition_label**
- Alternative A: `**Failure mode:**`
- Alternative B: `**Halt condition:**`
- Alternative C: `**Abort trigger:**`
- Alternative D: (No label — the definition is rendered as the first line of each criteria block, unlabeled.)
- PURPOSE: Label the definition field within the rendered prompt.
- HYPOTHESIS: The label should match the section header's framing. If the section is "Abort Conditions," then "Abort trigger" is consistent. If "Failure Criteria," then "Failure mode" is consistent. Alternative D (no label) works if the structure is obvious from layout — but explicit labels reduce ambiguity. "Halt condition" is the most operationally precise: it tells the agent this is a condition, not a judgment.
- STABILITY: LOW. This is a formatting choice that should be consistent with the section header but has minimal behavioral impact on its own.

**definition_rendering**
- Alternative A: Render the definition as-is, as a plain text statement.
- Alternative B: Render the definition as a bold or emphasized block, visually distinct from evidence items.
- Alternative C: Render the definition as a conditional: `IF [definition], THEN halt and report.`
- PURPOSE: Control how the definition is visually and semantically presented.
- HYPOTHESIS: Alternative A is simplest and relies on the section preamble to establish the halt semantics. Alternative B uses visual hierarchy to separate the failure category (definition) from the detection signals (evidence). Alternative C makes the conditional logic explicit — the definition is a predicate, halting is the consequent. Alternative C is the most behaviorally precise but may feel mechanical for naturally-worded definitions.
- STABILITY: MEDIUM. The rendering interacts with how evidence is presented. If evidence is rendered as sub-bullets under the definition, visual hierarchy (B) helps. If evidence is rendered as a separate list, plain text (A) is sufficient.

---

## FIELD: failure_evidence

TYPE: Array of strings (multiple per criteria entry)
VALUES: Builder has 3 items (input quality signals); Summarizer has 4 items (process breakage signals).

### What the agent needs to understand

`failure_evidence` items are **detection signals** — observable conditions that indicate the parent failure definition is true. Unlike success evidence (which is verified post-hoc), failure evidence must be **monitored continuously** during execution.

The relationship between definition and evidence:
- The **definition** is the abstract failure mode (what went wrong).
- The **evidence** items are the concrete observables (how you'd know).

An agent should halt when it observes evidence items. The definition tells the agent WHY it's halting (for reporting). The evidence tells the agent WHAT TO WATCH FOR (for detection).

Key behavioral distinction from success evidence:
- Success evidence = checklist verified at the end. "Did I do all these things?"
- Failure evidence = tripwires monitored throughout. "Am I seeing any of these things?"

Examining the values:

Builder evidence items:
1. "Requirements do not specify what the agent judges, assesses, or transforms" — detectable at input reading time (pre-flight).
2. "No sample data found in the preparation package" — detectable at input reading time (pre-flight).
3. "Required definition fields cannot be determined from the requirements" — detectable during early analysis (pre-flight or early in-flight).

All three are pre-flight checks. The builder should evaluate these before committing to full execution.

Summarizer evidence items:
1. "Any exchange skipped without a summary being written" — detectable during processing (in-flight).
2. "Output record count does not match input record count" — detectable after processing (post-flight, but still a failure).
3. "Input tempfile could not be read or parsed as JSONL" — detectable at input reading (pre-flight).
4. "Schema validation failure not resolved after retry" — detectable during output writing (in-flight).

The summarizer has a mix: one pre-flight check (#3), two in-flight checks (#1, #4), and one post-flight check (#2). This suggests failure evidence naturally spans the entire execution lifecycle.

### Fragments

**evidence_label**
- Alternative A: `**Evidence (any one is sufficient):**`
- Alternative B: `**Watch for:**`
- Alternative C: `**Detection signals:**`
- Alternative D: `**You should halt if you observe:**`
- PURPOSE: Label the evidence list and signal its behavioral function.
- HYPOTHESIS: Alternative A is explicit about the disjunctive logic (any one = halt). Alternative B frames the items as ongoing vigilance targets — "watch for" implies continuous monitoring. Alternative C is clinical and precise. Alternative D combines the label with the behavioral instruction, which is the most direct but potentially redundant with the section preamble. "Watch for" (B) best captures the continuous-monitoring nature of failure evidence.
- STABILITY: MEDIUM. The label shapes whether the agent treats evidence as a post-hoc checklist or ongoing monitoring. "Watch for" and "Detection signals" both push toward monitoring. "Evidence" alone may default to post-hoc verification.

**evidence_rendering**
- Alternative A: Bulleted list under the definition, no special formatting.
- Alternative B: Bulleted list with each item prefixed by a detection-timing hint: `[pre-flight]`, `[in-flight]`, `[post-flight]`.
- Alternative C: Bulleted list with conditional phrasing: `IF <condition> THEN this failure mode applies.`
- Alternative D: Bulleted list presented as observable states: `- You observe that [evidence item]`
- PURPOSE: Render evidence items in a way that maximizes detection behavior.
- HYPOTHESIS: Alternative A is simplest but treats evidence as inert text. Alternative B adds timing metadata — useful but requires the definition author to classify each item, adding complexity to the authoring process. Alternative C makes each item a conditional, which is logically precise but verbose. Alternative D rephrases items as first-person observations, which may increase the agent's likelihood of pattern-matching against its actual experience during execution. The best choice depends on whether the authoring burden of B is justified by the behavioral benefit.
- STABILITY: LOW-MEDIUM. The raw definitions already have enough clarity that simple bulleted rendering (A) probably works. Timing hints (B) add value for complex agents but increase authoring overhead.

**evidence_logical_connective**
- Alternative A: (Implicit disjunction — the section preamble already established that any criterion is sufficient.)
- Alternative B: Explicit within-evidence disjunction: `Any single observation below is sufficient to trigger this failure mode.`
- Alternative C: Explicit at the evidence list level: items joined with `OR` markers.
- PURPOSE: Clarify that evidence items within a single criterion are also disjunctive — observing ANY one of the evidence items means the failure definition applies.
- HYPOTHESIS: This is a second level of disjunction (first level: any criterion triggers halt; second level: any evidence item triggers its parent criterion). Alternative A relies on the preamble and label ("any one is sufficient") to carry this. Alternative B is explicit per-evidence-list. Alternative C is the most visually obvious but clutters the layout. Given that evidence items are detection signals, disjunction is the natural reading — if you see smoke OR hear an alarm OR smell gas, the fire condition applies. Explicit marking (B) is worth the clarity cost.
- STABILITY: MEDIUM. Getting this wrong means the agent waits to observe ALL evidence items before triggering, which defeats the purpose of early detection.

---

## STRUCTURAL: Definition-Evidence Relationship

### What the agent needs to understand

The two-level structure (definition + evidence array) creates a hierarchy:
- **Definition** = the failure mode (abstract, reportable, categorical).
- **Evidence** = the detection signals (concrete, observable, actionable).

The agent's behavioral loop should be:
1. Read definitions to understand what categories of failure exist.
2. Read evidence to know what to watch for.
3. During execution, when an evidence item is observed, map it to its parent definition.
4. Report the failure using the definition (the "what went wrong") and cite the evidence (the "how I know").

This mapping is crucial for the return_format section, which defines how failures are reported.

### Fragments

**hierarchy_framing**
- Alternative A: (No explicit framing — let the indentation/nesting of definition and evidence communicate the hierarchy.)
- Alternative B: `Each failure mode has a definition (what went wrong) and evidence signals (how you detect it). When reporting a failure, cite both the mode and the specific evidence you observed.`
- Alternative C: `Definitions describe categories of failure. Evidence items are the observable symptoms. You halt when you detect a symptom; you report the category.`
- PURPOSE: Make the two-level hierarchy explicit so the agent knows how to USE both fields, not just read them.
- HYPOTHESIS: Alternative A works if the visual structure is clear enough. Alternative B is instructional — it tells the agent the reporting protocol. Alternative C is the most precise about the different roles of definition vs. evidence. The reporting instruction in B is important because it connects failure_criteria to return_format — the agent needs to know that failure definitions become failure reports.
- STABILITY: MEDIUM-HIGH. Without this framing, agents may report vague failures ("something went wrong") rather than structured ones ("failure mode X detected via evidence Y"). The connection to return_format makes this a cross-section dependency.

---

## STRUCTURAL: Pre-flight vs In-flight Failure Models

### What the agent needs to understand

The raw data reveals two distinct failure temporalities:
1. **Pre-flight failures** (builder pattern): The input is insufficient. Detect before starting work. Abort before producing any output.
2. **In-flight failures** (summarizer pattern): The process breaks during execution. Detect during work. Abort and report partial state.

These have different behavioral implications:
- Pre-flight: The agent should evaluate failure conditions FIRST, before entering its main execution loop.
- In-flight: The agent should monitor failure conditions CONTINUOUSLY during execution.

A single agent may have both types of failure (the summarizer has one pre-flight check: "input tempfile could not be read").

### Fragments

**temporal_model_instruction**
- Alternative A: (No temporal instruction — the agent infers timing from the evidence wording.)
- Alternative B: `Evaluate evidence items that can be checked before starting work FIRST. If any pre-flight condition is met, halt immediately without beginning the main task.`
- Alternative C: `Some evidence items are checkable before work begins; others only become observable during execution. Prioritize early detection — check what you can before you start, and monitor the rest throughout.`
- Alternative D: Evidence items are explicitly tagged with timing by the definition author: `[CHECK BEFORE STARTING]` vs `[MONITOR DURING EXECUTION]`.
- PURPOSE: Help the agent detect failures as early as possible.
- HYPOTHESIS: Alternative A is the simplest and may be sufficient — the builder's evidence items are obviously pre-flight, the summarizer's are obviously in-flight. But "obviously" to a human reader may not be "obviously" to a model. Alternative B gives an explicit instruction to check early. Alternative C is more nuanced and covers the mixed case. Alternative D pushes the burden to the definition author, which increases precision but adds authoring complexity. Given that early detection prevents wasted work and potentially invalid partial output, some explicit instruction (B or C) is worth including.
- STABILITY: MEDIUM. More important for agents with expensive execution (the builder does substantial creative work that's wasted if requirements are insufficient). Less important for cheap batch processors.

---

## CROSS-SECTION DEPENDENCIES

### failure_criteria -> return_format
The return_format section defines HOW failures are reported. Failure criteria define WHEN to report and WHAT the failure is. These sections must be tightly coupled:
- The failure definition becomes the failure reason in the return.
- The failure evidence becomes the supporting detail in the return.
- The return_format must have a failure pathway that accommodates the structured information from failure_criteria.

**Design implication:** The failure_criteria rendering should reference the return_format or at least establish that failure definitions and evidence will be used in the failure report. Without this link, the agent may halt but produce an unstructured or unhelpful failure report.

### failure_criteria -> success_criteria
These are NOT inverses. They define different thresholds on a quality spectrum:
- Failure criteria define the FLOOR — below this, output is invalid and must not be produced.
- Success criteria define the CEILING — above this, output is complete and correct.
- Between them is a gray zone where output is "not broken but not great."

**Design implication:** The prompt should never frame failure criteria as "the opposite of success." They occupy a different behavioral register. The section preamble should establish this independence.

### failure_criteria -> guardrails (constraints, anti-patterns)
Guardrails define ongoing behavioral boundaries. Failure criteria define halt conditions. The distinction:
- Violating a guardrail means the agent is doing something WRONG but should correct course.
- Meeting a failure criterion means the agent should STOP.

**Design implication:** The failure criteria section should not duplicate guardrail content. If a constraint is "never fabricate data," that's a guardrail. If "input data is unreadable," that's a failure criterion. The former is about agent behavior; the latter is about environmental state.

### failure_criteria -> execution_instructions
Execution instructions define the processing steps. Failure evidence items often reference specific points in the execution flow ("input tempfile could not be read" = failure at step 1; "output record count does not match" = failure at the final step). The execution instructions should ideally reference failure checks at the appropriate points, or the failure criteria should reference execution steps.

**Design implication:** There's a potential for rendering failure checks INLINE with execution steps rather than in a separate section. This would increase detection likelihood but decrease the section's standalone readability. A hybrid approach — standalone section with cross-references — may be optimal.

---

## CONDITIONAL BRANCHES

### Single vs Multiple Failure Criteria Entries

The raw data shows both agents have exactly one `[[failure_criteria.criteria]]` entry. But the structure allows for multiple entries.

- **Single entry:** The section preamble about disjunction between criteria is unnecessary. The evidence-level disjunction is still relevant.
- **Multiple entries:** The two-level disjunction (any criterion, any evidence within a criterion) must both be explicit.

**Design implication:** The rendering should handle both cases gracefully. For single-entry agents, avoid language that implies multiple failure modes exist. For multi-entry agents, make the OR-relationship between criteria explicit.

### Pre-flight-only vs In-flight-only vs Mixed Failure Models

- **Pre-flight-only** (builder pattern): All evidence is checkable before starting. The agent should evaluate all conditions first, then either proceed or halt. The framing can be "check these conditions before beginning work."
- **In-flight-only** (hypothetical pure batch processor): All evidence emerges during execution. The framing should be "monitor these conditions during processing."
- **Mixed** (summarizer pattern): Some evidence is pre-flight, some is in-flight. The framing must accommodate both: "check what you can before starting; monitor the rest during execution."

**Design implication:** The temporal model instruction (if included) should be conditional on the agent's failure evidence profile. Alternatively, a generic "prioritize early detection" instruction covers all cases acceptably.

### Agents with No Failure Criteria

Some agents may have no failure criteria at all — their task always produces some output, even if mediocre. In this case, the section should be omitted entirely, not rendered as an empty section. An empty "Failure Criteria" section sends confusing signals.

**Design implication:** The rendering logic must handle the zero-criteria case by omitting the section.

---

## OPEN DESIGN QUESTIONS

1. **Should failure evidence be rendered inline with execution steps?** This would increase detection likelihood but create a cross-section rendering dependency. The standalone section is cleaner but may be less effective behaviorally.

2. **Should the definition-evidence hierarchy be flattened for simple cases?** When an agent has one criterion with one evidence item, the two-level structure is overhead. But consistency across agents may be worth the cost.

3. **How explicit should the abort-is-success reframe be?** Too subtle and the model ignores it. Too heavy and it reads as defensive or patronizing. The right calibration depends on model behavior testing.

4. **Should failure criteria reference specific return_format fields?** E.g., "When halting, populate the `failure_reason` field with the failure definition and the `failure_evidence` field with the observed evidence items." This is highly specific and couples the sections tightly, but it's also highly actionable.

5. **Is there a meaningful distinction between "halt and report" and "halt and retry"?** The summarizer's evidence item about schema validation says "not resolved after retry" — implying a retry happened before the failure was declared. Should failure criteria encode retry semantics, or is that an execution instruction concern?
