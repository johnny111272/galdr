# Identity Section — Four-Axis Review

## Data (IdentityAnthropic)

```
IdentityAnthropic
  .title             AgentTitle (TitleString scalar)
  .role_identity     StringText (scalar)
  .role_responsibility  RoleResponsibility (StringProse scalar)
  .role_description  RoleDescription (StringProse scalar, optional)
  .role_expertise    RoleExpertise (list of StringText, optional)
```

Agent-builder has all fields populated. `role_expertise` has 4 items. `role_description` is present but has no content template.

## Content (IdentityContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `heading` | StringTemplate | (no suffix — IS the heading) | heading | `"AGENT: {{title}}"` |
| ✅ | 2 | `role_identity_declaration` | StringTemplate | `_declaration` | body | `"You are a {{role_identity}}."` |
| ❌ | 3 | `role_identity_declaration_heuristic_postscript` | StringTemplate | `_postscript` | body | `"...what would a {{role_identity}} do?"` — trunk `role_identity_declaration_heuristic` doesn't match data field `role_identity` |
| ✅ | 4 | `role_responsibility_declaration` | StringTemplate | `_declaration` | body | `"**Scope:** {{role_responsibility}}"` |
| ✅ | 5 | `role_expertise_label` | StringText | `_label` | body | `"**Your judgment is authoritative in:**"` |
| ❌ | 6 | `role_expertise_is_strictly_limited_postscript` | StringProse | `_postscript` | body | `"Your expertise is strictly limited to the areas listed above."` — trunk `role_expertise_is_strictly_limited` doesn't match data field `role_expertise` |
| ✅ | 7 | `identity_reminder_closing` | StringTemplate | `_closing` | closing | `"Remember: you are a {{role_identity}}."` |

## Structure (IdentityStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `field_ordering` | IdentityFieldOrdering (enum) | `"identity_first"` | Field render order within section |
| ⚠️ | 2 | `fuse_role_identity_declaration_and_role_description` | Boolean | `false` | Merge declaration + description — role_description has no content template anyway |
| ✅ | 3 | `role_identity_declaration_heuristic_postscript_visible` | Boolean | `true` | → content #3 |
| ✅ | 4 | `role_expertise_is_strictly_limited_postscript_visible` | Boolean | `true` | → content #6 |
| ✅ | 5 | `identity_reminder_closing_visible` | Boolean | `false` | → content #7 |
| ⚠️ | 6 | `bold_contrast_phrase_from_role_description_visible` | Boolean | `false` | → role_description rendering — role_description has no content template |

## Display (IdentityDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `role_expertise_format` | FormatPair | `["bulleted", "inline"]` | → data.role_expertise list format (bulleted above threshold, inline at/below) |
| ✅ | 2 | `role_expertise_format_threshold` | Integer | `3` | → switch at 3 items (4 items → bulleted) |

---

## Rendering Order

```
HEADING:
  ✅ heading                                "AGENT: {{title}}"
                                             ← data.title

PREAMBLE:
  (none for identity)

BODY (in data field order):
  ⚠️ data.title                             SCALAR — consumed by heading template, may render again in body
  ✅ data.role_identity                      SCALAR
       ✅ role_identity_declaration            "You are a {{role_identity}}."
       ❌ role_identity_declaration_heuristic_postscript
                                             "...what would a {{role_identity}} do?"
                                             trunk `role_identity_declaration_heuristic` ≠ data field `role_identity`
                                             [visible: role_identity_declaration_heuristic_postscript_visible = true]
  ✅ data.role_responsibility                SCALAR
       ✅ role_responsibility_declaration      "**Scope:** {{role_responsibility}}"
  ❌ data.role_description                   SCALAR (optional) — no content template, renders as bare text
                                             [structure: fuse_role_identity_declaration_and_role_description = false]
                                             [structure: bold_contrast_phrase_from_role_description_visible = false]
  ✅ data.role_expertise                     LIST (4 items for agent-builder)
       ✅ role_expertise_label                 "**Your judgment is authoritative in:**"
       ✅ [list items rendered here]
            [display: role_expertise_format = bulleted above 3, inline at/below 3 → bulleted for 4 items]
       ❌ role_expertise_is_strictly_limited_postscript
                                             "Your expertise is strictly limited to the areas listed above."
                                             trunk `role_expertise_is_strictly_limited` ≠ data field `role_expertise`
                                             [visible: role_expertise_is_strictly_limited_postscript_visible = true]

CLOSING:
  ✅ identity_reminder_closing              "Remember: you are a {{role_identity}}."
                                             [visible: identity_reminder_closing_visible = false]
```

---

## Issues

### ❌ ISSUE 1: `role_description` has no content template

Data field `role_description` (optional, scalar prose) has two structure controls (`fuse_role_identity_declaration_and_role_description`, `bold_contrast_phrase_from_role_description_visible`) but NO content template. The trunk resolver renders it as bare text — no framing, no decoration.

**Fix required:** Add a content template for `role_description` (e.g. `role_description_declaration`), or decide this field always renders bare.

### ❌ ISSUE 2: Postscript trunk names don't match data field names

- `role_identity_declaration_heuristic_postscript` — trunk = `role_identity_declaration_heuristic`. No data field matches. Semantically follows `role_identity`, not `role_identity_declaration_heuristic`.
- `role_expertise_is_strictly_limited_postscript` — trunk = `role_expertise_is_strictly_limited`. No data field matches. Semantically follows `role_expertise`.

The decoration matcher looks for `{data_field}_postscript`. Neither matches. Both postscripts are orphaned — they depend on the visibility flags being `true` to show at all, but the engine cannot connect them to their host fields mechanically.

**Fix required:** Rename to match their host data fields — `role_identity_postscript` and `role_expertise_postscript` — or accept that trunk-resolution handles these as section-level decorations rather than field decorations.

### ⚠️ ISSUE 3: `title` may render twice

`title` is consumed by heading template `"AGENT: {{title}}"`. The trunk resolver also processes it as a scalar body field. `render_scalar_value` scans for `{{title}}` in content templates — may find the heading template and render it again in the body. Needs verification.

### ⚠️ ISSUE 4: `fuse_role_identity_declaration_and_role_description` operates on unfilled content

Structure toggle `fuse_role_identity_declaration_and_role_description = false` implies a fusion mode exists. But `role_description` has no content template, so even with `fuse = true` there is nothing to fuse the declaration with. The toggle is currently a no-op in both states.

---

## Renames Needed

### Template suffix (`_template` as final suffix)

- `heading` → `heading_template` — contains `{{title}}`, must signal template to author
- `role_identity_declaration` → `role_identity_declaration_template` — contains `{{role_identity}}`
- `role_responsibility_declaration` → `role_responsibility_declaration_template` — contains `{{role_responsibility}}`
- `identity_reminder_closing` → `identity_reminder_closing_template` — contains `{{role_identity}}`

### Trunk fixes (trunk must match data field)

- `role_identity_declaration_heuristic_postscript` → `role_identity_postscript_template` — trunk `role_identity_declaration_heuristic` matches no data field; correct trunk is `role_identity`; also contains `{{role_identity}}` so `_template` final suffix required
- `role_expertise_is_strictly_limited_postscript` → `role_expertise_postscript` — trunk `role_expertise_is_strictly_limited` matches no data field; correct trunk is `role_expertise`; plain prose, no `_template` needed
