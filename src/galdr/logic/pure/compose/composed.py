"""Compose composed — generic section processors.

CC=4-8. The composition engine's core loops: classify data annotations,
process section-level content, walk data fields with decoration.

Architecture: data drives, content decorates. See
COMPOSITION_ENGINE_DESIGN.md "Processing Order."

List rendering uses render/simple (bulleted default). Display-aware
format resolution happens at assembled level via render/composed.
"""

from pydantic import BaseModel

from galdr.logic.pure.compose.simple import (
    assemble_buffer,
    find_decoration,
    get_visibility_toggle,
    has_enum_discriminator,
    is_body_consumed_content,
    is_compound_list_annotation,
    is_gate_annotation,
    is_list_rootmodel,
    is_nested_annotation,
    process_variant_field,
    slot_for_prose,
    is_rootmodel_annotation,
    is_toggle_visible,
    is_variant_annotation,
    list_item_to_string,
    list_item_type,
    render_content_text,
    render_entries_from_dicts,
    render_item_scalar_field,
    resolve_section_variant,
    strip_optional_annotation,
    template_references_data,
    unwrap_scalar_field,
)
from galdr.logic.pure.render.primitive import heading as render_heading_md
from galdr.structure.model.section_buffer import SectionBuffer
from galdr.logic.pure.render.simple import render_bulleted
from galdr.logic.pure.template.primitive import interpolate
from galdr.structure.gen.output_content import StringTemplate


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
        if nested_item is not None and is_nested_annotation(nested_item):
            return True
    return False


def classify_data_annotation(annotation: type) -> str:
    """Classify a data field annotation: 'gate', 'scalar', 'list', or 'nested'.

    Strips Optional wrapper, then dispatches through simple-level predicates.
    """
    annotation = strip_optional_annotation(annotation)
    if is_gate_annotation(annotation):
        return "gate"
    if is_nested_annotation(annotation):
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


def find_data_driven_templates(
    content_section: BaseModel,
    data_field_names: frozenset[str],
) -> frozenset[str]:
    """Identify content fields that are StringTemplates consumed by the data walk.

    render_scalar_value scans StringTemplate content fields for {{field_name}}.
    This replicates that scan so slot assignment can skip them.
    """
    driven: set[str] = set()
    for content_name, content_field_info in content_section.model_fields.items():
        if content_field_info.annotation is not StringTemplate:
            continue
        content_value = getattr(content_section, content_name)
        if content_value is not None and template_references_data(content_value.root, data_field_names):
            driven.add(content_name)
    return frozenset(driven)



