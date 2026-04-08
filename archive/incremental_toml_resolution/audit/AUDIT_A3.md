# TOML Extraction Audit

## Summary

Overall conformance is high. All 13 sections follow the architecture doc's naming conventions, interface patterns, and threshold suffix rules consistently. Two prior rounds of fixes have resolved the bulk of issues. Two findings remain in CONSTRAINTS and RETURN_FORMAT — both involve content fields that lack a structure-side visibility mechanism.

## Findings

### [CONVENTION]: CONSTRAINTS hierarchy prose fields have no visibility toggles

- **Where**: CONSTRAINTS section — content.toml fields `hierarchy_tier_comparison` and `hierarchy_three_tier_explanation`
- **Convention violated**: Architecture doc, Visibility Toggles section — prose fragments that can meaningfully vary should have a structure.toml `_visible` toggle. The filtering principle says only things that VARY are knobs, and these are knobs (they're in content.toml). But the architecture doc also says: "If there's a legitimate reason to suppress prose when data is present, the toggle is justified."
- **Specific**: `hierarchy_tier_comparison` and `hierarchy_three_tier_explanation` are content.toml entries with no corresponding structure.toml `_visible` fields. Their rendering is side-effected by `section_preamble_variant = "references_critical_rules"` — they render when that variant is active. An author cannot suppress hierarchy framing independently of the preamble variant. All other optional prose fragments in the 13 sections have either (a) a `_visible` toggle, (b) a variant suffix linking them to a `_variant` selector, or (c) a documented data gate making them invariant.
- **Fix**: Either (a) add `hierarchy_tier_comparison_visible = true` and `hierarchy_three_tier_explanation_visible = true` to structure.toml, or (b) fold their content into the `section_preamble_references_critical_rules` text itself (eliminating them as independent fields), or (c) document them as invariant sub-fragments of the `references_critical_rules` variant in the Excluded section.

### [CONVENTION]: RETURN_FORMAT `track_metrics_as_you_work_antidrift` has no visibility control

- **Where**: RETURN_FORMAT section — content.toml field `track_metrics_as_you_work_antidrift`
- **Convention violated**: Architecture doc, Visibility Toggles section — independently useful prose fragments should have a structure.toml visibility mechanism. The Decisions text says "More valuable for batch tasks — code can conditionally include," acknowledging this fragment has selective applicability. Yet there is no `_visible` toggle in structure.toml and no documented data gate in the Excluded section.
- **Specific**: `track_metrics_as_you_work_antidrift` is a content field describing anti-drift behavior ("The dispatcher is waiting for your return signal..."). The companion field `track_metrics_as_you_work_postscript` has a toggle (`track_metrics_as_you_work_postscript_visible`). The antidrift field has no corresponding toggle. It is unclear whether the renderer includes it always, ties it to the postscript toggle, or applies its own data gate — the extraction doesn't document this.
- **Fix**: Either (a) add `track_metrics_as_you_work_antidrift_visible = true` to structure.toml (allowing independent suppression), or (b) document in the Excluded section that it renders unconditionally when the postscript renders (tying it to the existing toggle), or (c) document the specific data gate the renderer applies (e.g., "renders only for batch agents").
