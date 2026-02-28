"""Galdr — template renderer CLI entry point."""

import argparse
import sys
from pathlib import Path

from loguru import logger

from galdr.functions.impure.paths import derive_dispatcher_output_path, derive_output_path, find_workspace_root
from galdr.functions.impure.pipeline import run_check, run_render


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="galdr",
        description="Render anthropic_render.toml into deployable agent .md files",
    )
    parser.add_argument("input", help="Path to anthropic_render.toml")
    parser.add_argument("-o", "--output", help="Output file path for rendered agent")
    parser.add_argument("--check", action="store_true", help="Render to stdout without writing")
    parser.add_argument("--workspace", help="Workspace root (auto-detected if omitted)")
    parser.add_argument("--agent-only", action="store_true", help="Skip dispatcher SKILL.md generation")
    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    input_path = Path(args.input)

    if args.check:
        agent_content, dispatcher_content = run_check(str(input_path))
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

    agent_path, dispatcher_path = run_render(str(input_path), agent_output, dispatcher_output)
    logger.info(f"Agent: {agent_path}")
    if dispatcher_path is not None:
        logger.info(f"Dispatcher: {dispatcher_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
