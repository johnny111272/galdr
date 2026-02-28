"""Reshape frontmatter section: compose hook commands, join tools list."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import Frontmatter, HookAction
from galdr.structures.template_context import FrontmatterContext, HookContext


def reshape_frontmatter(frontmatter: Frontmatter) -> FrontmatterContext:
    """Compose hook commands from binary+arguments, join tools to CSV."""
    return FrontmatterContext(
        name=unwrap(frontmatter.name),
        description=unwrap(frontmatter.description),
        model=unwrap(frontmatter.model),
        permission_mode=unwrap(frontmatter.permission_mode),
        tools=", ".join(unwrap(tool) for tool in frontmatter.tools.root),
        hooks=extract_hooks(frontmatter),
    )


def extract_hooks(frontmatter: Frontmatter) -> list[HookContext] | None:
    """Extract and compose hook entries from frontmatter hooks config."""
    if frontmatter.hooks is None:
        return None
    actions = frontmatter.hooks.PreToolUse
    if actions is None:
        return None
    return [reshape_hook(hook) for hook in actions.root]


def reshape_hook(hook: HookAction) -> HookContext:
    """Compose a single hook's binary and arguments into a command string."""
    binary = unwrap(hook.binary)
    arguments = [unwrap(arg) for arg in hook.arguments.root] if hook.arguments else []
    command = f"{binary} {' '.join(arguments)}" if arguments else binary
    return HookContext(matcher=unwrap(hook.matcher), command=command)
