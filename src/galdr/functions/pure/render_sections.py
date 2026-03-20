"""Section renderers — one function per module.

Each function takes its context model + typed style + ModuleConfig
and returns a markdown string. All pure — no IO.
"""

from galdr.functions.pure.render_primitives import (
    bold_label,
    bold_label_code,
    code_block,
    heading,
    list_as_bullets,
    list_as_numbered,
    list_as_prose,
    section_frame,
    structured_entries,
)
from galdr.structures.recipe import ModuleConfig
from galdr.structures.style import (
    CriticalRulesStyle,
    IdentityStyle,
    InputStyle,
    OutputStyle,
    ReturnFormatStyle,
    SectionStyle,
    SecurityBoundaryStyle,
    SuccessCriteriaStyle,
    FailureCriteriaStyle,
)
from galdr.structures.template_context import (
    AntiPatternsContext,
    ConstraintsContext,
    CriticalRulesContext,
    ExamplesContext,
    FailureCriterionContext,
    FrontmatterContext,
    IdentityContext,
    InputContext,
    InstructionsContext,
    OutputContext,
    ReturnFormatContext,
    SecurityBoundaryContext,
    SuccessCriterionContext,
    WritingOutputContext,
)


def render_frontmatter(data: FrontmatterContext) -> str:
    """Render YAML frontmatter block. No style/config — structurally fixed."""
    lines = [
        "---",
        f'name: "{data.name}"',
        f'description: "{data.description}"',
        f'tools: "{data.tools}"',
        f'model: "{data.model}"',
        f'permissionMode: "{data.permission_mode}"',
    ]
    if data.hooks:
        lines.append("hooks:")
        lines.append("  PreToolUse:")
        for hook in data.hooks:
            lines.append(f"  - matcher: {hook.matcher}")
            lines.append("    hooks:")
            lines.append("    - type: command")
            lines.append(f"      command: {hook.command}")
    lines.append("---")
    return "\n".join(lines)


def render_identity(data: IdentityContext, style: IdentityStyle, config: ModuleConfig) -> str:
    """Render identity section. Uses data.title as H1, not style heading.

    When config.fields is set, only renders the named fields."""
    allowed = set(config.fields) if config.fields else None
    parts = []
    if not allowed or "title" in allowed:
        parts.append(heading(1, data.title))
    if not allowed or "description" in allowed:
        parts.append(bold_label(style.purpose_label, data.description))
    if data.role_identity and (not allowed or "role_identity" in allowed):
        parts.append(style.role_identity_template.format(role_identity=data.role_identity))
    if data.role_description and (not allowed or "role_description" in allowed):
        parts.append(data.role_description)
    if data.role_responsibility and (not allowed or "role_responsibility" in allowed):
        parts.append(bold_label(style.responsibility_label, data.role_responsibility))
    if data.role_expertise and (not allowed or "role_expertise" in allowed):
        parts.append(bold_label(style.expertise_label, ", ".join(data.role_expertise)))
    return "\n\n".join(parts)


def render_security_boundary(data: SecurityBoundaryContext, style: SecurityBoundaryStyle, config: ModuleConfig) -> str:
    """Render security boundary grants display."""
    entry_lines = []
    for entry in data.display:
        tools_str = ", ".join(entry.tools)
        entry_lines.append(bold_label_code(tools_str, entry.path))
    content_parts = [
        style.preamble,
        style.grants_intro,
        "\n".join(entry_lines),
        style.boundary_warning,
    ]
    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def format_parameter(param, optional_suffix: str) -> str:
    """Format a single parameter for the input section bullet list."""
    parts = [param.name]
    if param.type:
        parts.append(f" ({param.type})")
    if not param.required:
        parts.append(f" {optional_suffix}")
    if param.description:
        parts.append(f": {param.description}")
    return "".join(parts)


