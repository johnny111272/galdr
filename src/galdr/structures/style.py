"""Style config models for the composition engine."""

from pydantic import BaseModel, ConfigDict


class StyleEntry(BaseModel):
    """Heading, framing, and warning text for one module."""

    model_config = ConfigDict(frozen=True)
    heading: str = ""
    framing: str = ""
    warning: str = ""


class StyleConfig(BaseModel):
    """Tone config: per-module headings, framing, and warnings."""

    model_config = ConfigDict(frozen=True)
    name: str
    sections: dict[str, StyleEntry]
