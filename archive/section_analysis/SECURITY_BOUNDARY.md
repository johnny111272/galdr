# SECURITY_BOUNDARY -- Control Surface Synthesis

## Section Purpose

This section transforms access-control data (a workspace root path and an optional array of path-tool pairs) into a **spatial self-model** -- the agent's understanding of where it exists, where it can go, and what operations are available at each location. The section does not exist to restrict the agent. It exists to orient it.

Both analyses converged strongly on the **cage-vs-territory framing** as the section's central design axis. The same data presented as restriction ("you are confined to these paths") versus territory ("these are your working areas") produces measurably different agent postures: cage framing activates compliance-checking that slows legitimate operations; territory framing activates confident navigation within bounds. Analysis A additionally identified a third option -- **environmental framing** ("operations outside this workspace do not exist from your perspective") -- which sidesteps the restriction/permission axis entirely by making the boundary a physical law rather than a rule. This three-way axis (cage / territory / environmental) is the section's primary design variable.

Both analyses agree the current renderer is defective in three specific ways: (1) it leaks infrastructure implementation details (`bypassPermissions`, "hook-based"), (2) it uses tool-first ordering instead of path-first, and (3) it omits the entire section when the display array is empty, leaving no-grant agents without a workspace root or spatial model. All three are unambiguous defects, not design tradeoffs.

## Fragment Catalog

### workspace_path_presentation
- CONVERGED: The workspace path must always be rendered, for every agent. It is the spatial root against which all other paths resolve. The current renderer either hides it (builder) or omits the section entirely (summarizer). Both are failures.
- DIVERGED: A identifies three functions (root anchor, confinement boundary, identity grounding). B focuses on two (absolute location, boundary semantics) but adds the "resolver" concept -- explicitly teaching the agent that all prompt paths connect back to this root. The resolver framing is B's unique contribution.
- ALTERNATIVES:
  - A: `Your workspace is {path}. All paths in this prompt are relative to this root.` -- declarative + resolver relationship. Teaches the agent to use workspace_path as a reference point for every other path it encounters.
  - B: `Your operational environment is rooted at {path}. Files and directories outside this tree do not exist from your perspective.` -- environmental framing. Makes the boundary a property of reality, not a rule.
  - C: `Workspace root: {path}` -- minimal label-value. No framing overhead, no risk of bad framing. Lets downstream sections carry the behavioral weight.
- HYPOTHESIS: The resolver framing (A) is operationally the most useful -- it prevents path-resolution errors by explicitly teaching the root-to-branch relationship. Environmental framing (B) is behaviorally the most interesting but makes a strong ontological claim. The minimal form (C) is safest when other sections already establish spatial context.
- STABILITY: **structural** (value always renders) + **experimental** (framing choice)
- CONDITIONAL: none -- identical value for all agents in this workspace

### path_resolution_instruction
- CONVERGED: The current renderer never explains how relative paths (`./definitions/`) connect to the absolute workspace root. Both analyses flag this as a correctness gap.
- DIVERGED: A proposes three options (explicit rule, resolved absolute paths, worked example). B folds this into workspace_path_presentation Alternative B ("all paths in this prompt are relative to this root") rather than treating it as a separate fragment.
- ALTERNATIVES:
  - A: Fold into workspace_path_presentation -- `All paths in this prompt are relative to this root.` One sentence, no separate fragment.
  - B: One worked example -- `Paths beginning with ./ are relative to the workspace. ./definitions/ means {workspace_path}/definitions/.` Teaches by demonstration.
- HYPOTHESIS: A single sentence in the workspace presentation is sufficient. A separate fragment is over-engineering unless agents consistently misresolve paths, in which case the worked example becomes necessary.
- STABILITY: **structural** -- this is a correctness concern, not a behavioral experiment
- CONDITIONAL: none

