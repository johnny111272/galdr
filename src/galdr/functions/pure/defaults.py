"""Default recipe and style that reproduce current standard_v1 output."""

from galdr.structures.recipe import ModuleConfig, RecipeConfig
from galdr.structures.style import StyleConfig, StyleEntry


def default_recipe() -> RecipeConfig:
    """Module order and config matching standard_v1.md.j2."""
    return RecipeConfig(
        name="standard-v1",
        style="default",
        modules=[
            ModuleConfig(section="frontmatter"),
            ModuleConfig(section="identity"),
            ModuleConfig(section="security_boundary"),
            ModuleConfig(section="input"),
            ModuleConfig(section="instructions"),
            ModuleConfig(section="examples"),
            ModuleConfig(section="output"),
            ModuleConfig(section="writing_output"),
            ModuleConfig(section="constraints"),
            ModuleConfig(section="anti_patterns"),
            ModuleConfig(section="success_criteria"),
            ModuleConfig(section="failure_criteria"),
            ModuleConfig(section="return_format"),
            ModuleConfig(section="critical_rules"),
        ],
    )


def default_style() -> StyleConfig:
    """Headings and framing matching current template text."""
    return StyleConfig(
        name="default",
        sections={
            "frontmatter": StyleEntry(),
            "identity": StyleEntry(),
            "security_boundary": StyleEntry(heading="Security Boundary"),
            "input": StyleEntry(heading="Input"),
            "instructions": StyleEntry(heading="Processing"),
            "examples": StyleEntry(heading="Examples"),
            "output": StyleEntry(heading="Output"),
            "writing_output": StyleEntry(heading="Writing Output (MANDATORY)"),
            "constraints": StyleEntry(heading="Constraints"),
            "anti_patterns": StyleEntry(heading="Anti-Patterns"),
            "success_criteria": StyleEntry(heading="Success Criteria"),
            "failure_criteria": StyleEntry(heading="Failure Criteria"),
            "return_format": StyleEntry(heading="Return Format"),
            "critical_rules": StyleEntry(heading="Critical Rules"),
        },
    )
