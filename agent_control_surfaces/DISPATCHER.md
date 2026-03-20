# DISPATCHER -- Control Surface Synthesis

## Section Purpose

The dispatcher section is architecturally unique: it renders into a SKILL.md file that programs the CALLER, not the agent. Both analyses converge on this being an interface specification -- a mini-prompt that teaches a parent agent (or human) the single skill of invoking this specific agent. The audience is external; every design decision must serve the caller's question: "Can I correctly dispatch this agent given only this document?"

The rendered SKILL.md maps to the caller's lifecycle: decide, prepare, invoke, manage, consume. The dispatcher's fields are declarative data, but the output is prose instructions. The rendering layer -- translating field combinations into qualitatively different instruction structures -- is where the real design complexity lives. A single-agent foreground dispatch produces fundamentally different prose than a multi-agent background fan-out, even though both draw from the same field set.

## Fragment Catalog

### `agent_name`

- CONVERGED: Pure machine-readable identifier. Foreign key into agent registry. Appears verbatim in Task tool invocation. Not a display name.
- DIVERGED: A treats as data-only; B emphasizes dual use (document identity + literal invocation string).
- ALTERNATIVES:
  - A: Bare string field -- lookup key, nothing more
  - B: Rendered twice -- once as document header, once as invocation handle in the dispatch template
- HYPOTHESIS: The name serves two rendering sites (header identity + invocation reference) but is one atomic value. The rendering layer, not the data model, handles this.
- STABILITY: structural
- CONDITIONAL: none

### `agent_description`

- CONVERGED: Caller-facing decision support. Answers "what does this agent do?" from the outside. Mirrors identity.description semantically.
- DIVERGED: A focuses on whether to independently author vs. reference canonical description. B focuses on framing -- "what it does" vs. "when to dispatch it" are different prompts that produce different prose.
- ALTERNATIVES:
  - A: "When to Dispatch" framing -- tells the caller the triggering condition, not just the capability. Most actionable for LLM callers making routing decisions.
  - B: "What This Agent Does" + one-line dispatch trigger -- combines capability summary with decision support.
  - C: Independent prose field, caller-optimized. Accept duplication with identity.description; the audiences differ enough to justify separate authoring.
- HYPOTHESIS: Framing as "when to use" produces better autonomous dispatch decisions than framing as "what it does." The former is a match condition; the latter is a label.
- STABILITY: formatting
- CONDITIONAL: none

### `dispatch_mode`

- CONVERGED: Both examples show "full." Field existence is stable; enum values are underdetermined with only one observed value.
- DIVERGED: A reads "full" as "send everything at once" (delivery semantics). B reads "full" as "agent handles complete task, no follow-up needed" (lifecycle semantics). These are meaningfully different interpretations.
- ALTERNATIVES:
  - A: Simple enum {full, batch} -- delivery semantics, how input is chunked
  - B: Lifecycle enum {full, partial, advisory} -- completion semantics, what the caller does after
  - C: Default-implicit -- "full" is the assumed default; only render non-full modes
- HYPOTHESIS: The semantic ambiguity (delivery vs. lifecycle) must be resolved before this field can be rendered. If "full" is the only value in practice, consider deferring the field entirely until a second mode materializes.
- STABILITY: experimental
- CONDITIONAL: Rendering behavior depends on whether non-full modes exist. If only "full," omit from rendered output.

### `background_mode`

- CONVERGED: Binary enum {allowed, forbidden}. "forbidden" = caller MUST wait. "allowed" = caller MAY background. Critical dispatch constraint.
- DIVERGED: Minor. A considers ternary with "required"; B does not.
- ALTERNATIVES:
  - A: Constraint statement -- "Background execution: FORBIDDEN. Wait for completion."
  - B: Integrated into invocation instructions -- weave directly into the dispatch how-to
  - C: Lifecycle-oriented -- explain operational implications ("you can continue with other work" vs. "do not dispatch other dependent work")
