"""Composition engine — assembles rendered sections into complete agent markdown.

Pure functions. No IO, no side effects.
"""

from galdr.functions.pure.render_sections import (
    render_anti_patterns,
    render_constraints,
    render_critical_rules,
    render_examples,
    render_failure_criteria,
    render_frontmatter,
    render_identity,
    render_input,
    render_instructions,
    render_output,
    render_return_format,
    render_security_boundary,
    render_success_criteria,
    render_writing_output,
)
from typing import Any

from galdr.structures.recipe import ModuleConfig, RecipeConfig
from galdr.functions.pure.defaults import default_section_style
from galdr.structures.style import DispatcherStyle, SectionStyle, StyleConfig
from galdr.structures.template_context import RenderContext


KNOWN_SECTIONS = frozenset(
    [
        "frontmatter",
        "identity",
        "security_boundary",
        "input",
        "instructions",
        "examples",
        "output",
        "writing_output",
        "constraints",
        "anti_patterns",
        "success_criteria",
        "failure_criteria",
        "return_format",
        "critical_rules",
    ]
)


def validate_section_names(recipe: RecipeConfig) -> list[str]:
    """Return list of unknown section names in a recipe. Empty = valid."""
    return [module.section for module in recipe.modules if module.section not in KNOWN_SECTIONS]


def validate_style_sections(style: StyleConfig) -> list[str]:
    """Return list of unknown section names in a style. Empty = valid."""
    return [name for name in style.sections if name not in KNOWN_SECTIONS]


def reshape_style_toml(parsed_toml: dict[str, Any]) -> dict[str, Any]:
    """Reshape flat style TOML into StyleConfig-compatible dict.

    Style TOML uses top-level [section_name] tables. StyleConfig expects
    sections: dict[str, SectionStyle]. This pops 'name' and 'dispatcher',
    wraps the rest as sections."""
    reshaped = dict(parsed_toml)
    name = reshaped.pop("name", None)
    dispatcher = reshaped.pop("dispatcher", None)
    result: dict[str, Any] = {"name": name, "sections": reshaped}
    if dispatcher is not None:
        result["dispatcher"] = dispatcher
    return result


def extract_section_data(section: str, context: RenderContext):
    """Extract the data for a section from the render context."""
    return getattr(context, section, None)


def resolve_renderer(section: str):
    """Resolve a section name to its renderer function."""
    renderers = {
        "frontmatter": render_frontmatter,
        "identity": render_identity,
        "security_boundary": render_security_boundary,
        "input": render_input,
        "instructions": render_instructions,
        "examples": render_examples,
        "output": render_output,
        "writing_output": render_writing_output,
        "constraints": render_constraints,
        "anti_patterns": render_anti_patterns,
        "success_criteria": render_success_criteria,
        "failure_criteria": render_failure_criteria,
        "return_format": render_return_format,
        "critical_rules": render_critical_rules,
    }
    return renderers[section]


def should_skip(section: str, data) -> bool:
    """Determine if a section should be skipped based on its data."""
    if data is None:
        return True
    if section == "security_boundary" and not data.has_grants:
        return True
    if section in ("success_criteria", "failure_criteria") and not data:
        return True
    return False


def render_module(section: str, data, style: SectionStyle, config: ModuleConfig) -> str:
    """Render a single module via its resolved renderer."""
    renderer = resolve_renderer(section)
    if section == "frontmatter":
        return renderer(data)
    return renderer(data, style, config)


def compose_agent(context: RenderContext, recipe: RecipeConfig, style: StyleConfig) -> str:
    """Compose a complete agent markdown file from context, recipe, and style.

    Iterates recipe modules, extracts data from context, calls section renderers,
    and joins results. Frontmatter is joined without a separator; all other
    sections are separated by ---."""
    frontmatter_result = ""
    body_sections = []

    for module in recipe.modules:
        data = extract_section_data(module.section, context)

        if should_skip(module.section, data):
            continue

        section_style = style.sections.get(module.section, default_section_style(module.section))
        rendered = render_module(module.section, data, section_style, module)

        if not rendered:
            continue

        if module.section == "frontmatter":
            frontmatter_result = rendered
        else:
            body_sections.append(rendered)

    body = "\n\n---\n\n".join(body_sections)

    if frontmatter_result and body:
        return frontmatter_result + "\n\n" + body + "\n"
    if frontmatter_result:
        return frontmatter_result + "\n"
    return body + "\n" if body else ""


