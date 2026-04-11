"""Compose composed — generic section processors.

CC=4-8. The composition engine's core loops: classify data annotations,
process section-level content, walk data fields with decoration.

Architecture: data drives, content decorates. See
COMPOSITION_ENGINE_DESIGN.md "Processing Order."

List rendering uses render/simple (bulleted default). Display-aware
format resolution happens at assembled level via render/composed.
"""

from pydantic import BaseModel

from galdr.logic.pure.compose.primitive import (
    has_closing_suffix,
    has_preamble_suffix,
    has_start_suffix,
    is_preprocessing_field,
    strip_structure_control_suffix,
)
from galdr.logic.pure.compose.simple import (
    assemble_buffer,
    buffer_slot_for_field,
    classify_content_slot,
    find_decoration,
    place_display_fields_into_slots,
    find_d1_content_table,
    find_enum_field_name,
    get_visibility_toggle,
    has_enum_discriminator,
    has_scalar_list_field,
    is_compound_list_annotation,
    is_gate_annotation,
    is_list_rootmodel,
    is_basemodel_annotation,
    is_rootmodel_annotation,
    is_toggle_visible,
    list_item_to_string,
    list_item_type,
    render_item_scalar_field,
    resolve_format_pair,
    select_active_roles,
    select_section_variant,
    strip_optional_annotation,
    unwrap_scalar_field,
)
from galdr.logic.pure.render.primitive import heading as render_heading_md
from galdr.structure.model.preprocessing_fields import PreprocessingFields
from galdr.structure.model.section_buffer import SectionBuffer
from galdr.logic.pure.render.simple import render_bulleted
from galdr.logic.pure.template.simple import interpolate
from galdr.structure.gen.output_content import StringTemplate
from galdr.structure.model.section_context import SectionContext


def unwrap_item_fields(item: BaseModel) -> dict[str, str]:
    """Extract all fields from a compound list item as plain strings.

    Iterates item fields, uses annotation-based unwrapping via simple-level
    helpers. Enum → .value, RootModel → peel/join, nested BaseModel → skip.
    """
    values: dict[str, str] = {}
    for field_name, field_info in item.model_fields.items():
        field_value = getattr(item, field_name)
        if field_value is None:
            continue
        result = unwrap_scalar_field(field_value, field_info.annotation)
        if result is not None:
            values[field_name] = result
    return values


def find_entry_template(content_section: BaseModel) -> str | None:
    """Find a content field named *_entry_template with StringTemplate annotation.

    Entry templates define how compound list items render. Returns the
    template string, or None if no entry template exists.
    """
    for content_name, content_field_info in content_section.model_fields.items():
        if not content_name.endswith("_entry_template"):
            continue
        if content_field_info.annotation is not StringTemplate:
            continue
        value = getattr(content_section, content_name)
        if value is not None:
            return value.root
    return None


def has_nested_list_field(item_type: type[BaseModel]) -> bool:
    """True if a BaseModel type has any field that is a list of BaseModels.

    Detects ExampleGroup (example_entries is list of ExampleEntry).
    Does NOT match lists of scalar RootModels (SuccessEvidence is list of StringProse).
    """
    for field_info in item_type.model_fields.values():
        annotation = strip_optional_annotation(field_info.annotation)
        if not is_rootmodel_annotation(annotation):
            continue
        if not is_list_rootmodel(annotation):
            continue
        nested_item = list_item_type(annotation)
        if nested_item is not None and is_basemodel_annotation(nested_item):
            return True
    return False


def collect_list_format(
    trunk: str,
    display_section: BaseModel | None,
    item_count: int,
) -> str:
    """Look up display format for a list trunk, resolve threshold if needed.

    Returns resolved format string ('bulleted', 'numbered', etc.).
    Falls back to 'bulleted' if no display section or no format field.
    Format fields are either FormatPair (RootModel[tuple]) for threshold-based
    switching, or ListFormat (RootModel[str]) for fixed format.
    """
    if display_section is None:
        return "bulleted"
    format_field = getattr(display_section, trunk + "_format", None)
    if format_field is None:
        return "bulleted"
    if hasattr(format_field, "root"):
        threshold_field = getattr(display_section, trunk + "_format_threshold", None)
        if threshold_field is not None and isinstance(format_field.root, tuple):
            above, at_or_below = format_field.root
            return resolve_format_pair(above, at_or_below, item_count, threshold_field.root)
        format_value = format_field.root
        return format_value.value if hasattr(format_value, "value") else str(format_value)
    return format_field.value if hasattr(format_field, "value") else str(format_field)


