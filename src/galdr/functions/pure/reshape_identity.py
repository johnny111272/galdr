"""Reshape identity section: select fields needed by template, unwrap RootModels."""

from galdr.functions.pure.unwrap import unwrap
from galdr.structures.anthropic_render import IdentityAnthropic
from galdr.structures.template_context import IdentityContext


def reshape_identity(identity: IdentityAnthropic) -> IdentityContext:
    """Select template-relevant fields from identity, excluding model (used in frontmatter)."""
    return IdentityContext(
        title=unwrap(identity.title),
        description=unwrap(identity.description),
        role_identity=unwrap(identity.role_identity),
        role_description=unwrap(identity.role_description) if identity.role_description else None,
        role_expertise=[unwrap(expertise) for expertise in identity.role_expertise.root] if identity.role_expertise else None,
        role_responsibility=unwrap(identity.role_responsibility),
    )
