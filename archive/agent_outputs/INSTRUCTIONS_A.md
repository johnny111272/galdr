# Instructions Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The instructions section is the agent's operational program. After the identity section configures *what the agent is*, this section configures *what the agent does, in what order, and with what degree of latitude at each step*. It is the most direct behavioral programming in the entire prompt.

But "direct behavioral programming" conceals a critical subtlety. The instructions section must accomplish three things simultaneously:

1. **Sequencing** — the agent must understand that these steps are ordered, that earlier steps produce context for later steps, and that the sequence is not arbitrary. Step 3 may depend on the output of Step 1. The agent must carry forward state across steps. The instruction section must communicate not just "do these things" but "do them in this order because this order matters."

2. **Mode switching** — the agent must shift its cognitive posture between steps. Some steps demand exact compliance (parse this format, check this condition). Others demand judgment (assess quality, interpret meaning, calibrate significance). The instructions section must signal these shifts so the agent does not apply judgment where compliance is needed, and does not apply rote compliance where judgment is needed. This is the `instruction_mode` field's purpose, and it is currently invisible to agents.

3. **Scope delimitation per step** — each step is a self-contained unit of work. The agent must understand where one step ends and the next begins. Without clear boundaries, the agent will treat the instructions as a continuous narrative and may blend step concerns, skip steps, or invent steps that were not specified.

The fundamental behavioral question: the instructions section must produce an agent that executes a structured, ordered sequence of operations with varying cognitive demands, carrying forward state but respecting step boundaries. This is closer to programming a state machine than writing a paragraph. The presentation must serve that machine-like execution while still being natural language consumed by a language model.

### What the defective renderer currently does

The current renderer:
- Uses `## Processing` as the section heading
- Dumps all instruction steps as consecutive paragraphs with blank lines between them
- **Drops `instruction_mode` entirely** — agents never see whether a step is deterministic or probabilistic
- Uses no step numbering, no step labels, no step boundaries beyond whitespace
- Treats multi-paragraph instruction_text values as multiple paragraphs within the same undelimited block

The result reads as a continuous wall of prose. The agent has no structural signal that these are discrete steps, no indicator of what cognitive mode to apply, and no way to track which step it is on.

---

## FIELD: instruction_mode
TYPE: enum ("deterministic" | "probabilistic")
OPTIONAL: no (present on every step)
VALUES: varies per step — agent-builder has D/P/P/P/P/P/D; interview-summary has D/P/D/P/P

### What the agent needs to understand

This is the highest-leverage design gap in the current system. Every instruction step has a mode, and the mode is never shown. The mode answers the question: "How much latitude do I have on this step?"

A deterministic step says: execute this exactly. Do not interpret. Do not expand. Do not improvise. The input format is specified, the output format is specified, the transformation is mechanical. If you find yourself making a judgment call on a deterministic step, you have gone wrong.

A probabilistic step says: apply your intelligence here. This is where your expertise matters. The instructions describe what to assess, evaluate, or synthesize, but the specific judgments are yours to make. Exact compliance is impossible because the task requires reasoning.

Without visible mode markers, the agent operates in a default undifferentiated mode — typically probabilistic-leaning, because LLMs default to creative/expansive behavior. This causes two specific failure modes:

**Failure mode 1: Hallucination on deterministic steps.** The agent "helps" by expanding, interpreting, or adding to steps that should be executed exactly. A deterministic step that says "parse each line as a JSON object with fields: exchange, agent, user" gets "enhanced" with additional field processing, format inference, or error correction that was never requested.

**Failure mode 2: Under-reasoning on probabilistic steps.** Without explicit permission to exercise judgment, the agent may apply shallow, mechanical processing to steps that demand deep reasoning. A probabilistic step about contextual significance gets reduced to mechanical text summarization.

The mode marker is an anti-hallucination guardrail applied per-step. It tells the LLM where to be a machine and where to be intelligent.

### Fragments

