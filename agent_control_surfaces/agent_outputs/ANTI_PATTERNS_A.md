# ANALYSIS: `anti_patterns` Section

## FIRST PRINCIPLES: What Does Failure Mode Inoculation Accomplish?

Anti-patterns are not constraints restated in the negative. They operate through a fundamentally different behavioral mechanism: **recognition-triggered aversion**. When an agent reads "Do not classify importance," two things happen simultaneously: (1) the agent builds an internal representation of the mistake — it now knows what "classifying importance" looks like as a behavior, and (2) the agent associates that recognized behavior with wrongness, creating an aversion response.

This is distinct from constraints, which create **boundary awareness** (the agent knows where the edges are and stays within them), and from instructions, which create **action plans** (the agent knows what to do and does it). Anti-patterns create **failure mode recognition** — the agent can detect when it is drifting toward a known-bad behavior and correct course mid-generation.

The deeper function is **experience transfer**. Anti-patterns encode what a human operator learned from watching agents fail. They compress "I ran this agent ten times and it kept classifying importance instead of summarizing significance" into a single corrective statement. The agent receives the lesson without having failed. This is why they feel like LESSONS LEARNED more than warnings or corrections — they carry the epistemic weight of observed failure.

The "Do not X — because Y" structure is pedagogically specific. The prohibition alone ("Do not classify importance") creates a surface-level rule. The reasoning ("summarize what the exchange signifies in context, not how important it is") creates a **generative alternative**. The agent doesn't just know what NOT to do — it knows what to do INSTEAD. This transforms a pure aversion into a course correction. The dash is structurally load-bearing: it separates the recognition trigger from the redirect.

**Ironic process theory risk is real but mitigated by the redirect.** "Do not think of a white bear" primes white bears. But "Do not think of a white bear — think of its shadow on the snow instead" redirects attention. The anti-patterns in both agents follow the redirect pattern: every prohibition includes either an alternative action or an explanation that reframes the mistake. The risk would be higher with bare prohibitions ("Do not classify importance." Full stop.) The structure as observed is self-mitigating.

**Authority level sits between constraints and critical rules.** Violating a critical rule breaks the system. Violating a constraint breaks the task's contract. Following an anti-pattern degrades output quality. The consequences are real but not catastrophic — a summary that classifies importance is still a summary, just a worse one. This means the framing should convey "this will make your output worse" rather than "this will cause system failure."

---

## FIELD: `patterns`

TYPE: Array of strings
VALUES: 5 entries (agent-builder) / 5 entries (interview-enrich-create-summary)

### What the agent needs to understand

Each string in the array describes a specific failure mode the agent must recognize and avoid. The agent must understand that these are not generic advice but are informed by actual or anticipated failures specific to THIS task. The agent must parse both the prohibition (what not to do) and the correction (what to do instead or why the behavior is wrong). The agent must treat these as active behavioral constraints during generation — not background context to be acknowledged and forgotten.

### Fragments

#### Section Header

**header_label**
- Alternative A: `"## Anti-Patterns"`
- Alternative B: `"## Known Failure Modes"`
- Alternative C: `"## Mistakes to Avoid"`
- Alternative D: `"## Failure Mode Inoculation"`
- Alternative E: `"## Do Not"`
- PURPOSE: Frame the section so the agent understands the NATURE of what follows — that these are recognized failure modes, not general advice.
- HYPOTHESIS: "Anti-Patterns" is technically precise and familiar from software engineering, but may read as abstract. "Known Failure Modes" emphasizes that these are empirically grounded. "Mistakes to Avoid" is plain but might read as patronizing. "Failure Mode Inoculation" is accurate but jargon-heavy. "Do Not" is blunt and emphasizes the prohibitive nature — but every entry already starts with "Do not," making the header redundant with the content.
- STABILITY: HIGH. The label is cosmetic. The behavioral effect comes from the patterns themselves. Any reasonable header that signals "these are things to avoid" will work.

