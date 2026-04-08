# FRONTMATTER — Control Surface Synthesis

## Section Purpose

Frontmatter is the only section in the agent composition system that is NOT agent-consumed prose. It is infrastructure metadata serialized as YAML, parsed by the Claude Code dispatch layer before the agent prompt body is assembled. The agent never sees it during execution.

This means template design for frontmatter is about correct serialization and structural integrity, not prose quality, voice, or behavioral shaping. The template is a serializer with validation, not a prose composer. Its inputs and outputs are both structured data.

The critical design principle: frontmatter is the source of truth for infrastructure concerns (tools, permissions, paths, model). Agent-visible body sections that reference these concerns must be DERIVED from frontmatter data, never the reverse. This prevents mismatches between what the agent believes it can do and what the infrastructure actually allows.

## Fragment Catalog

### name
- CONVERGED: Display string for dispatch UI and logs. Must be identical wherever it appears (frontmatter, identity section). Single source value emitted to all locations.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Simple string passthrough from definition — no transformation needed
- HYPOTHESIS: No behavioral leverage. Pure identification.
- STABILITY: structural
- CONDITIONAL: none — always present

### description
- CONVERGED: System-facing summary. Appears in frontmatter, identity section, and dispatcher SKILL.md — three different consumers.
- DIVERGED: Whether to use a single canonical string everywhere or purpose-tailored variants per location.
  - A argued for independent generation per audience (frontmatter=terse/machine-friendly, identity=natural/agent-friendly). Explicitly advised against unifying.
  - B argued for single canonical string emitted everywhere, with per-location overrides available but not default.
