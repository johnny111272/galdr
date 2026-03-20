# SUCCESS_CRITERIA Section Analysis

## FIRST PRINCIPLES: What Does This Section Do?

Success criteria are not a post-hoc checklist. They are a **behavioral shaping mechanism** that operates before, during, and after execution. When an agent internalizes success criteria, three things happen:

1. **Goal formation.** The agent constructs an internal model of what "done" looks like. This is not the same as understanding instructions — instructions say what to do, success criteria say what the result should be. An agent that reads "summarize each exchange" knows the task. An agent that also reads "every exchange number in the input appears exactly once in the output" knows what complete execution looks like. The difference is between knowing the verb and knowing the target state.

2. **Quality calibration.** Success evidence items set the resolution of the agent's self-evaluation. Without them, the agent's notion of "good enough" is whatever its training suggests. With them, the agent has specific dimensions to evaluate against. This is especially powerful for judgment-based evidence ("summaries reflecting accumulated conversational significance") because it names a quality dimension the agent might not spontaneously attend to.

3. **Completion detection.** The agent needs to know when to stop. Success criteria provide the stopping condition — not "when you've processed all inputs" (that's a loop termination) but "when these conditions hold" (that's a quality gate). This distinction matters because an agent can process all inputs and still not be done if the outputs don't meet the criteria.

The behavioral effect depends critically on **when** the agent encounters the criteria relative to the task. If success criteria come before instructions, they prime goal-oriented reasoning. If they come after, they function as a verification checklist. If they come interleaved with execution steps, they function as per-step quality gates. The rendering strategy must make a deliberate choice here.

---

## THE DEFINITION-EVIDENCE HIERARCHY

The `success_definition` and `success_evidence` fields form a two-level structure that maps to a well-known cognitive pattern: **claim and warrant**. The definition is the claim ("this is what success looks like"), and the evidence items are warrants ("here is how you know the claim holds").

This is NOT a summary-detail relationship. A summary compresses information; the definition does not compress the evidence items. "Every input exchange has been contextually summarized and written as a validated output record" is not a compression of the five evidence items — it is a different level of abstraction. The evidence items are TESTS of the definition, not EXPANSIONS of it.

This has rendering implications. If presented as summary-detail, the agent may treat evidence as elaboration and skim it. If presented as claim-warrant, the agent treats evidence as the operational content and the definition as the framing.

---

## FIELD: success_definition

TYPE: String (single sentence, declarative)
VALUES: "A complete TOML definition and include files have been written that fully specify the agent described in the requirements." / "Every input exchange has been contextually summarized and written as a validated output record."

### What the agent needs to understand

The success definition is the agent's highest-level success predicate — the single statement that, if true, means the task succeeded. It operates at a different granularity than evidence items. The definition answers "what does done look like?" while evidence answers "how do I verify done?"

The definition also serves as a **disambiguation anchor** when evidence items could be interpreted multiple ways. "Examples are grounded in actual data shapes" could mean many things in isolation; anchored to "fully specify the agent described in the requirements," it means grounded in a way that serves specification completeness, not grounded in a way that serves documentation clarity.

There is a tension in how declaratively vs imperatively to frame the definition. The raw data uses declarative-resultative framing ("have been written," "has been summarized"), describing a state of the world after success. This is distinct from imperative ("write a complete TOML definition") or conditional ("if every input exchange has been summarized, the task is complete").

### Fragments

**definition_frame_declarative** — Present the definition as a state of the world that holds when the task is complete.
- Alternative A: "Success: {success_definition}"
- Alternative B: "The task is complete when the following is true: {success_definition}"
- Alternative C: "Your goal is to reach a state where: {success_definition}"
- PURPOSE: Frame success as a target state, orienting the agent toward an end condition rather than a process.
- HYPOTHESIS: Declarative framing produces more self-monitoring behavior because the agent repeatedly checks "does this state hold yet?" rather than "have I followed the steps?" This should reduce cases where the agent completes all steps but produces output that doesn't actually satisfy the definition.
- STABILITY: HIGH. The raw data already uses declarative-resultative phrasing. This fragment preserves authorial intent. The only variation is in the framing wrapper.

