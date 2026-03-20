"""Tests for section renderers."""

from galdr.functions.pure.render_sections import (
    render_anti_patterns,
    render_constraints,
    render_critical_rules,
    render_examples,
    render_failure_criteria,
    render_frontmatter,
    render_identity,
    render_input,
    render_instructions,
    render_output,
    render_return_format,
    render_security_boundary,
    render_success_criteria,
    render_writing_output,
)
from galdr.structures.recipe import ModuleConfig
from galdr.structures.style import (
    AntiPatternsStyle,
    ConstraintsStyle,
    CriticalRulesStyle,
    ExamplesStyle,
    FailureCriteriaStyle,
    IdentityStyle,
    InputStyle,
    InstructionsStyle,
    OutputStyle,
    ReturnFormatStyle,
    SecurityBoundaryStyle,
    SuccessCriteriaStyle,
    WritingOutputStyle,
)
from galdr.structures.template_context import (
    AntiPatternsContext,
    ConstraintsContext,
    ContextItemContext,
    CriticalRulesContext,
    DisplayEntryContext,
    ExampleEntryContext,
    ExampleGroupContext,
    ExamplesContext,
    FailureCriterionContext,
    FrontmatterContext,
    HookContext,
    IdentityContext,
    InputContext,
    InstructionStepContext,
    InstructionsContext,
    OutputContext,
    ParameterContext,
    ReturnFormatContext,
    SecurityBoundaryContext,
    SuccessCriterionContext,
    WritingOutputContext,
)

DEFAULT_CONFIG = ModuleConfig(section="test")


# --- frontmatter ---


def test_render_frontmatter_without_hooks():
    data = FrontmatterContext(
        name="my-agent",
        description="Does things",
        model="opus",
        permission_mode="bypassPermissions",
        tools="Bash, Read, Write",
    )
    result = render_frontmatter(data)
    assert result.startswith("---\n")
    assert result.endswith("\n---")
    assert 'name: "my-agent"' in result
    assert 'permissionMode: "bypassPermissions"' in result
    assert "hooks:" not in result


def test_render_frontmatter_with_hooks():
    data = FrontmatterContext(
        name="my-agent",
        description="Does things",
        model="opus",
        permission_mode="bypassPermissions",
        tools="Bash, Read",
        hooks=[
            HookContext(matcher="Bash", command="/usr/bin/hook_validate"),
        ],
    )
    result = render_frontmatter(data)
    assert "hooks:" in result
    assert "PreToolUse:" in result
    assert "matcher: Bash" in result
    assert "command: /usr/bin/hook_validate" in result


# --- identity ---


def test_render_identity_all_fields():
    data = IdentityContext(
        title="Summary Writer",
        description="Writes summaries",
        role_identity="summary extraction specialist",
        role_description="You process interviews.",
        role_responsibility="Extract signal from noise",
        role_expertise=["NLP", "summarization"],
    )
    result = render_identity(data, IdentityStyle(), DEFAULT_CONFIG)
    assert result.startswith("# Summary Writer")
    assert "**Purpose:** Writes summaries" in result
    assert "You are a summary extraction specialist." in result
    assert "You process interviews." in result
    assert "**Your responsibility:** Extract signal from noise" in result
    assert "**Expertise:** NLP, summarization" in result


def test_render_identity_minimal():
    data = IdentityContext(title="Agent", description="Does work")
    result = render_identity(data, IdentityStyle(), DEFAULT_CONFIG)
    assert "# Agent" in result
    assert "**Purpose:** Does work" in result
    assert "You are a" not in result
    assert "responsibility" not in result


# --- security_boundary ---


def test_render_security_boundary():
    data = SecurityBoundaryContext(
        has_grants=True,
        display=[
            DisplayEntryContext(path="/some/path", tools=["Read", "Write"]),
            DisplayEntryContext(path="/other/path", tools=["Bash"]),
        ],
    )
    result = render_security_boundary(data, SecurityBoundaryStyle(), DEFAULT_CONFIG)
    assert "## Security Boundary" in result
    assert "**Read, Write:** `/some/path`" in result
    assert "**Bash:** `/other/path`" in result
    assert "bypassPermissions" in result


# --- input ---


