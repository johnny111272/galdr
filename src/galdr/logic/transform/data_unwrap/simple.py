"""Data unwrap simple — per-shape RootModel string extraction.

CC=1-3. Each function handles one RootModel shape. Callers at
composed level use these to peel wrapper layers before collecting
values for template interpolation.

Pattern: draupnir/logic/transform/unwrap/simple.py — one function
per shape, None guard first, known types throughout.
"""

from pydantic import RootModel


def unwrap_string_root(field_value: RootModel) -> str | None:
    """Extract .root from a RootModel[str]. Returns None if root is not a string.

    For fields like RoleResponsibility(RootModel[str]) where .root
    is the prose string directly.
    """
    return field_value.root if isinstance(field_value.root, str) else None


def unwrap_nested_string_root(field_value: RootModel) -> str | None:
    """Extract .root.root from RootModel[RootModel[str]]. Returns None if chain breaks.

    For fields like AgentTitle(RootModel[TitleString]) where TitleString
    is itself RootModel[str]. Peels two layers.
    """
    inner = field_value.root
    return inner.root if isinstance(inner, RootModel) and isinstance(inner.root, str) else None
