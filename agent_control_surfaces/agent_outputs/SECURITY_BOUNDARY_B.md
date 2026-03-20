# Security Boundary Section: Control Surface Analysis (Agent B)

## SECTION-LEVEL PURPOSE: What Must the Agent Be After Reading This?

The security boundary section does not exist to restrict the agent. It exists to give the agent a spatial self-model: a sense of where it is, where it can go, and what it can do in each place. An agent without this section is locationless. An agent with this section inhabits a territory.

This is a crucial distinction. "Security boundary" as a concept name suggests restriction, perimeter, defense. But the behavioral effect the section must produce is not caution or compliance. It is ORIENTATION. The agent must finish reading this section with a working mental map: "I exist at this root. These are the places I can reach. These are the operations available to me at each place." That mental map then shapes every subsequent decision. When the agent encounters an instruction that says "read the template file," the mental map resolves that instruction immediately — the agent knows where the template file lives and which tools it has there. Without the map, the instruction floats in the abstract.

This reveals the fundamental design tension of the section: the data encodes ACCESS CONTROL (which paths, which tools), but the behavioral effect needed is SPATIAL AWARENESS (where am I, where can I go). The section must transform access control data into a spatial understanding.

### The cage-vs-territory framing

Consider two framings for the same data:

**Cage framing:** "You are restricted to the following paths. Operations outside these paths will be rejected. Do not attempt to access anything not listed below."

**Territory framing:** "Your workspace is rooted at /Users/johnny/.ai/spaces/bragi. The following paths are available to you for the listed operations."

Both contain identical information. Both result in the same operational permissions. But they configure radically different default behaviors:

- The cage-framed agent starts from a posture of "I cannot do most things." Its first instinct when encountering a novel situation is to check whether it is allowed. It is hesitant. It asks permission mentally before acting. It may fail to use legitimate paths because it is uncertain whether they are within bounds.

- The territory-framed agent starts from a posture of "I know my space." Its first instinct when encountering a novel situation is to consult its mental map. It is confident within its territory and does not attempt to leave it — not because leaving is forbidden, but because its territory contains everything it needs.

The cage framing is safer but slower and more error-prone (the agent second-guesses legitimate actions). The territory framing is more productive but risks boundary-testing if the territory description feels incomplete. The optimal framing may be hybrid: empowering within, absolute at the boundary.

### What the defective renderer currently does

Agent-builder (7 display entries):
```
## Security Boundary

This agent operates under `bypassPermissions` with hook-based restrictions.

The following operations are allowed — everything else is blocked by the system.

**Glob, Grep, Read, find:** `./definitions/agents/agent-template.toml`
**Glob, Grep, Read, find:** `./definitions/audit/`
**Glob, Grep, Read, find:** `./definitions/prompts/`
**Glob, Grep, Read, find:** `./definitions/staging/`
**Glob, Grep, Read, find:** `./interview/`
**Glob, Grep, Read, find:** `./schemas/`
**Glob, Grep, Read, find:** `./truth/`

Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.
```

Interview-summary (0 display entries): **The section is completely absent.** No heading, no workspace path, no acknowledgment that a security boundary exists.

Observations about the defective output:

1. The preamble "This agent operates under `bypassPermissions` with hook-based restrictions" leaks infrastructure implementation details (`bypassPermissions`, "hook-based"). The agent does not need to know HOW its permissions are enforced — it needs to know WHAT it can do. Telling it about hooks and bypass modes is like explaining to a carpenter that the house frame uses a specific nail standard — irrelevant to building the house.

2. The compound entries display tools first, path second: `**Glob, Grep, Read, find:** ./path/`. This is backwards from the agent's mental model. The agent thinks "I need to read the template file" (path first), not "I want to use Read" (tool first). The path is the primary key; the tools are metadata about what is available at that path.

