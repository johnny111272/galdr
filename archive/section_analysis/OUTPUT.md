# OUTPUT — Control Surface Synthesis

## Section Purpose

The output section answers: **What am I producing?** It is the agent's mental model of its deliverable as an artifact — shape, location, naming, and structural contract. This is distinct from instructions (what to DO), success/failure criteria (what GOOD/BAD looks like), and writing_output (how to physically write). Output specifies the artifact, not the process.

This is the most heavily conditional section. The `name_known` three-way branch produces fundamentally different section shapes, and the schema presence/embed combination adds another branching axis. A minimal agent gets three fields; a maximal one gets seven-plus with embedded schema content. The conditionality reflects genuine variance in what "output" means across agent types.

The critical boundary: output must never bleed into writing mechanics (tools, batch sizes, write frequency). The connection point is that output establishes format and location; writing_output provides mechanics to realize them.

## Fragment Catalog

### output_section_header
- CONVERGED: Every agent needs a section header. The choice is between agent-addressed and formal styles.
- DIVERGED: No substantive disagreement.
- ALTERNATIVES:
  - A: `"## What You Produce"` — agent-centered, frames section as identity-level knowledge
  - B: `"## Output Specification"` — formal, better for schema-heavy agents
  - C: `"## Output"` — minimal, depends on consistency with other section headers
- HYPOTHESIS: Agent-addressed framing reinforces responsibility, but consistency across sections may matter more than per-section optimization.
- STABILITY: structural
- CONDITIONAL: none

### output_description_frame
- CONVERGED: Description is the conceptual anchor — the "elevator pitch" of the deliverable. It carries structural topology (one file vs. many) and content preview. It is the grounding the agent returns to when deep in processing.
- DIVERGED: A emphasizes description as load-bearing when no schema exists; B frames it as always-primary with schema as override layer. Both valid framings.
- ALTERNATIVES:
  - A: `"You produce: {description}"` — direct, least ambiguous
  - B: `"Your deliverable is {description}."` — noun-definition may produce stronger structural adherence by treating output as fixed specification
- HYPOTHESIS: The verb matters. "Produce" implies manufacturing; "deliverable" implies a handoff to a consumer, which may help agents whose output feeds other agents.
- STABILITY: structural
- CONDITIONAL: none

### output_description_sufficiency_cue
- CONVERGED: When no schema exists, the agent must understand that the description is load-bearing — primary specification, not casual summary.
- DIVERGED: A proposed explicit cue text; B questioned whether silence is sufficient (especially for text format).
- ALTERNATIVES:
  - A: `"No schema governs this output. The description above is your authoritative guide to structure and content."` — makes absence explicit, elevates description
  - B: `"Your output is description-driven, not schema-driven. The description above defines what complete and correct output looks like."` — introduces useful vocabulary
  - C: Render nothing (silence) — may be sufficient for text-format agents
- HYPOTHESIS: Explicit noting helps structured-but-unschemaed agents. Silence is likely correct for freeform text. May need to branch on format value.
- STABILITY: experimental
- CONDITIONAL: schema_path absent; may further condition on format value

### output_format_declaration
- CONVERGED: Simple declaration. Every agent has a format. The fragment is invariant; only the value changes.
- DIVERGED: No substantive disagreement.
- ALTERNATIVES:
  - A: `"Output format: {format}"` — terse, may suffice
  - B: `"You are writing {format} output."` — integrates into agent self-model, fits prose rendering
- HYPOTHESIS: Terse is sufficient because the implications fragment carries the behavioral weight.
- STABILITY: structural
- CONDITIONAL: none

### output_format_implications
- CONVERGED: Format name alone is insufficient. JSONL agents need explicit per-line validity rules. Text agents need to know they have structural freedom. LLMs are notorious for emitting JSON arrays when JSONL is requested.
- DIVERGED: Whether text format needs any implications fragment at all. A includes text implications; B suggests text probably needs none.
- ALTERNATIVES:
  - A (jsonl): `"JSONL means one valid JSON object per line. No multi-line records. No trailing commas. No array wrappers."` — explicit negation blocks common failure modes
  - B (jsonl): `"Each line of your output is an independent JSON object. Lines are separated by newlines. The file is not itself a JSON array."` — positive + one key negation
  - C (text): `"Text output means you control the structure. Organize the content as the task requires."` — grants structural authority
