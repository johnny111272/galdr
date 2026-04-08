# Trunk Matching

## What It Solves

Data fields and content fields come from different models. Trunk matching is how the engine connects them — finding which content decorates which data, without a mapping table.

## The Trunk Concept

A "trunk" is the shared root name that connects fields across axes. A content field like `alpha_label` has trunk `alpha` — strip the positional suffix and what's left is the trunk. If a data field is also named `alpha`, they match. The content decorates the data.

This works because the naming convention ensures content fields are named `{data_field}_{suffix}`. The suffix says what role the content plays (label, postscript, declaration, etc.). The trunk says which data field it belongs to.

## Two Matching Mechanisms

### Decoration matching

Strip the positional suffix from a content field name to get the trunk. If the trunk matches a data field name, the content decorates that data field.

Example: `alpha_label` → trunk `alpha` → matches data field `alpha`. So `alpha_label` renders before the data value of `alpha`.

This works for: `_label`, `_postscript`, `_transition`, `_intro`, `_separator`, `_declaration`

### Placeholder matching

Content templates contain `{{placeholder}}` markers. If a placeholder name matches a data field name, the template consumes that data field.

Example: a template containing `{{alpha}}` references data field `alpha`. The template gets interpolated with the data value.

This works for: `_declaration` templates, heading templates, any content with `{{...}}` markers.

## What Doesn't Match = Standalone

After both matching passes, any content body field that wasn't matched to any data field is standalone content. It renders at the end of the body in content declaration order.

## The Critical Requirement

**Trunks must match exactly.** If a content field is `descriptive_name_for_alpha_postscript`, the trunk is `descriptive_name_for_alpha`, which does NOT match data field `alpha`. The content is orphaned — the engine can't connect it to its data.

This is a naming convention issue, not an engine issue. The fix is always in the schema: rename the content field so its trunk matches the data field.

See `TOML_ARCHITECTURE.md` for the full naming convention. See `review/` files for current trunk matching status per section — they flag every mismatch.
