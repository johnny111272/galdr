"""Gate loader — imports and calls Nornir PyO3 gate modules.

This is the ONLY module that touches sys.path and importlib.
All other code calls gates through this interface.
"""

import importlib
import os
import sys
from functools import lru_cache
from types import ModuleType

from galdr.structures.gate_types import GateResult

GATE_LIB_PATH = os.environ.get("GALDR_GATE_LIB", "/Users/johnny/.ai/tools/lib")


@lru_cache(maxsize=4)
def load_gate(gate_name: str) -> ModuleType:
    """Import a gate module by name, caching the result."""
    if GATE_LIB_PATH not in sys.path:
        sys.path.insert(0, GATE_LIB_PATH)
    return importlib.import_module(gate_name)


def call_input_gate(gate_name: str, path: str) -> GateResult:
    """Call an input gate: reads TOML file, returns validated JSON."""
    gate = load_gate(gate_name)
    return GateResult.model_validate(gate.validate(path))
