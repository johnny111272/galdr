"""Load and validate style TOML files."""

import json
from pathlib import Path

import gate_galdr_style_input

from galdr.functions.pure.compose import reshape_style_toml
from galdr.functions.pure.defaults import default_style, section_style_model
from galdr.structures.errors import StyleLoadError
from galdr.structures.style import DispatcherStyle, SectionStyle, StyleConfig


def typed_sections(raw_sections: dict[str, dict[str, str]]) -> dict[str, SectionStyle]:
    """Instantiate typed style models for each section from raw TOML dicts."""
    result: dict[str, SectionStyle] = {}
    for section_name, section_data in raw_sections.items():
        model_class = section_style_model(section_name)
        result[section_name] = model_class.model_validate(section_data)
    return result


def resolve_style(style_name: str, styles_dir: Path) -> StyleConfig:
    """Resolve a style name to a StyleConfig by loading {styles_dir}/{name}.toml."""
    style_path = styles_dir / f"{style_name}.toml"
    if style_path.is_file():
        return load_style(str(style_path))
    if style_name == "default":
        return default_style()
    raise StyleLoadError(f"Style '{style_name}' not found at {style_path}")


def load_style(path: str) -> StyleConfig:
    """Load a style TOML file, validate against schema, return StyleConfig."""
    result = gate_galdr_style_input.validate(path)

    if not result["ok"]:
        raise StyleLoadError(f"Style validation failed for {path}: {result['error']['message']}")

    parsed = json.loads(result["data"])
    reshaped = reshape_style_toml(parsed)

    sections = typed_sections(reshaped.get("sections", {}))
    dispatcher_data = reshaped.get("dispatcher")
    dispatcher = DispatcherStyle.model_validate(dispatcher_data) if dispatcher_data else None

    return StyleConfig(
        name=reshaped.get("name", ""),
        sections=sections,
        dispatcher=dispatcher,
    )
