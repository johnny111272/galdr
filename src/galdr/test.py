═══ INJECTION (full) ═══

── src/galdr/logic/pure/compose/primitive.py ──
def has_preamble_suffix(name: str) -> bool:
    return name.endswith(("_preamble", "_p_variant"))

def has_closing_suffix(name: str) -> bool:
    return name.endswith(("_closing", "_c_variant"))

def has_heading_suffix(name: str) -> bool:
    return name.endswith(("heading", "_h_variant"))

── src/galdr/logic/pure/render/primitive.py ──
def heading(text: str, level: int) -> str:
    return f"{'#' * level} {text}"

def bold(text: str) -> str:
    return f"**{text}**"

def bullet_item(text: str) -> str:
    return f"- {text}"

def numbered_item(text: str, position: int) -> str:
    return f"{position}. {text}"

── src/galdr/logic/pure/template/primitive.py ──
def interpolate(template: str, values: dict[str, str]) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1).lower(), m.group(0)), template)

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
) -> ListFormat:
    return above if count > threshold else at_or_below

def find_decoration(trunk: str, content_model: BaseModel) -> dict[str, str]:
    decoration: dict[str, str] = {}
    for suffix in ("_heading", "_preamble", "_label", "_postscript", "_transition"):
        field = getattr(content_model, trunk + suffix, None)
        if field is not None:
            decoration[suffix] = field.root
    return decoration

def is_gate_annotation(annotation: type) -> bool:
    return is_bool_gate_annotation(annotation) or is_enum_annotation(annotation)

def is_rootmodel_annotation(annotation: type) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, RootModel)

def is_basemodel_annotation(annotation: type) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, BaseModel) and not issubclass(annotation, RootModel)

def is_list_rootmodel(rootmodel_type: type[RootModel]) -> bool:
    return get_origin(rootmodel_type.model_fields["root"].annotation) is list

def list_item_type(rootmodel_type: type[RootModel]) -> type | None:
    inner = rootmodel_inner_type(rootmodel_type)
    if get_origin(inner) is list:
        args = get_args(inner)
        return args[0] if args else None
    return None

def is_compound_list_annotation(annotation: type) -> bool:
    if not is_rootmodel_annotation(annotation):
        return False
    item_t = list_item_type(annotation)
    return item_t is not None and is_basemodel_annotation(item_t)

def unwrap_scalar_field(field_value: BaseModel, annotation: type) -> str | None:
    cleaned = strip_optional_annotation(annotation)
    if is_enum_annotation(cleaned):
        return field_value.value
    if is_rootmodel_annotation(cleaned):
        return unwrap_rootmodel_field(field_value, cleaned)
    return None

def select_active_roles(mode_content: BaseModel) -> list[str]:
    active: list[str] = []
    for role_name in mode_content.model_fields:
        if not is_role_alternative(role_name, active):
            active.append(role_name)
    return active

def find_d1_content_table(
    enum_field_name: str,
    content_section: BaseModel,
) -> BaseModel | None:
    content_value = getattr(content_section, enum_field_name, None)
    if content_value is not None and is_basemodel_annotation(type(content_value)):
        return content_value
    return None

def find_enum_field_name(item_type: type[BaseModel]) -> str | None:
    for field_name, field_info in item_type.model_fields.items():
        if is_enum_annotation(field_info.annotation):
            return field_name
    return None

def has_enum_discriminator(item_type: type[BaseModel]) -> bool:
    for field_info in item_type.model_fields.values():
        if is_enum_annotation(field_info.annotation):
            return True
    return False

def has_scalar_list_field(item_type: type[BaseModel]) -> bool:
    for field_info in item_type.model_fields.values():
        if is_scalar_list_annotation(strip_optional_annotation(field_info.annotation)):
            return True
    return False

def strip_optional_annotation(annotation: type) -> type:
    if get_origin(annotation) is not type(int | str):
        return annotation
    args = get_args(annotation)
    return args[0] if args[0] is not type(None) else args[1]

def render_item_scalar_field(field_name: str, text: str) -> str:
    if field_name.endswith("_name") or field_name.endswith("_heading"):
        return heading(text, 3)
    return text

def render_entries_from_dicts(
    item_dicts: list[dict[str, str]],
    entry_template: str,
    section_data_values: dict[str, str],
) -> list[str]:
    rendered: list[str] = []
    for item_values in item_dicts:
        merged = {**section_data_values, **item_values}
        rendered.append(interpolate(entry_template, merged))
    return rendered

