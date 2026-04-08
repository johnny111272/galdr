"""Template interpolation primitive.

CC=1. Replaces {{placeholder}} markers in content templates with
data values. Content TOML uses double-brace syntax:
  heading_template = "AGENT: {{title}}"
  role_identity_declaration_template = "You are a {{role_identity}}."

Note: uses lambda in re.sub — deferred gleipnir violation.
The lambda-free version (loop + if) is CC=3, which forces this to L2,
creating an import boundary violation for L2 callers. The lambda
keeps CC=1 at L1 where all callers can reach it.
"""

import re


def resolve_placeholder(match: re.Match, values: dict[str, str]) -> str:
    """Look up a single placeholder match in the values dict, case-insensitive."""
    return values.get(match.group(1).lower(), match.group(0))


def interpolate(template: str, values: dict[str, str]) -> str:
    """Replace {{key}} placeholders with values from the dict, case-insensitive."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: resolve_placeholder(m, values), template)
