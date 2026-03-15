# Plan: Galdr Composition Engine

**What:** Replace Jinja2 template rendering with a config-driven composition engine built on pure Python rendering primitives.

**Why:** Enable empirical optimization of agent prompts. Produce multiple structurally different prompts from identical content, varying only composition and style. Measure which prompt structure produces the best agent behavior for a given task.

**Key decisions:**

- Drop Jinja2 — rendering primitives are pure Python functions returning markdown strings
- 14 independent modules (split success/failure criteria out of return_format, split constraints/anti_patterns out of guardrails)
- Four control knobs: order/skips, display structure, flavor/tone, special settings
- Three TOML inputs: vendor render (content), recipe (composition), style (tone)
- No variant template files — rendering primitives + config replace the entire template directory
- Section configs in recipes control variant, field selection, framing, warnings

**Milestones:**

- **L1: Parity** — `galdr input.toml` with no flags produces equivalent output to current system. Default recipe and style are built-in. No new CLI flags needed yet.
- **L2: Recipes** — `--recipe` flag enables module reordering, variant selection, per-module config from TOML files.
- **L3: Styles** — `--style` flag (or style field in recipe) enables tone variation from TOML files.
- **L4: Benchmarking** — `--recipe-batch` renders multiple compositions from same content for comparison.
