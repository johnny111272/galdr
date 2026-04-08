# Control Surface Design

Three-axis composition: data × style × display. This document designs the control surfaces for the style and display axes — the minimal set of knobs that enables meaningful variation across benchmark variants.

Knobs that don't produce variants worth benchmarking are cut. Knobs that always change together are collapsed into one.

---

## Guiding Principle: What Makes a Knob Worth Keeping

A knob earns its place if and only if two different values produce outputs with meaningfully different effects on agent behavior. Aesthetic variation is not a benchmark axis. Behavioral variation is.

The benchmark goal is: `agent_definitions × styles × displays = variants`. Each axis must be orthogonal and independently meaningful.

---

## Fixed Points (Not Knobs)

Before the design, establish what is NOT configurable:

- **frontmatter**: Machine-parsed YAML. YAML key names are dictated by the Claude Code agent spec. Not style knobs. The hook block structure is fixed. The only display choice is how to join the `tools` array in YAML — and that choice is trivially obvious (comma-separated inline) with no behavioral impact.
- **workspace_path on security_boundary**: Rendered as a fact in critical_rules, not in security_boundary body. Not a style knob.
- **output.format**: Pipeline control. Confirmed not agent-facing. Not rendered.
- **dispatcher section**: Fixed-structure rendering path, separate from the recipe. Not part of the style/display matrix. Its text slots are style knobs in a separate system.
- **invocation_display in writing_output**: Pre-composed data string. The container wraps it in a code fence; the fence language tag is the only knob.
- **example_display_headings**: Data field (Boolean on ExampleGroup). Data controls heading visibility; style controls the heading text. Style cannot override the data field's decision.

---

## Part 1: Universal Control Surfaces

Every agent-body section (identity through critical_rules) shares these controls.

### 1.1 Universal Section Container Interface

Every section container receives:
- `data`: the section's typed Pydantic model
- `style`: the section's style block
- `display`: the section's display block (optional — sections with no arrays have no display block)

The container produces a markdown string or empty string (when optional data is None).

### 1.2 Controls That Appear on Every Section

**heading** (style)
The text displayed as the section title. Every section has this. Range of values: the current heading text or a variant. Example variants for `instructions`: `"Processing"` / `"Instructions"` / `"Execution Steps"`.

**heading_level** (style)
H1, H2, or H3. Currently all body sections should be H2. Four sections (constraints, anti_patterns, success_criteria, failure_criteria) have H3 as a fossil. The knob allows benchmarking the fossil H3 against the corrected H2 — this has potential behavioral impact because heading level signals priority.

These are the only two controls that appear on every section. Nothing else is universal.

### 1.3 Controls That Appear on Most Sections (Not All)

**section_separator** (global, not per-section)
The horizontal rule (`---`) between sections. A single global knob, not per-section. Two meaningful variants: present or absent. Affects visual segmentation. Worth benchmarking.

**intro_prose** (style, on most sections)
Framing sentence before the main content. Some sections have it (security_boundary has preamble + grants_intro, input has parameters_intro, constraints has optional intro). Some sections have no meaningful intro (identity, examples). Not universal but common enough to note as a recurrent pattern. Each section's intro_prose is independently named in the style block.

---

## Part 2: Section-Specific Control Surfaces

The interesting design is here. Each section has a distinct data shape that creates distinct rendering challenges.

### 2.1 identity — The Role Template

**What makes identity unique**: `role_identity` is the only field in the entire system that is NEVER rendered standalone — it always goes into a sentence template. This template is the highest-behavioral-impact style knob in the system.

**Knobs that matter:**
```
role_identity_template   "You are a {role_identity}."
                         "You are an expert {role_identity}."
                         "Operating as a {role_identity}:"
```
This directly shapes how the agent models its identity. Worth benchmarking.

```
responsibility_label     "**Your responsibility:**"
                         "**Mission:**"
                         "" (no label — responsibility is a complete sentence)
```
Whether the responsibility sentence gets a label or stands alone changes emphasis.

