# FAILURE_CRITERIA — Control Surface Synthesis

## Section Purpose

Failure criteria configure the agent's **abort circuitry** — conditions that halt work, not degrade it. This is adversarial to LLM training: models are completion machines, rewarded for producing output. Failure criteria must make stopping feel like correct professional behavior, not task abandonment. The target behavioral state is **armed vigilance with a license to halt.**

Failure criteria are not the inverse of success criteria. Success defines the quality ceiling (what done-right looks like). Failure defines the validity floor (what broken looks like). Between them lies mediocre-but-not-broken output. Failure criteria mark the cliff edge, not the quality gradient.

The raw data reveals two failure archetypes: **pre-flight** (builder: input insufficiency, checkable before work starts) and **in-flight** (summarizer: process breakage, discovered during execution). These require different monitoring postures but may or may not need different rendering.

---

## Fragment Catalog

### section_header

- CONVERGED: Both rejected "Failure Criteria" as carrying agent-inadequacy connotations that suppress abort willingness. Both favored externalizing framing.
- DIVERGED: A preferred mechanical language ("Abort Conditions," "Halt Triggers"). B explored diagnostic/impossibility framing ("Recognizing Broken Input," "Conditions That Prevent Success").
- ALTERNATIVES:
  - A: `## Abort Conditions` — Systems language, no emotional loading, frames these as environmental states.
  - B: `## Conditions That Prevent Success` — Externalizes failure completely; the agent is not broken, conditions are. Strongest completion-bias override.
  - C: `## When to Stop` — Most direct, lowest cognitive overhead, but potentially informal.
- HYPOTHESIS: The header name propagates through agent self-understanding. Names implying agent failure suppress abort behavior. "Conditions That Prevent Success" provides the strongest externalization but is long; "Abort Conditions" is tighter and still neutral.
- STABILITY: structural
- CONDITIONAL: none

### section_preamble

- CONVERGED: Both identified the preamble as the critical behavioral reframe — it must resolve the tension between training-driven completion bias and desired abort behavior. Both agreed stopping must be positioned as the correct, professional action. Both agreed output-after-detection is framed as worse than no output.
- DIVERGED: A explored four alternatives ranging from empathetic to permission-granting ("license to halt"). B explored consequence-based and quality-violation framings. B uniquely proposed omitting the preamble entirely.
- ALTERNATIVES:
  - A: `The following conditions make valid output impossible. When detected, halt immediately and report. An agent that detects a halt condition and stops is performing correctly. An agent that ignores a halt condition and produces output anyway has failed.` — Sharp inversion: halting = success, continuing = failure.
  - B: `Not every task can be completed. These conditions indicate that this task cannot produce valid output, and attempting to force output would violate quality standards.` — Normalizes incompletability, leverages quality-maintenance motivation.
  - C: `You have a license to halt. The conditions below define when exercising that license is mandatory. Output produced after a halt condition is detected is worse than no output — it is confidently wrong output that downstream consumers will trust.` — Permission-granting frame with downstream-harm consequence.
- HYPOTHESIS: The preamble's effect is priming — it shapes interpretation of everything that follows. The inversion frame (halting = success) is the most direct override of completion bias. The consequence frame (downstream harm) provides a secondary motivation. Both may be needed.
- STABILITY: structural
- CONDITIONAL: none — always present when the section exists

### failure_definition (field label)

- CONVERGED: Both identified the definition as a **category label** for a class of failure, distinct from detection signals. Both noted it serves as cognitive anchor, reporting label, and scope limiter (prevents catastrophizing every imperfection into a failure state).
- DIVERGED: A focused on label naming ("Failure mode" / "Halt condition" / "Abort trigger"). B focused on framing verbs ("Abort condition" / "Recognize this failure mode" / "Stop work if you determine" / "This work cannot succeed when").
- ALTERNATIVES:
  - A: `**This work cannot succeed when:** {definition}` — Externalizes failure, strongest completion-bias bypass.
  - B: `**Halt condition:** {definition}` — Operationally precise, matches "Abort Conditions" header.
  - C: No label — definition as first line of criteria block, semantics from layout.
- HYPOTHESIS: The label should be consistent with the section header. If the section is "Abort Conditions," "Halt condition" is coherent. If "Conditions That Prevent Success," the impossibility framing ("cannot succeed when") is coherent. Label consistency > label cleverness.
- STABILITY: formatting
- CONDITIONAL: Label wording follows section_header choice

### failure_evidence (list introduction)

