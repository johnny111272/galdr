# Custom Write Tools

How enforcement output tools work, from agent definition to deployed binary.

## Overview

Agents that produce structured output (JSON or JSONL) don't use generic file writes. They use **enforcement output tools** — purpose-built Rust binaries that validate every write against an embedded JSON Schema before committing to disk. Each binary is ~15 lines of Rust config on top of a shared runtime (`write_core`).

The system has five layers:

1. **Agent definition** — declares what output tool it needs
2. **Regin discovery** — matches the spec against deployed tools (or fails with a build request)
3. **Codegen** — generates the Rust crate from parameters
4. **Runtime** — `write_core` handles all validation, path protection, and IO
5. **Deployment** — builds, symlinks, and verifies

## The Demand Signal

The agent definition's `[security.security_schema]` and `[task.processing]` sections together produce an `enforcement_output_tool` group during Regin's permission resolution. This group contains:

| Field | Source | Example |
|-------|--------|---------|
| `enforcement_output_tool_format` | `processing_output_file_format` | `jsonl` |
| `enforcement_output_tool_write_frequency` | `processing_output_write_frequency` | `record` |
| `enforcement_output_tool_batch_size` | `processing_output_batch_size` | `20` |
| `enforcement_output_tool_name_needed` | `processing_output_file_name_known` | `true` (when `partially` or `unknown`) |
| `enforcement_output_tool_name_pattern` | `processing_output_file_name_template` | `{uid}.summaries.jsonl` |
| `enforcement_output_tool_schema_path` | `security_output_schema` (absolutized) | `/abs/path/to/summaries.schema.json` |
| `enforcement_output_tool_file_path` | `security_io_output_file` (absolutized) | `/abs/path/to/output.jsonl` |
| `enforcement_output_tool_directory_path` | `security_io_output_directory` (absolutized) | `/abs/path/to/interviews/` |

The conditional system controls which fields appear:

- `file_path` only when `processing_output_file_name_known = "known"` (full path known at definition time)
- `directory_path` + `name_pattern` when `partially` (suffix known, LLM provides prefix/stem)
- `directory_path` only when `unknown` (LLM provides full filename)

## Tool Discovery (Regin Level 8)

During anthropic resolution, `tool_discovery.py` matches the agent's spec against `tool_registry.toml`. Matching checks **all** of:

1. `output_format` — jsonl or json
2. `write_frequency` — record or batch
3. `schema_path` — exact path match
4. Output path — depends on kind:
   - `fixed_file`: exact `file_path` match
   - `directory_name` / `directory_prefix`: exact `directory_path` match AND naming pattern suffix match

The naming pattern suffix is extracted from the `FilenameTemplate` (everything after the `{variable}` placeholder) and compared against the registry's `name_extension` (prefixed with `.`) or `name_suffix`:

```
Pattern: {uid}.summaries.jsonl  →  suffix: .summaries.jsonl
Registry: name_suffix = ".summaries.jsonl"  →  match

Pattern: {entry-id}.json  →  suffix: .json
Registry: name_extension = "json"  →  match (becomes .json)
```

**Three outcomes:**

- **No spec** — agent has no output tool. `discover_custom_tool` returns `None`.
- **Match** — returns `ResolvedTool` with binary name, invocation variant, and heredoc display.
- **No match** — raises `CustomToolNotFound` with a `ToolBuildRequest` containing everything needed to build the missing binary.

## The Tool Registry

`tools/regin/tool_registry.toml` lists all deployed writer binaries with their capabilities:

```toml
[[tools]]
binary_name = "append_interview_summaries_record"
output_format = "jsonl"
write_frequency = "record"
output_path_kind = "directory_prefix"
schema_path = "/abs/path/to/summaries.schema.json"
directory_path = "/abs/path/to/interviews"
name_suffix = ".summaries.jsonl"
```

Fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `binary_name` | always | Name of the deployed binary |
| `output_format` | always | `jsonl` or `json` |
| `write_frequency` | always | `record` or `batch` |
| `output_path_kind` | always | `fixed_file`, `directory_name`, or `directory_prefix` |
| `schema_path` | always | Absolute path to the `.schema.json` file |
| `file_path` | `fixed_file` only | Absolute path to the output file |
| `directory_path` | directory kinds | Absolute path to the output directory |
| `name_extension` | `directory_name` | File extension without dot (e.g., `json`) |
| `name_suffix` | `directory_prefix` | File suffix including dots (e.g., `.summaries.jsonl`) |

## Binary Naming Convention

```
{verb}_{human_chosen_name}_{frequency}[_{batch_size}]
```

- `append_` — JSONL format (append to existing file)
- `write_` — JSON format (create new file, atomic)
- The middle segment is **human-chosen** for readability among dozens of binaries
- `_record` or `_batch_N` suffix

Examples:

```
append_truth_qc_report_record        # JSONL, record-at-a-time, fixed file
write_truth_glossary_record           # JSON, one file per invocation, directory + extension
append_embedding_normalize_batch_20   # JSONL, 20 records per batch, fixed file
append_interview_summaries_record     # JSONL, record-at-a-time, directory + suffix
```

## The Writer Binary

Each writer is a Rust crate with two files. The `main.rs` is a `WriterConfig` struct literal:

```rust
use schemas_embedded::SUMMARIES;
use write_core::{OutputFormat, OutputPath, WriteFrequency, WriterConfig};

fn main() {
    write_core::run(&WriterConfig {
        name: "append_interview_summaries_record",
        schema: &SUMMARIES,
        schema_source_path: "/abs/path/to/summaries.schema.json",
        format: OutputFormat::Jsonl,
        frequency: WriteFrequency::Record,
        output: OutputPath::DirectoryPrefix {
            dir: "/abs/path/to/interviews",
            suffix: ".summaries.jsonl",
        },
        batch_size: None,
    });
}
```

