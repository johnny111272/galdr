# Cross-Section Patterns

Observations from reading all 15 per-section syntheses. Organized into four categories: patterns that shape the TOML extraction plan, concrete findings the agents surfaced (schema errors, extension candidates, rendering conditionals), and open questions.

---

## PART 1: Patterns That Shape the Extraction Plan

### Pattern 1: Schema Extension — task_type

The most behavioral fragments across the system are gated on an agent property that doesn't exist in the data model: **task type** — a creative/broad vs mechanical/narrow distinction that affects five sections:

| Section | What task_type gates |
|---|---|
| IDENTITY | Declaration mechanism: heuristic vs negation |
| INSTRUCTIONS | Mode indicator framing, preamble intensity |
| SUCCESS_CRITERIA | Engagement mode: self-model vs checklist |
| FAILURE_CRITERIA | Abort stance: obligation vs permission |
| EXAMPLES | Calibration approach: demonstration vs pattern |

task_type affects more fragments across more sections than any single existing data field. Strongest candidate for schema addition. Without it, the most impactful style knobs have no data field to drive them.

Other inferred properties with less cross-section reach:
- **Prompt length** — affects IDENTITY bookend/recap
- **Evidence composition** (mechanical vs judgment) — affects SUCCESS_CRITERIA
- **Role strength** — affects voice/agency decisions

### Pattern 2: Three-Tier Compliance Hierarchy

Three sections form a graduated authority system with shared data shape but distinct rendering strategies:

| Tier | Section | Violation = | Rendering Strategy |
|---|---|---|---|
| 1 | CRITICAL_RULES | System failure / rejection | Terse axioms, no reasoning surface, ontological framing |
| 2 | CONSTRAINTS | Defective output | Ambient law, always-on filters, conjunctive application |
| 3 | ANTI_PATTERNS | Quality degradation | "Don't X — because Y" inoculation, show the wrong thing |

The hierarchy relationship itself may need cross-section prose — the agent should perceive three distinct authority levels, not three similar lists. CONSTRAINTS synthesis explicitly flags that the ordering CRITICAL_RULES > CONSTRAINTS > ANTI_PATTERNS should be visible to the agent.

### Pattern 3: Stability Spectrum Maps to Control Files

Across all 15 documents, fragment stability classifications cluster into three clear bands:

**STRUCTURAL** (rarely changes) — Section ordering, section presence, field sequence, heading levels, assembly order. The rendering skeleton.

**FORMATTING** (sometimes changes) — List style, label text, separator type, display thresholds, entry templates. Display variations.

**EXPERIMENTAL** (frequently changes) — Framing sentences, preambles, mode indicators, identity templates, authority language. The active behavioral tuning surface.

This maps onto a natural TOML split:
- **Skeleton** — structural decisions, rarely touched
- **Format** — display decisions, occasionally tuned
- **Style** — experimental prose, frequently adjusted

**Resolved:** Four axes — data (anthropic_render.toml), content (content.toml), structure (structure.toml), display (display.toml).

### Pattern 4: Motor vs Judgment Axis

Sections fall along a spectrum that affects their skeleton-to-style ratio:

**Motor sections** — Agent reproduces patterns. Mostly skeleton, little style.
- WRITING_OUTPUT, RETURN_FORMAT, FRONTMATTER

**Judgment sections** — Agent internalizes principles. Mostly style, flexible skeleton.
- EXAMPLES, ANTI_PATTERNS, SUCCESS_CRITERIA, FAILURE_CRITERIA

**Hybrid sections** — Mix of both.
- INSTRUCTIONS, CRITICAL_RULES, IDENTITY, INPUT

Motor sections need precise structural templates. Judgment sections need experimental prose with flexible structure. The TOML architecture must accommodate both without forcing uniform structure.

### Pattern 5: Section Ordering as a Control Surface

Multiple sections express strong positioning preferences based on LLM primacy/recency effects:

