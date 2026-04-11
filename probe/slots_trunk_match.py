"""Slot fill + trunk match probe.

NOT PRODUCTION CODE. Exempt from gleipnir.

Step 1: fill slots with data (body) and content (by positional suffix).
Step 2: pull each structure / display field into the slot where its
        trunk matches an existing data or content entry.
Step 3: list whatever couldn't be matched.

Trunk matching:
- structure _selector: special — duplicate into every slot that
  contains a content entry whose trunk starts with the selector trunk.
- structure / display other: compute extract_trunk (strip control
  suffixes, strip modifiers), then look for a data/content entry in
  any slot whose extract_trunk equals the field's trunk or has a
  prefix relationship in either direction.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(Path.home() / ".ai" / "tools" / "lib"))

from galdr.logic.orchestrate.compose.orchestrate import load_all_inputs
from galdr.logic.pure.compose.primitive import (
    extract_trunk,
    is_preprocessing_field,
)
from galdr.logic.pure.compose.simple import classify_content_slot
from galdr.structure.gen.output_content import AgentOutputContent

DEFAULT_DATA_PATH = Path.home() / ".ai" / "spaces" / "bragi" / "definitions" / "agents" / "agent-builder" / "anthropic_render.toml"
DEFAULT_CONTENT_PATH = REPO_ROOT / "extracted" / "content.toml"
DEFAULT_STRUCTURE_PATH = REPO_ROOT / "extracted" / "structure.toml"
DEFAULT_DISPLAY_PATH = REPO_ROOT / "extracted" / "display.toml"


def trunks_match(subject: str, target: str) -> bool:
    if subject == target:
        return True
    if target.startswith(subject + "_"):
        return True
    if subject.startswith(target + "_"):
        return True
    return False


def find_slots_for_trunk(trunk: str, slots: dict) -> list:
    matches = []
    for slot_name, entries in slots.items():
        for axis, fname in entries:
            if axis not in ("data", "content"):
                continue
            target = extract_trunk(fname)
            if trunks_match(trunk, target):
                matches.append(slot_name)
                break
    return matches


def find_selector_slots(selector_trunk: str, slots: dict) -> list:
    matches = []
    for slot_name, entries in slots.items():
        for axis, fname in entries:
            if axis != "content":
                continue
            if extract_trunk(fname).startswith(selector_trunk):
                matches.append(slot_name)
                break
    return matches


def place_structure_field(name: str, slots: dict) -> list:
    if name.endswith("_selector"):
        return find_selector_slots(name.removesuffix("_selector"), slots)
    return find_slots_for_trunk(extract_trunk(name), slots)


def place_display_field(name: str, slots: dict) -> list:
    return find_slots_for_trunk(extract_trunk(name), slots)


def fill_and_match(data_section, content_section, structure_section, display_section):
    slots = {"heading": [], "preamble": [], "body": [], "closing": []}
    leftover = []

    for name in data_section.model_fields:
        slots["body"].append(("data", name))
    for name in content_section.model_fields:
        slots[classify_content_slot(name)].append(("content", name))

    for name in structure_section.model_fields:
        if is_preprocessing_field(name):
            continue
        placements = place_structure_field(name, slots)
        if placements:
            for slot_name in placements:
                slots[slot_name].append(("structure", name))
        else:
            leftover.append(("structure", name))

    if display_section is not None:
        for name in display_section.model_fields:
            if is_preprocessing_field(name):
                continue
            placements = place_display_field(name, slots)
            if placements:
                for slot_name in placements:
                    slots[slot_name].append(("display", name))
            else:
                leftover.append(("display", name))

    return slots, leftover


def run_probe():
    data, content, structure, display = load_all_inputs(
        DEFAULT_DATA_PATH, DEFAULT_CONTENT_PATH, DEFAULT_STRUCTURE_PATH, DEFAULT_DISPLAY_PATH,
    )
    total_leftover = 0
    for section_name in AgentOutputContent.model_fields:
        data_section = getattr(data, section_name, None)
        content_section = getattr(content, section_name, None)
        structure_section = getattr(structure, section_name, None)
        display_section = getattr(display, section_name, None)
        if data_section is None or content_section is None or structure_section is None:
            print(f"## {section_name} — skipped\n")
            continue
        slots, leftover = fill_and_match(data_section, content_section, structure_section, display_section)
        print(f"## {section_name}")
        for slot_name in ("heading", "preamble", "body", "closing"):
            entries = slots[slot_name]
            print(f"  {slot_name} ({len(entries)})")
            for axis, name in entries:
                print(f"    {axis}: {name}")
        if leftover:
            print(f"  LEFTOVER ({len(leftover)})")
            for axis, name in leftover:
                print(f"    {axis}: {name}")
            total_leftover += len(leftover)
        print()
    print(f"TOTAL LEFTOVER: {total_leftover}")


if __name__ == "__main__":
    run_probe()
