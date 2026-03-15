"""Load and validate style TOML files."""

import tomllib
from pathlib import Path

from pydantic import ValidationError

from galdr.functions.pure.compose import reshape_style_toml, validate_style_sections
from galdr.functions.pure.defaults import default_style
from galdr.structures.errors import StyleLoadError
from galdr.structures.style import StyleConfig


def resolve_style(style_name: str, styles_dir: Path) -> StyleConfig:
    """Resolve a style name to a StyleConfig by loading {styles_dir}/{name}.toml."""
    style_path = styles_dir / f"{style_name}.toml"
    if style_path.is_file():
        return load_style(str(style_path))
    if style_name == "default":
        return default_style()
    raise StyleLoadError(f"Style '{style_name}' not found at {style_path}")


def load_style(path: str) -> StyleConfig:
    """Load a style TOML file and return a validated StyleConfig."""
    try:
        with open(path, "rb") as fh:
            parsed_toml = tomllib.load(fh)
    except tomllib.TOMLDecodeError as err:
        raise StyleLoadError(f"Invalid TOML in {path}: {err}") from err

    reshaped = reshape_style_toml(parsed_toml)

    try:
        style = StyleConfig.model_validate(reshaped)
    except ValidationError as err:
        raise StyleLoadError(f"Style validation failed for {path}: {err}") from err

    unknown = validate_style_sections(style)
    if unknown:
        raise StyleLoadError(
            f"Unknown section names in {path}: {', '.join(unknown)}"
        )

    return style
