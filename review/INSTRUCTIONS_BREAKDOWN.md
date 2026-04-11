# Instructions Section — Full Breakdown

## What This Section Does

Renders an ordered list of instruction steps. Each step has a mode (deterministic or probabilistic) and text. The section wraps these steps with preamble prose, per-step mode labels and headers, and closing reinforcement.

Agent-builder example: 7 steps, mixed modes (step 1 and 7 are deterministic, steps 2-6 are probabilistic).

---

## Data

```
Instructions
  steps: list of InstructionStep (7 items for agent-builder)
    .instruction_mode    enum: deterministic | probabilistic
    .instruction_text    markdown prose
```

One data field (`steps`), one list, each item has a mode and text. That's all the data.

---

## What The Output Looks Like

With current agent-builder settings (mode labels on every step, dash separator, bold headers):

```markdown
## Instructions

You will execute 7 steps.

Do not add steps. Do not skip steps. Do not reorder steps.

Steps marked (exact) leave no room for interpretation. Steps marked (judgment) is where your reasoning matters.

Each instruction step is a complete specification. Do not supplement steps with general knowledge or add operations not specified.

**EXACT** — **Step 1 of 7.**

Read the preparation package from the tempfile path...

**JUDGMENT** — **Step 2 of 7.**

Identify the agent's core domain from the requirements...

[... steps 3-6, mode label shown on each ...]

**EXACT** — **Step 7 of 7.**

Map all structured fields from the requirements to definition fields...

These 7 steps constitute your complete task. Do not add additional steps.
```

With `steps_mode_restrict_to_transition = true` (suppress consecutive same-mode labels):

```markdown
**EXACT** — **Step 1 of 7.**

Read the preparation package...

**JUDGMENT** — **Step 2 of 7.**

Identify the agent's core domain...

**Step 3 of 7.**

Design the instruction steps...

**Step 4 of 7.**

Create calibration examples...

**Step 5 of 7.**

Write guardrails...

**Step 6 of 7.**

Write success and failure criteria...

**EXACT** — **Step 7 of 7.**

Map all structured fields...
```

Steps 3-6 share the same mode as step 2, so their labels are suppressed.

---

## Per-Step Rendering — Decomposed

Each step is composed from three independent parts:

```
{MODE_LABEL} {SEPARATOR} {STEP_HEADER}

{STEP_BODY}
```

| Part | Source | Control |
|------|--------|---------|
| MODE_LABEL | content `steps_mode_label_variant` keyed by step's `instruction_mode` | display `steps_mode_restrict_to_transition` can suppress |
| SEPARATOR | display `steps_mode_separator` enum (dash/colon/pipe/newline) | Only rendered when both MODE_LABEL and STEP_HEADER present |
| STEP_HEADER | content `steps_heading_template` or `steps_heading_n_only_template` | structure `steps_index_tracking` selects which |
| STEP_BODY | data `instruction_text` | display `steps_body_container` wraps it |

Each concern is on its own axis:
- Content controls the TEXT (mode label wording, header template)
- Display controls the FORMAT (separator style, transition suppression, header format, body container)
- Structure controls the SELECTION (which header template, which visibility toggles)

---

## Remaining Issues

1. **`instruction_mode_explanation_preamble_variant`** — variant key computed from data (mode mix), no structure selector
2. **`pre_scaffolding_tier_override`** — meta-policy computing visibility toggles, not directly processable
3. **`steps_index_tracking`** — enum values (`n_of_m`/`n_only`) don't match content field names (`steps_heading_template`/`steps_heading_n_only_template`)
4. **Computed placeholders** — `{{step_count}}`, `{{step_n}}`, `{{step_total}}`, etc. need generation before interpolation
