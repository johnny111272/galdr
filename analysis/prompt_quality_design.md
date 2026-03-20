# Prompt Quality Design

Analysis of what the current renderer wastes, what the data makes possible, and concrete proposals for how each section could be rendered to produce meaningfully better agent prompts — with before/after examples and benchmarkable variant axes.

---

## Framing

The current output treats the agent prompt as a reference document. Sections have headings, content is listed, labels are bolded. An agent scanning this prompt sees what a human would see reading documentation.

That is the wrong target. An agent prompt is behavioral programming. Every sentence either shapes what the agent does or it does not. The question for every section is: does this presentation make the agent more likely to do the right thing?

The data model is richer than the output. What follows is an analysis by section of what's being left on the table.

---

## 1. Instruction Mode — currently dropped entirely

### What the data provides

Each step has `instruction_mode`: either `"deterministic"` or `"probabilistic"`. The data is fully typed. The current renderer discards this entirely — all steps render as sequential paragraphs with no differentiation.

### What the agent loses

An agent reading the current output cannot distinguish "this is a strict rule with zero latitude" from "this is where you apply judgment." Both look identical. This is a significant compliance risk: a deterministic step treated as probabilistic will produce variation; a probabilistic step treated as deterministic will produce over-rigid behavior.

### What the data makes possible

The mode boundary is the primary signal that controls agent compliance on each step. There are at least four presentation approaches worth benchmarking:

**Variant A: Inline mode tag (concise)**
```
1. [DETERMINISTIC] Read the input tempfile. Each line is a JSON object with fields...

2. [PROBABILISTIC] For each exchange, write one sentence that captures what this exchange signifies...
```

**Variant B: Typographic gating (visual)**
```
═══ STEP 1 — FOLLOW EXACTLY ═══
Read the input tempfile. Each line is a JSON object with fields: exchange (integer), agent (string), user (string). Process exchanges in order, first to last.

--- Step 2 — Use judgment ---
For each exchange, write one sentence that captures what this exchange signifies given everything that came before it.
```

**Variant C: Grouped by mode (structural)**
```
## Fixed Steps (execute as written)

1. Read the input tempfile...
3. Each summary is exactly one sentence...

## Judgment Steps (apply expertise)

2. For each exchange, write one sentence...
4. Session transitions...
5. Decontamination...
```

**Variant D: Margin marker (minimal)**
```
→ Read the input tempfile...
~ For each exchange, write one sentence...
→ Each summary is exactly one sentence...
~ Session transitions...
~ Decontamination...
```
Where `→` = deterministic (follow as written), `~` = probabilistic (apply judgment)

### Primary benchmark question

Does showing instruction_mode boundaries in the rendered prompt increase compliance on deterministic steps without reducing appropriate flexibility on probabilistic ones? Variants A and D preserve step ordering; C inverts it. A/B/D all allow natural reading flow.

**Recommended investigation:** Variant A (tagged, numbered) vs current (no tags). Clear and low-risk first test.

---

## 2. Critical Rules — currently a numbered list with no conditional logic

### What the data provides

`critical_rules` has structured fields: `has_output_tool` (boolean), `tool_name` (string), `batch_size` (integer), `name_needed` (boolean), `workspace_path` (string). The rendered rules are derived from these fields — each rule is generated from typed data.

The current renderer produces a numbered list. The list items are prose sentences generated from the structured fields. Each item gets a bolded lead phrase. The list is at the bottom of the document.

### What the current output loses

**Position:** Critical rules are at the end. Agents scanning forward read them last. If these are the highest-compliance-requirement rules, they may be more effective at the top or immediately before the section they govern (output tool rule before the output section, for example).

**Style tone:** The current style is neutral. `"Fail fast — if something is wrong, FAILURE immediately with clear reason"` is correct but mild. The data supports generating this at significantly different tonal levels.

### Tone variants worth benchmarking

**Current (neutral):**
```
1. **Use append_interview_summaries_record for all output** — never write files directly, never use a different write tool
2. **Batch discipline** — process exactly 20 records per batch (last batch may be smaller)
```

