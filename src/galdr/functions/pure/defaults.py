"""Default recipe and style that reproduce current standard_v1 output."""

from galdr.structures.recipe import ModuleConfig, RecipeConfig
from galdr.structures.style import (
    AntiPatternsStyle,
    ConstraintsStyle,
    CriticalRulesStyle,
    DispatcherStyle,
    ExamplesStyle,
    FailureCriteriaStyle,
    FrontmatterStyle,
    IdentityStyle,
    InputStyle,
    InstructionsStyle,
    OutputStyle,
    ReturnFormatStyle,
    SectionStyle,
    SecurityBoundaryStyle,
    StyleConfig,
    SuccessCriteriaStyle,
    WritingOutputStyle,
)


def section_style_model(section_name: str) -> type[SectionStyle]:
    """Return the typed style model class for a section name."""
    models: dict[str, type[SectionStyle]] = {
        "frontmatter": FrontmatterStyle,
        "identity": IdentityStyle,
        "security_boundary": SecurityBoundaryStyle,
        "input": InputStyle,
        "instructions": InstructionsStyle,
        "examples": ExamplesStyle,
        "output": OutputStyle,
        "writing_output": WritingOutputStyle,
        "constraints": ConstraintsStyle,
        "anti_patterns": AntiPatternsStyle,
        "success_criteria": SuccessCriteriaStyle,
        "failure_criteria": FailureCriteriaStyle,
        "return_format": ReturnFormatStyle,
        "critical_rules": CriticalRulesStyle,
    }
    return models.get(section_name, SectionStyle)


def default_section_style(section_name: str) -> SectionStyle:
    """Return a typed default style instance for a section name.

    Used as fallback when a style TOML omits a section."""
    return section_style_model(section_name)()


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
    """All text matching current output. Each model's defaults carry the values."""
    return StyleConfig(
        name="default",
        sections={
            "frontmatter": FrontmatterStyle(),
            "identity": IdentityStyle(),
            "security_boundary": SecurityBoundaryStyle(),
            "input": InputStyle(),
            "instructions": InstructionsStyle(),
            "examples": ExamplesStyle(),
            "output": OutputStyle(),
            "writing_output": WritingOutputStyle(),
            "constraints": ConstraintsStyle(),
            "anti_patterns": AntiPatternsStyle(),
            "success_criteria": SuccessCriteriaStyle(),
            "failure_criteria": FailureCriteriaStyle(),
            "return_format": ReturnFormatStyle(),
            "critical_rules": CriticalRulesStyle(),
        },
        dispatcher=DispatcherStyle(),
    )