def compose_dispatcher(context: RenderContext, style: StyleConfig | None = None) -> str:
    """Compose a complete dispatcher SKILL.md from context.

    Dispatcher structure is fixed — no recipe. Style controls text."""
    dispatcher = context.dispatcher
    if not dispatcher:
        return ""

    dispatcher_style = style.dispatcher if style and style.dispatcher else DispatcherStyle()

    frontmatter = render_dispatcher_frontmatter(dispatcher)
    body_sections = [
        render_dispatcher_header(dispatcher, context.identity.title, dispatcher_style),
        render_dispatcher_paths(context, dispatcher_style),
        render_dispatcher_with_arguments(dispatcher, dispatcher_style),
        render_dispatcher_scope_discovery(dispatcher, dispatcher_style),
    ]

    if dispatcher.dispatch_mode == "batch":
        body_sections.append(render_dispatcher_batch_splitting(dispatcher, dispatcher_style))

    body_sections.append(render_dispatcher_dispatch(dispatcher, dispatcher_style))
    body_sections.append(render_dispatcher_post_dispatch(dispatcher, dispatcher_style))
    body_sections.append(render_dispatcher_rules(dispatcher_style))

    body = "\n\n---\n\n".join(body_sections)
    return frontmatter + "\n\n" + body + "\n"


def render_dispatcher_frontmatter(dispatcher) -> str:
    """Render dispatcher SKILL.md frontmatter."""
    lines = [
        "---",
        f'name: dispatch-{dispatcher.agent_name}',
        f'description: {dispatcher.agent_description}',
    ]
    if dispatcher.parameters:
        hint_parts = [param.name for param in dispatcher.parameters]
        lines.append(f'argument-hint: "{" ".join(hint_parts)}"')
    lines.append("disable-model-invocation: true")
    lines.append("---")
    return "\n".join(lines)


def render_dispatcher_header(dispatcher, title: str, style: DispatcherStyle) -> str:
    """Render dispatch title and execution mode."""
    lines = [f"# {style.title_template.format(title=title)}"]
    lines.append(f"\n**{style.agent_label}** `{dispatcher.agent_name}`")

    if dispatcher.dispatch_mode == "batch":
        lines.append(
            f"**{style.execution_batch_template.format(min=dispatcher.batch_size[0], max=dispatcher.batch_size[1])}**"
        )
    else:
        lines.append(f"**{style.execution_full}**")

    return "\n".join(lines)


def render_dispatcher_paths(context: RenderContext, style: DispatcherStyle) -> str:
    """Render the paths table from input/output context."""
    rows = []

    if context.input.input_schema:
        rows.append(f"| {style.input_schema_label} | `{context.input.input_schema}` |")
    if context.input.context_required:
        for item in context.input.context_required:
            rows.append(f"| {item.label} | `{item.path}` |")
    if context.input.context_available:
        for item in context.input.context_available:
            rows.append(f"| {item.label} | `{item.path}` |")
    if context.output.schema_path:
        rows.append(f"| {style.output_schema_label} | `{context.output.schema_path}` |")
    if context.output.file_path:
        rows.append(f"| {style.output_file_label} | `{context.output.file_path}` |")
    if context.output.directory_path:
        rows.append(f"| {style.output_directory_label} | `{context.output.directory_path}` |")
    if context.output.output_directory:
        rows.append(f"| {style.output_directory_label} | `{context.output.output_directory}` |")

    header = f"## {style.paths_heading}\n\n| {style.table_header_label} | {style.table_header_path} |\n|-------|------|"
    return header + "\n" + "\n".join(rows) if rows else header


