# CodeAI Durable Git Lifecycle Loop Resumption Consumption v0.1

## Status

Additive one-shot consumption boundary between durable resumption admission and a later bounded loop-resumption executor.

This stage is the immediate successor of **CodeAI Durable Git Lifecycle Loop Resumption Admission v0.1**. The predecessor reads one committed checkpoint, verifies exact lineage, and emits one inactive future-only resume input. This stage consumes that exact resume input once and converts it into one active, one-shot bounded loop execution input.

```text
successful resumption-admission receipt and evidence
+ matching successful resumption registry
+ exact inactive future-only resume input
+ fresh consumption request and nonce
+ deny-by-default consumption policy
+ monotone consumption registry
  -> exact source correspondence
  -> one-shot resume-input consumption
  -> one active bounded loop execution input
  -> exact inherited budgets and lineage
  -> no loop execution during consumption
  -> no Git effect during consumption
```

## Why this stage exists

A resume input is not self-activating authority. Durable checkpoint verification and future-only admission are deliberately separated from activation.

```text
verified checkpoint != active loop
resume input issuance != resume input consumption
future-only input != current execution authority
active bounded input != automatic execution
bounded loop authority != direct Git authority
consumption receipt != unrestricted successor authority
```

The separation provides a replay boundary after durable read and before execution. A later executor can require the exact consumption receipt and active execution-input digest rather than accepting a reusable checkpoint or admission receipt.

## Inputs

The kernel requires:

1. one successful resumption-admission receipt;
2. the matching resumption-admission evidence;
3. the matching successful resumption registry;
4. the exact emitted resume input;
5. one fresh consumption request and nonce;
6. one deny-by-default consumption policy;
7. one sealed consumption registry.

The request binds the exact receipt, evidence, registry, resume-input, checkpoint, loop, lifecycle, repository, consumer, and execution-session identities.

## Source requirements

The source admission must prove:

- the committed checkpoint read was verified;
- one resume input was issued;
- the source receipt, evidence, and registry correspond exactly;
- the checkpoint and envelope digest are present in successful admission history;
- no unavailable, failed, or quarantined read disposition is accepted;
- no loop execution, Git effect, automatic resumption, network access, secret read, general Git authority, or general successor authority occurred;
- the resume input is future-only and inactive;
- the resume input has no prior loop, Git, automatic-resumption, or general-successor authority.

The resume input is validated with an exact field set and canonical digest. Additional or missing fields fail closed.

## Consumption semantics

A successful consumption requires:

- a fresh request within the policy age bound;
- an unused consumption nonce;
- an unconsumed source resumption receipt;
- an unconsumed resume-input digest;
- an authorized exact consumer identity;
- explicit resume-input consumption and execution-input issuance requests;
- exact source correspondence confirmation;
- all inherited budgets within the consumption-policy maxima;
- remaining registry capacity.

The transition appends exactly one entry to each parallel history:

- consumed consumption nonce digests;
- consumed resumption receipt digests;
- consumed resume-input digests;
- issued execution-input digests.

The registry revision and successful-consumption count each advance by exactly one.

## Active execution input

Successful consumption emits one sealed execution input containing:

- exact resumption receipt, evidence, registry, and resume-input lineage;
- checkpoint, loop, lifecycle, and repository identity;
- prior loop disposition and effect accounting;
- exact resume effect, command, and output budgets;
- one execution-session-derived identifier;
- one-shot and non-reusable status;
- active bounded loop-execution authority.

The active input grants no direct Git effect. Git effects remain available only through the existing lifecycle evaluator and exact one-effect lease chain when a later executor is separately invoked.

The input also grants no automatic execution, network access, secret read, general Git authority, or general successor-stage authority.

## Fixed boundaries

```text
resumption consumption != loop execution
resumption consumption != Git effect
active input != automatic execution
active input != direct Git capability
one-shot input != reusable capability
budget inheritance != budget consumption
loop execution authority != unrestricted command authority
consumption registry transition != external atomic persistence
consumption receipt != correctness
consumption receipt != general successor authority
```

## Failure behavior

Any validation, correspondence, policy, freshness, capacity, or replay failure returns `blocked` and emits:

- no active execution input;
- no evidence;
- no next registry;
- no receipt.

No partial registry transition is returned.

## Machine-readable artifacts

- runtime:
  `runtime/kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1.py`
- checker:
  `scripts/check_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1.py`
- tests:
  `tests/test_kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1.py`
- example:
  `examples/codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1.json`
- manifest:
  `manifests/kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1.json`
- formal kernel:
  `formal/KUOS/CodeAI/DurableGitLifecycleLoopResumptionConsumptionV0_1.lean`
- formal root:
  `formal/KuuOSCodeAIDurableGitLifecycleLoopResumptionConsumptionV0_1.lean`

## Validation

The dedicated workflow performs:

1. Python syntax compilation;
2. example and manifest JSON validation;
3. integration checking;
4. bounded-loop regression tests;
5. checkpoint-persistence regression tests;
6. resumption-admission regression tests;
7. resumption-consumption tests;
8. canonical dependency-manifest verification;
9. strict compilation of the new Lean root;
10. strict compilation of the complete `KuuOSFormal` baseline.

Warnings and `sorry` are treated as errors for Lean compilation.
