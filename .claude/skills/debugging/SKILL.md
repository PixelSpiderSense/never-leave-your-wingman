---
name: debugging
description: Hypothesis-driven debugging with disciplined instrumentation and cleanup. Use for any non-trivial bug — anything beyond an obvious one-line fix — especially when the cause is unknown or a first fix attempt has already failed.
---

# Debugging

Debug by testing hypotheses against evidence, not by pattern-matching to the first
plausible cause. After two failed fixes, revisit the hypothesis; failure does not prove that the hypothesis is false.

## The loop

1. Reproduce the reported failure before claiming a fix. If it cannot be triggered safely or reliably, collect existing evidence, record the exact unknown and propose the smallest observation that would discriminate between causes. Label the outcome investigation-only until the original failure or an agreed equivalent can be verified.
2. **Hypothesize explicitly.** Write down numbered candidate causes (H1, H2, …) with what
   evidence would confirm or kill each. Rank by likelihood.
   - When the failure spans components (services, layers, processes), correlate before
     hypothesizing: line up each component's logs around the failure moment (timestamps,
     request/trace ids) and map the cascade — which part failed *first*, and what were
     merely its downstream symptoms. Hypothesize about the first domino, not the loudest
     symptom.
3. **Instrument surgically.** Add the minimum logging/breakpoints needed to discriminate
   between hypotheses:
   - Tag every temporary log line with its hypothesis (`[H2] cache size after evict: …`)
     so output reads as evidence for/against something specific.
   - Wrap every temporary addition in paired markers (e.g. `// DEBUG-START` /
     `// DEBUG-END`) so cleanup is a mechanical search-and-delete, not archaeology.
   - Send debug output to a scratch log file, not stdout — don't contaminate program
     output or test snapshots.
4. **Run the reproduction, read the evidence.** Eliminate hypotheses the data kills. If
   all die, the list was wrong — widen it; don't force the survivor.
5. **Trace causation up the stack.** When you find *where* it breaks, keep going to where
   the bad value is *born*. Fix at the origin, not at the crash site — patching the
   symptom leaves every other consumer of the bad value broken.
6. Re-run the reproduction and relevant surrounding checks. Remove temporary instrumentation, inspect the resulting diff, then re-run the affected checks on the final artifact. Preserve a regression test when practical; do not remove it merely to leave only production-code changes.

## Exit checklist

A debugging session isn't over until all four are true — state them explicitly when
reporting done:

- **Reproduced** — the failure was triggered on demand, not assumed from the report.
- **Root-caused** — the origin of the bad state is identified and cited (file:line), not
  just the crash site.
- **Validated** — the fix was re-verified against the original reproduction and the
  surrounding tests.
- **Prevented** — something now guards against a repeat: a regression test, or a proposed
  lesson (per `AGENTS.md`'s memory-confirmation rule) when the guard can't be mechanical.

## Rules of thumb

- After two failed fixes, revisit the hypothesis; failure does not prove that the hypothesis is false. Record what each experiment established. Three failed fixes trigger the pipeline's evidence-based reassessment; they do not prove an architectural defect.
- **Invariant breakpoints beat stepping.** Instead of walking the code line by line, break
  conditionally on the invariant being violated ("break when total < 0") — let the
  program find the moment for you.
- **One variable at a time.** A run that changed two things proves nothing about either.
- When the bug involves *history* ("this used to work"), switch to the
  `reverse-engineering` skill's archaeology workflow — bisect and diff evidence beats
  fresh instrumentation.

Temporary diagnostics record only necessary, non-sensitive values. Prefer identifiers, counts and state transitions over payload dumps. Use a task-owned scratch path and delete only instrumentation and scratch files created by this task. Never log credentials or private source payloads.

For state-dependent bugs, write a state witness before changing code: the real producer of each relevant state value; the event and ordering that reach it; the observed failure; the expected result after the fix; and one existing valid behavior that must remain unchanged. Cite implementation paths for reachability. A fixture made from arbitrary flags is insufficient unless the production path can produce that combination.
