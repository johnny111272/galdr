# Examples Section: Control Surface Analysis (Agent B)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The examples section exists to solve a problem that no other section can solve: configuring the agent's judgment without being able to specify what judgment means in advance.

Instructions tell the agent what cognitive operations to perform. Constraints and anti-patterns tell it what to avoid. Success criteria tell it what "done" looks like. But none of these can transmit the *quality of judgment* the agent needs for probabilistic tasks. You cannot write an instruction that says "summarize with the right amount of significance" because "the right amount" is the exact thing that needs calibrating. You can only show the agent cases where the amount was right, cases where it was wrong, and the reasoning that distinguishes them.

This makes the examples section fundamentally different from every other section. Every other section operates through declaration: "you are X," "do Y," "never do Z." The examples section operates through **induction** — the agent must extract the general principle from specific demonstrations and apply it to unseen inputs. The section is not a reference manual the agent consults during processing. It is a training sequence the agent absorbs before processing begins, which reconfigures the probability distribution over its outputs.

Three things the examples section must accomplish:

1. **Mark decision boundaries.** A single GOOD example shows the agent one correct output. Two contrasting examples (GOOD/BAD for the same input) show it where the boundary between correct and incorrect lies. The summarizer's "thin content with rich context" vs "thin content with thin context" pair is a boundary marker: both inputs are short text, but they require opposite treatments. The boundary is context weight, not content length. Without both sides of the boundary, the agent has no way to know that text length is not the governing variable.

2. **Name the agent's natural failure modes.** Every BAD example is a prediction about what the uncalibrated agent would produce. "User makes a brief comment" is what an uncalibrated summarizer produces for short text — it matches text length to summary length. "User confirms the approach to recursive knowledge architecture" is what an uncalibrated summarizer produces for administrative text — it inflates significance by mining prior context for the most impressive-sounding topic. The BAD examples are not arbitrary wrong answers. They are the specific wrong answers the agent is most likely to produce. This makes them failure-mode inoculations: the agent encounters its own probable mistake before encountering live data.

3. **Transmit reasoning about quality.** The WHY blocks are not supplementary commentary. They are the only mechanism that teaches the agent why one output is correct and another is wrong. Without WHY, the agent has matched examples — it can pattern-match "this input looks like that example, so produce that output." With WHY, the agent has principles — it can reason "this input has property X, and the principle says property X governs treatment, so I should..." The WHY is what converts examples from a lookup table into a reasoning framework.

The design challenge is that all three of these functions must operate within a three-level hierarchy (section, group, entry) where the structural scaffolding around the raw data either amplifies or attenuates the calibration effect. Too much scaffolding and the structure overshadows the content. Too little and the agent processes examples as an undifferentiated stream, losing the per-group calibration targeting.

---

## THE THREE-LEVEL HIERARCHY AS A FIRST-CLASS DESIGN CONCERN

The hierarchy is not a formatting convenience. It is the structural expression of how calibration should work:

```
Section    = "you are entering calibration mode"
  Group    = "this calibration targets {this specific kind of judgment}"
    Entry  = "here is one decision boundary for that kind of judgment"
```

Each level serves a distinct cognitive function:

- **Section level:** Mode transition. The agent shifts from absorbing procedure (instructions) or constraints (rules) into absorbing demonstrations. The section boundary tells the agent: what follows is not more instructions, it is material that configures how you execute the instructions you already have.

- **Group level:** Calibration targeting. Each group corresponds to a distinct cognitive task — a type of judgment the agent must exercise. The builder's "Definition Design" group targets instruction step decomposition and permission minimization. The summarizer's "Contextual Summaries" group targets contextual significance extraction, thin-content disambiguation, and source decontamination. A well-structured agent would have separate groups for each of these, because they are different kinds of judgment that require independent calibration.

- **Entry level:** Decision boundary demonstration. Each entry shows the agent one specific case where judgment is required, what correct judgment produces, and (optionally) what incorrect judgment produces and why.

The current data shows both agents using a single group despite needing multiple calibration targets. This is a definition authoring concern, not a template concern — but the template must make multi-group structure easy enough that authors use it. If the template makes single-group and multi-group agents look the same, there is no structural incentive to split groups. If multi-group structure is visually clear and well-differentiated, authors will naturally target each group to a specific instruction step.

---

## FRAGMENT CATALOG

### Fragment 1: section_heading

**Data field:** None (structural)
**Purpose:** Signal the transition from procedural/declarative sections into demonstrative calibration material. The heading marks a cognitive mode shift for the agent.

**Prose alternatives:**
- (a) `## Examples`
- (b) `## Calibration Examples`
- (c) `## Worked Examples`
- (d) `## Judgment Calibration`
- (e) `## How These Judgments Should Look`

**PURPOSE:** The heading is the agent's first signal that the mode of content has changed. Everything before this was declaration ("do X," "you are Y," "never Z"). Everything after this is demonstration ("here is what doing X correctly looks like"). The heading either names this transition explicitly or relies on the word "Examples" to carry it implicitly.

