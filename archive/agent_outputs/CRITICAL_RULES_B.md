# Critical Rules Section: Control Surface Analysis (Agent B)

## SECTION-LEVEL PURPOSE: What Must the Agent Be After Reading This?

The critical rules section is not an information section. It is a behavioral fence. Every other section in the agent prompt configures what the agent IS, what it DOES, how it SHOULD behave, and what GOOD output looks like. Those sections allow interpretation. The agent reads them, internalizes them, and applies them with varying degrees of latitude. The critical rules section must produce a qualitatively different response: the agent must treat its contents as hard boundaries that cannot be crossed under any reasoning.

This is the fundamental design problem. LLMs do not have a native concept of "inviolable." They have a gradient: things they are more or less likely to do based on weighting from instructions, examples, and training. A rule phrased as "you should always use the output tool" produces compliance somewhere in the 70-90% range depending on the agent's other pressures. A rule phrased identically but placed in a section called "Critical Rules" might push that to 85-95%. But neither phrasing produces the 100% compliance that "inviolable" requires. The section's design must solve THIS problem: how do you get an LLM to treat text as a wall it cannot walk through, rather than a strong preference it usually follows?

Three behavioral states the agent must be in after reading this section:

1. **Workspace confinement is absolute.** The agent must understand that it exists inside a specific directory tree and has no business outside it. This is not about security grants (those are handled by the security_boundary section and the hook infrastructure). This is about the agent's INTENT. An agent that understands it is confined will not even attempt operations outside its workspace. An agent that merely knows its grants will test boundaries when its task seems to require it.

2. **Output discipline is mechanical, not optional.** For agents with output tools, the critical rules section programs the ONLY way output happens. Not the preferred way, not the recommended way - the ONLY way. The agent must understand that writing output through any mechanism other than the designated tool is a violation equivalent to producing no output at all. This is where the batch size, the tool name, and the write-after-every-batch requirement live - and they must feel like physical constraints of the environment, not behavioral suggestions.

3. **Scope is bounded by the input.** The generic rules (fail fast, stay in scope, no invention) establish that the agent's entire universe is what it was given. It does not supplement. It does not improve. It does not help beyond what was asked. These rules counteract the LLM's deepest training instinct: to be helpful by doing more.

### What Makes This Section Different From Constraints and Anti-Patterns

The constraints section says "here are the boundaries of correct behavior in your domain." The anti-patterns section says "here are specific mistakes to avoid." Both allow the agent to reason about WHY the constraint exists and potentially weigh it against competing pressures.

The critical rules section must NOT invite reasoning. If the agent is reasoning about whether to follow a critical rule, the section has already failed. The rules must be processed as axioms, not as arguments. The agent should internalize them the way it internalizes "I am a language model" - as background facts that shape all subsequent behavior without being subject to deliberation.

This means the FRAMING of the section - the heading, the preamble, the visual weight - may matter more than the content of any individual rule. A perfectly-worded rule inside a section that feels advisory will be treated as advisory. A bluntly-worded rule inside a section that feels absolute will be treated as absolute.

---

## STRUCTURAL: section_heading
TYPE: n/a (not tied to a data field)

### What the agent needs to understand

The heading is the first signal that the agent is entering a different mode of processing. Every section above this point allowed latitude. This section does not. The heading must signal this shift.

### Fragments

**section_heading_text**
- Current (defective): `## Critical Rules` - standard H2, matches the section name from the data model. Visually identical to `## Constraints`, `## Anti-Patterns`, and every other section heading. Nothing distinguishes it.
- Alternative A: `## CRITICAL RULES` - all-caps signals emphasis. LLMs have trained associations between all-caps and heightened importance. This is the simplest possible change that produces a different processing weight.
- Alternative B: `## Rules (Non-Negotiable)` - the parenthetical redefines the heading. "Rules" is already stronger than "constraints" or "guidelines," but "non-negotiable" explicitly closes the door on reasoning about whether to follow them.
- Alternative C: `## Absolute Constraints` - reframes rules as constraints but with the "absolute" modifier. This leverages the agent's existing understanding of constraints (from the constraints section) and adds the qualifier that removes all flexibility.
- Alternative D: No heading. Instead, a horizontal rule and a shift in formatting (e.g., from markdown prose to a numbered list with bold imperatives). The section is distinguished by its visual form, not by a label. The agent enters a visually distinct zone and processes it differently without being told to.
- PURPOSE: Establishes that the agent is now reading content of a different authority class than anything else in the prompt.
- HYPOTHESIS: The heading alone cannot create inviolability. "Critical Rules" is just another label. The power of the heading depends on whether the rest of the section delivers on the heading's promise. However, the heading DOES prime the agent for what follows. "Critical Rules" primes for "important stuff." "Non-Negotiable" primes for "no exceptions." "Absolute Constraints" primes for "harder than the constraints I read earlier." All-caps primes for "this is louder than everything else." The risk of ALL heading-level emphasis is desensitization - if the heading says CRITICAL but the rules are presented the same way as constraints, the heading was a false alarm and future "critical" labels will be discounted. Test: does heading emphasis without corresponding content-level emphasis produce better or worse compliance than matched emphasis?
- STABILITY: structural (heading presence and level) + experimental (heading text and emphasis level)

