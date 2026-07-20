# CodeAI Maintainability Trajectory Gate v0.1

## Purpose

CodeAI Maintainability Trajectory Gate v0.1 is authoritative roadmap step 9.

It consumes:

- the exact Evidence-Weighted Selection and Abstention decision and receipt;
- the exact Version-Bound Repair Memory snapshot and receipt;
- a sealed packet of independently assessed maintainability measurements from the isolated selected candidate;
- an exact gate request;
- a deny-by-default trajectory policy.

It produces a sealed `admitted` or `held` gate decision. The gate does not run tests, repair a candidate, mutate a repository, create Git effects, or grant downstream authority.

## Completed roadmap

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

## Exact lineage

The gate is bound to all of:

1. selection decision digest;
2. selection receipt digest;
3. memory snapshot digest;
4. memory receipt digest;
5. trajectory evidence packet digest;
6. repository full name;
7. source commit SHA;
8. source repository snapshot digest;
9. selected candidate ID;
10. selected candidate digest.

The memory query must be bound to the same repository, commit, snapshot, and selected candidate digest. A matching historical repair hint is optional and never changes the trajectory thresholds.

## Maintainability axes

All six axes are lower-is-better bounded measurements:

- `structural_complexity`;
- `dependency_surface`;
- `duplication`;
- `test_burden`;
- `proof_burden`;
- `repair_recurrence`.

Each record preserves the baseline value, isolated-candidate value, signed observed delta, measurement artifact digest, assessor and reviewer identities, and isolation/source/effect flags.

The reference fixture is:

| Axis | Baseline | Candidate | Positive regression allowance |
|---|---:|---:|---:|
| Structural complexity | 120 | 118 | 0 |
| Dependency surface | 40 | 41 | 1 |
| Duplication | 15 | 12 | 0 |
| Test burden | 80 | 82 | 3 |
| Proof burden | 12 | 12 | 0 |
| Repair recurrence | 9 | 7 | 0 |

Therefore:

```text
axis_count = 6
improved_axis_count = 3
total_positive_regression = 3
maximum_total_regression = 4
gate_decision = admitted
```

## Gate rules

The selected candidate is admitted only when:

- the upstream decision actually selected the same candidate;
- selection, memory, evidence, request, and policy lineage match exactly;
- all six axes are present exactly once in canonical order;
- assessor, reviewer, and candidate producer are distinct;
- measurements are completed, external, independent, isolated, source-corresponding, and read-only;
- every positive axis regression is within its explicit allowance;
- total positive regression is within the aggregate allowance;
- the required number of axes strictly improve.

Otherwise valid evidence yields `held`. A hold is a bounded deferral, not rejection.

Malformed, stale, unsealed, incomplete, non-independent, non-isolated, authority-claiming, mutation-bearing, or Git-effect-bearing inputs fail closed with `blocked`.

## Memory boundary

```text
memory hint != threshold waiver
historical repair outcome != probability
historical repair outcome != future success proof
no memory hint != rejection
```

The gate records whether an exact version-bound hint exists, but admissibility is definitionally independent of hint presence.

## Fixed boundaries

```text
bounded maintainability measurement != future maintainability proof
maintainability admission != correctness proof
maintainability admission != probability
maintainability hold != rejection
gate decision != selection authority
gate decision != verification authority
gate decision != repair authority
gate decision != execution authority
gate decision != Git authority
gate evaluation != test execution
gate evaluation != repository mutation
gate evaluation != Git effect
```

## Formal surface

The generic Lean layer defines axis observations, positive regression, per-axis bounds, aggregate regression, improvement counts, and gate admissibility.

It proves:

- every admitted observation satisfies its per-axis allowance;
- every admitted trajectory satisfies the aggregate regression bound;
- every admitted trajectory satisfies the improvement floor;
- a memory hint cannot override a failed axis bound;
- admissibility is independent of memory-hint presence;
- hold is not rejection;
- downstream authority and effect boundaries remain false.

The actual specialization proves the six-axis reference trajectory has total regression `3`, exactly `3` improved axes, satisfies the step-9 policy, and preserves all authority boundaries.

## Surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_codeai_maintainability_trajectory_gate_v0_1.py` |
| Checks | `runtime/kuuos_codeai_maintainability_trajectory_gate_checks_v0_1.py` |
| Schema | `runtime/kuuos_codeai_maintainability_trajectory_gate_schema_v0_1.py` |
| Fixture builder | `scripts/build_codeai_maintainability_trajectory_gate_fixture_v0_1.py` |
| Checker | `scripts/check_codeai_maintainability_trajectory_gate_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_maintainability_trajectory_gate_v0_1.py` |
| Example | `examples/codeai_maintainability_trajectory_gate_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_maintainability_trajectory_gate_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/MaintainabilityTrajectoryGateV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIMaintainabilityTrajectoryGateV0_1.lean` |
| Workflow | `.github/workflows/codeai-maintainability-trajectory-gate-v0-1.yml` |

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic fixture reconstruction;
- 81 dedicated admit/hold/exact-lineage/fail-closed tests;
- Version-Bound Repair Memory and predecessor regressions;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.
