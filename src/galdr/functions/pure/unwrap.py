"""Unwrap RootModel and enum values to plain Python types.

Schema models produced by datamodel-codegen nest RootModel wrappers
(e.g., AgentTitle → TitleString → str). This utility recursively
unwraps to the innermost scalar value.
"""

from enum import Enum

from pydantic import RootModel


def unwrap(value: RootModel | Enum | str | int | bool) -> str | int | bool:
    """Recursively unwrap RootModel .root and enum .value to a plain scalar."""
    current = value
    while isinstance(current, RootModel):
        current = current.root
    if isinstance(current, Enum):
        current = current.value
    return current
