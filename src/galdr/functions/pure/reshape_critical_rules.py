"""Reshape critical rules section: unwrap RootModel fields."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import CriticalRules
from galdr.structures.template_context import CriticalRulesContext


def reshape_critical_rules(critical_rules: CriticalRules) -> CriticalRulesContext:
    """Unwrap critical rules fields from RootModel wrappers."""
    return CriticalRulesContext(
        has_output_tool=unwrap(critical_rules.has_output_tool),
        workspace_path=unwrap(critical_rules.workspace_path),
        tool_name=unwrap(critical_rules.tool_name) if critical_rules.tool_name else None,
        batch_size=unwrap(critical_rules.batch_size) if critical_rules.batch_size else None,
    )