### display_section_intro
- CONVERGED: The current intro ("The following operations are allowed -- everything else is blocked by the system") is cage framing and should be replaced. Both analyses want territory or map framing.
- DIVERGED: A proposes a "completeness" alternative ("Everything you need is here") which B does not consider. B proposes a "no intro" option (entries appear directly after workspace_path).
- ALTERNATIVES:
  - A: `Your filesystem map:` -- metaphor framing. Reframes the list as a map to internalize, not a permission set to consult.
  - B: `You have access to the following workspace locations:` -- neutral territory framing. Possessive ("you have"), not restrictive.
  - C: No intro -- entries follow workspace_path directly. Removes the risk of bad framing entirely.
- HYPOTHESIS: The intro's leverage depends on entry count. For 1-3 entries, no intro is fine. For 4+ entries, a brief framing line helps the agent process the list as a coherent territory rather than as isolated grants.
- STABILITY: **experimental**
- CONDITIONAL: omitted when display array is empty; framing may vary by entry count

### compound_entry_template
- CONVERGED: Both analyses agree that **path-first ordering** is correct and tool-first (current) is wrong. The agent's decision flow is "I need X -> where is it?" not "I have Glob -> where can I use it?" Both identify table, list, grouped, and prose as format options.
- DIVERGED: A raises a radical option -- **omit tool names entirely** since hooks enforce grants regardless of what the prompt says. B does not consider this. A also proposes **named paths** (path + human-readable label). B proposes **sentence dissolution** ("You can search and read `./path/`").
- ALTERNATIVES:
  - A: `- {path} -- {tools}` -- bulleted path-first list. Clean, scannable, works for heterogeneous tool sets.
  - B: Grouped by tool set when tools are uniform -- state tools once as a header, list all paths beneath. Eliminates per-entry repetition for the common case.
  - C: Path only, tools omitted -- the simplest representation. Hooks enforce actual grants; the prompt shows territory only.
- HYPOTHESIS: When all entries share the same tool set (the common case), grouped format eliminates noise and presents the territory as a cohesive unit. When tool sets differ, per-entry path-first list is necessary. Tool omission (C) is worth testing -- if hook enforcement means prompt-displayed tools are purely advisory, displaying them may be wasted tokens that add no behavioral value.
- STABILITY: **formatting** (layout) + **experimental** (whether to display tools at all)
- CONDITIONAL: format switches based on tool-set uniformity (uniform -> grouped; heterogeneous -> per-entry list)

### compound_entry_path_style
- CONVERGED: Both analyses note the current `./` prefix convention and the tradeoff between relative (compact) and absolute (unambiguous) paths.
- DIVERGED: A proposes **named paths** (`definitions/agents/agent-template.toml (Agent Template)`) to add semantic context. B does not consider this.
- ALTERNATIVES:
  - A: Relative with `./` prefix -- conventional, compact, requires workspace_path to be established first.
  - B: Bare relative without `./` -- slightly cleaner visually, loses the "relative to here" signal.
- HYPOTHESIS: The `./` prefix is cheap and signals relativity. Absolute paths create visual clutter for no behavioral gain if the workspace root is already established. Named paths are interesting but belong in purpose annotations (see path_semantic_annotation), not the path string itself.
- STABILITY: **formatting**
- CONDITIONAL: none

### path_semantic_annotation
- CONVERGED: Both analyses identify that current entries provide no context for WHY the agent has each path. A develops this further with per-path annotations and purpose grouping.
- DIVERGED: A treats this as a distinct novel fragment ("territory_purpose_mapping") and proposes grouping by purpose (Reference / Working data / Validation / Output staging). B mentions it only briefly as a sub-option.
- ALTERNATIVES:
  - A: Per-path brief annotation -- `./schemas/ -- validation schemas for output records`
  - B: Paths grouped by purpose -- `Reference: [template, prompts] | Working data: [interviews, truth] | Validation: [schemas]`
  - C: No annotation -- instructions already explain what each location is for; annotations here would duplicate.