def classify_compound_list_shape(
    item_type: type[BaseModel],
    content_section: BaseModel,
) -> str:
    """Classify a compound list (BaseModel items) into D1/D2/E shape.

    One content lookup (entry_template). Item type introspection for the rest.
    """
    if find_entry_template(content_section) is not None:
        return "templated_list"
    if has_enum_discriminator(item_type):
        return "enum_list"
    if has_nested_list_field(item_type):
        return "nested_list"
    if has_scalar_list_field(item_type):
        return "framed_list"
    return "nested_list"


def classify_trunk_shape(
    annotation: type,
    content_section: BaseModel,
) -> str:
    """Classify a data field into a rendering shape.

    Returns: 'gate', 'nested', 'scalar', 'simple_list',
    'templated_list', 'enum_list', 'nested_list', 'framed_list'.
    """
    base = classify_data_annotation(annotation)
    if base != "list":
        return base
    cleaned = strip_optional_annotation(annotation)
    if not is_compound_list_annotation(cleaned):
        return "simple_list"
    item_type = list_item_type(cleaned)
    if item_type is None:
        return "simple_list"
    return classify_compound_list_shape(item_type, content_section)


def classify_data_annotation(annotation: type) -> str:
    """Classify a data field annotation: 'gate', 'scalar', 'list', or 'nested'.

    Strips Optional wrapper, then dispatches through simple-level predicates.
    """
    annotation = strip_optional_annotation(annotation)
    if is_gate_annotation(annotation):
        return "gate"
    if is_basemodel_annotation(annotation):
        return "nested"
    if is_rootmodel_annotation(annotation):
        return "list" if is_list_rootmodel(annotation) else "scalar"
    return "scalar"


def render_scalar_value(
    field_name: str,
    field_value: BaseModel,
    content_section: BaseModel,
    data_values: dict[str, str],
) -> str:
    """Render a scalar data field using content templates.

    Scans StringTemplate fields in content for a {{field_name}} placeholder.
    If found, interpolates the template with data values. Otherwise falls
    back to the raw .root value. Uses annotation to identify templates —
    no isinstance on values.
    """
    placeholder = "{{" + field_name + "}}"
    for content_name, content_field_info in content_section.model_fields.items():
        if content_field_info.annotation is not StringTemplate:
            continue
        content_value = getattr(content_section, content_name)
        if content_value is not None and placeholder in content_value.root:
            return interpolate(content_value.root, data_values)
    # Peel nested RootModels (e.g. AgentTitle(RootModel[TitleString]) → str)
    value = field_value.root
    while hasattr(type(value), "model_fields") and "root" in type(value).model_fields:
        value = value.root
    return str(value)




