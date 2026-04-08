# SUCCESS_CRITERIA -- Control Surface Synthesis

## Section Purpose

Success criteria function as a **preloaded evaluation function**, not a post-hoc checklist. When an agent internalizes success criteria, it constructs an image of "done" that shapes decision-making throughout execution -- before, during, and after the work. The section's job is to install this evaluation function cleanly. Both analyses converge strongly on this point: the behavioral effect is not "the agent checks these at the end" but "the agent works differently because it knows what success looks like."

The section achieves three things: **goal formation** (what does done look like?), **quality calibration** (what dimensions matter?), and **completion detection** (when to stop). These are distinct from instructions, which tell the agent what to do. Success criteria tell the agent what the result should be -- the difference between knowing the verb and knowing the target state.

The key tension is **mode of engagement**. Both analyses identify three modes -- checklist (verify at end), compass (consult at decision points), and self-model (internalize as identity) -- and agree the optimal mode depends on task type. Batch-processing agents benefit from checklist mode; creative-constructive agents benefit from self-model mode. This is the primary conditional branch governing the entire section's rendering.

## Fragment Catalog

### success_definition_framing

- CONVERGED: The definition is the highest-level success predicate -- a single statement that, if true, means the task succeeded. It operates at a different granularity than evidence. It serves as both an orientation anchor (re-centering during execution) and a completion signal (deciding "I am done"). The raw data uses declarative-resultative phrasing ("have been written," "has been summarized"), which should be preserved.
- DIVERGED: A offered three frames (declarative, imperative, conditional) as separate fragments. B offered five alternatives along a different axis (goal declaration, completion identity, output specification, assertion, conditional gate). B's "completion identity" frame ("You have succeeded when...") has no equivalent in A. A's analysis of imperative framing as high-risk (requires rewriting author text) is an insight B did not surface.
- ALTERNATIVES:
  - A: **Declarative assertion** -- "{definition} -- this is what done looks like." Direct, no rewriting, relies on the definition's own language. Behavioral rationale: installs the mental image without prescribing the agent's relationship to it. Most general-purpose.
  - B: **Conditional gate** -- "This task is complete if and only if: {definition}" Strongest completion-checking behavior, but may cause premature evaluation or lead the agent to ignore evidence items. Best for agents where the definition is self-sufficient.
  - C: **Completion identity** -- "You have succeeded when {definition}" Makes success a property of the agent, not the artifact. Strongest for creative agents where ownership drives quality.
- HYPOTHESIS: Declarative assertion (A) is the safest default. Completion identity (C) is strongest for creative-constructive agents. Conditional gate (B) is strongest for batch agents needing hard stop signals. Imperative framing should be avoided -- it requires rewriting author-supplied text and reduces self-monitoring.
- STABILITY: structural
- CONDITIONAL: Agent task type. Creative-constructive agents may benefit from completion identity framing; batch-processing agents from conditional gate or declarative assertion.

### evidence_list_framing

- CONVERGED: Evidence items are the operational teeth of success criteria -- independently evaluable assertions that collectively prove the definition holds. They decompose success into observable conditions. Both analyses agree the framing determines whether the agent treats evidence as terminal verification, ongoing properties, or internalized quality signals.
- DIVERGED: A identified a "mixed strategy" fragment (split mechanical/judgment into sub-lists) that B did not propose as a separate fragment. B proposed "Quality Signals" framing ("You know you have succeeded when...") that A did not surface. B noted evidence ordering (structural completeness -> correctness -> quality) may be an implicit priority the presentation should make explicit; A did not address ordering.
- ALTERNATIVES:
  - A: **Properties of success** -- "A successful output has these properties: ..." Describes evidence as inherent output properties. Compatible with all engagement modes. Best general-purpose option.
  - B: **Verification checklist** -- "Verify each of the following before declaring completion: ..." Explicit end-of-work gate. Strongest for batch agents with mechanical evidence. Risk: concentrates quality attention at the end, too late for judgment evidence.
  - C: **Quality signals** -- "You know you have succeeded when all of the following are true: ..." Makes the agent the evaluator, calibrating internal quality signal. Strongest for creative agents with judgment evidence.
- HYPOTHESIS: Properties of success (A) is the best default because it does not prescribe when or how the agent checks. Verification checklist (B) for predominantly mechanical evidence. Quality signals (C) for predominantly judgment evidence.
- STABILITY: experimental
- CONDITIONAL: Evidence composition (all-mechanical vs. all-judgment vs. mixed) and agent task type.