- ALTERNATIVES:
  - A: Single canonical description, emitted to all three locations — matches observed practice, simplest (B's recommendation)
  - B: Independent rendering per audience — more correct but adds complexity with no demonstrated need (A's recommendation)
- HYPOTHESIS: Current agents use near-identical strings across locations. The divergence is theoretical until an agent demonstrably needs different descriptions for different consumers.
- STABILITY: structural
- CONDITIONAL: none — always present

### model
- CONVERGED: Infrastructure directive controlling which LLM runs. Must be consistent with any identity section references to model capabilities. Single source value.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Simple enum passthrough (opus, sonnet) — flag unknown values
- HYPOTHESIS: If identity references model capabilities ("you have capacity for deep reasoning"), the template must ensure consistency with frontmatter model value. An agent told it is opus but running as sonnet would be incoherent.
- STABILITY: structural
- CONDITIONAL: none — always present

### permission_mode
- CONVERGED: Both agents use "bypassPermissions". Invisible to agent. May be invariant for all subagents (they inherit parent session's permission grants via hooks).
- DIVERGED: Whether this should be a template default or a parameter.
- ALTERNATIVES:
  - A: Default to "bypassPermissions", flag any other value as potentially erroneous
  - B: Require explicit specification every time — no assumption
- HYPOTHESIS: Likely always "bypassPermissions" for dispatched subagents. Template should default it but allow override.
- STABILITY: structural
- CONDITIONAL: none — always present

### tools
- CONVERGED: List of Claude Code tools the agent can invoke. This is ENFORCEMENT — tools not listed are unavailable regardless of what body prose says. The most dangerous duplication point: security_boundary prose MUST be derived from this list.
- DIVERGED: None on the field itself; strong convergence that this is the authoritative source for tool grants.
- ALTERNATIVES:
  - A: Flat list passthrough from definition, feeds both YAML tools array and security_boundary generation
- HYPOTHESIS: Single tool list feeding both frontmatter and body prose is mandatory, not optional. Mismatch here causes agents to attempt unavailable tools or remain unaware of available ones.
- STABILITY: structural
- CONDITIONAL: none — always present, but contents vary

### hooks.tool_entries
- CONVERGED: Array of {tool, paths} objects. Each pairs a tool name with allowed filesystem paths. Most structurally complex part of frontmatter. Path repetition across entries is extreme (builder has same 7 paths repeated across three tools).
- DIVERGED: Whether the TOML input format should allow path pooling or require per-tool explicit paths.
  - Both agreed the YAML output must be per-tool explicit (infrastructure requirement).
  - A explicitly recommended the input TOML could use a shared path pool that the serializer expands.
  - B focused on the template as pure serializer of whatever the definition provides.
- ALTERNATIVES:
  - A: Per-tool explicit paths in both input and output — matches infrastructure, maximally explicit, repetitive
  - B: Shared path pool in TOML input, expanded to per-tool entries during serialization — DRY input, correct output
- HYPOTHESIS: Path pooling in the input format is a definition-layer concern, not a template-layer concern. The template serializes what it receives. Whether the input uses pooling is an upstream design decision.
- STABILITY: structural
- CONDITIONAL: present when tools beyond Bash are granted

### hooks.command_entries
- CONVERGED: Array of {command, paths} objects restricting specific shell commands within Bash. Conditional — only present when Bash commands need path restrictions.
- DIVERGED: None.
- ALTERNATIVES:
  - A: Optional section, omit entirely when absent — no empty arrays
- HYPOTHESIS: command_entries is the Bash-specific restriction mechanism. Bash itself gets no tool_entry; restrictions on Bash operate through command_entries.
- STABILITY: structural
- CONDITIONAL: present only when Bash commands need filesystem path restrictions. If present, "Bash" must be in tools list.

### hooks.output_tool
- CONVERGED: Simple string naming a custom output tool binary. Conditional — only present when the agent uses a registered output tool. The summarizer has one; the builder does not.
- DIVERGED: None on structure. Both flagged that the registration mechanism (where infrastructure looks for the binary, naming conventions) is unknown.
- ALTERNATIVES:
  - A: Optional scalar, emit when present, omit when absent
- HYPOTHESIS: This is the mechanism for custom validated-write tools. Agents that produce structured records use output_tool; agents that write files directly do not.
- STABILITY: structural
- CONDITIONAL: present only when agent uses a registered output tool (binary)

### YAML field ordering
- CONVERGED: Consistent ordering aids readability and diff stability.
- DIVERGED: Which ordering to use.
  - A noted observed ordering is alphabetical, proposed semantic grouping: identity (name, description) / infrastructure (model, permission_mode) / permissions (tools, hooks). Recommended matching infrastructure convention to minimize diff noise.
  - B proposed: name, description, model, permission_mode, tools, hooks (top-down from identity to detail).
- ALTERNATIVES:
  - A: Semantic grouping (name, description, model, permission_mode, tools, hooks) — logical clusters, matches B's proposal
  - B: Alphabetical (description, model, name, permission_mode, tools) — matches observed infrastructure output
- HYPOTHESIS: If infrastructure produces alphabetical, match it. Otherwise semantic grouping is more readable. Requires checking infrastructure convention.
- STABILITY: formatting
- CONDITIONAL: none

### YAML comments
- CONVERGED: No comments in rendered YAML. The definition TOML and audit trail are where rationale lives. The YAML is a build artifact.
- DIVERGED: None.
- ALTERNATIVES:
  - A: No comments — clean machine-parsed output
- HYPOTHESIS: No behavioral leverage. Clean artifacts reduce parsing risk.
- STABILITY: formatting
- CONDITIONAL: none

## Cross-Section Dependencies

**Frontmatter -> security_boundary**: tools list and hooks paths are the source of truth. security_boundary prose must be derived from or validated against frontmatter. This is the highest-risk consistency requirement in the entire system.

**Frontmatter -> identity**: name, description, and model echo into identity. Must use single source values.

**Frontmatter -> dispatcher (SKILL.md)**: description echoes into the dispatch-layer skill file. Same single-source requirement.

**Frontmatter -> all body sections**: Frontmatter is upstream of everything. No body section should introduce infrastructure claims (tool access, path access, model identity) that contradict frontmatter.

## Conditional Branches

| Condition | Effect |
|---|---|
| Agent has tools beyond Bash | tool_entries section present with per-tool path arrays |
| Agent uses restricted Bash commands | command_entries section present |
| Agent uses registered output tool | hooks.output_tool scalar present |
| Agent has no hooks at all | hooks section omitted entirely (untested — may not occur) |

All conditionals are binary (present/absent). No conditional affects scalar field presence — all five top-level scalars are always present.

## Open Design Questions

1. **Is permission_mode always "bypassPermissions"?** Both agents use it. If invariant, should it be a hard default or still require explicit specification? Broader audit needed.

2. **What is the full tools enum?** Samples show Bash, Glob, Grep, Read. Are Write, Edit, and other Claude Code tools ever granted? The builder creates files but lacks Write — does it use Bash for writes?

3. **How does output_tool registration work?** Where does infrastructure look for the binary? Naming convention? PATH or specific directory? Template needs this to validate.

4. **Do any agents have divergent per-tool path sets?** Both samples repeat identical paths across tool_entries. If some agents need tool-specific restrictions, the shared-path-pool input design must support overrides.

5. **Frontmatter fence format**: Standard YAML frontmatter uses `---` delimiters. Does this infrastructure use the same convention?

6. **Should the input TOML allow path pooling?** Both analyses agree the output must be per-tool explicit. Whether the input allows shorthand is an upstream design decision that affects definition ergonomics.

## Key Design Decisions

1. **Frontmatter is source of truth for infrastructure concerns.** Body sections derive from it, not the reverse. Both analyses converged on this with high confidence.

2. **The template is a serializer, not a decision-maker.** It accepts structured data, validates structural integrity, and emits correct YAML. No prose composition, no behavioral shaping.

3. **Omit absent optional fields entirely.** No empty arrays, no null values. Clean YAML means only present fields have values.

4. **Structural integrity checks the serializer CAN enforce:**
   - All five scalar fields present
   - Every non-Bash tool in `tools` has a corresponding `tool_entries` entry
   - If `command_entries` present, "Bash" must be in `tools`
   - `permission_mode` flagged if not "bypassPermissions"
   - `model` flagged if not a known value
   - All paths are absolute

5. **Single-source emission for echoed fields.** name, description, model each have one canonical value that feeds frontmatter and any body section that references them. No independent generation per location (simpler path chosen; override mechanism available if future need arises).
