---
type: moc
name: Agents — Map of Content
aliases: [agents-moc, Agents]
status: active
date: "2026-06-30"
tags: [moc, agents, index]
---

# 🤖 Agents — Map of Content

The agent roster of the Second Brain OS. Two peer models (Claude + Codex) operate the
five role agents. Up: [[second-brain-os|Home]].

## Peer personas
- [[claude-persona]] — orchestrator: plans, analyzes, writes, reviews, researches.
- [[codex-persona]] — implementer: codes, debugs, refactors, tests.

## Role agents (`05-Agents/*/definition.md`)

The peer labels below are usual preferences, not exclusive assignments. Claude and Codex are equal collaborators; select the peer for the concrete task while preserving the five roles.

- [[ceo/definition|CEO Agent]] — leadership / direction (peer: claude).
- [[coder/definition|Coder Agent]] — development / execution (peer: codex).
- [[reviewer/definition|Reviewer Agent]] — code review / QA (peer: claude).
- [[memory/definition|Memory Agent]] — operations / vault memory (peer: claude).
- [[scribe/definition|Scribe Agent]] — operations / writing (peer: claude).

## Protocols
- [[handoff-protocol]] — inbox/outbox handoff format between agents.
- [[agent-pipeline]] — named-stage workflow the agents run.
- [[harness-evals]] — records harness checks and their evidence limits. Pending cases remain pending, and a syntax check does not establish runtime behavior. Re-run applicable cases after approved harness changes.
