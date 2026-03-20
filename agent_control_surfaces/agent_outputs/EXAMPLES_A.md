# Examples Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The examples section is a **calibration system**. Not a collection of samples. Not a reference appendix. A system that configures the agent's judgment for specific cognitive tasks by showing it decision boundaries — the exact points where one correct response diverges from another.

This distinction matters because it determines the entire presentation design. If examples are "samples," you display them as a reference list. If examples are a calibration system, you present them as a structured training sequence where the agent must internalize patterns of judgment before encountering live data.

To understand what calibration means here: the instructions section tells the agent *what to do*. The examples section tells the agent *what doing it well looks like, what doing it badly looks like, and what distinguishes the two*. Instructions configure procedure. Examples configure the quality threshold within each procedure step. An agent with perfect instruction compliance but no example calibration will execute the right steps with uncalibrated judgment — it will summarize, but summarize badly; it will assess, but assess against wrong standards.

The examples section must accomplish three things:

1. **Decision boundary marking** — Each example shows where one treatment ends and another begins. The "thin content with rich context" vs "thin content with thin context" pair in the summarizer demonstrates the exact boundary: both inputs are short text, but one carries accumulated conversational weight and the other does not. The agent must learn to distinguish these, and the only way to teach that distinction is to show both sides of the boundary.

2. **Failure mode inoculation** — The BAD examples are not failures to avoid — they are *specific attractors in the agent's default behavior*. LLMs default to certain failure modes: inflating significance, taking text at face value, producing thin output for thin input regardless of context. The BAD examples name these attractors explicitly and demonstrate why they fail. The WHY reasoning creates a cognitive pathway from "I am about to do this" to "this is the known failure mode." Without the BAD examples, the agent has no reference for what its own mistakes look like.

3. **Judgment calibration per cognitive task** — Different probabilistic instruction steps require different kinds of judgment. Summarizing a standard exchange requires different calibration than decontaminating a reconstructed exchange. The examples section must separately calibrate each kind of judgment the agent will exercise. This is the **instructions-examples pairing**: each example group should ideally correspond to one or more probabilistic instruction steps.

### What the defective renderer currently does

Unknown from the provided data — the raw `anthropic_render.toml` files contain the data but I have no rendered output to compare against. The analysis proceeds from the data alone, designing the presentation from first principles.

### The three-level hierarchy

The examples section has an inherent structure deeper than any other section:

```
examples (section level)
  └── groups (calibration units)
       └── entries (individual decision boundary demonstrations)
```

This hierarchy is not incidental. It exists because a single agent may exercise multiple kinds of judgment, and each kind requires independent calibration. The builder agent's one group ("Definition Design") covers two very different skills (instruction decomposition and permission minimization) — arguably these should be separate groups. The summarizer's one group ("Contextual Summaries") covers standard summarization, thin/rich disambiguation, and decontamination — at least two distinct cognitive tasks.

The hierarchy is the architectural expression of the instructions-examples pairing principle. It is a first-class structural concern, not a formatting convenience.

---

## STRUCTURAL: section_heading
TYPE: n/a

### What the agent needs to understand

The section heading tells the agent it is transitioning from operational instructions into calibration material. The heading must signal: "What follows is not more instructions. It is worked examples that show you how to exercise the judgment the instructions require."

This transition is critical because the agent's processing mode must shift. During instructions, the agent is absorbing procedure. During examples, the agent is absorbing standards of quality. The heading must trigger that mode shift.

### Fragments

**section_heading_text**
- Alternative A: `## Examples` — neutral, minimal. Signals section transition without framing the content's purpose.
- Alternative B: `## Calibration Examples` — names the purpose. The word "calibration" tells the agent these examples exist to tune its judgment, not merely to illustrate format.
- Alternative C: `## Reference Examples` — frames examples as something to consult during processing, like a lookup table.
- Alternative D: `## Worked Examples` — frames examples as demonstrations of completed reasoning, not just input-output pairs. Implies the agent should study the reasoning process, not just memorize the outputs.
- Alternative E: `## How to Apply Your Judgment` — bypasses the word "examples" entirely. Frames the section as behavioral guidance rather than a sample collection.
- PURPOSE: The heading primes the agent's processing mode for the entire section. "Examples" says "here are some samples." "Calibration Examples" says "here is material that configures your judgment." "Worked Examples" says "here are demonstrations to learn from." The difference matters because the agent may process samples passively (store and move on) but process calibration material actively (internalize and apply).
- HYPOTHESIS: "Calibration" is a technical term that may not shift behavior in most models — the model may not have strong associations with the word in this context. "Worked Examples" is more universally understood as "study these demonstrations" and may produce deeper engagement with the example content. "Reference" may cause the agent to defer looking at the examples until it needs them during processing, rather than internalizing them upfront. Test: does the heading affect how deeply the agent engages with example content before beginning its task? Does "calibration" produce different behavior than "worked" or "reference"?
- STABILITY: structural (heading presence and level) + experimental (heading text choice)

