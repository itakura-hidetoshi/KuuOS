# CodeAI / MemoryOS Lean repair memory implementation plan

Goal: preserve compiler successes, failures and unknown outcomes as immutable observations; retrieve scoped advice before proposals and avoid exact repeated failed candidates without granting proof authority.
Architecture: existing MemoryOS GitHub external pointer API plus a new append-only evidence journal; a separate CodeAI replay guard; an additive adapter around the existing fixed-Lean portfolio runner.
Tech stack: Python standard library, existing KuuOS MemoryOS API, read-only GitHub Actions.

Constraints: canonical main unchanged; no Lean proof edits; preserve #3522/#3530 and protected #1558; fixed Lean v4.30.0-rc2/mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6; GitHub writes only through MCP. No weights training claim. Memory cannot certify a theorem or merge a PR.

Design decision: use a separate draft PR based on the observed repair branch instead of mutating a concurrently active proof branch. Exact replay suppression requires identical repository, source HEAD/tree, target, toolchain, manifest, flags, dependency and candidate bytes. Incomplete or mismatched context is advisory only. A timeout is not a counterexample. Conflicting success/failure is retained as a conflict.

Tasks:
- [x] Write failing tests for schema, immutable append, exact binding, conflict, stage status and missing evidence.
- [x] Implement evidence ingestion + existing MemoryOS pointer validation/context compilation.
- [x] Implement CodeAI advice-before-generation + exact replay filter + after-run capture adapter.
- [x] Seed evidence from downloaded immutable GitHub workflow artifacts; preserve full diagnostics separately from inferred causes.
- [ ] Add Python-only CI, run tests, create draft PR by GitHub MCP, observe actual CI.

Local verification before publication: 40 tests passed, including nine genuine compiler observations (three successes and six failures). GitHub CI status is intentionally left pending until an actual run completes on the published commit.

Review focus: corrupted memory must not silently turn into an empty history; exact repeated source failure must not ban a tactic in other contexts; a green workflow must not imply a green candidate; omitted diagnostics must remain NO_DATA; memory content must never be executed or treated as instructions.
