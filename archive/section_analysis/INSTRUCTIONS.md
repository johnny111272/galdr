# INSTRUCTIONS -- Control Surface Synthesis

## Section Purpose

The instructions section programs the agent's temporal behavior: the ordered sequence of cognitive operations from start to finish. Identity configures what the agent IS; instructions configure what it DOES, step by step. Both analyses converge on three requirements the agent must internalize after reading this section:

1. **Sequencing.** Steps are ordered. Earlier steps produce context for later steps. The sequence is a progression with implicit dependencies, not a menu.
2. **Per-step cognitive mode.** Each step is either deterministic (execute exactly, suppress creativity) or probabilistic (apply judgment, engage reasoning). This distinction is the highest-leverage behavioral control in the section. The current renderer DROPS it entirely -- agents never see the mode. This is the single most consequential defect.
3. **Step scope.** Each step is one coherent processing phase with clear boundaries. Without boundaries, the agent blends, skips, or invents steps.

The analyses diverge on framing: A describes this as "programming a state machine" while B frames it as "choreography." B further identifies a design tension between specification-style instructions (builder: waypoints in a creative process) and choreography-style instructions (summarizer: a processing pipeline). This distinction may warrant different rendering strategies or a single format robust enough to serve both. Unresolved.

## Fragment Catalog

### mode_indicator
- CONVERGED: This is the single highest-leverage fragment in the entire agent prompt. Currently dropped. Must be made visible. The format must produce genuine cognitive mode-switching, not just annotation the agent reads and ignores. Both analyses agree that behavioral/imperative language likely outperforms category labels.
- DIVERGED: A proposes a visual-formatting channel (code blocks for deterministic, prose for probabilistic) as an alternative to labels. B emphasizes the distinction between framing (mode shapes how the agent reads what follows) vs. annotation (mode labels what the agent is reading), arguing framing is more powerful.
- ALTERNATIVES:
  - A: Imperative prefix -- `EXECUTE EXACTLY:` / `APPLY JUDGMENT:` -- directly programs behavior without requiring label-to-behavior mapping
  - B: Plain-language parenthetical in step header -- `Step 1 (mechanical):` / `Step 2 (reasoning):` -- mode as identity, not instruction
  - C: Visual formatting differentiation -- deterministic steps in code-block style, probabilistic in flowing prose -- leverages trained associations below explicit reasoning
- HYPOTHESIS: Imperative framing produces the strongest mode-switching because it IS a behavioral instruction, not a label requiring interpretation. Visual formatting is high-risk/high-reward and untested. Plain-language parentheticals are the safest compromise. Key test: hallucination rate in deterministic steps and reasoning depth in probabilistic steps across formats.
- STABILITY: experimental
- CONDITIONAL: If all steps share one mode, a single preamble statement replaces per-step indicators.

### mode_preamble
- CONVERGED: Some form of mode-awareness before the first step improves mode compliance. Both analyses agree the current absence is a defect.
- DIVERGED: A offers a spectrum from full definitions to no definition. B focuses on whether a preamble teaches the agent "about" modes (meta-knowledge) versus priming the agent to respond to modes (behavioral preparation). B introduces "non-negotiable" as an anchor word for deterministic compliance.
- ALTERNATIVES:
  - A: Guardrail-style -- `Steps marked [exact] leave no room for interpretation. Steps marked [judgment] are where your reasoning matters.` -- brief, behavioral, no statistical jargon
  - B: No preamble -- trust the per-step indicators to work alone, avoiding dilution through meta-commentary
- HYPOTHESIS: Preamble helps on first encounter with mode markers. May become noise for well-calibrated agents. Model-dependent: Sonnet may need it more than Opus. Test: mode compliance with vs. without preamble, per model.
- STABILITY: experimental
- CONDITIONAL: May be omitted when all steps share one mode (no transitions to explain).

### mode_transition_signal
- CONVERGED: Both analyses identify the cognitive gear-shift at mode boundaries as a distinct behavioral event. A calls these "cognitive_transition_markers"; B calls them "mode_transition_signals." Same concept.
- DIVERGED: A proposes explicit prose markers between steps (`-- Now apply your judgment --`). B proposes visual breaks (extra whitespace or thin rule) at mode boundaries. Both worry about over-instrumentation.
- ALTERNATIVES:
  - A: Visual differentiation at mode-change boundaries only (stronger divider than same-mode boundaries)
  - B: Explicit transition phrase at mode changes -- `The following step requires your judgment.`