| Section | Preferred position | Rationale |
|---|---|---|
| IDENTITY | First | Primacy — first impression shapes all processing |
| SECURITY_BOUNDARY | After identity | Spatial model before task instructions reference paths |
| CRITICAL_RULES | Early, after identity | Rules as initialization frame, not afterthought |
| INSTRUCTIONS | After spatial and rules | Agent needs identity + territory + rules before task |
| EXAMPLES | After instructions | Calibration while procedure is fresh |
| RETURN_FORMAT | End of prompt | Recency — last thing before execution |

Section ordering belongs in the skeleton as a `section_order` array. Simple decision, high impact.

### Pattern 6: Two Architectural Outliers

**FRONTMATTER** — Zero experimental fragments. Pure serializer (data → YAML). No behavioral leverage. Not a presentation concern — infrastructure that feeds downstream sections.

**DISPATCHER** — Programs the caller, not the agent. Different audience, different purpose, different rendering problem. The dispatch strategy matrix (background_mode x max_agents) determines entirely different document shapes.

These two may not share the body-section TOML architecture.

### Design Principle: Format Knobs vs Structural Variants

Two categories of variation with completely different cost profiles:

**Format variation** (bullets, numbered, inline, sequential, table) — trivially dynamic. The renderer receives an enum and switches output. One function, one code path per format. These are cheap TOML knobs. Change them freely.

**Structural variation** (field ordering, field grouping, fused vs discrete) — requires either a dynamic ordering engine (complex, bug-prone) or a model variant (one extra Pydantic model). The model variant wins. The model IS the specification — field order is defined by the model's field sequence. No engine needed.

**Architecture:** Format knobs are dynamic. Structural variants are static models. The cost of a new variant is one Pydantic model. The cost of dynamic structural reordering is a system nobody wants to maintain.

**Application:** Only IDENTITY shows meaningful intra-section ordering variation (identity-first vs responsibility-first). This is a unicorn — two section model variants, not a configurable ordering system. All other sections have one natural ordering that both A/B analyses independently converged on.

**Inter-section ordering** (which section comes first in the prompt) is a separate concern — a simple `section_order` array in the skeleton TOML. This is a list, not a structural variant.

---

## PART 2: Schema Findings

### Confirmed Schema Errors

These are defects in the current system, independently identified by multiple analyses:

1. **SECURITY_BOUNDARY section omitted for no-grant agents.** The summarizer has no display entries, so the entire section is skipped — including workspace_path. Every agent needs a spatial root. (SECURITY_BOUNDARY synthesis)

2. **Implementation details leak into prompt.** `bypassPermissions`, "hook-based restrictions" appear in rendered output. The agent needs WHAT it can do, not HOW enforcement works. (SECURITY_BOUNDARY synthesis)

3. **instruction_mode dropped by renderer.** The mode field (deterministic/probabilistic) exists in the data but is never rendered. Both INSTRUCTIONS analyses independently identified this as the highest-leverage gap in the current system. (INSTRUCTIONS synthesis)

4. **Tool-first ordering in security grants.** Current renderer orders by tool, not by path. Agent's decision flow is location-first ("where is it?"), not tool-first ("what tool?"). (SECURITY_BOUNDARY synthesis)

5. **Critical rules missing workspace confinement rule.** The rule referencing workspace_path is absent when it should be present. (CRITICAL_RULES synthesis)

6. **Critical rules missing preamble.** No authority-establishing text before the rule list. Rules appear without framing. (CRITICAL_RULES synthesis)

### Schema Extension Candidates

New fields or field modifications surfaced by the analyses as promising additions:

1. **task_type** — See Pattern 1. Strongest candidate. Affects 5+ sections. Enum values TBD (creative/mechanical? broad/narrow?).

2. **instruction_mode subcategories** — Not just PROBABILISTIC but `PROBABILISTIC: summarizing`, `PROBABILISTIC: synthesis`, `PROBABILISTIC: assessment`. Finer-grained cognitive operation markers. (IDEA_CAPTURE.md)

3. **context_required purpose annotations** — Per-entry `purpose` field that transforms "read this file" into "read this file to learn X." Simple optional string, backward-compatible. (IDEA_CAPTURE.md, INPUT synthesis)