**mode_indicator**
- Current (defective): not rendered at all — agents never see the mode
- Alternative A: `[DETERMINISTIC]` / `[PROBABILISTIC]` — bracketed label at the start of each step, visually loud
- Alternative B: `Mode: exact compliance` / `Mode: judgment required` — labeled but translated into behavioral language rather than technical enum names
- Alternative C: A behavioral preamble sentence per step: `Execute this step exactly as specified.` / `This step requires your judgment. Apply your expertise.` — the mode becomes a framing sentence rather than a label
- Alternative D: Visual formatting difference — deterministic steps in a code block or monospace, probabilistic steps in normal prose. The visual channel carries the mode signal without any label.
- Alternative E: Integrated into the step header: `Step 3 (exact):` / `Step 3 (judgment):` — mode as a parenthetical in the step number
- PURPOSE: Makes the mode visible. The specific form controls how strongly the mode constrains the agent's behavior and how it processes the instruction text that follows.
- HYPOTHESIS: Bracketed labels (A) are visually strong but may be parsed as metadata rather than behavioral instruction — the agent notes the label without shifting its processing mode. Behavioral language (B/C) translates the mode into a direct command about how to process the step, which may produce stronger mode-switching. Visual formatting (D) operates below explicit reasoning — the agent "feels" a different processing context without being told about it. Integrated parenthetical (E) keeps the mode tightly bound to the step identity. Test: does behavioral language ("judgment required") produce more genuine mode-switching than technical labels ("PROBABILISTIC")? Does visual formatting produce unconscious mode-switching even without explicit labels?
- STABILITY: experimental — this fragment does not exist yet and has the highest behavioral leverage of any single fragment in this section

**mode_definition_preamble**
- Current (defective): not rendered — no explanation of what modes mean
- Alternative A: Before the first step, define both modes: `Steps marked EXACT require literal compliance — do not interpret, expand, or improvise. Steps marked JUDGMENT require you to apply your expertise — assess, evaluate, synthesize.` — upfront definition
- Alternative B: No upfront definition — modes are self-explanatory from their labels. Defining them risks over-explaining and treating the agent as unable to understand "deterministic" and "probabilistic."
- Alternative C: Define modes only implicitly through the step text — deterministic steps use imperative, mechanical language; probabilistic steps use reasoning-oriented language. The mode is carried by prose style, not labels.
- Alternative D: A single sentence before the steps: `Some steps require exact execution. Others require judgment. The markers tell you which.` — minimal meta-awareness without full definitions
- PURPOSE: Decides whether the agent needs to be taught what modes mean, or whether the mode indicators are self-sufficient.
- HYPOTHESIS: Upfront definition (A) is clearest but adds length and may feel patronizing to a capable model. No definition (B) relies on the agent understanding the labels from context, which Opus likely can but Sonnet might not. Implicit encoding (C) is elegant but fragile — a single step written in the wrong prose register breaks the pattern. Minimal meta-awareness (D) acknowledges modes exist without over-defining. Test: does mode performance differ between models that received definitions vs. those that received only labels? Does Sonnet need definitions more than Opus?
- STABILITY: structural (whether to include at all) + experimental (the specific definition text)

---

## FIELD: instruction_text
TYPE: string (single or multi-paragraph)
OPTIONAL: no (present on every step)
VALUES: varies — see raw data above

### What the agent needs to understand

This is the actual work instruction. Each step's instruction_text tells the agent what to do during that step. The text ranges from single sentences ("Read the input tempfile.") to multi-paragraph blocks with sub-instructions, examples, and edge case handling (the decontamination step has 5 paragraphs with a bulleted sub-list).

The instruction_text is pre-authored domain content — it is not something the template system generates. The template's job is to present it with appropriate framing, boundaries, and context. The text itself is invariant.

Key structural observation: instruction_text values vary enormously in length and internal complexity:
- Builder step 1: single sentence (32 words)
- Builder step 3: 4 paragraphs with a bulleted sub-list (~80 words)
- Summary step 2: 3 paragraphs with inline examples (~120 words)
- Summary step 5: 6 paragraphs with bulleted sub-list, marker syntax, and detailed handling instructions (~200 words)

This variation means the presentation system must handle both terse mechanical directives and rich multi-paragraph reasoning blocks. A step boundary system that works for single-sentence steps must also work for 200-word steps without causing ambiguity about where the step ends.

