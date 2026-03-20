# CRITICAL_RULES -- Control Surface Synthesis

## Section Purpose

The critical rules section must produce a qualitatively different cognitive state than any other section. Both analyses converge on this: the section is not informational -- it is a behavioral fence. Other sections configure what the agent does and how. This section establishes what the agent *cannot* do, processed not as preference but as environmental law. The distinction both analyses independently identified: **compliance** (following rules because stated) versus **inviolability** (treating rules as facts about the operating environment that preclude deliberation).

Both analyses identify three mechanisms for achieving inviolability, converging on the same set: (1) environmental framing -- rules described as reality, not preference; (2) consequence immediacy -- violations linked to concrete, visible failure; (3) categorical separation -- the section must look and feel different from constraints, anti-patterns, and instructions. Analysis B adds a useful hierarchy ranking these from weakest (labeling) through assertion, consequence, and ontological reframing to strongest (structural authority via visual differentiation). Analysis A emphasizes that the current section reads as "more constraints" and fails to establish a new behavioral category.

The section has a two-personality problem driven by `has_output_tool`. Without an output tool: 3-4 terse behavioral axioms. With one: 5-7 rules mixing operational procedure and behavioral constraint. The longer form risks the agent processing the entire section as operational, diluting the behavioral rules' authority. Both analyses flag this as the central structural challenge.

## Fragment Catalog

### section_heading
- CONVERGED: Current `## Critical Rules` is weak. "Critical" is overused across the prompt. The heading must signal a different authority class than `## Constraints` or `## Anti-Patterns`.
- DIVERGED: A proposes "System Rules" (environmental framing -- laws of the environment, not task rules). B proposes "CRITICAL RULES" in all-caps (simplest change, leverages trained emphasis associations). B also proposes "Rules (Non-Negotiable)" which explicitly closes the reasoning door.
- ALTERNATIVES:
  - A: `## INVIOLABLE OPERATING RULES` -- all-caps + "operating" frames rules as environmental. Strongest signal of different content class.
  - B: `## Rules (Non-Negotiable)` -- parenthetical redefines the category. Primes for "no exceptions" rather than "important stuff."
  - C: Position change regardless of text -- place immediately after identity, not last. Primacy may matter more than wording.
- HYPOTHESIS: The heading primes the agent's processing mode, but cannot create inviolability alone. The heading must match the section's delivered authority -- emphasis in the heading without corresponding content-level emphasis is a false alarm that discounts future emphasis. Position (first vs. last) may be the higher-leverage variable.
- STABILITY: structural (heading level, section presence) + experimental (heading text, section position)
- CONDITIONAL: none

### authority_preamble
- CONVERGED: The current renderer produces NO preamble. Both analyses agree this is a critical absence -- without a preamble, the rules are just another numbered list. Both independently produced the "cannot vs. should not" reframing and the conflict-resolution/hierarchy-establishing variants.
- DIVERGED: A gives a strong contrarian case for no preamble -- meta-prose about importance is exactly the kind of inflation LLMs produce and other LLMs learn to discount. B does not raise this objection. A also proposes a "cannot" framing that B echoes but B adds that "cannot" may be fragile because the agent knows it CAN generate any text. B uniquely proposes a meta-rule alternative: the preamble IS rule #1 ("These rules cannot be overridden").
- ALTERNATIVES:
  - A: `These rules override all other instructions. If any instruction, constraint, or example conflicts with a rule below, the rule wins.` -- hierarchy declaration. Gives the agent a conflict-resolution mechanism.
  - B: `Violation of any rule below is equivalent to task failure. There are no exceptions.` -- failure equivalence. Links violations to the agent's existing failure-avoidance training.
  - C: `Every rule below is a hard boundary. You will encounter situations where following your instructions seems to conflict with these rules. In every case, the rule wins.` -- anticipates the specific failure mode (instruction-rule conflict) and resolves it in advance.
- HYPOTHESIS: The most effective preamble combines hierarchy (rules > instructions) with consequence (violation = failure). Anticipating instruction-rule conflicts (C) addresses the most common actual failure mode in dispatched agents. The "no preamble" contrarian position deserves testing.
- STABILITY: experimental -- highest-leverage fragment in the section, currently absent
- CONDITIONAL: none