**definition_frame_imperative** — Present the definition as a direct instruction.
- Alternative A: "You succeed by: {definition rewritten as imperative}"
- Alternative B: "Achieve the following: {definition rewritten as imperative}"
- Alternative C: "Your job is to ensure that {definition rewritten as present-tense assertion}"
- PURPOSE: Make the definition feel like a direct command rather than an abstract goal, increasing urgency and directness.
- HYPOTHESIS: Imperative framing may produce faster task initiation but weaker self-monitoring. The agent treats the definition as another instruction rather than as a quality predicate. This could lead to "I did the thing" rather than "the thing I did meets the bar."
- STABILITY: LOW. Requires rewriting author-supplied declarative text into imperative, which introduces transformation risk and may lose nuance. "Have been written that fully specify" carries different weight than "write files that fully specify."

**definition_frame_conditional** — Present the definition as a conditional gate.
- Alternative A: "The task succeeds if and only if: {success_definition}"
- Alternative B: "Before declaring completion, verify: {success_definition}"
- Alternative C: "Do not stop until: {success_definition}"
- PURPOSE: Make the definition explicitly function as a completion gate — the agent must evaluate this predicate before finishing.
- HYPOTHESIS: Conditional framing produces the strongest completion-checking behavior. The agent is explicitly told this is a gate, not a description. However, it may also produce premature evaluation — the agent checking the gate after each step rather than building toward it holistically.
- STABILITY: MEDIUM. The transformation is minimal (adding a conditional wrapper), but the behavioral effect is strong and may not suit all agent types. Batch-processing agents (summarizer) benefit from clear gates; creative agents (builder) may be over-constrained by "if and only if" language.

### Cross-section dependencies

- **Instructions:** The definition must not duplicate instruction content. If instructions say "summarize each exchange," the definition should not also say "summarize each exchange" — it should say what the result of successful summarization looks like. Overlap creates ambiguity about whether the definition is an instruction or a quality predicate.
- **Failure criteria:** The definition and failure definitions must not be logical inverses. If they are, one is redundant. In practice, the success definition describes a positive target state while failure definitions describe specific breakdown modes.
- **Return/output:** The definition implicitly references what the agent produces. "A complete TOML definition... has been written" implies a written artifact. The return section defines how that artifact is delivered. These must be consistent.

### Conditional branches

- **Single vs multiple definitions:** The structure allows multiple `[[success_criteria.criteria]]` entries, each with its own definition. When multiple definitions exist, the rendering must clarify whether they are conjunctive (all must hold) or disjunctive (any suffices). The raw data suggests conjunctive — multiple success dimensions all required.
- **Definition specificity:** The builder's definition references a specific artifact type ("TOML definition and include files"). The summarizer's definition references a transformation property ("every input exchange has been... summarized"). Rendering might need to handle artifact-oriented vs property-oriented definitions differently, or it might not — this depends on whether the distinction matters behaviorally.

---

## FIELD: success_evidence

TYPE: Array of strings (each a single assertion)
VALUES: 6 items (builder) / 5 items (summarizer)

### What the agent needs to understand

Evidence items are the operational teeth of success criteria. The definition says what success is; evidence items say how to verify it. Each evidence item is an independently evaluable assertion that, taken together, constitute sufficient proof that the definition holds.

The critical design question is: **are evidence items a checklist or a mindset?** If a checklist, the agent evaluates each one at the end. If a mindset, the agent internalizes them as ongoing quality constraints. The answer depends on the evidence type:

- **Mechanically verifiable evidence** ("Output record count equals input record count") functions naturally as a checklist item. The agent can count and compare.
- **Judgment-based evidence** ("Examples are grounded in actual data shapes from the preparation package") cannot be mechanically checked. It functions as a quality orientation — a dimension the agent should attend to throughout execution, not just at the end.
- **Negative evidence** ("No instruction step contains operational content") is a constraint to maintain during execution, not a condition to check afterward. By the time you check at the end, the violation is already baked in.

This heterogeneity in evidence types is a key design challenge. A single rendering strategy may not serve all types equally.

### Fragments

