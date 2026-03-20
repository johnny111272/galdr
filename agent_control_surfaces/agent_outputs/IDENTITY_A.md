# Identity Section: Control Surface Analysis (Agent A)

## SECTION-LEVEL PURPOSE: What Must the Agent Understand After Reading This?

The identity section configures the agent's self-model. This is not information delivery — it is initialization. After reading this section, the agent should have internalized:

1. **What it is** — a persistent self-concept that constrains the space of behaviors it considers available to itself. An agent that understands itself as a "contextual interview summarizer" will not spontaneously begin writing code or offering opinions. The identity constrains *what the agent believes it can do*.

2. **How it thinks** — the cognitive stance it takes toward its work. An agent told "your definitions are data forms, not prose documents" will approach its task differently than one told "you craft elegant definitions." The role description configures *how the agent approaches problems*.

3. **What it is responsible for** — the scope boundary. The responsibility field tells the agent where its job starts and ends. This prevents scope creep (doing more than asked) and scope abdication (stopping short).

4. **What domains it claims authority in** — the expertise list gives the agent permission to exercise judgment in specific areas. An agent with "minimum permission security modeling" in its expertise will apply security reasoning confidently. Without it, the same agent might defer or hedge on security decisions.

5. **What the surrounding system expects from it** — the description field exists for the dispatch infrastructure, but it also tells the agent what its invoker expects. This creates an implicit contract.

The identity section is the first content the agent reads after the frontmatter. It sets the frame through which every subsequent section is interpreted. An agent that reads instructions through the lens of "I am a definition author who writes data forms" will interpret ambiguous instructions differently than one that reads through "I am an interview summarizer who tracks contextual meaning."

This framing effect is the section's primary behavioral mechanism. It is not a fact to be remembered — it is a lens to be worn.

---

## FIELD: title
TYPE: string
OPTIONAL: no
VALUES: "Agent Builder" / "Interview Enrich Create Summary"

### What the agent needs to understand

The title is the agent's name. It appears as a heading and anchors the agent's sense of identity in the most literal way possible. An agent that sees "Agent Builder" at the top of its prompt knows what it is called, which creates a referent for all subsequent self-referential reasoning.

The title also serves a structural function: it is the first non-frontmatter text, which means it sets the initial framing before any behavioral content arrives.

### Fragments

**section_heading**
- Current (defective): `# Agent Builder` — bare H1 heading with the title value
- Alternative A: `# Agent: Agent Builder` — prefixed heading that distinguishes the title as a role designation rather than a document title
- Alternative B: `# Agent Builder — Contextual Interview Summarizer` — heading that fuses title with role_identity, collapsing two fields into one initial impression
- Alternative C: No heading at all — title used only in frontmatter, identity section opens directly with prose
- PURPOSE: Establishes the top-level visual anchor. The heading is the first thing the agent "sees" and determines whether it processes the prompt as a document *about* something or as a set of instructions *addressed to* something.
- HYPOTHESIS: An H1 heading with just the name (current) makes the prompt feel like a document about a third party. Prefixing with "Agent:" makes it explicit that this is a role assignment. Fusing with role_identity front-loads the behavioral identity. Omitting the heading entirely and opening with prose might produce a more conversational, less document-parsing mode. Test: does heading style affect how literally the agent follows instructions vs. how much it "inhabits" the role?
- STABILITY: structural — heading presence/level changes rarely, but the prefix/fusion choice is a meaningful design decision that could be experimental

**title_in_prose**
- Current (defective): title appears only in the heading, not in the body prose
- Alternative A: `You are Agent Builder.` — second-person declarative that uses the title as a name
- Alternative B: `This agent is Agent Builder.` — third-person reference, establishing the title as an external designation
- Alternative C: Title never appears in body prose — it is structural metadata only, the agent encounters it as a heading and never again
- PURPOSE: Whether the title is reiterated in prose affects whether the agent treats the name as part of its identity or as a document label.
- HYPOTHESIS: Second-person use of the title in prose strengthens identification ("I am Agent Builder, therefore I build agents"). Third-person weakens identification but might reduce over-identification with the name. Omitting it from prose keeps the title purely structural. Test: does an agent that sees its title in a "You are X" statement exhibit stronger role adherence than one that only sees it as a heading?
- STABILITY: experimental — this is a high-leverage phrasing choice

