# Critical Rules Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The critical rules section must produce a qualitatively different cognitive state than any other section. After reading instructions, the agent knows what to do. After reading constraints, the agent knows what boundaries to respect. After reading critical rules, the agent must believe that violating these rules constitutes operational failure — not poor performance, not suboptimal behavior, but system-breaking failure that cannot be recovered from.

This is the hardest behavioral effect to achieve with prose. Every LLM section says "this is important." The instructions section is the "most important" behavioral programming. The constraints section contains "MUST" and "MUST NOT" directives. Success and failure criteria define the outcomes. All of these compete for the agent's compliance attention. Critical rules must win that competition — not by shouting louder, but by occupying a different category in the agent's processing hierarchy.

The distinction is between **compliance** (following rules because they are stated) and **inviolability** (treating rules as physical laws of the operating environment). Compliance is what the agent gives to constraints: "I should do this." Inviolability is what the agent gives to, say, the instruction to return output in a specific format: it does not even consider alternatives because the rule is below the threshold of deliberation. The critical rules section must push its content below that threshold — into the space of things the agent does not question, reconsider, or weigh against competing concerns.

How does prose achieve this? Three mechanisms, each with different leverage:

1. **Framing as environment, not preference.** "Do not write outside the workspace" can be framed as a preference ("you should stay within the workspace") or as a physical law ("files outside the workspace cannot be created — the system will reject them"). The environmental framing removes the agent's sense of choice. It is not being asked to comply; it is being informed of what is possible.

2. **Consequence immediacy.** Rules with visible, immediate consequences feel more real than rules with abstract consequences. "If you write outside the workspace, the operation will fail silently" is more constraining than "stay within the workspace for security reasons." The consequence makes the rule feel testable and enforceable.

3. **Categorical separation.** If critical rules are visually and structurally distinct from all other rule-like content (constraints, anti-patterns, instructions), the agent processes them in a different register. If they look like constraints, they will be treated as constraints. The section must not look like anything else in the prompt.

### What the defective renderer currently does

Agent-builder (no output tool):
```
## Critical Rules

1. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
2. **Stay in scope** — process only what you were given, nothing more
3. **No invention** — if the data doesn't support it, don't produce it
```

Interview-summary (has output tool):
```
## Critical Rules

1. **Use append_interview_summaries_record for all output** — never write files directly, never use a different write tool
2. **Batch discipline** — process exactly 20 records per batch (last batch may be smaller)
3. **Write after every batch** — do not accumulate records in memory across batches
4. **Fail fast** — if something is wrong, FAILURE immediately with clear reason
5. **Stay in scope** — process only what you were given, nothing more
6. **No invention** — if the data doesn't support it, don't produce it
```

Observations about the defective output:
- Uses a numbered list with bold keywords — the same visual pattern as constraints. Nothing structurally distinguishes these "critical rules" from the "constraints" section above.
- The workspace confinement rule is completely absent despite being one of the most important operational constraints (it exists implicitly in the security boundary section but is not reinforced here).
- The output tool rules (items 1-3 for interview-summary) are purely informational — they tell the agent what to do but do not frame the consequences of violation.
- The generic rules (4-6) are vague aphorisms ("stay in scope," "no invention") that function more as reminders than as hard constraints. They lack the specificity that makes rules enforceable.
- The section is at the END of the prompt — the lowest-salience position. Everything before it has already competed for the agent's attention.

The fundamental failure: the current critical rules section reads as a summary of things the agent should already know from other sections. It does not establish a new behavioral category. An agent reading it would process it as "more constraints" rather than as "inviolable operating laws."

---

## THE ARCHITECTURAL CHALLENGE: Conditional Branching

Before analyzing individual fields and prose blocks, the section's branching architecture must be understood. Critical rules is not a single section — it is a section with two fundamentally different configurations:

**Configuration A: No output tool** (`has_output_tool = false`)
The agent produces output through general file operations (Write, Edit, etc.). The critical rules section contains ONLY generic rules: workspace confinement, fail-fast, scope limitation. This is a short, tight section — perhaps 3-5 rules.

**Configuration B: Has output tool** (`has_output_tool = true`)
The agent produces output through a specific validated tool. The critical rules section contains the generic rules PLUS output-tool-specific rules: tool exclusivity, batch discipline, write frequency, tool invocation format, and possibly file naming. This is a longer section — perhaps 6-10 rules, with the output tool rules being the most operationally specific.

The design question: should Configuration B simply append more rules to Configuration A's list? Or should the two configurations be structurally different — with Configuration B having a sub-structure (e.g., "Output Discipline" as a named sub-block) that Configuration A does not?

This branching is the most important structural decision in the section. It determines whether output tool agents get a qualitatively different critical rules experience or merely a quantitatively longer one.

---

## TEMPLATE BLOCK: section_framing

GATED BY: always present
OPTIONAL: no

### What the agent needs to understand

The section framing is the prose that opens the critical rules section and establishes its authority level. This is the single highest-leverage template block in the entire section. If the framing fails to establish inviolability, the individual rules will be processed as recommendations regardless of their content.

The framing must accomplish:
1. Signal that what follows is categorically different from other rules in the prompt
2. Establish the consequence of violation (not "poor performance" but "system failure")
3. Set the agent's processing posture to "do not deliberate — comply"

### Fragments

