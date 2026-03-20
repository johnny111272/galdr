# RETURN_FORMAT — TOML Extraction

## structure.toml

```toml
[return_format]
# Two-channel model: output goes to files, return carries status signal
files_vs_status_explanation_preamble_visible = true

# Protocol preamble: tokens are machine-parsed, first-position requirement
token_must_be_first_word_preamble_visible = true

# Metrics obligation: agents must report all specified metrics
report_all_metrics_postscript_visible = true

# ABORT vs FAILURE semantic distinction (conditional on ABORT in status_instruction)
abort_vs_failure_distinction_preamble_visible = true

# Failure honesty: explicit permission to return clean FAILURE
honest_failure_over_dubious_success_preamble_visible = true

# Retroactive orientation: return requirements imply tracking requirements
track_metrics_as_you_work_postscript_visible = true

# Accuracy clause: report actual metrics, do not fabricate
do_not_fabricate_metrics_postscript_visible = true

# Cross-reference to failure_criteria section
failure_cross_reference_preamble_visible = false
```

**Decisions:**
- `files_vs_status_explanation`: Structural toggle for the two-channel explanation. Only relevant when mode="status" (only observed mode). Combined audience distinction into this single toggle per B's approach — separating them adds complexity with no observed benefit.
- `token_must_be_first_word`: Highest-priority fragment per both analyses. Always on for status mode but toggle allows hypothetical non-status modes to suppress it.
- `report_all_metrics`: Structural because agents will omit metrics without it. The downstream-dependency framing vs threat framing is a content concern, not structure.
- `abort_vs_failure_distinction`: Structural toggle. Conditional on ABORT appearing in status_instruction — code checks that condition, toggle controls whether the fragment renders at all.
- `honest_failure_over_dubious_success`: Universal, second-highest-priority fragment. Toggle exists for completeness but expected always-on.
- `track_metrics_as_you_work`: Controls whether agents get the "track as you work" instruction. Formatting-stability in source but structural in behavioral impact.
- `do_not_fabricate_metrics`: Prevents metric fabrication. Low cost, meaningful downside protection.
- `failure_cross_reference`: Defaulted to false. Experimental stability — explicit bridge between failure_criteria and return_format. Off by default; well-structured prompts may not need it.

## content.toml

```toml
[return_format]
heading = "Return Protocol"

files_vs_status_explanation_preamble = "Your return mode is status. Your work products go to files. Your return goes to the dispatcher as a brief status signal — not the deliverable."

token_must_be_first_word_preamble = "Your return must begin with a protocol token. The dispatch layer parses this token programmatically. Do not paraphrase or embed in prose — it must appear as the first word."

token_must_be_first_word_tokens_three = "Three terminal states: SUCCESS, FAILURE, or ABORT."
token_must_be_first_word_tokens_two = "Two terminal states: SUCCESS or FAILURE."

report_completion_label = "Report your completion as follows:"

report_all_metrics_postscript = "Report all metrics specified for your return state. The dispatcher and downstream processes depend on these values being present."

abort_vs_failure_distinction_preamble = "ABORT means you determined the work should not be attempted — inputs insufficient, prerequisites missing. ABORT is not failure. It is a responsible decision to stop before producing bad output."

honest_failure_over_dubious_success_preamble = "An honest FAILURE is better than a dubious SUCCESS. If your work did not meet success conditions, return FAILURE. A clean FAILURE with a clear reason is more valuable than a SUCCESS with compromised output."

track_metrics_as_you_work_postscript = "Your return requirements imply tracking requirements. If you must report a count, maintain that count as you work. If you must report a path, know the path before you write."

track_metrics_as_you_work_antidrift = "The dispatcher is waiting for your return signal. When you reach a terminal state, report it immediately. Do not continue work after reaching a terminal state."

do_not_fabricate_metrics_postscript = "Report actual metrics from your execution. Do not fabricate values to match the expected format."

failure_cross_reference_preamble = "The conditions for failure are defined in your failure criteria. Here, you learn how to report failure to the dispatcher."
```

**Decisions:**
- `section_heading`: "Return Protocol" chosen over "Completion Protocol" — both outperform "Return Format" but "Return Protocol" is more direct. Marginal difference per synthesis.
- `files_vs_status_explanation_preamble`: Merged A's two-channel clarity with B's machine-parsing context. Single prose block names both channels explicitly.
- `token_must_be_first_word_preamble`: Kept A's explicit positional instruction ("first word"). This is the highest-priority fragment — clarity over terseness.
- `token_must_be_first_word_tokens_three` / `_two`: Two variants for the conditional ABORT branch. Code selects based on status_instruction content.
- `report_completion_label`: Chose "Report your completion as follows:" — direct imperative, minimal framing. The status_instruction itself is verbatim from the definition author and is NOT a content knob (it passes through as data).
- `report_all_metrics_postscript`: Position as postscript because it follows the verbatim status_instruction. Chose A's downstream-dependency framing over B's pure threat language — explaining WHY is hypothesized more effective.
- `abort_vs_failure_distinction_preamble`: A's "responsible professional decision" framing. Critical for preventing agents from defaulting all non-success to FAILURE.
- `honest_failure_over_dubious_success_preamble`: Combined A's signal-integrity appeal with B's explicit-permission framing. Both analyses rank this second-highest priority.
- `track_metrics_as_you_work_postscript`: A's concrete operational version ("if you must report a count, maintain that count").
- `track_metrics_as_you_work_antidrift`: B's anti-drift instruction kept as separate field. More valuable for batch tasks — code can conditionally include.
- `do_not_fabricate_metrics_postscript`: Kept standalone rather than embedded in report_all_metrics. Cleaner for conditional inclusion per synthesis recommendation.
- `failure_cross_reference_preamble`: Explicit bridge text. Renders only when structure toggle is on.

## display.toml

```toml
[return_format]
# No display knobs for this section.
```

## Excluded (invariant rules / bare data)

- **Sub-block ordering**: token_must_be_first_word → status_instruction → report_all_metrics → honest_failure_over_dubious_success. Invariant.
- **status_instruction verbatim pass-through**: Author's status_instruction text is data. Passes through unmodified.
- **mode="status" gate**: Entire section assumes status mode. Other modes would need a different section entirely.