**HYPOTHESIS:** The word "Examples" alone is semantically weak — in training data, "Examples" sections range from formatting references to API documentation to few-shot prompting samples. The agent may process an "Examples" heading as "optional reference material" rather than "mandatory calibration material." A heading like "Judgment Calibration" or "How These Judgments Should Look" explicitly frames the content as configuring the agent's behavior, not illustrating a format. However, unusual headings may confuse more than they clarify if they diverge too far from convention. Test: does heading phrasing measurably affect how deeply the agent engages with the example content (measured by consistency of applying example principles to novel inputs)?

**STABILITY:** Structural (heading presence and level are fixed; an agent always has an examples section heading at H2). Experimental (heading text is the lever — the word choice is where behavioral hypotheses live).

---

### Fragment 2: section_preamble

**Data field:** None (structural/optional)
**Purpose:** Prime the agent for how to process the examples that follow — what to extract, what the GOOD/BAD/WHY vocabulary means, and how examples relate to instruction steps.

**Prose alternatives:**
- (a) No preamble. Section heading is followed directly by the first group.
- (b) Short framing: `Each example below shows a judgment you must make and what correct judgment looks like. Where BAD outputs appear, they show the specific mistake you are most likely to make. The WHY explains the principle — learn the principle, not just the example.`
- (c) Instruction-linking preamble: `The examples below calibrate the judgment required by your probabilistic instruction steps. Each example group targets a specific kind of reasoning. Study the decision boundaries, not the specific cases.`
- (d) Generalization instruction: `These examples are not exhaustive. They mark the boundaries of correct judgment. For inputs that fall between the demonstrated cases, reason from the principles shown in the WHY explanations.`
- (e) Combined: a short paragraph that explains the GOOD/BAD/WHY vocabulary, links examples to instruction steps, and instructs on generalization.

**PURPOSE:** Without a preamble, the agent discovers the GOOD/BAD/WHY pattern inductively — it sees the first "GOOD summary:" label and must infer that this is a calibration vocabulary, not decorative text. With a preamble, the agent enters the examples section with an explicit framework for interpreting what it reads. The preamble also determines whether the agent understands that examples are boundary markers (generalize from them) or specific references (match inputs to them).

This is a question of how much meta-instruction the calibration system needs. The risk of no preamble: the agent processes examples as a list and misses the calibration intent. The risk of too much preamble: the agent reads about calibration instead of absorbing calibration — the meta-instruction becomes noise that displaces the demonstrations themselves.

**HYPOTHESIS:** A short preamble (b or d) likely outperforms no preamble, because it installs the interpretive framework before the first example arrives. The agent encounters "GOOD summary:" knowing it is a calibration label, not just a prefix. The generalization instruction (d) is the highest-leverage single sentence because it explicitly tells the agent to extract principles — without it, the agent may memorize the specific examples rather than the judgment they demonstrate. The combined form (e) risks being too long — a 3-4 sentence preamble before any actual example content may cause the agent to treat the preamble as "instructions about examples" rather than shifting into example-processing mode. Test: does a preamble improve generalization to inputs not covered by any example? Does a long preamble reduce engagement with the examples themselves?

**STABILITY:** Experimental (whether to include, what to say). This is a high-leverage fragment because it configures how the agent processes all subsequent example content.

---

### Fragment 3: group_heading

**Data field:** `example_group_name` (string)
**Purpose:** Introduce a calibration unit — a set of entries that all target the same kind of judgment.

**Prose alternatives:**
- (a) `### {example_group_name}` — H3 heading using the group name directly. Creates the middle level of the three-level hierarchy.
- (b) `### Calibration: {example_group_name}` — prefixed heading that names the group's function.
- (c) `**{example_group_name}**` — bold text, no heading. Reduces the heading hierarchy from three levels to two.
- (d) Conditional: if only one group, suppress the heading entirely (the section heading covers it). If multiple groups, render as H3.
- (e) `### {example_group_name} ({N} examples)` — heading with entry count.

**PURPOSE:** The group heading establishes a calibration context. When the agent reads "### Contextual Summaries," it should understand: the entries that follow demonstrate how to produce contextual summaries. When it later reads "### Source Decontamination" (hypothetical second group), it should understand: the calibration context has shifted to a different cognitive task.

The heading also participates in the instructions-examples pairing. If the group name echoes the vocabulary of a probabilistic instruction step, the agent can connect them. The builder's "Definition Design" group maps loosely to instruction steps 3 and 7. The summarizer's "Contextual Summaries" maps to instruction step 2 but also covers decontamination content that maps to step 5. This loose mapping suggests the group name should be specific enough to target one cognitive task, and that definition authors should be guided to create separate groups rather than lumping disparate tasks under one name.

**HYPOTHESIS:** H3 headings (a) create the strongest group boundaries in the agent's processing. Bold text (c) creates weaker boundaries — the group may not register as a distinct calibration context. Conditional suppression (d) is pragmatic for single-group agents but introduces template complexity. The key question is whether the single-group case (both current agents) benefits from the group heading at all. With one group, the heading is redundant information — it names the only calibration unit, which the agent could infer from the section heading alone. With multiple groups, the heading is essential for context switching. The count suffix (e) may trigger completionist processing rather than deep engagement. Test: for multi-group agents, does H3 group separation produce better per-group calibration adherence than bold-text separation? For single-group agents, does including the group heading add structure or noise?