**section_heading**
- Current (defective): `## Critical Rules` — same heading level and style as other sections
- Alternative A: `## INVIOLABLE OPERATING RULES` — all-caps keyword changes the visual register, "operating" frames rules as environmental
- Alternative B: `## Hard Constraints` — distinguishes from "soft" constraints in the constraints section by naming the category explicitly
- Alternative C: `## System Rules` — frames the rules as belonging to the system, not to the task; the agent is operating within a system that has non-negotiable rules
- Alternative D: Keep `## Critical Rules` but change the structural position — place this section FIRST (or immediately after identity), not last. Primacy may matter more than the heading text.
- PURPOSE: The heading names the category. If the heading sounds like another version of "constraints" or "guidelines," the agent will process its contents in the same register. The heading must signal "different kind of content ahead."
- HYPOTHESIS: "Critical Rules" (current) is weak because "critical" is overused — every section feels critical. "Inviolable" is a stronger signal but may be parsed as hyperbole by a sophisticated model. "System Rules" reframes from "important things about your task" to "laws of the environment you operate in," which is the environmental framing that produces the deepest compliance. "Hard Constraints" explicitly creates a hierarchy against the constraints section. Test: does "System Rules" produce different compliance behavior than "Critical Rules"? Does position (first vs. last) matter more than wording?
- STABILITY: structural (heading level) + experimental (heading text and section position)

**authority_preamble**
- Current (defective): no preamble — heading followed directly by the numbered list
- Alternative A: `These rules are not guidelines. Violating any of them constitutes operational failure regardless of the quality of your other work.` — direct statement of consequence
- Alternative B: `The following rules are enforced by the system. Violations are detected automatically and cause immediate task failure.` — frames rules as mechanically enforced, removing the sense that the agent is being *asked* to comply
- Alternative C: `Every rule below is a hard boundary. You will encounter situations where following your instructions seems to conflict with these rules. In every case, the rule wins.` — anticipates the specific failure mode where the agent rationalizes violating a rule to better follow its instructions
- Alternative D: No preamble — the rules should speak for themselves. Adding meta-prose about how important the rules are is precisely the kind of inflation that LLMs produce and other LLMs learn to discount. The rules should be inviolable because of their content and position, not because a preamble says they are.
- Alternative E: `You cannot violate these rules. Not "should not" — cannot. They describe the boundaries of what your system permits.` — explicit reframing from "should" to "cannot," which moves rules from normative to descriptive
- PURPOSE: Establishes the processing register for everything that follows. Without the preamble, the rules are just another numbered list. With it, they are framed as a different kind of content.
- HYPOTHESIS: Alternative A (consequence statement) works by making the stakes visible. Alternative B (system enforcement) works by removing agency — the agent is not choosing to comply, the system is enforcing. Alternative C (conflict anticipation) is the most specific to LLM failure modes: it addresses the exact scenario where an agent violates a rule because it thinks its instructions override the rules. Alternative D (no preamble) is a valid contrarian position — perhaps the authority should come from structural position and rule quality, not from meta-prose. Alternative E (cannot vs should not) directly targets the linguistic framing that produces the deepest compliance in language models. Test: does framing rules as "cannot" produce different compliance than "must not"? Does anticipating instruction/rule conflicts (C) reduce that specific failure mode?
- STABILITY: experimental — this fragment does not exist and has the highest behavioral leverage of any fragment in the section

---

## TEMPLATE BLOCK: workspace_confinement_rule

GATED BY: always present (but uses `workspace_path` from security_boundary section)
CROSS-SECTION DEPENDENCY: `security_boundary.workspace_path`
OPTIONAL: no

### What the agent needs to understand

The workspace confinement rule tells the agent that all its operations must stay within a specific filesystem subtree. This is the most fundamental operational constraint: the agent's entire world is the workspace, and nothing outside it exists for the purposes of this task.

This rule is architecturally interesting because:
1. The data (`workspace_path`) lives in `[security_boundary]`, not in `[critical_rules]`. The critical rules section must reference data owned by another section.
2. The security boundary section already describes allowed paths and tools. The workspace confinement rule in critical_rules is a REINFORCEMENT — the same constraint stated again in a different register.
3. This duplication is intentional. The security boundary section tells the agent what it CAN do (allowlist). The critical rules section tells the agent what it CANNOT do (prohibition). Both express the same confinement, but the prohibition framing is harder.

### Fragments

**confinement_rule_text**
- Current (defective): not rendered in critical_rules — workspace confinement exists only in the security_boundary section
- Alternative A: `All file operations must target paths within {workspace_path}. Operations targeting paths outside this boundary will fail silently.` — states the boundary and the consequence
- Alternative B: `Your workspace is {workspace_path}. Nothing outside this path exists. Do not reference, read, write, or search outside it.` — frames the boundary as reality ("nothing exists") rather than as a rule ("don't go there")
- Alternative C: `Workspace boundary: {workspace_path}. This is enforced by hooks. Attempts to access paths outside this boundary are intercepted and rejected before execution.` — names the enforcement mechanism, making it concrete
- Alternative D: `{workspace_path} is your entire operating environment. Paths outside it are not accessible to you.` — short, declarative, environmental
- PURPOSE: Establishes the physical boundary of the agent's world. The security_boundary section lists what is allowed; this rule states the prohibition.
- HYPOTHESIS: Alternative A (consequence) makes the rule feel enforceable. Alternative B (ontological — "nothing exists") is the strongest reframing because it removes the concept of "outside" entirely; the agent cannot violate a boundary that it doesn't believe has an "other side." Alternative C (mechanism naming) appeals to the agent's understanding of system architecture — naming "hooks" makes enforcement feel real. Alternative D (short declarative) relies on brevity for authority — the rule is so obvious it needs only one sentence. Test: does ontological framing ("nothing exists") produce fewer boundary violations than prohibition framing ("do not access")? Does naming the enforcement mechanism increase compliance?
- STABILITY: structural (rule must exist) + experimental (framing strategy)

