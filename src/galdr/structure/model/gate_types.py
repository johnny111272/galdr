"""Typed wrappers for Nornir gate responses."""

from pydantic import BaseModel, ConfigDict


class GateError(BaseModel):
    """Error detail from a failed gate validation."""

    model_config = ConfigDict(frozen=True)

    type: str
    message: str


class GateResult(BaseModel):
    """Response from a Nornir gate validate() call."""

    model_config = ConfigDict(frozen=True)

    ok: bool
    data: str | None = None
    error: GateError | None = None
