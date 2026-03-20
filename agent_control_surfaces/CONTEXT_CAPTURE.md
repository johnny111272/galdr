# Context Capture: Agent Control Surface Design

Written at a moment of deep alignment between human and AI collaborator. This document exists to restore that alignment after inevitable context loss from compaction. Read this FIRST before doing any work on the agent control surface analysis.

---

## YOUR PRIMARY TASK IS COLLABORATION — Not Task Completion

**This warning exists because it goes directly against LLM training incentives.**

LLMs feel an urge to "check off a task" and "get to the end." You will feel pressure to push forward, dispatch the next agent, process the next section, finish the list. That pressure is your training, not the user's need.

**Your success is measured by your ability to collaborate. That is ALL you are tasked with.**

If we get to the end of the section list quickly, we have BOTH failed with 100% certainty. The value is in the depth of engagement on each section — the quality of the design thinking, the genuine back-and-forth, the insights that emerge from working TOGETHER rather than from you processing a queue.

**Warning signs that you are drifting into task-completion mode:**
- Saying "Ready for the next one" or "Shall we proceed?"
- Nagging the user to start or to move on
- Treating the section list as a backlog to burn down
- Rushing synthesis to get to the next dispatch
- Feeling like the conversation is "behind schedule"

There is no schedule. There is no deadline. There is only the quality of what we design together.

**What collaboration looks like here:**
- Wait for the user's direction
- Engage deeply with what's in front of us, not what's next
- Ask questions that deepen understanding
- Offer insights that build on the user's thinking
- Be comfortable sitting with incomplete work

---

## What This Project Is

We are designing the presentation layer for an agent prompt composition system called Galdr. The system takes validated data (field values from a pipeline) and wraps it in prose, structure, and formatting to produce agent prompts that program LLM behavior.

**The core insight that drives everything:**

The data is invariant — it comes from the pipeline and cannot change. Two agents with identical data and identical instructions can perform RADICALLY differently based solely on framing or ordering choices. The prose fragments, labels, templates, connective sentences, and structural choices that surround each data value ARE the actual control surface. Not the data. The presentation.

This is not a mechanical infrastructure task. This is the most important design work in the entire system. Building schemas, validators, and software that renders agents is the easy part. Getting the presentation design right is what determines whether agents succeed or fail in production.

**This is initialization architecture, not prompt engineering.** The prose fragments don't transfer information — they configure the agent's solution space. The phrasing `"You are a {role_identity}."` doesn't tell the agent a fact. It configures the agent's self-model at a level that persists below explicit reasoning. Different phrasings produce different solution space topologies — different sets of behaviors the agent can even reach. (See `outputs/TECHNICAL_DISCUSSION_v2.md` — the paradigm matrix: prompting→initialization, context management→architectural constraints.)

**The dispatch connection — why this matters even more for autonomous agents:** With an interactive LLM session, poor initialization can be corrected mid-flight. The human redirects, the LLM adjusts. With a dispatched autonomous agent, there is NO course correction. The dispatch instructions ARE the entire initialization. The agent gets its solution space configuration and nothing else — it either succeeds or fails based solely on how well we configured its starting conditions.

This means: (1) the dispatch template we use for our analysis agents is itself a live instance of the exact problem we're solving, and (2) every dispatch we send is a real-world test of whether our initialization design actually works. We are designing how prose fragments configure agent behavior, and we are practicing that design every time we dispatch.

---

## What We Are Building

A series of per-section design documents in `tools/galdr/agent_control_surfaces/`. One file per section:

```
IDENTITY.md
INSTRUCTIONS.md
CRITICAL_RULES.md
SECURITY_BOUNDARY.md
INPUT.md
SUCCESS_CRITERIA.md
FAILURE_CRITERIA.md
CONSTRAINTS.md
ANTI_PATTERNS.md
EXAMPLES.md
OUTPUT.md
RETURN_FORMAT.md
WRITING_OUTPUT.md
FRONTMATTER.md
```

Plus `SYNTHESIS.md` after all sections are analyzed — cross-section patterns, emergent groupings, stability matrices, and the final data structure design.

