# Instructions Section: Control Surface Analysis (Agent B)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The instructions section is the agent's procedure. After reading it, the agent should have internalized not just WHAT to do, but HOW to do it and — critically — WHERE its own judgment is required versus where it must execute mechanically.

This section programs the agent's temporal behavior: the sequence of cognitive operations it performs from start to finish. The identity section configures WHAT the agent is. The instructions section configures WHAT the agent DOES, step by step, in order.

Three things must be true after the agent reads this section:

1. **The agent knows the order of operations.** Steps have a sequence. Step 1 happens before step 2. The agent must understand that the steps are a progression, not a menu of independent activities. Some steps depend on outputs of previous steps (the builder cannot write guardrails in step 5 without having designed instruction steps in step 3). The sequence carries implicit dependencies.

2. **The agent knows where to apply judgment and where to suppress it.** This is the single most important behavioral distinction in the entire section, and the current system DROPS it. Each step has a mode: deterministic (zero latitude, do exactly this) or probabilistic (judgment required, apply intelligence). An agent that treats every step as probabilistic will hallucinate, invent, and drift. An agent that treats every step as deterministic will produce rigid, brittle, unthinking output. The mode boundary between steps is an anti-hallucination guardrail applied per-step.

3. **The agent knows the scope of each step.** Each step is one coherent processing phase. Not a checklist of twelve tasks crammed into a paragraph. Not a vague directive to "do the work." One phase. The agent must understand where step N ends and step N+1 begins — what completion looks like for each step before proceeding.

The instructions section is where the agent's actual cognitive work is programmed. If the identity is the agent's self-model and the security boundary is its cage, the instructions are the choreography it dances within that cage. The quality of the choreography — the precision of the step boundaries, the clarity of the mode signals, the logic of the ordering — determines whether the agent produces coherent output or drifts into chaos.

---

## FIELD: instruction_mode
TYPE: enum ("deterministic" | "probabilistic")
OPTIONAL: no (every step has a mode)
VALUES: "deterministic" (agent-builder steps 1,7) / "probabilistic" (agent-builder steps 2-6) ; "deterministic" (summary steps 1,3) / "probabilistic" (summary steps 2,4,5)

### What the agent needs to understand

This is the most under-served field in the entire system. It is currently INVISIBLE to agents — the defective renderer drops it completely. The agent never sees whether a step is deterministic or probabilistic. This means every step is processed with the agent's default cognitive stance, which for LLMs is: "apply creativity and helpfulness everywhere, expanding scope whenever possible."

The mode field exists to solve a fundamental problem with LLM cognition: LLMs do not naturally distinguish between "execute this precisely" and "apply judgment here." Without visible mode markers, an LLM will:
- Add creative interpretation to a step that says "read the input tempfile and produce one output per input" (a deterministic operation that needs ZERO creativity)
- Fail to apply sufficient judgment to a step that says "write one sentence capturing what this exchange signifies" (a probabilistic operation that needs deep contextual reasoning)

The mode marker is a cognitive brake (deterministic) or a cognitive accelerator (probabilistic). When the agent sees a deterministic marker, it should suppress its tendency to elaborate, invent, or "help." When it sees a probabilistic marker, it should engage its full reasoning capacity. Without these markers, the agent has no per-step calibration — it runs at the same cognitive intensity across all steps, which is wrong for both types.

The design question is profound: how do you tell an LLM "turn off your intelligence here, turn it on there" in a way that actually works? The format, language, and visual weight of the mode indicator determines whether the agent genuinely downshifts and upshifts, or whether it reads the marker and ignores it.

### Fragments