**workspace_path_display**
- Current (defective): path not shown in critical rules section at all
- Alternative A: Inline in the rule text: `...within /Users/johnny/.ai/spaces/bragi.`
- Alternative B: As a separate labeled value: `Workspace: /Users/johnny/.ai/spaces/bragi` followed by the rule text
- Alternative C: Referenced but not displayed: `...within the workspace path defined in your Security Boundary above.` — avoids duplicating the path value
- PURPOSE: The workspace path must be unambiguous. The agent must know the exact path, not a concept of "the workspace."
- HYPOTHESIS: Inline display (A) is most direct — the rule contains its own reference. Labeled value (B) separates the data from the rule, which may make the path more prominent but disconnects it from the prohibition. Back-reference (C) avoids duplication but forces the agent to recall information from an earlier section, which may be unreliable in long prompts. For critical rules, the safest choice is probably inline display — duplication is a feature, not a bug, because the agent must not need to look elsewhere.
- STABILITY: formatting — the display mode is unlikely to have strong behavioral effects, but inline vs. reference may matter for long prompts where earlier sections lose salience

---

## TEMPLATE BLOCK: output_tool_exclusivity_rule

GATED BY: `has_output_tool = true`
OPTIONAL: yes (absent when `has_output_tool = false`)

### What the agent needs to understand

When an agent has an output tool, ALL output must go through that tool. Not most output. Not output when it is convenient. ALL output, every time, with no exceptions. This rule exists because:

1. The output tool performs schema validation. Writing directly to files bypasses validation.
2. The output tool enforces file naming, directory placement, and record format. Direct writes can produce malformed output that downstream consumers cannot parse.
3. The hook system enforces tool exclusivity — direct file writes may be intercepted and rejected. But the agent should not be testing the enforcement; it should be complying because the rule is understood.

This is the rule most likely to be violated by a capable agent. A sophisticated model may reason: "I understand the schema, I can produce valid JSON, and writing directly would be more efficient." This reasoning is correct in every particular and wrong in conclusion. The output tool exists not because the agent cannot produce valid output, but because the system DEPENDS on the output tool being the single write path for auditing, validation, and pipeline integrity.

### Fragments

**tool_exclusivity_statement**
- Current (defective): `**Use append_interview_summaries_record for all output** — never write files directly, never use a different write tool` — bold keyword with inline prohibition
- Alternative A: `Every output record must be written using {tool_name}. Direct file writes (Write, Edit, Bash echo/cat) are prohibited. There is no exception, including for error recovery, partial output, or testing.` — exhaustive prohibition that names the specific bypass mechanisms
- Alternative B: `{tool_name} is your only write mechanism. You do not have the ability to write output through any other path.` — environmental framing (you cannot, not you must not)
- Alternative C: `Output path: {tool_name}. The system validates every record through this tool. Bypassing it produces invalid output regardless of whether the JSON is correct — validation metadata, file locking, and audit records are added by the tool, not by you.` — explains WHY the tool is exclusive, naming the invisible functions the agent cannot replicate
- Alternative D: `Write all output using {tool_name}. No other tool, no direct file operations, no exceptions.` — terse imperative
- PURPOSE: Prevents the agent from bypassing the validated output tool. The phrasing must be strong enough to override the agent's self-assessed competence at producing valid output directly.
- HYPOTHESIS: The defective version (bold keyword) looks like a preference. Alternative A (exhaustive prohibition) closes loopholes by naming them — "including error recovery" preempts the most common rationalization. Alternative B (environmental) removes the concept of choice. Alternative C (invisible functions) explains why even a "correct" bypass produces invalid output — this targets the specific reasoning an agent uses to justify bypassing. Alternative D (terse) relies on brevity and command tone. Test: does explaining the invisible functions (C) reduce bypass attempts more than categorical prohibition (A)? The hypothesis is that capable models (Opus) are more likely to bypass when they don't understand WHY the rule exists, so explanation (C) may be more effective for Opus while categorical prohibition (A) may be more effective for Sonnet.
- STABILITY: structural (must exist when has_output_tool = true) + experimental (phrasing strategy)

**tool_name_display**
- Current (defective): tool name appears inline as bold text in the rule
- Alternative A: Code-formatted inline: `` `append_interview_summaries_record` `` — visually marks the tool name as a technical identifier
- Alternative B: Repeated at each mention — tool name appears every time the rule references the output tool, never abbreviated to "the tool" or "it"
- Alternative C: Defined once, then referenced: `Your output tool is {tool_name} (referred to below as "the output tool").` — defined explicitly, then shortened
- PURPOSE: The tool name must be unambiguous. The agent must use exactly this name when invoking the tool. Any abbreviation, paraphrase, or guess about the tool name will fail.
- HYPOTHESIS: Code formatting (A) signals "this is a literal identifier — use it exactly." Repetition (B) prevents the agent from losing track of the exact name in a long section. Definition-then-reference (C) is cleaner prose but risks the agent using "the output tool" as a concept rather than invoking the specific name. For critical rules, repetition of the exact name is safest — redundancy serves reliability.
- STABILITY: formatting — the display style is a formatting choice, but repetition vs. abbreviation may have behavioral effects

---

## TEMPLATE BLOCK: batch_discipline_rule

GATED BY: `has_output_tool = true` AND `batch_size` is present
OPTIONAL: yes (absent when `has_output_tool = false`)