- HYPOTHESIS: Mode switches without any signal may be too subtle. But triple-instrumentation (preamble + per-step indicator + transition signal) likely causes the agent to focus on the meta-system. Pick at most two of three. Test: do transition signals improve compliance over indicators alone?
- STABILITY: experimental
- CONDITIONAL: Value scales with mode-switch frequency. High for interspersed patterns (D/P/D/P/P). Low for bookend patterns (D/P/P/P/P/P/D).

### section_heading_text
- CONVERGED: `## Processing` (current) is the weakest possible heading. It implies continuous activity, not discrete ordered steps. Both analyses agree it must change.
- DIVERGED: A proposes including the step count in the heading (`## Steps (7 total)`). B proposes removing the heading entirely. Neither is strongly endorsed by the other.
- ALTERNATIVES:
  - A: `## Instructions` -- standard LLM framing with strongest trained compliance associations
  - B: `## Procedure` -- strongest formality, reduces improvisation, best for deterministic-heavy agents
  - C: `## Steps ({N} total)` -- includes count, gives agent a completion target
- HYPOTHESIS: "Instructions" is the safe default. "Procedure" may outperform for batch-processing agents. Step count in the heading primes allocation but may cause rushing. Test: step-skipping rates across heading choices.
- STABILITY: structural (heading level and presence) + experimental (text choice)
- CONDITIONAL: none

### instructions_preamble
- CONVERGED: No preamble (current) means the agent discovers section structure mid-read. Both analyses agree a count-bearing preamble aids planning for longer step sequences.
- DIVERGED: B proposes an anti-failure guardrail preamble (`Do not add steps. Do not skip steps. Do not reorder steps.`) which A does not consider. This is a distinct behavioral intervention.
- ALTERNATIVES:
  - A: Count + mode preview -- `You will execute {N} steps. Steps marked [exact] must be followed precisely. Steps marked [judgment] require your reasoning.`
  - B: Guardrail preamble -- `The following steps define your complete workflow. Do not add steps. Do not skip steps. Do not reorder steps.`
  - C: No preamble -- step headers and mode indicators carry all information
- HYPOTHESIS: The guardrail preamble addresses the three most common step-level failures preemptively. Count preview helps the agent pace itself. These could combine but brevity matters. Test: does a step-count preamble reduce step-skipping for 7+ step agents?
- STABILITY: experimental
- CONDITIONAL: Content varies by step count (omit count for 2-3 steps) and mode distribution (omit mode preview if uniform).

### step_delimiter
- CONVERGED: The current same-separator defect (blank lines between AND within steps) is a structural failure that must be fixed. Both analyses treat this as non-negotiable.
- DIVERGED: A proposes combining the delimiter with mode and a first-sentence summary (`Step 1: Read input tempfile [EXACT]`). B proposes mode-varying separators (different divider weight at mode transitions vs. same-mode boundaries).
- ALTERNATIVES:
  - A: Numbered step headers with mode -- `**Step 1 [exact].** instruction_text...` -- boundary, identity, and mode in one element
  - B: Markdown H3 headings per step -- `### Step 1` -- strongest structural signal via heading hierarchy
- HYPOTHESIS: Fusing step number, mode indicator, and boundary into a single header element is the most information-dense option and avoids the over-instrumentation problem (one element carries three signals). Headings create the clearest visual hierarchy. Test: does mode-integrated numbering produce better mode compliance than separate mode labels?
- STABILITY: structural (steps MUST be delimited) + experimental (delimiter form)
- CONDITIONAL: none

### step_index_tracking
- CONVERGED: Steps must be numbered. Both analyses agree no-index is a defect. Both consider `N of M` format for completion awareness.
- DIVERGED: A considers descriptive identifiers instead of numbers (`Input Parsing`, `Core Analysis`). B does not.
- ALTERNATIVES:
  - A: `Step N of M` -- position + total, provides progress model
  - B: `Step N` -- position only, simpler, no rushing risk from visible total
