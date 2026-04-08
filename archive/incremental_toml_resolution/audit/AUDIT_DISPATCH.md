# TOML Extraction Audit — Dispatch Template

## What You Are Auditing

13 TOML extraction files that define the control surface for an agent prompt composition system called Galdr. Each file specifies which prose fragments, structural toggles, and display formats are configurable for one section of an agent prompt.

The extraction files are design documents — they contain proposed TOML blocks for three files (structure.toml, content.toml, display.toml) plus decisions rationale and excluded invariants.

## Why This Audit Matters

The next step after these extractions is building JSON Schemas that validate the TOML files mechanically. If naming patterns are inconsistent, if interface patterns are applied differently across sections, if structure/content field names don't match — the schema can't be written. Every inconsistency that survives this audit becomes a special case in the schema, a branch in the renderer, and a trap for every LLM that edits these files.

The audit exists to ensure the 13 extractions are coherent enough to derive a single, consistent schema from.

## What You Must Read Before Writing Anything

Read ALL of the following. Do not start writing until you have read every file.

1. **The architecture doc** — `agent_control_surfaces/TOML_ARCHITECTURE.md`
   This is the source of truth. It defines the file architecture, interface patterns, naming conventions, section categories, threshold types, and crucially: the design decisions that explain WHY things are the way they are. Every finding you produce must be measured against this document. If the architecture doc says something is intentional, it is not an issue.

2. **Two reference data files** — real `anthropic_render.toml` showing what the renderer receives:
   - `definitions/agents/agent-builder/anthropic_render.toml` (no output tool, creative task, many context docs)
   - `definitions/agents/interview-enrich-create-summary/anthropic_render.toml` (has output tool, batch processing task)

3. **All 13 extraction files** in `agent_control_surfaces/incremental_toml_resolution/` (every .md file, NOT the audit/ subdirectory):
   ANTI_PATTERNS, CONSTRAINTS, CRITICAL_RULES, EXAMPLES, FAILURE_CRITERIA, IDENTITY, INPUT, INSTRUCTIONS, OUTPUT, RETURN_FORMAT, SECURITY_BOUNDARY, SUCCESS_CRITERIA, WRITING_OUTPUT

## What The Audit Is Looking For

You are checking whether the 13 extraction files conform to the architecture doc. You are NOT redesigning the system or questioning documented design decisions.

### Good findings (report these)

**Convention violations** — the architecture doc establishes conventions. Does every file follow them?
- Do all `_visible` fields in structure.toml have matching content fields with the SAME name (including position suffix)?
- Do all `_variant` selectors follow the pattern: structure has `{concept}_variant = "{value}"`, content has `{concept}_{value} = "..."`?
- Do all threshold fields use the correct suffix (`_format_threshold`, `_visibility_threshold`, `_activation_threshold`, `_auto_threshold`)?
- Are field names self-documenting to a naive reader without comments?

**Misplaced fields** — does any field live in the wrong file?
- Prose/behavioral content in display.toml (should be content.toml)
- Variant selectors in display.toml (should be structure.toml)
- Format selectors in structure.toml (should be display.toml)

**Phantom fields** — structure toggle with no matching content field, or content field with no structure toggle (when the field is optional and should be togglable)

**Cross-section inconsistency** — the same pattern handled differently in two sections without documented reason

**Content that restates data** — a content field that just says what the data already provides, adding no prose value. Per the filtering principle: "if a fragment has no meaningful variation, it does NOT get a TOML entry."

### Bad findings (do NOT report these)

**Re-litigating documented decisions** — the architecture doc explains:
- Why guardrails family (anti_patterns, constraints, success_criteria, failure_criteria) has `section_visible` and `max_entries_rendered` but other sections don't
- Why CRITICAL_RULES has per-rule `_visible` toggles even when data gates exist (boilerplate show/hide for testing)
- Why CRITICAL_RULES and WRITING_OUTPUT intentionally overlap on tool exclusivity
- Why mechanics sections (output, writing_output, return_format) have thin control surfaces

If the architecture doc explains it, it is not a finding. Move on.

**Flagging invariants as issues** — silence-for-absence, heading levels, sub-block ordering are all documented as code behavior. Noting that a section doesn't have a toggle for an invariant is not useful.

**Suggesting new knobs** — your job is to check what exists against the conventions, not to propose additions.

## Output Format

Write ONE holistic report covering all 13 sections. Not 13 separate reports. One document that sees the full picture.

Structure your report as:

```markdown
# TOML Extraction Audit

## Summary
2-3 sentences on overall conformance quality.

## Findings

### [SEVERITY]: Brief title
- **Where**: section(s) and field(s) affected
- **Convention violated**: which architecture doc rule
- **Specific**: exact field names, exact mismatch
- **Fix**: what the correct state should be
```

Severity levels:
- **CONVENTION**: violates a documented pattern from the architecture doc
- **MISMATCH**: structure/content field names don't match
- **MISPLACED**: field in wrong file
- **INCONSISTENCY**: same pattern handled differently across sections without reason

Do not pad the report. If a section is clean, don't mention it. Only report actual findings with specific field names and specific fixes.

## Write To

Write your report to the path specified when you are dispatched (AUDIT_A.md, AUDIT_B.md, or AUDIT_C.md).

Return SUCCESS or FAILURE.
