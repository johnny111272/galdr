# ANTI_PATTERNS — Control Surface Analysis (B)

## FIRST PRINCIPLES: What does this section accomplish behaviorally?

Anti-patterns are **failure mode inoculation**. They do not set boundaries (that is what constraints do). They do not declare inviolable rules (that is what critical_rules does). Anti-patterns describe **specific mistakes the agent is likely to make** and pair each with reasoning that explains why it is a mistake.

The behavioral mechanism is fundamentally different from constraints. A constraint says "stay inside this line." An anti-pattern says "you will be tempted to do X — here is why X is wrong." Constraints create walls. Anti-patterns create aversions. The distinction matters because aversions require the agent to *recognize* a failure mode in its own reasoning, not just comply with an external rule.

This is closer to clinical inoculation than to rule-setting. You expose the agent to a weakened form of the mistake (the description) paired with the antidote (the reasoning), so that when the agent encounters the live pathogen during execution, it has antibodies.

**The critical tension:** Ironic process theory suggests that naming a mistake can prime it. "Do not think of a white bear" activates the very representation it forbids. Anti-patterns must navigate this — they need to activate the failure mode representation strongly enough to build recognition, but frame it so the aversion dominates the activation. The "because Y" clause is the mechanism that tips the balance: the reasoning gives the agent somewhere to GO after recognizing the pattern, rather than leaving it stuck with an activated-but-forbidden representation.

---

## FIELD: `patterns`
TYPE: Array of strings (flat, unkeyed, ordered)

### What the agent needs to understand

Each string is a self-contained failure mode description. The agent must:
1. Recognize the described behavior as something it would naturally do
2. Understand WHY the behavior is wrong in context
3. Develop an aversion strong enough to override default tendencies

The patterns are deeply domain-specific. Builder anti-patterns address definition-authoring mistakes (verbosity, elaboration, scope creep). Summarizer anti-patterns address judgment mistakes (classification, interpretation bias, context neglect). These are not generic "be careful" warnings — they are precision-targeted corrections for observed or anticipated failure modes specific to that agent's task.

### Fragments

**Section heading / framing label**
- Alternative A: `## Anti-Patterns` — neutral label, no additional framing
- Alternative B: `## Known Failure Modes` — reframes as empirical observations rather than prohibitions
- Alternative C: `## Mistakes You Will Make` — confrontational, directly addresses the agent as the likely source
- Alternative D: `## Corrections From Prior Failures` — implies learning from experience, positions as lessons learned
- Alternative E: `## Quality Degradation Patterns` — clinical, positions patterns as quality threats
- PURPOSE: The heading frames how the agent interprets the list. "Anti-patterns" is the software engineering term — familiar but slightly abstract. "Known Failure Modes" positions the patterns as empirical facts about LLM behavior, which may increase respect for them. "Mistakes You Will Make" is maximally confrontational — it presupposes failure and demands vigilance. "Corrections From Prior Failures" implies these were discovered through actual failure, adding weight. "Quality Degradation Patterns" is clinical and may reduce emotional salience.
- HYPOTHESIS: "Known Failure Modes" or "Mistakes You Will Make" will produce stronger aversions than "Anti-Patterns" because they make the agent's own liability explicit. "Anti-Patterns" is too much of a software engineering cliche — it has been diluted through overuse. The confrontational framing ("you WILL make these mistakes") may be most effective because it forces the agent to prove otherwise, activating effortful processing rather than passive acknowledgment. However, it risks adversarial framing that could reduce cooperation. "Corrections From Prior Failures" balances authority with approachability.
- STABILITY: MEDIUM — the framing label sets the interpretive context for everything below it, but the individual patterns do most of the heavy lifting. A bad heading can undermine good patterns; a good heading cannot rescue bad patterns.

