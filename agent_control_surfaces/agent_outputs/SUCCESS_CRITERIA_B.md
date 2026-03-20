# ANALYSIS: `success_criteria` Section — Behavioral Design Surface

This analysis examines the `success_criteria` section of the agent prompt composition system from first principles, treating the raw data as the only invariant and designing the presentation layer from scratch.

---

## FOUNDATIONAL ANALYSIS: What Success Criteria Actually Do

Success criteria are not a checklist bolted onto the end of an agent prompt. They are a **cognitive frame** — a mental model of "done" that the agent internalizes before it begins work and carries throughout execution. The behavioral effect is not "the agent checks these at the end." The behavioral effect is: **the agent works differently because it knows what success looks like.**

Consider the difference between a carpenter told "build a table" versus a carpenter told "success means a table that is level, supports 200 pounds, and fits through a standard doorway." The second carpenter does not build a table and then check those things. The second carpenter **makes different decisions throughout construction** because the success image is already loaded.

This is the core insight: success criteria function as a **preloaded evaluation function**. The agent runs this function continuously against its work-in-progress, not just against finished output. The section's job is to install this evaluation function cleanly.

There are three possible modes of engagement:
1. **CHECKLIST mode** — agent works, then verifies. Risk: late discovery of structural failure.
2. **COMPASS mode** — agent consults criteria at decision points. Risk: over-consultation, paralysis.
3. **SELF-MODEL mode** — agent internalizes criteria as "what I produce." Risk: criteria become invisible, unchecked.

The optimal mode depends on the agent's task type. Batch-processing agents (summarizer) benefit from checklist mode because each unit of work is small and the criteria are mechanical. Creative-constructive agents (builder) benefit from self-model mode because the criteria are judgment-heavy and the work is monolithic. This is a key conditional branch.

---

## FIELD: `success_definition`

TYPE: string (single sentence or clause)
VALUES: "A complete TOML definition and include files have been written that fully specify the agent described in the requirements." / "Every input exchange has been contextually summarized and written as a validated output record."

### What the agent needs to understand

The `success_definition` is the **thesis statement of completion**. It answers: "In one sentence, what does it mean for this agent to have succeeded?" This is not a summary of the evidence items — it is a higher-order claim that the evidence items collectively substantiate. The definition operates at the level of *intent* ("fully specify the agent"), while evidence operates at the level of *proof* ("every requirement maps to a named field").

The definition serves two behavioral functions:
1. **Orientation anchor**: When the agent is deep in execution and loses the forest for the trees, the definition re-centers it. "Am I still working toward a complete TOML definition, or have I drifted into something else?"
2. **Completion signal**: The definition is what the agent evaluates to decide "I am done." Evidence items are what it evaluates to decide "I am done *correctly*."

The critical design question is how tightly to couple the definition to the evidence. If the definition is presented as a summary that the evidence unpacks, the agent treats evidence as "the real criteria" and the definition as decoration. If the definition is presented as a goal that evidence proves, the agent treats the definition as primary and evidence as verification — which is the correct hierarchy.

### Fragments

**success_definition_framing**

- Alternative A (Goal Declaration): "Your goal is achieved when: {definition}"
  This frames the definition as an objective to reach. The agent orients toward it. Clean, directional, but slightly distant — "your goal" implies the definition is external to the agent.

- Alternative B (Completion Identity): "You have succeeded when {definition}"
  This frames success as a state the agent enters. "You have succeeded" makes the agent the subject of success, not the work. This promotes self-model mode — the agent identifies with successful completion.

- Alternative C (Output Specification): "The completed output is: {definition}"
  This frames the definition as a description of the artifact, not the agent. The agent is invisible; only the work matters. This promotes checklist mode — the agent builds toward a described artifact and checks whether it matches.

- Alternative D (Assertion of Done): "{definition} — this is what done looks like."
  No framing, just the definition followed by a grounding clause. The most direct. Relies on the definition's own language to carry the weight. The tag "this is what done looks like" installs the mental image without prescribing how to use it.