- HYPOTHESIS: For JSONL, explicit negation ("no array wrappers", "no trailing commas") is more effective than positive-only description because it directly blocks the most common failure modes. For text, a brief structural-freedom statement may help but is lower priority.
- STABILITY: formatting (jsonl implications are stable per format; the set of formats may expand)
- CONDITIONAL: varies by format value; text implications may be omittable

### output_directory_frame
- CONVERGED: Declares the filesystem root. Combined with resolved filename, forms complete output path. Must be within security boundary.
- DIVERGED: Whether to include boundary-enforcement language ("must be within this directory or its subdirectories"). A favors it for multi-file agents; B favors it specifically for name_known="unknown" agents. Same instinct, different triggers.
- ALTERNATIVES:
  - A: `"All output files are written under: {output_directory}"` — clear, implies containment
  - B: `"Your output location is {output_directory}. All files you create must be within this directory or its subdirectories."` — explicit boundary enforcement for high-autonomy agents
  - C: `"Output directory: {output_directory}"` — minimal, for constrained agents
- HYPOTHESIS: Boundary-enforcement language matters for name_known="unknown" agents (high autonomy). Minimal declaration suffices for "partially"/"known". The frame should adapt to the naming branch.
- STABILITY: structural
- CONDITIONAL: framing intensity may vary with name_known value

### output_naming_branch_unknown
- CONVERGED: Agent has naming authority. Must understand this is a judgment act, not an unresolved ambiguity. The name_instruction content is consumed inline.
- DIVERGED: Minor framing preference. Both agree on signaling "you decide" + providing policy.
- ALTERNATIVES:
  - A: `"The output filename is not predetermined — you must derive it from the task context. Naming guidance: {name_instruction}"` — explains WHY the agent is naming, frames instruction as guidance
  - B: `"Output naming is your responsibility. Follow this convention: {name_instruction}"` — more directive, better for agents that should not get creative
- HYPOTHESIS: The "not predetermined" framing pre-empts agents that default to asking for clarification. Making filename determination an explicit job responsibility prevents stalling.
- STABILITY: formatting
- CONDITIONAL: name_known = "unknown"

### output_naming_branch_partial
- CONVERGED: Agent fills a template — substitution, not invention. Must understand placeholders are not literal.
- DIVERGED: Whether to explicitly enumerate placeholder names (B proposes it, A does not). Enumeration requires rendering-time computation.
- ALTERNATIVES:
  - A: `"Your output filename follows the pattern {name_template}. Fill in the bracketed placeholders using the corresponding values from your input data."` — explicit about bracket semantics
  - B: `"Output filename follows this template: {name_template}. Replace placeholders with values from your input context."` — slightly more terse
- HYPOTHESIS: Being explicit about what placeholders mean reduces the risk of agents treating part of the literal filename as a placeholder. Placeholder enumeration would help further but adds rendering complexity.
- STABILITY: formatting
- CONDITIONAL: name_known = "partially"

### output_naming_branch_known
- CONVERGED: Simplest branch. Fixed filename, zero agent autonomy. Not observed in current data but implied by the enum.
- DIVERGED: No disagreement.
- ALTERNATIVES:
  - A: `"Output filename: {name_literal}. Write to exactly this file."` — minimal and sufficient
  - B: `"Write to: {name_literal}. This filename is exact and must not be modified."` — anti-template clarification
- HYPOTHESIS: Minimal framing is appropriate. Over-explaining a fixed filename wastes tokens. The "not a template" clarification (B) has value only if agents frequently encounter template examples.
- STABILITY: structural
- CONDITIONAL: name_known = "known" (hypothesized, not in current data)

### output_schema_embedded_header
- CONVERGED: When schema is embedded, frame it as authoritative and non-negotiable before rendering the JSON content.
- DIVERGED: How much interpretive guidance to add around raw schema. A keeps it brief; B considers adding field-level reinforcement ("every required field must be present") but flags it as potentially redundant.
- ALTERNATIVES:
  - A: `"The following JSON Schema defines your output structure. Every record you produce must validate against it."` — names the thing, states the constraint
  - B: `"Output schema (authoritative — all records must match):\n\n{schema_content}"` — terse, treats schema as self-explanatory
- HYPOTHESIS: LLMs sometimes treat embedded JSON as informational rather than normative. Minimal but explicit constraint language ("must validate against it") is necessary. Post-schema interpretive guidance is likely redundant — the schema speaks for itself.
- STABILITY: formatting
- CONDITIONAL: schema_path present AND schema_embed = true