**header_preamble**
- Alternative A: (no preamble — patterns listed directly under header)
- Alternative B: `"Each pattern below describes a specific mistake. Recognize the behavior. Avoid it."`
- Alternative C: `"These failure modes have been identified for this task. When you notice yourself drifting toward any of these behaviors, correct course."`
- Alternative D: `"The following are known failure modes for agents performing this task. Each names a mistake and provides either an alternative or an explanation of why the behavior is wrong."`
- Alternative E: `"You will be tempted to do each of the following. Do not."`
- PURPOSE: Prime the agent to READ the patterns as actionable behavioral corrections rather than background context.
- HYPOTHESIS: No preamble (A) trusts the patterns to speak for themselves — this works if the "Do not X — Y" structure is self-explanatory, which it largely is. Alternative B is minimal and action-oriented. Alternative C introduces the concept of "drifting" which models the failure mode as a gradient rather than a binary — more accurate to how LLMs actually fail. Alternative D is explanatory but wordy. Alternative E is maximally direct but risks feeling adversarial.
- STABILITY: MEDIUM. The preamble's value depends on whether patterns are self-explanatory. With the current "Do not X — Y" structure, they largely are. A preamble adds value if it frames the READING MODE (these are active constraints, not background context). Diminishing returns beyond one sentence.

#### Pattern Rendering

**pattern_format**
- Alternative A: Bare list — each pattern as a bullet point, no additional formatting
  ```
  - Do not classify importance — summarize what the exchange signifies in context, not how important it is.
  ```
- Alternative B: Numbered list — implies priority ordering
  ```
  1. Do not classify importance — summarize what the exchange signifies in context, not how important it is.
  ```
- Alternative C: Bold prohibition, plain correction — visually separates the two parts
  ```
  - **Do not classify importance** — summarize what the exchange signifies in context, not how important it is.
  ```
- Alternative D: Separated structure — prohibition on one line, reasoning indented below
  ```
  - Do not classify importance.
    → Instead: summarize what the exchange signifies in context, not how important it is.
  ```
- Alternative E: Warning-style prefix
  ```
  - ⚠ Do not classify importance — summarize what the exchange signifies in context, not how important it is.
  ```
- PURPOSE: Render each pattern for maximum recognition and retention. The format should make the prohibition easy to identify and the correction easy to follow.
- HYPOTHESIS: Bare list (A) is minimal and trusts the "Do not" prefix to carry the signal — consistent with how anti-patterns are authored. Numbered list (B) implies ordering which may or may not be intentional. Bold prohibition (C) adds visual hierarchy that helps the agent parse the two-part structure. Separated structure (D) is the most explicit about the prohibition/correction split but doubles the line count. Warning prefix (E) adds visual urgency but is noisy if there are many patterns. Given that every pattern already starts with "Do not," the structure is self-parsing. Bold (C) adds marginal value. Separation (D) is overkill for patterns that are already well-structured.
- STABILITY: HIGH. The patterns are pre-authored with consistent internal structure. The rendering format is cosmetic. Bare list is the simplest correct answer.

**pattern_ordering**
- Alternative A: Preserve authored order — trust that the author ordered them intentionally
- Alternative B: Most critical first — reorder by severity of the failure mode
- Alternative C: Most common first — reorder by likelihood of the agent making this mistake
- Alternative D: Grouped by theme — cluster related anti-patterns together
- PURPOSE: Determine whether the template should reorder patterns or preserve authored order.
- HYPOTHESIS: Primacy effects are real — the first pattern in a list gets more attention than the last. However, reordering requires the template to make judgments about relative severity or frequency, which it cannot reliably do. The author who wrote the patterns knows the domain better than the template. Preserving authored order (A) is the only option that doesn't require the template to have domain knowledge it lacks. If ordering matters, the author should order them at authoring time.
- STABILITY: HIGH. This is a clear "don't touch it" decision. The template should preserve order.

#### Behavioral Framing

**framing_tone**
- Alternative A: Neutral/instructional — present patterns as facts about what to avoid
  ```
  "The following patterns degrade output quality for this task:"
  ```
- Alternative B: Experiential — present patterns as lessons from observed failures
  ```
  "Agents performing this task have consistently made these mistakes:"
  ```
- Alternative C: Predictive — present patterns as anticipated temptations
  ```
  "You will be drawn toward these behaviors. Each one degrades your output:"
  ```
- Alternative D: Contrastive — present patterns as the difference between good and bad output
  ```
  "The difference between adequate and excellent output often comes down to avoiding these specific mistakes:"
  ```
