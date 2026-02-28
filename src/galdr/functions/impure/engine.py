"""Jinja2 template engine for rendering agent markdown files.

Impure: reads template files from disk via FileSystemLoader.
"""

from pathlib import Path

import jinja2

from galdr.structures.template_context import RenderContext

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"


def create_environment() -> jinja2.Environment:
    """Create a Jinja2 environment loading from the templates directory."""
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_agent(context: RenderContext) -> str:
    """Render an agent markdown file from a typed context."""
    env = create_environment()
    template = env.get_template("variants/standard_v1.md.j2")
    template_vars = {field: getattr(context, field) for field in RenderContext.model_fields}
    return template.render(template_vars)


def render_dispatcher(context: RenderContext) -> str:
    """Render a dispatcher SKILL.md file from a typed context."""
    env = create_environment()
    template = env.get_template("skills/dispatch_v1.md.j2")
    template_vars = {field: getattr(context, field) for field in RenderContext.model_fields}
    return template.render(template_vars)
