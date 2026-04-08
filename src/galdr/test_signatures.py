═══ INJECTION (signatures) ═══

── src/galdr/logic/pure/compose/primitive.py ──
def has_preamble_suffix(name: str) -> bool

def has_closing_suffix(name: str) -> bool

def has_heading_suffix(name: str) -> bool

── src/galdr/logic/pure/render/primitive.py ──
def heading(text: str, level: int) -> str

def bold(text: str) -> str

def bullet_item(text: str) -> str

def numbered_item(text: str, position: int) -> str

── src/galdr/logic/pure/template/primitive.py ──
def interpolate(template: str, values: dict[str, str]) -> str

── src/galdr/structure/gen/output_content.py ──
class StringTemplate(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description='Prose string containing at least one {{placeholder}} interpolation marker. The renderer substitutes marker contents with data field values at composition time. Used for content.toml template blobs like headings, declarations, and labels that embed agent-specific data in prose.\n',
            min_length=5,
            pattern='\\{\\{[a-zA-Z_]+\\}\\}',
            title='StringTemplate',
        ),
    ]

── src/galdr/structure/gen/output_display.py ──
class ListFormat(Enum):
    bulleted = 'bulleted'
    numbered = 'numbered'
    inline = 'inline'
    prose = 'prose'
    bare = 'bare'

class FormatPair(RootModel[tuple[ListFormat, ListFormat]]):
    root: Annotated[
        tuple[ListFormat, ListFormat],
        Field(
            description='Threshold-based format switching pair. First element is the format used when item count is above the threshold. Second element is the format used at or below the threshold. Example: [bulleted, inline] with threshold 3 means bulleted above 3, inline at or below 3.\n',
            max_length=2,
            min_length=2,
            title='FormatPair',
        ),
    ]

class HeadingFormat(Enum):
    bold = 'bold'
    h3 = 'h3'
    h4 = 'h4'

class InlineFormat(Enum):
    backtick = 'backtick'
    plain = 'plain'
    bold = 'bold'
    metadata = 'metadata'

── src/galdr/structure/model/section_buffer.py ──
class SectionBuffer(BaseModel):
    model_config = ConfigDict(frozen=True)
    heading: str | None = None
    preamble: tuple[str, ...] = ()
    body: tuple[str, ...] = ()
    postscript: tuple[str, ...] = ()

── src/galdr/logic/pure/compose/simple.py ──
def resolve_format_pair(
    above: ListFormat,
    at_or_below: ListFormat,
    count: int,
    threshold: int,
) -> ListFormat

def find_decoration(trunk: str, content_model: BaseModel) -> dict[str, str]

def is_gate_annotation(annotation: type) -> bool

def is_rootmodel_annotation(annotation: type) -> bool

def is_basemodel_annotation(annotation: type) -> bool

def is_list_rootmodel(rootmodel_type: type[RootModel]) -> bool

def list_item_type(rootmodel_type: type[RootModel]) -> type | None

def is_compound_list_annotation(annotation: type) -> bool

def unwrap_scalar_field(field_value: BaseModel, annotation: type) -> str | None

def select_active_roles(mode_content: BaseModel) -> list[str]

def find_d1_content_table(
    enum_field_name: str,
    content_section: BaseModel,
) -> BaseModel | None

def find_enum_field_name(item_type: type[BaseModel]) -> str | None

def has_enum_discriminator(item_type: type[BaseModel]) -> bool

def has_scalar_list_field(item_type: type[BaseModel]) -> bool

def strip_optional_annotation(annotation: type) -> type

def render_item_scalar_field(field_name: str, text: str) -> str

def render_entries_from_dicts(
    item_dicts: list[dict[str, str]],
    entry_template: str,
    section_data_values: dict[str, str],
) -> list[str]

def render_content_text(content_value: RootModel, data_values: dict[str, str]) -> str

def assemble_buffer(
    heading_text: str | None,
    items: list[tuple[str, str]],
) -> "SectionBuffer"

def buffer_slot_for_field(content_name: str) -> str | None

def resolve_section_variant(
    content_name: str,
    content_value: BaseModel,
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> str | None

def list_item_to_string(item: BaseModel) -> str

def get_visibility_toggle(content_name: str, structure_section: BaseModel) -> str | bool | None

def is_toggle_visible(toggle_value: str | bool | None) -> bool

def check_section_gate(data_section: BaseModel | None, section_visible: bool) -> bool

def extract_section_visible(structure_section: BaseModel) -> bool

def render_buffer(buffer: BaseModel) -> str | None

── src/galdr/logic/pure/render/simple.py ──
def render_bulleted(items: list[str]) -> str

── src/galdr/logic/pure/compose/composed.py ──
def populate_section_buffer(
    content_section: BaseModel,
    data_field_names: frozenset[str],
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> tuple[SectionBuffer, frozenset[str]]

def resolve_all_trunks(
    data_section: BaseModel,
    content_section: BaseModel,
    structure_section: BaseModel,
    display_section: BaseModel | None,
    data_values: dict[str, str],
    consumed_variants: frozenset[str],
) -> list[str]

═══ FILE CONTENT ═══

"""Compose assembled — section composition wiring.

CC=1-2. Wires composed-level processors into a complete section render.
One guard (section gate), then pure wiring calls. Zero other decisions.

Pattern: regin/logic/transform/section_regroup/assembled.py — regroup()
is CC=1, calls 12 functions, zero decisions.
"""

from pydantic import BaseModel

from galdr.logic.pure.compose.composed import (
    populate_section_buffer,
    resolve_all_trunks,
)
from galdr.logic.pure.compose.simple import (
    check_section_gate,
    extract_section_visible,
    render_buffer,
)


def compose_section(
    data_section: BaseModel,
    structure_section: BaseModel,
    content_section: BaseModel,
    display_section: BaseModel | None,
    data_values: dict[str, str],
) -> str | None:
    """Generic section composer. Data drives, content decorates.

    Populates a buffer with heading/preamble/postscript from content,
    fills body from data walk, then renders the buffer in order.
    Returns the section as a markdown string, or None if gated off.
    """
    if not check_section_gate(data_section, extract_section_visible(structure_section)):
        return None
    data_field_names = frozenset(data_section.model_fields.keys())
    buffer, consumed_variants = populate_section_buffer(content_section, data_field_names, structure_section, data_values)
    body = resolve_all_trunks(data_section, content_section, structure_section, display_section, data_values, consumed_variants)
    filled = buffer.model_copy(update={"body": tuple(body)})
    return render_buffer(filled)