```
expertise_label          "**Expertise:**"
                         "**Domain knowledge:**"
                         "" (no label)
```

**Not a knob**: `description_label`. The description renders as an unlabeled paragraph in the current design, and there is no evidence that labeling it produces a different behavioral outcome. Omit.

**Not a knob**: `model_display`. The model is in frontmatter. It should not render in identity prose. Fixed: omit.

**Display knob for identity:**
```
expertise_display        inline / bulleted
expertise_separator      ", " (only matters when inline)
```
Short expertise phrases render inline by default. A bulleted variant is worth testing — bullets signal items of equal weight.

**Cut**: No heading on identity. Identity is the lead section; the H1 heading IS the heading. The level (`heading_level`) suffices.

### 2.2 security_boundary — The Entry Template

**What makes security_boundary unique**: The entry template inverts the typical key:value pattern — tools act as the label, path is the value. This is the only compound per-item template in the system.

**Knobs that matter:**
```
preamble      "This agent operates under `bypassPermissions` with hook-based restrictions."
              "This agent uses hook-based path enforcement."
              (shorter variants)
```
The preamble crosses section boundaries: it references `permission_mode` from frontmatter. The template must embed this data value. The framing around it is the knob.

```
grants_intro  "The following operations are allowed — everything else is blocked by the system."
              "Allowed paths:"
              "" (no intro — jump straight to entries)
```

```
entry_template   "**{tools}:** `{path}`"
                 "`{path}` — {tools}"
                 "- {path}: {tools}"
```
The inverted template (tools as label) is the current design. The alternative (path first) is a legitimate behavioral hypothesis: does the agent scan by path or by tool when checking permissions?

```
boundary_warning   "Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."
                   "All other operations are blocked."
                   "" (omit — boundary already implied by the entries)
```

**Display knob:**
```
entries_display     sequential (current) — one entry per line, no blank lines
                    bulleted — each entry preceded by "- "
tools_separator     ", " (within entry_template)
```

**Cut**: `workspace_path_display`. workspace_path is rendered by critical_rules. Not rendered in security_boundary body. Fixed.

### 2.3 input — Context Display

**What makes input unique**: It has the most optional sub-blocks of any section. Parameters, context_required, context_available, input_schema — all optional. Each sub-block has its own intro label. The item templates for parameters and context items are compound (combining multiple fields).

**Knobs that matter:**
```
parameters_intro      "The dispatcher provides:"
                      "Parameters:"
                      "You receive:"
```

```
param_entry_template  "{param_name} ({param_type}): {param_description}"
                      "**{param_name}** ({param_type}) — {param_description}"
                      "`{param_name}` [{param_type}]: {param_description}"
```
How parameters are visually structured affects how the agent reads them.

```
context_required_label    "**Required context:**"
                          "Required context:"
                          "You must read:"
context_available_label   "**Available context:**"
                          "Available context:"
                          "You may read:"
```

```
context_entry_template    "**{context_label}:** `{context_path}`"
                          "- {context_label}: `{context_path}`"
```

```
optional_suffix     "(optional)" — appended to param_type for optional params
```

**Display knobs:**
```
parameters_display      bulleted (current)
                        numbered (implies ordered sequence)
context_display         bulleted (current)
```

**Cut**: `schema_intro` for input_schema. This field is not exercised in current agents. Define the label slot but no benchmark variant needed yet.

**Cut**: `delivery_display_map` and `format_display_map`. These enum-to-prose mappings change what words appear for `tempfile` → `"temporary file"` etc. This is cosmetic, not behavioral. The agent doesn't need a human-readable delivery label to function correctly. Omit from benchmark axes.

### 2.4 instructions — The Mode Boundary

**What makes instructions unique**: `instruction_mode` is a required field on every step that MUST be rendered. It is currently a bug (not rendered). The display format for mode is the primary benchmark axis of this section — arguably the highest-value display knob in the entire system.