**Preamble / introductory prose**
- Alternative A: No preamble — patterns speak for themselves
- Alternative B: "These are specific mistakes this task type triggers in LLMs. Each one has been observed or is highly probable given your training distribution."
- Alternative C: "Read each pattern. Recognize why you are susceptible. The reasoning after the dash is the correction — internalize it."
- Alternative D: "These failures are not hypothetical. They emerge naturally from how you process instructions. Recognizing them before they happen is the purpose of this section."
- Alternative E: "WARNING: Your default processing will produce these exact failures unless you actively guard against them. Each pattern names the failure and explains why your default is wrong."
- PURPOSE: A preamble can prime the agent to take the list seriously before it reads the first pattern. Without a preamble, the agent encounters the patterns cold and must self-contextualize. With a preamble, the agent enters the list with a specific interpretive stance.
- HYPOTHESIS: A brief, sharp preamble (B or D) is likely optimal. No preamble risks the agent treating the list as advisory rather than critical. An overly long preamble dilutes urgency. The preamble should accomplish exactly one thing: signal that these are not suggestions but descriptions of failures the agent is specifically prone to. Alternative E's "WARNING" framing may be too alarming and trigger defensive processing. Alternative C's imperative "Read each pattern" is unusual — it directs the agent's reading process itself, which may increase engagement or may feel patronizing.
- STABILITY: LOW-MEDIUM — the preamble is a one-shot framing device. Once the agent is reading the patterns, the preamble's influence decays rapidly. Its value is concentrated entirely in the first few milliseconds of pattern processing.

**Individual pattern structure: "Do not X — Y"**
- Alternative A: `"Do not X — Y"` — current structure, prohibition + reasoning joined by dash
- Alternative B: `"WRONG: X. CORRECT: Y."` — explicit wrong/right pairing
- Alternative C: `"When you encounter [situation], you will default to [mistake]. Instead: [correction]."` — narrative structure with trigger-default-correction
- Alternative D: `"X is a failure. Y."` — declarative statement of failure without prohibition framing
- Alternative E: `"Avoid X because Y"` — softer prohibition, same structure
- PURPOSE: The internal structure of each pattern determines how the agent processes and stores the aversion. "Do not" is a direct prohibition — it activates the forbidden representation and immediately negates it. The trigger-default-correction structure (C) is more complex but may build stronger recognition because it describes the MECHANISM of failure, not just the outcome. The wrong/right pairing (B) is maximally explicit but mechanical.
- HYPOTHESIS: The current "Do not X — Y" structure is surprisingly effective despite its simplicity. The dash creates a natural pause that separates the prohibition from the reasoning, and the reasoning provides the constructive alternative that prevents ironic process effects. Alternative C (trigger-default-correction) may be more effective for complex failure modes where the agent needs to recognize a SITUATION, not just a behavior — but it is significantly more verbose and would inflate the section. Alternative B is too mechanical and may trigger pattern-matching rather than understanding. The "Do not" opening is powerful because it is unambiguous — there is no way to interpret "Do not classify importance" as anything other than a prohibition. Softer framings (E) sacrifice this clarity.
- STABILITY: HIGH — this is the load-bearing structure. Every pattern's effectiveness depends on this internal format. Changing the structure changes how every pattern is processed. The "Do not X — Y" format has a strong track record in the raw data; both agents use it consistently, suggesting it was deliberately chosen.

**Reasoning clause (the part after the dash)**
- Alternative A: Present reasoning inline after dash (current approach) — `"Do not X — because Y"`
- Alternative B: Omit reasoning, bare prohibition only — `"Do not X."`
- Alternative C: Separate reasoning into a companion field — `{ pattern = "Do not X", rationale = "Y" }`
- Alternative D: Reasoning as a conditional — `"Do not X — if you do, the result will be Z"`
- Alternative E: Reasoning as positive reframe — `"Do not X — instead, do Y"`
- PURPOSE: The reasoning clause is the antidote that prevents ironic process priming. Without it, "Do not classify importance" leaves the agent with an activated representation of importance-classification and no constructive alternative. With it, "summarize what the exchange signifies in context, not how important it is" redirects the activated representation toward the correct behavior.
- HYPOTHESIS: The inline reasoning (A) is essential — removing it (B) would significantly degrade anti-pattern effectiveness and likely trigger the ironic process problem. Separating it into a companion field (C) creates a formal structure that might encourage more careful reasoning authoring, but adds structural complexity. The current inline approach keeps the prohibition and its antidote in a single cognitive unit, which is almost certainly more effective than separation. Alternative D (consequence-based) may work for some patterns but not others — not all failures have easily described consequences. Alternative E (positive reframe) is the most constructive but may weaken the prohibition aspect — the agent needs to feel the "do not" before it receives the "instead."
- STABILITY: VERY HIGH — the reasoning clause is what differentiates anti-patterns from bare rules. Without reasoning, anti-patterns collapse into constraints. The reasoning is the core mechanism that makes failure mode inoculation work.

---

## STRUCTURAL: List format and ordering

### What the agent needs to understand

The patterns are currently a flat ordered array. This raises several structural questions about format, ordering, and count.

### Fragments