### hierarchy_connector

- CONVERGED: The definition-evidence relationship is **claim-and-warrant**, not summary-and-detail. The definition is a higher-order claim that evidence items substantiate. If presented as summary-detail, the agent treats evidence as "the real criteria" and the definition as decoration. If presented as claim-warrant, the agent treats the definition as the organizing principle. Both analyses strongly agree the hierarchy must be preserved, not flattened.
- DIVERGED: A proposed three alternatives (claim-warrant, goal-criteria, flat). B proposed five (proof, decomposition, dual-presentation, no-connector, goal-then-criteria). Both agree flat/no-connector should be avoided. A explicitly warned against the goal-criteria pattern for judgment evidence (acceptance criteria feel binary). B warned against decomposition framing as it demotes the definition.
- ALTERNATIVES:
  - A: **Goal-then-criteria** -- "{definition}\nMeeting this standard means:\n{evidence}" Natural-sounding, preserves hierarchy, gives evidence the role of operationalizing an abstract goal.
  - B: **Proof framing** -- "{definition}\nThis is proven by:\n{evidence}" Strongest hierarchy signal. Clearest about why evidence items exist. May feel overly formal.
  - C: **Dual presentation** -- "{definition}\nYou can confirm this by checking:\n{evidence}" Preserves definition primacy while giving evidence a clear verification role.
- HYPOTHESIS: Goal-then-criteria (A) is the best balance of clarity and naturalness. Proof framing (B) is available when stronger hierarchy signaling is needed. Decomposition framing ("Specifically:") and flat presentation should be avoided as they demote or destroy the hierarchy.
- STABILITY: structural
- CONDITIONAL: None. This relationship is inherent in the data structure and should be consistent across all agents.

### evidence_type_handling

- CONVERGED: Evidence arrays contain two fundamentally different types -- **mechanical** (verifiable by procedure: counting, set membership, running validation) and **judgment** (verifiable by reasoning: assessing quality, imagining counterfactuals). Both analyses agree these require different cognitive strategies from the agent and that uniform treatment under-serves one type.
- DIVERGED: A proposed a mixed-strategy fragment (split into sub-lists by type) and flagged it as LOW stability due to requiring semantic classification not in the raw data. B proposed graduated verb language as the most elegant solution (must/equals for mechanical, should reflect/captures for judgment) -- a subtler approach A did not consider. B also proposed explicit type markers ([VERIFY]/[ASSESS]) and a verification guidance suffix.
- ALTERNATIVES:
  - A: **Graduated language** -- Encode verification expectations in verb choice within each item. "Record count must equal..." vs. "Summaries should reflect..." Subtle, elegant, no structural overhead. Risk: may be too subtle for reliable behavioral differentiation.
  - B: **Undifferentiated list** -- Single flat list, no type distinction. Simplest. Sufficient when evidence is predominantly one type. Risk: uneven verification depth on mixed lists.
  - C: **Verification guidance suffix** -- Single list followed by: "Some conditions above are mechanically verifiable; others require your judgment. Apply appropriate rigor to each." Middle ground -- raises awareness without marking individual items.
- HYPOTHESIS: Graduated language (A) is the most promising for mixed evidence because it operates at the linguistic level agents naturally process. Undifferentiated list (B) is sufficient for agents with homogeneous evidence. The mixed-strategy sub-list approach is too heavy and requires classification not present in the data.
- STABILITY: experimental
- CONDITIONAL: Evidence composition. All-mechanical -> undifferentiated with verification language. All-judgment -> undifferentiated with quality language. Mixed -> graduated language or verification guidance suffix.

### temporal_engagement_framing

- CONVERGED: When the agent encounters success criteria relative to instructions determines how it uses them. Before-instructions = goal priming. After-instructions = verification gate. Both analyses identify dual placement (definition before, evidence after) as the most powerful option but the most complex. Both agree the optimal placement depends on task type.
- DIVERGED: B proposed "integrated reminders" (weave criteria references into instruction steps) and "explicit temporal instruction" (meta-instruction about when to consult) -- neither appeared in A. A analyzed the bookend approach's weakness more precisely: it splits structurally coupled data, weakening the claim-warrant link.
- ALTERNATIVES:
  - A: **Post-execution placement** -- Success criteria as verification section after instructions. Most conventional, highest stability. Best for batch agents.
  - B: **Pre-execution placement** -- Success criteria before instructions, priming goal-oriented behavior. Best for creative agents. Requires definitions that are comprehensible without instruction context.
  - C: **Bookend/dual placement** -- Definition before instructions (compass), evidence after (checklist). Most powerful but fragments the claim-warrant relationship and increases template complexity.