def resolve_heading_text(
    content_section: BaseModel,
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> tuple[str | None, frozenset[str]]:
    """Resolve the section heading and track consumed heading variants.

    Scans content for _start-suffixed fields (section-level heading);
    if the field is a variant sub-table, selects via the matching
    structure selector. Returns (heading_text, consumed_names).
    """
    result: str | None = None
    consumed: set[str] = set()
    for content_name, content_field_info in content_section.model_fields.items():
        if not has_start_suffix(content_name):
            continue
        content_value = getattr(content_section, content_name)
        if content_value is None:
            continue
        if is_basemodel_annotation(content_field_info.annotation):
            selected = select_section_variant(content_name, content_value, structure_section)
            if selected:
                result = interpolate(selected, data_values)
                consumed.add(content_name)
        else:
            result = interpolate(content_value.root, data_values)
    return result, frozenset(consumed)


def populate_section_buffer(
    content_section: BaseModel,
    data_field_names: frozenset[str],
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> tuple[SectionBuffer, frozenset[str]]:
    """Populate heading, preamble, and closing slots from content fields.

    Single pass using terminal suffix classification. Each content field's
    suffix determines its buffer slot:
    - _start → heading (handled by resolve_heading_text)
    - _preamble → preamble slot
    - _closing → closing (postscript) slot
    - Everything else → body (skipped, left for data walk)

    Returns the buffer AND consumed variant names (for body walk).
    """
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
            selected = select_section_variant(content_name, content_value, structure_section)
            if selected:
                items.append((slot, interpolate(selected, data_values)))
                consumed_variants.add(content_name)
        else:
            if is_toggle_visible(get_visibility_toggle(content_name, structure_section)):
                items.append((slot, interpolate(content_value.root, data_values)))
    return assemble_buffer(heading_text, items), frozenset(consumed_variants)


def render_sub_item_fields(sub_item: BaseModel) -> list[str]:
    """Render a nested sub-item (e.g., ExampleEntry) as flat fragments.

    Unwraps each field. Fields ending in _heading or _name render as H4.
    Other fields render as plain text paragraphs.
    """
    fragments: list[str] = []
    sub_values = unwrap_item_fields(sub_item)
    for field_name, text in sub_values.items():
        if field_name.endswith("_heading") or field_name.endswith("_name"):
            fragments.append(render_heading_md(text, 4))
        else:
            fragments.append(text)
    return fragments


def render_item_list_field(field_value: BaseModel, annotation: type) -> list[str]:
    """Render a list field from a structured item.

    Nested BaseModel items → sub-item field rendering (H4 headings + text).
    Scalar items → bulleted list. Returns list of fragments.
    """
    sub_items = field_value.root
    if not sub_items:
        return []
    nested_type = list_item_type(annotation)
    if nested_type is not None and is_basemodel_annotation(nested_type):
        fragments: list[str] = []
        for sub_item in sub_items:
            fragments.extend(render_sub_item_fields(sub_item))
        return fragments
    return [render_bulleted([list_item_to_string(element) for element in sub_items])]


def render_structured_item(
    item: BaseModel,
    section_data_values: dict[str, str],
) -> str:
    """Render a structured compound item with scalar fields and nested lists.

    Handles SuccessItem (definition + evidence list), FailureItem,
    ExampleGroup (name + entries). Checks list fields first to avoid
    compound list stringification, then scalars via unwrap_scalar_field.
    """
    fragments: list[str] = []
    for field_name, field_info in item.model_fields.items():
        field_value = getattr(item, field_name)
        if field_value is None:
            continue
        annotation = strip_optional_annotation(field_info.annotation)
        if is_gate_annotation(annotation):
            continue
        if is_rootmodel_annotation(annotation) and is_list_rootmodel(annotation):
            fragments.extend(render_item_list_field(field_value, annotation))
            continue
        result = unwrap_scalar_field(field_value, annotation)
        if result is not None:
            fragments.append(render_item_scalar_field(field_name, result))
    return "\n\n".join(fragments)


def resolve_role_templates(
    mode_content: BaseModel,
    active_roles: list[str],
    enum_value: str,
    render_values: dict[str, str],
) -> list[str]:
    """Look up enum value in each active role sub-table, interpolate templates."""
    parts: list[str] = []
    for role_name in active_roles:
        role_table = getattr(mode_content, role_name)
        template_field = getattr(role_table, enum_value, None)
        if template_field is not None:
            text = template_field.root if hasattr(template_field, "root") else str(template_field)
            parts.append(interpolate(text, render_values))
    return parts


def render_enum_discriminated_items(
    items: list[BaseModel],
    enum_field_name: str,
    mode_content: BaseModel,
    active_roles: list[str],
    section_data_values: dict[str, str],
) -> list[str]:
    """Generic D1 renderer — render items with enum-keyed role templates.

    For each item: extracts enum value, resolves role templates,
    extracts body text from non-enum fields, joins.
    """
    item_total = str(len(items))
    rendered: list[str] = []
    for index, item in enumerate(items):
        item_values = unwrap_item_fields(item)
        enum_value = item_values.get(enum_field_name, "")
        render_values = {
            **section_data_values,
            **item_values,
            "item_n": str(index + 1),
            "item_total": item_total,
            "step_n": str(index + 1),
            "step_total": item_total,
        }
        parts = resolve_role_templates(mode_content, active_roles, enum_value, render_values)
        parts.extend(text for fname, text in item_values.items() if fname != enum_field_name and text)
        if parts:
            rendered.append("\n\n".join(parts))
    return rendered


def render_decoration_before(
    decoration: dict[str, str],
    data_values: dict[str, str],
) -> list[str]:
    """Render heading/preamble/label decoration fragments before data."""
    fragments: list[str] = []
    for suffix in ("_heading", "_preamble", "_label"):
        if suffix in decoration:
            text = decoration[suffix]
            fragments.append(interpolate(text, data_values) if "{{" in text else text)
    return fragments


def render_decoration_after(
    field_name: str,
    decoration: dict[str, str],
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> list[str]:
    """Render postscript/transition decoration fragments after data, with visibility."""
    fragments: list[str] = []
    for suffix in ("_postscript", "_transition"):
        if suffix in decoration:
            toggle = get_visibility_toggle(field_name + suffix, structure_section)
            if is_toggle_visible(toggle):
                text = decoration[suffix]
                fragments.append(interpolate(text, data_values) if "{{" in text else text)
    return fragments



def render_enum_list(
    field_value: BaseModel,
    content_section: BaseModel,
    data_values: dict[str, str],
) -> list[str]:
    """Render an enum-discriminated list using the D1 template table."""
    items = field_value.root
    enum_fname = find_enum_field_name(type(items[0]))
    mode_table = find_d1_content_table(enum_fname, content_section) if enum_fname else None
    if mode_table is not None:
        active_roles = select_active_roles(mode_table)
        return render_enum_discriminated_items(items, enum_fname, mode_table, active_roles, data_values)
    return [render_structured_item(item, data_values) for item in items]


def render_trunk_body(
    shape: str,
    field_name: str,
    field_value: BaseModel,
    section_context: SectionContext,
) -> list[str]:
    """Dispatch a trunk to its shape-specific renderer. Returns body fragments."""
    if shape == "scalar":
        return [render_scalar_value(field_name, field_value, section_context.content, section_context.data_values)]
    if shape == "simple_list":
        items = field_value.root
        resolved_format = collect_list_format(field_name, section_context.display, len(items))
        return [render_bulleted([list_item_to_string(item) for item in items])]
    if shape == "templated_list":
        entry_template = find_entry_template(section_context.content)
        rendered_entries: list[str] = []
        for item in field_value.root:
            merged = {**section_context.data_values, **unwrap_item_fields(item)}
            rendered_entries.append(interpolate(entry_template, merged))
        return [render_bulleted(rendered_entries)]
    if shape == "enum_list":
        return render_enum_list(field_value, section_context.content, section_context.data_values)
    return [render_structured_item(item, section_context.data_values) for item in field_value.root]


def resolve_all_trunks(
    data_section: BaseModel,
    section_context: SectionContext,
    consumed_variants: frozenset[str],
) -> list[str]:
    """Walk data fields in declaration order, render each by shape.

    Classifies, decorates, renders body, wraps with decoration.
    """
    fragments: list[str] = []
    for field_name, field_info in data_section.model_fields.items():
        field_value = getattr(data_section, field_name)
        if field_value is None:
            continue
        shape = classify_trunk_shape(field_info.annotation, section_context.content)
        if shape in ("gate", "nested"):
            continue
        decoration = find_decoration(field_name, section_context.content)
        fragments.extend(render_decoration_before(decoration, section_context.data_values))
        fragments.extend(render_trunk_body(shape, field_name, field_value, section_context))
        fragments.extend(render_decoration_after(field_name, decoration, section_context.structure, section_context.data_values))
    return fragments


def place_structure_field(
    name: str,
    slots: dict[str, list[tuple[str, str]]],
) -> list[tuple[str, tuple[str, str]]]:
    """Determine which slot(s) a structure field belongs to.

    Selectors are duplicated to every slot containing a matching content
    variant (by prefix). Other structure fields are classified by
    stripping their control suffix and classifying the remainder.
    Returns list of (slot_name, (axis, field_name)) placements.
    """
    if name.endswith("_selector"):
        selector_trunk = name.removesuffix("_selector")
        return [
            (slot_name, ("structure", name))
            for slot_name, entries in slots.items()
            if any(axis == "content" and fname.startswith(selector_trunk) for axis, fname in entries)
        ]
    trunk = strip_structure_control_suffix(name)
    return [(classify_content_slot(trunk), ("structure", name))]


def sort_into_slots(
    content_section: BaseModel,
    data_section: BaseModel,
    structure_section: BaseModel,
    display_section: BaseModel | None,
) -> dict[str, list[tuple[str, str]]]:
    """Sort all fields from all four axes into buffer slots.

    Data first (all body), content second (by positional suffix),
    structure third (by content trunk or selector duplication),
    display last (all body).

    Returns {slot: [(axis, field_name), ...]}.
    """
    slots: dict[str, list[tuple[str, str]]] = {
        "heading": [], "preamble": [], "body": [], "closing": [],
    }
    for name in data_section.model_fields:
        slots["body"].append(("data", name))
    for name in content_section.model_fields:
        slots[classify_content_slot(name)].append(("content", name))
    for name in structure_section.model_fields:
        if is_preprocessing_field(name):
            continue
        for slot_name, entry in place_structure_field(name, slots):
            slots[slot_name].append(entry)
    if display_section is not None:
        slots = place_display_fields_into_slots(display_section, slots)
    return slots


def extract_preprocessing_fields(structure_section: BaseModel) -> PreprocessingFields:
    """Extract pre-processing fields from a structure section into a typed model.

    Pre-processing fields (pre_ prefix) are consumed before slot sorting.
    Not every section has every field — missing fields fall back to defaults
    on PreprocessingFields. Boolean/Integer wrappers unwrap via .root; enum
    wrappers unwrap via .value to their string form.
    """
    visible = getattr(structure_section, "pre_section_visible", None)
    max_entries = getattr(structure_section, "pre_max_entries_rendered", None)
    ordering = getattr(structure_section, "pre_field_ordering", None)
    tier = getattr(structure_section, "pre_scaffolding_tier_override", None)
    return PreprocessingFields(
        section_visible=visible.root if visible is not None else True,
        max_entries_rendered=max_entries.root if max_entries is not None else None,
        field_ordering=ordering.value if ordering is not None else None,
        scaffolding_tier_override=tier.value if tier is not None else None,
    )
