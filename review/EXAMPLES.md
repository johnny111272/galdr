# Examples Section — Four-Axis Review

## Data (Examples)

```
Examples
  └─ groups: list of ExampleGroup
       ├─ .example_group_name    ExampleGroupName (TitleString scalar)
       ├─ .example_display_headings   Boolean (optional) — per-group gate
       ├─ .examples_max_number   Integer (optional) — per-group cap
       └─ .example_entries: list of ExampleEntry
            ├─ .example_heading   StringText (scalar)
            └─ .example_text      StringMarkdown (scalar)
```

Agent-builder has 3 groups, each with 1-2 entries.

## Content (ExamplesContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `heading` | StringText | heading | heading | `"Worked Examples"` |
| ✅ | 2 | `section_preamble` | StringProse | _preamble | preamble | `"Examples may show GOOD and BAD outputs with WHY reasoning..."` |
| ✅ | 3 | `group_framing_preamble` | StringTemplate | _preamble | preamble | `"The following examples demonstrate {{example_group_name}}:"` |
| ⚠️ | 4 | `example_heading` | StringTemplate | _heading | heading | `"{{example_heading}}"` — template wrapping a per-entry field |

## Structure (ExamplesStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 1 | `section_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 2 | `suppress_lone_group_heading` | Boolean | `true` | Skip group heading when only 1 group |
| ⚠️ | 3 | `example_display_headings_override` | Boolean | `false` | Override per-group gate — not implemented |
| ⚠️ | 4 | `examples_max_number_override` | Boolean | `false` | Override per-group cap — not implemented |
| ✅ | 5 | `group_framing_preamble_visible` | Boolean | `false` | → content #3 |

## Display (ExamplesDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `example_heading_format` | enum | `"bold"` | Entry heading as bold vs H4 — not wired |
| ⚠️ | 2 | `example_body_container` | enum | `"bare_with_endmarker"` | How entry body is contained — not wired |
| ⚠️ | 3 | `example_separator` | enum | `"horizontal_rule"` | Between entries when headings off — not wired |
| ⚠️ | 4 | `multi_group_separator` | enum | `"horizontal_rule"` | Between groups — not wired |

---

## Rendering Order

```
HEADING:
  ✅ heading                            "Worked Examples"
  ⚠️ example_heading                    "{{example_heading}}" — per-entry, NOT section heading

PREAMBLE:
  ✅ section_preamble                   "Examples may show GOOD and BAD..."
                                         [visible: section_preamble_visible = true]

BODY:
  For each ExampleGroup:
    GROUP LEVEL:
      .example_group_name               → render as H3 (unless suppress_lone_group_heading)
      .example_display_headings         → GATE: controls whether entry headings render
      .examples_max_number              → GATE: caps number of entries rendered
      group_framing_preamble            "The following examples demonstrate {{example_group_name}}:"
                                         [visible: group_framing_preamble_visible = false]

    ENTRY LEVEL (for each ExampleEntry):
      .example_heading                  → render per display.example_heading_format (bold/H4)
                                         only if example_display_headings = true
      .example_text                     → render as markdown prose
                                         [display: example_body_container]
      ---                               [display: example_separator between entries]

    === between groups ===              [display: multi_group_separator]

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: `example_heading` content template in heading slot

Content field `example_heading = "{{example_heading}}"` has `_heading` suffix → classified as heading slot. But it's a per-entry template, not a section heading. It wraps the per-entry `example_heading` data field. The buffer consumes it as a heading when it should be body-level per-item content.

**Options:** Rename to something without `_heading` suffix (but what?). Or the data field `example_heading` itself ends in `_heading` — maybe the data field name should change.

### ⚠️ ISSUE 2: `group_framing_preamble` needs per-group interpolation

This template uses `{{example_group_name}}` but sits in the preamble slot (renders once at section level). It should render per-group, before each group's entries. The `_preamble` suffix routes it to section preamble, but its function is per-group.

### ⚠️ ISSUE 3: Per-group gates and overrides not implemented

`example_display_headings` (per-group boolean gate) and `examples_max_number` (per-group cap) control per-group rendering. Structure overrides exist. Engine doesn't check any of them.

### ⚠️ ISSUE 4: Display controls not implemented

4 display fields control formatting but engine uses hardcoded defaults.

---

## Renames Needed

### Template suffix (`_template` as final suffix)

- `group_framing_preamble` → `group_framing_preamble_template` — contains `{{example_group_name}}`
- `example_heading` → `example_heading_template` — contains `{{example_heading}}`; also has the slot-classification issue flagged in Issue 1 (the `_heading` suffix routes it to heading slot but it is per-entry content)