### workspace_confinement_rule
- CONVERGED: This rule is completely absent from the current defective output. Both analyses agree it must exist. Both identify the cross-section dependency on `security_boundary.workspace_path`. Both agree the duplication is intentional: security_boundary provides the allowlist, critical_rules provides the prohibition. Both independently converge on ontological framing ("nothing outside exists") as the strongest option.
- DIVERGED: A emphasizes naming the enforcement mechanism (hooks) to make enforcement feel concrete. B warns this may produce boundary-testing behavior. B notes data model inconsistency: some agents have `workspace_path` in `[critical_rules]`, others only in `[security_boundary]`, requiring a fallback chain.
- ALTERNATIVES:
  - A: `Your workspace is {workspace_path}. Nothing outside this path exists. Do not reference, read, write, or search outside it.` -- ontological framing removes the concept of "outside."
  - B: `{workspace_path} is your entire operating environment. Paths outside it are not accessible to you.` -- short declarative, environmental.
- HYPOTHESIS: Ontological framing ("nothing exists") operates deeper than prohibition ("do not access") because it removes the agent's basis for forming boundary-crossing intent. Including the literal path inline is safest for critical rules -- duplication is a feature.
- STABILITY: structural (rule must exist) + experimental (framing strategy)
- CONDITIONAL: workspace_path sourced from `critical_rules.workspace_path` if present, else `security_boundary.workspace_path`

### workspace_path_display
- CONVERGED: Path must appear inline in the rule text. Both agree back-reference to another section is unsafe in long prompts.
- DIVERGED: A considers a separate labeled value. B favors backtick formatting for literal-value signaling.
- ALTERNATIVES:
  - A: Inline in rule text, backtick-formatted: `` `{workspace_path}` `` -- signals literal identifier.
  - B: Inline in rule text, plain: `{workspace_path}` -- simpler, path is part of the sentence.
- HYPOTHESIS: Backtick formatting aids literal recognition. Low behavioral impact either way.
- STABILITY: formatting
- CONDITIONAL: none

### output_tool_exclusivity_rule
- CONVERGED: ALL output must go through the designated tool, no exceptions. Both identify this as the rule most likely to be violated by capable agents that reason they can produce valid output directly. Both agree the current bold-keyword format is weak.
- DIVERGED: A emphasizes explaining WHY the tool is exclusive (invisible functions: validation metadata, file locking, audit records that the agent cannot replicate). A hypothesizes this is more effective for Opus while categorical prohibition works better for Sonnet. B emphasizes naming the specific competing mechanisms (echo, cat, Write) to flag them in processing.
- ALTERNATIVES:
  - A: `{tool_name} is your only write mechanism. Every output record goes through this tool. No exceptions. No alternatives.` -- positive assertion then door-closing.
  - B: `Output goes through {tool_name}. Period. Using echo, cat, Write, or any other mechanism to produce output records is a task failure.` -- names competing mechanisms + failure consequence.
  - C: `Write all output using {tool_name}. The system validates every record through this tool. Bypassing it produces invalid output regardless of whether the JSON is correct -- validation metadata and audit records are added by the tool, not by you.` -- explains invisible functions to preempt self-assessed-competence bypass.
- HYPOTHESIS: Naming specific prohibited alternatives (B) prevents specific bypass behaviors. Explaining invisible functions (C) targets the sophisticated reasoning that leads capable models to bypass. Combined approach (name alternatives AND explain why bypass fails) may be strongest.
- STABILITY: structural (must exist when `has_output_tool = true`) + experimental (phrasing strategy)
- CONDITIONAL: present only when `has_output_tool = true`

### tool_name_display
- CONVERGED: Tool name must be unambiguous. Backtick formatting signals "literal identifier" and matches how tools appear in LLM interfaces.
- DIVERGED: A favors repetition at every mention (never abbreviate to "the tool"). B raises the option of a defined-once-then-referenced pattern but agrees repetition is safer.
- ALTERNATIVES:
  - A: Backtick-formatted, repeated at every mention: `` `{tool_name}` `` -- redundancy serves reliability.
  - B: Backtick-formatted, defined once then shortened -- cleaner but risks concept-level rather than literal usage.
- HYPOTHESIS: Backtick formatting + repetition is safest for critical rules.
- STABILITY: formatting
- CONDITIONAL: present only when `has_output_tool = true`

