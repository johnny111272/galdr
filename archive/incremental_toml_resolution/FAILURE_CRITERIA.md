# FAILURE_CRITERIA — TOML Extraction

## structure.toml

```toml
[failure_criteria]
# Master visibility toggle
section_visible = true

# Maximum entries to render (0 = render all). Truncates from the end, preserving author priority order.
max_entries_rendered = 0

# Whether to render the behavioral preamble that reframes abort as correct action
abort_stance_preamble_visible = true

# Whether to include hierarchy framing connecting definition/evidence to return_format reporting
cite_definition_and_evidence_postscript_visible = false

# Whether to include the generic temporal instruction
check_before_and_during_visible = false

# Abort behavioral posture: "obligation" = MUST stop (batch/binary evidence), "permission" = correct action is to stop (creative/judgment evidence)
abort_stance_variant = "obligation"  # governs: abort_stance_preamble_*, abort_stance_definition_label_*
```

**Decisions:**

- `abort_stance_variant`: Highest-impact variable. "obligation" = MUST stop (batch/binary agents). "permission" = correct action is to stop (creative/judgment agents). Experimental — may need to be conditional on agent type.
- `cite_definition_and_evidence_visible`: Off by default — conditional on return_format section existing.

## content.toml

```toml
[failure_criteria]
# Section heading
heading = "Abort Conditions"

# Behavioral preamble — the completion-bias override
abort_stance_preamble_obligation = "The following conditions make valid output impossible. When detected, stop immediately and report. Producing output after detecting a halt condition is worse than producing no output — it is confidently wrong output that downstream consumers will trust."
abort_stance_preamble_permission = "Not every task can be completed. The following conditions indicate the task cannot produce valid output. The correct action is to stop and report. Attempting to force output past these conditions violates quality standards."

# Multi-criteria disjunction statement (rendered only when >1 failure criterion exists)
any_one_triggers_abort = "Any ONE of the following failure modes is sufficient to trigger abort."

# Label template preceding each failure definition
abort_stance_definition_label_obligation = "Halt condition:"
abort_stance_definition_label_permission = "This work cannot succeed when:"

# Evidence list introduction
evidence_preamble = "Any of the following indicates this failure — one signal is sufficient:"

# Hierarchy framing — reporting instruction connecting to return_format
cite_definition_and_evidence_postscript = "Each failure mode has a definition (what went wrong) and evidence (how you detect it). When reporting failure, cite both."

# Generic temporal instruction
check_before_and_during = "Check what you can before starting. Monitor the rest throughout."
```

**Decisions:**

- `heading`: "Abort Conditions" is the primary knob if testing shows heading affects abort willingness. Alternative: "Conditions That Prevent Success".
- `preamble_obligation`: Sharp inversion frame (halting = success, continuing = failure). `preamble_permission`: Normalizes incompletability, appeals to quality standards.
- `any_one_triggers_abort`: Code renders only when >1 failure criterion exists.

## display.toml

```toml
[failure_criteria]
# Evidence item format
evidence_format = "bare"

# No other display knobs — evidence items are bare, disjunction is code-gated on count > 1
```

**Decisions:**

- `evidence_format`: "bare" — list introduction carries behavioral weight; items just need to be scannable. Alternatives: "conditional" (`IF...THEN`), "signal" (`SIGNAL: ...`).

## Excluded (invariant rules / bare data)

- **Failure/success independence**: Never frame failure criteria as the opposite of success criteria. Cross-section invariant.
- **Failure/guardrails boundary**: Guardrails = course-correct, failure = halt. Architectural invariant.
- **Sub-block ordering**: Definition before evidence within each criterion. Invariant.
- **Disjunction statement at count > 1**: Always renders `any_one_triggers_abort` when multiple criteria exist. Invariant.
