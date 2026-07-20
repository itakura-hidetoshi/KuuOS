# CodeAI Version-Bound Repair Memory v0.1

## Purpose

CodeAI Version-Bound Repair Memory v0.1 is authoritative roadmap step 8.

It consumes:

- the exact Typed Error Classification and receipt;
- a sealed packet of externally executed, independently verified repair evidence;
- an exact version-bound lookup request;
- a deny-by-default memory policy.

It produces a sealed read-only repair-memory snapshot. The snapshot may expose an exact historical repair hint, but it never executes repair, mutates a repository, creates Git effects, or grants authority.

## Authoritative roadmap

```text
1. Baseline and Replay Evaluation
2. Selective Repository Semantic Context Pack
3. Typed Structured Edit IR
4. Candidate Static Admissibility Preflight
5. Typed Error Classification
6. Independent Test Strengthening
7. Evidence-Weighted Selection and Abstention
8. Version-Bound Repair Memory
9. Maintainability Trajectory Gate
```

## Exact version binding

Every reusable memory entry is bound to all of:

1. repository full name;
2. source commit SHA;
3. repository snapshot digest;
4. source candidate digest;
5. typed error digest;
6. error fingerprint;
7. classification schema version;
8. toolchain digest;
9. dependency-manifest digest;
10. repair-policy digest.

All fields must match exactly. A different commit, candidate, error, schema, toolchain, dependency manifest, or repair policy is excluded.

```text
same error fingerprint + different toolchain != transferable repair hint
same candidate + different dependency manifest != transferable repair hint
historically effective + different source commit != transferable repair hint
```

## Repair evidence packet

Each repair record preserves:

- exact candidate and typed-error identity;
- error family, stage, fingerprint, and repair route;
- repair action digest;
- outcome: `verified_effective`, `verified_ineffective`, or `inconclusive`;
- independent verification evidence digest;
- toolchain, dependency-manifest, and repair-policy digests;
- producer and verifier identities;
- completion, isolation, live-repository, and Git-effect flags.

The repair producer, independent verifier, and memory curator must be distinct.

External repair execution is historical evidence. The memory kernel itself performs no repair.

## Matching and exclusion

The reference policy permits only `verified_effective` entries as hints.

Entries are excluded when:

- any version-binding field differs;
- the repair outcome is not allowed;
- typed-error correspondence is incomplete;
- evidence is stale, malformed, unsealed, non-independent, non-isolated, or associated with live-repository or Git effects.

The output recommendation is one of:

- `exact_version_bound_repair_hint_available`;
- `no_exact_version_bound_repair_hint`.

No hint is not rejection. A hint is not repair authority.

## Reference fixture

The reference fixture creates four memory entries:

- three current typed-error repair records;
- one duplicate historical record for the same typed error under a legacy toolchain.

The exact query matches one current `verified_effective` entry. The other three are excluded due to candidate/error binding, outcome, or legacy toolchain mismatch.

```text
memory_entry_count = 4
matched_entry_count = 1
excluded_entry_count = 3
recommendation = exact_version_bound_repair_hint_available
```

## Fixed boundaries

```text
historical repair outcome != probability
verified effective history != future success proof
memory hint != correctness proof
memory hint != repair authority
memory hint != verification authority
memory hint != execution authority
memory hint != Git authority
memory lookup != repair execution
memory lookup != repository mutation
memory lookup != Git effect
version mismatch != transferable knowledge
```

## Formal surface

The generic Lean layer proves:

- source-commit mismatch blocks exact transfer;
- toolchain mismatch blocks exact transfer;
- dependency-manifest mismatch blocks exact transfer;
- repair-policy mismatch blocks exact transfer;
- candidate or typed-error mismatch blocks exact transfer;
- every emitted hint is exactly version-bound and preserved in the sealed entry set;
- historical outcomes are neither probabilities nor future-success or correctness proofs;
- repair, verification, execution, and Git authority remain separate;
- lookup is read-only and creates no repair, repository, or Git effect.

## Fail-closed conditions

The surface blocks on, among other cases:

- malformed or unsealed inputs;
- request, policy, classification, receipt, packet, record, or entry digest mismatch;
- classification or receipt correspondence mismatch;
- unknown typed-error digest;
- candidate, sequence, candidate digest, fingerprint, family, stage, or route mismatch;
- stale or future request or repair evidence;
- producer, verifier, or curator identity collision;
- incomplete, non-independent, or non-isolated repair evidence;
- live-repository mutation or Git effects;
- disabled exact binding or evidence guarantees;
- enabled repair, repository, execution, or Git authority;
- memory-entry or matched-entry budget excess.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_version_bound_repair_memory_v0_1.py` |
| Checks | `runtime/kuuos_codeai_version_bound_repair_memory_checks_v0_1.py` |
| Schema | `runtime/kuuos_codeai_version_bound_repair_memory_schema_v0_1.py` |
| Fixture builder | `scripts/build_codeai_version_bound_repair_memory_fixture_v0_1.py` |
| Checker | `scripts/check_codeai_version_bound_repair_memory_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_version_bound_repair_memory_v0_1.py` |
| Example | `examples/codeai_version_bound_repair_memory_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_version_bound_repair_memory_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/VersionBoundRepairMemoryV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIVersionBoundRepairMemoryV0_1.lean` |
| Workflow | `.github/workflows/codeai-version-bound-repair-memory-v0-1.yml` |

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic reconstruction;
- dedicated exact-binding, no-hint, and fail-closed tests;
- Typed Error Classification and predecessor regressions;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.
