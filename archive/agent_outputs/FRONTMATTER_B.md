# FRONTMATTER SECTION ANALYSIS

This section is fundamentally unlike every other section in the agent composition system. It is machine-consumed YAML metadata parsed by Claude Code infrastructure, not behavioral prose read by the agent. The analysis must respect this distinction while still identifying template-relevant structure.

---

## 1. NATURE OF THE SECTION

Frontmatter is not agent instruction. It is infrastructure configuration. The fields control:
- Which model runs the agent (model)
- What the agent is called in the dispatch system (name)
- What tools the agent can access (tools)
- What filesystem paths those tools are restricted to (hooks.tool_entries, hooks.command_entries)
- Whether an output tool is registered (hooks.output_tool)
- How permissions are handled (permission_mode)

The agent never sees this content during execution. It is consumed by the Claude Code dispatch layer before the agent prompt body is assembled. This means template design for frontmatter is about **correct serialization**, not about prose quality, voice, or behavioral shaping.

---

## 2. FIELD INVENTORY AND STRUCTURE

### Top-level scalar fields (always present in both agents):

| Field | Agent 1 (builder) | Agent 2 (summarizer) |
|---|---|---|
| name | "Agent Builder" | "Interview Enrich Create Summary" |
| description | "Creates new agent TOML definitions..." | "Reads stripped interview exchanges sequentially..." |
| model | "opus" | "sonnet" |
| permission_mode | "bypassPermissions" | "bypassPermissions" |
| tools | ["Bash", "Glob", "Grep", "Read"] | ["Bash", "Read"] |

