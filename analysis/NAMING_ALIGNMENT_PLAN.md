# Naming Alignment Plan: Cross-Axis Mechanical Matching

## Purpose

Make field names mechanically matchable across all four axes (data, content, structure, display) so the galdr composition engine can derive cross-axis connections from field names alone — no heuristics, no mapping tables.

## The Mechanical Matching Rule

```
content:   {trunk}_label           → data:      {trunk}
content:   {trunk}_postscript      → structure: {trunk}_postscript_visible
display:   {trunk}_format          → data:      {trunk}  (the list it formats)
display:   {trunk}_format_threshold → pairs with {trunk}_format
structure: {field_name}_visible     → content:   {field_name}
```

Strip the positional suffix from a content field name → get the trunk → trunk maps to the data field and display format field. Template placeholders (`{{name}}`) use direct name lookup against data fields.

---

## Required Changes

### Group 1: Identity Data — Drop `role_` Prefix

The `role_` prefix on identity data fields breaks trunk matching against content/display.

**Verdandi source:** agent-builder YAML, identity section fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| `role_expertise` | `expertise` | content: `expertise_label`, display: `expertise_format` |
| `role_responsibility` | `responsibility` | content: `responsibility_label`, display: `responsibility_format` |

**Note on `role_identity` and `role_description`:** These are scalar template placeholders (`{{role_identity}}`, `{{role_description}}`) resolved by direct name lookup. Renaming them would require updating all content templates that reference them. Recommendation: **keep as-is** — they don't participate in trunk matching, only template interpolation. The `role_` prefix is acceptable for scalars used in templates since the template names the field explicitly.

**Cascade:** Verdandi YAML → Draupnir schemas → Nornir gates (agent-builder gates) → Regin generated models + pipeline code + all agent definition TOML files → Galdr generated models

**Agent definition impact:** Every agent definition TOML that has `[identity]` with `role_expertise` and `role_responsibility` fields needs updating. Check `~/.ai/spaces/bragi/definitions/agents/` for all `.toml` files.

---

### Group 2: Constraints Display — Match Data Field Name

Data calls the list `rules`. Display calls the format `enumeration_format`. No shared trunk.

**Verdandi source:** agent-output YAML, constraints display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| `enumeration_format` | `rules_format` | data: `rules` |
| `enumeration_format_threshold` | `rules_format_threshold` | pairs with `rules_format` |

**Cascade:** Verdandi YAML → Draupnir schemas → Nornir gates (output gates) → Galdr generated models + `extracted/display.toml`

---

### Group 3: Anti-Patterns Display — Match Data Field Name

Data calls the list `patterns`. Display calls the format `pattern_list_format`. Trunk mismatch (`patterns` vs `pattern_list`).

**Verdandi source:** agent-output YAML, anti_patterns display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| `pattern_list_format` | `patterns_format` | data: `patterns` |

**Cascade:** Same as Group 2.

---

### Group 4: Examples Content/Display — Match Data Field Name

Data calls the field `example_heading`. Content calls it `entry_heading`. Display calls it `entry_heading_format`.

**Verdandi source:** agent-output YAML, examples content and display fields

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| content: `entry_heading` | `example_heading` | data: `example_heading` (in ExampleEntry) |
| display: `entry_heading_format` | `example_heading_format` | content: `example_heading` |
| display: `entry_body_container` | `example_body_container` | consistency with `example_` prefix |
| display: `entry_separator` | `example_separator` | consistency |

**Cascade:** Same as Group 2.

---

### Group 5: Instructions Vocabulary — Align Terminology

Data uses `instruction_mode` with values `deterministic`/`probabilistic`. Content/structure/display all use `exact_vs_judgment` / `exact`/`judgment` terminology.

This is different from the other mismatches — the data field name and content field names serve different purposes. Data carries the semantic classification. Content carries the rendering terminology. But the vocabulary divergence means the engine can't derive one from the other.

**Two options:**

**Option A — Rename data enum values:** Change `deterministic` → `exact`, `probabilistic` → `judgment` in the verdandi `instruction_mode` enum. This makes the data vocabulary match content/structure/display. The data field stays `instruction_mode`, the values change.

**Option B — Rename content/structure/display fields:** Change all `exact_vs_judgment_*` fields to `deterministic_vs_probabilistic_*`. Longer but semantically precise.

**Recommendation:** Option A. The content/structure/display terminology (`exact`/`judgment`) is more intuitive for the agent reading the prompt. Making the data values match is the smaller change. The `instruction_mode` field name stays — only the enum values change.

