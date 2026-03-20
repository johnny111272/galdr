# ANTI_PATTERNS -- Control Surface Synthesis

## Section Purpose

Anti-patterns are **failure mode inoculation**. They operate through recognition-triggered aversion, not boundary enforcement (constraints) or inviolable rules (critical_rules). The mechanism: expose the agent to a weakened form of a mistake paired with its antidote, so the agent has antibodies when the live pathogen appears during execution. This is experience transfer -- compressing "I watched agents fail this way ten times" into a single corrective statement the agent receives without having failed.

The "Do not X -- Y" structure is the load-bearing element. The prohibition activates a failure mode representation. The reasoning clause after the dash redirects that activation toward correct behavior. This two-part structure is what mitigates ironic process risk: "Do not think of a white bear -- think of its shadow on the snow instead" redirects rather than merely suppresses. Bare prohibitions without reasoning clauses would collapse anti-patterns into weaker constraints.

Authority sits between constraints and critical rules. Violating an anti-pattern degrades output quality but does not break the system. The framing should convey "this will make your output worse," not "this will cause system failure."

## Fragment Catalog

### header_label
- CONVERGED: "Anti-Patterns" is too diluted through software engineering overuse. Both prefer labels that make the agent's own liability explicit.
- DIVERGED: A rates header stability HIGH (cosmetic, patterns do the work); B rates it MEDIUM (sets interpretive context for everything below).
- ALTERNATIVES:
  - A: `## Known Failure Modes` -- empirically grounded, positions patterns as observed facts, both analyses favor this
  - B: `## Mistakes You Will Make` -- confrontational, forces effortful processing, risk of adversarial framing reducing cooperation
  - C: `## Anti-Patterns` -- familiar but abstract; safe fallback
- HYPOTHESIS: Headers that name the agent as the likely failure source produce stronger aversions than neutral engineering labels.
- STABILITY: formatting
- CONDITIONAL: none

### header_preamble
- CONVERGED: One line maximum. The patterns are the payload; framing is packaging. Overly long preambles dilute urgency.
- DIVERGED: A considers no-preamble viable (patterns self-explain with "Do not" prefix). B insists a brief preamble is needed to prevent the agent from treating the list as advisory.
- ALTERNATIVES:
  - A: No preamble -- trusts the "Do not" structure to self-contextualize
  - B: `"These are specific failure modes for this task. Each names a mistake and provides the correction after the dash."` -- establishes reading mode in one line
  - C: `"These failures emerge naturally from how you process instructions. Recognizing them before they happen is the purpose of this section."` -- frames as self-recognition task
- HYPOTHESIS: A one-line preamble that signals "these are active behavioral corrections, not background context" shifts the agent from passive acknowledgment to active monitoring. Value is concentrated entirely in the first moments of pattern processing.
- STABILITY: formatting
- CONDITIONAL: Omit preamble if pattern count is 1-2 (self-evident); include if 3+.

### pattern_format
- CONVERGED: The "Do not X -- Y" structure is self-parsing. Bare bullet list is sufficient. Numbering implies unintended priority. Bold or separation adds marginal value for well-structured patterns.
- DIVERGED: Minimal. Both favor simplicity. B additionally considers keyed/named patterns for cross-referencing but classifies it as over-engineering.
- ALTERNATIVES:
  - A: Bare bulleted list -- `- Do not X -- Y.` -- minimal, correct, consistent with authored format
  - B: Bold prohibition -- `- **Do not X** -- Y.` -- adds visual hierarchy for the two-part structure
- HYPOTHESIS: Since every pattern already starts with "Do not," the structure is self-parsing. Additional formatting competes with content for attention.
- STABILITY: structural
- CONDITIONAL: none

### pattern_ordering
- CONVERGED: Author-determined order. Template must not reorder. Author has domain knowledge the template lacks. Primacy effects are real -- first pattern gets disproportionate attention.
- DIVERGED: B suggests making the convention explicit ("first = most critical") in authoring guidance. A leaves ordering authority entirely to the author without stated convention.
- ALTERNATIVES:
  - A: Preserve authored order silently -- no ordering signal in output
  - B: Preserve authored order + state convention in authoring guidance: "list most critical failure mode first"
