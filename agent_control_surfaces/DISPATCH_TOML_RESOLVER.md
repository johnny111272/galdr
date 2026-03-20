# Dispatch Template: TOML Resolution

## How To Use This Template

For each section, dispatch ONE opus agent. Replace `{SECTION_NAME}` with the section name (e.g., IDENTITY, INPUT, CRITICAL_RULES). The agent reads the section synthesis and extracts TOML configuration for three files.

---

## Prompt Template

```
STRICT OPERATIONAL CONSTRAINT — READ THIS FIRST:
Your ONLY tool uses are:
1. Read the section synthesis file specified below
2. Write the output file
Do NOT read any other files. Do NOT search or grep the codebase.
Do NOT explore directories. Do NOT use Glob or Grep tools.

---

STEP 1: Read:
/Users/johnny/.ai/spaces/bragi/tools/galdr/agent_control_surfaces/{SECTION_NAME}.md

STEP 2: Write your extraction to:
/Users/johnny/.ai/spaces/bragi/tools/galdr/agent_control_surfaces/incremental_toml_resolution/{SECTION_NAME}.md

---

WHAT YOU ARE DOING:

You are extracting TOML configuration from a section synthesis document.
The synthesis describes fragments of an agent prompt section — prose,
templates, format choices, structural decisions. Your job is to sort
each fragment into one of three TOML files based on clear rules.

---

THE THREE FILES:

### structure.toml — [section_name]

Stable configuration. Shared across all variants. Never copied for experiments.

Contains:
- Visibility toggles (boolean: show/hide optional fragments)
- Structural variant selectors (e.g., field_ordering = "identity_first")
- Presentation paradigm selectors (e.g., context_entry_presentation = "list")

Does NOT contain prose, templates, or format enums.
A field goes here when it controls WHETHER something appears or
WHICH structural variant is used — not WHAT the text says.

### content.toml — [section_name]

The variant surface. What gets copied/overridden for behavioral experiments.

Contains:
- Text blobs — pure prose, no {{DATA}} references
- Template blobs — prose with {{DATA}} holes

Every field is a string. Empty string means "don't render this fragment."

### display.toml — [section_name]

Format selectors. Orthogonal to prose changes.

Contains:
- Format enums dispatching to renderer functions
- Threshold tuples for count-based format switching
- Joiner strings for array inline rendering

---

CRITICAL RULES FOR EXTRACTION:

1. FILTERING PRINCIPLE: If a fragment has no meaningful variation — if it
   is just rendering data as-is with no prose wrapping, no label, no
   framing — it does NOT get a TOML entry. The renderer just outputs the
   data. Only things that VARY are knobs.

2. INVARIANT RULES ARE CODE, NOT TOML:
   - Silence for absence (optional data absent → render nothing)
   - Boolean data gates (has_output_tool, context_required presence)
   - Heading levels (always H2 for sections, H3 for grouped children)
   - Embedded schema rendering (always json code fence)
   - Frontmatter delimiters (always ---)
   - Sub-block ordering when both analyses converged on one order
   These are baked into the renderer. Do NOT create TOML entries for them.

3. POSITION SIGNIFIERS ON FIELD NAMES: Every content field name must
   encode its position relative to the data it references. This is
   mandatory — LLMs editing these files pattern-match on names.

   The universal block assembly order is:
   heading → preamble → label → entries → postscript

   | Suffix      | Position     | Meaning                                    |
   |-------------|--------------|---------------------------------------------|
   | _heading    | First        | Names the block. Rendered as heading.       |
   | _preamble   | After heading| Sets context before data arrives.           |
   | _label      | Before data  | Immediately introduces a field or list.     |
   | (entries)   | Middle       | The data itself — no suffix needed.         |
   | _postscript | After data   | Reinforces or constrains what was presented.|
   | _transition | Between blocks| Marks cognitive shift to next block.       |

4. DESCRIPTIVE NAMES OVER SHORT NAMES: Each file is read in isolation.
   Field names must be self-documenting. Bad: "closer = false".
   Good: "closing_identity_reinforcement = false".

5. MATCHING NAMES ACROSS FILES: When structure.toml controls visibility
   of a content.toml fragment, use the same field name in both.
   Boolean in structure, string in content.

6. NO LIST MARKERS IN CONTENT: Bullet "- " or number "1. " prefixes
   belong to the display layer, not content. Content templates contain
   only the text/template for each item, not the list formatting.

7. NO HEADING LEVEL MARKERS IN CONTENT: Do not put "## " or "### " in
   content heading fields. Heading level is determined by the renderer
   based on whether the section is standalone (H2) or in a group (H3).
   Content heading fields contain only the heading TEXT.

8. THRESHOLD TUPLE NOTATION: Count-based format switches use:
   format_field = ["above_threshold_format", "at_or_below_format"]
   threshold_field = N
   Single format (no switch) is just a plain string: format_field = "bulleted"

9. DESCRIPTION FIELD: The description field from the data model is
   catalog metadata (for lookups, dispatch routing). It is NOT
   agent-facing content. Do not include it in identity or other
   agent-facing sections.

---

WORKED EXAMPLE A: IDENTITY

Input synthesis identified these fragments: heading, identity declaration,
role_description envelope, responsibility framing, expertise display,
negative boundary, section closer, model rendering (omit), field ordering.

Extraction:

### structure.toml — [identity]

```toml
[identity]
field_ordering = "identity_first"
fuse_declaration_and_role_description = false
expertise_scope_limitation = true
closing_identity_reinforcement = false
```

### content.toml — [identity]

```toml
[identity]
heading = "AGENT: {{title}}"
declaration = "You are a {{role_identity}}."
responsibility_label = "**Scope:** {{role_responsibility}}"
expertise_label = "**Your judgment is authoritative in:**"
expertise_postscript = "Your expertise is strictly limited to the areas listed above."
closing_identity_reinforcement = "Remember: you are a {{role_identity}}."
```

### display.toml — [identity]

```toml
[identity]
expertise_format = ["bulleted", "inline"]
expertise_threshold = 3
responsibility_format = ["bulleted", "prose"]
responsibility_threshold = 3
```

WHY these decisions:
- field_ordering in structure: structural variant (two Pydantic models)
- fuse_declaration_and_role_description in structure: boolean layout toggle
- expertise_scope_limitation / closing_identity_reinforcement: structure
  toggles matching content strings (same field name in both files)
- role_description NOT in content: no template needed, renderer outputs
  it directly (bare data, no prose wrapping)
- expertise items NOT in content: bare data, display handles formatting
- model NOT anywhere: invariant rule (always omit)
- "- " NOT in content templates: list markers belong to display layer
- No "## " in heading: renderer handles heading level

---

WORKED EXAMPLE B: INPUT

Input synthesis identified: heading, integrated description+format,
context_required block (heading, preamble, entries, transition),
parameters, completeness assertion, readiness checkpoint.

Extraction:

### structure.toml — [input]

```toml
[input]
input_completeness_assertion = true
readiness_checkpoint = true
context_entry_presentation = "list"
parameter_presentation = "list"
```

### content.toml — [input]

```toml
[input]
heading = "Input"
input_description = "Your input is a {{format}} file containing {{description}}."
context_required_heading = "Required Reading"
context_required_preamble = "These are not reference materials to consult during work. They are foundational knowledge you must absorb before starting."
context_entry = "**{{context_label}}**: Read `{{context_path}}`"
knowledge_data_transition = "With this knowledge internalized, here is your input data:"
input_completeness_postscript = "Your tempfile and required reading together constitute your complete input. Do not seek additional sources."
readiness_checkpoint_postscript = "Confirm you have: (1) your input data at the tempfile path, (2) knowledge from all required reading. Now proceed."
```

### display.toml — [input]

```toml
[input]
context_entry_format = ["numbered", "bulleted"]
context_entry_threshold = 4
parameter_format = ["bulleted", "prose"]
parameter_threshold = 2
```

WHY these decisions:
- input_completeness_assertion / readiness_checkpoint in structure:
  optional fragments not gated by data — genuine toggles
- context_entry_presentation / parameter_presentation in structure:
  paradigm selection (list vs table vs prose)
- Context-conditional fragments in content without structure toggles:
  renderer handles the data condition (context_required present/absent).
  Empty string in content = silence even when data would trigger rendering.
- Sub-block ordering NOT in TOML: converged (description → context →
  parameters), invariant, baked into renderer
- Delivery declaration NOT in TOML: invariant ("tempfile"), integrated
  into input_description template
- Parameter required/optional labels NOT in TOML: data-driven
  (show only when mix exists), invariant rule
- No "- " in context_entry: display layer handles list markers
- Position signifiers: _heading, _preamble, _postscript, _transition
  encode where each blob sits in the rendering sequence

---

OUTPUT FORMAT:

Write a markdown file with the section name as the title, followed by
three labeled TOML code blocks. After each block, include a brief
"WHY" section explaining key decisions (especially: why something was
excluded, why a field is in this file rather than another, any judgment
calls). Follow this structure exactly:

# {SECTION_NAME} — TOML Extraction

## structure.toml

```toml
[section_name]
field = value
```

**Decisions:**
- [Brief explanation of each field and key exclusions]

## content.toml

```toml
[section_name]
field = "value"
```

**Decisions:**
- [Brief explanation of position signifiers, template choices, exclusions]

## display.toml

```toml
[section_name]
field = value
```

**Decisions:**
- [Brief explanation of format choices and thresholds]

## Excluded (invariant rules / bare data)

- [List of fragments from the synthesis that were NOT extracted and why]
```

---

## Dispatch Checklist

1. Replace `{SECTION_NAME}` (all occurrences) with the section name in UPPER_CASE for file paths, lower_case for TOML section headers
2. Use `model: "opus"` for all dispatches
3. Use `subagent_type: "general-purpose"`
4. Verify output path: `agent_control_surfaces/incremental_toml_resolution/{SECTION_NAME}.md`
5. Do NOT dispatch FRONTMATTER or DISPATCHER — these are architectural outliers with different rendering patterns
