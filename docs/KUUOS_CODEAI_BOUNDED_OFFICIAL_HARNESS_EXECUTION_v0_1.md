# CodeAI Bounded Official Harness Execution v0.1

## Purpose

This stage follows **Gold-Patch Environment Smoke Validation v0.1**. The predecessor established that the exact frozen SWE-bench Verified environment can reproduce one evaluator-only gold outcome. This stage exercises the official non-`gold` prediction-file path with one frozen, bounded, deliberately non-correctness-claiming prediction.

The disposition is either:

- `bounded_official_harness_execution_admitted`;
- `bounded_official_harness_execution_held`.

Admission means that the pinned official harness consumed the exact frozen prediction, applied its patch, completed the evaluation, and produced observable report and log evidence. Admission does **not** require `resolved = true`; an unresolved report is a valid engineering observation rather than a protocol failure.

## Exact lineage

- controller repository: `itakura-hidetoshi/KuuOS`;
- controller source commit: `51255adf60e78cba5569993a1164c6ba830f252f`;
- predecessor profile: `CodeAI Gold-Patch Environment Smoke Validation v0.1`;
- predecessor manifest digest: `efdb8c93cdfd9976977cf30181c985898c80184902e1bbae95ca15d54fea7d66`;
- predecessor smoke pack: `ebe734d57d827eb1602d1b5d489c650d2dc355d617ff5cac9c0f08363509c0b1`;
- predecessor smoke receipt: `f9e1756bbd2e05a494088ff68732764647099d901e28da14553d0e13edec0223`;
- completed predecessor artifact digest: `bf820bfff2f3a17e528b63777f5f30803b821bed67f7aa338116ef333a8d3b3d`.

The stage is developed on the fixed head of Draft PR #1338 while normalization PR #1337 is still pending. PR #1338 exact-head workflow run `29887932347` and evidence artifact `8517212458` are completed and content-addressed; queued or in-progress runs are never treated as success evidence.

## Frozen execution contract

```text
dataset = princeton-nlp/SWE-bench_Verified
revision = c104f840cc67f8b6eec6f759ebc8b2693d585d4a
artifact sha256 = a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd
harness = swe-bench/SWE-bench
harness commit = f7bbbb2ccdf479001d6467c9e34af59e44a840f9
instance = sympy__sympy-20590
base commit = cffd4e0f86fefd4802349a9f9b19ed70934ea354
sample count = 1
maximum workers = 1
timeout = 1800 seconds
cache level = none
```

## Non-gold prediction

The committed prediction uses the official three-field JSONL shape:

```text
instance_id
model_name_or_path
model_patch
```

The patch adds one harmless documentation line to `sympy/core/_print_helpers.py`. It does not add `__slots__`, modify tests, inspect the gold patch, or claim to solve the issue. Its purpose is to verify that a non-empty prediction can pass through the exact patch-application and evaluation path.

The patch source is deterministic and content-addressed. Gold material remains unavailable to candidate generation, prompt selection, repair memory, routing, tuning, and model selection.

## Observable evidence

The external job requires:

- the exact frozen dataset hash;
- the exact harness commit;
- Docker availability;
- one exact prediction JSONL line;
- successful patch application;
- completed test execution;
- non-empty `report.json`;
- non-empty `test_output.txt`;
- non-empty `run_instance.log`;
- content digests for all three evidence files.

The report's `resolved` field is recorded but is not an admission predicate. This prevents the infrastructure contract from being silently weakened into a benchmark-correctness claim.

## BLOCK versus HOLD

Structural BLOCK includes malformed or extra fields, invalid digests, request/plan/observation or run-ID binding mismatch, stale evidence, predecessor-manifest mismatch, unsafe diff paths, source-digest mismatch, and prediction-file digest mismatch.

Valid HOLD includes missing predecessor admission, unfrozen sample or prediction, gold-derived prediction, patch-application failure, incomplete evaluation, missing report or logs, kernel-side harness execution, gold exposure, repository mutation, Git authority, and correctness overclaim.

## Reference result

- decision: `bounded_official_harness_execution_admitted`;
- reference resolved outcome: `false`;
- execution pack: `3f5e691391b67e0e56d39d6ed241989d50a0a68cbc8eb901d9371ae6e3da4726`;
- receipt: `774e1a3835020c4d25b7f6eec9834958746ed4270a0b62b7d57654f9e7d86cff`;
- prediction digest: `9a2aeff25ca565214ecbae781f20df4c23eea20db72b135702aa56d5de238050`.

## Formal kernel

The Lean surface defines `Binding`, `ExecutionPlan`, `PredictionEvidence`, `ExecutionObservation`, `ExecutionEvidence`, `ExactBinding`, `PlanBounded`, `PredictionFrozen`, `ObservationComplete`, `GoldIsolationPreserved`, `BoundaryPreserved`, and `ExecutionAdmitted`.

It proves that missing or unapplied patches, incomplete evaluation, gold exposure, kernel-side harness execution, and repository mutation forbid admission. It also proves the reference unresolved execution is admitted, making the distinction between protocol completion and benchmark resolution explicit.

## Fixed boundaries

```text
patch application != issue resolution
evaluation completion != correctness
resolved false != protocol failure
resolved true != population generalization
official harness execution != future harness authority
external Docker execution != kernel execution authority
prediction artifact != gold patch
report observation != repository mutation
execution receipt != Git authority
```

## Validation

The dedicated workflow performs Python compilation, deterministic fixture and manifest checks, 35 focused tests, predecessor regressions, strict dedicated Lean compilation, strict aggregate `KuuOSFormal` compilation, exact dataset verification, exact harness checkout, prediction JSONL validation, Docker execution, report/log verification, and evidence artifact upload.