def render_content_text(content_value: RootModel, data_values: dict[str, str]) -> str:
    text = content_value.root
    return interpolate(text, data_values) if "{{" in text else text

def assemble_buffer(
    heading_text: str | None,
    items: list[tuple[str, str]],
) -> "SectionBuffer":
    from galdr.structure.model.section_buffer import SectionBuffer

    return SectionBuffer(
        heading=heading(heading_text, 2) if heading_text else None,
        preamble=items_for_slot(items, "preamble"),
        postscript=items_for_slot(items, "postscript"),
    )

def buffer_slot_for_field(content_name: str) -> str | None:
    if has_preamble_suffix(content_name):
        return "preamble"
    if has_closing_suffix(content_name):
        return "postscript"
    return None

def resolve_section_variant(
    content_name: str,
    content_value: BaseModel,
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> str | None:
    selector = getattr(structure_section, content_name, None)
    if selector is None:
        return None
    return render_variant(content_value, get_enum_string(selector), data_values)

def list_item_to_string(item: BaseModel) -> str:
    value = item
    while hasattr(type(value), "model_fields") and "root" in type(value).model_fields:
        value = value.root
    return str(value)

def get_visibility_toggle(content_name: str, structure_section: BaseModel) -> str | bool | None:
    field_key = content_name + "_visible"
    if field_key not in structure_section.model_fields:
        return None
    toggle = getattr(structure_section, field_key)
    if toggle is None:
        return None
    return extract_field_value(toggle)

def is_toggle_visible(toggle_value: str | bool | None) -> bool:
    if toggle_value is None:
        return True
    if isinstance(toggle_value, str):
        return is_visible_by_mode(toggle_value)
    return bool(toggle_value)

def check_section_gate(data_section: BaseModel | None, section_visible: bool) -> bool:
    return data_section is not None and section_visible

def extract_section_visible(structure_section: BaseModel) -> bool:
    toggle = getattr(structure_section, "section_visible", None)
    if toggle is None:
        return True
    return bool(toggle.root)

def render_buffer(buffer: BaseModel) -> str | None:
    parts: list[str] = []
    if buffer.heading:
        parts.append(buffer.heading)
    parts.extend(buffer.preamble)
    parts.extend(buffer.body)
    parts.extend(buffer.postscript)
    return "\n\n".join(parts) if parts else None

── src/galdr/logic/pure/render/simple.py ──
def render_bulleted(items: list[str]) -> str:
    return "\n".join(bullet_item(item) for item in items)

── src/galdr/logic/pure/compose/composed.py ──
def populate_section_buffer(
    content_section: BaseModel,
    data_field_names: frozenset[str],
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> tuple[SectionBuffer, frozenset[str]]:
    heading_text, heading_consumed = resolve_heading_text(content_section, structure_section, data_values)
    items: list[tuple[str, str]] = []
    consumed_variants: set[str] = set(heading_consumed)
    for content_name, content_field_info in content_section.model_fields.items():
        content_value = getattr(content_section, content_name)
        if content_value is None:
            continue
        slot = buffer_slot_for_field(content_name)
        if slot is None:
            continue
        if is_basemodel_annotation(content_field_info.annotation):
            rendered = resolve_section_variant(content_name, content_value, structure_section, data_values)
            if rendered:
                items.append((slot, rendered))
                consumed_variants.add(content_name)
        else:
            if is_toggle_visible(get_visibility_toggle(content_name, structure_section)):
                items.append((slot, render_content_text(content_value, data_values)))
    return assemble_buffer(heading_text, items), frozenset(consumed_variants)

def resolve_all_trunks(
    data_section: BaseModel,
    content_section: BaseModel,
    structure_section: BaseModel,
    display_section: BaseModel | None,
    data_values: dict[str, str],
    consumed_variants: frozenset[str],
) -> list[str]:
    fragments: list[str] = []
    for field_name, field_info in data_section.model_fields.items():
        field_value = getattr(data_section, field_name)
        if field_value is None:
            continue
        shape = classify_trunk_shape(field_info.annotation, content_section)
        if shape in ("gate", "nested"):
            continue
        decoration = find_decoration(field_name, content_section)
        fragments.extend(render_decoration_before(decoration, data_values))
        fragments.extend(render_trunk_body(shape, field_name, field_value, content_section, display_section, data_values))
        fragments.extend(render_decoration_after(field_name, decoration, structure_section, data_values))
    return fragments

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
