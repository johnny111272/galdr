"""Tests for the composition engine."""

from galdr.functions.pure.compose import (
    compose_agent,
    compose_dispatcher,
    reshape_style_toml,
    validate_section_names,
    validate_style_sections,
)
from galdr.functions.pure.defaults import default_recipe, default_style
from galdr.structures.recipe import ModuleConfig, RecipeConfig
from galdr.structures.style import ConstraintsStyle, InputStyle, SectionStyle, StyleConfig
from galdr.structures.template_context import (
    ConstraintsContext,
    CriticalRulesContext,
    DispatcherContext,
    ExampleEntryContext,
    ExampleGroupContext,
    ExamplesContext,
    FailureCriterionContext,
    FrontmatterContext,
    IdentityContext,
    InputContext,
    InstructionsContext,
    InstructionStepContext,
    OutputContext,
    ParameterContext,
    RenderContext,
    ReturnFormatContext,
    SecurityBoundaryContext,
    DisplayEntryContext,
    SuccessCriterionContext,
    WritingOutputContext,
)


def make_minimal_context(**overrides) -> RenderContext:
    """Build a RenderContext with only required fields."""
    defaults = dict(
        frontmatter=FrontmatterContext(
            name="test-agent",
            description="Test agent",
            model="opus",
            permission_mode="bypassPermissions",
            tools="Bash, Read",
        ),
        identity=IdentityContext(title="Test Agent", description="Does testing"),
        input=InputContext(description="Test input", format="jsonl", delivery="tempfile"),
        instructions=InstructionsContext(
            steps=[InstructionStepContext(mode="mandatory", text="Do the thing.")]
        ),
        output=OutputContext(description="Test output", format="jsonl"),
        return_format=ReturnFormatContext(mode="status"),
    )
    defaults.update(overrides)
    return RenderContext(**defaults)


# --- compose_agent ---


def test_compose_agent_minimal():
    context = make_minimal_context()
    result = compose_agent(context, default_recipe(), default_style())
    assert result.startswith("---\n")
    assert "# Test Agent" in result
    assert "Do the thing." in result
    assert "SUCCESS" in result


def test_compose_agent_no_separator_between_frontmatter_and_identity():
    context = make_minimal_context()
    result = compose_agent(context, default_recipe(), default_style())
    frontmatter_end = result.index("---\n", 4)
    after_frontmatter = result[frontmatter_end + 4 :]
    assert not after_frontmatter.startswith("---"), "No --- separator between frontmatter and identity"
    assert after_frontmatter.startswith("\n# Test Agent")


def test_compose_agent_separator_between_body_sections():
    context = make_minimal_context()
    result = compose_agent(context, default_recipe(), default_style())
    assert "\n\n---\n\n## Input" in result or "\n\n---\n\n## Processing" in result


def test_compose_agent_skips_none_sections():
    context = make_minimal_context()
    result = compose_agent(context, default_recipe(), default_style())
    assert "Security Boundary" not in result
    assert "Examples" not in result
    assert "Writing Output" not in result
    assert "Constraints" not in result
    assert "Anti-Patterns" not in result
    assert "Critical Rules" not in result


def test_compose_agent_includes_optional_sections():
    context = make_minimal_context(
        constraints=ConstraintsContext(rules=["Stay focused"]),
        examples=ExamplesContext(
            groups=[
                ExampleGroupContext(
                    group_name="Basic",
                    display_headings=False,
                    entries=[ExampleEntryContext(heading="Ex1", text="Example content")],
                )
            ]
        ),
        critical_rules=CriticalRulesContext(has_output_tool=False),
    )
    result = compose_agent(context, default_recipe(), default_style())
    assert "Stay focused" in result
    assert "Example content" in result
    assert "Fail fast" in result


def test_compose_agent_security_boundary_skipped_without_grants():
    context = make_minimal_context(
        security_boundary=SecurityBoundaryContext(has_grants=False, display=[])
    )
    result = compose_agent(context, default_recipe(), default_style())
    assert "Security Boundary" not in result


