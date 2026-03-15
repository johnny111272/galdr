"""Recipe and module config models for the composition engine."""

from pydantic import BaseModel, ConfigDict


class ModuleConfig(BaseModel):
    """Per-module rendering config within a recipe."""

    model_config = ConfigDict(frozen=True)
    section: str
    variant: str = "standard"
    framing: bool = False
    warning: bool = False
    fields: list[str] | None = None
    max_entries: int | None = None
    display_headings: bool | None = None


class RecipeConfig(BaseModel):
    """Composition recipe: which modules, what order, what settings."""

    model_config = ConfigDict(frozen=True)
    name: str
    style: str = "default"
    modules: list[ModuleConfig]


class BatchResult(BaseModel):
    """Output from rendering one recipe in a batch run."""

    model_config = ConfigDict(frozen=True)
    recipe_name: str
    agent_content: str
    dispatcher_content: str | None = None