### Fragments

**step_text_presentation**
- Current (defective): instruction_text rendered as bare paragraphs — multi-paragraph texts become multiple paragraphs with no indication they belong to the same step
- Alternative A: Each step's text in a visually bounded container — indented block, blockquote, or fenced section. Multi-paragraph texts are clearly within a single step's container.
- Alternative B: No special presentation — the instruction_text speaks for itself. Step boundary markers (see structural fragments below) make it clear where one step ends and the next begins, so the text needs no wrapping.
- Alternative C: Long instruction texts (above some threshold) get a sub-heading derived from the first sentence or phrase: `### Step 3: Design instruction steps` followed by the full text. Short texts get no sub-heading.
- PURPOSE: Controls whether multi-paragraph instruction texts are perceived as one unit or as multiple disconnected paragraphs.
- HYPOTHESIS: Without containers, a 200-word instruction text with paragraphs, bullets, and examples looks identical to multiple separate steps. The agent may start treating paragraph 3 of a 6-paragraph step as a new step. Containers (A) prevent this at the cost of visual complexity. Step boundary markers (B) solve this indirectly — the agent doesn't need to know where a step ends if it knows where the next step begins. Sub-headings (C) give long steps a named identity that aids memory and reference. Test: for agents with long instruction texts (5+ paragraphs per step), does containerization reduce step-boundary confusion?
- STABILITY: formatting (container style) + conditional (based on text length)

---

## STRUCTURAL: section_heading
TYPE: n/a

### What the agent needs to understand

The section heading tells the agent what kind of content follows. The current heading is "## Processing" — a label that does not communicate sequence, steps, or mode variation. It treats the instructions as a processing block rather than as an ordered program.

### Fragments

**section_heading_text**
- Current (defective): `## Processing` — implies a single undifferentiated processing phase
- Alternative A: `## Instructions` — neutral label that says "these are your instructions" without implying structure
- Alternative B: `## Execution Steps` — implies discrete, ordered steps to execute
- Alternative C: `## Your Task` — second-person framing that makes the instructions personal
- Alternative D: `## Procedure` — implies a formal, ordered protocol
- Alternative E: `## Steps ({N} total)` — heading includes the step count, giving the agent an explicit expectation of how many steps to track
- PURPOSE: Sets the agent's expectation for what follows. "Processing" says "here's what to process." "Execution Steps" says "here are ordered steps to execute." "Procedure" says "here is a formal protocol." The heading primes the agent's processing mode for the entire section.
- HYPOTHESIS: "Processing" (current) produces the weakest step-awareness because it implies a continuous activity, not discrete units. "Execution Steps" explicitly primes for sequential discrete execution. "Procedure" carries the strongest formality — the agent is less likely to improvise. Including the step count (E) gives the agent a completion target, which may improve step-tracking but may also cause the agent to rush. Test: does "Execution Steps" produce better step-boundary respect than "Processing"? Does including the count improve or degrade execution quality?
- STABILITY: structural (heading level and presence) + experimental (heading text choice)

---

## STRUCTURAL: section_preamble
TYPE: n/a

### What the agent needs to understand

Before the first step, the agent may need framing that explains the section's structure. The current system has no preamble — the heading is immediately followed by the first instruction step's text.

### Fragments

**instruction_section_intro**
- Current (defective): no preamble — heading followed immediately by first step text
- Alternative A: `Follow these steps in order. Each step is marked as exact (execute literally) or judgment (apply your expertise).` — brief structural guide
- Alternative B: `The following {N} steps define your complete procedure. Execute them sequentially, carrying forward context from earlier steps.` — states count, order, and context-carry
- Alternative C: No preamble — the step structure should be self-evident from the step markers. Adding an intro is redundant.
- Alternative D: A context-setting sentence only when the instructions are complex (many steps, mixed modes): `This task has {N} steps alternating between exact compliance and judgment. Stay aware of which mode you are in.` — conditional preamble
- PURPOSE: Prepares the agent for what the section contains before it encounters the first step. Sets expectations about structure, count, and cognitive demands.
- HYPOTHESIS: No preamble (current/C) means the agent discovers the section's structure as it reads — it may not realize until step 3 that there are 7 steps total. A count-bearing preamble (B/D) gives the agent a mental model of the section's size upfront, which may improve planning and pacing. A mode-aware preamble (A/D) explicitly tells the agent about mode variation, which may prime better mode-switching. Test: does knowing the step count upfront reduce step-skipping? Does mode-awareness priming improve mode compliance?
- STABILITY: experimental (whether to include) + conditional (content varies by step count and mode distribution)

