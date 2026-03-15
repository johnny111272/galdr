"""Reshape frontmatter section: compose hook commands, join tools list."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import (
    CommandPathEntry,
    Frontmatter,
    HooksConfig,
    ToolPathEntry,
)
from galdr.structures.template_context import FrontmatterContext, HookContext


def reshape_frontmatter(frontmatter: Frontmatter) -> FrontmatterContext:
    """Compose hook commands from structured entries, join tools to CSV."""
    return FrontmatterContext(
        name=unwrap(frontmatter.name),
        description=unwrap(frontmatter.description),
        model=unwrap(frontmatter.model),
        permission_mode=unwrap(frontmatter.permission_mode),
        tools=", ".join(unwrap(tool) for tool in frontmatter.tools.root),
        hooks=build_hook_commands(frontmatter.hooks),
    )


def build_hook_commands(hooks: HooksConfig) -> list[HookContext] | None:
    """Build CLI hook commands from structured tool/command entries."""
    results: list[HookContext] = []
    tool_hook = build_tool_hook(hooks)
    if tool_hook is not None:
        results.append(tool_hook)
    bash_hook = build_bash_hook(hooks)
    if bash_hook is not None:
        results.append(bash_hook)
    return results if results else None


def build_tool_hook(hooks: HooksConfig) -> HookContext | None:
    """Build the tool intercept hook from tool_entries."""
    if hooks.tool_entries is None:
        return None
    entries = hooks.tool_entries.root
    if not entries:
        return None
    matcher = build_tool_matcher(entries)
    args = [format_tool_arg(entry) for entry in entries]
    command = f"hook_intercept_subagent_tool {' '.join(args)}"
    return HookContext(matcher=matcher, command=command)


def build_tool_matcher(entries: list[ToolPathEntry]) -> str:
    """Build matcher string — all tool names joined with pipe."""
    return "|".join(unwrap(entry.tool) for entry in entries)


def format_tool_arg(entry: ToolPathEntry) -> str:
    """Format a single tool entry as Tool=/path1/,/path2/ CLI argument."""
    tool_name = unwrap(entry.tool)
    paths = ",".join(unwrap(path) for path in entry.paths.root)
    return f"{tool_name}={paths}"


def build_bash_hook(hooks: HooksConfig) -> HookContext | None:
    """Build the bash intercept hook from command_entries + output_tool."""
    has_commands = hooks.command_entries is not None and hooks.command_entries.root
    has_output = hooks.output_tool is not None
    if not has_commands and not has_output:
        return None
    parts = ["hook_intercept_subagent_bash"]
    if has_output:
        parts.append(f"--writer {unwrap(hooks.output_tool)}")
    if has_commands:
        parts.append("--inspect")
        for entry in hooks.command_entries.root:
            parts.append(format_command_arg(entry))
    return HookContext(matcher="Bash", command=" ".join(parts))


def format_command_arg(entry: CommandPathEntry) -> str:
    """Format a single command entry as cmd=/path1/,/path2/ CLI argument."""
    cmd_name = unwrap(entry.command)
    paths = ",".join(unwrap(path) for path in entry.paths.root)
    return f"{cmd_name}={paths}"
