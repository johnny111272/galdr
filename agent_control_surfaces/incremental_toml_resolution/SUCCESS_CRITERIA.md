# SUCCESS_CRITERIA -- TOML Extraction

## structure.toml

```toml
[success_criteria]
# Master visibility toggle
section_visible = true

# Maximum entries to render (0 = render all). Truncates from the end, preserving author priority order.
max_entries_rendered = 0

# Definition framing paradigm: "declarative_assertion" | "conditional_gate" | "completion_identity"
definition_framing_variant = "declarative_assertion"

# Evidence list framing paradigm: "properties" | "verification_checklist" | "quality_signals"
evidence_framing_variant = "properties"

# Hierarchy connector paradigm: "goal_then_criteria" | "proof" | "dual_presentation"
definition_to_evidence_transition_variant = "goal_then_criteria"

# Evidence type handling: "graduated_language" (per-item type markers) | "undifferentiated" (all items equal)
evidence_type_handling_variant = "undifferentiated"

# Voice paradigm: "output_centric" | "agent_centric"
output_vs_agent_voice_variant = "output_centric"

# Whether to include explicit statement that success != not-failing
success_failure_independence_statement_visible = true

# Whether to include verification guidance suffix for mixed evidence lists
verification_guidance_suffix_visible = false

# Multi-criteria relationship paradigm (only applies when criteria_count > 1): "independent_blocks" | "numbered_dimensions"
multi_criteria_relationship = "independent_blocks"
```

**Decisions:**

- `definition_framing_variant`: Declarative assertion (safest). Conditional gate (batch agents). Completion identity (creative agents).
- `evidence_framing_variant`: Properties (general). Verification checklist (mechanical). Quality signals (judgment).
- `output_vs_agent_voice_variant`: Output-centric promotes objective evaluation. Agent-centric pairs with strong role identity.
- `multi_criteria_relationship`: "independent_blocks" is the only tested approach; "numbered_dimensions" is speculative.

## content.toml

```toml
[success_criteria]
heading = "Success Criteria"

# Definition framing templates (one per paradigm)
definition_framing_declarative_assertion = "{{DEFINITION}}"
definition_framing_conditional_gate = "This task is complete if and only if: {{DEFINITION}}"
definition_framing_completion_identity = "You have succeeded when {{DEFINITION}}"

# Evidence list preamble templates (one per paradigm)
evidence_framing_properties = "A successful output has these properties:"
evidence_framing_verification_checklist = "Verify each of the following before declaring completion:"
evidence_framing_quality_signals = "You know you have succeeded when all of the following are true:"

# Hierarchy connector templates (one per paradigm)
definition_to_evidence_transition_goal_then_criteria = "Meeting this standard means:"
definition_to_evidence_transition_proof = "This is proven by:"
definition_to_evidence_transition_dual_presentation = "You can confirm this by checking:"

# Verification guidance suffix (appended after evidence list when enabled)
verification_guidance_suffix = "Some conditions above are mechanically verifiable; others require your judgment. Apply appropriate rigor to each."

# Success-failure independence statement
success_failure_independence_statement = "Success criteria define quality. Failure criteria define breakage. These are independent evaluations."

# Multi-criteria transition (between criteria blocks when count > 1)
multi_criteria_transition = "Additionally:"
```

**Decisions:**

- `definition_framing_declarative_assertion`: Bare data, no added framing — the definition's own phrasing is sufficient.
- `definition_to_evidence_transition_*`: Claim-warrant linkers. Goal-then-criteria (natural), proof (formal), dual-presentation (verification role).

## display.toml

```toml
[success_criteria]
# Evidence item format: threshold-based on evidence count
evidence_format_threshold = 5
evidence_format = ["bulleted", "numbered"]
```

**Decisions:**

- `evidence_format`: Bulleted above 5 (reduces false priority signaling). Numbered at ≤5 (implicit priority ordering).

## Excluded (invariant rules / bare data)

- **Claim-warrant hierarchy**: Definition is primary, evidence is subordinate. Code renders definition first, evidence second, with connector. Never flattened.
- **Multiple criteria are conjunctive**: Always AND, never OR. Data-model invariant.
