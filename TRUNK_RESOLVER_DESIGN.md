# Trunk Resolver Design

## What This Document Is

The design for the trunk resolver — the component that processes each data field through shape detection, targeted collection, and rendering to produce body slot entries in the SectionBuffer.

This replaces the current `process_data_fields` in `composed.py`.

---

## Critical Finding: Shape-First, Not Collect-First

The original design assumed a wide collection stage (gather everything per trunk) followed by narrowing. Analysis of the actual data shows this is inverted:

**57% of trunks (16/28) have ZERO cross-axis pieces.** No label, no format, no visibility toggle, no override, no entry template, no variants. They're naked scalars consumed by content templates.

**The optimal order is: detect shape FIRST (from data type alone, zero cross-axis lookups), THEN collect only the pieces that shape needs.**

This reduces average lookups per trunk from ~11 to ~2.

### Key Mutual Exclusivity Rules

| Rule | Implication |
|------|-------------|
| Scalar data → Shape A | Skip ALL cross-axis lookups except content template scan |
| Entry template found → Shape C | Skip decoration, format, variants |
| Format exists → Shape B or E only | Skip format for A, C, D |
| Per-item variants → Shape E only | Skip variant lookups for A, B, C, D |
| Labels/postscripts → identity section only | Skip decoration outside identity |
| No trunk has `_visible` or `_override` | Visibility/override are decoration-level, not trunk-level |

---

## The Funnel (Not an Hourglass)

The original design assumed wide collection → narrow resolution. Analysis shows the flow is actually a **funnel** — narrow early, stay narrow:

```
    CLASSIFY: type-only (zero cross-axis lookups)
    ┌───────────────┐
    │  annotation    │
    │  ↓             │
    │  gate? ────────│──→ skip
    │  nested? ──────│──→ skip
    │  scalar? ──────│──→ Shape A (57% of trunks exit here)
    │  list items?   │
    │  ├─ scalar ────│──→ Shape B
    │  └─ BaseModel ─│──→ need one content check
    └───────┬───────┘
            │
    DISAMBIGUATE: one content lookup
    ┌───────┴───────┐
    │  entry_template│
    │  found? ───────│──→ Shape C
    │  not found?    │
    │  ├─ enum? ─────│──→ Shape D1
    │  ├─ BM sub? ───│──→ Shape D2
    │  └─ scalar sub?│──→ Shape E
    └───────┬───────┘
            │
    COLLECT: only what this shape needs
    ┌───────┴───────┐
    │  A: decoration │  (identity only)
    │  B: format     │  + decoration
    │  C: template   │  (already found)
    │  D: headers    │  from content
    │  E: variants   │  + format + framing
    └───────┬───────┘
            │
    RENDER: shape-specific
    ┌───────┴───────┐
    │  A ──→ text    │
    │  B ──→ list    │
    │  C ──→ entries │
    │  D ──→ headed  │
    │  E ──→ framed  │
    └───────┬───────┘
            │
    ┌───────┴───────┐
    │  append body   │
    └───────────────┘
```

Most trunks exit at the first stage. Only compound BaseModel lists need the content lookup. Only Shape E needs variant resolution.

---

## Co-Occurrence Matrix (Actual Data)

What cross-axis pieces ACTUALLY EXIST for each trunk:

| Trunk | Shape | Label | Postscript | Entry Tmpl | Format | Threshold | Per-Item Variants |
|-------|-------|-------|------------|------------|--------|-----------|-------------------|
| title | A | — | — | — | — | — | — |
| description | A | — | — | — | — | — | — |
| role_identity | A | — | PST | — | — | — | — |
| role_responsibility | A | LBL | — | — | — | — | — |
| role_description | A | — | — | — | — | — | — |
| role_expertise | B | LBL | PST | — | FMT | THR | — |
| workspace_path | A | — | — | — | — | — | — |
| display (sec.boundary) | C | — | — | TPL | — | — | — |
| parameters | C | — | — | TPL | — | — | — |
| steps | D1 | — | — | — | — | — | — |
| groups | D2 | — | — | — | — | — | — |
| rules (constraints) | B | — | — | — | FMT | THR | — |
| patterns | B | — | — | — | FMT | — | — |
| criteria (success) | E | — | — | — | FMT | THR | VAR (3 tables) |
| criteria (failure) | E | — | — | — | FMT | — | VAR (1 table) |

