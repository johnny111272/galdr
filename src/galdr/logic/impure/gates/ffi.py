"""Gate FFI bindings — Rust/PyO3 gate module invocation.

CC=1. These are the only functions that call into compiled Rust gate
modules. The internals are a black box — purity is asserted by placement
in impure/gates/ffi.py.

NornirGate is a type alias for compiled Rust/PyO3 gate modules (.so files
at ~/.ai/tools/lib/gate_*.cpython-313-darwin.so). Each gate module has a
.validate() method. Input gates take a file path and return a dict.

All return {"ok": bool, "data": str | None, "error": {"type": str, "message": str} | None}.
Gate modules are imported by name (e.g. `import gate_anthropic_render_input`).
"""

from pathlib import Path
from types import ModuleType

from galdr.structure.model.gate_types import GateResult

type NornirGate = ModuleType


def call_input_gate(gate: NornirGate, file_path: Path) -> GateResult:
    """Call an input gate, return the raw validated result."""
    return GateResult.model_validate(gate.validate(str(file_path)))
