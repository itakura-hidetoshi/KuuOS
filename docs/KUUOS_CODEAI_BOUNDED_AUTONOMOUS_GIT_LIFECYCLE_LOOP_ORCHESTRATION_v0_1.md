# CodeAI Bounded Autonomous Git Lifecycle Loop Orchestration v0.1

## Status

Additive synchronous bounded-loop orchestrator.

This stage composes four existing CodeAI contracts without widening any of them:

```text
Autonomous Git Lifecycle one-effect lease
  -> Autonomous Git Effect Execution
  -> Autonomous Git Effect Re-observation
  -> Re-observation-Gated Git Lifecycle Continuation
  -> at most one next one-effect lease
```

The composition may repeat only within an exact effect-count bound, exact cumulative execution and observation budgets, and three monotone replay registries. Only one active lifecycle lease is consumed at a time.

## Why this stage exists

The four predecessor stages close each local authority transition, but none owns the bounded repetition of the entire lifecycle. Calling them ad hoc could lose the global effect count, cumulative budget, replay history, or stop reason. This stage records those loop-level obligations explicitly.

```text
one-effect lease != unbounded autonomy
fresh state != automatic continuation
remaining budget != reusable authority
execution failure != automatic retry authority
checks passed != correctness proof
merge observed != truth
```

## Inputs

The orchestrator requires:

1. one supported Autonomous Trajectory Synthesis receipt;
2. one active Autonomous Git Lifecycle receipt;
3. a fresh loop request and nonce;
4. a bounded deny-by-default loop policy;
5. a loop replay registry;
6. the existing execution, re-observation, and continuation registries;
7. one structured Git-effect adapter;
8. one structured read-only re-observation adapter.

The request binds the trajectory, initial lifecycle receipt, lifecycle, repository, source commit, executor, observer, base/head branches, remote, change set, commit message, PR text, merge method, prior lifecycle sessions/nonces/receipts, and requested maximum effect count.

## Per-iteration contract

For each admitted iteration, the kernel:

1. verifies that the current lifecycle receipt contains exactly one active supported lease;
2. derives a fresh deterministic execution request and bounded execution policy;
3. invokes Autonomous Git Effect Execution exactly once;
4. invokes Git Effect Re-observation exactly once even when execution reports failure or quarantined evidence;
5. admits continuation only when re-observation emits a fresh lifecycle state;
6. invokes Re-observation-Gated Git Lifecycle Continuation exactly once;
7. records the execution, re-observation, continuation, and delegated lifecycle receipt digests;
8. advances to at most the one lease contained in the delegated lifecycle receipt.

No two effect leases are executed concurrently.

## Bounded termination

The loop stops on the first applicable condition:

- lifecycle completion;
- a non-active terminal lifecycle hold;
- requested effect-count exhaustion;
- cumulative execution or re-observation budget exhaustion;
- execution failure or evidence quarantine, after fresh re-observation;
- re-observation failure or evidence quarantine;
- any predecessor-stage fail-closed block.

A failed execution is not retried by this stage. The fresh re-observed state and delegated lifecycle receipt remain evidence for a separately admitted future operation.

## Budgets

The policy fixes:

- maximum effect count;
- cumulative execution command count and output bytes;
- cumulative re-observation command count and output bytes;
- per-effect execution command count, output bytes, and timeout seconds;
- per-effect re-observation command count and output bytes;
- request, state, and observation freshness windows;
- registry capacity.

Unused budget is not a capability and does not authorize another loop.

## Continuation state projection compatibility

The predecessor continuation specification already permits one non-factual representation projection when checks have not yet been observed:

```text
checks_observed = false
successful = pending = failed = []
required_check_names = policy-owned names
  -> required_check_names = []
```

The loop delegates this already-implemented projection to the authoritative continuation runtime before the existing lifecycle validator is invoked. This stage does not modify the continuation runtime or its tests. No factual observation field changes, and the continuation evidence records both source and evaluated state digests and whether the projection occurred.

## Replay closure

The loop registry contains parallel unique histories of:

- consumed initial lifecycle receipt digests;
- consumed loop nonce digests.

An admitted loop advances its revision and completed-loop count by exactly one and adds the number of actually admitted effect iterations to the cumulative effect count. The execution, re-observation, and continuation registries advance only through their owning predecessor stages.

## Fixed boundaries

```text
bounded loop != correctness proof
bounded loop != unrestricted autonomous execution
one active lease != general Git authority
execution completion != correct repository state
re-observation != truth
continuation evaluation != effect execution
budget exhaustion != failure repair authority
execution failure != automatic retry
state projection != factual mutation
merge completion != deployment authority
loop receipt != secret access authority
loop receipt != human handover authority
loop receipt != general successor-stage authority
```

Force push, remote branch deletion, admin bypass, deployment, secret-material reading, human/external handover, networked re-observation, concurrent effect execution, and unbounded continuation are unavailable.

## Artifacts

- runtime: `runtime/kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1.py`
- checker: `scripts/check_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1.py`
- tests: `tests/test_kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1.py`
- example: `examples/codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1.json`
- manifest: `manifests/kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/BoundedAutonomousGitLifecycleLoopOrchestrationV0_1.lean`
- formal root: `formal/KuuOSCodeAIBoundedAutonomousGitLifecycleLoopOrchestrationV0_1.lean`
- workflow: `.github/workflows/codeai-bounded-autonomous-git-lifecycle-loop-orchestration-v0-1.yml`
