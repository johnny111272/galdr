# Deferred Rendering Features

Features identified during schema review that require significant engine capability beyond the v1 build. These are **deferred, not cancelled** — they're worth implementing but add complexity the initial rendering engine doesn't need to handle.

The schema fields for these features exist in Verdandi but the engine ignores them. When we're ready to implement, the fields are already there — we just flip the switch on engine support.

---

## 1. Rule Presentation: Single Sentence vs Heading Plus Body

**Field:** `critical_rules_rule_presentation` (structure)
**Values:** `"single_sentence"` | `"heading_plus_body"`

**Current behavior (single_sentence):** Each critical rule renders as dense prose. Example:
```
Your workspace is /path/to/workspace. Nothing outside this path exists. Do not reference, read, write, or search outside it.

On error: return FAILURE immediately. Do not attempt recovery...
```

**Target behavior (heading_plus_body):** Each critical rule gets a bold heading plus explanatory body:
```
**Workspace Confinement**
Your workspace is /path/to/workspace. Nothing outside this path exists...

**Fail Fast**
On error: return FAILURE immediately...
```

### Why it matters

Critical rules are the most important rules in the agent prompt. Visual distinction as named blocks may help the agent internalize each rule more thoroughly than dense prose. Headings also make rules referenceable ("you violated rule X").

This is exactly the kind of formatting variation galdr's benchmarking matrix exists to test.

### What's needed to implement

1. **Heading source for each rule.** Two options:
   - **Mechanical derivation:** Strip the suffix from the content field name and title-case it. `workspace_confinement_declaration_template` → "Workspace Confinement". Cheap but constrains field naming.
   - **Explicit content fields:** Add `{rule}_heading` content fields like `workspace_confinement_heading = "Workspace Confinement"`. More flexible, more authoring work.

2. **Engine awareness.** The rules body renderer needs to read `rule_presentation` and either:
   - Render each rule as-is (single_sentence), or
   - Render a heading + body per rule (heading_plus_body)

   Currently the engine renders each content field as one output point. The heading_plus_body mode needs to render TWO outputs per rule (heading + body).

3. **Spacing control.** In heading_plus_body mode, the separator between rules matters more. Would want to ensure `rule_separator` works correctly with the heading format.

### Estimated complexity

Medium. The mechanical derivation path is cheap to implement. The engine change is localized to the rules body renderer.

---

## 2. Internal Hierarchy: Flat vs Grouped Rules

**Field:** `critical_rules_internal_hierarchy` (structure)
**Values:** `"flat"` | `"universal_then_output_tool"`

**Current behavior (flat):** All critical rules render in one list.

**Target behavior (universal_then_output_tool):** Rules are split into two groups by applicability:
```
### Universal Rules
(rules that always apply — workspace, fail fast, input source, no invention)

### Output Tool Rules
(rules that only apply when has_output_tool=true — exclusivity, batch discipline)
```

### Why it matters

When `has_output_tool=true`, there are 3 additional rules. Grouping makes the conditionality structure explicit — the agent sees that certain rules ONLY matter when using the output tool, not for every action.

When `has_output_tool=false`, the output-tool rules are already suppressed (via suppress-on-incomplete interpolation). The grouping would only be visible when has_output_tool=true.

### What's needed to implement

1. **Rule classification.** The engine needs to determine which rules are "universal" vs "output tool specific". Two approaches:
   - **Placeholder scanning:** A rule that references `{{tool_name}}` or `{{batch_size}}` is output-tool-specific. Otherwise universal. This works generically without per-section metadata.
   - **Explicit classification:** Add a metadata field on each rule's content definition. More explicit but more authoring work.

2. **Sub-heading content.** The group headings ("Universal Rules" / "Output Tool Rules") don't exist. Would need two new content fields or hardcoded strings.

3. **Sub-group rendering capability.** The engine currently renders a section's body as a flat sequence. Sub-groups within a body are a new rendering concept — each group has its own heading + body.

4. **Conditional rendering.** The "Output Tool Rules" group should only render when has_output_tool=true. This is already the behavior for the individual rules, but the group heading needs the same gate.

### Estimated complexity

High. Sub-group rendering within a section body is a significant engine capability that affects multiple sections (examples already has groups, which currently work via the nested group pattern). May be worth unifying the two concepts.

---

## 3. Output vs Agent Voice

**Field:** `success_criteria_output_vs_agent_voice` (structure)
**Values:** `"output_centric"` | `"agent_centric"`

**Current behavior (output_centric):** Success criteria describe what the output looks like. "The output contains X. Every record has Y."

**Target behavior (agent_centric):** Success criteria describe what the agent did. "You have produced X. You have validated Y."

### Why it matters

Voice framing affects self-evaluation. An agent reading "the output contains X" checks the output. An agent reading "you have produced X" checks its own actions. These might lead to different completion judgments in edge cases.

This distinction might apply beyond success_criteria — the same voice question exists for failure_criteria, instructions, constraints, and identity. If voice matters, it's probably a cross-section concern that should be consistent throughout an agent prompt.

### What's needed to implement

1. **Decision on scope.** Is voice per-section or global?
   - **Per-section:** Each section has its own voice control. Flexible but inconsistent.
   - **Global:** One voice setting applies to all agent-facing prose. Consistent but coarse.

2. **Variant content for both voices.** The engine can't mechanically transform prose voice. Each piece of prose needs to be authored twice — once in each voice.

3. **Content axis expansion.** For each section with voice-sensitive prose, add variant sub-tables keyed by voice value. Every content fragment that's affected needs both variants.

4. **Authoring burden.** This is the highest-cost feature because it doubles authoring work for every voice-sensitive prose fragment.

### Estimated complexity

High. The engine change is small (variant selection already exists), but the content authoring cost is substantial. May be worth experimenting with voice on ONE section first to see if the effect is measurable before investing in full cross-section coverage.

### Alternative: cross-section voice as override pattern

Instead of adding variant sub-tables per section, keep the default voice and create "voice override" content files that replace voice-sensitive prose fragments. The override system already exists in the four-axis design (override.toml). A voice experiment would be a named override file that swaps prose fragments.

This avoids expanding every content.toml with variants and keeps voice experiments as opt-in override bundles.

---

## Priority Order for Implementation

1. **Rule separator** — already kept, simple display control, implement with the body renderer
2. **Rule presentation** (heading_plus_body) — medium complexity, high experimental value for critical rules
3. **Internal hierarchy** (universal_then_output_tool) — high complexity, depends on sub-group rendering capability
4. **Output vs agent voice** — high authoring cost, consider override pattern instead of per-section variants

## Current Status

All four fields remain in the Verdandi schema. The engine ignores three of them (presentation, hierarchy, voice) during v1 rendering. The fourth (rule_separator) is wired in as a section-wide display control.

When implementing any of these, the schema doesn't need to change — just the engine.