- HYPOTHESIS: Post-execution (A) is the safest default. Pre-execution (B) is warranted for creative-constructive agents with clear, standalone definitions. Bookend (C) should be reserved for agents where testing shows the benefit outweighs the structural fragmentation.
- STABILITY: formatting
- CONDITIONAL: Agent task type. Batch -> post-execution. Creative-constructive -> pre-execution or bookend.

### voice_and_agency

- CONVERGED: Grammatical voice affects how the agent relates to criteria. Agent-centric ("you succeed when") promotes ownership. Output-centric ("the output satisfies") promotes objective evaluation. Both agree the raw data uses output-centric phrasing and that voice must be consistent with the role section.
- DIVERGED: A treated this as a full fragment with three alternatives (agent-centric, output-centric, impersonal). B embedded agency considerations within other fragments (definition framing, evidence framing) rather than treating voice as a standalone concern. B's approach may be more practical -- voice is a property of how other fragments are rendered, not a separate fragment.
- ALTERNATIVES:
  - A: **Output-centric** -- "The output satisfies..." / "A correct output has these properties..." Matches raw data phrasing. Promotes objective self-evaluation.
  - B: **Agent-centric** -- "You succeed when..." / "Your success depends on..." Promotes ownership. Best paired with strong role identity.
- HYPOTHESIS: Output-centric is the better default because it matches the raw data voice and promotes cleaner error detection (easier to critique an artifact than oneself). Agent-centric is warranted when the role section establishes a strong identity the success criteria should reinforce.
- STABILITY: formatting
- CONDITIONAL: Role section framing. Strong agent identity -> agent-centric voice. Functional/process role -> output-centric voice.

### multi_criteria_relationship

- CONVERGED: The criteria field is an array, but both current agents have exactly one entry. Both analyses agree: design for single-entry (the common case), accommodate multi-entry without over-engineering. Multiple entries are conjunctive (all must hold), not disjunctive.
- DIVERGED: A explored dimensional framing in more depth (independent quality dimensions, lenses metaphor). B proposed a pragmatic hierarchy: single entry assumed, multi as exception with "additionally" framing. B explicitly recommended against over-designing for an undemonstrated case.
- ALTERNATIVES:
  - A: **Independent blocks** -- Each entry is self-contained with its own definition and evidence. No explicit relationship. Simplest, safest.
  - B: **Numbered dimensions** -- "Success has N dimensions: ..." Makes multi-dimensional nature explicit. Adds implicit priority through numbering.
- HYPOTHESIS: Independent blocks (A) for now. Revisit when real multi-entry agents exist. Single-entry requires no special framing -- the definition and evidence are the section.
- STABILITY: structural
- CONDITIONAL: Criteria count. Count = 1 -> no multi-entry framing. Count > 1 -> independent blocks or numbered dimensions. Count = 0 -> validation error, not a rendering case.

### success_failure_relationship

- CONVERGED: Success and failure are **not inverses**. Both analyses use the same structural argument: an agent can fail success criteria (mediocre output) without triggering failure criteria (broken output). The three-state model (succeeded / mediocre / failed) is real and the rendering must not accidentally collapse it.
- DIVERGED: A treated this as a cross-section dependency. B elevated it to a full fragment with five alternatives. B's explicit separation statement ("avoiding failure does not guarantee success") is a concrete, testable intervention A did not specify.
- ALTERNATIVES:
  - A: **Explicit separation statement** -- Note in one or both sections: "Success criteria define quality. Failure criteria define breakage. These are independent evaluations." Clearest, most reliable.
  - B: **Structural separation only** -- Present as completely separate sections with no cross-reference. Clean, but the agent may conflate "not failed" with "succeeded."
- HYPOTHESIS: Explicit separation statement (A) is worth including. It costs one sentence and prevents a real conflation risk. Whether it lives in success criteria, failure criteria, or both is a rendering decision.
- STABILITY: structural
- CONDITIONAL: None. The independence is a fundamental principle.

## Cross-Section Dependencies