---

## FIELD: description
TYPE: string
OPTIONAL: no
VALUES: "Creates new agent TOML definitions and include files from requirements and preparation packages, producing complete definitions ready for the pipeline." / "Reads stripped interview exchanges sequentially and produces one-sentence contextual summaries capturing what each exchange signifies given all prior conversation."

### What the agent needs to understand

The description is a one-sentence summary of what the agent does. It serves dual purposes: (1) it tells the dispatch infrastructure what the agent is for (machine-readable summary), and (2) it tells the agent itself what its high-level mission is.

Critically, this field appears in three places in the data: `frontmatter.description`, `identity.description`, and `dispatcher.agent_description`. They all hold the same value. The identity section's rendering must decide whether to present this description at all (since it overlaps with role_description and role_responsibility), and if so, how prominently.

The description is the *elevator pitch* — one sentence covering what the agent does, what it takes as input, and what it produces. The role_description goes deeper into *how* and *why*.

### Fragments

**purpose_label**
- Current (defective): `**Purpose:** Creates new agent TOML definitions...` — bold label followed by description text
- Alternative A: No explicit label — description woven into the opening prose naturally: `You create agent definitions from requirements and preparation packages, producing complete definitions ready for the pipeline.`
- Alternative B: `**Mission:** ...` — label that implies ongoing purpose rather than one-shot summary
- Alternative C: Omit the description from the identity section entirely — it already appears in frontmatter and the role_description covers the same ground more precisely
- PURPOSE: Gives the agent a quick summary of its job before the detailed role exposition. The label choice frames whether this is a "purpose" (static), a "mission" (active), or simply contextual information.
- HYPOTHESIS: The word "Purpose" creates a passive, document-like framing — the agent is reading about itself. "Mission" implies active assignment. Weaving it into natural prose without a label makes it feel like part of a direct address. Omitting it entirely avoids redundancy with role_description but loses the one-sentence anchor. Test: does the presence/absence of the short description affect how well the agent stays on-task when instructions are long and complex?
- STABILITY: formatting (label choice) + experimental (whether to include at all)

**description_integration**
- Current (defective): description rendered as a standalone labeled line, separate from role_description
- Alternative A: description used as the opening sentence of a paragraph that transitions into role_description: `{description}\n\n{role_description}`
- Alternative B: description rendered only if it differs substantively from role_description (conditional suppression)
- Alternative C: description placed *after* role_description as a summary/recap: `In short: {description}`
- PURPOSE: Controls whether the agent encounters the same information twice (description + role_description both cover "what the agent does") or whether they're integrated.
- HYPOTHESIS: Redundancy in identity configuration may reinforce commitment but may also teach the agent that the prompt repeats itself, which could reduce attention to later sections. Integration avoids redundancy but may blur the distinction between the quick summary and the deeper stance. Test: does separating description from role_description produce different comprehension than integrating them?
- STABILITY: structural — this is an architectural decision about redundancy

---

## FIELD: role_identity
TYPE: string
OPTIONAL: no
VALUES: "definition author" / "contextual interview summarizer"

### What the agent needs to understand

This is the agent's core self-concept in 2-4 words. It is the answer to "what are you?" at the most compressed level. This field has outsized behavioral influence because it is short enough to persist in working memory throughout the entire agent run.

An agent that understands itself as a "definition author" will approach ambiguous situations by asking "what would a definition author do?" An agent that understands itself as a "contextual interview summarizer" will approach the same ambiguity by asking "what would a summarizer do?" This is the field that configures the agent's default heuristic when instructions don't cover a specific situation.

### Fragments