**evidence_as_checklist** — Present evidence items as a verification list the agent checks against its output.
- Alternative A: "Verify each of the following before completing:\n- [ ] {evidence_1}\n- [ ] {evidence_2}\n..."
- Alternative B: "Your output must satisfy all of the following conditions:\n1. {evidence_1}\n2. {evidence_2}\n..."
- Alternative C: "Final verification — confirm each holds:\n- {evidence_1}\n- {evidence_2}\n..."
- PURPOSE: Make evidence items function as an explicit quality gate at task completion. The agent processes, then verifies, then submits.
- HYPOTHESIS: Checklist framing produces reliable coverage of all evidence items but may concentrate quality attention at the end rather than throughout. For mechanical evidence, this is fine. For judgment-based evidence, this is too late — you cannot retroactively make examples "grounded in actual data shapes" without reworking them.
- STABILITY: HIGH for batch-processing agents where output is produced then checked. MEDIUM for creative agents where quality must be maintained throughout construction.

**evidence_as_quality_dimensions** — Present evidence items as dimensions of quality the agent should attend to throughout execution.
- Alternative A: "Throughout your work, maintain awareness of these quality dimensions:\n- {evidence_1}\n- {evidence_2}\n..."
- Alternative B: "The following define what quality means for this task:\n- {evidence_1}\n- {evidence_2}\n..."
- Alternative C: "Hold these standards as you work — they define success:\n- {evidence_1}\n- {evidence_2}\n..."
- PURPOSE: Internalize evidence as ongoing quality orientation rather than terminal verification. The agent considers each dimension as it works, not just at the end.
- HYPOTHESIS: Quality-dimension framing produces more consistent adherence to judgment-based evidence but may slow execution as the agent repeatedly evaluates against multiple dimensions. It also risks the agent treating evidence items as soft suggestions rather than hard requirements.
- STABILITY: MEDIUM. This framing works well for judgment-based evidence but over-weights mechanical evidence. "Output record count equals input record count" does not need to be an ongoing quality dimension — it is a terminal check.

**evidence_as_assertions** — Present evidence items as assertions that must be true of the completed work, stated as facts about the output.
- Alternative A: "When complete, the following will be true of your output:\n- {evidence_1}\n- {evidence_2}\n..."
- Alternative B: "A successful output has these properties:\n- {evidence_1}\n- {evidence_2}\n..."
- Alternative C: "These statements describe your output when the task is done correctly:\n- {evidence_1}\n- {evidence_2}\n..."
- PURPOSE: Frame evidence as properties of the output rather than actions for the agent. This shifts the locus from "what you must do" to "what the result is."
- HYPOTHESIS: Assertion framing produces the cleanest separation between process (instructions) and outcome (success criteria). The agent understands that success is defined by output properties, not by process adherence. This may produce more creative problem-solving since the agent is free to find any path to the asserted properties.
- STABILITY: HIGH. The raw data already uses assertion-style phrasing ("Every requirement maps to...", "Output record count equals..."). This fragment preserves the existing voice.

**evidence_mixed_strategy** — Render mechanical evidence as verification items and judgment-based evidence as quality orientations, within the same block.
- Alternative A: "Quality standards (maintain throughout):\n- {judgment_evidence}\n\nVerification checks (confirm at completion):\n- {mechanical_evidence}"
- Alternative B: "As you work, ensure:\n- {judgment_evidence}\n\nBefore finishing, verify:\n- {mechanical_evidence}"
- Alternative C: "These define the quality of your work:\n- {judgment_evidence}\n\nThese are checkable at the end:\n- {mechanical_evidence}"
- PURPOSE: Handle the heterogeneity of evidence types by rendering them differently based on their nature.
- HYPOTHESIS: Mixed strategy produces the most behaviorally appropriate handling but requires the renderer to classify evidence items as mechanical vs judgment-based. This classification is itself a judgment call and may be difficult to automate reliably.
- STABILITY: LOW. Requires semantic classification of evidence items that is not present in the raw data. Would need either author annotation or automated classification, both of which add complexity and fragility.

### Cross-section dependencies