- Alternative E (Conditional Gate): "This task is complete if and only if {definition}"
  Formal, precise, gate-like. Signals that the definition is a hard boundary — nothing less counts, but nothing more is required. Risk: "if and only if" may cause the agent to treat the definition as sufficient and ignore evidence items.

- PURPOSE: Install a high-level image of "done" that the agent carries throughout execution, not just at the end. The framing determines whether the agent relates to the definition as a goal (reaching toward), an identity (being), or a specification (matching against).
- HYPOTHESIS: Alternative B (Completion Identity) produces the strongest behavioral internalization for creative/constructive agents because it makes success a property of the agent, not the artifact. Alternative C (Output Specification) produces the most reliable behavior for batch agents because it externalizes the check. Alternative D (Assertion of Done) may be the best general-purpose option because it avoids prescribing the agent's relationship to the definition.
- STABILITY: HIGH. Every agent needs exactly one success definition presented in a consistent frame. The framing choice may be stable across all agents even if the content varies wildly.

---

## FIELD: `success_evidence`

TYPE: array of strings (each a checkable condition or observable property)
VALUES: 6 items (builder) / 5 items (summarizer)

### What the agent needs to understand

Evidence items are the **decomposition of success into observable conditions**. They answer: "How would I know the definition has been met? What specific things would I check?" Each evidence item is a claim that, if true, contributes to proving the definition.

The evidence array has a critical dual nature that the presentation must handle:

**Mechanical evidence** can be verified by inspection or counting:
- "Output record count equals input record count."
- "Every exchange number in the input appears exactly once in the output."
- "All conditional field rules pass validation."

**Judgment evidence** requires qualitative assessment:
- "Examples are grounded in actual data shapes from the preparation package."
- "Thin-content-rich-context exchanges have summaries reflecting accumulated conversational significance."
- "The definition could be rendered through any template and produce a functional agent."

These two types should arguably be presented differently, or at minimum the agent should understand that they require different verification strategies. Mechanical evidence can be checked procedurally. Judgment evidence requires the agent to reason about quality, which is a fundamentally different cognitive operation.

Another observation: evidence items are **not ordered by importance**. In the builder, the first item ("every requirement maps to a named field") is arguably the most fundamental, while the last ("could be rendered through any template") is the most aspirational. In the summarizer, the first two are mechanical checks and the last three are quality assertions. The ordering appears to be: structural completeness → correctness → quality. This may be an implicit priority that the presentation should make explicit, or it may be accidental.

### Fragments

**evidence_list_framing**

- Alternative A (Verification Checklist): "Verify each of the following before declaring completion:\n- {evidence_1}\n- {evidence_2}\n..."
  Explicit checklist framing. The agent is told to verify each item, implying a sequential end-of-work check. Clear, procedural, but promotes late evaluation — the agent may defer checking until it thinks it is done.

- Alternative B (Properties of Success): "A successful output has these properties:\n- {evidence_1}\n- {evidence_2}\n..."
  Describes evidence as inherent properties of the output, not actions the agent takes. This promotes compass mode — the agent knows what properties to maintain throughout, not just check at the end. The output either has these properties or it does not.

- Alternative C (Proof Points): "Success is demonstrated by:\n- {evidence_1}\n- {evidence_2}\n..."
  Frames evidence as demonstrations — things that prove success to an observer. This externalizes evaluation: the agent imagines someone else checking its work. This can promote thoroughness (the agent anticipates scrutiny) but may also promote surface compliance (the agent optimizes for appearance of success rather than substance).

- Alternative D (Invariants): "These conditions must hold in the final output:\n- {evidence_1}\n- {evidence_2}\n..."
  Frames evidence as invariants — conditions that must be true, period. Strongest constraint language. "Must hold" implies no exceptions, no judgment calls. This works well for mechanical evidence but may feel coercive for judgment evidence.

- Alternative E (Quality Signals): "You know you have succeeded when all of the following are true:\n- {evidence_1}\n- {evidence_2}\n..."
  Frames evidence as the agent's own recognition of success. "You know" makes the agent the evaluator. This promotes self-model mode most strongly — the agent's internal quality signal is calibrated by these items.