**mode_indicator**
- Current (defective): Mode is DROPPED. Not rendered at all. The agent never sees it. Every step looks identical.
- Alternative A: `**[DETERMINISTIC]** Read the input tempfile...` / `**[PROBABILISTIC]** For each exchange, write one sentence...` — bold bracketed prefix before each step. The label is visually heavy and semantically explicit.
- Alternative B: `EXECUTE EXACTLY: Read the input tempfile...` / `APPLY JUDGMENT: For each exchange, write one sentence...` — imperative phrasing that tells the agent what to DO with the step, not what category the step is in. The difference: a category label requires the agent to interpret the label's behavioral implication. An imperative phrasing IS the behavioral instruction.
- Alternative C: `Step 1 (mechanical): Read the input tempfile...` / `Step 2 (reasoning): For each exchange...` — parenthetical after the step number, using plain-language descriptions of cognitive mode rather than system jargon. "Mechanical" and "reasoning" map to everyday understanding; "deterministic" and "probabilistic" are statistical terminology that may not map cleanly to LLM behavioral control.
- Alternative D: Two visually distinct formatting blocks. Deterministic steps in a fenced code-like block or monospace, signaling "this is a specification to follow literally." Probabilistic steps in normal prose, signaling "this is guidance to reason about." The visual difference creates a mode switch without any labeling at all.
- Alternative E: No per-step indicator. Instead, a preamble before the step list: `Some steps require exact execution. Others require judgment. The step label tells you which.` followed by `[exact]` and `[judgment]` prefixes. The preamble teaches the agent what the labels mean before it encounters them.
- PURPOSE: Creates per-step cognitive mode switching. The agent must change how it processes information when it moves from a deterministic step to a probabilistic one. Without this fragment, all steps are processed identically. With it, the agent has explicit authorization to think in some steps and explicit prohibition against thinking in others.
- HYPOTHESIS: The behavioral question is whether the label or the framing does the work. A bracketed label like `[DETERMINISTIC]` requires the agent to have a pre-existing association between that word and "suppress creativity." An imperative like `EXECUTE EXACTLY` directly programs the behavior without relying on a label-to-behavior mapping. A visual-formatting approach (code blocks vs prose) leverages the LLM's trained association between code = literal execution and prose = interpretive reading. The imperative form likely produces the strongest behavioral shift because it is a direct instruction, not a category to interpret. The visual form is untested but potentially powerful because it uses learned formatting associations rather than explicit instruction. Test: compare output quality across mode-indicator formats, specifically measuring (a) hallucination rate in deterministic steps and (b) reasoning depth in probabilistic steps.
- STABILITY: experimental — this is the single highest-leverage fragment in the instructions section and possibly the entire agent prompt. The choice here directly determines whether agents hallucinate in mechanical steps.

**mode_preamble**
- Current (defective): No preamble. The concept of instruction mode does not exist in the rendered output.
- Alternative A: `Each instruction step is marked as either exact-execution or judgment-required. Follow the markers strictly — exact steps leave no room for interpretation; judgment steps are where you apply your expertise.` — placed before the first step, teaches the agent what mode markers mean.
- Alternative B: `Steps below alternate between mechanical operations and judgment calls. Mechanical steps are non-negotiable: do exactly what they say, nothing more. Judgment steps are where your reasoning matters.` — shorter, more direct, uses "non-negotiable" as an anchor word.
- Alternative C: No preamble. The mode indicators on each step are self-explanatory. Adding a preamble may dilute the indicator's effect by teaching the agent "about" mode rather than letting the mode marker work directly.
- PURPOSE: Primes the agent to expect and respond to mode transitions. Without a preamble, the first mode indicator arrives unexplained. With a preamble, the agent understands the mode system before encountering any steps.
- HYPOTHESIS: A preamble likely helps the FIRST time an agent encounters mode markers (it understands the framework) but may become noise for well-calibrated agents. The "non-negotiable" anchor in Alternative B may produce stronger deterministic compliance because the word itself carries enforcement weight. No-preamble (Alternative C) is the riskiest but also the most elegant — it trusts the indicator to work on its own. Test: does preamble presence improve mode compliance, or does it teach the agent to think about modes rather than just following them?
- STABILITY: experimental — depends on how well mode indicators work alone

**mode_transition_signal**
- Current (defective): No transitions. All steps rendered as identical consecutive paragraphs.
- Alternative A: A visual break (extra whitespace or a thin rule) between steps of different modes. When the agent crosses from deterministic to probabilistic, the visual break signals "shift your cognitive gear."
- Alternative B: An explicit transition phrase: `The following step requires your judgment.` or `The following step is mechanical — follow it exactly.` — inserted between steps when the mode changes.
- Alternative C: No explicit transition. The mode indicator on each step IS the transition signal. Adding separate transition markers may over-instrument the mode system.
- PURPOSE: Signals that a mode change is happening at a specific boundary. The agent may read through steps fluidly; a transition signal forces a cognitive pause at mode boundaries.
- HYPOTHESIS: LLMs process text as a stream. Without explicit signals, they maintain whatever cognitive mode they entered the section with. A transition signal forces a reset. But over-instrumentation (both a mode indicator AND a transition AND a preamble) may cause the agent to focus on the meta-system rather than the content. Test: does adding transition signals between mode changes improve compliance over mode indicators alone?
- STABILITY: experimental — likely depends on step count and mode distribution