- CONVERGED: Both identified evidence items as **detection signals** (not consequences), analogous to symptoms of a disease. Both agreed items are individually sufficient (disjunctive). Both recognized the continuous-monitoring nature versus success evidence's post-hoc checklist nature.
- DIVERGED: A favored "Watch for" as best capturing ongoing vigilance. B explored a wider range: obligation framing ("MUST abort"), logical framing ("any of the following indicates"), and temporally-split framing (different intros for pre-flight vs in-flight).
- ALTERNATIVES:
  - A: `**Any of the following indicates this failure — one signal is sufficient:**` — Logical, precise, makes disjunction explicit.
  - B: `**Watch for these signals:**` — Implies continuous monitoring, natural language.
  - C: `**You MUST abort if you observe:**` — Strongest behavioral signal, but risks over-triggering on ambiguous evidence.
- HYPOTHESIS: The disjunction must be explicit — without it, agents may wait for multiple signals before halting. "Any of the following" + "one signal is sufficient" handles both the logical relationship and the behavioral instruction in one line.
- STABILITY: formatting
- CONDITIONAL: none

### failure_evidence (item formatting)

- CONVERGED: Both agreed bulleted list is the baseline. Both explored conditional formatting (`IF...THEN`) and timing annotations (`[pre-flight]`/`[in-flight]`).
- DIVERGED: A considered first-person rephrasing ("You observe that..."). B explored signal notation ("SIGNAL: ...").
- ALTERNATIVES:
  - A: Bulleted list, bare text — clean, scannable, relies on introduction to carry semantics.
  - B: Conditional formatting `- IF {evidence} THEN this failure applies` — logically precise but verbose.
- HYPOTHESIS: Bare bullets are sufficient when the list introduction is strong. The introduction carries the behavioral weight; individual items just need to be scannable.
- STABILITY: formatting
- CONDITIONAL: none

### hierarchy_framing (definition-evidence relationship)

- CONVERGED: Both identified the two-level hierarchy (definition = category, evidence = symptoms) as important for structured failure reporting. Both connected this to return_format — the definition becomes the failure reason, evidence becomes supporting detail.
- DIVERGED: A proposed explicit framing text explaining the hierarchy. B embedded this understanding in the disease/symptoms metaphor without a separate fragment.
- ALTERNATIVES:
  - A: `Each failure mode has a definition (what went wrong) and evidence (how you detect it). When reporting, cite both.` — Instructional, connects to return_format.
  - B: No explicit framing — let nesting/indentation communicate the hierarchy.
- HYPOTHESIS: The reporting instruction ("cite both") is the high-value part. Without it, agents produce vague failure reports. This fragment's value is primarily in connecting failure_criteria to return_format.
- STABILITY: structural
- CONDITIONAL: Present only when return_format section exists

### temporal_model (pre-flight vs in-flight)

- CONVERGED: Both identified the builder=pre-flight / summarizer=in-flight distinction. Both agreed evidence items are largely self-describing for timing. Both recommended starting with unified treatment.
- DIVERGED: A proposed explicit timing tags on evidence items (`[CHECK BEFORE STARTING]`). B proposed schema-level timing field and renderer-level split, but ultimately recommended unified-first with split-if-needed.
- ALTERNATIVES:
  - A: No temporal instruction — evidence wording is self-describing.
  - B: Generic instruction: `Check what you can before starting; monitor the rest throughout.`
  - C: Explicit timing tags per evidence item (schema-level `timing` field).
- HYPOTHESIS: Start unified (A or B). Add temporal distinction only if testing shows agents fail to check pre-flight conditions before starting work. The generic instruction (B) is cheap insurance.
- STABILITY: experimental
- CONDITIONAL: More important for agents with expensive execution (builder) than cheap batch processors (summarizer)

### abort_behavioral_stance (obligation vs permission)

- CONVERGED: Both identified this as the deepest behavioral design question. Both recognized the tension: too permissive and agents ignore failures, too mandatory and agents abort on ambiguity.
- DIVERGED: A did not isolate this as a separate fragment — it was distributed across preamble alternatives. B gave it dedicated analysis and proposed it as potentially conditional on agent type (obligation for batch tasks, permission for creative tasks).
- ALTERNATIVES:
  - A: Pure obligation: `You MUST stop. Do not attempt to work around these conditions.` — Binary, no judgment. Best for batch tasks with unambiguous evidence.
  - B: Strong permission: `The correct action is to stop and report.` — Guides without commanding. Better for creative tasks with judgment-dependent evidence.
  - C: Consequence framing: `Continuing past these conditions produces output that will be rejected.` — Appeals to outcome rather than authority.