**57% of trunks have zero cross-axis pieces.**

### Skip Table: What Each Shape Can Skip

| Lookup | A | B | C | D1 | D2 | E |
|--------|---|---|---|----|----|---|
| Decoration (label/postscript) | identity only | identity only | SKIP | SKIP | SKIP | SKIP |
| Entry template scan | SKIP | SKIP | USE | already checked | already checked | already checked |
| Display format | SKIP | USE | SKIP | SKIP | SKIP | USE (evidence) |
| Display threshold | SKIP | USE | SKIP | SKIP | SKIP | USE (evidence) |
| Variant selectors | SKIP | SKIP | SKIP | SKIP | SKIP | USE |
| Variant tables | SKIP | SKIP | SKIP | SKIP | SKIP | USE |

---

## Stage 1: Collection (Shape-Targeted)

After shape detection, collect ONLY the pieces that shape needs:

### Shape A collection (scalars — 57% of trunks)
- Decoration: `find_decoration(trunk, content)` — only needed for identity section
- Content template: already identified by `find_data_driven_templates`
- **Skip everything else**

### Shape B collection (simple lists)
- Decoration: `find_decoration(trunk, content)` — only identity section
- Format: `getattr(display, trunk + "_format")`
- Threshold: `getattr(display, trunk + "_format_threshold")`

### Shape C collection (templated lists)
- Entry template: already found during shape detection
- **Skip decoration, format, variants**

### Shape D collection (headed paragraphs)
- Step headers from content (D1) or group/entry structure from content (D2)
- **Skip format, variants**

### Shape E collection (definition + evidence)
- Variant selectors from structure: `definition_framing_variant`, `evidence_framing_variant`, `definition_to_evidence_transition_variant`
- Variant tables from content: matching sub-tables
- Evidence format: `getattr(display, "evidence_format")`
- Evidence threshold: `getattr(display, "evidence_format_threshold")`

### No TrunkBundle model needed

The original design proposed a `TrunkBundle` with 12 fields. Analysis shows:
- `visible` and `override_active` are always True/False (no trunk has `_visible` or `_override`)
- Most fields are None for most trunks
- Each shape needs a DIFFERENT subset

Instead of collecting everything into one model: **the shape-specific collection functions return only what the corresponding renderer needs.** No bundle, no wasted fields, no `Any` types.

---

## Stage 2: Shape Detection (The Decision Tree)

Shape detection uses ONLY the data annotation type + one optional content lookup. Zero structure/display lookups.

```
1. is_gate_annotation? ──→ skip (extract value for gate dict)
2. is_nested_annotation? ──→ skip (handled by orchestrate)
3. is_scalar_rootmodel? ──→ Shape A  (majority exit here)
4. is_list of scalar RootModels? ──→ Shape B
5. --- list of BaseModels from here ---
6. entry_template found in content? ──→ Shape C
7. item has Enum discriminator? ──→ Shape D1 (steps)
8. item has nested BaseModel sub-list? ──→ Shape D2 (examples)
9. item has scalar sub-list? ──→ Shape E (criteria)
10. fallback ──→ Shape D2
```

Steps 1-4 are type-only checks (zero lookups). Step 6 is the only cross-axis check. Steps 7-9 are item type introspection.

### Visibility and Override — Not Trunk-Level

Analysis revealed: **no trunk has a `{trunk}_visible` or `{trunk}_override` toggle.** All `_visible` toggles in structure.toml control content decoration fields (preambles, postscripts, closing prose). All `_override` flags control per-group data values (example_display_headings).

These are handled in the buffer population (preamble/postscript visibility) and inside structured item rendering (override substitution), not in the trunk resolver.

---

## Stage 3: Rendering (Five Generic Shapes)

Every renderer is generic — it knows about field TYPES and NAMING CONVENTIONS, never about specific sections or field names.

### Shape A: Scalar Text

**Resolver provides:** interpolated text string, decoration dict
**Renderer:** wrap with decoration (label before, postscript after), output text

### Shape B: Simple List

**Resolver provides:** list of scalar strings, resolved format enum, decoration dict
**Renderer:** format list (bulleted/numbered/inline), wrap with decoration

### Shape C: Templated Entry List

**Resolver provides:** list of interpolated entry strings, resolved format enum
**Renderer:** format list, wrap with decoration