- HYPOTHESIS: Position already encodes priority if the convention is known. Making it explicit costs nothing and strengthens the signal.
- STABILITY: structural
- CONDITIONAL: none

### reasoning_clause
- CONVERGED: **MANDATORY.** The reasoning clause after the dash is the core mechanism that differentiates anti-patterns from bare constraints and prevents ironic process priming. Both analyses rate this as their highest-confidence finding. Without it, anti-patterns collapse into weaker constraints.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Inline after dash (current) -- `"Do not X -- because Y"` -- keeps prohibition and antidote in one cognitive unit
  - B: Positive reframe variant -- `"Do not X -- instead, do Y"` -- more constructive but may weaken prohibition aspect
- HYPOTHESIS: The inline format keeps the failure mode and its correction as a single cognitive unit, which is almost certainly more effective than any separated structure.
- STABILITY: structural
- CONDITIONAL: Validation warning if a pattern lacks a reasoning clause after the dash.

### authority_signal
- CONVERGED: Anti-patterns need distinguishable authority level. They sit below critical_rules, above general instructions. Merging anti-patterns into constraints destroys the distinct behavioral mechanism.
- DIVERGED: A considers placement alone may be sufficient for small definition files; B insists on explicit prose. B proposes the framing "guard your judgment" as the most accurate description of what anti-patterns do.
- ALTERNATIVES:
  - A: No explicit signal -- rely on section ordering to convey hierarchy
  - B: One-line bridging: `"Constraints bound WHAT you do. Anti-patterns correct HOW you do it."`
  - C: Full positioning: `"Anti-patterns guard your judgment. Critical rules protect the system. Constraints bound your behavior."`
- HYPOTHESIS: If the rendered prompt has 3+ restrictive sections, explicit authority differentiation prevents the agent from flattening them into a single rule list.
- STABILITY: formatting
- CONDITIONAL: Include explicit authority prose when constraints AND critical_rules AND anti-patterns all appear. Omit when anti-patterns appear alone.

### empty_handling
- CONVERGED: If no anti-patterns are defined, omit the section entirely. No placeholder, no note, no "exercise standard judgment" filler.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Omit when empty -- the only option
- HYPOTHESIS: An absent section is simpler and less harmful than an empty section with anxiety-inducing meta-commentary about unknown failure modes.
- STABILITY: structural
- CONDITIONAL: `patterns` absent or empty array -> omit entire section.

### scaling_behavior
- CONVERGED: Render all author-provided patterns without truncation. If the author wrote 15, they had 15 failure modes to communicate. Capping discards author knowledge.
- DIVERGED: A says scaling is purely an authoring problem. B recommends soft guidance of 3-7 patterns and suggests high counts (>7) may indicate section misuse where some items are better classified as constraints.
- ALTERNATIVES:
  - A: Render all, no limit -- authoring problem, not template problem
  - B: Render all + soft authoring guidance of 3-7 + validation warning at >7
- HYPOTHESIS: Each additional pattern dilutes per-pattern attention. 5 patterns (current data) is near optimal. The template should not enforce limits, but authoring guidance should recommend restraint.
- STABILITY: structural
- CONDITIONAL: none (template renders all; authoring layer may warn)

### ironic_process_management
- CONVERGED: The "Do not X -- Y" structure handles ironic process effects implicitly through the reasoning clause. No explicit meta-framing needed. If ironic process effects are observed, fix the specific pattern's reasoning clause, not the global framing.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Implicit handling only -- trust the pattern structure
- HYPOTHESIS: The agent does not need to understand WHY the structure works. Adding meta-commentary about ironic process theory is over-engineering that competes with patterns for attention.
- STABILITY: structural
- CONDITIONAL: none

