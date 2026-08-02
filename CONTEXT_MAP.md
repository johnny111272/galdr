<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- DO NOT EDIT THIS BLOCK. Before editing ANY part of this file, you MUST  -->
<!-- first read /Users/johnny/.ai/CONTEXT_MANAGEMENT_SYSTEM.md — it defines  -->
<!-- what this file is for and what may NOT go in it.                        -->
<!--                                                                          -->
<!-- This file is a MAP (a router), not a source. Its only job is to tell    -->
<!-- you WHERE the context lives — it never holds the context, state, or     -->
<!-- progress itself. Reading this map does NOT orient you; you are NOT      -->
<!-- oriented until you have read the Orientation-gate docs it points to, in -->
<!-- the order given.                                                         -->
<!--                                                                          -->
<!-- THE WHITELIST RULE: if a doc is not in this map, it is not for           -->
<!-- orientation — do not read it. A stale doc is UNLINKED or DELETED, never -->
<!-- flagged in place. No freshness tags. No "do-not" guards. No state.       -->
<!-- Behavioral rules live in CLAUDE.md, not here.                            -->
<!--                                                                          -->
<!-- This file is LOW-CHURN. It changes only when how-to-get-oriented        -->
<!-- changes — i.e. a doc is added or removed. It is not a worklog and is    -->
<!-- not regenerated per session.                                            -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

# CONTEXT_MAP — Galdr

## Purpose

Galdr is the composition engine — the final stage of the agent pipeline (Verdandi → Draupnir → Nornir → Regin → **Galdr**): it combines one gate-validated agent data model with three independently swappable control surfaces (structure, content, display) into deployable agent prompts.

---

## Orientation gate — read these, in this order, to be oriented

1. `redesign/AGENT_BUILD_SYSTEM.md` — the four-axis model and the benchmarking matrix: why the axes exist and why entangling any two of them destroys the product.
2. `redesign/COMPOSITION_ENGINE_DESIGN.md` — the generic engine: one `compose_section()` for all sections, buffer slots, data gates, zero per-section code.
3. `redesign/01_PROCESSING_FLOW.md` — the four-stage pipeline (chunk, gather, resolve+render, buffer) and why each stage shrinks the problem.
4. `redesign/TOML_ARCHITECTURE.md` — the naming law: positional suffixes, field interface patterns, threshold types, section categories. The engine reads names mechanically; this doc is the authority on what names mean.
5. `~/.ai/smidja/nornir/core/gleipnir_core/V2_ZONE_ARCHITECTURE.md` — the import law: zones, levels, CC bands, the gravity rule. Where code is allowed to live.

**Proof:** before writing anything, state three project-specific constraints that
diverge from how you'd normally do this work, with reasons. If you can't, you are
not oriented — go back and read.

---

## Refresh guide — want X → read Y

| Need | Read |
|------|------|
| bundle container design | `redesign/02_INTERMEDIATE_CONTAINER.md` |
| chunking / slot assignment | `redesign/03_CHUNKING.md` |
| hourglass resolver (visibility, variants, interpolation, suppress-on-incomplete) | `redesign/04_HOURGLASS_RESOLVER.md` |
| body ordering (data drives, decorations, standalone content) | `redesign/05_BODY_ORDERING.md` |
| renderer set / data shape detection | `redesign/06_RENDERER_TYPES.md` |
| trunk matching (content↔data linking) | `redesign/07_TRUNK_MATCHING.md` |
| naming rules in one page | `redesign/08_NAMING_REQUIREMENTS.md` |
| enforcement output tools, end to end | `redesign/CUSTOM_WRITE_TOOL.md` |
| per-section four-axis field inventory | `review/{SECTION}.md` — audit sheets; verify any wiring claim against the code before relying on it |
| current bundle snapshot + probes | `review/BUNDLE_INSPECTION.md`, `probe/*.py` (regenerate, don't trust old output) |
| deferred rendering features | `plans/DEFERRED_RENDERING_FEATURES.md` |
| data / content / structure / display model shapes | `src/galdr/structure/gen/*.py` (generated — never edit) |
| the live control-surface TOMLs | `extracted/content.toml`, `extracted/structure.toml`, `extracted/display.toml` |
| how to run | `src/galdr/cli.py` — the CLI is the truth; `uv run galdr --help` |
| gate pattern / orchestrate wiring reference | `~/.ai/smidja/regin/src/regin/logic/` |
| level progression reference | `~/.ai/smidja/draupnir/src/draupnir/logic/` |
| current state / what's left to build | read live: the code + `git log`. Nothing is stored. |