- **Guardrails/anti-patterns:** Some evidence items are phrased as negatives ("No instruction step contains operational content," "No source quality markers appear"). These overlap conceptually with guardrails (things to avoid). The rendering must distinguish between "absence of bad things" (success evidence) and "do not do bad things" (guardrails). The difference is temporal: guardrails constrain behavior during execution; success evidence verifies properties of the output.
- **Instructions:** Evidence items that reference specific process expectations ("Every exchange number in the input appears exactly once in the output") imply processing behavior. This overlaps with instruction content. The rendering must ensure instructions describe HOW to process and evidence describes WHAT correct processing produces, without circular reference.
- **Examples:** The builder's evidence includes "Examples are grounded in actual data shapes from the preparation package." This references the examples section. Success evidence can reference other sections, creating a web of dependencies that the rendering must handle gracefully.

### Conditional branches

- **Evidence count:** The builder has 6 items; the summarizer has 5. There is no structural minimum or maximum. Rendering must handle 1 to N items gracefully without becoming either a wall of text (many items) or feeling trivially obvious (one item).
- **All-mechanical vs all-judgment vs mixed:** An agent could have all mechanical evidence (pure batch validator), all judgment evidence (creative agent), or a mix (most agents). The rendering strategy should degrade gracefully across all three cases.
- **Negative vs positive evidence:** Some evidence is phrased positively ("Every summary is a single sentence") and some negatively ("No source quality markers appear"). Rendering may or may not need to handle these differently. Positive evidence says what to see; negative evidence says what not to see. Both are verifiable, but negative evidence is harder to confirm exhaustively.

---

## STRUCTURAL: definition_evidence_relationship

### What the agent needs to understand

The relationship between the definition and its evidence array is the core structural element of this section. The definition is not a title and the evidence is not body text. The definition is a claim and the evidence items are its warrants. This relationship must be clear in rendering.

### Fragments

**relationship_claim_warrant** — Explicitly frame the definition as a claim and evidence as warrants.
- Alternative A: "{success_definition}\n\nThis is demonstrated by:\n- {evidence_1}\n..."
- Alternative B: "{success_definition}\n\nSpecifically, this means:\n- {evidence_1}\n..."
- Alternative C: "{success_definition}\n\nThe proof is:\n- {evidence_1}\n..."
- PURPOSE: Make the hierarchical relationship explicit. The definition is the top-level assertion; evidence items prove it.
- HYPOTHESIS: Claim-warrant framing produces the clearest understanding of why evidence items matter — each one exists to prove the definition, not as independent requirements. This prevents the agent from treating evidence items as an unrelated list.
- STABILITY: HIGH. This relationship is inherent in the data structure. The fragments merely make it linguistically explicit.

**relationship_goal_criteria** — Frame definition as goal and evidence as acceptance criteria.
- Alternative A: "Goal: {success_definition}\n\nAcceptance criteria:\n- {evidence_1}\n..."
- Alternative B: "Objective: {success_definition}\n\nMet when:\n- {evidence_1}\n..."
- Alternative C: "Target: {success_definition}\n\nVerified by:\n- {evidence_1}\n..."
- PURPOSE: Use familiar software engineering terminology (goal/acceptance criteria) to signal the relationship.
- HYPOTHESIS: Goal-criteria framing leverages the agent's training on software specs, producing precise evaluation behavior. However, it may over-formalize the relationship, making judgment-based evidence feel out of place (acceptance criteria are typically binary).
- STABILITY: MEDIUM. Works well for mechanical evidence but may clash with judgment-based evidence that doesn't have a clean pass/fail boundary.

**relationship_flat** — Present definition and evidence as a single flat list without explicit hierarchy.
- Alternative A: "Success means:\n- {success_definition}\n- {evidence_1}\n- {evidence_2}\n..."
- Alternative B: "The following must all be true:\n- {success_definition}\n- {evidence_1}\n..."
- Alternative C: "Complete when:\n- {success_definition}\n- {evidence_1}\n..."
- PURPOSE: Flatten the hierarchy, treating the definition as just another criterion alongside evidence items.
- HYPOTHESIS: Flat presentation is simpler but loses the hierarchical relationship. The agent may treat all items as equally weighted, missing that the definition is the organizing principle. For short lists this is fine; for longer lists it produces a wall of undifferentiated criteria.
- STABILITY: LOW. Actively destroys structural information present in the raw data. Only appropriate if testing shows agents handle flat lists better than hierarchical ones.

