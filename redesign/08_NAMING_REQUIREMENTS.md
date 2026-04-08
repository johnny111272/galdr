# Naming Requirements

## Why Naming Is Mechanical, Not Cosmetic

The composition engine uses field names as its primary mechanism. The terminal suffix determines the buffer slot. The trunk determines which data field a content field decorates. The placeholder name determines template interpolation. Wrong names don't just look bad — they cause wrong rendering, orphaned content, or silent suppression.

Every naming convention must hold simultaneously for the engine to work without heuristics or special cases.

## The Three Naming Rules

### 1. Every content field has a terminal positional suffix

The suffix declares the buffer slot. The full suffix table is in `TOML_ARCHITECTURE.md` — that is the single source of truth for which suffixes exist and what they mean. Fields without a recognized buffer-slot suffix go to body by default — this covers D1 template tables (BaseModel fields named after enum fields) and any standalone content using the explicit `_body` suffix.

### 2. Content trunks match data field names exactly

For content that decorates a data field, strip the positional suffix and the remaining trunk must exactly match the data field name. `alpha_label` decorates data field `alpha`. If the trunk doesn't match, the content is orphaned.

### 3. Template placeholders match data field names

Content templates with `{{placeholder}}` markers get interpolated from data values. The placeholder name (case-insensitive) must match a data field name. If it doesn't match, the placeholder stays unresolved and the content gets suppressed.

## What Happens When Names Are Wrong

- **Missing suffix:** The engine can't determine the buffer slot. The field either goes to a wrong slot or gets lost.
- **Trunk mismatch:** Content meant to decorate a data field becomes standalone. It renders at the wrong position or not at all.
- **Placeholder mismatch:** Templates retain literal `{{...}}` text and get suppressed by the resolver.

Every case is a schema fix, not an engine fix. Rename the field to follow the convention.

## Where to Check Current Status

The `review/` directory has per-section field inventories that flag every naming issue with ✅❌⚠️ indicators. These are the ground truth for what's currently aligned and what needs fixing.