- HYPOTHESIS: For LLM callers, the operational implication (what to DO differently) matters more than the label. Lifecycle framing (C) outperforms bare constraint (A).
- STABILITY: structural
- CONDITIONAL: Rendered prose is fully conditional on the value. Two distinct prose blocks required.

### `max_agents`

- CONVERGED: Hard ceiling on concurrent instances. max_agents=1 implies sequential/ordering constraint. max_agents>1 enables fan-out.
- DIVERGED: A flags an unresolved ambiguity: max_agents=6 + dispatch_mode="full" -- does each agent get the same input redundantly, or does the caller partition? B focuses on the emergent grouping with background_mode.
- ALTERNATIVES:
  - A: Simple integer -- clean, matches data
  - B: Rendered as combined "Dispatch Strategy" block with background_mode -- the two fields jointly determine caller behavior
- HYPOTHESIS: `background_mode` + `max_agents` form a natural rendering group. Their combination produces the dispatch strategy matrix (see Conditional Branches). Rendering them separately loses the interaction.
- STABILITY: structural
- CONDITIONAL: Rendered prose varies by value. max_agents=1 vs. max_agents>1 produces qualitatively different instructions.

### `input_delivery`

- CONVERGED: Mechanism for physically handing data to the agent. Both examples show "tempfile." Implied alternatives: inline, directory.
- DIVERGED: A considers cleanup responsibility (who deletes tempfiles?). B notes the structural coupling to the tempfile parameter.
- ALTERNATIVES:
  - A: Simple enum {tempfile, inline, directory}
  - B: Rendered as part of unified "Input" block with format and description -- the three fields together answer "what, how, where"
- HYPOTHESIS: input_delivery is a structural field that determines whether a `tempfile` parameter exists in the invocation signature. It renders as preparation instructions, not as a standalone label.
- STABILITY: structural
- CONDITIONAL: Delivery method changes preparation instructions and parameter presence.

### `input_format`

- CONVERGED: Contract field. The caller MUST produce this exact format. High stability.
- DIVERGED: A considers adding schema references for structured formats (jsonl, json). B emphasizes that format alone is insufficient -- the caller needs the record schema too.
- ALTERNATIVES:
  - A: Simple enum {text, jsonl, json, toml} -- matches data
  - B: Rendered jointly with input_description -- format is the container, description is the content spec
- HYPOTHESIS: For structured formats, input_format without field-level schema is an incomplete contract. The input_description currently carries this load in prose. Whether to formalize with schema references depends on how reliably LLM callers parse prose field specs.
- STABILITY: structural
- CONDITIONAL: Structured formats (jsonl, json) may warrant additional rendering (field specs, schema hints) that unstructured (text) does not.

### `input_description`

