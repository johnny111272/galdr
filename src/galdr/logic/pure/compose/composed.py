"""Compose composed — the generic section walker.

CC=4-8. Walks data fields in declaration order, finds content
decoration by trunk matching, renders each field with the
appropriate operation. Processes ALL sections identically.

Pattern: draupnir/logic/pure/graph_build/composed.py — extract_refs
(stack-based walker with isinstance dispatch inside the loop).

Architecture: data drives, content decorates. This function walks
the DATA model's fields. Content fields attach via trunk naming.
See COMPOSITION_ENGINE_DESIGN.md "Processing Order."
"""

from enum import Enum

from pydantic import BaseModel, RootModel

from galdr.logic.pure.compose.primitive import format_key, strip_suffix, threshold_key
from galdr.logic.pure.compose.simple import (
    check_section_gate,
    find_decoration,
    is_visible_by_mode,
    resolve_format_pair,
    select_variant,
)
from galdr.logic.pure.render.primitive import heading
from galdr.logic.pure.render.simple import (
    render_bare_list,
    render_bulleted,
    render_inline_list,
    render_numbered,
    render_prose_list,
)
from galdr.logic.pure.template.primitive import interpolate
from galdr.structure.gen.output_display import FormatPair, ListFormat, UnionFormatOrPair


def compose_section(
    section_name: str,
    data_section: BaseModel,
    structure_section: BaseModel,
    content_section: BaseModel,
    display_section: BaseModel | None,
    data_values: dict[str, str],
) -> str | None:
    """Generic section composer. Data drives, content decorates.

    Returns the section as a markdown string, or None if gated off.
    Every section is processed by this ONE function — it never asks
    which section it is.
    """
    # Section gate: check data presence + section_visible toggle
    visible_field = getattr(structure_section, "section_visible", None)
    section_visible = visible_field.root if isinstance(visible_field, RootModel) else True
    if not check_section_gate(data_section, section_visible):
        return None

    fragments: list[str] = []

    # Section heading from content
    content_heading = getattr(content_section, "heading", None)
    if content_heading is not None:
        heading_text = content_heading.root
        heading_rendered = interpolate(heading_text, data_values)
        fragments.append(heading(heading_rendered, 2))

    # Collect data field names for trunk matching
    data_field_names = set(data_section.model_fields.keys())

    # Process content fields: section-level prose (no data trunk match)
    for content_name, content_info in content_section.model_fields.items():
        if content_name == "heading":
            continue
        content_value = getattr(content_section, content_name)
        if content_value is None:
            continue

        # Check if this is a variant sub-table (BaseModel, not a string type)
        if isinstance(content_value, BaseModel) and not isinstance(content_value, RootModel):
            # Variant: look up selector in structure, pick prose
            selector = getattr(structure_section, content_name, None)
            if selector is not None:
                selector_str = selector.value if isinstance(selector, Enum) else selector
                selected = select_variant(content_value, selector_str)
                if selected:
                    fragments.append(interpolate(selected, data_values) if "{{" in selected else selected)
            continue

        # Check if trunk matches a data field (field-level decoration — skip here, handled in data walk)
        trunk = None
        for suffix in ("_heading", "_preamble", "_label", "_postscript", "_transition"):
            if content_name.endswith(suffix):
                trunk = strip_suffix(content_name, suffix)
                break
        if trunk and trunk in data_field_names:
            continue

        # Section-level content: check visibility, render
        vis_key = content_name + "_visible"
        vis_toggle = getattr(structure_section, vis_key, None)
        if vis_toggle is not None:
            vis_val = vis_toggle.root if isinstance(vis_toggle, RootModel) else vis_toggle
            if isinstance(vis_val, bool) and not vis_val:
                continue
            if isinstance(vis_val, str) and not is_visible_by_mode(vis_val):
                continue

        text = content_value.root
        rendered = interpolate(text, data_values) if "{{" in text else text
        fragments.append(rendered)

    # Data walk: iterate data fields in declaration order
    for field_name in data_section.model_fields:
        field_value = getattr(data_section, field_name)
        if field_value is None:
            continue

        # Skip gates (bool, enum used for branching)
        if isinstance(field_value, bool):
            continue
        if isinstance(field_value, Enum):
            continue
        if isinstance(field_value, RootModel) and isinstance(field_value.root, bool):
            continue

        # Find content decoration for this field's trunk
        decoration = find_decoration(field_name, content_section)

        # Render decoration before
        for suffix in ("_heading", "_preamble", "_label"):
            if suffix in decoration:
                dec_text = decoration[suffix]
                fragments.append(interpolate(dec_text, data_values) if "{{" in dec_text else dec_text)

        # Render the data value
        if isinstance(field_value, RootModel):
            root = field_value.root
            if isinstance(root, (list, tuple)):
                # List field: format per display
                items = [item.root if isinstance(item, RootModel) else str(item) for item in root]
                list_format = _resolve_display_format(display_section, field_name, len(items))
                fragments.append(_render_list_by_format(items, list_format))
            elif isinstance(root, str):
                # Scalar in template or bare
                template = _find_template_for_field(field_name, content_section, data_values)
                if template:
                    fragments.append(template)
                else:
                    fragments.append(root)
        elif isinstance(field_value, BaseModel):
            # Nested model — handled by specific sub-block logic if needed
            pass

        # Render decoration after
        for suffix in ("_postscript", "_transition"):
            if suffix in decoration:
                dec_text = decoration[suffix]
                vis_key = field_name + suffix.replace("_", "_", 1) + "_visible"
                vis = getattr(structure_section, vis_key, None)
                visible = True
                if vis is not None:
                    vis_val = vis.root if isinstance(vis, RootModel) else vis
                    if isinstance(vis_val, bool):
                        visible = vis_val
                    elif isinstance(vis_val, str):
                        visible = is_visible_by_mode(vis_val)
                if visible:
                    fragments.append(interpolate(dec_text, data_values) if "{{" in dec_text else dec_text)

    return "\n\n".join(fragments) if fragments else None


