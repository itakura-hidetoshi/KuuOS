# Public Proof Root Restoration Implementation Plan

> Execute inline using superpowers:executing-plans; this is the user's explicitly authorized repair.

**Goal:** Undo blanket unpublication of retained Lean proofs while keeping independent Kuu free of Gray prerequisites.
**Architecture:** Separate package publication/build coverage from mathematical dependency authority; reuse original proofs and classify transitive dependencies.
**Tech Stack:** Pinned Lean 4.30.0-rc2, committed mathlib manifest, Lake TOML, Python unittest, GitHub Actions.
**Spec:** docs/superpowers/specs/2026-10-17-public-proof-root-restoration-design.md

## Global constraints

Preserve legacy/v5.291 byte-for-byte; no sorry/admit/new axioms, no pin upgrades, no merges of #2339/#1558, no blanket KUOS-prefix exclusion.

## Review focus

Missing or duplicate roots; transitive Gray leakage; restored wrapper importing a changed aggregate; standard builds omitting retained proofs; stale CI routing and authority documentation.

## Tasks

- [ ] Reproduce missing-root regression on exact main-derived HEAD; inventory roots and transitive imports, including aggregate modules.
- [ ] Restore Lake publication and build reachability; add dependency-specific boundary and coverage tests; keep original theorem sources intact.
- [ ] Correct CI consumers/checks and live README/ROADMAP/AGENTS without altering historical documents.
- [ ] Run regression tests, actual pinned Lean restored-root builds, independent-core boundary checks, snapshot integrity checks, and exact-head CI; review full diff and integrate only on verified success.