- HYPOTHESIS: Obligation framing is correct for tight batch tasks with binary evidence. Permission framing is correct for broad creative tasks with judgment-dependent evidence. This may need to be a conditional rendering parameter. Highest-impact design variable in the section — **must be tested empirically.**
- STABILITY: experimental
- CONDITIONAL: Potentially conditional on agent type or evidence ambiguity

---

## Cross-Section Dependencies

**failure_criteria -> return_format** (HARD dependency): Failure definitions become failure reasons in the return. Evidence becomes supporting detail. If failure_criteria exist, return_format MUST have a failure reporting mechanism. The hierarchy_framing fragment bridges these sections.

**failure_criteria -> success_criteria** (INDEPENDENCE): Not inverses. Different behavioral registers. The prompt must never frame failure criteria as "the opposite of success." No shared language between sections.

**failure_criteria -> guardrails** (BOUNDARY): Guardrails = "Am I doing this correctly?" (course-correct). Failure criteria = "Can I do this at all?" (halt). Guardrail violations mean wrong behavior; failure conditions mean impossible task. No content duplication across sections.

**failure_criteria -> execution_instructions** (SOFT dependency): Failure evidence references specific execution points. Pre-flight checks map to step 1. In-flight checks map to processing loops. Potential for inline rendering of failure checks within execution steps — increases detection but creates rendering coupling.

**failure_criteria -> role/identity** (B only): The agent's role affects how it relates to failure. An auditor role makes failure detection natural. A builder role makes it feel like defeat. The abort-is-correct reframe must be strong enough to override role-identity resistance.

---

## Conditional Branches

| Condition | Rendering Decision |
|---|---|
| Zero failure criteria entries | Omit section entirely. Never render empty. |
| Single failure criteria entry | Omit criteria-level disjunction language. Evidence-level disjunction still needed. |
| Multiple failure criteria entries | Explicit: "Any ONE of the following failure modes is sufficient to trigger abort." |
| All evidence is pre-flight | Consider checklist framing: "Confirm before proceeding." |
| All evidence is in-flight | Consider monitoring framing: "Monitor during execution." |
| Mixed evidence timing | Unified rendering with generic temporal instruction. |
| Tight batch agent (binary evidence) | Obligation abort stance. |
| Creative/analytical agent (judgment evidence) | Permission abort stance with strong guidance. |
| return_format section exists | Include hierarchy_framing with reporting instruction. |
| return_format section absent | Omit hierarchy_framing or reduce to definition-only reporting. |

---

## Open Design Questions

1. **Inline vs standalone rendering.** Should failure evidence be woven into execution steps (higher detection) or kept in a standalone section (cleaner structure, cross-agent consistency)? Both analyses noted the tradeoff; neither resolved it.

2. **Prompt placement.** Pre-flight failure criteria are most useful when encountered before execution instructions. Should the section render ABOVE execution_instructions? Placement is a rendering decision with behavioral consequences.

3. **Retry semantics.** The summarizer's "not resolved after retry" implies retry-before-abort logic. Is this a failure_criteria concern (retry annotation per evidence item) or an execution_instructions concern? Both analyses flagged this; both left it open.

4. **Schema-level abort strength.** Should definition authors control abort aggressiveness via a field (`abort_strength = "mandatory" | "recommended"`)? This directly resolves the obligation-vs-permission tension at the data level rather than the rendering level.

5. **Evidence severity levels.** Some evidence is binary ("input could not be read"). Some involves judgment ("requirements do not specify"). Should severity be annotated, allowing the renderer to frame binary evidence as mandatory-abort and judgment evidence as strong-recommendation-abort?

---

## Key Design Decisions

**DECIDED (high confidence, both converged):**
- Section preamble is mandatory and must explicitly reframe abort as correct behavior
- Failure criteria are disjunctive (any one criterion = halt) and this must be stated
- Evidence items within a criterion are disjunctive (any one signal = criterion met) and this must be stated
- Definition and evidence serve different roles (category vs detection) and the hierarchy matters for reporting
- Zero-criteria agents get no section, not an empty section
- Failure criteria are independent from success criteria — never frame as inverses

**OPEN (must test empirically):**
- Obligation vs permission abort stance — highest-impact variable, potentially conditional on agent type
- Unified vs temporally-split evidence rendering — start unified, split if testing shows timing-blind behavior
- Section header naming — "Abort Conditions" (tight, neutral) vs "Conditions That Prevent Success" (strongest externalization)
- Inline rendering within execution steps vs standalone section