def test_render_input_with_parameters():
    data = InputContext(
        description="JSONL records",
        format="jsonl",
        delivery="tempfile",
        parameters=[
            ParameterContext(name="tempfile", type="string", required=True, description="Path to input"),
            ParameterContext(name="mode", type="string", required=False),
        ],
    )
    result = render_input(data, InputStyle(), DEFAULT_CONFIG)
    assert "## Input" in result
    assert "JSONL records" in result
    assert "The dispatcher provides:" in result
    assert "- tempfile (string): Path to input" in result
    assert "- mode (string) (optional)" in result


def test_render_input_with_context():
    data = InputContext(
        description="Data",
        format="json",
        delivery="inline",
        context_required=[ContextItemContext(label="Schema", path="/schemas/test.json")],
        context_available=[ContextItemContext(label="Docs", path="/docs/guide.md")],
    )
    result = render_input(data, InputStyle(), DEFAULT_CONFIG)
    assert "**Required context:**" in result
    assert "**Schema:** `/schemas/test.json`" in result
    assert "**Available context:**" in result
    assert "**Docs:** `/docs/guide.md`" in result


def test_render_input_with_schema():
    data = InputContext(
        description="Data",
        format="json",
        delivery="inline",
        input_schema="/schemas/input.json",
    )
    result = render_input(data, InputStyle(), DEFAULT_CONFIG)
    assert "Input validates against: `/schemas/input.json`" in result


# --- instructions ---


def test_render_instructions():
    data = InstructionsContext(
        steps=[
            InstructionStepContext(mode="mandatory", text="Read the input file."),
            InstructionStepContext(mode="mandatory", text="Process each record."),
        ],
    )
    result = render_instructions(data, InstructionsStyle(), DEFAULT_CONFIG)
    assert "## Processing" in result
    assert "Read the input file." in result
    assert "Process each record." in result


# --- examples ---


def test_render_examples_with_headings():
    data = ExamplesContext(
        groups=[
            ExampleGroupContext(
                group_name="Basic",
                display_headings=True,
                entries=[
                    ExampleEntryContext(heading="Example 1", text="Content one"),
                    ExampleEntryContext(heading="Example 2", text="Content two"),
                ],
            ),
        ],
    )
    result = render_examples(data, ExamplesStyle(), DEFAULT_CONFIG)
    assert "## Examples" in result
    assert "### Basic" in result
    assert "#### Example 1" in result
    assert "Content one" in result
    assert "#### Example 2" in result


def test_render_examples_without_headings():
    data = ExamplesContext(
        groups=[
            ExampleGroupContext(
                group_name="Basic",
                display_headings=False,
                entries=[
                    ExampleEntryContext(heading="Example 1", text="Content one"),
                ],
            ),
        ],
    )
    result = render_examples(data, ExamplesStyle(), DEFAULT_CONFIG)
    assert "#### Example 1" not in result
    assert "Content one" in result


def test_render_examples_with_cap():
    data = ExamplesContext(
        groups=[
            ExampleGroupContext(
                group_name="Many",
                display_headings=False,
                entries=[
                    ExampleEntryContext(heading=f"Ex {idx}", text=f"Text {idx}")
                    for idx in range(5)
                ],
            ),
        ],
    )
    config = ModuleConfig(section="examples", max_entries=2)
    result = render_examples(data, ExamplesStyle(), config)
    assert "Text 0" in result
    assert "Text 1" in result
    assert "Text 2" not in result


def test_render_examples_data_cap():
    data = ExamplesContext(
        groups=[
            ExampleGroupContext(
                group_name="Group",
                display_headings=False,
                max_entries=1,
                entries=[
                    ExampleEntryContext(heading="A", text="First"),
                    ExampleEntryContext(heading="B", text="Second"),
                ],
            ),
        ],
    )
    result = render_examples(data, ExamplesStyle(), DEFAULT_CONFIG)
    assert "First" in result
    assert "Second" not in result


# --- output ---


def test_render_output_with_file():
    data = OutputContext(
        description="One JSONL file",
        format="jsonl",
        schema_path="/schemas/output.json",
        file_path="/output/results.jsonl",
    )
    result = render_output(data, OutputStyle(), DEFAULT_CONFIG)
    assert "## Output" in result
    assert "**Schema:** `/schemas/output.json`" in result
    assert "**Output file:** `/output/results.jsonl`" in result
    assert "One JSONL file" in result


def test_render_output_with_directory():
    data = OutputContext(
        description="Per-interview files",
        format="jsonl",
        directory_path="/output/interviews",
    )
    result = render_output(data, OutputStyle(), DEFAULT_CONFIG)
    assert "**Output directory:** `/output/interviews`" in result


