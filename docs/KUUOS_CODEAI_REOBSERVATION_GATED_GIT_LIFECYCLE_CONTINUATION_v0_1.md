# CodeAI Re-observation-Gated Git Lifecycle Continuation v0.1

## Status

Additive continuation-admission bridge.

This stage is the immediate authority successor of **CodeAI Autonomous Git Effect Re-observation v0.1**. Re-observation emits fresh lifecycle-state evidence but deliberately grants no successor effect. This stage closes that gap by consuming the exact completed re-observation receipt once, checking its evidence and state lineage, and invoking the existing **CodeAI Autonomous Git Lifecycle v0.1** evaluator exactly once.

```text
sealed source trajectory receipt
+ completed Git effect re-observation receipt
+ sealed re-observation evidence
+ fresh lifecycle state
+ fresh continuation request and nonce
+ continuation policy
+ replay registry
+ delegated lifecycle request and policy
  -> exact source correspondence
  -> optional non-factual check-name projection
  -> exactly one existing lifecycle evaluation
  -> at most one next-effect lease
  -> source receipt and nonce consumption
  -> monotone next registry
  -> no automatic effect execution
```

## Why this stage exists

The re-observation stage establishes fresh evidence about repository, branch, pull-request, checks, and merge state. That evidence is not itself a capability. A later effect requires a fresh lifecycle evaluation with a new execution session and nonce, explicit policy, replay history, and the prior lifecycle receipt recorded exactly once.

The stage therefore preserves:

```text
fresh re-observation state != next-effect lease
state evidence != Git authority
continuation evaluation != effect execution
one delegated lease != general Git authority
checks passed != correctness proof
merge observed != truth
```

## Inputs

The kernel requires:

1. the original Autonomous Trajectory Synthesis receipt;
2. one completed Autonomous Git Effect Re-observation receipt;
3. the matching re-observation evidence;
4. the matching fresh lifecycle state;
5. a fresh continuation request and nonce;
6. a continuation policy;
7. a parallel replay registry;
8. a fresh delegated Autonomous Git Lifecycle request;
9. the delegated lifecycle policy.

All request, policy, registry, evidence, state, and receipt digests are canonical. Repository, lifecycle, executor, source trajectory, source lifecycle receipt, delegated request, and delegated policy lineage must match exactly.

## Re-observation admission

Only a source receipt with all of the following is admitted:

- `autonomous_git_effect_reobservation_completed`;
- valid adapter evidence;
- lifecycle-state and source-effect correspondence confirmed;
- fresh lifecycle state issued;
- source execution receipt and re-observation nonce consumed;
- no network, secret, Git write, deployment, automatic successor, general Git, or general successor authority.

Failed or quarantined re-observation receipts issue no fresh state and cannot enter continuation evaluation.

## State projection boundary

Autonomous Git Lifecycle v0.1 represents unobserved checks with an empty required-check list. Re-observation records the policy-owned required-check names even before checks have been observed. The continuation bridge may therefore perform one explicit projection:

```text
checks_observed = false
successful = pending = failed = []
required_check_names = policy names
  -> required_check_names = []
```

No factual observation field may change. The projected state receives a new canonical lifecycle-state digest and is submitted to the existing lifecycle evaluator. If checks have been observed, the exact required-check list must match the delegated lifecycle policy and no projection is performed.

## Delegated lifecycle evaluation

The delegated request must:

- use a fresh execution session and nonce;
- bind the same lifecycle, trajectory, repository, source commit, executor, branches, remote, change-set, commit-message digest, and merge method;
- record the source lifecycle receipt digest exactly once in prior lifecycle history;
- remain within request and state freshness windows.

The existing lifecycle evaluator retains ownership of all route decisions. The continuation stage does not independently decide commit, push, PR, readiness, checks, or merge eligibility. It records the delegated disposition and issues at most the one exact lease contained in the delegated receipt.

## Replay closure

The continuation registry contains parallel unique histories of:

- consumed source re-observation receipt digests;
- consumed continuation nonce digests.

An admitted continuation advances registry revision and consumed count by exactly one. Receipt replay, nonce replay, parallel-history mismatch, stale input, and capacity exhaustion fail closed before lifecycle evaluation.

## Fixed boundaries

```text
re-observation receipt consumption != effect execution
state projection != factual mutation
lifecycle evaluation != correctness proof
one-effect lease != general Git authority
hold / degraded / completed != active lease
unused policy capacity != reusable authority
continuation receipt != deployment authority
continuation receipt != secret access authority
continuation receipt != general successor-stage authority
```

The stage performs no Git write, ref mutation, commit, push, PR mutation, merge, deployment, secret access, network call, or handover. A separately admitted Git Effect Execution stage must consume any delegated active lease.

## Artifacts

- runtime: `runtime/kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1.py`
- checker: `scripts/check_codeai_reobservation_gated_git_lifecycle_continuation_v0_1.py`
- tests: `tests/test_kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1.py`
- example: `examples/codeai_reobservation_gated_git_lifecycle_continuation_v0_1.json`
- manifest: `manifests/kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/ReobservationGatedGitLifecycleContinuationV0_1.lean`
- formal root: `formal/KuuOSCodeAIReobservationGatedGitLifecycleContinuationV0_1.lean`
- workflow: `.github/workflows/codeai-reobservation-gated-git-lifecycle-continuation-v0-1.yml`