- PURPOSE: Decompose the success definition into observable, checkable conditions that the agent can evaluate against its own output. The framing determines whether the agent treats evidence as external checks (checklist), inherent properties (compass), or internalized quality signals (self-model).
- HYPOTHESIS: Alternative B (Properties of Success) is the best general-purpose framing because it describes the output without prescribing when or how the agent checks. It is equally compatible with all three modes. Alternative A (Verification Checklist) is strongest for batch agents where mechanical checking is appropriate. Alternative E (Quality Signals) is strongest for creative agents where internalized judgment matters.
- STABILITY: HIGH for framing choice (one style per agent). MEDIUM for whether the same framing works across all agent types — the mechanical/judgment split may require conditional presentation.

---

## STRUCTURAL: definition-to-evidence relationship

### What the agent needs to understand

The relationship between `success_definition` and `success_evidence` is hierarchical but the nature of that hierarchy is ambiguous. Two interpretations:

1. **Definition is the claim; evidence is the proof.** The agent's job is to make the definition true. Evidence items are how it (and others) verify the definition is true. This is a logical relationship: evidence → definition.

2. **Definition is the summary; evidence is the detail.** The definition is a compressed version of the evidence items. It exists for convenience. The evidence items are the real criteria. This is a compositional relationship: evidence ∈ definition.

Interpretation 1 is more powerful because it preserves the definition as a first-class behavioral anchor. Under interpretation 2, the definition becomes redundant — you could delete it and lose nothing. Under interpretation 1, deleting the definition would remove the orienting frame that gives evidence items their coherence.

The presentation must make this hierarchy explicit. If it does not, agents will default to interpretation 2 (treating evidence as primary) because evidence items are more concrete and actionable.

### Fragments

**hierarchy_connector**

- Alternative A (Proof Framing): "{definition}\n\nThis is proven by:\n{evidence_list}"
  Explicit proof relationship. The definition stands as the primary claim. Evidence items support it. The word "proven" signals logical subordination of evidence to definition.

- Alternative B (Decomposition Framing): "{definition}\n\nSpecifically:\n{evidence_list}"
  The definition is unpacked into specifics. "Specifically" signals that evidence items are the definition's detailed form. This is interpretation 2 — the definition is a summary.

- Alternative C (Dual Presentation): "{definition}\n\nYou can confirm this by checking:\n{evidence_list}"
  The definition is primary. Evidence items are a confirmation mechanism — a way to check, not the definition itself. This preserves the definition's primacy while giving evidence a clear role.

- Alternative D (No Explicit Connector): "{definition}\n\n{evidence_list}"
  Let the agent infer the relationship. The definition appears first, evidence follows. Positional hierarchy implies logical hierarchy. Risk: the agent may not infer the correct relationship, especially if evidence items are more concrete and feel more "real."

- Alternative E (Goal-then-Criteria): "{definition}\n\nMeeting this standard means:\n{evidence_list}"
  The definition is a "standard" — a level to reach. Evidence items define what reaching that level looks like. "Meeting this standard" explicitly subordinates evidence to definition while giving evidence the role of operationalizing an abstract goal.

- PURPOSE: Establish the correct hierarchical relationship between definition (orienting claim) and evidence (proof/verification conditions) so the agent treats the definition as the primary behavioral anchor and evidence as its operationalization.
- HYPOTHESIS: Alternative A (Proof Framing) most clearly installs the correct hierarchy but may feel overly formal. Alternative E (Goal-then-Criteria) is the most natural-sounding while still preserving hierarchy. Alternative B (Decomposition) should be avoided as it demotes the definition to a summary. Alternative D (No Connector) is risky — it relies on the agent inferring hierarchy from position, which is not reliable.
- STABILITY: HIGH. This is a structural design choice that should be consistent across all agents. The connector pattern chosen here becomes part of the rendering template.

---

## STRUCTURAL: mechanical vs. judgment evidence

### What the agent needs to understand

The evidence array contains two fundamentally different types of claims:

