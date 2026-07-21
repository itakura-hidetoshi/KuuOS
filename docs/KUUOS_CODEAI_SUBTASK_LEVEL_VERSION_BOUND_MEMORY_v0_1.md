# CodeAI Subtask-Level Version-Bound Memory v0.1

## Purpose

This additive stage upgrades repository memory from coarse task-level recall to **functional subtask-level recall** while retaining exact repository-version, dependency-slice, toolchain, environment, temporal-corpus, context-pack, and verifier-ensemble bindings.

The stage is read-only. It retrieves a bounded historical hint; it does not inspect or mutate a live repository, execute a repair, select or reject a candidate, authorize a successor stage, or prove correctness.

## Research basis

The design follows four recent results:

1. **Structurally Aligned Subtask-Level Memory for Software Engineering Agents** (ICML 2026; arXiv:2602.21611) reports that storage, retrieval, and update should align with functional decomposition rather than whole-task similarity.
2. **Beyond Semantic Organization: Memory as Execution State Management for Long-Horizon Agents** (arXiv:2606.06090) treats memory as validated execution-state reconstruction and isolates invalid branches.
3. **State-Adaptive Memory for Long-Horizon Reasoning Agent** (arXiv:2605.24468) keeps compact state cues while preserving raw trajectory evidence for intent-driven recall.
4. **Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents** (arXiv:2607.08716) identifies behavioral state decay and supports selective, state-grounded intervention rather than always-on memory injection.

KuuOS specializes these findings into a fail-closed software-engineering memory contract: a memory is reusable only for the exact current subtask and exact versioned execution context.

## Functional decomposition

The required subtask vocabulary is fixed to:

- `localize`
- `diagnose`
- `edit`
- `verify`

A corpus is invalid unless all four kinds are represented. Retrieval is performed against the current subtask contract, not against whole-issue surface similarity.

## Exact binding

Every request and memory entry binds:

- repository full name;
- exact source commit SHA;
- source-tree digest;
- temporal holdout corpus digest;
- intent-aligned dataflow context-pack digest;
- independent verifier-ensemble digest;
- subtask kind;
- subtask-contract digest;
- predecessor-output digest;
- dependency-slice digest;
- toolchain digest;
- environment digest;
- memory-policy digest.

Any mismatch excludes the entry. A similar issue description, error fingerprint, or repair narrative cannot override these bindings.

## Holdout and lifecycle protection

An entry is ineligible when it is:

- derived from temporal holdout labels;
- superseded;
- stale or future-dated;
- not independently verified useful;
- bound to another subtask, dependency slice, repository version, toolchain, environment, or policy;
- carrying any mutation, selection, repair, authority, correctness, or future-success claim.

This prevents evaluation leakage and stale-memory transfer.

## Reference corpus

The deterministic reference corpus contains 9 entries and covers all four functional subtasks.

The active query is for the `verify` subtask at exact base `2e3801430959946c1d2ecc784cf9e37dab139632`.

- corpus entries: 9
- matched entries: 1
- excluded entries: 8
- matched entry: `memory-verify-current-001`
- recommendation: `exact_subtask_version_bound_memory_available`

Excluded paths demonstrate subtask mismatch, stale commit/tree, dependency mismatch, holdout derivation, supersession, and inconclusive outcome.

## Fixed boundaries

```text
subtask memory != whole-task semantic similarity
historical usefulness != probability
historical usefulness != future success proof
memory hint != correctness proof
memory hint != candidate selection
memory hint != candidate rejection
memory hint != repair execution
memory hint != repository mutation
memory hint != execution authority
memory hint != Git authority
holdout-derived memory != reusable memory
version mismatch != transferable knowledge
dependency mismatch != transferable knowledge
```

## Formal surface

The generic Lean kernel defines:

- `SubtaskKind`
- `MemoryOutcome`
- exact `Binding`
- `MemoryEntry`
- `BoundaryPreserved`
- `Eligible`

It proves that eligibility entails exact binding, subtask alignment, dependency alignment, holdout exclusion, non-supersession, and authority/effect boundary preservation. Separate generic theorems show that repository-version, subtask, dependency, or holdout mismatch forbids transfer.

The actual specialization proves one exact current `verify` entry is eligible and stale, wrong-subtask, and holdout-derived entries are not.

## Surfaces

| Surface | Path |
|---|---|
| Schema | `runtime/kuuos_codeai_subtask_level_version_bound_memory_schema_v0_1.py` |
| Checks | `runtime/kuuos_codeai_subtask_level_version_bound_memory_checks_v0_1.py` |
| Runtime | `runtime/kuuos_codeai_subtask_level_version_bound_memory_v0_1.py` |
| Fixture | `scripts/build_codeai_subtask_level_version_bound_memory_fixture_v0_1.py` |
| Projection | `scripts/project_codeai_subtask_level_version_bound_memory_fixture_v0_1.py` |
| Checker | `scripts/check_codeai_subtask_level_version_bound_memory_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_subtask_level_version_bound_memory_v0_1.py` |
| Example | `examples/codeai_subtask_level_version_bound_memory_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_subtask_level_version_bound_memory_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/SubtaskLevelVersionBoundMemoryV0_1.lean` |
| Formal root | `formal/KuuOSCodeAISubtaskLevelVersionBoundMemoryV0_1.lean` |
| Workflow | `.github/workflows/codeai-subtask-level-version-bound-memory-v0-1.yml` |