- HYPOTHESIS: `N of M` improves completion rates for long step sequences by preventing the agent from treating early steps as the whole task. May cause rushing for later steps. Test: completion quality in steps 5-7 of a 7-step agent with vs. without totals.
- STABILITY: formatting
- CONDITIONAL: `N of M` likely unnecessary for 3 or fewer steps.

### step_body_presentation
- CONVERGED: Multi-paragraph instruction_text values must be perceived as one unit. Current rendering makes them indistinguishable from multiple steps.
- DIVERGED: A emphasizes containerization (blockquote, indented block). B notes that current bare rendering is "accidentally correct" for well-authored text and that containers risk "paragraph blindness."
- ALTERNATIVES:
  - A: Visual container per step (blockquote or indented block) -- binds multi-paragraph content as a unit
  - B: No wrapping -- rely on step headers/delimiters to mark boundaries; the text speaks for itself
- HYPOTHESIS: If step delimiters are strong enough (numbered headers), explicit body containers may be redundant. Containers add value primarily when instruction_text contains embedded lists that could be confused with step-level structure. Test: does containerization reduce step-boundary confusion beyond what strong headers provide?
- STABILITY: formatting
- CONDITIONAL: Steps with embedded bullet lists may need stronger containment than single-paragraph steps.

### step_mode_and_body_integration
- CONVERGED: Mode must arrive before or with the instruction text, never after. The primacy effect means mode-first placement shapes how the body is read.
- DIVERGED: B explicitly distinguishes three integration points: mode in body prefix, mode on separate line above body, mode in step header. A discusses these implicitly but does not isolate the integration as its own fragment.
- ALTERNATIVES:
  - A: Mode fused with step header -- `**Step 1 (exact):**` -- mode as identity
  - B: Mode as body prefix -- `[EXACT] Read the input...` -- mode as framing for what follows
- HYPOTHESIS: Mode-in-header makes mode part of the step's identity. Mode-as-body-prefix creates a priming effect for the content that follows. The header approach combines cleanly with step numbering. The prefix approach is more visually prominent per-step. Test: mode compliance with header-fused vs. body-prefix placement.
- STABILITY: structural
- CONDITIONAL: none

### section_closer
- CONVERGED: The section needs a clear endpoint. Without it, the agent may treat subsequent content as additional steps.
- DIVERGED: A focuses on "End of instructions" markers. B proposes a mode-recap closer that summarizes which steps are exact and which are judgment, serving as both reinforcement and guardrail against step invention. B also proposes a transition closer that frames subsequent sections as elaboration on the instructions.
- ALTERNATIVES:
  - A: Mode-recap closer -- `Steps 1 and 3 are exact. Steps 2, 4, and 5 require judgment. There are no other steps.` -- reinforces mode system + bounds step count
  - B: Guardrail closer -- `These {N} steps constitute your complete task. Do not add additional steps.` -- explicit boundary
- HYPOTHESIS: The mode-recap closer is the highest-value option because it serves three functions: mode reinforcement, step-count bounding, and compressed reference for execution. Test: does a mode-recap closer improve mode compliance compared to no closer?
- STABILITY: structural (whether to close) + experimental (closer content)
- CONDITIONAL: Mode-recap only valuable for mixed-mode agents. Uniform-mode agents need only the guardrail form.

### dependency_signaling
- CONVERGED: Both analyses identify cross-step dependencies as implicit in instruction ordering but invisible in presentation. Both are cautious about over-annotating.
- DIVERGED: A proposes explicit annotations (`Step 4 (uses: preparation package from Step 1)`). B proposes weaving dependency language into instruction text (`Using the instruction steps designed in the previous phase...`).
- ALTERNATIVES:
  - A: Woven into instruction text -- natural prose reference to prior step output
  - B: No explicit annotation -- linear ordering IS the dependency graph for most agents
- HYPOTHESIS: For 5 or fewer steps, implicit ordering suffices. For 7+ steps, the agent may lose track of what was established 5 steps ago. Woven references are less intrusive than formal annotations. Test: do woven dependency references reduce cases where agents forget earlier outputs in 7+ step sequences?
- STABILITY: conditional + experimental
- CONDITIONAL: Likely unnecessary for 5 or fewer steps. Scales with step count and cross-step reference density.