def test_compose_agent_security_boundary_included_with_grants():
    context = make_minimal_context(
        security_boundary=SecurityBoundaryContext(
            has_grants=True,
            display=[DisplayEntryContext(path="/some/path", tools=["Read"])],
        )
    )
    result = compose_agent(context, default_recipe(), default_style())
    assert "Security Boundary" in result
    assert "/some/path" in result


def test_compose_agent_empty_criteria_skipped():
    context = make_minimal_context(
        return_format=ReturnFormatContext(
            mode="status", success_criteria=[], failure_criteria=[]
        )
    )
    result = compose_agent(context, default_recipe(), default_style())
    assert "Success Criteria" not in result
    assert "Failure Criteria" not in result


def test_compose_agent_criteria_included():
    context = make_minimal_context(
        return_format=ReturnFormatContext(
            mode="status",
            success_criteria=[
                SuccessCriterionContext(
                    definition="All done", evidence=["Output exists"]
                )
            ],
            failure_criteria=[
                FailureCriterionContext(
                    definition="Bad data", evidence=["Schema error"]
                )
            ],
        )
    )
    result = compose_agent(context, default_recipe(), default_style())
    assert "### Success Criteria" in result
    assert "All done" in result
    assert "### Failure Criteria" in result
    assert "Bad data" in result


def test_compose_agent_custom_recipe_order():
    recipe = RecipeConfig(
        name="reordered",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="identity"),
            ModuleConfig(section="output"),
            ModuleConfig(section="input"),
            ModuleConfig(section="instructions"),
            ModuleConfig(section="return_format"),
        ],
    )
    context = make_minimal_context()
    result = compose_agent(context, recipe, default_style())
    output_pos = result.index("## Output")
    input_pos = result.index("## Input")
    assert output_pos < input_pos, "Output should appear before Input in reordered recipe"


def test_compose_agent_recipe_skip_module():
    recipe = RecipeConfig(
        name="minimal",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="identity"),
            ModuleConfig(section="return_format"),
        ],
    )
    context = make_minimal_context()
    result = compose_agent(context, recipe, default_style())
    assert "# Test Agent" in result
    assert "## Input" not in result
    assert "## Processing" not in result
    assert "## Output" not in result


# --- compose_dispatcher ---


def make_dispatcher_context(**dispatcher_overrides) -> RenderContext:
    """Build a RenderContext with dispatcher for testing."""
    dispatcher_defaults = dict(
        agent_name="test-agent",
        agent_description="Test agent description",
        dispatch_mode="full",
        background_mode="foreground",
        input_format="jsonl",
        input_delivery="tempfile",
        input_description="Test input",
        output_format="jsonl",
        output_name_known="known",
        return_mode="status",
    )
    dispatcher_defaults.update(dispatcher_overrides)

    return make_minimal_context(
        dispatcher=DispatcherContext(**dispatcher_defaults),
        input=InputContext(
            description="Test input",
            format="jsonl",
            delivery="tempfile",
            input_schema="/schemas/input.json",
        ),
        output=OutputContext(
            description="Test output",
            format="jsonl",
            schema_path="/schemas/output.json",
            file_path="/output/results.jsonl",
        ),
    )


def test_compose_dispatcher_full_mode():
    context = make_dispatcher_context()
    result = compose_dispatcher(context)
    assert "# Dispatch: Test Agent" in result
    assert "**Execution: FULL" in result
    assert "Batch Splitting" not in result


def test_compose_dispatcher_batch_mode():
    context = make_dispatcher_context(
        dispatch_mode="batch", batch_size=[20, 50]
    )
    result = compose_dispatcher(context)
    assert "**Execution: BATCH" in result
    assert "## Batch Splitting" in result
    assert "split_jsonl_batches" in result
    assert "--min-batch 20 --max-batch 50" in result


def test_compose_dispatcher_paths_table():
    context = make_dispatcher_context()
    result = compose_dispatcher(context)
    assert "## Paths" in result
    assert "| Input schema | `/schemas/input.json` |" in result
    assert "| Output schema | `/schemas/output.json` |" in result
    assert "| Output file | `/output/results.jsonl` |" in result