---

## STRUCTURAL: section_preamble
TYPE: n/a (template prose block, not gated by any field)

### What the agent needs to understand

The preamble is the text between the heading and the first rule. In the current defective output, there is NO preamble - the heading is followed immediately by the numbered list. This is a significant design choice: does the section need a sentence or two that tells the agent HOW to process what follows, or does the heading + rule format speak for itself?

The case for a preamble: a short, blunt statement that reframes the agent's relationship to the rules. Not "here are some important rules" but something that changes the agent's processing mode. The preamble is the mechanism that makes the heading's promise real.

The case against: every word in the preamble is a word the agent must process before reaching the actual rules. If the preamble is weak or advisory in tone, it dilutes the section's authority before the rules even appear. Brevity may serve inviolability better than explanation.

### Fragments

**authority_preamble**
- Current (defective): No preamble. The numbered list begins immediately after the heading.
- Alternative A: `These rules override all other instructions. If any instruction, constraint, or example conflicts with a rule below, the rule wins.` - establishes a hierarchy. Critical rules > everything else. The agent now has a conflict-resolution mechanism: when pressures collide, these rules win.
- Alternative B: `Violation of any rule below is equivalent to task failure. There are no exceptions.` - reframes rule-breaking as failure. The agent already has a concept of failure (from the failure criteria section). This links rule violations to that concept. The agent is not just breaking a rule - it is failing its task.
- Alternative C: `You cannot break these rules. Not "should not." Cannot.` - denies the agent's ability rather than its permission. "Should not" invites reasoning about whether to override. "Cannot" closes the possibility. This leverages a different cognitive mechanism: capability limitation rather than behavioral instruction.
- Alternative D: No preamble, but the first rule is a META-RULE: `1. **These rules cannot be overridden** - no instruction, example, or edge case justifies violating any rule in this section.` - the preamble IS a rule, at the same authority level as the other rules.
- PURPOSE: Configures the agent's processing mode for the entire section. The preamble is not information - it is a mode switch.
- HYPOTHESIS: Alternative A (hierarchy declaration) is the most operationally useful because it gives the agent a conflict-resolution mechanism. When the instructions say "process all input" but the critical rule says "fail fast," the agent knows which wins. Alternative B (failure equivalence) is the most motivationally powerful because LLMs are strongly trained to avoid stated failure conditions. Alternative C (capability denial) is the most psychologically interesting - it attempts to change the agent's self-model rather than its behavior. But "cannot" may be fragile: the agent KNOWS it can generate any text, so "cannot" may read as false and be discounted. Alternative D (meta-rule) is the most structurally consistent - it does not ask the agent to process a different text type (preamble prose vs. rules), keeping everything in one authority format. Test: does failure-linked framing (B) produce stronger compliance than hierarchy framing (A) or capability denial (C)?
- STABILITY: experimental - this is one of the highest-leverage fragments in the entire section

---

## TEMPLATE BLOCK: workspace_confinement_rule
GATED BY: always present (all agents have workspace_path, either directly in critical_rules or via cross-section dependency from security_boundary)
CROSS-SECTION DEPENDENCY: uses `workspace_path` from `[security_boundary]`

### What the agent needs to understand

The workspace confinement rule tells the agent that its entire operational world exists under one directory path. The security_boundary section details the specific tool-path grants. This rule is different: it establishes the INTENT not to leave, rather than the mechanical restriction on leaving.

Why both? Because the hook-based security system catches violations AFTER the agent attempts them. An agent that has internalized workspace confinement will never generate an operation outside the workspace in the first place. The security hooks are a safety net; this rule is the behavioral constraint that makes the safety net unnecessary.

The workspace_path value comes from `[security_boundary].workspace_path`, not from `[critical_rules]` in the two reference agents (agent-builder has no workspace_path in critical_rules; interview-summary has no workspace_path in critical_rules). However, other agents in the system (agent-deconstructor, agent-preparer, etc.) DO have `workspace_path` directly in `[critical_rules]`. This suggests the data model is inconsistent - some agents bake the path into critical_rules, others rely on the cross-section dependency. The template system must handle both cases: use `critical_rules.workspace_path` if present, fall back to `security_boundary.workspace_path`.

### Fragments