**STABILITY:** Structural (heading level is a hierarchy decision). Conditional (single-group vs multi-group display). Experimental (prefix text, count suffix).

---

### Fragment 4: group_framing_sentence

**Data field:** None (structural/optional, but could incorporate `example_group_name`)
**Purpose:** Explain what the following entries calibrate and optionally link the group to specific instruction steps.

**Prose alternatives:**
- (a) No framing sentence. Group heading is followed directly by the first entry.
- (b) `The following examples demonstrate {example_group_name_lowered}:` — simple transitional lead-in.
- (c) `These examples calibrate your judgment for Step {N}: {instruction_step_summary}.` — explicit cross-section link to the paired instruction step.
- (d) `{N} examples follow, showing correct and incorrect treatments for {example_group_name_lowered}.` — count + GOOD/BAD preview.
- (e) Per-group processing instruction: `Study the difference between GOOD and BAD outputs — the boundary is where your calibration lives.`

**PURPOSE:** Determines whether the group has connective tissue between its heading and its first entry. No framing (a) is cleanest. The instruction-step link (c) is the most powerful form of the instructions-examples pairing because it explicitly connects "this is what you learned to do in step N" with "here is what doing it looks like." But it requires cross-section data (instruction step numbers/summaries in the examples data) and adds a maintenance dependency.

**HYPOTHESIS:** The instruction-step link (c) is architecturally attractive but practically fragile. If instruction steps are renumbered or reworded, the examples section references become stale. The simple lead-in (b) adds no information but provides a smooth reading transition. The per-group processing instruction (e) risks being redundant with the section preamble. The strongest design may be: preamble establishes the GOOD/BAD/WHY framework once, group headings name the calibration target, and entries follow immediately. No group framing sentence. Test: does the instruction-step link improve calibration application during the linked step enough to justify the maintenance cost?

**STABILITY:** Experimental (whether to include, what to say). Conditional (instruction-step links require cross-section data access).

---

### Fragment 5: example_display_headings toggle

**Data field:** `example_display_headings` (boolean)
**Purpose:** Controls whether individual entries within a group have visible headings derived from `example_heading`.

**Prose alternatives:**
This is not a prose fragment — it is a control gate that determines whether Fragment 6 (entry heading) renders or not. When `true`, entries get headings. When `false`, entries are separated by a delimiter or whitespace alone.

**PURPOSE:** This toggle determines whether the agent perceives each example as a named scenario or as one entry in an anonymous sequence. Named scenarios give the agent retrieval hooks: during processing, it can think "this input resembles the thin-content-rich-context case." Anonymous entries force the agent to extract patterns from content alone, without the cognitive shortcut of a heading name.

There is a deeper question: should this be per-group at all? The current data has both agents setting `example_display_headings = true`. The boolean sits on the group, not the entry, so within one group either all entries have headings or none do. This means the toggle is a group-level display mode: "this group presents named scenarios" vs "this group presents an anonymous sequence."

**HYPOTHESIS:** Headings-on is the safer default because it creates clear entry boundaries and gives the agent cognitive anchors. Headings-off is a specialized mode for cases where entries should blend into a continuous calibration stream — possibly useful for very short entries or for entries that form a narrative sequence where headings would interrupt flow. The interesting design question is whether headings-off ever improves calibration. It might, for cases where the heading name causes over-indexing: the agent looks for inputs that match the heading phrase rather than inputs that match the underlying pattern. "Thin content with rich context" as a heading might cause the agent to only apply that calibration when content is literally thin — a more abstract heading or no heading might produce broader application of the underlying principle. Test: does heading specificity correlate with over-indexing on matching inputs at the expense of generalization?

**STABILITY:** Formatting (display mode toggle). Currently both agents use `true`, so the `false` branch is untested.

---

### Fragment 6: entry_heading

**Data field:** `example_heading` (string, conditional on `example_display_headings = true`)
**Purpose:** Name the scenario, decision boundary, or cognitive skill that the entry demonstrates.

**Prose alternatives:**
- (a) `#### {example_heading}` — H4 heading, completing the three-level hierarchy (H2 section, H3 group, H4 entry).
- (b) `**{example_heading}**` — bold text, visually subordinate, no heading level.
- (c) `**Example: {example_heading}**` — prefixed bold text.
- (d) `**{n}. {example_heading}**` — numbered bold text, adding sequence position.
- (e) `> **{example_heading}**` — blockquoted bold, visually contained.

**PURPOSE:** The entry heading serves two distinct functions depending on the naming convention:

- **Skill-naming** (builder style): "Designing Instruction Steps From Requirements" names what the entry teaches the agent to do. The heading is a skill label. The agent reads it and expects to learn a technique.
- **Condition-naming** (summarizer style): "Thin content with rich context" names what the input looks like. The heading is an input classifier. The agent reads it and expects to learn how to handle this input type.

This is not a template choice — it is an authoring convention. But the template's heading format influences how strongly the heading functions as a retrieval hook. H4 headings (a) make entries navigable sub-sections — the agent can "look up" a specific entry. Bold text (b) makes entries visually distinct without structural weight. Numbered entries (d) add sequence, which implies ordering significance that may or may not exist.

