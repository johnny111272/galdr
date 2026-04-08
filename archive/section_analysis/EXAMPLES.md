# EXAMPLES — Control Surface Synthesis

## Section Purpose

The examples section is a **judgment calibration system** that operates through induction rather than declaration. Every other section tells the agent what to do or avoid. This section shows it what correct judgment looks like, what its own most probable mistakes look like, and why the boundary falls where it does. The agent must extract transferable principles from specific demonstrations and apply them to unseen inputs. [CONVERGED — both analyses independently reached this framing with high confidence.]

The section has a three-level hierarchy that is architecturally meaningful, not incidental:

- **Section level:** Mode transition — the agent shifts from absorbing procedure into absorbing demonstrations.
- **Group level:** Calibration targeting — each group corresponds to a distinct cognitive task requiring independent calibration.
- **Entry level:** Decision boundary demonstration — each entry shows one case where judgment is required, what correct and incorrect judgment produce, and why.

The GOOD/BAD/WHY mechanism is the core behavioral programming pattern. GOOD establishes the target. BAD names the agent's most probable mistake (a failure-mode fingerprint, not an arbitrary wrong answer). WHY converts the specific contrast into a transferable principle — the variable that governs the decision, not the decision itself. Entries without BAD/WHY establish baseline correct behavior; entries with the full pattern mark decision boundaries. [CONVERGED — both analyses identified this as the section's central mechanism.]

## Fragment Catalog

### section_heading
- CONVERGED: The heading marks a cognitive mode shift from declaration to demonstration. Heading presence and level (H2) are fixed.
- DIVERGED: None significant. Both identified the same alternatives and the same core tension.
- ALTERNATIVES:
  - A: `## Worked Examples` — "worked" universally signals "study the reasoning process," may produce deeper engagement than the neutral word "examples."
  - B: `## Calibration Examples` — names the purpose explicitly, but "calibration" may not have strong behavioral associations in training data.
  - C: `## Examples` — neutral, conventional. Risk: agent processes as "optional reference" rather than "mandatory calibration."
- HYPOTHESIS: Heading text is the lever. "Worked Examples" likely produces the strongest engagement because it primes active study rather than passive scanning. Testable: does heading phrasing affect consistency of applying example principles to novel inputs?
- STABILITY: **structural** (presence, level) + **experimental** (text choice)
- CONDITIONAL: none

### section_preamble
- CONVERGED: Both identified this as one of the highest-leverage fragments in the entire section. It configures how the agent processes all subsequent examples. Both flagged the risk of too-long preambles displacing the demonstrations themselves.
- DIVERGED: A on whether the generalization instruction or the GOOD/BAD/WHY vocabulary explanation carries more weight. B emphasized the generalization instruction as highest-leverage single sentence; A emphasized the structural guide naming the GOOD/BAD/WHY pattern.
- ALTERNATIVES:
  - A: GOOD/BAD/WHY vocabulary + generalization combined (short): `Examples may show GOOD and BAD outputs with WHY reasoning. GOOD is correct judgment. BAD is the specific mistake you are most likely to make. WHY is the principle — learn the principle and apply it to inputs not shown here.`
  - B: No preamble — examples speak for themselves. Cleanest, but risks passive scanning and missed calibration intent.
- HYPOTHESIS: A short preamble that installs the interpretive framework AND the generalization instruction outperforms both no-preamble and long-preamble. The agent needs to know (1) what GOOD/BAD/WHY labels mean, and (2) that it should extract principles for novel inputs, not memorize specific cases. Both fit in 2-3 sentences. Testable: does a preamble improve generalization to inputs not covered by any example?
- STABILITY: **experimental** (whether to include, what to say — this is where behavioral leverage concentrates)
- CONDITIONAL: none

### group_heading
- CONVERGED: H3 heading creates the strongest group boundaries. The group heading is architecturally necessary for multi-group agents and redundant for single-group agents.
- DIVERGED: On whether to suppress for single-group agents. A leaned toward conditional suppression as cleaner. B noted that suppression creates inconsistency but is pragmatically correct.
- ALTERNATIVES:
  - A: `### {example_group_name}` — H3, direct. Full hierarchy preserved.
  - B: Conditional: suppress heading when group_count = 1, render at H3 when group_count > 1.
  - C: `### Calibration: {example_group_name}` — prefixed, names the group's function.
