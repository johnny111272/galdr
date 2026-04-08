# INPUT — Control Surface Synthesis

## Section Purpose

The input section answers: **where does my work come from?** It configures three things in the agent's cognition: (1) what data arrives and in what shape, (2) what prerequisite knowledge must be absorbed before touching that data, and (3) what concrete handles (parameters) the agent uses to locate everything.

Both analyses converged on a critical structural insight: the input section contains two fundamentally different concerns that must not be conflated. The **payload** (tempfile + description + format) is material to transform. The **preparation** (context_required) is knowledge to absorb. An agent that confuses these — treating context documents as data to process, or treating the tempfile as knowledge to internalize — will produce degraded output. The rendering must enforce this separation.

Both analyses also converged on a secondary signal: the input section's *shape* telegraphs task type. Text format + many context documents = knowledge-intensive creative work. JSONL format + zero context documents = tight batch processing. This correlation is not a rule (all four combinations are valid), but it is a strong cognitive primer that the rendering can leverage.

## Fragment Catalog

### section_heading
- CONVERGED: A heading is needed. Both favor minimal framing over ceremonial transitions.
- DIVERGED: A named the two sub-blocks in one option ("Data and Context"); B kept it simpler. A considered metaphorical headings ("Starting Materials"); B did not.
- ALTERNATIVES:
  - A: `## Input` — neutral, familiar, zero cognitive overhead
  - B: `## What You Receive` — active framing that establishes the agent was just handed something
  - C: `## Data and Context` — previews the section's two-part structure for context-heavy agents
- HYPOTHESIS: Minimal heading is safest as a default. "Data and Context" is interesting only when context_required is present but risks confusion when absent.
- STABILITY: structural
- CONDITIONAL: If context_required is absent, option C is misleading — use A or B.

### section_preamble
- CONVERGED: Simple sections (no context_required) need no preamble. Complex sections benefit from one.
- DIVERGED: A proposed conditional preambles (different text with/without context); B proposed minimal or no preamble universally.
- ALTERNATIVES:
  - A: No preamble — open directly with content (when context_required absent)
  - B: `Before processing your input, you must read and internalize several reference documents. Your input data and prerequisite knowledge are described below.` (when context_required present)
- HYPOTHESIS: Conditional preamble is the right pattern. The with-context preamble explicitly names the knowledge-acquisition requirement, priming thorough reading. The without-context case needs nothing.
- STABILITY: experimental
- CONDITIONAL: Present only when context_required is non-empty.

### sub_block_ordering
- CONVERGED: Both independently reached the same conclusion: **description + format → context_required → parameters**. This follows the cognitive hierarchy: what → knowledge → mechanics.
- DIVERGED: None. This is the highest-confidence convergence in the analysis.
- ALTERNATIVES:
  - A: description/format → context_required → parameters (the convergent choice)
  - B: context_required → description/format → parameters (knowledge-first, untested)
- HYPOTHESIS: Description-first mirrors natural briefing order: "Your job involves X. Here is the background reading. Here are the files on your desk."
- STABILITY: structural
- CONDITIONAL: none

### delivery_declaration
- CONVERGED: Both noted delivery is currently invariant ("tempfile") and may not need explicit rendering. Both observed that the parameter named "tempfile" already carries the delivery semantics.
- DIVERGED: A more strongly considered omitting delivery entirely; B treated it as a distinct fragment worth rendering.
- ALTERNATIVES:
  - A: Omit — the tempfile parameter is self-explanatory
  - B: `Your input arrives as a temporary file at the path specified below.` — one sentence, links to parameter
  - C: Weave delivery into description: `Your input is a {format} tempfile containing {description}.`
- HYPOTHESIS: Delivery + description + format are best rendered as a single integrated statement. Separate delivery declaration adds redundancy in a system where delivery is always "tempfile."
- STABILITY: structural (near-constant value)
- CONDITIONAL: If non-tempfile delivery types emerge, this becomes a critical dispatch point.

### input_description_presentation
- CONVERGED: Description is the agent's first mental model of its data. It must be presented before the agent encounters raw data. Both favor presenting description verbatim from the definition.
- DIVERGED: A explored integrated presentation (description + format in one sentence) more thoroughly; B treated them as separate but coupled fields.
- ALTERNATIVES:
  - A: `Your input is a {format} file containing {description}.` — integrated, information-dense, one sentence
  - B: `You will receive: {description}` — preview framing, creates temporal expectation
  - C: `{description}. This arrives as a {format} tempfile at the path given below.` — description leads, format follows as logistics
- HYPOTHESIS: Integrated presentation (A) is strongest — the agent learns what and how in one sentence. Separating description from format creates two partial mental models that the agent must combine.
- STABILITY: formatting (label choice), experimental (framing strategy)
- CONDITIONAL: none

