# Building a Dispatcher with Galdr

A dispatcher is a **skill** (`.claude/skills/dispatch-{name}/SKILL.md`) that orchestrates agent work. It is NOT a subagent — it runs as instructions for the orchestrating Claude when the user types `/dispatch-{name}`.

Dispatchers are mechanistic. They route input to agents, split batches, and report results. They do not contribute to the quality of the agent's output beyond ensuring the correct materials are handed over. For this reason, dispatchers have minimal composition variation compared to agents.

---

## What a Dispatcher Does

Three things:

1. **Orchestrate** — receive user intent, route to the right agent with the right input
2. **Batch split** — divide work into chunks using `split_jsonl_batches` (batch mode only)
3. **Scope discovery** (no-args only) — read filesystem state, figure out what work exists, present options via AskUserQuestion

Everything else is baked into the agent prompt. The dispatcher provides only: `subagent_type` + input path + dispatch parameters.

**The Task prompt is thin.** The agent already has everything it needs.

---

## The Dispatcher Data Packet

The `anthropic_render.toml` carries a `[dispatcher]` section:

| Field | Purpose |
|-------|---------|
| `agent_name` | `subagent_type` for Task calls |
| `agent_description` | Skill description |
| `dispatch_mode` | `batch` or `full` |
| `batch_size` | `[min, max]` records per chunk (batch mode only) |
| `max_agents` | Concurrency limit |
| `background_mode` | `allowed`, `required`, or `forbidden` |
| `input_format` | `jsonl`, `json`, `text` |
| `input_delivery` | `tempfile`, `inline`, `file`, `directory` |
| `input_description` | What the input data is |
| `output_format` | `jsonl`, `json`, `text`, `markdown` |
| `output_name_known` | `known`, `partially`, `unknown` |
| `return_mode` | `status`, `status-metrics`, `metrics-output`, `output` |
| `parameters` | Array of `{name, type, required, description}` |

---

## Dispatcher Structure

### Frontmatter

```yaml
---
name: dispatch-{agent-name}
description: {agent_description}
argument-hint: "{derived from parameters}"
disable-model-invocation: true
---
```

`disable-model-invocation: true` — dispatchers run only when the user explicitly types the slash command.

### Header

```markdown
# Dispatch: {humanized agent_name}
**Agent:** `{agent-name}`
**Execution:** {BATCH — one agent per batch (~N entries), parallel | FULL — single agent}
```

### Paths

Consolidated listing of all paths the dispatcher references — input, output, schema, context. Absolute paths with human-readable labels.

### With Arguments

When the user provides specific targets (entry IDs, UIDs), the dispatcher validates them, prepares input, and dispatches directly. No state assessment needed.

### No Arguments (Scope Discovery)

The dispatcher reads filesystem state to figure out what work exists, what's done, what's stale. Presents sensible options via AskUserQuestion. The orchestrating Claude handles the actual filesystem inspection — the dispatcher describes what "done" looks like and what input/output paths to check.

**Mandate:** Every step uses actual tool calls. Never cached or remembered state.

### Batch Splitting

For `dispatch_mode = batch`, use `split_jsonl_batches` (compiled tool in `$PATH`):

```bash
split_jsonl_batches --input /tmp/input.jsonl --directory {agent_name} \
  --min-batch {batch_size[0]} --max-batch {batch_size[1]}
```

Returns a JSONL manifest to stdout:
```json
{"batch":1,"file":"/tmp/{agent_name}/batch_001.jsonl","records":50}
```

Optimizes batch count — distributes records evenly within the `[min, max]` range.

### Dispatch

Launch ALL Task calls in a SINGLE message for foreground parallel execution.

**Do NOT use `run_in_background`.** Foreground parallel returns all results in one response.

Tempfiles survive agent failure — failed batches can be redispatched without regenerating input.

### Post-dispatch

Collect results. Report aggregate summary. Offer to redispatch failures.

---

## Composition

Dispatchers are rendered from a single template (`templates/skills/dispatch_v1.md.j2`). Unlike agent prompts, dispatchers have minimal composition variation — the structure is mechanical and consistent across all dispatchers.

The dispatcher template reads from the same `RenderContext` as the agent, accessing `dispatcher`, `identity`, `input`, and `output` contexts.

If dispatcher variants become necessary in the future, they follow the same module system as agents: module directories with variant templates, selected by recipe. For now, a single template with batch/full conditionals is sufficient.

---

## Design Rules

1. **Task prompt is thin.** `subagent_type` + input path + parameters. The agent already knows its job.
2. **Foreground parallel.** All Task calls in a single message. No background dispatch.
3. **Tempfiles survive failure.** Never cleaned up automatically.
4. **State is never cached.** Every filesystem check is a real tool call.
5. **User-invoked only.** `disable-model-invocation: true`.
6. **Dispatchers don't affect output quality.** Their job is logistics — correct materials to correct agents. Quality comes from the agent prompt.

---

## Open Questions

### Paths Data Source

The dispatcher data packet carries dispatch config but not a consolidated path listing with labels. A `dispatcher.paths` array composed upstream from security IO, schema, and context paths would make the Paths section cleaner. Currently unclear whether this is populated in the anthropic render TOML.

### Scope Discovery Content

The "no arguments" flow varies between dispatchers — what constitutes "done", what options to present. Options:
- Prose field in the definition describing what "done" looks like
- Generated skeleton with mechanical structure, Claude figures out domain logic
- Not generated — hand-written per dispatcher
