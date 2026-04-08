# ANTI_PATTERNS — TOML Extraction

## structure.toml

```toml
[anti_patterns]
# Whether to render the section at all (false = omit even if patterns exist)
section_visible = true

# Maximum entries to render (0 = render all). Truncates from the end, preserving author priority order.
max_entries_rendered = 0

# Whether to include a preamble line before the pattern list
section_preamble_visible = true

# Whether to include authority positioning prose distinguishing anti-patterns from constraints/critical_rules
constraints_vs_anti_patterns_distinction_visible = true
```

**Decisions:**

- `section_preamble_visible`: Code default is "omit for 1-2 patterns, include for 3+." This toggle overrides that default in either direction.
- `constraints_vs_anti_patterns_distinction_visible`: Code default is "include when constraints + critical_rules + anti_patterns all co-present." This toggle overrides.

## content.toml

```toml
[anti_patterns]
# Section heading text
heading = "Known Failure Modes"

# One-line preamble rendered before the pattern list
section_preamble = "These are specific failure modes for this task. Each names a mistake and provides the correction after the dash."

# Distinguishes anti-patterns from constraints when both sections co-exist
constraints_vs_anti_patterns_distinction = "Constraints are your operating rules. Anti-patterns are your likely mistakes."
```

**Decisions:**

- `heading`: "Known Failure Modes" is MEDIUM confidence. Alternatives: "Mistakes You Will Make", "Anti-Patterns".

## display.toml

```toml
[anti_patterns]
# Format for rendering the pattern list
# Options: "bare_bullets", "bold_prohibition"
pattern_list_format = "bare_bullets"

```

**Decisions:**

- `pattern_list_format`: "bare_bullets" = `- Do not X -- Y.` "bold_prohibition" = `- **Do not X** -- Y.`

## Excluded (invariant rules / bare data)

- **Pattern ordering**: Author-determined order preserved exactly. Template never reorders.
- **Reasoning clause mandatory**: "-- Y" clause is a validation rule. Code warns if missing; does not rewrite.
- **Pattern text passthrough**: Template does not rewrite author content. Patterns render as-is.
- **Prohibition priming mitigation**: "Do not X — Y" pattern redirects to the correction, mitigating priming from the prohibition. Implicit in pattern structure.
- **Redundancy with instructions tolerated**: Deduplication is never applied.
