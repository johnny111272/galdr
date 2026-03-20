"""Build template context from validated anthropic render data.

Each section is reshaped by an explicit function that maps schema model
fields to template context fields. No silent field dropping — every
field selection is visible in the reshape function.
"""

from galdr.functions.pure.reshape_critical_rules import reshape_critical_rules
from galdr.functions.pure.reshape_dispatcher import reshape_dispatcher
from galdr.functions.pure.reshape_examples import reshape_examples
from galdr.functions.pure.reshape_frontmatter import reshape_frontmatter
from galdr.functions.pure.reshape_guardrails import reshape_anti_patterns, reshape_constraints
from galdr.functions.pure.reshape_identity import reshape_identity
from galdr.functions.pure.reshape_input import reshape_input
from galdr.functions.pure.reshape_instructions import reshape_instructions
from galdr.functions.pure.reshape_output import reshape_output
from galdr.functions.pure.reshape_return_format import (
    reshape_failure_criteria,
    reshape_return_format,
    reshape_success_criteria,
)
from galdr.functions.pure.reshape_security_boundary import reshape_security_boundary
from galdr.functions.pure.reshape_writing_output import reshape_writing_output
from galdr.structures.anthropic_render import AgentAnthropicRender
from galdr.structures.template_context import RenderContext


def build_render_context(json_data: str) -> RenderContext:
    """Parse gate JSON into a typed template context."""
    model = AgentAnthropicRender.model_validate_json(json_data)
    return RenderContext(
        frontmatter=reshape_frontmatter(model.frontmatter),
        identity=reshape_identity(model.identity),
        security_boundary=reshape_security_boundary(model.security_boundary) if model.security_boundary else None,
        input=reshape_input(model.input),
        instructions=reshape_instructions(model.instructions),
        examples=reshape_examples(model.examples),
        output=reshape_output(model.output),
        writing_output=reshape_writing_output(model.writing_output) if model.writing_output else None,
        constraints=reshape_constraints(model.constraints) if model.constraints else None,
        anti_patterns=reshape_anti_patterns(model.anti_patterns) if model.anti_patterns else None,
        return_format=reshape_return_format(model.return_format),
        success_criteria=reshape_success_criteria(model.success_criteria) if model.success_criteria else None,
        failure_criteria=reshape_failure_criteria(model.failure_criteria) if model.failure_criteria else None,
        critical_rules=reshape_critical_rules(model.critical_rules) if model.critical_rules else None,
        dispatcher=reshape_dispatcher(model.dispatcher) if model.dispatcher else None,
    )
