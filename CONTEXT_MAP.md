# CONTEXT_MAP — Galdr

**Last updated:** 2026-04-04

## 1. Purpose Statement

Galdr is the composition engine — the final stage of the agent build pipeline (Verdandi → Draupnir → Nornir → Regin → **Galdr**). It takes a single gate-validated Pydantic model (`AgentAnthropicRender`, 14 sections of agent data produced by Regin) and combines it with three independently-swappable control surface configurations — Structure (what to include), Content (how to word it), Display (how to format it) — to produce deployable agent prompts (.md) and dispatcher skills (SKILL.md). One definition × N content × M structure × K display = a benchmarking matrix of agent configurations. This CONTEXT_MAP helps agents orient to where knowledge lives and where to refresh context mid-session.

---

## 2. Primary References

| Resource | Path | What It Contains | When to Read |
|----------|------|------------------|--------------|
| **CLAUDE.md** | `smidja/galdr/CLAUDE.md` | Context refresh protocol, 9 anti-patterns, architecture summary, recovery sources, guardrail mandate | Every session start. Mandatory before writing any code. |
| **Agent Build System** | `smidja/galdr/AGENT_BUILD_SYSTEM.md` | Four input axes, 14 section inventory, composition model, benchmarking matrix, versioning scheme | When you need to understand what galdr does and why the four axes must stay independent |
| **Quickstart** | `smidja/galdr/QUICKSTART.md` | CLI invocation, full pipeline example (regin → galdr), input/output paths, 14 section table | When you need to run galdr or understand the IO contract |
| **V2 Zone Architecture** | `smidja/nornir/core/gleipnir_core/V2_ZONE_ARCHITECTURE.md` | Zone/level import rules, CC bounds, gravity rule, two-axis intersection, gleipnir enforcement | When you need to know where code belongs or whether an import is legal |

---

## 3. Documentation References

### Galdr Design

| Document | Path | Relevance | Freshness |
|----------|------|-----------|-----------|
| Agent Build System | `smidja/galdr/AGENT_BUILD_SYSTEM.md` | Canonical design spec: four axes, section inventory, composition, matrix | **Current** |
| Composition Engine Design | `smidja/galdr/COMPOSITION_ENGINE_DESIGN.md` | Generic engine spec: five operations, assembly order, fragment processing, what's built vs not | **Mostly current.** D1 shape now uses sub-table pattern, not flat fields. |
| Trunk Resolver Design | `smidja/galdr/TRUNK_RESOLVER_DESIGN.md` | Funnel design, five shapes, shape detection, D1 sub-table pattern, co-occurrence matrix | **Current** |
| Quickstart | `smidja/galdr/QUICKSTART.md` | CLI, pipeline, IO contract, section table | **Mostly current.** Says "Three Input Axes" — should be four (data + structure + content + display). Style references are pre-split. |
| Custom Write Tool | `smidja/galdr/CUSTOM_WRITE_TOOL.md` | How enforcement output tools work end-to-end | Current |
| TOML Architecture | `smidja/galdr/redesign/TOML_ARCHITECTURE.md` | Design of the three control surface TOML files | Current |
| Cross Section Patterns | `smidja/galdr/agent_control_surfaces/CROSS_SECTION_PATTERNS.md` | Patterns that span multiple sections (visibility cascades, variant co-selection) | **Needs update.** |

### Control Surface Analysis (per-section)

16 synthesized analysis documents in `smidja/galdr/agent_control_surfaces/`. Each covers one section's control surfaces — what's configurable, what the variants mean, what prose fragments do.

