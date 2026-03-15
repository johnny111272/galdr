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
from galdr.structures.style import StyleConfig, StyleEntry
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
    sections: dict[str, StyleEntry]. This pops 'name' and wraps the rest."""
    reshaped = dict(parsed_toml)
    name = reshaped.pop("name", None)
    return {"name": name, "sections": reshaped}


def extract_section_data(section: str, context: RenderContext):
    """Extract the data for a section from the render context."""
    if section == "success_criteria":
        return context.return_format.success_criteria
    if section == "failure_criteria":
        return context.return_format.failure_criteria
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


def render_module(section: str, data, style: StyleEntry, config: ModuleConfig) -> str:
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

        section_style = style.sections.get(module.section, StyleEntry())
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


def compose_dispatcher(context: RenderContext) -> str:
    """Compose a complete dispatcher SKILL.md from context.

    Fixed structure — no recipe or style. The dispatcher template has its own
    layout that doesn't vary."""
    dispatcher = context.dispatcher
    if not dispatcher:
        return ""

    frontmatter = render_dispatcher_frontmatter(dispatcher)
    body_sections = [
        render_dispatcher_header(dispatcher, context.identity.title),
        render_dispatcher_paths(context),
        render_dispatcher_with_arguments(dispatcher),
        render_dispatcher_scope_discovery(dispatcher),
    ]

    if dispatcher.dispatch_mode == "batch":
        body_sections.append(render_dispatcher_batch_splitting(dispatcher))

    body_sections.append(render_dispatcher_dispatch(dispatcher))
    body_sections.append(render_dispatcher_post_dispatch(dispatcher))
    body_sections.append(render_dispatcher_rules())

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


def render_dispatcher_header(dispatcher, title: str) -> str:
    """Render dispatch title and execution mode."""
    lines = [f"# Dispatch: {title}"]
    lines.append(f"\n**Agent:** `{dispatcher.agent_name}`")

    if dispatcher.dispatch_mode == "batch":
        lines.append(
            f"**Execution:** BATCH — one agent per batch "
            f"(~{dispatcher.batch_size[0]}-{dispatcher.batch_size[1]} entries), parallel"
        )
    else:
        lines.append("**Execution:** FULL — single agent, all input at once")

    return "\n".join(lines)


def render_dispatcher_paths(context: RenderContext) -> str:
    """Render the paths table from input/output context."""
    rows = []

    if context.input.input_schema:
        rows.append(f"| Input schema | `{context.input.input_schema}` |")
    if context.input.context_required:
        for item in context.input.context_required:
            rows.append(f"| {item.label} | `{item.path}` |")
    if context.input.context_available:
        for item in context.input.context_available:
            rows.append(f"| {item.label} | `{item.path}` |")
    if context.output.schema_path:
        rows.append(f"| Output schema | `{context.output.schema_path}` |")
    if context.output.file_path:
        rows.append(f"| Output file | `{context.output.file_path}` |")
    if context.output.directory_path:
        rows.append(f"| Output directory | `{context.output.directory_path}` |")
    if context.output.output_directory:
        rows.append(f"| Output directory | `{context.output.output_directory}` |")

    header = "## Paths\n\n| Label | Path |\n|-------|------|"
    return header + "\n" + "\n".join(rows) if rows else header


def render_dispatcher_with_arguments(dispatcher) -> str:
    """Render the 'With Arguments' section."""
    return (
        "## With Arguments\n\n"
        "When the user provides specific targets:\n\n"
        f"1. Validate the targets exist\n"
        f"2. Prepare input ({dispatcher.input_format} format)\n"
        "3. Dispatch directly — skip scope discovery"
    )


def render_dispatcher_scope_discovery(dispatcher) -> str:
    """Render the 'No Arguments — Scope Discovery' section."""
    delivery_note = " and write to a tempfile" if dispatcher.input_delivery == "tempfile" else ""
    return (
        "## No Arguments — Scope Discovery\n\n"
        "**MANDATORY: Every step requires actual tool calls. Never use cached or remembered state.**\n\n"
        "When the user provides no arguments:\n\n"
        "1. **Assess state** — Read the filesystem to determine what work exists, what is already done, and what is stale\n"
        "2. **Present options** — Use AskUserQuestion to present sensible choices to the user\n"
        f"3. **Prepare input** — Based on user selection, prepare the {dispatcher.input_format} input{delivery_note}\n"
        "4. Proceed to dispatch"
    )


def render_dispatcher_batch_splitting(dispatcher) -> str:
    """Render the 'Batch Splitting' section (only for batch mode)."""
    return (
        "## Batch Splitting\n\n"
        "Split input into batches using `split_jsonl_batches`:\n\n"
        "```bash\n"
        f"split_jsonl_batches --input /tmp/input.jsonl --directory {dispatcher.agent_name} \\\n"
        f"  --min-batch {dispatcher.batch_size[0]} --max-batch {dispatcher.batch_size[1]}\n"
        "```\n\n"
        "This outputs a JSONL manifest to stdout — one line per batch:\n"
        "```json\n"
        f'{{"batch":1,"file":"/tmp/{dispatcher.agent_name}/batch_001.jsonl","records":50}}\n'
        "```\n\n"
        "Parse the manifest. Each line is one agent invocation."
    )


def render_dispatcher_dispatch(dispatcher) -> str:
    """Render the 'Dispatch' section."""
    parts = [
        "## Dispatch\n",
        "Launch ALL Agent tool calls in a **SINGLE message** for foreground parallel execution.\n",
        "**Do NOT use `run_in_background`.** Foreground parallel returns all results in one response.\n",
        "Each Agent call:",
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
    parts.append("Tempfiles survive agent failure — failed batches can be redispatched without regenerating input.")

    return "\n".join(parts)


def render_dispatcher_post_dispatch(dispatcher) -> str:
    """Render the 'Post-Dispatch' section."""
    return (
        "## Post-Dispatch\n\n"
        "1. Collect all agent results\n"
        f"2. Report aggregate summary ({dispatcher.return_mode} format)\n"
        "3. If any agents failed, offer to redispatch the failed batches"
    )


def render_dispatcher_rules() -> str:
    """Render the 'Rules' section."""
    return (
        "## Rules\n\n"
        "1. **Task prompt is thin.** `subagent_type` + input path + parameters. The agent already knows its job.\n"
        "2. **Foreground parallel.** All Agent calls in a single message. No background dispatch.\n"
        "3. **Tempfiles survive failure.** Never clean up tempfiles automatically.\n"
        "4. **State is never cached.** Every filesystem check is a real tool call.\n"
        "5. **User-invoked only.** This skill runs only when explicitly requested."
    )
