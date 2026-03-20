# IDENTITY — Control Surface Synthesis

## Section Purpose

The identity section narrows the agent's self-model from general-purpose assistant to a specific actor with a defined cognitive stance, scope, and authority. Both analyses converge on three behavioral effects this narrowing produces: **filtering** (constraining which actions the agent considers available), **defaulting** (providing a fallback heuristic for uncovered cases), and **resistance** (stabilizing the agent against task drift when inputs push it off-course). These effects compound — filtering shrinks the solution space, defaulting fills gaps, resistance holds it steady.

Identity is not information delivery — it is initialization. The section sets a lens through which every subsequent section is interpreted. An agent reading instructions through "data forms, not prose documents" interprets ambiguity differently than one reading through "contextual significance." This framing effect is the section's primary behavioral mechanism.

One analysis adds a critical observation: identity serves different functions depending on agent type. For creative/broad agents (builder), identity is primarily a **boundary** — don't go here. For mechanical/narrow agents (summarizer), identity is primarily a **lens** — look at it this way. A uniform template may miss this distinction. Whether the template should adapt to agent type is an open design question that affects multiple fragments below.

## Fragment Catalog

### heading_element
- CONVERGED: The H1 heading with the agent's name creates a "biographical document" framing that may cause the agent to treat subsequent content as descriptive rather than prescriptive. Both analyses see this as potentially defective.
- DIVERGED: B raises whether heading level itself matters (H1 vs H2 vs none), treating level as a signal about the section's status within the larger prompt. A focuses more on prefix options ("Agent:" prefix).
- ALTERNATIVES:
  - A: `# AGENT: {title}` — prefix distinguishes role assignment from document title, keeps structural anchor
  - B: No heading — section opens with prose. Title is metadata only; role_identity carries the self-concept. Strongest for agents with clunky system names.
- HYPOTHESIS: Heading presence is less important than which name dominates the agent's self-concept. When title is a natural role label ("Agent Builder"), use it. When it is a pipeline identifier ("Interview Enrich Create Summary"), suppress it from prose and lead with role_identity.
- STABILITY: structural
- CONDITIONAL: Title readability. Natural-language titles may appear in heading; pipeline identifiers should not. Requires definition-time annotation or heuristic.

### name_in_prose
- CONVERGED: Title currently appears only as heading text, never in body prose. Both analyses see this as a design decision, not a bug.
- DIVERGED: A considers "You are Agent Builder" as identity reinforcement. B argues that role_identity ("definition author") is almost always the better self-concept to amplify, since titles are often system labels rather than usable identity anchors.
- ALTERNATIVES:
  - A: Title absent from prose — role_identity is the sole self-concept in body text
  - B: Title in closing reinforcement: `Remember: you are Agent Builder, a definition author.` — bookend pattern using both names
- HYPOTHESIS: For agents with readable titles, both names can coexist. For agents with system-label titles, role_identity should be the only self-concept in prose.
- STABILITY: experimental
- CONDITIONAL: Title readability (same trigger as heading_element)

### description_presence
- CONVERGED: The description field is triple-redundant (frontmatter, identity, dispatcher) and written in third person, creating a voice mismatch with the second-person role_description. Both analyses question whether it belongs in the identity section at all.
- DIVERGED: A sees possible value in keeping it as a one-sentence anchor. B argues more firmly for suppression, noting the description serves the dispatch infrastructure, not the agent.
- ALTERNATIVES:
  - A: Omit entirely — role_description already covers the same ground in the correct voice
  - B: Render only when description carries information absent from role_description (builder: mentions "include files" and "preparation packages" which role_description does not; summarizer: fully redundant)
  - C: Transform to second person and use as opening sentence, eliminating voice mismatch
- HYPOTHESIS: Conditional presence (B) is the most precise solution. The voice mismatch from rendering both third-person description and second-person role_description may subtly undermine the prompt's authority.
- STABILITY: structural
- CONDITIONAL: Content overlap between description and role_description. Requires definition-time annotation or content-comparison logic.

### description_label
- CONVERGED: If description IS rendered, "Purpose:" is passive and document-like.
- DIVERGED: Minor. A explores "Mission:" framing; B explores "You do this:" for voice matching.
- ALTERNATIVES:
  - A: `**Mission:**` — active assignment framing
  - B: No label — woven into prose