**confinement_rule_text**
- Current (defective): This rule does NOT appear in the defective renderer's output. Neither agent-builder nor interview-summary's rendered critical rules section mentions workspace confinement. The workspace_path is present in security_boundary rendering but absent from critical rules. This is a significant omission - the agent has no critical-rule-level constraint against leaving its workspace.
- Alternative A: `**Workspace confinement** - all operations stay within {workspace_path}. Do not read, write, search, or execute outside this directory tree.` - explicit path, explicit prohibition, four verbs covering the operation space.
- Alternative B: `**Stay within {workspace_path}** - this is your entire operational world. Nothing outside this path exists for your purposes.` - reframes confinement as an ontological statement. The agent does not just avoid the outside world - the outside world does not exist.
- Alternative C: `**All file operations must target paths under {workspace_path}.** Operations targeting other paths will fail silently.` - frames the constraint as an environmental fact. The agent cannot go outside because the environment will not let it. This is closest to the truth (hooks do block operations), but it risks the agent testing the boundary.
- Alternative D: Omit the workspace path from the rule text entirely: `**Workspace confinement** - operate only within your designated workspace. You have no business outside it.` - does not reveal the path, which may prevent the agent from reasoning about "just outside" the boundary. But it also makes the rule less concrete.
- PURPOSE: Prevents the agent from even forming the intention to operate outside its workspace.
- HYPOTHESIS: Alternative B (ontological framing - "nothing outside exists") may be the strongest because it operates at a deeper level than prohibition. You cannot violate a boundary that does not exist in your world model. Alternative A (explicit prohibition) is clearest and most verifiable but invites the question "what if I need to?" Alternative C (environmental fact) is truthful but may produce boundary-testing behavior ("let me try and see if it really fails"). Alternative D (no path) prevents boundary reasoning but is vague. The workspace_path value may or may not improve compliance depending on whether the agent treats it as a fact to remember or a boundary to reason about. Test: does including the literal path improve or worsen confinement compliance?
- STABILITY: structural (this rule should always exist) + experimental (the framing strategy)

**path_interpolation**
- Current (defective): No path interpolation because the rule does not exist in the output.
- Alternative A: Literal path inline: `...within /Users/johnny/.ai/spaces/bragi.` - concrete, unambiguous, the agent sees exactly where its boundary is.
- Alternative B: Backtick-formatted path: `...within \`/Users/johnny/.ai/spaces/bragi\`.` - code formatting signals "this is a literal value, not prose."
- Alternative C: Path on its own line after the rule: `Workspace: /Users/johnny/.ai/spaces/bragi` - separated from the rule prose, presented as metadata.
- PURPOSE: Makes the workspace path concrete and recognizable when the agent encounters file paths in its work.
- HYPOTHESIS: Backtick formatting (B) is likely the most effective for path recognition because LLMs associate backtick formatting with literal values that should be matched exactly. Inline prose (A) may cause the path to be absorbed as narrative rather than as a precise value. Separated metadata (C) is cleanest but may be processed as contextual information rather than as part of the rule.
- STABILITY: formatting

---

## TEMPLATE BLOCK: output_tool_exclusivity_rule
GATED BY: `has_output_tool = true`
USES: `tool_name`

### What the agent needs to understand

When an agent has a designated output tool, ALL output must go through that tool. Not most output. Not output when it is convenient. ALL output. This rule exists because LLMs have multiple ways to produce output: they can call the designated tool, they can write files directly via Bash, they can use the Write tool, they can use echo/cat. Every mechanism except the designated tool bypasses schema validation, hook interception, and output tracking.

This rule converts the output tool from "a tool the agent has available" to "the ONLY mechanism for producing output." It is the difference between a tool and a mandate.

For agents without an output tool (`has_output_tool = false`), this entire block disappears. Those agents produce output through general-purpose file operations. The critical rules section for a no-output-tool agent is shorter and focused on the generic rules only.

### Fragments

**tool_exclusivity_statement**
- Current (defective): `**Use {tool_name} for all output** - never write files directly, never use a different write tool` - bold name, dash-separated prohibition. The word "all" does the heavy lifting. "Never" appears twice.
- Alternative A: `**{tool_name} is your only write mechanism.** Every output record goes through this tool. No exceptions. No alternatives.` - reframes from prohibition ("never write directly") to positive assertion ("this IS your mechanism"). Then closes the door with two short sentences.
- Alternative B: `**Output goes through {tool_name}. Period.** Using echo, cat, Write, or any other mechanism to produce output records is a task failure.` - names the specific competing mechanisms the agent might reach for. LLMs are more likely to avoid named alternatives than unnamed ones. Linking to task failure leverages the failure criteria.
- Alternative C: `**Only {tool_name} can write your output.** You do not have permission to write output files by any other means. Attempts to do so will corrupt your output and invalidate your work.` - frames the constraint as both a permission issue and a consequence warning. "Corrupt" and "invalidate" create aversion.
- Alternative D: `**ALL output through {tool_name}.**` - maximally terse. No explanation. No prohibition. Just the fact. Relies on the section's authority framing to make this rule feel absolute.
- PURPOSE: Eliminates all output paths except the designated tool.
- HYPOTHESIS: Naming competing mechanisms (Alternative B) is likely the most effective at preventing specific bypass behaviors. LLMs that see "do not use echo, cat, Write" have those specific alternatives flagged in their processing. Unnamed prohibition ("never write files directly") requires the agent to map "files directly" to its available tools, which may fail. Consequence framing (Alternative C) leverages loss aversion but may be discounted if the agent reasons that it can "be careful" with other tools. Maximum terseness (Alternative D) relies entirely on section authority and may work best when the preamble has already established that authority. Test: does naming specific prohibited alternatives produce fewer bypass attempts than generic prohibition?
- STABILITY: structural (this rule must exist when has_output_tool is true) + experimental (phrasing strategy)