**Numbered vs bulleted vs bare array**
- Alternative A: Bare TOML array (current) — `patterns = [...]`
- Alternative B: Numbered in rendered output — `1. Do not...  2. Do not...`
- Alternative C: Bulleted in rendered output — `- Do not...  - Do not...`
- Alternative D: Keyed/named patterns — `{ name = "verbosity_trap", pattern = "Do not..." }`
- PURPOSE: Format affects perceived authority and distinctness of each pattern. Numbered lists imply priority ordering and discrete importance. Bulleted lists imply equal weight and unordered collection. Bare arrays delegate formatting to the rendering layer.
- HYPOTHESIS: Numbering may inadvertently create a priority hierarchy where earlier patterns are weighted more heavily — which could be desirable if patterns ARE priority-ordered, or harmful if they are not. Bullets signal equal weight, which is more honest for most anti-pattern sets. Keyed/named patterns (D) would enable referencing specific anti-patterns from other sections ("see anti-pattern: verbosity_trap") but add significant structural complexity. The bare array is the correct storage format; the rendering decision should be made at render time based on whether the agent definition author has indicated priority ordering.
- STABILITY: LOW-MEDIUM — format is a presentation concern. The patterns themselves do the work; format provides mild weighting effects at best.

**Ordering effects**
- Alternative A: Author-determined order, no explicit ordering signal — first pattern is most important by convention
- Alternative B: Explicit priority field — `{ priority = 1, pattern = "Do not..." }`
- Alternative C: Random/shuffled at render time to eliminate primacy bias
- Alternative D: Alphabetical or structural ordering to signal NO priority hierarchy
- PURPOSE: Primacy and recency effects are real in language model processing. The first pattern in the list will receive disproportionate attention. The last pattern may receive slightly elevated attention due to recency. Middle patterns are at highest risk of being treated as "filler."
- HYPOTHESIS: Author-determined order (A) is the pragmatic choice — the definition author knows which failure modes are most critical and should place them first. Making this convention explicit ("patterns are listed in priority order; the first pattern addresses the most likely or most damaging failure mode") would strengthen the signal. Shuffling (C) is theoretically interesting for eliminating bias but practically harmful because it prevents the author from using position strategically. Priority fields (B) add complexity for marginal benefit — position already encodes priority if the convention is stated.
- STABILITY: MEDIUM — ordering affects attention distribution, which directly affects which patterns the agent internalizes most strongly. For a 5-pattern list this effect is moderate; for a 10+ pattern list it could be significant.

**Count / dilution effects**
- Alternative A: No count limit — author discretion
- Alternative B: Soft guidance — "3-7 patterns recommended"
- Alternative C: Hard limit — maximum 7 patterns
- Alternative D: Tiered — "critical" (max 3) and "additional" (unlimited) sub-arrays
- PURPOSE: Each additional pattern dilutes the attention given to all other patterns. A single anti-pattern receives 100% of the attention budget. Five patterns share it. Ten patterns may individually receive too little attention to build effective aversions.
- HYPOTHESIS: The current 5-pattern count in both agents feels close to optimal. Enough to cover the major failure modes, few enough that each receives meaningful attention. A soft guidance of 3-7 (B) is the right approach — hard limits are too rigid for a section that is inherently domain-specific. The tiered approach (D) is interesting but may be over-engineering — if a pattern is not critical enough to be in the main list, it may not be critical enough to include at all. Anti-patterns should be the author's strongest failure mode convictions, not an exhaustive catalog.
- STABILITY: MEDIUM-HIGH — count directly affects per-pattern effectiveness. Too many patterns and the section becomes a wall of "do nots" that the agent skims rather than internalizes. This is a structural property that affects all patterns equally.

---

## STRUCTURAL: Relationship to constraints and critical_rules

### What the agent needs to understand

Anti-patterns occupy a specific niche in the authority hierarchy. They are not constraints (boundary conditions on behavior) and they are not critical rules (inviolable system-level rules). They are domain-specific quality aversions.

### Fragments