---

## STRUCTURAL: step_boundary
TYPE: n/a

### What the agent needs to understand

Step boundaries are the most important structural fragment in this section. They tell the agent where one step ends and the next begins. Without them, the instructions are a continuous stream of prose that the agent must parse into steps using only whitespace and topic shifts.

### Fragments

**step_delimiter**
- Current (defective): blank lines between paragraphs — no explicit step delimiters, step boundaries are indistinguishable from paragraph breaks within multi-paragraph steps
- Alternative A: `---` horizontal rule between steps — strong visual break, unambiguous
- Alternative B: Numbered step headers: `**Step 1.**` / `**Step 2.**` — each step gets a numbered label that doubles as a delimiter
- Alternative C: Numbered step headers with mode: `**Step 1 [EXACT].**` / `**Step 2 [JUDGMENT].**` — combined step label, delimiter, and mode indicator
- Alternative D: Markdown numbered list — each step is a `1.` / `2.` / `3.` list item. Multi-paragraph steps use indentation to stay within the list item.
- Alternative E: Step headers with first-sentence summaries: `**Step 1: Read input tempfile** [EXACT]` — the header names the step, the tag indicates mode, and the full instruction text follows
- PURPOSE: Creates unambiguous step boundaries. Without these, the agent cannot reliably track which step it is on, especially when steps contain multiple paragraphs.
- HYPOTHESIS: Blank lines (current) produce the weakest boundaries — the agent treats the instructions as flowing prose. Horizontal rules (A) create strong visual breaks but carry no semantic content. Numbered headers (B) are the minimum viable delimiter — they tell the agent both where a step begins and which step it is. Mode-integrated headers (C) combine three functions: boundary, identity, and mode. Named headers (E) add a fourth: a short mnemonic label the agent can use to track progress. Markdown lists (D) use the LLM's training on list structures to implicitly communicate "these are discrete items." Test: does explicit numbering reduce step-skipping? Does mode-integrated numbering produce better mode compliance than separate mode labels?
- STABILITY: structural (step delimiters are foundational) + experimental (the specific delimiter form)

**step_index_tracking**
- Current (defective): no index — steps are not numbered, agent cannot refer to "step 3"
- Alternative A: Sequential numbers: Step 1, Step 2, Step 3
- Alternative B: Sequential numbers with total: Step 1/7, Step 2/7, Step 3/7 — agent always knows how many steps remain
- Alternative C: No numbers — steps are identified by their content, not by position. Numbering may cause the agent to over-focus on ordinal position rather than content.
- Alternative D: Descriptive identifiers instead of numbers: "Input Parsing", "Core Analysis", "Output Formatting" — each step gets a name derived from its content
- PURPOSE: Gives the agent a way to track where it is in the sequence. Without indices, the agent must maintain its own internal count.
- HYPOTHESIS: No index (current) means the agent may lose track in long instruction sets (7 steps for builder). Sequential numbers (A) provide basic tracking. Numbers with totals (B) add completion awareness — "I am on step 4 of 7, past the halfway point." This may affect pacing: the agent knows how much is left. Descriptive identifiers (D) provide tracking through meaning rather than position, which may improve recall but loses the sequential primacy signal. Test: does step-count awareness (B) improve execution quality for long instruction sets? Does it cause rushing on later steps?
- STABILITY: formatting (numbering style) + structural (whether to number at all)

---

## STRUCTURAL: step_mode_distribution_pattern
TYPE: n/a

### What the agent needs to understand