- HYPOTHESIS: Second-order effect. The description-presence decision dominates. If description is rendered, label choice has marginal impact.
- STABILITY: formatting
- CONDITIONAL: Only relevant if description is rendered (depends on description_presence decision)

### identity_declaration
- CONVERGED: This is the single highest-leverage fragment in the entire identity section. Both analyses rank it #1 for behavioral impact. The standard "You are a X" pattern is recognized by all LLMs but may be processed shallowly due to familiarity.
- DIVERGED: A emphasizes negative bounding ("not a software engineer, not a prompt writer") as a mechanism. B emphasizes making identity *usable* by adding an explicit decision heuristic ("ask: what would a definition author do?"). These are different mechanisms — boundaries vs. decision procedure.
- ALTERNATIVES:
  - A: `You are a {role_identity}. This identity governs every decision you make — when in doubt, ask: what would a {role_identity} do?` — declaration + explicit heuristic
  - B: `You are a {role_identity} — not a debugger, not a reviewer, not a creative writer.` — declaration + scope negation
  - C: `As a {role_identity}, you...` — subordinate clause leading into role_description, fusing identity with stance
- HYPOTHESIS: The decision-heuristic form (A) gives the agent a reusable procedure. The negation form (B) closes specific adjacent identities. The subordinate form (C) prevents identity from floating as an abstract label. These may not be mutually exclusive — a fused form could combine heuristic + negation. Testing should compare heuristic vs. negation as independent mechanisms.
- STABILITY: experimental
- CONDITIONAL: Agent type may determine which mechanism matters more. Creative/broad agents may benefit from negation (preventing drift into adjacent roles). Mechanical/narrow agents may benefit from the heuristic (reinforcing the specific cognitive stance).

### identity_placement
- CONVERGED: Primacy effects are strong — first-encountered information disproportionately shapes interpretation. Identity should appear early.
- DIVERGED: B proposes a bookend pattern (identity at start AND end) to exploit both primacy and recency. A considers this but frames it as the section_closer fragment.
- ALTERNATIVES:
  - A: First prose the agent reads — identity as opening salvo
  - B: Bookend — opens with identity, closes with recap. `You are a {role_identity}. ... Remember: {role_identity}.`
- HYPOTHESIS: The bookend pattern may reduce identity fade for agents with long prompts. For short-prompt agents, primacy alone is sufficient. Whether this is worth the redundancy cost is an empirical question.
- STABILITY: structural
- CONDITIONAL: Prompt length. Long prompts may benefit from recency reinforcement; short prompts need only primacy.

### role_description_envelope
- CONVERGED: The role_description is pre-authored in second person. Any wrapping prose competes with its own voice. Both analyses agree: minimal or no envelope is best. Labels convert immersive experience into specification-reading.
- DIVERGED: B identifies a specific sub-pattern — the role_description typically contains an explicit cognitive contrast ("data forms, not prose documents"; "conversational significance, not isolated text") — and asks whether the template should amplify that contrast. A does not identify this pattern.
- ALTERNATIVES:
  - A: No envelope — role_description stands as bare paragraph directly after identity declaration
  - B: Fused with identity: `You are a {role_identity}. {role_description}` — one continuous paragraph, preventing the agent from separating "who" from "how"
- HYPOTHESIS: The fused form (B) may produce the strongest identity-stance unity. The bare paragraph (A) respects the authored text's voice. Adding any label weakens the role_description's effectiveness.
- STABILITY: structural
- CONDITIONAL: none

### contrast_amplification
- CONVERGED: n/a — only B identified this fragment
- DIVERGED: B observes that role_descriptions contain explicit cognitive contrasts and asks whether the template should amplify them (e.g., extracting "Data forms, not prose documents" as a separate bold line). A does not address this.
- ALTERNATIVES:
  - A: Do nothing — trust the authored text. The definition creator chose their words.
  - B: Follow the role_description with the extracted contrast in bold: `**{contrast phrase}.**`
- HYPOTHESIS: Amplification may reinforce the core cognitive distinction but teaches the agent that the prompt repeats important things, potentially causing it to downweight non-repeated content. May be useful for long prompts where the contrast risks being forgotten. Risky for short prompts.
- STABILITY: experimental
- CONDITIONAL: Prompt length. Only valuable if the total prompt is long enough that the contrast would otherwise fade.

