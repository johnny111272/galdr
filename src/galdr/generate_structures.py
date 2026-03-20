#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datamodel-code-generator>=0.26",
# ]
# ///
"""Generate Pydantic models from JSON Schema files.

Reads schema mappings from codegen_schemas.toml, fetches schemas from
smidja/verdandi/agent-builder/output/, and writes model modules to structures/.

Run after Draupnir regenerates schemas to keep models in sync.
"""

import subprocess
import sys
import tomllib
from pathlib import Path

from galdr.functions.pure.codegen_transforms import apply_all_transforms

PACKAGE_ROOT = Path(__file__).resolve().parent
WORKSPACE = PACKAGE_ROOT.parents[3]
SMIDJA = Path.home() / ".ai" / "smidja"
SCHEMAS_DIR = SMIDJA / "verdandi" / "agent-builder" / "output"
STRUCTURES_DIR = PACKAGE_ROOT / "structures"
CONFIG_PATH = PACKAGE_ROOT / "codegen_schemas.toml"


def main() -> int:
    """Generate all Pydantic model modules from JSON Schemas."""
    config = tomllib.loads(CONFIG_PATH.read_text())
    all_schemas = {**config["checkpoint"], **config.get("include", {})}

    success = 0
    failed = 0
    for schema_name, module_name in all_schemas.items():
        schema_path = SCHEMAS_DIR / f"{schema_name}.schema.json"
        if not schema_path.exists():
            sys.stdout.write(f"  SKIP: {schema_name} (schema not found)\n")
            continue

        output_path = STRUCTURES_DIR / f"{module_name}.py"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "datamodel_code_generator",
                "--input",
                str(schema_path),
                "--input-file-type",
                "jsonschema",
                "--output",
                str(output_path),
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--use-standard-collections",
                "--use-annotated",
                "--use-title-as-name",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            sys.stderr.write(f"  FAIL: {schema_name}\n")
            sys.stderr.write(result.stderr)
            failed += 1
            continue

        content = output_path.read_text()
        output_path.write_text(apply_all_transforms(content))
        sys.stdout.write(f"  {schema_name} -> {module_name}.py\n")
        success += 1

    sys.stdout.write(f"\nGenerated: {success}/{len(all_schemas)}\n")
    if failed:
        sys.stderr.write(f"Failed: {failed}\n")
        return 1
    sys.stdout.write("Done.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