def test_compose_dispatcher_with_parameters():
    context = make_dispatcher_context(
        parameters=[
            ParameterContext(name="tempfile", type="string", required=True),
            ParameterContext(name="mode", type="string", required=False),
        ]
    )
    result = compose_dispatcher(context)
    assert 'argument-hint: "tempfile mode"' in result
    assert "`mode`" in result


def test_compose_dispatcher_no_dispatcher():
    context = make_minimal_context()
    result = compose_dispatcher(context)
    assert result == ""


def test_compose_dispatcher_frontmatter():
    context = make_dispatcher_context()
    result = compose_dispatcher(context)
    assert result.startswith("---\n")
    assert "name: dispatch-test-agent" in result
    assert "disable-model-invocation: true" in result


def test_compose_dispatcher_rules():
    context = make_dispatcher_context()
    result = compose_dispatcher(context)
    assert "## Rules" in result
    assert "Task prompt is thin" in result
    assert "Foreground parallel" in result


# --- validate_section_names ---


def test_validate_section_names_all_valid():
    recipe = RecipeConfig(
        name="valid",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="identity"),
            ModuleConfig(section="input"),
            ModuleConfig(section="instructions"),
            ModuleConfig(section="examples"),
            ModuleConfig(section="output"),
            ModuleConfig(section="writing_output"),
            ModuleConfig(section="constraints"),
            ModuleConfig(section="anti_patterns"),
            ModuleConfig(section="success_criteria"),
            ModuleConfig(section="failure_criteria"),
            ModuleConfig(section="return_format"),
            ModuleConfig(section="critical_rules"),
            ModuleConfig(section="security_boundary"),
        ],
    )
    assert validate_section_names(recipe) == []


def test_validate_section_names_unknown():
    recipe = RecipeConfig(
        name="typo",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="constrants"),
            ModuleConfig(section="identiy"),
        ],
    )
    unknown = validate_section_names(recipe)
    assert "constrants" in unknown
    assert "identiy" in unknown
    assert len(unknown) == 2


# --- reshape_style_toml ---


def test_reshape_style_toml():
    flat = {
        "name": "test",
        "input": {"heading": "Input"},
        "constraints": {"heading": "Rules", "framing": "Stay focused:"},
    }
    result = reshape_style_toml(flat)
    assert result["name"] == "test"
    assert "input" in result["sections"]
    assert result["sections"]["constraints"]["heading"] == "Rules"


def test_reshape_style_toml_no_sections():
    flat = {"name": "empty"}
    result = reshape_style_toml(flat)
    assert result["name"] == "empty"
    assert result["sections"] == {}


# --- validate_style_sections ---


def test_validate_style_sections_valid():
    style = StyleConfig(
        name="test",
        sections={
            "input": InputStyle(),
            "constraints": ConstraintsStyle(heading="Rules"),
        },
    )
    assert validate_style_sections(style) == []


def test_compose_agent_variant_recipe():
    """A recipe with variant='numbered' on constraints produces numbered output."""
    context = make_minimal_context(
        constraints=ConstraintsContext(rules=["Stay focused", "No hallucination"]),
    )
    numbered_recipe = RecipeConfig(
        name="numbered-test",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="identity"),
            ModuleConfig(section="input"),
            ModuleConfig(section="instructions"),
            ModuleConfig(section="constraints", variant="numbered"),
            ModuleConfig(section="output"),
            ModuleConfig(section="return_format"),
        ],
    )
    default_result = compose_agent(context, default_recipe(), default_style())
    variant_result = compose_agent(context, numbered_recipe, default_style())
    assert "- Stay focused" in default_result
    assert "1. Stay focused" in variant_result
    assert "- Stay focused" not in variant_result


def test_validate_style_sections_unknown():
    style = StyleConfig(
        name="test",
        sections={
            "input": InputStyle(),
            "constrants": ConstraintsStyle(heading="Rules"),
        },
    )
    unknown = validate_style_sections(style)
    assert "constrants" in unknown
    assert len(unknown) == 1
