"""Reshape input section: rename param_* fields, extract context resources."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import ContextItem, Input, ParameterItem
from galdr.structures.template_context import ContextItemContext, InputContext, ParameterContext


def reshape_input(input_section: Input) -> InputContext:
    """Rename param_name/param_type/param_required to name/type/required."""
    params = None
    if input_section.parameters is not None:
        params = [reshape_param(param) for param in input_section.parameters.root]
    context_required = None
    context_available = None
    if input_section.context is not None:
        if input_section.context.context_required is not None:
            context_required = [reshape_context_item(item) for item in input_section.context.context_required.root]
        if input_section.context.context_available is not None:
            context_available = [reshape_context_item(item) for item in input_section.context.context_available.root]
    return InputContext(
        description=unwrap(input_section.description),
        format=unwrap(input_section.format),
        delivery=unwrap(input_section.delivery),
        input_schema=unwrap(input_section.input_schema) if input_section.input_schema else None,
        parameters=params,
        context_required=context_required,
        context_available=context_available,
    )


def reshape_param(param: ParameterItem) -> ParameterContext:
    """Reshape a single parameter item to template-friendly names."""
    return ParameterContext(
        name=unwrap(param.param_name),
        type=unwrap(param.param_type) if param.param_type else None,
        required=unwrap(param.param_required) if param.param_required else True,
        description=unwrap(param.param_description) if param.param_description else None,
    )


def reshape_context_item(context_item: ContextItem) -> ContextItemContext:
    """Rename context_label/context_path to label/path."""
    return ContextItemContext(
        label=unwrap(context_item.context_label),
        path=unwrap(context_item.context_path),
    )
