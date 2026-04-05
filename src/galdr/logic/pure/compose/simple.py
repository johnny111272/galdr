"""Compose simple — single-decision helpers for section composition.

CC=1-3. Each function takes already-resolved plain values (not raw
model attributes). The composed-level walker handles RootModel
unwrapping and type dispatch before calling these.

Annotation classification: the schema metadata tells us field types
without runtime isinstance on values. Gates validated everything —
inside the sandbox, all types are known by construction.

Pattern: regin/logic/transform/section_regroup/simple.py — guard_return_field
(single gate, plain types), wrap_nullable (None guard + delegate).
"""

from enum import Enum
from typing import Annotated, get_args, get_origin

from pydantic import BaseModel, RootModel

from galdr.logic.pure.compose.primitive import has_closing_suffix, has_preamble_suffix, strip_suffix
from galdr.logic.pure.render.primitive import heading
from galdr.logic.pure.template.primitive import interpolate
from galdr.structure.gen.output_content import StringTemplate
from galdr.structure.gen.output_display import FormatPair, ListFormat


def is_visible_by_mode(mode: str) -> bool:
    """Check a VisibilityMode string: 'never' → False, else True.

    'auto' returns True here — the count threshold check is separate.
    'always' returns True. Absent toggles never reach this function.
    """
    return mode != "never"


def resolve_format_pair(
    above: ListFormat,
    at_or_below: ListFormat,
    count: int,
    threshold: int,
) -> ListFormat:
    """Pick format from a threshold pair based on item count."""
    return above if count > threshold else at_or_below




def select_variant(variant_model: BaseModel, selector_value: str) -> str:
    """Look up selector value as attribute on a variant sub-table model.

    Variant field values are RootModel[str] wrappers — extract_field_value
    unwraps to the plain string. Returns empty string if selector not found.
    """
    field_value = getattr(variant_model, selector_value, None)
    if field_value is None:
        return ""
    return str(extract_field_value(field_value))


def find_decoration(trunk: str, content_model: BaseModel) -> dict[str, str]:
    """Find content fields matching a data trunk name.

    Checks for {trunk}_heading, _preamble, _label, _postscript, _transition.
    Returns dict of {suffix: value_string} for fields that are present.
    Values are accessed via .root (all content fields are RootModel[str]).
    """
    decoration: dict[str, str] = {}
    for suffix in ("_heading", "_preamble", "_label", "_postscript", "_transition"):
        field = getattr(content_model, trunk + suffix, None)
        if field is not None:
            decoration[suffix] = field.root
    return decoration


def check_section_gate(data_section: BaseModel | None, section_visible: bool) -> bool:
    """Check if a section should render: data present + visibility toggle."""
    return data_section is not None and section_visible


# --- Annotation classification ---


def rootmodel_inner_type(annotation: type) -> type | None:
    """Extract the inner type from a RootModel annotation.

    RootModel fields use Annotated wrappers (e.g., root: Annotated[bool, ...]).
    Strips the Annotated layer to return the bare inner type.
    Returns None if model_fields lacks 'root'.
    """
    root_info = annotation.model_fields.get("root")
    if root_info is None:
        return None
    inner = root_info.annotation
    if get_origin(inner) is Annotated:
        inner = get_args(inner)[0]
    return inner


def is_enum_annotation(annotation: type) -> bool:
    """True if the annotation is an Enum subclass."""
    return isinstance(annotation, type) and issubclass(annotation, Enum)


def is_bool_gate_annotation(annotation: type) -> bool:
    """True if annotation is bool or RootModel[bool] (e.g., Boolean).

    Boolean gates in the data model are wrapped as RootModel[bool].
    Checks both bare bool and the RootModel inner type.
    """
    if annotation is bool:
        return True
    if is_rootmodel_annotation(annotation):
        return rootmodel_inner_type(annotation) is bool
    return False


