# Session Handover — 2026-04-04 (Session 2)

## What Happened This Session

### Phase 1: Bug fixes (iterative, flawed approach)

Fixed 5 output bugs from the previous session:
- **Bug #5 (bare "False")** — `is_gate_annotation` now recognizes `RootModel[bool]` (e.g., `Boolean`). Gate fields correctly classified and skipped.
- **Bug #2 (unresolved templates)** — `interpolate` now does case-insensitive placeholder lookup (`.lower()` before dict.get).
- **Bug #1 (duplicate content)** — `find_data_driven_templates` identifies StringTemplates referencing data fields, skipped in content pass.
- **Bug #3 (nested model stringification)** — compound list detection, entry template rendering, structured item rendering, instruction step rendering all built. Zero Pydantic repr strings in output.
- **Section dividers** — `---` between sections.

**Problem:** This was done iteratively without reading the project documentation first. Trial-and-error, not plan-driven. Led to reactive CC decomposition and whack-a-mole debugging.

### Phase 2: Reorientation

Read the documentation that should have been read FIRST:
- `TOML_ARCHITECTURE.md` — field naming conventions, position suffixes, interface patterns
- `NAMING_CONVENTION_ANALYSIS.md` — cross-axis field alignment analysis
- `NAMING_ALIGNMENT_PLAN.md` — mechanical matching rules
- `CROSS_AXIS_NAMING_INVENTORY.md` — every field across all four axes

Key realization: the naming conventions already define how content fields are classified. The engine's Pass 2 was doing blacklist-based exclusion instead of using naming conventions for classification.

### Phase 3: Buffer model (Step 1)

Replaced the multi-pass approach (heading pass → content pass → data walk) with a **SectionBuffer model**:

```python
class SectionBuffer(BaseModel):
    heading: str | None = None
    preamble: tuple[str, ...] = ()
    body: tuple[str, ...] = ()
    postscript: tuple[str, ...] = ()
```

**`populate_section_buffer`** — single pass over content fields, classifies each by naming convention:
- `heading` → heading slot
- Variants → resolve, route to preamble or postscript
- Pass 3 operational (`_entry_template`, `step_header_*`, `*_body_prefix_*`, etc.) → skip
- Field-level decoration (suffix trunk matches data field) → skip
- Data-driven templates → skip
- Postscript content (`_postscript` suffix, `closing`/`closer`) → postscript slot
- Everything else → preamble slot

**Fixes:** Postscripts now appear AFTER body content (was before). Heading renders once (was in separate pass). Entry templates no longer leak into section prose.

### Phase 4: Trunk resolver design

Designed the trunk resolver — the component that replaces `process_data_fields` to populate the body slot. Full design in `TRUNK_RESOLVER_DESIGN.md`.

**Key findings from Opus research agents:**
- 57% of trunks have ZERO cross-axis pieces → detect shape first, collect only what's needed
- No trunk has `_visible` or `_override` toggles (those are decoration-level)
- Labels/postscripts only exist in identity section (currently)
- Entry template implies Shape C exclusively (no overlap with other shapes)
- Per-item variants only appear in Shape E (success/failure criteria)

**Five rendering shapes:**
- A: scalar text (57% of trunks)
- B: simple list (constraints, anti-patterns, expertise)
- C: templated entry list (security display, parameters)
- D: enum-discriminated items (instruction steps) / nested items (example groups)
- E: variant-framed items with sub-lists (success/failure criteria)

**Generic design requirements:**
- No per-section or per-field special rules
- Shape detection from annotation type + one optional content lookup
- D1 renderer finds Enum field by annotation, matches content templates by enum value
- E renderer finds per-item variants by elimination (buffer consumed section-level ones)
- Decoration gathering is universal (always, not per-shape)
- Overrides are item-level, handled inside shape renderers

### Phase 5: Schema fix

`role_responsibility_label` → `role_responsibility_declaration` in Verdandi agent-output YAML. Cascade completed by user. The field was misnamed as a `_label` (decoration) but was actually a template containing `{{role_responsibility}}`. Renaming eliminated the duplicate "Scope:" without engine special-casing. Confirms: when naming is correct, engine mechanisms don't overlap.

---

## Current State

### What exists and works

| Component | Status |
|-----------|--------|
| CLI (`cli.py`) | ✅ working |
| Gate loading (orchestrate.py) | ✅ working |
| SectionBuffer model | ✅ new, working |
| `populate_section_buffer` (composed.py) | ✅ new, passes guardrails |
| `process_data_fields` (composed.py) | ✅ working but will be replaced by trunk resolver |
| `compose_section` (assembled.py) | ✅ updated to use buffer |
| Compound list rendering | ✅ working (DisplayEntry, ParameterItem) |
| Instruction step rendering | ✅ working but hardcoded (to be genericized) |
| Structured item rendering | ✅ working (ExampleGroup, SuccessItem, FailureItem) |
| Pass 3 content skip predicates | ✅ working (`is_pass3_operational`, `is_body_consumed_content`) |
| Section dividers | ✅ working |

