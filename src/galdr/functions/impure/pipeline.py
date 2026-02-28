"""Pipeline orchestration: gate -> context -> render -> write."""

from pathlib import Path

from galdr.functions.impure.engine import render_agent, render_dispatcher
from galdr.functions.impure.loader import load_anthropic_render
from galdr.functions.impure.writer import write_agent_file, write_dispatcher_file
from galdr.functions.pure.context import build_render_context


def run_render(input_path: str, agent_output: Path, dispatcher_output: Path | None = None) -> tuple[Path, Path | None]:
    """Full pipeline: load, build context, render agent + dispatcher, write to disk."""
    json_data = load_anthropic_render(input_path)
    context = build_render_context(json_data)
    agent_path = write_agent_file(render_agent(context), agent_output)
    dispatcher_path = None
    if dispatcher_output is not None and context.dispatcher is not None:
        dispatcher_path = write_dispatcher_file(render_dispatcher(context), dispatcher_output)
    return agent_path, dispatcher_path


def run_check(input_path: str) -> tuple[str, str | None]:
    """Check pipeline: load, build context, render, return content strings."""
    json_data = load_anthropic_render(input_path)
    context = build_render_context(json_data)
    agent_content = render_agent(context)
    dispatcher_content = None
    if context.dispatcher is not None:
        dispatcher_content = render_dispatcher(context)
    return agent_content, dispatcher_content