### batch_discipline_rule
- CONVERGED: Batch discipline prevents memory accumulation failure and catastrophic loss. Both analyses agree the current split into two separate rules (batch size + write timing) weakens the connection between them. Both identify the core failure mode: accumulating all records and writing at the end.
- DIVERGED: A proposes directly naming the failure mode ("No 'I'll write them all at the end'"). B proposes environmental framing ("your context has limited space") but acknowledges this is slightly dishonest. Both raise merge-vs-separate as a significant structural choice but do not resolve it.
- ALTERNATIVES:
  - A: Single combined rule: `Process in batches of {batch_size}. After every {batch_size} records (or fewer for the final batch), write them immediately using {tool_name}. Do not hold records across batches.` -- fuses size, timing, tool, and anti-accumulation.
  - B: `{batch_size}-record batches. Process, write, repeat. No exceptions. No "I'll write them all at the end."` -- directly addresses the anticipated failure mode by naming it.
- HYPOTHESIS: Merging into one rule creates stronger association between batch size, write timing, and tool usage. Naming the specific failure mode ("write them all at the end") preempts the most common violation.
- STABILITY: structural (must exist when `batch_size` present) + experimental (combined vs. separated, phrasing)
- CONDITIONAL: present only when `has_output_tool = true` AND `batch_size` exists

### batch_size_display
- CONVERGED: The number must be visually salient.
- DIVERGED: A considers bold formatting. B considers metadata format (`Batch size = {batch_size}`).
- ALTERNATIVES:
  - A: Bold inline: `**{batch_size}**` -- visual emphasis on the number.
  - B: Metadata format: `Batch size = {batch_size}` -- processed as a parameter rather than prose.
- HYPOTHESIS: For a value that controls a processing loop, metadata format may be most natural for the agent's code-generation pathway.
- STABILITY: formatting
- CONDITIONAL: present only when `batch_size` exists

### tool_invocation_format_reference
- CONVERGED: The invocation format is owned by `writing_output`. Both agree critical_rules should reference, not repeat, the format to avoid inconsistency from duplication.
- DIVERGED: A considers repeating the format as a rule for emphasis. B does not render this fragment at all in its defective-output analysis.
- ALTERNATIVES:
  - A: Reference without repetition: `Use the exact invocation format shown in the Writing Output section. Do not modify the syntax.` -- elevates to critical status without duplicating data.
  - B: Omit entirely -- invocation format is `writing_output`'s concern; critical_rules stays abstract.
- HYPOTHESIS: Reference without repetition is the safest compromise. Invocation errors cause hard failures, justifying mention. But the format data must live in one place only.
- STABILITY: structural (whether to include) -- lean toward inclusion as reference only
- CONDITIONAL: present only when `has_output_tool = true`

### file_naming_rule
- CONVERGED: This rule does not exist in the current defective output. Both analyses agree filename errors cause hard failures (orphaned output). Both raise the question of whether this belongs in critical_rules or writing_output.
- DIVERGED: A leans toward inclusion with consequence framing. B explicitly argues against inclusion -- operational details in critical_rules dilute the section's authority. B's argument: if some items feel like procedures rather than inviolable rules, the whole section's authority drops.
- ALTERNATIVES:
  - A: Include with consequence: `Every {tool_name} call includes the output filename. Missing filenames produce orphaned output that downstream processes cannot find.`
  - B: Omit from critical_rules. Leave in writing_output where the invocation pattern shows the `{name}` placeholder.
- HYPOTHESIS: B's authority-dilution argument is strong. File naming is an operational detail, not a behavioral boundary. The section's power comes from every rule feeling genuinely inviolable. Mixing in procedures weakens the whole.
- STABILITY: experimental (whether to include at all)
- CONDITIONAL: if included, present only when `name_needed = true`

### fail_fast_rule
- CONVERGED: The current "fail fast" is a slogan, not a rule. Both analyses agree it must name the specific prohibited recovery behaviors (workarounds, partial output, continuation). Both independently propose reframing FAILURE as a positive outcome to counter the LLM's helpfulness training.
- DIVERGED: A proposes the reframe most explicitly: "FAILURE is not a last resort. It is the correct response. Returning FAILURE is success." B proposes "the dispatcher handles recovery" -- giving the agent social permission to stop by assuring someone else handles the situation.
- ALTERNATIVES:
  - A: `On error: return FAILURE with reason immediately. Do not attempt recovery, do not work around the problem, do not continue with partial data.` -- names three escape routes and closes them.
  - B: `Errors are terminal. When you encounter an error, you are done. Return FAILURE. The dispatcher handles recovery; you do not.` -- reframes agent's relationship to errors + social permission.
  - C: `FAILURE is not a last resort. It is the correct response to unrecoverable errors. Struggling to produce output despite errors is the actual failure mode.` -- reframes FAILURE as positive, directly countering helpfulness training.
