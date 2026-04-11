# Security Boundary Section — Four-Axis Review

## Data (SecurityBoundaryAnthropic)

```
SecurityBoundaryAnthropic
  .workspace_path            WorkspacePathXAbs (PathExistsAbsolute scalar)
  .filesystem_permissions    FilesystemPermissions (list of FilesystemPermission)
       .path                 FilesystemPermissionPath (scalar)
       .tools                FilesystemPermissionToolsCommands (list of tool name scalars)
```

Agent-builder has 7 filesystem_permissions entries. Tool sets vary per entry (heterogeneous).

## Content (SecurityBoundaryContent)

| | # | Field | Type | Suffix | Slot | Value |
|---|---|-------|------|--------|------|-------|
| ✅ | 1 | `filesystem_permissions_label` | StringText | `_label` | body | `"Your filesystem map:"` |
| ✅ | 2 | `section_closing` | StringProse | `_closing` | closing | `"If your task requires access to a path not listed above, report this in your return status."` |
| ✅ | 3 | `compound_entry_template` | StringTemplate | `_template` | body | `"{{PATH}} -- {{TOOLS}}"` — per-item interpolation |
| ⚠️ | 4 | `grouped_tool_heading_template` | StringTemplate | `_heading_template` | body | `"Available tools: {{TOOLS}}"` — `{{TOOLS}}` is a per-item aggregate, not a section scalar |
| ✅ | 5 | `framing_section_start_variant` | BaseModel | `_section_start_variant` | heading | `{territory: "Your Workspace", environmental: "Operating Environment", cage: "Permitted Boundaries"}` |
| ✅ | 6 | `framing_declaration_variant_template` | BaseModel | `_declaration_variant_template` | body | `{territory: "Your workspace is {{WORKSPACE_PATH}}...", environmental: "...", cage: "..."}` |
| ✅ | 7 | `framing_section_preamble_variant` | BaseModel | `_section_preamble_variant` | preamble | `{territory: "Within this workspace, you can access:", environmental: "...", cage: "..."}` |

## Structure (SecurityBoundaryStructure)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ✅ | 2 | `filesystem_permissions_label_visible` | Boolean | `true` | → content #1 visibility |
| ✅ | 3 | `framing_section_preamble_visible` | Boolean | `true` | → content #7 (framing_section_preamble_variant) visibility |
| ✅ | 4 | `section_closing_visible` | Boolean | `false` | → content #2 |
| ✅ | 5 | `framing_selector` | SecurityBoundaryFramingVariant (enum) | `"territory"` | → selects key in content #5, #6, #7 |

## Display (SecurityBoundaryDisplay)

| | # | Field | Type | Value | Controls |
|---|---|-------|------|-------|----------|
| ⚠️ | 1 | `filesystem_permissions_path_style` | enum | `"relative_dotslash"` | Path formatting — engine renders paths as-is from data |
| ⚠️ | 2 | `filesystem_permissions_toolset_format` | enum | `"grouped"` | When all entries share tools: grouped header vs per-entry — not wired |
| ⚠️ | 3 | `filesystem_permissions_toolset_format` | enum | `"per_entry_list"` | When entries have different tools: per-entry format — not wired |
| ✅ | 4 | `filesystem_permissions_label_visibility_threshold` | Integer | `4` | Entry count threshold for showing the label (7 entries → label shows) |
| ⚠️ | 5 | `filesystem_permissions_list_format` | enum | `"bullet"` | List marker style — engine uses bulleted regardless |

---

## Rendering Order

```
HEADING:
  [framing_section_start]
    ✅ framing_section_start_variant        selected by structure.framing_selector = "territory"
                                             → "Your Workspace"
    ✅ framing_selector                      (duplicated: drives heading + preamble + body variants)

PREAMBLE:
  [framing_section_preamble]
    ✅ framing_section_preamble_variant     selected by structure.framing_selector = "territory"
                                             → "Within this workspace, you can access:"
                                             [visible: framing_section_preamble_visible = true]
    ✅ framing_selector                      (duplicated)

BODY (per-trunk, matches BUNDLE_INSPECTION.md):
  [workspace_path]
    ✅ data.workspace_path                  SCALAR (interpolated into {{WORKSPACE_PATH}} via section-wide dict)

  [filesystem_permissions]
    ✅ data.filesystem_permissions          LIST (7 FilesystemPermission items)
    ✅ filesystem_permissions_label         "Your filesystem map:"
                                             [visible: filesystem_permissions_label_visible = true]
                                             [threshold: filesystem_permissions_label_visibility_threshold = 4 → 7 entries, would show]
    ⚠️ filesystem_permissions_path_style   "relative_dotslash" — not wired
    ⚠️ filesystem_permissions_toolset_format  "per_entry_list" — not wired
    ⚠️ filesystem_permissions_list_format   "bullet" — not wired

  [compound_entry]
    ✅ compound_entry_template              "{{PATH}} -- {{TOOLS}}" — per-item interpolation
                                             ← FilesystemPermission.path via {{PATH}}
                                             ← FilesystemPermission.tools via {{TOOLS}}

  [grouped_tool_heading]
    ⚠️ grouped_tool_heading_template        "Available tools: {{TOOLS}}" — body sub-heading
                                             {{TOOLS}} is not a section scalar — it's a per-item aggregate
                                             only renders when filesystem_permissions_toolset_format = "grouped"
                                             (agent-builder has heterogeneous tools — wouldn't render anyway)

  [framing_declaration]
    ✅ framing_declaration_variant_template selected by structure.framing_selector = "territory"
                                             → "Your workspace is {{WORKSPACE_PATH}}. All paths in this prompt are relative to this root."
                                             ← data.workspace_path via {{WORKSPACE_PATH}} (section-wide dict)
    ✅ framing_selector                      (duplicated)

CLOSING:
  [section_closing]
    ✅ section_closing                       "If your task requires access to a path not listed above, report this in your return status."
                                             [visible: section_closing_visible = false]
```

---

## Issues

### ⚠️ ISSUE 1: `grouped_tool_heading_template` references `{{TOOLS}}` — not a section scalar

`{{TOOLS}}` is not a field on SecurityBoundaryAnthropic. It represents the shared tool set across all FilesystemPermission items — a per-item aggregate that no engine mechanism computes. The template would render with literal `{{TOOLS}}` unsubstituted.

Additionally, this heading should only render when `filesystem_permissions_toolset_format = "grouped"` (all entries share the same tools). The engine doesn't check this condition. For agent-builder with heterogeneous tool sets, this heading would be wrong even if it rendered.

### ⚠️ ISSUE 2: Five display controls not implemented

The engine doesn't use any of the security_boundary display fields:
- `filesystem_permissions_path_style` — paths render as-is from data, no `./` prefix or formatting applied
- `filesystem_permissions_toolset_format` / `filesystem_permissions_toolset_format` — tool display mode not checked; engine always uses compound_entry_template
- `filesystem_permissions_list_format` — always renders bulleted
- `filesystem_permissions_label_visibility_threshold` — threshold field exists but engine doesn't compare entry count against it

