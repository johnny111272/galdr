"""Compose primitives — field name operations for trunk matching.

CC=1. Single expressions with known-typed string inputs.
Pattern: draupnir/logic/pure/graph_build/primitive.py — ref_prefix,
cache_key_to_defs_key (string partition/replace, no branching).

These support the trunk-matching mechanism: content field names like
'role_expertise_label' connect to data field 'role_expertise' and
display field 'role_expertise_format' via the shared trunk.
"""

def strip_suffix(name: str, suffix: str) -> str:
    """Remove a known suffix from a field name to get the trunk."""
    return name[: -len(suffix)]


def visibility_key(field_name: str) -> str:
    """Derive the structure visibility toggle name for a content field."""
    return field_name + "_visible"


def override_key(field_name: str) -> str:
    """Derive the structure override flag name for a data field."""
    return field_name + "_override"


def format_key(trunk: str) -> str:
    """Derive the display format field name for a data list."""
    return trunk + "_format"


def threshold_key(trunk: str) -> str:
    """Derive the display threshold field name for a format pair."""
    return trunk + "_format_threshold"