---

## STRUCTURAL: section_preamble
TYPE: n/a

### What the agent needs to understand

Before any example groups, the agent may need framing that explains what the examples are for and how to use them. This is particularly important because the examples section serves a fundamentally different purpose than every other section — it is teaching by demonstration rather than by instruction.

### Fragments

**examples_section_intro**
- Alternative A: No preamble — the section heading is followed immediately by the first group heading. The examples speak for themselves.
- Alternative B: `The following examples demonstrate decision boundaries for the judgments you must make. Study the reasoning, not just the outputs.` — brief framing that tells the agent what to extract from the examples.
- Alternative C: `Each example group calibrates a specific aspect of your judgment. GOOD outputs show correct treatment. BAD outputs show common failure modes. WHY explains the distinction.` — structural guide that names the GOOD/BAD/WHY pattern so the agent knows what to look for.
- Alternative D: A preamble that explicitly connects examples to instructions: `These examples correspond to the judgment tasks described in your instructions. Each group demonstrates how to exercise the judgment required by one or more of your processing steps.` — makes the instructions-examples pairing explicit.
- Alternative E: `When you encounter an input similar to these examples during processing, apply the same reasoning. The examples are not exhaustive — they mark the boundaries of correct judgment. Inputs that fall between example cases should be handled by interpolating between the demonstrated principles.` — frames examples as boundary markers and tells the agent how to generalize.
- PURPOSE: Decides whether the agent discovers the examples' purpose organically (no preamble) or whether it is told upfront what to extract from them. Also determines whether the instructions-examples pairing is explicit or implicit, and whether the GOOD/BAD/WHY pattern is explained or left for the agent to infer.
- HYPOTHESIS: No preamble (A) is cleanest but risks the agent scanning examples passively — storing them as reference rather than actively calibrating. The structural guide (C) is most explicit and ensures the agent processes the GOOD/BAD/WHY pattern as a deliberate teaching mechanism. The connection to instructions (D) strengthens the pairing but may be redundant if group names already signal the connection. The generalization instruction (E) is the most ambitious — it tells the agent how to extrapolate from examples to novel inputs, which is the actual purpose of calibration. Test: does explaining the GOOD/BAD/WHY pattern upfront increase the agent's attention to WHY reasoning? Does the generalization instruction (E) improve handling of edge cases not covered by examples?
- STABILITY: experimental (whether to include and what to say) + structural (presence/absence decision)

---

## FIELD: example_group_name
TYPE: string
OPTIONAL: no
VALUES: "Definition Design" / "Contextual Summaries"

### What the agent needs to understand

The group name identifies what kind of judgment the following entries calibrate. It is the label for a calibration unit. The agent should read "Contextual Summaries" and understand: "The examples that follow will show me how to produce contextual summaries — this is calibration for my summarization judgment."

This field carries more architectural weight than a simple label. It is the name of a cognitive skill the agent possesses. When there are multiple groups, the group names collectively define the agent's **judgment repertoire** — the set of distinct cognitive tasks it has been calibrated for.

In the current data, both agents have a single group. But the design must support multiple groups per agent. The builder agent could plausibly have separate groups: "Instruction Step Design" and "Permission Minimization." The summarizer could have: "Contextual Summarization," "Thin Content Disambiguation," and "Source Decontamination." The fact that these are lumped into single groups is arguably a deficiency in the current definitions, not a design constraint.

### Fragments

**group_heading**
- Alternative A: `### Definition Design` — H3 heading, group name as-is. Creates a visible sub-section within the examples section.
- Alternative B: `### Examples: Definition Design` — prefixed heading that reinforces the section context. Useful when multiple groups create navigation structure.
- Alternative C: `### Calibration: Definition Design` — prefixed heading that names the group's purpose as calibration. Stronger framing than "Examples."
- Alternative D: `**Definition Design**` — bold text, no heading. Reduces visual hierarchy, treats the group as a labeled block rather than a sub-section.
- Alternative E: No group heading when there is only one group — the section heading is sufficient. Group headings only appear when there are 2+ groups.
- PURPOSE: Creates the intermediate level of the three-level hierarchy. The group heading tells the agent it is entering a calibration context for a specific kind of judgment. The heading level, prefix, and conditional presence all affect how the agent perceives group boundaries and the shift between calibration contexts.
- HYPOTHESIS: H3 headings (A/B/C) create strong group boundaries — the agent clearly perceives the transition between calibration contexts. Bold text (D) creates weaker boundaries, which may cause the agent to treat all examples as one calibration mass rather than distinct units. Conditional presence (E) reduces noise for single-group agents but requires the template to distinguish single vs. multi-group cases. Test: when there are multiple groups, does heading-level group separation produce better per-group calibration adherence than bold-text separation? For single-group agents, does omitting the group heading reduce the agent's sense that calibration is structured?
- STABILITY: structural (heading level, presence) + conditional (single vs. multi-group) + experimental (prefix choice)

