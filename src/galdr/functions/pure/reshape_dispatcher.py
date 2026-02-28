"""Reshape dispatcher section: extract dispatch config for skill generation."""

from galdr.functions.pure.reshape_input import reshape_param
from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import Dispatcher
from galdr.structures.template_context import DispatcherContext


def reshape_dispatcher(dispatcher: Dispatcher) -> DispatcherContext:
    """Map Dispatcher schema model to template-friendly DispatcherContext."""
    parameters = None
    if dispatcher.parameters is not None:
        parameters = [reshape_param(param) for param in dispatcher.parameters.root]

    batch_size = None
    if dispatcher.batch_size is not None:
        batch_size = [unwrap(value) for value in dispatcher.batch_size.root]

    return DispatcherContext(
        agent_name=unwrap(dispatcher.agent_name),
        agent_description=unwrap(dispatcher.agent_description),
        dispatch_mode=unwrap(dispatcher.dispatch_mode),
        background_mode=unwrap(dispatcher.background_mode),
        input_format=unwrap(dispatcher.input_format),
        input_delivery=unwrap(dispatcher.input_delivery),
        input_description=unwrap(dispatcher.input_description),
        output_format=unwrap(dispatcher.output_format),
        output_name_known=unwrap(dispatcher.output_name_known),
        return_mode=unwrap(dispatcher.return_mode),
        max_agents=unwrap(dispatcher.max_agents) if dispatcher.max_agents is not None else None,
        batch_size=batch_size,
        parameters=parameters,
    )
