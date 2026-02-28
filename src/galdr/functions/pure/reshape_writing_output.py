"""Reshape writing output section: extract template-relevant fields."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import WritingOutputAnthropic
from galdr.structures.template_context import WritingOutputContext


def reshape_writing_output(writing_output: WritingOutputAnthropic) -> WritingOutputContext:
    """Extract invocation_display — the pre-composed display block from regin level 8."""
    return WritingOutputContext(
        invocation_display=unwrap(writing_output.invocation_display),
    )