- HYPOTHESIS: Conditional rendering (B) is the correct design. Single-group agents do not benefit from the intermediate heading; multi-group agents require it for calibration context switching. The "Calibration:" prefix (C) adds framing but may be redundant if the section preamble already establishes calibration context.
- STABILITY: **structural** (heading level, hierarchy decision) + **conditional** (single vs. multi-group)
- CONDITIONAL: group_count = 1 triggers suppression; group_count > 1 triggers full H3 rendering

### group_framing_sentence
- CONVERGED: Both identified the instruction-step link (explicit cross-reference to paired instruction steps) as the most powerful variant and both flagged its maintenance fragility.
- DIVERGED: A explored instruction-step linking as an active design option. B concluded the maintenance cost likely outweighs the benefit and recommended no framing sentence (let the heading carry the weight).
- ALTERNATIVES:
  - A: No framing sentence — heading followed directly by first entry. Cleanest.
  - B: `These examples calibrate your judgment for Step {N}: {step_summary}.` — explicit cross-section link. Most powerful but creates a maintenance dependency on instruction step numbering.
- HYPOTHESIS: No framing sentence (A) is the safer default. The instruction-step link is better placed as a back-reference FROM the instructions section (see cross-section dependencies) than as a forward-reference within examples. If instruction steps are renumbered, a forward reference in examples becomes stale.
- STABILITY: **experimental** (whether to include) + **conditional** (instruction-step links require cross-section data)
- CONDITIONAL: If pairing is rendered, requires instruction step numbers from the instructions section

### example_display_headings (toggle)
- CONVERGED: This is a per-group display mode gate, not a prose fragment. Both agents use `true`. Both analyses identified headings-on as the safer default.
- DIVERGED: B raised an over-indexing concern — named headings might cause the agent to match inputs to heading text rather than generalizing the underlying principle. A did not flag this risk.
- ALTERNATIVES:
  - A: `true` (headings on) — creates cognitive anchors for per-entry recall and reference during processing.
  - B: `false` (headings off) — forces the agent to extract patterns from content alone. Potentially deeper engagement but weaker recall.