---

## FIELD: instruction_text
TYPE: string (can be multi-paragraph, can contain embedded lists, can be a single sentence or a long block)
OPTIONAL: no
VALUES: see the two agents' full step lists in the task data

### What the agent needs to understand

The instruction text is the actual content of each step — what the agent does during that phase. This field varies enormously between agents and between steps within the same agent:

- Agent-builder step 1: single sentence, 34 words, purely mechanical
- Agent-builder step 2: three paragraphs, 91 words, requires domain reasoning
- Summary step 5: six paragraphs with embedded bullet lists, 204 words, describes a complex decontamination procedure

The instruction text is pre-authored prose. It is already written in a style appropriate for agent consumption (direct address, imperative mood, no hedging). The template system's job is to present it — not to rewrite it, not to wrap it in additional explanation, not to dilute it with meta-commentary.

The critical design question: what surrounds each instruction_text value to make it identifiable as a discrete step, distinguishable from its neighbors, and correctly associated with its mode?

### Fragments

**step_header**
- Current (defective): No step headers. Steps are rendered as consecutive paragraphs separated only by blank lines. The agent has no numbered reference, no step label, no way to refer back to "step 3."
- Alternative A: `### Step 1` / `### Step 2` / etc. — markdown H3 heading with sequential number. Creates a visual hierarchy where each step is a named section.
- Alternative B: `**Step 1.** Read the input tempfile...` — bold inline prefix. Step number fused with the first sentence of instruction text. Less visual weight than a heading, but each step is still numbered.
- Alternative C: `1. Read the input tempfile...` — ordered list format. Each step is a numbered list item. This is the most compact format but may cause the LLM to process steps as a flat checklist rather than as sequential phases.
- Alternative D: No numbers at all. Steps separated by horizontal rules or extra whitespace. Each step is a visually distinct block but not numbered. This removes the "checklist" framing entirely — the agent processes each block as a phase, not as item N of M.
- Alternative E: `Phase 1: Input Acquisition` / `Phase 2: Domain Analysis` — named phases with descriptive titles. The title comes from the instruction_text content (generated or templated). This gives each step a semantic identity beyond its ordinal position.
- PURPOSE: Makes each step visually distinct and individually referenceable. Without step headers, the instructions are a wall of text with paragraph breaks. With headers, they are discrete addressable units.
- HYPOTHESIS: Numbered steps create a "checklist" cognitive frame — the agent tracks progress through the list and checks off items. This may improve completion (fewer skipped steps) but may also encourage shallow processing ("get through the list"). Named phases create a "progression" frame — the agent moves through conceptual stages. This may improve depth but may introduce scope confusion if the phase names are ambiguous. No numbering creates a "flow" frame — the agent reads through a continuous procedure. This may produce the most natural processing but the weakest step tracking. Test: does step numbering reduce step-skipping errors? Does phase naming improve reasoning depth at each step?
- STABILITY: structural (whether to number) + formatting (heading vs inline vs list) + experimental (named phases)

**step_body_presentation**
- Current (defective): instruction_text rendered as-is, preserving internal paragraph breaks and list formatting. No wrapping, no indentation, no visual containment.
- Alternative A: Each step's instruction_text rendered inside a visual container — indented block, bordered section, or blockquote. This visually binds the step content together as a unit.
- Alternative B: instruction_text rendered as-is (current behavior is accidentally correct here) — the text is already well-authored prose and needs no wrapping.
- Alternative C: Long instruction_texts (3+ paragraphs) get a collapsible summary: a one-line precis followed by the full text. This helps the agent build a mental model of the step before reading the details.
- PURPOSE: Controls whether the agent perceives each step's content as a self-contained unit or as part of a continuous flow.
- HYPOTHESIS: Visual containment (Alternative A) may improve step isolation — the agent processes each step as a complete unit before moving to the next. But it may also slow processing and create "paragraph blindness" if every block looks the same. Bare rendering (Alternative B) trusts the whitespace between steps and the step headers to provide sufficient delineation. Test: does visual containment of step bodies improve step-boundary compliance?
- STABILITY: formatting