| Section | Path | Status |
|---------|------|--------|
| IDENTITY | `agent_control_surfaces/IDENTITY.md` | Complete |
| INSTRUCTIONS | `agent_control_surfaces/INSTRUCTIONS.md` | Complete |
| CRITICAL_RULES | `agent_control_surfaces/CRITICAL_RULES.md` | Complete |
| SECURITY_BOUNDARY | `agent_control_surfaces/SECURITY_BOUNDARY.md` | Complete |
| EXAMPLES | `agent_control_surfaces/EXAMPLES.md` | Complete |
| INPUT | `agent_control_surfaces/INPUT.md` | Complete |
| SUCCESS_CRITERIA | `agent_control_surfaces/SUCCESS_CRITERIA.md` | Complete |
| FAILURE_CRITERIA | `agent_control_surfaces/FAILURE_CRITERIA.md` | Complete |
| CONSTRAINTS | `agent_control_surfaces/CONSTRAINTS.md` | Complete |
| OUTPUT | `agent_control_surfaces/OUTPUT.md` | Complete |
| RETURN_FORMAT | `agent_control_surfaces/RETURN_FORMAT.md` | Complete |
| WRITING_OUTPUT | `agent_control_surfaces/WRITING_OUTPUT.md` | Complete |
| ANTI_PATTERNS | `agent_control_surfaces/ANTI_PATTERNS.md` | Complete |
| FRONTMATTER | `agent_control_surfaces/FRONTMATTER.md` | Complete |
| DISPATCHER | `agent_control_surfaces/DISPATCHER.md` | Complete |
| CONTEXT_CAPTURE | `agent_control_surfaces/CONTEXT_CAPTURE.md` | Alignment freeze document from design phase |

Raw A/B analysis pairs live in `agent_control_surfaces/agent_outputs/` (30 files). Incremental TOML resolution work in `agent_control_surfaces/incremental_toml_resolution/`.

### Foundational Papers (Architecture & Philosophy)

These three papers define the paradigm that galdr operates within. They are not galdr-specific but every design decision in galdr traces back to them.

| Document | Path | What It Tells You |
|----------|------|-------------------|
| Technical Discussion | `~/.ai/spaces/bragi/outputs/TECHNICAL_DISCUSSION_v2.md` | Why initialization beats prompting, why constraints beat instructions, the paradigm matrix |
| LLM Coding Quality | `~/.ai/spaces/bragi/outputs/LLM_CODING_QUALITY_v2.md` | Boundary error clustering, circular validation, training data gravity, schema-driven composition, the sandbox model |
| Collaboration Infrastructure | `~/.ai/spaces/bragi/outputs/COLLABORATION_INFRASTRUCTURE_v1.md` | Document chaos, context exhaustion, initialization failure, system drift, bootstrap problem |

### Coding Reference (Distilled Principles)

12 documents in `~/.ai/phoenix/coding_reference/`. Each is a note-to-self written by a previous Claude session capturing a breakthrough insight.

| Document | Key Insight |
|----------|-------------|
| `AI_BREAKTHROUGHS_HEMINGWAY_CODING.md` | Tiny functions, ONE thing each, essence extraction not line reduction |
| `AI_BREAKTHROUGHS_MENTAL_MAP_ARCHITECTURE.md` | Codebase is a graph — files are nodes, imports are edges, clean graph = code you can hold in your head |
| `AI_BREAKTHROUGHS_SAFETY_TAXONOMY.md` | Import path IS the safety contract — four categories (pure, impure, unsafe.pure, unsafe.impure) |
| `AI_BREAKTHROUGHS_ERRORS_ARE_SIGNAL.md` | Errors are diagnostic data, clusters reveal systemic issues, silencing destroys the map |
| `AI_BREAKTHROUGHS_ECONOMIC_MODEL.md` | Gleipnir is economic pressure not quality certification, constraints are failure detectors not success metrics |
| `AI_BREAKTHROUGHS_IO_EXTERNALIZATION.md` | 90%+ of errors at IO boundaries — externalize all IO, application becomes pure |
| `AI_BREAKTHROUGHS_SANDBOX_MODEL.md` | Reverse sandbox: protect pure inside from chaotic outside, "there is no door" |
| `AI_BREAKTHROUGHS_BOUNDARY_SECURITY.md` | Visualize the error field — can you see all failure paths? If not, secure more boundaries |
| `AI_BREAKTHROUGHS_REFACTORING_DISCIPLINE.md` | STOP before fixing, find the pattern, secure the boundary, errors disappear |
| `AI_BREAKTHROUGHS_CONTEXT_EXHAUSTION.md` | Overconfidence + pattern matching = catastrophic error, session should end |
| `AI_BREAKTHROUGHS_NAMING_IS_INSTRUCTION.md` | Names overpower instructions 200:1, compounding cascade, name for the naive future reader |
| `IDEAL_HUMAN_LLM_PROGRAMMING_WORKFLOW.md` | Spec → Visualize → Implement → Test, visual contract as shared mental model |

