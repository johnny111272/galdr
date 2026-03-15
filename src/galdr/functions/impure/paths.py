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


def discover_recipes(batch_dir: Path) -> list[str]:
    """Find all .toml files in a directory, sorted by name."""
    return sorted(str(path) for path in batch_dir.glob("*.toml"))


def find_galdr_styles_dir() -> Path:
    """Return the default styles directory in the galdr project root."""
    return Path(__file__).resolve().parent.parent.parent.parent / "styles"