def test_render_output_name_instruction():
    data = OutputContext(
        description="Files",
        format="json",
        name_known="unknown",
        name_instruction="Name files by their UID.",
    )
    result = render_output(data, OutputStyle(), DEFAULT_CONFIG)
    assert "Name files by their UID." in result


# --- writing_output ---


def test_render_writing_output():
    data = WritingOutputContext(invocation_display="append_records <<'EOF'\n{json_data}\nEOF")
    result = render_writing_output(data, WritingOutputStyle(), DEFAULT_CONFIG)
    assert "## Writing Output (MANDATORY)" in result
    assert "```\nappend_records <<'EOF'" in result


# --- constraints ---


def test_render_constraints():
    data = ConstraintsContext(rules=["Stay focused", "No hallucination"])
    result = render_constraints(data, ConstraintsStyle(), DEFAULT_CONFIG)
    assert "### Constraints" in result
    assert "- Stay focused" in result
    assert "- No hallucination" in result


def test_render_constraints_with_framing():
    data = ConstraintsContext(rules=["Rule one"])
    style = ConstraintsStyle(framing="You must stay within these boundaries:")
    config = ModuleConfig(section="constraints", framing=True)
    result = render_constraints(data, style, config)
    assert "You must stay within these boundaries:" in result
    assert "- Rule one" in result


# --- anti_patterns ---


def test_render_anti_patterns():
    data = AntiPatternsContext(patterns=["Verbosity", "Hallucination"])
    result = render_anti_patterns(data, AntiPatternsStyle(), DEFAULT_CONFIG)
    assert "### Anti-Patterns" in result
    assert "- Verbosity" in result


# --- success_criteria ---


def test_render_success_criteria():
    data = [
        SuccessCriterionContext(
            definition="All records processed",
            evidence=["Output file exists", "Record count matches"],
        ),
    ]
    result = render_success_criteria(data, SuccessCriteriaStyle(), DEFAULT_CONFIG)
    assert "### Success Criteria" in result
    assert "All records processed" in result
    assert "Evidence:" in result
    assert "- Output file exists" in result
    assert "- Record count matches" in result


def test_render_success_criteria_empty():
    result = render_success_criteria([], SuccessCriteriaStyle(), DEFAULT_CONFIG)
    assert result == ""


# --- failure_criteria ---


def test_render_failure_criteria():
    data = [
        FailureCriterionContext(
            definition="Schema validation fails",
            evidence=["Invalid JSON", "Missing required field"],
        ),
    ]
    result = render_failure_criteria(data, FailureCriteriaStyle(), DEFAULT_CONFIG)
    assert "### Failure Criteria" in result
    assert "Schema validation fails" in result
    assert "- Invalid JSON" in result


# --- return_format ---


def test_render_return_format_with_status():
    data = ReturnFormatContext(
        mode="status",
        status_instruction="Return SUCCESS or FAILURE.",
    )
    result = render_return_format(data, ReturnFormatStyle(), DEFAULT_CONFIG)
    assert "## Return Format" in result
    assert "On success:" in result
    assert "SUCCESS" in result
    assert "On failure:" in result
    assert "FAILURE: <reason>" in result
    assert "Return SUCCESS or FAILURE." in result


def test_render_return_format_status_metrics():
    data = ReturnFormatContext(
        mode="status-metrics",
        metrics_instruction="Include record counts.",
    )
    result = render_return_format(data, ReturnFormatStyle(), DEFAULT_CONFIG)
    assert "On success:" in result
    assert "Include record counts." in result


def test_render_return_format_no_status():
    data = ReturnFormatContext(
        mode="output",
        output_instruction="Return the processed data.",
    )
    result = render_return_format(data, ReturnFormatStyle(), DEFAULT_CONFIG)
    assert "On success:" not in result
    assert "Return the processed data." in result


# --- critical_rules ---


def test_render_critical_rules_with_tool_and_batch():
    data = CriticalRulesContext(
        has_output_tool=True,
        tool_name="append_records",
        batch_size=20,
    )
    result = render_critical_rules(data, CriticalRulesStyle(), DEFAULT_CONFIG)
    assert "## Critical Rules" in result
    assert "1. **Use append_records for all output**" in result
    assert "2. **Batch discipline** — process exactly 20 records" in result
    assert "3. **Write after every batch**" in result
    assert "4. **Fail fast**" in result
    assert "5. **Stay in scope**" in result
    assert "6. **No invention**" in result


