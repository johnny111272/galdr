"""Path resolution utilities for CLI."""

from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    """Walk parents looking for schemas/ + definitions/ as workspace marker."""
    current = start.resolve()
    while current != current.parent:
        if (current / "schemas").is_dir() and (current / "definitions").is_dir():
            return current
        current = current.parent
    return start.resolve()


def derive_output_path(input_path: Path, workspace: Path) -> Path:
    """Derive output path: {workspace}/definitions/staging/{agent_name}.md."""
    agent_name = input_path.parent.name
    return workspace / "definitions" / "staging" / f"{agent_name}.md"


def derive_dispatcher_output_path(input_path: Path, workspace: Path) -> Path:
    """Derive dispatcher output: {workspace}/definitions/staging/dispatch-{agent_name}/SKILL.md."""
    agent_name = input_path.parent.name
    return workspace / "definitions" / "staging" / f"dispatch-{agent_name}" / "SKILL.md"
