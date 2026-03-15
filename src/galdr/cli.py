"""Galdr — composition engine CLI entry point."""

import argparse
import sys
from pathlib import Path

from loguru import logger

from galdr.functions.impure.paths import (
    derive_dispatcher_output_path,
    derive_output_path,
    discover_recipes,
    find_galdr_styles_dir,
    find_workspace_root,
)
from galdr.functions.impure.pipeline import run_batch, run_check, run_render
from galdr.functions.impure.writer import write_agent_file, write_dispatcher_file
from galdr.structures.errors import RecipeLoadError, StyleLoadError


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="galdr",
        description="Compose anthropic_render.toml into deployable agent .md files",
    )
    parser.add_argument("input", help="Path to anthropic_render.toml")
    parser.add_argument("-o", "--output", help="Output file path for rendered agent")
    parser.add_argument("--check", action="store_true", help="Render to stdout without writing")

    recipe_group = parser.add_mutually_exclusive_group()
    recipe_group.add_argument("--recipe", help="Path to recipe TOML file")
    recipe_group.add_argument("--recipe-batch", help="Directory of recipe TOML files for batch rendering")

    parser.add_argument("--style", help="Path to style TOML file (overrides recipe style field)")
    parser.add_argument("--styles-dir", help="Directory for style auto-resolution (default: styles/)")
    parser.add_argument("--workspace", help="Workspace root (auto-detected if omitted)")
    parser.add_argument("--agent-only", action="store_true", help="Skip dispatcher SKILL.md generation")
    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    input_path = Path(args.input)
    styles_dir = Path(args.styles_dir) if args.styles_dir else find_galdr_styles_dir()

    style_override = None
    if args.style:
        from galdr.functions.impure.style_loader import load_style

        try:
            style_override = load_style(args.style)
        except StyleLoadError as err:
            logger.error(str(err))
            return 1

    if args.recipe_batch:
        return handle_batch(args, input_path, styles_dir, style_override)

    recipe = None
    if args.recipe:
        from galdr.functions.impure.recipe_loader import load_recipe

        try:
            recipe = load_recipe(args.recipe)
        except RecipeLoadError as err:
            logger.error(str(err))
            return 1

    style = style_override
    if style is None and recipe is not None:
        from galdr.functions.impure.style_loader import resolve_style

        try:
            style = resolve_style(recipe.style, styles_dir)
        except StyleLoadError as err:
            logger.error(str(err))
            return 1

    if args.check:
        agent_content, dispatcher_content = run_check(str(input_path), recipe, style)
        logger.info(agent_content)
        if dispatcher_content is not None:
            logger.info("\n--- DISPATCHER SKILL.md ---\n")
            logger.info(dispatcher_content)
        return 0

    workspace = Path(args.workspace) if args.workspace else find_workspace_root(input_path)
    agent_output = Path(args.output) if args.output else derive_output_path(input_path, workspace)
    dispatcher_output = None
    if not args.agent_only:
        dispatcher_output = derive_dispatcher_output_path(input_path, workspace)

    agent_path, dispatcher_path = run_render(str(input_path), agent_output, dispatcher_output, recipe, style)
    logger.info(f"Agent: {agent_path}")
    if dispatcher_path is not None:
        logger.info(f"Dispatcher: {dispatcher_path}")
    return 0


def handle_batch(args, input_path: Path, styles_dir: Path, style_override) -> int:
    """Handle --recipe-batch mode."""
    batch_dir = Path(args.recipe_batch)
    if not batch_dir.is_dir():
        logger.error(f"Recipe batch directory not found: {batch_dir}")
        return 1

    recipe_paths = discover_recipes(batch_dir)
    if not recipe_paths:
        logger.error(f"No .toml files found in {batch_dir}")
        return 1

    try:
        results = run_batch(str(input_path), recipe_paths, styles_dir, style_override)
    except (RecipeLoadError, StyleLoadError) as err:
        logger.error(str(err))
        return 1

    if args.check:
        for result in results:
            logger.info(f"\n=== Recipe: {result.recipe_name} ===\n")
            logger.info(result.agent_content)
            if result.dispatcher_content is not None:
                logger.info("\n--- DISPATCHER SKILL.md ---\n")
                logger.info(result.dispatcher_content)
        return 0

    workspace = Path(args.workspace) if args.workspace else find_workspace_root(input_path)
    output_dir = workspace / "definitions" / "staging"
    agent_name = input_path.parent.name

    for result in results:
        agent_path = output_dir / f"{agent_name}.{result.recipe_name}.md"
        write_agent_file(result.agent_content, agent_path)
        logger.info(f"Agent ({result.recipe_name}): {agent_path}")

        if not args.agent_only and result.dispatcher_content is not None:
            disp_dir = output_dir / f"dispatch-{agent_name}.{result.recipe_name}"
            dispatcher_path = disp_dir / "SKILL.md"
            write_dispatcher_file(result.dispatcher_content, dispatcher_path)
            logger.info(f"Dispatcher ({result.recipe_name}): {dispatcher_path}")

    logger.info(f"Batch complete: {len(results)} recipes rendered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