**Mechanical evidence** — verifiable by procedure:
- "Output record count equals input record count." → Count and compare.
- "Every exchange number in the input appears exactly once in the output." → Check set membership.
- "All conditional field rules pass validation." → Run validation.

**Judgment evidence** — verifiable by reasoning:
- "Examples are grounded in actual data shapes from the preparation package." → Requires understanding what "grounded" means and assessing whether examples match data shapes.
- "The definition could be rendered through any template and produce a functional agent." → Requires imagining counterfactual renderings and assessing functional viability.
- "Thin-content-rich-context exchanges have summaries reflecting accumulated conversational significance." → Requires understanding conversational dynamics and assessing summary quality.

This distinction matters because the agent needs **different cognitive strategies** for each type. Mechanical evidence calls for verification procedures. Judgment evidence calls for quality reasoning. If the agent treats all evidence as equally mechanical, it will under-evaluate judgment items. If it treats all evidence as equally subjective, it will over-complicate mechanical checks.

### Fragments

**evidence_type_handling**

- Alternative A (Undifferentiated List): Present all evidence items in a single list with no type distinction. Let the agent figure out which require mechanical checking and which require judgment.
  This is the simplest approach and avoids introducing a distinction that may not generalize. Risk: the agent's verification depth may be uneven — thorough on mechanical items (they are concrete) and shallow on judgment items (they are fuzzy).

- Alternative B (Explicit Type Markers): Mark each evidence item as [VERIFY] or [ASSESS] (or similar). "[VERIFY] Output record count equals input record count. [ASSESS] Examples are grounded in actual data shapes."
  This makes the distinction explicit. The agent knows which items need procedural checking and which need quality reasoning. Risk: the markers add visual noise and the categorization may not always be clean — some items are borderline.

- Alternative C (Two Sub-lists): Split evidence into "Verifiable conditions" and "Quality standards" (or similar headings). Group mechanical items under one heading and judgment items under another.
  This makes the distinction structural. The agent encounters two different kinds of evidence and knows to approach them differently. Risk: artificial separation — some items combine mechanical and judgment aspects.

- Alternative D (Graduated Language): Use different linguistic framing within the list. Mechanical items use "must" language ("record count must equal"), judgment items use "should reflect" or "should demonstrate" language. The agent infers verification strategy from the verb.
  This is the subtlest approach. It relies on the agent's language sensitivity to drive different evaluation strategies. Risk: the distinction may be too subtle for reliable behavioral differentiation.

- Alternative E (Verification Guidance Suffix): Append a brief note after the evidence list: "Some conditions above are mechanically verifiable; others require your judgment. Apply appropriate rigor to each." This acknowledges the distinction without marking individual items.
  This is a middle ground — it raises the agent's awareness of the distinction without prescribing how to handle each item. Risk: vague guidance may not change behavior.

- PURPOSE: Ensure the agent applies appropriate verification depth to both mechanical and judgment evidence, rather than defaulting to the same evaluation strategy for all items.
- HYPOTHESIS: Alternative A (Undifferentiated List) is sufficient for agents whose evidence is predominantly one type. Alternative D (Graduated Language) is the most elegant for mixed-type evidence because it encodes verification expectations in the language itself, which is how agents process instructions. Alternative B (Explicit Type Markers) is the most reliable but also the most visually intrusive.
- STABILITY: LOW-MEDIUM. This design choice depends heavily on the evidence mix of each specific agent. Some agents may have all-mechanical evidence (undifferentiated list is fine). Others may have a complex mix (graduated language or explicit markers needed). This may need to be a conditional branch based on evidence composition analysis.

---

## STRUCTURAL: criteria array cardinality (single vs. multiple entries)

### What the agent needs to understand

Both example agents have exactly one entry in `success_criteria.criteria`. But the data model is an array, meaning multiple entries are structurally possible. This raises the question: when would an agent have multiple success criteria entries, and how should they relate to each other?

Possible interpretations:
1. **Multiple independent success dimensions.** An agent that both transforms data AND validates schema might have one criteria entry for transformation success and another for validation success.
2. **Multiple stakeholder perspectives.** One criteria entry for "technically correct" and another for "user-acceptable."
3. **Phased success.** One criteria entry for "initial pass complete" and another for "refinement pass complete."