3. When the display array is empty (summarizer), the entire section vanishes. This is a design failure. The summarizer still has a workspace_path. It still operates within a boundary. It still needs a spatial self-model. The section should exist for every agent — the display entries are optional enrichment, not the section's reason for being.

4. The paths use relative notation (`./definitions/...`) but the workspace_path is never shown. The agent has no way to resolve these paths to absolute locations. The relationship between the workspace root and the display paths is implicit.

5. The closing warning "Do not attempt operations outside this boundary. They will fail silently" is cage framing. It also makes a specific claim ("fail silently") that may or may not be accurate depending on the infrastructure configuration.

---

## FIELD: workspace_path

TYPE: string (absolute filesystem path)
OPTIONAL: no (always present for every agent)
VALUES: `/Users/johnny/.ai/spaces/bragi` / `/Users/johnny/.ai/spaces/bragi`

### What the agent needs to understand

This is the most important field in the section because it defines the agent's HOME. Not its boundary, not its restriction — its home. Every other path in the entire prompt (display entries, output directories, schema paths, context file paths) is either inside this path or resolved relative to it. The workspace_path is the root of the agent's universe.

The field carries two kinds of information:
1. **Absolute location**: The agent knows exactly where it is in the filesystem. This matters for resolving relative paths, for understanding absolute paths in other sections (output directory, schema paths), and for constructing any paths it needs to.
2. **Boundary semantics**: Everything the agent does happens under this path. This is the spatial root constraint that the critical_rules section's workspace confinement rule reinforces.

The workspace_path is identical for both reference agents because they share a workspace. In a multi-workspace system, this would vary. But even when identical, the FRAMING of how this path is presented produces different behavioral effects.

### Fragments

**workspace_path_presentation**
- Current (defective): The workspace_path is not explicitly shown to the agent-builder — it appears only in the preamble subtext. For the summarizer, the entire section is missing.
- Alternative A: `Your workspace root is /Users/johnny/.ai/spaces/bragi.` — factual statement. The agent is told where it is. No emotional loading. "Root" establishes hierarchy — everything hangs from this path.
- Alternative B: `You operate within /Users/johnny/.ai/spaces/bragi. All paths in this prompt are relative to or contained within this directory.` — factual statement PLUS the key relationship: all other paths in the prompt connect to this one. This teaches the agent to use workspace_path as a resolver.
- Alternative C: `Workspace: /Users/johnny/.ai/spaces/bragi` — label-value pair. Minimal prose. Lets the path speak for itself. The label "Workspace" is neutral — neither restrictive nor expansive.
- Alternative D: `Home directory: /Users/johnny/.ai/spaces/bragi` — "home" is a loaded word. It implies belonging, familiarity, safety. An agent that sees this as its home may treat it differently than one that sees it as its "workspace" (a more transactional framing) or its "boundary" (a restrictive framing).
- PURPOSE: Establishes the agent's spatial root — the single absolute reference point from which the entire filesystem mental model is built.
- HYPOTHESIS: The key variable is whether the presentation teaches the agent that this path is a RESOLVER (Alternative B) or just a FACT (A, C, D). The resolver framing is operationally useful — the agent encounters relative paths in display entries and absolute paths in other sections, and understanding that all of them connect to workspace_path reduces path confusion. The minimal framing (C) is cleanest but misses the resolver relationship. "Home" (D) is behaviorally interesting — it may make the agent more comfortable operating freely within the path and less likely to attempt to leave — but it is a hypothesis without evidence. Test: does the resolver framing (B) reduce path-related errors compared to minimal framing (C)?
- STABILITY: structural (the path must be presented) + experimental (framing — fact vs. resolver vs. home)

---

## FIELD: display (array of compound entries)

TYPE: array of {path: string, tools: string[]}
OPTIONAL: yes (empty for interview-enrich-create-summary, 7 entries for agent-builder)
VALUES: 7 compound entries / empty array

### What the agent needs to understand