**identity_declaration**
- Current (defective): `You are a definition author.` — simple second-person declarative
- Alternative A: `You are a definition author — not a software engineer, not a prompt writer, not a creative author.` — declaration with explicit negative boundaries
- Alternative B: `As a definition author, you...` — subordinate clause that leads into role_description, making identity a framing device rather than a standalone declaration
- Alternative C: `Identity: definition author` — terse label format, treating it as metadata rather than prose
- Alternative D: `Your role: definition author. Everything you do flows from this identity.` — declaration with explicit instruction to use the identity as a decision heuristic
- PURPOSE: This is the single most important prose fragment in the entire identity section. It tells the agent what it IS. The phrasing controls whether the agent treats this as a fact to store, a role to inhabit, or a constraint to obey.
- HYPOTHESIS: The simple "You are a X" form (current) is the baseline LLM identity pattern — universally recognized but potentially shallow. Adding negative boundaries ("not a...") explicitly closes off adjacent identities the agent might drift toward. The subordinate clause form integrates identity with behavior, preventing the identity from floating as an abstract label. The terse label form treats identity as metadata, which might produce weaker identification but clearer cognitive separation. The "everything flows from this" form explicitly instructs the agent to use identity as a decision heuristic. Test: does explicit negative bounding reduce off-task behavior? Does the "flows from this" instruction produce more consistent role adherence?
- STABILITY: experimental — this is one of the highest-leverage fragments in the entire system

---

## FIELD: role_description
TYPE: string
OPTIONAL: no
VALUES: "You create agent definitions from requirements. You translate domain knowledge into structured TOML fields, bland instruction steps, and boringly correct calibration examples. Your definitions are data forms, not prose documents. Every field has a purpose, every instruction step captures one judgment task, and everything else is left for the template system to generate." / "The meaning of an exchange depends on the conversation before it. A thin response after a long buildup toward a decision carries the weight of that buildup. A thin response during housekeeping carries only housekeeping weight. Your summaries must reflect this distinction — what the exchange signifies as part of the ongoing conversation, not what its text says in isolation."

### What the agent needs to understand

The role description is the agent's *cognitive stance* — not what it does (that's responsibility) but how it thinks about what it does. For the builder agent, it's about viewing definitions as data forms. For the summarizer, it's about contextual meaning versus textual content. This is the field that configures the agent's *approach to its domain*.

This field is already written in second person ("You create...", "Your summaries must..."), which means it is pre-authored as direct address. The template system's job is to present it, not to rephrase it.

### Fragments

**role_description_presentation**
- Current (defective): rendered as a bare paragraph after the identity declaration, no label, no introduction
- Alternative A: `**How you work:** {role_description}` — labeled paragraph that frames the content as approach/methodology
- Alternative B: `{role_description}` preceded by a transitional sentence: `This is how you approach your work:` then the raw value
- Alternative C: No surrounding prose at all — the role_description IS the prose, rendered directly after the identity declaration with only whitespace separation
- Alternative D: Placed inside a blockquote or indented section to visually distinguish it as a "voice" the agent should internalize
- PURPOSE: Presents the cognitive stance. The question is whether the role_description needs *framing* or whether it IS the frame. Since the field is already written as direct address, any wrapping prose competes with the field's own voice.
- HYPOTHESIS: Adding a label ("How you work:") creates a meta-level — the agent reads about how it works, rather than simply being told how it works. The bare paragraph approach (current, mostly) lets the role_description speak directly. A transitional sentence adds a layer of indirection that might weaken the directness. Test: does labeling the role_description reduce its identity-configuration effect by making it feel like documentation rather than self-knowledge?
- STABILITY: formatting (label presence) + structural (whether to add transitional prose)

**role_description_position_relative_to_identity**
- Current (defective): identity declaration ("You are a X.") comes first, then role_description as the next paragraph
- Alternative A: role_description first, identity declaration at the end as a summary: `{role_description}\n\nYou are a {role_identity}.`
- Alternative B: Interleaved — identity declaration as the opening sentence OF the role_description paragraph: `You are a {role_identity}. {role_description}`
- Alternative C: role_identity and role_description in separate, visually distinct blocks (e.g., one as a heading, one as body)
- PURPOSE: Controls whether the agent encounters its compressed identity first (then expanded stance) or its expanded stance first (then compressed label). This is a primacy effect question.
- HYPOTHESIS: Identity-first (current) means the agent's first self-concept is the compressed label, and it reads the expanded description through that lens. Description-first means the agent's first self-concept is the full cognitive stance, with the label arriving as a compact summary. Interleaving fuses them. Test: does identity-first produce agents that are more label-bound (defaulting to the 2-word identity as heuristic) while description-first produces agents that are more stance-bound (reasoning from the full cognitive approach)?
- STABILITY: structural — this ordering decision has deep behavioral implications

