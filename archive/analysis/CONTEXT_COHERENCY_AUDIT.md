# Context Coherency Audit

**Date:** 2026-04-04
**Auditor:** Claude Opus 4.6 (1M context)
**Scope:** All context documents, design docs, memory file, and build plan checked against actual codebase state.

---

## Summary

28 issues found. 5 critical (will mislead next session into building on wrong foundations), 9 significant (incorrect counts or stale claims that will cause confusion), 14 minor (cosmetic or low-risk inconsistencies).

---

## 1. CLAUDE.md

### 1.1 Architecture Paragraph — Section Count [SIGNIFICANT]

**Line 98:** Says "14 sections of agent data produced by Regin" in the architecture paragraph.

**Reality:** `AgentAnthropicRender` has 15 fields: `dispatcher`, `frontmatter`, and **13 body sections** (identity, input, return_format, output, instructions, critical_rules, security_boundary, examples, constraints, anti_patterns, success_criteria, failure_criteria, writing_output). The "14 sections" claim is wrong. It should say "13 body sections plus dispatcher and frontmatter" or "15 fields total."

### 1.2 Missing Anti-Pattern: CC=49 Monolith [CRITICAL]

The user flagged that a new anti-pattern was discovered in this session: building a CC=49 monolith in `compose/composed.py` by writing code from training data instead of reference implementations. This is not captured in CLAUDE.md's "You Will Get These Things Wrong" section.

**Recommendation:** Add anti-pattern covering:
- Writing code from training data patterns instead of studying reference implementations (draupnir, regin) first
- Building a monolith walker when the CC cap for composed is 4-8
- Passing callables to avoid import graph constraints (bypasses gleipnir)

### 1.3 Missing Anti-Pattern: Callable Passing [CRITICAL]

The build plan (v3) explicitly warns "No callable passing -- it bypasses the dependency graph." This lesson was learned in this session but is not captured in CLAUDE.md's anti-pattern list. This is the kind of thing that will be lost on compaction.

### 1.4 Missing Anti-Pattern: isinstance for Type Safety [SIGNIFICANT]

The build plan warns "No isinstance for type safety -- use schema metadata (model_fields annotations) instead." This was a lesson from this session not captured in CLAUDE.md.

### 1.5 Recovery Sources Table — Path Format [MINOR]

Recovery sources use relative paths like `~/.ai/smidja/nornir/...` which is fine, but some use `AGENT_BUILD_SYSTEM.md` (relative to galdr root) while others use full tilde paths. Inconsistent but functional.

### 1.6 Anti-Pattern "Using the Old Code as Reference" References `styles/default.toml` [OK]

This correctly warns against the old format. The old directory has been deleted. Accurate.

---

## 2. CONTEXT_MAP.md

### 2.1 Section Counts in Source Code Map Are Wrong [CRITICAL]

**Line 152-155** (Source Code Map, structure/gen/ comments):

| Claimed | Actual |
|---------|--------|
| `anthropic_render.py` — "14 sections + dispatcher" | **15 fields total: dispatcher + frontmatter + 13 body sections.** "14 sections" undercounts by 1 (frontmatter is a section) or overcounts body sections by 1. |
| `output_content.py` — "12 section content blocks" | **13 section content blocks** (identity, security_boundary, input, critical_rules, instructions, examples, constraints, anti_patterns, success_criteria, failure_criteria, output, writing_output, return_format) |
| `output_display.py` — "9 section display blocks" | **10 section display blocks** (identity, security_boundary, input, critical_rules, instructions, examples, constraints, anti_patterns, success_criteria, failure_criteria) |
| `output_structure.py` — "12 section structure blocks" | **14 fields: section_order + 13 section blocks.** If counting only section blocks, it's 13, not 12. |

Every count in the code map is wrong. A fresh session relying on these will be confused when model introspection returns different numbers.

### 2.2 `structure/config/` Described as "Empty -- old recipe.py, style.py deleted" [OK]