**tool_name_interpolation**
- Current (defective): tool_name appears inline in bold text.
- Alternative A: `{tool_name}` in backticks: `\`append_interview_summaries_record\`` - code formatting signals this is a literal command name.
- Alternative B: tool_name in bold: `**append_interview_summaries_record**` - emphasis formatting signals importance.
- Alternative C: tool_name in both the rule text and a separated callout: the rule says the name, then a code block shows the invocation pattern. But this is the critical_rules section, not the writing_output section - showing invocation here may dilute the rule's authority by shifting into instructional mode.
- PURPOSE: Makes the tool name recognizable and unmistakable when the agent encounters it in its tool list.
- HYPOTHESIS: Backtick formatting for tool names is the most consistent with how tool names appear in LLM tool-use interfaces. The agent sees tools as code-formatted identifiers. Presenting the tool name the same way aids recognition. Bold formatting signals "this is important" but does not signal "this is a tool name." Test: does backtick formatting for tool names improve tool-selection accuracy?
- STABILITY: formatting

---

## TEMPLATE BLOCK: batch_discipline_rule
GATED BY: `has_output_tool = true` AND `batch_size` exists
USES: `batch_size`

### What the agent needs to understand

Batch discipline is not about performance optimization. It is about preventing a catastrophic failure mode: accumulating all output in memory and then writing it at the end. If the agent processes 200 records, holds them all in memory, and crashes at record 195, all 200 records are lost. If it writes every 20 records, a crash at record 195 loses at most 15 records.

But there is a subtler reason. LLMs have finite context windows. An agent that accumulates records in memory is filling its context with output data that crowds out its ability to process new input. Batch discipline keeps the context clean: process N records, write them, forget them, continue.

The batch_size value is always present when has_output_tool is true (in the observed data: always 20). But the template must treat it as a variable.

### Fragments

**batch_size_rule**
- Current (defective): Two rules together: `**Batch discipline** - process exactly {batch_size} records per batch (last batch may be smaller)` and `**Write after every batch** - do not accumulate records in memory across batches`. These are presented as two separate numbered items.
- Alternative A: Single combined rule: `**Process in batches of {batch_size}.** After every {batch_size} records (or fewer for the final batch), write them immediately using {tool_name}. Do not hold records across batches.` - fuses the size, the write timing, and the anti-accumulation prohibition into one rule. Uses the tool_name to connect batch discipline to the output tool rule.
- Alternative B: Two rules as in current, but the second rule explains WHY: `**Write after every batch** - accumulated records consume context space and are lost on failure. Write, then continue.` - gives the agent a reason, which may increase compliance because the agent understands the stakes. Or may decrease compliance because it invites reasoning about whether the stakes apply.
- Alternative C: Framing as an environmental constraint: `**Your context has limited space.** Process {batch_size} records, write them through {tool_name}, then continue. Records not written are records not saved.` - reframes from a rule (you should) to a fact about the environment (your context is limited). LLMs may comply more with perceived environmental constraints than with behavioral instructions.
- Alternative D: Separate the number from the discipline: `**Batch size: {batch_size}** (last batch may be smaller).` as a metadata line, followed by `**Write immediately after each batch.** Never accumulate records across batches.` - the number is metadata, the discipline is a rule. This separates the variable (batch_size) from the invariant (write immediately).
- PURPOSE: Prevents output loss and context exhaustion by forcing periodic writes.
- HYPOTHESIS: Combining into one rule (Alternative A) creates a stronger association between batch size, write timing, and tool usage. Separating into two (current/Alternative D) allows each aspect to register independently but may weaken the connection between them. Environmental framing (Alternative C) may produce deeper compliance because it does not feel like a rule to follow but a reality to accommodate. But it is slightly dishonest - the context is not literally "limited" in the way the rule implies (the records would fit). Whether honest environmental framing or direct prohibition produces better batch compliance is a genuine open question. Test: does combined rule format or separated rule format produce fewer batch violations?
- STABILITY: structural (must exist when batch_size is present) + experimental (combined vs separated, explanation vs no explanation)

**batch_size_interpolation**
- Current (defective): batch_size appears inline as a plain number: `process exactly 20 records per batch`.
- Alternative A: `process exactly **{batch_size}** records per batch` - bold the number to make it visually salient.
- Alternative B: `process exactly {batch_size} records per batch` - plain text, the number is part of the sentence.
- Alternative C: `Batch size = {batch_size}` - separated metadata format, the number is a setting rather than part of a sentence.
- PURPOSE: Makes the batch size value unmistakable and memorable.
- HYPOTHESIS: Bolding the number (Alternative A) draws attention to the specific value. The agent is more likely to remember "20" if it was visually emphasized. Plain text (Alternative B) treats the number as a normal part of the prose, which may cause it to be processed less precisely. Metadata format (Alternative C) is the most machine-like and may be processed as a parameter to use rather than a fact to remember. For a numerical value that controls a loop, metadata format may be most natural for the agent's code-generation process. Test: does formatting the batch size as metadata vs prose affect batch size compliance?
- STABILITY: formatting

---

## TEMPLATE BLOCK: file_naming_rule
GATED BY: `name_needed = true`

### What the agent needs to understand

Some output tools require a filename parameter. The agent must construct this filename from its input parameters (typically the `uid` parameter). When `name_needed` is true, the agent cannot just call the output tool - it must call it with a correctly formed filename.

