# TOML Extraction Audit

## Summary

After two rounds of conformance fixes, the 13 extraction files are in strong conformance with the architecture doc. All `_visible` / content field pairs match, all `_variant` selectors have correctly-suffixed content families, threshold suffixes are correct, no fields are misplaced across files, and the guardrails family sections consistently carry `section_visible` and `max_entries_rendered`. One minor inconsistency remains.

## Findings

### [INCONSISTENCY]: `exact_vs_judgment_explanation_visible` uses auto/always/never pattern without `_auto_threshold`

- **Where**: INSTRUCTIONS, structure.toml `[instructions]`
- **Convention violated**: Architecture doc, Field Interface Pattern 1 (`_visible` — Fragment Visibility), auto with threshold form
- **Specific**: `exact_vs_judgment_explanation_visible = "auto"` uses the auto/always/never tri-state but has no sibling `exact_vs_judgment_explanation_auto_threshold` field. In CRITICAL_RULES, the same pattern is correctly implemented: `rule_count_awareness_prelude_visible = "auto"` with `rule_count_awareness_prelude_auto_threshold = 5`. The INSTRUCTIONS "auto" condition is binary (mixed modes present vs uniform), not count-based, so a numeric threshold is semantically inappropriate. However, the architecture doc defines auto as "applies the threshold" with a mandatory sibling threshold field.
- **Fix**: Two options: (1) Add a comment to the architecture doc acknowledging that auto/always/never can also gate on binary data conditions without a threshold, then add a comment in INSTRUCTIONS clarifying what "auto" means here (e.g., `# "auto" = render when step modes are mixed`). (2) Alternatively, replace with a simple boolean `exact_vs_judgment_explanation_visible = true` and let the renderer silently skip when modes are uniform (data gate handles it), reserving the auto/always/never pattern exclusively for threshold-based decisions. Option 1 is lower disruption.