Each display entry is a LOCATION + CAPABILITY pair: "At this path, you can use these tools." Together, the display array forms the agent's operational map. This is the navigable territory — not just where the agent exists (workspace_path), but where it can ACT and what actions are available at each place.

The compound nature of each entry is the core design challenge. A display entry is not a path (a location) and not a tool grant (a capability). It is the intersection: a capability bound to a location. The template must present this compound data in a way that the agent reads as "place + what I can do there," not as two separate lists.

### Sub-analysis: the compound entry template

The compound entry is the section's atomic presentation unit. Every entry has two fields:
- `path`: a relative path (relative to workspace_path)
- `tools`: an array of tool names available at that path

The design space for presenting this compound data:

**Tool-first (current defective approach):**
```
**Glob, Grep, Read, find:** `./definitions/prompts/`
```
This reads as "these tools can access this path." The tool is the subject. The path is the object.

**Path-first:**
```
`./definitions/prompts/` — Glob, Grep, Read, find
```
This reads as "at this path, you have these tools." The path is the subject. The tools are metadata.

**Sentence form:**
```
You can search, read, and explore `./definitions/prompts/`.
```
This dissolves the tools into natural language verbs. The agent understands the CAPABILITY without tracking tool names.

**Table form:**
```
| Path | Available Operations |
|------|---------------------|
| ./definitions/prompts/ | Glob, Grep, Read, find |
```
This presents the data as structured reference. Compact for many entries. But may be processed as a data table to reference later rather than as a spatial model to internalize now.

**Resolved path form:**
```
/Users/johnny/.ai/spaces/bragi/definitions/prompts/ — Glob, Grep, Read, find
```
This resolves the relative path against workspace_path and shows the absolute path. The agent never has to mentally resolve `./` against the workspace root. But it is longer and the repeated prefix creates visual noise.

**Grouped by capability (transposed view):**
```
Search and read (Glob, Grep, Read, find):
- ./definitions/agents/agent-template.toml
- ./definitions/audit/
- ./definitions/prompts/
- ./definitions/staging/
- ./interview/
- ./schemas/
- ./truth/
```
When all entries share the same tool set (as in agent-builder), the tool list is redundant per entry. Grouping by capability and listing paths underneath is more compact and emphasizes the TERRITORY rather than the per-entry grants. But this structure breaks when different entries have different tool sets.

Each of these produces different agent behavior. The tool-first format makes the agent think in terms of capabilities ("I can Read this, I can Grep that"). The path-first format makes the agent think in terms of locations ("in this directory, these things are possible"). The sentence form makes the agent think in terms of actions ("I can do X here"). The table form makes the agent think in terms of lookup ("let me check what I can do at this path"). The grouped form makes the agent think in terms of territory ("these are all the places I can search").

### Fragments

**compound_entry_template**
- Current (defective): `**{tools joined by ", "}:** \`{path}\`` — tool-first, bold tools, backtick path, one per line
- Alternative A: `\`{path}\` — {tools joined by ", "}` — path-first, en-dash separator, tools as trailing metadata
- Alternative B: `- **{path}**: {tools joined by ", "}` — bulleted list, bold path, tools as description — standard definition-list feel
- Alternative C: Table format (see sub-analysis above) — useful when entries are numerous and the agent benefits from scannable reference
- Alternative D: Grouped by tool set — collapses redundancy when many entries share the same grant set, shows the territory as a cohesive unit
- Alternative E: Sentence dissolution — `You can search and read \`{path}\`.` — no tool names, just capability description in natural language
- PURPOSE: Presents the path-tool pair as a coherent unit that the agent can internalize into its spatial model.
- HYPOTHESIS: Path-first ordering (A, B) better serves the agent's decision flow: "I need X -> where is it? -> what can I do there?" Tool-first ordering (current) serves a different flow: "I have this tool -> where can I use it?" The path-first flow matches how agents actually work — they encounter a NEED (read a file, search for a pattern) and then locate the relevant path. Tool-first is useful only if the agent needs to reason about its capabilities abstractly, which is uncommon. The table format (C) is optimal for 5+ entries because it keeps the section compact and scannable, but may be read as data rather than internalized as spatial knowledge. Grouped format (D) is optimal when tool sets are homogeneous (as in agent-builder where all 7 entries share identical grants). Sentence form (E) maximizes internalization but is verbose and may obscure the exact tool names when precision matters. Test: does path-first ordering reduce instances of the agent attempting to use a tool at an unauthorized path, compared to tool-first?
- STABILITY: formatting (path-first vs. tool-first, list vs. table) + experimental (sentence dissolution, grouped format)

