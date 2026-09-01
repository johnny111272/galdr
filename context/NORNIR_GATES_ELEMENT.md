# Nornir Gates — The Validation Wall

[[AGENT_BUILD_SYSTEM|↑ the map]] · [[VERDANDI_ELEMENT|Verdandi]] → [[DRAUPNIR_ELEMENT|Draupnir]] → **Nornir gates** → [[REGIN_ELEMENT|Regin]] → [[GALDR_ELEMENT|Galdr]]

## Scope

Nornir is a large Rust monorepo — a hundred-plus crates, most of them unrelated to this
pipeline. **This system uses its gate builder**: the compiled schema validators that
every stage boundary passes through. Everything else in Nornir is out of scope here.

---

## What a gate is, concretely

A gate is a compiled Rust module exposed to Python through PyO3, deployed as a `.so`
file under `~/.ai/tools/lib/` and imported like any ordinary module. It carries a JSON
Schema baked in at build time.

Calling one is the whole interface:

```python
import gate_anthropic_render_input

result = gate_anthropic_render_input.validate(str(path))
#  → {"ok": bool, "data": str | None, "error": {"type": str, "message": str} | None}

if not result["ok"]:
    raise ValueError(...)                                   # see "hard failure" below
model = AgentAnthropicRender.model_validate_json(result["data"])
```

No subprocess. No parser import. `result["data"]` is a validated JSON string on its way
into a model — **not** raw material for `json.loads`.

### Four patterns

| Pattern | Call | Returns in `data` |
|---|---|---|
| **Input** | `validate(file_path)` | validated JSON, to feed `model_validate_json` |
| **Output** | `validate(json_data, file_path)` | nothing you consume — the write is the effect |
| **Passthrough** | `validate(input_path, output_path)` | nothing — reads, validates, writes |
| **Defaults** | `validate(input_path, output_path)` | reads, **applies conditional defaults**, validates, writes |

The `model_validate_json` step applies to **input gates only**. For the rest, checking `ok`
is the whole contract.

Passthrough exists for stages that transform nothing — validate the file and move it along.

The defaults pattern has one instance, `gate_raw_definition_defaults`, and it is worth
understanding because it is a *transform* living inside a gate. Defaults are declared in
Verdandi, compiled into the schema by Draupnir, embedded by the build, and applied here —
before validation, so a definition that omits a defaultable field still passes. No Python
touches any of it. This is what Regin's docstring means by *"Delta: NONE. The gate IS the
branch."*

### Two jobs, not one

The gate inventory splits cleanly, and the distinction is not cosmetic:

> **Stage boundaries** — the `*_input` / `*_output` pairs that bracket a transform. This is
> the double gate.
>
> **Entry points** — input-only gates with no output counterpart: the seven
> `gate_include_*_input`, the three Galdr control surfaces, and `gate_verdandi_input`.
> Nothing writes these files back, so there is nothing to bracket. They exist to be the
> place where authored material first becomes typed.

An include file, a `content.toml`, a Verdandi level file — each is hand- or agent-authored
and would otherwise arrive as trusted data through a side door. An entry-point gate is what
makes that impossible.

### What a gate actually checks — three kinds, not one

"Schema validation" undersells it. A gate does three separable things, in shared crates
every gate draws on:

> **Format conversion** (`format_core`) — TOML in, JSON out, and back. This is why no
> Python project imports a TOML parser.
>
> **Schema validation** (`schema_core` + `schemas_embedded`) — the embedded JSON Schema,
> strict by construction: `additionalProperties: false` and complete required-lists.
>
> **Runtime contract verification** (`path_verify_io`) — walks the data for fields whose
> schema `format` is `path_exists_absolute` and checks each one exists on disk.

That third one closes a loop left open on the Verdandi side. Verdandi's `element/` level is
described as "an atom plus a runtime format contract" and contains only three files, which
looks like an underused level until you see what consumes it: `element/path_exists_absolute`
compiles to a `"format"` marker in the schema, and `path_verify_io` is what executes it.

**The `element` level exists to carry constraints JSON Schema cannot express, and the gate
is the thing that runs them.** Three elements because there are three runtime contracts.

### What makes failure "hard"