The two reference agents have very different mode distributions:
- agent-builder: D, P, P, P, P, P, D — bookended by deterministic steps with five probabilistic steps in the middle
- interview-summary: D, P, D, P, P — alternating pattern with a deterministic constraint step sandwiched between probabilistic reasoning steps

These patterns communicate different things about the task:
- The builder's "bookend" pattern says: "Start with mechanical input reading, do a long stretch of creative work, end with mechanical output mapping."
- The summarizer's "alternating" pattern says: "Read mechanically, reason, enforce a hard constraint, reason some more, reason with caution."

The pattern itself is meaningful. A long stretch of probabilistic steps tells the agent it is in an extended creative/judgment zone. A deterministic step interrupting a probabilistic sequence is a checkpoint — "stop reasoning and apply this rule exactly."

### Fragments

**mode_pattern_awareness**
- Current (defective): no awareness — modes are invisible
- Alternative A: No explicit pattern communication — if modes are visible per-step (via mode_indicator), the agent discovers the pattern as it reads. Stating the pattern upfront is redundant.
- Alternative B: A preamble that describes the pattern: `Steps 1 and 7 are exact compliance. Steps 2-6 require your judgment.` — explicit pattern statement
- Alternative C: A visual overview before the detailed steps — a compact summary showing all steps with modes:
  ```
  Step 1 [EXACT]: Read input
  Step 2 [JUDGMENT]: Identify domain
  Step 3 [JUDGMENT]: Design steps
  ...
  ```
  Then the detailed steps follow.
- PURPOSE: Decides whether the agent should see the overall mode pattern before encountering individual steps.
- HYPOTHESIS: Upfront pattern awareness (B/C) gives the agent a map of the cognitive terrain before traversing it. It knows where the judgment zones are and where the compliance checkpoints are. This may improve planning and pacing. But it also adds length and may cause the agent to "skip ahead" mentally to the judgment steps. Step-by-step discovery (A) means the agent encounters each mode shift fresh, which may produce more attentive per-step compliance. Test: does an upfront step/mode overview improve execution quality for long instruction sets (7+ steps)?
- STABILITY: experimental — this fragment type does not exist in any current agent

---

## STRUCTURAL: deterministic_step_presentation vs. probabilistic_step_presentation
TYPE: n/a

### What the agent needs to understand

Beyond labeling the mode, there is a question of whether deterministic and probabilistic steps should be presented *differently* — not just labeled differently, but structurally different.

### Fragments

**differential_step_formatting**
- Current (defective): all steps rendered identically as paragraphs regardless of mode
- Alternative A: Deterministic steps in a code-block-like format (indented, monospace, or fenced) to signal "execute literally." Probabilistic steps in normal flowing prose to signal "reason freely."
- Alternative B: Deterministic steps as bulleted lists of sub-operations. Probabilistic steps as paragraphs. The structural difference carries the mode signal.
- Alternative C: No differential formatting — the mode indicator label is sufficient. Adding visual differences risks confusing formatting meaning with mode meaning.
- Alternative D: Deterministic steps are shorter and use imperative verbs ("Read X. Parse Y. Validate Z."). Probabilistic steps are longer and use reasoning verbs ("Assess whether... Evaluate how... Determine if..."). This is not a formatting choice — it is already implicit in the instruction text. The question is whether the template should enforce this pattern or let it emerge naturally from the authored text.
- PURPOSE: Makes the mode difference perceptible through visual/structural channels in addition to (or instead of) explicit labels.
- HYPOTHESIS: Humans and LLMs both respond to formatting cues below conscious processing. A code-block formatted deterministic step may trigger more literal, mechanical processing than the same text in a normal paragraph. Bulleted sub-operations make the mechanical nature explicit by decomposing the step into atomic operations. Test: does code-block formatting for deterministic steps reduce hallucination/expansion on those steps? Does normal-prose formatting for probabilistic steps increase reasoning depth?
- STABILITY: experimental — high-risk, high-reward. Wrong visual coding could confuse rather than guide.

---

## STRUCTURAL: context_carry_between_steps
TYPE: n/a

### What the agent needs to understand

