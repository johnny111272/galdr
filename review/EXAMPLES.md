# Examples Section — Four-Axis Review

## Data (Examples)

```
Examples
  └─ groups: list of ExampleGroup
       ├─ .example_group_name    ExampleGroupName (TitleString scalar)
       └─ .example_entries: list of ExampleEntry
            ├─ .example_heading   StringText (scalar)
            └─ .example_text      StringMarkdown (scalar)
```

Agent-builder has 3 groups, each with 1-2 entries. The display-headings and max-number controls live on the structure axis (`groups_display_headings`, `groups_max_number`), not as per-group data fields.

## Content (ExamplesContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"Worked Examples"` |
| ✅ | 2 | `section_preamble` | StringProse | `_preamble` | preamble | `"Examples may show GOOD and BAD outputs with WHY reasoning..."` |
| ✅ | 3 | `group_framing_preamble_template` | StringTemplate | `_preamble_template` | preamble | `"The following examples demonstrate {{example_group_name}}:"` |
| ✅ | 4 | `example_heading_template` | StringTemplate | `_heading_template` | body | `"{{example_heading}}"` — template wrapping a per-entry field (body sub-heading per `has_start_suffix`) |

## Structure (ExamplesStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `section_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 2 | `groups_suppress_lone_heading` | Boolean | `true` | Skip group heading when only 1 group |
| ⚠️ | 3 | `groups_display_headings` | Boolean (optional) | `true` (default) | Section-level gate: render entry headings within each group |
| ⚠️ | 4 | `groups_max_number` | Integer (optional) | `0` (default, no cap) | Section-level cap: max entries rendered per group |
| ⚠️ | 5 | `groups_display_headings_override` | Boolean | `false` | Override toggle for `groups_display_headings` — not implemented |
| ⚠️ | 6 | `groups_max_number_override` | Boolean | `false` | Override toggle for `groups_max_number` — not implemented |
| ✅ | 7 | `group_framing_preamble_visible` | Boolean | `false` | → content #3 |

## Display (ExamplesDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `groups_entry_heading_format` | enum | `"bold"` | Entry heading as bold vs H4 — not wired |
| ⚠️ | 2 | `groups_entry_body_container` | enum | `"bare_with_endmarker"` | How entry body is contained — not wired |
| ⚠️ | 3 | `groups_entry_separator` | enum | `"horizontal_rule"` | Between entries when headings off — not wired |
| ⚠️ | 4 | `groups_separator` | enum | `"horizontal_rule"` | Between groups — not wired |
| ⚠️ | 5 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 6 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                      "Worked Examples"

PREAMBLE:
  ✅ section_preamble                   "Examples may show GOOD and BAD..."
                                         [visible: section_preamble_visible = true]

BODY:
  [groups]
    For each ExampleGroup:
      GROUP LEVEL:
        .example_group_name             → render as H3 (unless groups_suppress_lone_heading)
        group_framing_preamble_template "The following examples demonstrate {{example_group_name}}:"
                                         [visible: group_framing_preamble_visible = false]

      ENTRY LEVEL (for each ExampleEntry):
        .example_heading                → render per display.groups_entry_heading_format (bold/H4)
                                         only if structure.groups_display_headings = true
        .example_text                   → render as markdown prose
                                         [display: groups_entry_body_container]
        ---                             [display: groups_entry_separator between entries]

      === between groups ===            [display: groups_separator]
                                         [structure: groups_max_number caps entries per group]

  [example_heading]
    ✅ example_heading_template         "{{example_heading}}" — body sub-heading template, wraps per-entry example_heading data field

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: `group_framing_preamble_template` needs per-group interpolation

This template uses `{{example_group_name}}` but sits in the preamble slot (renders once at section level). It should render per-group, before each group's entries. The `_preamble_template` suffix routes it to section preamble, but its function is per-group.

### ⚠️ ISSUE 2: Section-level gates and overrides not implemented

`groups_display_headings` (entry-heading gate) and `groups_max_number` (per-group cap) are section-level structure controls with corresponding override toggles. Engine doesn't check any of them.

### ⚠️ ISSUE 3: Display controls not implemented

4 display fields control formatting but engine uses hardcoded defaults.
