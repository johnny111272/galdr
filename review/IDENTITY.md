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
| ✅ | 1 | `heading_template` | StringTemplate | `_template` (IS the heading) | heading | `"AGENT: {{title}}"` |
| ✅ | 2 | `role_identity_declaration_template` | StringTemplate | `_declaration_template` | body | `"You are a {{role_identity}}."` |
| ✅ | 3 | `role_identity_postscript_template` | StringTemplate | `_postscript_template` | body | `"...what would a {{role_identity}} do?"` |
| ✅ | 4 | `role_responsibility_declaration_template` | StringTemplate | `_declaration_template` | body | `"**Scope:** {{role_responsibility}}"` |
| ✅ | 5 | `role_expertise_label` | StringText | `_label` | body | `"**Your judgment is authoritative in:**"` |
| ✅ | 6 | `role_expertise_postscript` | StringProse | `_postscript` | body | `"Your expertise is strictly limited to the areas listed above."` |
| ✅ | 7 | `identity_reminder_closing_template` | StringTemplate | `_closing_template` | closing | `"Remember: you are a {{role_identity}}."` |

## Structure (IdentityStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `field_ordering` | IdentityFieldOrdering (enum) | `"identity_first"` | Field render order within section |
| ✅ | 3 | `role_identity_postscript_template_visible` | Boolean | `true` | → content #3 |
| ✅ | 4 | `role_expertise_postscript_visible` | Boolean | `true` | → content #6 |
| ✅ | 5 | `identity_reminder_closing_template_visible` | Boolean | `false` | → content #7 |

## Display (IdentityDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `role_expertise_format` | FormatPair | `["bulleted", "inline"]` | → data.role_expertise list format (bulleted above threshold, inline at/below) |
| ✅ | 2 | `role_expertise_format_threshold` | Integer | `3` | → switch at 3 items (4 items → bulleted) |

---

## Rendering Order

```
HEADING:
  ✅ heading_template                       "AGENT: {{title}}"
                                             ← data.title

PREAMBLE:
  (none for identity)

BODY (in data field order):
  ⚠️ data.title                             SCALAR — consumed by heading template, may render again in body
  ✅ data.role_identity                      SCALAR
       ✅ role_identity_declaration_template   "You are a {{role_identity}}."
       ✅ role_identity_postscript_template
                                             "...what would a {{role_identity}} do?"
                                             [visible: role_identity_postscript_template_visible = true]
  ✅ data.role_responsibility                SCALAR
       ✅ role_responsibility_declaration_template  "**Scope:** {{role_responsibility}}"
  ❌ data.role_description                   SCALAR (optional) — no content template, renders as bare text


  ✅ data.role_expertise                     LIST (4 items for agent-builder)
       ✅ role_expertise_label                 "**Your judgment is authoritative in:**"
       ✅ [list items rendered here]
            [display: role_expertise_format = bulleted above 3, inline at/below 3 → bulleted for 4 items]
       ✅ role_expertise_postscript
                                             "Your expertise is strictly limited to the areas listed above."
                                             [visible: role_expertise_postscript_visible = true]

CLOSING:
  ✅ identity_reminder_closing_template     "Remember: you are a {{role_identity}}."
                                             [visible: identity_reminder_closing_template_visible = false]
```

---

## Issues

### ❌ ISSUE 1: `role_description` has no content template

Data field `role_description` (optional, scalar prose) has no content template. Renders as bare text — no framing, no decoration.

**Fix required:** Add a content template for `role_description` (e.g. `role_description_declaration_template`), or decide this field always renders bare.

### ⚠️ ISSUE 2: `title` may render twice

`title` is consumed by heading template `"AGENT: {{title}}"`. The trunk resolver also processes it as a scalar body field. `render_scalar_value` scans for `{{title}}` in content templates — may find the heading template and render it again in the body. Needs verification.

