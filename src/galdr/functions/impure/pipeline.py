"""Pipeline orchestration: gate -> context -> render -> write."""

from pathlib import Path

from galdr.functions.impure.engine import render_agent, render_dispatcher
from galdr.functions.impure.loader import load_anthropic_render
from galdr.functions.impure.recipe_loader import load_recipe
from galdr.functions.impure.style_loader import resolve_style
from galdr.functions.impure.writer import write_agent_file, write_dispatcher_file
from galdr.functions.pure.context import build_render_context
from galdr.structures.recipe import BatchResult, RecipeConfig
from galdr.structures.style import StyleConfig


def run_render(
    input_path: str,
    agent_output: Path,
    dispatcher_output: Path | None = None,
    recipe: RecipeConfig | None = None,
    style: StyleConfig | None = None,
) -> tuple[Path, Path | None]:
    """Full pipeline: load, build context, render agent + dispatcher, write to disk."""
    json_data = load_anthropic_render(input_path)
    context = build_render_context(json_data)
    agent_path = write_agent_file(render_agent(context, recipe, style), agent_output)
    dispatcher_path = None
    if dispatcher_output is not None and context.dispatcher is not None:
        dispatcher_path = write_dispatcher_file(render_dispatcher(context), dispatcher_output)
    return agent_path, dispatcher_path


def run_check(
    input_path: str,
    recipe: RecipeConfig | None = None,
    style: StyleConfig | None = None,
) -> tuple[str, str | None]:
    """Check pipeline: load, build context, render, return content strings."""
    json_data = load_anthropic_render(input_path)
    context = build_render_context(json_data)
    agent_content = render_agent(context, recipe, style)
    dispatcher_content = None
    if context.dispatcher is not None:
        dispatcher_content = render_dispatcher(context)
    return agent_content, dispatcher_content


def run_batch(
    input_path: str,
    recipe_paths: list[str],
    styles_dir: Path,
    style_override: StyleConfig | None = None,
) -> list[BatchResult]:
    """Render same content through multiple recipes, return results."""
    json_data = load_anthropic_render(input_path)
    context = build_render_context(json_data)
    results = []
    for recipe_path in recipe_paths:
        recipe = load_recipe(recipe_path)
        style = style_override or resolve_style(recipe.style, styles_dir)
        agent_content = render_agent(context, recipe, style)
        dispatcher_content = None
        if context.dispatcher is not None:
            dispatcher_content = render_dispatcher(context)
        results.append(
            BatchResult(
                recipe_name=recipe.name,
                agent_content=agent_content,
                dispatcher_content=dispatcher_content,
            )
        )
    return results
