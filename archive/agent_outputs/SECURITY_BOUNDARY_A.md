# Security Boundary Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The security boundary section must configure the agent's spatial awareness -- its understanding of where it exists, what territory it can reach, and what lies beyond its world. This is not a list of permissions to remember. It is the agent's operational geography.

After reading this section, the agent should have internalized:

1. **Where it lives.** The workspace path is not just a configuration value -- it is the agent's sense of place. Every relative path, every file reference, every tool invocation happens relative to this root. An agent that deeply understands its workspace path will resolve ambiguous references correctly, construct valid paths confidently, and never attempt to escape its boundary because the boundary IS the world.

2. **What it can see and touch.** The display entries (when present) are not a permissions list to consult before each action. They are the agent's mental map of its filesystem. An agent with 7 path grants should carry a spatial model: "I can look at definitions, prompts, staging, interviews, schemas, and truth data." An agent with 0 path grants should understand that its world is entirely mediated -- things arrive through its input channel and leave through its output channel, and it has no need to navigate the filesystem independently.

3. **The relationship between the root and the branches.** The workspace_path is the root. The display paths are branches. The agent must understand that `./definitions/prompts/` means `{workspace_path}/definitions/prompts/` -- that the relative notation is relative to ITS home, not to some abstract working directory. This resolution relationship is critical and easy to get wrong.

4. **What tools it wields where.** Each path grant is compound: a location AND the instruments available there. The agent does not just know "I can access ./schemas/" -- it knows "I can search, scan, and read ./schemas/ but I cannot write there." The tool list attached to each path creates a per-location capability profile.

5. **The shape of its autonomy.** An agent with many path grants is a navigator -- it must explore, discover, and gather. An agent with zero path grants is a processor -- it receives input and produces output. These are fundamentally different operational modes. The security boundary section configures which mode the agent operates in, which affects how it interprets every subsequent instruction.

### The cage-vs-territory problem

The most consequential design choice in this section is framing. The same data -- "you can access these 7 paths" -- can be presented as:

**Cage framing:** "You are restricted to the following paths. Everything else is blocked. Do not attempt to go beyond these boundaries." This produces a fearful, cautious agent that second-guesses every operation, adds unnecessary path validation to its reasoning, and wastes cognitive resources on compliance anxiety. The agent's primary relationship with its filesystem is adversarial -- the system is trying to prevent it from doing things.

**Territory framing:** "These are your operational areas. This is your workspace. Here is where your materials live." This produces a confident agent that navigates purposefully within its space. The agent's primary relationship with its filesystem is proprietary -- these are its resources, and it knows where everything is.

**Environmental framing:** "The workspace is at {path}. Operations outside this workspace are not possible -- the system does not support them." This produces an agent that treats the boundary as a physical law rather than a rule. It does not feel restricted because there is nothing to be restricted FROM. The boundary is simply the shape of reality.

The choice between these framings affects every subsequent section. An agent initialized with cage framing will interpret ambiguous instructions as potentially dangerous. An agent initialized with territory framing will interpret the same instructions as opportunities to use its resources. An agent with environmental framing will not even consider out-of-bounds operations because they are incoherent within its world model.

---

## FIELD: workspace_path
TYPE: string (absolute path)
OPTIONAL: no
VALUES: "/Users/johnny/.ai/spaces/bragi" / "/Users/johnny/.ai/spaces/bragi"

### What the agent needs to understand

This is the single most important field in the section. It appears in both agents with identical values. It serves three functions simultaneously:

1. **Root anchor:** Every relative path in the entire prompt resolves against this path. It is the coordinate origin.

2. **Confinement boundary:** The workspace path defines the outermost limit of the agent's filesystem access. This constraint appears not only here but also in the critical_rules section (cross-section dependency), where it becomes a violation-level rule.

3. **Identity grounding:** The workspace path tells the agent WHERE it exists. An agent at `/Users/johnny/.ai/spaces/bragi` is working in Bragi. This contextualizes all other information -- definitions, prompts, interviews, schemas all have meaning because of where they live.

The field is ALWAYS present and identical between agents. This makes it structurally invariant -- every agent in this workspace gets the same value. The presentation challenge is: how do you present a value that never varies but that must be deeply internalized?

### Fragments