- Alternative E: Bare — no framing, just the patterns
- PURPOSE: Set the emotional/cognitive frame for how the agent processes the anti-patterns.
- HYPOTHESIS: Neutral (A) is safe but may not create sufficient aversion — it reads like documentation. Experiential (B) implies empirical grounding which strengthens the patterns' authority. Predictive (C) is the most psychologically accurate — it names the temptation, which helps the agent recognize the behavior as it emerges during generation. Contrastive (D) ties the patterns to output quality, which gives the agent a concrete reason to care. Bare (E) is the simplest and lets the patterns carry their own weight. The risk with framing is over-explaining — if the patterns are well-written (and they are), framing can feel like lecturing.
- STABILITY: MEDIUM. The framing choice affects tone but not information content. A one-line frame is probably sufficient. The patterns do most of the work.

---

## STRUCTURAL: Relationship Between Prohibition and Correction

### What the agent needs to understand

Every anti-pattern in the data follows the structure: `"Do not [MISTAKE] — [CORRECTION/REASONING]."` The dash is the structural pivot. Everything before it names a behavior to recognize. Everything after it provides the redirect — either an alternative action or an explanation of why the behavior is wrong.

This two-part structure is what makes anti-patterns effective rather than merely prohibitive. A bare "Do not classify importance" creates an aversion but leaves a vacuum — the agent knows what NOT to do but not what to do INSTEAD. The correction fills the vacuum.

### Fragments

**structural_enforcement**
- Alternative A: Template does not enforce or validate the structure — trusts the author to write well-formed anti-patterns
- Alternative B: Template validates that each pattern starts with "Do not" — rejects patterns that don't follow the convention
- Alternative C: Template validates the two-part structure (prohibition + dash + correction) — rejects patterns missing either part
- Alternative D: Template adds the "Do not" prefix if missing, normalizing all patterns to the same structure
- PURPOSE: Decide whether the template should enforce the observed structural convention.
- HYPOTHESIS: The "Do not X — Y" structure is observed in ALL 10 patterns across both agents. This consistency suggests it's either an authoring convention or a natural way to write anti-patterns. Enforcing it (B or C) adds validation overhead for a convention that authors already follow. Not enforcing it (A) risks future anti-patterns that are bare prohibitions without corrections — which reduces effectiveness. Light enforcement (B, checking for "Do not" prefix) is cheap and catches the most common deviation. Full structural validation (C) is fragile because the dash separator isn't the only valid way to join prohibition and correction. Adding prefixes (D) is invasive and might mangle intent.
- STABILITY: LOW-MEDIUM. This depends on whether anti-patterns are always authored by the same person or by varied authors. If authoring is consistent, enforcement is unnecessary. If authoring varies, light enforcement prevents drift.

---

## STRUCTURAL: Distinction from Constraints

### What the agent needs to understand

Anti-patterns and constraints are both restrictive, but they restrict through different mechanisms. Constraints say "you MUST do X" or "you MUST NOT do X" — they are rules. Anti-patterns say "you will be tempted to do X, here is why that's wrong" — they are inoculations. The distinction matters because the agent's compliance mode is different: constraints are followed by rule-adherence, anti-patterns are followed by behavior-recognition.

If the agent treats anti-patterns as just more constraints, it loses the recognition-and-redirect mechanism. If it treats constraints as just more anti-patterns, it loses the absolute-boundary mechanism. The template must render them differently enough that the agent processes them through different cognitive channels.

### Fragments

**section_separation_strategy**
- Alternative A: Anti-patterns and constraints in separate sections with different headers — structural separation signals different processing modes
- Alternative B: Anti-patterns and constraints in the same section, differentiated by formatting — saves space but risks conflation
- Alternative C: Anti-patterns in a dedicated "Failure Modes" section placed AFTER constraints — the agent reads the rules first, then learns common ways to break them
- Alternative D: Anti-patterns placed BEFORE constraints — the agent learns what to avoid first, then reads the positive rules
- PURPOSE: Ensure the agent processes anti-patterns and constraints through different behavioral channels.
- HYPOTHESIS: Separate sections (A) is the clearest signal. Same-section differentiation (B) saves tokens but risks the agent treating both as a flat rule list. Ordering matters: constraints-first (C) establishes boundaries, then anti-patterns refine behavior within those boundaries — this is logically sound (know the rules, then learn common ways to accidentally break them). Anti-patterns-first (D) primes aversions before the agent even knows the rules, which is pedagogically backwards.
- STABILITY: HIGH. Separate sections with constraints before anti-patterns is the clear structural choice. This is load-bearing for the behavioral distinction.