def is_gate_annotation(annotation: type) -> bool:
    """True if the annotation is a gate type (bool, RootModel[bool], or Enum).

    Gate fields drive branching logic, not rendered content.
    They are skipped by the data walk.
    """
    return is_bool_gate_annotation(annotation) or is_enum_annotation(annotation)


def is_rootmodel_annotation(annotation: type) -> bool:
    """True if the annotation is a RootModel subclass.

    RootModel fields carry rendered data — scalars or lists.
    """
    return isinstance(annotation, type) and issubclass(annotation, RootModel)


def is_nested_annotation(annotation: type) -> bool:
    """True if the annotation is a non-RootModel BaseModel (nested section).

    Nested models are skipped by the walker — handled by orchestrate.
    """
    return isinstance(annotation, type) and issubclass(annotation, BaseModel) and not issubclass(annotation, RootModel)


def is_list_rootmodel(rootmodel_type: type[RootModel]) -> bool:
    """True if a RootModel's inner type is a list.

    Checks the root field's annotation origin. list origin = list field,
    otherwise = scalar field.
    """
    return get_origin(rootmodel_type.model_fields["root"].annotation) is list


def list_item_type(rootmodel_type: type[RootModel]) -> type | None:
    """Extract the item type from a RootModel[list[T]] annotation.

    Returns T if the RootModel wraps a list, None otherwise.
    Strips Annotated wrappers from the root field annotation.
    """
    inner = rootmodel_inner_type(rootmodel_type)
    if get_origin(inner) is list:
        args = get_args(inner)
        return args[0] if args else None
    return None


def is_compound_list_annotation(annotation: type) -> bool:
    """True if annotation is a RootModel[list[BaseModel]] (compound items).

    Compound list items are full BaseModels (not RootModels) — they need
    per-item field unwrapping and template rendering instead of simple
    RootModel peeling.
    """
    if not is_rootmodel_annotation(annotation):
        return False
    item_t = list_item_type(annotation)
    return item_t is not None and is_nested_annotation(item_t)


def unwrap_rootmodel_field(field_value: RootModel, annotation: type) -> str:
    """Unwrap a RootModel field: list items joined, scalars peeled."""
    if is_list_rootmodel(annotation):
        return ", ".join(list_item_to_string(element) for element in field_value.root)
    return list_item_to_string(field_value)


def unwrap_scalar_field(field_value: BaseModel, annotation: type) -> str | None:
    """Unwrap a single typed field to a string. None if not representable.

    Enum → .value, RootModel → peel. Non-RootModel BaseModel → None.
    Does NOT guard against compound lists — caller must check first.
    """
    cleaned = strip_optional_annotation(annotation)
    if is_enum_annotation(cleaned):
        return field_value.value
    if is_rootmodel_annotation(cleaned):
        return unwrap_rootmodel_field(field_value, cleaned)
    return None


def is_role_alternative(role_name: str, earlier_roles: list[str]) -> bool:
    """True if role_name is an alternative of an earlier role (shared prefix + underscore)."""
    for earlier in earlier_roles:
        if role_name.startswith(earlier + "_"):
            return True
    return False


def select_active_roles(mode_content: BaseModel) -> list[str]:
    """Select non-alternative roles from a D1 template table.

    Roles sharing a prefix with an earlier role are alternatives (e.g.,
    header_n_only is an alternative of header). Only the first is active.
    """
    active: list[str] = []
    for role_name in mode_content.model_fields:
        if not is_role_alternative(role_name, active):
            active.append(role_name)
    return active


def find_d1_content_table(
    enum_field_name: str,
    content_section: BaseModel,
) -> BaseModel | None:
    """Find a D1 template table on the content section matching the enum field name.

    D1 tables are non-RootModel BaseModel fields without _variant suffix,
    named after the data item's enum field.
    """
    content_value = getattr(content_section, enum_field_name, None)
    if content_value is not None and is_variant_annotation(type(content_value)):
        return content_value
    return None