### responsibility_framing
- CONVERGED: The responsibility is the scope contract — the deliverable. Both analyses distinguish it from role_description (how to think) and agree it needs its own framing.
- DIVERGED: B proposes "You are done when:" — inverting the frame from what-to-do to what-done-looks-like, directly configuring the agent's completion detector. A does not explore this inversion.
- ALTERNATIVES:
  - A: `**Scope:** {role_responsibility}` — boundary framing, emphasizing what is inside and outside
  - B: `**You are done when:** {role_responsibility}` — completion-condition framing, configuring the agent's termination criterion
  - C: No label — woven into the identity paragraph: `Specifically, you {role_responsibility}.`
- HYPOTHESIS: "Scope" may reduce scope creep for complex-task agents. "Done when" may reduce premature termination for continuous-task agents. The best label may be agent-type-conditional.
- STABILITY: experimental
- CONDITIONAL: Agent task type. Boundary framing for creative/broad agents; completion framing for mechanical/continuous agents.

### responsibility_decomposition
- CONVERGED: Complex responsibilities (builder: 7 verb phrases) should be decomposed into a list. Simple responsibilities (summarizer: 1 clause) should remain prose. Both analyses agree this is a conditional formatting decision.
- DIVERGED: B notes that numbered lists imply sequencing, which may or may not match the agent's actual workflow. A does not flag this risk.
- ALTERNATIVES:
  - A: Conditional on verb-phrase count. >3 clauses: bulleted list. <=3: prose.
  - B: Numbered list for complex responsibilities, with caveat that numbering implies order (use bullets if order is not meaningful)
- HYPOTHESIS: List decomposition of complex responsibilities reduces task omission. Bullet vs. number depends on whether sub-tasks have a meaningful sequence.
- STABILITY: formatting + conditional
- CONDITIONAL: Verb-phrase count in role_responsibility. Threshold around 3.

### expertise_framing
- CONVERGED: The current "Expertise:" label is a passive inventory. Both analyses argue it should be an active directive — either authority grant or attention directive.
- DIVERGED: A focuses on "Domain authority:" (permission to decide). B distinguishes two functions — permission ("authoritative in") and attention ("pay special attention to") — and argues the framing should activate whichever function matters more for the agent.
- ALTERNATIVES:
  - A: `**Your judgment is authoritative in:**` — authority grant, reduces hedging
  - B: `**Pay special attention to:**` — attention directive, increases signal detection
- HYPOTHESIS: "Authoritative" framing reduces hedging in expertise-domain judgments. "Pay attention" framing increases detection of relevant signals. For agents whose expertise areas involve decision-making (builder: security modeling), authority framing is better. For agents whose expertise involves noticing patterns (summarizer: marker decontamination), attention framing is better.
- STABILITY: experimental
- CONDITIONAL: Whether expertise domains are primarily decision-oriented or detection-oriented.

### expertise_display_format
- CONVERGED: Comma-separated inline text is too easy to skim. Both analyses prefer bulleted lists for visual weight.
- DIVERGED: B proposes a conditional threshold (2-3 items inline, 4+ bulleted). A does not specify a threshold.
- ALTERNATIVES:
  - A: Bulleted list always — each item gets visual weight
  - B: Conditional: <=3 items inline, >=4 items bulleted
- HYPOTHESIS: The threshold approach (B) prevents over-structuring short lists while maintaining readability for long ones.
- STABILITY: formatting
- CONDITIONAL: Array length. Threshold at 3-4 items.

### expertise_negative_boundary
- CONVERGED: Both analyses identify this as high-risk/high-reward. Explicit negation may close off adjacent identities OR may prime those identities via ironic process theory.
- DIVERGED: B distinguishes between explicit negation (naming excluded domains — risky), implicit negation ("strictly limited to the above" — safer but vaguer), and no negation (relying on the positive list). A considers only explicit negation vs. none.
- ALTERNATIVES:
  - A: Implicit negation: `Your expertise is strictly limited to the areas listed above.` — safe, non-priming
  - B: No negation — positive list is sufficient. Constraints section handles drift prevention.
