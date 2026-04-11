"""Slot fill probe — data + content axes only.

NOT PRODUCTION CODE. Exempt from gleipnir while we iterate on slot
semantics.

Question: what do the four slots look like when populated only by
data fields and content fields? No structure axis, no display axis —
just the semantic substance. This is the inner layer of a bundle
before controls are attached.

Output format: per section, each slot listed with its data and
content entries. Empty slots still shown.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(Path.home() / ".ai" / "tools" / "lib"))

from galdr.logic.orchestrate.compose.orchestrate import load_all_inputs
from galdr.logic.pure.compose.simple import classify_content_slot
from galdr.structure.gen.output_content import AgentOutputContent

DEFAULT_DATA_PATH = Path.home() / ".ai" / "spaces" / "bragi" / "definitions" / "agents" / "agent-builder" / "anthropic_render.toml"
DEFAULT_CONTENT_PATH = REPO_ROOT / "extracted" / "content.toml"
DEFAULT_STRUCTURE_PATH = REPO_ROOT / "extracted" / "structure.toml"
DEFAULT_DISPLAY_PATH = REPO_ROOT / "extracted" / "display.toml"


def fill_slots_data_content(data_section, content_section):
    slots = {"heading": [], "preamble": [], "body": [], "closing": []}
    for name in data_section.model_fields:
        slots["body"].append(("data", name))
    for name in content_section.model_fields:
        slots[classify_content_slot(name)].append(("content", name))
    return slots


def run_probe():
    data, content, _structure, _display = load_all_inputs(
        DEFAULT_DATA_PATH, DEFAULT_CONTENT_PATH, DEFAULT_STRUCTURE_PATH, DEFAULT_DISPLAY_PATH,
    )
    for section_name in AgentOutputContent.model_fields:
        data_section = getattr(data, section_name, None)
        content_section = getattr(content, section_name, None)
        if data_section is None or content_section is None:
            print(f"## {section_name} — skipped (missing data or content)\n")
            continue
        slots = fill_slots_data_content(data_section, content_section)
        print(f"## {section_name}")
        for slot_name in ("heading", "preamble", "body", "closing"):
            entries = slots[slot_name]
            print(f"  {slot_name} ({len(entries)})")
            for axis, name in entries:
                print(f"    {axis}: {name}")
        print()


if __name__ == "__main__":
    run_probe()