### Output quality (agent-builder)

- 314 lines (reference is 233)
- 0 Pydantic repr strings
- 0 bare True/False
- 7 unresolved `{{}}` — all computed values (`step_count`, `rule_count`, `batch_size`, `tool_name`, `workspace_path`, `COUNT`, `SCHEMA_PATH`)
- Postscripts correctly positioned after body
- "Scope:" appears once (was twice before schema fix)
- Some remaining issues with identity section duplicates (title in heading + data walk)

### Schema changes (Session 3 — 2026-04-04)

**Instruction mode content restructured:** Flat enum-keyed fields replaced with sub-table pattern.

**Old (10 flat fields):**
```
step_header_deterministic, step_header_probabilistic,
step_header_deterministic_n_only, step_header_probabilistic_n_only,
instruction_mode_body_prefix_deterministic, instruction_mode_body_prefix_probabilistic,
signal_at_mode_change_to_deterministic, signal_at_mode_change_to_probabilistic,
instruction_mode_explanation_mixed, instruction_mode_explanation_uniform_*
```

**New (2 sub-tables):**
- `instruction_mode` — group with 4 role sub-tables (`header`, `header_n_only`, `body_prefix`, `signal_at_mode_change`), each keyed by enum values (`deterministic`, `probabilistic`). Same pattern as `framing_variant` and `abort_stance_variant`.
- `instruction_mode_explanation_variant` — simplegroup keyed by mode composition (`mixed`, `uniform_deterministic`, `uniform_probabilistic`). Data-driven selector.

**Why:** The D1 renderer previously needed substring scanning to find position markers embedded in flat field names. The sub-table structure makes position information explicit — each role sub-table IS a position. The engine resolves D1 items the same way it resolves shared variants: find the content sub-table, iterate roles, look up enum value.

Schema cascade: verdandi YAML → draupnir → galdr generate_structures. Content TOML updated. All regenerated.

### What needs building (trunk resolver)

The trunk resolver replaces `process_data_fields`. Design in `TRUNK_RESOLVER_DESIGN.md`. Implementation involves:

1. **Shape detection** — classify each data field's annotation → A/B/C/D/E
2. **Decoration gathering** — universal, `find_decoration` for every trunk
3. **Shape-specific collection** — only gather what that shape needs
4. **Generic renderers** — D1 uses content sub-table (role sub-tables keyed by enum value), E uses remaining-variant resolution
5. **Replace `process_data_fields`** — the assembled-level wiring calls the resolver per trunk

### What needs building (other)

- Computed values enrichment (`step_count`, `rule_count`, etc.) — rendering-time computation
- Cross-section data injection (`workspace_path` into critical_rules)
- Input section nested model handling (context is nested BaseModel, currently skipped)
- Frontmatter rendering (separate path)
- Dispatcher rendering (separate path)

---

### Positional suffix alignment — Completed (Session 3)

163 files changed in Verdandi. Every content field now has a terminal positional suffix declaring its buffer slot. Shared variants split into per-slot simple variants. `_x_variant` slot letters added. Engine code still uses old heuristic classification — Phase 2 updates suffix-based classification.

Full suffix convention documented in `CONTEXT_MAP.md` §7 and in memory file `feedback_positional_suffixes.md`.

---

## Key Design Documents

| Document | What |
|----------|------|
| `TRUNK_RESOLVER_DESIGN.md` | Full resolver design: funnel, shapes, D1 sub-table pattern, renderers, co-occurrence |
| `COMPOSITION_ENGINE_DESIGN.md` | Original engine design (still valid for overall architecture) |
| `CONTEXT_MAP.md` §7 | Positional suffix convention, current known issues, active work status |
| `TOML_ARCHITECTURE.md` | Field naming conventions — **needs update** for new suffixes |
| `analysis/NAMING_CONVENTION_ANALYSIS.md` | Cross-axis alignment analysis — **outdated** (references pre-rename field names) |

---

## Warnings for Next Session

1. **Read TRUNK_RESOLVER_DESIGN.md BEFORE coding.** It has the shape detection tree, co-occurrence rules, skip table, and renderer signatures. Don't redesign from scratch.

2. **The resolver must be GENERIC.** No per-section rules, no hardcoded field names. Shape detection from annotations, content matching by naming convention. This is the entire point.

3. **Decoration is separate from shape rendering.** Labels introduce data (rendered before). Templates contain data (rendered as the value). `_label` never contains `{{trunk}}` — if it does, the naming is wrong (schema fix needed, not engine special-casing).

4. **`process_data_fields` still works** as the body populator. The trunk resolver replaces it but the existing code is functional. Don't delete it until the resolver is verified.

5. **Run the engine after EVERY change.** Previous session degraded because code was written and declared done without running. The test command:
   ```bash
   cd /Users/johnny/.ai/smidja/galdr && uv run galdr \
     ~/.ai/spaces/bragi/definitions/agents/agent-builder/anthropic_render.toml \
     -o staging/agent-builder-test.md
   ```