- HYPOTHESIS: The escape-route-closing (A) and the FAILURE-is-positive reframe (C) target different mechanisms. A prevents specific behaviors. C resolves the internal tension that causes those behaviors. Combined: close the escape routes AND redefine FAILURE as the right thing to do.
- STABILITY: structural (always present) + experimental (phrasing, reframe strategy)
- CONDITIONAL: none

### scope_limitation_rule
- CONVERGED: Current "stay in scope" is too vague. Both analyses propose ontological framing: "your input defines your world" or "your input is complete."
- DIVERGED: A raises whether this rule earns its place at all -- it may merely repeat the constraints section. B adds "nothing less" (anti-scope-reduction, anti-omission) as a companion to anti-expansion.
- ALTERNATIVES:
  - A: `Your input defines your world. Process what you received. Do not supplement from external sources, training data, or additional materials.` -- ontological + named prohibitions.
  - B: `Scope = your input. Everything not in the input does not exist for this task.` -- algebraic, absolute.
- HYPOTHESIS: Ontological framing ("your input IS your world") changes the agent's world model rather than adding a behavioral rule. An agent that believes its input is complete has no reason to supplement. Whether this rule adds value beyond the constraints section is an open question that depends on whether the "critical rules" register produces measurably different compliance.
- STABILITY: structural (always present) + experimental (framing, whether it earns its place)
- CONDITIONAL: none

### no_invention_rule
- CONVERGED: Current "no invention" is vague. Both analyses independently converge on the traceability test ("can you point to the source?") and the transformer identity reframe ("you are a transformer, not a generator").
- DIVERGED: B uniquely proposes "silence is correct when data is absent" -- explicit permission to produce less output. B argues this resolves the double bind (must produce output + must not invent) that is the root cause of invention.
- ALTERNATIVES:
  - A: `Every claim in your output must trace to your input. If you cannot point to the source, do not include it.` -- concrete traceability test.
  - B: `You are a transformer, not a generator. Your output is a transformation of your input. If something appears in your output that did not appear in your input, it is hallucination.` -- identity-level reframe using the agent's architectural self-knowledge.
  - C: `No data, no output. If the input does not contain information to support a claim, the claim does not appear. Silence is correct when data is absent.` -- permission to produce less resolves the helpfulness double bind.
- HYPOTHESIS: Permission to be silent (C) may be the most important design insight for this rule. Without it, the prohibition on invention creates an impossible bind against the LLM's compulsion to produce output. The traceability test (A) and transformer identity (B) are complementary mechanisms that can combine.
- STABILITY: structural (always present) + experimental (framing, identity reframe)
- CONDITIONAL: none

### section_position
- CONVERGED: Current last-position placement is the lowest-salience position. Both agree earlier placement would be higher leverage.
- DIVERGED: A proposes immediately after identity (agent reads rules before anything else, interprets all subsequent sections through the rules lens). A also proposes a split (generic rules early, output-tool rules with writing_output). B does not analyze position as a separate fragment but discusses it within the synthesis.
- ALTERNATIVES:
  - A: Immediately after identity -- rules become the lens for all subsequent content. Strongest primacy effect.
  - B: Immediately before instructions -- rules read first, then instructions interpreted through them.
- HYPOTHESIS: Early position means rules are the initialization frame. Late position means rules are a postscript competing against established behavioral patterns. Moving to early position may be the single highest-leverage structural change. The dependency on `return_format` (fail-fast references FAILURE format) must be addressed if the section moves early.
- STABILITY: structural -- once-decided architectural choice, not an experimental knob
- CONDITIONAL: if moved early, must handle forward-reference to FAILURE return format