**Cascade:** Verdandi YAML → all schemas → all gates → Regin models + pipeline code (any code that checks `InstructionMode.deterministic` or `.probabilistic`) → all agent definition TOMLs that declare instruction modes → Galdr content

---

### Group 6: Instructions Display — Align Scaffolding Terminology

Structure uses `structural_complexity_override`. Display uses `scaffolding_tier_*_activation_threshold`.

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| structure: `structural_complexity_override` | `scaffolding_tier` | display: `scaffolding_tier_*_activation_threshold` |

OR:

| Current | Rename To | Connects To |
|---------|-----------|-------------|
| display: `scaffolding_tier_lightweight_activation_threshold` | `structural_complexity_lightweight_threshold` | structure: `structural_complexity_override` |
| display: `scaffolding_tier_standard_activation_threshold` | `structural_complexity_standard_threshold` | structure: `structural_complexity_override` |

**Recommendation:** Rename structure field to `scaffolding_tier` — shorter, and `scaffolding_tier` is the more descriptive name for what it does.

**Cascade:** Verdandi YAML → schemas → gates → Galdr models + `extracted/structure.toml`

---

## Issues to Decide (Not Renames)

### `role_responsibility` Scalar-vs-List Anomaly

`role_responsibility` is typed as a single `RoleResponsibility` (StringProse) — a scalar. But display has `responsibility_format` with threshold-based switching, which only makes sense for lists.

**Options:**
1. Make `responsibility` a list type in verdandi (allows multiple responsibility statements)
2. Remove `responsibility_format` and `responsibility_format_threshold` from display (accept it's always scalar)
3. Keep both — the engine renders a single-item list using the format (works but odd)

**Recommendation:** Decide based on whether agents will ever have multiple responsibility statements. If yes, make it a list. If no, remove the display format fields.

### Input Section — No Content/Structure/Display Models

The `input` section exists in the data model but has no content, structure, or display counterpart. It doesn't participate in the composition pipeline.

**Options:**
1. Add input to all three output schemas (full composition pipeline participation)
2. Keep input as a data-only section with hardcoded rendering (simpler but inconsistent)
3. Defer — handle after the engine works for the other 12 sections

**Recommendation:** Option 3. Get the engine working first. Input can be added later.

### Content Fields Missing `_visible` Toggles

8 content fields have no corresponding structure `_visible` toggle:

| Section | Content Field | Always Renders? |
|---------|--------------|----------------|
| identity | `declaration_heuristic_postscript` | Currently yes |
| constraints | `hierarchy_tier_comparison` | Currently yes |
| constraints | `hierarchy_three_tier_explanation` | Currently yes |
| failure_criteria | `any_one_triggers_abort` | Currently yes |
| return_format | `report_completion_label` | Currently yes |
| return_format | `token_must_be_first_word_tokens_three` | Data-gated (3 tokens) |
| return_format | `token_must_be_first_word_tokens_two` | Data-gated (2 tokens) |
| examples | `group_framing_sentence` | Has toggle ✓ (was missing from count) |

**Recommendation:** Add `_visible` toggles for the first 5. The token fields are data-gated (mutually exclusive based on whether ABORT is a valid token), not visibility-toggled. Defer or handle as part of the input section work.

---

## Implementation Order

1. **Group 1** (identity data renames) — highest impact, touches verdandi agent-builder + all agent definitions
2. **Group 2** (constraints display) — verdandi agent-output only
3. **Group 3** (anti-patterns display) — verdandi agent-output only  
4. **Group 4** (examples content/display) — verdandi agent-output only
5. **Group 5** (instruction_mode enum values) — touches everything, do last
6. **Group 6** (scaffolding terminology) — small, structure + display

Groups 2-4 are all in agent-output and can be done together.

After all verdandi changes: full cascade — Draupnir → Nornir gates → Regin generate_structures → Galdr generate_structures → update `extracted/*.toml` files.

---

## Verification

After the cascade completes:

```bash
# Verify galdr models regenerate
cd ~/.ai/smidja/galdr && uv run python src/galdr/generate_structures.py

# Verify gates accept updated TOMLs
uv run python -c "
import gate_output_structure_input, gate_output_content_input, gate_output_display_input
for gate, path in [
    (gate_output_structure_input, 'extracted/structure.toml'),
    (gate_output_content_input, 'extracted/content.toml'),
    (gate_output_display_input, 'extracted/display.toml'),
]:
    result = gate.validate(path)
    print(f'{path}: {\"ok\" if result[\"ok\"] else \"FAIL: \" + result[\"error\"][\"message\"][:100]}')
"
```

Then verify mechanical matching works by inspecting generated model field names across axes.
