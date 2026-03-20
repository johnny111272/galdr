# CONSTRAINTS Section — Control Surface Analysis (B)

## First Principles: What Constraints Accomplish

Constraints are the **operational boundary layer** between what the agent is told to do (instructions) and what the agent must never do (anti-patterns). They define the rules of engagement — the conditions under which the agent's work is considered compliant. They are not workflow steps. They are not catastrophic failure modes. They are the sustained behavioral expectations that hold across every action the agent takes during execution.

Instructions say "do this, then this, then this." Anti-patterns say "this specific thing is always wrong." Constraints say "while you are working, these rules are always in force." They are the **ambient law** of the agent's operating environment — not sequenced, not exemplified, just enforced.

The critical distinction from critical_rules: critical rules are **termination triggers** — violations that invalidate the entire output. Constraints are **compliance standards** — violations that degrade quality, introduce drift, or produce non-conformant output, but the output itself may still exist. An agent that violates a critical rule has failed categorically. An agent that violates a constraint has failed partially — the output is defective but not necessarily void.

This creates a three-tier compliance model:
- **critical_rules**: Violation = output rejected. Binary pass/fail.
- **constraints**: Violation = output defective. Graded compliance.
- **anti_patterns**: Violation = output contaminated. Quality degradation with recognizable signatures.

Constraints occupy the middle tier: they are stricter than anti-patterns (which describe tendencies to avoid) but less absolute than critical rules (which describe hard termination conditions). An agent should treat constraints as **rules it will be audited against** — not suggestions, not aspirations, but accountable standards.

---

## DATA SHAPE ANALYSIS

### Raw Structure

Both agents use identical structure:

```toml
[constraints]
rules = [ "string", "string", ... ]
```

A single key (`rules`) containing a flat array of strings. No nesting. No metadata. No typing. No grouping. The structure is maximally simple.

### Rule Taxonomy (Emergent, Not Declared)

Despite the flat structure, rules fall into distinct categories when read:

**Agent 1 (builder) rule types:**
| Rule | Emergent Type |
|------|---------------|
| "Use ONLY field names from agent-template.toml..." | Namespace constraint (positive mandate) |
| "Validate ALL 18 conditional field rules..." | Completeness requirement |
| "Produce a COMPLETE definition or ABORT..." | Output integrity requirement |
| "Write instruction text as dull facts..." | Style/voice directive |
| "Apply minimum required permissions..." | Principle of least privilege |
| "Do not write tool invocation syntax..." | Content prohibition |
| "Do not write batch discipline rules..." | Content prohibition |
| "Do not write security boundary descriptions..." | Content prohibition |
| "Do not add capabilities_requested unless..." | Conditional field rule |
| "Ground examples in actual data shapes..." | Data sourcing requirement |

**Agent 2 (summary) rule types:**
| Rule | Emergent Type |
|------|---------------|
| "MUST process exchanges in order..." | Ordering mandate |
| "MUST produce exactly one sentence..." | Output cardinality |
| "MUST produce exactly as many output records..." | Input-output parity |
| "MUST NOT reference or load..." | Scope prohibition |
| "MUST NOT load truth system..." | Isolation prohibition |
| "MUST NOT output any source quality markers..." | Content prohibition |
| "MUST use hedging language..." | Style/voice directive |

The taxonomy is emergent — the author naturally writes rules that fall into categories, but the data structure does not declare or enforce these categories.

---

## FIELD: rules

TYPE: Array of strings
VALUES: 10 rules (agent-builder) / 7 rules (interview-enrich-create-summary)

### What the agent needs to understand

The agent must understand that every string in this array is an **active rule** that applies to all of its work, not just specific steps. Rules are not prioritized within the list — they are all simultaneously in force. The agent cannot selectively comply. It must hold all constraints in working memory across all phases of execution.

The agent also needs to understand that these rules are **testable** — an auditor (human or automated) could examine the agent's output and determine whether each rule was followed. This is what separates constraints from general guidance. "Try to be concise" is guidance. "MUST produce exactly one sentence per exchange" is a constraint.

### Fragments

#### STRUCTURAL: Section Preamble

The preamble establishes what constraints ARE in the agent's compliance model. This is where the authority level is set — the agent's interpretation of every rule that follows depends on how the preamble frames the section.

