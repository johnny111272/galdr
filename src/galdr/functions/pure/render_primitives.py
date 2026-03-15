"""Rendering primitives — pure functions that produce markdown strings.

Each function takes typed data and returns a markdown string.
No IO, no side effects, no dependencies beyond Python stdlib.
"""


def heading(level: int, text: str) -> str:
    """Produce a markdown heading. Returns empty string if text is empty."""
    if not text:
        return ""
    return f"{'#' * level} {text}"


def list_as_bullets(items: list[str]) -> str:
    """Render items as a bullet list."""
    if not items:
        return ""
    return "\n".join(f"- {item}" for item in items)


def list_as_numbered(items: list[str]) -> str:
    """Render items as a numbered list."""
    if not items:
        return ""
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))


def bold_label(label: str, value: str) -> str:
    """Produce **label:** value."""
    return f"**{label}:** {value}"


def bold_label_code(label: str, value: str) -> str:
    """Produce **label:** `value` with the value in inline code."""
    return f"**{label}:** `{value}`"


def code_block(content: str, language: str = "") -> str:
    """Produce a fenced code block."""
    return f"```{language}\n{content}\n```"


def paragraph(text: str) -> str:
    """Produce a text paragraph. Returns empty string if text is empty."""
    if not text:
        return ""
    return text


def join_sections(sections: list[str], separator: str = "\n---\n") -> str:
    """Join rendered sections, filtering out empty strings."""
    return separator.join(section for section in sections if section)


def section_frame(heading_text: str, level: int, framing: str, warning: str, content: str) -> str:
    """Universal section wrapper: heading + framing + warning + content.

    Returns empty string if content is empty (optional section with no data).
    """
    if not content:
        return ""
    parts = []
    rendered_heading = heading(level, heading_text)
    if rendered_heading:
        parts.append(rendered_heading)
    if framing:
        parts.append(framing)
    if warning:
        parts.append(warning)
    parts.append(content)
    return "\n\n".join(parts)


def yaml_frontmatter(fields: dict[str, str]) -> str:
    """Produce a YAML frontmatter block with quoted string values."""
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f'{key}: "{value}"')
    lines.append("---")
    return "\n".join(lines)
