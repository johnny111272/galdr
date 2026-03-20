# CONSTRAINTS Section Analysis

## First Principles: What Does This Section Accomplish?

Constraints occupy a unique behavioral niche. They are not instructions — instructions tell the agent *what to do* and *how to do it*. Constraints tell the agent *what it must not become* while doing whatever it does. They define the shape of the solution space by carving away what is forbidden, mandating what is non-negotiable, and establishing stylistic rails that keep output from drifting.

The behavioral effect of reading a constraint list is **boundary internalization**. The agent does not execute constraints sequentially (as it does instructions). Instead, it absorbs them as a persistent filter: every candidate action, every candidate output, passes through the constraint mesh. Constraints are always-on, not step-sequential.

This is the key distinction: instructions are a path; constraints are a fence around the path. Instructions say "walk north." Constraints say "do not cross the river, do not leave the road, carry your pack at all times." The agent can follow instructions perfectly and still violate constraints. They operate on orthogonal axes.

### The Compliance Hierarchy Problem

Three sections contain behavioral restrictions: `critical_rules`, `constraints`, and `anti_patterns`. The agent must understand their relative weight. Without explicit framing, an agent will treat all restrictions as roughly equivalent — or worse, will treat the *last one read* as most salient due to recency bias.

The natural hierarchy, derived from the data:

- **critical_rules**: Existential. Violation = task failure. These are the "if you do this, nothing else matters" rules. They are few (typically 2-4) and absolute.
- **constraints**: Operational. Violation = defective output. These define the boundaries of acceptable execution. They are numerous (7-10) and concrete. An agent that violates a constraint produces wrong work but has not fundamentally misunderstood its role.
- **anti_patterns**: Gravitational. Tendency toward these = quality degradation. These describe failure modes the agent is prone to, not rules it might break. An agent drifting toward an anti-pattern is losing quality, not violating a rule.

The relationship is not strictly hierarchical — it is more like concentric rings. Critical rules are the hard boundary (binary: violated or not). Constraints are the operational corridor (many specific boundaries). Anti-patterns are the quality gradient (continuous: more or less drift).

The framing of the constraints section must establish this middle position: more specific than critical rules, more authoritative than anti-patterns, and fundamentally about the *shape of acceptable output* rather than identity (critical rules) or tendency (anti-patterns).

---

## FIELD: rules
TYPE: array of strings (flat, untyped, variable-length)
VALUES: 10 rules (agent-builder) / 7 rules (interview-enrich-create-summary)

### What the agent needs to understand

Each rule is a discrete, independently-enforceable restriction. The agent must treat the list as a conjunction: ALL rules apply simultaneously, not selectively. There is no prioritization within the list — a constraint is either respected or violated, and violating any single rule is a defect.

The rules are not uniform in kind despite the flat structure. Examining the data reveals at least three distinct categories:

1. **Positive mandates** — things that MUST happen: "Use ONLY field names from agent-template.toml", "MUST process exchanges in order", "MUST produce exactly one sentence per exchange"
2. **Negative prohibitions** — things that MUST NOT happen: "Do not write tool invocation syntax...", "MUST NOT reference or load learned, threads, insight..."
3. **Completeness/style directives** — qualitative requirements: "Produce a COMPLETE definition or ABORT", "Write instruction text as dull facts", "MUST use hedging language for reconstructed exchanges"

The template has a choice: impose this categorization explicitly (group by type) or present flat and let the rules speak for themselves.

### Fragments

**constraint_list_preamble — establishes the section's authority and relationship to other restriction sections**

- Alternative A: "The following constraints define the boundaries of acceptable output. Every constraint applies simultaneously — violating any single rule produces defective work. Constraints are not suggestions; they are the shape of correct execution."
- Alternative B: "These rules are hard boundaries on your execution. They do not tell you what to do — your instructions handle that. They tell you what you must not become and what your output must not lack. All constraints are active at all times."
- Alternative C: "Constraints govern the form and limits of your work. Unlike instructions, which you follow step by step, constraints apply to every action you take. Unlike anti-patterns, which describe tendencies to avoid, constraints are binary: you either respect them or you violate them."
- Alternative D: "You must satisfy every constraint below while executing your instructions. A constraint violation makes your output defective regardless of how well you followed instructions. These are non-negotiable boundaries."

