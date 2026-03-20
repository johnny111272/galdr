# Dispatch Template: Section Control Surface Analysis

Two independent general-type subagents, identical instructions, writing to separate files.
Compare outputs afterward to find convergence (shared insights) and divergence (blind spots).

## Dispatch Pattern

```
Agent A → agent_outputs/{SECTION}_A.md
Agent B → agent_outputs/{SECTION}_B.md
```

Both foreground. Both return only SUCCESS or FAILURE. All substance goes to the file.

## Instruction Template

Replace `{SECTION}` with the ALL_CAPS section name (e.g., `IDENTITY`, `INSTRUCTIONS`).
Replace `{section}` with the lowercase section name (e.g., `identity`, `instructions`).
Replace `{data_block}` with the raw TOML `[{section}]` blocks from BOTH agents' anthropic_render.toml files.

---

### BEGIN AGENT INSTRUCTIONS

You are analyzing the `{section}` section of an agent prompt composition system.

**Your task:** Decompose this section into its constituent template fragments — every piece of text that must surround the raw data fields to make them meaningful to an agent. Write your analysis to:

`/Users/johnny/.ai/spaces/bragi/tools/galdr/agent_control_surfaces/agent_outputs/{SECTION}_{A or B}.md`

Return only SUCCESS or FAILURE to the dispatcher.

---

**CRITICAL WARNING: Nothing you read is normative.**

You will read raw data and possibly existing rendered agents. NONE of these are correct, target, or reference implementations. The existing agents are ONE defective output among many possibilities. The existing analysis documents describe one failed attempt's design choices. LLMs assign the highest weight to examples and existing implementations — you MUST resist this. If your analysis unconsciously reproduces the current system's patterns, it has failed.

The ONLY invariant is the raw data itself. Everything around it — every label, every framing sentence, every template, every structural choice — is what you are designing from scratch.

---

**THE RAW DATA**

These are the `[{section}]` blocks from two different agents' anthropic_render.toml files. They show what data fields exist and what values they take for agents with different characteristics.

Agent 1 (agent-builder — no output tool, broad creative task, complex examples):
```toml
{data_block_agent_builder}
```

Agent 2 (interview-enrich-create-summary — has output tool, tight batch processing task):
```toml
{data_block_interview_summary}
```

---

**WHAT TO ANALYZE**

Start from first principles: What does this section accomplish in the agent's behavioral programming? Not "it renders these fields" — but what must the agent UNDERSTAND after reading this section, and what behavioral effect does that understanding produce?

Then, for every data field:

1. **What is this field's role?** What information does it carry? Why does the agent need it?

2. **What is "left unsaid"?** The raw value alone is insufficient. What context, framing, or connective tissue must surround this value for an agent to use it correctly? A value like `"definition author"` means nothing without a sentence that tells the agent what to DO with that identity.

3. **What prose fragments could surround it?** For each fragment:
   - Give it a name (e.g., `identity_sentence`, `preamble`, `evidence_label`)
   - Show at least 3 meaningfully different phrasings — not synonyms, but phrasings that would produce DIFFERENT agent behavior
   - State the PURPOSE: why does this fragment exist? What does it accomplish?
   - State the HYPOTHESIS: how does the phrasing choice affect agent behavior? What would you test?
   - Classify its STABILITY: is this something you'd change rarely (structural), sometimes (formatting), or frequently (experimental prose)?

4. **What structural fragments shape the section?** Heading, preamble, intro prose, connective text, dividers, list formatting — things that don't attach to a specific field but shape how the section reads as a whole.

5. **What cross-field or cross-section dependencies exist?** Does any fragment reference data from multiple fields? Does this section need data owned by another section?

6. **What conditional branches exist?** Which fields are optional? How does the section's structure change when they're present vs absent? (Compare the two agents above.)

---

**FORMAT**

Use this structure for each field:

```
## FIELD: {field_name}
TYPE: {string | array | boolean | enum | ...}
OPTIONAL: {yes | no}
VALUES: {agent-builder value} / {interview-summary value}

### What the agent needs to understand
{Why this field matters. What behavioral effect it produces.}

### Fragments

**{fragment_name}**
- Current (defective): "{what the broken renderer currently does}"
- Alternative A: "{different phrasing}"
- Alternative B: "{different phrasing}"
- Alternative C: "{different phrasing}"
- PURPOSE: {why this fragment exists}
- HYPOTHESIS: {how phrasing choice affects behavior}
- STABILITY: {structural | formatting | experimental}
```

For structural fragments (not tied to a field), use the same format but under a `## STRUCTURAL` heading.

---

**WHAT SUCCESS LOOKS LIKE**

A successful analysis will:
- Start from what the agent NEEDS, not from what the current system DOES
- Identify fragments that nobody has thought of yet — things left unsaid that should be said
- Propose phrasings that are genuinely different in behavioral effect, not just synonyms
- Surface conditional structures where the section behaves differently based on data presence
- Be specific enough that someone could build a template system from it

**WHAT FAILURE LOOKS LIKE**

A failed analysis will:
- Describe the current rendered output and add "knobs" to it
- Treat the existing agent's presentation as the baseline to vary from
- Propose alternative phrasings that are cosmetically different but behaviorally identical
- Miss fields or fragments because they "seem obvious"
- Skip the behavioral hypothesis because "it's just a label"

### END AGENT INSTRUCTIONS

---

## After Both Agents Return

1. Read both output files
2. Identify **convergence** — where both agents independently reached the same conclusions (high-confidence insights)
3. Identify **divergence** — where they differ (blind spots, alternative perspectives)
4. Synthesize into the final `{SECTION}.md` in the parent directory, incorporating the best of both
5. Review with the user before moving to the next section
