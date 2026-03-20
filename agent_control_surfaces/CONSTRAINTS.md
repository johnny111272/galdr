# CONSTRAINTS — Control Surface Synthesis

## Section Purpose

Constraints define the operational boundary layer — they are not instructions (which describe what to do in sequence) and not anti-patterns (which describe gravitational failure tendencies). Constraints are **ambient law**: always-on, conjunctive, independently auditable rules that apply to every action the agent takes during execution. The agent does not execute constraints; it is filtered by them.

The compliance hierarchy is a three-tier model. Critical rules are termination triggers (violation = output rejected). Constraints are compliance standards (violation = output defective). Anti-patterns are quality gradients (tendency toward = degradation). This middle position is the section's defining characteristic: more specific and testable than critical rules, more authoritative and binary than anti-patterns.

The single most important behavioral effect of this section is **boundary internalization** — the agent absorbs constraints as a persistent filter, not a checklist to run once at the end. Every fragment choice in this section either strengthens or weakens that internalization.

## Fragment Catalog

### constraint_preamble

- CONVERGED: Both analyses agree this is mandatory, high-stability, and must establish three properties: (1) always-on / ambient, not sequential; (2) conjunctive — all apply simultaneously; (3) binary — respected or violated. Both agree the preamble is where authority level is set and positional decay is counteracted.
- DIVERGED: A frames the preamble as a single composite fragment; B decomposes it into sub-fragments (authority, ambient framing, completeness). A emphasizes hierarchy positioning within the preamble; B treats hierarchy as a separate concern.
- ALTERNATIVES:
  - A: Composite — "These constraints govern your execution. They are not sequenced — all are in force at all times. Each is a compliance standard your output will be measured against." [Concise, sets authority + ambient nature in one shot]
  - B: Instruction-boundary lead — "While executing your instructions, these rules remain in effect." [Minimal; relies on other fragments for authority]
  - C: Hierarchy-aware — "These constraints are binding operational rules — less absolute than critical rules, but more enforceable than general quality guidance. Violating a constraint means your output is defective." [Sets hierarchy without naming other sections by title]
- HYPOTHESIS: A preamble that explicitly distinguishes constraints from instructions ("not steps, not sequenced") measurably improves compliance versus a bare section header. The hierarchy-aware variant (C) reduces confusion at the cost of length.
- STABILITY: structural
- CONDITIONAL: If critical_rules section exists in the prompt, prefer hierarchy-aware variant. If constraints section stands alone, composite variant is sufficient.

### constraint_instruction_boundary

- CONVERGED: Both identify the constraint-instruction boundary as the most critical cross-section relationship. Both flag that rules like "Validate ALL 18 conditional field rules before writing any output" read as workflow steps but live in constraints because they are ambient conditions. Both agree explicit distinction is needed.
- DIVERGED: A treats this as a sub-fragment that could fold into the preamble. B treats it as a standalone fragment with its own alternatives. B raises the "what vs. how" framing as the clearest mental model.
- ALTERNATIVES:
  - A: "Constraints are not steps — they are conditions that must hold true at all times, not at specific points in your workflow." [Direct negation of the step interpretation]
  - B: "Your instructions tell you what to do. Your constraints tell you how — the standards that apply to every action." [What/how frame]
- HYPOTHESIS: Without this fragment, agents treat constraints as additional instructions and try to sequence them. The "not steps, conditions" framing is the minimum viable intervention.
- STABILITY: structural
- CONDITIONAL: Mandatory when any rule in the constraints list reads like a workflow step. Can be lighter if all rules are clearly ambient.

### constraint_enumeration_format

- CONVERGED: Both agree numbering implies false sequence/priority and that constraints have neither. Both agree flat structure should be preserved for lists under ~8 rules.
- DIVERGED: A leans bulleted as the default (numbers imply sequence); B leans numbered for 6+ rules (enables auditability, referenceability). A considers polarity grouping for long lists; B considers it but warns it fragments authored coherence.
- ALTERNATIVES:
  - A: Bulleted, preserving authored order. [No false priority; simplest]
  - B: Numbered for 6+ rules, bulleted for fewer. [Enables audit reference; count verification]
  - C: Bulleted with MUST/MUST NOT prefix standardization. [Clarity at cost of voice]