---

## STRUCTURAL: section_heading

TYPE: n/a (template-generated, not data-driven)

### What the agent needs to understand

The heading names the section and primes the agent for what follows. The current heading "Security Boundary" foregrounds SECURITY — a concept that primes for restriction, caution, and defensive behavior. But the section's purpose (as analyzed above) is SPATIAL ORIENTATION — giving the agent a map. The heading choice affects whether the agent reads the section as "here is what I cannot do" or "here is what I can do."

### Fragments

**section_heading_text**
- Current (defective): `## Security Boundary` — frames the section as a security construct. The agent processes it through a compliance lens.
- Alternative A: `## Workspace` — neutral naming. This section describes the workspace. Not a boundary, not a restriction — the workspace.
- Alternative B: `## Your Environment` — frames the section as a description of the agent's environment. "Your" makes it personal. "Environment" suggests something to be understood, not complied with.
- Alternative C: `## Operational Scope` — frames as scope (what you can do) rather than boundary (what you cannot). "Operational" connects to action rather than restriction.
- Alternative D: `## File Access` — bluntly descriptive. Names what the section actually contains: information about file access. No framing, no metaphor.
- Alternative E: No heading. Merge the workspace root and path grants into the section that needs them most (input section, or as a preamble to the entire prompt). The security boundary may not need to be a standalone section at all.
- PURPOSE: Names the section and primes the agent's processing mode for what follows.
- HYPOTHESIS: "Security Boundary" activates a compliance schema — the agent expects restrictions and processes the content defensively. "Workspace" is neutral and lets the content set the tone. "Your Environment" is the most territory-framing heading — it tells the agent "this describes YOUR space." "Operational Scope" emphasizes what the agent CAN do. "File Access" is flat and informational. The merge option (E) is radical but worth considering: if the workspace path is always mentioned in critical_rules (workspace confinement) and the display entries primarily serve the agent during instruction execution, perhaps they belong closer to the instructions or input rather than in a standalone section. Test: does "Your Environment" produce more confident, efficient agent behavior than "Security Boundary"? Does merging the section away reduce agent awareness of its boundaries?
- STABILITY: structural (heading presence) + experimental (heading text and framing) + potentially structural (whether the section exists as standalone)

---

## STRUCTURAL: section_preamble

TYPE: n/a (template-generated prose that introduces the section content)

### What the agent needs to understand

The preamble sits between the heading and the path grants. It provides the interpretive frame through which the agent reads the grants. A preamble that says "you are restricted to" primes a different reading than one that says "you have access to." The preamble is the section's lens.

### Fragments

