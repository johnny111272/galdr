"""Per-section style models for the composition engine.

Each section has its own model with typed fields for all configurable text.
Defaults match the current rendered output — changing a default changes the voice.
"""

from pydantic import BaseModel, ConfigDict


# --- Base ---


class SectionStyle(BaseModel):
    """Base for section styles. Provides heading, framing, and warning."""

    model_config = ConfigDict(frozen=True)
    heading: str = ""
    framing: str = ""
    warning: str = ""


# --- Agent section styles ---


class FrontmatterStyle(SectionStyle):
    """Frontmatter is machine-parsed. No configurable text beyond base."""


class IdentityStyle(SectionStyle):
    """Text for the identity section."""

    purpose_label: str = "Purpose"
    role_identity_template: str = "You are a {role_identity}."
    responsibility_label: str = "Your responsibility"
    expertise_label: str = "Expertise"


class SecurityBoundaryStyle(SectionStyle):
    """Text for the security boundary section."""

    heading: str = "Security Boundary"
    preamble: str = "This agent operates under `bypassPermissions` with hook-based restrictions."
    grants_intro: str = "The following operations are allowed — everything else is blocked by the system."
    boundary_warning: str = "Do not attempt operations outside this boundary. They will fail silently and cannot be approved interactively."


class InputStyle(SectionStyle):
    """Text for the input section."""

    heading: str = "Input"
    parameters_intro: str = "The dispatcher provides:"
    schema_intro: str = "Input validates against:"
    required_context_label: str = "Required context:"
    available_context_label: str = "Available context:"
    optional_suffix: str = "(optional)"


class InstructionsStyle(SectionStyle):
    """Text for the instructions section."""

    heading: str = "Processing"


class ExamplesStyle(SectionStyle):
    """Text for the examples section."""

    heading: str = "Examples"


class OutputStyle(SectionStyle):
    """Text for the output section."""

    heading: str = "Output"
    schema_label: str = "Schema"
    file_label: str = "Output file"
    directory_label: str = "Output directory"


class WritingOutputStyle(SectionStyle):
    """Text for the writing output section."""

    heading: str = "Writing Output (MANDATORY)"


class ConstraintsStyle(SectionStyle):
    """Text for the constraints section."""

    heading: str = "Constraints"


class AntiPatternsStyle(SectionStyle):
    """Text for the anti-patterns section."""

    heading: str = "Anti-Patterns"


class SuccessCriteriaStyle(SectionStyle):
    """Text for the success criteria section."""

    heading: str = "Success Criteria"
    evidence_label: str = "Evidence:"


class FailureCriteriaStyle(SectionStyle):
    """Text for the failure criteria section."""

    heading: str = "Failure Criteria"
    evidence_label: str = "Evidence:"


class ReturnFormatStyle(SectionStyle):
    """Text for the return format section."""

    heading: str = "Return Format"
    success_label: str = "On success:"
    failure_label: str = "On failure:"
    success_code: str = "SUCCESS"
    failure_code_template: str = "FAILURE: <reason>"


class CriticalRulesStyle(SectionStyle):
    """Text for the critical rules section."""

    heading: str = "Critical Rules"
    tool_rule: str = "**Use {tool_name} for all output** — never write files directly, never use a different write tool"
    batch_rule: str = "**Batch discipline** — process exactly {batch_size} records per batch (last batch may be smaller)"
    write_after_batch_rule: str = "**Write after every batch** — do not accumulate records in memory across batches"
    validate_rule: str = "**Validate before returning** — SUCCESS means all records passed schema validation"
    fail_fast_rule: str = "**Fail fast** — if something is wrong, FAILURE immediately with clear reason"
    stay_in_scope_rule: str = "**Stay in scope** — process only what you were given, nothing more"
    no_invention_rule: str = "**No invention** — if the data doesn't support it, don't produce it"


# --- Dispatcher style ---


class DispatcherStyle(BaseModel):
    """Text for all dispatcher sections."""

    model_config = ConfigDict(frozen=True)

    # header
    title_template: str = "Dispatch: {title}"
    agent_label: str = "Agent:"
    execution_batch_template: str = "Execution: BATCH — one agent per batch (~{min}-{max} entries), parallel"
    execution_full: str = "Execution: FULL — single agent, all input at once"

    # paths
    paths_heading: str = "Paths"
    input_schema_label: str = "Input schema"
    output_schema_label: str = "Output schema"
    output_file_label: str = "Output file"
    output_directory_label: str = "Output directory"
    table_header_label: str = "Label"
    table_header_path: str = "Path"

    # with arguments
    with_args_heading: str = "With Arguments"
    with_args_intro: str = "When the user provides specific targets:"
    with_args_step_validate: str = "Validate the targets exist"
    with_args_step_prepare: str = "Prepare input ({input_format} format)"
    with_args_step_dispatch: str = "Dispatch directly — skip scope discovery"

    # scope discovery
    scope_heading: str = "No Arguments — Scope Discovery"
    scope_mandatory_warning: str = "MANDATORY: Every step requires actual tool calls. Never use cached or remembered state."
    scope_intro: str = "When the user provides no arguments:"
    scope_step_assess: str = "**Assess state** — Read the filesystem to determine what work exists, what is already done, and what is stale"
    scope_step_present: str = "**Present options** — Use AskUserQuestion to present sensible choices to the user"
    scope_step_prepare: str = "**Prepare input** — Based on user selection, prepare the {input_format} input{delivery_note}"
    scope_step_proceed: str = "Proceed to dispatch"

    # batch splitting
    batch_heading: str = "Batch Splitting"
    batch_intro: str = "Split input into batches using `split_jsonl_batches`:"
    batch_manifest_explanation: str = "This outputs a JSONL manifest to stdout — one line per batch:"
    batch_parse_instruction: str = "Parse the manifest. Each line is one agent invocation."

    # dispatch
    dispatch_heading: str = "Dispatch"
    dispatch_launch_instruction: str = "Launch ALL Agent tool calls in a **SINGLE message** for foreground parallel execution."
    dispatch_background_warning: str = "**Do NOT use `run_in_background`.** Foreground parallel returns all results in one response."
    dispatch_call_intro: str = "Each Agent call:"
    dispatch_tempfile_note: str = "Tempfiles survive agent failure — failed batches can be redispatched without regenerating input."

    # post-dispatch
    post_dispatch_heading: str = "Post-Dispatch"
    post_dispatch_step_collect: str = "Collect all agent results"
    post_dispatch_step_report: str = "Report aggregate summary ({return_mode} format)"
    post_dispatch_step_redispatch: str = "If any agents failed, offer to redispatch the failed batches"

    # rules
    rules_heading: str = "Rules"
    rule_thin_prompt: str = "**Task prompt is thin.** `subagent_type` + input path + parameters. The agent already knows its job."
    rule_foreground: str = "**Foreground parallel.** All Agent calls in a single message. No background dispatch."
    rule_tempfiles: str = "**Tempfiles survive failure.** Never clean up tempfiles automatically."
    rule_no_cache: str = "**State is never cached.** Every filesystem check is a real tool call."
    rule_user_invoked: str = "**User-invoked only.** This skill runs only when explicitly requested."


# --- Top-level config ---


class StyleConfig(BaseModel):
    """Complete style: per-section text models + optional dispatcher text."""

    model_config = ConfigDict(frozen=True)
    name: str
    sections: dict[str, SectionStyle]
    dispatcher: DispatcherStyle | None = None