**Observations:**
- All five scalar fields appear in both agents. These are likely mandatory.
- `permission_mode` is identical in both. Possibly always "bypassPermissions" for subagents (they inherit the parent session's permission grants via hooks rather than prompting the user). This may be invariant rather than configurable.
- `tools` is a list that varies. Builder needs search tools (Glob, Grep); summarizer only needs Read. The tools list directly constrains what the agent can do at the infrastructure level.
- `model` varies: opus for complex construction work, sonnet for simpler summarization. This is a genuine per-agent decision.

### Hooks subsection:

This is where complexity diverges dramatically.

**Agent 1 (builder) hooks:**
```
hooks.command_entries: 1 entry (find, 7 paths)
hooks.tool_entries: 3 entries (Glob/7 paths, Grep/7 paths, Read/8 paths)
```

**Agent 2 (summarizer) hooks:**
```
hooks.output_tool: "append_interview_summaries_record"
hooks.tool_entries: 1 entry (Read, 1 path)
```

**Critical structural observations:**
- `command_entries` is present in builder, absent in summarizer. This is conditional on whether Bash commands need path restrictions.
- `output_tool` is present in summarizer, absent in builder. This is conditional on whether the agent uses a registered output tool.
- `tool_entries` is present in both but varies in count and complexity.
- Each tool_entry pairs a tool name with an array of allowed paths. This is the actual filesystem security enforcement.

---

## 3. FIELD DUPLICATION ACROSS SECTIONS

This is a critical design issue for the template system.

### `description`
- Appears in frontmatter (machine metadata)
- Appears in identity section (agent-visible behavioral context)
- Appears in dispatcher SKILL.md (dispatch-layer description)

These are three different consumers with three different purposes:
- Frontmatter description: used by Claude Code infrastructure for agent listing/selection
- Identity description: tells the agent what it does (behavioral self-understanding)
- Dispatcher description: tells the dispatch layer what to route to this agent

**Question:** Should these be identical strings or purpose-tailored variants? The raw data shows them as identical or near-identical across sections, suggesting they are currently copy-pasted. But the consumers are different. A frontmatter description optimized for machine listing ("Creates new agent TOML definitions from template and raw definition input") serves a different purpose than an identity description that shapes the agent's self-concept.

**Template implication:** The template must either (a) use a single canonical description and emit it to all three locations, or (b) allow per-location variants. Given that the current system uses identical strings, option (a) is simpler and matches observed practice. Option (b) is more correct but adds complexity with no demonstrated need.

**Recommendation:** Single canonical description, emitted to all locations. If a future agent needs divergent descriptions, that can be handled as an override, not a default pathway.

### `model`
- Appears in frontmatter (controls which model actually runs)
- Appears in identity section (tells the agent what model it is)

These serve genuinely different purposes. Frontmatter model is infrastructure configuration. Identity model is behavioral context (the agent may adjust its behavior knowing it is opus vs sonnet). But the value must be identical — an agent told it is opus but actually running as sonnet would be incoherent.

**Template implication:** Single source value, emitted to both locations. No divergence possible.

### `name`
- Appears in frontmatter (infrastructure agent identifier)
- Appears in identity section (agent self-identification)

Same pattern as model. Must be identical. Single source.

---

## 4. HOOK STRUCTURE ANALYSIS

Hooks are the most structurally complex part of frontmatter and the part most likely to cause template serialization errors.

### tool_entries pattern:

Each entry is a TOML array-of-tables:
```toml
[[frontmatter.hooks.tool_entries]]
tool = "ToolName"
paths = ["path1", "path2", ...]
```

**Invariant:** Every tool listed in the top-level `tools` array (except Bash) should have a corresponding tool_entry with path restrictions. Bash is handled differently — through command_entries.

**Verification opportunity:** A template system could enforce that `tools` and `tool_entries` are consistent: every non-Bash tool in `tools` must have a `tool_entries` entry, and every `tool_entries` tool must appear in `tools`. This is a structural integrity check the template can perform.

### command_entries pattern:

```toml
[[frontmatter.hooks.command_entries]]
command = "find"
paths = ["path1", "path2", ...]
```

**Conditional:** Only present when Bash commands need filesystem path restrictions. The builder needs `find` restricted to workspace paths. The summarizer apparently does not use filesystem-exploring Bash commands (or its Bash usage is unrestricted — which would be worth verifying in a broader audit).

**Template implication:** command_entries is an optional section. The template must handle its absence cleanly.

### output_tool pattern:

```toml
[frontmatter.hooks]
output_tool = "append_interview_summaries_record"
```

**Conditional:** Only present when the agent uses a registered output tool (a script in `tools/bin/` that the agent calls to write validated output). This is the summarizer's pattern — it produces structured records via a specific tool rather than writing files directly.

**Template implication:** output_tool is an optional scalar field within hooks. Present/absent is a binary conditional.

---

## 5. PATH STRUCTURE PATTERNS

Examining the paths arrays reveals structure:

**Builder paths (7 workspace paths):**
These are workspace-internal paths — definitions directories, prompt directories, schema directories. The builder needs broad read access across the definition infrastructure.

**Summarizer paths (1 path):**
Just `/tmp/bragi/cobalt-stage/` — a staging directory. The summarizer reads from staging, processes, and writes via output_tool. Extremely constrained.

**Template implication:** Paths are the most variable part of frontmatter. They cannot be templated as fixed values — they must be per-agent configuration. The template's job is to serialize whatever paths the definition provides, not to decide what paths are correct.

---

## 6. TEMPLATE DESIGN RECOMMENDATIONS

### Field ordering (YAML output):

```yaml
# Frontmatter — infrastructure metadata
name: <string>
description: <string>
model: <opus|sonnet>
permission_mode: bypassPermissions
tools: [<tool list>]
hooks:
  output_tool: <string>           # CONDITIONAL: only if present
  command_entries:                 # CONDITIONAL: only if present
    - command: <string>
      paths: [<path list>]
  tool_entries:                    # CONDITIONAL: only if tools beyond Bash
    - tool: <string>
      paths: [<path list>]
```

### Conditional branches the template must handle:

1. **output_tool present vs absent** — Binary. If the agent definition includes an output_tool, emit it. If not, omit entirely.
2. **command_entries present vs absent** — Binary. If the agent definition includes command_entries, emit the array. If not, omit entirely.
3. **tool_entries count varies** — The template must iterate over however many tool_entries the definition provides (0 to N).
4. **paths count varies per entry** — Each tool_entry or command_entry has a variable-length paths array.

### What the template does NOT decide:

- Which model to use (comes from agent definition)
- Which tools to grant (comes from agent definition)
- Which paths to allow (comes from agent definition)
- Whether to include output_tool (comes from agent definition)

The template is a serializer, not a decision-maker. For frontmatter specifically, this is even more true than for behavioral sections — there is no prose to shape, no voice to calibrate, no structure to design. There is only correct YAML emission.

### Structural integrity checks the template CAN enforce:

1. All five scalar fields (name, description, model, permission_mode, tools) must be present.
2. Every non-Bash tool in `tools` should have a corresponding `tool_entries` entry.
3. If `command_entries` is present, "Bash" should be in `tools`.
4. `permission_mode` should be "bypassPermissions" (flag if different — may indicate error).
5. `model` should be one of the known values (opus, sonnet — flag unknowns).

---

## 7. RELATIONSHIP TO AGENT-VISIBLE BODY

The frontmatter is not visible to the agent. But some of its content has echoes in the agent body:

- **description** echoes in identity and dispatcher
- **model** echoes in identity
- **name** echoes in identity
- **tools** has NO echo — the agent is not told what tools it has (it discovers them at runtime)
- **hooks** has NO echo in the body — but the security_boundary section provides behavioral guidance that should be *consistent* with hooks enforcement

**Critical consistency requirement:** The hooks enforce filesystem paths at the infrastructure level. The security_boundary section (in the agent body) provides behavioral guidance about where to read/write. These must be consistent. If hooks allow paths A, B, C, the security_boundary should reference the same paths (or a subset). If security_boundary references paths not in hooks, the agent will be told to do something infrastructure will block.

**Template implication:** The template system should either (a) derive security_boundary paths from hooks paths, or (b) validate consistency between them. This is a cross-section concern, not a frontmatter-internal concern, but frontmatter is the authoritative source for path restrictions.

---

## 8. SUMMARY

Frontmatter is infrastructure metadata, not behavioral content. Its template requirements are:

1. **Correct YAML serialization** of scalar fields, arrays, and nested structures
2. **Conditional emission** of output_tool, command_entries (present/absent)
3. **Variable-length iteration** over tool_entries and their paths
4. **Single-source emission** of name, description, model to frontmatter and their echo locations (identity, dispatcher)
5. **Structural integrity validation** (tools/tool_entries consistency, required fields present)
6. **Cross-section consistency** between hooks paths and security_boundary paths

The template for this section is fundamentally a serializer with validation, not a prose generator. Design accordingly.