**preamble_text**
- Current (defective): Two sentences: `"This agent operates under bypassPermissions with hook-based restrictions."` + `"The following operations are allowed — everything else is blocked by the system."`
- Alternative A: `"Your workspace is rooted at {workspace_path}. You have access to the following paths:"` — territory framing. Leads with the root, introduces grants as things the agent HAS, not things it is limited to.
- Alternative B: `"All file operations are confined to {workspace_path}. Within this workspace, you can access:"` — hybrid framing. The first sentence establishes the boundary (cage), the second opens the territory within it (map). The agent understands both the hard limit AND its freedom within that limit.
- Alternative C: No preamble. Present workspace_path as a label-value pair and go straight to the path list. Let the data speak. Every word of preamble is a word that frames the data before the agent sees it — sometimes that framing helps, sometimes it primes incorrect expectations.
- Alternative D: `"You operate in {workspace_path}. The paths below are your working directories — use them as needed to complete your task."` — action-oriented framing. The paths are not grants or restrictions — they are the agent's working directories. This frames the data as a practical resource rather than an access control list.
- PURPOSE: Sets the interpretive frame for the path grants that follow. The preamble determines whether grants are read as permissions, resources, or territorial knowledge.
- HYPOTHESIS: The current defective preamble actively harms agent behavior by (1) exposing irrelevant infrastructure details and (2) using cage framing ("everything else is blocked"). Alternative B (hybrid) may be optimal — it gives the agent BOTH the boundary awareness it needs (for the critical_rules workspace confinement to make sense) AND the territorial confidence to act within its space. The no-preamble option (C) is appealing for the same reason it was appealing in the critical_rules analysis — every preamble is an opportunity to say the wrong thing. But security_boundary has an additional challenge: without a preamble, the relationship between workspace_path and the display entries is implicit. The agent must figure out on its own that `./definitions/prompts/` means `{workspace_path}/definitions/prompts/`. A preamble that mentions the root BEFORE the relative paths aids resolution. Test: does the hybrid framing (B) produce agents that are both confident and boundary-aware, or does the boundary mention in the first sentence override the territory framing in the second?
- STABILITY: experimental — the preamble is high-leverage because it frames ALL subsequent content

---

## STRUCTURAL: section_closing

TYPE: n/a (template-generated prose after the path grants)

### What the agent needs to understand

The closing appears after the path grants (if any) and is the last thing the agent reads before leaving the section. It is a final behavioral instruction about how to use the information just presented.

### Fragments

**closing_text**
- Current (defective): `"Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."` — cage framing. Threatens failure. References interactive approval (irrelevant to an autonomous agent).
- Alternative A: No closing. The path list ends and the next section begins. The section is purely informational — it does not need to tell the agent what to do with the information.
- Alternative B: `"Operations outside these paths are not available."` — factual, not threatening. States a condition of the environment rather than issuing a prohibition. The agent does not need to be told not to try — it is told that there is nothing there.
- Alternative C: `"If your task requires access to a path not listed above, report this in your return status rather than attempting to access it."` — gives the agent a RECOVERY PATH. Instead of threatening failure, it tells the agent what to do when it encounters a boundary. This is operationally more useful than "do not attempt."
- Alternative D: `"These are all the paths you need. Your task is fully completable within this scope."` — reassurance framing. The agent is told that its territory is sufficient. This counters the LLM instinct to seek more information or broader access. The message is: you have everything you need.
- PURPOSE: Provides final behavioral instruction about the agent's relationship to its operational territory.
- HYPOTHESIS: The current defective closing is actively harmful — "fail silently" may cause the agent to become paranoid about boundary violations and over-cautious. Alternative A (no closing) is simplest and avoids the risk of bad framing. Alternative B (factual) is safe. Alternative C (recovery path) is operationally useful for agents that encounter unexpected needs. Alternative D (reassurance) is behaviorally interesting — it may reduce the agent's tendency to explore beyond its grants when it feels uncertain. But it makes a claim ("fully completable") that may not always be true, and a false reassurance discovered mid-task is worse than no reassurance. The best closing may depend on whether the agent has few grants (reassurance helps) or many grants (reassurance is unnecessary). Test: does the recovery-path closing (C) produce better failure reports when agents hit boundary issues, compared to no closing (A)?
- STABILITY: experimental — the closing has leverage because it is the agent's last impression before moving to the next section

---

## CONDITIONAL BRANCH: display array present vs. empty

This is the section's most important structural decision. Two agents exist in the data:

1. **agent-builder**: 7 display entries, all with identical tool grants (Glob, Grep, Read, find). A rich spatial map.
2. **interview-enrich-create-summary**: 0 display entries. No explicit path grants displayed. Its file access is entirely handled by infrastructure (hook-gated Read to `/tmp/bragi/cobalt-stage/` and Bash gated to the output tool).