- HYPOTHESIS: Purpose annotations transform a permission list into a resource guide and may reduce aimless exploration. But they create maintenance burden and risk diverging from instructions. Grouping by purpose (B) is the stronger form -- it imposes a navigational mental model without per-path prose.
- STABILITY: **experimental**
- CONDITIONAL: annotation content is agent-specific (each agent's paths serve different purposes)

### section_heading
- CONVERGED: Both analyses agree "Security Boundary" is wrong -- it primes for compliance/restriction when the section's purpose is spatial orientation. Both propose territory-oriented alternatives.
- DIVERGED: B proposes "No heading" (merge content into another section). A does not consider section elimination.
- ALTERNATIVES:
  - A: `## Your Workspace` -- possessive, territory framing. The agent expects to learn about its space.
  - B: `## Operating Environment` -- neutral, environmental framing. Slightly more formal.
  - C: No standalone heading -- merge workspace_path and display entries into the input or identity section. Eliminates the section as a separate unit.
- HYPOTHESIS: "Your Workspace" is the strongest replacement because it is both accurate and territory-framing. "Operating Environment" is safe but clinical. Section elimination (C) is a structural question that depends on whether the prompt benefits from a dedicated spatial section or whether spatial data is better co-located with task context.
- STABILITY: **structural** (heading presence) + **experimental** (heading text)
- CONDITIONAL: none

### section_preamble
- CONVERGED: Both analyses want to replace the current implementation-leaking preamble. Both propose hybrid framing (boundary awareness + territorial confidence) as optimal.
- DIVERGED: B explicitly proposes "no preamble" as an option. A does not.
- ALTERNATIVES:
  - A: `All file operations are confined to {workspace_path}. Within this workspace, you can access:` -- hybrid. First sentence establishes hard boundary; second opens territory.
  - B: `You operate in {workspace_path}. The paths below are your working directories -- use them as needed.` -- action-oriented. Paths are resources, not grants.
  - C: No preamble -- workspace_path as label-value, then straight to entries. Avoids framing risk.
- HYPOTHESIS: The preamble's key job is establishing the workspace_path-to-display-entries relationship. Without a preamble, the agent must infer that relative paths resolve against the workspace root. The hybrid form (A) is most complete; the no-preamble form (C) is safest if workspace_path_presentation already carries the resolver framing.
- STABILITY: **experimental**
- CONDITIONAL: different preamble when display is empty vs. populated

### section_closing
- CONVERGED: Both analyses agree the current closing ("fail silently and cannot be approved interactively") is harmful -- it is cage framing, references irrelevant infrastructure, and may trigger ironic process effects (priming the concept of boundary violation). Both consider "no closing" as a valid option.
- DIVERGED: A proposes a **recovery path** closing ("report the gap rather than attempting access"). B proposes a **reassurance** closing ("These are all the paths you need"). A raises the ironic process concern (explicit prohibition may increase violation attempts) which B does not.
- ALTERNATIVES:
  - A: No closing -- the path list ends, the next section begins. Cleanest option with no framing risk.
  - B: `If your task requires access to a path not listed above, report this in your return status.` -- recovery path. Gives the agent a constructive response to boundary encounters instead of a prohibition.
  - C: `Operations outside these paths are not available.` -- factual environmental statement. No prohibition, no threat, just physics.
- HYPOTHESIS: No closing (A) is the default choice unless evidence shows agents benefit from explicit boundary reinforcement. The recovery path (B) is useful for agents whose tasks might legitimately encounter missing paths -- it converts a failure into a reportable condition. The ironic process concern is real: "do not attempt X" puts X in the agent's active context.
- STABILITY: **experimental**
- CONDITIONAL: recovery-path closing more useful for broad-access agents; no closing probably sufficient for no-grant agents

### permission_mode_display
- CONVERGED: Both analyses agree this is a defect, not a design choice. Implementation details (`bypassPermissions`, "hook-based restrictions") must not appear in agent prompts. The agent needs to know WHAT it can do, not HOW enforcement works.
- DIVERGED: none -- full agreement.
- ALTERNATIVES:
  - A: Omit entirely -- the only correct option. Implementation details belong in dispatch infrastructure, not behavioral programming.
- HYPOTHESIS: N/A -- this is a correctness fix, not a behavioral experiment.
- STABILITY: **structural** -- implementation details never leak into agent prompts
- CONDITIONAL: none

### empty_display_handler
- CONVERGED: Both analyses agree the current behavior (omit entire section when display is empty) is a clear defect. The summarizer still has a workspace_path and still needs a spatial anchor. Both propose rendering a minimal section.
- DIVERGED: A proposes an explicit "you have no filesystem access" variant and a "mediated access" variant. B proposes a single-line workspace_path in another section (preamble/input) as the minimum viable anchor.
- ALTERNATIVES:
  - A: Minimal section with workspace_path only -- `Your workspace root is {path}.` The section exists but is short.
  - B: Workspace_path + mediated-access note -- `Your workspace root is {path}. Your access is fully managed -- input arrives through a tempfile and output is written through a dedicated tool.` Explains WHY there are no grants.
  - C: No standalone section; workspace_path appears as a line in the input section or preamble -- minimum viable spatial anchor without a dedicated section.
- HYPOTHESIS: Option B (mediated-access note) is the most informative for processing-only agents because it preempts confusion: the agent understands its lack of grants is intentional, not an omission. Option A is sufficient if the input section already explains delivery mechanism. Option C is viable but weakens the cross-section reference from critical_rules.
- STABILITY: **structural** (section must exist for all agents) + **experimental** (content depth)
- CONDITIONAL: triggered when `display` array is empty

### section_position
- CONVERGED: Both analyses agree the section should come early in the prompt -- after identity, before instructions. The agent needs its spatial model before encountering task instructions that reference paths.
- DIVERGED: A proposes embedding territory in identity ("You are a definition author. Your workspace is..."). B proposes merging with input. Neither strongly advocates these over standalone-after-identity.
- ALTERNATIVES:
  - A: Immediately after identity, standalone -- the natural "who am I, where am I, what do I do" sequence.
  - B: Merged with input section -- spatial context + task inputs as one "what you have to work with" unit.
- HYPOTHESIS: Standalone after identity preserves clear section boundaries and ensures workspace_path is established before critical_rules references it. Merging with input is compact but conflates two concerns (where you can go vs. what you received).
- STABILITY: **structural**
- CONDITIONAL: none

### display_entry_separator
- CONVERGED: Both analyses agree the format should adapt to whether tool sets are homogeneous or heterogeneous across entries.
- DIVERGED: A proposes inline comma-separated paths when tool sets are uniform. B does not go this far.
- ALTERNATIVES:
  - A: Bullet list -- standard, per-entry, works universally.
  - B: Grouped under shared tool header when tool sets are uniform -- most compact, emphasizes territory over individual grants.
- HYPOTHESIS: The separator choice is downstream of the compound_entry_template decision. If grouped format is chosen for uniform tool sets, entries become a simple path list under one header.
- STABILITY: **formatting**
- CONDITIONAL: format changes based on tool-set uniformity

### workspace_topology (A only)
- CONVERGED: N/A -- only Analysis A identified this.
- DIVERGED: A proposes a directory tree view showing the hierarchical relationship between granted paths. B does not consider this.
- ALTERNATIVES:
  - A: ASCII tree showing path hierarchy -- makes sibling/parent relationships visible.
  - B: Omit -- the flat list is sufficient and a tree adds visual bulk.
- HYPOTHESIS: The tree may help agents with many grants (7+) understand path relationships, but for most cases the flat list is sufficient. Low priority.
- STABILITY: **formatting**
- CONDITIONAL: potentially useful when entry count exceeds ~5 and paths share common prefixes

### capability_inference_hint (A only)
- CONVERGED: N/A -- only Analysis A identified this.
- DIVERGED: A notes that the builder's grants are all read-oriented (Glob, Grep, Read, find) with no write tools, but this is never stated explicitly. The agent must infer its read-only status.
- ALTERNATIVES:
  - A: Explicit statement -- `Your access to these locations is read-only. Output is handled through a separate channel.`
  - B: Omit -- tool names already imply read-only; explicit statement may over-constrain.
- HYPOTHESIS: An explicit read-only/read-write label helps the agent plan its output strategy from the start. Worth testing for agents where the distinction matters.
- STABILITY: **experimental**
- CONDITIONAL: content varies based on whether grants include write-capable tools

## Cross-Section Dependencies

1. **workspace_path -> critical_rules (workspace confinement)**: The critical_rules section contains a confinement rule referencing workspace_path. If security_boundary is presented first, the confinement rule REINFORCES an already-established spatial root. If security_boundary is omitted (empty display, defective renderer), the confinement rule must INTRODUCE the workspace path cold -- which is disorienting and less authoritative. Both analyses agree: security_boundary must come first, and both sections must use compatible but differentiated framing for the same path (spatial home vs. inviolable boundary).

2. **display entries -> instructions**: Instructions reference paths that should appear in the display grants. If instructions reference a location not in the display array, the agent perceives a contradiction. The display entries establish the navigable territory; the instructions assume it.

3. **workspace_path -> output section**: The output directory is a path within the workspace. The agent should recognize this relationship. The workspace_path establishes the root; the output directory is a known branch.

4. **security_boundary -> identity**: An agent's territory shapes its operational character. A "definition author" with access to definitions/prompts/schemas has a different self-model than a "summarizer" with no filesystem territory. Territory and identity must not contradict each other.

## Conditional Branches

1. **display array empty vs. populated** -> When empty: render minimal section (workspace_path + optional mediated-access note). When populated: render full section with entries.

2. **tool-set uniformity** -> When all entries share the same tools: use grouped format (tools once as header, paths as list). When tools differ per entry: use per-entry path-first list.

3. **entry count** -> 0: handled by branch 1. 1-3: simple list or prose. 4-7: structured list with intro. 8+: grouping by purpose or path hierarchy.

4. **file vs. directory paths** -> Entries pointing to specific files vs. directories may benefit from different treatment (the trailing `/` convention may be insufficient for some agents to distinguish).

## Open Design Questions

1. **Should tool names appear in the display at all?** Hooks enforce actual grants regardless of prompt content. If tools in the prompt are purely advisory, displaying them may waste tokens with no behavioral benefit. No evidence either way -- requires testing.

2. **Environmental framing ("does not exist from your perspective") vs. territory framing ("your workspace")** -- which produces better boundary compliance without compliance anxiety? A identified this as a distinct third option; B treated territory as the primary alternative to cage. The three-way choice is unresolved.

3. **Should the section exist as standalone or merge into another section (input, identity)?** Both analyses raised this but neither committed. Standalone is simpler and preserves clear cross-section references. Merged is more compact. The answer may depend on how many other sections reference workspace_path.

4. **Purpose annotations on paths -- worth the maintenance cost?** Both analyses see potential for reducing aimless exploration, but annotations duplicate information from instructions and must be kept in sync.

## Key Design Decisions

1. **Always render the section, even for empty-display agents.** Both analyses converge with high confidence. The workspace_path is the spatial root for every agent. Omitting it is a defect. Direction: render a minimal section (workspace_path + mediated-access note) when display is empty.

2. **Territory framing, not cage framing.** Both analyses converge. The section should present paths as resources the agent HAS, not restrictions it must obey. Prohibition-style warnings should be absent from this section (confinement enforcement belongs in critical_rules). Direction: territory or environmental framing throughout.

3. **Path-first ordering for compound entries.** Both analyses converge. The agent's decision flow is location-first ("where is the file?"), not tool-first ("what tool do I use?"). Direction: path as primary key, tools as annotation.

4. **Grouped format when tool sets are uniform.** Both analyses converge. When all entries share the same tools, per-entry tool repetition is noise. State tools once, list paths. Direction: conditional format based on tool-set homogeneity.

5. **No implementation details in agent prompts.** Both analyses converge. `bypassPermissions`, "hook-based restrictions", and similar infrastructure language must never appear. The agent needs WHAT it can do, not HOW enforcement works. Direction: omit entirely.