def find_enum_field_name(item_type: type[BaseModel]) -> str | None:
    """Find the name of the first Enum field on a BaseModel type. None if no Enum field."""
    for field_name, field_info in item_type.model_fields.items():
        if is_enum_annotation(field_info.annotation):
            return field_name
    return None


def has_enum_discriminator(item_type: type[BaseModel]) -> bool:
    """True if a BaseModel type has an Enum field (mode discriminator).

    Used to detect InstructionStep (has instruction_mode Enum) which
    needs mode-dependent header templates and per-step numbering.
    """
    for field_info in item_type.model_fields.values():
        if is_enum_annotation(field_info.annotation):
            return True
    return False


def is_scalar_list_annotation(annotation: type) -> bool:
    """True if annotation is a RootModel list of scalar (non-BaseModel) items."""
    if not is_rootmodel_annotation(annotation):
        return False
    return is_list_rootmodel(annotation) and not is_compound_list_annotation(annotation)


def has_scalar_list_field(item_type: type[BaseModel]) -> bool:
    """True if a BaseModel type has a list field of scalar RootModels.

    Detects SuccessItem/FailureItem (evidence is list of StringProse).
    """
    for field_info in item_type.model_fields.values():
        if is_scalar_list_annotation(strip_optional_annotation(field_info.annotation)):
            return True
    return False


def strip_optional_annotation(annotation: type) -> type:
    """If annotation is X | None, return X. Otherwise return unchanged.

    For Optional fields in the data model. The walker skips None values
    before classification, so we only need the non-None type.
    """
    if get_origin(annotation) is not type(int | str):
        return annotation
    args = get_args(annotation)
    return args[0] if args[0] is not type(None) else args[1]


def render_item_scalar_field(field_name: str, text: str) -> str:
    """Render a scalar from a structured item — title-like fields as H3."""
    if field_name.endswith("_name") or field_name.endswith("_heading"):
        return heading(text, 3)
    return text


def render_entries_from_dicts(
    item_dicts: list[dict[str, str]],
    entry_template: str,
    section_data_values: dict[str, str],
) -> list[str]:
    """Render pre-unwrapped item dicts through an entry template.

    Merges each item's values with section data values, then interpolates.
    Returns list of rendered strings (one per item).
    """
    rendered: list[str] = []
    for item_values in item_dicts:
        merged = {**section_data_values, **item_values}
        rendered.append(interpolate(entry_template, merged))
    return rendered


def render_content_text(content_value: RootModel, data_values: dict[str, str]) -> str:
    """Render a single content text field — interpolate if template, else passthrough."""
    text = content_value.root
    return interpolate(text, data_values) if "{{" in text else text


def get_enum_string(selector: Enum | str) -> str:
    """Extract string value from an enum selector or pass through a string."""
    return selector.value if isinstance(selector, Enum) else str(selector)


def render_variant(
    variant_model: BaseModel,
    selector_value: str,
    data_values: dict[str, str],
) -> str | None:
    """Select and render a variant prose alternative. None if empty."""
    selected = select_variant(variant_model, selector_value)
    if not selected:
        return None
    return interpolate(selected, data_values) if "{{" in selected else selected




def items_for_slot(items: list[tuple[str, str]], slot: str) -> tuple[str, ...]:
    """Filter (slot, text) tuples to just the texts matching a slot name."""
    return tuple(text for slot_name, text in items if slot_name == slot)


def assemble_buffer(
    heading_text: str | None,
    items: list[tuple[str, str]],
) -> "SectionBuffer":
    """Build a SectionBuffer from a heading and a list of (slot, text) tuples."""
    from galdr.structure.model.section_buffer import SectionBuffer

    return SectionBuffer(
        heading=heading(heading_text, 2) if heading_text else None,
        preamble=items_for_slot(items, "preamble"),
        postscript=items_for_slot(items, "postscript"),
    )