Steps are not independent. The summarizer's step 2 (write contextual summaries) depends on step 1 (read and parse input). The builder's step 4 (create examples) depends on step 1 (read preparation package — which provides the data for examples). Some steps explicitly reference earlier steps' outputs.

But nothing in the current presentation signals these dependencies. The agent must infer them from the instruction text.

### Fragments

**dependency_signaling**
- Current (defective): no explicit dependency signaling — steps are presented as a flat sequence
- Alternative A: Explicit dependency annotations: `Step 4 (uses: preparation package from Step 1):` — step headers name their inputs
- Alternative B: No explicit dependencies — the instruction text within each step names its inputs. The agent should infer dependencies from content, not from metadata. Adding dependency annotations duplicates information.
- Alternative C: A dependency preamble for steps that reference earlier work: `Building on the preparation package you read in Step 1:` followed by the step's instruction text
- Alternative D: Implicit through ordering alone — the steps are ordered so that each step can use the outputs of all prior steps. No annotation needed because the linear order IS the dependency graph.
- PURPOSE: Helps the agent maintain state across steps. If Step 4 needs the preparation package from Step 1, the agent must remember that it read a preparation package three steps ago.
- HYPOTHESIS: For short instruction sets (3-5 steps), implicit ordering (D) is probably sufficient — the agent's context window easily holds all prior steps. For longer sets (7+ steps), the agent may lose track of earlier outputs, and explicit references (A/C) may improve recall. Test: for 7-step agents, does explicit dependency annotation reduce cases where the agent forgets to use earlier outputs?
- STABILITY: conditional (based on instruction count) + experimental (whether to annotate at all)

---

## STRUCTURAL: section_closer
TYPE: n/a

### What the agent needs to understand

The instructions section ends and another section begins. The transition affects whether the agent treats the instructions as a complete program to execute, or as context that flows into the next section.

### Fragments

**section_transition**
- Current (defective): last instruction step ends, then `---` horizontal rule, then next section heading
- Alternative A: `---` only — clean break, no prose
- Alternative B: A closing summary: `These {N} steps are your complete procedure. Execute them in order.` — reinforces the section's purpose and the sequential execution model
- Alternative C: No closing — the last step's text flows directly into the `---` divider
- Alternative D: A completion marker: `End of instructions.` — explicit signal that no more steps follow
- PURPOSE: Signals the end of the instruction sequence. Without a clear end marker, the agent may treat content from the next section (examples, constraints) as additional instruction steps.
- HYPOTHESIS: A closing summary (B) reinforces the "ordered program" framing and gives the agent a sense of completeness. An explicit "End of instructions" (D) is the strongest boundary signal but feels mechanical. No closing (A/C) relies on the next section's heading to signal the transition. Test: does a closing summary reduce bleeding of post-instruction content into the execution model?
- STABILITY: structural (whether to close) + formatting (the closing text)

---

## CROSS-FIELD DEPENDENCIES

### instruction_mode + instruction_text (per step)
These two fields form a unit. The mode tells the agent HOW to process the text. The text tells the agent WHAT to do. Presenting them separately (mode as a header label, text as body) or integrated (mode as a behavioral preamble sentence within the text) is a fundamental design choice.

### instructions.steps -> identity.role_description
The role description sets the cognitive stance. The instruction steps operationalize it. For the summarizer, the role description says "meaning depends on conversation before it" — then Step 2 operationalizes this as "write one sentence that captures what this exchange signifies given everything that came before it." The instructions section must be consistent with the identity section's cognitive frame. If the identity says "data forms, not prose documents" but the instructions ask for "elegant narrative descriptions," the agent will be confused.

### instructions.steps -> examples
Instruction steps describe what to do. Examples show what correct execution looks like. For the builder, Step 3 says "design the instruction steps" — the examples section shows a concrete example of good vs. bad instruction step design. The instruction steps create expectations that the examples section must fulfill. In the summarizer, the instruction text itself CONTAINS inline examples (thin content / rich context scenarios). This means the instructions section already partially fills the role of the examples section.