### negative_boundary_in_description
- CONVERGED: Both identified that some descriptions contain negative information ("no learned, threads, or insight fields") and that this is an anti-hallucination measure.
- DIVERGED: A explored elevating the negative boundary to a warning; B suggested rendering descriptions as-is and trusting the definition author.
- ALTERNATIVES:
  - A: Pass through as-is — the negative clause is part of the description text
  - B: Split into positive/negative: `Contains: {fields}. Excluded: {excluded_fields}.` — structural separation makes absence impossible to miss
- HYPOTHESIS: Structural separation (B) is safer for agents processing structured data (JSONL) where field expectations matter. Pass-through (A) is fine for text-format agents where field-level precision is less critical. However, the renderer cannot reliably detect negative boundaries in free text, which argues for A unless the definition format evolves to separate positive/negative descriptions.
- STABILITY: experimental
- CONDITIONAL: Only relevant when description contains explicit negative boundaries. Currently not machine-detectable.

### format_declaration
- CONVERGED: Format is a critical behavioral switch. "text" = holistic reading, "jsonl" = per-record processing. Both identified this as having outsized influence on the agent's cognitive mode.
- DIVERGED: A pushed harder on format-specific operational prose; B was more conservative (declare format, let execution handle the rest).
- ALTERNATIVES:
  - A: Integrated with description (see input_description_presentation above)
  - B: Format-specific operational prose: `text` → "Read as a whole to build understanding." / `jsonl` → "One JSON object per line. Each line is one work unit."
- HYPOTHESIS: Format-specific operational prose (B) directly configures the agent's reading strategy and may reduce parsing errors for JSONL. But this guidance may belong in the first execution step rather than the input section. Design question: does the parsing directive live in input or execution?
- STABILITY: formatting (declaration style), experimental (operational prose), conditional (prose varies by format value)
- CONDITIONAL: Prose content changes based on format value. Always present as a field.

### context_section_heading
- CONVERGED: When present, context_required needs its own sub-heading to separate it from the payload.
- DIVERGED: A favored "Required Reading" for its educational obligation framing; B suggested "Before You Begin" or "Prerequisites" alongside "Required Reading."
- ALTERNATIVES:
  - A: `### Required Reading` — evokes educational obligation, signals depth of engagement expected
  - B: `### Before You Begin` — temporal framing, explicitly sequences reading before work
- HYPOTHESIS: "Required Reading" is the strongest label — it tells the agent both WHAT (documents to read) and HOW (as study material, not reference). "Before You Begin" tells WHEN but not HOW.
- STABILITY: experimental (label choice directly affects reading depth)
- CONDITIONAL: Present only when context_required is non-empty.

### context_preamble
- CONVERGED: Both agreed the most critical distinction is between "reference" (consult during work) and "prerequisite" (absorb before work). The preamble must establish the latter.
- DIVERGED: A explored stakes framing ("your work quality depends on..."); B preferred balanced instruction-plus-purpose.
- ALTERNATIVES:
  - A: `Read and internalize the following documents before processing your input. These establish the principles and reference structures your work depends on.` — instruction + purpose
  - B: `These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting.` — explicitly distinguishes reference vs. prerequisite modes
- HYPOTHESIS: B is stronger because it names and dismisses the wrong mental model ("not reference materials to consult") before establishing the right one. This pre-empts the most common failure mode.
- STABILITY: experimental (directly configures knowledge-acquisition behavior)
- CONDITIONAL: Present only when context_required is non-empty.

### context_entry_template
- CONVERGED: Label-first presentation. Both agreed the label is more important for the agent's understanding; the path is more important for the agent's action. Label should lead.
- DIVERGED: A explored numbered lists (implying reading order) more thoroughly; B favored bullets as default with numbered as an option.
- ALTERNATIVES:
  - A: `- **{context_label}**: Read `{context_path}`` — bulleted, label-first, action verb
  - B: Numbered list with same format — implies reading order, may produce more sequential engagement
  - C: `- **{context_label}** (`{context_path}`)` — compact, path as parenthetical
- HYPOTHESIS: Numbered list (B) is better for agents with 4+ context documents where reading order genuinely matters (template before philosophy before specifics). Bullets (A) are fine for small lists. Paths must always be rendered verbatim as absolute paths — no abbreviation.
- STABILITY: formatting (list style)
- CONDITIONAL: Numbered vs. bulleted may depend on whether the definition author specified an intentional ordering.

