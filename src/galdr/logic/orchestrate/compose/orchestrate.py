"""Composition pipeline orchestration — load inputs, walk sections, write output.

Orchestrate level (CC=1-5). Wires together impure (gate validation),
transform (data unwrapping), and pure (section composition) zones.

Gate modules are compiled Rust/PyO3 .so files imported directly.
Each is called via validate_input(gate, path) → JSON string.
No subprocess calls — pure PyO3 import and method invocation.
"""

from pathlib import Path

import gate_anthropic_render_input
import gate_output_content_input
import gate_output_display_input
import gate_output_structure_input

from galdr.logic.impure.gates.simple import validate_input
from galdr.logic.pure.compose.assembled import compose_section
from galdr.logic.pure.compose.simple import join_fragments
from galdr.logic.transform.data_unwrap.composed import unwrap_section_data
from galdr.structure.gen.anthropic_render import AgentAnthropicRender
from galdr.structure.gen.output_content import AgentOutputContent
from galdr.structure.gen.output_display import AgentOutputDisplay
from galdr.structure.gen.output_structure import AgentOutputStructure


def load_all_inputs(
    data_path: Path,
    content_path: Path,
    structure_path: Path,
    display_path: Path,
) -> tuple[AgentAnthropicRender, AgentOutputContent, AgentOutputStructure, AgentOutputDisplay]:
    """Validate all four inputs through gates, deserialize to Pydantic models."""
    data_json = validate_input(gate_anthropic_render_input, data_path)
    content_json = validate_input(gate_output_content_input, content_path)
    structure_json = validate_input(gate_output_structure_input, structure_path)
    display_json = validate_input(gate_output_display_input, display_path)
    return (
        AgentAnthropicRender.model_validate_json(data_json),
        AgentOutputContent.model_validate_json(content_json),
        AgentOutputStructure.model_validate_json(structure_json),
        AgentOutputDisplay.model_validate_json(display_json),
    )


def compose_one_section(
    section_name: str,
    data_model: AgentAnthropicRender,
    content_model: AgentOutputContent,
    structure_model: AgentOutputStructure,
    display_model: AgentOutputDisplay,
) -> str | None:
    """Compose a single section: extract chunks, unwrap data, render."""
    data_section = getattr(data_model, section_name, None)
    content_section = getattr(content_model, section_name, None)
    if data_section is None or content_section is None:
        return None
    structure_section = getattr(structure_model, section_name, None)
    display_section = getattr(display_model, section_name, None)
    data_values = unwrap_section_data(data_section)
    return compose_section(
        data_section, structure_section,
        content_section, display_section, data_values,
    )


def compose_all_sections(
    data_model: AgentAnthropicRender,
    content_model: AgentOutputContent,
    structure_model: AgentOutputStructure,
    display_model: AgentOutputDisplay,
) -> list[str]:
    """Iterate section_order, compose each section via the generic engine."""
    section_order = [item.value for item in structure_model.section_order.order.root]
    sections: list[str] = []
    for section_name in section_order:
        rendered = compose_one_section(section_name, data_model, content_model, structure_model, display_model)
        if rendered:
            sections.append(rendered)
    return sections


def run(
    data_path: Path,
    content_path: Path,
    structure_path: Path,
    display_path: Path,
    output_path: Path,
) -> int:
    """Run the composition pipeline: load, compose, write. Returns 0 on success."""
    data, content, structure, display = load_all_inputs(
        data_path, content_path, structure_path, display_path,
    )
    sections = compose_all_sections(data, content, structure, display)
    output = "\n\n---\n\n".join(sections) if sections else None
    if output:
        # TODO: replace with output gate when galdr output gate is built.
        # Raw write_text bypasses the gate pattern. Acceptable for bootstrap
        # since no compiled output gate exists for markdown yet.
        output_path.write_text(output + "\n", encoding="utf-8")
    return 0
