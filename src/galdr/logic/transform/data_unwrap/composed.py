"""Data unwrap composed — collect scalar strings from a section model.

CC=4-8. Iterates model fields with per-field unwrap attempts.
Pattern: draupnir/logic/transform/zone_collect/simple.build_zone_properties
(iterate dict, unwrap .root, collect into result dict).

Collects two kinds of values for template interpolation:
- String RootModels: unwrap to plain string via simple-level functions
- Enum fields: extract .value as string (mode names, format names)
"""

from pydantic import BaseModel, RootModel

from galdr.logic.transform.data_unwrap.simple import (
    unwrap_nested_string_root,
    unwrap_string_root,
)


def unwrap_section_data(section_model: BaseModel) -> dict[str, str]:
    """Extract all scalar string values from a data section model.

    Walks fields via Pydantic model iteration. For each non-None field:
    - RootModel → try direct string unwrap, then nested string unwrap
    - Enum-like (has .value str) → capture the enum value
    - Everything else (lists, nested models) → skip

    Returns a dict mapping field names to plain strings, suitable for
    {{field_name}} template interpolation.
    """
    values: dict[str, str] = {}
    for field_name, field_value in section_model:
        if field_value is None:
            continue
        if isinstance(field_value, RootModel):
            result = unwrap_string_root(field_value)
            if result is None:
                result = unwrap_nested_string_root(field_value)
            if result is not None:
                values[field_name] = result
        elif hasattr(field_value, "value") and isinstance(field_value.value, str):
            values[field_name] = field_value.value
    return values