### step_completion_signal
- CONVERGED: Both analyses independently identified this as a missing fragment. Neither the current system nor the data contains completion criteria per step. Both note it matters more for probabilistic steps (when is "identify the core domain" complete?) than deterministic (when is "read the file" complete? when the file is read).
- DIVERGED: A frames this as "step_completion_expectation" (configuring whether steps produce visible output). B frames it as "step_completion_signal" (preventing over- and under-processing). Related but distinct angles.
- ALTERNATIVES:
  - A: `Done when: {completion condition}` suffix on probabilistic steps only
  - B: No explicit signal -- the next step's existence implies the current step is bounded
- HYPOTHESIS: Completion signals for probabilistic steps may prevent the agent from exhausting context on early reasoning steps. But they are template-generated, not author-provided, raising the question of whether the template system should add behavioral guidance absent from the raw data. Test: do completion conditions on probabilistic steps reduce over-processing?
- STABILITY: experimental
- CONDITIONAL: Only for probabilistic steps. Deterministic steps have self-evident completion.

### instruction_text_authority
- CONVERGED: A identifies this explicitly ("instruction_text_is_authoritative"). B addresses it implicitly through mode design. Both recognize the core problem: LLMs default to expanding, interpreting, and supplementing instructions.
- DIVERGED: A asks whether this belongs in the instructions section or in critical_rules. B does not surface this placement question.
- ALTERNATIVES:
  - A: Preamble-level statement -- `Each instruction step is a complete specification. Do not add operations or supplement steps with general knowledge.`
  - B: Implicit in mode system -- deterministic mode already means "execute exactly this"
- HYPOTHESIS: For deterministic steps, the mode system handles this. For probabilistic steps, an anti-expansion directive risks suppressing useful reasoning. Scope this to the preamble as a default, with mode markers providing per-step calibration. Test: does an anti-expansion directive reduce hallucination on deterministic steps without degrading probabilistic reasoning?
- STABILITY: experimental
- CONDITIONAL: May need different strength based on mode distribution. All-probabilistic agents may not need it.

### progress_anchor
- CONVERGED: A identifies this; B identifies a related concept ("cognitive_load_warning"). Both address the "lost in the middle" problem where middle steps receive less attention.
- ALTERNATIVES:
  - A: Midpoint anchor -- `You are past the halfway point. Steps 1-4 established the foundation.`
  - B: Implicit through step numbering with totals (`Step 4 of 7`)
- HYPOTHESIS: `N of M` numbering may provide sufficient progress awareness without dedicated anchor fragments. Explicit anchors risk creating false phase transitions. Test: does `N of M` numbering alone prevent mid-sequence attention degradation?
- STABILITY: experimental
- CONDITIONAL: Only for 7+ step agents. Short sequences do not have a "middle."

## Cross-Section Dependencies

- **instructions -> identity.role_description**: Role description establishes the cognitive stance; instruction steps operationalize it. Shared terminology is mandatory -- if identity says "contextual significance," instructions must use the same phrase.
- **instructions -> examples**: Examples demonstrate correct instruction execution. Each example should map to one or more instruction steps. Some instruction_texts already contain inline examples, partially filling the examples section's role.
- **instructions -> constraints/critical_rules**: Constraints may duplicate instruction content (belt-and-suspenders). Critical rules may ADD operational requirements not present in any instruction step (batch discipline). Instructions must not contradict either. Rendering must decide whether constraint-instruction overlap is reinforcement or noise.
- **instructions -> success_criteria/failure_criteria**: Success criteria define what correct execution looks like. Every criterion should correspond to an instruction step. Instructions create the contract; criteria define compliance.
- **instructions -> input**: Step 1 typically restates or extends the input format. This creates a redundancy to manage: does step 1 repeat the input format or reference the input section?
- **instruction_mode + instruction_text**: These form a per-step unit. Mode must arrive before text to produce a priming effect. Presenting them separately (mode label, then text) or integrated (mode in header) is a core design choice.
- **instruction count -> structural decisions**: Step count drives whether to include counts in heading/preamble, whether `N of M` tracking adds value, whether progress anchors are needed, and how much structural scaffolding is warranted.

