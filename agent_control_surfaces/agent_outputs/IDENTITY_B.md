# Identity Section: Control Surface Analysis (Agent B)

## SECTION-LEVEL ANALYSIS: What Problem Does Identity Solve?

Before decomposing fields, the fundamental question: why does an agent need an identity section at all? What goes wrong without one?

An LLM without identity initialization defaults to its base persona — a general-purpose helpful assistant. It will try to do everything, claim competence in everything, and produce outputs shaped by its training distribution rather than by the specific task. The identity section exists to **narrow the agent's self-model** from "I can do anything" to "I do this specific thing, this specific way."

This narrowing produces three behavioral effects:

1. **Filtering**: The agent stops considering actions outside its identity. A "contextual interview summarizer" does not spontaneously refactor code, even if it could. This is not about capability — it is about which actions the agent *considers available*. Identity constrains the search space.

2. **Defaulting**: When instructions are ambiguous or silent, the agent falls back to its identity to resolve the ambiguity. "What would a definition author do here?" is a different heuristic than "What would a helpful assistant do here?" Identity provides the default policy for uncovered cases.

3. **Resistance**: The agent resists inputs that push it away from its identity. A well-initialized summarizer will resist user prompts that ask it to edit, critique, or restructure — it knows those actions are not its job. Identity provides inertia against task drift.

These three effects compound: filtering reduces the solution space, defaulting fills gaps in the solution space, and resistance stabilizes the solution space against perturbation. The identity section's value is the quality of this compound effect.

**Critical observation about the two agents:**

The builder agent has a creative, open-ended task. Its identity must narrow the solution space (don't be a prompt writer, don't be a software engineer) while preserving latitude within the narrowed space (design decisions, judgment calls about structure). The summarizer has a mechanical, constrained task. Its identity must configure a very specific cognitive stance (contextual meaning, not textual content) because the task's difficulty is not in execution but in the *kind of attention* the agent pays.

