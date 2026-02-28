"""Reshape guardrails sections: unwrap constraint rules and anti-pattern strings."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import AntiPatterns, Constraints
from galdr.structures.template_context import AntiPatternsContext, ConstraintsContext


def reshape_constraints(constraints: Constraints) -> ConstraintsContext:
    """Unwrap constraint rule strings from RootModel wrappers."""
    return ConstraintsContext(
        rules=[unwrap(rule) for rule in constraints.rules.root],
    )


def reshape_anti_patterns(anti_patterns: AntiPatterns) -> AntiPatternsContext:
    """Unwrap anti-pattern strings from RootModel wrappers."""
    return AntiPatternsContext(
        patterns=[unwrap(pattern) for pattern in anti_patterns.patterns.root],
    )