### Cross-section dependencies

- **Section ordering:** If success criteria appear before instructions, the definition-evidence relationship serves as goal-setting. If after, it serves as verification. The rendering choice here interacts with the overall section ordering strategy.
- **Failure criteria:** The definition-evidence pattern is mirrored in failure criteria (failure_definition + failure_evidence). Rendering should be consistent across both sections to create a clear mental model: success = {definition + evidence}, failure = {definition + evidence}.

### Conditional branches

- **Single vs multiple criteria entries:** With one entry, the relationship is straightforward. With multiple entries, the rendering must clarify whether each entry is independent (different success dimensions) or cumulative (all must hold). The array-of-entries structure suggests independent dimensions that are all required.
- **Evidence count zero:** If a criteria entry has a definition but no evidence items (not seen in the data, but structurally possible), the definition must stand alone. The rendering should handle this gracefully without dangling "demonstrated by:" headers.

---

## STRUCTURAL: section_placement_and_timing

### What the agent needs to understand

When the agent encounters success criteria relative to other sections determines how it uses them. This is not about the data structure — it is about the rendered output ordering.

### Fragments

**placement_before_instructions** — Place success criteria before the execution instructions.
- Alternative A: Present success criteria immediately after role/context, before any instructions.
- Alternative B: Open with "Here is what success looks like:" before any "Here is what to do:"
- Alternative C: Lead with the success definition as a framing sentence for the entire task.
- PURPOSE: Prime the agent with a goal model before it encounters process details. The agent reads "what done looks like" then reads "how to get there."
- HYPOTHESIS: Before-instructions placement produces more goal-oriented behavior. The agent processes instructions through the lens of "does this step move me toward the success state?" This may also produce more adaptive behavior — if an instruction seems counterproductive to the success definition, the agent may intelligently deviate.
- STABILITY: MEDIUM. Depends on whether the success definition is comprehensible without instruction context. The builder's definition ("A complete TOML definition and include files have been written...") makes sense before instructions. The summarizer's definition ("Every input exchange has been contextually summarized...") also works before instructions. But more complex definitions might not.

**placement_after_instructions** — Place success criteria after the execution instructions.
- Alternative A: Present success criteria as a verification section after all instructions.
- Alternative B: Close with "Before finishing, verify:" after all process steps.
- Alternative C: Append as a quality gate: "Your work is complete when:"
- PURPOSE: Function as a quality gate after the agent understands what to do. The agent reads process, then reads how to verify its output.
- HYPOTHESIS: After-instructions placement produces more reliable verification behavior. The agent treats success criteria as a checklist to run through after completing the process. This is effective for mechanical evidence but may be too late for judgment-based evidence that should have influenced the process.
- STABILITY: HIGH. This is the most conventional placement and maps to how humans use acceptance criteria (define the task, then define done).

**placement_bookend** — Place the success definition before instructions and evidence items after.
- Alternative A: Open with the definition ("Your goal: {success_definition}"), give instructions, close with evidence ("Verify: {evidence items}").
- Alternative B: Frame the task with the definition, execute with instructions, gate with evidence.
- Alternative C: Definition as heading, instructions as body, evidence as footer checklist.
- PURPOSE: Split the two-level structure across the document: definition primes, evidence verifies. The agent gets goal orientation AND terminal verification.
- HYPOTHESIS: Bookend placement captures the benefits of both before and after placement. The definition orients; the evidence verifies. However, it separates structurally coupled data (definition and its evidence), which may weaken the claim-warrant relationship. The agent may not connect the terminal evidence items back to the opening definition.
- STABILITY: LOW. Splits a single data structure across the document, requiring the agent to mentally reconnect separated pieces. Fragile if the document is long.

### Cross-section dependencies

- **Instructions:** Placement is defined relative to instructions. The two sections must be rendered as a coherent sequence, not independently.
- **Failure criteria:** If success criteria are placed before instructions, failure criteria should likely be co-located (before or after success). If success criteria are after instructions, failure criteria should follow. Splitting success before and failure after (or vice versa) creates asymmetry.
- **Guardrails:** Guardrails are constraints on process. Success criteria are constraints on output. If guardrails are interleaved with instructions (constraining as you go), success criteria might be better placed after (verifying at the end). If guardrails are grouped separately, success criteria could be co-located.

