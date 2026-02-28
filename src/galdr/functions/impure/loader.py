"""Load anthropic render data through the Nornir gate.

Single entry point: load_anthropic_render(path) -> validated JSON string.
"""

from galdr.functions.impure.gates import call_input_gate
from galdr.structures.errors import GateValidationError


def load_anthropic_render(path: str) -> str:
    """Load and validate an anthropic_render.toml file, returning JSON."""
    result = call_input_gate("gate_anthropic_render_input", path)
    if not result.ok:
        msg = result.error.message if result.error else "unknown gate error"
        raise GateValidationError(msg)
    if result.data is None:
        raise GateValidationError("gate returned ok=True but no data")
    return result.data
