"""Reshape security boundary: unwrap display entries."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import DisplayEntry, SecurityBoundaryAnthropic
from galdr.structures.template_context import DisplayEntryContext, SecurityBoundaryContext


def reshape_security_boundary(security_boundary: SecurityBoundaryAnthropic) -> SecurityBoundaryContext:
    """Derive has_grants from display entries presence."""
    display = (
        [reshape_display_entry(entry) for entry in security_boundary.display.root]
        if security_boundary.display is not None
        else []
    )
    return SecurityBoundaryContext(
        workspace_path=unwrap(security_boundary.workspace_path),
        has_grants=len(display) > 0,
        display=display,
    )


def reshape_display_entry(entry: DisplayEntry) -> DisplayEntryContext:
    """Unwrap a single display entry's path and tools list."""
    return DisplayEntryContext(
        path=unwrap(entry.path),
        tools=[unwrap(tool) for tool in entry.tools.root],
    )
