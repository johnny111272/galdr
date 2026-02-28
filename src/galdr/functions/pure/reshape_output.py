"""Reshape output section: map output_file/output_directory to template field names."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import Output
from galdr.structures.template_context import OutputContext


def reshape_output(output: Output) -> OutputContext:
    """Map schema field names to template-friendly names.

    Schema uses output_file/output_directory; template uses file_path/directory_path.
    """
    return OutputContext(
        description=unwrap(output.description),
        format=unwrap(output.format),
        name_known=unwrap(output.name_known),
        name_instruction=unwrap(output.name_instruction) if output.name_instruction else None,
        schema_path=unwrap(output.schema_path) if output.schema_path else None,
        file_path=unwrap(output.output_file) if output.output_file else None,
        directory_path=unwrap(output.output_directory) if output.output_directory else None,
    )
