"""Pure string transforms for post-processing generated Pydantic modules.

Applied after datamodel-code-generator runs. Each transform fixes a
specific codegen output issue: unwanted __future__ import, missing
frozen config, duplicated RootModel constraints.

No IO. Pure string -> string.
"""

import re


def strip_future_annotations(content: str) -> str:
    """Remove __future__ annotations import added by codegen.

    Python 3.13 does not need this import, and it breaks Pydantic
    validation by making all annotations strings at runtime.
    """
    marker = "__future__"
    target = f"from {marker} import annotations\n\n"
    return content.replace(target, "")


def inject_frozen(content: str) -> str:
    """Add frozen=True to all model configs."""
    return content.replace(
        "extra='forbid',",
        "extra='forbid',\n        frozen=True,",
    )


def collect_rootmodel_names(content: str) -> set[str]:
    """Find all class names that extend RootModel."""
    return set(re.findall(r"class (\w+)\(RootModel", content))


def strip_redundant_constraints(content: str) -> str:
    """Remove pattern/length constraints from Fields that reference RootModels.

    datamodel-code-generator duplicates pattern and length constraints — once
    on the RootModel root field (correct) and again on every Field that uses
    that type (causes TypeError at runtime). Strip the duplicates.
    """
    rootmodel_names = collect_rootmodel_names(content)
    if not rootmodel_names:
        return content
    lines = content.split("\n")
    result: list[str] = []
    in_rootmodel_field = False
    for line_index, line in enumerate(lines):
        stripped = line.strip()
        if "Annotated[" in stripped:
            next_line = lines[line_index + 1].strip() if line_index + 1 < len(lines) else ""
            next_type = next_line.rstrip(",")
            type_tokens = {token.strip() for token in next_type.split("|")}
            in_rootmodel_field = bool(type_tokens & rootmodel_names)
        elif stripped == "],":
            in_rootmodel_field = False
        if in_rootmodel_field and re.match(r"\s+(pattern|min_length|max_length)=", line):
            continue
        if in_rootmodel_field:
            line = re.sub(r",?\s*(min_length|max_length)=\d+", "", line)
        result.append(line)
    return "\n".join(result)


def apply_all_transforms(content: str) -> str:
    """Apply all post-generation transforms in sequence."""
    content = strip_future_annotations(content)
    content = inject_frozen(content)
    return strip_redundant_constraints(content)