def test_render_critical_rules_with_tool_no_batch():
    data = CriticalRulesContext(
        has_output_tool=True,
        tool_name="write_output",
    )
    result = render_critical_rules(data, CriticalRulesStyle(), DEFAULT_CONFIG)
    assert "1. **Use write_output for all output**" in result
    assert "2. **Validate before returning**" in result
    assert "3. **Fail fast**" in result
    assert "Batch discipline" not in result


def test_render_critical_rules_no_tool():
    data = CriticalRulesContext(has_output_tool=False)
    result = render_critical_rules(data, CriticalRulesStyle(), DEFAULT_CONFIG)
    assert "1. **Fail fast**" in result
    assert "2. **Stay in scope**" in result
    assert "3. **No invention**" in result
    assert "Use " not in result


# --- variant dispatch ---


def test_render_constraints_numbered():
    data = ConstraintsContext(rules=["Stay focused", "No hallucination"])
    config = ModuleConfig(section="constraints", variant="numbered")
    result = render_constraints(data, ConstraintsStyle(), config)
    assert "1. Stay focused" in result
    assert "2. No hallucination" in result
    assert "- " not in result


def test_render_constraints_prose():
    data = ConstraintsContext(rules=["Stay focused", "No hallucination"])
    config = ModuleConfig(section="constraints", variant="prose")
    result = render_constraints(data, ConstraintsStyle(), config)
    assert "Stay focused." in result
    assert "No hallucination." in result
    assert "- " not in result
    assert "1." not in result


def test_render_anti_patterns_numbered():
    data = AntiPatternsContext(patterns=["Verbosity", "Hallucination"])
    config = ModuleConfig(section="anti_patterns", variant="numbered")
    result = render_anti_patterns(data, AntiPatternsStyle(), config)
    assert "1. Verbosity" in result
    assert "2. Hallucination" in result


def test_render_critical_rules_bullets():
    data = CriticalRulesContext(has_output_tool=False)
    config = ModuleConfig(section="critical_rules", variant="bullets")
    result = render_critical_rules(data, CriticalRulesStyle(), config)
    assert "- **Fail fast**" in result
    assert "- **Stay in scope**" in result
    assert "1." not in result


def test_render_instructions_numbered():
    data = InstructionsContext(
        steps=[
            InstructionStepContext(mode="mandatory", text="Read the input file."),
            InstructionStepContext(mode="mandatory", text="Process each record."),
        ],
    )
    config = ModuleConfig(section="instructions", variant="numbered")
    result = render_instructions(data, InstructionsStyle(), config)
    assert "1. Read the input file." in result
    assert "2. Process each record." in result


def test_render_success_criteria_compact():
    data = [
        SuccessCriterionContext(
            definition="All records processed",
            evidence=["Output file exists", "Record count matches"],
        ),
        SuccessCriterionContext(
            definition="Schema valid",
            evidence=["No validation errors"],
        ),
    ]
    config = ModuleConfig(section="success_criteria", variant="compact")
    result = render_success_criteria(data, SuccessCriteriaStyle(), config)
    assert "- All records processed" in result
    assert "- Schema valid" in result
    assert "Evidence:" not in result
    assert "Output file exists" not in result


def test_render_failure_criteria_compact():
    data = [
        FailureCriterionContext(
            definition="Schema validation fails",
            evidence=["Invalid JSON", "Missing required field"],
        ),
    ]
    config = ModuleConfig(section="failure_criteria", variant="compact")
    result = render_failure_criteria(data, FailureCriteriaStyle(), config)
    assert "- Schema validation fails" in result
    assert "Evidence:" not in result
    assert "Invalid JSON" not in result


# --- field selection ---


def test_render_identity_field_selection():
    data = IdentityContext(
        title="Summary Writer",
        description="Writes summaries",
        role_identity="summary extraction specialist",
        role_description="You process interviews.",
        role_responsibility="Extract signal from noise",
        role_expertise=["NLP", "summarization"],
    )
    config = ModuleConfig(section="identity", fields=["title", "description"])
    result = render_identity(data, IdentityStyle(), config)
    assert "# Summary Writer" in result
    assert "**Purpose:** Writes summaries" in result
    assert "summary extraction specialist" not in result
    assert "You process interviews." not in result
    assert "responsibility" not in result
    assert "Expertise" not in result