The current data does not demonstrate multiple entries, so this is speculative design territory. But the presentation must handle the possibility.

### Fragments

**multi_criteria_relationship**

- Alternative A (Independent Blocks): Present each criteria entry as a self-contained block with its own definition and evidence. No explicit relationship between blocks. The agent must satisfy all blocks independently.
  This is the simplest approach and works well if criteria entries are truly independent dimensions.

- Alternative B (Numbered Dimensions): "Success has {N} dimensions:\n1. {definition_1}\n...\n2. {definition_2}\n..." Each dimension is labeled and numbered. The agent understands that success requires satisfying all dimensions.
  This makes the multi-dimensional nature explicit. The numbering creates an implicit priority (dimension 1 first), which may or may not be desired.

- Alternative C (Composite Definition): Merge multiple definitions into a single composite statement, then present all evidence items grouped by original entry. "Success means both {definition_1} AND {definition_2}."
  This preserves a single definition anchor while acknowledging that it has components. Risk: the composite may be awkward if the definitions are structurally different.

- Alternative D (Single Entry Assumed, Multi as Exception): Design for the common case (single entry) and handle multiple entries as a special case with additional framing. "Your primary success criterion is: {definition_1}. Additionally, you must also satisfy: {definition_2}."
  This prioritizes the first entry and treats additional entries as supplementary. Risk: false priority ordering if entries are equally important.

- PURPOSE: Handle the array cardinality of criteria entries so that single-entry agents (the common case) get clean presentation while multi-entry agents (the rare case) get correct presentation.
- HYPOTHESIS: Alternative A (Independent Blocks) is the safest general-purpose approach because it makes no assumptions about relationships between entries. Alternative B (Numbered Dimensions) is better if multi-entry agents become common and the entries represent genuinely different success dimensions. The rendering system should optimize for the single-entry case (no special framing needed) and add structure only when multiple entries are present.
- STABILITY: LOW. This is speculative — the data shows only single-entry cases. The design should be kept simple and revisited when real multi-entry agents exist. Over-designing for a case that may not occur is wasteful.

---

## STRUCTURAL: temporal engagement pattern

### What the agent needs to understand

When in the execution lifecycle does the agent engage with success criteria? This is not a data field — it is a behavioral question that the presentation implicitly or explicitly answers.

Three models:
1. **Pre-flight loading**: The agent reads success criteria before starting work, internalizes them, and carries the image of success throughout. Criteria are not re-consulted unless the agent feels lost.
2. **Checkpoint verification**: The agent reads success criteria at defined checkpoints (after each batch item, after each phase, before finalizing). Criteria serve as a periodic alignment check.
3. **Post-completion verification**: The agent reads success criteria only at the end, as a final gate before declaring done.

The optimal model depends on task structure:
- **Batch tasks** (summarizer): Checkpoint verification after each item or batch is natural. Mechanical evidence items lend themselves to periodic checking.
- **Monolithic tasks** (builder): Pre-flight loading is more appropriate. The agent builds a complex artifact and checking partway through may not be meaningful — you cannot verify "the definition could be rendered through any template" until the definition is complete.

### Fragments

**temporal_engagement_framing**

- Alternative A (Pre-flight Emphasis): Place success criteria early in the prompt (before execution instructions) with framing like "Before you begin, understand what success looks like:" This positions criteria as orientation, not verification.

- Alternative B (Post-execution Emphasis): Place success criteria after execution instructions with framing like "Before declaring completion, verify:" This positions criteria as a final gate.

- Alternative C (Dual Placement): Present the definition at the start (orientation) and the evidence list at the end (verification). Split the section across two prompt locations. This gives the agent both the compass (definition up front) and the checklist (evidence at the end).

- Alternative D (Integrated Reminders): Weave success criteria references into execution instructions at relevant points. "When writing examples, remember: examples must be grounded in actual data shapes." This distributes criteria awareness throughout execution.