- PURPOSE: Establish that constraints are (a) always-on, not sequential, (b) conjunctive — all apply simultaneously, (c) binary — respected or violated, and (d) positioned between critical rules (identity-level) and anti-patterns (tendency-level) in the compliance hierarchy.
- HYPOTHESIS: Without a preamble, agents treat constraint lists as "additional instructions" and weigh them proportionally to instruction count. A preamble that explicitly distinguishes constraints from instructions and establishes their always-on nature measurably improves compliance. The preamble that explicitly contrasts with other sections (Alternative C) will reduce confusion about the hierarchy but adds length. The terse version (Alternative D) may work best for short lists.
- STABILITY: High — every agent has constraints; every agent needs to understand their authority level. The preamble concept is stable even if the exact wording evolves.

**constraint_enumeration_format — how rules are presented within the list**

- Alternative A: Numbered list, preserving authored order exactly as written:
  ```
  1. Use ONLY field names from agent-template.toml...
  2. Validate ALL 18 conditional field rules...
  ```
- Alternative B: Bulleted list with MUST/MUST NOT normalization applied to all rules regardless of author voice:
  ```
  - MUST use only field names from agent-template.toml...
  - MUST validate all 18 conditional field rules...
  - MUST NOT write tool invocation syntax...
  ```
- Alternative C: Grouped by polarity (positive mandates first, then prohibitions), each group with a sub-header:
  ```
  **Required:**
  - Use ONLY field names from agent-template.toml...
  - Validate ALL 18 conditional field rules...

  **Prohibited:**
  - Do not write tool invocation syntax...
  - Do not write batch discipline rules...
  ```
- Alternative D: Flat bulleted list, preserving author voice exactly (no normalization, no grouping):
  ```
  - Use ONLY field names from agent-template.toml...
  - Do not write tool invocation syntax...
  ```

- PURPOSE: Determine whether the template imposes structure on the flat rule array or passes it through with minimal formatting.
- HYPOTHESIS: Numbering implies sequence/priority where none exists — constraints are conjunctive, not ordered. Bulleting avoids false priority. MUST/MUST NOT normalization (Alternative B) improves machine compliance by making polarity explicit, but overwrites authoring voice. Grouping by polarity (Alternative C) helps the agent mentally partition "things I must do" from "things I must avoid" but introduces a structural opinion the data does not contain. Preserving author voice (Alternative D) is simplest and respects the authored data, but misses the opportunity to clarify polarity for rules that use softer language.
- STABILITY: Medium — the choice between normalization and voice preservation is a design decision that will be revisited as more agents are observed. The numbered-vs-bulleted question is more stable (bulleted is almost certainly correct for a conjunctive list).

**constraint_completeness_signal — whether/how to signal that the list is exhaustive**

- Alternative A: "These are all of your constraints. No additional restrictions apply beyond what is listed here."
- Alternative B: "The following constraints are comprehensive. Your instructions may imply additional boundaries — but only these are enforceable as constraint violations."
- Alternative C: No completeness signal — the list simply ends.

- PURPOSE: Tell the agent whether it should infer additional constraints from context or treat this list as closed.
- HYPOTHESIS: Without a completeness signal, agents often infer phantom constraints from instruction text or role descriptions, leading to over-cautious behavior. An explicit "this is the complete list" signal (Alternative A) reduces phantom constraint inference. However, Alternative B acknowledges that instructions inherently contain implicit constraints without elevating them to the same enforcement level. Alternative C (no signal) is simplest and may be sufficient if the preamble is strong enough.
- STABILITY: Low-medium — this depends on observed agent behavior. If agents consistently infer phantom constraints, a completeness signal becomes necessary. If they don't, it's wasted tokens.

---

## STRUCTURAL: Constraint Polarity and Voice Normalization

### What the agent needs to understand

The raw data uses mixed voice conventions. The builder agent uses imperative voice ("Use ONLY...", "Do not write...") while the summarizer agent uses explicit modal markers ("MUST process...", "MUST NOT reference..."). This is an authoring difference, not a semantic one — both express the same compliance expectation.

The template must decide: normalize to a single voice, or preserve authored voice?

### Fragments

**polarity_normalization_strategy**

