"""Compose simple — single-decision helpers for section composition.

CC=1-3. Each function takes already-resolved plain values (not raw
model attributes). The composed-level walker handles RootModel
unwrapping and type dispatch before calling these.

Pattern: regin/logic/transform/section_regroup/simple.py — guard_return_field
(single gate, plain types), wrap_nullable (None guard + delegate).
"""

from pydantic import BaseModel

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
    """Look up selector value as attribute on a variant sub-table model."""
    return getattr(variant_model, selector_value, "")


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
