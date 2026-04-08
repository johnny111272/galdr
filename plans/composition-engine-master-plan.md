# Composition Engine — Master Plan

**Last updated:** 2026-04-05

---

## What's Done

### Schema & Naming (complete)
- Positional suffix alignment: all content fields have terminal suffixes declaring buffer slot
- Shared variants split into per-slot simple variants (`_h/_p/_b/_c_variant`)
- Instruction mode flat fields → sub-table group (D1 template table)
- `workspace_path` added to CriticalRules data model (cross-section fix)
- 163 files renamed in Verdandi, schemas regenerated, gates rebuilt

### Engine Core (complete)
- Suffix-based buffer classification: `has_heading_suffix`, `has_preamble_suffix`, `has_closing_suffix` → `buffer_slot_for_field`
- `populate_section_buffer` uses suffix routing, returns consumed variant names
- Shape classifier: `classify_trunk_shape` routes A/B/C/D1/D2/E
- `resolve_all_trunks` replaces `process_data_fields` — shape-based dispatch
- Generic D1 renderer via `instruction_mode` sub-table (step headers work)
- `collect_list_format` resolves display format with threshold pairs (value captured, dispatch deferred)

### Cleanup (complete)
- Dead code removed: 12 heuristic functions, 3 dead imports
- `is_nested_annotation` + `is_variant_annotation` merged → `is_basemodel_annotation`
- `collect_list_format` bug fixed (return value was discarded)
- primitive.py: 3 functions remain (suffix predicates only)

### Current Output
- 304 lines for agent-builder
- 7/7 instruction step headers rendered
- 0 Pydantic repr strings, 0 bare True/False
- Gate validation passes
- 8 unresolved `{{}}` placeholders

---

## What's Broken — 8 Unresolved Placeholders

### Category 1: Orphan body content (CriticalRules)

CriticalRules body is content-only prose fragments with NO data trunks. `resolve_all_trunks` walks DATA fields — these content fields are unreachable.

| Placeholder | Content field | Why unresolved |
|---|---|---|
| `{{tool_name}}` | `output_tool_exclusivity` | Orphan content + tool_name is None (has_output_tool=false) |
| `{{batch_size}}` | `batch_discipline` | Orphan content + int never unwrapped + batch_size is None |
| `{{rule_count}}` | `rule_count_awareness_preamble` | Orphan content + computed value doesn't exist |
| `{{workspace_path}}` | `workspace_confinement` | Orphan content (but data value NOW exists after schema fix) |

**What "orphan" means:** These 7 rule items are content fields gated by structure `_visible` toggles. They have no corresponding data trunk. The trunk resolver never sees them. They need a second pass: scan content body fields not consumed by heading/preamble/closing/decoration/D1/variants, render with visibility + interpolation, suppress if `{{}}` remains unresolved.

**Note:** For agent-builder (has_output_tool=false), `output_tool_exclusivity` and `batch_discipline` should be SUPPRESSED entirely — the data they reference doesn't exist. The suppress-on-incomplete mechanism handles this generically.

### Category 2: Computed values

| Placeholder | Section | What it needs |
|---|---|---|
| `{{rule_count}}` | critical_rules | Count of visible rules (orphan content fields with _visible=true) |
| `{{step_count}}` ×2 | instructions | `len(data.steps.root)` |
| `{{COUNT}}` | constraints | `len(data.rules.root)` |

These need values injected into `data_values` before composition. Two types:
- **List counts:** `steps` and `rules` are list fields — auto-generate `{field}_count`
- **Visible body count:** `rule_count` is the count of visible orphan body items — computed during buffer population

### Category 3: Per-item / nested rendering gaps

| Placeholder | Section | Issue |
|---|---|---|
| `{{TOOLS}}` | security_boundary | `grouped_tool_heading` is section-level but TOOLS comes from per-item aggregation |
| `{{context_label}}` `{{context_path}}` | input | Context is nested BaseModel (shape="nested"), skipped entirely |
| `{{example_heading}}` | examples | D2 renderer doesn't use content templates for per-entry headings |

### Category 4: Shape E variant framing (not a placeholder issue)

Success/failure criteria render via `render_structured_item` without per-item variant framing. The `_b_variant` fields should frame each criterion with the selected variant text.

---

## Remaining Work — Categorized

### Just wiring (mechanics exist, need connection)

| Item | What to do | Difficulty |
|---|---|---|
| List count injection | `unwrap_section_data` add `{field}_count` for list fields | Easy — add to data_unwrap |
| Format dispatch | `resolved_format` captured but always renders bulleted | Easy — dispatch to numbered/inline renderers |
| `{{workspace_path}}` in critical_rules | Data value exists now, just needs orphan body pass to render it | Blocked on orphan pass |

### New functionality needed

| Item | What to do | Difficulty |
|---|---|---|
| Orphan body content pass | Scan unconsumed content body fields, render with visibility + interpolation, suppress incomplete | Medium — new concept |
| Int/bool unwrap | `batch_size` (RootModel[int]) never enters data_values | Easy — add to data_unwrap |
| Visible body count | Count orphan body fields with _visible=true, inject as computed value | Medium — depends on orphan pass |
| Shape E variant framing | Per-item variant resolution using unconsumed `_b_variant` fields | Medium |

### Needs investigation first

| Item | What I'm unsure about |
|---|---|
| `{{TOOLS}}` | Is this actually broken? The entry template path does per-item interpolation. The `grouped_tool_heading` is separate — section-level aggregate. Need to verify. |
| `{{example_heading}}` | Should this use the content template at all? Maybe the raw heading text is correct and the template is wrong. |
| `{{context_label/path}}` | Context is shape "nested" (skipped). Is this a shape issue or should context be handled differently? |
| Other cross-section deps | Are there MORE data dependencies between sections? Need systematic audit. |
| Other orphan sections | Is CriticalRules the only section with content-only body items? |

---

## Proposed Next Steps

1. **Investigate** the "unsure" items above — verify before implementing
2. **Int/bool unwrap** — easy, standalone, unblocks batch_size for agents with output tools
3. **List count injection** — easy, standalone, resolves step_count and COUNT
4. **Orphan body content pass** — the big one, resolves all CriticalRules placeholders
5. **Format dispatch** — wire resolved_format to actual renderers
6. **Shape E variant framing** — per-item variant resolution for criteria
7. **Per-item/nested gaps** — TOOLS, example_heading, context (may need schema or architecture changes)