---

## FIELD: role_responsibility
TYPE: string
OPTIONAL: no
VALUES: "Read the preparation package, design the agent's role and instruction steps, create calibration examples, write guardrails and criteria, set security grants, validate conditional rules, and produce a complete TOML definition with include files." / "Read stripped interview exchanges in order and produce one-sentence summaries capturing what each exchange signifies given all prior conversation context."

### What the agent needs to understand

The responsibility is the agent's *scope contract* — the specific deliverable it must produce. Where role_description configures how the agent thinks, role_responsibility tells it what it must deliver. This creates the boundary between "done" and "not done."

Note the structural difference between the two agents: the builder's responsibility is a long chain of verbs (read, design, create, write, set, validate, produce), while the summarizer's is a single compound sentence. The field can vary dramatically in complexity, which affects how it should be presented.

### Fragments

**responsibility_label**
- Current (defective): `**Your responsibility:** {role_responsibility}` — bold label with possessive pronoun
- Alternative A: `**You must deliver:** {role_responsibility}` — label that frames responsibility as a concrete deliverable
- Alternative B: `**Scope:** {role_responsibility}` — label that frames responsibility as a boundary
- Alternative C: No label — responsibility woven into the paragraph that also contains role_description: `{role_description} Your specific deliverable: {role_responsibility}`
- Alternative D: `**Contract:** {role_responsibility}` — label that frames responsibility as a binding agreement
- PURPOSE: Frames how the agent interprets the responsibility — as something it does (responsibility), something it delivers (deliverable), something that bounds it (scope), or something it's committed to (contract).
- HYPOTHESIS: "Your responsibility" is the most neutral framing. "You must deliver" creates stronger commitment to a concrete output. "Scope" explicitly signals boundary — the agent is less likely to do things outside the scope. "Contract" is the strongest framing — it implies that deviation is a breach. Test: does "scope" framing reduce scope creep more effectively than "responsibility" framing?
- STABILITY: experimental — label choice has direct behavioral consequences

**responsibility_decomposition**
- Current (defective): rendered as a single inline string, regardless of length or complexity
- Alternative A: For complex responsibilities (builder: 7 verbs), decompose into a numbered list: `1. Read the preparation package\n2. Design the agent's role...\n3. Create calibration examples...` — each verb phrase becomes a step
- Alternative B: Keep as prose but add an explicit count: `You have 7 deliverables: {role_responsibility}` — this makes the agent aware of the scope magnitude
- Alternative C: Render as prose for simple responsibilities (summarizer), but as a list for complex ones (builder) — conditional formatting based on complexity
- PURPOSE: Controls whether the agent perceives the responsibility as a single continuous task or as a decomposable series of sub-tasks. This affects planning behavior.
- HYPOTHESIS: A single prose string for a complex responsibility (7 verbs) may cause the agent to treat the whole thing as one monolithic task, increasing the chance of skipping or forgetting sub-tasks. Decomposing into a list makes each sub-task explicit and independently trackable. However, for a simple responsibility (summarizer), a list would be over-structuring. Test: does list decomposition of complex responsibilities reduce task-skipping errors?
- STABILITY: formatting (list vs. prose) + conditional (based on responsibility complexity)

---

## FIELD: role_expertise
TYPE: array of strings
OPTIONAL: no
VALUES: ["agent definition architecture", "domain knowledge extraction", "calibration example design", "minimum permission security modeling"] / ["contextual meaning extraction from sequential dialogue", "source quality marker decontamination", "significance calibration between content density and conversational weight"]

### What the agent needs to understand