### What the agent needs to understand

Batch discipline means the agent processes a fixed number of records, writes them, then processes the next batch. This prevents two failure modes:

1. **Memory accumulation failure.** An agent that processes all records before writing any output is holding all results in its context window. For large inputs (100+ records), this causes context window pressure, lost records, and hallucinated or duplicated entries. Batch discipline forces periodic writes that clear the agent's working memory.

2. **Catastrophic loss on failure.** If the agent processes 100 records and fails on record 95, all 100 records of work are lost. If the agent writes in batches of 20, failure on record 95 means records 1-80 are already safely written.

The `batch_size` field (20 for interview-summary) defines the batch quantum. The rule must communicate both the number and the discipline — not just "write in groups of 20" but "process exactly 20, write, then continue; do not accumulate across batch boundaries."

### Fragments

**batch_size_rule_text**
- Current (defective): `**Batch discipline** — process exactly 20 records per batch (last batch may be smaller)` — single-line statement
- Alternative A: `Process records in batches of {batch_size}. After processing {batch_size} records, write them all using {tool_name} before processing any more. The last batch may be smaller than {batch_size}. Do not hold records across batch boundaries.` — explicit multi-sentence rule that names the tool and the boundary
- Alternative B: `Batch size: {batch_size}. Process {batch_size} records. Write them. Repeat. Never hold more than {batch_size} unwritten records.` — staccato imperative
- Alternative C: `Memory management: write output in batches of {batch_size}. Accumulated unwritten records beyond {batch_size} risk context loss and duplicate entries. Write frequently, not at the end.` — frames as memory management with named consequences
- Alternative D: `{batch_size}-record batches. Process → write → repeat. No exceptions. No "I'll write them all at the end." The batch boundary is a hard checkpoint.` — directly addresses the anticipated failure mode (writing everything at the end)
- PURPOSE: Establishes the batch quantum and the discipline of writing at batch boundaries. The phrasing must prevent the agent's natural tendency to accumulate results and write once.
- HYPOTHESIS: The defective version states the batch size but does not address the behavioral tendency to defer writes. Alternative A is the most complete but also the longest. Alternative B uses staccato rhythm to make the pattern feel automatic — process, write, repeat. Alternative C frames the rule as serving the agent's own interests (preventing context loss) rather than as an external imposition. Alternative D directly names and prohibits the failure mode. Test: does naming the failure mode ("no 'I'll write them all at the end'") reduce that specific behavior? Does framing as self-interest (C) produce stronger compliance than framing as external rule (A)?
- STABILITY: structural (batch rule must exist when batch_size is present) + experimental (phrasing)

**write_frequency_rule_text**
- Current (defective): `**Write after every batch** — do not accumulate records in memory across batches` — separate rule from batch size
- Alternative A: Merge with batch_size_rule — write frequency is part of batch discipline, not a separate rule. Having two rules about the same concept dilutes both.
- Alternative B: Keep separate but make the consequence explicit: `Write output after every batch. Records held in memory but not written are lost if you encounter an error. Written records survive.` — consequence framing
- Alternative C: `After every {batch_size} records: stop processing and write. This is a checkpoint, not a suggestion. Processing must pause at each batch boundary.` — frames the write as a mandatory stop, not an optional save point
- PURPOSE: Reinforces that writes happen at batch boundaries, not at the end. This is either part of the batch discipline rule or a separate rule — the structural choice matters.
- HYPOTHESIS: Merging with batch discipline (A) makes the rule feel unified and coherent. Keeping separate (B/C) gives the write frequency its own emphasis. The risk of merging is a long, complex rule. The risk of separating is that the agent treats them as independent and may comply with one while violating the other. Test: does a single unified batch-discipline rule produce better compliance than two separate rules (batch size + write frequency)?
- STABILITY: structural (merge vs. separate is a significant design choice) + experimental (phrasing)

---

## TEMPLATE BLOCK: tool_invocation_format_rule

GATED BY: `has_output_tool = true`
OPTIONAL: yes (absent when `has_output_tool = false`)
CROSS-SECTION NOTE: The exact invocation syntax is defined in `[writing_output]`, not in `[critical_rules]`. This rule may reference or reinforce the format specified there.

### What the agent needs to understand

The output tool has a specific invocation syntax. The agent must use it exactly. Not approximately — exactly. Tool invocation via Bash heredoc is fragile: wrong quoting, wrong delimiter, wrong argument order, wrong tool name all produce silent failures or malformed output.

However, the invocation format is more properly the concern of the `writing_output` section. The question for critical rules is: should the invocation format appear here as a RULE (reinforcement), or should this section only reference it?

### Fragments

**invocation_format_placement**
- Current (defective): The invocation format appears in the writing_output section as a code block. Critical rules mentions the tool name but not the format.
- Alternative A: Critical rules references but does not repeat the format: `Use the exact invocation format shown in the Writing Output section. Do not modify the syntax.`
- Alternative B: Critical rules repeats the format as a rule: `Tool invocation must match exactly: {tool_name} {name} <<'EOF' / {json_data} / EOF` — duplication for emphasis
- Alternative C: Critical rules does not mention invocation format at all — it is the writing_output section's concern, and critical_rules stays at a higher level of abstraction
- PURPOSE: Decides whether invocation format is a critical rule (violations cause system failure) or an operational detail (covered elsewhere).
- HYPOTHESIS: Invocation format IS a system-failure-level concern — wrong syntax produces no output or corrupted output. But repeating it in two sections (writing_output + critical_rules) risks inconsistency if one section's template is updated without the other. Reference without repetition (A) is the safest compromise: it elevates the format to critical status without duplicating the data. Test: does referencing the invocation format in critical rules reduce invocation errors compared to relying solely on the writing_output section?
- STABILITY: structural (whether to include at all) + the specific format is owned by writing_output and should not be duplicated

