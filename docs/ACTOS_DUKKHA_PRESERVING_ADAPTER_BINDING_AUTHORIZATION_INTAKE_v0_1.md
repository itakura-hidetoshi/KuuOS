# ActOS苦低減保持adapter binding・activation authorization intake kernel v0.1

## 位置づけ

このkernelはActOS v0.6のadapter bindingとactivation authorization intake層である。

入力はActOS v0.5が発行したmaterialization intake receipt、adapter registry snapshot、候補ごとのadapter binding、現在のWORLDとfreshnessを表すauthorization contextである。

この層はadapterを束縛し、現在のactivation frontierに対して単回authorizationの可否を判定する。

ただし、plan activation、adapter invocation、tool invocation、外部作用、persistent WORLD mutationは行わない。

## Source receipt

ActOS v0.5 receiptについて次を再検証する。

```text
receipt digest
materialization candidate set digest
candidate digest
candidate sequence
candidate state = prepared_not_activated
adapter binding digest = empty
checkpoint
stop condition
evidence lineage
dukkha support
protected group nonexternalization
future nonexternalization
```

source receiptが既にactivationまたはexecutionへ昇格している場合はfail-closedとする。

## Adapter registry

registry entryは次を持つ。

```text
adapter_id
adapter_class
supported_materialization_classes
capability_digest
scope_policy_digest
effect_ceiling_tags
active
revoked
lease_id
remaining_uses
entry_digest
```

registry snapshotと各entryはdigest-boundである。

adapter bindingは候補のmaterialization classをsupportしなければならない。

requested effect tagsはregistry effect ceilingの部分集合でなければならない。

次のeffectは引き続き禁止する。

```text
active_now
candidate_substitution
execution_permission
external_side_effect
persistent_world_mutation
selection_authority_transfer
tool_invocation
unreviewed_scope_expansion
```

## 一対一binding

各materialization candidateへ一つのadapter bindingを要求する。

```text
materialization_candidate_id
adapter_id
adapter_registry_entry_digest
capability_digest
scope_digest
effect_ceiling_digest
lease_id
requested_effect_tags
binding_state = bound_not_invoked
binding_digest
```

binding順序はmaterialization candidate順序と一致する。

候補を省略、追加、並べ替え、別adapter classへ差し替えることはできない。

## Activation frontier

authorization contextは、完了済みmaterialization candidate IDを連続prefixとして保持する。

次のfrontierは、まだ完了していない最初のcandidateである。

```text
completed = [m1, ..., mk]
frontier = m(k+1)
```

途中のcandidateを飛ばして後続stepをauthorizationすることはできない。

frontier intent digestは、selected candidate、plan intent、frontier candidate、source action digestから再計算する。

## WORLDとfreshness

次をsource receiptと比較する。

```text
WORLD binding digest
WORLD model state digest
WORLD revision
WORLD lineage digest
```

一致しない場合は`world_refresh_required`へ分岐する。

freshnessは次で判定する。

```text
0 <= current epoch - source observed epoch
current epoch - source observed epoch <= maximum freshness age
```

freshness observation digestとexact act cycle digestも再計算する。

古いauthorization contextは`freshness_refresh_required`へ分岐する。

## Registryとlease

frontier adapterがinactiveまたはrevokedの場合は`adapter_registry_repair_required`となる。

frontier leaseのremaining usesが0の場合は`lease_refresh_required`となる。

authorizationが成立する場合だけ、一回分を予約する。

```text
remaining uses after reservation + 1
=
remaining uses before reservation
```

この予約はadapter invocationによる消費ではない。

```text
lease_use_consumed = false
adapter_registry_snapshot_unchanged = true
```

## Replay exclusion

次の三つを独立に再利用禁止とする。

```text
session_id
intent_digest
authorization_nonce_digest
```

過去に使用済みの値が含まれる場合は`replay_conflict_rejected`となる。

## 不可逆step

frontierがirreversibleの場合、先行checkpointだけではauthorizationに十分ではない。

そのstepに対する最新VerifyOS再検証digestを要求する。

欠落時は`verifyos_step_reverification_required`へ分岐する。

これにより、plan生成時の検証を不可逆step直前まで使い回さない。

## Authorization disposition

構造が正しい場合、次のいずれかを発行する。

```text
activation_authorization_ready
world_refresh_required
freshness_refresh_required
adapter_registry_repair_required
lease_refresh_required
replay_conflict_rejected
verifyos_step_reverification_required
```

`activation_authorization_ready`だけが次を満たす。

```text
activation_authorization_admitted = true
activation_authorization_receipt_issued = true
single_use_authorization_reserved = true
```

他のdispositionではauthorizationを発行しない。

ただし、source planや候補を消去せず、必要な戻り経路を明示する。

## 苦低減の保持

この層はadapter都合で苦評価を再最適化しない。

次を保持する。

```text
dukkha_reduction_support_preserved
protected_group_nonexternalization_preserved
future_nonexternalization_preserved
revision_capacity_preserved
persistent_loop_reduction_preserved
single_scalar_utility_not_introduced
```

adapterの可用性を理由に、少数側または未来主体へ苦を移転する計画へ差し替えない。

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false
adapter_binding_performed = true
plan_activated = false
adapter_invocation_performed = false
tool_invocation_performed = false
external_side_effect_performed = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
active_now = false
```

activation authorizationはactivationそのものではない。

adapter bindingはadapter invocationではない。

## Fail-closed条件

次の場合はrouting receipt自体を発行しない。

- source receiptまたはcandidate digestが不正である。
- source candidateがすでにadapter boundまたはactivatedである。
- registry snapshotまたはentry digestが不正である。
- bindingがcandidateと一対一でない。
- adapter classがmaterialization classをsupportしない。
- requested effectがeffect ceilingを越える。
- authorization context digestが不正である。
- completed candidateが連続prefixでない。
- requested frontierが次の未完了candidateと一致しない。
- exact intent、freshness observation、act cycle digestが一致しない。
- authorization bundle digestが一致しない。

## Lean形式化

```text
ready_disposition_admits_single_use_authorization
refresh_route_does_not_authorize
repair_replay_or_reverification_route_does_not_authorize
adapter_binding_preserves_candidate_bijection_and_frontier
adapter_binding_preserves_scope_checkpoint_stop_and_evidence
authorization_intake_preserves_dukkha_and_nonexternalization
authorization_intake_preserves_alternatives_dissent_and_minority
authorization_intake_preserves_lineage_and_responsibility
authorization_intake_grants_no_selection_revision_or_minimization_authority
activation_authorization_is_not_activation_invocation_or_execution
```

## 接続

```text
DecisionOS justified selection
→ PlanOS bounded synthesis
→ VerifyOS bounded plan verification
→ VerifyOS dukkha reduction claim verification
→ ActOS materialization intake
→ ActOS adapter binding and activation authorization intake
```

次段は、単回authorization receiptを受け取り、plan activationを独立receiptとして確定する層である。

その後もadapter invocationは別段階として分離する。