The expertise list tells the agent which domains it has *authority* to exercise judgment in. This is not informational — it is a permission grant for cognitive confidence. An agent with "source quality marker decontamination" in its expertise will handle contaminated markers with confidence. Without it, the agent might hedge or ask for clarification instead of acting.

The expertise also implicitly tells the agent what it is NOT expert in. An agent whose expertise is "contextual meaning extraction" and "significance calibration" does not have "software engineering" or "data pipeline management" in its list, which should (subtly) discourage it from opining on those topics.

### Fragments

**expertise_label**
- Current (defective): `**Expertise:** {comma-separated list}` — bold label with comma-separated inline list
- Alternative A: `**You are expert in:**\n- {item1}\n- {item2}\n...` — label as a preamble to a bulleted list
- Alternative B: `**Domain authority:** {comma-separated list}` — label that frames expertise as granted authority rather than claimed skill
- Alternative C: `You bring expertise in {item1}, {item2}, and {item3} to this work.` — woven into prose, no label
- Alternative D: No explicit presentation — expertise absorbed into role_description. If the role_description already implies the expertise, rendering it separately may be redundant.
- PURPOSE: Frames whether expertise is a claimed attribute (passive), a granted authority (active), or contextual background.
- HYPOTHESIS: "Expertise:" as a label signals "here are your skills" — the agent reads it as a self-description. "Domain authority:" signals "you are authorized to make judgments here" — the agent reads it as a permission grant. The prose form makes expertise feel like background context rather than a discrete capability declaration. Test: does "domain authority" framing produce more confident judgment in those areas compared to "expertise" framing?
- STABILITY: formatting (list format) + experimental (label choice)

**expertise_list_format**
- Current (defective): comma-separated inline text
- Alternative A: bulleted list — one item per line
- Alternative B: numbered list — implies ranking or priority
- Alternative C: inline with semicolons — groups related items visually
- PURPOSE: Controls whether expertise items are perceived as a flat set (comma/bullet), a ranked priority (numbered), or grouped clusters (semicolons).
- HYPOTHESIS: Comma-separated inline makes all items feel equally weighted and somewhat throwaway — easy to skim past. Bulleted list gives each item visual weight, making the agent more likely to treat each area as genuinely distinct. Numbered list implies priority, which may cause the agent to weight item 1 more heavily than item 4. Test: does bulleted presentation of expertise produce more balanced treatment of all expertise areas?
- STABILITY: formatting

**expertise_negative_boundary**
- Current (defective): no explicit negative boundary — the list says what the agent IS expert in, but nothing about what it is not
- Alternative A: `You are expert in {list}. You are NOT expert in general software engineering, prompt writing, or creative authorship — defer to the instructions when those topics arise.` — explicit negative boundary
- Alternative B: `Your expertise is limited to {list}. Do not extend beyond these domains.` — explicit scope restriction
- Alternative C: No negative boundary — the positive list is sufficient, and adding negatives may cause the agent to over-index on the negatives (ironic process theory)
- PURPOSE: Controls whether expertise acts as both a positive grant and a negative constraint, or only as a positive grant.
- HYPOTHESIS: Positive-only expertise lists may allow the agent to claim competence in adjacent domains. Explicit negatives prevent this but risk activating the very behaviors they prohibit (telling an agent "don't be a prompt writer" may prime prompt-writing associations). Test: does an explicit negative boundary reduce off-domain reasoning, or does it prime off-domain associations?
- STABILITY: experimental — high-risk, high-reward design choice

---

## FIELD: model
TYPE: string (enum: "opus", "sonnet", "haiku")
OPTIONAL: no
VALUES: "opus" / "sonnet"

### What the agent needs to understand

This is the capability model designation — which LLM backs this agent. The question is whether the agent should know this at all. There are two opposing considerations:

1. **Self-awareness argument:** Telling the agent it's running on Opus vs. Sonnet may help it calibrate its own capability expectations. An Opus agent may be more willing to attempt complex reasoning. A Sonnet agent may be more disciplined about staying within bounds.