**Knobs that matter (style):**
```
heading     "Processing" (current)
            "Instructions"
            "Execution Steps"
```
The heading itself is a behavioral signal. "Processing" frames steps as a process flow. "Instructions" is more authoritative. Worth benchmarking.

```
deterministic_marker   "[DETERMINISTIC]"
                       "Deterministic:"
                       "**[D]**"
                       "" (suppress — never correct for the rebuild)

probabilistic_marker   "[PROBABILISTIC]"
                       "Probabilistic:"
                       "**[P]**"
                       "" (suppress — never correct for the rebuild)
```

```
mode_label_position    prefix_line   — marker on its own line before step text
                       inline_prefix — marker on same line as step text, before it
                       badge         — bold badge inline ("**Deterministic:** {text}")
```
These three positions produce genuinely different LLM-visible structures. prefix_line makes mode the most prominent. inline_prefix attaches it to the step. badge embeds it as a semantic tag. All three are benchmark hypotheses.

**Display knobs:**
```
steps_display   numbered (1. 2. 3. — signals sequence)
                sequential (paragraphs — no sequence signal)
```
Whether steps are numbered affects whether the agent treats them as ordered obligations or as a set of independent guidelines. Numbered is strongly preferred for steps. The sequential variant (current bug behavior) is a baseline only.

**Cut**: `mode_grouping`. Grouping all deterministic steps together and all probabilistic steps together would reorder the steps, breaking procedural coherence. This is not a valid variant — it changes what the instructions mean. Not a knob.

**Cut**: `step_separator`. Blank line is the only sensible separator when using sequential mode. In numbered mode there is no separator question. Not a meaningful variant.

### 2.5 examples — Heading Hierarchy

**What makes examples unique**: It is the only section with a three-level heading hierarchy (section → group → entry). The group and entry heading levels are relative to the section heading, not absolute. `example_display_headings` is a per-group data toggle, not a style knob.

**Knobs that matter (style):**
```
heading              "Examples"
                     "Calibration Examples"
                     "Reference Examples"
```

```
group_heading_offset   +1 (group at section_level + 1, entries at section_level + 2)
                       +0 (group at same level as section — unusual)
```
The relative offset is cleaner than specifying absolute H3/H4 — it stays correct regardless of section heading_level. In practice this is almost always +1.

**Display knobs:**
```
entries_display   sequential (current — entries flow as text blocks)
                  numbered (entries are numbered when headings are off)
```
When `example_display_headings = false`, entries are just text blocks. The numbered variant signals that each entry is a distinct example.

**Cut**: `groups_display`. Groups are always sequential. Bulleted groups is nonsensical for blocks of content. Not a variant.

**Cut**: `max_number_truncation_signal`. Whether to signal truncation is a minor cosmetic decision. Not a behavioral benchmark axis.

### 2.6 output — Three Conditional Branches

**What makes output unique**: The `name_known` enum (known/partially/unknown) creates three structurally different outputs. The labels for each branch are distinct.

**Knobs that matter (style):**
```
schema_label       "**Schema:**"
                   "Schema:"
                   "Validates against:"

directory_label    "**Output directory:**"
                   "Output directory:"
                   "Write to:"

file_label         "**Output file:**"
                   "Output file:"
                   "Write to:"

name_instruction_label   "" (unlabeled — current)
                         "Naming:"
```

**Cut**: `format_display_map`. Output format is pipeline control. Not rendered. Not a knob.

**Cut**: `schema_embed_display`. The `schema_embed` Boolean on the data model controls whether the schema content is inlined. The style choice is whether to wrap the inlined content in a code fence. This is a structural formatting decision: yes or no. Not a meaningful benchmark axis.

**Cut**: `name_known_display`. Whether to render the `name_known` enum value directly (showing "partially" as text) serves no agent-facing purpose. The path labels implicitly communicate the naming situation. Not a knob.

No display knobs — output has no arrays.

### 2.7 writing_output — The Code Fence

**What makes writing_output unique**: The `invocation_display` field is a pre-composed string displayed verbatim. The section's only structural choices are the heading suffix and the code fence language tag.

