# ActOS苦低減保持effect commit authorization intake kernel v0.1

## 位置づけ

このkernelはActOS v0.9のeffect commit authorization intake層である。

入力はActOS v0.8が発行したbounded adapter invocation receiptと、未commit effect proposalに対するeffect commit review certificateである。

v0.8ではadapter invocationは完了しているが、effectは`invoked_effect_not_committed`に留まっている。

v0.9はeffect commitの可否を判定し、条件が満たされた場合だけ単回authorizationを予約する。

ただし、effect commit、tool invocation、外部副作用、persistent WORLD mutationは行わない。

## Source invocation receipt

ActOS v0.8 receiptについて次を再検証する。

```text
invocation receipt digest
invocation record digest
adapter result envelope digest
lease consumption record digest
invocation_state_after = invoked_effect_not_committed
adapter_invocation_performed = true
adapter_lease_use_consumed = true
effect_proposal_recorded = true
effect_commit_required = true
effect_commit_performed = false
external_side_effect_performed = false
persistent_world_state_unchanged = true
```

adapter result envelopeは次を保持しなければならない。

```text
invocation_outcome = bounded_effect_proposal_recorded
effect_commit_state = not_committed
external_effect_requested = false
tool_invocation_requested = false
observation_intake_required = true
verification_debt_open = true
```

source receiptまたは内部recordのdigestが一致しない場合はreceiptを発行しない。

## Effect commit review certificate

review certificateは次をsource invocationへ束縛する。

```text
source invocation receipt digest
adapter result envelope digest
invocation record digest
review disposition
dukkha reduction support status
protected group nonexternalization status
future nonexternalization status
revision capacity status
persistent loop reduction status
effect scope status
effect ceiling status
checkpoint status
stop condition status
compensation route status
observation route status
verification route status
review epoch
reviewer responsibility digest
```

ready authorizationには次が必要である。

```text
review_disposition = dukkha_preserving_effect_commit_supported
dukkha_reduction_support_status = supported
protected_group_nonexternalization_status = preserved
future_nonexternalization_status = preserved
revision_capacity_status = preserved
persistent_loop_reduction_status = preserved
effect_scope_status = exact
effect_ceiling_status = exact
checkpoint_status = satisfied
stop_condition_status = current
compensation_route_status = ready
observation_route_status = ready
verification_route_status = ready
```

review certificate全体はdigest-boundである。

## Authorization context

commit authorization contextは次を束縛する。

```text
source invocation receipt digest
adapter result envelope digest
effect commit review certificate digest
current WORLD binding
current WORLD state
current WORLD revision
current WORLD lineage
invocation receipt observed epoch
authorization epoch
maximum authorization delay
commit session ID
commit intent digest
commit authorization nonce digest
prior session IDs
prior nonce digests
prior authorized source digests
requested effect commit operation digest
exact authorization cycle digest
```

WORLDが変化した場合はauthorizationを発行しない。

時間境界を越えた場合はeffect再検証へ戻す。

session、nonce、source invocation receiptの再利用も拒否する。

## Authorization disposition

v0.9は次のdispositionへrouteする。

```text
effect_commit_authorization_ready
world_refresh_required
effect_reverification_required
checkpoint_review_required
observation_route_repair_required
verification_route_repair_required
compensation_route_repair_required
effect_scope_repair_required
replay_conflict_rejected
```

構造、digest、source bindingが壊れている場合はblockedとなり、route receipt自体を発行しない。

意味論的条件が不足する場合は理由付きdispositionを発行するが、authorization tokenは発行しない。

## Ready authorization

readyの場合だけ次を発行する。

```text
effect_commit_authorization_record
effect_commit_authorization_record_digest
effect_commit_authorization_token_digest
```

同時に次を固定する。

```text
effect_commit_authorization_admitted = true
effect_commit_authorization_receipt_issued = true
single_use_effect_commit_authorization_reserved = true
effect_commit_intake_admitted = true
```

状態は次へ進む。

```text
invoked_effect_not_committed
→ authorized_not_committed
```

この状態はeffect commit済みを意味しない。

## Non-ready route

ready以外では次を固定する。

```text
effect_commit_authorization_admitted = false
effect_commit_authorization_receipt_issued = false
single_use_effect_commit_authorization_reserved = false
effect_commit_authorization_token_digest = ""
effect_commit_intake_admitted = false
```

状態は`invoked_effect_not_committed`のままである。

## 苦低減の保持

v0.9は苦評価を別の単一効用へ置換しない。

次を保持する。

```text
dukkha_reduction_support_preserved
protected_group_nonexternalization_preserved
future_nonexternalization_preserved
revision_capacity_preserved
persistent_loop_reduction_preserved
single_scalar_utility_not_introduced
```

代替候補、異論、少数側証拠、evidence lineage、responsibility lineageも保持する。

adapter resultの可用性を理由にcandidateを再選択しない。

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false

adapter_invocation_performed = true
effect_commit_authorization_may_be_issued = true
effect_commit_performed = false
tool_invocation_performed = false
external_side_effect_performed = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
active_now = false
```

したがって、次は分離される。

```text
effect commit authorization
≠ effect commit
≠ external host effect
≠ WORLD observation
```

## Fail-closed条件

次の場合はroute receiptを発行しない。

- ActOS v0.8 receiptが存在しない。
- source receipt digestが一致しない。
- invocation record digestが一致しない。
- adapter result envelope digestが一致しない。
- lease consumption record digestが一致しない。
- effectがすでにcommitされている。
- toolまたは外部作用へ昇格している。
- review certificateのschemaまたはdigestが一致しない。
- review certificateのsource bindingが一致しない。
- authorization contextのschemaまたはdigestが一致しない。
- operation digest、cycle digest、bundle digestが一致しない。

## Lean形式化

次を形式化する。

```text
invoked_uncommitted_effect_is_required_for_commit_authorization
ready_commit_authorization_reserves_single_use_token_without_commit
nonready_commit_authorization_issues_no_authorization
ready_commit_authorization_requires_current_exact_routes
commit_authorization_preserves_dukkha_and_nonexternalization
commit_authorization_preserves_alternatives_dissent_and_minority
commit_authorization_preserves_lineage_and_responsibility
commit_authorization_grants_no_selection_revision_or_minimization_authority
effect_commit_authorization_is_not_commit_external_effect_or_execution
```

## 接続

```text
DecisionOS justified selection
→ PlanOS bounded synthesis
→ VerifyOS bounded plan verification
→ VerifyOS dukkha reduction claim verification
→ ActOS materialization intake
→ ActOS adapter binding and activation authorization intake
→ ActOS frontier plan activation
→ ActOS bounded adapter invocation
→ ActOS effect commit authorization intake
```

次段は、readyな単回authorization tokenを消費し、未commit effect proposalをhost effect commit intakeへ移す独立層である。

その層でも、effect commit receipt、外部host effect receipt、ObserveOS observation receiptを分離する。