**step_mode_and_body_integration**
- Current (defective): mode does not exist in the output, so there is no integration to speak of. The step IS just the body.
- Alternative A: Mode indicator as the first element, then the body immediately after: `[EXACT] Read the input tempfile. Each line is a JSON object...` — mode and body fused into one block.
- Alternative B: Mode indicator on its own line, body as a separate block below: `Mode: exact execution\n\nRead the input tempfile. Each line is a JSON object...` — mode is a metadata label separated from content.
- Alternative C: Mode indicator fused with the step header: `### Step 1 [exact]` or `**Step 1 (judgment):**` — mode is part of the step's identity, not part of its content.
- PURPOSE: Controls whether the agent reads mode-then-content (priming effect: the mode shapes how the content is read) or content-with-mode-annotation (the content is primary, mode is metadata).
- HYPOTHESIS: Mode-first (Alternatives A and B) creates a priming effect: the agent reads "EXACT" and then processes the body with reduced latitude. This leverages the primacy effect. Mode-in-header (Alternative C) makes mode part of the step's identity — "this is step 1 and it is exact" rather than "exact: do this thing." The integration choice determines whether mode is FRAMING (it shapes how you read what follows) or ANNOTATION (it labels what you are reading). Framing is likely more powerful. Test: does mode-first placement produce stronger compliance than mode-as-annotation?
- STABILITY: structural — this is a fundamental design decision about how mode relates to content

---

## STRUCTURAL: section_heading
TYPE: n/a (not tied to a specific field)

### What the agent needs to understand

The section heading names the instructions section. This seems trivial but the word choice programs whether the agent treats the section's contents as orders, guidelines, a procedure, or a workflow.

### Fragments

**section_heading_text**
- Current (defective): `## Processing` — the section is called "Processing," not "Instructions." This reframes the instruction steps as a description of a process rather than as directives to follow.
- Alternative A: `## Instructions` — direct, standard, unambiguous. The agent is being given instructions.
- Alternative B: `## Procedure` — implies a fixed sequence of operations with no latitude. Stronger than "Instructions" for deterministic-heavy agents, weaker for probabilistic-heavy ones.
- Alternative C: `## Your Task` — possessive, directive. The agent is being given its task. This frames the section as a thing to accomplish rather than a sequence to follow.
- Alternative D: `## Steps` — the most neutral framing. These are steps. Neither orders nor guidelines nor a procedure — just a sequence.
- Alternative E: No section heading. The instructions follow directly from the previous section (input) without a heading break. The steps ARE the main content of the prompt — they do not need to be labeled as a section.
- PURPOSE: Sets the cognitive frame for the entire section. "Processing" tells the agent to process. "Instructions" tells the agent to follow instructions. "Procedure" tells the agent to execute a procedure. "Your Task" tells the agent to accomplish a goal. These produce different compliance patterns.
- HYPOTHESIS: "Processing" (current) is the weakest framing — it describes what happens rather than commanding the agent to make it happen. "Instructions" is the standard LLM framing with the strongest trained associations to compliance. "Procedure" may produce the most rigid adherence (good for batch processors, bad for creative agents). "Your Task" may produce the most goal-oriented behavior (the agent focuses on outcomes rather than step compliance). Test: does section heading choice affect step-skipping rates and output quality?
- STABILITY: structural (heading presence) + experimental (heading text)

---

## STRUCTURAL: section_preamble
TYPE: n/a

### What the agent needs to understand

A preamble before the first step can orient the agent to the section's purpose and structure. Or it can be omitted, letting the steps speak for themselves.

### Fragments

**instructions_preamble**
- Current (defective): No preamble. The section heading is immediately followed by the first step's instruction_text.
- Alternative A: `Follow these steps in order. Each step is one processing phase.` — minimal preamble establishing sequence and step granularity.
- Alternative B: `You will execute {N} steps. Steps marked [exact] must be followed precisely. Steps marked [judgment] require your reasoning.` — preamble that previews step count and teaches the mode system.
- Alternative C: `The following steps define your complete workflow from input to output. Do not add steps. Do not skip steps. Do not reorder steps.` — preamble as a guardrail, explicitly prohibiting the three most common step-level failures.
- Alternative D: No preamble. The mode indicators and step headers carry all the necessary information. A preamble adds words without adding information.
- PURPOSE: Prepares the agent for what it is about to read and how to process it.
- HYPOTHESIS: The guardrail preamble (Alternative C) likely produces the best step compliance because it explicitly prohibits common failure modes BEFORE the agent encounters the steps. But it adds negativity before the actual content. The count-and-mode preamble (Alternative B) gives the agent a structural overview that may help it allocate attention across steps (if it knows there are 7 steps, it will not treat step 2 as the entire task). The minimal preamble (Alternative A) adds almost nothing. No preamble (Alternative D) is cleanest but risks the agent misinterpreting step structure. Test: does a step-count preamble improve completion rates for agents with many steps?
- STABILITY: experimental — preamble content is highly testable