**Preamble-Authority-Strict**
- Alternative A: "The following rules are binding for all work in this session. Every rule applies simultaneously — none override or qualify others. Violating any rule makes the affected output non-compliant."
- Alternative B: "These constraints govern your execution. They are not sequenced — all are in force at all times. Each rule is independently auditable: your output must satisfy every one."
- Alternative C: "Operational constraints — active for the duration of this task. These are not guidelines. Each is a compliance standard your output will be measured against."
- PURPOSE: Establish that constraints are accountable rules, not soft guidance. The agent must treat them as audit criteria.
- HYPOTHESIS: Without explicit authority framing, LLMs tend to treat list items as suggestions with decreasing weight toward the end of the list. The preamble counteracts positional decay by establishing uniform authority up front.
- STABILITY: HIGH — the authority level of constraints relative to other sections is a fundamental design decision. Once set, it should not change per-agent.

**Preamble-Authority-Ambient**
- Alternative A: "While executing your instructions, these rules remain in effect:"
- Alternative B: "The following rules apply throughout your work — not at specific steps, but as continuous conditions:"
- Alternative C: "Maintain these standards across all phases of execution:"
- PURPOSE: Frame constraints as ambient rather than sequential — they don't belong to a step, they belong to the entire session.
- HYPOTHESIS: The "ambient" framing helps the agent distinguish constraints from instructions. Instructions are consumed step-by-step. Constraints persist. This distinction matters for how the agent allocates attention during multi-step work.
- STABILITY: HIGH — the ambient nature of constraints is structural, not stylistic.

**Preamble-Completeness**
- Alternative A: "This is the complete set of operational rules. No additional constraints apply beyond these and the critical rules above."
- Alternative B: "These {N} rules are exhaustive — do not infer additional constraints not listed here."
- Alternative C: (Omit completeness framing entirely — let the list speak for itself.)
- PURPOSE: Prevent the agent from hallucinating additional constraints based on training data or inferred "best practices."
- HYPOTHESIS: LLMs frequently self-impose constraints not present in the prompt ("I should also make sure to..." syndrome). Explicit completeness framing may reduce this. But it may also create a loophole mentality ("if it's not listed, it's allowed"). The tradeoff is real.
- STABILITY: MEDIUM — depends on observed agent behavior. If agents consistently self-impose phantom constraints, add completeness framing. If they demonstrate loophole exploitation, remove it.

---

#### STRUCTURAL: Rule Formatting

How individual rules are presented within the list. This affects perceived authority, scannability, and compliance weight.

**Format-Numbered**
- Alternative A: Number every rule (1. 2. 3. ...) to imply completeness and enable reference ("violated rule 4").
- Alternative B: Number rules but group by emergent type with sub-numbering (1a, 1b, 2a...).
- Alternative C: Number rules with explicit count header: "7 constraints follow:" then numbered list.
- PURPOSE: Numbering creates referenceability and implies that each rule is a discrete, countable obligation.
- HYPOTHESIS: Numbered rules carry more compliance weight than bulleted rules in LLM responses. Numbering also enables structured audit reporting ("constraint 3 violated"). The count header variant adds an implicit completeness check — the agent can verify it processed all N.
- STABILITY: MEDIUM — numbering vs bullets is a presentation choice that may interact with rule count. Short lists (3-5) work fine either way. Longer lists (8+) benefit from numbering.

**Format-Bulleted**
- Alternative A: Simple bullet points, preserving the authored order as-is.
- Alternative B: Bullet points with MUST/MUST NOT prefix standardization (regardless of author voice).
- Alternative C: Bullet points with bold lead phrases extracted from each rule ("**Namespace compliance**: Use ONLY field names from...").
- PURPOSE: Bullets are lighter than numbers — they suggest "all of these" rather than "these in order." Bold leads add scannability at the cost of injecting structure the author didn't write.
- HYPOTHESIS: For constraint sections specifically, bullets may be preferable to numbers because constraints have no inherent ordering. Numbers imply sequence; bullets imply set membership. However, bold leads risk the template editorializing the author's rules.
- STABILITY: LOW — this is a formatting preference that should be tested empirically.

**Format-Prose-Block**
- Alternative A: Render rules as a dense paragraph with semicolons: "Use ONLY field names from template; validate ALL conditional rules; produce COMPLETE output or ABORT; ..."
- Alternative B: Render as a continuous block but with sentence breaks and no list formatting.
- Alternative C: (Rejected — prose blocks reduce scannability and compliance tracking. Included for completeness.)
- PURPOSE: Test whether dense prose increases "read all at once" comprehension or decreases per-rule salience.
- HYPOTHESIS: Prose blocks almost certainly reduce compliance. Individual rules need visual separation to function as independent audit criteria. This format is likely anti-productive.
- STABILITY: LOW — likely eliminated early in testing.

---

#### STRUCTURAL: Rule Voice Normalization

