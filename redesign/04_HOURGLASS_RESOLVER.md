# Hourglass Resolver-Renderer

## What It Does

Takes one bundle. Returns rendered text, or nothing if the bundle resolves to invisible.

The same resolution process applies to every bundle regardless of which slot it's in or which section it came from. The rendering differs based on what the resolution produces — but the resolution steps are uniform.

## The Hourglass Shape

**Wide input:** The bundle arrives with everything gathered — data value, content text, variant info, visibility state, display format, shape.

**Narrow middle — resolution:** A series of checks that determine what, if anything, to render:

1. **Visibility** — is this visible? If the structure toggle says no, return nothing. If it says "auto," check the threshold or data condition.

2. **Variant selection** — if this is a variant, look up the selector value and pick the matching alternative. The selected text becomes the content for the remaining steps.

3. **Template interpolation** — if the content has `{{placeholder}}` markers, fill them from a **scope chain of three layers**, not a flat dict:

   - **section-wide** — all scalar data values from the entire section, not just the bundle's own data field. This is how a heading template can reference `{{title}}` even though the heading bundle isn't "about" the title data field.
   - **per-item** — for compound list renderers, the current item's fields, merged on top of the section layer.
   - **engine-computed** — values no data field will ever supply: `{{step_n}}`, `{{step_total}}`, `{{rule_count}}`, `{{midpoint}}`. Derived from the list in scope and the current index, and from each other. **This vocabulary must be a closed set** — otherwise a placeholder naming nothing and a typo are indistinguishable, and nothing can count them.

   If any placeholder remains unfilled after interpolation, return nothing — the required data isn't available. This is the generic gate mechanism: missing data suppresses the content silently.

   > **Know what that costs.** Suppression cannot tell an absent-by-design field from a misspelled one. Both leave an unfilled placeholder; both vanish. So the mechanism that makes conditionality free also swallows every naming error at this layer, exactly as standalone-content-versus-mistyped-trunk does at the trunk layer. The closed computed vocabulary is what keeps one of the three cases detectable.

4. **Type determination** — based on the bundle's shape, determine which renderer handles the output.

**Wide output — rendering:** Route to the appropriate renderer. Simple types return immediately. Complex types go to specialized renderers that handle per-item logic with all four axes available.

## What the Resolver Does NOT Do

- It does not decide which slot things go in — that was chunking
- It does not scan models or walk field lists — that was gathering
- It does not know about sections — it processes one bundle
- It does not order output — that's the buffer

## The Suppress-on-Incomplete Mechanism

This is the most important design decision in the resolver. If a template still contains `{{...}}` after interpolation, the resolver returns nothing instead of rendering broken text.

This handles data gates generically. When a boolean gate is false and the gated data field is absent, any content template that references that data will have unresolved placeholders. The resolver suppresses it. No hardcoded gate logic needed — just: if you can't fill all the holes, stay silent.

## Renderer Routing

The resolver determines the type. The renderer produces text. Different types need different renderers:

- **Plain text** — the resolved string goes straight to the buffer
- **Simple list** — format per display settings (bulleted, numbered, inline, based on count and threshold)
- **Compound structures** — hand to a specialized renderer with whatever that renderer needs from all four axes

The specialized renderers for compound structures are documented in `06_RENDERER_TYPES.md`. What matters here: each renderer takes exactly what IT needs. The resolver gathers from the bundle and hands over the right subset. Simple renderers get a string. Complex renderers get the full context of all four axes for their specific data shape.

## We Don't Know the Full Renderer Set Yet

The schema review will reveal what data shapes actually exist and what rendering cases each produces. The resolver's design is stable — it always resolves the same way. The renderers will be designed after we know what they need to handle.
