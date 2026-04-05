"""Compose primitives — suffix predicates for buffer slot classification.

CC=1. Single expressions with known-typed string inputs.
Pattern: draupnir/logic/pure/graph_build/primitive.py — ref_prefix,
cache_key_to_defs_key (string partition/replace, no branching).

The positional suffix convention: every content field's terminal suffix
declares which buffer slot it belongs to. These predicates detect
heading, preamble, and closing suffixes. Everything else is body.
"""


def has_heading_suffix(name: str) -> bool:
    """True if name ends with a heading-slot suffix (_heading, _h_variant, or bare 'heading')."""
    return name.endswith(("heading", "_h_variant"))


def has_preamble_suffix(name: str) -> bool:
    """True if name ends with a preamble-slot suffix (_preamble, _p_variant)."""
    return name.endswith(("_preamble", "_p_variant"))


def has_closing_suffix(name: str) -> bool:
    """True if name ends with a closing-slot suffix (_closing, _c_variant)."""
    return name.endswith(("_closing", "_c_variant"))