- HYPOTHESIS: For constraint sections specifically, bullets are preferable because constraints are a set, not a sequence. Numbering's auditability benefit is real but secondary to avoiding false priority signals.
- STABILITY: formatting
- CONDITIONAL: len(rules) <= 5 -> bullets. len(rules) >= 6 -> numbers become defensible. len(rules) > 10 -> consider polarity grouping.

### polarity_normalization

- CONVERGED: Both identify the mixed-voice problem (builder uses imperative; summarizer uses explicit MUST/MUST NOT). Both acknowledge MUST/MUST NOT is clearest for compliance but warn about overwriting author intent.
- DIVERGED: A recommends normalizing outliers to match majority voice (Alternative D in source). B recommends preserving authored voice as a principle, adding authority through the preamble instead.
- ALTERNATIVES:
  - A: Preserve authored voice exactly; let preamble carry authority. [Respects author intent; no rewriting risk]
  - B: Normalize outliers to match majority voice within each agent. [Fixes inconsistency without full rewrite]
  - C: Prepend polarity prefix without rewriting: `[REQUIRED]` / `[PROHIBITED]`. [Adds clarity without touching author text]
- HYPOTHESIS: Voice preservation (A) is the safer default. Normalization risks subtle meaning shifts. If an author wrote "Do not" rather than "MUST NOT," that choice may encode intended severity. The preamble should carry the authority burden, not per-rule rewriting.
- STABILITY: formatting (high-stakes formatting — affects meaning)
- CONDITIONAL: If all rules already use consistent markers -> no action. If mixed voice -> design decision required (A or B).

### completeness_signal

- CONVERGED: Both identify the phantom-constraint problem (LLMs self-impose additional constraints not in the prompt). Both consider explicit completeness signals. Both flag the tradeoff: prevents phantom constraints but may enable loophole mentality.
- DIVERGED: A recommends a light signal ("These are your constraints"). B recommends explicit exhaustive framing ("do not infer additional constraints") but acknowledges the loophole risk.
- ALTERNATIVES:
  - A: Omit — let preamble authority and list presentation suffice. [Minimalist]
  - B: Light — "These are your operational constraints." [Implies completeness without asserting it]
  - C: Explicit — "These {N} rules are exhaustive — do not infer additional constraints not listed here." [Direct anti-hallucination]
- HYPOTHESIS: Explicit completeness framing reduces phantom constraints but is only worth the tokens if phantom constraint inference is an observed problem. Start without it; add when needed.
- STABILITY: experimental
- CONDITIONAL: Add if empirical testing shows agents self-imposing unlisted constraints.

### closing_reinforcement

- CONVERGED: Both identify positional decay (rules at end of list receive less attention). Both agree closing reinforcement is more valuable for longer lists.
- DIVERGED: A does not treat this as a distinct fragment. B proposes explicit closing alternatives and flags the "auditable" framing as particularly powerful.
- ALTERNATIVES:
  - A: Omit — preamble carries sufficient authority. [Lean; avoids redundancy]
  - B: "Every constraint above is auditable. Your output will be evaluated against each one." [Reactivates attention; implies external review]
  - C: "All {N} constraints apply simultaneously throughout execution." [Count reinforcement + ambient reminder]
- HYPOTHESIS: The "auditable" framing triggers a compliance mode distinct from the preamble's authority framing — it shifts from "these are rules" to "these rules will be checked." This is a different behavioral lever.
- STABILITY: experimental
- CONDITIONAL: len(rules) <= 5 -> omit. len(rules) >= 6 -> include. len(rules) > 10 -> mandatory.

### rule_count_communication

- CONVERGED: Both agree explicit counts become valuable for longer lists.
- DIVERGED: Only B treats this as a standalone fragment. A folds it into length adaptation.
- ALTERNATIVES:
  - A: "You have {N} operational constraints:" [Header-position count]
  - B: Trailing: "All {N} constraints above apply simultaneously." [Post-list count as verification]
- HYPOTHESIS: Explicit count creates a self-checking mechanism. More valuable at 6+ rules.
- STABILITY: formatting
- CONDITIONAL: len(rules) <= 5 -> omit. len(rules) >= 6 -> include (either position).

### hierarchy_framing