---

## STRUCTURAL: step_numbering_scheme
TYPE: n/a

### What the agent needs to understand

Steps have an inherent ordering (they are an array, not a set). The numbering scheme determines how explicitly that ordering is communicated and whether the agent perceives the sequence as rigid.

### Fragments

**numbering_format**
- Current (defective): No numbering. Steps are visually separated by blank lines only. The agent must infer ordering from reading sequence.
- Alternative A: Sequential integers starting from 1: `Step 1`, `Step 2`, etc.
- Alternative B: Cardinal numbers with total: `Step 1 of 7`, `Step 2 of 7`, etc. — this tells the agent both its position and the total, which may improve allocation of effort across steps.
- Alternative C: No numbers, but visual anchors: each step preceded by a consistent marker (bullet, dash, arrow) that creates a visual list without imposing numeric ordering.
- Alternative D: Numbers fused with mode: `1. [exact]`, `2. [judgment]`, `3. [judgment]` — the most information-dense format, combining ordinal position and cognitive mode.
- PURPOSE: Communicates step ordering explicitly (if numbered) or implicitly (if unnumbered). Also provides reference points for error messages and self-monitoring ("I am on step 4 of 7").
- HYPOTHESIS: `Step N of M` format likely produces the best step-completion rates because the agent has a progress model. It knows it is not done until it reaches step M. Unnumbered steps risk the agent treating the first 2-3 steps as the whole task and skimming past the rest. Fused numbering+mode (Alternative D) is the most compact but may create visual noise. Test: does `N of M` numbering reduce step-skipping compared to simple sequential numbers?
- STABILITY: formatting (number format) + structural (whether to number at all)

---

## STRUCTURAL: step_separation
TYPE: n/a

### What the agent needs to understand

The visual and structural separation between steps determines whether the agent treats each step as a discrete processing unit or as a paragraph in a continuous flow.

### Fragments

**inter_step_separator**
- Current (defective): Blank line only. Same separator used between paragraphs WITHIN a step and BETWEEN steps. The agent cannot visually distinguish "new paragraph in the same step" from "new step."
- Alternative A: Horizontal rule (`---`) between steps. Strong visual break. Unambiguously signals a step boundary.
- Alternative B: Extra whitespace (two blank lines instead of one) between steps, while keeping single blank lines within steps. Subtle but consistent.
- Alternative C: Each step as a subsection with its own heading (H3 or H4). The heading itself is the separator.
- Alternative D: Different separators for different mode transitions: thin rule when staying in the same mode, thick rule or visual marker when switching modes. This makes mode transitions visually salient.
- PURPOSE: Creates unambiguous step boundaries. The current failure — using the same separator between and within steps — means the agent cannot tell where one step ends and the next begins. This is a structural defect, not a cosmetic issue.
- HYPOTHESIS: The same-separator problem (current) is probably causing real step-boundary confusion. An agent reading a multi-paragraph deterministic step followed by a multi-paragraph probabilistic step may not realize a step boundary occurred. The heading-based approach (Alternative C) provides the clearest boundaries because headings are structurally distinct from body paragraphs. The horizontal rule (Alternative A) is clear but adds visual weight. The mode-transition variant (Alternative D) is novel — it makes the INTERESTING boundaries (mode changes) more salient than same-mode boundaries. Test: does unambiguous step separation reduce cases where the agent merges or reorders steps?
- STABILITY: structural — this is a defect fix, not an experimental variable. Steps MUST be unambiguously separated. The choice of HOW is formatting.

---

## STRUCTURAL: section_closer
TYPE: n/a

### What the agent needs to understand

After the last step, what happens? The section ends and the agent transitions to the next section (examples, output, constraints, etc.). The closer controls whether the instructions "stick" as the dominant behavioral program or whether the agent shifts into a new cognitive frame.

### Fragments