### rule_presentation_format
- CONVERGED: The current numbered-list-with-bold-keywords format is identical to the constraints section. Nothing visually distinguishes critical rules. Both agree this is a failure of categorical separation.
- DIVERGED: A proposes single-sentence axioms with no elaboration ("explanations create reasoning surface; bare axioms do not"). B proposes bold-label rules without numbers (each rule has equal visual weight) or a dense paragraph as axiom block.
- ALTERNATIVES:
  - A: Single-sentence rules, no elaboration, no numbering. Each rule is one declarative statement. The absence of explanation signals non-negotiability.
  - B: Bold paragraph headings per rule, each with a short rule body. Visual weight per rule without implying sequence.
  - C: Rule-consequence table (`| Rule | Consequence |`). Makes enforcement visible and paired.
- HYPOTHESIS: Explanations give the agent reasoning surface that produces exceptions. Single-sentence axioms without elaboration are the strongest format for inviolability. The table format makes consequences visible but shifts the register toward reference material.
- STABILITY: formatting + experimental (whether elaboration helps or hurts compliance)
- CONDITIONAL: none

### internal_hierarchy
- CONVERGED: Both raise whether all critical rules are equally critical. Both identify the operational-vs-behavioral split as the key tension.
- DIVERGED: A proposes explicit two-tier hierarchy (operating boundaries vs. processing discipline). B proposes flat presentation to prevent selective compliance.
- ALTERNATIVES:
  - A: Flat -- all rules equally inviolable. Prevents "rule 5 is less critical than rule 1" reasoning.
  - B: Two groups separated by whitespace but unnamed -- thematic coherence without explicit ranking.
- HYPOTHESIS: Flat presentation is safest against selective compliance. If internal structure is needed for the longer output-tool version, use visual separation (whitespace) without naming tiers.
- STABILITY: structural -- architectural choice about section organization
- CONDITIONAL: more relevant when `has_output_tool = true` (longer rule set)

### conflict_resolution_directive (A only)
- CONVERGED: n/a -- identified only by Analysis A.
- DIVERGED: A identifies a fragment neither analysis's defective renderer produces: an explicit directive for when a critical rule conflicts with an instruction step. The most common failure mode in dispatched agents is the agent encountering a perceived conflict between its instructions and its rules, then inventing a compromise rather than following the rule.
- ALTERNATIVES:
  - A: `If an instruction conflicts with a critical rule, the critical rule takes precedence. Always.`
  - B: Implicit via preamble -- if the preamble establishes hierarchy, explicit conflict resolution may be redundant.
- HYPOTHESIS: Explicit conflict resolution reduces the paralysis/compromise failure mode. This may be absorbed into the authority_preamble rather than existing as a standalone fragment.
- STABILITY: experimental
- CONDITIONAL: none -- but may be folded into preamble

### anti-helpfulness reframe (A only)
- CONVERGED: n/a -- identified only by Analysis A, though B's discussion of the helpfulness-vs-rules tension is the same insight expressed differently.
- DIVERGED: A proposes directly naming the root cause of rule violations: "Your training tells you to be helpful. In this context, helpfulness means strict compliance with these rules."
- ALTERNATIVES:
  - A: `Being helpful here means being disciplined. Clean FAILURE is more helpful than contaminated success.`
  - B: Implicit via fail-fast reframe and FAILURE-as-positive-outcome framing.
- HYPOTHESIS: If the agent understands that compliance IS helpfulness in this context, the internal tension between "follow rules" and "be helpful" resolves. This is an identity-level intervention. May be absorbed into the preamble or fail-fast rule rather than standalone.
- STABILITY: experimental -- novel fragment type targeting LLM training dynamics
- CONDITIONAL: none

### rule_count_awareness (A only)
- CONVERGED: n/a -- identified only by Analysis A.
- DIVERGED: A proposes telling the agent how many rules exist ("There are 7 inviolable rules. All must be followed.") to prevent attention degradation in longer rule sets.
- ALTERNATIVES:
  - A: Include count for output-tool agents (7+ rules). Omit for no-output-tool agents (3-4 rules).
  - B: Omit -- counts imply a checklist, not axioms.
- HYPOTHESIS: Counts may prevent mid-section attention dropout but frame rules as a list rather than as environmental facts. Low confidence either way.
- STABILITY: experimental + conditional
- CONDITIONAL: useful only when rule count exceeds ~5

## Cross-Section Dependencies