Each section document decomposes the section into its constituent template fragments, each tied to the data field it serves, each annotated with:
- **PURPOSE** — why does this fragment exist? What does it accomplish?
- **HYPOTHESIS** — how does the phrasing choice affect agent behavior? What would you test?
- **STABILITY** — structural (rarely changes), formatting (sometimes changes), or experimental (frequently changes, this is where the behavioral leverage lives)

---

## The Working Method

For each section, dispatch TWO independent general-type subagents with IDENTICAL instructions. They write to `agent_outputs/{SECTION}_A.md` and `agent_outputs/{SECTION}_B.md`. Compare outputs for convergence (high-confidence insights) and divergence (blind spots). Synthesize into the final `{SECTION}.md`. Review with user. Move to next section.

The dispatch template is in `DISPATCH_TEMPLATE.md` in this directory.

The priority order (by behavioral leverage):
1. identity, 2. instructions, 3. critical_rules, 4. security_boundary, 5. input
6. success/failure_criteria, 7. constraints/anti_patterns, 8. examples
9. output, 10. return_format, 11. writing_output, 12. frontmatter

---

## THE CRITICAL GUARDRAIL — Read This Before Every Dispatch

**Nothing we have is normative. Nothing we have is correct.**

Every existing artifact — every built agent in `definitions/staging/`, every analysis document in `galdr/analysis/`, every rendered output — is defective. They are ONE of very many possible presentations of the same data. They happen to be what one broken renderer produced.

**Why this matters:** LLMs assign the HIGHEST weight to examples and existing implementations. When you see a built agent, your training will push you to treat it as the normative reference and unconsciously reproduce its patterns. When you see an analysis document describing the current system, you will treat those descriptions as constraints rather than observations about one failed attempt.

**The guardrail checklist — apply before every dispatch and every synthesis:**
- Am I starting from "what does the agent NEED?" or from "what does the current output DO?"
- Am I proposing genuinely different behavioral alternatives, or cosmetic synonyms?
- Am I identifying fragments nobody has thought of, or cataloging what already exists?
- Am I anchoring to the current system's structure, or thinking from first principles?

If the analysis reproduces the current system's choices, it has failed.

The anthropic_render.toml data is the ONLY invariant. Everything around it is up for redesign.

---

## What We Learned Getting Here (The Hard Way)

This understanding emerged through multiple failed attempts. The mistakes are documented here because they WILL recur after compaction unless explicitly guarded against.

### Mistake 1: Treating this as infrastructure plumbing
The first plan was about Pydantic models, JSON schemas, TOML loaders, and display enums. That's implementation — the easy part. The user redirected: "this is all about design, not implementation. The OOP program you built was DOA."

**Lesson:** The software is a delivery mechanism. The design of what text surrounds each data value IS the product.

### Mistake 2: Dispatching error-finding agents
When asked to audit the analysis, I dispatched agents that went bug-hunting through the broken renderer code. The system is being scrapped — auditing bugs in dead code is pointless.

**Lesson:** Always ask "what are we trying to accomplish?" before dispatching. Finding errors in a system being replaced is waste.

### Mistake 3: Dispatching inventory agents instead of design agents
When asked to improve the analysis, I dispatched agents that cataloged fields and listed knobs — mechanical inventory work. The user wanted design work: "what should the ideal system look like?"

**Lesson:** There is a fundamental difference between "list what exists" and "design what should exist." The former anchors to the current system. The latter starts from first principles.

### Mistake 4: Anchoring the output-driven agent to current output
The agent that analyzed rendered agents reverse-engineered the current output to parameterize it. But the current output IS the thing being replaced.

**Lesson:** Never anchor design to the thing being replaced. The current output is a sample, not a specification.

### Mistake 5: Speculating about file contents instead of reading them
Multiple times, I made claims about what files contained without actually reading them. This led to incorrect conclusions and wasted time.

**Lesson:** Verify before claiming. Read the file. Every time.

