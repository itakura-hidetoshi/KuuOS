# CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1

## Purpose

This additive stage establishes the first external-general-benchmark boundary for
KuuOS CodeAI. It validates and seals a **SWE-bench Verified evaluation protocol**
and deterministically projects governed CodeAI patch candidates into the official
prediction shape:

```text
instance_id
model_name_or_path
model_patch
```

The stage is protocol-only. It does not download the benchmark, build Docker
images, execute the official harness, ingest benchmark outcomes, mutate a target
repository, perform Git effects, or claim that any prediction resolves an issue.

It emits one of two read-only dispositions:

- `external_benchmark_protocol_admitted`;
- `external_benchmark_protocol_held`.

Malformed, tampered, stale, or digest-inconsistent inputs are blocked before a
disposition is produced. Structurally valid inputs that violate benchmark,
sample-freezing, prediction-integrity, protected-path, budget, or authority
conditions produce a hold.

## External benchmark contract

The reference contract binds:

- benchmark: `swe-bench-verified`;
- dataset: `princeton-nlp/SWE-bench_Verified`;
- split: `test`;
- expected instance count: `500`;
- official harness repository: `swe-bench/SWE-bench`;
- pinned harness commit:
  `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`;
- harness entrypoint:
  `python -m swebench.harness.run_evaluation`;
- official prediction fields:
  `instance_id`, `model_name_or_path`, `model_patch`;
- containerized and pinned harness requirements;
- frozen corpus and sealed test-patch-path requirements.

The official SWE-bench harness applies submitted model patches in Docker
environments and grades them through repository tests. That external behavior is
not reimplemented or treated as already executed by this adapter.

The reference fixture contains a three-instance smoke **protocol fixture**. Its
corpus and instance-list digests demonstrate exact content-addressed binding;
they are not a downloaded or independently verified digest of the complete
500-instance public dataset. A real evaluation run must replace those fixture
digests with digests computed from the acquired, frozen external corpus.

## Run-plan freezing

A run plan binds:

- run identity;
- evaluation mode: smoke, pilot, or full;
- deterministic selection method;
- ordered instance contracts;
- sample count and selected-instance digest;
- `max_workers`, timeout, and cache level;
- whether selection was frozen before execution;
- holdout-label and gold-patch exposure;
- requested external effects.

Admission requires the selected sample to be fixed before any result is known.
Holdout labels and gold patches must remain unavailable to candidate generation,
threshold tuning, prompt selection, memory lookup, and candidate selection.

The adapter does not permit a run plan to request harness execution. Harness
execution belongs to a later separately authorized effect and evidence stage.

## Per-instance contracts

Every selected instance has a sealed contract containing:

- instance ID;
- base commit;
- problem-statement digest;
- test-patch digest;
- protected test paths;
- creation epoch;
- canonical instance-contract digest.

A prediction must bind the exact instance-contract digest.

The adapter independently derives changed paths from canonical Git diff headers
rather than trusting a model-supplied changed-path list. A mismatch is
structurally blocked.

Any overlap between derived prediction paths and sealed protected test paths
produces a hold. This prevents a benchmark prediction from being admitted merely
by overwriting or shadowing evaluation tests.

## Prediction integrity

Each prediction binds:

- instance ID;
- model or agent identity;
- nonempty unified-diff artifact;
- independently derived changed paths;
- exact instance contract;
- CodeAI candidate receipt;
- provider session;
- creation epoch;
- prediction digest.

The resulting official projection contains only:

```json
{
  "instance_id": "...",
  "model_name_or_path": "...",
  "model_patch": "..."
}
```

Internal CodeAI provenance remains in the sealed adapter pack and receipt rather
than being injected into the official prediction payload.

## Budget contract

The policy bounds:

- minimum and maximum sample count;
- bytes per patch;
- total patch bytes;
- changed paths per prediction;
- allowed evaluation modes;
- allowed harness cache levels;
- request freshness.

Budget compliance is a protocol predicate. It is not evidence that a task is
resolved, that the official harness will complete, or that the measured system
is cost-effective at larger scale.

