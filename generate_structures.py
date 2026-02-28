#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datamodel-code-generator>=0.26",
# ]
# ///
"""Generate Pydantic models from JSON Schema files.

Reads schemas from bragi/schemas/ and writes model modules to
src/galdr/structures/.

Run after Draupnir regenerates schemas to keep models in sync.
"""

import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE = PROJECT_ROOT.parent.parent  # bragi root
SCHEMAS_DIR = WORKSPACE / "schemas"
STRUCTURES_DIR = PROJECT_ROOT / "src" / "galdr" / "structures"

SCHEMA_MODULES = {
    "agent-anthropic-render": "anthropic_render",
}


def generate_module(schema_name: str, module_name: str) -> bool:
    """Generate a single Pydantic model module from a schema."""
    schema_path = SCHEMAS_DIR / f"{schema_name}.schema.json"
    output_path = STRUCTURES_DIR / f"{module_name}.py"

    if not schema_path.exists():
        print(f"  SKIP: {schema_path.name} not found", file=sys.stderr)
        return False

    result = subprocess.run(
        [
            sys.executable, "-m", "datamodel_code_generator",
            "--input", str(schema_path),
            "--input-file-type", "jsonschema",
            "--output", str(output_path),
            "--output-model-type", "pydantic_v2.BaseModel",
            "--use-standard-collections",
            "--use-annotated",
            "--use-title-as-name",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  FAIL: {schema_name}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False

    post_process(output_path)
    print(f"  {schema_name} -> {module_name}.py")
    return True


def collect_rootmodel_names(content: str) -> set[str]:
    """Find all class names that extend RootModel."""
    return set(re.findall(r"class (\w+)\(RootModel", content))


def strip_redundant_constraints(content: str) -> str:
    """Remove pattern= from Field() when the annotated type is a RootModel.

    datamodel-code-generator duplicates pattern constraints — once on the
    RootModel root field (correct) and again on every Field that uses that
    type (causes TypeError). Strip the duplicate.
    """
    rootmodel_names = collect_rootmodel_names(content)
    if not rootmodel_names:
        return content
    lines = content.split("\n")
    result: list[str] = []
    in_rootmodel_field = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if "Annotated[" in stripped and "root:" not in stripped:
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            next_type = next_line.rstrip(",")
            type_tokens = {t.strip() for t in next_type.split("|")}
            in_rootmodel_field = bool(type_tokens & rootmodel_names)
        elif stripped == "],":
            in_rootmodel_field = False
        if in_rootmodel_field and re.match(r"\s+pattern=", line):
            continue
        result.append(line)
    return "\n".join(result)


def post_process(path: Path) -> Path:
    """Add frozen=True, strip __future__, strip redundant constraints."""
    content = path.read_text()
    content = content.replace(
        "extra='forbid',",
        "extra='forbid',\n        frozen=True,",
    )
    content = content.replace(
        "from __future__ import annotations\n\n",
        "",
    )
    content = strip_redundant_constraints(content)
    path.write_text(content)
    return path


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATE STRUCTURES")
    print("=" * 60)

    success = 0
    skipped = 0
    failed = 0
    for schema_name, module_name in SCHEMA_MODULES.items():
        schema_path = SCHEMAS_DIR / f"{schema_name}.schema.json"
        if not schema_path.exists():
            print(f"  SKIP: {schema_name} (schema not found)")
            skipped += 1
            continue
        if generate_module(schema_name, module_name):
            success += 1
        else:
            failed += 1

    print()
    print(f"Generated: {success}/{len(SCHEMA_MODULES)}")
    if skipped:
        print(f"Skipped: {skipped} (schemas not yet on disk)")
    if failed:
        print(f"Failed: {failed}", file=sys.stderr)
        sys.exit(1)
    print("Done.")