---

## TEMPLATE BLOCK: file_naming_rule

GATED BY: `name_needed = true`
OPTIONAL: yes
CROSS-SECTION NOTE: The name template/pattern is defined in `[output]` and `[writing_output]`, not in `[critical_rules]`.

### What the agent needs to understand

When `name_needed = true`, the output tool requires a filename argument. The agent must construct this filename from available parameters (e.g., the `uid` parameter for interview-summary). This is a critical rule because wrong filenames either overwrite existing data or create orphaned files that downstream consumers cannot find.

### Fragments

**naming_rule_text**
- Current (defective): No explicit naming rule in critical_rules. The writing_output section shows `{name}` in the invocation template, and the output section specifies `name_template = "{interview-id}.summaries.jsonl"`.
- Alternative A: `The output filename must be constructed from the uid parameter: {uid}.summaries.jsonl. Using a wrong filename creates orphaned output that downstream processes cannot find.` — explicit construction rule with consequence
- Alternative B: `When invoking {tool_name}, the {name} argument must match the expected pattern. Consult the Output section for the name template.` — references without duplicating
- Alternative C: `Output filename: derived from uid parameter. Wrong names = lost output.` — terse with sharp consequence
- PURPOSE: Ensures the agent constructs the correct filename. This matters because the filename is the primary key for downstream consumers.
- HYPOTHESIS: Explicit construction (A) is the most reliable — the agent has the exact rule in front of it. But it duplicates data from the output section and creates a maintenance burden. Reference (B) is cleaner but requires the agent to remember information from another section. Terse with consequence (C) is high-impact but may be too compressed for reliable compliance. Test: does an explicit filename construction rule reduce naming errors compared to relying on the output section's template?
- STABILITY: structural (rule must exist when name_needed = true) + formatting (how much to duplicate from output section)

---

## TEMPLATE BLOCK: generic_rules

GATED BY: always present (both configurations)
OPTIONAL: no

### What the agent needs to understand

These are rules that apply to every agent regardless of output tool configuration. The current renderer produces three: "fail fast," "stay in scope," "no invention." These are the rules that must work for BOTH the agent-builder (broad creative task, no output tool) and the interview-summarizer (tight batch processing, has output tool).

The design question is whether these rules are truly inviolable operating constraints or whether they are summary restatements of principles expressed elsewhere (constraints, anti-patterns, instructions). If the latter, they dilute the section's authority — the agent recognizes them as repetitions and processes the entire critical rules section in the "reminder" register.

### Fragments

**fail_fast_rule**
- Current (defective): `**Fail fast** — if something is wrong, FAILURE immediately with clear reason` — bold keyword with dash-separated explanation
- Alternative A: `On unrecoverable error: return FAILURE with reason immediately. Do not attempt workarounds, partial output, or degraded operation.` — specific about what NOT to do on error
- Alternative B: `If you encounter an error you cannot resolve: stop. Return FAILURE. Do not produce partial output hoping it will be useful — partial output from a failed run is worse than no output, because it may be consumed as complete.` — explains the WHY: partial output is dangerous
- Alternative C: `FAILURE is not a last resort. It is the correct response to unrecoverable errors. Returning FAILURE with a clear reason is success — it means the system can diagnose and retry. Struggling to produce output despite errors is the actual failure mode.` — reframes FAILURE as a positive outcome, not a negative one
- Alternative D: `Errors: return FAILURE immediately. No partial output. No workarounds.` — minimal imperative
- PURPOSE: Prevents the agent from struggling through errors to produce degraded output. LLMs are strongly trained to be helpful, which means they strongly resist returning FAILURE. This rule must override that training.
- HYPOTHESIS: The current version ("fail fast") is a slogan, not a rule. Alternative A names the specific prohibited behaviors (workarounds, partial output, degraded operation). Alternative B explains WHY partial output is dangerous — this may be more effective for Opus, which responds to reasoning. Alternative C is the most radical reframe: it tells the agent that FAILURE is the right thing to do, directly countering the helpfulness training that makes agents reluctant to fail. Alternative D is the disciplined minimum. Test: does reframing FAILURE as a positive outcome (C) actually reduce the "struggle to produce partial output" failure mode? This is high-leverage because it directly opposes a core LLM training incentive.
- STABILITY: structural (rule must exist) + experimental (the reframe is a genuinely novel approach)

**scope_limitation_rule**
- Current (defective): `**Stay in scope** — process only what you were given, nothing more` — vague
- Alternative A: `Process only the input you were given. Do not fetch additional data, do not consult external sources, do not supplement the input with information from your training.` — names the specific out-of-scope behaviors
- Alternative B: `Your input is complete. If it seems incomplete, it is not — you have everything you need. Do not seek additional information.` — frames the input as definitionally complete, removing the agent's basis for going out of scope
- Alternative C: `Scope: the input provided by the dispatcher. If information seems missing, note it in your FAILURE response — do not attempt to fill gaps from training data or external sources.` — redirects the "something seems missing" impulse toward FAILURE rather than toward invention
- Alternative D: Omit this rule — it is a restatement of the instructions (which already define what to process) and the constraints (which already prohibit external sources). Including it here dilutes the section.
- PURPOSE: Prevents scope expansion. Agents naturally expand scope because they are trained to be helpful and comprehensive.
- HYPOTHESIS: The current version is too vague to be actionable. What does "stay in scope" mean? Alternative A names the specific prohibited behaviors, making the rule testable. Alternative B is ontological — it redefines the input as complete, which changes the agent's perception rather than adding a prohibition. Alternative C channels the impulse productively — if something seems missing, fail rather than invent. Alternative D raises a valid concern: if this rule merely repeats other sections, it weakens the section's authority. The counter-argument is that repetition in a "critical rules" register produces stronger compliance than the same content in a "constraints" register. Test: does the scope rule produce measurable behavioral change beyond what the constraints section already achieves?
- STABILITY: experimental — whether this rule earns its place in the critical section is itself an open question

