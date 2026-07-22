# CodeAI Gold-Patch Environment Smoke Validation v0.1

## Purpose

This additive stage follows **CodeAI External Corpus Acquisition and Freeze Receipt v0.1**.

It preregisters one evaluator-only gold-patch smoke run, consumes completed official SWE-bench harness evidence, and emits either:

- `gold_patch_environment_smoke_admitted`;
- `gold_patch_environment_smoke_held`.

Admission means only that the pinned harness and one pinned Verified instance reproduced its gold outcome in Docker with observable report and log artifacts. It is not candidate correctness, model performance, benchmark-wide validity, execution authority for another run, repository mutation authority, or Git authority.

## Current lineage

The stage is developed on the fixed #1336 merge head while normalization PR #1337 delivers that predecessor to `main`.

- controller repository: `itakura-hidetoshi/KuuOS`
- controller source commit: `c16c2e33aba95e93d352d6b790491f3b57300c92`
- predecessor manifest digest: `561be27194532088736124afa7c11542bc72dd00f724f3a422be429892c08f2a`
- predecessor freeze pack: `f0de4f9fc1e5c7348ced5a6272d37d7b289d3dbbf2df086496f358a601351a6f`
- predecessor freeze receipt: `31575449c7bbe77179e744563e7054eeeae5f037dd5673d5e1220901eeefe16b`

The pull request targets `main` directly but remains Draft until #1337 is integrated and the changed-base CI is completed.

## Preregistered smoke instance

- dataset: `princeton-nlp/SWE-bench_Verified`
- dataset revision: `c104f840cc67f8b6eec6f759ebc8b2693d585d4a`
- dataset artifact SHA-256: `a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd`
- harness repository: `swe-bench/SWE-bench`
- harness commit: `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`
- instance: `sympy__sympy-20590`
- predictions path: `gold`
- workers: `1`
- per-instance timeout: `1800` seconds
- cache level: `none`

The official SWE-bench quickstart uses `--predictions_path gold` with `sympy__sympy-20590` to check that the evaluation environment is configured correctly. This stage additionally pins the Verified corpus revision and extracts the single evaluator row from that exact Parquet artifact before execution.

## Evaluator-only isolation

The workflow may read the restricted `patch`, `test_patch`, `FAIL_TO_PASS`, and `PASS_TO_PASS` fields only inside the external evaluator job.

The gold patch must remain unavailable to:

- CodeAI candidate generation;
- provider prompts;
- repair memory;
- specialist routing;
- threshold tuning;
- model selection;
- solver-visible artifacts.

The committed example contains digests and Boolean evidence only. It does not contain the gold patch.

## Execution separation

The runtime kernel does not invoke Docker or the harness. It validates already observed evidence:

```text
external_harness_execution_observed = true
harness_execution_performed_by_kernel = false
```

The dedicated GitHub Actions evaluator performs the actual smoke run and emits content digests for:

- `report.json`;
- `test_output.txt`;
- `run_instance.log`.

A missing image, container, patch application, completed evaluation, report, logs, or resolved outcome produces a hold.

## BLOCK and HOLD

Structural BLOCK includes malformed fields, digest mismatch, stale input, cross-input binding mismatch, predecessor mismatch, non-gold prediction mode, and request or policy authority expansion.

A structurally valid HOLD includes unresolved gold outcome, missing observable evidence, solver gold exposure, gold use by candidate generation or repair memory, kernel-side harness execution, repository mutation, Git authority, or correctness overclaim.

## Reference content addresses

- smoke pack: `ebe734d57d827eb1602d1b5d489c650d2dc355d617ff5cac9c0f08363509c0b1`
- receipt: `f9e1756bbd2e05a494088ff68732764647099d901e28da14553d0e13edec0223`

## Formal kernel

The Lean/mathlib layer defines:

- `Binding`;
- `SmokePlan`;
- `SmokeObservation`;
- `SmokeEvidence`;
- `ExactBinding`;
- `PlanPreregistered`;
- `ObservationVerified`;
- `GoldIsolationPreserved`;
- `BoundaryPreserved`;
- `SmokeAdmitted`.

It proves that an unresolved gold run, solver gold exposure, candidate-generation gold use, repair-memory gold use, kernel-side harness execution, controller-version mismatch, or repository mutation forbids admission.

## Fixed boundaries

```text
one gold instance resolved != benchmark-wide environment validity
gold patch applied != generated patch correctness
gold smoke admission != model evaluation result
external harness execution evidence != kernel execution authority
gold evaluator access != solver access
gold patch != repair memory
report digest != population generalization
completed smoke run != future harness authority
smoke receipt != repository mutation or Git authority
```

## Validation

The dedicated workflow performs:

- Python compilation;
- deterministic example and manifest reconstruction;
- 30 focused positive, tamper, stale, isolation, unresolved, and authority tests;
- predecessor freeze and benchmark-adapter regression tests;
- pinned corpus acquisition and SHA-256 verification;
- extraction of exactly one preregistered row;
- pinned SWE-bench harness checkout and installation;
- Docker gold evaluation with one worker;
- report, test-output, and instance-log verification;
- strict dedicated Lean compilation;
- strict aggregate `KuuOSFormal` compilation.

The next separately governed stage is **Bounded Official Harness Execution v0.1** for model-generated predictions on a frozen engineering smoke sample.
