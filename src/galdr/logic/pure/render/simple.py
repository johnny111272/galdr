"""Render simple — list renderers and inline/heading formatters.

CC=1-3. List renderers iterate over items using primitives.
Inline and heading formatters dispatch on format enums.

Display enum types are defined in structure/gen/output_display.py:
  ListFormat: bulleted, numbered, inline, prose, bare
  InlineFormat: backtick, plain, bold, metadata
  HeadingFormat: bold, h3, h4
"""

from galdr.logic.pure.render.primitive import bold, bullet_item, heading, numbered_item
from galdr.structure.gen.output_display import HeadingFormat, InlineFormat


def render_bulleted(items: list[str]) -> str:
    """Join items as a bulleted markdown list."""
    return "\n".join(bullet_item(item) for item in items)


def render_numbered(items: list[str]) -> str:
    """Join items as a numbered markdown list."""
    return "\n".join(numbered_item(item, position) for position, item in enumerate(items, 1))


def render_inline_list(items: list[str]) -> str:
    """Join items as comma-separated inline text."""
    return ", ".join(items)


def render_prose_list(items: list[str]) -> str:
    """Join items as space-separated prose."""
    return " ".join(items)


def render_bare_list(items: list[str]) -> str:
    """Join items with newlines, no markers."""
    return "\n".join(items)


def format_inline(text: str, inline_format: InlineFormat) -> str:
    """Format a single value according to the InlineFormat enum."""
    if inline_format == InlineFormat.backtick:
        return backtick(text)
    if inline_format == InlineFormat.bold:
        return bold(text)
    return text


def format_heading(text: str, heading_format: HeadingFormat) -> str:
    """Format a sub-block heading according to the HeadingFormat enum."""
    if heading_format == HeadingFormat.h3:
        return heading(text, 3)
    if heading_format == HeadingFormat.h4:
        return heading(text, 4)
    return bold(text)