**section_closing**
- Current (defective): The last step's text is followed by `---` (horizontal rule), then the next section begins. No closing summary, no reinforcement.
- Alternative A: A brief closing statement: `These {N} steps constitute your complete task. Do not add additional steps.` — reinforcement + guardrail.
- Alternative B: No explicit closer. The last step ends, the divider appears, the next section begins. The instructions are self-contained and need no summary.
- Alternative C: A recap line listing step modes: `Steps 1 and 3 are exact. Steps 2, 4, and 5 require judgment. There are no other steps.` — serves as both a summary and a guardrail against step invention.
- Alternative D: A transition that connects instructions to what follows: `The following sections provide examples, constraints, and criteria that refine the steps above.` — this frames the rest of the prompt as elaboration on the instructions, not independent content.
- PURPOSE: Controls whether the agent carries the instruction sequence as a persistent behavioral program or whether it fades as the agent processes subsequent sections.
- HYPOTHESIS: The recap-with-modes closer (Alternative C) is potentially the most powerful because it (a) reinforces the mode system one final time, (b) explicitly bounds the step count (preventing step invention), and (c) gives the agent a compressed reference it can use during execution. The transition closer (Alternative D) reframes the entire rest of the prompt as supporting material for the instructions, which may keep the instructions primary. No closer (Alternative B) is the simplest and trusts the instructions to persist without reinforcement. Test: does a mode-recap closer improve mode compliance during execution?
- STABILITY: experimental — closer content is testable, closer presence is structural

---

## CROSS-FIELD DEPENDENCIES

### instruction_mode + instruction_text (within each step)
These two fields are bound together per step. The mode tells the agent HOW to process the text. They must be rendered as a unit — the mode must arrive before or simultaneously with the text, never after. If the agent reads the text before seeing the mode, the mode loses its priming effect.

### instruction ordering (implicit array index)
The steps array is ordered. The index is not stored as a field — it is the array position. The rendering system must preserve this ordering and make it explicit (through numbering, sequencing, or visual flow). If steps are rendered out of order, the agent's procedure is scrambled.