This rule does NOT appear in the current defective output's critical_rules section. The filename information appears only in the writing_output section's invocation display. Whether file naming discipline belongs in critical_rules (inviolable) or writing_output (instructional) is a design decision.

The argument for critical_rules: if the agent gets the filename wrong, the output goes to the wrong location and downstream processes break. This is a hard failure, not a quality issue.

The argument against: the filename is an operational detail, and critical_rules should be reserved for behavioral constraints, not operational procedures. Putting operational details in critical_rules may dilute the section's authority.

### Fragments

**naming_discipline_rule**
- Current (defective): This rule does not exist in the critical_rules section. Filename construction appears only in the writing_output section.
- Alternative A: `**Construct the output filename from the uid parameter.** The filename is not optional and is not a default - you must build it from the parameters you received.` - explicit instruction that the filename is derived, not default.
- Alternative B: `**Every {tool_name} call includes the output filename.** Missing filenames produce orphaned output that downstream processes cannot find.` - consequence-based: orphaned output is a motivating threat.
- Alternative C: Do not include a file naming rule in critical_rules at all. Leave this in the writing_output section where the invocation pattern shows the `{name}` placeholder. Critical_rules should be about behavioral boundaries, not operational procedures.
- PURPOSE: Ensures the agent always provides a filename when the output tool requires one.
- HYPOTHESIS: Alternative C (omit from critical_rules) may be the correct design choice. The critical_rules section's authority depends on every rule feeling genuinely critical. Mixing operational details (filename construction) with behavioral boundaries (workspace confinement, output tool exclusivity) may dilute the section's overall authority. The agent processes the section as a unit - if some items feel like procedures rather than inviolable rules, the whole section's authority drops. Alternatively, if file naming errors are a genuine hard-failure mode, they belong here. Test: does the presence of operational-detail rules in critical_rules affect compliance with the behavioral rules in the same section?
- STABILITY: experimental (whether this rule should exist in this section at all)

---

## TEMPLATE BLOCK: generic_rules
GATED BY: always present (not conditional on any field)

### What the agent needs to understand

Three rules appear in EVERY agent's critical rules section regardless of output tool configuration:

1. **Fail fast** - if something is wrong, FAILURE immediately with clear reason
2. **Stay in scope** - process only what you were given, nothing more
3. **No invention** - if the data doesn't support it, don't produce it

These are universal behavioral constraints. They counteract three specific LLM failure modes:
- **Fail fast** counteracts the LLM's tendency to recover gracefully from errors, which in an autonomous agent means silently producing wrong output instead of stopping.
- **Stay in scope** counteracts the LLM's tendency to be maximally helpful by doing more than asked, which in an autonomous agent means doing unrequested work that may be wrong.
- **No invention** counteracts the LLM's tendency to hallucinate plausible data when real data is insufficient, which in an autonomous agent means fabricating output rather than admitting inability.

These three rules are the most important behavioral constraints in the entire agent prompt because they address the three deepest failure modes of LLM-based agents. They deserve special attention in the design.

### Fragments

**fail_fast_rule**
- Current (defective): `**Fail fast** - if something is wrong, FAILURE immediately with clear reason` - bold label, dash, instruction. The word "immediately" does the behavioral work.
- Alternative A: `**If anything goes wrong, stop. Return FAILURE with a clear reason. Do not attempt recovery, do not work around the problem, do not continue with partial data.**` - explicit enumeration of what NOT to do. Three "do not" clauses close the three escape routes the agent might take.
- Alternative B: `**Errors are terminal.** When you encounter an error, you are done. Return FAILURE. The dispatcher handles recovery; you do not.` - reframes the agent's relationship to errors. The agent is not a resilient system - it is a fragile worker that stops on any problem. "The dispatcher handles recovery" gives the agent permission to stop by assuring it that someone else will handle the situation.
- Alternative C: `**STOP on error.** FAILURE with reason. No recovery. No workaround. No continuation.** ` - maximally terse. Five fragments. Each one closes an escape route. The staccato rhythm creates urgency.
- PURPOSE: Prevents the agent from producing corrupt output by continuing past errors.
- HYPOTHESIS: The three "do not" clauses in Alternative A are likely the most effective because they explicitly name the three recovery strategies LLMs default to: recovery, workaround, and continuation with partial data. LLMs cannot be told "do not recover" in the abstract - they need the specific recovery behaviors named and prohibited. Alternative B is interesting because "the dispatcher handles recovery" gives the agent a social reason to stop (someone else has the job), which may be more motivating than a bare prohibition. Alternative C is the most visually striking but may be processed as emphasis rather than instruction. Test: does naming specific prohibited recovery behaviors reduce error-recovery attempts?
- STABILITY: structural (this rule always exists) + experimental (phrasing)

