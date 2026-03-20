"""Typed context models for the composition engine.

Each model represents exactly what its corresponding section renderer needs.
"""

from pydantic import BaseModel, ConfigDict


class HookContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    matcher: str
    command: str


class FrontmatterContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    description: str
    model: str
    permission_mode: str
    tools: str
    hooks: list[HookContext] | None = None


class IdentityContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str
    description: str
    role_identity: str | None = None
    role_description: str | None = None
    role_expertise: list[str] | None = None
    role_responsibility: str | None = None


class DisplayEntryContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    path: str
    tools: list[str]


class SecurityBoundaryContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    workspace_path: str
    has_grants: bool
    display: list[DisplayEntryContext]


class ParameterContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    type: str | None = None
    required: bool = True
    description: str | None = None


class ContextItemContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    label: str
    path: str


class InputContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    description: str
    format: str
    delivery: str
    input_schema: str | None = None
    parameters: list[ParameterContext] | None = None
    context_required: list[ContextItemContext] | None = None
    context_available: list[ContextItemContext] | None = None


class InstructionStepContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    mode: str
    text: str


class InstructionsContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    steps: list[InstructionStepContext]


class ExampleEntryContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    heading: str
    text: str


class ExampleGroupContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    group_name: str
    display_headings: bool
    max_entries: int | None = None
    entries: list[ExampleEntryContext]


class ExamplesContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    groups: list[ExampleGroupContext]


class OutputContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    description: str
    format: str
    name_known: str | None = None
    name_instruction: str | None = None
    schema_path: str | None = None
    file_path: str | None = None
    directory_path: str | None = None
    output_directory: str | None = None


class WritingOutputContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    invocation_display: str


class ConstraintsContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    rules: list[str]


class AntiPatternsContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    patterns: list[str]


class SuccessCriterionContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    definition: str
    evidence: list[str]


class FailureCriterionContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    definition: str
    evidence: list[str]


class ReturnFormatContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    mode: str
    status_instruction: str | None = None
    metrics_instruction: str | None = None
    output_instruction: str | None = None


class CriticalRulesContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    has_output_tool: bool
    tool_name: str | None = None
    batch_size: int | None = None


class DispatcherContext(BaseModel):
    """Dispatcher skill generation context — orchestration, batching, scope discovery."""

    model_config = ConfigDict(frozen=True)
    agent_name: str
    agent_description: str
    dispatch_mode: str
    background_mode: str
    input_format: str
    input_delivery: str
    input_description: str
    output_format: str
    output_name_known: str
    return_mode: str
    max_agents: int | None = None
    batch_size: list[int] | None = None
    parameters: list[ParameterContext] | None = None


class RenderContext(BaseModel):
    """Top-level container: the complete template context."""

    model_config = ConfigDict(frozen=True)
    frontmatter: FrontmatterContext
    identity: IdentityContext
    security_boundary: SecurityBoundaryContext | None = None
    input: InputContext
    instructions: InstructionsContext
    examples: ExamplesContext | None = None
    output: OutputContext
    writing_output: WritingOutputContext | None = None
    constraints: ConstraintsContext | None = None
    anti_patterns: AntiPatternsContext | None = None
    return_format: ReturnFormatContext
    success_criteria: list[SuccessCriterionContext] | None = None
    failure_criteria: list[FailureCriterionContext] | None = None
    critical_rules: CriticalRulesContext | None = None
    dispatcher: DispatcherContext | None = None