## Conditional Branches

- **STEP COUNT -> SCAFFOLDING WEIGHT**: 1-3 steps: lightweight (numbers, compact mode). 4-7 steps: standard (headers, mode indicators, dividers). 8+ steps: heavy (named phases, recap preamble, progress indicators).
- **MODE DISTRIBUTION -> MODE INFRASTRUCTURE**: All-same-mode: single preamble statement, no per-step indicators. Mixed-mode: per-step indicators + preamble. High-frequency switching (D/P/D/P/P): transition signals gain value. Low-frequency switching (D/P/P/P/P/P/D): transition signals at the two boundaries only.
- **INSTRUCTION_TEXT LENGTH -> BODY TREATMENT**: Single-sentence steps: inline after header. Multi-paragraph steps: own visual space with clear boundaries. Steps with embedded lists: stronger containment to prevent list/step confusion.
- **INLINE EXAMPLES IN INSTRUCTION_TEXT -> CONTAINER STRENGTH**: Steps containing inline examples need stronger visual containment because example content resembles separate paragraphs.
- **CROSS-STEP REFERENCES -> DEPENDENCY SIGNALING**: Steps that explicitly reference earlier outputs need step numbering/naming for referenceability. Self-contained steps do not.
- **SPECIFICATION VS. CHOREOGRAPHY -> FRAGMENT TUNING**: Builder-type (creative specification): completion signals more valuable, mode indicators less critical. Summarizer-type (processing choreography): mode indicators more critical, completion signals less needed.

## Open Design Questions

1. **Should the template system add behavioral guidance not present in the raw data?** Completion signals, dependency annotations, and progress anchors are all template-generated, not author-provided. Where is the boundary between presentation and behavioral augmentation?

2. **Specification vs. choreography: one format or two?** The builder's instructions are creative waypoints. The summarizer's are a processing pipeline. Do these need different rendering strategies, or can one format serve both? Neither analysis resolves this.

3. **Over-instrumentation threshold.** Preamble + per-step mode indicator + transition signal + progress anchor = four layers of meta-commentary around the actual instruction content. At what point does scaffolding drown the content? Which combination of two or three (not all) produces the best result?

4. **Model dependency of mode indicators.** Do plain-language terms ("exact"/"judgment") outperform technical terms ("deterministic"/"probabilistic") across model tiers? Opus may have stronger concept mappings for statistical terms. Sonnet may respond better to behavioral language. Is this a model-conditional rendering choice?

5. **Constraint-instruction overlap: reinforcement or noise?** When constraints restate instruction content, is this deliberate belt-and-suspenders or accidental duplication that dilutes both sections?

## Key Design Decisions

1. **Mode indicator format.** Imperative prefix (`EXECUTE EXACTLY:`) vs. header-fused parenthetical (`Step 1 (exact):`) vs. visual formatting. Both analyses lean toward behavioral language over category labels. Strongest direction: imperative or plain-language form that directly programs behavior rather than requiring label interpretation.

2. **Step delimiter design.** Whether to fuse step number, mode indicator, and boundary into a single element (e.g., `**Step 1 [exact].**`) or keep them as separate layers. Strongest direction: fused single-element headers that carry boundary + identity + mode, avoiding triple-instrumentation overhead.

3. **Preamble composition.** What combination of count preview, mode explanation, and anti-failure guardrails to include before the first step. Strongest direction: count + mode preview for mixed-mode agents with 4+ steps; guardrail prohibitions (`Do not add/skip/reorder steps`) for all agents.

4. **Closer design.** Whether the section ends silently or with a mode-recap / step-count-bounding statement. Strongest direction: mode-recap closer for mixed-mode agents; simple guardrail closer for uniform-mode agents.

5. **Scaffolding weight as a function of step count and mode distribution.** The rendering system must scale its structural overhead to the complexity of the instruction set. Strongest direction: define three tiers (lightweight/standard/heavy) with explicit thresholds based on step count, with mode distribution as a secondary factor.
