# CONSTRAINTS — TOML Extraction

## structure.toml

```toml
[constraints]
# Visibility / activation
section_visible = true

# Maximum entries to render (0 = render all). Truncates from the end, preserving author priority order.
max_entries_rendered = 0

preamble_visible = true
constraints_are_not_steps_visible = true
no_inferred_constraints_visible = false
closing_compliance_reminder_visible = true
constraint_count_heading_visible = true

# Variant selectors
preamble_variant = "standalone"       # "standalone" | "references_instructions" | "references_critical_rules"
closing_compliance_reminder_variant = "evaluation_warning"  # "evaluation_warning" | "simultaneity_reminder"
no_inferred_constraints_variant = "light"  # "light" | "explicit"
must_vs_must_not_normalization = "preserve_voice"  # "preserve_voice" | "normalize_outliers" | "prefix_tags"
```

**Decisions:**

- `no_inferred_constraints_visible`: Default false. Only enable when agents invent phantom constraints not in the list.
- `closing_compliance_reminder_visible` and `constraint_count_heading_visible`: Controlled by display.toml visibility thresholds (default 6).
- `preamble_variant`: "standalone" for solo sections. "references_critical_rules" when critical_rules co-exists — hierarchy framing is implicit in this variant.

## content.toml

```toml
[constraints]
heading = "Constraints"

# Preamble variants
preamble_standalone = "These constraints govern your execution. They are not sequenced — all are in force at all times. Each is a compliance standard your output will be measured against."
preamble_references_instructions = "While executing your instructions, these rules remain in effect."
preamble_references_critical_rules = "These constraints are binding operational rules — less absolute than critical rules, but more enforceable than general quality guidance. Violating a constraint means your output is defective."

# "Not steps" distinction
constraints_are_not_steps = "Constraints are not steps — they are conditions that must hold true at all times, not at specific points in your workflow."

# Constraint count header template
constraint_count_heading = "You have {{COUNT}} operational constraints:"

# Closing reinforcement variants
closing_compliance_reminder_evaluation_warning = "Every constraint above is auditable. Your output will be evaluated against each one."
closing_compliance_reminder_simultaneity = "All {{COUNT}} constraints apply simultaneously throughout execution."

# No-inference signal
no_inferred_constraints_light = "These are your operational constraints."
no_inferred_constraints_explicit = "These {{COUNT}} rules are exhaustive — do not infer additional constraints not listed here."

# Hierarchy framing (when folded into preamble)
hierarchy_tier_comparison = "These constraints are binding operational rules — less severe than critical rules but more enforceable than quality guidance."
hierarchy_three_tier_explanation = "You operate under three tiers of behavioral rules: critical rules (hard failures), constraints (compliance standards), and anti-patterns (quality risks). This section defines tier 2."
```

**Decisions:**

- `closing_compliance_reminder_evaluation_warning`: External review framing ("your output will be evaluated"). `closing_compliance_reminder_simultaneity`: Count + simultaneity reminder.
- `hierarchy_tier_comparison` vs `hierarchy_three_tier_explanation`: Relative comparison (decoupled, preferred) vs explicit three-tier model. Both render when `preamble_variant = "references_critical_rules"`.

## display.toml

```toml
[constraints]
# Enumeration format
enumeration_format = ["bulleted", "numbered"]
enumeration_format_threshold = 6

# Closing reinforcement activation threshold
closing_compliance_reminder_visibility_threshold = 6

# Constraint count heading activation threshold
constraint_count_heading_visibility_threshold = 6

# Polarity grouping for long lists
polarity_grouping_activation_threshold = 11
```

**Decisions:**

- Closing compliance reminder is mandatory above 10 (code invariant, overrides the threshold).
- `polarity_grouping_activation_threshold`: Advisory — triggers MUST/MUST NOT clustering for very long lists. Actual grouping logic is code.

## Excluded (invariant rules / bare data)

- **Sub-block ordering**: Preamble → not-steps distinction → count header → rule list → closing compliance reminder. Invariant.
- **Rule text passthrough**: Constraint rules render as-is. Template does not rewrite author content.
- **Mandatory closing at len > 10**: Code overrides the visibility threshold — always renders above 10.
- **No inline examples**: Constraints may reference the examples section but must not inline examples.