**Stern:**
```
RULE 1 — OUTPUT TOOL IS MANDATORY
You MUST use `append_interview_summaries_record` for ALL output. Writing files directly or using any other tool is a violation that terminates the task. No exceptions.

RULE 2 — BATCH DISCIPLINE IS NON-NEGOTIABLE
Process exactly 20 records per batch. Do not accumulate records. Write after every batch. The last batch may be smaller.
```

**Collaborative:**
```
To produce valid output, this agent writes through a validated tool:
- Use `append_interview_summaries_record` — this ensures schema validation and correct JSONL format
- Write in batches of 20 — this prevents memory accumulation and ensures partial progress survives failure
```

**Concise:**
```
Output: `append_interview_summaries_record` only. Batch: 20. Fail fast.
```

### Conditional rule generation

The data distinguishes `has_output_tool = true` from `has_output_tool = false`. When false (agent-builder), the output tool rules disappear and only the generic rules remain. When true (interview-enrich-create-summary), output tool, batch, and name rules appear.

The style controls what prose wraps each conditional rule. A stern style generates MUST-capital language. A collaborative style generates rationale. This is exactly the axis that should be benchmarked: does a stern tone on critical rules improve compliance vs. a collaborative tone?

### Placement variant

The current output puts critical rules last. An alternative worth testing: place output-tool and batch rules immediately after the output section, where the agent is thinking about writing output. Placement at point-of-use may outperform placement at end-of-document.

---

## 3. Security Boundary — currently a flat inverted-label list

### What the data provides

```
workspace_path = "/Users/johnny/.ai/spaces/bragi"
display[n].path = "./definitions/agents/agent-template.toml"
display[n].tools = ["Glob", "Grep", "Read", "find"]
```

The data has: a workspace root, relative paths from that root, and tool sets per path. The current output uses tools as bold labels and path as value — an inverted format. The workspace_path is not rendered at all.

### Problems with the current format

The current output:
```
**Glob, Grep, Read, find:** `./definitions/agents/agent-template.toml`
**Glob, Grep, Read, find:** `./definitions/audit/`
```

This makes tools the primary label and path the secondary value. To scan what paths are accessible, the agent must read past the repeated tools lists. When many paths share the same tool set, the repetition adds noise.

The workspace path is data that anchors all relative paths. Not rendering it means the agent cannot resolve `./definitions/` to an absolute path without inference.

### Proposed variants

**Variant A: Table format (scannable)**
```
## Security Boundary

Workspace: `/Users/johnny/.ai/spaces/bragi`
All paths below are relative to workspace. Access is restricted to these entries.

| Path | Allowed Tools |
|------|---------------|
| `./definitions/agents/agent-template.toml` | Glob, Grep, Read, find |
| `./definitions/audit/` | Glob, Grep, Read, find |
| `./definitions/prompts/` | Glob, Grep, Read, find |
| `./definitions/staging/` | Glob, Grep, Read, find |
| `./interview/` | Glob, Grep, Read, find |
| `./schemas/` | Glob, Grep, Read, find |
| `./truth/` | Glob, Grep, Read, find |
```

**Variant B: Path-first bulleted (compact)**
```
## Security Boundary

Workspace root: `/Users/johnny/.ai/spaces/bragi`

Allowed paths (Glob, Grep, Read, find):
- `./definitions/agents/agent-template.toml`
- `./definitions/audit/`
- `./definitions/prompts/`
- `./definitions/staging/`
- `./interview/`
- `./schemas/`
- `./truth/`
```
This variant exploits path grouping: when multiple paths share the same tool set, the tools label appears once for the group, not once per entry.

**Variant C: Current format but with workspace**
```
Workspace: `/Users/johnny/.ai/spaces/bragi`
**Glob, Grep, Read, find:** `./definitions/agents/agent-template.toml`
...
```

### Tool differentiation

The current output renders `Glob, Grep, Read, find` as a flat list. But `find` is a Bash command, not a Claude Code tool. A style variant could visually distinguish them:
- `Glob Grep Read` + `(bash: find)`
- `Read·Grep·Glob·find` where `find` is styled differently

### Benchmark question

Does rendering the workspace_path and anchoring relative paths to it reduce agent path errors (attempting to access paths outside the boundary)?