### Shape D1: Enum-Discriminated Items (generic — not instruction-specific)

**Detection:** list of BaseModels where item type has an Enum annotation field.

**Content schema pattern:** The content section contains a sub-table named after the enum field (e.g., `instruction_mode`). This sub-table is a group containing role sub-tables (`header`, `body_prefix`, etc.), each keyed by the enum values (`deterministic`, `probabilistic`). This is structurally identical to the shared variant pattern used by `framing_variant` and `abort_stance_variant`.

**Generic mechanism:**
1. Find the Enum field by scanning item type's `model_fields` annotations
2. Find the matching content sub-table by enum field name (BaseModel annotation, not a string)
3. The sub-table's fields are role sub-tables. Each role is a BaseModel with enum values as keys.
4. For structure-selected roles (e.g., `header` vs `header_n_only`), the structure selector picks which role to use
5. Find the text body field(s) by scanning item type for non-Enum scalar RootModel fields
6. For each item:
   a. Extract the Enum value (e.g., "deterministic")
   b. Look up that value in each active role sub-table → get the template text
   c. Interpolate templates with per-item computed values (index, total)
   d. Extract body text from non-Enum fields
7. Render: role templates in declaration order + body text

**Why this is generic:** The renderer finds an Enum field, finds a content sub-table with the same name, iterates its role sub-tables, and looks up the enum value in each. It never references "steps", "instructions", or "modes". Any section with an enum-discriminated list and a matching content sub-table would work the same way.

**Structure-selected roles:** When a sub-table group has peer roles that are alternatives (e.g., `header` and `header_n_only`), a structure selector picks which one to use. The engine detects this by finding multiple role sub-tables with a shared prefix and a structure field that selects between them (e.g., `step_index_tracking = "n_of_m" | "n_only"`). Only the selected role renders.

**Computed per-item values:** The renderer iterates items and injects index-based values. Standard names: `item_n` (1-based index), `item_total` (count). Content templates reference these via `{{step_n}}` etc. — the case-insensitive interpolation matches.

### Shape D2: Nested-List Items (generic — not example-specific)

**Detection:** list of BaseModels where item type has a sub-list field containing BaseModel items.

**Generic mechanism:**
1. Walk item fields by annotation:
   - Scalar RootModel with `_name` or `_heading` suffix → render as heading (H3 for top, H4 for nested)
   - Scalar RootModel without name suffix → render as paragraph text
   - Boolean/Enum gate fields → skip (gate, not content)
   - List of BaseModels → recurse: render each sub-item's fields the same way
   - List of scalar RootModels → render as bulleted list
2. Heading level determined by nesting depth, not by field name

**Why this is generic:** The renderer walks the item's field structure. It doesn't know about "example groups" or "entries." Any section with a nested-list compound item would work the same way.

### Shape E: Scalar + Sub-List Items with Variant Framing (generic — not criteria-specific)

**Detection:** list of BaseModels where item type has scalar fields + a sub-list of scalars, AND the content section has per-item variant sub-tables.

**Generic mechanism:**
1. Find all variant sub-tables in the content section (BaseModel annotations) that were NOT consumed by buffer population (section-level variants were already consumed — remaining ones are per-item)
2. For each variant: look up the matching selector from structure (same-name convention)
3. Resolve each variant text by selector value
4. For each item:
   a. Unwrap scalar fields to strings
   b. Interpolate variant framing texts with item field values (e.g., `{{DEFINITION}}` → definition text, resolved by case-insensitive interpolation matching field names)
   c. Unwrap sub-list items to strings
   d. Format sub-list per display format
5. Render: framing texts (in content declaration order) interleaved with item data

**Why this is generic:** The renderer finds remaining variants by annotation (not by name), resolves them by structure selector (same-name convention), and interpolates with item field names (case-insensitive). Any section with scalar+sub-list items and per-item variant framing would work the same way.

**How "remaining variants" works:** Buffer population consumes section-level variants. It marks consumed variants by their content field names. The body resolver sees which variant fields were NOT consumed — these are per-item. This replaces `is_per_item_variant` (an explicit name set) with a generic detection: variant that the buffer didn't use = per-item variant.

---

## Data Fields → Shape Mapping (Verification, Not Code)

This table verifies the generic detection works for all current fields. The resolver does NOT use this table — it discovers shapes from annotations and naming conventions.