### instructions.steps -> constraints / anti_patterns
Several constraints restate or reinforce instruction step content. The summarizer's constraints include "MUST process exchanges in order" — which is also stated in instruction step 1. This creates a question: should constraints that duplicate instruction content be rendered in both places, or should the instructions section defer to the constraints section?

### instructions.steps -> critical_rules
Critical rules may add operational steps that are NOT in the instruction steps. The summarizer's critical rules add "batch discipline — process exactly 20 records per batch" — this is not an instruction step, but it affects HOW instruction steps are executed. The instruction section must not contradict or complicate the critical rules, and the agent must understand that critical rules may modify how instructions execute.

### instruction count -> section preamble, step tracking, closing
The number of steps affects several structural decisions: whether to include a count in the heading or preamble, whether step numbers include totals (Step 3/7), and whether a closing summary is needed. This creates a conditional dependency on the length of the steps array.

---

## CROSS-SECTION DEPENDENCIES

### instructions -> identity
The identity section's role_description often foreshadows the instructions. The summarizer's role_description establishes the contextual-meaning-vs-isolation principle. Steps 2, 4, and 5 all operationalize this principle. If the identity is read first (which it is), the agent should arrive at the instructions section already primed with the cognitive stance the instructions operationalize.

### instructions -> writing_output / critical_rules
For agents with output tools, the critical_rules section adds batch discipline and tool invocation requirements that modify instruction execution. The instruction steps describe WHAT to do; the critical rules and writing_output sections describe HOW to physically output the work. The instructions must not contain operational output content (which would duplicate and potentially contradict the writing_output section).

### instructions -> success_criteria / failure_criteria
Success and failure criteria describe what correct and incorrect instruction execution looks like. Every success criterion should correspond to something the instructions ask for. Every failure criterion should correspond to a way the instructions can be executed incorrectly. The instructions section creates the contract; the criteria sections define compliance.

---

## CONDITIONAL BRANCHES

### Variable step count
The builder has 7 steps. The summarizer has 5. The number of steps affects:
- Whether a preamble with count is useful (7 steps = yes; 3 steps = probably not)
- Whether step-count tracking (Step 3/7) adds value or overhead
- Whether a closing summary is warranted
- How much structural scaffolding is needed to maintain step boundaries

A 3-step agent may need minimal scaffolding: a heading, three numbered paragraphs, done. A 10-step agent may need a table of contents, step headers with sub-headings, and explicit dependency annotations.

### Variable mode distribution
The builder has 5 probabilistic and 2 deterministic steps. The summarizer has 3 probabilistic and 2 deterministic. For an agent that is ALL deterministic (a pure mechanical processing agent), the mode marking may be unnecessary — or it may be maximally important as reinforcement against hallucination. For an agent that is ALL probabilistic, mode marking may be unnecessary because there is never a mode switch to signal.

Mixed-mode agents benefit most from mode marking because the switches are the critical behavioral transitions. The density of mode switches may also matter — the summarizer's D/P/D/P/P pattern has a mode switch between every pair of the first four steps, while the builder's D/P/P/P/P/P/D pattern has only two switches.

### Variable instruction_text length
Steps range from single sentences to 200-word multi-paragraph blocks. Short steps may benefit from compact presentation (inline with the step header). Long steps need their own visual space with clear boundaries. This is a conditional formatting decision based on text length.

### Presence of inline examples in instruction_text
The summarizer's Steps 2 and 5 contain inline examples within the instruction text (thin content scenarios, marker examples). The builder's instruction steps do not contain inline examples. When instruction text contains examples, the step is harder to delimit visually because the example content looks like separate paragraphs. This creates a conditional need for stronger step containers when inline examples exist.