**group_framing_sentence**
- Alternative A: No framing — the group heading is followed immediately by the first entry.
- Alternative B: `The following examples demonstrate {group_name_lowercased}:` — simple transitional sentence that leads into the entries.
- Alternative C: A per-group sentence that connects the group to its corresponding instruction step(s): `These examples calibrate the judgment required in Step {N}: {instruction_summary}.` — makes the pairing explicit and traceable.
- Alternative D: `{N} examples follow:` — bare count, no framing. Gives the agent a completion target.
- PURPOSE: Decides whether the agent knows what it is about to be calibrated for (beyond the heading), whether the instructions-examples pairing is rendered per-group, and whether entry count is visible.
- HYPOTHESIS: The instruction-step link (C) is the most powerful because it tells the agent exactly which operational step benefits from this calibration. But it requires cross-section data access (instruction step numbers and summaries), which complicates the template. Simple framing (B) is neutral. No framing (A) is cleanest. Count (D) may cause completionist behavior — the agent processes all N entries mechanically rather than deeply. Test: does per-group instruction linking improve the agent's application of calibrated judgment during the linked instruction step?
- STABILITY: experimental (whether to include) + conditional (content depends on instruction step mapping) + structural (if instruction linking is chosen, the cross-section dependency becomes an architectural constraint)

---

## FIELD: example_display_headings
TYPE: boolean
OPTIONAL: no (present on every group)
VALUES: true / true (both agents use true)

### What the agent needs to understand

This boolean controls whether individual example entries within a group have visible headings. When true, each entry has a heading (e.g., "Standard substantive exchange," "Thin content with rich context"). When false, entries are presented without per-entry headings.

This is a **display mode toggle**, not a content field. It determines whether the examples are a titled sequence (each entry is a named scenario) or an untitled flow (entries merge into a continuous calibration stream).

### Fragments

**heading_toggle_behavior**
- When true: each entry renders with its `example_heading` as a visible heading (see entry heading fragments below).
- When false: entries render without per-entry headings, separated only by whitespace or a delimiter.
- PURPOSE: Controls whether the agent perceives each example as a named, individually addressable scenario or as one entry in an undifferentiated stream.
- HYPOTHESIS: Named scenarios (headings on) give the agent a cognitive hook for each example — it can think "this is the thin-content-rich-context case" during processing. Unnamed entries (headings off) force the agent to derive the pattern from the example content itself, which may produce deeper engagement but weaker recall. Named scenarios also enable the agent to reference specific examples during reasoning ("as in the reconstructed content case..."). Test: do agents with named examples demonstrate better application of specific example lessons to matching input cases? Does naming create an over-indexing risk where the agent only applies examples to inputs that match the heading rather than generalizing the principle?
- STABILITY: formatting (whether headings appear) — this is a per-group display mode decision

---

## FIELD: example_heading
TYPE: string
OPTIONAL: conditional (only rendered when example_display_headings = true)
VALUES: "Designing Instruction Steps From Requirements", "Minimum Required Permissions", "Standard substantive exchange", "Thin content with rich context", "Thin content with thin context", "Transferred content decontamination", "Reconstructed content decontamination"

### What the agent needs to understand

The example heading names the scenario, the decision boundary, or the skill being demonstrated by one entry. It is a cognitive anchor — a short phrase that the agent can hold in working memory and retrieve when encountering a similar input during processing.

Critically, the heading names are doing two different things across the two agents:

- Builder headings name **skills**: "Designing Instruction Steps From Requirements" (a skill), "Minimum Required Permissions" (a concept to apply).
- Summarizer headings name **input conditions**: "Standard substantive exchange" (what the input looks like), "Thin content with rich context" (what the input looks like), "Reconstructed content decontamination" (what the input contains).

This is a meaningful design divergence. Skill-named headings tell the agent "here is how to do X." Condition-named headings tell the agent "here is what to do when you encounter Y." Both are valid, but they prime different retrieval patterns. A skill-named heading triggers recognition of "I need to apply skill X." A condition-named heading triggers recognition of "my input matches condition Y."

### Fragments

**entry_heading_display**
- Alternative A: `#### Standard substantive exchange` — H4 heading, creating the third level of the heading hierarchy (section H2, group H3, entry H4).
- Alternative B: `**Standard substantive exchange**` — bold text, no heading level. Reduces visual hierarchy, keeps entries visually subordinate to the group.
- Alternative C: `**Example: Standard substantive exchange**` — prefixed bold text that labels the entry as an example.
- Alternative D: `_Standard substantive exchange_` — italic, visually softer. Positions the heading as a descriptor rather than a title.
- Alternative E: `--- Standard substantive exchange ---` — delimiter-framed heading, creates visual separation between entries without using markdown heading levels.
- PURPOSE: Creates the innermost level of the three-level hierarchy. The heading level, formatting, and prefix all affect how the agent perceives entry boundaries and whether it treats each example as a discrete unit or as part of a continuous flow.
- HYPOTHESIS: H4 headings (A) create the strongest entry boundaries and the most navigable structure, but in a long examples section they may create visual noise. Bold text (B) is the most common markdown pattern for sub-sub-headings and is familiar without being structurally heavy. The "Example:" prefix (C) is redundant (we are already in the examples section) but may help agents that lose context in long prompts. Italic (D) is visually subordinate enough that the agent may not perceive it as a boundary marker. Delimiters (E) create the clearest visual separation but are not standard markdown and may be parsed differently by different models. Test: does heading level affect the agent's ability to recall and reference specific examples during processing? Do H4 headings improve entry-by-entry recall compared to bold text?
- STABILITY: formatting (heading level/style) + structural (hierarchy depth decision)