**HYPOTHESIS:** H4 headings are the strongest entry boundaries but may create visual density in groups with many entries. The summarizer's 5 entries as H4 headings produce a heading-heavy section where the structural chrome competes with the content for attention. Bold text (b) is lighter and keeps the entry heading visually subordinate to the group heading. The "Example:" prefix (c) is redundant — the reader already knows these are examples. Numbering (d) may create primacy bias where earlier examples carry more calibration weight. Test: for groups with 5+ entries, does H4 heading density impair content engagement compared to bold text? Does numbering create measurable primacy bias?

**STABILITY:** Formatting (heading level/style is a design choice). Conditional (only rendered when `example_display_headings = true`).

---

### Fragment 7: entry_body_container

**Data field:** `example_text` (multi-line string)
**Purpose:** Present the example content with appropriate visual containment.

**Prose alternatives:**
- (a) Bare rendering — `example_text` is emitted as-is, with no wrapping. Whatever the author wrote is what appears.
- (b) Blockquote wrapping — each line of `example_text` is prefixed with `> `. The entry content is visually distinguished from surrounding structure.
- (c) Indented block — the entire `example_text` is indented by 2-4 spaces, creating visual offset without blockquote formatting.
- (d) Bare rendering with explicit end-marker — the text appears as-is, followed by a `---` or blank-line delimiter that definitively terminates the entry.
- (e) Code fence (non-code) — ````text\n{example_text}\n```` — strongest containment, but may trigger literal-processing mode in the agent.

**PURPOSE:** The entry body is where all the calibration content lives. The question is whether the container should be transparent (bare text) or visible (blockquote, indent, fence). Transparent containers let the content flow naturally — the author's GOOD/BAD/WHY labels, input scenarios, and reasoning are presented without additional visual framing. Visible containers create clear boundaries between "this is example content" and "this is structural scaffolding" — important when entries are long (the reconstructed content decontamination entry is ~10 lines) or when multiple entries sit next to each other.

The content inside `example_text` is not template-controlled — it is author-written free-form text. The template controls only the container. This means the template cannot rely on any internal structure within the text. Some entries have GOOD/BAD/WHY. Some have Wrong/Right. Some have Note: blocks. The container must work regardless of internal structure.

**HYPOTHESIS:** Bare rendering (a) is highest-fidelity and lowest-noise. But for multi-entry groups (summarizer has 5 entries), bare rendering may cause entry-boundary blur — especially when one entry ends with a principle statement and the next begins with an input scenario. The reader (agent) may not clearly perceive where one entry ends and the next begins if the only separator is a heading or whitespace. Blockquote (b) creates the clearest containment but adds visual weight that may cause the agent to process examples more superficially — scanning the blockquote rather than absorbing its content. The end-marker approach (d) preserves bare rendering but guarantees clean entry termination. Test: for multi-entry groups, does entry-boundary clarity improve when entries have visible containers vs bare rendering?

**STABILITY:** Formatting (container style applies uniformly to all entries within a group).

---

### Fragment 8: entry_separator

**Data field:** None (structural)
**Purpose:** Separate adjacent entries within a group. Distinct from the entry body container — the separator is what appears between entries.

**Prose alternatives:**
- (a) Single blank line between entries.
- (b) `---` horizontal rule between entries.
- (c) Double blank line between entries.
- (d) No explicit separator — entry headings provide the boundary (when `example_display_headings = true`).
- (e) Blank line + a thin visual marker like `* * *` between entries.

**PURPOSE:** The separator controls how strongly the agent perceives the boundary between adjacent entries. This interacts with Fragment 5 (headings toggle) and Fragment 6 (entry heading): when headings are on, the heading itself acts as a separator, and an additional separator between entries may be redundant. When headings are off, the separator is the only boundary signal.

In the current rendered output, the defective renderer uses H4 headings with no explicit separator between entries. The markdown heading itself creates the visual break. This is arguably correct for the headings-on case — a heading already signals "new entry" and a horizontal rule before it would be visual noise.

**HYPOTHESIS:** When headings are on, no explicit separator (d) is cleanest — the heading IS the separator. Adding a horizontal rule (b) before each heading would create a double-boundary effect (rule + heading) that is visually heavy and may cause the agent to over-segment its processing, treating each entry as more isolated than intended. When headings are off, the separator becomes critical — blank lines alone (a) may not create strong enough boundaries, and a horizontal rule (b) or double blank line (c) may be needed. Test: when headings are off, does separator strength affect entry-level processing quality?

**STABILITY:** Formatting (separator style). Conditional (interacts with the `example_display_headings` toggle — different behavior when headings are on vs off).

---

### Fragment 9: multi-group transition

**Data field:** None (structural, conditional on group count > 1)
**Purpose:** Signal the boundary between one calibration group and the next.

**Prose alternatives:**
- (a) No explicit transition. The next group heading is sufficient.
- (b) `---` horizontal rule between groups.
- (c) A transitional sentence: `The following examples address a different kind of judgment.`
- (d) Horizontal rule + transitional sentence.
- (e) Different heading level or style for subsequent groups (e.g., the first group gets a standard heading, subsequent groups get a prefixed heading like `### Also: Source Decontamination`).