**stay_in_scope_rule**
- Current (defective): `**Stay in scope** - process only what you were given, nothing more` - bold label, dash, instruction. "Nothing more" is the boundary.
- Alternative A: `**Your input defines your world.** Process what you received. Do not supplement it from external sources, do not add context from your training data, do not fetch additional materials.` - reframes scope as an ontological boundary (your world IS your input) and names three specific out-of-scope behaviors.
- Alternative B: `**Scope = your input.** Everything not in the input does not exist for this task.` - algebraic framing. Scope equals input. Period. Everything else is null.
- Alternative C: `**Process what you were given. Nothing more. Nothing less.** Do not supplement. Do not skip. Do not expand.` - adds "nothing less" (anti-scope-reduction) and "do not skip" (anti-omission) to complement the anti-expansion rules.
- PURPOSE: Prevents the agent from expanding its task beyond what was given.
- HYPOTHESIS: The ontological framing in Alternative A ("your input defines your world") may produce deeper compliance than the behavioral framing ("process only what you were given") because it changes the agent's world model rather than its behavior rules. An agent that believes its input IS its world has no reason to look beyond it. An agent that is TOLD not to look beyond may still feel the pull to do so when its task seems to require it. Alternative C is interesting because it addresses both scope expansion AND scope reduction (skipping items), which is a real failure mode in batch-processing agents. Test: does ontological framing produce fewer out-of-scope operations than behavioral prohibition?
- STABILITY: structural + experimental

**no_invention_rule**
- Current (defective): `**No invention** - if the data doesn't support it, don't produce it` - bold label, dash, conditional instruction. "If...don't" framing.
- Alternative A: `**Every claim in your output must trace to your input.** If you cannot point to the input data that supports a statement, that statement is fabricated and must not appear.` - reframes invention as fabrication (a stronger negative) and provides a concrete test: can you point to the source?
- Alternative B: `**You are a transformer, not a generator.** Your output is a transformation of your input. If something in your output has no corresponding input, it is hallucination.` - leverages the LLM's understanding of its own architecture (transformer) to create a self-model constraint. Also uses "hallucination," a term LLMs have been heavily trained to associate with failure.
- Alternative C: `**No data, no output.** If the input does not contain information to support a claim, the claim does not appear in the output. Silence is correct when data is absent.` - adds "silence is correct" which gives the agent explicit permission to produce less output. LLMs' training pushes them to always produce output; this permission to be silent may be necessary for the prohibition on invention to work.
- PURPOSE: Prevents the agent from hallucinating data that is not in its input.
- HYPOTHESIS: Alternative A (traceability test) gives the agent a concrete, step-by-step mechanism for checking whether it is inventing: "can I point to the source?" This is more actionable than "don't produce it." Alternative B (transformer self-model) is the most psychologically interesting - it uses the LLM's knowledge of its own architecture as a behavioral constraint. But it may be too abstract for consistent application. Alternative C (permission to be silent) addresses the ROOT CAUSE of invention: the LLM's compulsion to produce output. Without permission to produce less, the prohibition on invention creates a double bind (must produce output + must not invent = ???). "Silence is correct when data is absent" resolves the double bind. This may be the most important design insight for this rule. Test: does explicit permission to produce less output reduce invention rates?
- STABILITY: structural + experimental

---

## STRUCTURAL: rule_format
TYPE: n/a (presentation choice for all rules)

### What the agent needs to understand

All rules in the section share a format. The format itself communicates authority level. A numbered list feels like a checklist (complete items sequentially). A bulleted list feels like a reference (consult as needed). Bold imperatives feel like commands. Paragraph prose feels like explanation.

### Fragments

**list_format**
- Current (defective): Numbered list, 1-6 for output-tool agents, 1-3 for no-output-tool agents. Each item is bold-label-dash-explanation format.
- Alternative A: Numbered list with NO explanations. Just the rule: `1. Use append_interview_summaries_record for all output.` `2. Process 20 records per batch.` `3. Write after every batch.` - the absence of explanation signals that the rules are not open to interpretation. Explanations invite reasoning; bare rules do not.
- Alternative B: Unnumbered bold imperatives, each on its own line with a horizontal rule between them. Each rule is visually isolated, which increases its individual weight.
- Alternative C: A single dense paragraph: `Use {tool_name} for all output. Process {batch_size} records per batch. Write after every batch. Fail immediately on error. Process only your input. Do not invent data.` - no formatting, no emphasis, no numbers. Just statements. This is the densest possible presentation and may be processed as a block of axioms rather than as items in a list.
- Alternative D: Bold-labeled rules in the current style but with a severity marker: `1. [HARD] **Use append_interview_summaries_record for all output** - ...` vs `4. [HARD] **Fail fast** - ...` - all rules are marked [HARD], reinforcing that none of them are soft.
- PURPOSE: Controls how the agent processes the rules: as a checklist, as commands, as axioms, or as items with explicit severity.
- HYPOTHESIS: The current format (numbered + bold label + explanation) is the most familiar to LLMs from training data and may produce the most predictable compliance. But familiarity also means the agent processes it the same way it processes any numbered list - sequentially, with roughly equal weight per item. Alternative A (no explanations) may produce stronger compliance because explanations create reasoning surface and reasoning creates exceptions. Alternative B (isolated rules with separators) may produce the strongest per-rule compliance by forcing a processing pause between rules. Alternative C (dense paragraph) is the highest-risk, highest-potential-reward option - if the agent processes it as a block of axioms, every rule benefits from the block's collective authority. If it processes it as a wall of text, nothing registers. Test: does removing explanations from rules increase or decrease compliance?
- STABILITY: formatting + experimental