- HYPOTHESIS: Headings-on is correct default. The over-indexing risk (B's concern) is real but secondary to the benefit of entry-level recall hooks. Testable: does heading specificity correlate with over-indexing on matching inputs at the expense of generalization?
- STABILITY: **formatting** (display mode toggle)
- CONDITIONAL: none currently; both agents use `true`, so `false` branch is untested

### entry_heading
- CONVERGED: Both identified two distinct naming conventions — skill-naming (builder: "Designing Instruction Steps") vs. condition-naming (summarizer: "Thin content with rich context") — and noted this is an authoring convention, not a template choice.
- DIVERGED: B gave more weight to the heading format (H4 vs bold) as a visual density concern for groups with many entries. A treated it more as a straightforward hierarchy decision.
- ALTERNATIVES:
  - A: `**{example_heading}**` — bold text, visually subordinate to group heading. Lighter for dense groups.
  - B: `#### {example_heading}` — H4, completing the three-level hierarchy. Strongest entry boundaries but heavy for 5+ entry groups.
- HYPOTHESIS: Bold text (A) is the better default. H4 creates visual density in groups with many entries where structural chrome competes with content for attention. Bold preserves clear entry boundaries without adding heading-level weight. The naming convention (skill vs condition) should be documented as authoring guidance: use skill-naming for creative/design tasks, condition-naming for classification/treatment tasks.
- STABILITY: **formatting** (heading level/style) + **conditional** (only rendered when display_headings = true)
- CONDITIONAL: Gated by example_display_headings = true

### entry_body_container
- CONVERGED: Both identified bare rendering as highest-fidelity and both flagged entry-boundary blur as the risk for multi-entry groups.
- DIVERGED: A considered fenced blocks; B considered blockquotes more seriously. Both converged on an end-marker approach as the best compromise.
- ALTERNATIVES:
  - A: Bare rendering with end-marker — text as-is, followed by a delimiter that cleanly terminates the entry. Best fidelity with guaranteed boundaries.
  - B: Blockquote wrapping (`> `) — clearest containment, but adds visual weight that may cause superficial scanning.
- HYPOTHESIS: Bare rendering with end-marker (A) is the correct default. The author's GOOD/BAD/WHY labels, input scenarios, and reasoning are presented without additional visual framing. The end-marker guarantees clean entry termination without wrapping overhead. Blockquotes are the fallback if boundary blur proves problematic in testing.
- STABILITY: **formatting** (container style, applies uniformly to all entries)
- CONDITIONAL: none

### entry_separator
- CONVERGED: When headings are on, the heading IS the separator — no additional separator needed. When headings are off, an explicit separator becomes critical.
- DIVERGED: None significant.
- ALTERNATIVES:
  - A: No explicit separator when headings are on (heading provides the boundary).
  - B: `---` horizontal rule when headings are off (strongest boundary for anonymous entries).
- HYPOTHESIS: Let the heading carry the separation burden when present. Only add horizontal rules in the headings-off mode. Double-boundary (rule + heading) is visual noise.
- STABILITY: **formatting** (separator style) + **conditional** (behavior differs based on display_headings toggle)
- CONDITIONAL: display_headings = true -> no separator; display_headings = false -> horizontal rule

### GOOD/BAD/WHY pattern treatment
- CONVERGED: Both identified this as a foundational architecture decision. Both converged on the preamble-only approach as the best balance — teach the agent the vocabulary without parsing the text.
- DIVERGED: A explored promoting GOOD/BAD/WHY to separate data fields (structural approach) more seriously. B considered it but dismissed it faster due to author flexibility constraints.
- ALTERNATIVES:
  - A: Preamble-only awareness — section preamble explains the vocabulary; template renders example_text as opaque. Author retains full flexibility; agent has the interpretive framework.
  - B: Pattern-structural — GOOD/BAD/WHY become separate fields. Template controls presentation of each component. Most powerful for experiments but constrains authors (builder's Wrong/Right pattern does not fit).
- HYPOTHESIS: Preamble-only (A) is the correct design. It invests the section preamble with responsibility for installing the interpretive framework, then trusts authored labels to work within it. The structural approach (B) is more powerful but incompatible with the variety of internal patterns observed (GOOD/BAD/WHY, Wrong/Right, Required/NOT required). Testable: does preamble priming plus authored labels produce equivalent calibration to structured fields with template-controlled formatting?
- STABILITY: **structural** (whether the template is pattern-aware at all — foundational decision)
- CONDITIONAL: none

### multi_group_transition
- CONVERGED: Fragment only activates for group_count > 1. Neither current agent exercises this path. Both agreed the design must anticipate it.
- DIVERGED: A explored transitional prose between groups. B favored horizontal rule as cleaner.
- ALTERNATIVES:
  - A: `---` horizontal rule between groups — clean visual break, no prose filler.
  - B: Next group heading alone (no explicit transition) — sufficient if groups are clearly different cognitive tasks.
- HYPOTHESIS: Horizontal rule (A) provides a clear context-switch signal without adding prose. Group headings alone may be sufficient for very different calibration contexts but insufficient for similar ones. Default to horizontal rule.
- STABILITY: **structural** (transition mechanism) + **conditional** (only for multi-group agents)
- CONDITIONAL: group_count > 1

### single_group_simplification
- CONVERGED: Both identified the hierarchy collapse question as important. Both leaned toward suppressing the group heading for single-group agents.
- DIVERGED: A proposed promoting entries to H3 when group heading is suppressed (clean two-level hierarchy). B proposed rendering the group name as a non-structural epigraph. Both are valid.
- ALTERNATIVES:
  - A: Suppress group heading, promote entries to H3. Agent sees `## Examples` -> `### {entry}`. Clean, no hierarchy gap.
  - B: Suppress group heading, keep entries at current level. Agent sees `## Examples` -> `**{entry}**` (bold entries). Simpler template logic.
- HYPOTHESIS: Option A (suppress + promote) is cleanest. Two-level hierarchy for single-group agents, three-level for multi-group. The inconsistency is justified because single-group agents genuinely need less structure. Testable: does suppressing the group heading improve content engagement (less chrome) or reduce it (weaker organizational signal)?
- STABILITY: **conditional** (group_count = 1) + **structural** (affects heading hierarchy)
- CONDITIONAL: group_count = 1

### section_position
- CONVERGED: Both identified immediately-after-instructions as the natural calibration sequence. Both flagged interleaved placement as strongest pairing but architecturally incompatible with section-based structure.
- DIVERGED: B considered after-anti-patterns positioning more seriously (agent has prohibition knowledge before seeing demonstrations). A treated it as secondary.
- ALTERNATIVES:
  - A: Immediately after instructions — "here is what to do" then "here is what doing it well looks like." Natural pedagogical sequence.
  - B: After anti-patterns/constraints — agent has both procedural and prohibition knowledge before calibration. BAD examples reinforce already-absorbed prohibitions.
- HYPOTHESIS: After-instructions (A) is the default. The agent calibrates while procedural knowledge is freshest. After-anti-patterns (B) is worth testing if BAD example recognition proves weak.
- STABILITY: **structural** (section ordering is architectural)
- CONDITIONAL: none

## Cross-Section Dependencies

**Examples <-> Instructions (pairing):** The most important cross-section relationship. Each probabilistic instruction step describes a cognitive task; each example group calibrates that task. Currently implicit. The strongest rendering is a back-reference FROM instruction steps TO example groups (`See examples: {group_name}`), because the agent encounters the link at the point of use. Forward references from examples to instruction steps are fragile (break when steps are renumbered). [CONVERGED]

**Examples <-> Anti-Patterns (reinforcement):** BAD examples and anti-patterns describe the same behavioral boundaries from different perspectives — one as concrete demonstration, one as abstract rule. Uncoordinated redundancy is the correct design: both mechanisms reinforce without needing explicit cross-references. [CONVERGED]

**Examples <-> Success Criteria (grounding):** Examples are case-level instantiations of section-level success criteria. The connection is natural enough that explicit grounding adds noise, not value. [CONVERGED — both rated this low-priority]

## Conditional Branches

**group_count = 1 -> suppress group heading, promote entries.** Single-group agents render a two-level hierarchy (section, entry). Group name exists in data but does not render as a heading.

**group_count > 1 -> full three-level hierarchy with horizontal rule transitions.** Each group gets an H3 heading. Horizontal rule separates groups. Entries render under their group.

**display_headings = true -> entry headings as bold text, no entry separator.** The heading provides the boundary between entries.

**display_headings = false -> no entry headings, horizontal rule between entries.** The separator is the only boundary signal.

**Probabilistic instruction steps with paired example groups -> back-reference in instructions section.** The examples section itself does not render the link; the instructions section does.

**Probabilistic instruction steps WITHOUT paired example groups -> no acknowledgment.** Silence is better than drawing attention to missing calibration. The section preamble's generalization instruction covers uncalibrated steps implicitly.

## Open Design Questions

1. **Does heading text ("Worked Examples" vs "Examples" vs "Calibration Examples") measurably affect depth of engagement with example content?** Both analyses hypothesized it matters but neither had evidence. This is a testable question.

2. **Does the over-indexing risk from named entry headings outweigh the recall benefit?** B flagged that specific heading names (e.g., "Thin content with rich context") might cause the agent to apply calibration only when inputs literally match the heading phrase, reducing generalization. A did not address this. Unresolved.

3. **Is the preamble-only approach to GOOD/BAD/WHY sufficient, or does structural promotion to separate fields produce meaningfully better calibration?** Both analyses favored preamble-only for its flexibility, but neither could rule out that structured fields with template-controlled formatting would be more effective.

4. **Should the back-reference from instruction steps to example groups be implemented?** Both analyses identified it as the most powerful pairing mechanism. Neither resolved whether the maintenance cost (cross-section data coupling) is justified by the behavioral improvement.

5. **What is the optimal entry count per group before calibration quality degrades?** The builder has 2 entries (possibly under-calibrated), the summarizer has 5 (covering at least two distinct cognitive tasks that should arguably be separate groups). No guidance exists on the sweet spot.

## Key Design Decisions

1. **Template treats example_text as opaque; preamble installs the interpretive framework.** The GOOD/BAD/WHY pattern is handled through preamble vocabulary explanation, not through template parsing or field promotion. This preserves author flexibility across varied internal patterns (GOOD/BAD/WHY, Wrong/Right, Required/NOT required). Direction: preamble-only. [HIGH CONFIDENCE — both analyses converged]

2. **Single-group agents suppress the group heading; multi-group agents render full hierarchy.** The conditional branch simplifies the common case (most current agents are single-group) while preserving structural clarity for the multi-group case. Direction: conditional rendering with entry promotion. [HIGH CONFIDENCE — both analyses converged]

3. **Instructions-examples pairing rendered as back-reference from instructions, not forward-reference from examples.** The link is most useful at the point where the agent is about to execute a step, not when it is absorbing calibration. Back-references are also more resilient to renumbering. Direction: implement in instructions section, not examples section. [MODERATE CONFIDENCE — architecturally sound but untested]

4. **Section preamble is mandatory and short (2-3 sentences).** It must accomplish exactly two things: install the GOOD/BAD/WHY vocabulary and instruct the agent to generalize principles to novel inputs. Nothing else. Direction: always include, keep tight. [HIGH CONFIDENCE — both analyses identified this as highest-leverage fragment]

5. **Entry headings use bold text, not H4.** Bold preserves clear entry boundaries without the visual density of heading-level markup. For groups with 5+ entries, this is a significant readability improvement. Direction: bold text default. [MODERATE CONFIDENCE — reasonable but testable]
