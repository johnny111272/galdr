# Archive Index

Files moved here are historical source material. They informed decisions that have been implemented. They reference pre-rename field names and old architecture patterns.

**Do not use these as reference for current field names or architecture.** Use `extracted/*.toml` and `review/*.md` for current state.

## Contents

### analysis/ (10 files)
Pre-rename analysis documents. Cross-axis naming analysis, knob inventories, control surface design. These drove the positional suffix alignment and naming renames (163-file Verdandi cascade). All field names are pre-rename.

### agent_outputs/ (30 files)
Raw A/B analysis pairs from the independent agent analysis phase. Each section was analyzed by two agents; results were synthesized into the section analysis docs in `agent_control_surfaces/`. Source material for traceability.

### incremental_toml_resolution/ (13 files)
Per-section TOML field extraction proposals. These were the first-draft TOML files that became `extracted/content.toml`, `extracted/structure.toml`, `extracted/display.toml`. All field names are pre-rename.

### incremental_toml_resolution/audit/ (10 files)
Three rounds of cross-axis naming audits (3 agents × 3 rounds + dispatch template). These identified the naming mismatches that drove the rename cascade. All findings have been addressed.

### dispatch_templates/ (3 files)
Agent dispatch templates used to launch the A/B analysis and TOML resolution agents. Process documentation — the tasks are complete.

### staging/ (2 files)
Old rendered agent outputs from before the trunk resolver and suffix alignment. Stale — regenerate from current engine.