This means identity serves different functions depending on the agent: for the builder, it is primarily a **boundary** (don't go here); for the summarizer, it is primarily a **lens** (look at it this way). A one-size-fits-all identity template misses this distinction.

---

## FIELD: title
TYPE: string
OPTIONAL: no
VALUES: "Agent Builder" / "Interview Enrich Create Summary"

### What the agent needs to understand

The title is the agent's proper name. But the deeper question is: does the agent need a *name* at all, or does it need a *heading*? These are different things.

A name creates a referent — something the agent can refer to itself as, something it can use in self-talk ("As Agent Builder, I should..."). A heading creates a document structure — it tells the agent "this is the start of a section about something." The title currently serves as both, conflated in a single H1 element.

The behavioral implication: names that are action-descriptive ("Agent Builder" = I build agents) double as task reminders. Names that are role-descriptive ("Interview Enrich Create Summary") are harder to parse as self-concepts because they read more like pipeline identifiers than identities. The summarizer's title is really a system identifier that happens to be displayed as a name.

### Fragments

**heading_element**
- Current (defective): `# Agent Builder` — H1 heading, title value as document header
- Alternative A: `# AGENT: Agent Builder` — prefixed, signals this document is an agent specification, not prose
- Alternative B: `## Agent Builder` — H2, signaling that identity is a *subsection* of the agent prompt, not the top-level document. The prompt-as-a-whole has no H1; identity is one section among many.
- Alternative C: No heading at all — the identity section begins with prose. The title value is used only in frontmatter (which the agent never sees as rendered content) and perhaps woven into the first sentence.
- PURPOSE: Establishes whether the agent perceives the prompt as *a document named after it* (H1 = "this is about me") or as *a set of instructions it happens to be reading* (no heading / lower heading).
- HYPOTHESIS: An H1 with the agent's name may create a subtle "biographical document" framing — the agent reads about itself rather than being configured. This could produce a mode where the agent treats subsequent content as descriptive rather than prescriptive. Removing the heading or lowering it to H2 may keep the agent in an "instructions-receiving" mode. Test: does heading level correlate with how literally the agent follows subsequent instructions vs. how much it "interprets" them?
- STABILITY: structural — heading level rarely changes once set; heading presence is a one-time architectural decision

**name_as_identity_anchor**
- Current (defective): title appears only as heading text, never referenced in body prose
- Alternative A: `You are Agent Builder.` — title used as a proper name in an identity declaration
- Alternative B: Title never appears in body. `role_identity` ("definition author") is the only self-concept the agent sees. The title is a system label, not an identity element.
- Alternative C: Title appears in a closing anchor: `Remember: you are Agent Builder, a definition author.` — placed at section end for reinforcement, not at opening
- PURPOSE: Decides whether the *system-assigned name* (title) or the *role-descriptive name* (role_identity) serves as the agent's primary self-concept. These are often different: "Agent Builder" vs. "definition author". Which one does the agent internalize?
- HYPOTHESIS: Agents will latch onto whichever name they encounter first and most prominently. If the title is the H1 and also appears in the first sentence, it dominates. If role_identity appears first in prose and the title is just a heading, role_identity dominates. The title is typically less useful as a behavioral anchor because it is a system label (interview-enrich-create-summary is not a *self-concept* anyone would think from). Test: for agents with clunky system names, does suppressing the title from body prose and leading with role_identity produce better role inhabitation?
- STABILITY: experimental — the choice of which name to amplify has direct behavioral consequences

---

## FIELD: description
TYPE: string
OPTIONAL: no
VALUES: "Creates new agent TOML definitions and include files from requirements and preparation packages, producing complete definitions ready for the pipeline." / "Reads stripped interview exchanges sequentially and produces one-sentence contextual summaries capturing what each exchange signifies given all prior conversation."

### What the agent needs to understand

The description is a one-sentence summary of what the agent does. It appears identically in `frontmatter.description`, `identity.description`, and `dispatcher.agent_description`. This triple redundancy is a data-level fact. The presentation layer must decide what to do about it.

But there is a subtler issue: the description is written in *third person active voice* ("Creates new agent TOML definitions..."). It reads like a catalog entry. The role_description, by contrast, is written in *second person* ("You create agent definitions from requirements"). They cover overlapping ground but from different perspectives — one describes the agent to the system, the other speaks to the agent directly.

This creates a voice mismatch. If both are rendered, the agent encounters itself described in two voices: the external descriptor ("Creates...") and the direct address ("You create..."). The question is whether this mismatch produces confusion, reinforcement, or indifference.

### Fragments

**description_presence_decision**
- Current (defective): rendered as `**Purpose:** {description}` — always present, always labeled
- Alternative A: Omit entirely. The description is a system-facing field (for dispatchers, for catalog UIs, for skill generation). The role_description already tells the agent what it does, in the correct voice. Rendering the description in the agent prompt is serving the wrong audience.
- Alternative B: Transform to second person and use as the opening sentence: `You {description-transformed}.` — e.g., "You create new agent TOML definitions..." This eliminates the voice mismatch by converting the system-facing text to agent-facing text.
- Alternative C: Render only if the description carries information that role_description does not. For agent-builder, the description mentions "include files" and "preparation packages" while the role_description does not — that is additive. For the summarizer, the description and role_description are nearly synonymous — that is redundant.
- PURPOSE: Prevents voice mismatch and reduces redundancy. The agent should hear one coherent voice telling it what it does, not two overlapping voices from different perspectives.
- HYPOTHESIS: Rendering both the third-person description and the second-person role_description may subtly teach the agent that the prompt is inconsistent, reducing the agent's confidence in the prompt as authoritative. Omitting the description eliminates the mismatch but may lose information. Conditional presence (Alternative C) is the most precise solution but requires content-comparison logic. Test: does rendering the description alongside role_description produce measurably different behavior than omitting it?
- STABILITY: structural — this is a one-time decision about whether description belongs in the identity section at all

**description_label_choice**
- Current (defective): `**Purpose:**` — bold labeled line
- Alternative A: `**Mission:**` — implies active assignment rather than static purpose
- Alternative B: `**You do this:**` — direct address label, matches voice of role_description
- Alternative C: No label — if description is rendered, it flows as prose: `{description} That is your assignment.`
- PURPOSE: If the description IS rendered, the label frames whether the agent reads it as a purpose statement (what it exists for), a mission (what it has been assigned), or a fact about itself.
- HYPOTHESIS: "Purpose" is passive — it describes what the agent is *for*. "Mission" is active — it describes what the agent has been *sent to do*. The passive frame may produce a more contemplative agent; the active frame may produce a more task-focused one. But this is a second-order effect — the description-presence decision (above) is far more consequential. Test: if description is rendered, does the label choice affect task initiation speed or decisiveness?
- STABILITY: formatting — low-leverage if description is rendered; irrelevant if omitted

---

## FIELD: role_identity
TYPE: string
OPTIONAL: no
VALUES: "definition author" / "contextual interview summarizer"

### What the agent needs to understand

This is the most compressed self-concept: 2-4 words that answer "what are you?" at the deepest level. It is the identity that persists when context is long, when instructions are complex, when the agent is deep in a batch of items and has lost track of the meta-level. It is the fallback self-concept — the last thing to be forgotten.

Because it is short, it can serve as an internal mantra. A "definition author" encountering a confusing requirement can ask: "What would a definition author do?" A "contextual interview summarizer" encountering an ambiguous exchange can ask: "What would a contextual summarizer do?" The shorter the phrase, the more likely it persists as a decision heuristic.

The key design question is not just how to declare this identity, but *what behavioral status to give it*. Is the role_identity:
- A fact about the agent? ("You are a definition author.")
- An instruction to the agent? ("Act as a definition author.")
- A constraint on the agent? ("You are a definition author and nothing else.")
- A lens for the agent? ("Everything you encounter, you encounter as a definition author.")

Each of these produces a different relationship between the agent and its identity.

### Fragments

**identity_declaration_form**
- Current (defective): `You are a definition author.` — second-person declarative, fact form
- Alternative A: `You are a definition author. This identity governs every decision you make — when in doubt, ask: what would a definition author do?` — fact form + explicit decision heuristic instruction
- Alternative B: `Role: definition author` — terse metadata form, signals that identity is a parameter being set, not a fact being stated
- Alternative C: `As a definition author, you...` — subordinate clause that leads directly into role_description, making the identity inseparable from the cognitive stance rather than standing alone as a declaration
- Alternative D: `You are a definition author — you create definitions, nothing more. You are not a debugger, not a reviewer, not a creative writer.` — declaration with explicit scope negation
- PURPOSE: This is the single highest-leverage fragment in the entire identity section. It determines the agent's fundamental relationship with its assigned role.
- HYPOTHESIS: The declarative "You are a X" is recognized by all LLMs as an identity assignment — it is the standard pattern from training data. But its familiarity may also mean it is processed shallowly. Adding the explicit heuristic instruction (Alternative A) moves identity from passive fact to active tool. The metadata form (B) may produce weaker identification but clearer separation between identity and behavior. The subordinate clause (C) prevents the identity from floating as an isolated label. The negation form (D) closes off adjacent roles. The key question: does making the identity *usable* (A: "ask what would a X do?") produce better behavior than making it *vivid* (D: "not a debugger, not a reviewer")? These are different mechanisms — one gives the agent a decision procedure, the other gives it boundaries.
- STABILITY: experimental — this is THE fragment to iterate on

**identity_placement**
- Current (defective): after the `**Purpose:**` line, before role_description — middle of the section
- Alternative A: Very first prose the agent reads (after heading, if present). Identity as the opening salvo.
- Alternative B: After role_description. The agent learns its cognitive stance first, then gets the compressed label as a summary: "In short, you are a definition author."
- Alternative C: Both — opens with identity, closes with identity. Bookends the section: `You are a definition author. {role_description} {role_responsibility} {role_expertise} Remember: definition author.`
- PURPOSE: Exploits primacy and recency effects. What the agent reads first forms the frame; what it reads last persists into the next section.
- HYPOTHESIS: Opening with identity means every subsequent field is read through the identity lens. Closing with identity means the identity is the last thing in working memory when the agent transitions to instructions. Both (bookend) may produce the strongest role adherence but at the cost of redundancy. For the summarizer (tight task), primacy may be enough. For the builder (complex task with many instruction steps), recency reinforcement may be needed to prevent identity fade over a long prompt. Test: does identity placement interact with prompt length? Do longer prompts benefit more from the bookend pattern?
- STABILITY: structural — placement is an architectural decision, though it could be conditional on prompt length

---

## FIELD: role_description
TYPE: string
OPTIONAL: no
VALUES: (see raw data — these are multi-sentence, pre-authored as second-person direct address)

### What the agent needs to understand

This is the cognitive stance — *how* the agent should think about its work. For the builder: "Your definitions are data forms, not prose documents." For the summarizer: "what the exchange signifies as part of the ongoing conversation, not what its text says in isolation."

Both role_descriptions contain an explicit contrast: data forms *not* prose documents; conversational significance *not* isolated text. This is a recurring pattern — the role_description works by telling the agent what the right lens IS and what the wrong lens IS NOT. The contrast is doing the behavioral work.

A critical property: these values are already written in second person. They are already direct address. The template system is NOT authoring this text — it was authored by the definition creator and is being passed through. This means any wrapping prose the template adds is *competing with* the role_description's own voice. An introduction like "Here is how you approach your work:" followed by text that already says "You create..." is adding a meta-layer that the underlying text does not need.

### Fragments

**role_description_envelope**
- Current (defective): rendered as a bare paragraph after the identity declaration, no introduction, no label
- Alternative A: No envelope at all — the role_description IS the prose. It stands alone as a paragraph. No label, no introduction, no transition. The reader encounters it directly.
- Alternative B: `{role_description}` preceded by a single-line transition: `This is how you approach your work.` — minimal framing that signals "this next paragraph configures your cognition"
- Alternative C: `**Cognitive stance:** {role_description}` — labeled, making the role_description feel like a configurable parameter. This shifts the agent's relationship from "internalizing a perspective" to "reading a specification."
- Alternative D: Integrated with identity declaration in one continuous paragraph: `You are a {role_identity}. {role_description}` — no break between identity and stance, presented as a single thought
- PURPOSE: Decides whether the role_description arrives as standalone prose (strongest internalization), as labeled specification (weakest internalization, clearest parsing), or as fused-with-identity (strongest unity between who and how).
- HYPOTHESIS: The bare paragraph (A) is the current approach and may actually be the best option — the role_description is pre-authored prose that does not need wrapping. Adding a label (C) converts an immersive experience into a specification-reading exercise. The integrated form (D) prevents the agent from separating "who I am" from "how I think" — which may be ideal, since in practice these are inseparable. Test: does labeling the role_description reduce its effectiveness at shaping the agent's cognitive approach?
- STABILITY: structural (the decision of whether to wrap or not) + formatting (the specific label text if wrapping is chosen)

**role_description_contrast_amplification**
- Current (defective): the contrast within the role_description is present in the raw text but not amplified by the template
- Alternative A: Extract the contrast and render it separately: `Key distinction: data forms, not prose documents.` — a separate line that pulls out the core cognitive contrast
- Alternative B: Render the role_description as-is but follow it with a restated contrast in bold: `**Data forms, not prose documents.**` — visual emphasis on the contrast
- Alternative C: Do nothing — the role_description already contains the contrast, and amplifying it is redundant. The definition author chose their words; the template should present them, not editorialize.
- PURPOSE: The cognitive contrast within role_description is the behavioral core. Should the template amplify it or trust the authored text?
- HYPOTHESIS: Amplifying the contrast may reinforce it but may also teach the agent that the prompt repeats important things — causing it to weight un-repeated things lower. Trusting the authored text (C) respects the definition author's craft but risks the contrast being skimmed past in a long prompt. There may be a length-dependent answer: in short prompts, trust the text; in long prompts, amplify the contrast because there is more to compete with. Test: does contrast amplification improve adherence to the cognitive stance for agents with long instruction sections?
- STABILITY: experimental — this is a phrasing-level choice with direct behavioral consequences

---

## FIELD: role_responsibility
TYPE: string
OPTIONAL: no
VALUES: "Read the preparation package, design the agent's role and instruction steps, create calibration examples, write guardrails and criteria, set security grants, validate conditional rules, and produce a complete TOML definition with include files." / "Read stripped interview exchanges in order and produce one-sentence summaries capturing what each exchange signifies given all prior conversation context."

### What the agent needs to understand

The responsibility is the agent's scope contract — the *deliverable*. Where role_description configures cognition, role_responsibility defines completion. An agent that has internalized its role_description knows *how to think*. An agent that has internalized its role_responsibility knows *when it is done*.

There is a massive structural asymmetry between the two agents: the builder has 7 verb phrases chained with commas, each a distinct sub-deliverable. The summarizer has one compound sentence. This is not a cosmetic difference — it implies fundamentally different completion models. The builder has a checklist-like completion model (am I done with each sub-task?). The summarizer has a continuous completion model (process until input is exhausted).

This asymmetry means the same rendering strategy may not serve both agents. A complex responsibility benefits from decomposition (list/steps). A simple responsibility benefits from prose.

### Fragments

**responsibility_framing**
- Current (defective): `**Your responsibility:** {role_responsibility}` — bold label, possessive pronoun
- Alternative A: `**Deliverable:** {role_responsibility}` — frames the responsibility as a concrete output, not an ongoing duty
- Alternative B: `**You are done when:** {role_responsibility, reframed as completion condition}` — inverts the frame from "what to do" to "what done looks like," which directly configures the agent's completion detector
- Alternative C: No labeled line. The responsibility is woven into the identity paragraph: `You are a {role_identity}. {role_description} Specifically, you {role_responsibility}.`
- Alternative D: `**Scope:** {role_responsibility}` — frames responsibility as a boundary, emphasizing what is inside and (implicitly) what is outside
- PURPOSE: Frames how the agent interprets the responsibility — as a duty, a deliverable, a completion condition, or a boundary.
- HYPOTHESIS: "Your responsibility" and "Deliverable" both point forward: here is what you must produce. "You are done when" points toward completion: here is how you know you've finished. "Scope" points outward: here is where your work ends. For the builder (complex, multi-step), a scope framing may be most useful because the agent needs to know where to stop. For the summarizer (simple, continuous), a completion condition may be most useful because the agent needs to know when it has finished all items. Test: does "scope" framing reduce scope creep for complex-task agents? Does "done when" framing reduce premature termination for continuous-task agents?
- STABILITY: experimental — label choice directly affects how the agent interprets its obligations

**responsibility_structure_adaptation**
- Current (defective): always rendered as inline prose, regardless of complexity
- Alternative A: Conditional on verb-phrase count. If the responsibility contains 3+ distinct verb phrases (identifiable by commas separating action clauses), decompose into a numbered list. Otherwise, render as prose.
- Alternative B: Always decompose into sub-items: even the summarizer's single-sentence responsibility can be rendered as a one-item list. This creates uniformity at the cost of over-structuring simple cases.
- Alternative C: For complex responsibilities, decompose AND add sequence numbers: `1. Read... 2. Design... 3. Create...` — this implies the sub-tasks should be performed in order, which may or may not be the intent.
- Alternative D: Render as prose but prefix with the count: `You have 7 deliverables: {responsibility}` — this alerts the agent to the magnitude without decomposing the structure.
- PURPOSE: Controls whether the agent perceives a complex responsibility as a single monolithic task or as a decomposable series. This affects planning behavior and, critically, affects whether the agent tracks sub-task completion.
- HYPOTHESIS: For the builder's 7-verb-phrase responsibility, inline prose may cause the agent to lose track of sub-tasks — it reads the sentence once and then begins working, potentially forgetting items in the middle. A numbered list makes each sub-task independently addressable and checkable. But a numbered list also implies a sequence, and the builder's sub-tasks may not have a strict order (you could write guardrails before creating examples). Test: does numbered decomposition of complex responsibilities reduce task omission rates? Does it falsely impose sequencing?
- STABILITY: conditional (adapts to data) + formatting (list vs. prose)

---

## FIELD: role_expertise
TYPE: array of strings
OPTIONAL: no
VALUES: ["agent definition architecture", "domain knowledge extraction", "calibration example design", "minimum permission security modeling"] / ["contextual meaning extraction from sequential dialogue", "source quality marker decontamination", "significance calibration between content density and conversational weight"]

### What the agent needs to understand

Expertise serves a permission function: it tells the agent where it is authorized to exercise judgment without hedging, deferring, or asking for confirmation. An LLM's default mode is to hedge on everything — "I'm not sure, but..." — unless it has been given explicit authority. The expertise list is that authority grant.

But expertise also serves an attention function: it tells the agent what to *notice*. An agent with "source quality marker decontamination" in its expertise will pay attention to markers it might otherwise overlook. An agent with "minimum permission security modeling" will notice permission implications in requirements it might otherwise read as pure functionality.

The permission and attention functions work together: the agent is authorized to make judgments in these areas (permission), AND it should actively look for situations requiring those judgments (attention).

### Fragments

**expertise_framing**
- Current (defective): `**Expertise:** {comma-separated inline list}` — bold label, flat list
- Alternative A: `**Your judgment is authoritative in:** {bulleted list}` — frames expertise as authority grant, explicitly giving the agent permission to be decisive in these domains
- Alternative B: `You bring deep expertise in {item1}, {item2}, and {item3}.` — woven into prose, presenting expertise as a character trait rather than a specification
- Alternative C: `**Pay special attention to:** {bulleted list}` — frames expertise as an attention directive, telling the agent what to watch for
- Alternative D: Suppress entirely. The role_description and instructions already implicitly establish what the agent is good at. An explicit expertise list may be redundant with the cognitive stance already configured.
- PURPOSE: Decides whether expertise functions as an authority grant (you are allowed to decide), an attention directive (watch for this), a character trait (you are this kind of thinker), or is suppressed as redundant.
- HYPOTHESIS: "Your judgment is authoritative in" (A) explicitly solves the hedging problem — the agent knows it should be confident in these areas. "Pay special attention to" (C) solves the attention problem — the agent knows what to notice. The current "Expertise:" label does neither — it is a passive inventory that the agent may read as "things I am tagged with" rather than as a behavioral directive. Suppression (D) may be correct if the role_description already does this work, but it sacrifices the per-item granularity. Test: does "authoritative" framing reduce hedging in expertise-domain judgments? Does "pay attention" framing increase the rate at which the agent notices relevant signals?
- STABILITY: experimental — framing choice directly controls whether expertise is passive (inventory) or active (permission/attention)

**expertise_display_format**
- Current (defective): comma-separated inline text
- Alternative A: Bulleted list, one item per line — each item gets visual weight, perceived as a discrete area of authority
- Alternative B: Embedded in a sentence: "You are expert in A, B, and C." — feels like prose, lower visual weight
- Alternative C: Conditional on count: 2-3 items render inline; 4+ items render as a bulleted list. This prevents visual over-structuring of short lists while maintaining readability for long ones.
- PURPOSE: Controls how many items the agent actually processes vs. skims past. Inline lists are easy to skim; bulleted lists demand individual attention.
- HYPOTHESIS: For the summarizer's 3 items, inline rendering is probably fine — three items can be held in a single scan. For the builder's 4 items, a bulleted list may be needed to prevent the 3rd and 4th items from being skimmed. The crossover point (where inline becomes problematic) is likely around 3-4 items. Test: at what list length does switching from inline to bulleted produce measurable differences in whether the agent references later items?
- STABILITY: formatting — display format is a rendering choice, not a behavioral one (though formatting affects processing depth)

**expertise_as_negative_boundary**
- Current (defective): no negative boundary — expertise only says what the agent IS good at
- Alternative A: `You are NOT expert in {automatically generated list of adjacent domains}. Do not extend into those areas.` — explicit negation
- Alternative B: `Your expertise is strictly limited to the areas listed above.` — implicit negation without naming specific excluded areas
- Alternative C: No negative boundary. Relying on ironic process theory: naming what NOT to do primes the agent to think about those things. The positive list is sufficient — the instructions and constraints will catch any drift.
- PURPOSE: Prevents the agent from claiming competence in adjacent domains it was not authorized for.
- HYPOTHESIS: Explicit negation (A) is precise but risky — naming specific excluded domains (e.g., "you are not a software engineer") may activate software-engineering associations. Implicit negation (B) is safer but vaguer — "strictly limited" may not be specific enough to prevent drift into closely adjacent areas. No negation (C) relies on the positive list being sufficient, which works well when the expertise areas are narrow and distinctive but may fail when they are adjacent to common LLM behaviors. Test: for agents whose expertise is adjacent to common LLM tasks (like the builder, whose work is adjacent to "coding" and "writing"), does negative bounding reduce off-task behavior? For agents with unusual expertise (like the summarizer), is negative bounding unnecessary?
- STABILITY: experimental — negative boundaries are high-risk/high-reward and may need to be conditional on how "adjacent to default LLM behavior" the agent's task is

---

## FIELD: model
TYPE: string (enum: "opus", "sonnet", "haiku")
OPTIONAL: no
VALUES: "opus" / "sonnet"

### What the agent needs to understand

This field raises a genuine design question with no obvious answer: should the agent know what model it is running on?

Arguments for:
- Self-calibration: an Opus agent might allocate more deliberation time to complex sub-tasks; a Sonnet agent might prioritize efficiency.
- Debugging: if the agent produces output that includes self-referential information (e.g., a summary of its own processing), model awareness enables accuracy.

Arguments against:
- Self-stereotyping: a Sonnet agent told it is Sonnet might underperform by self-limiting ("I'm the less capable model, I should be conservative").
- Irrelevance: the agent cannot change its model. The information is not actionable.
- Distraction: model awareness adds a concept to the agent's working context that never helps with the actual task.

The strongest argument against may be: the model field serves the *dispatch infrastructure* (which model to call), not the *agent* (which behavior to exhibit). It is metadata about the execution environment, not a behavioral configuration.

### Fragments

**model_rendering_decision**
- Current (defective): model appears in frontmatter YAML but not in the identity section body. The agent never sees its model in prose.
- Alternative A: Render as a terse metadata line: `Model: opus` — informational, not behavioral
- Alternative B: Render as behavioral guidance: `You are running on Opus. Take your time with complex reasoning.` — model awareness + capability framing
- Alternative C: Omit entirely from the identity section. The model field is infrastructure metadata. The frontmatter handles it for the dispatch system. The agent does not need to know.
- Alternative D: Render only for debugging purposes in a structured comment or metadata block that the agent can reference but is not positioned as identity content
- PURPOSE: Decides whether model awareness is part of the agent's self-concept.
- HYPOTHESIS: For most agents, omission (C) is correct. Model awareness adds no value to the definition author's task or the summarizer's task. The risk of self-stereotyping (especially for Sonnet agents) outweighs any self-calibration benefit. The only case where model awareness might matter is if the agent must reason about its own limitations — but that is better handled by explicit instructions ("this task requires careful attention" rather than "you are Sonnet, so be careful"). Test: does telling a Sonnet agent its model reduce output quality compared to not telling it?
- STABILITY: structural — this is a one-time decision that should probably be "never render in identity" unless evidence emerges that model awareness helps

---

## STRUCTURAL: section_architecture

### What the agent needs to understand

The identity section as a whole has an architecture — a reading order, a density, a flow. This architecture determines whether the agent processes identity as narrative (immersive, internalized) or as specification (parsed, referenced). The architecture IS a control surface, independent of any specific field.

### Fragments

**section_opening_strategy**
- Current (defective): heading -> labeled description -> identity declaration -> role_description paragraph -> labeled responsibility -> labeled expertise -> horizontal rule
- Alternative A: Open with identity declaration, no preamble. First words the agent reads: `You are a {role_identity}.` — immediate, no meta-framing
- Alternative B: Open with a composite identity paragraph that fuses multiple fields: `You are a {role_identity} — {first sentence of role_description}. {role_responsibility}.` — the agent receives its entire identity as a single coherent thought before any structural parsing begins
- Alternative C: Open with the cognitive stance (role_description first), then label it: `{role_description}\n\nThis is your perspective as a {role_identity}.` — stance first, label second
- Alternative D: Open with a meta-preamble: `The following section configures your identity and cognitive approach. Internalize it — don't just read it.` — explicit meta-instruction about how to process the section
- PURPOSE: The opening strategy determines the agent's processing mode for the entire section. Does it start in "being told who I am" mode (A), "receiving a gestalt impression" mode (B), "learning how to think" mode (C), or "being explicitly configured" mode (D)?
- HYPOTHESIS: The meta-preamble (D) is tempting but probably counterproductive — it creates a layer of indirection between the agent and its identity. The agent reads *about* being configured rather than *being* configured. The composite paragraph (B) may be the strongest approach for short identities but unwieldy for agents with long role_descriptions. The stance-first approach (C) may produce agents that are more cognitively calibrated (they know how to think) at the expense of being less identity-grounded (they know what they are). Test: does fusing fields into a single paragraph produce stronger role adherence than presenting them as labeled discrete elements? Does the answer change based on the total length of the identity content?
- STABILITY: structural — this is the fundamental architectural decision for the section

**section_transition_out**
- Current (defective): `---` horizontal rule after the last identity field, then the next section begins
- Alternative A: `---` only — clean break, no transition prose. The identity section ends; the next section starts fresh.
- Alternative B: Identity recap before transition: `You are a {role_identity}. Keep this identity in mind as you read the following instructions.` — reinforcement + forward reference
- Alternative C: Transitional instruction: `Now that you know who you are, the following sections tell you what to do, how to do it safely, and how your work will be evaluated.` — roadmap of what follows
- Alternative D: No divider, no transition. The identity section flows directly into the next section, creating a continuous document rather than a segmented one.
- PURPOSE: Controls whether identity "leaks" into subsequent sections (no divider), is reinforced at the boundary (recap), or is compartmentalized (clean break).
- HYPOTHESIS: For agents with long prompts, identity fade is a real phenomenon — by the time the agent reaches the 10th instruction step, its identity may have weakened. A recap at the section boundary may slow this fade. But a recap is also a form of redundancy, and agents that learn "the prompt repeats important things" may weight un-repeated things lower. The clean break (A) is neutral — it neither reinforces nor fades identity. The continuous flow (D) is an interesting experiment: if there is no section boundary, does the agent treat all content as part of a single continuous configuration? Test: does a recap at the identity section boundary measurably reduce identity fade in agents with long instruction sections?
- STABILITY: experimental (recap presence) + structural (divider choice)

---

## STRUCTURAL: field_ordering_and_grouping

### What the agent needs to understand

Primacy effects in LLM processing are strong: the first information encountered disproportionately shapes interpretation of everything that follows. The ordering of identity fields determines what serves as the primary frame.

### Fragments

**field_sequence**
- Current (defective): title-heading -> description-labeled -> role_identity-prose -> role_description-paragraph -> role_responsibility-labeled -> role_expertise-labeled
- Alternative A: **Identity-first**: role_identity -> role_description -> role_responsibility -> role_expertise (description suppressed). The agent learns who it is, how it thinks, what it delivers, and what it is expert in — in that order. Each field elaborates on the previous one.
- Alternative B: **Stance-first**: role_description -> role_identity -> role_expertise -> role_responsibility. The agent learns how to think first, then gets a label for that thinking style, then learns its authority domains, then learns its deliverable. This order prioritizes cognitive calibration over identity.
- Alternative C: **Responsibility-first**: role_responsibility -> role_identity -> role_description -> role_expertise. The agent learns its deliverable first — "here is what you must produce" — then learns who it is and how to think about producing it. This may produce the most task-focused agents.
- Alternative D: **Fused**: no discrete field ordering. All fields composed into 1-2 natural-language paragraphs. `You are a {role_identity}. {role_description} Your specific deliverable: {role_responsibility}. You bring expertise in {expertise_list}.`
- PURPOSE: Determines the agent's primary cognitive frame for interpreting everything that follows. Identity-first produces identity-framed agents. Responsibility-first produces task-framed agents. Stance-first produces cognition-framed agents.
- HYPOTHESIS: The best ordering may depend on the agent type. For the builder (creative, broad task), identity-first may produce better results because the agent needs a strong self-concept to navigate a complex design space. For the summarizer (mechanical, narrow task), responsibility-first may work better because the agent primarily needs to know what to produce and the cognitive stance is really a task instruction. This suggests the field ordering may need to be configurable based on agent characteristics — not one ordering for all agents. Test: does identity-first ordering improve output for creative-task agents? Does responsibility-first ordering improve output for mechanical-task agents?
- STABILITY: structural — but potentially conditional on agent type, which makes it a high-leverage design decision

**density_and_visual_weight**
- Current (defective): medium density — some fields labeled, some as prose, whitespace between elements
- Alternative A: High density — all fields in 1-2 paragraphs, no labels, no line breaks within the section. Identity reads as a single block of continuous text.
- Alternative B: Low density — each field gets its own labeled line with whitespace above and below. Identity reads as a structured specification.
- Alternative C: Variable density — core fields (role_identity, role_description) rendered as dense prose; supporting fields (expertise, responsibility) rendered as labeled specifications. The agent processes the core identity immersively and the supporting details structurally.
- PURPOSE: High density promotes internalization (the agent absorbs identity as a gestalt). Low density promotes recall (the agent can reference specific fields). Variable density combines both.
- HYPOTHESIS: For identity specifically, internalization may be more important than recall. The agent does not need to "look up" its identity — it needs to *be* its identity. This argues for higher density. But if the agent has a complex responsibility (7 sub-tasks), that specific field may need to be structured for recall even if the rest is dense. Variable density (C) may be the right answer: dense core, structured periphery. Test: does increasing density of the identity section improve role adherence? Does it hurt recall of specific responsibility items?
- STABILITY: structural (density strategy) + formatting (exact whitespace/label choices)

---

## CROSS-FIELD DEPENDENCIES

### description x role_description (voice mismatch)
Description is third-person ("Creates new agent TOML definitions..."). Role_description is second-person ("You create agent definitions from requirements."). If both are rendered, the agent encounters two voices describing the same thing. Resolution: either transform description to second person, suppress it, or render it only when it carries information not present in role_description.

### role_identity x role_description (identity-stance fusion)
These two fields are cognitively linked: role_identity IS the compressed version of role_description. Rendering them separately risks the agent treating them as independent facts rather than as two resolutions of the same self-concept. The template must decide whether to fuse them ("You are a definition author. You create agent definitions from requirements...") or separate them ("You are a definition author.\n\n**How you work:** You create agent definitions from requirements...").

### role_responsibility x instructions
The responsibility defines what the agent delivers. The instructions tell it how to produce that deliverable. If the responsibility says "produce a complete TOML definition" but the instructions only cover 5 of 7 sub-tasks, the agent must resolve the gap. The identity section creates an expectation that the instructions section must fulfill. The template system should validate this alignment, not leave it to the agent.

### role_expertise x constraints/anti_patterns
Expertise grants authority in specific domains. Constraints restrict behavior in potentially overlapping domains. If expertise says "minimum permission security modeling" and constraints say "do not make security decisions independently," there is a contradiction. The template system needs at minimum a linting step to detect these conflicts.

### title x role_identity (naming collision)
The agent has two names: the system name (title) and the role name (role_identity). These are often different: "Agent Builder" vs. "definition author", "Interview Enrich Create Summary" vs. "contextual interview summarizer." The template must decide which one the agent internalizes. Rendering both without clear hierarchy may cause the agent to oscillate between self-concepts.

### description x frontmatter.description x dispatcher.agent_description (triple redundancy)
Same string appears in three places in the data. The identity section rendering must be aware of this and avoid triple-presenting the same information.

---

## CROSS-SECTION DEPENDENCIES

### identity -> instructions
The identity section sets up the cognitive lens through which instructions are interpreted. An identity that emphasizes "data forms, not prose documents" will cause the agent to interpret ambiguous instructions as requiring structured output. An identity that emphasizes "contextual significance" will cause the agent to apply more judgment. The identity section is not standalone — it is the interpretive frame for the instructions section.

### identity -> critical_rules
Critical rules override everything, including identity. The identity section should not promise capabilities that critical rules will deny. But there is a subtler dependency: the identity section's framing affects how the agent *receives* critical rules. An agent with a strong identity ("I am a definition author, this governs all my decisions") may resist a critical rule that seems to contradict that identity. The framing of identity affects the agent's receptiveness to overrides.

### identity -> security_boundary
The security boundary constrains what the agent CAN do. The identity says what the agent SHOULD do. These must not conflict. An identity claiming expertise in "filesystem management" for an agent with no Write tool creates a frustrating dissonance.

### identity.model -> frontmatter.model
Same value. If model is rendered in identity, it is redundant with frontmatter. If not rendered in identity, frontmatter carries it for infrastructure purposes only.

---

## CONDITIONAL BRANCHES

### Branch 1: role_responsibility complexity
The builder's responsibility has 7 verb phrases. The summarizer's has 1. The rendering strategy should adapt: complex responsibilities may need decomposition (numbered list), simple ones should stay as prose. The trigger is the number of distinct action clauses in the responsibility string. Approximate heuristic: split on commas that separate independent clauses containing verbs; if count > 3, decompose.

### Branch 2: description redundancy with role_description
When description and role_description convey essentially the same information (summarizer case), description should be suppressed to avoid redundancy. When they carry complementary information (builder case — description mentions "include files" and "preparation packages" which role_description does not), description may be rendered. The trigger is content overlap, which is harder to detect programmatically but could be a definition-time annotation.

### Branch 3: title usefulness as identity
When the title is role-descriptive and natural ("Agent Builder"), it can serve as an identity anchor. When it is a pipeline identifier ("Interview Enrich Create Summary"), it is a poor identity anchor and should be suppressed from body prose in favor of role_identity. The trigger is whether the title reads as a natural self-concept — which again may need to be a definition-time annotation.

### Branch 4: expertise count
At 2-3 items, inline rendering works. At 4+ items, bulleted list is more appropriate. This is a purely mechanical conditional based on array length.

### Branch 5: agent task type (latent, not in data)
The builder is creative/broad. The summarizer is mechanical/narrow. The identity section may need to serve different functions for each type: boundary-setting for creative agents (don't go here), lens-configuring for mechanical agents (look at it this way). This conditional is NOT present in the current data model — there is no "task_type" field. Either the template must infer it from other signals (e.g., instruction count, model choice) or a new field should be added to the data model.

---

## FRAGMENTS NOT IN THE CURRENT SYSTEM

### task_mode_primer
Before any identity content, a brief statement about the kind of cognitive work this agent performs:
- `This task requires sustained attention over a sequence of items.` (summarizer)
- `This task requires creative-technical synthesis from a specification.` (builder)
- `This task requires systematic assessment against quality criteria.` (QC agent)
- PURPOSE: Pre-configures the LLM's cognitive processing mode before identity details arrive. Different task types activate different internal processing strategies.
- HYPOTHESIS: A task mode primer at the very start of the identity section may improve task performance by setting expectations about the *kind* of thinking required before the agent knows the specifics. This is analogous to telling someone "you're about to take a math test" vs. "you're about to write a creative essay" before they enter the room — the mental preparation is different. Test: does a task mode primer before identity content improve output quality?
- STABILITY: experimental — this fragment does not exist in the current system and its value is unknown
- NOTE: This would require a new field in the data model, or inference from existing fields.

### completeness_contract
A fragment that explicitly states the completeness expectation:
- `You must complete your entire scope. Partial completion is failure.` (for agents where completeness matters — builder, where a half-finished definition is useless)
- `Process every item. Skipping an item is a failure, even if the skip seems harmless.` (for batch agents — summarizer)
- Or conversely: `You may produce partial results if the input is insufficient. Report what you could not complete.` (for agents where partial completion is acceptable)
- PURPOSE: Configures the agent's relationship with incompleteness. Some agents must be all-or-nothing. Some agents may reasonably produce partial output. This is currently implied by other sections but never stated directly in identity.
- HYPOTHESIS: An explicit completeness contract in the identity section reduces ambiguity about what to do when problems arise mid-task. Without it, the agent must infer from success/failure criteria whether partial completion is acceptable — and that inference happens late in the prompt, after the agent has already started working.
- STABILITY: experimental — positioning this in identity vs. instructions vs. critical_rules is itself a design decision

### agency_calibration
A fragment that tells the agent how much autonomous judgment to exercise:
- `When instructions are ambiguous, apply your expertise to resolve the ambiguity. Do not stop to ask.` (high agency — builder)
- `When instructions are unclear, follow the most conservative interpretation. Do not improvise.` (low agency — summarizer)
- `When instructions are silent on a case, flag the gap in your return status but continue processing.` (medium agency — report and continue)
- PURPOSE: Configures the agent's default response to novel situations. This is not the same as expertise (which says *where* to exercise judgment) — it is about *how much* judgment to exercise.
- HYPOTHESIS: Without explicit agency calibration, agents default to their base persona's level of helpfulness — which for most LLMs means "try to solve everything, never admit uncertainty." This default is wrong for tight batch agents (they should be conservative) and may be wrong for creative agents (they should exercise judgment but within scope). Test: does explicit agency calibration reduce error rates in ambiguous cases?
- STABILITY: experimental — and possibly conditional on agent type
