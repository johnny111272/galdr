"""Render primitives — single-item markdown formatters.

CC=1. Each function formats one item. No iteration, no branching.
These are the atoms — list renderers compose them at simple level.
"""


def heading(text: str, level: int) -> str:
    """Render a markdown heading at the given level."""
    return f"{'#' * level} {text}"


def bold(text: str) -> str:
    """Wrap text in markdown bold."""
    return f"**{text}**"


def backtick(text: str) -> str:
    """Wrap text in inline code backticks."""
    return f"`{text}`"


def bullet_item(text: str) -> str:
    """Render a markdown bullet list item."""
    return f"- {text}"


def numbered_item(text: str, position: int) -> str:
    """Render a markdown numbered list item."""
    return f"{position}. {text}"
