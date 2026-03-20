"""Reshape return format and criteria sections."""

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
    """Reshape return format fields. Criteria are separate sections."""
    return ReturnFormatContext(
        mode=unwrap(return_format.mode),
        status_instruction=unwrap(return_format.status_instruction) if return_format.status_instruction else None,
        metrics_instruction=unwrap(return_format.metrics_instruction) if return_format.metrics_instruction else None,
        output_instruction=unwrap(return_format.output_instruction) if return_format.output_instruction else None,
    )


def reshape_success_criteria(criteria: SuccessCriteria) -> list[SuccessCriterionContext]:
    """Reshape success criteria from schema model."""
    return [
        SuccessCriterionContext(
            definition=unwrap(item.success_definition),
            evidence=[unwrap(evidence) for evidence in item.success_evidence.root],
        )
        for item in criteria.criteria.root
    ]


def reshape_failure_criteria(criteria: FailureCriteria) -> list[FailureCriterionContext]:
    """Reshape failure criteria from schema model."""
    return [
        FailureCriterionContext(
            definition=unwrap(item.failure_definition),
            evidence=[unwrap(evidence) for evidence in item.failure_evidence.root],
        )
        for item in criteria.criteria.root
    ]