**workspace_declaration**
- Current (defective): `This agent operates under bypassPermissions with hook-based restrictions.` -- the workspace path is not even mentioned in the agent-builder's security section; it appears only implicitly. For the summarizer, no security boundary section is rendered at all.
- Alternative A: `Your workspace is /Users/johnny/.ai/spaces/bragi.` -- simple declarative, treating the workspace as a fact about the agent's location
- Alternative B: `You operate within /Users/johnny/.ai/spaces/bragi. All paths in this prompt are relative to this root.` -- declarative plus functional explanation of what the path DOES
- Alternative C: `Workspace root: /Users/johnny/.ai/spaces/bragi` -- terse metadata-style, treating it as a configuration parameter
- Alternative D: `Your operational environment is rooted at /Users/johnny/.ai/spaces/bragi. Files and directories outside this tree do not exist from your perspective.` -- environmental framing that makes the boundary a physical law
- PURPOSE: Establishes the agent's sense of place and the root against which all paths resolve. This is the foundation that all display entries build on.
- HYPOTHESIS: The declarative form (A) treats the workspace as a datum to store. The functional form (B) teaches the agent what the path means operationally, which may reduce path-resolution errors. The terse form (C) signals "this is infrastructure, not behavioral" which may cause the agent to skip over it. The environmental form (D) implicitly communicates the confinement boundary without framing it as a restriction, which may produce the most natural compliance. Test: does environmental framing ("does not exist from your perspective") reduce out-of-bounds tool invocations compared to simple declaration?
- STABILITY: experimental (framing choice) + structural (the value itself always renders)

**path_resolution_instruction**
- Current (defective): not present -- the agent is never told how relative paths (./definitions/, ./schemas/) relate to the workspace path
- Alternative A: `Paths beginning with ./ are relative to the workspace root.` -- explicit resolution rule, placed near the workspace_path declaration
- Alternative B: No explicit instruction -- the display entries show resolved paths (absolute) so the agent never needs to resolve anything
- Alternative C: `Below, paths are shown relative to the workspace. ./definitions/ means /Users/johnny/.ai/spaces/bragi/definitions/.` -- one concrete example of resolution
- PURPOSE: Prevents path-resolution errors. The display entries use relative paths (./definitions/), but the workspace_path is absolute. The agent must understand the relationship.
- HYPOTHESIS: An explicit resolution rule (A) addresses the problem directly but adds instructional overhead. Showing resolved absolute paths (B) eliminates the need for the agent to do resolution but creates very long lines and loses the visual compactness of relative paths. A single concrete example (C) teaches by demonstration rather than rule, which LLMs may internalize more reliably. Test: do agents make fewer path errors when given an explicit resolution rule, or when shown one worked example?
- STABILITY: structural -- this is a correctness concern, not a behavioral experiment

---

## FIELD: display (array of path-tool compound entries)
TYPE: array of objects, each with `path` (string) and `tools` (array of strings)
OPTIONAL: yes (can be empty -- Agent 2 has NO entries)
VALUES: 7 entries for agent-builder / 0 entries for interview-summary

### What the agent needs to understand

This is the most complex field in the section because each entry is compound -- a pairing of WHERE (path) and HOW (tools). The agent needs to build a mental map that associates locations with capabilities. Not "I can use Glob" and separately "I can access ./definitions/" -- but "I can use Glob AT ./definitions/."

When present, the display array tells the agent: here is your operational territory, parcel by parcel, with the instruments you have at each location.

When absent (as for the summarizer), the section is telling the agent something equally important through OMISSION: you have no filesystem territory. Your world is your input channel and your output channel. There is nothing for you to explore.

This creates a fundamental conditional branch in the section's design.

### The compound entry design challenge

Each display entry pairs a path with a tool list. This pairing is the atomic unit of the section -- not the path alone, not the tool alone, but the combination. The template must present this compound as a coherent unit. Several approaches exist:

**Table format:**
```
| Path | Tools |
|---|---|
| ./definitions/agents/agent-template.toml | Glob, Grep, Read, find |
| ./definitions/audit/ | Glob, Grep, Read, find |
```
Advantages: visual density, scannable, paths and tools aligned in columns. Disadvantages: may feel like a data dump rather than a map; tables in prompts are sometimes poorly parsed by LLMs; loses the opportunity to provide per-entry context.

**List format (path-first):**
```
- ./definitions/agents/agent-template.toml -- Glob, Grep, Read, find
- ./definitions/audit/ -- Glob, Grep, Read, find
```
Advantages: compact, linear, easy to parse. Disadvantages: the dash-separator between path and tools is a formatting convention, not a semantic one; all entries look the same even if they serve different purposes.

**List format (tool-first):**
```
- Glob, Grep, Read, find: ./definitions/agents/agent-template.toml
- Glob, Grep, Read, find: ./definitions/audit/
```
Advantages: groups by capability first, which may help the agent think "what can I do?" before "where can I go?" Disadvantages: when tool lists are identical across entries (as in agent-builder, where ALL entries have the same 4 tools), the repeated tool prefix is visual noise.

**Grouped-by-tools format:**
```
**Glob, Grep, Read, find:**
- ./definitions/agents/agent-template.toml
- ./definitions/audit/
- ./definitions/prompts/
- ./definitions/staging/
- ./interview/
- ./schemas/
- ./truth/
```
Advantages: eliminates repetition when tool lists are identical; visually clean; emphasizes that the tool set is uniform. Disadvantages: breaks down when entries have DIFFERENT tool sets; imposes a grouping that may not be present in the data.