**entry_separator** (when headings are off)
- Alternative A: Blank line between entries — minimal separation, entries run together.
- Alternative B: `---` horizontal rule between entries — strong visual break.
- Alternative C: Numbered entries: `1. {entry_text}`, `2. {entry_text}` — entries become an ordered list.
- Alternative D: Double blank line between entries — stronger than single blank line, weaker than horizontal rule.
- PURPOSE: When headings are disabled, something must still separate entries. The separator choice determines whether the agent perceives entries as distinct units or as a continuous stream.
- HYPOTHESIS: Blank lines (A) are weak separators — the agent may merge adjacent entries into one example. Horizontal rules (B) are the strongest markdown separator and clearly delineate entries. Numbering (C) adds sequence and count awareness. Double blanks (D) are a compromise. Test: when headings are off, does entry separation affect the agent's ability to process each entry independently?
- STABILITY: formatting (separator style) + conditional (only active when example_display_headings = false)

---

## FIELD: example_text
TYPE: string (multi-line, free-form)
OPTIONAL: no
VALUES: see raw data above — varies from 5 lines to 20+ lines

### What the agent needs to understand

This is the body of each example entry — the actual calibration content. It is the most complex field in the entire examples section because it has no fixed internal structure. The field is free-form multi-line text, but the author-written content follows recurring patterns that the presentation system must support without constraining.

### Internal patterns observed in the raw data

Studying the two agents' example texts reveals distinct internal structures:

**Pattern 1: Input -> GOOD output -> reasoning** (builder examples, summarizer "standard" and "transferred" examples)
```
[input scenario or context]
[GOOD output with label]
[brief reasoning note]
```

**Pattern 2: Input -> GOOD output -> BAD output -> WHY** (summarizer "thin content" and "reconstructed" examples)
```
[input scenario or context]
[GOOD output with label]
[BAD output with label]
[WHY: explanation of the distinction]
```

**Pattern 3: Wrong -> Right** (builder instruction decomposition example)
```
[requirement]
[Wrong approach with label]
[Right approach with label]
[concluding principle]
```

**Pattern 4: Required -> NOT required -> conclusion** (builder permissions example)
```
[scenario]
[what is required, with items]
[what is NOT required, with items and reasons]
[concluding principle]
```

These patterns are not template-generated — they are author-written content within the `example_text` field. The template system does NOT control the internal structure of example_text. However, the template system's surrounding presentation (headings, separators, entry containers) affects how the agent processes this internally structured content.

### Fragments

**example_text_presentation**
- Alternative A: Bare text — the example_text is rendered as-is with no wrapping. Whatever the author wrote is what the agent sees.
- Alternative B: Each example_text wrapped in a blockquote: `> {line1}\n> {line2}\n...` — visually distinguishes example content from surrounding structural prose.
- Alternative C: Each example_text in a fenced block (but not a code block): some kind of container that creates visual boundaries without implying the content is code.
- Alternative D: Bare text with an explicit entry-end marker: the text is followed by a delimiter or blank space that clearly terminates the entry before the next one begins.
- PURPOSE: Controls whether example text is visually contained or flows openly. Containment helps the agent perceive where one example ends and the next begins. Open flow is cleaner but may cause boundary confusion with long entries.
- HYPOTHESIS: Bare text (A) is highest-fidelity — the agent sees exactly what the author wrote. But for long examples (the reconstructed content entry is ~10 lines), bare text may blur into the surrounding structure. Blockquotes (B) create clear containment at the cost of visual density. Fenced blocks (C) are the strongest container but may trigger "code processing" mode in the agent. An end marker (D) is a compromise — the text flows freely but has a definitive endpoint. Test: for agents with 5+ entries and varying entry lengths, does containment reduce entry-boundary confusion?
- STABILITY: formatting (container choice) — this decision applies uniformly to all entries

---

## STRUCTURAL: GOOD/BAD/WHY pattern
TYPE: n/a (this is an internal pattern within example_text, not a field)

### What the agent needs to understand

The GOOD/BAD/WHY pattern is the core mechanism of the calibration system. It does not just show the agent correct output — it shows it the boundary between correct and incorrect, and explains why the boundary exists where it does. This is what makes examples a calibration system rather than a sample collection.

The pattern has three components:

1. **GOOD output** — what the correct response looks like for this input. Labeled explicitly ("GOOD summary:", "Right —").
2. **BAD output** — what the attractive-but-wrong response looks like. Labeled explicitly ("BAD summary:", "Wrong —"). This is the failure attractor — the response the agent would produce if uncalibrated.
3. **WHY** — the reasoning that explains the distinction. This is the most important component because it teaches the agent the *principle* behind the distinction, not just the specific case.

Not all entries use the full pattern. Some entries are GOOD-only (the "standard substantive exchange" and "transferred content" entries have GOOD output and a "Note:" but no BAD/WHY). This creates a spectrum:

- **GOOD-only entries** demonstrate baseline correct behavior — "this is how to handle the normal case."
- **GOOD/BAD/WHY entries** demonstrate decision boundaries — "this is where the normal case stops and a different treatment begins."

The entries with BAD/WHY are doing heavier calibration work. They are inoculating the agent against specific failure modes. The GOOD-only entries are establishing the baseline that the GOOD/BAD/WHY entries modify.

This is not a formatting choice — it is a behavioral programming mechanism. The question for the template system is: does the template need to recognize and support this pattern, or does it treat example_text as opaque?

### Fragments

**pattern_recognition_in_template**
- Alternative A: The template treats example_text as fully opaque — no recognition of GOOD/BAD/WHY labels. The author is responsible for all internal formatting. The template provides containment, headings, and separators, nothing more.
- Alternative B: The template recognizes GOOD/BAD labels and applies visual emphasis — e.g., GOOD lines get a green-tinted blockquote or bold prefix, BAD lines get a red-tinted prefix. This requires the template to parse example_text for known label patterns.
- Alternative C: GOOD, BAD, and WHY become separate fields on each entry instead of being embedded in example_text. The template then controls the presentation of each component independently.
- Alternative D: The template adds a structural preamble that explains the pattern before the first entry: `Examples may show GOOD and BAD outputs. GOOD outputs demonstrate correct judgment. BAD outputs demonstrate common failure modes. WHY explains the distinction.` — the template teaches the agent the pattern vocabulary.
- PURPOSE: Decides whether the GOOD/BAD/WHY pattern is a template-level concern (the template knows about it and presents it) or an authorial concern (the template is blind to it, the author handles it within free-form text).
- HYPOTHESIS: Treating example_text as opaque (A) is simplest and preserves maximum author flexibility. It means some entries will have GOOD/BAD/WHY and others will not, and the template does not care. But this means the labels "GOOD" and "BAD" are just text — they have no visual distinction and the agent may not process them as labels. Promoting GOOD/BAD/WHY to separate fields (C) gives the template full control but constrains author flexibility — every entry must fit the pattern. The preamble approach (D) is a middle ground — the template explains the pattern vocabulary without parsing the text. Test: does visual emphasis on GOOD/BAD labels increase the agent's attention to the distinction? Does breaking them into separate fields produce better calibration than embedded labels?
- STABILITY: structural (whether the template is pattern-aware) + experimental (if pattern-aware, how to render)

**why_reasoning_emphasis**
- Alternative A: WHY reasoning rendered as-is within the example_text — no special treatment.
- Alternative B: WHY sections rendered in italic or a distinct style to visually separate the reasoning from the demonstration. Helps the agent distinguish "here is what to do" from "here is why."
- Alternative C: WHY sections rendered as a callout or aside: `> **Why:** {reasoning}` — makes the reasoning visually prominent and structurally distinct.
- PURPOSE: The WHY reasoning is where the agent learns the *principle* behind the decision boundary. If it blends visually into the GOOD/BAD demonstration, the agent may process it as more example rather than as meta-reasoning about examples.
- HYPOTHESIS: Visual distinction for WHY sections may help the agent extract and retain the principle separately from the specific example. Without distinction, the reasoning merges into the example flow and may be treated as "more example content" rather than as transferable logic. Test: do agents that receive visually distinguished WHY reasoning demonstrate better generalization to novel inputs?
- STABILITY: experimental (high-leverage if the GOOD/BAD/WHY pattern is template-aware) + conditional (only relevant for entries that contain WHY blocks)

---

## STRUCTURAL: single_group vs. multi_group
TYPE: conditional branch

### What the agent needs to understand

An agent may have one example group or many. This is a first-class structural decision because it determines whether the examples section is monolithic or segmented. The two agents in the data both have a single group, but the design must accommodate multiple groups.

The behavioral difference is significant:

- **Single group:** All examples live in one calibration context. The agent processes them as one stream of demonstrations. There is no structural signal that different entries calibrate different skills.
- **Multiple groups:** Each group is a distinct calibration context. The agent transitions between calibration contexts, and the group structure tells it "you need these different kinds of judgment, and each is independently calibrated."

### Fragments

