"""Section renderers — one function per module.

Each function takes its context model + StyleEntry + ModuleConfig
and returns a markdown string. All pure — no IO.
"""

from galdr.functions.pure.render_primitives import (
    bold_label,
    bold_label_code,
    code_block,
    heading,
    list_as_bullets,
    list_as_numbered,
    section_frame,
)
from galdr.structures.recipe import ModuleConfig
from galdr.structures.style import StyleEntry
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


def render_identity(data: IdentityContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render identity section. Uses data.title as H1, not style heading."""
    parts = [
        heading(1, data.title),
        bold_label("Purpose", data.description),
    ]
    if data.role_identity:
        parts.append(f"You are a {data.role_identity}.")
    if data.role_description:
        parts.append(data.role_description)
    if data.role_responsibility:
        parts.append(bold_label("Your responsibility", data.role_responsibility))
    if data.role_expertise:
        parts.append(bold_label("Expertise", ", ".join(data.role_expertise)))
    return "\n\n".join(parts)


def render_security_boundary(data: SecurityBoundaryContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render security boundary grants display."""
    entry_lines = []
    for entry in data.display:
        tools_str = ", ".join(entry.tools)
        entry_lines.append(bold_label_code(tools_str, entry.path))
    content_parts = [
        "This agent operates under `bypassPermissions` with hook-based restrictions.",
        "The following operations are allowed — everything else is blocked by the system.",
        "\n".join(entry_lines),
        "Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively.",
    ]
    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def format_parameter(param) -> str:
    """Format a single parameter for the input section bullet list."""
    parts = [param.name]
    if param.type:
        parts.append(f" ({param.type})")
    if not param.required:
        parts.append(" (optional)")
    if param.description:
        parts.append(f": {param.description}")
    return "".join(parts)


def render_input(data: InputContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render input section with parameters and context items."""
    content_parts = [data.description]

    if data.parameters:
        param_items = [format_parameter(param) for param in data.parameters]
        content_parts.append("The dispatcher provides:\n" + list_as_bullets(param_items))

    if data.input_schema:
        content_parts.append(f"Input validates against: `{data.input_schema}`")

    if data.context_required:
        items = [bold_label_code(ctx.label, ctx.path) for ctx in data.context_required]
        content_parts.append("**Required context:**\n" + list_as_bullets(items))

    if data.context_available:
        items = [bold_label_code(ctx.label, ctx.path) for ctx in data.context_available]
        content_parts.append("**Available context:**\n" + list_as_bullets(items))

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_instructions(data: InstructionsContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render processing instructions."""
    content = "\n\n".join(step.text for step in data.steps)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_examples(data: ExamplesContext, style: StyleEntry, config: ModuleConfig) -> str:
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


def render_output(data: OutputContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render output section with schema, paths, and description."""
    header_lines = []
    if data.schema_path:
        header_lines.append(bold_label_code("Schema", data.schema_path))
    if data.file_path:
        header_lines.append(bold_label_code("Output file", data.file_path))
    elif data.directory_path:
        header_lines.append(bold_label_code("Output directory", data.directory_path))

    content_parts = []
    if header_lines:
        content_parts.append("\n".join(header_lines))
    content_parts.append(data.description)

    if data.name_known == "unknown" and data.name_instruction:
        content_parts.append(data.name_instruction)

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_writing_output(data: WritingOutputContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render writing output invocation in a code block."""
    content = code_block(data.invocation_display)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_constraints(data: ConstraintsContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render constraints as a list."""
    content = list_as_bullets(data.rules)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_anti_patterns(data: AntiPatternsContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render anti-patterns as a list."""
    content = list_as_bullets(data.patterns)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_criteria_list(criteria: list[SuccessCriterionContext] | list[FailureCriterionContext]) -> str:
    """Render a list of criteria with definitions and evidence."""
    blocks = []
    for criterion in criteria:
        evidence = list_as_bullets(criterion.evidence)
        blocks.append(f"{criterion.definition}\n\nEvidence:\n{evidence}")
    return "\n\n".join(blocks)


def render_success_criteria(data: list[SuccessCriterionContext], style: StyleEntry, config: ModuleConfig) -> str:
    """Render success criteria with definitions and evidence."""
    if not data:
        return ""
    content = render_criteria_list(data)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_failure_criteria(data: list[FailureCriterionContext], style: StyleEntry, config: ModuleConfig) -> str:
    """Render failure criteria with definitions and evidence."""
    if not data:
        return ""
    content = render_criteria_list(data)
    return section_frame(style.heading, 3, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_return_format(data: ReturnFormatContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render return format instructions (excluding success/failure criteria)."""
    content_parts = []

    if "status" in data.mode:
        content_parts.append(f"On success:\n{code_block('SUCCESS')}\n\nOn failure:\n{code_block('FAILURE: <reason>')}")

    if data.status_instruction:
        content_parts.append(data.status_instruction)
    if data.metrics_instruction:
        content_parts.append(data.metrics_instruction)
    if data.output_instruction:
        content_parts.append(data.output_instruction)

    content = "\n\n".join(content_parts)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)


def render_critical_rules(data: CriticalRulesContext, style: StyleEntry, config: ModuleConfig) -> str:
    """Render critical rules as a numbered list, varying by output tool config."""
    rules = []
    if data.has_output_tool:
        rules.append(f"**Use {data.tool_name} for all output** — never write files directly, never use a different write tool")
        if data.batch_size:
            rules.append(f"**Batch discipline** — process exactly {data.batch_size} records per batch (last batch may be smaller)")
            rules.append("**Write after every batch** — do not accumulate records in memory across batches")
        else:
            rules.append("**Validate before returning** — SUCCESS means all records passed schema validation")
    rules.append("**Fail fast** — if something is wrong, FAILURE immediately with clear reason")
    rules.append("**Stay in scope** — process only what you were given, nothing more")
    rules.append("**No invention** — if the data doesn't support it, don't produce it")

    content = list_as_numbered(rules)
    return section_frame(style.heading, 2, style.framing if config.framing else "", style.warning if config.warning else "", content)
