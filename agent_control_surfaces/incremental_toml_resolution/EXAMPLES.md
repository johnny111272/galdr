# EXAMPLES — TOML Extraction

## structure.toml
```toml
[examples]
section_preamble_visible = true

# Group heading suppression for single-group agents
# true = suppress group heading + promote entries; false = render full three-level hierarchy
suppress_lone_group_heading_visible = true

# Override for per-group example_display_headings from data
example_display_headings_override = false
example_display_headings = true                    # only when override = true

# Override for per-group examples_max_number from data
examples_max_number_override = false
examples_max_number = 0                            # 0 = no truncation, N = cap. Only when override = true

# Whether a framing sentence renders between the group heading and first entry
group_framing_sentence_visible = false

# Multi-group transition mechanism (only activates when group_count > 1)
multi_group_separator_visible = true
```
**Decisions:**

- `suppress_lone_group_heading_visible`: When only one example group exists, suppress the group heading and promote entries to H3. Avoids a single-child hierarchy.
- `example_display_headings_override` + `example_display_headings`: Override pattern. `_override = false` → use per-group data value. `_override = true` → use sibling value for all groups.
- `examples_max_number_override` + `examples_max_number`: Same pattern. 0 = no truncation (render all). N = cap at N examples per group.
- GOOD/BAD/WHY are handled by preamble text, not structural fields. Synthesis explicitly rejected structural promotion.

## content.toml
```toml
[examples]
# Section heading text — cognitive mode shift from declaration to demonstration
heading = "Worked Examples"

# Preamble — installs interpretive framework + generalization instruction
# Two jobs: (1) GOOD/BAD/WHY vocabulary, (2) generalize to novel inputs
preamble = "Examples may show GOOD and BAD outputs with WHY reasoning. GOOD is correct judgment. BAD is the specific mistake you are most likely to make. WHY is the principle — learn the principle and apply it to inputs not shown here."

# Entry heading template — renders per entry when display_headings = true
entry_heading = "{{example_heading}}"
```
**Decisions:**

- `heading`: "Worked Examples" primes active study over passive scanning. Experimental.
- `preamble`: Highest-leverage prose fragment in section. Two jobs: (1) install GOOD/BAD/WHY vocabulary, (2) instruct generalization to novel inputs.

## display.toml
```toml
[examples]
# Entry heading format — bold text vs H4
# Bold preserves boundaries without visual density for groups with 5+ entries
entry_heading_format = "bold"

# Entry body container — how entry content is visually contained
entry_body_container = "bare_with_endmarker"

# Entry separator — what divides entries when headings are off (per-group data)
entry_separator = "horizontal_rule"

# Multi-group separator — visual break between groups
# Only activates when group_count > 1
multi_group_separator = "horizontal_rule"
```
**Decisions:**

- `entry_body_container`: "bare_with_endmarker" preserves fidelity; endmarker guarantees boundaries. "blockquote" is fallback.
- `entry_separator` vs `multi_group_separator`: Separate fields because they serve different hierarchy levels (within-group vs between-group).

## Excluded (invariant rules / bare data)

- **Heading hierarchy**: H2 section, H3 group, bold/H4 entry. Entry level is in display.toml; section and group levels are fixed.
- **Back-reference from instructions**: Cross-section dependency that lives in the instructions section's control surface, not here.