**Knobs that matter (style):**
```
heading_suffix    "(MANDATORY)" (current — appended to heading)
                  "— Required"
                  "" (no suffix — heading alone)
```
Whether the heading signals mandatory status affects emphasis. "MANDATORY" is a strong signal. Worth benchmarking whether the signal adds value over the writing_output heading itself.

```
code_fence_lang   "" (no language tag — current)
                  "bash"
                  "shell"
```
Language tag affects syntax highlighting in renderers that apply it. Marginal behavioral impact. Include as a low-cost variant.

**Cut**: `preamble` for writing_output. There is no preamble before the code fence in the current design, and adding one would just be noise before the invocation pattern the agent needs to copy. Not worth benchmarking.

No display knobs — no arrays.

### 2.8 constraints and anti_patterns — Flat Lists

**What makes these unique**: Nothing. They are structurally identical: heading + flat list of StringProse sentences. They are the simplest sections in the system.

**Knobs that matter (style):**
```
heading     "Constraints" / "Rules" / "Behavioral Constraints"
            (anti_patterns): "Anti-Patterns" / "Common Mistakes" / "What To Avoid"
```
Whether the behavioral distinction between "constraint" (MUST/NEVER) and "anti-pattern" (common mistake) is reinforced by the heading is worth benchmarking.

**Display knobs:**
```
rules_display / patterns_display   bulleted (current)
                                   numbered (implies priority ordering)
```
Whether constraint rules are numbered changes whether the agent treats them as a priority-ordered list. This is a behavioral hypothesis.

**Cut**: `intro_prose` and `footer_prose` for both sections. The heading is sufficient framing. Adding prose before or after a list of complete sentences is noise. Not a knob.

**Collapsed**: constraints and anti_patterns share identical knob structure. The style block fields are named differently (`rules_display` vs `patterns_display`) but the design pattern is the same.

### 2.9 success_criteria and failure_criteria — Definition + Evidence Pairs

**What makes these unique**: Each criterion is a paired structure: definition sentence + evidence list. The asymmetric labeling (definition unlabeled, evidence labeled) is a current design choice that warrants benchmarking. The `Evidence:` label uses plain text while all other labels use bold — another asymmetry worth testing.

**Knobs that matter (style):**
```
heading    "Success Criteria" / "What Success Looks Like" / "Done When"
           (failure): "Failure Criteria" / "Process Failure" / "Failure Conditions"
```

```
definition_label   "" (unlabeled — current)
                   "**Success:**" / "**Failure:**"
```
Labeling the definition sentence changes whether it reads as a heading-like declaration or as an unlabeled block.

```
evidence_label   "Evidence:" (plain — current)
                 "**Evidence:**" (bold — consistent with other labels)
                 "Observable evidence:" (verbose)
```
The bold vs plain inconsistency in the current design is worth correcting. Benchmarking plain vs bold tests whether consistency matters.

**Display knobs:**
```
criteria_display     sequential (current — each criterion is a block)
                     numbered (for multiple criteria)

evidence_display     bulleted (current)
                     numbered (implies priority ordering)
```

**Collapsed**: success_criteria and failure_criteria share identical knob structure. Only the heading and definition_label differ between them.

### 2.10 return_format — Static Examples

**What makes return_format unique**: The `SUCCESS` and `FAILURE: <reason>` blocks inside the code fences are STATIC STYLE TEXT. They are not derived from data. The renderer constructs them from the mode value. This is the highest concentration of style-sourced content in any section other than critical_rules.

**Knobs that matter (style):**
```
success_label    "On success:"
                 "Success:"
                 "" (omit — code fence is self-evident)

failure_label    "On failure:"
                 "Failure:"
                 "" (omit)
```

```
success_example   "SUCCESS"
failure_example   "FAILURE: <reason>"
```
These should not be benchmarked — they are protocol tokens the dispatcher parses. Change them only if the protocol changes.

```
code_fence_lang   "" (current)
                  "bash"
```

