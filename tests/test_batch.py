"""Tests for batch rendering pipeline."""

from pathlib import Path

import pytest

from galdr.functions.impure.paths import discover_recipes
from galdr.functions.impure.pipeline import run_batch
from galdr.functions.pure.defaults import default_style
from galdr.structures.recipe import BatchResult


MINIMAL_RECIPE = """\
name = "{name}"
style = "default"

[[modules]]
section = "frontmatter"

[[modules]]
section = "identity"

[[modules]]
section = "return_format"
"""

MINIMAL_STYLE = """\
name = "default"

[input]
heading = "Input"
"""

AGENT_RENDER = Path("/Users/johnny/.ai/spaces/bragi/definitions/agents/agent-auditor/anthropic_render.toml")


@pytest.fixture()
def batch_dir(tmp_path):
    """Create a temp directory with two recipe files."""
    recipe_a = tmp_path / "alpha.toml"
    recipe_a.write_text(MINIMAL_RECIPE.format(name="alpha"))
    recipe_b = tmp_path / "beta.toml"
    recipe_b.write_text(MINIMAL_RECIPE.format(name="beta"))
    return tmp_path


@pytest.fixture()
def styles_dir(tmp_path):
    """Create a temp styles directory with default.toml."""
    style_dir = tmp_path / "styles"
    style_dir.mkdir()
    (style_dir / "default.toml").write_text(MINIMAL_STYLE)
    return style_dir


def test_discover_recipes(batch_dir):
    paths = discover_recipes(batch_dir)
    assert len(paths) == 2
    assert paths[0].endswith("alpha.toml")
    assert paths[1].endswith("beta.toml")


def test_discover_recipes_empty(tmp_path):
    assert discover_recipes(tmp_path) == []


@pytest.mark.skipif(not AGENT_RENDER.exists(), reason="requires agent-auditor render data")
def test_run_batch_multiple_recipes(batch_dir, styles_dir):
    recipe_paths = discover_recipes(batch_dir)
    results = run_batch(str(AGENT_RENDER), recipe_paths, styles_dir)
    assert len(results) == 2
    assert results[0].recipe_name == "alpha"
    assert results[1].recipe_name == "beta"
    assert "# Agent Auditor" in results[0].agent_content
    assert "# Agent Auditor" in results[1].agent_content


@pytest.mark.skipif(not AGENT_RENDER.exists(), reason="requires agent-auditor render data")
def test_run_batch_style_override(batch_dir, styles_dir):
    recipe_paths = discover_recipes(batch_dir)
    override = default_style()
    results = run_batch(str(AGENT_RENDER), recipe_paths, styles_dir, style_override=override)
    assert len(results) == 2
    for result in results:
        assert isinstance(result, BatchResult)


def test_batch_result_model():
    result = BatchResult(recipe_name="test", agent_content="# Agent")
    assert result.recipe_name == "test"
    assert result.agent_content == "# Agent"
    assert result.dispatcher_content is None


def test_batch_result_frozen():
    result = BatchResult(recipe_name="test", agent_content="# Agent")
    with pytest.raises(Exception):
        result.recipe_name = "other"
