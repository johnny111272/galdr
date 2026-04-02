"""Pipeline error types for Galdr."""


class GateValidationError(Exception):
    """A gate rejected its input."""


class RecipeLoadError(Exception):
    """A recipe TOML file could not be loaded or validated."""


class StyleLoadError(Exception):
    """A style TOML file could not be loaded or validated."""
