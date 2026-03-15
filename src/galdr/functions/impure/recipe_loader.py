"""Load and validate recipe TOML files."""

import tomllib

from pydantic import ValidationError

from galdr.functions.pure.compose import validate_section_names
from galdr.structures.errors import RecipeLoadError
from galdr.structures.recipe import RecipeConfig


def load_recipe(path: str) -> RecipeConfig:
    """Load a recipe TOML file and return a validated RecipeConfig."""
    try:
        with open(path, "rb") as fh:
            raw = tomllib.load(fh)
    except tomllib.TOMLDecodeError as err:
        raise RecipeLoadError(f"Invalid TOML in {path}: {err}") from err

    try:
        recipe = RecipeConfig.model_validate(raw)
    except ValidationError as err:
        raise RecipeLoadError(f"Recipe validation failed for {path}: {err}") from err

    unknown = validate_section_names(recipe)
    if unknown:
        raise RecipeLoadError(
            f"Unknown section names in {path}: {', '.join(unknown)}"
        )

    return recipe
