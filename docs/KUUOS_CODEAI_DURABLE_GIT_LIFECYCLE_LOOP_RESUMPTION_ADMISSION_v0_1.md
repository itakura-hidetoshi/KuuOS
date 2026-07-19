# CodeAI Durable Git Lifecycle Loop Resumption Admission v0.1

## Status

Additive durable checkpoint read and resumption-input admission boundary.

This stage is the immediate successor of **CodeAI Durable Git Lifecycle Loop Checkpoint Persistence v0.1**. The predecessor commits one sealed bounded-loop checkpoint but explicitly grants no resumption authority. This stage independently reads that checkpoint through one structured read adapter, verifies the exact committed envelope, and may issue one future-only bounded resume input.

```text
committed checkpoint persistence receipt/evidence
+ committed persistence registry and store state
+ fresh resumption request and nonce
+ deny-by-default resumption policy
+ resumption replay registry
+ one structured checkpoint read adapter
  -> exact persisted-source correspondence
  -> exact checkpoint envelope digest verification
  -> one future-only bounded resume input on verified read
  -> monotone attempt registry
  -> successful checkpoint consumption only on admission
  -> no loop execution and no Git effect
```

## Why this stage exists

A persisted checkpoint is evidence, not a capability. Resumption must not trust the in-memory envelope returned during persistence, nor treat store membership as execution authority.

```text
persisted checkpoint != resume input
checkpoint identifier != checkpoint contents
adapter acknowledgement != verified envelope
verified envelope != automatic resumption
resume input != loop execution authority
failed read != automatic retry authority
```

## Inputs

The kernel requires:

1. one successful checkpoint-persistence receipt;
2. the exact matching persistence evidence;
3. the matching successful persistence registry;
4. the matching checkpoint-store state;
5. a fresh resumption-admission request and nonce;
6. a bounded resumption policy;
7. a resumption replay registry;
8. one structured read adapter.

The request binds the exact persistence receipt/evidence, registry, store state, checkpoint identifier and envelope digest, loop and lifecycle identity, repository, reader, adapter, store, requested resume budgets, and creation epoch.

## Read and admission semantics

Admission requires:

- a canonical successful persistence receipt and evidence;
- exact correspondence with the persistence registry and store state;
- checkpoint identifier and envelope digest present in both durable histories;
- a fresh request within the age bound;
- an unused resumption nonce;
- no prior successful admission for the checkpoint, envelope, or persistence receipt;
- requested resume budgets within policy bounds;
- explicit checkpoint-read and resume-input issuance permission;
- explicit denial of loop execution, Git effect, automatic resumption, network, secret read, and general successor authority.

The read adapter is invoked exactly once only after all admission checks pass.

## Read result classes

- `verified`: the checkpoint is found, read once, and the returned envelope is canonical and exactly matches the committed digest and identifier;
- `unavailable`: the store read completes but the checkpoint is not available;
- `failed`: no verified checkpoint is returned;
- malformed or effect-bearing evidence is sealed as `quarantined`.

Adapter exceptions are converted into a sealed failed read result rather than escaping the kernel.

## Registry transitions

Every admitted read attempt consumes exactly one fresh resumption nonce and advances the attempt registry by one.

Only a verified checkpoint read may additionally append:

- the checkpoint identifier;
- the checkpoint envelope digest;
- the source persistence receipt digest;
- one successful resumption-admission count.

Unavailable, failed, and quarantined reads do not consume the checkpoint successfully. A separately authorized fresh request with a fresh nonce may retry.

## Resume input

A successful admission emits one sealed future-only resume input containing:

- exact checkpoint and persistence lineage;
- loop, lifecycle, and repository identity;
- prior loop disposition and effect count;
- final lifecycle receipt/state digests;
- final lifecycle completion and lease status;
- bounded resume effect, command, and output budgets;
- an issuance epoch;
- explicit false values for active execution, Git effect, automatic resumption, and general successor authority.

The resume input is an input to a later separately admitted loop-resumption execution stage. It is not itself an active lease or execution capability.

## Fixed boundaries

```text
checkpoint read != loop execution
checkpoint read != Git effect
verified envelope != automatic resumption
resume input != active execution
resume input != general Git authority
resume input != general successor authority
unavailable or failed read != retry authority
adapter evidence != durable truth without digest verification
```

This stage performs no Git write, loop execution, repository mutation, deployment, network access, secret-material read, checkpoint overwrite, checkpoint deletion, or automatic resumption.

## Artifacts

- runtime facade: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1.py`
- runtime types: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1.py`
- runtime validation: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_validation_v0_1.py`
- runtime adapter boundary: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_adapter_v0_1.py`
- runtime core: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_core_v0_1.py`
- checker: `scripts/check_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1.py`
- tests: `tests/test_kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1.py`
- example: `examples/codeai_durable_git_lifecycle_loop_resumption_admission_v0_1.json`
- manifest: `manifests/kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/DurableGitLifecycleLoopResumptionAdmissionV0_1.lean`
- formal root: `formal/KuuOSCodeAIDurableGitLifecycleLoopResumptionAdmissionV0_1.lean`
- workflow: `.github/workflows/codeai-durable-git-lifecycle-loop-resumption-admission-v0-1.yml`