**Authority positioning prose**
- Alternative A: No explicit authority positioning — let the section heading and content speak
- Alternative B: "These patterns describe quality failures, not rule violations. Violating an anti-pattern degrades output quality; violating a critical rule is a system failure."
- Alternative C: "Anti-patterns are not rules. They are descriptions of how you will fail at this specific task. Critical rules protect the system. Constraints bound your behavior. Anti-patterns guard your judgment."
- Alternative D: "These sit below critical_rules in authority but above general instruction text. They are mandatory aversions, not suggestions."
- PURPOSE: The agent needs to understand where anti-patterns sit relative to other behavioral controls. If anti-patterns are perceived as equivalent to critical_rules, the agent may treat them as inviolable absolutes rather than quality-preserving aversions. If perceived as equivalent to general instructions, they may be treated as suggestions.
- HYPOTHESIS: Explicit positioning (C or D) is valuable because the authority hierarchy is non-obvious. An agent encountering anti-patterns, constraints, and critical_rules in the same definition needs to understand that these operate through different mechanisms and at different authority levels. Alternative C's framing ("guard your judgment") is the most accurate description of what anti-patterns do — they are not about compliance, they are about judgment quality. This framing should appear somewhere in the rendered output, either as prose or as part of the section heading context.
- STABILITY: MEDIUM — authority positioning affects how the agent weighs anti-pattern violations against other pressures. If the agent must choose between violating an anti-pattern and violating a constraint, the relative authority determines the outcome.

**Boundary with constraints**
- Alternative A: No explicit boundary — the content is different enough to self-differentiate
- Alternative B: Render anti-patterns in a separate section from constraints with distinct headings
- Alternative C: Add a brief bridging note — "Constraints bound WHAT you do. Anti-patterns correct HOW you do it."
- Alternative D: Merge anti-patterns into constraints as a sub-section
- PURPOSE: Constraints and anti-patterns can blur. "Do not classify importance" could be framed as a constraint. "MUST process entries in sequence" could be framed as an anti-pattern for parallel processing. The distinction is behavioral mechanism, not content.
- HYPOTHESIS: Anti-patterns MUST remain separate from constraints. Merging them (D) would destroy the distinct behavioral mechanism. A constraint is a wall — it blocks. An anti-pattern is a vaccination — it builds recognition and aversion. The content format is different ("MUST X" vs "Do not X — because Y"), the processing mechanism is different (compliance vs recognition), and the failure mode is different (boundary violation vs quality degradation). Brief bridging prose (C) is the right approach — acknowledge the potential confusion and resolve it with a single clear distinction.
- STABILITY: HIGH — the separation between anti-patterns and constraints is a structural invariant. Collapsing them would fundamentally change how both sections function.

---

## STRUCTURAL: Ironic process management

### What the agent needs to understand

Anti-patterns name specific mistakes. Naming a mistake activates the representation of that mistake in the agent's processing. This is the fundamental tension of failure mode inoculation: you must activate the failure mode to build an aversion to it, but activation itself increases the probability of the failure mode occurring.

### Fragments

**Inoculation framing**
- Alternative A: No explicit management — trust the "Do not X — Y" structure to handle it implicitly
- Alternative B: "Each pattern names a failure you must recognize. The reasoning after the dash is the correction. Focus on the correction, not the failure."
- Alternative C: "After reading each pattern, the correct behavior is described after the dash. That is what you should internalize."
- Alternative D: "These patterns activate failure representations deliberately. The reasoning clause redirects the activation toward correct behavior. This is the intended mechanism."
- PURPOSE: Ironic process theory is well-documented in human cognition and has analogs in LLM processing. The question is whether explicit management of this effect improves outcomes or adds unnecessary meta-complexity.
- HYPOTHESIS: The "Do not X — Y" structure already handles ironic process effects implicitly through the reasoning clause. Making this mechanism explicit (D) is interesting from a transparency perspective but may be over-engineering — the agent does not need to understand WHY the structure works, it just needs to process it effectively. Alternative B or C might help by directing attention toward the correction rather than the prohibition, but they add processing overhead for what may be a marginal improvement. The implicit handling (A) is likely sufficient for most agents. If ironic process effects are observed (i.e., an agent makes the exact mistake described in an anti-pattern), the fix is to improve the reasoning clause for that specific pattern, not to add global meta-framing.
- STABILITY: LOW — this is a theoretical concern with real but hard-to-measure effects. The implicit handling through pattern structure is the pragmatic choice.

---

## STRUCTURAL: Pre-authored text policy

### What the agent needs to understand

The raw data contains only the patterns themselves — no framing prose, no preamble, no authority positioning. The question is how much scaffolding the rendering layer should add around author-written patterns.

### Fragments

