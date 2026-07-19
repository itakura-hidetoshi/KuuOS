# CodeAI Durable Git Lifecycle Loop Checkpoint Persistence v0.1

## Status

Additive durable checkpoint persistence boundary.

This stage is the immediate persistence successor of **CodeAI Bounded Autonomous Git Lifecycle Loop Orchestration v0.1**. The predecessor returns a sealed loop receipt, loop evidence, four updated replay registries, and a final lifecycle receipt/state. Those values remain process-local evidence until a separately authorized persistence operation commits them to a durable checkpoint store.

```text
completed bounded-loop bundle
+ fresh persistence request and nonce
+ deny-by-default persistence policy
+ persistence replay registry
+ checkpoint store state
+ one structured checkpoint adapter
  -> exact source correspondence
  -> atomic compare-and-swap attempt
  -> one sealed durable checkpoint envelope
  -> monotone persistence registry
  -> monotone store state only on commit
  -> no resume input and no loop re-execution
```

## Why this stage exists

The bounded loop closes effect count, cumulative budget, and replay obligations within one synchronous invocation. It does not own external durability, crash recovery, or process restart. Treating an in-memory loop receipt as already durable would erase the distinction between evidence creation and committed storage.

```text
loop receipt != durable checkpoint
adapter acknowledgement != durable truth
checkpoint persistence != resumption authority
unused store capacity != write authority
CAS conflict != successful persistence
persistence failure != automatic retry authority
```

## Inputs

The kernel requires:

1. one completed or terminal bounded-loop receipt;
2. the exact matching loop evidence;
3. the matching loop, execution, re-observation, and continuation registries;
4. the matching final lifecycle receipt and optional final lifecycle state;
5. a fresh checkpoint-persistence request and nonce;
6. a bounded persistence policy;
7. a persistence replay registry;
8. the current checkpoint-store state;
9. one structured persistence adapter.

All digests are canonical. The request and policy bind the exact loop bundle, lifecycle, repository, persister, adapter, store, expected store revision, and checkpoint identifier.

## Persistence admission

Admission requires:

- canonical and mutually corresponding source receipt/evidence/registry digests;
- a supported bounded-loop disposition;
- a fresh request within the configured age window;
- a previously unused persistence nonce;
- a loop receipt and checkpoint identifier not previously persisted;
- matching persistence registry and checkpoint-store histories;
- remaining registry and store capacity;
- checkpoint revision exactly `1`;
- explicit permission for checkpoint persistence;
- mandatory atomic compare-and-swap, checkpoint absence, and nonce consumption;
- explicit denial of overwrite, delete, network, secret, Git-effect, loop-execution, resume, and general-successor permissions.

The adapter is invoked exactly once only after all admission checks pass.

## Atomic compare-and-swap result classes

The adapter result is validated as one of three factual result classes:

- `committed`: observed revision equals the expected revision, the committed revision advances by exactly one, the checkpoint was absent, and the write committed;
- `conflict`: the observed revision differs from the expected revision and no write committed;
- `failed`: no write committed and the store revision did not advance.

Malformed or effect-bearing adapter evidence is quarantined. Adapter exceptions are converted into a sealed failed result rather than escaping the kernel.

## Registry and store transitions

Every admitted persistence attempt consumes exactly one persistence nonce and advances the persistence registry revision and attempt count by exactly one.

Only a committed CAS write may additionally:

- append the source loop receipt digest;
- append the checkpoint identifier;
- increment the successful-persistence count;
- increment the checkpoint-store revision;
- append the checkpoint-envelope digest;
- update the last committed epoch.

Conflict, failure, and quarantine preserve the checkpoint-store state. They do not mark the loop receipt or checkpoint identifier as successfully persisted, so a separately authorized fresh request with a fresh nonce may retry.

## Checkpoint envelope

The sealed envelope records:

- all source receipt/evidence/registry digests;
- final lifecycle receipt/state digests;
- loop, lifecycle, repository, checkpoint, and store identity;
- loop disposition and effect counts;
- final lifecycle completion and lease status;
- request and policy digests;
- creation epoch;
- explicit absence of resume input, automatic resumption, and general successor authority.

The envelope is evidence for later read/resumption stages. It is not itself a capability.

## Fixed boundaries

```text
checkpoint persistence != loop execution
checkpoint persistence != Git effect
checkpoint persistence != resume input issuance
checkpoint persistence != automatic resumption
checkpoint persistence != general successor authority
checkpoint persistence != correctness proof
checkpoint persistence != deployment authority
checkpoint persistence != secret access authority
checkpoint persistence != network authority
checkpoint persistence != overwrite or delete authority
CAS acknowledgement != durable truth
```

This stage performs no Git write, loop execution, repository mutation, deployment, network access, secret-material read, checkpoint overwrite, checkpoint deletion, resume input issuance, or automatic resumption. A later separately admitted stage must read and verify the durable checkpoint before producing any resumption input.

## Artifacts

- runtime facade: `runtime/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1.py`
- runtime types: `runtime/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_types_v0_1.py`
- runtime validation: `runtime/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_validation_v0_1.py`
- runtime adapter boundary: `runtime/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_adapter_v0_1.py`
- runtime core: `runtime/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_core_v0_1.py`
- checker: `scripts/check_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1.py`
- tests: `tests/test_kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1.py`
- example: `examples/codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1.json`
- manifest: `manifests/kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/DurableGitLifecycleLoopCheckpointPersistenceV0_1.lean`
- formal root: `formal/KuuOSCodeAIDurableGitLifecycleLoopCheckpointPersistenceV0_1.lean`
- workflow: `.github/workflows/codeai-durable-git-lifecycle-loop-checkpoint-persistence-v0-1.yml`
