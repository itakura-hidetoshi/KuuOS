# CodeAI Durable Git Lifecycle Loop Resumption Execution v0.1

## Status

Additive, separately invoked execution boundary after durable checkpoint persistence, resumption admission, and one-shot resumption consumption.

The predecessor emits one active, one-shot, non-reusable bounded loop execution input. This stage consumes that exact input once, rechecks the original inactive resume input as a lineage witness, binds the checkpointed final lifecycle receipt to the resumed initial lifecycle receipt, and invokes the existing bounded autonomous Git lifecycle loop orchestrator exactly once.

```text
successful resumption-consumption receipt and evidence
+ matching successful consumption registry
+ exact original inactive resume input
+ exact active one-shot execution input
+ fresh invocation request and nonce
+ deny-by-default execution policy
+ monotone execution registry
+ exact bounded-loop invocation bundle
  -> exact lineage correspondence
  -> exact checkpoint-to-lifecycle binding
  -> one-shot execution-input consumption
  -> one bounded loop invocation
  -> existing lifecycle evaluator and one-effect lease chain only
  -> exactly-once execution-registry transition
```

## Why this stage exists

An active execution input is bounded authority, not automatic execution. Consumption and execution remain separate operations.

```text
active input != automatic invocation
one-shot authority != reusable capability
resume-input digest != sufficient lifecycle witness
checkpoint identity != arbitrary lifecycle state
loop execution authority != direct Git authority
bounded delegation != unbounded command authority
successful inner loop != unrestricted successor authority
```

The original inactive resume input is required again because it carries the checkpointed final lifecycle receipt digest. The executor rejects any resumed initial lifecycle receipt that does not match that exact digest.

## Inputs

The kernel requires:

1. the successful resumption-consumption receipt;
2. the matching resumption-consumption evidence;
3. the matching successful consumption registry;
4. the original inactive resume input;
5. the exact active one-shot execution input;
6. a fresh invocation request and nonce;
7. a deny-by-default execution policy;
8. a monotone execution registry;
9. the exact source trajectory receipt and initial lifecycle receipt;
10. the bounded loop request, policy, registries, and adapters.

## Exact correspondence

The following identities must agree:

- consumption receipt, evidence, and registry digests;
- original resume-input digest;
- active execution-input digest;
- checkpoint, loop, lifecycle, and repository identity;
- authorized executor identity;
- active input issuance history in the consumption registry;
- resumed initial lifecycle receipt digest and the checkpointed final lifecycle receipt digest;
- bounded loop request and policy digests.

Any mismatch blocks before the bounded loop is invoked.

## One-shot replay boundary

The execution registry records three parallel histories:

- consumed invocation nonce digests;
- consumed execution-input digests;
- emitted bounded-loop receipt digests.

On success, all histories append exactly one entry and the registry revision and successful-execution count advance exactly once.

A used nonce or execution input is rejected. A failed preflight or failed inner invocation emits no outer evidence, next registry, or receipt.

## Budget mapping

The active input carries the remaining resume budgets:

- effect budget;
- total command budget;
- total output-byte budget.

The execution policy may narrow but never expand these budgets. The delegated bounded-loop request and policy must remain within both the active input and the execution policy.

Execution and re-observation command and output maxima are combined for this outer budget check.

## Git-effect boundary

This stage does not create a direct Git capability.

The only permitted Git-effect route is the existing bounded lifecycle loop:

```text
resumption executor
  -> bounded lifecycle loop orchestrator
  -> lifecycle evaluator
  -> exact one-effect execution lease
  -> Git effect adapter
  -> re-observation
  -> continuation evaluation
```

The outer receipt distinguishes:

- `direct_git_effect_performed = false`;
- delegated effect count reported by the bounded loop.

No force push, admin bypass, remote branch deletion, deployment, or other authority is added here. Those remain governed by the existing lifecycle policy and effect chain.

## Success output

A successful invocation returns:

- the complete bounded-loop result;
- sealed execution evidence;
- the next execution registry;
- a sealed execution receipt.

The receipt records:

- exact source digests;
- bounded-loop request, policy, evidence, and receipt digests;
- checkpoint, loop, lifecycle, and repository identity;
- execution-input and nonce consumption;
- exactly-once registry advancement;
- single bounded-loop invocation;
- enforcement of the existing lifecycle effect chain;
- absence of direct Git effect and automatic execution;
- delegated effect count and final bounded-loop disposition.

## Failure behavior

Any malformed input, digest mismatch, identity mismatch, stale request, replay, capacity violation, unsafe policy, budget expansion, invalid checkpoint-to-lifecycle binding, or non-ready inner loop result returns `blocked`.

Blocked results contain:

- no outer evidence;
- no next execution registry;
- no outer receipt.

The inner result is retained only for diagnosis when the bounded loop itself was invoked and did not return a complete ready result.

## Fixed boundaries

```text
resumption execution != direct Git effect
resumption execution != automatic execution
resumption execution != unbounded execution
active input != reusable capability
checkpoint witness != arbitrary lifecycle substitution
outer registry transition != external atomic persistence
inner ready status != truth or correctness
execution receipt != general Git authority
execution receipt != general successor authority
```

## Machine-readable artifacts

- runtime: `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1.py`
- checker: `scripts/check_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1.py`
- tests: `tests/test_kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1.py`
- example: `examples/codeai_durable_git_lifecycle_loop_resumption_execution_v0_1.json`
- manifest: `manifests/kuuos_codeai_durable_git_lifecycle_loop_resumption_execution_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/DurableGitLifecycleLoopResumptionExecutionV0_1.lean`
- formal root: `formal/KuuOSCodeAIDurableGitLifecycleLoopResumptionExecutionV0_1.lean`

## Validation

The dedicated workflow performs:

1. Python syntax compilation;
2. example and manifest JSON validation;
3. integration checking;
4. bounded-loop, checkpoint, admission, consumption, and execution regression tests;
5. canonical dependency-manifest verification;
6. strict compilation of the new Lean root;
7. strict compilation of the complete `KuuOSFormal` baseline.

Warnings and `sorry` are errors for Lean compilation.
