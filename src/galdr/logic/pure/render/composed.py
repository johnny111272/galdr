"""Render composed — list format resolution and adaptive rendering.

CC=4-8. Resolves polymorphic format fields and dispatches to the
correct simple-level list renderer.

Display TOML uses a tuple convention for count-based switching:
  expertise_format = ["bulleted", "inline"]   # above/at-or-below threshold
  expertise_format_threshold = 3

See structure/gen/output_display.py for FormatPair and UnionFormatOrPair.
"""

from galdr.logic.pure.render.simple import (
    render_bare_list,
    render_bulleted,
    render_inline_list,
    render_numbered,
    render_prose_list,
)
from galdr.structure.gen.output_display import FormatPair, ListFormat, UnionFormatOrPair


def resolve_format(format_or_pair: UnionFormatOrPair, count: int, threshold: int) -> ListFormat:
    """Resolve a UnionFormatOrPair to a concrete ListFormat.

    Plain ListFormat passes through unchanged. FormatPair switches:
    first element when count is above threshold, second when at or below.
    """
    inner = format_or_pair.root
    if isinstance(inner, ListFormat):
        return inner
    if isinstance(inner, FormatPair):
        above, at_or_below = inner.root
        return above if count > threshold else at_or_below
    return ListFormat.bulleted


def render_list(items: list[str], list_format: ListFormat) -> str:
    """Render a list of strings by dispatching on ListFormat enum."""
    if list_format == ListFormat.bulleted:
        return render_bulleted(items)
    if list_format == ListFormat.numbered:
        return render_numbered(items)
    if list_format == ListFormat.inline:
        return render_inline_list(items)
    if list_format == ListFormat.prose:
        return render_prose_list(items)
    return render_bare_list(items)