---

## 4. Examples — currently H2 > H3 > H4 flat text

### What the data provides

```
[[examples.groups]]
example_group_name = "Contextual Summaries"
example_display_headings = true

[[examples.groups.example_entries]]
example_heading = "Standard substantive exchange"
example_text = "..."
```

The data has: groups (named categories), entries (named examples), and a heading display flag. Each entry text is free-form markdown containing good/bad/why patterns in some cases, plain demonstrations in others.

### Problems with the current format

**Hierarchy problem:** H2 (Examples) > H3 (group name) > H4 (example heading) is three heading levels. In a document where the agent is reading for operational guidance, four-level nesting is visually noisy and makes examples feel buried.

**Heading level problem:** H4 is the entry heading. H4 renders in markdown as text that barely stands out from the surrounding content. Entry titles like "Thin content with rich context" disappear into the flow.

**Good/bad/why is unstructured:** The example text contains patterns like `GOOD summary:` and `BAD summary:` and `WHY:` written as prose. These are structurally meaningful distinctions that the renderer treats as raw text. A style could render these with visual differentiation.

### Display variants worth benchmarking

**Variant A: Collapsible-style with prominent titles (structural)**
```
## Examples

### Contextual Summaries

---

**Thin content with rich context**

Exchange 16 user text: "You would understand why."
(25 characters, after several exchanges debating what understanding means)

GOOD: "User states that actual understanding of something like boundary security insight would mean understanding why it exists, not just being able to describe what it is."

BAD: "User makes a brief comment."

WHY: The text is 5 words, but the preceding exchanges built toward a distinction between surface description and genuine understanding.

---
```
Horizontal rules between entries make each example a discrete block. The entry title is H3 (not H4), making it scannable.

**Variant B: Labeled blocks (semantic)**
```
EXAMPLE: Thin content with rich context

INPUT
Exchange 16 user text: "You would understand why."
(25 characters, after several exchanges debating what understanding means)

CORRECT OUTPUT
"User states that actual understanding of something like boundary security insight..."

INCORRECT OUTPUT
"User makes a brief comment."

REASON
The text is 5 words, but preceding exchanges built toward a distinction...
```
This makes the GOOD/BAD/WHY structure explicit and machine-readable rather than embedded prose labels.

**Variant C: Side-by-side contrast (compact)**
```
**Thin content with rich context**

| | |
|---|---|
| Input | "You would understand why." (5 words, after lengthy debate about understanding) |
| Correct | "User states that actual understanding means knowing why, not just describing what." |
| Incorrect | "User makes a brief comment." |
| Why | Preceding context gives "You would understand why" its weight. |
```

**Variant D: No group headings (flat)**
When `example_display_headings = false`, the group name disappears entirely and entries render sequentially. This is a recipe-level flag that already exists in the data — the style needs to honor it.

### Benchmark question

Does a more structured example format (labeled blocks) improve agent accuracy on the calibrated task vs. the current H4-and-prose format? Does example prominence (early in document vs. late) change agent behavior?

---

## 5. Success and Failure Criteria — currently definition + evidence bullets

### What the data provides

```
[[success_criteria.criteria]]
success_definition = "Every input exchange has been contextually summarized..."
success_evidence = [
    "Output record count equals input record count.",
    "Every exchange number in the input appears exactly once in the output.",
    ...
]
```

The data has: a definition (prose summary of the criterion) and evidence (a list of verifiable conditions). The current renderer produces: definition as a paragraph, evidence as a bulleted list.

### What the current output loses

**Evidence is passive.** Evidence items are stated as facts about correct output ("Output record count equals input record count"). They read as descriptions, not self-check instructions. An agent that fails to check these won't notice.

**Definition and evidence are separated visually.** The definition paragraph appears, then "Evidence:" as a label, then the list. An agent scanning for success signals reads the definition and may not read the evidence. The definition is often too abstract; the evidence is what matters operationally.

**No severity differentiation.** All success items are equal. In practice, some evidence items are necessary conditions (count must match) and others are quality signals (thin-context exchanges have rich summaries). The current format does not reflect this distinction.

