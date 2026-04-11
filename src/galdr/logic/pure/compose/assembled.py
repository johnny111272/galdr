"""Compose assembled — section composition wiring.

CC=1-2. Wires composed-level processors into a complete section render.
One guard (section gate), then pure wiring calls. Zero other decisions.

Pattern: regin/logic/transform/section_regroup/assembled.py — regroup()
is CC=1, calls 12 functions, zero decisions.
"""

from pydantic import BaseModel

from galdr.logic.pure.compose.composed import (
    extract_preprocessing_fields,
    populate_section_buffer,
    resolve_all_trunks,
)
from galdr.logic.pure.compose.simple import (
    check_section_gate,
    render_buffer,
)
from galdr.structure.model.section_context import SectionContext


def compose_section(
    data_section: BaseModel,
    structure_section: BaseModel,
    content_section: BaseModel,
    display_section: BaseModel | None,
    data_values: dict[str, str],
) -> str | None:
    """Generic section composer. Data drives, content decorates.

    Extracts typed pre-processing fields, then populates a buffer with
    heading/preamble/postscript from content, fills body from the data
    walk, and renders the buffer in order. Returns the section as a
    markdown string, or None if gated off.
    """
    pre_fields = extract_preprocessing_fields(structure_section)
    if not check_section_gate(data_section, pre_fields.section_visible):
        return None
    section_context = SectionContext(
        content=content_section,
        structure=structure_section,
        display=display_section,
        data_values=data_values,
    )
    data_field_names = frozenset(data_section.model_fields.keys())
    buffer, consumed_variants = populate_section_buffer(content_section, data_field_names, structure_section, data_values)
    body = resolve_all_trunks(data_section, section_context, consumed_variants)
    filled = buffer.model_copy(update={"body": tuple(body)})
    return render_buffer(filled)