def resolve_heading_text(
    content_section: BaseModel,
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> str | None:
    """Resolve the section heading from content heading field or heading_variant.

    heading_variant (if present and resolvable) overrides the plain heading.
    """
    heading_field = getattr(content_section, "heading", None)
    result = render_content_text(heading_field, data_values) if heading_field is not None else None
    heading_variant = getattr(content_section, "heading_variant", None)
    if heading_variant is not None and is_variant_annotation(type(heading_variant)):
        resolved = resolve_section_variant("heading_variant", heading_variant, structure_section, data_values)
        if resolved:
            result = resolved
    return result


def classify_buffer_field(
    content_name: str,
    annotation: type,
    data_field_names: frozenset[str],
    data_driven: frozenset[str],
) -> str:
    """Classify a content field for buffer population: 'skip', 'variant', or 'prose'."""
    if content_name in ("heading", "heading_variant"):
        return "skip"
    if is_variant_annotation(annotation):
        return "variant"
    if is_body_consumed_content(content_name, data_field_names, data_driven):
        return "skip"
    return "prose"


def populate_section_buffer(
    content_section: BaseModel,
    data_field_names: frozenset[str],
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> SectionBuffer:
    """Populate heading, preamble, and postscript slots from content fields.

    Single pass. Classifies each field, collects (slot, text) tuples for
    variants and prose, then assembles into a SectionBuffer.
    Body-consumed fields (decoration, entry templates, step headers,
    data-driven templates) are skipped — consumed by the data walk.
    """
    data_driven = find_data_driven_templates(content_section, data_field_names)
    heading_text = resolve_heading_text(content_section, structure_section, data_values)
    items: list[tuple[str, str]] = []
    for content_name, content_field_info in content_section.model_fields.items():
        content_value = getattr(content_section, content_name)
        if content_value is None:
            continue
        kind = classify_buffer_field(content_name, content_field_info.annotation, data_field_names, data_driven)
        if kind == "skip":
            continue
        if kind == "variant":
            result = process_variant_field(content_name, content_value, structure_section, data_values, data_field_names)
            if result:
                items.append(result)
            continue
        if not is_toggle_visible(get_visibility_toggle(content_name, structure_section)):
            continue
        items.append((slot_for_prose(content_name, data_field_names), render_content_text(content_value, data_values)))
    return assemble_buffer(heading_text, items)


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
    if nested_type is not None and is_nested_annotation(nested_type):
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


def render_instruction_steps(
    items: list[BaseModel],
    content_section: BaseModel,
    section_data_values: dict[str, str],
) -> list[str]:
    """Render instruction steps with mode-dependent headers and numbering.

    Each step has an Enum discriminator (instruction_mode) and text body.
    Selects header template by mode value, interpolates step_n/step_total.
    """
    step_total = str(len(items))
    rendered: list[str] = []
    for index, item in enumerate(items):
        item_values = unwrap_item_fields(item)
        step_values = {
            **section_data_values,
            **item_values,
            "step_n": str(index + 1),
            "step_total": step_total,
        }
        mode = item_values.get("instruction_mode", "")
        header_key = "step_header_" + mode
        header_template = getattr(content_section, header_key, None)
        step_parts: list[str] = []
        if header_template is not None:
            step_parts.append(interpolate(header_template.root, step_values))
        body_text = item_values.get("instruction_text", "")
        if body_text:
            step_parts.append(body_text)
        if step_parts:
            rendered.append("\n\n".join(step_parts))
    return rendered


def render_compound_list_field(
    items: list[BaseModel],
    content_section: BaseModel,
    data_values: dict[str, str],
) -> list[str]:
    """Route a compound list to the appropriate renderer.

    Priority order:
    1. Enum discriminator → instruction steps (mode headers + numbering)
    2. Entry template exists → flat compound items (template interpolation)
    3. Nested list or scalar list fields → structured items (definition + evidence)
    4. Fallback → join fields with comma
    """
    item_type = type(items[0])
    if has_enum_discriminator(item_type):
        return render_instruction_steps(items, content_section, data_values)
    entry_template = find_entry_template(content_section)
    if entry_template:
        item_dicts = [unwrap_item_fields(item) for item in items]
        return [render_bulleted(render_entries_from_dicts(item_dicts, entry_template, data_values))]
    return [render_structured_item(item, data_values) for item in items]


def render_list_data(
    annotation: type,
    field_value: BaseModel,
    content_section: BaseModel,
    data_values: dict[str, str],
) -> list[str]:
    """Render a list data field — compound or scalar.

    Strips Optional, checks annotation to determine compound vs scalar
    items, delegates to the appropriate renderer.
    """
    items = field_value.root
    if not items:
        return []
    cleaned = strip_optional_annotation(annotation)
    if is_compound_list_annotation(cleaned):
        return render_compound_list_field(items, content_section, data_values)
    return [render_bulleted([list_item_to_string(item) for item in items])]


def process_data_fields(
    data_section: BaseModel,
    content_section: BaseModel,
    structure_section: BaseModel,
    data_values: dict[str, str],
) -> list[str]:
    """Walk data fields in declaration order, attach content decoration.

    Classifies each field by annotation. Skips gates and nested.
    Renders scalars via templates, lists via compound or scalar renderers.
    """
    fragments: list[str] = []
    for field_name, field_info in data_section.model_fields.items():
        field_value = getattr(data_section, field_name)
        if field_value is None:
            continue
        classification = classify_data_annotation(field_info.annotation)
        if classification in ("gate", "nested"):
            continue
        decoration = find_decoration(field_name, content_section)
        fragments.extend(render_decoration_before(decoration, data_values))
        if classification == "scalar":
            fragments.append(render_scalar_value(field_name, field_value, content_section, data_values))
        elif classification == "list":
            fragments.extend(render_list_data(field_info.annotation, field_value, content_section, data_values))
        fragments.extend(render_decoration_after(field_name, decoration, structure_section, data_values))
    return fragments


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
