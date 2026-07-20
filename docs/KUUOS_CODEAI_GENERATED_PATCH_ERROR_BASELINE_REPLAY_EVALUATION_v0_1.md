# CodeAI Generated Patch Error Baseline Replay Evaluation v0.1

## Status

Additive, read-only, deterministic evaluation surface for normalized historical
CodeAI patch evidence.

This stage establishes the measurement layer required before changing retrieval,
editing, selection, repair, test generation, or memory policy. It does not generate
a patch, execute historical code, invoke a provider, run a verification command, or
grant any Git or successor authority.

```text
normalized historical CodeAI replay cases
+ exact case digests and repository lineage
+ sealed baseline request
+ bounded read-only evaluation policy
  -> exact dataset and request correspondence
  -> sequential evidence validation
  -> deterministic stage and failure metrics
  -> repeated-error and repair-efficiency metrics
  -> sealed evidence and receipt
  -> no historical code re-execution
  -> no provider or runner invocation
```

## Why the baseline comes first

Improving generated code without a fixed baseline risks optimizing anecdotal
failures while moving errors to another stage. The profile therefore measures the
current pipeline before adding the planned semantic context, typed edit,
admissibility, error-routing, test-strengthening, and repair-memory surfaces.

The baseline is designed around findings from repository-level code-generation and
repair literature:

- RepoCoder and related repository-level retrieval work motivate measuring errors
  separately from retrieval quality.
- Repoformer motivates selective context rather than assuming that more context is
  always better.
- Agentless motivates strong localization, repair, and validation stages before
  increasing agent complexity.
- CodeT and test-driven generation motivate execution evidence while preserving the
  distinction between test agreement and correctness.
- EvalPlus and automated-program-repair studies motivate stronger evaluation than a
  small visible test suite because test-passing patches can still overfit.
- self-debugging studies motivate bounded, normalized feedback rather than repeated
  forwarding of raw logs.
- long-horizon software-agent evaluations motivate tracking repair cost and repeated
  failure patterns, not only one-step pass rates.

This profile does not encode those papers as authority. It creates the metrics
needed to test whether later KuuOS changes actually improve the local CodeAI
pipeline.

## Replay case

A replay case is a content-addressed, normalized observation of one generated patch
trajectory. It records:

1. repository and source-commit identity;
2. candidate, patch, generation, application, execution, and verification digests;
3. provider and model identity;
4. structured-output, patch-application, parse, typecheck, targeted-test, and
   full-regression status;
5. independent-verification status;
6. bounded repair-cycle count and whether repair reached a verified patch;
7. provider-call and generated-output accounting;
8. normalized error fingerprints;
9. observation epoch;
10. one canonical case digest.

A replay case contains evidence summaries, not executable code or raw provider
output.

## Sequential evidence

When the policy requires sequential evidence, a later stage may be observed only
after every predecessor passed.

```text
structured output
  -> patch application
  -> parse
  -> typecheck
  -> targeted tests
  -> full regression
  -> independent verification
```

A failed or aborted predecessor requires every later stage to remain `not_run`.
A predecessor may pass while a later stage remains `not_run`; this is reported as
incomplete evidence rather than silently converted into success or failure.

## Dataset

The dataset binds:

- one dataset identifier;
- one repository;
- one observation window;
- a nonempty ordered replay-case list;
- the exact ordered case-digest list;
- one canonical dataset digest.

Duplicate case identifiers or case digests are rejected. Every case must belong to
the dataset repository and observation window.

## Policy bounds

The sealed policy limits:

- request age;
- total case count;
- error fingerprints per case;
- repair cycles per case;
- provider calls per case;
- generated output bytes per case;
- authorized evaluator identities.

The policy requires exact case digests, sequential evidence, and read-only
evaluation. It denies execution, repository mutation, Git effects, network access,
secret reads, candidate-selection authority, and general successor authority.

## Metrics

### Stage metrics

For each pre-verification stage the report records:

- reached count;
- passed count;
- failed count;
- aborted count;
- not-run count;
- conditional pass rate among reached cases.

The conditional denominator prevents a late-stage pass rate from being diluted by
cases that never reached that stage.

### Independent verification

The report separately records:

- reached;
- passed;
- failed;
- inconclusive;
- not run;
- conditional pass rate.

```text
verification passed != correctness proof
verification failed != required edit
verification inconclusive != evidence deletion
```

### Failure localization

For each case, the first failed or aborted stage is counted. A case with no recorded
failure and no independent-verification outcome is counted as incomplete evidence.

