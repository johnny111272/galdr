# Frontmatter Section Analysis

---

## 1. Nature of the Section

Frontmatter is categorically different from every other section in the agent composition system. Every other section is prose that shapes agent behavior through language. Frontmatter is structured metadata consumed by the Claude Code dispatch infrastructure. The agent never reads it as behavioral content. It is rendered as YAML at the top of the prompt file and parsed by machinery, not by the LLM.

This distinction matters for template design because the design constraints are serialization correctness and infrastructure contract compliance, not clarity of communication to an agent mind.

---

## 2. Field Inventory and Semantics

From the two agents, the complete field set is:

| Field | Builder | Summarizer | Purpose |
|---|---|---|---|
| `name` | "Agent Builder" | "Interview Enrich Create Summary" | Display name for the agent in dispatch UI and logs |
| `description` | Long sentence | Long sentence | System-facing summary of what the agent does |
| `model` | "opus" | "sonnet" | Which LLM backs the agent |
| `permission_mode` | "bypassPermissions" | "bypassPermissions" | Security policy — both use bypass |
| `tools` | ["Bash", "Glob", "Grep", "Read"] | ["Bash", "Read"] | Which Claude Code tools the agent can invoke |
| `hooks.command_entries` | Present (find command) | Absent | Shell command permissions with path restrictions |
| `hooks.tool_entries` | 3 entries (Glob, Grep, Read) | 1 entry (Read) | Per-tool path restrictions |
| `hooks.output_tool` | Absent | "append_interview_summaries_record" | Registers a custom output tool with infrastructure |

### Field-by-field observations

**`name`**: A display string. The builder's name is clean and short. The summarizer's name is a long hyphenated pipeline path rendered as title case. Both are human-readable. This field has no behavioral effect on the agent — it is for logging, dispatch UI, and identification.

**`description`**: A single sentence summarizing the agent's function. This is system-facing — it helps the dispatcher (or a human reading the YAML) understand what the agent does without reading the full prompt. It does NOT appear in the agent-visible body as-is. However, the content overlaps heavily with what appears in the identity and role sections. This is the first duplication concern.

**`model`**: "opus" for the creative builder, "sonnet" for the batch summarizer. This is a pure infrastructure directive — it tells the dispatch system which model to instantiate. The agent cannot perceive which model it is running on. There is no reason for this to appear in agent-visible content.

**`permission_mode`**: Both use "bypassPermissions". This is an infrastructure-level security setting. The value space appears to be at least {"bypassPermissions", ...} but with only two agents both using the same value, the full enum cannot be determined from sample data alone. This field is invisible to the agent and should remain so — agents should not know their own permission mode.

**`tools`**: The list of Claude Code tools the agent is granted. The builder gets four tools (Bash, Glob, Grep, Read); the summarizer gets two (Bash, Read). This is enforced by infrastructure — tools not in this list are unavailable regardless of what the agent's behavioral prose says. This is the second duplication concern: the security_boundary section in the agent-visible body also describes tool grants. The frontmatter list is the actual enforcement; the body prose is behavioral guidance that should mirror it but is not the source of truth.

**`hooks`**: The permission enforcement mechanism. This is the most structurally complex part of frontmatter and the most important to get right because it is the actual security implementation. See Section 4.

---

## 3. Duplication Between Frontmatter and Agent-Visible Sections

Three frontmatter fields have semantic duplicates in other sections.

### 3.1 `description` vs. identity/role/dispatcher content

The frontmatter `description` says what the agent does in one sentence. The identity section contains a role description and expertise statement that say similar things in agent-visible prose. The dispatcher (skill file) also contains a description.

**The question**: Should the frontmatter description be derived from identity content, or independent?

**Analysis**: These serve different audiences. The frontmatter description is for the dispatch system and human operators reading YAML. The identity role description is for the agent to understand itself. The dispatcher description is for the parent agent deciding whether to invoke this agent. They SHOULD say similar things but are NOT the same field. The frontmatter description should be terse and machine-friendly. The identity description should be natural and agent-friendly. Attempting to unify them into a single source would compromise one audience or the other.

**Template implication**: The template should generate the frontmatter description independently from identity content. It may reference the same source material, but the rendering is different.

### 3.2 `model` vs. identity model reference

Some agent identity sections reference the model ("You are an Opus-class agent" or similar). The frontmatter `model` is the actual infrastructure directive.

**Analysis**: The identity section's model reference, if any, is behavioral suggestion ("you have the capacity for deep reasoning"). The frontmatter model is the actual selection. These are different concerns. The template should not attempt to derive one from the other. However, they must be consistent — if the frontmatter says "sonnet", the identity section should not imply opus-class capabilities.

**Template implication**: The model field in frontmatter should be a simple parameter. If identity content references model capabilities, the template should ensure consistency but not couple them.

### 3.3 `tools` vs. security_boundary tool grants