**multi_group_transition**
- Alternative A: No explicit transition — group headings create the boundary. The agent reads `### Contextual Summarization`, processes those entries, then reads `### Source Decontamination` and processes those.
- Alternative B: A transitional sentence between groups: `The following examples address a different aspect of your judgment:` — explicit signal of context shift.
- Alternative C: A horizontal rule `---` between groups — visual break without prose.
- Alternative D: Group numbering: `### Group 1: Contextual Summarization`, `### Group 2: Source Decontamination` — numbered groups signal sequence and count.
- PURPOSE: Controls how strongly the agent perceives the shift between calibration contexts. Weak transitions may cause bleed — the agent still thinking about contextual summarization principles while reading decontamination examples. Strong transitions create clean cognitive breaks.
- HYPOTHESIS: For agents with 2-3 groups, heading-only transitions (A) are probably sufficient. For agents with 4+ groups, the agent may lose track of which calibration context it is in, and stronger transitions (B/D) help. Numbering (D) gives the agent a count and position, which aids working memory. Test: for multi-group agents, does transition strength correlate with calibration adherence per-group?
- STABILITY: structural (transition mechanism) + conditional (only relevant for multi-group agents)

**single_group_simplification**
- Alternative A: Single-group agents render exactly like multi-group agents — with group heading and full hierarchy. Consistency over brevity.
- Alternative B: Single-group agents suppress the group heading — the examples section heading is followed directly by entries. The group name still exists in data but does not add a heading level, reducing hierarchy depth from 3 to 2.
- Alternative C: Single-group agents suppress the group heading but keep the group name as a subtitle or epigraph: `*Contextual Summaries*` — visible but not structural.
- PURPOSE: Decides whether the three-level hierarchy collapses to two when there is only one group. This affects visual complexity and whether the agent perceives a single-group examples section as structured or flat.
- HYPOTHESIS: Suppressing the group heading for single-group agents (B) reduces unnecessary hierarchy — the agent does not need to navigate sub-sections when there is only one. But it creates inconsistency: agents with one group look different from agents with two. Consistent rendering (A) means every agent has the same structure regardless of group count, which simplifies the template but adds visual noise for simple cases. Test: does suppressing the single-group heading reduce calibration engagement (the agent treats examples as less structured) or improve it (less visual chrome, more content focus)?
- STABILITY: conditional (based on group count) + structural (hierarchy depth decision)

---

## STRUCTURAL: instructions_examples_pairing
TYPE: architectural constraint (cross-section dependency)

### What the agent needs to understand

This is the most important architectural feature of the examples section, and it is currently invisible in the data structure.

The design intent is: each probabilistic instruction step describes a cognitive task, and each example group calibrates that cognitive task with demonstrations. The pairing is:

```
instruction step (probabilistic) <----> example group
```

For the summarizer, the mapping could be:
- Instruction step 2 (contextual summarization) <-> Examples: "Standard substantive exchange," "Thin content with rich context," "Thin content with thin context"
- Instruction step 5 (decontamination) <-> Examples: "Transferred content decontamination," "Reconstructed content decontamination"
- Instruction step 4 (session transitions) <-> No examples currently exist

For the builder, the mapping could be:
- Instruction step 3 (design instruction steps) <-> Example: "Designing Instruction Steps From Requirements"
- Instruction step 7 (set security fields) <-> Example: "Minimum Required Permissions"
- Instruction steps 2, 4, 5, 6 <-> No examples currently exist

The pairing is incomplete in both agents. This is likely a deficiency in the definitions, but it reveals that the template system must handle the case where not every probabilistic step has a corresponding example group, and where an example group may cover multiple steps.

### Fragments

**pairing_visibility**
- Alternative A: The pairing is implicit — example groups exist near the instructions section and group names suggest which steps they relate to, but no explicit connection is rendered.
- Alternative B: Each example group includes a reference to its paired instruction step: `These examples calibrate Step 2 (contextual summarization).` — explicit forward reference.
- Alternative C: Each probabilistic instruction step includes a reference to its example group: `(See examples: Contextual Summaries)` — explicit back-reference from instructions to examples.
- Alternative D: Both forward and back references — the pairing is visible from both sides.
- Alternative E: The pairing is purely structural — example groups are rendered in the same order as their paired instruction steps, making the correspondence positional. No explicit references needed.
- PURPOSE: Decides whether the agent can connect "I am executing step 2" with "here are the examples that calibrate step 2." If the connection is invisible, the agent must infer it from group names and step content. If visible, the agent has a direct link.
- HYPOTHESIS: Explicit pairing (B/C/D) is the most powerful because it tells the agent exactly which calibration to apply at which processing stage. But it requires the definition author to specify the pairing, adding another field to maintain. Positional correspondence (E) is elegant but fragile — it breaks if groups are reordered or if a step has no group. Implicit pairing (A) is what currently exists and depends on the agent's ability to match group names to step topics, which may work for obvious cases but fail for subtle ones. Test: does explicit pairing improve the agent's application of example-calibrated judgment during the specific paired step? Is the improvement large enough to justify the maintenance cost?
- STABILITY: structural (whether pairing exists at all) + experimental (the mechanism of pairing) + conditional (impossible when steps have no groups)