---

## STRUCTURAL: Distinction from Critical Rules

### What the agent needs to understand

Critical rules (from the `critical_rules` section if it exists) are inviolable system-level constraints — workspace confinement, tool usage mandates, security boundaries. Anti-patterns are domain-specific quality concerns. The consequence scale is different: violating a critical rule breaks the system or violates security; following an anti-pattern produces bad-but-functional output.

The agent must not elevate anti-patterns to critical-rule severity (which would make the agent overly cautious and rigid) or demote critical rules to anti-pattern severity (which would make the agent cavalier about system boundaries).

### Fragments

**authority_signal**
- Alternative A: No explicit authority signal — let the section placement and header convey relative importance
- Alternative B: Explicit statement: "Following these patterns degrades output quality but does not violate system constraints."
- Alternative C: Severity marker on each pattern (e.g., "quality-critical" vs "nice-to-have")
- Alternative D: Frame as "output quality" concerns vs "system integrity" concerns elsewhere
- PURPOSE: Help the agent calibrate how much weight to give anti-patterns relative to critical rules and constraints.
- HYPOTHESIS: No signal (A) is cleanest but risks the agent defaulting to equal weighting across all restrictive sections. Explicit statement (B) names the consequence tier directly, which helps calibration, but adds a sentence that might read as hedging ("it's not THAT important"). Per-pattern severity (C) is granular but overkill — anti-patterns as a class have the same consequence tier. Quality vs integrity framing (D) is the most natural distinction because it maps to how the agent already thinks about different kinds of failure. However, if anti-patterns are rendered after constraints and before critical rules, the structural placement alone may convey the hierarchy.
- STABILITY: MEDIUM. Depends on how many restrictive sections exist and whether the agent can infer the hierarchy from placement alone. If there are only 2-3 restrictive sections, placement is sufficient. If there are 5+, an explicit authority signal helps.

---

## STRUCTURAL: Count Variability

### What the agent needs to understand

Both agents happen to have 5 anti-patterns, but nothing in the structure mandates a specific count. The template must handle 1 anti-pattern, 5, 10, or 0 (section absent).

### Fragments

**empty_handling**
- Alternative A: If no anti-patterns are defined, omit the section entirely — no empty section, no placeholder
- Alternative B: If no anti-patterns are defined, include a note: "No known failure modes have been identified for this task."
- Alternative C: If no anti-patterns are defined, include a minimal warning: "Exercise standard judgment — no task-specific failure modes have been cataloged."
- PURPOSE: Handle the case where an agent definition has no anti-patterns.
- HYPOTHESIS: Omission (A) is cleanest — an absent section is simpler than an empty section with a note. Note (B) is informative but adds a line that carries no behavioral value. Warning (C) is worse — it creates anxiety about unknown failure modes, which is counterproductive. The section should exist when it has content and not exist when it doesn't.
- STABILITY: HIGH. Omit when empty. This is consistent with how other optional sections should work.

**scaling_behavior**
- Alternative A: Render all patterns regardless of count — no compression, no summarization
- Alternative B: If pattern count exceeds a threshold (e.g., 10), group by theme with sub-headers
- Alternative C: Cap at a maximum count and note that additional patterns were truncated
- PURPOSE: Handle cases where the anti-pattern list grows large.
- HYPOTHESIS: The current data shows 5 patterns per agent, which is manageable. Render-all (A) is correct for reasonable counts (1-10). Grouping (B) adds structure that may help with large counts but requires theme detection the template can't reliably do. Capping (C) discards author-provided information, which is unacceptable — if the author wrote 15 anti-patterns, they had 15 failure modes to communicate. Render all, no exceptions.
- STABILITY: HIGH. Render all patterns. If the list becomes unwieldy, that's an authoring problem, not a template problem.