**PURPOSE:** The multi-group transition is what makes the agent understand that it is shifting from one calibration context to another. If the summarizer had two groups ("Contextual Summarization" and "Source Decontamination"), the transition between them must signal: "you have finished calibrating one kind of judgment; now calibrate a different kind." Without an adequate transition, the agent may carry principles from the first group into the second — e.g., applying the "thin content" reasoning framework to decontamination examples where it does not apply.

This fragment only activates when there are 2+ groups. Neither current agent exercises this code path. But the design must anticipate it because the instructions-examples pairing principle implies multi-group structure as the ideal.

**HYPOTHESIS:** A horizontal rule (b) provides the cleanest visual break between groups. A transitional sentence (c) explicitly names the context shift but may feel like filler. The key question is whether group headings alone (a) provide sufficient cognitive separation. In a prompt where the agent has been processing "Contextual Summarization" entries and then encounters `### Source Decontamination`, does the heading alone create the mode-shift, or does the agent need an additional signal? This likely depends on how different the two calibration contexts are — very different contexts (summarizing vs decontaminating) may be self-separating, while similar contexts (summarizing short text vs summarizing long text) may need stronger boundaries. Test: in multi-group agents, does transition strength affect calibration bleed between groups?

**STABILITY:** Structural (transition mechanism). Conditional (only relevant for multi-group agents, which do not exist in current data).

---

### Fragment 10: single-group simplification

**Data field:** None (conditional on group count = 1)
**Purpose:** Determine whether a single-group agent suppresses the group heading level.

**Behavioral alternatives:**
- (a) Always render the full three-level hierarchy, even for single-group agents. H2 section heading, H3 group heading, H4 entry headings. Consistency across all agents.
- (b) Suppress the group heading for single-group agents. H2 section heading, then directly H4 entry headings (or H3 entry headings if the missing level is collapsed upward).
- (c) Suppress the group heading but render the group name as an epigraph or subtitle: `*Contextual Summaries*` below the section heading. The name is visible but not structural.
- (d) Promote entry headings to H3 when the group heading is suppressed. The hierarchy becomes: H2 section, H3 entries. No missing level.

**PURPOSE:** With one group, the group heading is technically redundant — the section heading already signals "examples" and the single group does not need disambiguation. But suppressing it changes the hierarchy depth and may affect how the agent perceives the structural weight of the section. An agent reading H2 > H3 > H4 perceives a deeply structured section with clear sub-organization. An agent reading H2 > H4 (with a gap) perceives an oddly structured section. An agent reading H2 > H3 (entries promoted) perceives a simple structured section.

**HYPOTHESIS:** The cleanest approach for single-group agents is (d): suppress the group heading and promote entries to H3. The agent sees `## Examples` followed by `### Standard substantive exchange`, `### Thin content with rich context`, etc. No redundant group heading, no hierarchy gap, and entries are visually prominent. This is what the current renderer approximately does (it renders group as H3 and entries as H4, which for a single group means H3 is an unnecessary intermediate level). The tradeoff: this means single-group and multi-group agents have different heading structures, which complicates the template. Test: for single-group agents, does suppressing the group heading improve content engagement (less structural noise) or reduce it (weaker organizational signal)?

**STABILITY:** Conditional (based on group count). Structural (affects heading hierarchy for the entire section).

---

## THE GOOD/BAD/WHY MECHANISM: BEHAVIORAL PROGRAMMING THROUGH CONTRAST

The GOOD/BAD/WHY pattern is not a formatting convention. It is the core behavioral programming mechanism of the examples section, and its design has consequences that ripple across the entire agent prompt.

### What Each Component Does

**GOOD output** establishes the target. It shows the agent one correct output for one specific input. In isolation, a GOOD example says "produce something like this." The agent may overgeneralize (produce this exact output for all inputs) or undergeneralize (only apply when the input exactly matches), but it has a quality target.

**BAD output** does something much more specific: it names the agent's *most probable mistake* for this input. "User makes a brief comment" is not a random wrong answer — it is the exact output an uncalibrated language model produces when given 5 words of input. "User confirms the approach to recursive knowledge architecture" is not a random wrong answer — it is the exact output an uncalibrated language model produces when given administrative text adjacent to substantive discussions. The BAD output is a prediction about the agent's default behavior.

This is why BAD examples are not just "wrong answers for contrast." They are **failure-mode fingerprints**. Each one identifies a specific attractor in the model's behavioral space. The agent encounters its own probable mistake, labeled as BAD, before encountering live data. This pre-exposure creates a recognition pattern: when the agent is about to produce the BAD output during processing, it has already seen that output labeled as wrong. The failure mode has been poisoned.

**WHY reasoning** converts the specific GOOD/BAD contrast into a transferable principle. "The text is 5 words, but the preceding exchanges built toward a distinction" — this is not about exchange 16 specifically. It is about any input where text length and contextual significance diverge. The WHY teaches the agent the *variable that governs the decision*, not the decision itself. Once the agent internalizes "context weight, not content length, determines summary depth," it can apply that principle to any input, not just the specific one shown.