**Cut**: `mode_display_map`. Whether the mode enum value renders in the section (as a label "Return mode: status") has no behavioral value. The instructions implicitly communicate the mode. Not a knob.

No display knobs — no arrays.

### 2.11 critical_rules — The Style-Heavy Section

**What makes critical_rules unique**: Almost all rendered content is STYLE CONTENT, not data. The data fields are conditional gates and interpolation values. The actual rule sentences live in the style TOML. This section is more a style template than a data container.

There are two independent conditional branches:
- `has_output_tool = false`: generic rules only
- `has_output_tool = true`: output-tool-specific rules + generic rules

**Style knobs that matter:**

Output-tool rule templates (interpolated):
```
output_tool_rule_template    "**Use {tool_name} for all output** — never write files directly, never use a different write tool"
                             "Use `{tool_name}` exclusively — do not invoke Write or Edit for output"
```

```
batch_discipline_rule_template   "**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)"
                                 "Write every {batch_size} records — batch size is a hard limit"
```

Static rules (no interpolation):
```
write_after_batch_rule   "**Write after every batch** — do not accumulate records in memory across batches"
fail_fast_rule           "**Fail fast** — if something is wrong, FAILURE immediately with clear reason"
stay_in_scope_rule       "**Stay in scope** — process only what you were given, nothing more"
no_invention_rule        "**No invention** — if the data doesn't support it, don't produce it"
```

Rule structure:
```
rule_label_bold   true (bold short label before em-dash — current)
                  false (flat sentence, no bold label)
rule_separator    " — " (em-dash with spaces — current)
                  ": " (colon)
```

The bold-label + em-dash + explanation structure is a style convention. Benchmarking flat sentences vs structured rules tests whether the formatting adds clarity.

**Display knob:**
```
rules_display   numbered (current — numbered list)
                bulleted (unordered)
```

**Not a knob**: The ordering of output-tool rules before generic rules. This is a fixed design decision. Mixing tool-specific and generic rules in a configurable order adds complexity with no behavioral hypothesis to test.

---

## Part 3: Style TOML Schema Design

### Shape

A style TOML has two top-level keys: `name` (string identifier) and the section blocks.

```toml
name = "default"

[identity]
heading_level    = "H1"
role_identity_template = "You are a {role_identity}."
responsibility_label = "**Your responsibility:**"
expertise_label  = "**Expertise:**"

[security_boundary]
heading          = "Security Boundary"
heading_level    = "H2"
preamble         = "This agent operates under `bypassPermissions` with hook-based restrictions."
grants_intro     = "The following operations are allowed — everything else is blocked by the system."
entry_template   = "**{tools}:** `{path}`"
boundary_warning = "Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."

[input]
heading               = "Input"
heading_level         = "H2"
parameters_intro      = "The dispatcher provides:"
param_entry_template  = "{param_name} ({param_type}): {param_description}"
optional_suffix       = "(optional)"
context_required_label = "**Required context:**"
context_available_label = "**Available context:**"

[instructions]
heading                  = "Processing"
heading_level            = "H2"
deterministic_marker     = "[DETERMINISTIC]"
probabilistic_marker     = "[PROBABILISTIC]"
mode_label_position      = "prefix_line"

[examples]
heading              = "Examples"
heading_level        = "H2"
group_heading_offset = 1

[output]
heading          = "Output"
heading_level    = "H2"
schema_label     = "**Schema:**"
directory_label  = "**Output directory:**"
file_label       = "**Output file:**"

[writing_output]
heading          = "Writing Output"
heading_level    = "H2"
heading_suffix   = "(MANDATORY)"
code_fence_lang  = ""

[constraints]
heading          = "Constraints"
heading_level    = "H2"

[anti_patterns]
heading          = "Anti-Patterns"
heading_level    = "H2"

[success_criteria]
heading            = "Success Criteria"
heading_level      = "H2"
definition_label   = ""
evidence_label     = "Evidence:"

[failure_criteria]
heading            = "Failure Criteria"
heading_level      = "H2"
definition_label   = ""
evidence_label     = "Evidence:"

[return_format]
heading          = "Return Format"
heading_level    = "H2"
success_label    = "On success:"
failure_label    = "On failure:"
success_example  = "SUCCESS"
failure_example  = "FAILURE: <reason>"
code_fence_lang  = ""

[critical_rules]
heading                      = "Critical Rules"
heading_level                = "H2"
output_tool_rule_template    = "**Use {tool_name} for all output** — never write files directly, never use a different write tool"
batch_discipline_rule_template = "**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)"
write_after_batch_rule       = "**Write after every batch** — do not accumulate records in memory across batches"
fail_fast_rule               = "**Fail fast** — if something is wrong, FAILURE immediately with clear reason"
stay_in_scope_rule           = "**Stay in scope** — process only what you were given, nothing more"
no_invention_rule            = "**No invention** — if the data doesn't support it, don't produce it"
rule_label_bold              = true
rule_separator               = " — "

[global]
section_separator = "---"
```

