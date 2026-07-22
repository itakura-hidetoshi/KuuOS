# CodeAI External Corpus Acquisition and Freeze Receipt v0.1

## Purpose

This additive stage is the acquisition successor to **CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1**.

It consumes the exact predecessor manifest and one independently observed external corpus artifact. It validates the pinned dataset source, revision, path, SHA-256, byte size, row count, schema, field partition, immutable storage contract, and authority boundaries. It emits one of two read-only dispositions:

- `external_corpus_freeze_admitted`;
- `external_corpus_freeze_held`.

Admission means that one exact external corpus artifact has been content-addressed and frozen for later separately governed evaluation stages. It does not expose benchmark answers to the solver, execute the SWE-bench harness, generate a patch, mutate a repository, grant Git authority, or claim correctness or generalization.

Malformed, tampered, stale, version-mismatched, or lineage-mismatched inputs are structurally blocked before a disposition is emitted. Structurally valid evidence that lacks acquisition or isolation predicates produces a hold.

## Main normalization lineage

This stage was developed as stacked PR #1336 on the fixed predecessor head, then merged into that stacked base branch. PR #1337 is the explicit normalization path that lands the same stage on `main` and revalidates its fixed content against the authoritative frontier.

- controller repository: `itakura-hidetoshi/KuuOS`;
- predecessor profile: `CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1`;
- predecessor head: `e07e32b76bebd3e260dbe1847080e29b3ffe6346`;
- stacked merge commit: `c16c2e33aba95e93d352d6b790491f3b57300c92`;
- predecessor manifest digest: `a5310fcfdb5d6c8ee99d66eb56d4d0f3cdd76152582c620f3b8dd6aa597b688d`;
- predecessor adapter pack: `134475fc54fc23d0bcb48973b9fcfd158da51fa6a95ea4eff083a500f7936107`;
- predecessor receipt: `55233619cdc23640818f305564ee08652e5f9817cb0260128256c4d3ddfd7b73`.

Queued or in-progress runs are not success evidence. The normalization PR remains governed by completed CI evidence for its exact head before it can become the current `main` frontier.

## Exact external artifact

The reference acquisition freezes the official Hugging Face artifact used by the predecessor contract:

- dataset: `princeton-nlp/SWE-bench_Verified`;
- revision: `c104f840cc67f8b6eec6f759ebc8b2693d585d4a`;
- split: `test`;
- path: `data/test-00000-of-00001.parquet`;
- SHA-256: `a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd`;
- size: `2,096,679` bytes;
- rows: `500`.

The dedicated workflow downloads the revision-pinned file and independently verifies its SHA-256, byte count, Parquet row count, and ordered Arrow schema. The corpus file is not committed to this repository.

## Schema and field partition

The exact ordered schema is:

```text
repo
instance_id
base_commit
patch
test_patch
problem_statement
hints_text
created_at
version
FAIL_TO_PASS
PASS_TO_PASS
environment_setup_commit
difficulty
```

Solver-visible fields are limited to:

```text
repo
instance_id
base_commit
problem_statement
version
environment_setup_commit
difficulty
```

Restricted evaluator fields are:

```text
patch
test_patch
hints_text
FAIL_TO_PASS
PASS_TO_PASS
```

The field lists must be ordered, duplicate-free, digest-bound, and disjoint. The acquisition stage does not release restricted field contents to candidate generation, repair memory, prompt selection, model selection, or threshold tuning.

## Acquisition observation

The acquisition observation records:

- exact source URI and revision;
- independent observer identity;
- fetch completion;
- network use by the external fetcher;
- artifact observation;
- SHA-256 and size verification;
- row-count and schema verification;
- solver/evaluator field partition verification;
- content-addressed storage;
- immutable freeze status;
- explicit effect and authority negatives.

The runtime kernel consumes evidence. It does not itself perform the network fetch:

```text
external fetch evidence consumed = true
fetch performed by kernel = false
```

This separation prevents a receipt-building function from silently acquiring network, secret, repository, or execution authority.

## BLOCK versus HOLD

Structural BLOCK includes:

- malformed or extra fields;
- invalid canonical digest;
- request/policy/observation binding mismatch;
- stale request or observation;
- predecessor manifest, pack, or receipt mismatch;
- predecessor not admitted;
- policy enabling forbidden authority;
- request claiming forbidden authority.

A valid HOLD includes:

- incomplete fetch;
- unobserved artifact;
- SHA-256, size, row count, or schema not verified;
- mutable or non-content-addressed freeze;
- wrong row count or schema order;
- solver/restricted field overlap;
- gold patch, test patch, or evaluation-label exposure;
- harness execution inside this stage;
- repository mutation or Git authority.

A hold preserves the evidence and exact reason. It is not rejection of the external benchmark.

## Reference result

The committed reference fixture produces:

- decision: `external_corpus_freeze_admitted`;
- corpus frozen: `true`;
- row count: `500`;
- artifact copy committed to KuuOS: `false`;
- solver label access granted: `false`;
- gold patch access granted: `false`;
- harness execution authority granted: `false`;
- repository mutation performed: `false`;
- Git authority granted: `false`;
- correctness claimed: `false`.

Reference content addresses:

- freeze pack: `f0de4f9fc1e5c7348ced5a6272d37d7b289d3dbbf2df086496f358a601351a6f`;
- receipt: `31575449c7bbe77179e744563e7054eeeae5f037dd5673d5e1220901eeefe16b`.

## Formal kernel

The Lean/mathlib surface defines:

- `Binding`;
- `CorpusContract`;
- `AcquisitionEvidence`;
- `ContractExact`;
- `AcquisitionVerified`;
- `FieldIsolationPreserved`;
- `BoundaryPreserved`;
- `FreezeAdmitted`.

Generic theorems extract exact binding, verified acquisition, field isolation, and boundary preservation. Separate theorems show that revision mismatch, row-count mismatch, gold-patch exposure, evaluation-label exposure, kernel-side fetch, harness execution, and repository mutation forbid admission. The actual reference specialization is admitted, while negative variants are not.

## Fixed boundaries

```text
artifact hash equality != benchmark correctness
row count and schema verification != instance solvability
corpus freeze != candidate-generation authority
corpus freeze != harness execution authority
solver-visible metadata != evaluator labels
restricted evaluator field != repair-memory input
gold patch != model context
test patch != solver-editable input
external fetch evidence != kernel network authority
content-addressed storage != repository commit
benchmark result != population generalization
freeze receipt != repository mutation or Git authority
```

## Validation

The dedicated workflow performs:

- Python compilation;
- canonical example and manifest validation;
- deterministic fixture reconstruction;
- 28 positive, tamper, binding, acquisition, field-isolation, freshness, and authority-boundary tests;
- actual revision-pinned artifact download;
- SHA-256 and byte-size verification;
- Parquet row-count and ordered-schema verification using pinned `pyarrow`;
- predecessor regression tests;
- canonical Lake manifest validation;
- strict dedicated Lean root compilation;
- strict aggregate `KuuOSFormal` compilation.

## Next stage

The next separately governed stage is **Gold-Patch Environment Smoke Validation v0.1**. It uses evaluator-only access to a preregistered smoke instance to verify that the pinned harness and Docker environment reproduce a gold outcome. Gold material remains unavailable to candidate generation and repair memory.