The raw data shows two voice patterns: Agent 1 uses mixed voice (some positive, some negative, some imperative, some declarative). Agent 2 uses explicit MUST/MUST NOT markers consistently. Should the template normalize voice?

**Voice-Preserve-Authored**
- Alternative A: Render each rule exactly as authored — no normalization, no rewriting.
- Alternative B: Render as authored but add a framing note: "Rules are written by the agent author and may use varied phrasing. All carry equal weight."
- Alternative C: Render as authored but visually distinguish positive mandates from prohibitions (e.g., different prefix markers).
- PURPOSE: Preserve the author's intent and voice. The author chose specific phrasing for reasons the template shouldn't override.
- HYPOTHESIS: Author voice preservation avoids the template layer introducing subtle meaning changes. "Do not write tool invocation syntax" and "MUST NOT write tool invocation syntax" are semantically identical but the MUST NOT version adds emphasis the author may not have intended at that level. Normalization risks over-weighting or under-weighting rules relative to author intent.
- STABILITY: HIGH — voice preservation is a principle, not a formatting choice. The template should not rewrite authored content.

**Voice-Normalize-Must**
- Alternative A: Rewrite all rules to use explicit MUST/MUST NOT prefixes for uniform authority.
- Alternative B: Prepend MUST/MUST NOT only to rules that lack explicit modality markers, leaving already-marked rules unchanged.
- Alternative C: Replace "Do not" with "MUST NOT" and "Use/Validate/Produce/Apply" with "MUST" mechanically.
- PURPOSE: Create uniform authority markers that signal compliance weight consistently.
- HYPOTHESIS: MUST/MUST NOT is a recognized compliance language (RFC 2119 convention). Uniform markers may increase the agent's treatment of all rules as equally mandatory. But mechanical rewriting can produce awkward phrasing ("MUST write instruction text as dull facts" reads differently than "Write instruction text as dull facts").
- STABILITY: LOW — normalization introduces a rewriting step that may have unintended consequences. Testing needed.