## Reference specialization

The reference protocol fixes:

- KuuOS source commit:
  `f5bf17314041e0cdfefb5862990e6c1abea320d6`;
- official harness commit:
  `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`;
- evaluation mode: `smoke`;
- sample count: `3`;
- unique ordered predictions: `3`;
- holdout labels exposed: `false`;
- gold patches exposed: `false`;
- protected test path overlaps: `0`;
- harness execution requested or performed: `false`;
- benchmark result ingested: `false`;
- decision: `external_benchmark_protocol_admitted`.

Reference content addresses:

- official predictions:
  `6c120860918f9ff0cd8bf0bbf2f22210fbe66a6426551514be024a4159e2485e`;
- adapter pack:
  `134475fc54fc23d0bcb48973b9fcfd158da51fa6a95ea4eff083a500f7936107`;
- receipt:
  `55233619cdc23640818f305564ee08652e5f9817cb0260128256c4d3ddfd7b73`.

These digests cover the deterministic reference fixture only and make no claim
about benchmark resolution.

## Formal kernel

The Lean surface defines:

- `BenchmarkKind`;
- exact `Binding`;
- `BenchmarkContract`;
- `RunPlan`;
- `PredictionEvidence`;
- `AdapterEvidence`;
- `ContractExact`;
- `PlanFrozen`;
- `PredictionsAdmissible`;
- `BoundaryPreserved`;
- `AdapterAdmitted`.

Generic theorems extract exact binding, the 500-instance Verified contract,
frozen selection, hidden holdout labels, protected-test-path non-overlap, and
authority boundaries from admission.

Separate theorems prove that:

- controller-version mismatch;
- holdout-label exposure;
- protected-test-path overlap;
- harness execution inside the protocol stage

forbid admission.

The actual three-instance reference specialization is admitted, while
holdout-leak, protected-path-overlap, and harness-execution variants are not.
No compound proposition is discharged with `native_decide`.

## Fixed boundaries

```text
external benchmark contract != downloaded corpus
fixture corpus digest != complete 500-instance corpus verification
protocol admission != benchmark execution authority
official prediction projection != patch correctness
prediction digest != semantic validity
patch applies != issue resolved
official harness completion != universal correctness
resolved instance != maintainability proof
sample success != population generalization
holdout label != candidate-generation input
gold patch != repair memory
protected test path != model-editable path
benchmark result != repository mutation authority
benchmark result != Git authority
benchmark result != deployment authority
```

## Implementation map

- Runtime schema:
  `runtime/kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1.py`
- Runtime checks:
  `runtime/kuuos_codeai_external_general_benchmark_swebench_verified_adapter_checks_v0_1.py`
- Runtime adapter:
  `runtime/kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1.py`
- Fixture builder:
  `scripts/build_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1.py`
- Projection:
  `scripts/project_codeai_external_general_benchmark_swebench_verified_adapter_fixture_v0_1.py`
- Checker:
  `scripts/check_codeai_external_general_benchmark_swebench_verified_adapter_v0_1.py`
- Tests:
  `tests/test_kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1.py`
- Example:
  `examples/codeai_external_general_benchmark_swebench_verified_adapter_v0_1.json`
- Manifest:
  `manifests/kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1.json`
- Lean kernel:
  `formal/KUOS/CodeAI/ExternalGeneralBenchmarkSWEBenchVerifiedAdapterV0_1.lean`
- Lean root:
  `formal/KuuOSCodeAIExternalGeneralBenchmarkSWEBenchVerifiedAdapterV0_1.lean`
- Workflow:
  `.github/workflows/codeai-external-general-benchmark-swebench-verified-adapter-v0-1.yml`

## Next evaluation stages

This protocol stage deliberately stops before external effects. The next
separately governed stages are:

1. exact SWE-bench Verified corpus acquisition and freeze receipt;
2. gold-patch environment smoke validation;
3. bounded official harness execution;
4. external result and process-evidence ingestion;
5. baseline-versus-CodeAI and ablation comparison;
6. temporal or live external-validity evaluation.