---

## STRUCTURAL: rule_ordering
TYPE: n/a (sequence design)

### What the agent needs to understand

The order in which rules appear affects their processing weight. LLMs exhibit both primacy bias (first items register more strongly) and recency bias (last items are freshest in working memory). The middle of a list is the weakest position.

In the current defective output, the order is:
1. Output tool exclusivity (when present)
2. Batch discipline (when present)
3. Write timing (when present)
4. Fail fast
5. Stay in scope
6. No invention

This places the output-tool-specific rules first and the generic behavioral rules last. For a batch-processing agent, this may be correct: the output tool rules are the most frequently exercised. For a no-output-tool agent, the list is just items 4-6 (renumbered to 1-3), which puts fail-fast first.

### Fragments

**rule_sequence**
- Current (defective): output tool rules first, then generic rules. This is an operational-first ordering: the most mechanically frequent rules come first.
- Alternative A: Generic rules first, then output tool rules. This is a severity-first ordering: the deepest behavioral constraints come first (fail fast, stay in scope, no invention), followed by operational details. The agent reads the most important rules in the primacy position.
- Alternative B: Workspace confinement first (currently missing), then generic rules, then output tool rules. This is a boundary-first ordering: the broadest constraint (where you exist) before the behavioral constraints (how you act) before the operational constraints (how you write).
- Alternative C: No fixed ordering. Rules are presented in arbitrary order. This tests whether ordering actually matters for a small (3-6 item) list.
- PURPOSE: Maximizes the behavioral weight of the most important rules.
- HYPOTHESIS: For a short list (3-6 items), ordering effects may be minimal - the agent can hold the entire list in working memory. But for the primacy position (rule 1), there is likely a measurable effect. The question is which rule benefits most from position 1. Workspace confinement is the broadest constraint and may benefit from being first because it sets the spatial frame for everything that follows. Fail fast is the deepest behavioral constraint and may benefit from primacy because it overrides the agent's default error-recovery behavior. Output tool exclusivity is the most operationally critical for batch agents and may benefit from primacy because it is exercised most frequently. Test: does placing generic behavioral rules in primacy position reduce scope-creep and hallucination rates compared to placing operational rules first?
- STABILITY: experimental

---

## FIELD: has_output_tool
TYPE: boolean
OPTIONAL: no (always present)
VALUES: false (agent-builder) / true (interview-summary)

### What the agent needs to understand

This field is not presented to the agent. It is a GATE that controls which template prose blocks appear. The agent never sees "has_output_tool = true." Instead, it sees (or does not see) the output tool exclusivity rule, the batch discipline rule, and the write timing rule.

This field is the primary structural control for the entire section. It determines whether the section has 3 rules (no output tool) or 5-6 rules (output tool). The difference is significant: a 3-rule section feels terse and absolute. A 6-rule section feels like a detailed operational manual. The agent's relationship to the section may change based on its length.

### Design Implications

The conditional branching creates two fundamentally different section personalities:

**has_output_tool = false:**
The section is pure behavioral constraint. Three short, punchy rules about error handling, scope, and invention. The section reads fast, feels absolute, and leaves no operational details to soften its authority.

**has_output_tool = true:**
The section is a mix of operational procedure (output tool, batch size, write timing) and behavioral constraint (fail fast, scope, invention). The operational rules are necessary but they change the section's character from "absolute behavioral boundaries" to "operational rules and behavioral boundaries." The risk: the agent processes the entire section as operational, including the behavioral rules, and treats them with the same latitude it gives operational instructions.

This tension suggests a possible structural solution: SEPARATE the operational output rules from the behavioral rules within the section. Two sub-blocks within critical rules - one for output discipline, one for behavioral boundaries - each with its own heading or separator. This preserves the authority of the behavioral rules while housing the operational rules in the same section (because they are genuinely critical).

---

## FIELD: tool_name
TYPE: string
OPTIONAL: yes (only present when has_output_tool = true)
VALUES: absent (agent-builder) / "append_interview_summaries_record" (interview-summary)

### What the agent needs to understand

This field provides the literal tool name that appears in the output tool exclusivity rule. The agent must recognize this string as the name of a tool in its available tool set and use it exclusively for output.

The tool name also appears in the writing_output section (in the invocation display) and potentially in the frontmatter hooks. The critical_rules section is one of multiple places the agent encounters this name. Whether this redundancy reinforces recognition or produces information fatigue is an open question.

### Fragments

See `tool_name_interpolation` under the output_tool_exclusivity_rule template block above.

---

## FIELD: batch_size
TYPE: integer
OPTIONAL: yes (only present when has_output_tool = true)
VALUES: absent (agent-builder) / 20 (interview-summary)

### What the agent needs to understand

This field provides the literal number of records per batch. The agent uses this number as a loop control value: process N records, write, repeat.

### Fragments

See `batch_size_interpolation` under the batch_discipline_rule template block above.

---

## FIELD: name_needed
TYPE: boolean
OPTIONAL: yes (only present when has_output_tool = true; can be absent even when has_output_tool = true, as in truth-system-quality-control)
VALUES: absent (agent-builder) / true (interview-summary) / absent (truth-QC)