- Alternative E (Explicit Temporal Instruction): Include a meta-instruction about when to consult criteria. "Review these criteria before starting, check them periodically during execution, and verify all of them before completing." This explicitly installs the engagement pattern rather than relying on positional cues.

- PURPOSE: Determine when in the execution lifecycle the agent engages with success criteria, and how the prompt presentation drives that timing.
- HYPOTHESIS: Alternative C (Dual Placement) is the most powerful because it serves both functions — orientation and verification — without requiring the agent to scroll back or remember. However, it requires the rendering system to split a single data source across two prompt locations, which increases template complexity. Alternative A (Pre-flight Emphasis) is best for creative/constructive agents. Alternative B (Post-execution Emphasis) is best for batch agents. The choice may need to be conditional on task type.
- STABILITY: MEDIUM. Placement is a rendering decision that affects behavior significantly. The choice should be principled but may need to vary by agent archetype. Cross-section dependency: this interacts with prompt ordering decisions made for ALL sections, not just success criteria.

---

## STRUCTURAL: success_criteria relationship to failure_criteria

### What the agent needs to understand

Success criteria and failure criteria are **not inverses**. This is critical.

Consider the summarizer:
- Success: "Every summary is a single sentence capturing contextual significance."
- A hypothetical failure: "The agent hallucinated data not present in the input."

The failure is not "summaries are not single sentences" (the inverse of success). It is a wholly different kind of problem — a safety violation, not a quality shortfall. An agent can produce multi-sentence summaries (failing success criteria) without hallucinating (not triggering failure criteria). The agent occupies a middle zone: not successful, not failed, just mediocre.

The presentation must not allow the agent to conflate "not failed" with "succeeded." Nor should it allow "not succeeded" to feel like "failed." These are separate evaluation dimensions:
- **Success criteria**: What does excellent output look like?
- **Failure criteria**: What does broken/dangerous output look like?
- **The gap between**: Mediocre output that triggers neither.

### Fragments

**success_failure_relationship**

- Alternative A (No Explicit Relationship): Present success criteria and failure criteria as completely separate sections with no cross-references. Let the agent understand each independently.
  This is clean and avoids confusion, but the agent may not understand that satisfying all success criteria does not automatically mean it has avoided all failure criteria (and vice versa).

- Alternative B (Explicit Separation Statement): Include a note in one or both sections: "Success criteria define what quality looks like. Failure criteria define what broken looks like. These are independent evaluations — avoiding failure does not guarantee success."
  This makes the independence explicit. The agent understands the three-state model (succeeded / mediocre / failed).

- Alternative C (Unified Evaluation Frame): Present both in a single "Evaluation" section with clear sub-headers. "Your output is evaluated on two independent axes: success (does it meet quality standards?) and failure (does it contain critical defects?)."
  This gives the agent the full evaluation picture in one place. Risk: lumping them together may reduce the independent weight of each.

- Alternative D (Priority Ordering): "First: ensure your output triggers no failure criteria. Then: ensure it satisfies all success criteria." This establishes a clear priority — avoid failure first, then achieve success.
  This is practical and actionable. Risk: the agent may treat success criteria as secondary or optional once failure criteria are cleared.

- PURPOSE: Ensure the agent understands that success and failure are independent evaluation dimensions, and that mediocre output (neither succeeded nor failed) is a real possibility that should be avoided.
- HYPOTHESIS: Alternative B (Explicit Separation Statement) is the clearest and most reliable. It makes the independence explicit without restructuring the prompt. Alternative D (Priority Ordering) is pragmatically useful but risks demoting success criteria. Alternative A (No Explicit Relationship) is acceptable if the sections are well-separated in the prompt and the agent is unlikely to conflate them.
- STABILITY: HIGH. The independence of success and failure criteria is a fundamental design principle that should hold across all agents. The presentation of this independence should be consistent.

---

## CROSS-SECTION DEPENDENCIES