The frontmatter `tools` array is the enforcement. The security_boundary section's tool grant prose is behavioral guidance. Both describe which tools the agent can use.

**Analysis**: This is the most dangerous duplication. If frontmatter grants ["Bash", "Read"] but the security_boundary prose says "You have access to Bash, Read, and Glob", the agent will attempt to use Glob and fail. Worse, if frontmatter grants a tool but security_boundary does not mention it, the agent has access but does not know it.

**Template implication**: The security_boundary tool grant prose MUST be derived from the frontmatter tools list. This is not optional. The frontmatter is the source of truth; the body prose reflects it. The template should have a single tool list that feeds both the frontmatter tools array and the security_boundary generation.

---

## 4. Hooks: The Permission Enforcement Mechanism

Hooks are the most structurally complex part of frontmatter and the most important to get right because they are the actual security implementation.

### 4.1 Structure observed

**`hooks.tool_entries`**: An array of objects, each with:
- `tool`: The tool name (matches an entry in the `tools` array)
- `paths`: An array of absolute paths (files or directories) the tool is allowed to access

**`hooks.command_entries`**: An array of objects, each with:
- `command`: The command name (e.g., "find")
- `paths`: An array of absolute paths the command is allowed to access

**`hooks.output_tool`**: A string naming a custom output tool binary.

### 4.2 Observations on hook structure

**Path repetition is extreme.** The builder has the same 7-path array repeated across three tool_entries (Glob, Grep, Read) and the command_entries. The summarizer has a single path for its single tool_entry. This suggests that most agents will have a common set of allowed paths, and the per-tool breakdown is often identical.

**Not every tool in `tools` gets a hook entry.** The builder has `tools = ["Bash", "Glob", "Grep", "Read"]` but no tool_entry for Bash. The summarizer has `tools = ["Bash", "Read"]` but only a tool_entry for Read. This implies Bash is either unrestricted or restricted through command_entries only.

**command_entries vs. tool_entries**: Tool entries restrict Claude Code tools (Glob, Grep, Read). Command entries restrict shell commands invoked through Bash. These are different permission layers. The builder has both; the summarizer has neither command_entries nor Bash tool_entries.

**output_tool is a simple string, not a structured entry.** It names a binary that the infrastructure makes available as a tool. The summarizer has one; the builder does not. This is the mechanism for custom write tools.

### 4.3 Template design implications for hooks

The hook structure presents a genuine design challenge:

**Option A: Per-tool path specification.** Each tool gets its own explicit path list. This is what the raw data shows. It is maximally explicit but creates massive repetition when paths are identical across tools.

**Option B: Shared path pool with per-tool overrides.** Define a common path set, then allow individual tools to extend or restrict. This reduces repetition but adds structural complexity.

**Option C: Path tiers (read paths, write paths, search paths).** Group paths by access pattern rather than by tool. This is semantically cleaner but may not match the infrastructure's actual enforcement model.

**Recommendation**: The template should use Option A (per-tool explicit paths) because that is what the infrastructure parses. However, the TOML definition format (the input to the pipeline) could use a shared path pool that the serializer expands into per-tool entries. The template is about the OUTPUT format, and that format must match what the infrastructure expects.

### 4.4 The Bash gap

Both agents grant Bash but neither has a tool_entry for Bash. The builder has command_entries restricting `find`. This suggests:

- Bash itself is unrestricted (any command can run)
- command_entries restrict SPECIFIC commands within Bash
- Or Bash restrictions work through a different mechanism

The template must handle this: if Bash is in the tools list, it does not necessarily need a tool_entry. Command_entries are the Bash-specific restriction mechanism.

---

## 5. Serialization Concerns

Since frontmatter is machine-parsed YAML, the template must produce syntactically correct output. This is different from all other sections where the template produces prose that merely needs to be clear.

### 5.1 Field ordering

YAML does not require field ordering, but consistent ordering aids human readability and diff stability. The observed order in both agents is:

1. `description`
2. `model`
3. `name`
4. `permission_mode`
5. `tools`
6. `hooks` (with sub-fields)

This appears to be alphabetical. A template should enforce consistent ordering. A more semantic ordering would be:

1. `name` (identity first)
2. `description` (what it does)
3. `model` (which LLM)
4. `permission_mode` (security posture)
5. `tools` (granted capabilities)
6. `hooks` (detailed permissions)

This groups identity (name, description), infrastructure (model, permission_mode), and permissions (tools, hooks) in logical clusters. However, if the infrastructure expects or produces alphabetical ordering, the template should match that to minimize diff noise.

### 5.2 YAML vs. TOML representation

The raw data is in TOML (the definition format). The output is YAML (the rendered prompt frontmatter). The template must handle this conversion correctly:

- TOML arrays of tables (`[[frontmatter.hooks.tool_entries]]`) become YAML sequences of mappings
- TOML inline arrays (`tools = ["Bash", "Read"]`) become YAML flow or block sequences
- TOML strings become YAML strings (quoting rules differ)

