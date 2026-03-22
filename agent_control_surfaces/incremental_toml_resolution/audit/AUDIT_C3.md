# TOML Extraction Audit — C3 (Verification Round)

## Summary

The 13 extraction files are in strong conformance with the architecture doc after two rounds of fixes. All `_visible` toggles have matching content fields. All `_variant` selectors have complete content coverage with correct suffix naming. All threshold fields use the correct documented suffixes. One cross-section inconsistency remains in how the `auto/always/never` pattern is applied.

## Findings

### [INCONSISTENCY]: `_visible = "auto"` used with and without `_auto_threshold`

- **Where**: INSTRUCTIONS `exact_vs_judgment_explanation_visible = "auto"` (no threshold) vs CRITICAL_RULES `rule_count_awareness_prelude_visible = "auto"` with `rule_count_awareness_prelude_auto_threshold = 5`
- **Convention violated**: Architecture doc section "1. `_visible` — Fragment Visibility" defines the auto pattern as requiring an `_auto_threshold` sibling field. The example shows `_visible = "auto"` paired with `_auto_threshold = 5`.
- **Specific**: INSTRUCTIONS structure.toml has `exact_vs_judgment_explanation_visible = "auto"` with the comment `# "auto" (render when mixed modes) | "always" | "never"`. The auto condition is a boolean data property (mixed vs uniform mode distribution), not a count threshold. There is no `exact_vs_judgment_explanation_auto_threshold` field.
- **Fix**: Two options. (1) Document a second form of auto — "auto-from-data-condition" — where the threshold is implicit in the renderer's data inspection, and note this in the architecture doc as a recognized variant. (2) Replace with a dedicated boolean toggle like `exact_vs_judgment_explanation_when_mixed_modes = true` and drop the auto/always/never enum, reserving that enum exclusively for count-threshold cases. Option 1 is lower-disruption; option 2 is stricter conformance.