- Alternative A: **Normalize all rules to MUST/MUST NOT** — rewrite rules to use explicit modal verbs regardless of how the author wrote them. "Do not write tool invocation syntax" becomes "MUST NOT write tool invocation syntax." "Use ONLY field names" becomes "MUST use only field names."
- Alternative B: **Preserve authored voice exactly** — pass rules through as written. The author's choice of "Do not" vs "MUST NOT" is their authoring decision.
- Alternative C: **Add polarity prefix without rewriting** — prepend a visual marker to each rule without changing the text: `[REQUIRED] Use ONLY field names...` / `[PROHIBITED] Do not write tool invocation syntax...`
- Alternative D: **Normalize only inconsistent rules** — if the author used MUST/MUST NOT for some rules and plain imperative for others, normalize the outliers to match the majority voice. Fully consistent authored voice is preserved.

- PURPOSE: Determine whether the template should impose voice consistency on the constraint list.
- HYPOTHESIS: MUST/MUST NOT normalization (Alternative A) produces the clearest compliance signal for the agent, making every rule's polarity unambiguous. But it overwrites authoring choices and may flatten emphasis patterns the author intentionally created (the builder uses "Do not" for soft prohibitions and reserves stronger language for mandates). Polarity prefixes (Alternative C) add clarity without overwriting, but introduce visual clutter. Preserving voice (Alternative B) respects authoring but may reduce compliance clarity for rules with ambiguous polarity. Alternative D is the pragmatic middle — it fixes inconsistency without overwriting intentional voice.
- STABILITY: Medium — this is a template-level design choice. Once decided, it should apply consistently. But it may be revised after observing whether voice normalization measurably affects compliance.

---

## STRUCTURAL: Constraint List Length and Cognitive Load

### What the agent needs to understand

The builder has 10 constraints; the summarizer has 7. Future agents may have 3 or 15. The template must handle variable-length lists without losing effectiveness at either extreme.

### Fragments

**length_adaptation_strategy**

- Alternative A: **No adaptation** — present all constraints identically regardless of count. 3 constraints or 15 constraints get the same preamble and format.
- Alternative B: **Adapted preamble intensity** — short lists (1-4 rules) get a minimal preamble; medium lists (5-10) get the standard preamble; long lists (11+) get the standard preamble plus an explicit "all of these apply simultaneously" reinforcement.
- Alternative C: **Chunking for long lists** — lists over 8 rules are split into logical groups (positive/negative, or by topic) to reduce cognitive load. Short lists remain flat.

- PURPOSE: Ensure constraint compliance does not degrade as list length increases.
- HYPOTHESIS: For LLMs, compliance with list items tends to degrade past ~8 items in a flat list — items in the middle receive less attention than those at the beginning or end. Grouping (Alternative C) mitigates this by creating multiple short lists instead of one long one. However, grouping introduces structural opinions. No adaptation (Alternative A) is simplest and relies on the model's native attention. Adapted preamble (Alternative B) is a lightweight intervention that reinforces the conjunctive nature for longer lists without restructuring the data.
- STABILITY: Low — this depends heavily on empirical observation. The right strategy will emerge from seeing which agents drop which constraints.

---

## STRUCTURAL: Section Positioning and Cross-Section Dependencies

### What the agent needs to understand

Constraints interact with three other sections: `critical_rules` (higher authority), `anti_patterns` (lower authority/different kind), and `instructions` (orthogonal — what to do vs. what boundaries apply). The agent must understand that constraint compliance is evaluated *during* instruction execution, not as a separate phase.

### Fragments

**hierarchy_framing — how to establish the constraint section's position relative to other restriction sections**

- Alternative A: **Explicit hierarchy statement in preamble**: "Constraints sit between critical rules (which define task failure) and anti-patterns (which describe quality drift). A constraint violation makes output defective; a critical rule violation makes the task failed; an anti-pattern is a tendency to monitor, not a rule to enforce."
- Alternative B: **Implicit hierarchy through section ordering**: Place critical_rules first, then constraints, then anti_patterns. Let position imply authority. No explicit comparison.
- Alternative C: **Relative framing without naming other sections**: "These constraints are binding rules — not as absolute as your core rules, but more enforceable than general quality guidance. Violating a constraint means your output is defective."
- Alternative D: **No hierarchy framing** — each section stands on its own. The agent infers relationships from the content and section names.

