# CodeAI Autonomous Git Effect Re-observation v0.1

## Status

Additive read-only observation adapter.

This stage is the immediate evidence successor of **CodeAI Autonomous Git Effect Execution v0.1**. The execution stage consumes one exact effect lease and records completed, failed, or evidence-quarantined outcome evidence. It intentionally grants no automatic successor effect. This stage closes the next gap by reading the resulting repository and hosted pull-request state again and emitting a fresh lifecycle-state object compatible with **CodeAI Autonomous Git Lifecycle v0.1**.

```text
sealed lifecycle lease receipt
+ sealed Git effect execution receipt
+ sealed Git effect execution evidence
+ fresh re-observation request
+ deny-by-default read-only policy
+ sealed replay registry
+ bounded read-only observation adapter
  -> exact source and execution lineage
  -> one adapter invocation
  -> fresh repository / branch / PR / checks / merge observation
  -> existing lifecycle-state validator compatibility
  -> execution-receipt and nonce consumption
  -> monotone next registry
  -> no successor effect authority
```

## Why this stage exists

The execution receipt is evidence about one attempted effect. It is not a reusable capability and it is not automatically the next lifecycle state. Even a completed adapter result must be re-observed before a later lifecycle evaluation can authorize another effect. Failed and quarantined attempts require the same treatment because an execution failure is not proof that no external effect occurred.

The re-observation stage therefore separates:

```text
execution evidence != fresh state evidence
adapter completion != current repository truth
failed command != confirmed no-effect
quarantined evidence != reusable lease
fresh state != successor effect authority
```

## Inputs

The kernel requires all of the following with exact canonical digests and field sets:

1. the source Autonomous Git Lifecycle v0.1 one-effect lease receipt;
2. the source Autonomous Git Effect Execution v0.1 receipt;
3. the source execution evidence, including the structured adapter result;
4. a fresh re-observation request and nonce;
5. a deny-by-default policy;
6. a parallel replay registry;
7. one structured read-only observation adapter.

The request binds lifecycle, repository, source commit, base and head branches, remote, change-set digest, commit-message digest, merge method, effect phase, observer identity, and all three source receipt/evidence digests.

## Source outcomes

All three execution outcomes are supported:

- `autonomous_git_effect_execution_completed`;
- `autonomous_git_effect_execution_failed`;
- `autonomous_git_effect_evidence_quarantined`.

A completed source requires exact effect-specific correspondence between the execution adapter evidence and the newly observed state. A failed or quarantined source does not imply that the effect is absent; the observer reports the actual current state without converting uncertainty into retry authority.

## Read-only observation contract

The adapter returns a complete Autonomous Git Lifecycle v0.1 state surface plus bounded observation metadata. It may observe:

- local commit and parent SHA;
- remote branch head;
- pull-request number, URL digest, draft status, head and base;
- exact required-check partition;
- mergeability and unresolved blockers;
- merged head and merge commit.

The adapter must explicitly record:

```text
network_accessed = false
secret_material_read = false
git_write_performed = false
deployment_performed = false
force_push_performed = false
remote_branch_deleted = false
admin_merge_bypass_used = false
human_handover_performed = false
external_authority_handover_performed = false
```

Any malformed, stale, over-budget, effect-bearing, contradictory, or lineage-mismatched evidence is quarantined and produces no lifecycle state.

## Lifecycle-state compatibility

A successful observation emits the exact `STATE_FIELDS` object owned by Autonomous Git Lifecycle v0.1 and seals it with the existing lifecycle-state digest field. The dedicated checker submits the result to the existing lifecycle state validator.

The state is monotone relative to already observed lifecycle history. Previously observed commit, push, PR, checks, or merge facts cannot disappear in the next state.

Required checks are represented as an exact duplicate-free partition of successful, pending, and failed check names whenever checks have been observed.

## Replay closure

The re-observation registry contains parallel unique histories of:

- consumed source execution receipt digests;
- consumed re-observation nonce digests.

An admitted adapter invocation consumes both entries regardless of whether the result is completed, failed, or quarantined. The next registry advances by exactly one revision and one consumed count.

## Fixed boundaries

```text
re-observation != effect execution
re-observation != correctness proof
re-observation != truth
fresh lifecycle state != next-effect lease
source failure != retry authority
source quarantine != no-effect proof
checks successful != correctness
merge observed != truth
unused observation budget != reusable authority
receipt != general Git authority
receipt != deployment authority
receipt != general successor-stage authority
```

The stage performs no Git write, ref mutation, commit, push, PR mutation, merge, deployment, secret access, network access, or human/external handover.

## Artifacts

- runtime: `runtime/kuuos_codeai_autonomous_git_effect_reobservation_v0_1.py`
- checker: `scripts/check_codeai_autonomous_git_effect_reobservation_v0_1.py`
- tests: `tests/test_kuuos_codeai_autonomous_git_effect_reobservation_v0_1.py`
- example: `examples/codeai_autonomous_git_effect_reobservation_v0_1.json`
- manifest: `manifests/kuuos_codeai_autonomous_git_effect_reobservation_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/AutonomousGitEffectReobservationV0_1.lean`
- formal root: `formal/KuuOSCodeAIAutonomousGitEffectReobservationV0_1.lean`
- workflow: `.github/workflows/codeai-autonomous-git-effect-reobservation-v0-1.yml`
