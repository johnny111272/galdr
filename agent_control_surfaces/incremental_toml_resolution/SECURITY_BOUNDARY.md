# SECURITY_BOUNDARY -- TOML Extraction

## structure.toml
```toml
[security_boundary]
# Whether to fuse workspace_path with path-resolution instruction in a single sentence
fuse_workspace_path_and_resolver = true

# Whether to render an intro line before display entries
filesystem_map_intro_visible = true

# Whether to render a preamble between heading and entries
section_preamble_visible = true

# Whether to render a closing after entries
section_closing_visible = false

# Whether to show tool names alongside paths (hooks enforce regardless)
tool_names_visible = true

# Framing paradigm: selects which content posture the section uses
framing_variant = "territory"  # "territory" | "environmental" | "cage" — governs: heading_*, workspace_path_declaration_*, section_preamble_*
```
**Decisions:**

- `section_closing_visible`: Default false — closing text risks priming "what if I need more access?" thinking.
- `tool_names_visible`: Open question whether tool names add value given hook enforcement. Default true (conservative).

## content.toml
```toml
[security_boundary]
# Section heading — keyed by framing_variant
heading_territory = "Your Workspace"
heading_environmental = "Operating Environment"
heading_cage = "Permitted Boundaries"

# Workspace path declaration — keyed by framing_variant
workspace_path_declaration_territory = "Your workspace is {{WORKSPACE_PATH}}. All paths in this prompt are relative to this root."
workspace_path_declaration_environmental = "You operate within {{WORKSPACE_PATH}}. All paths in this prompt are relative to this root."
workspace_path_declaration_cage = "You are confined to {{WORKSPACE_PATH}}. You cannot access anything outside this path."

# Intro line before display entries (when enabled)
filesystem_map_intro = "Your filesystem map:"

# Preamble — keyed by framing_variant
section_preamble_territory = "Within this workspace, you can access:"
section_preamble_environmental = "The following paths are available to you:"
section_preamble_cage = "You are permitted to access only the following paths:"

# Closing text after entries (when enabled)
section_closing = "If your task requires access to a path not listed above, report this in your return status."

# Compound entry template for per-entry format (template)
compound_entry_template = "{{PATH}} -- {{TOOLS}}"

# Grouped format: tool header when all entries share the same tool set (template)
grouped_tool_header = "Available tools: {{TOOLS}}"
```
**Decisions:**

- `heading`: "Your Workspace" — possessive territory framing. Alternative: "Operating Environment".
- Preamble and intro are distinct: preamble establishes root relationship, intro labels the entry list.

## display.toml
```toml
[security_boundary]
# Path style: "relative_dotslash" | "relative_bare" | "absolute"
path_style = "relative_dotslash"

# Entry format when tool sets are uniform across all entries: "grouped" | "per_entry"
uniform_toolset_format = "grouped"

# Entry format when tool sets differ across entries: "per_entry_list" | "per_entry_prose"
heterogeneous_toolset_format = "per_entry_list"

# Entry count threshold for switching from no-intro to intro-present
filesystem_map_intro_visibility_threshold = 4

# Entry list marker style (applied by display layer)
entry_list_format = "bullet"
```
**Decisions:**

- `filesystem_map_intro_visibility_threshold`: Interacts with structure toggle — below threshold, intro suppressed regardless of toggle.

## Excluded (invariant rules / bare data)

- **permission_mode_display**: Implementation details (`bypassPermissions`, hook-based) never leak into agent prompts. Always omit.
- **Path-first ordering**: Tool-first is a defect. Invariant.
- **Section always renders**: Even empty-display agents get workspace_path. Invariant.