### Conditional branches

- **Agent type:** Batch-processing agents (summarizer) may benefit more from after-instructions placement (clear verification gate). Creative agents (builder) may benefit more from before-instructions placement (goal orientation). The renderer may need to select placement based on agent characteristics.
- **Evidence type mix:** Agents with predominantly mechanical evidence benefit from after-instructions placement (checklist). Agents with predominantly judgment-based evidence benefit from before-instructions placement (quality orientation). Mixed agents present the hardest case.

---

## STRUCTURAL: multiple_criteria_entries

### What the agent needs to understand

The `success_criteria.criteria` field is an array, meaning multiple criteria entries can coexist. Each entry represents a distinct success dimension with its own definition and evidence. The agent must understand whether these are independent checks (all must pass) or alternative success paths (any suffices).

### Fragments

**multi_entry_conjunctive** — All criteria entries must be satisfied.
- Alternative A: "All of the following success dimensions must be achieved:"
- Alternative B: "Success requires meeting every one of these criteria:"
- Alternative C: Present each entry under a numbered heading with no "or" language.
- PURPOSE: Make explicit that multiple entries are conjunctive — partial success is not success.
- HYPOTHESIS: Conjunctive framing prevents the agent from satisfying one criterion and neglecting others. It forces attention across all dimensions. However, it may create anxiety about completeness that slows the agent down.
- STABILITY: HIGH. The data structure (array of required criteria) strongly implies conjunction. This is the natural reading.

**multi_entry_dimensional** — Each criteria entry represents a different quality dimension.
- Alternative A: "Your output is evaluated on these independent dimensions:\n\n**Dimension 1: {definition_1}**\n{evidence_1}\n\n**Dimension 2: {definition_2}**\n{evidence_2}"
- Alternative B: "Success has multiple facets. Each must be satisfied:\n..."
- Alternative C: "Think of these as independent lenses on your output — it must look right through all of them:\n..."
- PURPOSE: Clarify that each entry evaluates a different aspect, preventing the agent from treating the entries as redundant or overlapping.
- HYPOTHESIS: Dimensional framing produces more balanced attention across criteria. The agent understands that satisfying one dimension does not contribute to another — each must be independently addressed. This is especially important when dimensions are in tension (e.g., completeness vs minimality).
- STABILITY: MEDIUM. Only relevant when multiple entries exist. For single-entry agents (both current examples), this fragment is not rendered. Stability depends on whether future agents actually use multiple entries.

### Cross-section dependencies

- **Failure criteria:** If success criteria have multiple dimensions, failure criteria may be organized by the same dimensions or may cut across them. Consistent dimensionality across success and failure simplifies the agent's mental model.

### Conditional branches

- **Count = 1:** No multi-entry framing needed. The single entry's definition and evidence are the entire section. This is the current case for both agents.
- **Count > 1:** Multi-entry framing is required. The renderer must decide whether to use conjunctive, dimensional, or other framing based on the nature of the entries.
- **Count = 0:** Structurally possible but semantically degenerate. An agent with no success criteria has no defined success state. This should probably be a validation error, not a rendering case.

---

## STRUCTURAL: voice_and_agency

### What the agent needs to understand

The grammatical voice and agency attribution in success criteria affect how the agent relates to them. "You succeed when X" places agency with the agent. "The output satisfies X" places it with the output. "X is true" places it nowhere (impersonal). Each produces different behavioral effects.

### Fragments

**voice_agent_centric** — Address the agent directly as the actor responsible for success.
- Alternative A: "You have succeeded when: {definition}. You can verify this by checking: {evidence}"
- Alternative B: "You are done when you have ensured: {evidence items}"
- Alternative C: "Your success depends on: {evidence items}"
- PURPOSE: Make the agent feel personally responsible for meeting the criteria. Success is about the agent's performance, not just the output's properties.
- HYPOTHESIS: Agent-centric voice produces stronger ownership and self-monitoring. The agent treats success criteria as personal commitments rather than external specifications. This may increase effort on judgment-based evidence (the agent cares about quality) but could also increase anxiety and second-guessing.
- STABILITY: MEDIUM. Natural and motivating, but may over-personalize what should be objective output properties. "You have succeeded" implies a judgment of the agent, not just the output.

