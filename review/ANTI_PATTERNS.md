# Anti Patterns Section — Four-Axis Review

## Data (AntiPatterns)

```
AntiPatterns
  └─ patterns: list of GuardrailsAntiPattern (scalar prose — RootModel[StringProse])
```

Agent-builder has 5 anti-pattern entries. Each is a `RootModel[str]` — unwrapped to a plain string.

## Content (AntiPatternsContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `section_start` | StringText | `section_start` | heading | `"Known Failure Modes"` |
| ✅ | 2 | `section_preamble` | StringProse | `_preamble` | preamble | `"These are specific failure modes for this task. Each names a mistake and provides the correction after the dash."` |
| ✅ | 3 | `constraints_vs_anti_patterns_distinction_preamble` | StringProse | `_preamble` | preamble | `"Constraints are your operating rules. Anti-patterns are your likely mistakes."` |

## Structure (AntiPatternsStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `pre_section_visible` | Boolean | `true` | master section toggle — not checked by engine |
| ✅ | 2 | `pre_max_entries_rendered` | Integer | `0` | render all entries (0 = all) |
| ✅ | 3 | `section_preamble_visible` | Boolean | `true` | → content #2 |
| ✅ | 4 | `constraints_vs_anti_patterns_distinction_preamble_visible` | Boolean | `true` | → content #3 |

## Display (AntiPatternsDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `patterns_format` | AntiPatternsPatternsFormat | `"bare_bullets"` | list rendering style — not wired |
| ⚠️ | 2 | `pre_section_divider_override` | SeparatorContent (optional) | `null` | Section-level divider override — not wired |
| ⚠️ | 3 | `pre_body_entry_separator_override` | SeparatorContent (optional) | `null` | Body-entry separator override — not wired |

---

## Rendering Order

```
HEADING:
  ✅ section_start                         "Known Failure Modes"

PREAMBLE:
  ✅ section_preamble                      "These are specific failure modes for this task..."
                                             [visible: section_preamble_visible = true]
  ✅ constraints_vs_anti_patterns_distinction_preamble  "Constraints are your operating rules. Anti-patterns are your likely mistakes."
                                             [visible: constraints_vs_anti_patterns_distinction_preamble_visible = true]

BODY:
  For each GuardrailsAntiPattern (RootModel[str]):
    .root                                  → unwrapped prose string
    ⚠️ format: patterns_format = "bare_bullets" — not wired

CLOSING:
  (none)
```

---

## Issues

### ⚠️ ISSUE 1: `pre_section_visible` master toggle not checked by engine

The master `pre_section_visible = true` toggle exists in structure but the engine does not check it before rendering the section. Section-skip decisions belong at the orchestrate level.

### ⚠️ ISSUE 2: `patterns_format` display control not wired

Display control `patterns_format = "bare_bullets"` specifies how the list renders. The engine does not read it — list format is currently hardcoded. The other option `"bold_prohibition"` would prepend a bold prohibition marker to each item.

### ⚠️ ISSUE 3: `pre_max_entries_rendered = 0` not implemented

Structure field `pre_max_entries_rendered` (0 = render all, N = cap at N) is present but the engine does not slice the list. Currently renders all items regardless. For this agent the value is 0 so no practical difference, but the mechanism is absent.
