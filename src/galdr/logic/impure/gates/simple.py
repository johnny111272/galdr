"""Gate validation — the IO boundary.

CC=2-3. Validates gate results and formats errors. Calls FFI layer
for the actual Rust invocation — never calls gate.validate() directly.
See gates/ffi.py for the NornirGate type alias and FFI bindings.
"""

from pathlib import Path

from galdr.logic.impure.gates.ffi import NornirGate, call_input_gate
from galdr.structure.model.gate_types import GateResult


def format_gate_error(gate_name: str, result: GateResult) -> str:
    """Build an error message from a failed gate result."""
    message = result.error.message if result.error else "Unknown gate error"
    error_type = result.error.type if result.error else "unknown"
    return f"Gate '{gate_name}' failed ({error_type}): {message}"


def validate_input(gate: NornirGate, file_path: Path) -> str:
    """Validate input through a gate. Returns validated JSON string."""
    result = call_input_gate(gate, file_path)
    if not result.ok:
        raise ValueError(format_gate_error(gate.__name__, result))
    return result.data
