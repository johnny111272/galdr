"""Galdr CLI — compose agent prompts from four-axis inputs.

Takes a gate-validated anthropic_render.toml (data axis) plus three
control surface TOMLs (content, structure, display) and produces
a deployable agent prompt (.md).

Usage:
    galdr /path/to/anthropic_render.toml
    galdr /path/to/anthropic_render.toml -o /path/to/output.md
"""

from pathlib import Path

import typer

from galdr.logic.orchestrate.compose.orchestrate import run

app = typer.Typer(help="Compose agent prompts from four-axis inputs.")


@app.command()
def compose(
    data: Path = typer.Argument(help="Path to anthropic_render.toml (data axis)"),
    content: Path = typer.Option("extracted/content.toml", help="Path to content.toml"),
    structure: Path = typer.Option("extracted/structure.toml", help="Path to structure.toml"),
    display: Path = typer.Option("extracted/display.toml", help="Path to display.toml"),
    output: Path = typer.Option("staging/output.md", "-o", help="Path for output markdown"),
) -> None:
    """Compose an agent prompt from four-axis TOML inputs."""
    raise SystemExit(run(data, content, structure, display, output))


def main() -> None:
    """Entry point for pyproject.toml script."""
    app()