### Proposed variants

**Variant A: Self-check checklist**
```
## Success

Before returning SUCCESS, verify each condition:

- [ ] Output record count equals input record count
- [ ] Every exchange number appears exactly once in output
- [ ] Every summary is a single sentence capturing contextual significance
- [ ] No source quality markers appear in any output record
- [ ] Thin-content-rich-context exchanges reflect accumulated conversational significance
```
Checkbox formatting signals these are not descriptions — they are things to check. This transforms evidence from passive observation into active verification.

**Variant B: Conditional gate format**
```
## Return Conditions

SUCCESS requires ALL of the following:
1. Output record count equals input record count
2. Every exchange number in the input appears exactly once in the output
3. Every summary is a single sentence capturing contextual significance
4. No source quality markers appear in any output record
5. Thin-content-rich-context exchanges have summaries reflecting accumulated significance

FAILURE is triggered by ANY of the following:
1. Any exchange skipped without a summary being written
2. Output record count does not match input record count
3. Input tempfile could not be read or parsed as JSONL
4. Schema validation failure not resolved after retry
```
Unifying success and failure under "return conditions" with AND/ANY framing makes the logic explicit. The agent sees: ALL success gates must clear; ANY failure gate triggers FAILURE.

**Variant C: Severity-weighted (critical/required/quality)**
```
## Success Criteria

CRITICAL (must pass or FAILURE):
- Output record count equals input record count
- Every exchange number appears exactly once in output

REQUIRED:
- Every summary is a single sentence capturing contextual significance
- No source quality markers appear in any output record

QUALITY:
- Thin-content-rich-context exchanges reflect accumulated conversational significance
```
This variant requires adding severity metadata to the data model — it is not currently typed. However, it could be derived from cross-referencing success criteria against failure criteria: anything that appears in both (success version and failure version) is CRITICAL.

### Benchmark question

Does checklist formatting increase the rate at which agents correctly self-verify before returning status? Does conditional gate framing (ALL/ANY) improve compliance vs. the current passive-evidence format?

---

## 6. Overall Structure — section ordering, separators, scanability

### Current ordering (agent-builder)

```
Identity → Security Boundary → Input → Processing → Examples → Output → Constraints → Anti-Patterns → Success → Failure → Return Format → Critical Rules
```

### Problems with current ordering

**Processing (instructions) is in the middle.** The agent reads identity and security boundary before it reads what it's supposed to do. Security boundary is important to the hook system — but does the agent need to know about it before it understands its task? The boundary doesn't change what the agent does; it constrains where it reads from.

**Critical rules are last.** For agents with output tools, the most compliance-critical rules are at the end of a potentially long document. An agent that fails partway through may not have processed these rules into its behavioral state.

**Constraints and anti-patterns are split from instructions.** The current format separates how to do the work (instructions/processing) from the guardrails on how to do it (constraints/anti-patterns). An alternative: render constraints and anti-patterns adjacent to the instructions they govern, rather than at the end.

**No structural hierarchy signal.** The document uses `---` separators between most sections but headings are a mix of H1 (identity), H2 (most sections), and H3/H4 (subsections). There is no visual language that says "this is a tier-1 section" vs "this is operational detail."

### Proposed orderings

**Ordering A: Mission-first**
```
1. Identity (who you are)
2. Critical Rules (highest-compliance requirements — seen early)
3. Input (what you receive)
4. Instructions (what to do, with modes visible)
5. Output (what you produce)
6. Examples (calibration)
7. Success/Failure Criteria (return conditions)
8. Security Boundary (access constraints)
9. Constraints + Anti-Patterns (behavioral guardrails)
10. Return Format
```
Rationale: An agent reading this sees its identity, the non-negotiable rules, its input, its task, and its output before any calibration examples or guardrails. Critical rules are page 2, not page last.

**Ordering B: Operational-first**
```
1. Identity (who you are, very compact)
2. Input (what you receive)
3. Instructions (what to do)
4. Output (what you produce)
5. Writing Output (mandatory invocation if has_output_tool)
6. Critical Rules (immediately after output)
7. Examples
8. Success/Failure
9. Security Boundary
10. Constraints/Anti-Patterns
11. Return Format
```
Rationale: Critical rules appear immediately after the output section where they're operationally relevant. Output-tool rules at point of use.