### context_absent_handling
- CONVERGED: **Silence.** Both analyses independently and unambiguously concluded: when context_required is absent, render nothing. Do not mention it. Do not say "you have no required reading."
- DIVERGED: A explored whether explicit absence ("this agent requires no external knowledge") might prevent information-seeking behavior; B dismissed this.
- ALTERNATIVES:
  - A: Silence — the concept of prerequisite knowledge never enters the agent's prompt
- HYPOTHESIS: Mentioning the absence of something creates noise and may paradoxically prime the agent to think about what it does not have. Silence is always correct here.
- STABILITY: structural (very high confidence)
- CONDITIONAL: This IS the condition — applies only when context_required is absent.

### parameters_section_heading
- CONVERGED: Parameters need clear presentation but are reference material, not narrative.
- DIVERGED: A explored "What You Received" for ownership framing; B stayed with minimal heading or no heading.
- ALTERNATIVES:
  - A: `### Parameters` — neutral, familiar
  - B: No heading — parameters presented inline after description/format, especially for 1-parameter agents
- HYPOTHESIS: For 1-2 parameters, inline presentation works and avoids structural overhead. For 3+ parameters, a heading improves scannability.
- STABILITY: formatting
- CONDITIONAL: Inline vs. headed may depend on parameter count.

### parameter_entry_template
- CONVERGED: Code-formatted parameter names signal literal identifiers. Both favor compact, scannable presentation.
- DIVERGED: A explored table format for multi-parameter agents; B explored natural prose integration.
- ALTERNATIVES:
  - A: `- \`{param_name}\` ({param_type}): {param_description}` — bulleted, all fields inline, code-formatted name
  - B: Prose for small lists: `You receive a tempfile path pointing to the JSONL input, and a uid string identifying the interview.`
  - C: Table for 3+ parameters with Name | Type | Description columns
- HYPOTHESIS: Bulleted with code-formatted names (A) is the best default — scannable, precise, and signals the name is a literal identifier. Prose (B) works for 1-parameter agents where a list of one feels odd.
- STABILITY: formatting
- CONDITIONAL: Presentation style may shift based on parameter count (1 → prose, 2-3 → bullets, 4+ → table).

### parameter_required_rendering
- CONVERGED: When all parameters are required, the "required" label is noise. Both favor omitting it in the all-required case.
- DIVERGED: None meaningful.
- ALTERNATIVES:
  - A: Omit when all parameters are required
  - B: Show `(required)` / `(optional)` only when there is a mix
- HYPOTHESIS: Required/optional distinction becomes meaningful only when parameters have different required values. Until then, omit.
- STABILITY: conditional
- CONDITIONAL: Show only when the parameter set contains both required and optional entries.

### knowledge_data_separator
- CONVERGED: Both identified that context_required and payload must be visually and conceptually separated to prevent conflation.
- DIVERGED: A proposed a cognitive transition sentence; B proposed sub-headings.
- ALTERNATIVES:
  - A: Transition sentence: `With this knowledge internalized, here is your input data:` — explicit cognitive shift from learning to operating
  - B: Sub-headings that name each block (handled by context_section_heading + parameters_section_heading)
- HYPOTHESIS: The transition sentence (A) is stronger because it explicitly names the cognitive shift. Sub-headings provide structure but do not articulate the mode change.
- STABILITY: structural (whether to separate), experimental (phrasing)
- CONDITIONAL: Present only when context_required is non-empty.

### section_closer
- CONVERGED: The transition from input to execution is one of the most important cognitive shifts in the prompt.
- DIVERGED: A proposed a readiness checkpoint ("Confirm you have: ..."); B proposed minimal transition or none.
- ALTERNATIVES:
  - A: `---` divider only — clean break, let the next section heading carry the transition
  - B: Readiness checkpoint: `Confirm you have: (1) your input data at the tempfile path, (2) knowledge from all {N} reference documents. Now proceed.` — forces mental verification
- HYPOTHESIS: Readiness checkpoint (B) is high-leverage for context-heavy agents — it forces the agent to mentally verify its starting state. For no-context agents, a bare divider (A) suffices.
- STABILITY: experimental (content), conditional (checkpoint content varies with context_required)
- CONDITIONAL: Checkpoint warranted only when context_required is non-empty.

### input_completeness_assertion
- CONVERGED: Both recognized this as a novel fragment not present in the current system.
- DIVERGED: A explored it more thoroughly; B did not identify it as a distinct fragment.
- ALTERNATIVES:
  - A: `Your tempfile and required reading together constitute your complete input. Do not seek additional sources.`
  - B: Omit — infer completeness from the absence of seek-more instructions
- HYPOTHESIS: Explicit completeness assertion reduces caveat-hedging ("I would need more information to...") in autonomous dispatched agents that cannot ask follow-up questions. Worth testing.
- STABILITY: experimental
- CONDITIONAL: May be more important for context-heavy agents where the boundary of "everything you need" is less obvious.

