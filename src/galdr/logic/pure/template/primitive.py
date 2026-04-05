"""Template interpolation primitive.

CC=1. Replaces {{placeholder}} markers in content templates with
data values. Content TOML uses double-brace syntax:
  heading = "AGENT: {{title}}"
  declaration = "You are a {{role_identity}}."
"""

import re


def interpolate(template: str, values: dict[str, str]) -> str:
    """Replace {{key}} placeholders with values from the dict."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1).lower(), m.group(0)), template)
