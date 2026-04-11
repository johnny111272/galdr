"""Preprocessing fields — structure-axis fields consumed before slot sorting.

Pre-processing fields control section-level behavior (skip section,
truncate list, select data variant, expand tier preset) and never
enter the bundling pipeline. Extracted once per section compose and
passed through as typed state.

Not every section has every field — each is Optional. Guardrails
family uses section_visible + max_entries_rendered. Identity uses
field_ordering. Instructions uses scaffolding_tier_override.
"""

from pydantic import BaseModel, ConfigDict


class PreprocessingFields(BaseModel):
    model_config = ConfigDict(frozen=True)
    section_visible: bool = True
    max_entries_rendered: int | None = None
    field_ordering: str | None = None
    scaffolding_tier_override: str | None = None