| Section | Trunk | Shape | Notes |
|---------|-------|-------|-------|
| identity | title | A | template: `"AGENT: {{title}}"` (consumed by heading, skipped in body) |
| identity | description | A | bare scalar |
| identity | role_identity | A | template: `"You are a {{role_identity}}."` (consumed by heading/preamble templates) |
| identity | role_responsibility | A | template: `"**Scope:** {{role_responsibility}}"` |
| identity | role_description | A | bare prose block |
| identity | role_expertise | B | format: bulleted/inline per threshold |
| security_boundary | workspace_path | A | template in framing_variant (consumed by preamble) |
| security_boundary | display | C | entry template: `"{{PATH}} -- {{TOOLS}}"` |
| critical_rules | has_output_tool | gate | skip — gate value only |
| critical_rules | tool_name | A | consumed by preamble templates |
| critical_rules | batch_size | A | consumed by preamble templates |
| input | description | A | template |
| input | format | A | template |
| input | parameters | C | entry template: `` "`{{param_name}}` ({{param_type}})..." `` |
| input | context | nested | skip — needs orchestrate-level recursion |
| instructions | steps | D1 | mode-dependent step headers |
| examples | groups | D2 | group heading + entries |
| constraints | rules | B | format: bulleted/numbered per threshold |
| anti_patterns | patterns | B | format per display |
| success_criteria | criteria | E | definition + evidence with variant framing |
| failure_criteria | criteria | E | same pattern |
| output | description | A | template: `"You produce: {{DESCRIPTION}}"` |
| output | format | A | template: `"Output format: {{FORMAT}}"` |
| output | schema_path | A | template |
| output | output_directory | A | template in variant |
| return_format | mode | gate | skip — drives conditional rendering |
| return_format | status_instruction | A | bare prose |
| return_format | metrics_instruction | A | bare prose |

### Observations

1. **Shape A dominates** — most data fields are scalars consumed by content templates. Many of these are already consumed by preamble templates (role_identity in declaration, workspace_path in framing_variant). The body resolver needs to know: was this scalar already consumed by a preamble template? If yes, skip it in the body walk. `find_data_driven_templates` handles this.

2. **Shapes B and C** are straightforward — existing code handles them correctly.

3. **Shape D** has two sub-types with different rendering needs but similar structure (list of items → headed paragraphs).

4. **Shape E** is the only shape that needs per-item variant framing — limited to success_criteria and failure_criteria.

5. **Several data fields are consumed by preamble/heading**, not body. `title` goes into the section heading. `role_identity` goes into the `declaration` template in preamble. `workspace_path` goes into the `framing_variant` preamble. The body resolver should skip these — they're already rendered.

---

## Resolution Sequence Diagram

```
collect_trunk_bundle(trunk, data, content, structure, display, data_values)
    │
    ▼
is gate? ──── yes ──→ extract gate value, return None
    │ no
    ▼
is visible? ── no ──→ return None
    │ yes
    ▼
is override? ─ yes ─→ substitute data_value
    │ no
    ▼
already consumed by preamble? ── yes ──→ return None
    │ no
    ▼
classify shape (A/B/C/D/E)
    │
    ├── A ──→ render_scalar(template_text or bare_value, decoration)
    ├── B ──→ render_simple_list(items, format, decoration)
    ├── C ──→ render_templated_list(item_dicts, template, format, decoration)
    ├── D ──→ render_headed_list(items, content_section, ...)
    └── E ──→ render_framed_items(items, variant_framing, evidence_format, decoration)
    │
    ▼
return rendered_text ──→ append to body slot
```

---

## Renderer Input Signatures

### Common wrapper (all shapes)

Every shape's rendered content gets wrapped with decoration:
```
[decoration_before] + [rendered_content] + [decoration_after]
```

Decoration (label, postscript, etc.) comes from `find_decoration(trunk, content)`. The wrapping is done by the resolver after the shape renderer returns.

### Shape A: render_scalar
```
text: str                    # interpolated template text or bare value
```
Returns: str

### Shape B: render_formatted_list
```
items: list[str]             # scalar strings peeled from RootModels
format: str                  # resolved format enum
```
Returns: str (formatted list)

### Shape C: render_formatted_list (same renderer as B)
```
entries: list[str]           # interpolated entry strings
format: str                  # resolved format enum
```
Returns: str (formatted list)