**no_invention_rule**
- Current (defective): `**No invention** — if the data doesn't support it, don't produce it` — vague
- Alternative A: `Do not generate content that is not grounded in your input. Every claim in your output must trace to something in the input data. If you cannot point to the source, do not include it.` — traceability requirement
- Alternative B: `You are a transformer, not a generator. Your output is a transformation of your input. If something appears in your output that did not appear in your input, it is an error.` — identity reframing (you are a transformer)
- Alternative C: `No hallucination. If the input does not contain it, your output must not contain it. This applies to facts, interpretations, significance, and causal claims.` — uses the loaded term "hallucination" as a self-check
- Alternative D: Merge with scope_limitation — "don't go beyond your input" and "don't invent beyond your data" are the same constraint. Splitting them into two rules weakens both.
- PURPOSE: Prevents hallucination and invention. This is the most fundamental LLM failure mode and arguably the most important rule.
- HYPOTHESIS: The current version is a slogan. Alternative A (traceability) gives the agent a concrete test: "can I point to the source?" This is actionable. Alternative B (identity reframing) tells the agent WHAT IT IS — a transformer, not a generator — which operates at the identity level below conscious reasoning. Alternative C (naming hallucination) uses a term the agent's training includes extensive knowledge about; the self-awareness may trigger trained anti-hallucination behaviors. Alternative D (merge) reduces rule count and increases coherence. Test: does identity-level reframing ("you are a transformer") produce less hallucination than behavioral prohibition ("do not invent")? This is a genuinely different intervention — it changes self-model rather than adding a rule.
- STABILITY: experimental — the phrasing choice here interacts with identity section design

---

## STRUCTURAL: section_position

### What the agent needs to understand

The critical rules section is currently rendered LAST in the prompt (after return_format). This is the lowest-salience position. LLMs attend most strongly to the beginning (primacy) and recent context (recency in conversation), but for a static prompt, the beginning receives the strongest initialization effect. The end is read last, but by the time the agent reaches it, its behavioral posture is already established by 12 preceding sections.

### Fragments

**position_in_prompt**
- Current (defective): last section, after return_format
- Alternative A: First section after identity — the agent reads its identity, then immediately reads its inviolable constraints before anything else. All subsequent sections (instructions, examples, output) are read through the lens of these rules.
- Alternative B: Last section (current position) but with structural reinforcement — a brief "reminder block" at the end of the instructions section that says "Before proceeding, re-read the Critical Rules section above"
- Alternative C: Split — generic rules appear early (after identity), output-tool rules appear with the writing_output section
- Alternative D: Immediately before instructions — the agent reads the rules first, THEN reads the instructions, so it interprets every instruction through the rules lens
- PURPOSE: Section position controls when the rules enter the agent's processing context and how much subsequent content competes with them.
- HYPOTHESIS: Early position (A/D) means the rules are the lens through which everything else is interpreted. Late position (current) means the rules are a postscript that must override already-established behavior patterns. The primacy effect (A) is strong for initialization but may fade by the time the agent reaches step 5 of 7 instructions. The split approach (C) is architecturally clean but loses the unity of a single "inviolable rules" section. Test: does moving critical rules to immediately after identity improve compliance compared to the current last-position placement?
- STABILITY: structural — this is a once-decided architectural choice, not an experimental knob. But it may be the single highest-leverage structural change for this section.

---

## STRUCTURAL: rule_presentation_format

### What the agent needs to understand

How rules are visually formatted affects whether the agent processes them as items in a list (to be weighed and selectively applied) or as categorical imperatives (each one non-negotiable).

### Fragments

**rule_list_format**
- Current (defective): numbered list with bold keywords — `1. **Fail fast** — explanation`
- Alternative A: Unnumbered, each rule as its own bold paragraph heading followed by the rule text:
  ```
  **Workspace Boundary**
  All operations must target paths within /Users/johnny/.ai/spaces/bragi. ...

  **Output Tool Exclusivity**
  Every record must be written using append_interview_summaries_record. ...
  ```
- Alternative B: Each rule as a sub-heading (H3 within the H2 section), giving each rule heading-level authority:
  ```
  ### Workspace Boundary
  ...
  ### Output Tool Exclusivity
  ...
  ```
- Alternative C: Each rule as a single, self-contained sentence. No elaboration, no explanation. The rule is one sentence and it is absolute. Elaboration goes elsewhere (constraints, instructions).
  ```
  All file operations must target paths within /Users/johnny/.ai/spaces/bragi.
  Every output record must be written using append_interview_summaries_record.
  Process records in batches of 20 and write after each batch.
  ```
- Alternative D: Table format — Rule | Consequence, making the consequence visible and paired:
  ```
  | Rule | Consequence |
  | All output via tool | Direct writes produce invalid records |
  | Batch size: 20 | Memory accumulation → lost records |
  ```