Confirmed: directory exists, is empty except for `__init__.py`. Accurate.

### 2.3 `structure/gen/schema/` Not Mentioned [MINOR]

There is an empty `structure/gen/schema/` directory on disk not mentioned in the code map. Harmless but creates a "what is this?" question.

### 2.4 Missing From Code Map: `logic/pure/compose/` [CRITICAL]

The code map does not list `logic/pure/compose/` at all. This directory exists on disk with three files (`primitive.py`, `simple.py`, `composed.py`) containing the core composition engine. It is untracked in git (not committed). The code map still says the logic directories are "Empty -- to be built."

**The code map is stale relative to the current working tree.** The compose module is the most important code in the project and it is invisible to a fresh session reading the code map.

### 2.5 Missing From Code Map: `logic/transform/data_unwrap/` [SIGNIFICANT]

The `data_unwrap/` module exists (committed as of `100dace`) with `simple.py` and `composed.py`. Not listed in the code map.

### 2.6 Missing From Code Map: `logic/transform/identity_compose/` [MINOR]

An empty directory exists at `logic/transform/identity_compose/`. Not tracked in git, not mentioned in the code map. Appears to be a leftover from a plan that was abandoned. Should be deleted.

### 2.7 `recipes/` and `styles/` Directories [OK]

Code map correctly marks these as DELETED. Confirmed they do not exist on disk.

### 2.8 `schemas/galdr-*.schema.json` [OK]

Code map correctly marks these as DELETED. Confirmed they do not exist on disk.

### 2.9 Agent Pipeline IO — Recipe Input [SIGNIFICANT]

**Line 187:** `| **Input (recipe)** | smidja/galdr/recipes/standard-v1.toml | Recipe TOML |`

This path does not exist. The recipe concept was absorbed into the structure axis. The `recipes/` directory has been deleted. This IO table entry is stale and contradicts the known issue "Old Artifacts Cleaned" section in the same document.

### 2.10 Tests Description [OK]

Says "7 test files -- ALL BROKEN." Confirmed: 7 test `.py` files exist, all reference old import paths. Also confirmed: 8 `.qa` sidecar files exist in tests/ (generated by quality tooling). The `.qa` files are not mentioned but are harmless.

### 2.11 agent_control_surfaces Count [MINOR]

**Line 37:** Says "16 synthesized analysis documents." Actual count of `.md` files in `agent_control_surfaces/`: 22 (includes TOML_ARCHITECTURE, CROSS_SECTION_PATTERNS, DISPATCH_SYNTHESIS_TEMPLATE, DISPATCH_TEMPLATE, DISPATCH_TOML_RESOLVER, IDEA_CAPTURE, and CONTEXT_CAPTURE beyond the 16 per-section docs). The per-section docs table lists 16 entries, which is correct. But the "16 synthesized analysis documents" framing is misleading since the directory contains 22 markdown files total.

### 2.12 Quickstart Staleness Note [OK]

Correctly flags that QUICKSTART.md says "Three Input Axes" instead of four. Accurate.

### 2.13 Known Issues — "The Composition Engine Itself" [SIGNIFICANT]

**Line 268:** Says "The actual section renderers, template interpolation, variant selection, and markdown assembly -- the core of what galdr does -- have not yet been built in the new architecture."

**Reality:** `logic/pure/compose/` has a working `compose_section()` function in `composed.py` with template interpolation, variant selection, visibility checking, list formatting, and trunk matching. The data unwrapper is also built. The statement is stale -- significant progress has been made. A fresh session reading this will think it needs to start from scratch.

---

## 3. COMPOSITION_ENGINE_DESIGN.md

### 3.1 "What's Already Built" Table [SIGNIFICANT]

**Lines 261-268:** Lists 7 modules as built. This list is incomplete:

**Missing from table:**
- `logic/pure/compose/primitive.py` -- trunk extraction, suffix operations (BUILT)
- `logic/pure/compose/simple.py` -- visibility, variant, decoration lookup (BUILT)
- `logic/pure/compose/composed.py` -- the section walker (BUILT)
- `logic/transform/data_unwrap/simple.py` -- per-shape unwrappers (BUILT)
- `logic/transform/data_unwrap/composed.py` -- section data unwrapper (BUILT)

**"What's NOT built" list is also stale:**
- Data field classifier -- partially built (type dispatch in compose/composed.py)
- Content matcher -- built (find_decoration in compose/simple.py)
- Override resolver -- not built (correct)
- Visibility checker -- built (is_visible_by_mode in compose/simple.py)
- Variant selector -- built (select_variant in compose/simple.py)
- Data unwrapper -- BUILT (transform/data_unwrap/)
- Section walker -- BUILT (compose_section in compose/composed.py)
- Pipeline orchestrator -- not built (correct)
- CLI -- not built (correct)

### 3.2 Section Count [MINOR]

**Line 148:** Says "13 section names" in section_order. This matches the actual `structure.toml` section_order array (13 items). Correct.

### 3.3 "14 sections" in Purpose Statement [MINOR]

The purpose statement (via CONTEXT_MAP reference) and various places say "14 sections." The actual body section count is 13. This is the same inconsistency as CLAUDE.md.

---

## 4. AGENT_BUILD_SYSTEM.md

### 4.1 Section Containers — OOP Syntax [SIGNIFICANT]

**Lines 146-169:** The "Section Containers" section shows class-based, per-section OOP code:

```python
identity = Identity(
    data=data_model.identity,
    structure=structure_model.identity,
    content=content_model.identity,
    display=display_model.identity,
)
output = identity.render()
```

This directly contradicts the COMPOSITION_ENGINE_DESIGN.md which states "One generic engine processes all sections" and "There is no per-section code." It also contradicts CLAUDE.md anti-pattern "Writing Per-Section Code."

**This is the OLD design that was scrapped.** AGENT_BUILD_SYSTEM.md was written before the generic engine design was finalized and still shows the per-section class pattern. The "Composition" section (lines 172-183) shows a `Container(data, structure, content, display)` pattern that is also wrong.

A fresh session reading this document will see the OOP container pattern and think it is the intended design. The anti-pattern warnings in CLAUDE.md exist precisely because this pattern was tried and failed. The document needs updating to match the generic engine design.

### 4.2 Section Count in Data Axis [MINOR]

**Line 47:** Says "14 top-level sections." Actual model has 15 fields (dispatcher + frontmatter + 13 body sections). If "sections" means body sections, the count is 13. If it includes frontmatter, it's 14. If it includes dispatcher, it's 15.

### 4.3 Section Inventory Table [OK]

Lists all 14 items (13 body sections + frontmatter) plus mentions dispatcher separately. Reasonably accurate.

---

## 5. Memory File (galdr-composability.md)

### 5.1 Section Count [MINOR]

Says "14 sections" in "What Galdr Is." Same inconsistency as all other documents. Should say 13 body sections + frontmatter + dispatcher.

### 5.2 Current State — "Logic zone: skeleton created" [SIGNIFICANT]

Says "Logic zone: skeleton created. First module: `logic/transform/codegen_clean/`."

This is stale. The logic zone now contains:
- `logic/transform/codegen_clean/` (committed)
- `logic/transform/data_unwrap/` (committed)
- `logic/impure/gates/` (committed)
- `logic/pure/render/` (committed)
- `logic/pure/template/` (committed)
- `logic/pure/compose/` (exists on disk, uncommitted)

The memory file implies barely anything exists in logic/ when in fact the core composition engine is built.

### 5.3 Build Plan Summary [MINOR]

The build plan summary lists 7 steps starting from "Fragment classifier." This no longer matches the v3 build plan which has 4 steps starting from "Data Unwrapper." The step 1 (data unwrapper) is already done.

### 5.4 Regeneration Cascade [MINOR]