- HYPOTHESIS: Explicit negation is too risky (priming effect). Implicit negation adds a safety margin without naming specific excluded domains. For agents adjacent to default LLM behaviors (builder ~ coding), implicit negation may be worth including. For agents with unusual expertise (summarizer), the positive list is distinctive enough to be self-limiting.
- STABILITY: experimental
- CONDITIONAL: How adjacent the agent's task is to default LLM behaviors.

### model_rendering
- CONVERGED: Both analyses lean toward omitting model from the identity section. The risk of self-stereotyping (Sonnet agents underperforming) outweighs self-calibration benefit. Model is infrastructure metadata for the dispatch system, not behavioral configuration.
- DIVERGED: Neither analysis presents strong arguments for rendering. Convergence is high.
- ALTERNATIVES:
  - A: Omit entirely — model belongs in frontmatter only
  - B: Render only for specific use cases (debugging, self-referential output) — but these cases are rare
- HYPOTHESIS: Omission is the correct default. If model awareness is ever needed, it should be an explicit opt-in, not a default rendering.
- STABILITY: structural
- CONDITIONAL: none (omit unless future evidence shows model awareness helps specific agent types)

### section_opening_strategy
- CONVERGED: Meta-preambles ("The following configures your identity...") are counterproductive — they create cognitive distance between the agent and its identity. The agent observes initialization rather than experiencing it.
- DIVERGED: A considers a cognitive-mode primer ("This task requires sustained analytical judgment...") as a pre-identity fragment. B calls this "task_mode_primer" and agrees it is worth testing but notes it requires a new data field or inference logic.
- ALTERNATIVES:
  - A: Open directly with identity declaration: `You are a {role_identity}.` — no meta-layer, immediate initialization
  - B: Composite paragraph fusing identity + stance: `You are a {role_identity}. {role_description}` — single coherent impression before any structural parsing
- HYPOTHESIS: Direct opening (A) is the safe default. Composite opening (B) may produce stronger identity-stance unity but becomes unwieldy for long role_descriptions.
- STABILITY: structural
- CONDITIONAL: Length of role_description. Short descriptions fuse well; long descriptions may need separation.

### section_closer
- CONVERGED: Clean `---` divider is the neutral default. Both analyses raise the question of identity reinforcement at the section boundary.
- DIVERGED: B proposes a forward-referencing transition ("the following sections tell you what to do, how to do it safely, and how your work will be evaluated"). A proposes a backward-referencing recap ("Remember: you are a {role_identity}").
- ALTERNATIVES:
  - A: `---` only — clean break, no transition prose
  - B: Recap before divider: `Remember: you are a {role_identity}.` followed by `---`
- HYPOTHESIS: Recap may reduce identity fade for long prompts. For short prompts, the clean break is sufficient. The forward-referencing roadmap is interesting but may violate separation of concerns (identity section should not describe other sections).
- STABILITY: experimental
- CONDITIONAL: Prompt length

### field_sequence
- CONVERGED: Both analyses identify primacy effects as the dominant concern. Both list identity-first, stance-first, responsibility-first, and fused as the main alternatives.
- DIVERGED: B argues the best ordering may be agent-type-conditional (identity-first for creative agents, responsibility-first for mechanical agents). A lists the alternatives without making this conditional claim.
- ALTERNATIVES:
  - A: **Identity-first**: role_identity -> role_description -> role_responsibility -> role_expertise
  - B: **Fused**: all fields composed into 1-2 paragraphs, no discrete ordering
- HYPOTHESIS: Identity-first is the safe default for all agents. Fused is the experimental alternative for agents where identity-stance unity is critical. Responsibility-first is worth testing for mechanical agents but is a departure from the standard identity-section purpose.
- STABILITY: structural
- CONDITIONAL: Potentially agent type, but establishing a single default ordering first is advisable.

### density_strategy
- CONVERGED: Identity benefits from internalization (dense prose) more than recall (labeled specification). Both analyses argue for higher density in the core identity fields.
- DIVERGED: Both independently propose variable density as the best compromise. Convergence is strong.
- ALTERNATIVES:
  - A: Variable density — core fields (role_identity, role_description) as dense prose; supporting fields (responsibility, expertise) as labeled/structured
  - B: High density — all fields in 1-2 paragraphs, no labels