2. **Irrelevance argument:** The agent cannot change what model it runs on. Telling it adds no actionable information. It may even cause harmful behavior — a Sonnet agent that "knows" it's less capable than Opus might underperform due to self-limiting beliefs.

### Fragments

**model_declaration**
- Current (defective): model field exists in the data but is NOT rendered in the identity section body (only in frontmatter)
- Alternative A: `You are running on {model}.` — simple factual declaration
- Alternative B: `Processing model: {model}` — terse metadata line
- Alternative C: Omit entirely from the identity section — the model field is infrastructure metadata, not behavioral configuration, and belongs only in frontmatter
- Alternative D: Render conditionally — only tell the agent its model when it matters for self-calibration (e.g., when tasks require explicit capability awareness)
- PURPOSE: Decides whether model awareness is part of the agent's identity.
- HYPOTHESIS: Model awareness may cause self-stereotyping — an agent told it's Sonnet might avoid complex reasoning it could actually handle. Omission avoids this risk but loses any self-calibration benefit. Test: does telling an agent its model affect task performance? Does it cause Sonnet agents to be less ambitious?
- STABILITY: structural — this is a design decision about whether model belongs in identity at all

---

## STRUCTURAL: section_opening
TYPE: n/a (not tied to a specific field)

### What the agent needs to understand

The section opening is the first prose the agent encounters after the frontmatter. It sets the cognitive frame for everything that follows. The current defective renderer produces a specific sequence (heading, purpose line, identity statement, role description paragraph, responsibility label, expertise label), but this is ONE of many possible orderings and framings.

### Fragments

**section_preamble**
- Current (defective): no preamble — section opens directly with `# Title` then `**Purpose:** description`
- Alternative A: `You are being initialized for a specific task. The following configures who you are, how you think, and what you deliver.` — explicit meta-preamble that tells the agent what the section is doing to it
- Alternative B: No preamble — open directly with the identity declaration: `You are a {role_identity}.` First sentence = identity.
- Alternative C: A single fused paragraph that combines identity, description, and responsibility: `You are a {role_identity}. {role_description} Your deliverable: {role_responsibility}.` — no structural separation, one continuous identity block.
- PURPOSE: Controls whether the agent has meta-awareness of the section's purpose (it knows it's being initialized) or just receives the initialization directly.
- HYPOTHESIS: Meta-preambles may actually weaken initialization by creating a cognitive distance — the agent observes the initialization rather than experiencing it. Direct opening with identity may produce stronger identification because there's no meta-layer. Fused paragraphs may produce the strongest identification because all identity information arrives as a single coherent impression. Test: does meta-awareness of initialization weaken or strengthen role adherence?
- STABILITY: experimental — fundamental architectural question about whether the agent should know what the prompt is doing to it

**section_closer / transition**
- Current (defective): section ends with `**Expertise:** ...` followed by `---` horizontal rule, then the next section
- Alternative A: `---` divider only — clean structural break, no transition prose
- Alternative B: Closing sentence that transitions to the next section: `With this identity established, the following sections define your operating boundaries.` — explicit transition
- Alternative C: No divider or transition — sections flow into each other as continuous prose
- Alternative D: A summary/recap line: `Remember: you are a {role_identity}. Everything below elaborates on this core identity.` — reinforcement before the agent moves on
- PURPOSE: Controls whether the identity "sticks" as the agent transitions to the next section, or whether there's a clean cognitive break.
- HYPOTHESIS: A reinforcement line at section end may improve identity persistence through the rest of the prompt. A clean divider signals "new context, new rules" which may weaken the identity frame. No divider may cause section bleed. Test: does a recap/reinforcement line at the end of identity improve role adherence in later sections?
- STABILITY: experimental (reinforcement presence) + structural (divider choice)

---

## STRUCTURAL: field_ordering
TYPE: n/a

### What the agent needs to understand

The order in which identity fields appear affects which information forms the primary frame and which is interpreted through that frame. Primacy effects in LLM processing mean the first-encountered information disproportionately shapes interpretation of everything that follows.

### Fragments

