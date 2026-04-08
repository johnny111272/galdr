# Body Ordering

## The Problem

The body slot has two input streams: data fields and content fields. Both contribute to the body, but they come from different models with different field orders. The body ordering rules determine how they interleave.

## Data Drives Order

The data model's field declaration order IS the body rendering order. Content attaches to data — not the other way around.

For each data field (in declaration order):
- Find all content that decorates it (by trunk matching — the shared root name connects them)
- The decorations have a natural order: transition before, label before, the data itself, postscript after
- Each of these becomes a separate bundle, each independently resolved

This means if the data model declares `field_alpha` before `field_bravo`, then `field_alpha` and all its decorations render before `field_bravo` and all its decorations. To change the body order, change the data model's field order.

## Trunk Matching Links Content to Data

A content field like `field_alpha_label` has trunk `field_alpha` (strip the `_label` suffix). If that matches data field `field_alpha`, the content decorates that data. The decoration ordering around a data field follows the suffix convention:

- `_transition` renders first (pre-label, bridges from the previous field)
- `_label` renders next (introduces the data)
- `_declaration` or the data value itself renders next
- `_postscript` renders last (reinforces what was just shown)

Each decoration is its own bundle with its own visibility toggle. A label can be visible while the postscript is hidden.

## Standalone Content Comes Last

After all data-driven bundles, any content body field that didn't match any data field renders at the end, in content declaration order. These are standalone prose — content that exists in the body but isn't tied to a specific data field.

## Compound Data

When a data field contains a list of structured items (nested groups, enum-discriminated items, variant-framed items), the entire list is one bundle. The specialized renderer handles per-item iteration internally. Decorations still wrap the whole list: label before the list, postscript after.

## Gates and Nested Models

Boolean and enum data fields that serve as gates produce no output — they're skipped during body ordering. Their VALUES may be used by the resolver (for visibility decisions), but they don't generate bundles.

Nested BaseModel fields (e.g., context resources within input) are handled by a different mechanism outside the normal body flow.