- HYPOTHESIS: Variable density (A) optimizes for both internalization (core) and recall (supporting details). High density (B) risks losing trackability for complex responsibilities.
- STABILITY: structural
- CONDITIONAL: none

## Cross-Section Dependencies

- **identity -> instructions**: Identity sets the interpretive lens for instructions. An identity emphasizing "data forms, not prose" causes the agent to interpret ambiguous instructions toward structured output. The identity creates expectations the instructions must fulfill.
- **identity -> critical_rules**: Critical rules override identity. Strong identity framing ("this governs all decisions") may cause the agent to resist critical rules that seem contradictory. Identity framing affects the agent's receptiveness to overrides.
- **identity -> security_boundary**: Identity claims must not imply capabilities the security boundary denies. Expertise in "filesystem management" + read-only access = dissonance.
- **identity.role_responsibility -> success_criteria**: Every item in the responsibility chain should have corresponding success evidence. Misalignment forces the agent to resolve the gap.
- **identity.role_expertise -> constraints/anti_patterns**: Expertise grants authority; constraints restrict it. Overlapping domains create contradictions the template system should detect, not leave to the agent.

## Conditional Branches

- **RESPONSIBILITY COMPLEXITY** (verb-phrase count > 3) -> Decompose into bulleted/numbered list instead of inline prose
- **DESCRIPTION REDUNDANCY** (content overlap with role_description is high) -> Suppress description from identity section
- **TITLE READABILITY** (system-label vs. natural-language name) -> Suppress title from body prose; lead with role_identity
- **EXPERTISE COUNT** (array length > 3) -> Switch from inline to bulleted list
- **PROMPT LENGTH** (long instruction section) -> Add identity recap at section closer; consider contrast amplification
- **AGENT TASK TYPE** (creative/broad vs. mechanical/narrow) -> Affects identity_declaration mechanism (negation vs. heuristic), responsibility_framing (scope vs. done-when), expertise_framing (authority vs. attention). Note: this conditional is NOT in the current data model. Either infer from signals or add a field.

## Open Design Questions

1. **Should the template infer agent type, or should the data model include a task_type field?** Multiple fragments have agent-type-conditional behavior. Inference is fragile; a new field is clean but adds authoring burden. Both analyses surface this but neither resolves it.

2. **Does identity reinforcement at section boundaries actually reduce identity fade, or does it teach the agent that the prompt repeats itself?** The bookend/recap pattern is promising but carries a redundancy cost. Empirical testing required.

3. **Does making identity a decision procedure ("ask: what would a X do?") outperform making it a boundary ("not a debugger, not a reviewer")?** These are different behavioral mechanisms. They might compose well or interfere. Neither analysis had data to resolve this.

4. **Should the template amplify cognitive contrasts embedded in role_description, or trust the authored text?** Only one analysis identified this pattern. Its value is unknown and likely prompt-length-dependent.

5. **Where does agency calibration belong — identity, instructions, or critical_rules?** Both analyses identify the need to tell the agent how much autonomous judgment to exercise in novel situations. Neither establishes which section owns this fragment.

## Key Design Decisions

1. **Description rendering: suppress, conditional, or always present?** Strongest direction: conditional — render only when description carries information absent from role_description. Eliminates voice mismatch and redundancy in the common case while preserving additive information.

2. **Identity declaration mechanism: heuristic, negation, or fusion?** Strongest direction: start with the heuristic form ("when in doubt, ask what would a {role_identity} do?") as the default, test negation as an enhancement for agents adjacent to default LLM behaviors. Fusion (subordinate clause into role_description) is the fallback if standalone declarations prove shallow.

3. **Field ordering: fixed or agent-type-conditional?** Strongest direction: establish identity-first as the default ordering for all agents. Test fused rendering as an experimental variant. Defer agent-type-conditional ordering until the task_type question (Open Question 1) is resolved.

4. **Variable density as default architecture?** Strongest direction: yes. Dense prose for role_identity + role_description (internalization), structured/labeled for role_responsibility + role_expertise (recall). Both analyses converge on this independently.

5. **Expertise as active directive vs. passive inventory?** Strongest direction: reframe from "Expertise:" to an active form. The specific active form (authority grant vs. attention directive) may be conditional on the nature of the expertise domains, but any active framing outperforms the current passive label.
