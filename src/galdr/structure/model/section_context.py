"""Section context — bundled control surfaces for section composition.

Groups the four inputs that travel together through every section
processor: content, structure, display, and pre-unwrapped data values.
Avoids passing these as separate parameters through every function call.
"""

from pydantic import BaseModel, ConfigDict


class SectionContext(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    content: BaseModel
    structure: BaseModel
    display: BaseModel | None
    data_values: dict[str, str]