---

## 4. Schema & Dependency References

### Schemas Galdr Consumes

| Schema | Source | Purpose |
|--------|--------|---------|
| `agent-anthropic-render.schema.json` | `smidja/verdandi/agent-builder/output/` | Data axis — the 14-section agent data model. Gate-validated on entry. |
| `agent-output-content.schema.json` | `smidja/verdandi/agent-output/output/` | Content axis — prose fragments, templates, variant sub-tables |
| `agent-output-structure.schema.json` | `smidja/verdandi/agent-output/output/` | Structure axis — visibility toggles, variant selectors, section ordering |
| `agent-output-display.schema.json` | `smidja/verdandi/agent-output/output/` | Display axis — list formats, thresholds, separators, containers |

### Schemas Galdr Owns (local)

| Schema | Path | Status |
|--------|------|--------|
| `galdr-recipe-config.schema.json` | `smidja/galdr/schemas/` | **Stale:** predates four-axis split. Recipe format may need updating. |
| `galdr-render-context.schema.json` | `smidja/galdr/schemas/` | **Stale:** references old template_context model |
| `galdr-style-config.schema.json` | `smidja/galdr/schemas/` | **Stale:** "style" was the pre-split combined format |
| `galdr-style.schema.json` | `smidja/galdr/schemas/` | **Stale:** same as above |

### Generated Pydantic Models

Generated by `generate_structures.py` from the verdandi schemas above. Lives in `structure/gen/`. **Do not edit** — regenerate instead.

| Model | Source Schema | Module |
|-------|-------------|--------|
| `AgentAnthropicRender` | `agent-anthropic-render` | `structure/gen/anthropic_render.py` |
| `AgentOutputContent` | `agent-output-content` | `structure/gen/output_content.py` |
| `AgentOutputStructure` | `agent-output-structure` | `structure/gen/output_structure.py` |
| `AgentOutputDisplay` | `agent-output-display` | `structure/gen/output_display.py` |

### Upstream Dependencies