The template must produce valid YAML. This is a hard constraint. Malformed YAML will cause the infrastructure to reject the agent.

### 5.3 Comments in YAML frontmatter

YAML supports comments. Should the rendered frontmatter include any?

- **For**: Comments explaining permission rationale help human auditors
- **Against**: Machine-parsed metadata should be clean; rationale belongs in the definition TOML, not the output YAML

**Recommendation**: No comments in rendered YAML. The definition TOML and the audit trail are where rationale lives. The YAML is a build artifact.

---

## 6. Template Design

Given that frontmatter is serialization rather than prose composition, the template's job is different from other sections. It must:

### 6.1 Accept parameters

The template needs these inputs:
- `name`: string
- `description`: string
- `model`: enum (at minimum: "opus", "sonnet")
- `permission_mode`: enum (at minimum: "bypassPermissions")
- `tools`: list of strings
- `hooks.tool_entries`: list of {tool, paths} objects
- `hooks.command_entries`: list of {command, paths} objects (optional)
- `hooks.output_tool`: string (optional)

### 6.2 Validate inputs

Unlike prose sections where flexibility is acceptable, frontmatter has hard constraints:
- Every tool in tool_entries must appear in the tools list
- Every command in command_entries must be a valid shell command
- All paths must be absolute
- output_tool, if present, must name an existing binary

### 6.3 Serialize correctly

The template must produce YAML that the infrastructure parses without error. This means:
- Correct indentation (YAML is whitespace-sensitive)
- Correct quoting (strings with special characters)
- Correct sequence/mapping syntax
- Correct frontmatter delimiters (typically `---` fences)

### 6.4 Ensure consistency with body sections

The template must feed its data into downstream sections:
- `tools` list feeds into security_boundary tool grant prose
- `description` may inform identity section content
- `model` may inform identity capability references
- `hooks` paths may inform security_boundary path prose

This is the template's most important coordination responsibility.

---

## 7. What the Template Should NOT Do

1. **Should NOT embed behavioral content.** Frontmatter is not read by the agent. Putting behavioral instructions here wastes tokens and has no effect.

2. **Should NOT duplicate enforcement.** The hooks ARE the enforcement. The agent-visible security_boundary is behavioral guidance. The template should not try to make frontmatter do double duty.

3. **Should NOT be flexible about structure.** Unlike prose sections where the template can offer alternatives, the YAML structure must match what the infrastructure expects. There is one correct format.

4. **Should NOT include optional fields with empty values.** If there are no command_entries, omit the field entirely rather than rendering an empty array. Clean YAML means only present fields have values.

---

## 8. Open Questions

### 8.1 Is permission_mode always "bypassPermissions"?

Both agents use the same value. If this is always the case, should it be a template default rather than a parameter? Or are there other modes that exist but are not represented in the sample data?

### 8.2 What other tools exist?

The samples show Bash, Glob, Grep, Read. Are Write, Edit, and other Claude Code tools ever granted? The builder notably lacks Write despite creating files. Does it use Bash for writes? Or is Write implicitly available?

### 8.3 How does output_tool registration work?

The summarizer registers "append_interview_summaries_record". Where does the infrastructure look for this binary? Is there a naming convention? Does the binary need to be on PATH or in a specific directory? The template needs to know this to validate the output_tool field.

### 8.4 Are there agents with different path sets per tool?

Both samples have identical paths across all tool_entries. Is this always the case, or do some agents have tool-specific path restrictions (e.g., Read can access more paths than Grep)?

### 8.5 Frontmatter fence format

Standard YAML frontmatter uses `---` delimiters. Does this infrastructure use the same convention, or a different one?

---

## 9. Relationship to Control Surface Design

Frontmatter is a control surface, but not a behavioral one. It is the infrastructure control surface — the interface between the agent definition system and the Claude Code dispatch machinery.

The template for frontmatter should be treated as a serializer with validation, not as a prose composer. Its inputs are structured data. Its output is structured data. The only "design" question is whether the input format (TOML definition) should mirror the output format (YAML frontmatter) exactly, or whether the input can use higher-level abstractions (shared path pools, tool group presets) that the serializer expands.

**Recommendation**: The definition TOML should allow higher-level abstractions. The serializer should expand them to the flat, explicit YAML the infrastructure requires. This keeps definitions DRY while keeping rendered output correct.

---

## 10. Summary

Frontmatter is the only section in the agent composition system that is NOT agent-consumed prose. It is infrastructure metadata serialized as YAML. The template design challenge is serialization correctness, input validation, and consistency with agent-visible sections that reference the same data (particularly tools and paths).

The critical design principle: **Frontmatter is the source of truth for infrastructure concerns (tools, permissions, paths, model). Agent-visible body sections that reference these concerns must be DERIVED from frontmatter data, never the reverse.** This prevents the most dangerous class of bugs: mismatches between what the agent believes it can do and what the infrastructure actually allows.