**uncalibrated_step_handling**
- Alternative A: Steps without examples are simply uncalibrated — the agent applies default judgment. No acknowledgment.
- Alternative B: A note in the examples section: `Not all processing steps have dedicated examples. For uncalibrated steps, apply the general principles demonstrated in the available examples.` — explicit acknowledgment with generalization instruction.
- Alternative C: No section-level note, but each example group's framing sentence specifies which steps it covers, making the absence of other groups an implicit signal.
- PURPOSE: Addresses the gap between the ideal (every probabilistic step has calibration examples) and reality (some steps have no examples). The agent needs to know what to do with uncalibrated judgment tasks.
- HYPOTHESIS: Acknowledging the gap (B) may be counterproductive — it draws attention to missing calibration and may cause the agent to be less confident on uncalibrated steps. Ignoring the gap (A) lets the agent proceed with whatever default judgment it has. The implicit signal (C) is the most subtle — the agent can infer what is calibrated without being told what is not. Test: does explicit acknowledgment of uncalibrated steps reduce quality on those steps (by reducing confidence) or improve it (by prompting the agent to be more careful)?
- STABILITY: experimental (high uncertainty about behavioral effect)

---

## STRUCTURAL: entry_count_and_density
TYPE: design consideration

### What the agent needs to understand

The two agents have very different example profiles:
- Builder: 1 group, 2 entries, entries are concept demonstrations (not GOOD/BAD/WHY pairs)
- Summarizer: 1 group, 5 entries, entries are a mix of GOOD-only and GOOD/BAD/WHY pairs

The number of entries per group and the density of each entry (length, presence of BAD/WHY components) affect calibration quality. Too few entries and the agent under-calibrates — it has insufficient decision boundary data. Too many entries and the agent may over-index on specific cases rather than extracting principles.

### Fragments

**entry_count_awareness**
- Alternative A: No count communicated — the agent processes entries as they appear.
- Alternative B: Count stated in the group heading or framing: `### Contextual Summaries (5 examples)` or `The following 5 examples demonstrate...`
- Alternative C: Entries are numbered: `**Example 1: Standard substantive exchange**`, `**Example 2: Thin content with rich context**`
- PURPOSE: Decides whether the agent knows how many examples to expect. Count awareness may affect pacing and thoroughness.
- HYPOTHESIS: Count in the heading (B) gives the agent an expectation that may help it pace its processing — knowing there are 5 examples prevents it from assuming it is done after 2. Numbering (C) provides both count and position, which may improve recall ("example 3 showed..."). But numbering also implies ordering significance that may not exist — the agent may assume example 1 is more important than example 5. Test: does numbered ordering create a primacy bias where early examples receive more calibration weight?
- STABILITY: formatting (display choice) + experimental (behavioral effects of count/numbering)

---

## STRUCTURAL: examples_section_ordering
TYPE: positional design decision

### What the agent needs to understand

Where the examples section appears in the overall agent prompt affects how it is processed. Examples placed immediately after instructions allow the agent to calibrate before encountering operational details (output format, security boundaries). Examples placed at the end serve as a reference section — calibration material available but not prioritized.

### Fragments

**section_position**
- Alternative A: Examples immediately after instructions — the natural position for calibration material. "Here is what to do (instructions). Here is what doing it well looks like (examples)."
- Alternative B: Examples after all operational sections (output, security, constraints, etc.) — examples are a reference appendix.
- Alternative C: Examples before instructions — the agent sees what good looks like before being told what to do. This is how some pedagogical approaches work: show the expert performance first, then explain the procedure.
- Alternative D: Examples interleaved with instructions — each instruction step is immediately followed by its calibration examples. This is the strongest pairing mechanism but creates a very different prompt structure.
- PURPOSE: Controls whether calibration happens before, after, or during procedural instruction processing. This is a fundamental prompt architecture decision.
- HYPOTHESIS: Immediately-after-instructions (A) is the natural calibration sequence — learn the procedure, then calibrate judgment for it. Appendix position (B) may cause the agent to treat examples as optional reference rather than mandatory calibration. Before-instructions (C) is pedagogically interesting — the agent forms a quality model before learning the procedure, which may produce higher-quality execution. Interleaved (D) is the strongest pairing but makes the prompt harder to navigate and may cause the agent to lose the procedural thread. Test: does section position affect calibration depth? Does interleaved placement produce better step-specific calibration at the cost of procedural coherence?
- STABILITY: structural (section ordering is an architectural decision) + experimental (different orderings may produce different behavioral profiles)

---

## CROSS-SECTION: examples_and_anti_patterns
TYPE: cross-section dependency

### What the agent needs to understand

The BAD examples in the examples section overlap functionally with the anti_patterns section. Both name things the agent should not do. The difference is:

- **BAD examples** show a specific incorrect output for a specific input, with reasoning about why it fails. They are grounded in concrete cases.
- **Anti-patterns** state general principles about what to avoid: "Do not classify importance," "Do not invent significance for administrative exchanges."

