"""Reshape return format section: rename *_definition/*_evidence fields."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import (
    FailureCriteria,
    ReturnFormat,
    SuccessCriteria,
)
from galdr.structures.template_context import (
    FailureCriterionContext,
    ReturnFormatContext,
    SuccessCriterionContext,
)


def reshape_return_format(return_format: ReturnFormat) -> ReturnFormatContext:
    """Rename success_definition/success_evidence to definition/evidence."""
    return ReturnFormatContext(
        mode=unwrap(return_format.mode),
        status_instruction=unwrap(return_format.status_instruction) if return_format.status_instruction else None,
        metrics_instruction=unwrap(return_format.metrics_instruction) if return_format.metrics_instruction else None,
        output_instruction=unwrap(return_format.output_instruction) if return_format.output_instruction else None,
        success_criteria=reshape_success(return_format.success_criteria),
        failure_criteria=reshape_failure(return_format.failure_criteria),
    )


def reshape_success(criteria: SuccessCriteria | None) -> list[SuccessCriterionContext] | None:
    """Reshape success criteria list from schema model."""
    if criteria is None:
        return None
    return [
        SuccessCriterionContext(
            definition=unwrap(item.success_definition),
            evidence=[unwrap(evidence) for evidence in item.success_evidence.root],
        )
        for item in criteria.root
    ]


def reshape_failure(criteria: FailureCriteria | None) -> list[FailureCriterionContext] | None:
    """Reshape failure criteria list from schema model."""
    if criteria is None:
        return None
    return [
        FailureCriterionContext(
            definition=unwrap(item.failure_definition),
            evidence=[unwrap(evidence) for evidence in item.failure_evidence.root],
        )
        for item in criteria.root
    ]