- PURPOSE: Ensure the agent correctly weights constraints relative to other behavioral restriction sections.
- HYPOTHESIS: Explicit hierarchy (Alternative A) is the clearest signal but creates cross-section coupling — if section names change, the preamble breaks. Implicit hierarchy through ordering (Alternative B) is elegant but fragile — the agent may not infer authority from position. Relative framing (Alternative C) avoids naming sections while still establishing weight. No framing (Alternative D) is cleanest but risks the agent treating all restrictions as equally weighted, which collapses the useful distinction between "your output is wrong" (constraint violation) and "your output is drifting" (anti-pattern tendency).
- STABILITY: High for the concept, medium for the implementation — the need to differentiate constraint authority is stable; the best mechanism to express it will evolve.

**instruction_constraint_interaction — how the agent understands constraints during instruction execution**

- Alternative A: "Apply these constraints throughout instruction execution. Every step you take must satisfy every constraint simultaneously."
- Alternative B: "Constraints are not steps — they are filters. As you execute each instruction, check your candidate output against every constraint before committing it."
- Alternative C: No explicit interaction statement — the preamble's "always-on" language handles this implicitly.

- PURPOSE: Prevent the agent from treating constraints as a checklist to run once at the end, rather than a continuous filter during execution.
- HYPOTHESIS: Alternative B produces the clearest mental model (filter, not checklist) but may over-specify the mechanism. Alternative A is more directive but uses "simultaneously" which may be interpreted as "check at the end." Alternative C relies on the preamble doing enough work. The risk of no interaction statement is that agents write their full output following instructions, then "check constraints" at the end — which produces worse results than continuous constraint awareness.
- STABILITY: Medium — the need to establish continuous application is clear; whether it needs its own fragment or can be folded into the preamble is a design question.

---

## STRUCTURAL: Constraint-to-Rule Boundary (When Does a Constraint Become a Critical Rule?)

### What the agent needs to understand

Some constraints read like they should be critical rules. "Produce a COMPLETE definition or ABORT with a structured fault list — no partial definitions" (builder) feels existential — it defines what task failure looks like. "MUST process exchanges in order — never skip, never reorder" (summarizer) also feels foundational. Why are these in constraints and not critical_rules?

### Fragments

**boundary_principle**

- Alternative A: **Critical rules are about identity; constraints are about output.** A critical rule violation means the agent fundamentally misunderstood its job. A constraint violation means the agent understood its job but produced defective output. "Produce COMPLETE or ABORT" is a constraint because it governs output form, not agent identity.
- Alternative B: **Critical rules are few and absolute; constraints are many and concrete.** The distinction is about count and specificity: critical rules are 2-4 broad principles; constraints are 5-15 specific rules. Any rule specific enough to be testable belongs in constraints.
- Alternative C: **Critical rules survive across all agents of a type; constraints are task-specific.** If a rule would apply to ANY builder agent regardless of what it's building, it's a critical rule. If it's specific to this agent's particular task, it's a constraint.
- Alternative D: **The distinction is author intent, not formal criteria.** The template does not enforce a boundary — the author places rules where they judge them to belong, and the template frames each section appropriately.

- PURPOSE: Establish a principle for why rules land in constraints vs. critical_rules, so the template can frame each section's authority consistently.
- HYPOTHESIS: Alternative A provides the cleanest conceptual distinction but may not match all data (some critical rules are about output, not identity). Alternative B is practical but arbitrary — "few and absolute" doesn't explain *why* they're different, just *how* they differ in practice. Alternative C aligns with the pattern in the data but may be too subtle for the agent to act on. Alternative D is the safest — it doesn't try to formalize the boundary, just frames what it's given.
- STABILITY: Low — this is a design question that may not have a single right answer. The principle should be documented but may evolve as more agent definitions are authored.

---

## STRUCTURAL: The Summarizer's Exhaustive Specification Pattern

### What the agent needs to understand

The summarizer's constraints form a near-complete behavioral specification: process in order, one sentence per exchange, exact count match, no external data, no quality markers, use hedging language. Together, these constraints leave almost no room for interpretation — they tightly specify what correct output looks like.

