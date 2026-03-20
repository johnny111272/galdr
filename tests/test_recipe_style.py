"""Tests for recipe/style models and defaults."""

import pytest
from pydantic import ValidationError

from galdr.functions.pure.defaults import default_recipe, default_style
from galdr.structures.recipe import ModuleConfig, RecipeConfig
from galdr.structures.style import ConstraintsStyle, SectionStyle, StyleConfig


# --- Model construction ---


def test_module_config_defaults():
    config = ModuleConfig(section="constraints")
    assert config.variant == "standard"
    assert config.framing is False
    assert config.warning is False
    assert config.fields is None
    assert config.max_entries is None
    assert config.display_headings is None


def test_module_config_all_fields():
    config = ModuleConfig(
        section="examples",
        variant="compact",
        framing=True,
        warning=True,
        max_entries=3,
        display_headings=False,
    )
    assert config.section == "examples"
    assert config.variant == "compact"
    assert config.max_entries == 3


def test_recipe_config_minimal():
    recipe = RecipeConfig(
        name="test",
        modules=[ModuleConfig(section="frontmatter")],
    )
    assert recipe.name == "test"
    assert recipe.style == "default"
    assert len(recipe.modules) == 1


def test_section_style_defaults():
    entry = SectionStyle()
    assert entry.heading == ""
    assert entry.framing == ""
    assert entry.warning == ""


def test_style_config():
    style = StyleConfig(
        name="test",
        sections={"constraints": ConstraintsStyle(heading="Rules")},
    )
    assert style.sections["constraints"].heading == "Rules"


# --- Frozen models ---


def test_module_config_frozen():
    config = ModuleConfig(section="constraints")
    with pytest.raises(ValidationError):
        config.section = "other"


def test_recipe_config_frozen():
    recipe = RecipeConfig(name="test", modules=[])
    with pytest.raises(ValidationError):
        recipe.name = "other"


def test_style_config_frozen():
    style = StyleConfig(name="test", sections={})
    with pytest.raises(ValidationError):
        style.name = "other"


# --- Defaults ---


EXPECTED_MODULE_ORDER = [
    "frontmatter",
    "identity",
    "security_boundary",
    "input",
    "instructions",
    "examples",
    "output",
    "writing_output",
    "constraints",
    "anti_patterns",
    "success_criteria",
    "failure_criteria",
    "return_format",
    "critical_rules",
]


def test_default_recipe_module_count():
    recipe = default_recipe()
    assert len(recipe.modules) == 14


def test_default_recipe_module_order():
    recipe = default_recipe()
    section_names = [module.section for module in recipe.modules]
    assert section_names == EXPECTED_MODULE_ORDER


def test_default_style_covers_all_modules():
    recipe = default_recipe()
    style = default_style()
    recipe_sections = {module.section for module in recipe.modules}
    style_sections = set(style.sections.keys())
    assert recipe_sections == style_sections


def test_default_style_headings():
    style = default_style()
    assert style.sections["input"].heading == "Input"
    assert style.sections["instructions"].heading == "Processing"
    assert style.sections["constraints"].heading == "Constraints"
    assert style.sections["anti_patterns"].heading == "Anti-Patterns"
    assert style.sections["critical_rules"].heading == "Critical Rules"
    assert style.sections["writing_output"].heading == "Writing Output (MANDATORY)"


def test_default_style_identity_no_heading():
    style = default_style()
    assert style.sections["identity"].heading == ""


def test_default_style_frontmatter_no_heading():
    style = default_style()
    assert style.sections["frontmatter"].heading == ""