**Ordering C: Current order, minor fix**
Move Critical Rules to position 3 (after identity and before security boundary). Everything else stays. Minimum intervention, testable.

### Separator discipline

The current output uses `---` (horizontal rule) as a universal separator between all sections. This produces visual uniformity but no hierarchy. A display variant could use different separators:

- Double `---\n---` between major sections (identity, instructions, output)
- Single `---` between minor sections (constraints, anti-patterns)
- No separator between paired sections (constraints + anti-patterns together)

### Compact identity

The identity section currently renders 5 paragraphs. A compact variant renders it in fewer lines:

**Current:**
```
# Agent Builder

**Purpose:** Creates new agent TOML definitions...

You are a definition author.

You create agent definitions from requirements...

**Your responsibility:** Read the preparation package...

**Expertise:** agent definition architecture, domain knowledge extraction...
```

**Compact:**
```
# Agent Builder — definition author

Creates new agent TOML definitions and include files from requirements and preparation packages.

You translate domain knowledge into structured TOML fields, bland instruction steps, and boringly correct calibration examples. Every field has a purpose, every instruction step captures one judgment task.

Expertise: agent definition architecture, domain knowledge extraction, calibration example design, minimum permission security modeling
```

Compact identity saves vertical space and gets the agent to operational content faster. Whether this improves or degrades behavior is an empirical question — a benchmark axis.

---

## 7. Instructions Section — the highest-value redesign opportunity

The instructions section is currently called "Processing" and renders all steps as sequential paragraphs with no structural differentiation. This is the most critical section to redesign because it programs the agent's core behavior.

### What the data provides

```
[[instructions.steps]]
instruction_mode = "deterministic"
instruction_text = "Read the input tempfile. Each line is..."

[[instructions.steps]]
instruction_mode = "probabilistic"
instruction_text = "For each exchange, write one sentence..."
```

Each step has: mode (deterministic/probabilistic) and text. The data is clean. The renderer flattens it.

### Before (current)

```
## Processing

Read the input tempfile. Each line is a JSON object with fields: exchange (integer), agent (string), user (string). Process exchanges in order, first to last. Produce one output record per input record with fields: exchange (integer), summary (string).

For each exchange, write one sentence that captures what this exchange signifies given everything that came before it...
```

Steps are indistinguishable paragraphs. No numbering, no mode signal, no visual boundary between steps.

### After (proposed — numbered + mode-tagged)

```
## Instructions

**Step 1 — Execute exactly** `[deterministic]`
Read the input tempfile. Each line is a JSON object with fields: exchange (integer), agent (string), user (string). Process exchanges in order, first to last. Produce one output record per input record with fields: exchange (integer), summary (string).

**Step 2 — Apply judgment** `[probabilistic]`
For each exchange, write one sentence that captures what this exchange signifies given everything that came before it. The meaning of an exchange is a logical continuation of the earlier exchanges...

**Step 3 — Execute exactly** `[deterministic]`
Each summary is exactly one sentence. The sentence can be long and compound, but it must be syntactically one sentence. No two-sentence summaries. No bullet points. No fragments.

**Step 4 — Apply judgment** `[probabilistic]`
Session transitions — when an exchange contains recap or re-establishment of prior topics...

**Step 5 — Apply judgment** `[probabilistic]`
Decontamination: source quality markers...
```

### Additional display variants for instructions

**Variant: Deterministic steps as blockquotes**
```
> **STEP 1**
> Read the input tempfile. Each line is a JSON object...
> Process exchanges in order, first to last.

**STEP 2** _(use judgment)_
For each exchange, write one sentence...
```

**Variant: Separate processing phases with visual breaks**
```
═══ PHASE 1: READ AND VALIDATE ═══

Read the input tempfile...

════════════════════════════════

PHASE 2: SUMMARIZE (repeat per exchange)

For each exchange...

════════════════════════════════

PHASE 3: WRITE OUTPUT

Each summary is exactly one sentence...
```

### Benchmark question