The first-failure baseline is intended to distinguish, for example:

- malformed structured output;
- patch-application failure;
- syntax failure;
- unknown symbol or type failure;
- targeted-test failure;
- full-regression failure;
- independent-verification failure or inconclusiveness.

The v0.1 case schema stores normalized error fingerprints but does not infer them
from raw logs. Typed error classification is a planned successor surface.

### Repair efficiency

The report records:

- cases with one or more repair cycles;
- cases whose repair reached an independently verified patch;
- repair-green rate;
- total repair cycles;
- repair cycles per verified patch.

These are cost and outcome measurements, not proof that a repair is semantically
correct.

### Provider and output efficiency

The report records:

- total provider calls;
- provider calls per verified patch;
- total generated output bytes;
- generated output bytes per verified patch.

When no patch is independently verified, the denominator remains zero and the
ratio is explicitly undefined. No division-by-zero value is fabricated.

### Error recurrence

The report counts:

- distinct normalized error fingerprints;
- fingerprints appearing in more than one case;
- cases containing a repeated fingerprint;
- deterministic per-fingerprint frequencies.

This is the baseline for a later version-bound repair-memory surface.

## Determinism

For fixed dataset, request, and policy mappings, orchestration and metric ordering
are deterministic. All cases and reports are content-addressed by canonical JSON
digests.

Determinism here means reproducible aggregation. It does not establish that the
source observations were complete or correct.

## Outputs

A successful evaluation emits:

1. a sealed metrics object;
2. sealed read-only evaluation evidence;
3. a sealed route receipt.

The evidence and receipt record that:

- exact source correspondence was verified;
- replay evaluation completed;
- historical code was not re-executed;
- no provider or verification runner was invoked;
- no repository or Git effect occurred;
- no network or secret access occurred;
- no selection or successor authority was granted.

## Blocked conditions

The route blocks for:

- malformed or extra fields;
- unsupported schemas or profiles;
- invalid identifiers, repositories, Git SHAs, or SHA-256 digests;
- stale or future requests;
- unauthorized evaluators;
- request, policy, dataset, or case digest mismatch;
- repository or dataset correspondence mismatch;
- empty or over-budget datasets;
- duplicate case identities;
- case-digest order drift;
- case observations outside the dataset window;
- nonsequential stage evidence;
- missing or unexpected lineage digests;
- malformed error fingerprints;
- repair, provider-call, or output-budget excess;
- any policy that enables effects or authority.

Blocked results contain no evidence and no receipt.

## Fixed boundaries

```text
baseline replay != historical code execution
normalized case != repository truth
case digest != semantic correctness
stage pass rate != correctness rate
test pass != proof
verification pass != proof
error fingerprint != required edit
repair-green rate != production readiness
deterministic aggregation != unbiased dataset
baseline receipt != selection authority
baseline receipt != execution authority
baseline receipt != Git authority
baseline receipt != successor authority
```

## Planned successors

The measured baseline is intended to support the following sequence:

1. Selective Repository Semantic Context Pack;
2. Typed Structured Edit IR;
3. Candidate Static Admissibility Preflight;
4. Evidence-Bearing Candidate Portfolio;
5. Typed Verification Failure Taxonomy and Repair Router;
6. Independent Test Synthesis and Mutation-Guided Strengthening;
7. Evidence-Weighted Selection and Abstention;
8. Version-Bound Repair Memory;
9. Maintainability Trajectory Gate.

Each successor should be evaluated against the same replay dataset or a
content-addressed successor dataset.

## Machine-readable artifacts

- runtime:
  `runtime/kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1.py`
- checker:
  `scripts/check_codeai_generated_patch_error_baseline_replay_evaluation_v0_1.py`
- tests:
  `tests/test_kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1.py`
- example:
  `examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json`
- manifest:
  `manifests/kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json`
- formal kernel:
  `formal/KUOS/CodeAI/GeneratedPatchErrorBaselineReplayEvaluationV0_1.lean`
- formal root:
  `formal/KuuOSCodeAIGeneratedPatchErrorBaselineReplayEvaluationV0_1.lean`

## Validation

The dedicated workflow performs:

1. Python syntax compilation;
2. example and manifest JSON validation;
3. integration checking;
4. 23 fail-closed and metric tests;
5. related structured-generation, verification, and repair regression tests;
6. canonical dependency-manifest verification;
7. strict compilation of the new Lean root;
8. strict compilation of the complete `KuuOSFormal` baseline.

Lean warnings and `sorry` are treated as errors.