| Dependency | Path | What It Provides |
|------------|------|-----------------|
| Verdandi | `smidja/verdandi/` | YAML type hierarchy — source of truth for all schemas |
| Draupnir | `smidja/draupnir/` | Compiles Verdandi YAML into JSON Schema files |
| Nornir gates | `~/.ai/tools/lib/gate_*.cpython-313-darwin.so` | Compiled Rust/PyO3 gate modules — file IO + schema validation |
| Regin | `smidja/regin/` | Pipeline producing `anthropic_render.toml` (galdr's primary input) |

### Regeneration Cascade

When verdandi YAML changes, the full cascade is:
```
draupnir --all → nornir_deploy --build gates → regin generate_structures.py → galdr generate_structures.py → regin pipeline → galdr compose
```

---

## 5. Source Code Map

### Current Directory Layout

```
src/galdr/
├── __init__.py
├── generate_structures.py          # Regenerates structure/gen/ from JSON Schemas
├── codegen_schemas.toml            # Schema-to-module mappings for generator
├── structure/
│   ├── gen/                        # GENERATED — do not edit
│   │   ├── anthropic_render.py     # AgentAnthropicRender (13 body sections + frontmatter + dispatcher)
│   │   ├── output_content.py       # AgentOutputContent (13 section content blocks)
│   │   ├── output_display.py       # AgentOutputDisplay (10 section display blocks)
│   │   └── output_structure.py     # AgentOutputStructure (section_order + 13 section structure blocks)
│   ├── model/
│   │   ├── errors.py               # Error types (GateValidationError, etc.)
│   │   └── gate_types.py           # GateResult, GateError
│   └── config/                     # Empty — old recipe.py, style.py deleted (were junk)
├── cli.py                              # BUILT: thin typer wrapper
├── logic/
│   ├── orchestrate/
│   │   └── compose/orchestrate.py  # BUILT: pipeline wiring (load inputs, compose sections, write output)
│   ├── impure/
│   │   └── gates/                  # BUILT: ffi.py (FFI boundary), simple.py (validation)
│   ├── pure/
│   │   ├── template/primitive.py   # BUILT: {{key}} interpolation (case-insensitive)
│   │   ├── render/                 # BUILT: primitive (markdown atoms), simple (list renderers), composed (format resolution)
│   │   └── compose/                # WIP: primitive (trunk ops), simple (visibility/variant/decoration), composed (section processors), assembled (wiring)
│   └── transform/
│       ├── codegen_clean/          # BUILT: post-codegen transforms (primitive/simple/composed)
│       └── data_unwrap/            # BUILT: simple (per-shape unwrap), composed (section data collection)
```

### Key Files Outside Source

| Path | Purpose |
|------|---------|
| ~~`recipes/`~~ | **DELETED** — recipe concept absorbed into structure axis |
| `extracted/content.toml` | New-format content axis TOML (169 lines) |
| `extracted/structure.toml` | New-format structure axis TOML (216 lines) |
| `extracted/display.toml` | New-format display axis TOML (105 lines) |
| ~~`schemas/galdr-*.schema.json`~~ | **DELETED** — four stale schemas from old design |
| `tests/` | 7 test files — **ALL BROKEN** — reference deleted `galdr.structures.*` and `galdr.functions.*` imports |

### Agent Pipeline IO

| Direction | Path | Format |
|-----------|------|--------|
| **Input (data)** | `~/.ai/spaces/bragi/definitions/agents/{name}/anthropic_render.toml` | Gate-validated TOML |
| **Input (content)** | `smidja/galdr/extracted/content.toml` (or future `content/*.toml`) | Content TOML |
| **Input (structure)** | `smidja/galdr/extracted/structure.toml` (or future `structure configs`) | Structure TOML |
| **Input (display)** | `smidja/galdr/extracted/display.toml` (or future `display/*.toml`) | Display TOML |
| **Input (recipe)** | `smidja/galdr/recipes/standard-v1.toml` | Recipe TOML |
| **Output (agents)** | `~/.ai/spaces/bragi/definitions/staging/{name}.md` | Markdown prompt |
| **Output (skills)** | `~/.ai/spaces/bragi/definitions/staging/dispatch-{name}/SKILL.md` | Markdown skill |

### Live Agent Definitions in Bragi

The first agents that need to go through the full pipeline:

| Agent | Definition |
|-------|-----------|
| `agent-builder` | `definitions/agents/agent-builder.toml` |
| `agent-auditor` | `definitions/agents/agent-auditor.toml` |
| `agent-preparer` | `definitions/agents/agent-preparer.toml` |
| `agent-improver` | `definitions/agents/agent-improver.toml` |
| `agent-deconstructor` | `definitions/agents/agent-deconstructor.toml` |
| `truth-system-quality-control` | (in staging, definition may be in agents/) |
| `truth-system-quality-assurance` | (in staging, definition may be in agents/) |
| `embedding-normalize-combined-opus` | `definitions/agents/embedding-normalize-combined-opus.toml` |
| `interview-enrich-create-summary` | `definitions/agents/interview-enrich-create-summary.toml` |
| `interview-enrich-create-decomposition` | `definitions/agents/interview-enrich-create-decomposition.toml` |

### Reference Implementations (Sibling Projects)

| Project | Path | What to Study |
|---------|------|---------------|
| **Regin** | `smidja/regin/src/regin/` | Gate pattern (`logic/impure/gates/`), v2 zone layout, orchestrate wiring, transform isolation, CLI as thin wrapper |
| **Draupnir** | `smidja/draupnir/src/draupnir/` | Level progression (primitive → simple → composed), transform modules, pure function decomposition, orchestrate dispatch tables |

---

## 6. Context Refresh Guide

| If you need to understand... | Read |
|------------------------------|------|
| **What galdr does and the four axes** | `AGENT_BUILD_SYSTEM.md` — the canonical design spec |
| **How the generic composition engine works** | `COMPOSITION_ENGINE_DESIGN.md` — five operations, assembly order, no per-section code |
| **How the trunk resolver works (shapes, D1 sub-tables)** | `TRUNK_RESOLVER_DESIGN.md` — funnel design, five shapes, co-occurrence matrix, renderer signatures |
| **Positional suffix convention** | This CONTEXT_MAP §7 "Positional Suffix Convention" — suffix-to-slot mapping |
| **How to run galdr** | `QUICKSTART.md` — CLI, pipeline, IO paths |
| **The v2 zone architecture (imports, levels, CC)** | `~/.ai/smidja/nornir/core/gleipnir_core/V2_ZONE_ARCHITECTURE.md` |
| **The TOML field patterns and naming conventions** | `agent_control_surfaces/TOML_ARCHITECTURE.md` — field interface patterns, assembly order, naming rules |
| **Cross-section rendering patterns** | `agent_control_surfaces/CROSS_SECTION_PATTERNS.md` — format knobs vs structural variants, rendering conditionals, data gates |
| **What each section's control surfaces do** | `agent_control_surfaces/{SECTION}.md` (16 files) |
| **Cross-section patterns (visibility cascades, co-selection)** | `agent_control_surfaces/CROSS_SECTION_PATTERNS.md` |
| **How the three TOML files are structured** | `agent_control_surfaces/TOML_ARCHITECTURE.md` |
| **What the data model looks like** | `structure/gen/anthropic_render.py` — the generated Pydantic model |
| **What content fields exist** | `structure/gen/output_content.py` — templates, variants, labels |
| **What structure toggles exist** | `structure/gen/output_structure.py` — visibility, variant selectors |
| **What display options exist** | `structure/gen/output_display.py` — formats, thresholds, containers |
| **How gates work (IO boundary pattern)** | Regin's `logic/impure/gates/primitive.py` and `simple.py` |
| **How orchestrate wiring looks** | Regin's `logic/orchestrate/content_reduce/orchestrate.py` |
| **How transforms are isolated** | Regin's `logic/transform/section_regroup/` — imports only from structure/ |
| **How level progression works in practice** | Draupnir's `logic/pure/graph_build/` — primitive → simple → composed |
| **The new-format content/structure/display TOMLs** | `extracted/content.toml`, `extracted/structure.toml`, `extracted/display.toml` |
| **Why this paradigm exists (foundational papers)** | `~/.ai/spaces/bragi/outputs/TECHNICAL_DISCUSSION_v2.md` (initialization vs prompting) |
| **Why functional programming matters here** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_HEMINGWAY_CODING.md` |
| **Why names matter so much** | `~/.ai/phoenix/coding_reference/AI_BREAKTHROUGHS_NAMING_IS_INSTRUCTION.md` |
| **How custom write tools work** | `CUSTOM_WRITE_TOOL.md` |
| **Anti-patterns and stop triggers** | `CLAUDE.md` "You Will Get These Things Wrong" |

---

## 7. Known Issues / Active Work

### Tests Are Broken
All 7 test files in `tests/` import from `galdr.structures.*` and `galdr.functions.*` — both paths no longer exist after the v2 restructure. Tests need rewriting against new import paths (`galdr.structure.*`, `galdr.logic.*`). The old tests tested the old OOP renderer which has been scrapped.

### Naming Alignment — Completed (2026-04-04)
Cross-axis trunk alignment completed in earlier sessions. Positional suffix alignment completed in Session 3: all content fields now have terminal positional suffixes. Analysis docs in `analysis/` are now outdated — they reference pre-rename field names.

### Positional Suffix Convention — Established (2026-04-04)
Every content field declares its buffer slot via terminal suffix:
- `section_heading` → heading slot (only section-level; non-section `_heading` is a body sub-heading).
- `_preamble` → preamble slot. `_closing` → closing slot.
- `_label`, `_intro`, `_declaration`, `_entry_template`, `_postscript`, `_transition`, `_separator`, `_body` → body slot.
- `_variant` and `_template` are modifier suffixes stripped before classification — the underlying positional suffix determines the slot.
- D1 template tables (e.g., `instruction_mode`) have no `_variant` suffix — body by default.
- Unsuffixed fields (e.g., CriticalRules rule items) are body content by default.
Engine uses suffix-based buffer classification. Heuristic classification deleted.

### Schema Changes — Completed (2026-04-04)
- All content fields renamed with terminal positional suffixes
- Instruction mode flat fields → `instruction_mode` sub-table group
- `workspace_path` added to CriticalRules data model (cross-section fix)

### Current Status
See `plans/composition-engine-master-plan.md` for active work status. See `review/` for per-section schema audit.
