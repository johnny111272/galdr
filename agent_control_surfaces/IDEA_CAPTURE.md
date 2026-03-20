# Idea Capture: Agent Control Surface Design

Running collection of ideas, intuitions, and observations that emerge during the analysis phase. Not conclusions — seeds.

---

## instruction_mode subcategories

**Source:** User intuition confirmed by INSTRUCTIONS A/B analysis convergence

The current instruction_mode is binary: `deterministic` or `probabilistic`. Both agents independently identified this as critically important and currently invisible (dropped by renderer).

But binary may be too coarse. The probabilistic side especially covers very different cognitive tasks:

- `PROBABILISTIC: summarizing` — compress meaning, preserve significance
- `PROBABILISTIC: synthesis` — combine inputs into new structure
- `PROBABILISTIC: assessment` — evaluate against criteria, render judgment

These are genuinely different cognitive operations. An LLM in "summarizing" mode processes differently than one in "assessment" mode. Making the subcategory visible could:

1. Pre-configure the specific cognitive operation before the instruction text arrives
2. Help the agent switch gears between steps that require different kinds of thinking
3. Give the template system a finer-grained control surface for per-step framing

The deterministic side might also benefit from subcategories, though the need is less obvious since deterministic steps have less behavioral variance by definition.

**Open questions:**
- Where do the subcategory labels come from? Fixed enum? Free text? Definition-author choice?
- Does the subcategory belong in the data model (new field) or in the presentation layer (inferred from instruction text)?
- What's the interaction between instruction_mode subcategory and the task_mode_primer fragment both IDENTITY agents independently proposed?

---

## context_required purpose annotations

**Source:** INPUT synthesis — surfaced by Agent A, confirmed as promising during synthesis review

The current `context_required` entries are (label, path) pairs. Labels like "Bland Is Correct" are evocative but not explanatory — the agent knows what to read but not WHY it's on the reading list or what to extract from it.

Adding a `purpose` field per context entry would let the definition author direct reading attention:

```toml
[[input.context_required]]
context_label = "Bland Is Correct"
context_path = "/path/to/bland_is_correct.md"
purpose = "the quality standard for your writing style"
```

Rendered as: `- **Bland Is Correct** — the quality standard for your writing style: Read \`/path/...\``

**Why this matters:** Context documents are prerequisite knowledge, not reference material. A purpose annotation transforms "read this file" into "read this file to learn X" — which may significantly improve knowledge extraction and application during execution.

**Implementation:** Simple schema addition — one optional string field on context entries. Easy to add, easy to populate, backward-compatible (absent = render without annotation).

**Risk:** Purpose annotations could narrow the agent's reading, causing it to extract only what the annotation says rather than absorbing the full document. Needs testing.