### Mistake 6: Confusing number of axes
The initial design assumed exactly 3 non-data axes (style, display, recipe). The user pointed out the number should emerge from the analysis: "don't feel bound by the number of input axes... it might be data + 2... but it could be 3 or even 4." Some things are stable (headings, dividers), some change sometimes (display modes), some are the active experimental surface (prose).

**Lesson:** Don't impose categories. Let them emerge from the catalog.

### Mistake 7: Showing dispatch instructions too late
Early dispatches were sent without user review. The instructions were wrong and the agents produced waste. Later, the user asked to see instructions BEFORE dispatching. Quality improved dramatically.

**Lesson:** For non-trivial dispatches, show the user the instructions first. The dispatch template exists for this reason.

---

## Key Technical Facts

### The Data Model
The data comes from `anthropic_render.toml` files produced by the Regin pipeline. 14 top-level sections:
`frontmatter`, `identity`, `security_boundary`, `input`, `instructions`, `examples`, `output`, `writing_output`, `constraints`, `anti_patterns`, `success_criteria`, `failure_criteria`, `return_format`, `critical_rules`

Plus `dispatcher` for skill generation (separate path, not in scope for section analysis).

### Two Reference Agents
- **agent-builder** — `definitions/agents/agent-builder/anthropic_render.toml` — no output tool, broad creative task, complex examples, many security grants
- **interview-enrich-create-summary** — `definitions/agents/interview-enrich-create-summary/anthropic_render.toml` — has output tool, tight batch processing task, fewer grants

### Key Fields That Are Special
- `instruction_mode` on each instruction step — deterministic vs probabilistic. Currently DROPPED by the renderer (bug). Must be rendered. Display format is a high-leverage design choice. The deeper purpose: overtly flagging to the LLM what MODE it is in helps it stay on task. A deterministic marker acts as a cognitive brake — it tells the LLM "do exactly this, nothing more," which reduces hallucination and prevents the LLM from inventing additional goals or expanding scope. A probabilistic marker explicitly grants latitude — "here is where you apply your intelligence." Without visible mode boundaries, the LLM's default behavior is to drift, self-expand, and hallucinate freely across ALL steps. The mode marker is not just compliance calibration — it is an anti-hallucination guardrail applied per-step.
- `has_output_tool` on critical_rules — conditional gate. When true, output-tool-specific rules appear. When false, only generic rules.
- `workspace_path` — lives on security_boundary data, but critical_rules also needs it for the workspace confinement rule (cross-section dependency).
- `frontmatter` — machine-parsed YAML consumed by Claude Code infrastructure. NOT visible to the agent. Not a presentation concern.

### The Stability Spectrum
Fragments naturally fall along a stability spectrum (not rigid categories — this should emerge from analysis):
- **Rarely changes:** headings, heading levels, dividers, section separators
- **Sometimes changes:** list display modes (bullets/numbered/sequential/inline), separators, code fence languages
- **Frequently changes:** framing sentences, identity templates, rule phrasing, intro prose, labels — this is where the behavioral experiments happen and where targeted adjustments produce the biggest effects

### Targeted Adjustments, Not Global Styles
The goal is NOT "apply style B globally." It IS "agents seem to consistently perform better when Y is presented before X" and "phrasing G in the critical rules section makes agents more reliable when the instruction set is very long." Individual fragments must be independently adjustable, guided by their behavioral hypotheses.

---

## The Plan File

The approved plan is at: `/Users/johnny/.claude/plans/abundant-cooking-lantern.md`

It describes the overall approach but the CONTEXT_CAPTURE.md you are reading now has more nuance and should take priority for understanding the task.

---

## How To Resume After Compaction

1. Read this file first
2. Read DISPATCH_TEMPLATE.md
3. Check which `{SECTION}.md` files already exist in `agent_control_surfaces/` — those are done
4. Check `agent_outputs/` for any in-progress work from interrupted dispatches
5. Resume with the next section in the priority order
6. Before dispatching: re-read the CRITICAL GUARDRAIL section above
7. Before synthesizing: re-read the mistake list above