### Section Block Rules

1. Every section block uses the section's exact name from the data model (`identity`, `security_boundary`, `input`, etc.).
2. Section blocks are optional. When a block is absent, the container uses built-in defaults.
3. Individual fields within a block are optional. A partial block is valid — omitted fields fall back to defaults.
4. `heading_level` values are `"H1"`, `"H2"`, `"H3"` (strings, not integers).
5. Template fields use `{field_name}` syntax. Field names are the data model field names as they appear in the Pydantic models.

### Per-Style Files

A complete style file provides all section blocks. But style files are partial — only override what differs. Three initial style files:

**default.toml** — the current rendering behavior, corrected for fossils. H2 everywhere, mode markers active.

**strict.toml** — maximally authoritative. Numbered steps, bold evidence labels, no framing prose (headings only), numbered constraints. Hypothesis: stricter framing improves constraint adherence.

**concise.toml** — minimal framing. No boundary_warning, no grants_intro, no intro_prose on any section, shorter role_identity_template. Hypothesis: shorter prompts improve signal-to-noise.

---

## Part 4: Display TOML Schema Design

### Shape

A display TOML has one top-level key `name` and section blocks. Each section block names its array fields and assigns a display mode. Inline arrays additionally specify a separator. Structured arrays (items with multiple fields) use an item_template.

```toml
name = "standard"

[identity]
expertise = "inline"
expertise_separator = ", "

[security_boundary]
entries = "sequential"
entry_tools_separator = ", "

[input]
parameters = "bulleted"
context_required = "bulleted"
context_available = "bulleted"

[instructions]
steps = "numbered"

[examples]
entries = "sequential"

[constraints]
rules = "bulleted"

[anti_patterns]
patterns = "bulleted"

[success_criteria]
criteria = "sequential"
evidence = "bulleted"

[failure_criteria]
criteria = "sequential"
evidence = "bulleted"

[critical_rules]
rules = "numbered"
```

### Display Mode Definitions

| Mode | Behavior |
|------|----------|
| `bulleted` | Each item prefixed with `- ` |
| `numbered` | Each item prefixed with `{n}. ` |
| `sequential` | Items separated by blank lines, no list marker |
| `inline` | Items joined with separator string |

### Default Cascade

When a display TOML omits a section block or a field within a block, the container uses the built-in default for that array. The cascade is:

```
display TOML per-section value
  → built-in default for that array
```

There is no global display default in the TOML — every array has a hard-coded default in the container implementation that the display TOML overrides.

Built-in defaults by array type:
- `list[StringProse]` (constraints.rules, anti_patterns.patterns, evidence lists) → `bulleted`
- `list[InstructionStep]` (instructions.steps) → `numbered`
- `list[ExampleGroup]` or complex nested items → `sequential`
- `list[StringText]` (identity.expertise — short phrases) → `inline`

### Per-Display Files

Three initial display files:

**standard.toml** — the defaults above. Bulleted lists for rules/evidence, numbered instructions, inline expertise.