### Template-Level Questions About the Pattern

The central design question: should the template be pattern-aware or pattern-blind?

**Pattern-blind** (opaque `example_text`): The template renders whatever is in the `example_text` field. If the author wrote "GOOD summary:" and "BAD summary:" as text, that is what appears. The template does not parse, recognize, or format these labels. The author controls the entire internal structure.

**Pattern-aware** (template recognizes GOOD/BAD/WHY): The template identifies GOOD/BAD/WHY labels within `example_text` and applies special formatting — perhaps visual emphasis on labels, different indentation for BAD outputs, or callout formatting for WHY blocks.

**Pattern-structural** (GOOD/BAD/WHY become separate fields): Instead of embedding the pattern in free-form text, each entry has structured fields: `example_input`, `example_good`, `example_bad` (optional), `example_why` (optional). The template controls the presentation of each component independently.

**Fragment 11: pattern_treatment**

**Prose alternatives:**
- (a) Opaque: render `example_text` as-is. The GOOD/BAD/WHY labels are just text.
- (b) Label recognition: scan `example_text` for lines starting with `GOOD`, `BAD`, `WHY`, `Note:`, `Wrong`, `Right` and apply bold formatting to the label.
- (c) Structural promotion: split `example_text` into separate fields in the data model. The template renders `example_input` as bare text, `example_good` with a `+` or checkmark prefix, `example_bad` with a `-` or cross prefix, `example_why` in italic or a callout.
- (d) Preamble-only awareness: the section preamble explains the GOOD/BAD/WHY vocabulary, but the template does not parse or format the labels within entries. The agent is told what the labels mean; the labels appear as authored text.

**PURPOSE:** This is the deepest design tension in the examples section. The opaque approach (a) preserves maximum author flexibility and is simplest to implement. But it means the most important behavioral programming mechanism — the GOOD/BAD/WHY contrast — has no visual distinction from any other text in the entry. The labels are just words. The template contributes nothing to making them effective.