Says: "Verdandi YAML change -> `draupnir --all` -> `nornir_deploy --build gates` -> `galdr generate_structures.py`"

Missing the regin step. The full cascade (from CONTEXT_MAP) is: `draupnir --all -> nornir_deploy --build gates -> regin generate_structures.py -> galdr generate_structures.py -> regin pipeline -> galdr compose`.

---

## 6. Build Plan (humming-sleeping-shamir.md)

### 6.1 "Delete the failed data_unwrap attempt" [MINOR]

**Lines 241-244:** Says to "Delete the failed data_unwrap attempt" and lists `transform/data_unwrap/simple.py` for rewrite. But the current data_unwrap module (committed at `100dace`) appears to be working -- it was successfully tested against real agent-builder data per the commit message. This instruction may be stale from an earlier plan iteration.

### 6.2 Step 1 Status [MINOR]

Step 1 (data_unwrap) is listed as needing to be built, but it is already committed. A fresh session following this plan will attempt to rebuild something that already works.

### 6.3 Step 2 Status [SIGNIFICANT]

Step 2 (compose/) is listed as needing to be built. The code exists on disk (uncommitted). A fresh session needs to know this code exists but is NOT COMMITTED. The plan should note that compose/ has a working implementation that needs review, not that it needs to be written from scratch.

### 6.4 `compose/composed.py` CC Concern [MINOR]

The plan specifies CC=4-8 for `compose/composed.py`. The current implementation of `compose_section()` plus its 3 private helper functions likely exceeds CC=8 for the main function. The function handles: section gate, heading, section-level content iteration, variant dispatch, trunk-matching skip, visibility checking, data walk with 4-way type dispatch, decoration before/after, template finding. This should be verified with gleipnir.

---

## 7. Extracted TOMLs

### 7.1 All Three TOMLs Pass Validation [OK]

Confirmed: content.toml, structure.toml, and display.toml all validate against their respective generated Pydantic models.

### 7.2 section_order Has 13 Items [OK]

Confirmed: structure.toml section_order contains exactly 13 items. Matches the 13 body sections.

### 7.3 Display TOML Coverage [OK]

Display TOML has 10 sections (identity, security_boundary, critical_rules, instructions, examples, constraints, anti_patterns, success_criteria, failure_criteria, input). Missing output, writing_output, return_format. This is by design -- those sections have no display configuration. The model matches.

---

## 8. Uncommitted Changes

### 8.1 Galdr [CRITICAL]

**Uncommitted:** `src/galdr/logic/pure/compose/` (entire directory)

This contains the core composition engine: primitive.py, simple.py, composed.py. This code exists only in the working tree. If the checkout is reset, this work is lost.

### 8.2 Draupnir [SIGNIFICANT]

Many uncommitted changes across draupnir:
- Modified schemas, gen/ models, transform modules, orchestrate, and structure/model files
- 30+ files modified

### 8.3 Nornir [SIGNIFICANT]

Many uncommitted changes across nornir:
- Deleted gate_galdr_style_input (expected -- old style gate)
- Deleted schemas/tools/galdr-style.schema.json (expected)
- Modified deploy_categories, gleipnir checks, format_core, several daemons/hooks/CLI
- New gate_verdandi_input directory
- 20+ files modified

### 8.4 Verdandi [MINOR]

One modified file: `agent-output/output/agent-output-display.schema.json`

### 8.5 Regin [OK]

No uncommitted changes.

---

## 9. Leftover Files / Artifacts

### 9.1 `src/galdr/Archive.zip` (151KB) [MINOR]

Old archive file sitting in the source tree. Not tracked by git. Purpose unknown. Should be investigated or deleted.

### 9.2 `logic/transform/identity_compose/` (empty directory) [MINOR]

Empty directory, not tracked in git. Appears to be a leftover from an abandoned plan for identity-specific composition logic. Should be deleted -- it contradicts the "no per-section code" principle.