---

## STRUCTURAL: Relationship to Instructions

### What the agent needs to understand

Anti-patterns and instructions are complementary but work through opposite mechanisms. Instructions say "do this." Anti-patterns say "don't do this." Together, they create a behavioral corridor: instructions define the path, anti-patterns mark the ditches on either side.

The risk is redundancy — an instruction "summarize significance, not importance" and an anti-pattern "do not classify importance" say overlapping things. The instruction creates action. The anti-pattern creates recognition. Both are useful, but the agent shouldn't feel like it's reading the same thing twice.

### Fragments

**redundancy_stance**
- Alternative A: Tolerate redundancy — the behavioral mechanisms are different even when the content overlaps
- Alternative B: Deduplicate — if an instruction already covers a behavior, omit the corresponding anti-pattern
- Alternative C: Cross-reference — note when an anti-pattern reinforces an instruction
- PURPOSE: Handle the potential overlap between instructions and anti-patterns.
- HYPOTHESIS: Tolerate redundancy (A) is the safest choice. The instruction "summarize significance" and the anti-pattern "do not classify importance" operate through different channels even though they point at the same behavior. The instruction creates a positive drive. The anti-pattern creates recognition of a failure mode. An agent that has BOTH is better calibrated than one with either alone. Deduplication (B) removes safety-net redundancy. Cross-referencing (C) adds cognitive overhead without behavioral benefit.
- STABILITY: HIGH. Redundancy between instructions and anti-patterns is a feature, not a bug. Different mechanisms, same goal.

---

## CROSS-SECTION DEPENDENCIES

| Dependency | Nature | Implication |
|---|---|---|
| anti_patterns ← instructions | Complementary | Anti-patterns mark failure modes; instructions mark the correct path. Both needed for full behavioral corridor. |
| anti_patterns ← constraints | Distinct mechanism | Constraints set boundaries (MUST/MUST NOT). Anti-patterns set aversions (recognize and avoid). Must be rendered as separate sections. |
| anti_patterns ← critical_rules | Severity hierarchy | Critical rules > constraints > anti-patterns in authority. Anti-pattern violation degrades quality; critical rule violation breaks system. |
| anti_patterns ← examples | Reinforcing | Good examples demonstrate anti-pattern avoidance implicitly. Bad examples (if they existed) would show anti-patterns in action. |
| anti_patterns ← role | Scoping | The role determines what domain the anti-patterns apply to. Builder anti-patterns make no sense for a summarizer. |

---

## CONDITIONAL BRANCHES

| Condition | Branch | Effect |
|---|---|---|
| `anti_patterns.patterns` is empty or absent | Omit section entirely | No header, no placeholder, no note |
| `anti_patterns.patterns` has 1 entry | Render as single bullet | No list framing needed |
| `anti_patterns.patterns` has 2+ entries | Render as bulleted list | Standard rendering |
| All patterns follow "Do not X — Y" structure | No special handling | Current data is consistent |
| A pattern lacks the correction/reasoning after the dash | Still render as-is | Template does not rewrite author content; authoring guidance may flag this |
| A pattern does not start with "Do not" | Still render as-is | Light validation could warn, but template should not reject |

---

## OPEN QUESTIONS

1. **Ironic process mitigation at scale:** With 5 anti-patterns, the priming risk is low — the corrections redirect effectively. At 15+ anti-patterns, the agent is spending significant cognitive budget on behaviors-to-avoid, which could create a net-negative attention allocation. Is there a practical ceiling on anti-pattern count?

2. **Anti-pattern as implicit instruction:** "Do not classify importance — summarize what the exchange signifies in context" is functionally an instruction disguised as a prohibition. Should the template recognize this duality, or is the negative framing itself the point (recognition-triggered aversion vs. action-triggered execution)?

3. **Ordering authority:** Who decides the order of anti-patterns — the author or the template? Current analysis says the template should preserve authored order. But should authoring guidance recommend ordering by severity or frequency?

4. **Anti-patterns for anti-patterns:** The meta-risk is that an agent becomes so focused on avoiding named failure modes that it becomes rigid and overly cautious. Should the template include a counter-instruction like "these are specific patterns to avoid, not a mandate for general caution"?