The pattern-structural approach (c) is the most powerful: the template independently controls how GOOD, BAD, and WHY are presented, which means experiments can target "does emphasizing BAD outputs reduce failure-mode recurrence?" without changing the example content. But it constrains authors: every entry must decompose into input/good/bad/why, and entries that do not fit this pattern (the builder's Wrong/Right examples) need a different structure.

The preamble-only approach (d) is a middle ground: the template teaches the agent what the vocabulary means (via the section preamble) without parsing it. The labels remain authored text, but the agent has been primed to process them as calibration markers rather than arbitrary prefixes.

**HYPOTHESIS:** The preamble-only approach (d) may be the best balance. It invests the section preamble (Fragment 2) with the responsibility of installing the GOOD/BAD/WHY interpretive framework, then trusts the authored labels to work within that framework. This avoids parsing complexity, preserves author flexibility, and still ensures the agent knows what the labels mean. The structural approach (c) is more powerful but may over-constrain entry authoring — not every calibration demonstration fits the GOOD/BAD/WHY pattern (the builder's permission minimization example has Required/NOT required/conclusion, which is a different structure entirely). Test: does preamble priming plus authored labels produce equivalent calibration quality to structured fields with template-controlled formatting?

**STABILITY:** Structural (whether the template recognizes the pattern at all). This is a foundational architecture decision that constrains what the template can experiment with.

---

## THE INSTRUCTIONS-EXAMPLES PAIRING

This is the most important architectural relationship in the examples section, and it currently exists only in intent, not in data or rendering.

The principle: each probabilistic instruction step describes a cognitive task that requires judgment. Each example group should calibrate that judgment with demonstrations. The pairing makes examples targeted — instead of "here are some examples for the whole agent," the structure says "here are examples specifically for the judgment you exercise in step N."

### Current State of the Pairing

**Summarizer instruction steps:**
1. (deterministic) Read input, process in order, one record per input
2. (probabilistic) Contextual summarization — significance in context, thin content disambiguation
3. (deterministic) One sentence per exchange
4. (probabilistic) Session transition handling
5. (probabilistic) Source decontamination — TRANSFERRED and RECONSTRUCTED markers

**Summarizer example entries (all in one group "Contextual Summaries"):**
- "Standard substantive exchange" -> maps to step 2
- "Thin content with rich context" -> maps to step 2
- "Thin content with thin context" -> maps to step 2
- "Transferred content decontamination" -> maps to step 5
- "Reconstructed content decontamination" -> maps to step 5

Step 4 (session transitions) has no calibration examples. Steps 2 and 5 are calibrated but lumped in one group. The ideal structure would have at least two groups: one for contextual summarization (entries 1-3) and one for decontamination (entries 4-5), with a potential third for session transitions.

**Builder instruction steps:**
1. (deterministic) Read preparation package and context
2. (probabilistic) Identify core domain, write role fields
3. (probabilistic) Design instruction steps
4. (probabilistic) Create calibration examples
5. (probabilistic) Write guardrails
6. (probabilistic) Write success/failure criteria
7. (deterministic) Map structured fields, set security, validate

**Builder example entries (all in one group "Definition Design"):**
- "Designing Instruction Steps From Requirements" -> maps to step 3
- "Minimum Required Permissions" -> maps to step 7

Steps 2, 4, 5, 6 have no calibration examples. The two entries target different cognitive tasks (creative design vs mechanical mapping) and should arguably be in separate groups.

### Template Fragments for the Pairing

**Fragment 12: pairing_visibility**

**Prose alternatives:**
- (a) Implicit pairing. No explicit link between groups and steps. The group name suggests the connection; the agent infers the rest.
- (b) Forward reference from example group to instruction step: `These examples calibrate your judgment for Step {N}.` rendered as the group framing sentence (Fragment 4c).
- (c) Back-reference from instruction step to example group: `(See examples: {group_name})` appended to probabilistic instruction steps. This puts the link in the instructions section, not the examples section.
- (d) Positional correspondence. Example groups are rendered in the same order as their paired instruction steps. No explicit reference, but the order signals the mapping.
- (e) Bidirectional. Both forward and back references. The group says "this calibrates step N" and the step says "see examples: group_name."

**PURPOSE:** The pairing is what makes examples a calibration system rather than a sample collection. Without any pairing signal, the agent must infer "these decontamination examples are relevant when I am executing the decontamination step." With an explicit signal, the agent has a direct link: "step 5 tells me to see the decontamination examples."

This is a cross-section dependency: the examples section needs to reference instruction step numbers, or the instructions section needs to reference example group names. Either way, one section must know about the other's content.

**HYPOTHESIS:** The back-reference (c) is probably more powerful than the forward reference (b), because the agent encounters the link at the moment it is most useful — while reading the instruction step it is about to execute. A forward reference ("this calibrates step 5") requires the agent to remember the link when it later encounters step 5, which is a working-memory demand. A back-reference ("see examples: Source Decontamination") gives the agent the link at the point of use. Bidirectional (e) is the most complete but also the most maintenance-heavy. Positional (d) is elegant but fragile. Implicit (a) is what currently exists and works when group names clearly echo step content, but fails when the mapping is non-obvious. Test: does back-referencing from instruction steps to example groups improve per-step calibration quality? Is the improvement worth the cross-section coupling?

**STABILITY:** Structural (whether pairing is visible at all). Cross-section (requires data flow between instructions and examples sections). Experimental (the mechanism of visibility).

---

**Fragment 13: uncalibrated_step_acknowledgment**

**Prose alternatives:**
- (a) No acknowledgment. Steps without matching example groups proceed with uncalibrated judgment. The agent is not told about the gap.
- (b) A section-level note: `Not all judgment steps have dedicated examples. For steps without examples, apply the principles demonstrated in the available examples.`
- (c) Per-step flagging: uncalibrated probabilistic instruction steps get a note like `(No calibration examples provided for this step.)` in the instructions section.
- (d) Implicit through completeness: if every probabilistic step has a paired group, this fragment never activates. The gap only exists when the definition is incomplete.

**PURPOSE:** The gap between "every probabilistic step should have calibration examples" and "these definitions only have examples for some steps" needs handling. The question is whether drawing attention to uncalibrated steps helps (the agent is more careful) or hurts (the agent is less confident).

**HYPOTHESIS:** Acknowledging the gap (b) with a generalization instruction ("apply the principles demonstrated in the available examples") is probably better than silence (a), because it explicitly tells the agent to extrapolate rather than to assume uncalibrated steps need no judgment calibration. The per-step flag (c) is too heavy — it draws repeated attention to what is missing rather than helping the agent work with what is present. Test: does acknowledging uncalibrated steps with a generalization instruction improve quality on those steps?

**STABILITY:** Experimental (uncertain behavioral effect). Conditional (only relevant when the pairing is incomplete).

---

## CROSS-SECTION DEPENDENCIES

### Examples and Anti-Patterns

The BAD examples and the anti-patterns section describe the same behavioral boundaries from different perspectives. Anti-pattern: "Do not invent significance for administrative exchanges." BAD example: "User confirms the approach to recursive knowledge architecture discussed over the prior twelve exchanges, marking a conceptual milestone." These are the same prohibition — one as a rule, one as a demonstration.

**Fragment 14: anti_pattern_coordination**

- (a) No coordination. The redundancy is intentional — abstract rule + concrete demonstration produces stronger behavioral programming than either alone.
- (b) Examples reference anti-patterns: `(Anti-pattern: Do not invent significance...)` after BAD outputs.
- (c) Anti-patterns reference examples: `(Demonstrated in example: Thin content with thin context)` after relevant anti-patterns.

**PURPOSE:** The question is whether the redundancy needs coordination or whether uncoordinated redundancy is the correct design. If the agent encounters the same prohibition as both a rule and a demonstration, does it process them as reinforcing (same thing said twice = stronger signal) or as independent pieces of information that it must reconcile?

**HYPOTHESIS:** Uncoordinated redundancy (a) is probably correct. The rule and the demonstration operate through different mechanisms — the rule states a prohibition declaratively, the demonstration shows the violation concretely. They reinforce each other without the agent needing to know they are related. Coordination (b/c) makes the relationship explicit but adds maintenance burden and may be unnecessary. Test: is uncoordinated reinforcement measurably less effective than coordinated cross-referencing?

**STABILITY:** Structural (whether cross-references exist). Low-priority — the uncoordinated approach is likely correct.

### Examples and Success Criteria

Success criteria describe what correct output looks like at the section level. Examples show what correct output looks like at the case level. The summarizer's success criterion "Thin-content-rich-context exchanges have summaries reflecting accumulated conversational significance" is precisely demonstrated by the "Thin content with rich context" entry.

**Fragment 15: success_criteria_grounding**

- (a) No explicit grounding. The agent implicitly connects examples to success criteria.
- (b) A note in the examples preamble: `These examples demonstrate the quality standards described in your success criteria.`

**PURPOSE:** Makes explicit what is likely implicit. The agent probably already connects "success criterion says do X" with "example shows X done correctly" without being told. The question is whether explicit grounding adds value or just adds noise.

**HYPOTHESIS:** Implicit grounding (a) is probably sufficient. The overlap between examples and success criteria is natural and obvious enough that the agent does not need help connecting them. Explicit grounding (b) is low-risk but low-reward. Not a high-priority design concern.

**STABILITY:** Experimental (low-priority).

---

## STRUCTURAL: Section Position in the Agent Prompt

**Fragment 16: section_ordering**

**Alternatives:**
- (a) Examples immediately after instructions. The natural reading: "here is what to do" followed by "here is what doing it well looks like."
- (b) Examples after constraints and anti-patterns. The agent absorbs prohibitions first, then sees examples that demonstrate the boundaries those prohibitions describe.
- (c) Examples at the end of the prompt (reference position). The agent processes all operational sections first, then encounters examples as a final calibration pass.
- (d) Examples interleaved with instruction steps. Each probabilistic step is immediately followed by its calibration examples. This maximizes pairing proximity but destroys the self-contained examples section.

**PURPOSE:** Where the examples section appears determines when the agent absorbs calibration material relative to other information. Immediately-after-instructions (a) means the agent calibrates its judgment before encountering constraints, anti-patterns, or output format rules. After-anti-patterns (b) means the agent has both procedural knowledge (instructions) and prohibition knowledge (anti-patterns) before encountering calibration, which may strengthen the BAD example recognition — "I was told not to invent significance, and here is what inventing significance looks like."

**HYPOTHESIS:** After-instructions (a) is the most natural position and ensures calibration happens while procedural knowledge is freshest in the agent's processing. After-anti-patterns (b) is interesting because it pairs prohibitions with demonstrations, but it delays calibration and interposes non-calibration material between instructions and examples. Interleaved (d) is the strongest pairing but is architecturally incompatible with the section-based prompt structure. End-of-prompt (c) risks the agent treating examples as optional reference rather than mandatory calibration. Test: does proximity between instructions and examples affect calibration quality?

**STABILITY:** Structural (section ordering is an architectural decision). Cross-section (the position relative to other sections affects all of them).

---

## SYNTHESIS: The Design Tensions

The examples section has three fundamental design tensions that all other fragment decisions express:

### Tension 1: Structured vs. Opaque Content

Should the template know about the internal structure of examples (GOOD/BAD/WHY patterns, input/output blocks) or treat `example_text` as an opaque blob? Structured knowledge enables targeted formatting experiments. Opacity preserves author flexibility and simplifies the template. The resolution likely lies in the preamble-only approach: teach the agent the vocabulary, let the author use it freely.

### Tension 2: Explicit vs. Implicit Pairing

Should the instructions-examples link be rendered (cross-references, matching order) or left for the agent to infer? Explicit pairing is more powerful but creates cross-section coupling. Implicit pairing is simpler but relies on naming conventions. The resolution depends on whether multi-group structure becomes common enough to justify the maintenance cost.

### Tension 3: Hierarchy Depth vs. Visual Simplicity

The three-level hierarchy (section, group, entry) is architecturally meaningful for multi-group agents but potentially noisy for single-group agents. Collapsing the hierarchy for simple cases reduces chrome but creates inconsistency. The resolution involves a conditional path: single-group agents suppress the group heading and promote entries; multi-group agents render the full hierarchy.

### The Highest-Leverage Fragments

If forced to rank by behavioral impact:

1. **Section preamble** (Fragment 2) — configures how the agent processes ALL subsequent examples. Gets one chance to install the GOOD/BAD/WHY framework, the generalization instruction, and the calibration mindset.

2. **Pattern treatment** (Fragment 11) — whether the template is pattern-blind, pattern-aware, or uses structural fields determines the entire experimental surface for calibration effectiveness.

3. **Entry heading naming convention** (Fragment 6) — not a template choice, but the template's documentation should guide authors on skill-naming vs condition-naming and when to use each.

4. **Pairing visibility** (Fragment 12) — the connection between examples and instructions is the architectural justification for the entire section. Making it visible (especially via back-references from instruction steps) is the highest-leverage cross-section fragment.

5. **Single-group simplification** (Fragment 10) — for the common case (most current agents), this determines whether the section feels over-engineered or appropriately structured.