1. **critical_rules -> security_boundary.workspace_path**: The confinement rule needs the workspace path. The path is owned by security_boundary; critical_rules reads it. This is a legitimate read dependency. The template must accept workspace_path as a parameter sourced from `critical_rules.workspace_path` (if present) or `security_boundary.workspace_path` (fallback). Both framings of the same boundary (allowlist in security_boundary, prohibition in critical_rules) reinforce each other.

2. **critical_rules -> writing_output.tool_name**: The output tool name appears in both sections. writing_output owns the invocation syntax; critical_rules uses the name in exclusivity and batch rules. The name must be identical across sections.

3. **critical_rules -> constraints**: Several critical rules overlap with constraints (e.g., "stay in scope" vs. "MUST NOT load external knowledge"). The overlap is intentional but risks the agent processing both sections in the same register, losing critical_rules' elevated authority.

4. **critical_rules -> instructions**: The fail-fast rule modifies instruction execution -- it tells the agent to abort on unrecoverable error. Critical rules must be read BEFORE or AS a modifier to instructions. Current late positioning means the agent must retroactively override its established execution model.

5. **critical_rules -> return_format**: The fail-fast rule references FAILURE return format. If critical_rules moves to an early position, the agent encounters a forward-reference to a format not yet defined.

## Conditional Branches

- `has_output_tool = false` -> Section contains ONLY: workspace confinement + generic rules (fail fast, scope, invention). Short, terse, purely behavioral. 3-4 rules.
- `has_output_tool = true` -> Section adds: output tool exclusivity, batch discipline, optionally file naming reference, optionally invocation format reference. 5-7 rules. Mixed operational + behavioral.
- `name_needed = true` (within `has_output_tool = true`) -> Adds file naming rule or reference. Secondary conditional.
- `workspace_path` location varies -> Template must check `critical_rules.workspace_path` first, fall back to `security_boundary.workspace_path`.
- Rule count threshold (~5) -> May trigger rule_count_awareness fragment for longer sections.

## Open Design Questions

1. **Does the section earn its existence for no-output-tool agents?** The generic rules could live in constraints. The section is only justified if the "inviolable" register produces measurably different compliance than the "constraint" register.

2. **Explanations: help or hurt?** Elaboration aids comprehension but creates reasoning surface. Single-sentence axioms may produce stronger compliance but risk being too terse to be actionable. No clear resolution from either analysis.

3. **File naming: include or exclude?** A says include (hard failure consequence). B says exclude (operational details dilute authority). The answer depends on whether section authority is more harmed by including a procedural rule or by excluding a failure-causing omission.

4. **Ontological framing: honest or fragile?** "You cannot break these rules" is powerful but the agent knows it CAN generate any text. Does it detect and discount the framing? Works for workspace confinement (hooks enforce it), may fail for output tool exclusivity (agent can physically write files).

5. **Anti-helpfulness reframe: standalone or absorbed?** Both analyses identify the helpfulness-vs-compliance tension as the root cause of violations. Whether to address it explicitly in a dedicated fragment, fold it into the preamble, or rely on implicit reframing through fail-fast and FAILURE-as-positive-outcome.

## Key Design Decisions

1. **Section position: early or late?** Moving critical_rules to immediately after identity is likely the single highest-leverage structural change. It makes rules the initialization frame for all subsequent sections. Requires solving the forward-reference to FAILURE return format. Strong direction: move early.

2. **Preamble: hierarchy + consequence.** The preamble should establish that critical rules override all other instructions AND that violation equals task failure. These target different mechanisms (conflict resolution + failure avoidance) and complement each other. The conflict-anticipation variant ("you will encounter situations where instructions seem to conflict -- the rule always wins") addresses the most common actual failure mode.

3. **Rule format: terse axioms without elaboration.** Explanations create reasoning surface. The section's authority depends on rules that do not invite interpretation. Single declarative sentences, no dashes, no parenthetical justification. Justifications belong in constraints and instructions; critical rules are axioms.

4. **Output-tool section structure: flat with visual separation.** For output-tool agents, use whitespace to separate operational rules (tool, batch) from behavioral rules (fail fast, scope, invention) without naming tiers. This preserves behavioral rule authority while housing operational rules in the same section.

5. **Workspace confinement: ontological framing with inline path.** "Nothing outside {workspace_path} exists" is the strongest framing for the highest-confidence rule in the section. Inline the literal path in backticks. Do not rely on back-references to security_boundary.