**Scaffolding approach**
- Alternative A: Minimal scaffolding — section heading + patterns, nothing else
- Alternative B: Light scaffolding — section heading + one-line purpose statement + patterns
- Alternative C: Full scaffolding — section heading + purpose statement + authority positioning + ironic process note + patterns
- Alternative D: Conditional scaffolding — add framing only when pattern count exceeds a threshold (e.g., >5 patterns get a preamble)
- PURPOSE: Scaffolding prose competes with patterns for attention. Too much scaffolding and the patterns themselves receive less attention. Too little and the agent may misinterpret the section's purpose.
- HYPOTHESIS: Light scaffolding (B) is optimal. A single line establishing that these are failure modes the agent is specifically prone to, followed by the patterns themselves. The patterns are the payload — everything else is packaging. The definition author wrote specific, carefully reasoned anti-patterns; the rendering layer should not bury them under generic framing prose. Alternative D (conditional scaffolding) is over-engineered for a section that typically contains 3-7 items.
- STABILITY: MEDIUM — scaffolding affects how much attention reaches the actual patterns. Getting this wrong in either direction (too much or too little) degrades anti-pattern effectiveness.

---

## CROSS-SECTION DEPENDENCIES

1. **anti_patterns <-> constraints**: Must be rendered as distinct sections with different behavioral mechanisms. If rendered adjacently, bridging prose should differentiate them. Anti-patterns should NOT be merged into constraints even when the content appears similar.

2. **anti_patterns <-> critical_rules**: Anti-patterns sit below critical_rules in authority. A critical_rules violation is a system failure; an anti-pattern violation is a quality degradation. This hierarchy should be inferable from the rendered output, either through section ordering (critical_rules first) or explicit authority language.

3. **anti_patterns <-> instructions**: Anti-patterns may reference concepts introduced in instructions. An anti-pattern like "Do not create instruction steps for operations handled by software tools" assumes the agent knows what "software tools" handle. This creates a soft dependency: anti-patterns should be rendered AFTER instructions so the agent has context for what the anti-patterns are correcting.

4. **anti_patterns <-> examples**: Examples can demonstrate what anti-pattern violations look like. If examples exist that show "wrong" vs "right" output, they reinforce anti-pattern aversions through demonstration rather than description. This is a one-way dependency: examples may reference anti-patterns, but anti-patterns should not reference examples.

5. **anti_patterns <-> role/identity**: The effectiveness of anti-patterns depends on the agent understanding its task deeply enough to recognize WHY these specific failures are relevant. An agent that does not understand its role cannot contextualize domain-specific anti-patterns. This creates a hard dependency: role/identity must be established before anti-patterns are processed.

---

## CONDITIONAL BRANCHES

1. **Zero anti-patterns**: If `patterns = []` or the section is absent, no anti-pattern section should be rendered. Unlike critical_rules (where absence may indicate an oversight), absent anti-patterns simply mean the definition author has not identified specific failure modes. This is not necessarily an error — some tasks may not have predictable failure modes worth inoculating against.

2. **High pattern count (>7)**: If the author provides many anti-patterns, the rendering layer should consider whether all of them are truly anti-patterns or whether some are better classified as constraints. A long anti-pattern list may indicate section misuse. Soft warning during definition validation, not a hard error.

3. **Patterns without reasoning clauses**: If a pattern is just "Do not X" without a "— Y" reasoning clause, it is structurally incomplete. The reasoning clause is the mechanism that prevents ironic process effects. A bare prohibition without reasoning should trigger a validation warning: "Anti-pattern lacks reasoning clause; consider adding explanation after a dash."

4. **Overlap with constraints**: If a pattern closely mirrors a constraint (e.g., anti-pattern "Do not process out of order" + constraint "MUST process in order"), the rendering layer should flag potential redundancy. Redundancy is not always bad — the same rule expressed as both a wall and an aversion may be more effective — but unintentional redundancy suggests section confusion.

---

## SUMMARY OF KEY DESIGN DECISIONS

| Decision | Recommendation | Confidence |
|----------|---------------|------------|
| Internal pattern structure | Keep "Do not X — Y" format | HIGH |
| Reasoning clause | MANDATORY — omission degrades effectiveness | VERY HIGH |
| Separation from constraints | MUST remain separate sections | HIGH |
| Section heading | "Known Failure Modes" or "Mistakes You Will Make" over "Anti-Patterns" | MEDIUM |
| Preamble | One line establishing failure-mode context | MEDIUM |
| Authority positioning | Below critical_rules, above general instructions | MEDIUM-HIGH |
| Pattern count guidance | Soft recommendation of 3-7 | MEDIUM |
| Ordering convention | Author-determined, first = most critical | MEDIUM |
| Ironic process management | Implicit through pattern structure, not explicit meta-framing | MEDIUM |
| Scaffolding level | Light — heading + one-line purpose + patterns | MEDIUM |
| Render order dependency | After role/identity and instructions, before or alongside constraints | MEDIUM-HIGH |
