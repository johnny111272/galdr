# INSTRUCTIONS -- TOML Extraction

## structure.toml
```toml
[instructions]
# Heading
heading_variant = "default"                   # "default" | "procedure" | "steps_with_count"

# Mode infrastructure
exact_vs_judgment_explanation_visible = "auto" # "auto" (render when mixed modes) | "always" | "never"
exact_vs_judgment_marker_placement = "header_fused"  # "header_fused" | "body_prefix" | "visual_formatting"
signal_at_mode_change_boundaries_visible = false

# Preamble components
instructions_preamble_step_count_visible = true
instructions_preamble_no_add_skip_reorder_visible = true
instructions_preamble_exact_vs_judgment_preview_visible = true
instructions_preamble_no_extra_operations_visible = true

# Step structure
step_index_tracking = "n_of_m"  # "n_only" | "n_of_m"
step_body_container_visible = false
step_done_when_suffix_visible = false

# Closer
section_closer_visible = true
section_closer_exact_vs_judgment_recap_visible = false

# Dependency and progress
cross_step_dependency_phrases_visible = false
halfway_point_reminder_visible = false

# Scaffolding tier override (null = auto from step count)
structural_complexity_override = "auto"  # "auto" | "lightweight" | "standard" | "heavy"
```
**Decisions:**

- `signal_at_mode_change_boundaries_visible`: Off by default — synthesis warns against combining all four mode layers simultaneously.
- `step_done_when_suffix_visible`: Experimental. `{{completion_condition}}` is template-generated, not author data.
- `cross_step_dependency_phrases_visible` and `halfway_point_reminder_visible`: Conditional on step count (7+). Lightweight agents don't need these.
- `structural_complexity_override`: "auto" derives from step count. Override when auto-detection makes wrong choice.

## content.toml
```toml
[instructions]
# Heading — selector among variants (moved from structure: this is prose selection, not structural)
heading_default = "Instructions"
heading_procedure = "Procedure"
heading_steps_with_count = "Steps ({{step_count}} total)"

# Mode preamble
exact_vs_judgment_explanation_mixed = "Steps marked (exact) must be followed precisely with no interpretation. Steps marked (judgment) require your reasoning and expertise."
exact_vs_judgment_explanation_uniform_exact = "Every step below is exact. Execute each one precisely as written."
exact_vs_judgment_explanation_uniform_judgment = "Every step below requires your judgment. Apply your reasoning and expertise throughout."

# Instructions preamble
instructions_preamble_step_count = "You will execute {{step_count}} steps."
instructions_preamble_no_add_skip_reorder = "Do not add steps. Do not skip steps. Do not reorder steps."
instructions_preamble_exact_vs_judgment_preview = "Steps marked (exact) leave no room for interpretation. Steps marked (judgment) are where your reasoning matters."
instructions_preamble_no_extra_operations_postscript = "Each instruction step is a complete specification. Do not supplement steps with general knowledge or add operations not specified."

# Step header
step_header_exact = "**Step {{step_n}} of {{step_total}} (exact).**"
step_header_judgment = "**Step {{step_n}} of {{step_total}} (judgment).**"
step_header_exact_n_only = "**Step {{step_n}} (exact).**"
step_header_judgment_n_only = "**Step {{step_n}} (judgment).**"

# Mode body prefix (alternative to header-fused)
exact_vs_judgment_body_prefix_exact = "EXECUTE EXACTLY:"
exact_vs_judgment_body_prefix_judgment = "APPLY JUDGMENT:"

# Mode transition signal
signal_at_mode_change_to_exact = "The following step must be executed exactly."
signal_at_mode_change_to_judgment = "The following step requires your judgment."

# Step completion suffix (probabilistic steps only)
step_done_when_suffix = "Done when: {{completion_condition}}"

# Progress anchor
halfway_point_reminder = "You are past the halfway point. Steps 1-{{midpoint}} established the foundation. Steps {{midpoint_next}}-{{step_total}} build on that work."

# Closer
section_closer_guardrail = "These {{step_count}} steps constitute your complete task. Do not add additional steps."
section_closer_exact_vs_judgment_recap = "{{mode_recap_text}} There are no other steps."
```
**Decisions:**

- Mode preamble: three variants (mixed, uniform-exact, uniform-judgment). Renderer selects based on mode distribution of step data.
- Preamble position order: step_count → mode_preview → no_add_skip_reorder → no_extra_operations.
- Mode recap text is computed ("Steps 1 and 3 are exact. Steps 2, 4, and 5 require judgment.").

## display.toml
```toml
[instructions]
# Step header formatting
step_header_format = "bold"  # "bold" | "h3"

# Scaffolding tier thresholds
scaffolding_tier_boundary_lightweight = 3
scaffolding_tier_boundary_standard = 7

# Mode recap format in closer
exact_vs_judgment_recap_format = "prose"  # "prose" | "tabular"
```
**Decisions:**

- `step_header_format`: Bold is lower visual weight; H3 is strongest structural signal.
- Tier boundaries: ≤3 lightweight, 4-7 standard, 8+ heavy. Drive conditional rendering of preamble components, progress anchors, and dependency signaling.

## Excluded (invariant rules / bare data)

- **Mode-before-body primacy**: Mode indicator always arrives before or with instruction text, never after. Invariant.
- **Over-instrumentation**: Meta-constraint "pick at most two of three mode layers." Enforced by structure booleans.
- **Model-dependent tuning**: Open question — no TOML entry until empirical testing resolves.