4. **dispatch_mode semantic clarification** — Current "full" value is ambiguous: delivery semantics (A) vs lifecycle semantics (B). Needs resolution before non-full modes materialize. (DISPATCHER synthesis)

5. **output name_pattern for partially-known outputs** — The "partially" value of name_known is vague without a template showing the pattern. (OUTPUT synthesis, DISPATCHER synthesis)

---

## PART 3: Rendering Conditionals

These are data-driven branching points the renderer must implement. They are invariant rules (code), not configurable knobs (TOML). "Silence for absence" is the universal principle — when optional data is absent, render nothing.

### Boolean Gates (present/absent)

| Condition | Effect |
|---|---|
| has_output_tool = false | Skip output-tool rules in CRITICAL_RULES, skip WRITING_OUTPUT section entirely |
| context_required absent | Skip reading list, heading, preamble, knowledge-data separator in INPUT |
| display array empty | Render minimal SECURITY_BOUNDARY (workspace_path only + mediated-access note) |
| constraints list empty | Skip CONSTRAINTS section |
| anti_patterns list empty | Skip ANTI_PATTERNS section |
| schema_path absent | Skip schema rendering in OUTPUT, consider description_sufficiency_cue |

### Enum Branches

| Field | Values | Effect |
|---|---|---|
| name_known | unknown / partially / known | Three different OUTPUT naming fragments |
| schema_embed | true / false | Embedded schema content vs path reference in OUTPUT |
| format | text / jsonl | Different operational prose, different parsing expectations |
| background_mode | allowed / forbidden | Different dispatch strategy prose in DISPATCHER |

### Count-Based Format Switches

| What | Threshold | Effect |
|---|---|---|
| Parameter count | 1 → prose, 2-3 → bullets, 4+ → table | INPUT parameter display format |
| Context entry count | affects numbered vs bulleted | INPUT reading list format |
| Rule/constraint count | affects display density | CONSTRAINTS, CRITICAL_RULES formatting |
| Security grant count | 0 / 1-3 / 4-7 / 8+ | SECURITY_BOUNDARY display format |
| Display tool-set uniformity | uniform vs heterogeneous | SECURITY_BOUNDARY grouped vs per-entry format |

### The Compound Conditional: Dispatch Strategy Matrix

| background_mode | max_agents | Strategy | Document Shape |
|---|---|---|---|
| forbidden | 1 | Sequential foreground | Linear: prepare, invoke, wait, consume |
| allowed | >1 | Parallel background | Orchestration: batch, fan-out, collect |
| forbidden | >1 | Sequential batching | Loop: prepare, invoke one-at-a-time |
| allowed | 1 | Single background | Fire-and-forget: invoke, continue, check later |

---

## PART 4: Cross-Section Data Flow

Same data values appear at multiple rendering sites. This is normal — the pipeline duplicates values into every section that needs them. Each site renders the value with its own template for its own purpose. Not a consistency risk — the source data is invariant.

Notable multi-site values:
- **workspace_path** → SECURITY_BOUNDARY (territory framing), CRITICAL_RULES (prohibition framing). Deliberate: same path, two behavioral mechanisms.
- **tool_name** → CRITICAL_RULES (exclusivity axiom), WRITING_OUTPUT (mechanics), SECURITY_BOUNDARY (grants), FRONTMATTER (enforcement config). Four rendering contexts.
- **parameters** → INPUT (agent-facing), DISPATCHER (caller-facing). Different audiences.
- **description** → IDENTITY (self-model), FRONTMATTER (machine metadata), DISPATCHER (caller decision support). Three purposes.

---

## Open Questions

1. Does `task_type` become a schema field? If yes, what are its values?
2. ~~Do we need three TOML files?~~ **Resolved:** Four axes — data, content, structure, display.
3. Do FRONTMATTER and DISPATCHER share the body-section architecture or get their own?
4. ~~How does section_order interact with per-section templates?~~ **Resolved:** structure.section_order.order drives iteration. Content is per-section, not per-template.
5. Which of the schema extension candidates are worth implementing now vs deferring?
