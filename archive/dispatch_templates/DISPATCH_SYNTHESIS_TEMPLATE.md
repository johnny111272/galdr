# Dispatch Template: A/B Synthesis

## How To Use This Template

For each section, dispatch ONE opus agent with the following prompt structure. Replace all `{PLACEHOLDERS}` with actual values. The agent receives both A and B analysis texts inline and produces a single synthesized document.

---

## Prompt Template

```
STRICT OPERATIONAL CONSTRAINT — READ THIS FIRST:
Your ONLY tool use should be the Write tool to create the output file.
Do NOT read ANY files on disk. Do NOT search or grep the codebase.
Do NOT explore directories. Do NOT use Glob, Grep, or Read tools.
Everything you need is provided inline below.

---

You are synthesizing two independent analyses of the {SECTION_NAME} section
of an agent prompt composition system. Both analyses examined the same raw data
and were given identical instructions. Your job is to produce a single design
document that captures the best of both while being SHORTER than either input.

OUTPUT FILE: Write your synthesis to:
/Users/johnny/.ai/smidja/galdr/agent_control_surfaces/{SECTION_NAME}.md

---

WHAT THIS IS FOR:

We are designing the presentation layer for agent prompts. The data (field values)
is fixed. The behavioral leverage is entirely in the prose fragments, framing,
labels, templates, and structural choices that surround each data value. Two agents
with identical data can perform radically differently based solely on these choices.

These analyses catalog the fragments and their alternatives for one section of the
agent prompt. Your synthesis distills them into a design document.

---

SYNTHESIS RULES:

1. COMPRESS, DO NOT MERGE. The output must be shorter than either input.
   Both analyses are exploratory and verbose. Your job is distillation —
   keep signal, discard redundancy. If both said the same thing in
   different words, say it once in the best words.

2. CONVERGENCE IS SIGNAL. When both analyses independently reached the
   same conclusion, that conclusion has high confidence. Mark it clearly.

3. DIVERGENCE IS ALSO SIGNAL. When one analysis saw something the other
   missed, or they disagreed, that is a design question to preserve.
   Do not resolve it — surface it.

4. CURATE ALTERNATIVES. Each analysis lists 3-6 alternatives per fragment.
   Keep only the 2-3 most distinct and promising. Drop synonyms,
   drop weak alternatives, drop alternatives that both analyses
   implicitly dismissed.

5. EVERY FRAGMENT GETS A STABILITY CLASSIFICATION. This is critical for
   the downstream extraction plan. Classify each fragment as:
   - STRUCTURAL: Rarely changes. Heading text, heading level, section
     presence, divider style. Part of the rendering skeleton.
   - FORMATTING: Sometimes changes. List style, separator type,
     container style, numbering scheme. Display variations.
   - EXPERIMENTAL: Frequently changes. Framing sentences, behavioral
     preambles, mode indicators, identity templates. This is where
     the behavioral leverage lives and where targeted adjustments
     produce the biggest effects.

6. CONDITIONAL BRANCHES MUST BE EXPLICIT. If a fragment changes based
   on agent characteristics (step count, mode distribution, evidence
   type mix, presence/absence of optional data), state the condition
   and what changes.

---

OUTPUT STRUCTURE — Follow this exactly:

# {SECTION_NAME} — Control Surface Synthesis

## Section Purpose
[2-3 paragraphs maximum. What does this section do to the agent's cognition?
State convergent findings as established. Note divergent framings briefly.]

## Fragment Catalog

### {fragment_name}
- CONVERGED: [What both analyses agreed on — stated once, clearly]
- DIVERGED: [Where they disagreed or one saw something the other missed]
- ALTERNATIVES:
  - A: [Best alternative — with brief behavioral rationale]
  - B: [Second best — with brief behavioral rationale]
  - C: [Third if warranted — otherwise omit]
- HYPOTHESIS: [The strongest behavioral hypothesis, synthesized]
- STABILITY: structural | formatting | experimental
- CONDITIONAL: [What agent characteristics trigger variation, or "none"]

[Repeat for each fragment. Include BOTH data-field fragments and structural
fragments (heading, preamble, separators, closers, envelope patterns).]

## Cross-Section Dependencies
[Unified list from both analyses. Each dependency stated once with the
section it connects to and WHY the dependency matters.]

## Conditional Branches
[The major rendering forks this section requires. State each as:
CONDITION → EFFECT. Keep it concrete.]

## Open Design Questions
[Genuine uncertainties. Questions where the analyses diverged without
resolution, or where neither had a clear answer. These are inputs to
the overarching design, not problems to solve here.]

## Key Design Decisions
[The 3-5 most important choices this section requires. State each as
a question with the most promising direction from the analysis.
These feed directly into the extraction plan.]

---

ANALYSIS A:

{PASTE_FULL_TEXT_OF_SECTION_A}

---

ANALYSIS B:

{PASTE_FULL_TEXT_OF_SECTION_B}
```

---

## Dispatch Checklist

Before dispatching:
1. Replace `{SECTION_NAME}` (all occurrences) with the section name in UPPER_CASE
2. Replace `{PASTE_FULL_TEXT_OF_SECTION_A}` with the full contents of `agent_outputs/{SECTION}_A.md`
3. Replace `{PASTE_FULL_TEXT_OF_SECTION_B}` with the full contents of `agent_outputs/{SECTION}_B.md`
4. Use `model: "opus"` for all synthesis dispatches
5. Use `subagent_type: "general-purpose"`
6. Verify the output file path matches: `agent_control_surfaces/{SECTION_NAME}.md`

## After Dispatch

The synthesized document lands in `agent_control_surfaces/{SECTION_NAME}.md`.
Review with the user before proceeding to the next section.
Do NOT dispatch the next section until the current one is reviewed.