### Shape D1: render_enum_discriminated_items
```
items: list[BaseModel]                  # the raw items
enum_field_name: str                    # discovered Enum field name
mode_content: BaseModel                 # the content sub-table (group of role sub-tables)
active_roles: list[str]                 # role names to render (after structure selection)
data_values: dict[str, str]             # for interpolation
```
Returns: list[str] (one rendered paragraph per item)

### Shape D2: render_nested_items
```
items: list[BaseModel]       # the raw items
content_section: BaseModel   # for group framing, entry templates
data_values: dict[str, str]  # for interpolation
heading_depth: int           # starting heading level (H3 for top)
```
Returns: list[str] (one rendered block per item)

### Shape E: render_variant_framed_items
```
items: list[BaseModel]               # the raw items
resolved_framings: list[str]         # variant-resolved framing texts
evidence_format: str                 # resolved format for sub-lists
data_values: dict[str, str]          # for interpolation
```
Returns: list[str] (one rendered block per item)

---

## Implementation Approach

### Step 1: TrunkBundle model
Frozen Pydantic model in `structure/model/`. Holds all collected pieces.

### Step 2: collect_trunk_bundle function
Simple/composed level. Mechanical lookups by naming convention.

### Step 3: resolve_trunk function
Composed level. The hourglass — applies gate/visibility/override/shape decisions.

### Step 4: Shape renderers
Mostly exist already. Shape E needs the variant framing addition.

### Step 5: Replace process_data_fields
The assembled-level wiring: iterate data fields → collect → resolve → append to body.

---

## Eliminating Per-Section Knowledge

Three mechanisms that WERE per-section become generic:

### 1. `is_per_item_variant` → "remaining variants"

**Old:** Explicit name set `{"definition_framing_variant", "evidence_framing_variant", ...}`

**New:** Buffer population tracks which variant sub-tables it consumed (section-level). Any variant in the content section NOT consumed by the buffer is per-item. Detection by elimination, not by name.

**Implementation:** `populate_section_buffer` returns both the buffer AND a set of consumed variant names. The body resolver checks `is_variant_annotation` on content fields — if the name is NOT in the consumed set, it's a per-item variant for Shape E.

### 2. `render_instruction_steps` → generic enum-discriminated renderer

**Old:** Hardcoded `instruction_mode` field name and `step_header_` prefix matching.

**New (schema change completed):** The content schema now uses a sub-table pattern. `instruction_mode` is a group containing role sub-tables (`header`, `header_n_only`, `body_prefix`, `signal_at_mode_change`), each keyed by enum values (`deterministic`, `probabilistic`). The engine finds the Enum field by annotation, finds the matching content sub-table by name, and iterates role sub-tables. No substring scanning, no position-marker detection — the sub-table structure IS the position information. This is the same pattern as `framing_variant` and `abort_stance_variant`.

**Also changed:** `instruction_mode_explanation_variant` is now a variant sub-table keyed by mode composition (`mixed`, `uniform_deterministic`, `uniform_probabilistic`). The selector is computed from data (are modes mixed or uniform), not from structure.

### 3. `render_structured_item` → generic nested-item renderer

**Old:** Hardcoded `_name`/`_heading` suffix for heading detection.

**New:** Same suffix convention, but it IS generic — the convention applies to any field in any section. `_name` → title-like → heading. This isn't per-section knowledge, it's a TOML naming convention.

---

## What Already Exists and Can Be Reused

| Function | File | Reuse |
|----------|------|-------|
| `find_decoration` | simple.py | Trunk-based decoration lookup ✓ |
| `render_content_text` | simple.py | Template interpolation ✓ |
| `render_bulleted` | render/simple.py | List formatting ✓ |
| `render_entries_from_dicts` | simple.py | Templated entry rendering ✓ |
| `unwrap_item_fields` | composed.py | Per-item field extraction ✓ |
| `render_instruction_steps` | composed.py | Shape D1 renderer ✓ |
| `render_structured_item` | composed.py | Shape D2/E base (needs variant addition for E) |
| `render_decoration_before` | composed.py | Decoration assembly ✓ |
| `render_decoration_after` | composed.py | Decoration assembly with visibility ✓ |
| `classify_data_annotation` | composed.py | Gate/scalar/list/nested classification ✓ |
| `resolve_format_pair` | simple.py | Threshold-based format resolution ✓ |
