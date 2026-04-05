"""Section buffer — intermediate collection model for section composition.

Collects rendered fragments into positional slots (heading, preamble, body,
postscript) before final assembly. The buffer is populated in one pass over
content fields, then body is filled by the data walk, then rendered in order.

Pattern: regin/structure/model/anthropic_context.py — intermediate model
with named slots for render composition.
"""

from pydantic import BaseModel, ConfigDict


class SectionBuffer(BaseModel):
    model_config = ConfigDict(frozen=True)
    heading: str | None = None
    preamble: tuple[str, ...] = ()
    body: tuple[str, ...] = ()
    postscript: tuple[str, ...] = ()
