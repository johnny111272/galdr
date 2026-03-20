# IDENTITY — TOML Extraction

## structure.toml

```toml
[identity]
field_ordering = "identity_first"
fuse_declaration_and_role_description = false
expertise_is_strictly_limited_visible = true
closing_identity_reminder_visible = false
bold_contrast_phrase_from_role_description_visible = false
```

**Decisions:**

- `field_ordering`: "identity_first" is converged default. "fused" is experimental. Each is a separate Pydantic layout model.
- `expertise_is_strictly_limited_visible`: Implicit negation — safer than explicit negation which primes excluded domains.
- `closing_identity_reminder_visible`: Default false — bookend pattern may teach the agent the prompt repeats itself.
- `bold_contrast_phrase_from_role_description_visible`: Default false — single-analysis origin, risk of teaching agent to downweight non-repeated content.

## content.toml

```toml
[identity]
heading = "AGENT: {{title}}"
declaration = "You are a {{role_identity}}."
declaration_decision_test_postscript = "This identity governs every decision you make — when in doubt, ask: what would a {{role_identity}} do?"
responsibility_label = "**Scope:** {{role_responsibility}}"
expertise_label = "**Your judgment is authoritative in:**"
expertise_is_strictly_limited = "Your expertise is strictly limited to the areas listed above."
closing_identity_reminder = "Remember: you are a {{role_identity}}."
```

**Decisions:**

- `declaration`: Highest-leverage fragment. "You are a X" kept separate from decision test postscript for independent variation.
- `declaration_decision_test_postscript`: Heuristic form ("what would a X do?") over negation form (which risks priming adjacent identities).
- `responsibility_label`: "Scope:" is converged default. "Done when:" is alternative for mechanical agents (requires task_type).
- `expertise_label`: Authority-grant framing ("Your judgment is authoritative in:") over passive "Expertise:" — reduces hedging. Alternative: "Pay special attention to:".
- role_description and description are bare data — no templates. Labels ("Purpose:", "Mission:") convert immersive experience into specification-reading.

## display.toml

```toml
[identity]
expertise_format = ["bulleted", "inline"]
expertise_format_threshold = 3
responsibility_format = ["bulleted", "prose"]
responsibility_format_threshold = 3
```

**Decisions:**

- `responsibility_format`: Bullets over numbers — numbering implies sequencing that may not match actual workflow.

## Excluded (invariant rules / bare data)

- **Model never renders**: Infrastructure metadata for dispatch, not behavioral configuration.
- **No meta-preamble**: Renderer opens directly with identity declaration. Meta-preambles are counterproductive.
- **Field sub-ordering**: declaration → role_description → responsibility → expertise. Invariant within identity_first ordering.
- **bold_contrast_phrase_from_role_description**: No content.toml entry — renderer extracts contrast phrase directly from role_description data when enabled.