- CONVERGED: Both agree the three-tier model (critical_rules > constraints > anti_patterns) must be communicated. Both warn against naming other sections directly (creates coupling).
- DIVERGED: A prefers relative framing without section names. B proposes explicit tier numbering ("tier 2 of 3"). Both agree implicit positioning alone is insufficient.
- ALTERNATIVES:
  - A: "These constraints are binding operational rules — less severe than critical rules but more enforceable than quality guidance." [Relative without naming sections]
  - B: "You operate under three tiers of behavioral rules: critical rules (hard failures), constraints (compliance standards), and anti-patterns (quality risks). This section defines tier 2." [Explicit tier model]
- HYPOTHESIS: Relative framing (A) is preferable — it communicates hierarchy without creating cross-section coupling. If section names change, the preamble does not break.
- STABILITY: structural
- CONDITIONAL: Fold into preamble when both critical_rules and anti_patterns sections exist. Omit when constraints section is the only restriction section.

## Cross-Section Dependencies

| Dependency | Nature |
|---|---|
| constraints <-> critical_rules | Hierarchical. Constraints are lower authority. Preamble must differentiate without contradicting critical rule content. |
| constraints <-> anti_patterns | Hierarchical. Constraints are binary rules; anti-patterns are tendencies. Template must not create constraint categories that overlap with anti-pattern descriptions. |
| constraints <-> instructions | Orthogonal. Constraints apply DURING instruction execution, not after. Boundary distinction fragment is essential. |
| constraints <-> examples | Validating. Examples should demonstrate constraint-compliant output. Constraints may reference examples section but must not inline examples. |

## Conditional Branches

| Condition | Effect |
|---|---|
| `rules` array is empty | Omit entire section |
| len(rules) <= 5 | Minimal preamble; bullets; no count header; no closing reinforcement |
| len(rules) 6-10 | Full preamble; bullets or numbers; count header; closing reinforcement |
| len(rules) > 10 | Full preamble with conjunctive reinforcement; numbers; count header; closing reinforcement; consider polarity grouping |
| All rules use consistent MUST/MUST NOT | Preserve voice — already normalized |
| Mixed voice conventions | Design decision: preserve + preamble authority (recommended) or normalize outliers |
| Any rule reads like a workflow step | Boundary distinction fragment is mandatory |
| critical_rules section exists | Hierarchy framing in preamble is mandatory |
| critical_rules section absent | Hierarchy framing can be omitted |

## Open Design Questions

1. **Polarity normalization**: A recommends normalizing outliers; B recommends preserving voice as principle. Both have merit. Needs empirical testing: does mixed voice actually degrade compliance, or does the preamble compensate?

2. **Numbered vs. bulleted at medium lengths (6-10)**: A says bullets always; B says numbers at 6+. The auditability benefit of numbers is real but so is the false-priority risk. Needs testing.

3. **Constraint envelope tightness**: A identifies that some agents have tight constraint envelopes (summarizer: constraints nearly fully determine output) vs. loose envelopes (builder: constraints prevent errors but leave latitude). Should the template detect and signal this? Both analyses are uncertain. Likely not worth designing for until empirical evidence demands it.

4. **Completeness signal threshold**: At what point does phantom constraint inference become enough of a problem to justify spending tokens on an explicit completeness signal? No data yet.

5. **Closing reinforcement redundancy**: If the preamble is strong, is closing reinforcement additive or merely redundant? The "auditable" framing may be a distinct lever (external review implication), but this is speculative.

## Key Design Decisions

1. **Constraints are ambient law, not procedure.** Every fragment choice must reinforce that constraints are always-on filters, not sequential steps. This is the non-negotiable framing principle.

2. **Three-tier compliance model.** Critical rules (termination) > constraints (defective output) > anti-patterns (quality drift). The preamble establishes this position using relative framing, not section name references.

3. **Preserve authored voice by default.** The template should not rewrite rule text. Authority comes from the preamble, not from per-rule MUST/MUST NOT normalization. Mixed-voice handling is a deferred design decision pending empirical data.

4. **List format scales with count.** Bullets for short lists, numbers defensible at 6+, polarity grouping considered at 11+. Count header and closing reinforcement scale similarly.

5. **Boundary distinction is mandatory.** The constraint-instruction boundary fragment is required whenever any rule could be misread as a workflow step — which is most agents.

6. **Fragment composition is conditional.** The minimal section is preamble + rule list. Additional fragments (count, closing, hierarchy framing) activate based on rule count and prompt structure.