- **success_criteria -> execution_instructions**: Evidence items reference what instructions describe how to do. Success criteria state what correct execution produces; instructions state how to produce it. No circular reference or re-explanation.
- **success_criteria -> failure_criteria**: Independent evaluation dimensions. Must not be presented as inverses. Rendering should be parallel in structure (both use definition + evidence) but separate in location. Consistent dimensionality if success uses multiple criteria entries.
- **success_criteria -> guardrails**: Overlap exists. "No instruction step contains operational content" could be success evidence or a guardrail. Distinction: guardrails constrain behavior during execution; success evidence verifies output properties. Same condition, different temporal locus.
- **success_criteria -> examples**: Examples demonstrate what success looks like concretely. The builder's evidence explicitly references examples ("grounded in actual data shapes"). Criteria provide the abstract standard; examples provide concrete instances.
- **success_criteria -> role/identity**: Role framing affects how deeply the agent identifies with success criteria. A strong role identity ("meticulous builder") pairs with agent-centric voice. A functional role ("batch processor") pairs with output-centric voice.
- **success_criteria -> return/output**: The definition implicitly references what the agent produces ("have been written," "has been summarized"). The return section defines delivery mechanics. These must be consistent.
- **success_criteria -> section_ordering**: Placement relative to instructions is a cross-cutting concern that interacts with ordering decisions for all sections, not just this one.

## Conditional Branches

- **task_type (creative-constructive vs. batch-processing)** -> Affects definition framing (identity vs. specification), evidence framing (quality signals vs. checklist), temporal placement (pre-execution vs. post-execution), and engagement mode (self-model vs. checklist).
- **evidence_composition (all-mechanical vs. all-judgment vs. mixed)** -> Affects evidence type handling (undifferentiated list vs. graduated language vs. verification suffix) and temporal placement preference.
- **criteria_count (1 vs. N)** -> Count = 1: no multi-entry framing. Count > 1: independent blocks or numbered dimensions with conjunctive semantics.
- **evidence_count (few vs. many)** -> 3-4 items: tight list. 6+ items: consider thematic grouping to counteract primacy/recency bias.
- **role_strength (strong identity vs. functional)** -> Affects voice choice (agent-centric vs. output-centric) throughout the section.

## Open Design Questions

1. **Should evidence ordering be prescribed?** B observed an implicit priority in the raw data (structural completeness -> correctness -> quality). Is this deliberate? Should the renderer enforce or suggest an ordering, or leave it to the author?

2. **Is graduated language reliably detectable by agents?** The graduated verb strategy (must/equals for mechanical, should reflect/captures for judgment) is elegant but untested. Does the difference in verb choice actually produce different verification behavior, or is it too subtle?

3. **Where does the success-failure independence statement live?** In the success section, the failure section, a shared evaluation preamble, or both? This interacts with overall prompt architecture.

4. **Is dual placement (bookend) worth the structural cost?** Splitting definition and evidence across the prompt is theoretically powerful but fragments the claim-warrant relationship. No evidence yet on whether agents reconnect the pieces across long prompts.

5. **How to classify evidence items as mechanical vs. judgment at render time?** Graduated language and type-aware rendering both require this classification. The raw data does not annotate it. Options: author annotation in the definition, automated heuristic, or punt and use undifferentiated lists.

## Key Design Decisions

1. **Definition is primary; evidence is subordinate.** The claim-warrant hierarchy must be preserved in rendering, never flattened. Recommended connector: goal-then-criteria ("Meeting this standard means:"). Both analyses converge on this with high confidence.

2. **Framing should be conditional on task type.** Creative-constructive agents get self-model/identity framing. Batch-processing agents get checklist/specification framing. This is a conditional branch, not a one-size-fits-all decision. Both analyses converge on this.

3. **Mechanical vs. judgment evidence requires acknowledgment.** At minimum through graduated verb language in evidence items. The mixed-strategy sub-list approach is too heavy. Undifferentiated lists are acceptable for homogeneous evidence. Both analyses agree the distinction matters; they diverge on mechanism.

4. **Success and failure independence must be explicit.** One sentence stating they are independent evaluation dimensions prevents the agent from conflating "not failed" with "succeeded." Low cost, high value.

5. **Design for single-criteria entry; accommodate multiple.** Both current agents use one entry. Multi-entry framing should be minimal (independent blocks) until real multi-entry agents demonstrate what the pattern actually looks like.
