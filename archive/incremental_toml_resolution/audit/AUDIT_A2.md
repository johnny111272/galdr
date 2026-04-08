# TOML Extraction Audit (A2 -- Verification)

## Summary

The conformance fixes from the prior round resolved all findings from audits A, B, and C. All `_visible` toggles now have matching content field roots. All `_variant` selectors follow the `{concept}_variant` -> `{concept}_{value}` pattern (or the documented shared variant pattern with governing comments). All threshold fields use documented suffixes. Preamble naming is consistent across sections. One new finding remains.

## Findings

### [CONVENTION]: EXAMPLES `suppress_lone_group_heading_visible` uses `_visible` on a behavioral switch, not a prose fragment

- **Where**: EXAMPLES, structure.toml `suppress_lone_group_heading_visible = true`
- **Convention violated**: Architecture doc, "Field Interface Patterns" section 1: "`_visible` -- Fragment Visibility: Controls whether a prose fragment renders." The `_visible` suffix is reserved for controlling whether a prose fragment or visual element is shown. This field controls whether a *behavioral optimization* (heading suppression + entry promotion) is active.
- **Specific**: `suppress_lone_group_heading_visible = true` means "the suppression behavior is active," which means the heading is *hidden*. This inverts the `_visible` convention where `true` means "the thing renders." There is no content field `suppress_lone_group_heading` because this is not prose -- it is a structural behavior. Compare with IDENTITY's `fuse_declaration_and_role_description = false`, which correctly uses a plain boolean for a structural behavior toggle without the `_visible` suffix.
- **Fix**: Rename to `suppress_lone_group_heading = true` (plain boolean, no `_visible` suffix). This follows the established pattern for structural behavior toggles in structure.toml.