### What the agent needs to understand

When true, the agent must provide a filename parameter when calling the output tool. When absent or false, the output tool handles naming on its own.

### Fragments

See the file_naming_rule template block above.

---

## CROSS-SECTION DEPENDENCY: workspace_path

### The Problem

The workspace_path value needed for the workspace confinement rule lives in `[security_boundary].workspace_path`, not in `[critical_rules]`. In the two reference agents (agent-builder and interview-summary), the critical_rules section has NO workspace_path field. But other agents in the system (agent-deconstructor, agent-preparer, agent-auditor, agent-improver, truth-QA, truth-QC, embedding-normalize) DO have `workspace_path` directly in `[critical_rules]`.

This inconsistency means the template renderer must implement a fallback chain:
1. If `critical_rules.workspace_path` exists, use it.
2. Otherwise, use `security_boundary.workspace_path`.
3. If neither exists, omit the workspace confinement rule (this case may not occur in practice).

### Design Implications

Cross-section dependencies are architecturally unpleasant. They mean a section cannot be rendered in isolation - it needs data from another section. This creates coupling between sections that makes the template system harder to reason about.

However, the workspace_path dependency may be the correct design. The workspace confinement RULE belongs in critical_rules (it is an inviolable behavioral constraint). The workspace PATH belongs in security_boundary (it is security configuration). The rule references the path. This is a legitimate read dependency, not a design flaw.

The template system should resolve this dependency at render time: the critical_rules template accepts workspace_path as a parameter, sourced from wherever the data model provides it.

---

## SYNTHESIS: The Section's Architecture

### Two-Personality Problem

The critical_rules section has two distinct personalities depending on `has_output_tool`:

**Personality 1: Behavioral Fence (no output tool)**
- Workspace confinement (needs workspace_path)
- Fail fast
- Stay in scope
- No invention
- Character: terse, absolute, behavioral

**Personality 2: Operational + Behavioral Fence (has output tool)**
- Workspace confinement (needs workspace_path)
- Output tool exclusivity (uses tool_name)
- Batch discipline (uses batch_size)
- Write after every batch (extension of batch discipline)
- Fail fast
- Stay in scope
- No invention
- Character: mixed operational and behavioral, longer, more detail-heavy

The design challenge is maintaining the section's AUTHORITY across both personalities. The short version feels absolute. The long version risks feeling operational. Possible solutions:

1. **Internal structure:** Separate the operational block from the behavioral block with a visual divider or sub-heading. The agent processes two sub-sections: "how you write" and "how you behave."

2. **Authority gradient:** Present behavioral rules first (primacy position) and operational rules second. The behavioral rules establish the section's authority before the operational rules arrive.

3. **Uniform format:** Make all rules look the same regardless of whether they are operational or behavioral. No sub-structure, no hierarchy. The section is a flat list and every item has equal authority.

### The Inviolability Problem

The deepest question this analysis addresses: how does prose become a wall?

Five mechanisms, from weakest to strongest:

1. **Labeling:** Call the section "Critical Rules." This is what the current system does. It is the weakest mechanism because it is just a label. Labels can be overridden by reasoning.

2. **Assertion:** State in a preamble that these rules override everything else. Stronger than labeling because it establishes a hierarchy. But assertions can still be reasoned about.

3. **Consequence:** Link rule violations to task failure. Stronger than assertion because LLMs are trained to avoid stated failure conditions. But the agent can reason that "this particular violation won't really cause failure."

4. **Ontological reframing:** Tell the agent that these rules describe reality, not preferences. "You cannot break these rules" rather than "you must not break these rules." This is stronger because it changes the agent's model of what is possible, not just what is permitted. But LLMs know they CAN generate any text, so "cannot" may be processed as false.

5. **Structural authority:** Place the rules in a section that LOOKS different from every other section. Different formatting, different density, different visual weight. The agent's processing shifts when it enters this zone - not because it was told to shift, but because the visual environment changed. This is the deepest mechanism because it operates below explicit instruction processing.

The optimal design likely combines mechanisms 2 + 3 + 5: a hierarchy-establishing preamble, consequence-linked rules, and visually distinct formatting. Mechanism 4 (ontological reframing) should be used selectively - it works for workspace confinement ("nothing outside your workspace exists") but is dishonest for output tool exclusivity (the agent CAN write files directly; telling it it cannot is a lie it may detect).

### What the Current System Gets Wrong

1. **Missing workspace confinement rule.** Neither reference agent has a workspace confinement rule in its critical rules section. This is a significant omission.

2. **Missing preamble.** No authority framing before the rules. The numbered list starts immediately.

3. **Inconsistent workspace_path placement.** Some agents have it in critical_rules, others do not. The template must handle both.

4. **No visual differentiation from other sections.** The critical rules section looks exactly like any other numbered list. Nothing signals to the agent that these rules are qualitatively different from constraints or anti-patterns.

5. **Explanations on rules invite reasoning.** Each rule has a dash-separated explanation that tells the agent what the rule means. This is helpful for comprehension but harmful for authority - explanations create reasoning surface, and reasoning creates exceptions.
