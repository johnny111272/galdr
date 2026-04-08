"""Template interpolation simple.

CC=1-3. Loop-based placeholder interpolation.
Replaces {{placeholder}} markers in content templates with
data values, case-insensitive. Content TOML uses double-brace syntax:
  heading_template = "AGENT: {{title}}"
  role_identity_declaration_template = "You are a {{role_identity}}."
"""

import re


def interpolate(template: str, values: dict[str, str]) -> str:
    """Replace {{key}} placeholders with values from the dict, case-insensitive.

    Iterates over regex matches, replacing each with the corresponding
    value from the dict. Unmatched placeholders are preserved as-is.
    """
    result = template
    for match in re.finditer(r"\{\{(\w+)\}\}", template):
        result = result.replace(match.group(0), values.get(match.group(1).lower(), match.group(0)))
    return result