The current defective renderer handles this by omitting the entire section when display is empty. This is wrong. The summarizer still has a workspace_path. It still operates within a spatial boundary. It still benefits from knowing where it is.

### What should happen when display is empty?

**Option 1: Omit the section entirely (current behavior).** The agent gets no spatial model. It does not know its workspace root. The critical_rules workspace confinement rule references a boundary the agent has never been told about.

**Option 2: Show the section with workspace_path only.** The agent knows where it is. It has no explicit path grants — but it does not need them. Its access is infrastructure-mediated (tempfile input, output tool). The section exists but is minimal:
```
## Workspace

Your workspace root is /Users/johnny/.ai/spaces/bragi.
```

**Option 3: Show the section with workspace_path and an explicit note about infrastructure-mediated access.** The agent knows where it is AND knows that its file access is handled through its input/output mechanisms rather than direct path grants:
```
## Workspace

Your workspace root is /Users/johnny/.ai/spaces/bragi.

Your file access is provided through your input delivery and output tool. No additional path grants are needed.
```

**Option 4: Show the section with workspace_path and a different kind of map — show the paths that the agent's infrastructure provides access to, even though they are not in the display array.** This would mean deriving implicit path information from other sections (tempdir from input, output directory from writing_output) and presenting it here. This enriches the agent's spatial model but creates cross-section content generation complexity.

### Fragments

**empty_display_handler**
- Current (defective): Section omitted entirely
- Alternative A: Section present with workspace_path only — minimal but establishes spatial root
- Alternative B: Section present with workspace_path + explanatory note about infrastructure-mediated access — the agent understands WHY there are no grants (not because it has no access, but because its access comes through different channels)
- Alternative C: Section present with workspace_path + derived map from other sections — richest spatial model but highest template complexity
- Alternative D: Section replaced by a single line in the preamble or input section — `Workspace: /Users/johnny/.ai/spaces/bragi` — the minimum viable spatial anchor without a dedicated section
- PURPOSE: Ensures that agents with no explicit display grants still have a spatial self-model.
- HYPOTHESIS: Option 1 (current) is a clear failure — it creates a gap in the agent's understanding that the critical_rules section later tries to fill from the other direction. Option 2 (minimal) is probably sufficient — the workspace root is the most important piece of spatial information and the summarizer does not need a directory map. Option 3 (explanatory) is useful if agents with no display grants tend to be confused about their access — the note preempts confusion. Option 4 (derived) is the richest but may be over-engineering — if the agent already sees its tempdir in the input section and its output path in the writing_output section, re-presenting them in a spatial map may be redundant. Test: do agents with no display grants perform differently when they receive workspace_path only (Option 2) vs. the full omission (Option 1)?
- STABILITY: structural (whether the section exists for empty-display agents) + experimental (what content it contains)

---

## CROSS-SECTION DEPENDENCY: workspace_path used by critical_rules

The `workspace_path` field lives in `[security_boundary]` but is consumed by the `[critical_rules]` section for the workspace confinement rule. This creates a cross-section data dependency that has design implications.

### The dependency chain

1. `security_boundary.workspace_path` defines the agent's root
2. `critical_rules` contains a workspace confinement rule that says (in effect) "do not operate outside {workspace_path}"
3. The confinement rule references a path that was (should have been) introduced in the security_boundary section

### Design implications