Nothing in the gate. The gate returns `{"ok": false, ...}` — the softest possible shape.
Each Python project has a thin wrapper that turns that into a raised `ValueError` with a
formatted message. So hardness is **convention implemented per project**, not a property
of the gate. If you write a new call site, you are responsible for it.

### Naming

`gate_{checkpoint}_{direction}`, where checkpoint is the **schema** being validated and
direction is `input` or `output` (passthrough gates omit it). Named for the schema, not
the caller: several branches read the same checkpoint, and one gate serves all of them.
Name a gate after a caller and you invite one near-duplicate gate per caller, each
looking meaningfully different when they are not.

### Schemas are embedded

Each gate compiles its schema in via `include_str!`. The schema files in the Nornir tree
are symlinks into the directory where **Draupnir writes its output** (which lives inside
the Verdandi tree — Verdandi itself runs nothing).

The consequence people trip on: **a changed schema has no effect until the gate is
rebuilt.**

```bash
nornir_deploy --build gates       # after any schema regeneration
```

The flip side is what makes the rebuild step worth having. **Tighten a schema, rebuild, and
what passed yesterday is refused today.** Data that got through because a schema was too
permissive stops getting through the moment the gate carries the stricter one —
retroactively, for every future run, with nothing to remember and no way around it.
Enforcement ratchets in one direction, and it is hard and fast mechanical.

That is also the repair path for the failure Verdandi exists to prevent. A too-permissive
schema is silent for as long as it stands; tightening it and rebuilding converts every
previously-tolerated input into a loud failure at the boundary.

### The gate that does not embed

`gate_verdandi_input` loads its schema from disk by name at runtime. It is generic — one
gate validating all fifteen Verdandi level formats, with the caller naming which schema
to use per call.

This genuinely weakens the guarantees claimed for embedding: that gate *can* be pointed
at a wrong or missing schema, and its schema changes are live without a rebuild. That is
a real inconsistency in the model, not a detail to wave past. It exists because a
generic validator cannot bake in fifteen alternatives; whether the trade is the right
one is a question for the author, not something to resolve by reasoning.

---

## The output tool builder

A generated agent does not get the `Write` tool. It gets a **purpose-built binary** that
can write one format, to one place, validated against one schema — and nothing else.

This is the double gate applied one level out. Regin and Galdr gate the *build*; the writer
binary gates the finished agent's *runtime output*. The agent is the LLM in the middle, and
the same rule holds: it may do whatever it does, so long as what comes out is verifiably
correct.

### The three pieces

> **`tool_registry.toml`** — the inventory of deployed writers. Each entry carries
> `binary_name`, `invocation`, `output_format`, `write_frequency`, `output_path_kind`,
> `schema_path`, and the file or directory path. Those fields mirror Verdandi's
> `enforcement_output_tool` group one-for-one, which is what makes matching possible at
> all.
>
> **`generate_writer.py`** — builds a new writer crate from parameters, emitting
> `writers/{name}/Cargo.toml` and a `main.rs` that is roughly twenty lines: a `WriterConfig`
> handed to `write_engine::run`. It deliberately does **not** self-register — it prints the
> four lines a human must add (`schemas_embedded`, workspace members, `tool_registry.toml`,
> `deploy_categories.toml`).
>
> **`write_engine`** — the shared runtime every writer delegates to. Reads stdin, validates
> against the embedded schema, then writes.

### What the binary guarantees

The schema is compiled in via `schemas_embedded`, exactly as with gates — so a writer
validates its own output before it lands, and a rebuild ratchets it the same way. Any
filename component the agent supplies at runtime goes through
`path_core::validate_path_segment` first, so the one degree of freedom the agent has cannot
become traversal. Writes are atomic or append-with-fsync.

And the failures are written **for the agent**, not for a log:

```
FAIL:batch too large — got 47 records, max is 20.
Split the batch into smaller chunks.
```

That is a repair instruction delivered through the only channel the agent is listening on.

### The Regin side, and where it stops

`discover_tool` (`logic/pure/tool_resolve/composed.py`) matches the agent's declared output
spec against the registry. On a hit it returns the `binary_name` plus the exact invocation
string, and whether the variant needs a runtime filename.

The intent is that a miss produces a request to build the missing binary. **That half does
not exist.** `discover_tool` returns `None`, and downstream `has_tool = resolved_tool is not
None` treats that as *this agent has no output tool* — indistinguishable from an agent that
never declared one. An agent that asks for a JSONL writer it has no binary for silently
becomes an agent with no writer at all.