**numbered.toml** — all lists that are currently bulleted become numbered. Tests whether numbered constraints signal stronger priority ordering.

**compact.toml** — steps are `sequential` (no numbering, paragraphs only), constraints are `sequential` (long paragraphs not bulleted). Tests whether removing list structure changes agent parsing.

---

## Part 5: The Cut List

Fields inventoried but cut from the control surface:

| Field | Reason Cut |
|-------|-----------|
| `format_display_map` (input.format, output.format) | Pipeline enum values. output.format is not rendered. input.format appears only as data in delivery context. No behavioral impact from the label. |
| `delivery_display_map` (input.delivery) | Enum-to-prose mapping for `tempfile` etc. The agent knows it receives input through the dispatcher mechanism. Cosmetic. |
| `name_known_display` (output) | Whether to display the `name_known` enum value. The path labels communicate the naming situation implicitly. Redundant. |
| `schema_embed_display` (output) | Whether to wrap embedded schema in a code fence. Structural formatting only. Not behavioral. |
| `mode_grouping` (instructions) | Grouping deterministic/probabilistic steps would reorder them. Changes content meaning, not display format. Invalid as a display variant. |
| `step_separator` (instructions) | Blank line is the only sensible separator. Not meaningful. |
| `mode_display_map` (return_format) | Whether to render the mode enum ("status") as a label. No agent-facing value. |
| `workspace_path_display` (security_boundary) | workspace_path renders in critical_rules. Not a security_boundary display concern. |
| `max_number_truncation_signal` (examples) | Whether to note that examples were truncated. Cosmetic. |
| `rule ordering` (critical_rules) | Output-tool rules before generic rules is a fixed convention. Not a variant. |
| `description_label` (identity) | The description renders as an unlabeled paragraph. Adding a label produces no behavioral hypothesis worth testing. |
| `model_display` (identity) | Model is in frontmatter. Should not render in identity prose. Fixed: omit. |
| `preamble` (writing_output) | No preamble before the invocation display code fence. Noise before the pattern the agent copies. Not a knob. |

---

## Part 6: The Benchmark Matrix

With the above design:

**Style variants** (3):
- `default` — corrected fossils, mode markers active, H2 everywhere
- `strict` — numbered constraints, bold evidence, minimal prose framing
- `concise` — shorter templates, no warnings, no intro prose

**Display variants** (3):
- `standard` — bulleted rules, numbered steps, inline expertise
- `numbered` — numbered rules and evidence (everything that can be numbered, is)
- `compact` — sequential steps and rules (no list markers)

**Per definition**: 3 styles × 3 displays = 9 combinations per agent.

**Highest-impact benchmark axes** (by expected behavioral effect):
1. `steps_display`: numbered vs sequential — does numbering enforce step sequencing?
2. `mode_label_position` + `deterministic_marker`: where and how mode boundaries are marked
3. `role_identity_template`: "You are a" vs "As a" — identity framing
4. `heading_level` on constraints/anti_patterns: H2 vs H3 — does heading level affect adherence weight?
5. `rules_display`: bulleted vs numbered — does numbering signal priority order?

These five axes represent the core hypotheses. Everything else in the matrix is background variation that provides statistical coverage.

---

## Part 7: Cross-Section Data Threading

Two design decisions required by the control surface:

**security_boundary.preamble needs frontmatter.permission_mode**
The preamble template `"This agent operates under {permission_mode}..."` must reference data from a different section. Resolution: the composition engine passes `permission_mode` as an additional context value to the security_boundary container alongside its own data. Not a knob — an architectural requirement.

**critical_rules needs workspace_path from security_boundary**
The workspace confinement rule uses `workspace_path`. It lives on `SecurityBoundaryAnthropic`, not on `CriticalRules`. Resolution: the composition engine extracts `workspace_path` and passes it to the critical_rules container as an additional context value. This does not require a style knob — it is an injection step in the composition engine.

These cross-section references are fixed data dependencies, not style choices. The style TOML does not need to specify them.