def _resolve_display_format(
    display_section: BaseModel | None,
    trunk: str,
    count: int,
) -> ListFormat:
    """Resolve the display format for a list field."""
    if display_section is None:
        return ListFormat.bulleted
    format_field = getattr(display_section, format_key(trunk), None)
    if format_field is None:
        return ListFormat.bulleted
    inner = format_field.root if isinstance(format_field, UnionFormatOrPair) else format_field
    if isinstance(inner, ListFormat):
        return inner
    if isinstance(inner, FormatPair):
        threshold_field = getattr(display_section, threshold_key(trunk), None)
        threshold = threshold_field.root if threshold_field is not None and hasattr(threshold_field, "root") else 3
        return resolve_format_pair(inner.root[0], inner.root[1], count, threshold)
    return ListFormat.bulleted


def _render_list_by_format(items: list[str], list_format: ListFormat) -> str:
    """Dispatch to the correct simple-level list renderer."""
    if list_format == ListFormat.bulleted:
        return render_bulleted(items)
    if list_format == ListFormat.numbered:
        return render_numbered(items)
    if list_format == ListFormat.inline:
        return render_inline_list(items)
    if list_format == ListFormat.prose:
        return render_prose_list(items)
    return render_bare_list(items)


def _find_template_for_field(
    field_name: str,
    content_section: BaseModel,
    data_values: dict[str, str],
) -> str | None:
    """Find a content template that references this data field and render it.

    Scans content fields for templates containing {{field_name}}.
    Returns the interpolated string, or None if no template references this field.
    """
    placeholder = "{{" + field_name + "}}"
    for content_name in content_section.model_fields:
        content_value = getattr(content_section, content_name)
        if content_value is None:
            continue
        if not isinstance(content_value, RootModel):
            continue
        text = content_value.root
        if isinstance(text, str) and placeholder in text:
            return interpolate(text, data_values)
    return None
