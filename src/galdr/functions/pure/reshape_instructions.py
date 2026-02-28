"""Reshape instructions section: rename instruction_* to template names."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import Instructions, InstructionStep
from galdr.structures.template_context import (
    InstructionStepContext,
    InstructionsContext,
)


def reshape_instructions(instructions: Instructions) -> InstructionsContext:
    """Rename instruction_mode/instruction_text to mode/text."""
    return InstructionsContext(
        steps=[reshape_step(step) for step in instructions.steps.root],
    )


def reshape_step(step: InstructionStep) -> InstructionStepContext:
    """Reshape a single instruction step."""
    return InstructionStepContext(
        mode=unwrap(step.instruction_mode),
        text=unwrap(step.instruction_text),
    )