Everything is hardcoded at compile time. The binary embeds the schema, the paths, the format, the frequency, and the batch limit. The LLM provides only:

- **Data** via stdin (piped JSON or heredoc)
- **Name** as a CLI argument (only for directory-based outputs)

## Output Path Strategies

| Strategy | Config | LLM provides | Constructed path |
|----------|--------|--------------|------------------|
| `FixedFile("/path/output.jsonl")` | hardcoded path | nothing | `/path/output.jsonl` |
| `DirectoryName { dir, ext }` | dir + extension | filename stem | `{dir}/{stem}.{ext}` |
| `DirectoryPrefix { dir, suffix }` | dir + suffix | prefix | `{dir}/{prefix}{suffix}` |

Path traversal protection validates the LLM-provided component before path construction. Attempts like `../escape` or `/absolute/override` are rejected.

## write_core Runtime

`write_core::run()` handles:

- **Stdin reading** — reads all input to a string
- **JSON parsing** — validates well-formed JSON
- **Schema validation** — validates against the embedded schema (`schemas_embedded`)
- **Path resolution** — constructs the output path from config + CLI arg
- **Path traversal protection** — rejects `..`, absolute overrides in LLM-provided components
- **Format enforcement** — JSONL appends to existing files; JSON creates new files atomically
- **Batch limits** — for `Batch` frequency, enforces max records per invocation
- **Atomic writes** — JSON files written to temp + renamed (no partial writes)
- **`--help`** — prints all hardcoded config, schema path, invocation pattern
- **`--dump-schema`** — prints the embedded JSON Schema to stdout for inspection

Exit protocol: `OK` on success, `FAIL:<reason>` on failure. Exit code 0 or 1.

## schemas_embedded

`schemas_embedded` is a Rust crate that compiles JSON Schema files into the binary via `include_str!()`. Each schema becomes a `pub static EmbeddedValidator`:

```rust
static SUMMARIES_JSON: &str =
    include_str!("/abs/path/to/summaries.schema.json");
pub static SUMMARIES: EmbeddedValidator =
    EmbeddedValidator::new(SUMMARIES_JSON, "summaries");
```

Absolute paths are used so the schemas can be inspected from `--help` output without consulting source code. The validator compiles the schema once on first use (`OnceLock`) and validates via `jsonschema`.

## Generating a New Writer

Use `tools/nornir/generate_writer.py`:

```bash
./tools/nornir/generate_writer.py \
    --name append_interview_summaries_record \
    --schema-const SUMMARIES \
    --schema-path /abs/path/to/summaries.schema.json \
    --format jsonl \
    --frequency record \
    --output-kind directory_prefix \
    --dir-path /abs/path/to/interviews \
    --suffix .summaries.jsonl
```

This generates `writers/{name}/Cargo.toml` and `writers/{name}/src/main.rs`, then prints the manual wiring steps:

1. Add the schema to `schemas_embedded/src/lib.rs` (if new)
2. Add `"writers/{name}"` to workspace `Cargo.toml` members
3. Add entry to `tool_registry.toml`
4. Add to `WRITER_CRATES` in `tools/nornir/deploy_writers.py`

Use `--dry-run` to preview without writing files.

## Deployment

Two separate scripts in `tools/nornir/`:

**Gates and CLI checkers** — schema validation infrastructure:
```bash
./tools/nornir/deploy_gates.py
```
Builds 8 CLI check tools (`check_*`) and 32 PyO3 gate modules (`gate_*`) via maturin. Gates deploy to `~/.ai/tools/lib/`, CLI tools symlink to `~/.ai/tools/bin/`. Run after Verdandi/Draupnir schema changes.

**Writer tools** — enforcement output binaries:
```bash
./tools/nornir/deploy_writers.py
```
Builds writer binaries via `cargo build --release`, symlinks to `~/.ai/tools/bin/`, verifies with `--help`. Run after adding or modifying a writer crate.

## Invocation by the LLM

The generated agent prompt includes a `writing_output` section with the exact invocation pattern:

**Fixed file (no name needed):**
```bash
cat <<'RECORD' | append_embedding_normalize_batch_20
{"uid":"...","description":"..."}
RECORD
```

**Directory output (name needed):**
```bash
cat <<'RECORD' | append_interview_summaries_record my-interview-id
{"uid":"...","summary":"..."}
RECORD
```

The binary handles everything else — the LLM never constructs file paths.

## End-to-End Flow

```
Agent definition TOML
    │
    ▼
Regin levels 1-7 (resolve paths, permissions, merge, regroup)
    │
    ▼
Regin level 8: tool_discovery.py
    │
    ├─ match found → ResolvedTool (binary name, invocation)
    │       │
    │       ▼
    │   anthropic_resolver populates:
    │     - writing_output (invocation pattern for LLM)
    │     - critical_rules (workspace path, tool name)
    │     - frontmatter.hooks (Bash hook validates tool usage)
    │     - frontmatter.tools (tool allowlist)
    │       │
    │       ▼
    │   Galdr renders agent .md with writing_output section
    │       │
    │       ▼
    │   LLM uses: cat <<'RECORD' | binary_name [name]
    │
    └─ no match → CustomToolNotFound + ToolBuildRequest
            │
            ▼
        generate_writer.py (codegen)
            │
            ▼
        Manual wiring (Cargo.toml, registry, schemas_embedded)
            │
            ▼
        deploy_writers.py (build + symlink + verify)
            │
            ▼
        Re-run Regin → match found → agent passes
```
