"""Write rendered agent markdown files to disk."""

from pathlib import Path


def write_agent_file(content: str, output_path: Path) -> Path:
    """Write rendered markdown string to disk, creating parents."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    return output_path


def write_dispatcher_file(content: str, output_path: Path) -> Path:
    """Write rendered dispatcher SKILL.md to disk, creating parents."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    return output_path