**Prose format:**
```
You can search, scan, and read files in these locations: ./definitions/agents/agent-template.toml, ./definitions/audit/, ./definitions/prompts/, ./definitions/staging/, ./interview/, ./schemas/, ./truth/.
```
Advantages: natural language, no structural overhead, integrates with the territory framing. Disadvantages: harder to parse for quick reference; may not scale to agents with heterogeneous tool grants.

The design choice depends on two data characteristics:
1. **Tool uniformity:** When all entries share the same tools (agent-builder), grouped-by-tools or prose is most efficient. When entries have different tools, per-entry formats (table, list) are necessary.
2. **Entry count:** A small number of entries (2-3) works in prose. A large number (7+) needs structured display.

### Fragments

**display_section_intro**
- Current (defective): `The following operations are allowed -- everything else is blocked by the system.` -- cage framing, prohibition-forward
- Alternative A: `Your operational areas and the tools available in each:` -- neutral inventory framing, territory-like
- Alternative B: `You have access to the following workspace locations:` -- territory framing, possessive
- Alternative C: `Your filesystem map:` -- metaphor framing, the entries are a map, not a permission list
- Alternative D: `These paths are yours to navigate. Everything you need is here.` -- empowering territory framing that also implies completeness (no need to look elsewhere)
- Alternative E: No introduction -- the entries appear immediately after workspace_path, with no connective prose
- PURPOSE: Frames how the agent interprets the entries that follow. This is where the cage/territory/environment decision is operationalized.
- HYPOTHESIS: Cage framing ("allowed...everything else blocked") activates a prohibition-monitoring mode where the agent checks each action against the permission list. Territory framing ("your areas", "yours to navigate") activates a resource-navigation mode where the agent consults its map to find what it needs. Map framing (C) converts the list into a spatial mental model. Completeness framing (D, "everything you need is here") reduces the probability that the agent will attempt to access paths not in the list by asserting there is no reason to. Test: does completeness framing reduce out-of-bounds attempts more effectively than prohibition framing?
- STABILITY: experimental -- this is one of the highest-leverage fragments in the section

**compound_entry_format**
- Current (defective): `**Glob, Grep, Read, find:** ./definitions/agents/agent-template.toml` -- bold tool list as a label prefix, followed by path. Tool-first ordering.
- Alternative A: `./definitions/agents/agent-template.toml (Glob, Grep, Read, find)` -- path-first with parenthetical tools, treating the location as primary and the capabilities as annotation
- Alternative B: Table with Path and Tools columns
- Alternative C: Grouped by tool set (as described above) -- all paths under their shared tool heading
- Alternative D: Natural prose per entry: `You can search and read ./definitions/agents/agent-template.toml.` -- tool names translated to verbs, path as the object
- Alternative E: Path only, tools omitted from display -- the tool grants are enforced by the hook system regardless of whether the agent knows about them
- PURPOSE: Controls how the agent perceives the path-tool pairing. Does it think "I have these tools, and here's where I use them" (tool-first) or "here are my locations, and here's what I can do there" (path-first)?
- HYPOTHESIS: Tool-first (current) primes the agent to think about capabilities before locations, which may be useful when the agent's task is tool-heavy. Path-first primes the agent to think about territory, which may be useful when the agent needs to navigate and discover. Grouped-by-tools eliminates repetition but may cause the agent to lose the per-path distinctiveness (it stops differentiating between "./schemas/" and "./truth/" because they have the same tools). Natural prose (D) makes each entry self-contained but does not scale well. Omitting tools entirely (E) is a radical simplification -- the hook system enforces the grants whether or not the agent is told about them, so displaying tools may be pure overhead. Test: does omitting tool names from the display change agent behavior at all, given that hooks enforce the real boundary?
- STABILITY: formatting (layout choice) + experimental (whether to display tools at all)

**compound_entry_path_style**
- Current (defective): relative paths with `./` prefix: `./definitions/agents/agent-template.toml`
- Alternative A: Absolute paths: `/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-template.toml` -- unambiguous but very long
- Alternative B: Bare relative paths without `./`: `definitions/agents/agent-template.toml` -- cleaner visually, but `./` is a conventional signal for "relative to here"
- Alternative C: Named paths: `definitions/agents/agent-template.toml (Agent Template)` -- path plus human-readable label
- PURPOSE: Affects path readability and whether the agent treats the paths as relative (needing resolution) or as addresses (ready to use).
- HYPOTHESIS: The `./` prefix signals "relative to the workspace root" which helps the agent resolve correctly. Absolute paths eliminate ambiguity but create visual clutter, especially when the workspace root is long. Named paths add semantic context ("Agent Template") that helps the agent understand WHY it has access to each location, not just WHERE the location is. Test: do named paths produce better-targeted access patterns (agent goes to the right location first) compared to bare paths?
- STABILITY: formatting