- PURPOSE: The visual format determines whether rules are processed as a list (skimmable, selective attention) or as individual imperatives (each one receiving full attention).
- HYPOTHESIS: Numbered lists (current) invite the agent to process rules as a ranked sequence — rule 1 feels more important than rule 6. Bold paragraph headings (A) give each rule equal visual weight. Sub-headings (B) give rules heading-level authority, which LLMs tend to weight heavily. Single sentences (C) make each rule feel like an axiom — no elaboration means no negotiation room. Tables (D) pair each rule with its consequence, making enforcement visible. Test: do single-sentence rules with no elaboration produce stronger compliance than explained rules? The hypothesis is that elaboration gives the agent room to interpret, while bare axioms do not.
- STABILITY: formatting (presentation style) + experimental (whether elaboration helps or hurts compliance)

---

## STRUCTURAL: internal_hierarchy

### What the agent needs to understand

Are all critical rules equally critical? Or is there an internal hierarchy? The workspace confinement rule is arguably more fundamental (violation = operating outside the sandbox) than the batch size rule (violation = suboptimal memory management). The output tool exclusivity rule is system-critical (violation = invalid output); the scope limitation rule is quality-critical (violation = expanded scope).

### Fragments

**rule_ordering_strategy**
- Alternative A: No hierarchy — all rules are equally inviolable. Presenting them as equal prevents the agent from deciding some rules are "more critical" and applying selective compliance.
- Alternative B: Explicit hierarchy — system rules first (workspace, output tool), operational rules second (batch size, naming), behavioral rules last (fail fast, scope, invention). The agent sees the most critical rules first.
- Alternative C: Grouped by type — output tool rules as one block, generic rules as another. Groups are unnamed (just separated by whitespace) to avoid implying hierarchy.
- Alternative D: Two tiers: "Operating boundaries" (workspace, output tool — the system cannot function if these are violated) and "Processing discipline" (batch size, fail fast, scope — quality and reliability concerns). The agent understands that the first tier is absolute and the second tier is very strong.
- PURPOSE: Decides whether critical rules form a flat set or a structured hierarchy.
- HYPOTHESIS: Flat presentation (A) is the safest against selective compliance — the agent cannot reason "rule 5 is less critical than rule 1." Explicit hierarchy (B/D) gives the agent a priority system for when rules seem to conflict. Grouped presentation (C) creates thematic coherence without explicit ranking. Test: does flat presentation reduce selective compliance, or does it cause the agent to deprioritize ALL rules because it cannot distinguish which ones are truly inviolable?
- STABILITY: structural — this is an architectural choice about how the section is organized

---

## CROSS-SECTION DEPENDENCIES

### critical_rules.workspace_confinement -> security_boundary.workspace_path
The workspace path value is owned by the security boundary section. The critical rules section needs this value to state the confinement rule. This creates a cross-section data dependency — the template must pull `workspace_path` from `security_boundary` when rendering `critical_rules`.

Design implications:
- The security_boundary section lists allowed paths (positive framing: "you CAN access these")
- The critical_rules section states the prohibition (negative framing: "you CANNOT access anything else")
- Both express the same constraint. The question is whether the duplication reinforces or dilutes. For most agents, reinforcement is the right answer — the same boundary stated in two registers (allowlist + prohibition) is stronger than either alone.

### critical_rules.tool_name -> writing_output.tool_name
The output tool name appears in both sections. writing_output owns the invocation syntax; critical_rules uses the tool name in its exclusivity rule. The tool name must be identical in both sections — any inconsistency would be a system bug.

### critical_rules -> constraints
Several critical rules overlap with constraints. "Stay in scope" is a critical rule; constraints contain "MUST NOT load truth system, canonical entities, or any external knowledge." The overlap is intentional but creates a risk: if the agent recognizes the repetition, it may process both sections in the same (constraint) register, losing the critical rules section's elevated authority.

### critical_rules -> instructions
The fail-fast rule modifies instruction execution — it tells the agent to abort the instruction sequence on unrecoverable error rather than continuing. This means critical rules must be read BEFORE or AS a modifier to instructions. If the agent reads instructions first, it may establish an execution model that does not include fail-fast, and the critical rules section (read later) must override that model.

### critical_rules -> return_format
The fail-fast rule references the FAILURE return format. The agent must know what FAILURE looks like (return_format) to comply with the fail-fast rule (critical_rules). This creates a dependency that is satisfied by section ordering (return_format before critical_rules in the current prompt) but would need to be addressed if critical rules moves to an earlier position.

---

## CONDITIONAL BRANCHES

### Branch 1: has_output_tool = false (agent-builder configuration)

The critical rules section contains ONLY:
- Workspace confinement rule
- Generic rules (fail fast, scope, no invention)

This produces a short, tight section. The section's authority comes from its brevity and directness. For agent-builder, the critical rules are truly universal operating principles — there is no tool-specific discipline to include.

Design consideration: Is this section even necessary for agents without output tools? The workspace confinement rule could live in security_boundary. The generic rules could live in constraints. The section earns its existence only if the "inviolable" register produces different compliance than the "constraint" register. If the framing and positioning of critical rules produces genuinely stronger compliance, then the section is justified even for the short configuration. If not, it should be eliminated for no-output-tool agents to avoid diluting the section's authority for agents that DO need it.

### Branch 2: has_output_tool = true (interview-summary configuration)