**voice_output_centric** — Describe properties of the output rather than actions of the agent.
- Alternative A: "The output satisfies the following: {evidence items}"
- Alternative B: "A correct output has these properties: {evidence items}"
- Alternative C: "The result, when complete, will exhibit: {evidence items}"
- PURPOSE: Shift focus from the agent's actions to the output's properties. This depersonalizes success — it is not about whether the agent "did well" but whether the output "is correct."
- HYPOTHESIS: Output-centric voice produces more objective self-evaluation. The agent evaluates its output as a separate artifact rather than evaluating itself. This may produce better error detection (easier to critique an object than oneself) and less defensive reasoning when errors are found.
- STABILITY: HIGH. The raw data already uses output-centric phrasing ("Output record count equals," "Every requirement maps to"). This fragment preserves the existing voice.

**voice_impersonal** — State criteria as impersonal facts without attributing agency.
- Alternative A: "{evidence_1}. {evidence_2}. {evidence_3}."
- Alternative B: "The following hold: {evidence items}"
- Alternative C: "True of a successful completion: {evidence items}"
- PURPOSE: Maximum neutrality. The criteria are facts about the world, not commands to the agent or properties of the output.
- HYPOTHESIS: Impersonal voice is the most compact but may feel disconnected from the agent's task. The agent may not feel the criteria are "its business" — they are just facts. This could reduce self-monitoring. However, for highly mechanical agents (batch processors), impersonal voice may reduce unnecessary cognitive overhead.
- STABILITY: MEDIUM. Works well for mechanical evidence but feels odd for judgment-based evidence. "Summaries reflecting accumulated conversational significance" as an impersonal fact is less actionable than as a quality dimension to attend to.

### Cross-section dependencies

- **Role section:** If the role section establishes strong agent identity ("You are a meticulous validator"), agent-centric voice in success criteria reinforces that identity. If the role is more functional ("This agent processes batches"), output-centric voice is more consistent.
- **Instructions:** The voice used in instructions should be consistent with the voice used in success criteria. If instructions say "you must" and success criteria say "the output satisfies," there is a voice mismatch that may confuse the agent's self-model.

### Conditional branches

- **Agent type:** Creative agents (builder) may respond better to agent-centric voice (ownership of a complex creative output). Batch agents (summarizer) may respond better to output-centric voice (objective properties of a mechanical transformation).
- **Evidence type:** Judgment-based evidence may benefit from agent-centric voice (personal responsibility for quality). Mechanical evidence may benefit from output-centric or impersonal voice (objective verification).

---

## SUMMARY OF KEY DESIGN TENSIONS

1. **Checklist vs compass.** Success criteria can function as terminal verification (checklist) or ongoing orientation (compass). The optimal choice depends on whether evidence is mechanical or judgment-based. A single rendering strategy may not serve both.

2. **Definition weight.** The success definition can be rendered as the primary content (with evidence as supporting detail) or as a header (with evidence as the primary content). The claim-warrant relationship suggests the evidence is the operational content, but the definition is what the agent should internalize as its goal model.

3. **Placement timing.** Before-instructions placement primes goal-oriented behavior. After-instructions placement enables verification behavior. The optimal choice depends on the agent's task type and the nature of its evidence items.

4. **Voice consistency.** The voice used in success criteria must be consistent with the voice used in other sections (role, instructions, guardrails). An agent-centric role section with output-centric success criteria creates a dissonant self-model.

5. **Heterogeneous evidence.** The mix of mechanical and judgment-based evidence within a single criteria entry is the hardest rendering problem. Uniform treatment (all as checklist, all as quality dimensions) under-serves one type. Split treatment (mechanical as checklist, judgment as orientation) requires semantic classification not present in the data.

6. **Success is not the inverse of failure.** This section must be rendered in a way that does not suggest "if success criteria are met, failure is impossible" or "if failure criteria are not triggered, success is achieved." The gap between success and failure — mediocre output that neither succeeds nor fails — is a real behavioral zone that the rendering must not accidentally close.
