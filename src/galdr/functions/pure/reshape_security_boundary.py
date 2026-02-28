"""Reshape security boundary: unwrap display entries."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import DisplayEntry, SecurityBoundaryAnthropic
from galdr.structures.template_context import DisplayEntryContext, SecurityBoundaryContext


def reshape_security_boundary(security_boundary: SecurityBoundaryAnthropic) -> SecurityBoundaryContext:
    """Unwrap has_grants and display entries from RootModel wrappers."""
    return SecurityBoundaryContext(
        has_grants=unwrap(security_boundary.has_grants),
        display=[reshape_display_entry(entry) for entry in security_boundary.display.root],
    )


def reshape_display_entry(entry: DisplayEntry) -> DisplayEntryContext:
    """Unwrap a single display entry's path and tools list."""
    return DisplayEntryContext(
        path=unwrap(entry.path),
        tools=[unwrap(tool) for tool in entry.tools.root],
    )
