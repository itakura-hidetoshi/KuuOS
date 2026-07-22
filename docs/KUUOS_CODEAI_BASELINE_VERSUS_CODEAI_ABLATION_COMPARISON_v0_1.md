# Baseline-versus-CodeAI and Ablation Comparison v0.1

## Purpose

This stage follows **CodeAI External Result and Process-Evidence Ingestion v0.1**. It binds the admitted aggregate ingestion receipt, preregisters a balanced baseline/CodeAI/ablation comparison contract, and grants only the authority needed to compare future aggregate observations under that contract.

The reference specialization admits the preregistration contract. It does **not** claim that a performance comparison has been completed.

## Current evaluation frontier

| Evaluation item | State |
|---|---|
| Reproducible evaluation environment | succeeded |
| Gold-patch resolution check | succeeded |
| Non-gold prediction path | succeeded |
| Submitted candidate solved the issue | failed (0/1) |
| CodeAI performance comparison | not yet performed |
| Baseline comparison | not yet performed |
| Ablation comparison | not yet performed |

The measured CodeAI predecessor remains:

```text
instance = sympy__sympy-20590
execution valid = true
resolved = false
FAIL_TO_PASS = 0 success / 1 failure
PASS_TO_PASS = 21 success / 0 failure
```

This single `0/1` observation is preserved as evidence. It is not expanded into a general performance claim.

## Exact predecessor

```text
main source commit = b842d6bd04aad4f202d41e400d7130c64f4d054f
predecessor compact manifest canonical digest = sha256:98fa9a5f87f3ee3cbfedda4303533e818d15a9211ea0f76c3ccec60c693241f0
predecessor ingestion pack = f1c2a5d24c4d1a54e2e539ca7fef7c409c10aae83b4f5815174674b7df8db9e6
predecessor receipt = 3e1711fa4aa26feb8a19feb8829f44ceb06a0e7a23f1bbf32c8db67615f3191f
```

The `3e45fc99...` digest from the prior stage is the canonical digest of the bounded-execution predecessor manifest consumed by #1340. The comparison stage instead binds the committed #1340 compact ingestion manifest; its canonical digest is `98fa9a5f87f3ee3cbfedda4303533e818d15a9211ea0f76c3ccec60c693241f0`.

## Preregistered cohorts

All cohorts use one frozen sample binding and one frozen holdout partition.

1. `baseline-deterministic-patch`
2. `codeai-full`
3. `ablation-no-repair-memory`
4. `ablation-no-specialist-routing`
5. `ablation-no-evidence-weighted-selection`

Each cohort has the same target sample count. Gold material, raw test names, raw logs, candidate-generation feedback, and repair-memory feedback are unavailable to every cohort.

The comparison pairs are fixed before additional observations:

```text
baseline-deterministic-patch vs codeai-full
codeai-full vs ablation-no-repair-memory
codeai-full vs ablation-no-specialist-routing
codeai-full vs ablation-no-evidence-weighted-selection
```

## Preregistered metrics

The primary metric is `resolved-rate`, with higher values preferred.

Secondary and guardrail metrics are:

- `fail-to-pass-success-rate`: higher is better;
- `pass-to-pass-preservation-rate`: higher is better;
- `execution-valid-rate`: higher is better;
- `error-rate`: lower is better.

Missing evidence produces `HOLD`. Execution failure is counted as unresolved rather than silently discarded. Directions and handling rules are sealed before future observations.

## Reference observation state

The admitted #1340 CodeAI aggregate is bound as one measured observation. Baseline and all three ablation observations remain `pending`.

Therefore the reference receipt states:

```text
preregistration completed = true
performance comparison completed = false
pending cohort count = 4
performance claimed = false
```

A request to enter `comparison-execution` while any required cohort remains pending is held for insufficient evidence.

## BLOCK and HOLD

Structural `BLOCK` includes malformed or extra fields, invalid seals, exact-binding mismatch, nested sample/holdout cross-binding, predecessor-manifest digest mismatch, and stale or future-dated material.

Semantically valid `HOLD` includes:

- predecessor admission or aggregate mismatch;
- missing cohort observation or required metric;
- unequal cohort target counts or unequal measured sample counts;
- unfrozen holdout;
- gold, raw-test-name, or raw-log leakage;
- candidate-generation or repair-memory feedback;
- incomplete metric values;
- insufficient evidence for execution;
- repository mutation, Git authority, correctness claim, or broader authority overreach.

## Limited authority

This stage grants `limited_aggregate_comparison_authority_granted = true`. That authority is limited to the sealed cohorts, metrics, sample binding, holdout partition, and aggregate observations.

It does not grant:

```text
raw gold access
raw test-name access
raw log access
candidate-generation feedback
repair-memory feedback
repository mutation authority
Git authority
correctness authority
performance-claim authority
```

## Content addresses

```text
sample binding = d3162c78a1552f22411b87c019271cfbc692ffa048a039067f4c83c65d42012c
holdout partition = b88c73c43b0a14c23cdd58269ccba3c5437ffba3651c0f3dc2ceb7aa7ebcf2e6
comparison contract = f99ae02bd48c51563060a7b0de6be53f9ea98278efe0e837ab73bdd77e4c7016
cohort registry = 527ff02e523e1d7b9a9f15280ba82032df94a04e08675bc4096a2c63cd42882f
metric registry = 462627a160ec8bf265b25cb2853421746b0bdfa84dc6e27d61710b5226bdb97c
observation registry = c0e63a57a297319d421031a7379c277802c7218fa05529a1976d3383291c3d6a
comparison pack = aee1ad7919af50124c79cb27b86fc8c6d9a54192237e963b62e1869d986fdf23
comparison receipt = 1629e68f87175bf0ce7393e652d58df6bd3611832db84995feb1566644fd2ce4
```

## Formal kernel

The Lean surface defines `Binding`, `ComparisonPlan`, `CohortRegistry`, `MetricRegistry`, `ObservationRegistry`, `ComparisonEvidence`, `ExactBinding`, `CohortsPreregistered`, `MetricsPreregistered`, `ObservationPreregistrationComplete`, `IsolationPreserved`, `BoundaryPreserved`, and `PreregistrationAdmitted`.

It proves that binding mismatch, cohort imbalance, missing primary metrics, gold visibility, raw test-name visibility, repository-mutation authority, and correctness claims forbid admission. The reference specialization is admitted while `performanceComparisonCompleted = false`.

## Fixed semantics

```text
preregistration admitted != performance comparison completed
one measured CodeAI case != CodeAI performance estimate
same metric names != same sample binding
aggregate observation != raw test evidence
missing evidence != zero performance
execution failure != omitted sample
limited comparison authority != repository or Git authority
```

## Next execution step

The next evidence-producing work is to run the frozen baseline and ablation cohorts, ingest aggregate-only observations under the exact receipt, verify balanced sample binding, and only then enter `comparison-execution`.
