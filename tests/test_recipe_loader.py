"""Tests for recipe TOML loading and validation."""

import pytest

from galdr.functions.impure.recipe_loader import load_recipe
from galdr.structures.errors import RecipeLoadError


def write_toml(tmp_path, content: str) -> str:
    """Write TOML content to a temp file, return path as string."""
    path = tmp_path / "recipe.toml"
    path.write_text(content)
    return str(path)


def test_load_recipe_valid(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "test"\nstyle = "default"\n\n[[modules]]\nsection = "frontmatter"\n\n[[modules]]\nsection = "identity"\n',
    )
    recipe = load_recipe(path)
    assert recipe.name == "test"
    assert recipe.style == "default"
    assert len(recipe.modules) == 2
    assert recipe.modules[0].section == "frontmatter"


def test_load_recipe_minimal(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "minimal"\n\n[[modules]]\nsection = "frontmatter"\n',
    )
    recipe = load_recipe(path)
    assert recipe.name == "minimal"
    assert recipe.style == "default"
    assert recipe.modules[0].variant == "standard"


def test_load_recipe_all_fields(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "full"\nstyle = "custom"\n\n[[modules]]\nsection = "examples"\nvariant = "prose"\nframing = true\nwarning = true\nmax_entries = 5\ndisplay_headings = false\nfields = ["heading", "text"]\n',
    )
    recipe = load_recipe(path)
    module = recipe.modules[0]
    assert module.section == "examples"
    assert module.variant == "prose"
    assert module.framing is True
    assert module.warning is True
    assert module.max_entries == 5
    assert module.display_headings is False
    assert module.fields == ["heading", "text"]


def test_load_recipe_missing_name(tmp_path):
    path = write_toml(
        tmp_path,
        '[[modules]]\nsection = "frontmatter"\n',
    )
    with pytest.raises(RecipeLoadError, match="validation failed"):
        load_recipe(path)


def test_load_recipe_unknown_section(tmp_path):
    path = write_toml(
        tmp_path,
        'name = "typo"\n\n[[modules]]\nsection = "constrants"\n',
    )
    with pytest.raises(RecipeLoadError, match="Unknown section.*constrants"):
        load_recipe(path)


def test_load_recipe_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_recipe("/nonexistent/recipe.toml")


def test_load_recipe_invalid_toml(tmp_path):
    path = write_toml(tmp_path, "this is not = [valid toml")
    with pytest.raises(RecipeLoadError, match="Invalid TOML"):
        load_recipe(path)