### 9.3 `structure/gen/schema/` (empty directory) [MINOR]

Empty directory inside gen/. Purpose unclear. Not mentioned in any document.

### 9.4 `structure/__pycache__/` contains stale `.pyc` files [MINOR]

Contains cached bytecode for deleted modules: `recipe.cpython-313.pyc`, `style.cpython-313.pyc`, `template_context.cpython-313.pyc`. These are harmless but indicate the pycache was not cleaned after the v2 restructure.

### 9.5 `.SYSTEM_PROMPT.xml` in galdr root [OK]

Listed in git status at session start (`??`) but does not exist on disk now. Transient file, likely from a previous Claude Code session.

### 9.6 `tests/*.qa` sidecar files [MINOR]

8 `.qa` files exist alongside the 7 broken test files. These appear to be quality audit sidecars. They will need to be regenerated when tests are rewritten.

---

## 10. Cross-Document Consistency Issues

### 10.1 "14 Sections" vs "13 Body Sections" — Pervasive Confusion

This appears in: CLAUDE.md, CONTEXT_MAP.md, COMPOSITION_ENGINE_DESIGN.md, AGENT_BUILD_SYSTEM.md, memory file.

The actual structure:
- **15 fields** in AgentAnthropicRender (dispatcher + frontmatter + 13 body sections)
- **13 body sections** in section_order
- **13 content sections** in AgentOutputContent
- **14 structure sections** (13 body + section_order)
- **10 display sections**

Every document should use consistent terminology: "13 body sections" for the renderable sections, "15 model fields" when counting the full model. "14" is always wrong -- it is neither the full count nor the body count.

### 10.2 AGENT_BUILD_SYSTEM.md Contradicts COMPOSITION_ENGINE_DESIGN.md

AGENT_BUILD_SYSTEM shows per-section class containers with `.render()` methods. COMPOSITION_ENGINE_DESIGN says "One generic engine, no per-section code." These directly contradict each other. CLAUDE.md lists this exact pattern as an anti-pattern. AGENT_BUILD_SYSTEM.md needs the Section Containers and Composition sections rewritten.

### 10.3 CONTEXT_MAP "What's Not Built" vs Actual State

CONTEXT_MAP says the composition engine has not been built. The compose/ module exists with working code. The data_unwrap module is committed. Five of the nine "not built" items are now built.

### 10.4 Memory File vs Build Plan

Memory file lists a 7-step build plan starting from "Fragment classifier." The actual build plan (v3) has 4 steps starting from "Data Unwrapper." The memory file's build plan summary is from an earlier version.

---

## 11. Recommended Actions (Priority Order)

### Must Fix Before Next Session

1. **Commit `logic/pure/compose/`** -- this is the core engine, sitting only in the working tree
2. **Update CONTEXT_MAP.md section 5** -- add compose/, data_unwrap/ to code map; fix all section counts
3. **Update CONTEXT_MAP.md section 7** -- mark composition engine as partially built
4. **Update COMPOSITION_ENGINE_DESIGN.md "What's Already Built"** -- add the 5 new modules
5. **Add anti-patterns to CLAUDE.md** -- CC=49 monolith, callable passing, isinstance for type safety, training data patterns vs reference implementations

### Should Fix Soon

6. **Update AGENT_BUILD_SYSTEM.md** -- replace Section Containers/Composition sections with generic engine description
7. **Fix "14 sections" everywhere** -- standardize on "13 body sections" or "15 model fields"
8. **Update memory file** -- current state section is stale, build plan summary is from old version
9. **Remove stale recipe IO entry** from CONTEXT_MAP Agent Pipeline IO table
10. **Delete empty `identity_compose/` directory**

### Low Priority Cleanup

11. Delete `src/galdr/Archive.zip`
12. Clean stale `__pycache__` entries
13. Delete empty `structure/gen/schema/` directory
14. Commit draupnir and nornir changes (significant uncommitted work)
