"""Rendering entry points for agent and dispatcher markdown files.

Thin adapter: calls pure composition functions with default recipe and style.
"""

from galdr.functions.pure.compose import compose_agent, compose_dispatcher
from galdr.functions.pure.defaults import default_recipe, default_style
from galdr.structures.recipe import RecipeConfig
from galdr.structures.style import StyleConfig
from galdr.structures.template_context import RenderContext


def render_agent(
    context: RenderContext,
    recipe: RecipeConfig | None = None,
    style: StyleConfig | None = None,
) -> str:
    """Render an agent markdown file from a typed context."""
    return compose_agent(context, recipe or default_recipe(), style or default_style())


def render_dispatcher(context: RenderContext, style: StyleConfig | None = None) -> str:
    """Render a dispatcher SKILL.md file from a typed context."""
    return compose_dispatcher(context, style or default_style())