Does numbering instruction steps improve sequential compliance? Does the mode tag ("execute exactly" vs "apply judgment") reduce over-rigid behavior on probabilistic steps while improving compliance on deterministic steps?

---

## 8. Constraints and Anti-Patterns — currently buried, currently separated

### What the data provides

Two separate arrays: `constraints.rules` and `anti_patterns.patterns`. Both are string lists. The current output renders them as `### Constraints` and `### Anti-Patterns` subsections, under H3 headings, at the bottom of the document.

### Problems

**H3 headings are visually weak.** In the current document, constraints and anti-patterns appear under headings that are one level below the main sections. They read as appendices.

**Separation is artificial.** Constraints say what to do ("MUST process exchanges in order"); anti-patterns say what not to do ("Do not classify importance"). These are two sides of the same guardrail coin. Separating them forces the agent to read two sections to understand the behavioral boundary.

**MUST prefix is inconsistent.** Some constraint items start with "MUST" or "MUST NOT"; others start with "Use" or "Produce." The typographic signal (MUST) carries compliance weight that should be consistent.

### Proposed variants

**Variant A: Unified guardrails section**
```
## Guardrails

**Always:**
- Process exchanges in order — never skip, never reorder
- Produce exactly one sentence per exchange
- Match output record count to input record count exactly
- Use hedging language for reconstructed exchanges

**Never:**
- Reference or load learned, threads, insight, or fields beyond exchange, agent, user
- Load truth system, canonical entities, or any external knowledge
- Output any source quality markers in any record
- Classify importance — summarize what the exchange signifies, not how important it is
- Take reconstructed text at face value — deflate headline-like formulations
```
Unifying always/never under one section makes the guardrail space legible as a single object.

**Variant B: MUST / MUST NOT with consistent formatting**
```
## Constraints

MUST:
- Process exchanges in order
- Produce exactly one sentence per exchange
- Produce exactly as many output records as input records
- Use hedging language for reconstructed exchanges

MUST NOT:
- Reference or load learned, threads, insight fields
- Load truth system, canonical entities, external knowledge
- Output any source quality markers
- Take reconstructed text at face value
- Classify importance — summarize significance, not importance
```
This preserves the current constraint style but makes MUST/MUST NOT explicit and visual rather than embedded in prose.

**Variant C: Inline with instructions (per-step guardrails)**
For agents where guardrails map clearly to specific instruction steps, a style could append relevant guardrails to each step rather than separating them into a section. This is the highest-integration approach and the hardest to implement, but potentially the most effective.

---

## Summary: Benchmarkable Variant Matrix

The following axes represent independent, testable variations. Each can be varied independently against a fixed agent definition:

| Axis | Variants |
|------|----------|
| Instruction mode display | none (current) / inline tag / grouped-by-mode / margin marker |
| Critical rules position | end (current) / after output / beginning (post-identity) |
| Critical rules tone | neutral (current) / stern (MUST-capital) / collaborative (with rationale) / concise |
| Security boundary format | inverted-label (current) / table / path-first-bulleted |
| Security boundary workspace | omitted (current) / rendered as anchor |
| Example hierarchy | H4 prose (current) / H3 with separators / labeled blocks / side-by-side contrast |
| Success/failure format | definition + evidence (current) / checklist / conditional gates (ALL/ANY) |
| Section ordering | current / mission-first / operational-first |
| Identity compactness | full (current) / compact |
| Constraints/anti-patterns | separated (current) / unified guardrails / MUST/MUST-NOT |

Any combination of these is a valid benchmark configuration. The total matrix is large; the highest-value first tests are:

1. **Instruction mode tags vs. none** — directly tests whether mode visibility improves step-level compliance
2. **Critical rules position: end vs. after-output** — directly tests whether point-of-use placement improves output discipline
3. **Critical rules tone: neutral vs. stern** — directly tests whether authoritative framing changes behavior
4. **Success/failure: evidence vs. checklist** — directly tests whether active verification framing changes self-check behavior

These four axes, against two agents with different characteristics (agent-builder without output tool, interview-enrich-create-summary with output tool), produce 2^4 × 2 = 32 prompts to test before exploring the full matrix.