def render_dispatcher_with_arguments(dispatcher, style: DispatcherStyle) -> str:
    """Render the 'With Arguments' section."""
    return (
        f"## {style.with_args_heading}\n\n"
        f"{style.with_args_intro}\n\n"
        f"1. {style.with_args_step_validate}\n"
        f"2. {style.with_args_step_prepare.format(input_format=dispatcher.input_format)}\n"
        f"3. {style.with_args_step_dispatch}"
    )


def render_dispatcher_scope_discovery(dispatcher, style: DispatcherStyle) -> str:
    """Render the 'No Arguments — Scope Discovery' section."""
    delivery_note = " and write to a tempfile" if dispatcher.input_delivery == "tempfile" else ""
    return (
        f"## {style.scope_heading}\n\n"
        f"**{style.scope_mandatory_warning}**\n\n"
        f"{style.scope_intro}\n\n"
        f"1. {style.scope_step_assess}\n"
        f"2. {style.scope_step_present}\n"
        f"3. {style.scope_step_prepare.format(input_format=dispatcher.input_format, delivery_note=delivery_note)}\n"
        f"4. {style.scope_step_proceed}"
    )


def render_dispatcher_batch_splitting(dispatcher, style: DispatcherStyle) -> str:
    """Render the 'Batch Splitting' section (only for batch mode)."""
    return (
        f"## {style.batch_heading}\n\n"
        f"{style.batch_intro}\n\n"
        "```bash\n"
        f"split_jsonl_batches --input /tmp/input.jsonl --directory {dispatcher.agent_name} \\\n"
        f"  --min-batch {dispatcher.batch_size[0]} --max-batch {dispatcher.batch_size[1]}\n"
        "```\n\n"
        f"{style.batch_manifest_explanation}\n"
        "```json\n"
        f'{{"batch":1,"file":"/tmp/{dispatcher.agent_name}/batch_001.jsonl","records":50}}\n'
        "```\n\n"
        f"{style.batch_parse_instruction}"
    )


def render_dispatcher_dispatch(dispatcher, style: DispatcherStyle) -> str:
    """Render the 'Dispatch' section."""
    parts = [
        f"## {style.dispatch_heading}\n",
        f"{style.dispatch_launch_instruction}\n",
        f"{style.dispatch_background_warning}\n",
        f"{style.dispatch_call_intro}",
        f"- `subagent_type`: `{dispatcher.agent_name}`",
    ]

    if dispatcher.dispatch_mode == "batch":
        prompt_line = "- `prompt`: Path to the batch tempfile"
    else:
        prompt_line = "- `prompt`: Path to the input"
        if dispatcher.input_delivery == "tempfile":
            prompt_line += " tempfile"

    if dispatcher.parameters:
        extra_params = [param.name for param in dispatcher.parameters if param.name != "tempfile"]
        if extra_params:
            prompt_line += " + " + " + ".join(f"`{name}`" for name in extra_params)

    parts.append(prompt_line)
    parts.append(style.dispatch_tempfile_note)

    return "\n".join(parts)


def render_dispatcher_post_dispatch(dispatcher, style: DispatcherStyle) -> str:
    """Render the 'Post-Dispatch' section."""
    return (
        f"## {style.post_dispatch_heading}\n\n"
        f"1. {style.post_dispatch_step_collect}\n"
        f"2. {style.post_dispatch_step_report.format(return_mode=dispatcher.return_mode)}\n"
        f"3. {style.post_dispatch_step_redispatch}"
    )


def render_dispatcher_rules(style: DispatcherStyle) -> str:
    """Render the 'Rules' section."""
    return (
        f"## {style.rules_heading}\n\n"
        f"1. {style.rule_thin_prompt}\n"
        f"2. {style.rule_foreground}\n"
        f"3. {style.rule_tempfiles}\n"
        f"4. {style.rule_no_cache}\n"
        f"5. {style.rule_user_invoked}"
    )