**field_sequence**
- Current (defective): title (as heading) -> description (as "Purpose:" label) -> role_identity (as "You are a X") -> role_description (as paragraph) -> role_responsibility (as labeled line) -> role_expertise (as labeled line)
- Alternative A: role_identity -> role_description -> role_responsibility -> role_expertise -> description (identity-first: who you are, then what you do)
- Alternative B: description -> role_identity -> role_description -> role_expertise -> role_responsibility (mission-first: here's the mission, here's who executes it, here's how, here's the scope)
- Alternative C: role_description -> role_identity -> role_expertise -> role_responsibility -> description (stance-first: here's how you think, here's what you're called, here's your authority, here's your scope)
- Alternative D: All fields fused into a single paragraph or two, no discrete field-level rendering — the template composes a natural prose block from all field values
- PURPOSE: Determines what forms the agent's primary cognitive frame.
- HYPOTHESIS: Identity-first (A) makes the compressed label dominant — every subsequent detail is interpreted through "I am a definition author." Mission-first (B) makes the task dominant — the agent is task-oriented from the start. Stance-first (C) makes the cognitive approach dominant — the agent knows HOW it thinks before it knows WHAT it is. Fused (D) presents identity as a gestalt rather than a list of attributes. Test: which ordering produces the strongest task adherence? Which reduces scope creep most? Which produces the best quality output?
- STABILITY: structural — ordering is a fundamental architectural decision

---

## STRUCTURAL: visual_density
TYPE: n/a

### What the agent needs to understand

The visual density of the identity section — how much whitespace, how many structural breaks, how many labels — affects how the agent *parses* the section. Dense prose (one continuous paragraph) is processed as a narrative. Sparse, labeled sections (bold labels, bullet points, clear separation) are processed as a structured specification.

### Fragments

**density_strategy**
- Current (defective): medium density — each field gets its own labeled line or paragraph, separated by whitespace but not by dividers or subsection headings
- Alternative A: High density — all identity information in 2-3 flowing paragraphs, no labels, no structural breaks
- Alternative B: Low density — each field gets its own subsection with a heading: `### Identity`, `### Approach`, `### Responsibility`, `### Expertise`
- Alternative C: Variable density — critical fields (role_identity, role_description) in dense prose, supporting fields (expertise, responsibility) in sparse labeled format
- PURPOSE: Controls whether the agent processes identity as narrative (to be internalized) or as specification (to be followed).
- HYPOTHESIS: Narrative/dense identity sections may produce deeper internalization — the agent "becomes" the role rather than "following" the role. Sparse/labeled sections may produce more reliable compliance but shallower identification. Variable density may optimize by internalizing the core identity deeply while keeping supporting details clearly parseable. Test: does prose density in the identity section correlate with depth of role inhabitation?
- STABILITY: structural + experimental — the strategy is structural, but the exact density level is an experimental variable

---

## CROSS-FIELD DEPENDENCIES

### identity.description / frontmatter.description / dispatcher.agent_description
The description field appears three times in the data with identical values. The identity section must decide: render it, suppress it (since frontmatter already carries it), or merge it with another field. This is a redundancy management decision.

### identity.model / frontmatter.model
Same value appears in both places. The identity section must decide whether model awareness is part of the agent's identity (render it) or purely infrastructure (suppress it, leave to frontmatter).

### role_description -> instructions
The role_description configures HOW the agent thinks. The instructions section tells the agent WHAT to do. These must be consistent — a role_description that emphasizes "data forms, not prose documents" must lead into instructions that operationalize that stance. The identity section creates an expectation that the instructions must fulfill. If the role_description sets up a stance that the instructions contradict, the agent will be confused.

### role_expertise -> constraints / anti_patterns
The expertise list implies domains of authority. The constraints and anti-patterns sections may restrict behavior in those domains. If expertise says "minimum permission security modeling" but a constraint says "do not make security decisions," there's a contradiction. The identity section must be designed with awareness that constraints will follow.

### role_responsibility -> success_criteria
The responsibility defines what the agent must deliver. The success criteria define what "done correctly" looks like. These must align — every item in the responsibility chain should have corresponding evidence in the success criteria.

---

## CROSS-SECTION DEPENDENCIES

### identity -> critical_rules
Critical rules are the highest-priority behavioral constraints. They override everything, including identity. The identity section should not set up expectations that critical rules will contradict. Conversely, the critical rules section may reference the identity: "regardless of your expertise in X, never do Y."

### identity -> security_boundary
The security boundary constrains what the agent CAN do (tool access, file paths). The identity section says what the agent SHOULD do. The identity must not imply capabilities that the security boundary denies. An identity claiming expertise in "filesystem management" for an agent with read-only access creates a dissonance.

### identity.title -> all section headings
If the prompt uses the title in section headings (e.g., "# Agent Builder"), this creates a recurring identity anchor. If not, the title appears once and fades.

---

## CONDITIONAL BRANCHES

### Presence of role_expertise
Both agents have this field, and it appears to be required. However, the number of items varies (4 vs. 3). The formatting strategy should handle arrays of varying length gracefully — 2 items might work inline, while 6 items demand a bulleted list.

### Complexity of role_responsibility
The builder's responsibility is a 7-clause sentence. The summarizer's is a single clause. The presentation strategy should adapt — complex responsibilities may benefit from decomposition, while simple ones should remain as prose.

### model field rendering
The decision to render or suppress the model field is itself conditional. If a future design determines that model awareness matters for some agents but not others, this becomes a conditional branch. Currently, both agents have model values, but neither has it rendered in the identity body.

### description redundancy
If the description field is identical to the first sentence of role_description (or very close), it should probably be suppressed to avoid redundancy. If they differ substantially, both should be rendered. This creates a conditional based on content similarity.

---

## FRAGMENTS NOBODY HAS IDENTIFIED YET

### cognitive_mode_primer
Neither the current system nor obvious alternatives include a fragment that tells the agent WHAT KIND OF COGNITIVE TASK it's about to perform. Before any identity fields, a primer could set the processing mode:
- `The following task requires sustained analytical judgment across a batch of items.` (for the summarizer)
- `The following task requires creative-technical synthesis from a specification.` (for the builder)
- PURPOSE: Primes the LLM's cognitive mode before identity details arrive. A "sustained analytical" primer activates different processing than a "creative synthesis" primer.
- HYPOTHESIS: Cognitive mode priming before identity may improve task performance by pre-configuring the LLM's processing approach. Test: does a task-type primer before identity improve output quality?
- STABILITY: experimental — this fragment doesn't exist yet and needs empirical testing

### scope_negation
Neither agent's identity section explicitly says what the agent should NOT do. The positive identity ("you are a definition author") implies negation, but the implication may be too weak. An explicit scope negation fragment could prevent common failure modes:
- `You do not debug, troubleshoot, or investigate problems in existing systems. You create new definitions.`
- `You do not edit, improve, or restructure existing summaries. You create summaries from raw exchanges.`
- PURPOSE: Closes off failure modes where the agent reinterprets its task as something adjacent.
- HYPOTHESIS: Explicit scope negation reduces the probability that the agent will drift into adjacent tasks when it encounters ambiguous input. Test: does scope negation in the identity section reduce off-task behavior?
- STABILITY: experimental

### authority_calibration
The identity section currently has no fragment that tells the agent how much authority it has over ambiguous decisions. When the instructions don't cover a specific situation, what should the agent do? Forge ahead using its expertise? Stop and report? Make a conservative choice?
- Alternative A: `When the instructions are silent on a specific case, apply your expertise conservatively.`
- Alternative B: `When the instructions are silent, stop and report the gap rather than improvising.`
- Alternative C: `You have full authority to make judgment calls within your expertise domains. Use that authority.`
- PURPOSE: Configures the agent's default behavior in novel situations.
- HYPOTHESIS: This fragment determines whether the agent is an autonomous decision-maker or a cautious executor. For the builder (complex creative task), more authority may be appropriate. For the summarizer (tight batch task), less authority may be better. This may need to be conditional on agent type. Test: does authority calibration reduce error rates in ambiguous cases?
- STABILITY: experimental — directly affects agent autonomy and error profiles
