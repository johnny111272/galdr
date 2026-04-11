"""Body suffix coverage probe.

NOT PRODUCTION CODE. Non-permanent measurement tool.

Question: of every field that currently lands in the body slot, how
many have a recognizable positional suffix and how many don't? The
current slot classifier only positively recognizes section_heading,
_preamble, and _closing — everything else falls through to body. This
probe looks at what's actually in body and tells us which entries
would still be body under a positive classifier and which would land
as unknown.

Axes handled:
  data      — trunks, no suffix check (data goes to body by rule)
  content   — strip _template / _variant modifiers, then check
  structure — strip _visible / _selector / _override / _auto_threshold,
              then strip modifiers, then check
  display   — strip _format / _format_threshold / _visibility_threshold
              / _activation_threshold, then strip modifiers, then check

Known body positional suffixes (from TOML_ARCHITECTURE.md and
08_NAMING_REQUIREMENTS.md):
  _heading       — sub-heading in body (section_heading already split
                   off by the existing classifier)
  _label
  _declaration
  _intro
  _entry_template — compound; must be checked on the RAW name before
                    modifier strip would reduce it to _entry
  _separator
  _postscript
  _transition
  _body          — explicit standalone body marker

Output:
  Per section, body breakdown by role (data, and each known suffix).
  Plus a section for unknown names — axis:name, axis, raw trunk after
  stripping. These are the candidates for either a schema rename or a
  new predicate.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(Path.home() / ".ai" / "tools" / "lib"))

from galdr.logic.orchestrate.compose.orchestrate import load_all_inputs
from galdr.logic.pure.compose.composed import sort_into_slots
from galdr.logic.pure.compose.primitive import (
    strip_display_control_suffix,
    strip_modifiers,
    strip_structure_control_suffix,
)
from galdr.structure.gen.output_content import AgentOutputContent

BODY_SUFFIXES = (
    "_label",
    "_declaration",
    "_intro",
    "_entry_template",  # checked on raw name before modifier strip
    "_separator",
    "_postscript",
    "_transition",
    "_body",
    "_heading",  # sub-heading — not section_heading (that goes to heading slot)
)

DEFAULT_DATA_PATH = Path.home() / ".ai" / "spaces" / "bragi" / "definitions" / "agents" / "agent-builder" / "anthropic_render.toml"
DEFAULT_CONTENT_PATH = REPO_ROOT / "extracted" / "content.toml"
DEFAULT_STRUCTURE_PATH = REPO_ROOT / "extracted" / "structure.toml"
DEFAULT_DISPLAY_PATH = REPO_ROOT / "extracted" / "display.toml"


def effective_name(axis: str, name: str) -> str:
    """Strip the control suffix for the axis, then strip modifiers."""
    if axis == "content":
        base = name
    elif axis == "structure":
        base = strip_structure_control_suffix(name)
    elif axis == "display":
        base = strip_display_control_suffix(name)
    else:
        return name  # data — trunk itself
    return strip_modifiers(base)


def matched_suffix(axis: str, name: str) -> str | None:
    """Return the body positional suffix that matches, or None."""
    # _entry_template is a compound suffix that must be checked on the raw
    # name (or after axis control strip but BEFORE modifier strip) because
    # strip_modifiers("foo_entry_template") returns "foo_entry".
    if axis == "content":
        raw_axis = name
    elif axis == "structure":
        raw_axis = strip_structure_control_suffix(name)
    elif axis == "display":
        raw_axis = strip_display_control_suffix(name)
    else:
        return None
    if raw_axis.endswith("_entry_template"):
        return "_entry_template"
    stripped = strip_modifiers(raw_axis)
    for suffix in BODY_SUFFIXES:
        if suffix == "_entry_template":
            continue  # already handled above
        if stripped.endswith(suffix):
            return suffix
    return None


def run_audit() -> None:
    data, content, structure, display = load_all_inputs(
        DEFAULT_DATA_PATH, DEFAULT_CONTENT_PATH, DEFAULT_STRUCTURE_PATH, DEFAULT_DISPLAY_PATH,
    )
    section_names = list(AgentOutputContent.model_fields.keys())

    total_body = 0
    total_data = 0
    total_known = 0
    total_unknown = 0
    suffix_tally: dict[str, int] = {}
    unknown_rows: list[tuple[str, str, str, str]] = []  # (section, axis, name, stripped)

    for section_name in section_names:
        ds = getattr(data, section_name, None)
        cs = getattr(content, section_name, None)
        ss = getattr(structure, section_name, None)
        dd = getattr(display, section_name, None)
        if ds is None or cs is None or ss is None:
            continue
        slots = sort_into_slots(cs, ds, ss, dd)
        body_entries = slots["body"]

        for axis, name in body_entries:
            total_body += 1
            if axis == "data":
                total_data += 1
                suffix_tally["data"] = suffix_tally.get("data", 0) + 1
                continue
            suffix = matched_suffix(axis, name)
            if suffix is None:
                total_unknown += 1
                unknown_rows.append((section_name, axis, name, effective_name(axis, name)))
            else:
                total_known += 1
                key = f"{suffix}"
                suffix_tally[key] = suffix_tally.get(key, 0) + 1

    print("=" * 70)
    print("BODY SUFFIX COVERAGE")
    print("=" * 70)
    print(f"Total body entries:        {total_body}")
    print(f"  data trunks (no suffix): {total_data}")
    print(f"  known positional:        {total_known}")
    print(f"  unknown (no suffix):     {total_unknown}")
    print()
    print("Breakdown by role:")
    for key in sorted(suffix_tally.keys()):
        print(f"  {key:20s} {suffix_tally[key]:4d}")
    print()
    if unknown_rows:
        print(f"UNKNOWN entries ({total_unknown}):")
        print(f"  {'section':<20} {'axis':<10} {'raw name':<55} {'effective trunk'}")
        print(f"  {'-' * 20} {'-' * 10} {'-' * 55} {'-' * 40}")
        for section, axis, name, stripped in unknown_rows:
            print(f"  {section:<20} {axis:<10} {name:<55} {stripped}")


if __name__ == "__main__":
    run_audit()