### context_document_purpose_annotations
- CONVERGED: Both recognized that labels alone ("Bland Is Correct") are evocative but not explanatory.
- DIVERGED: Only A identified this as a distinct fragment opportunity with explicit alternatives.
- ALTERNATIVES:
  - A: Append purpose to entry: `- **Bland Is Correct** — the quality standard for your writing style: Read \`{path}\``
  - B: Rely on labels alone — trust the definition author's label choice
- HYPOTHESIS: Purpose annotations direct reading attention and may significantly improve knowledge extraction. Risk: narrowing the agent's reading to only what the annotation says. This is a high-leverage experimental fragment, but requires annotation data that does not currently exist in the definition format.
- STABILITY: experimental
- CONDITIONAL: Only possible if the definition format evolves to include purpose annotations per context entry.

## Cross-Section Dependencies

- **input.description ↔ identity.description**: Different fields, different values, must be coherent. Identity says what the agent does; input says what it receives.
- **input.format → execution.steps[0]**: The first instruction step almost always references the input format. If input says "jsonl" but step 1 says "read as text," the agent is confused.
- **input.context_required → security.paths.allowed_read**: Context paths must be within read grants. An agent told to read a file it cannot access creates a contradictory instruction.
- **input.parameters ↔ dispatcher.parameters**: Same data, different rendering contexts. Must be identical.
- **input.parameters.uid → output.name_template**: The uid parameter is construction material for the output filename. Input and output sections are linked through this parameter.
- **input.context_required → execution**: Knowledge from context documents shapes how the agent executes. The execution section assumes this knowledge has been absorbed.
- **input → critical_rules**: Batch discipline rules (e.g., batch_size = 20) modify how input data flows through the agent. Input describes the data; critical_rules constrain its processing.

## Conditional Branches

- **context_required present vs. absent** → Primary branch. When present: render reading list sub-block with heading, preamble, entries, knowledge-data separator, readiness checkpoint. When absent: skip all of these silently. Section length varies 3-5x.
- **format = "text" vs. "jsonl"** → Determines whether operational prose says "read holistically" or "process per-record." Affects description framing and may influence first execution step.
- **parameter count: 1 vs. 2-3 vs. 4+** → Shifts parameter presentation from prose/inline to bullets to table.
- **all parameters required vs. mixed** → Controls whether required/optional labels appear.
- **format x context_required (2x2 matrix)** → All four combinations are valid. The common cases are text+context (knowledge-intensive) and jsonl+no-context (batch), but the design must handle jsonl+context and text+no-context cleanly.

## Open Design Questions

1. **Where does format-specific operational guidance live — input or execution?** Both analyses identified that format ("read holistically" vs. "process per line") directly configures the agent's first action. Input describes it; execution uses it. Placing the guidance in input pre-configures the cognitive stance early but creates overlap with step 1 of execution.

2. **Should context_required entries be numbered (implying order) or bulleted (implying set)?** For agents with many context documents that have a natural pedagogical sequence, numbering may improve knowledge integration. But numbering imposes order that the definition author may not have intended.

3. **Is an explicit input_completeness_assertion worth its token cost?** It may reduce caveat-hedging in autonomous agents, but it is also something the agent could infer from the absence of seek-more instructions. No data yet on whether this changes behavior.

4. **Should the definition format evolve to support purpose annotations on context entries?** Currently labels are the only metadata per context document. Purpose annotations could significantly improve reading quality but require schema changes.

5. **Should delivery be rendered at all when it is invariant?** Both analyses noted "tempfile" is currently the only delivery mechanism. Rendering it explicitly may be wasted tokens, but omitting it leaves an architectural gap if new delivery types appear.

## Key Design Decisions

1. **Integrated description+format presentation** — Render description and format as a single sentence rather than separate fields. Both analyses lean toward integration. This is the most information-dense approach and avoids partial mental models. Direction: integrate.

2. **Conditional preamble based on context_required** — The section needs different openings for knowledge-heavy and self-contained agents. Direction: conditional preamble that names the knowledge-acquisition requirement when context_required is present; no preamble when absent.

3. **"Absorb before starting" framing for context_required** — The preamble must explicitly distinguish prerequisite knowledge from reference material. Direction: name and dismiss the wrong mental model ("not reference materials to consult") before establishing the correct one.

4. **Knowledge-data separator as a cognitive transition sentence** — When context_required is present, an explicit sentence marking the shift from "learning mode" to "operating mode" prevents conflation. Direction: use a transition sentence, not just a structural divider.

5. **Silence for absence** — When optional blocks (context_required) are absent, emit nothing. Do not acknowledge what is not there. This is the highest-confidence convergent finding across both analyses. Direction: established.