### success_criteria → execution_instructions
Evidence items often reference things that execution instructions describe how to do. "All conditional field rules pass validation" (success evidence) depends on the agent knowing what conditional field rules are and how to validate them (execution instructions). The success criteria section must not re-explain execution — it must assume the agent has already internalized execution instructions and simply state what the successful output of that execution looks like.

### success_criteria → guardrails
Some evidence items overlap with guardrail constraints. "No instruction step contains operational content" (success evidence) could also be a guardrail. The distinction: guardrails are prohibitions (do NOT do X), while success evidence items are assertions about the output (the output DOES NOT contain X). Same condition, different framing. The rendering system should be aware of this overlap and avoid redundancy, or deliberately use redundancy for reinforcement.

### success_criteria → examples
Examples demonstrate what success looks like concretely. If success criteria say "every summary is a single sentence capturing contextual significance," examples should show what such a sentence looks like. The criteria section provides the abstract standard; the examples section provides the concrete instances. They are complementary and should not contradict.

### success_criteria → failure_criteria
As analyzed above, these are independent evaluation dimensions. The rendering system must present them as separate sections. Cross-reference may be useful but is not required.

### success_criteria → role/identity
The agent's relationship to success criteria is shaped by its role. A "builder" may internalize success criteria as craftsmanship standards. A "summarizer" may internalize them as processing requirements. The role section's framing affects how deeply the agent identifies with success criteria versus treating them as external checks.

---

## CONDITIONAL BRANCHES

### Branch: task_type (creative-constructive vs. batch-processing)

**When creative-constructive** (builder):
- Success criteria are best presented as internalized quality standards (self-model mode)
- Definition should use identity framing ("you have succeeded when")
- Evidence items lean heavily on judgment — graduated language is appropriate
- Temporal engagement: pre-flight loading with definition as compass
- Evidence ordering likely matters and should flow from structural to aspirational

**When batch-processing** (summarizer):
- Success criteria are best presented as verification checklists
- Definition should use output specification framing ("the completed output is")
- Evidence items lean heavily on mechanical — undifferentiated list is fine
- Temporal engagement: checkpoint verification after each batch segment
- Evidence ordering can be count-first, quality-second

### Branch: evidence_composition (all-mechanical vs. all-judgment vs. mixed)

**When all-mechanical**: Undifferentiated list with verification language. No need for type markers.
**When all-judgment**: Undifferentiated list with quality-standard language. Explicit note that the agent must reason about each item rather than mechanically check.
**When mixed**: Consider graduated language (Alternative D from evidence_type_handling) or explicit type markers (Alternative B) depending on the ratio and clarity of the distinction.

### Branch: criteria_count (single vs. multiple)

**When single entry**: No special framing needed. Present definition and evidence directly.
**When multiple entries**: Add dimensional framing (Alternative B from multi_criteria_relationship) or independent blocks (Alternative A). Do not attempt to merge definitions.

### Branch: evidence_count (few vs. many)

**When few (3-4)**: Present as a tight list. Each item carries significant weight.
**When many (6+)**: Consider whether items can be grouped by theme (structural, correctness, quality). Ungrouped long lists may cause later items to receive less attention from the agent — a known primacy/recency effect in instruction following.

---

## SUMMARY OF KEY DESIGN DECISIONS

1. **Definition is primary; evidence is subordinate.** The rendering must preserve this hierarchy, not flatten it. Alternative E (Goal-then-Criteria connector) recommended.

2. **Framing should match task type.** Creative agents get self-model framing. Batch agents get checklist framing. This is a conditional branch, not a one-size-fits-all decision.

3. **Mechanical vs. judgment evidence is a real distinction** that the rendering should acknowledge, at minimum through graduated verb language (must/equals for mechanical, should reflect/captures for judgment).

4. **Success and failure are independent.** This must be explicit somewhere in the prompt, either as a separation statement or through clear structural separation.

5. **Temporal engagement should be principled.** The definition belongs early (compass). Evidence belongs late (verification). Dual placement (Alternative C) is the most powerful but most complex option.

6. **Single-criteria is the norm; multi-criteria is the edge case.** Design for single, accommodate multiple. Do not over-engineer for a case the data does not yet demonstrate.