**Voice-Normalize-Polarity**
- Alternative A: Group rules into "DO" and "DO NOT" sections within constraints.
- Alternative B: Prefix positive rules with a "+" marker and negative rules with a "-" marker.
- Alternative C: Present all rules as prohibitions (rewrite positive mandates as "Do not deviate from..." formulations).
- PURPOSE: Make polarity explicit so the agent can quickly distinguish what to do from what to avoid.
- HYPOTHESIS: Polarity grouping may help agents with compliance — they can check "am I doing all the DOs?" and "am I avoiding all the DON'Ts?" separately. But it fragments the authored order, which may have been intentional (e.g., the builder's rules flow from namespace → validation → output → style → permissions → prohibitions → conditional → sourcing, which tells a coherent story).
- STABILITY: LOW — polarity grouping is a structural intervention that may or may not help. High risk of disrupting authored coherence.

---

#### STRUCTURAL: Rule Count Communication

The agent needs to know how many rules exist so it can self-audit completeness. But explicitly stating the count may have compliance effects.

**Count-Explicit-Header**
- Alternative A: "You have {N} operational constraints:" followed by the list.
- Alternative B: "{N} constraints govern your execution:" followed by the list.
- Alternative C: "Constraints ({N}):" as a section header.
- PURPOSE: Give the agent an explicit count to verify it has processed all rules.
- HYPOTHESIS: Explicit count creates a self-checking mechanism — the agent can count the rules it's tracking and verify against the stated total. This is especially valuable for longer lists (8+) where positional decay is a real risk.
- STABILITY: MEDIUM — useful but the count can be derived from the list itself. The question is whether stating it explicitly improves compliance.

**Count-Implicit**
- Alternative A: Present the list with no count header — the agent infers the count from the list.
- Alternative B: End the section with "All {N} constraints above apply simultaneously." as a reinforcement.
- Alternative C: (No count communication at all.)
- PURPOSE: Avoid the overhead of explicit counting in favor of trusting the list presentation.
- HYPOTHESIS: For short lists (under 6), explicit counts add little value. For longer lists, they may help. The trailing reinforcement variant (B) has the advantage of appearing after the agent has read all rules, serving as a "did you get all of those?" check.
- STABILITY: MEDIUM — depends on list length, which varies per agent.

---

#### STRUCTURAL: Constraint-to-Instruction Boundary

Some constraints are dangerously close to being instructions. "Validate ALL 18 conditional field rules before writing any output" sounds like a workflow step. "Write instruction text as dull facts" sounds like a style instruction. The template must clarify why these live in constraints rather than instructions.

**Boundary-Preamble-Distinction**
- Alternative A: "Constraints are not steps — they are conditions that must hold true at all times, not at specific points in your workflow."
- Alternative B: "Unlike instructions, which you follow in sequence, constraints are rules you must not violate at any point during execution."
- Alternative C: "Your instructions tell you what to do. Your constraints tell you how to do it — the standards that apply to every action."
- PURPOSE: Help the agent distinguish between "do this now" (instruction) and "always do this" (constraint).
- HYPOTHESIS: Alternative C's "what vs how" framing is the clearest mental model. Instructions are the WHAT. Constraints are the HOW and the ALWAYS. This framing reduces the risk of the agent treating constraints as additional workflow steps to be sequenced.
- STABILITY: HIGH — the relationship between constraints and instructions is architectural. The framing should be consistent across all agents.

**Boundary-No-Distinction**
- Alternative A: (Omit any explicit distinction — let section naming and ordering convey the difference.)
- Alternative B: Use only the section header "Constraints" with no elaboration on what makes them different from instructions.
- Alternative C: Rely on the overall prompt structure (instructions appear earlier, constraints appear later) to convey the difference.
- PURPOSE: Minimize template overhead by trusting structural positioning.
- HYPOTHESIS: Risky. Without explicit distinction, the agent may treat constraints as "more instructions" and try to sequence them into its workflow. This is particularly dangerous for rules like "Validate ALL 18 conditional field rules before writing any output" which SOUNDS like a step. The agent needs to understand this is a rule ("never write without validating first") not a step ("step N: validate").
- STABILITY: LOW — likely insufficient for reliable compliance.

---

#### STRUCTURAL: Relationship to Critical Rules

Constraints exist in a hierarchy with critical_rules above them and anti_patterns below. The agent must understand this hierarchy to calibrate its compliance effort.

**Hierarchy-Explicit-Tier**
- Alternative A: "These constraints are mandatory compliance standards. They are less severe than critical rules (which trigger output rejection) but more binding than anti-patterns (which describe quality risks)."
- Alternative B: "Constraint violations produce non-compliant output. Critical rule violations produce rejected output. Treat both seriously, but understand: critical rules are absolute, constraints are standards."
- Alternative C: "You operate under three tiers of behavioral rules: critical rules (hard failures), constraints (compliance standards), and anti-patterns (quality risks). This section defines tier 2."
- PURPOSE: Give the agent a calibrated understanding of how much effort to invest in constraint compliance relative to other rule types.
- HYPOTHESIS: Without explicit hierarchy, agents tend to either flatten all rules to the same weight (over-compliance that wastes capacity) or create their own implicit hierarchy (under-compliance on rules they deem "less important"). Explicit tiering gives the agent permission to invest proportionally while ensuring nothing is ignored.
- STABILITY: HIGH — the three-tier model is an architectural decision that should be consistent.

**Hierarchy-Implicit-Positioning**
- Alternative A: Place constraints between critical_rules and anti_patterns in the prompt, relying on position to convey hierarchy.
- Alternative B: Use section headers with descending severity language: "Critical Rules" → "Constraints" → "Anti-Patterns" (severity is implied by naming).
- Alternative C: (No hierarchy communication — each section stands alone.)
- PURPOSE: Reduce template verbosity by using structural cues instead of explicit statements.
- HYPOTHESIS: Positioning alone is insufficient. "Constraints" does not inherently communicate "tier 2 of 3." The agent may not infer a hierarchy from section ordering. Explicit framing is likely necessary, at least minimally.
- STABILITY: MEDIUM — if testing shows agents reliably infer hierarchy from position, explicit framing can be reduced.

---

#### STRUCTURAL: Closing Reinforcement

After the rule list, should the template add a closing statement that reinforces the section's authority?

**Closing-Reinforcement-Active**
- Alternative A: "Every constraint above is auditable. Your output will be evaluated against each one."
- Alternative B: "These constraints are non-negotiable for the duration of this task."
- Alternative C: "Maintain compliance with all {N} constraints throughout execution. Partial compliance is not acceptable."
- PURPOSE: Counter the positional decay effect where rules at the start of a list carry more weight than rules at the end.
- HYPOTHESIS: A closing reinforcement re-activates the agent's attention to the entire constraint set. It's a "don't forget the ones you just read" signal. The "auditable" framing (A) is particularly powerful because it implies external review — the agent's compliance will be checked.
- STABILITY: MEDIUM — useful but risks feeling redundant if the preamble already established authority clearly.

**Closing-Reinforcement-None**
- Alternative A: (End section after the last rule — no closing statement.)
- Alternative B: Use a horizontal rule or section break to signal the section is complete.
- Alternative C: Transition directly to the next section header.
- PURPOSE: Keep the template lean. If the preamble established authority, a closing statement may be redundant.
- HYPOTHESIS: For short constraint lists (under 6), closing reinforcement adds little. For longer lists (8+), it may be valuable. The decision may depend on rule count — a conditional inclusion.
- STABILITY: MEDIUM — may be conditioned on rule count.

---

## CROSS-SECTION DEPENDENCIES

### Constraints ↔ Critical Rules
- Critical rules define hard failures. Constraints define compliance standards. The agent must understand that violating a constraint is bad but violating a critical rule is terminal. If both sections lack clear authority differentiation, the agent may treat them identically (over-cautious) or conflate them (unpredictable).
- **Design requirement**: The constraint preamble should reference critical rules if it establishes a hierarchy. But it must not repeat or contradict critical rule content.

### Constraints ↔ Anti-Patterns
- Anti-patterns describe recognizable failure modes — things the agent's training data makes it likely to do wrong. Constraints describe rules. The difference: anti-patterns say "you will be tempted to do X — don't." Constraints say "rule: don't do X."
- Some constraints COULD be anti-patterns and vice versa. The author's placement is the authority. The template should not second-guess it.
- **Design requirement**: If the template adds grouping or categorization to constraints, it must not create categories that overlap with what anti-patterns already cover.

### Constraints ↔ Instructions
- This is the most critical boundary. Rules like "Validate ALL 18 conditional field rules before writing any output" straddle the line. It reads like an instruction step but lives in constraints because it's a RULE (always validate before writing) not a STEP (step 5: validate).
- **Design requirement**: The boundary preamble fragment is essential. Without it, constraint-instruction confusion is likely.

### Constraints ↔ Examples
- Constraints can be grounded by examples (e.g., "Write instruction text as dull facts" is much clearer with a before/after example). But examples live in their own section.
- **Design requirement**: The template should not inject examples into the constraint section, but the constraint section may reference the examples section if needed.

---

## CONDITIONAL BRANCHES

### Branch: Rule Count
- If `len(rules) <= 5`: Short list. Numbering optional, closing reinforcement unnecessary, count header adds little.
- If `len(rules) >= 6 and <= 10`: Medium list. Numbering recommended, count header helpful, closing reinforcement valuable.
- If `len(rules) > 10`: Long list. Numbering essential, count header essential, closing reinforcement essential, consider whether some rules should have been critical_rules or anti-patterns instead.

### Branch: Rule Voice Uniformity
- If all rules use consistent MUST/MUST NOT markers: No normalization needed. Preserve authored voice.
- If rules use mixed voice (some imperative, some declarative, some MUST-prefixed): Decision point — normalize or preserve? Recommendation: preserve, but add uniform authority framing in the preamble.

### Branch: Presence of Near-Instruction Rules
- If any constraint reads like a workflow step: Boundary distinction preamble is mandatory.
- If all constraints are clearly ambient rules: Boundary distinction can be lighter.

### Branch: Hierarchy Communication
- If the overall prompt template renders critical_rules, constraints, and anti_patterns in sequence: Positional hierarchy can supplement explicit hierarchy framing.
- If sections are rendered in non-hierarchical order or separated by other content: Explicit hierarchy framing is mandatory.

---

## SYNTHESIS: Recommended Fragment Stack

For a constraint section, the template should compose from these layers:

1. **Preamble** (required): Authority establishment + ambient framing + boundary distinction
2. **Count** (conditional on list length): Explicit count for 6+ rules
3. **Rule list** (required): Preserved authored voice, numbered for 6+ rules, bulleted for fewer
4. **Closing** (conditional on list length): Reinforcement for 8+ rules

The minimal viable constraint section for a short-list agent:

```
Constraints — these rules apply throughout your work, not at specific steps:

- Rule 1...
- Rule 2...
- Rule 3...
```

The full constraint section for a long-list agent:

```
You have 10 operational constraints. These are compliance standards — less severe than critical rules (which reject your output) but mandatory throughout execution. They are not workflow steps; they are conditions that must hold true across all phases of your work.

1. Rule 1...
2. Rule 2...
...
10. Rule 10...

Every constraint above is auditable. Your output will be measured against each one.
```

The key design insight: **constraints are the agent's operating law, not its operating procedure.** The template must frame them as law — ambient, simultaneous, accountable — and resist any presentation that makes them feel like additional instructions to be sequenced.
