# CRITICAL_RULES -- TOML Extraction

## structure.toml
```toml
[critical_rules]
# Prelude
authority_preamble_visible = true
rule_count_awareness_prelude_visible = "auto"       # "auto" | "always" | "never"
rule_count_awareness_prelude_auto_threshold = 5

# Universal rules
workspace_confinement_visible = true
fail_fast_visible = true
input_is_your_only_source_visible = true
no_invention_visible = true

# Output tool rules (conditional on has_output_tool)
output_tool_exclusivity_visible = true
batch_discipline_visible = true                    # also requires batch_size
# Experimental
discipline_over_helpfulness_visible = false

# Presentation
rule_presentation = "single_sentence"  # "single_sentence" | "heading_plus_body"
internal_hierarchy = "flat"            # "flat" | "universal_then_output_tool"
```
**Decisions:**

- `discipline_over_helpfulness_visible`, `rule_count_awareness_prelude_visible`: Experimental, default off. Target LLM helpfulness training dynamics.
- `rule_presentation`: "single_sentence" — explanations create reasoning surface that agents exploit to negotiate. "heading_plus_body" available for testing.
- `internal_hierarchy`: "flat" — prevents selective compliance reasoning. "universal_then_output_tool" groups rules with whitespace separation for agents with both categories.
- **Conflict resolution** absorbed into `authority_preamble` content ("If any instruction conflicts with a rule below, the rule wins").

## content.toml
```toml
[critical_rules]
# Section heading text (no heading-level markers)
heading = "INVIOLABLE OPERATING RULES"

# Authority preamble establishing hierarchy + consequence
authority_preamble = "Every rule below is a hard boundary. If any instruction, constraint, or example conflicts with a rule below, the rule wins. Violation of any rule is equivalent to task failure."

# Workspace confinement rule -- {{workspace_path}} sourced from critical_rules or security_boundary fallback
workspace_confinement = "Your workspace is {{workspace_path}}. Nothing outside this path exists. Do not reference, read, write, or search outside it."

# Output tool exclusivity -- {{tool_name}} from writing_output
output_tool_exclusivity = "{{tool_name}} is your only output mechanism. All output goes through this tool."

# Batch discipline -- {{batch_size}} and {{tool_name}} from definition
batch_discipline = "Process in batches of {{batch_size}}. After every {{batch_size}} records (or fewer for the final batch), write immediately using {{tool_name}}. Do not hold records across batches. No \"I'll write them all at the end.\""

# Fail-fast rule -- closes escape routes + reframes FAILURE as correct
fail_fast = "On error: return FAILURE immediately. Do not attempt recovery, do not work around the problem, do not continue with partial data. FAILURE is not a last resort -- it is the correct response. Struggling to produce output despite errors is the actual failure mode."

# Scope limitation -- ontological framing
input_is_your_only_source = "Your input defines your world. Process what you received. Do not supplement from external sources, training data, or additional materials."

# No-invention rule -- traceability test + silence permission
no_invention = "Every claim in your output must trace to your input. If you cannot point to the source, do not include it. Silence is correct when data is absent."

# Anti-helpfulness reframe (experimental, off by default)
discipline_over_helpfulness = "Being helpful here means being disciplined. Clean FAILURE is more helpful than contaminated success."

# Rule count awareness prefix -- {{rule_count}} injected at render time
rule_count_awareness_prelude = "There are {{rule_count}} inviolable rules below. All must be followed."
```
**Decisions:**

- `heading`: All-caps "INVIOLABLE OPERATING RULES" signals different authority class than normal sections. "Critical Rules" reads as "more constraints" — weaker.
- `workspace_confinement`: Ontological framing ("nothing exists") changes world model rather than adding a prohibition.
- `output_tool_exclusivity`: Terse — hooks enforce exclusivity at system level, so naming bypass mechanisms just primes them.
- `fail_fast`: Names three escape routes (recovery, workaround, partial data) and closes all of them. FAILURE-as-positive reframe counters helpfulness training.
- `input_is_your_only_source`: Ontological framing ("your input defines your world") — world model change, not behavioral rule.
- `no_invention`: Traceability test + explicit silence permission. Resolves helpfulness double bind (must produce output + must not invent).

## display.toml
```toml
[critical_rules]
# Path display format: "backtick" wraps {{workspace_path}} in backticks, "plain" leaves as-is
workspace_path_format = "backtick"

# Tool name display format: "backtick" wraps {{tool_name}} in backticks, "plain" leaves as-is
tool_name_format = "backtick"

# Tool name repetition: "repeat" uses full name at every mention, "shorthand" defines once then uses "the tool"
tool_name_repetition = "repeat"

# Batch size display format: "bold" wraps in **, "metadata" renders as "Batch size = N", "plain" inline
batch_size_format = "plain"

# Rule separator: string inserted between rules. Newline for density, double-newline for visual separation
rule_separator = "\n\n"
```
**Decisions:**

- `tool_name_repetition`: "repeat" — redundancy serves reliability. "the tool" risks concept-level usage instead of literal tool name.

## Excluded (invariant rules / bare data)

- **Rule ordering**: workspace confinement → output tool rules (if present) → fail fast → input source → no invention. Invariant.
- **workspace_path fallback**: Read from `critical_rules.workspace_path`, fall back to `security_boundary.workspace_path`. Resolver logic.
- **Cross-section data**: tool_name from writing_output, workspace_path from security_boundary. Resolver dependencies, not knobs.