Two further sharp edges in the same path, both tracked in Verdandi's `TODO.md`:

> `field_matches` returns `True` when the spec value is `None`, so **a missing spec field
> matches any registry entry.** Combined with the dead `always_when` that leaves
> `output_tool_schema_path` never required, a spec with no schema path will match the first
> entry of the right format — binding an agent to a writer that validates against a
> different schema entirely.
>
> This is very likely the upstream cause of the literal `{{tool_name}}` that
> [[GALDR_ELEMENT]] reports shipping into the staging artifact. Not one bug — a silent
> `None` here meeting an unimplemented suppress-on-incomplete there.

---

## Why it is built this way

### Why a wall — two reasons, one mechanism

These are coequal, and as coupled as they look.

**The gate is the only door.** Roughly nine of ten persistent errors in LLM-written code
occur at IO boundaries — where data enters and its type dissolves into "whatever the file
contained." Measured across independent projects, and rooted in a training corpus that is
weakest exactly there. Because a compiled module owns reading and writing, every other
avenue for data to get into or out of the application can be closed.

**The gate is the checkpoint.** Two of them bracketing a transform keep the blast radius
small and give incremental verification. An LLM may do whatever it does in the middle, so
long as the result is correct going in and correct coming out — verifiably, mechanically,
at both ends. That is what makes LLM-written transformation safe to have in the pipeline at
all, and it is why nothing merges or advances unless the previous stage was verifiably
correct.

Neither half stands alone. Verification without owning the IO leaves a path for data to
arrive around the check; owning the IO without verification gives a safe door and no proof.
The architecture *depends* on the double gate — and the double gate can be airtight only
because the same component owns the door.

The stated evolution: secure the boundaries → externalize the IO → *there is no door*.

**How far that has actually gone, precisely.** Input is gated everywhere. Output is not
yet — Galdr writes its result with a direct `write_text` call rather than through an
output gate. Python retains `open()`; nothing removes it. What holds the line is that
gates are the only reasonable path, that a guardrail system analyses every file you
write and flags zone violations, and that you know the rule.

**Treat "no IO in Python" as an obligation you maintain, not a guarantee you inherit.**
The aspirational phrasing — violations being *unrepresentable* — describes the target,
and reading it as the present state is the most expensive mistake available here,
because it converts vigilance into false confidence.

One nuance worth holding: even where gates are used, **Python still chooses the path**.
It builds the string and hands it over. The wall absorbs decoding and validation, not
path selection.

### Why a separate language

The wall and the logic have different jobs and different change rates: solved once and
left alone, versus churning constantly. A separate language, build, and repository means
an LLM iterating on Python business logic is not one file away from the validator that
constrains it. That is a distance argument rather than an impossibility argument — the
Rust source is a writable file on the same disk — but distance plus a rebuild step plus
a guardrail is what exists, and it is meaningfully stronger than a comment.

### Why one decoder

Every project could parse its own TOML. None do. Decoding happens once, in one engine,
for every format and project. The point is not that `tomllib` is bad — it is that a
second decode site is a second place data enters *without passing a schema*. One door,
or several.

### Why loud failure

Rename a field three layers above where it is used. In defensive code — catching
broadly, defaulting generously — every layer absorbs the mismatch and passes slightly
wrong data on. The bug surfaces weeks later as wrong output with no traceback.

Gate validation fails immediately at the boundary instead. **This depends on the schemas
being strict** — `additionalProperties: false` and complete required-lists — which the
generated schemas are. Under a permissive schema the rename would pass silently and this
argument would not hold.

---

## Working with it

**Build with `nornir_deploy`. Never bare `cargo build` or `maturin build`.** A bare cargo
build leaves the artifact in `target/release/` where nothing looks for it. Gates
additionally need the maturin path — wheel build, `.so` extraction into
`~/.ai/tools/lib/`, and code signing, without which macOS kills the process on import.

**When you meet data with no gate for its format or schema, stop and ask the author for
one.** Not parse it "temporarily," not type it `Any` "for now." Every gate that exists
came into being that way. There is no self-service procedure — a gate is hand-written
Rust plus a workspace entry plus a deploy category, so adding a schema file and
rebuilding will not produce one.

Unidentified data waits at the door.