**Ordering matters.** If security_boundary is presented BEFORE critical_rules (as in the current defective renderer's section ordering for agent-builder), the confinement rule can REFERENCE the already-established workspace root. The agent reads "your workspace is X" first, then later reads "never leave X." The second reinforces the first.

If critical_rules comes FIRST (possible in a reordered prompt), the confinement rule introduces a boundary the agent has not yet been told about. It must introduce the workspace_path inline or the rule will feel groundless.

**Reinforcement vs. redundancy.** The workspace_path appearing in both sections creates an intentional redundancy. Security_boundary introduces the spatial model; critical_rules elevates the boundary to inviolable status. This is reinforcement, not duplication — the same data serves different behavioral purposes in different sections. But the template must be aware of this: if security_boundary already says "all operations are confined to X" AND critical_rules says "never operate outside X," the combined effect might be interpreted as anxiety rather than authority. The two sections should use different language to frame the same constraint at different authority levels.

**The empty-display case is especially fragile here.** If the security boundary section is omitted (as the defective renderer does for the summarizer), the critical_rules workspace confinement rule must introduce the workspace_path cold. The agent has never heard of this path before, and suddenly it is a critical rule. This is disorienting. It is another argument for always presenting the security_boundary section, even when display is empty — it ensures the critical_rules section can reference rather than introduce the workspace root.

### Fragments

**workspace_path_cross_reference_in_critical_rules**
- If security_boundary is presented first: `"All operations must remain within your workspace."` — the workspace has already been established; the rule can reference it by name.
- If security_boundary is omitted (empty display, bad design): `"All operations must remain within /Users/johnny/.ai/spaces/bragi."` — the rule must introduce the path because no earlier section did.
- If both sections present the path: the template must ensure different framing — security_boundary for spatial understanding, critical_rules for behavioral enforcement. Same data, different purpose.
- PURPOSE: Ensures the workspace confinement rule connects to the agent's spatial model rather than introducing an ungrounded constraint.
- HYPOTHESIS: The cross-reference is smoother and more authoritative when security_boundary comes first. The confinement rule gains authority by REINFORCING something the agent already believes, rather than INTRODUCING something new. This is a standard persuasion principle: alignment with prior beliefs increases compliance. Test: does the confinement rule produce higher compliance when it references an already-established workspace (security_boundary first) vs. introducing the workspace cold (critical_rules first, or security_boundary omitted)?
- STABILITY: structural — this dependency is a fixed property of the data model

---

## STRUCTURAL: section_position

TYPE: n/a (template-level ordering decision)

### What the agent needs to understand

Where the security boundary section appears in the overall prompt determines when the agent builds its spatial model. This is not a fragment within the section — it is a property of the section's relationship to other sections.

### Fragments

**section_position_in_prompt**
- Current (defective): Security boundary appears after identity and before input. For the summarizer, it is omitted entirely.
- Alternative A: Immediately after identity, before everything else. The agent knows WHO it is (identity), then WHERE it is (security_boundary), then WHAT to do (instructions). This is the natural human onboarding sequence: name, location, task.
- Alternative B: Immediately before instructions. The agent knows its identity, input, and operational context, then receives its spatial map right before it needs it (the instructions reference paths). This is just-in-time spatial information.
- Alternative C: Merged into input section. The workspace_path and display entries become part of the input context — "here is what you are given AND here is where you can find additional resources." This eliminates the standalone section but tightly couples spatial information with task context.
- Alternative D: At the very end, as a reference appendix. The agent reads all behavioral programming first, then receives the spatial reference at the end. This treats the path grants as lookup data rather than as foundational context.
- PURPOSE: Determines when the agent builds its spatial model relative to other behavioral programming.
- HYPOTHESIS: Position A (after identity) is consistent with the territory framing — the agent establishes its spatial model early and carries it through all subsequent sections. The instructions, examples, and output sections can all reference paths without needing to reintroduce them. Position B (before instructions) is just-in-time but means that the critical_rules workspace confinement rule (which typically appears late in the prompt) references a workspace introduced only recently. Position C (merged with input) is compact but conflates two different concepts: input delivery (what you receive) and spatial access (where you can go). Position D (appendix) is weakest — the agent has already processed instructions and may have formed assumptions about its environment. Test: does early spatial model establishment (A) produce fewer path-related errors than late establishment (B, D)?
- STABILITY: structural — section ordering is a high-level template decision that changes rarely once set

---

## STRUCTURAL: display_entry_separator

TYPE: n/a (formatting between compound entries)

### What the agent needs to understand

When multiple display entries exist, the visual separator between them affects whether the agent reads them as a continuous list (one coherent territory) or as individual grants (separate permissions). This is a low-level formatting choice with subtle behavioral effects.

### Fragments

**entry_separator**
- Current (defective): Newline-separated bold lines — each entry on its own line with no explicit separator.
- Alternative A: Bullet list — `- \`./path/\` — tools` — standard markdown list. Groups entries as peers.
- Alternative B: Table — entries in rows. Most compact for many entries. Processed as data reference.
- Alternative C: Newline-separated with grouping — entries with identical tool sets grouped under a shared tool header. Reduces visual repetition.
- Alternative D: Comma-separated inline — `./definitions/prompts/, ./definitions/staging/, ./schemas/` — when tool sets are identical, collapse to a path list with a single tool header. Most compact representation.
- PURPOSE: Determines how the agent perceives the relationship between entries — as a cohesive map or as individual grants.
- HYPOTHESIS: When all entries share the same tool set (agent-builder: all 7 are Glob/Grep/Read/find), repeating the tool set 7 times is wasteful and makes each entry feel like a separate permission rather than part of one territory. The grouped format (C) or inline format (D) would present the SAME information as "you can search and read all of these" rather than "you have 7 separate permissions." When entries have different tool sets, per-entry display is necessary. Test: does grouped display produce a more cohesive spatial model (fewer boundary-confusion errors) than per-entry display?
- STABILITY: formatting — this changes based on the data shape (homogeneous vs. heterogeneous tool sets)

---

## SYNTHESIS: The Section as a Whole

### What the section accomplishes

The security boundary section transforms access control data (workspace_path, path-tool pairs) into a spatial self-model. The agent finishes the section knowing: where it is, where it can go, and what it can do in each place. This spatial model persists throughout the agent's entire run and is consulted implicitly every time the agent interacts with the filesystem.

### The critical design decisions (in order of leverage)

1. **Whether the section exists for empty-display agents.** This is binary and structural. The current omission is a clear defect. The section should always exist when workspace_path exists — which is always.

2. **Cage vs. territory framing.** The preamble and closing together establish whether the agent reads its grants as restrictions or as resources. This affects every subsequent operation. The optimal framing is probably hybrid: territorial within, absolute at the boundary.

3. **Compound entry format.** Path-first vs. tool-first ordering. Table vs. list vs. grouped. This determines whether the agent's spatial model is organized by LOCATION (where can I go?) or by CAPABILITY (what can I use?). Location-organized is more natural for how agents actually work.

4. **Section position relative to critical_rules.** The workspace confinement rule in critical_rules depends on the agent already knowing its workspace root. Security_boundary should come first.

5. **Cross-section workspace_path framing.** The same path appears in security_boundary and critical_rules but serves different purposes. Security_boundary introduces it as spatial home; critical_rules enforces it as hard boundary. Different prose for the same data.

### The full template structure (sketch)

For agents WITH display entries:
```
{section_heading}

{preamble with workspace_path — territory framing}

{display entries — path-first, grouped when tool sets are homogeneous}

{closing — optional, recovery-path or reassurance framing}
```

For agents WITHOUT display entries:
```
{section_heading}

{workspace_path_only presentation — minimal spatial anchor}
```

### Open questions for synthesis

1. Should the section heading be "Security Boundary" or something that primes for territory rather than restriction?
2. Should the display entries use resolved absolute paths or relative paths with the workspace_path established separately?
3. Should the closing exist at all, or should the section end cleanly after the path grants?
4. When all entries share tool sets, should the template automatically group them, or should per-entry display be the universal format?
5. Should the section exist as a standalone, or is there a stronger home for this data (merged into input, preamble, or a combined "environment" section)?