### Steps that reference other steps
Some instruction texts explicitly reference earlier steps ("Use the sample records from the preparation package" in builder Step 4 references Step 1's package reading). Others are self-contained. The presence of cross-step references creates a conditional need for step identity (numbering/naming) that other steps can refer to.

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### cognitive_transition_markers
Between steps, especially at mode transitions, a brief marker could signal the cognitive shift:
- Between a deterministic and probabilistic step: `— Now apply your judgment —`
- Between a probabilistic and deterministic step: `— Execute the following exactly —`
- Between two probabilistic steps: no marker (same mode continues)

This fragment type does not map to any data field. It is derived from the mode transition pattern between adjacent steps. It exists purely to signal cognitive gear-shifts.

**PURPOSE:** Makes mode transitions explicit and salient. The mode indicator on each step tells the agent the current mode; the transition marker tells the agent the mode is CHANGING.

**HYPOTHESIS:** Mode switches without transition markers may be too subtle — the agent reads a new step label but doesn't shift its processing posture. An explicit "now shift gears" marker between steps may produce stronger mode compliance. However, it also adds noise, and for agents with many mode switches (D/P/D/P/P), it may become repetitive. Test: do transition markers at D-to-P and P-to-D boundaries improve mode compliance? Do they degrade for high-frequency switching?

**STABILITY:** experimental — this fragment type does not exist anywhere in the system

### progress_anchor
For long instruction sets, a periodic anchor that reminds the agent of its position:
- After step 4 of 7: `You are past the halfway point. Steps 1-4 have established the foundation. Steps 5-7 refine and validate.`
- This is NOT in the instruction text. It is a structural fragment generated by the template based on the step count and position.

**PURPOSE:** Prevents the "lost in the middle" effect where the agent gives less attention to steps in the middle of a long sequence. This is a known phenomenon in LLM attention patterns — middle content receives less weight than beginning and end content.

**HYPOTHESIS:** Progress anchors at the midpoint of long instruction sets may improve attention to middle steps. They may also create a false sense of "phase transitions" that the instruction author did not intend. Test: does a midpoint progress anchor improve execution quality of steps 3-5 in a 7-step agent?

**STABILITY:** experimental + conditional (only for instruction sets above some length threshold)

### step_completion_expectation
Nothing in the current system tells the agent what "completing a step" means. Does the agent produce visible output after each step? Does it simply advance to the next step internally? Should it checkpoint its state?

- Alternative A: `After each step, proceed to the next. Do not produce interim output unless the step explicitly requests it.`
- Alternative B: `Each step should produce a clear intermediate result, even if it's only in your working memory.`
- Alternative C: No explicit completion model — the agent determines step completion from the instruction text.

**PURPOSE:** Configures whether the agent treats steps as internal checkpoints (advance through them) or as output-producing stages (each step has a visible deliverable).

**HYPOTHESIS:** For agents that write output (summarizer), steps may naturally produce output because the task is batch processing. For agents that build a complex artifact (builder), steps build toward a final output and intermediate checkpoints may be helpful for quality. An explicit completion model may reduce cases where the agent "blends" adjacent steps by proceeding to the next before finishing the current one. Test: does an explicit "complete each step before proceeding" instruction reduce step-blending errors?

**STABILITY:** experimental

### instruction_text_is_authoritative
Nothing currently tells the agent that the instruction text is the complete specification for each step — that nothing should be added, and nothing should be inferred from general knowledge. For deterministic steps especially, the instruction text IS the program. The agent should not "help" by adding operations it thinks are useful.

- Alternative A: A preamble: `Each instruction step is a complete specification. Do not add operations, interpret ambiguity as an invitation to expand, or supplement steps with general knowledge.`
- Alternative B: This constraint belongs in critical_rules, not instructions. The instruction section should state what to do; the rules section should state what NOT to do.
- Alternative C: This is implicit in the mode system — deterministic steps mean "execute exactly this," which implies "do not add." Making it explicit may be redundant.

**PURPOSE:** Prevents the LLM's strongest instinct: being helpful by expanding, interpreting, and adding to instructions.

**HYPOTHESIS:** Without this explicit anti-expansion directive, agents will add operations to steps — especially probabilistic steps where they feel they have latitude. The directive pre-empts this behavior. But it may also suppress genuinely useful reasoning on probabilistic steps where some expansion is desirable. This fragment may need to be scoped to deterministic steps only. Test: does an anti-expansion directive reduce hallucination on deterministic steps without degrading reasoning quality on probabilistic steps?

**STABILITY:** experimental — directly addresses a core LLM failure mode