The builder's constraints are looser — they prohibit specific mistakes but leave more room for judgment within the allowed space.

This is a spectrum: some agents have **tight constraint envelopes** (the summarizer) where constraints nearly fully determine output; others have **loose constraint envelopes** (the builder) where constraints prevent specific errors but leave wide latitude.

### Fragments

**envelope_awareness — whether the template acknowledges constraint tightness**

- Alternative A: **No acknowledgment** — the template presents all constraint lists identically. The tightness of the envelope emerges naturally from the content.
- Alternative B: **Adaptive framing** — for tight envelopes (many MUST + MUST NOT rules that collectively specify output), add: "These constraints collectively define the exact shape of correct output. Deviation from any single constraint means your output is wrong." For loose envelopes, add: "These constraints define boundaries. Within those boundaries, use your judgment."
- Alternative C: **Author-controlled signal** — add an optional field like `constraint_envelope = "tight"` or `"loose"` that controls which framing the template uses.

- PURPOSE: Help the agent understand whether constraints are leaving room for judgment or fully specifying behavior.
- HYPOTHESIS: Alternative B could significantly improve compliance for tight-envelope agents by signaling that there is no room for creative interpretation. But it requires the template to detect tightness, which is a judgment call. Alternative C makes it explicit but adds a field to the definition format. Alternative A is simplest and may be sufficient — an agent reading 7 MUST/MUST NOT rules should naturally understand there's no room for creativity.
- STABILITY: Low — this is speculative. It may not be worth designing for until empirical evidence shows that tight-envelope agents underperform without explicit envelope signaling.

---

## Summary of Key Design Decisions

1. **Compliance hierarchy**: Constraints sit between critical_rules (existential/identity) and anti_patterns (gravitational/tendency). The preamble must establish this position.

2. **Always-on framing**: Constraints are continuous filters, not sequential steps. This is the single most important thing the preamble must communicate.

3. **Conjunctive application**: ALL constraints apply simultaneously. Violating one is a defect regardless of compliance with the others.

4. **Voice normalization**: The strongest candidate is Alternative D (normalize inconsistent rules within an agent, preserve consistent authored voice). This respects authoring intent while fixing ambiguity.

5. **List format**: Bulleted, not numbered. Numbers imply priority or sequence; constraints have neither.

6. **Grouping**: Preserve flat structure for lists under ~8 rules. Consider polarity grouping for longer lists, but this is an empirical question.

7. **Completeness signal**: Include a light signal ("These are your constraints" rather than "These are ALL your constraints") unless phantom constraint inference becomes an observed problem.

8. **Cross-section interaction**: The preamble should establish authority relative to other sections, but by relative description (Alternative C) rather than by naming other sections (Alternative A), to avoid coupling.

---

## Cross-Section Dependency Map

| Dependency | Direction | Nature |
|---|---|---|
| constraints <-> critical_rules | Hierarchical | Constraints are lower authority; must not contradict critical rules; preamble must establish the difference |
| constraints <-> anti_patterns | Hierarchical | Constraints are higher authority and binary; anti-patterns are tendencies; preamble must establish the difference |
| constraints <-> instructions | Orthogonal | Constraints apply DURING instruction execution, not after; the agent must check constraints at every step |
| constraints <-> examples | Validating | Examples should demonstrate constraint-compliant output; constraint violations in examples would be contradictory |
| constraints <-> role | Informing | Role context may explain WHY certain constraints exist, but constraints are binding regardless of role understanding |

---

## Conditional Branches

| Condition | Branch |
|---|---|
| rules array is empty | Omit the entire section — an empty constraint section is noise |
| rules array has 1-3 items | Minimal preamble; flat bulleted list; no grouping |
| rules array has 4-10 items | Standard preamble; flat bulleted list; consider completeness signal |
| rules array has 11+ items | Standard preamble with reinforced conjunctive language; consider polarity grouping |
| All rules use MUST/MUST NOT | Preserve voice — already normalized |
| Rules use mixed voice | Apply Alternative D normalization (normalize outliers to match majority voice) |
| Rules are all negative prohibitions | Consider reframing preamble to emphasize "boundary" metaphor over "requirement" metaphor |
| Rules are all positive mandates | Consider reframing preamble to emphasize "specification" metaphor |