These are two perspectives on the same behavioral boundaries. The anti-pattern "Do not invent significance for administrative exchanges" corresponds directly to the BAD example in the "Thin content with thin context" entry. The anti-pattern states the rule; the BAD example demonstrates the violation.

### Fragments

**anti_pattern_echo_in_examples**
- Alternative A: No coordination — anti-patterns and examples are independently authored and may overlap. The agent encounters the same prohibition twice in different forms.
- Alternative B: Examples reference anti-patterns: `(See anti-pattern: Do not invent significance...)` — explicit connection between the demonstration and the rule.
- Alternative C: Anti-patterns reference examples: `(Demonstrated in example: Thin content with thin context)` — explicit connection from the rule to the demonstration.
- Alternative D: The overlap is intentional and desirable — stating a prohibition as a rule AND demonstrating it with a concrete case produces stronger behavioral programming than either alone. No coordination needed because the redundancy is the feature.
- PURPOSE: Decides whether the overlap between BAD examples and anti-patterns is managed (coordinated references) or accepted (intentional redundancy).
- HYPOTHESIS: Intentional redundancy (D) is probably correct. The rule states the prohibition abstractly. The BAD example shows what the violation looks like concretely. Together they cover both abstract understanding and pattern recognition. Explicit cross-references (B/C) may strengthen the connection but add maintenance burden. Test: does the agent violate an anti-pattern less often when it has both the abstract rule and a concrete BAD example, compared to having only one?
- STABILITY: structural (whether cross-references exist) + experimental (whether redundancy helps or hurts)

---

## CROSS-SECTION: examples_and_success_criteria
TYPE: cross-section dependency

### What the agent needs to understand

Success criteria define what "done correctly" looks like at the section level. Examples define what "done correctly" looks like at the case level. The summarizer's success criterion "Thin-content-rich-context exchanges have summaries reflecting accumulated conversational significance" is precisely what the "Thin content with rich context" example demonstrates.

The examples section is effectively a case-level instantiation of the success criteria. If the success criteria say "every summary is a single sentence capturing contextual significance," the examples show what "contextual significance" means for different input types.

### Fragments

**success_criteria_grounding**
- Alternative A: No explicit connection — the agent must infer that the examples demonstrate what the success criteria describe.
- Alternative B: A note in the examples section: `These examples demonstrate the quality standards described in your success criteria.` — makes the grounding explicit.
- Alternative C: The connection is structural — example group names echo success criteria language, making the correspondence apparent without explicit references.
- PURPOSE: Decides whether the agent perceives examples as grounded in success criteria or as independent demonstrations.
- HYPOTHESIS: Explicit grounding (B) may help the agent connect its quality standards to its calibration material, producing more consistent quality assessment. But it may also be redundant — the agent likely makes this connection implicitly. Test: does explicit grounding produce measurable quality improvement, or is it just noise?
- STABILITY: experimental (uncertain benefit)

---

## SYNTHESIS: The Examples Section as Behavioral Programming

The examples section is architecturally unique among all sections because it operates through **demonstration rather than instruction**. Every other section tells the agent what to do, what to avoid, what to produce, or what constraints to obey. The examples section shows it what quality looks like.

This distinction creates the core design tension: the examples section must be structured enough to organize calibration material (heading hierarchy, group boundaries, entry separation) but flexible enough to accommodate wildly different calibration content (GOOD-only entries, GOOD/BAD/WHY entries, Wrong/Right entries, concept demonstrations).

The highest-leverage design decisions are:

1. **Whether the template is GOOD/BAD/WHY-aware** — If the template treats example_text as opaque, the GOOD/BAD/WHY pattern is an authorial convention that the template does not control. If the template recognizes the pattern, it can apply visual emphasis that may strengthen calibration. The tradeoff is flexibility vs. control.

2. **Whether instructions-examples pairing is explicit** — The pairing is the architectural reason example groups exist. Making it visible (forward/back references) strengthens per-step calibration but adds complexity. Leaving it implicit is simpler but relies on the agent to make the connection.

3. **Whether single-group agents suppress the group heading** — The three-level hierarchy (section, group, entry) is structurally meaningful for multi-group agents but potentially noisy for single-group agents. The conditional suppression decision affects visual complexity.

4. **The section preamble** — Whether to explain the GOOD/BAD/WHY pattern, the instructions-examples pairing, and the generalization principle upfront. This is the highest-leverage single fragment because it configures how the agent processes all subsequent example content.

5. **Entry heading naming convention** — Whether headings name skills (builder style) or input conditions (summarizer style) affects the agent's retrieval pattern during processing. This is not a template decision (headings are authored content) but the template documentation should guide authors on which naming convention to use for which agent type.

The examples section is where the distance between "here are some samples" and "here is a structured calibration system" is widest. Every design choice either reinforces or undermines the calibration intent. The presentation must make it unmistakable that these demonstrations exist to configure the agent's judgment, not merely to illustrate its task.
