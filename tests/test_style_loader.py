"""Tests for style TOML loading and validation."""

from pathlib import Path

import pytest

from galdr.functions.impure.style_loader import load_style, resolve_style
from galdr.functions.pure.defaults import default_style
from galdr.structures.errors import StyleLoadError


def write_toml(tmp_path, content: str) -> str:
    """Write TOML content to a temp file, return path as string."""
    path = tmp_path / "style.toml"
    path.write_text(content)
    return str(path)


def test_load_style_valid(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "test"\n\n[input]\nheading = "Input"\n\n[output]\nheading = "Output"\n',
    )
    style = load_style(path)
    assert style.name == "test"
    assert len(style.sections) == 2
    assert style.sections["input"].heading == "Input"
    assert style.sections["output"].heading == "Output"


def test_load_style_minimal(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "minimal"\n\n[constraints]\n',
    )
    style = load_style(path)
    assert style.name == "minimal"
    assert style.sections["constraints"].heading == "Constraints"
    assert style.sections["constraints"].framing == ""
    assert style.sections["constraints"].warning == ""


def test_load_style_all_fields(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "full"\n\n[constraints]\nheading = "Rules"\nframing = "Stay within bounds:"\nwarning = "Violation is failure."\n',
    )
    style = load_style(path)
    section = style.sections["constraints"]
    assert section.heading == "Rules"
    assert section.framing == "Stay within bounds:"
    assert section.warning == "Violation is failure."


def test_load_style_missing_name(tmp_path):
    path = write_toml(
        tmp_path,
        '[input]\nheading = "Input"\n',
    )
    with pytest.raises(StyleLoadError, match="validation failed"):
        load_style(path)


def test_load_style_unknown_section(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "typo"\n\n[constrants]\nheading = "Rules"\n',
    )
    with pytest.raises(StyleLoadError, match="additional_property"):
        load_style(path)


def test_load_style_file_not_found():
    with pytest.raises(StyleLoadError, match="No such file or directory"):
        load_style("/nonexistent/style.toml")


def test_load_style_invalid_toml(tmp_path):
    path = write_toml(tmp_path, "this is not = [valid toml")
    with pytest.raises(StyleLoadError, match="TOML parse error"):
        load_style(path)


# --- resolve_style ---


def test_resolve_style_found(tmp_path):
    style_file = tmp_path / "custom.toml"
    style_file.write_text('name = "custom"\n\n[input]\nheading = "Custom Input"\n')
    style = resolve_style("custom", tmp_path)
    assert style.name == "custom"
    assert style.sections["input"].heading == "Custom Input"


def test_resolve_style_default_fallback(tmp_path):
    style = resolve_style("default", tmp_path)
    expected = default_style()
    assert style.name == expected.name
    assert style.sections == expected.sections


def test_resolve_style_not_found(tmp_path):
    with pytest.raises(StyleLoadError, match="not found"):
        resolve_style("nonexistent", tmp_path)
