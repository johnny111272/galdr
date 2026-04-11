"""Compose assembled — section composition wiring.

CC=1-2. Wires composed-level processors into a stage-1 section inspection.
One guard (data + content presence), then two composed calls: preprocessor
and slot sorter. Zero other decisions.

STAGE 1 ONLY. The hourglass pipeline has four stages (chunk, gather,
resolve+render, buffer). Only stage 1 is implemented. compose_section
returns the raw slot dict plus the extracted preprocessing fields for
inspection — no bundling, no resolution, no rendering.

The walker-based composition (populate_section_buffer, resolve_all_trunks,
render_buffer) has been disconnected. Those functions remain in composed.py
as orphaned code until their hourglass replacements land.
"""

from pydantic import BaseModel

from galdr.logic.pure.compose.composed import (
    extract_preprocessing_fields,
    sort_into_slots,
)
from galdr.structure.model.preprocessing_fields import PreprocessingFields


def compose_section(
    data_section: BaseModel,
    structure_section: BaseModel,
    content_section: BaseModel,
    display_section: BaseModel | None,
) -> tuple[PreprocessingFields, dict[str, list[tuple[str, str]]]]:
    """Run stage 1 of the hourglass pipeline for one section.

    Preprocessor extracts pre_* fields into a typed state. Slot sorter
    classifies every remaining field into heading/preamble/body/closing
    by terminal suffix. Returns both — preprocessor state and the raw
    slot dict — for inspection.

    The slot dict is intentionally untyped: the shape discovery is
    ongoing, so we don't commit to a Pydantic model until we know what
    a bundle actually contains.
    """
    pre_fields = extract_preprocessing_fields(structure_section)
    slots = sort_into_slots(content_section, data_section, structure_section, display_section)
    return pre_fields, slots