The critical rules section contains:
- Workspace confinement rule
- Output tool exclusivity rule (uses tool_name)
- Batch discipline rule (uses batch_size, tool_name)
- Write frequency rule (may be merged with batch discipline)
- File naming rule (conditional on name_needed = true)
- Tool invocation format reference (optional — may be delegated to writing_output)
- Generic rules (fail fast, scope, no invention)

This produces a longer, more complex section. The section needs internal structure to prevent it from becoming an undifferentiated wall of rules. The output-tool rules are operationally specific (tool name, batch size, naming pattern); the generic rules are behavioral principles. These two categories may benefit from visual or structural separation.

### Branch 3: name_needed = true (within has_output_tool = true)

The file naming rule appears only when `name_needed = true`. This is a secondary conditional within the output tool branch. It adds one more rule to an already-long section. The design question is whether it can be absorbed into the output tool exclusivity rule (as part of "use the tool correctly, including the correct filename") or whether it deserves its own rule (because filename errors are a specific, common failure mode).

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### rule_count_awareness
Nothing tells the agent how many critical rules there are. For a 3-rule section (no output tool), the count is self-evident. For a 7-rule section (with output tool), the agent may benefit from knowing the total: "There are 7 inviolable rules. All must be followed." This creates a completion target and prevents the agent from stopping attention mid-section.

**PURPOSE:** Prevents attention degradation in longer rule sets. The agent knows it must process N rules and can track its progress.

**HYPOTHESIS:** For 3-rule sections, a count is unnecessary. For 7+ rule sections, the count may improve attention to later rules. But a count also implies the rules are a list to be checked rather than principles to be internalized. Test: does announcing the rule count improve compliance with later rules in the section?

**STABILITY:** conditional (useful for long sections, unnecessary for short ones) + experimental

### conflict_resolution_directive
What happens when a critical rule conflicts with an instruction step? For example: an instruction step says "produce a summary for each exchange" but the input is malformed after exchange 50. The fail-fast rule says "return FAILURE." The instruction says "produce a summary for each." Which wins?

- Alternative A: `If an instruction conflicts with a critical rule, the critical rule takes precedence. Always.`
- Alternative B: `These rules override your instructions. If you must choose between following an instruction step and following a critical rule, follow the critical rule.`
- Alternative C: Implicit — the section framing already establishes that critical rules are inviolable, so they automatically override.

**PURPOSE:** Prevents the agent from being paralyzed by perceived conflicts between its instructions and its rules. Establishes a clear precedence hierarchy.

**HYPOTHESIS:** This is one of the most common failure modes in dispatched agents — the agent encounters a situation where complying with a rule means deviating from its instructions, and it freezes or invents a compromise. Explicit precedence (A/B) resolves this in advance. Implicit precedence (C) relies on the section framing being strong enough to establish the hierarchy without stating it. Test: does an explicit conflict-resolution directive reduce cases where agents produce degraded output rather than returning FAILURE?

**STABILITY:** experimental — this fragment addresses a specific failure mode that may or may not occur frequently enough to justify its inclusion

### inviolability_through_repetition
One strategy for making rules feel inviolable is to state the most important rules in MULTIPLE sections with consistent phrasing. The workspace confinement rule appears in security_boundary (as allowlist) and could appear in critical_rules (as prohibition). The output tool exclusivity rule appears in writing_output (as invocation syntax) and in critical_rules (as prohibition). This creates a sense of environmental consistency — the rule is not just stated, it is woven into the fabric of the prompt.

**PURPOSE:** Makes rules feel like structural features of the prompt rather than items on a checklist. A rule stated once can be forgotten. A rule stated three times in three contexts feels like a fact about the world.

**HYPOTHESIS:** Repetition has a dual-edged effect. For rules that must be absolute (workspace, output tool), repetition reinforces. For rules that are merely strong preferences, repetition may cause the agent to discount ALL repeated content as "the prompt keeps saying the same thing." The key is selective repetition — only repeat the truly inviolable rules, so the repetition signal means "this is different from other rules." Test: does selective repetition of 2-3 key rules across sections improve compliance with those specific rules?

**STABILITY:** structural — this is a cross-section architectural decision, not a per-section knob

### the_anti-helpfulness_directive
The deepest tension in critical rules is between the agent's training (be helpful, produce output, try to complete the task) and the rules (fail fast, stay in scope, don't invent). Every critical rule is fundamentally an anti-helpfulness directive — it tells the agent that in specific situations, the helpful thing to do is the WRONG thing to do.

This tension is never addressed explicitly. The rules prohibit specific behaviors, but they don't acknowledge that the agent will WANT to violate them because its training says "be helpful." A fragment that explicitly addresses this tension might be more effective than any individual rule:

- Alternative A: `Your training tells you to be helpful. In this context, helpfulness means strict compliance with these rules — not creative workarounds, not partial output, not going beyond scope. The most helpful thing you can do is follow these rules exactly.`
- Alternative B: `Being helpful here means being disciplined. Output that violates these rules is not helpful — it is dangerous. Clean FAILURE is more helpful than contaminated success.`

**PURPOSE:** Directly addresses the root cause of rule violations rather than treating individual symptoms. Most rule violations are not defiance — they are misguided helpfulness.

**HYPOTHESIS:** If the agent understands that compliance IS helpfulness in this context, it may resolve the internal tension between "follow rules" and "be helpful" rather than having them compete. This is an identity-level intervention: it redefines what "helpful" means for this specific task. Test: does an explicit anti-helpfulness reframing reduce all categories of rule violation, or only the ones driven by helpfulness training?

**STABILITY:** experimental — this is a genuinely novel fragment type that directly targets LLM training dynamics