def render_input(data: InputContext, style: InputStyle, config: ModuleConfig) -> str:
    """Render input section with parameters and context items."""
    content_parts = [data.description]

    if data.parameters:
        param_items = [format_parameter(param, style.optional_suffix) for param in data.parameters]
        content_parts.append(f"{style.parameters_intro}\n" + list_as_bullets(param_items))

    if data.input_schema:
        content_parts.append(f"{style.schema_intro} `{data.input_schema}`")

    if data.context_required:
        items = [bold_label_code(ctx.label, ctx.path) for ctx in data.context_required]
        content_parts.append(f"**{style.required_context_label}**\n" + list_as_bullets(items))

    if data.context_available:
        items = [bold_label_code(ctx.label, ctx.path) for ctx in data.context_available]
        content_parts.append(f"**{style.available_context_label}**\n" + list_as_bullets(items))

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_instructions(data: InstructionsContext, style: SectionStyle, config: ModuleConfig) -> str:
    """Render processing instructions. Variant 'numbered' prefixes step numbers."""
    if config.variant == "numbered":
        content = "\n\n".join(
            f"{i}. {step.text}" for i, step in enumerate(data.steps, 1)
        )
    else:
        content = "\n\n".join(step.text for step in data.steps)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_examples(data: ExamplesContext, style: SectionStyle, config: ModuleConfig) -> str:
    """Render example groups with optional heading toggle and entry cap."""
    group_parts = []
    for group in data.groups:
        group_lines = [heading(3, group.group_name)]

        max_cap = config.max_entries if config.max_entries is not None else group.max_entries
        show_headings = config.display_headings if config.display_headings is not None else group.display_headings
        entries = group.entries[:max_cap] if max_cap else group.entries

        for entry in entries:
            if show_headings:
                group_lines.append(heading(4, entry.heading) + "\n\n" + entry.text)
            else:
                group_lines.append(entry.text)

        group_parts.append("\n\n".join(group_lines))

    content = "\n\n".join(group_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_output(data: OutputContext, style: OutputStyle, config: ModuleConfig) -> str:
    """Render output section with schema, paths, and description."""
    header_lines = []
    if data.schema_path:
        header_lines.append(bold_label_code(style.schema_label, data.schema_path))
    if data.file_path:
        header_lines.append(bold_label_code(style.file_label, data.file_path))
    elif data.directory_path:
        header_lines.append(bold_label_code(style.directory_label, data.directory_path))

    content_parts = []
    if header_lines:
        content_parts.append("\n".join(header_lines))
    content_parts.append(data.description)

    if data.name_known == "unknown" and data.name_instruction:
        content_parts.append(data.name_instruction)

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_writing_output(data: WritingOutputContext, style: SectionStyle, config: ModuleConfig) -> str:
    """Render writing output invocation in a code block."""
    content = code_block(data.invocation_display)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_list_variant(items: list[str], variant: str) -> str:
    """Dispatch a list of strings to the appropriate list primitive."""
    if variant == "numbered":
        return list_as_numbered(items)
    if variant == "prose":
        return list_as_prose(items)
    return list_as_bullets(items)


def render_constraints(data: ConstraintsContext, style: SectionStyle, config: ModuleConfig) -> str:
    """Render constraints as a list. Supports variants: bullets (default), numbered, prose."""
    content = render_list_variant(data.rules, config.variant)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_anti_patterns(data: AntiPatternsContext, style: SectionStyle, config: ModuleConfig) -> str:
    """Render anti-patterns as a list. Supports variants: bullets (default), numbered, prose."""
    content = render_list_variant(data.patterns, config.variant)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_criteria_list(
    criteria: list[SuccessCriterionContext] | list[FailureCriterionContext],
    variant: str = "standard",
    evidence_label: str = "Evidence:",
) -> str:
    """Render a list of criteria. Standard includes evidence, compact omits it."""
    entries = [(criterion.definition, criterion.evidence) for criterion in criteria]
    return structured_entries(entries, evidence_mode=variant, evidence_label=evidence_label)


def render_success_criteria(
    data: list[SuccessCriterionContext], style: SuccessCriteriaStyle, config: ModuleConfig,
) -> str:
    """Render success criteria. Supports variants: standard (default), compact."""
    if not data:
        return ""
    content = render_criteria_list(data, config.variant, style.evidence_label)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_failure_criteria(
    data: list[FailureCriterionContext], style: FailureCriteriaStyle, config: ModuleConfig,
) -> str:
    """Render failure criteria. Supports variants: standard (default), compact."""
    if not data:
        return ""
    content = render_criteria_list(data, config.variant, style.evidence_label)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_return_format(data: ReturnFormatContext, style: ReturnFormatStyle, config: ModuleConfig) -> str:
    """Render return format instructions (excluding success/failure criteria)."""
    content_parts = []

    if "status" in data.mode:
        content_parts.append(
            f"{style.success_label}\n{code_block(style.success_code)}\n\n"
            f"{style.failure_label}\n{code_block(style.failure_code_template)}"
        )

    if data.status_instruction:
        content_parts.append(data.status_instruction)
    if data.metrics_instruction:
        content_parts.append(data.metrics_instruction)
    if data.output_instruction:
        content_parts.append(data.output_instruction)

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_critical_rules(data: CriticalRulesContext, style: CriticalRulesStyle, config: ModuleConfig) -> str:
    """Render critical rules. Supports variants: numbered (default), bullets."""
    rules = []
    if data.has_output_tool:
        rules.append(style.tool_rule.format(tool_name=data.tool_name))
        if data.batch_size:
            rules.append(style.batch_rule.format(batch_size=data.batch_size))
            rules.append(style.write_after_batch_rule)
        else:
            rules.append(style.validate_rule)
    rules.append(style.fail_fast_rule)
    rules.append(style.stay_in_scope_rule)
    rules.append(style.no_invention_rule)

    if config.variant == "bullets":
        content = list_as_bullets(rules)
    else:
        content = list_as_numbered(rules)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)