### output_schema_reference
- CONVERGED: When schema is not embedded, the agent gets only the path. Must be told to actually read the schema file.
- DIVERGED: Strength of the "read this" directive. Both agree it is needed; B pushes harder ("you MUST read").
- ALTERNATIVES:
  - A: `"Your output must conform to the JSON Schema at {schema_path}. Read this schema to understand the required structure."` — directive but not shouting
  - B: `"Schema reference: {schema_path}. You MUST read this schema and conform your output to it."` — imperative, blocks the skip-and-guess failure mode
- HYPOTHESIS: Without embedding, there is real risk the agent skips reading the schema and works from description alone. Imperative language is justified here — this is a known failure mode, not hypothetical.
- STABILITY: formatting
- CONDITIONAL: schema_path present AND (schema_embed = false OR absent)

## Cross-Section Dependencies

| Output Field | Depends On | Nature |
|---|---|---|
| output_directory | security_boundary.workspace_path | Must be within permitted write zone (build-time validation) |
| name_instruction | output_directory | Paths in instruction are relative to directory |
| name_template placeholders | Input section fields | Placeholder values come from input context |
| schema_path | Schema files on disk | Must exist at path for validation and embedding |
| format | writing_output section | Format determines applicable writing mechanics (append vs. write-once) |
| output_directory + resolved name | writing_output.tool_invocation | Writing tool must target the computed path |
| description | schema (when both exist) | Schema is authoritative for structure; description provides semantic context schema cannot carry |
| schema compliance | success/failure criteria | Criteria should reference "the schema defined in output" rather than re-specify the path |

## Conditional Branches

```
ALWAYS PRESENT:
  description, format, output_directory, name_known

BRANCH 1 — name_known:
  "unknown"   → name_instruction (required) + high-autonomy directory framing
  "partially" → name_template (required) + substitution framing
  "known"     → name_literal (required, hypothesized) + minimal framing

BRANCH 2 — schema:
  schema_path present + schema_embed=true  → schema_embedded_header + schema content
  schema_path present + schema_embed=false → schema_reference (with read directive)
  schema_path absent                       → description_sufficiency_cue (or silence)

ASSEMBLY ORDER:
  1. output_section_header
  2. output_description_frame
  3. output_format_declaration + output_format_implications
  4. output_directory_frame (framing intensity adapts to name_known)
  5. output_naming_branch_{name_known}
  6. schema branch OR description_sufficiency_cue
```

## Open Design Questions

1. **Multi-file outputs overloading name_instruction.** Agent 1's name_instruction specifies two output paths in different subdirectories. Is name_instruction the right place for file topology, or should there be an explicit multi-file structure field? Both analyses flagged this independently.

2. **Should description_sufficiency_cue condition on format?** Silence may be correct for text-format agents. Explicit cue may help structured-but-unschemaed agents. This fragment's very existence is unresolved.

3. **Format enum expansion.** Current data shows text/jsonl. If json, toml, csv, or markdown appear, each needs its own implications fragment. The rendering logic needs format-specific knowledge.

4. **name_known="known" is hypothetical.** Neither observed agent uses it. Real data would confirm or revise the inferred fragments.

5. **Schema embedding token cost at batch scale.** For agents processing hundreds of items, embedded schema multiplies cost. Is a middle ground viable (embed schema summary, reference for full)?

6. **Specification vs. description framing adaptation.** Should the section's overall tone shift from "description" (informative, guiding) to "specification" (formal, constraining) based on schema presence? Both analyses noted this tension from different angles.

## Key Design Decisions

1. **Output vs. writing_output boundary is load-bearing.** Output specifies the artifact; writing_output specifies mechanics. Output never mentions tools, batch sizes, or write frequency. This boundary was independently identified and reinforced by both analyses.

2. **Assembly order is convergent.** Both analyses independently derived the same zoom-in sequence: concept (description) -> format -> location (directory) -> name (branched) -> structure (schema). This ordering is high-confidence.

3. **schema_embed is a rendering directive, not an agent-facing field.** The agent never sees this boolean — it experiences the result (inline schema or path reference). Both analyses agreed.

4. **JSONL implications require explicit negation.** Both analyses independently identified the same failure mode (LLMs emitting JSON arrays instead of JSONL) and the same mitigation (explicit "no array wrappers" language). High-confidence design decision.

5. **Directory framing should adapt to naming autonomy.** Both analyses noted that name_known="unknown" agents need boundary-enforcement language in the directory fragment, while constrained agents do not. The output_directory_frame is the one fragment whose intensity should vary with name_known.