- CONVERGED: Semantic specification of what the input contains. Most critical field for correct dispatch -- format right + content wrong = useless invocation.
- DIVERGED: A considers example-augmented descriptions (show, don't tell). B considers checklist form for verifiability. B also notes exclusion instructions ("no learned, threads, or insight fields") as a distinct requirement type.
- ALTERNATIVES:
  - A: Structured requirements list -- "must include: X, Y, Z / must exclude: A, B"
  - B: Prose paragraph -- flexible, natural, but harder for LLM callers to verify compliance
  - C: Prose + field-level spec for structured formats -- best of both when format is jsonl/json
- HYPOTHESIS: For structured formats, the description should decompose into include/exclude field lists. For unstructured text, prose is sufficient. The format value should gate the rendering strategy.
- STABILITY: formatting
- CONDITIONAL: Rendering approach gated by input_format. Structured formats get field-level treatment; unstructured formats get prose.

### `parameters` (compound array)

- CONVERGED: Invocation signature. Four sub-fields: name, type, required, description. This is the API contract. Both analyses identify the tempfile parameter as structurally derived from input_delivery, and uid as agent-specific semantic metadata.
- DIVERGED: A considers adding defaults, patterns, must_exist validation. B emphasizes the need for a concrete invocation example/template alongside parameter docs. B identifies two parameter categories: structural (tempfile, derived from delivery) vs. semantic (uid, agent-specific).
- ALTERNATIVES:
  - A: Parameter table + invocation template -- document each parameter AND show a concrete Task tool call
  - B: Parameter documentation only -- table format, no example
  - C: Invocation-first with inline parameter docs -- lead with the call template, annotate parameters within it
- HYPOTHESIS: An LLM caller constructing a Task tool call needs a concrete, copy-pasteable template more than it needs a parameter reference table. The invocation template IS the primary rendering; parameter documentation supports it. Fragment A (both) is safest.
- STABILITY: structural
- CONDITIONAL: Parameter count and types vary per agent. The tempfile parameter is conditionally present (gated by input_delivery=tempfile).

### `output_format`

- CONVERGED: Output contract. Mirrors input_format in structure and stability. Tells the caller how to parse results.
- DIVERGED: Both note that format alone is insufficient for structured output -- caller also needs output schema. Neither finds schema data in the raw definitions.
- ALTERNATIVES:
  - A: Simple enum, rendered as part of unified "Result Handling" block
  - B: With consumption guidance -- "parse each line as JSON object"
- HYPOTHESIS: output_format renders into the result handling group, not standalone. For structured formats, the rendering should include basic parsing guidance.
- STABILITY: structural
- CONDITIONAL: Structured vs. unstructured formats warrant different result-handling prose.

### `output_name_known`

- CONVERGED: Ternary {known, partially, unknown}. Affects caller's post-dispatch workflow -- can they pre-plan file handling or must they discover output location?
- DIVERGED: A considers adding a name pattern template for the "partially" case. B focuses on rendering as post-dispatch discovery instructions.
- ALTERNATIVES:
  - A: Ternary enum + optional name pattern -- "partially" becomes actionable when the caller knows the template (e.g., `{uid}_summaries.jsonl`)
  - B: Rendered as discovery instructions in result handling -- operational guidance over data labels
- HYPOTHESIS: "partially" is vague without a pattern template. The field value tells the caller how much to trust pre-dispatch assumptions; the pattern (if present) tells them what to expect. Both layers are needed for "partially."
- STABILITY: formatting
- CONDITIONAL: Each of the three values produces different post-dispatch instructions.

### `return_mode`

- CONVERGED: Both examples show "status" (success/failure indicator, content in files). Implied alternatives: content, reference. High stability.
- DIVERGED: Minimal. A considers documenting expected status values. B emphasizes success/failure handling paths.
- ALTERNATIVES:
  - A: Combined "Results" block -- return mode + output format + output location as unified handling instructions
  - B: Separate return specification with success/failure branching
- HYPOTHESIS: return_mode renders into the result handling group. The success/failure branching is the caller's most important post-dispatch decision point and deserves explicit prose.
- STABILITY: structural
- CONDITIONAL: Different return modes would produce fundamentally different result-handling instructions. Currently only "status" is observed.

## Cross-Section Dependencies

**Mirrored fields (dispatcher echoes data owned elsewhere):**

| Dispatcher Field | Home Section | Drift Risk |
|---|---|---|
| agent_description | identity.description | HIGH -- different audiences invite different phrasings that diverge over time |
| input_format | input section | MEDIUM -- mechanical, less likely to drift |
| output_format | output/enforcement section | MEDIUM |
| output_name_known | output section | LOW |
| return_mode | return section | LOW |
| parameters | input section | HIGH -- parameter descriptions may diverge |

**Unresolved ownership question:** Both analyses surface the tension between self-contained interface spec (dispatcher owns its values) vs. single-source-of-truth (dispatcher references home sections). B proposes a reference-and-override model: inherit from home section unless explicitly overridden. This is the strongest candidate but adds resolver complexity.

**Derived field relationship:** The `tempfile` parameter is a structural consequence of `input_delivery = "tempfile"`. If delivery method changes, the parameter set changes. This is a derivation, not just a mirror.

## Conditional Branches

### Dispatch Strategy Matrix (background_mode x max_agents)

This is the dominant conditional. It determines the overall shape of the rendered SKILL.md.

| background_mode | max_agents | Strategy | Rendering Shape |
|---|---|---|---|
| forbidden | 1 | Sequential foreground | Linear: prepare, invoke once, wait, consume |
| allowed | >1 | Parallel background | Orchestration: batch, fan-out, manage lifecycle, collect |
| forbidden | >1 | Sequential batching | Loop: prepare batch, invoke one-at-a-time, consume each |
| allowed | 1 | Single background | Fire-and-forget: prepare, invoke, continue, check later |

Only the first two are observed in data. The latter two are structurally implied.

### Input Format Conditional

- **Structured (jsonl, json, toml):** Rendering includes field-level specification, parsing guidance, possible schema reference.
- **Unstructured (text):** Rendering uses prose description only.

### Output Name Known Conditional

- **known:** Include exact filename/path template.
- **partially:** Include pattern template + discovery instruction.
- **unknown:** Include discovery-only instruction.

### Dispatch Mode Conditional

- **full:** Currently the only observed value. If non-full modes materialize, this becomes a major conditional affecting the entire caller workflow (multi-step dispatch, follow-up invocations, etc.).

## Open Design Questions

1. **Dispatch strategy as template selector vs. conditional composition?** B proposes modular composition (base + addons gated by field values), which aligns with the broader system's composability. A implicitly assumes a single template with field-driven prose variation. The strategy matrix suggests at least two qualitatively distinct documents -- can one template serve both?

2. **What does max_agents>1 + dispatch_mode="full" mean?** Each agent gets the same full input (redundant parallel), or the caller partitions (fan-out)? The raw data does not clarify. This ambiguity will manifest as incorrect dispatch behavior if unresolved.

3. **Output location:** Neither agent's dispatcher specifies WHERE output is written. Is this a parameter? A convention? A return status field? The caller needs this to consume results.

4. **Cleanup responsibility:** Who deletes tempfiles? Operational detail absent from data. Convention or explicit field?

5. **Error handling and retry:** No failure mode, retry policy, or timeout data in either agent. Gap or intentional delegation to caller?

6. **dispatch_mode viability:** If "full" is the only mode, the field is currently vestigial. Defer rendering until a second mode appears? Or keep as structural placeholder?

7. **Invocation syntax coupling:** Is the SKILL.md coupled to Claude Code Task tool syntax specifically, or should it be tool-agnostic? This determines whether the invocation template is a literal tool call or an abstract parameter specification.

## Key Design Decisions

1. **Natural rendering groups are confirmed by both analyses.** Five groups: Identity/Routing, Input Specification, Invocation Interface, Dispatch Strategy, Result Handling. These map to the caller's workflow phases and should be the structural skeleton of every SKILL.md.

2. **The dispatch strategy matrix is the primary structural conditional.** The combination of background_mode and max_agents -- not either field alone -- determines the rendered document's character. These two fields MUST render as a unified block.

3. **Input fields form a tight triad.** input_delivery + input_format + input_description answer a single compound question ("what do I prepare, in what format, how do I hand it over?") and should render as one block.

4. **Result fields form a tight triad.** output_format + output_name_known + return_mode answer "what comes back, where is it, how do I find it?" and should render as one block.

5. **The invocation template is the most important rendering artifact.** Both analyses converge: an LLM caller needs a concrete, copy-pasteable Task tool call more than any other single piece of information. Parameter documentation supports the template; the template does not support the documentation.

6. **Lean data model is correct for now.** Every "alternative worth considering" (schema refs, name patterns, defaults, validation hints) adds genuine value but is not evidenced in current data. The design should accommodate future extensions without requiring them today.