def buffer_slot_for_field(content_name: str) -> str | None:
    """Return buffer slot for a non-heading content field, or None if body-consumed.

    Uses terminal suffix: _preamble/_p_variant → 'preamble',
    _closing/_c_variant → 'postscript'. Everything else → None (body).
    """
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
    """Resolve a variant sub-table field: find selector in structure, pick and render.

    Returns the rendered variant prose, or None if no selector or empty selection.
    """
    selector = getattr(structure_section, content_name, None)
    if selector is None:
        return None
    return render_variant(content_value, get_enum_string(selector), data_values)


def list_item_to_string(item: BaseModel) -> str:
    """Extract a string from a list item by peeling RootModel wrappers.

    Peels nested RootModels until reaching a plain value, then stringifies.
    BaseModel items without 'root' are stringified directly.
    """
    value = item
    while hasattr(type(value), "model_fields") and "root" in type(value).model_fields:
        value = value.root
    return str(value)


def extract_field_value(field_value: BaseModel | Enum) -> str | bool:
    """Extract plain value from a structure field.

    Enum fields use .value. RootModel/BaseModel fields use .root.
    Enum check first since Enums don't have model_fields.
    """
    if isinstance(field_value, Enum):
        return field_value.value
    return field_value.root


def join_fragments(fragments: list[str]) -> str | None:
    """Join rendered fragments with double newlines. None if empty."""
    return "\n\n".join(fragments) if fragments else None


def extract_section_visible(structure_section: BaseModel) -> bool:
    """Get the section_visible toggle from structure, defaulting to True.

    Only guardrails family sections have this toggle. All others default visible.
    Structure toggle fields are RootModel wrappers — .root is always present.
    """
    toggle = getattr(structure_section, "section_visible", None)
    if toggle is None:
        return True
    return bool(toggle.root)


def render_section_heading(content_section: BaseModel, data_values: dict[str, str]) -> list[str]:
    """Render the section heading from content if present. Returns [] or [heading_str].

    Returning a list instead of Optional avoids a branch in the assembled wiring.
    """
    content_heading = getattr(content_section, "heading", None)
    if content_heading is None:
        return []
    return [heading(render_content_text(content_heading, data_values), 2)]




def get_visibility_toggle(content_name: str, structure_section: BaseModel) -> str | bool | None:
    """Get the raw visibility toggle value for a content field.

    Looks up {content_name}_visible in structure. Returns None if no toggle.
    Uses extract_field_value to unwrap RootModel or Enum uniformly.
    """
    field_key = content_name + "_visible"
    if field_key not in structure_section.model_fields:
        return None
    toggle = getattr(structure_section, field_key)
    if toggle is None:
        return None
    return extract_field_value(toggle)


def is_toggle_visible(toggle_value: str | bool | None) -> bool:
    """Resolve a visibility toggle value to a boolean.

    None = visible (no toggle defined). Bool = direct. String = mode check
    via is_visible_by_mode ('never' → False, everything else → True).
    """
    if toggle_value is None:
        return True
    if isinstance(toggle_value, str):
        return is_visible_by_mode(toggle_value)
    return bool(toggle_value)


def is_variant_annotation(annotation: type) -> bool:
    """True if a content field annotation is a variant sub-table type.

    Variant sub-tables are BaseModel subclasses that are NOT RootModel.
    Uses annotation inspection, not isinstance on values.
    """
    return isinstance(annotation, type) and issubclass(annotation, BaseModel) and not issubclass(annotation, RootModel)


def render_buffer(buffer: BaseModel) -> str | None:
    """Render a populated SectionBuffer to markdown.

    Joins heading + preamble + body + postscript with double newlines.
    Returns None if all slots are empty.
    """
    parts: list[str] = []
    if buffer.heading:
        parts.append(buffer.heading)
    parts.extend(buffer.preamble)
    parts.extend(buffer.body)
    parts.extend(buffer.postscript)
    return "\n\n".join(parts) if parts else None
