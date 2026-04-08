"""Codegen clean simple — RootModel field classifier and constraint stripping.

CC=1-3. No cross-module imports.

Predicate for identifying Annotated fields that reference RootModel types.
This is the classifier that decides whether a given Field annotation should
have its constraints stripped in the composed-level state machine.
"""

import re


def strip_inline_constraints(line: str) -> str:
    """Remove inline min_length/max_length constraint fragments from a line.

    Strips ,min_length=N and ,max_length=N fragments that appear inline
    within Field() annotations. These are duplicates of constraints already
    defined on the referenced RootModel type.
    """
    result = line
    for match in re.finditer(r",?\s*(min_length|max_length)=\d+", line):
        result = result.replace(match.group(0), "")
    return result


def check_rootmodel_field(lines: list[str], index: int, rootmodel_names: set[str]) -> bool:
    """Check if the Annotated field at this line references a RootModel type.

    Looks ahead one line from the Annotated[ opening to extract type tokens
    (split on |). If any of those type names are in the RootModel set, this
    field's constraints are duplicates of the RootModel's own constraints
    and must be removed by the composed-level state machine.
    """
    next_line = lines[index + 1].strip() if index + 1 < len(lines) else ""
    type_tokens = {token.strip() for token in next_line.rstrip(",").split("|")}
    return bool(type_tokens & rootmodel_names)
