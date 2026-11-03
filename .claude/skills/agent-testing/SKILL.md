---
name: agent-testing
description: Regression-testing agent behavior and building eval suites. Use when changing prompts, rules files, skills, or models and you need to know whether behavior regressed — or when standing up an eval harness for an agent workflow.
---

# Agent Testing

Agent behavior is nondeterministic; test it like a distribution, not like a function.

## Evaluation assets and oracles

Use versioned cases with inputs, allowed side effects, expected properties, an independent grader and a clear pass rule. A successful past run is a candidate fixture, not ground truth. Review and redact it before saving; record provenance and approval. Do not store credentials, raw private transcripts or hidden reasoning. Keep development cases separate from held-out cases used for acceptance.

## Coverage

Pairwise matrices help explore combinations, but do not replace explicit tests for security boundaries, ordering, state transitions and known higher-order interactions. Include should-trigger, should-not-trigger, malformed-input, missing-tool and permission-denied cases. For routing tests, leave the target skill in the available catalog on negative cases; otherwise the test cannot measure false activation. Record the full catalog and treat unrecognized responses as errors, not correct abstentions.

## Grader taxonomy (choose deliberately)

Mechanical first, judgment last:

1. **Exact / regex match** — cheapest, for outputs with a canonical form.
2. **Structural checks** — did it call the required tool, produce valid schema, touch
   only allowed files.
3. **Property checks** — latency, cost, output length within bounds.
4. **Semantic similarity** — meaning-level match when wording may vary.
5. **LLM-judge with a pinned rubric** — last resort; the rubric is versioned, and judge
   drift is itself a regression to test for.

## Compare behavior and report uncertainty

Compare the current and proposed skill on the same tasks, model settings, tools and initial state. Include a without-skill baseline when measuring added value. Choose repetitions and a practical effect threshold before observing results. Use a statistical method suitable for the metric and pairing; binary outcomes are not automatically a t-test problem. Report sample counts, variation, missing runs, costs and per-case regressions. Small samples can be inconclusive. Calculate incremental utility only for cases with both completed baseline and candidate runs. A missing baseline is unknown, not a failed baseline; disclose the paired denominator. A critical safety failure blocks acceptance even when the aggregate score improves.

An empty suite, missing required cases, failed grader, invalid output or inaccessible artifact is not PASS. Distinguish regression from infrastructure error. Baseline changes require a reviewed diff and the same memory or policy approval rules as the artifact they affect.

## Browser / E2E checks

- Detect an already-running dev server before assuming a URL — a harness that silently
  spawns a second server on a shifted port tests the wrong build.
- Run headed (visible browser) when a human is supervising the session; reserve headless
  for CI.

## Counterfactual debugging

When a regression appears, replay the recorded fixture varying one factor at a time
(model, prompt, rule file, tool availability) to isolate the cause — same
one-variable-at-a-time rule as the `debugging` skill.

## TDD for agent-assisted coding

For behavioral code changes, use a failing regression test when it meaningfully demonstrates
the defect, then verify the final artifact. Routine low-impact edits do not need tests that
merely mirror the implementation. Use independent checking for consequential boundaries;
record when only the maker's checks are available rather than implying independence.
