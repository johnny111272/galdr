# TOML Extraction Audit (B2 -- Verification Pass)

## Summary

All findings from audits A, B, and C have been resolved. The fix round successfully addressed every mismatch, phantom toggle, misplaced field, naming violation, and cross-section inconsistency. Two residual conformance issues remain in the EXAMPLES section, both involving `_visible` toggles that don't follow the documented convention.

## Findings

### [CONVENTION]: EXAMPLES `suppress_lone_group_heading_visible` misuses the `_visible` convention

- **Where**: EXAMPLES section, structure.toml `suppress_lone_group_heading_visible = true`
- **Convention violated**: "Visibility Toggles Use `_visible` Suffix" -- the architecture doc defines `_visible` as "Controls whether a prose fragment renders" where `true` means "render" and `false` means "suppress." This field inverts that semantic: `true` means "suppress the group heading," which is the opposite of what `_visible = true` conventionally means. Additionally, there is no content.toml field `suppress_lone_group_heading`.
- **Specific**: The comment says "true = suppress group heading + promote entries; false = render full three-level hierarchy." A naive reader seeing `suppress_lone_group_heading_visible = true` would parse it as "the suppression fragment is visible" rather than "suppress the lone group heading." The field controls a structural rendering decision (heading hierarchy promotion), not prose fragment visibility.
- **Fix**: Replace with a plain boolean that doesn't use `_visible`: either `suppress_lone_group_heading = true` (structural decision, no content counterpart needed), or invert to `lone_group_heading_visible = false` to follow the convention semantics (`_visible = false` means "hide this element").

### [CONVENTION]: EXAMPLES `multi_group_separator_visible` cross-references display.toml instead of content.toml

- **Where**: EXAMPLES section, structure.toml `multi_group_separator_visible = true`, display.toml `multi_group_separator = "horizontal_rule"`
- **Convention violated**: "The structure field is `{name}_visible` (boolean). The content field is `{name}` (string). The shared root name creates obvious cross-reference." The `_visible` toggle convention establishes a cross-reference from structure.toml to content.toml. Here the sibling field `multi_group_separator` lives in display.toml, not content.toml.
- **Specific**: A reader of structure.toml seeing `multi_group_separator_visible` would look for `multi_group_separator` in content.toml and not find it. The field is in display.toml because separators are display concerns (format selection), not prose content. Compare with CRITICAL_RULES which has `rule_separator` in display.toml with no structure toggle at all.
- **Fix**: Either (a) remove the structure toggle and let the display field handle it (a display value of `"none"` could replace the boolean toggle, following how INSTRUCTIONS uses `step_body_container = "none"` in display.toml), or (b) document this as a legitimate pattern where `_visible` can gate display elements, updating the architecture doc to note that `_visible` cross-references content.toml for prose fragments and display.toml for display elements.
