# Galdr — Context Refresh Protocol

## STOP. Read this before writing any code.

You have context from a compaction summary or from earlier in this session. You feel like you understand this project well enough to start working. **You are almost certainly wrong.**

After compaction, you have a summary — not understanding. The summary preserves conclusions but loses reasoning, constraints, and the specific shapes of things. You will produce output that looks right, compiles, and silently violates the project's architecture because the summary told you WHAT but not HOW or WHY NOT.

**This has happened before.** Previous sessions in this project have produced output that compiled, passed review, and implemented the wrong architecture — work that had to be thrown away.

None of them felt uncertain while doing it.

**The test:** Can you state three specific constraints of this project that diverge from how you'd normally write this code? Not "I should be careful" — actual constraints, with reasons. If you can't, you don't have enough context to write code. Orient via the CONTEXT_MAP `@import`ed below before proceeding — start with its orientation gate.

---
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- EVERYTHING ABOVE THIS LINE IS STANDARDIZED — DO NOT MODIFY            -->
<!-- (except the failure examples, which must be real)                      -->
<!-- EVERYTHING BELOW THIS LINE IS PROJECT-SPECIFIC                        -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
---

## Project Instructions

- **Write in small increments so feedback lands on small surfaces.** Feedback arrives on every file you write, automatically. A file at a time means each response points at one thing; a batch of files means untangling which change caused what.
- **Reshape the schema instead of complicating the engine.** The output schemas (agent-output-content/structure/display) are tail-end — no downstream cascade beyond galdr — so changing them costs only a mechanical regen (verdandi YAML → draupnir → gates → galdr models). When engine code gets complex to handle an awkward data format, reshape the schema rather than building detection logic around it.
- **Verify the output changed before decomposing.** Get the logic working and confirm the actual output moved, THEN decompose. Splitting functions to satisfy a complexity band before you've seen the logic work is optimizing blind.
- **General docs must stay valid for two weeks.** Keep concepts, principles, and data-flow descriptions in general docs. Keep function names, field-name examples, "what's built" inventories, and implementation status OUT of them — those are read live from the code or belong in volatile docs (`review/`) expected to change.

---

## How you orient — first time or recovery (same thing)

Orienting and recovering are one act: read the project's main documents, **routed by the
`CONTEXT_MAP` auto-included below** — start with its **orientation gate**, which *is* the
recovery-source list. If already verifiably oriented you needn't re-read everything; the map
always tells you where things live.

---

@CONTEXT_MAP.md