### redundancy_with_instructions
- CONVERGED: Redundancy between instructions and anti-patterns is a feature. The instruction "summarize significance" and the anti-pattern "do not classify importance" operate through different behavioral channels even when pointing at the same behavior. One creates positive drive, the other creates failure mode recognition.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Tolerate redundancy -- different mechanisms, same goal
- HYPOTHESIS: An agent that has both the positive instruction and the negative anti-pattern is better calibrated than one with either alone. Deduplication removes a safety net.
- STABILITY: structural
- CONDITIONAL: none

## Cross-Section Dependencies

| Dependency | Direction | Nature |
|---|---|---|
| role/identity -> anti_patterns | Hard | Agent must understand its task to contextualize domain-specific failure modes. Role MUST be established first. |
| instructions -> anti_patterns | Soft | Anti-patterns may reference concepts from instructions (e.g., "software tools"). Render anti-patterns AFTER instructions. |
| constraints <-> anti_patterns | Structural | MUST be separate sections. Constraints set walls (compliance). Anti-patterns build aversions (recognition). Different mechanisms, different failure consequences. |
| critical_rules > anti_patterns | Authority | Critical rule violation = system failure. Anti-pattern violation = quality degradation. Hierarchy must be inferable from output. |
| examples -> anti_patterns | Reinforcing | Good examples implicitly demonstrate anti-pattern avoidance. One-way: examples may reference anti-patterns, not vice versa. |

## Conditional Branches

| Condition | Action |
|---|---|
| `patterns` absent or empty | Omit entire section -- no header, no placeholder |
| `patterns` has 1 entry | Render as single bullet, omit preamble |
| `patterns` has 2+ entries | Render as bulleted list with optional preamble |
| Pattern lacks "-- Y" reasoning clause | Render as-is + emit validation warning at build time |
| Pattern does not start with "Do not" | Render as-is -- template does not rewrite author content |
| Pattern count >7 | Render all + emit soft validation warning suggesting review |
| Anti-patterns + constraints + critical_rules all present | Include explicit authority positioning prose |
| Anti-patterns appear without constraints or critical_rules | Omit authority positioning -- no hierarchy to differentiate |

## Open Design Questions

1. **Confrontational vs. empirical heading**: "Mistakes You Will Make" (confrontational, forces effortful processing) vs. "Known Failure Modes" (empirical, positions as observed fact). Both analyses favor departing from "Anti-Patterns" but diverge on replacement. Needs A/B testing or author preference.

2. **Preamble necessity threshold**: Is a one-line preamble needed at all when every pattern starts with "Do not"? A says the structure self-explains. B says without framing, the agent may treat the list as advisory. The cost of a one-line preamble is near zero; the cost of omitting it is uncertain.

3. **Anti-pattern ceiling**: At what count does the section become counterproductive? Both analyses agree 5 is near-optimal and >7 warrants review, but neither can define the point where ironic process effects or attention dilution outweigh additional inoculation.

4. **Anti-pattern rigidity risk**: Does extensive failure mode inoculation make agents overly cautious? Should the template include a counter-signal like "these are specific patterns to avoid, not a mandate for general caution"? Both analyses raise this but neither resolves it.

## Key Design Decisions

| Decision | Recommendation | Confidence |
|---|---|---|
| Internal pattern structure | Keep "Do not X -- Y" | HIGH |
| Reasoning clause | MANDATORY -- omission degrades effectiveness | VERY HIGH |
| Separation from constraints | MUST remain distinct sections | HIGH |
| Pattern ordering | Author-determined, preserve exactly | HIGH |
| Render all patterns | No truncation, no caps | HIGH |
| Empty section handling | Omit entirely | HIGH |
| Redundancy with instructions | Tolerate -- different mechanisms | HIGH |
| Ironic process management | Implicit through pattern structure | HIGH |
| Section heading | Depart from "Anti-Patterns"; prefer "Known Failure Modes" | MEDIUM |
| Preamble | One line max, omit for 1-2 patterns | MEDIUM |
| Authority positioning | Conditional on co-presence with constraints/critical_rules | MEDIUM |
| Scaffolding level | Light -- heading + optional one-liner + patterns | MEDIUM |
| Render order | After role and instructions | MEDIUM-HIGH |
| Pattern count guidance | Soft 3-7 recommendation in authoring guidance | MEDIUM |