---

## FIELD: display[].path
TYPE: string (relative path)
OPTIONAL: (present within each display entry)
VALUES: "./definitions/agents/agent-template.toml", "./definitions/audit/", "./definitions/prompts/", "./definitions/staging/", "./interview/", "./schemas/", "./truth/" / (no entries)

### What the agent needs to understand

Each path identifies a location in the workspace. Some paths point to specific files (agent-template.toml), others to directories. The agent must understand this distinction: a file path grants access to that file; a directory path grants access to everything within that directory.

The paths collectively form a map of the agent's operational territory. For the builder agent, the map covers: the template reference, audit records, prompt include files, staging outputs, interview data, schema definitions, and truth system data. This is a broad map that supports a creative, exploratory task.

For the summarizer agent, there is no map. This is not an omission -- it is a signal that the agent's task does not involve filesystem navigation.

### Fragments

(Covered primarily in the compound entry discussion above. The path field's fragments are inseparable from how the compound entry is formatted.)

**path_semantic_annotation**
- Current (defective): paths appear without context -- the agent must infer why it has access to "./schemas/"
- Alternative A: Each path accompanied by a brief annotation: `./schemas/ -- validation schemas for output records`
- Alternative B: Paths grouped by purpose: "Reference materials: [template, prompts] | Working data: [interviews, truth] | Validation: [schemas] | Output staging: [staging, audit]"
- Alternative C: No annotation -- the agent should understand from its instructions what each location is for. Adding annotations to the security section duplicates information from the instructions.
- PURPOSE: Controls whether the security boundary section is purely structural (here are your paths) or also semantic (here is why you have each path).
- HYPOTHESIS: Annotations help the agent build a richer mental map and may reduce aimless exploration ("I have access to 7 paths -- let me read everything in all of them"). Purpose grouping (B) is even stronger -- it organizes the territory by function, which maps directly to the agent's workflow. However, annotations create a maintenance burden and may conflict with what the instructions say about each location's purpose. Test: does annotated path display reduce wasted tool invocations (agent goes to the right place on the first try)?
- STABILITY: experimental -- annotations could significantly affect navigation behavior

---

## FIELD: display[].tools
TYPE: array of strings (tool names)
OPTIONAL: (present within each display entry)
VALUES: ["Glob", "Grep", "Read", "find"] (same for all entries in agent-builder) / (no entries)

### What the agent needs to understand

The tools array within each display entry tells the agent WHAT OPERATIONS it can perform at the given path. This creates a per-location capability profile. In principle, different paths could grant different tools (e.g., Read-only for schemas, Read+Write for staging). In practice, the agent-builder data shows uniform tool grants across all entries.

The question of whether the agent needs to know its tool grants AT ALL is genuinely open. The hook system enforces tool restrictions regardless of what the prompt says. If the agent tries to use Glob on a path not in its grants, the hook blocks it. The prompt's display of tool grants is therefore ADVISORY, not AUTHORITATIVE. The agent's awareness of its tool grants may serve a different purpose than enforcement: it may serve planning. An agent that knows it has Glob, Grep, Read, and find can plan multi-step discovery workflows (Glob to find files, Grep to search contents, Read to examine matches). An agent that does not know its tools would discover them by trial and error.

### Fragments

**tool_name_translation**
- Current (defective): raw tool names displayed as-is: "Glob, Grep, Read, find"
- Alternative A: Tool names translated to capabilities: "search, scan, read, list" -- verbs instead of proper nouns
- Alternative B: Tool names translated to categories: "discovery (Glob, find), search (Grep), reading (Read)" -- grouped by purpose
- Alternative C: Tool names as-is, but with brief descriptions the first time they appear: "Glob (file pattern matching), Grep (content search), Read (file reading), find (directory listing)"
- PURPOSE: Controls whether the agent thinks in terms of tool identities ("I'll use Glob") or capabilities ("I need to search for files"). Tool identities are precise but opaque to agents that may not have deep tool knowledge. Capability verbs are intuitive but may lead to imprecise tool selection.
- HYPOTHESIS: Raw tool names work well when the agent model already has strong associations with those tool names (Claude knows what Glob does). Capability translations may help when tool names are non-obvious, but for standard tools like Read and Grep, the translation may be unnecessary or even confusing if the verb does not perfectly match the tool's behavior. Grouped-by-purpose (B) helps the agent plan workflows ("first discover, then search, then read") but imposes a workflow model that may not match the task. Test: does capability-verb translation affect tool selection accuracy?
- STABILITY: formatting -- tool name display is a presentation choice, unlikely to have dramatic behavioral effects given that the tools themselves are well-known

---

## STRUCTURAL: section_heading
TYPE: n/a (not tied to a data field)

### What the agent needs to understand

The section heading signals the START of a boundary context. It tells the agent: "the information that follows is about where you can and cannot operate." The heading choice affects whether the agent perceives this as a permissions section (compliance-oriented) or a navigation section (capability-oriented).

### Fragments

**heading_text**
- Current (defective): `## Security Boundary` -- uses the internal data structure name
- Alternative A: `## Your Workspace` -- possessive, territory framing
- Alternative B: `## Operating Environment` -- neutral, environmental framing
- Alternative C: `## Access and Navigation` -- capability-oriented
- Alternative D: `## Operational Territory` -- territory framing with a sense of scope
- Alternative E: `## Where You Work` -- conversational, second-person, territory framing
- PURPOSE: The heading is the agent's first signal about what this section contains. It primes interpretation of everything that follows.
- HYPOTHESIS: "Security Boundary" immediately activates compliance/restriction processing -- the agent expects to learn what it CANNOT do. "Your Workspace" activates spatial/navigational processing -- the agent expects to learn about its environment. "Operating Environment" is neutral but slightly clinical. "Where You Work" is the most conversational and territory-oriented. Test: does changing the heading from "Security Boundary" to "Your Workspace" change the agent's relationship with its filesystem (fewer cautious pre-checks, more confident navigation)?
- STABILITY: experimental -- the heading is a single string but it primes interpretation of the entire section

---

## STRUCTURAL: section_presence_conditional
TYPE: n/a (conditional branch)

### What the agent needs to understand

This is the most important structural decision in the section: **what happens when there are no display entries?**

The summarizer agent has `workspace_path` but NO display entries. In the current (defective) renderer, this results in the entire security boundary section being OMITTED from the summarizer's prompt. This is a design choice with significant behavioral implications:

**Option 1: Omit the section entirely when display is empty.**
Rationale: if the agent has no filesystem territory, there is nothing to display. The workspace_path still exists in the data for cross-section use (critical_rules needs it), but the agent does not need to see it.
Risk: the agent has no explicit awareness of its workspace root, which may cause path-resolution issues if any other section references relative paths.

**Option 2: Render a minimal section with only workspace_path.**
Rationale: even a processing-only agent needs to know its workspace root. The section would be short: workspace declaration, a statement that all access is mediated through the input/output channels, no path list.
Risk: a nearly-empty section may feel like a stub and the agent may wonder what it is missing.

**Option 3: Render a section that explicitly states "you have no filesystem access."**
Rationale: explicit is better than implicit. Telling the agent it has no filesystem territory is a positive statement that configures its behavior -- it should not attempt to navigate, explore, or discover. Everything arrives through its input channel.
Risk: may cause the agent to refuse legitimate Read operations on its tempfile, which IS a filesystem operation even though it is mediated.

**Option 4: Render a section that describes the agent's access mode as "mediated."**
Rationale: the summarizer does not have zero filesystem access -- it has Read access to /tmp/bragi/cobalt-stage/ (the tempfile staging area). Its access is not zero, it is just not displayed in the security boundary because it is handled by hooks. A "mediated access" framing acknowledges that filesystem operations happen but are not the agent's concern to navigate.

### Fragments

**empty_display_branch**
- Current (defective): section omitted entirely when display array is empty
- Alternative A: Render workspace_path only: `Your workspace is /Users/johnny/.ai/spaces/bragi. Your input and output are delivered through dedicated channels -- no filesystem navigation is required.`
- Alternative B: Render with explicit no-access statement: `Your workspace is /Users/johnny/.ai/spaces/bragi. You do not have direct filesystem access. All data arrives through your input tempfile and leaves through your output tool.`
- Alternative C: Render workspace_path with a brief mediated-access explanation: `Your workspace is /Users/johnny/.ai/spaces/bragi. Your access to the workspace is fully managed -- input arrives through a tempfile and output is written through a dedicated tool. You do not need to navigate the filesystem.`
- Alternative D: Section omitted entirely, but workspace_path referenced in the critical_rules section where the confinement rule lives
- PURPOSE: Configures the agent's operational self-image when it has no filesystem territory. A processing-only agent should understand that its lack of path grants is intentional and appropriate, not an error or oversight.
- HYPOTHESIS: Omission (current/D) may leave the agent uncertain about its filesystem relationship -- it has Read in its tool list but no security section telling it what it can Read. Explicit "no filesystem access" (B) may be too restrictive and could cause the agent to refuse to read its own tempfile. "Mediated access" (C) is the most accurate framing and aligns with the agent's actual architecture. Test: does rendering a minimal security section for processing-only agents reduce path-related errors compared to omitting the section entirely?
- STABILITY: structural -- this is a conditional branch decision with architectural implications

---

## STRUCTURAL: permission_mode_mention
TYPE: n/a

### What the agent needs to understand

The current defective renderer opens the security section with: `This agent operates under bypassPermissions with hook-based restrictions.` This exposes an implementation detail (the permission mode, the hook mechanism) that is meaningless to the agent. The agent does not know what "bypassPermissions" means. It does not know what hooks are. This information is for the dispatch infrastructure, not for the agent's behavioral programming.

### Fragments

**permission_mode_display**
- Current (defective): `This agent operates under bypassPermissions with hook-based restrictions.` -- implementation detail exposed to the agent
- Alternative A: Omit entirely -- the agent does not need to know how its permissions are enforced, only what it can do
- Alternative B: Translate to behavioral language: `Operations outside your designated areas will be silently blocked.` -- tells the agent the CONSEQUENCE without the mechanism
- Alternative C: Translate to environmental language: `The system only supports operations within your designated workspace areas.` -- frames restriction as capability
- PURPOSE: Decides whether the agent should know HOW its security is enforced, or only WHAT it can do within the enforced boundary.
- HYPOTHESIS: Exposing implementation details ("bypassPermissions", "hooks") adds noise and may cause the agent to try to reason about the enforcement mechanism rather than simply operating within its territory. Behavioral translation (B) is more useful -- it tells the agent what will happen if it strays, without explaining how. Environmental translation (C) removes even the notion of enforcement -- there is simply no capability outside the boundary. Test: does removing implementation detail references reduce irrelevant reasoning about the permission system?
- STABILITY: structural -- implementation details should not leak into behavioral programming. This is a correctness issue, not an experiment.

---

## STRUCTURAL: warning_about_violations
TYPE: n/a

### What the agent needs to understand

The current renderer includes: `Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.` This is the only fragment that explicitly warns the agent about out-of-bounds behavior. It does two things: (1) prohibits the behavior ("do not attempt"), and (2) explains the consequence ("fail silently, cannot be approved").

### Fragments

**violation_warning**
- Current (defective): `Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.` -- prohibition + consequence, cage framing
- Alternative A: No explicit warning -- the territory framing should be sufficient. If the agent believes these are its resources and everything it needs is here, it has no reason to look elsewhere.
- Alternative B: `Operations outside these areas are not supported by the environment.` -- environmental framing, no prohibition, just physics
- Alternative C: `If you need something not listed above, report the gap -- do not attempt to access unlisted paths.` -- redirects the impulse rather than forbidding it
- Alternative D: Move the warning to critical_rules rather than having it in the security boundary section -- the confinement rule belongs with other inviolable rules, not with the territory map
- PURPOSE: Prevents the agent from attempting out-of-bounds operations. The question is whether this prevention comes from a warning (reactive) or from the framing (proactive).
- HYPOTHESIS: An explicit "do not attempt" warning may actually INCREASE the probability of out-of-bounds attempts through priming (the agent now has the concept of out-of-bounds operations in its active context). Environmental framing (B) avoids this priming by not raising the concept of violation. Redirect framing (C) gives the agent a constructive alternative to attempting a forbidden operation. Moving the warning to critical_rules (D) consolidates all prohibition-type content in one section, keeping the security boundary section purely descriptive. Test: does removing the explicit warning and relying on territory framing produce MORE or FEWER out-of-bounds attempts?
- STABILITY: experimental -- this is a high-stakes framing choice. Ironic process theory (don't think of a white bear) suggests explicit prohibitions may backfire.

---

## STRUCTURAL: section_position
TYPE: n/a

### What the agent needs to understand

The security boundary section appears after the identity section in the current prompt ordering. This means the agent has already established its self-model (who it is, how it thinks) before learning about its operational territory. This is significant because the spatial model interacts with the identity model -- a "definition author" who knows it has access to definitions, prompts, staging, schemas, and truth data has a much richer self-model than one that knows nothing about its territory.

### Fragments

**position_in_prompt**
- Current (defective): security boundary is the second content section, after identity, before input
- Alternative A: Security boundary immediately after identity -- the agent knows who it is, then where it lives, then what to do. This is the "identity, then territory, then task" sequence.
- Alternative B: Security boundary merged with input -- the agent's access territory and its input description are presented as one unified "what you have to work with" section.
- Alternative C: Security boundary at the end, near critical rules -- the agent learns its task first, then its constraints. This parallels how human workers operate (learn the job, then learn the rules).
- Alternative D: Security boundary embedded within identity -- the agent's territory is part of its identity. "You are a definition author. Your workspace is /Users/johnny/.ai/spaces/bragi. Your territory includes definitions, prompts, schemas, and truth data."
- PURPOSE: Determines when in the prompt sequence the agent builds its spatial model.
- HYPOTHESIS: Early positioning (A, current) means all subsequent sections are interpreted through the lens of "I have access to X, Y, Z." Late positioning (C) means the agent processes instructions and examples without spatial awareness, then learns its territory -- which may cause it to revise its understanding of earlier sections. Merged with input (B) creates a single "resources" block that is coherent but may dilute the spatial model into just being input context. Embedded in identity (D) produces the strongest integration but makes the identity section very long for agents with many path grants. Test: does positioning security boundary before instructions improve first-attempt success on filesystem operations?
- STABILITY: structural -- section ordering is an architectural decision

---

## STRUCTURAL: section_divider_and_transition
TYPE: n/a

### What the agent needs to understand

How the security boundary section ends and transitions to the next section affects whether the spatial model "sticks" or fades as the agent moves into the task-focused sections (input, instructions, etc.).

### Fragments

**section_closer**
- Current (defective): `---` horizontal rule, no transition text
- Alternative A: `---` only -- clean break, the spatial model should persist without reinforcement
- Alternative B: Closing reinforcement: `This is your complete operational territory. Everything you need is within these paths.` -- reinforces completeness before transitioning
- Alternative C: Transition that connects territory to task: `With your workspace established, the following sections describe your input and processing instructions.` -- explicitly bridges from space to task
- Alternative D: No divider -- security boundary flows directly into input, treating them as part of the same "what you have to work with" unit
- PURPOSE: Controls whether the spatial model is sealed (reinforced and closed) or open (flows into the next section).
- HYPOTHESIS: Reinforcement (B) may improve spatial model persistence through the rest of the prompt. A transition (C) helps the agent understand the prompt's structure (first territory, now task). No divider (D) may cause the agent to conflate its path grants with its input description. Test: does a closing reinforcement line reduce path-related errors in later sections?
- STABILITY: formatting (divider type) + experimental (whether to include transition text)

---

## CROSS-SECTION DEPENDENCIES

### security_boundary.workspace_path -> critical_rules (workspace confinement)

This is the most important cross-section dependency. The critical_rules section contains a workspace confinement rule that references the workspace path. The security boundary section establishes the workspace path. This creates two concerns:

1. **Consistency:** The workspace path must be identical in both locations. If security_boundary says `/Users/johnny/.ai/spaces/bragi` and critical_rules references a different path, the agent will be confused.

2. **Reinforcement vs. redundancy:** Does mentioning the workspace path in both security_boundary AND critical_rules reinforce the boundary, or does it create redundancy that teaches the agent "this prompt repeats itself"? The argument for dual mention: the two sections serve different functions -- security_boundary establishes the territory, critical_rules establishes the inviolability of that territory. The argument against: the agent sees the same value twice in different frames and may wonder which one to follow.

3. **Design coordination:** The security_boundary section's framing must be compatible with the critical_rules section's framing. If security_boundary uses territory framing ("your workspace is X") and critical_rules uses prohibition framing ("never operate outside X"), the agent receives mixed signals about its relationship with the boundary. Ideally, both sections would use consistent framing -- either both environmental ("the workspace IS your world" + "operations outside do not exist") or both territory-oriented.

### security_boundary.display -> instructions

The display entries tell the agent where it can go. The instructions tell the agent what to do. The instructions may reference paths or locations that appear in the display entries. For the builder agent, an instruction says "Read the preparation package from the tempfile path. Read all context_required documents." The agent needs to know that context_required documents live in paths covered by its display grants. If the instructions reference locations not in the display, the agent will encounter an apparent contradiction.

### security_boundary.workspace_path -> output

The output section specifies an output directory (e.g., `/Users/johnny/.ai/spaces/bragi/definitions`). This is a path within the workspace. The agent should recognize that its output directory is within its workspace boundary. The workspace_path establishes the root; the output directory is a branch within that root.

### security_boundary -> identity

An agent's territory shapes its identity. A definition author with access to definitions, prompts, schemas, and truth data has a different operational character than a summarizer with no filesystem territory. The security boundary section should not contradict the identity's implications about the agent's operational mode. A "definition author" should have access to definitions. A "summarizer" should not need filesystem navigation.

---

## CONDITIONAL BRANCHES

### Branch 1: display array populated vs. empty

This is the primary conditional branch, discussed in detail under STRUCTURAL: section_presence_conditional. Summary:

- **Populated (builder):** Full section with workspace path, display intro, compound entries, optional warning.
- **Empty (summarizer):** Three sub-options: (a) omit section entirely, (b) render minimal section with workspace path and mediated-access statement, (c) render workspace path only and defer territory language to critical_rules.

### Branch 2: uniform tool grants vs. heterogeneous tool grants

In the builder data, all 7 display entries share the same tool set (Glob, Grep, Read, find). This is the degenerate case -- the tool dimension adds no information per-entry. If a future agent has DIFFERENT tools per path (e.g., Read-only for schemas, Read+Write for staging), the compound entry format must handle this.

- **Uniform tools:** Grouped-by-tools format or prose format is optimal -- state the tools once, list all paths.
- **Heterogeneous tools:** Per-entry format (table, list, or individual statements) is necessary to show different tool sets.

The template system must detect which case applies and select the appropriate format. This is a conditional formatting branch.

### Branch 3: single file path vs. directory path

Display entries can point to specific files (./definitions/agents/agent-template.toml) or to directories (./definitions/audit/). The agent needs to understand the distinction: a file path grants access to that one file, a directory path grants access to all contents of that directory. Whether this distinction needs explicit framing or is obvious from the trailing slash is a design choice.

### Branch 4: number of display entries

The presentation strategy should adapt to the number of entries:
- **0 entries:** Handled by Branch 1 (empty display).
- **1-3 entries:** Prose or simple list is sufficient.
- **4-7 entries:** Structured list or table is more appropriate.
- **8+ entries:** Grouping by purpose, tool set, or path hierarchy becomes necessary to prevent cognitive overload.

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### territory_purpose_mapping

No current or obvious alternative includes a fragment that tells the agent WHY it has access to each location. The display entries say WHERE and WITH WHAT TOOLS, but not WHY. A purpose mapping would connect each path grant to the agent's task:

- `./definitions/agents/agent-template.toml -- your primary reference for field names, types, and constraints`
- `./schemas/ -- validation schemas you will reference when setting output_schema fields`
- `./truth/ -- existing data to examine for domain understanding`

This transforms the security boundary from a permission list into a resource guide. The agent does not just know where it CAN go -- it knows where it SHOULD go and why.

- PURPOSE: Reduces aimless exploration and helps the agent prioritize which locations to access first.
- HYPOTHESIS: Agents with purpose-mapped territory will make fewer wasted tool invocations (reading files that turn out to be irrelevant) and will navigate to the right location on the first attempt more often. Test: do purpose annotations on path grants correlate with reduced tool invocation count?
- STABILITY: experimental -- high potential leverage but adds maintenance burden

### workspace_topology

No current or obvious alternative includes a fragment that describes the SHAPE of the workspace. The display entries are a flat list of paths, but the workspace has a tree structure:

```
bragi/
  definitions/
    agents/agent-template.toml
    audit/
    prompts/
    staging/
  interview/
  schemas/
  truth/
```

A topology fragment would show the agent how its accessible paths relate to each other -- that definitions/agents/ and definitions/prompts/ are siblings, that schemas/ and truth/ are parallel top-level directories, that interview/ is separate from definitions/. This spatial understanding may improve the agent's ability to navigate and cross-reference.

- PURPOSE: Builds a richer spatial model than a flat list of paths.
- HYPOTHESIS: An agent with a tree-view mental model of its workspace will make more efficient navigation decisions (fewer wrong turns) than one with a flat list of unrelated paths. Test: does including a directory tree reduce the number of exploratory Glob operations before the agent finds what it needs?
- STABILITY: formatting -- the tree is a presentation choice for existing data, not new information

### capability_inference_hint

No current or obvious alternative explicitly tells the agent what KIND of work its tool grants imply. The builder has Glob, Grep, Read, and find -- all read-oriented discovery tools. It has NO write tools in its display grants. This fact (the agent is a reader, not a writer, within its display territory) is never stated explicitly. The agent must infer it from the tool list.

A capability inference hint would make this explicit:

- `Your access to these locations is read-only. You can discover, search, and read -- but output is handled through a separate channel.`

Or, for an agent that DID have write grants:

- `You have full read-write access to your staging area. Use it freely.`

- PURPOSE: Makes the agent's capability profile explicit, reducing trial-and-error discovery of what it can and cannot do.
- HYPOTHESIS: Explicit read-only/read-write labeling may reduce failed write attempts and help the agent plan its output strategy from the start. Test: does an explicit "read-only access" statement reduce the number of failed write attempts?
- STABILITY: experimental -- directly affects how the agent plans its tool usage

### temporal_stability_signal

No current or obvious alternative tells the agent whether its security boundary is STABLE for the duration of its run. Can the agent assume that the paths available at the start will remain available throughout? For dispatched autonomous agents (which these are), the answer is yes -- the boundary is fixed at dispatch time and never changes. But the agent does not know this unless told.

A stability signal would be: `Your operational territory is fixed for the duration of this task. No paths will be added or removed while you work.`

- PURPOSE: Reduces uncertainty about resource availability. An agent that knows its territory is stable will not waste cognitive resources wondering whether a previously accessible path might become unavailable.
- HYPOTHESIS: This is likely a low-leverage fragment because LLMs do not typically model temporal changes to their tool access. But for long-running batch agents, the assurance might prevent mid-run panic if a tool invocation takes slightly longer than expected. Test: does a stability signal reduce retry behavior after transient tool delays?
- STABILITY: structural -- the stability of the boundary is a factual property, not a design variable