### instruction_text internal structure
Some instruction_text values contain embedded lists (the summary agent's decontamination step has a bullet list of reconstructed-exchange handling rules). The rendering system must preserve this internal structure without confusing it with step-level structure. An embedded bullet list in step 5 must not look like a set of additional steps.

---

## CROSS-SECTION DEPENDENCIES

### instructions -> identity.role_description
The role_description configures HOW the agent thinks. The instructions tell it WHAT to do. The instruction_text values are authored with awareness of the role_description — the summary agent's steps reference "contextual significance" because the role_description established that frame. If the instructions used different terminology than the role_description, the agent would experience a frame collision.

### instructions -> examples
The examples section demonstrates correct execution of the instruction steps. Each example should map to one or more instruction steps. The builder's "Designing Instruction Steps From Requirements" example maps to instruction step 3. The summary agent's "Thin content with rich context" example maps to instruction step 2. If the examples and instructions use different terminology or imply different procedures, the agent gets conflicting behavioral signals.

### instructions -> constraints
Constraints restrict behavior during instruction execution. The summary agent's constraint "MUST process exchanges in order" reinforces instruction step 1's "Process exchanges in order, first to last." This redundancy may be intentional (reinforcement) or accidental. The rendering system must decide whether constraints that overlap with instructions are a feature (belt and suspenders) or a defect (noise that dilutes both).

### instructions -> success_criteria
Success criteria define what correct instruction execution looks like. The summary agent's success criterion "Every summary is a single sentence capturing contextual significance" maps directly to instruction steps 2 and 3. The instructions tell the agent what to do; the success criteria tell it what "done correctly" looks like. These must align.

### instructions -> critical_rules
Critical rules override everything, including instructions. The summary agent's critical rule about batch discipline (process exactly 20 records per batch) constrains HOW instruction steps are executed without being part of any instruction step. The instructions section should not contradict critical rules, and ideally should not duplicate them.

### instructions -> input
Instruction step 1 typically references the input section's data format. The builder's step 1 says "Read the preparation package from the tempfile path." The summary's step 1 says "Read the input tempfile. Each line is a JSON object with fields: exchange (integer), agent (string), user (string)." The input section has already described this format. The first instruction step re-states or extends it. This creates a redundancy that may need management — does step 1 repeat the input format, or does it say "process the input described above"?

---

## CONDITIONAL BRANCHES

### Step count variation
Agent-builder has 7 steps. Interview-summary has 5. The section structure must handle arbitrary step counts gracefully. With 2-3 steps, heavy per-step infrastructure (headings, dividers, mode indicators) may feel over-engineered. With 10+ steps, the same infrastructure becomes essential for navigation. This implies the rendering strategy may need to adapt to step count:
- 1-3 steps: lightweight (numbers, no headings, compact mode indicators)
- 4-7 steps: standard (headings or numbers, clear mode indicators, dividers)
- 8+ steps: heavy (named phases, mode-recap preamble, progress indicators)

### Mode distribution
Agent-builder: 2 deterministic, 5 probabilistic (bookend pattern — deterministic at start and end, probabilistic core).
Interview-summary: 2 deterministic, 3 probabilistic (interspersed — deterministic-probabilistic-deterministic-probabilistic-probabilistic).

The bookend pattern (builder) means the agent starts mechanical, enters a creative core, and exits mechanical. The interspersed pattern (summary) means the agent alternates between modes throughout. The mode transition signal fragment may be more important for the interspersed pattern, where transitions are frequent.

A conditional branch: if all steps are the same mode (hypothetical all-deterministic agent), mode indicators may be unnecessary. A single preamble statement ("All steps below are exact execution — follow them precisely") would suffice. Mode indicators per-step add value only when the mode varies.

### Instruction_text complexity
Some steps are single sentences. Others are multi-paragraph blocks with embedded formatting. The step_body_presentation fragment may need to adapt:
- Single-sentence steps: inline after the step header, no visual containment needed
- Multi-paragraph steps: their own section with visual containment, possibly a precis
- Steps with embedded lists: must preserve the list formatting without confusion with step-level formatting

### First step as input-processing preamble
In both agents, step 1 is deterministic and describes how to read the input. This may be a pattern: the first step is always "read and parse your input." If this is a universal pattern, the first step could be rendered differently — as a preamble that connects the input section to the instruction section, rather than as step 1 of the procedure. Alternatively, if this is NOT universal (some agents may start with a judgment step), treating it as special would break for those cases.

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### step_completion_signal
No existing or proposed design includes a fragment that tells the agent when a step is COMPLETE — when it should stop working on step N and begin step N+1. For deterministic steps this is usually obvious (read the file — done when the file is read). For probabilistic steps it is often ambiguous — when has the agent finished "identifying the agent's core domain"? A completion signal per step would prevent over-processing (spending too long on one step) and under-processing (moving on before the step is fully executed).

Possible forms:
- `Done when: {completion condition}` after each step's instruction_text
- Implicit: the next step's existence implies the current step is bounded
- Only for probabilistic steps: deterministic steps have obvious completion; probabilistic steps need explicit boundaries

This fragment does not exist in the data. It would be derived from the instruction_text or authored as a template-level addition. It raises the question: should the template system add behavioral guidance that is NOT in the raw data?

PURPOSE: Prevents over- and under-processing of individual steps.
HYPOTHESIS: Agents with completion signals for probabilistic steps may produce more consistently scoped output per step. Without completion signals, some agents may exhaust their context on the first probabilistic step and rush through the rest.
STABILITY: experimental — this is entirely novel and untested

### step_dependency_annotation
The steps have implicit dependencies (step 5 "write guardrails" depends on step 3 "design instruction steps" because you need to know the instruction steps to write guardrails that complement them). These dependencies are implicit in the text — the instruction author knows the ordering matters, but the agent may not realize that step 5's quality depends on step 3's output.

Possible forms:
- `Uses output from: Step 3` annotation on step 5
- `Prerequisites: Steps 1-4 must be complete` at the start of step 5
- Woven into the instruction_text: "Using the instruction steps designed in the previous phase, write guardrails..."

This fragment is partially present in some instruction_texts (the builder's step 1 says "read... the template defines every valid field" which implicitly feeds into step 7's "use the agent-template.toml as reference"). But it is never made explicit as a structural relationship between steps.

PURPOSE: Makes the step-dependency graph explicit, preventing the agent from treating steps as independent operations.
HYPOTHESIS: Explicit dependency annotations may improve output coherence (step 5's guardrails actually complement step 3's instructions) but may also create rigidity (the agent refuses to work on step 5 if it feels step 3 was incomplete).
STABILITY: experimental

### cognitive_load_warning
Some steps are enormously more complex than others. The summary agent's step 5 (decontamination) is 204 words with multiple sub-cases and a bullet list. Step 3 is 28 words. An agent that allocates equal attention to each step will under-process step 5 and over-process step 3. A cognitive load signal — some indication that a step is heavy or light — could help the agent allocate attention.

Possible forms:
- Implicit through visual weight: longer steps naturally look heavier
- Explicit: `[complex]` or `[simple]` tags alongside mode indicators
- Derived from instruction_text length: steps over N words get a "this step requires careful attention" prefix

PURPOSE: Helps the agent allocate cognitive resources across steps.
HYPOTHESIS: Explicit load signaling may reduce the "first-step bias" where agents invest disproportionate effort in early steps and rush through later, heavier ones. But it may also cause agents to over-index on load signals and treat "complex" steps as harder than they are.
STABILITY: experimental

### mode_behavioral_glossary
The terms "deterministic" and "probabilistic" have specific statistical meanings that may not map cleanly to the behavioral modes we want. An inline glossary that defines these terms in agent-behavioral language (not statistical language) could improve mode compliance.

Possible forms:
- Part of the preamble: `Exact steps: do exactly this, add nothing, interpret nothing. Judgment steps: apply your full reasoning to produce the best output.`
- Inline on first occurrence only: the first deterministic step gets `(exact: follow literally)` and the first probabilistic step gets `(judgment: apply reasoning)`. Subsequent steps use the bare indicator.
- Omitted: use plain-language terms instead of "deterministic"/"probabilistic" in the first place (see mode_indicator Alternative C above)

PURPOSE: Ensures the agent maps mode labels to the correct behavioral adjustments.
HYPOTHESIS: The statistical terms may cause the agent to think about probability distributions rather than behavioral compliance. Plain-language alternatives ("exact" / "judgment") may map more directly to the behaviors we want. Alternatively, the statistical terms may be more precise for Opus-class models that have strong concept mappings for these terms. This is a model-dependent design choice.
STABILITY: experimental

### aggregate_mode_ratio
Neither current nor proposed designs include a fragment that tells the agent the overall character of its task: "this is a mostly-judgment task with mechanical bookends" (builder: 5/7 probabilistic) vs "this is a mixed task alternating between mechanical and judgment work" (summary: 3/5 probabilistic). Knowing the ratio may help the agent calibrate its overall cognitive stance.

Possible forms:
- Part of the preamble: `This task is primarily judgment-based — 5 of 7 steps require your reasoning.`
- Implicit: the mode indicators on each step already communicate this in aggregate
- In the section closer as a recap

PURPOSE: Gives the agent a meta-view of the task's cognitive character before it begins processing steps.
HYPOTHESIS: An agent told "this is primarily judgment work" may allocate more total reasoning capacity than one told "this is primarily mechanical work." This could improve quality for judgment-heavy agents but might cause mechanical-heavy agents to over-think their few judgment steps.
STABILITY: experimental

---

## DESIGN TENSION: INSTRUCTIONS AS CHOREOGRAPHY VS. INSTRUCTIONS AS SPECIFICATION

The two reference agents reveal a fundamental tension in how instructions function:

**The builder's instructions are a specification.** They describe a creative process: identify the domain, write the role fields, design instruction steps, create examples, write guardrails, write criteria, map fields. The agent is being told WHAT to produce, and it must figure out HOW. The instruction steps are waypoints in a creative journey.

**The summary agent's instructions are choreography.** They describe a processing pipeline: read input, summarize each exchange, enforce one-sentence constraint, handle session transitions, decontaminate markers. The agent is being told HOW to process, and the WHAT (one-sentence summaries) is fixed.

This distinction affects nearly every fragment in the section:
- Mode indicators matter more for the summary agent (tight alternation between exact and judgment) than for the builder (broad creative core with mechanical bookends)
- Step numbering matters more for the builder (7 steps, easy to lose track) than for the summary agent (5 steps, tighter loop)
- Completion signals matter more for the builder (when is "identify the core domain" complete?) than for the summary agent (when is "read the input" complete? when the input is read)

The rendering system may need to detect — from the step count, mode distribution, and instruction_text characteristics — whether it is rendering specification-style instructions or choreography-style instructions, and adjust its fragments accordingly. Or it may need to provide a single format robust enough to serve both.

This is an open design question, not a solved problem.
