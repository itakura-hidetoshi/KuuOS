# ActOS苦低減保持bounded adapter invocation kernel v0.1

## 位置づけ

このkernelはActOS v0.8のbounded adapter invocation層である。

入力はActOS v0.7が発行したfrontier plan activation receiptと、そのreceiptが束縛しているActOS v0.6 adapter binding authorization receiptである。

v0.7のfrontierは`activated_not_invoked`であり、adapter leaseの予約はまだ消費されていない。

この層は現在のfrontierに束縛されたadapterを一回だけ呼び出し、結果をeffect proposalとして記録する。

ただし、tool invocation、外部副作用、effect commit、persistent WORLD mutationは行わない。

## Source receiptの再検証

ActOS v0.7 receiptについて次を再検証する。

```text
activation receipt digest
activation record digest
source authorization receipt binding
activated frontier candidate
activated frontier adapter
activated frontier binding
activated frontier lease
activation state = activated_not_invoked
adapter invocation intake admitted = true
adapter lease use consumed = false
adapter invocation performed = false
```

ActOS v0.6 receiptも同時に提出させる。

これにより、v0.7 receiptがdigestだけで参照しているadapter binding、effect ceiling、lease reservation arithmeticを復元する。

v0.6 receiptについて次を再検証する。

```text
authorization receipt digest
authorization disposition = activation_authorization_ready
frontier binding digest
adapter ID
lease ID
requested effect tags
remaining uses before reservation
remaining uses after reservation
```

v0.7とv0.6のsource authorization receipt digestが一致しない場合はfail-closedとする。

## Invocation context

invocation contextは次を束縛する。

```text
source activation receipt digest
source authorization receipt digest
frontier candidate ID
frontier adapter ID
frontier binding digest
frontier lease ID
lease reservation digest
invocation session ID
invocation intent digest
invocation nonce digest
current WORLD binding
current WORLD state
current WORLD revision
current WORLD lineage
activation receipt observed epoch
invocation epoch
maximum invocation delay
requested operation digest
exact invocation cycle digest
```

context全体はdigest-boundである。

WORLD条件が変化した場合はinvocationを開始しない。

activation receiptが時間境界を越えた場合もinvocationを開始しない。

## Exact operation binding

requested operation digestは次を束縛する。

```text
activated frontier candidate
adapter ID
binding digest
lease ID
capability digest
scope digest
effect ceiling digest
requested effect tags
state before
state after
```

adapterの可用性を理由に、別candidate、別adapter、別scope、別effectへ差し替えることはできない。

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

## 状態遷移

この層が許す状態遷移は一つだけである。

```text
activated_not_invoked
→ invoked_effect_not_committed
```

adapter invocationが成立しても、effectはまだcommitされていない。

後続candidateは未invokeのまま保持する。

completed prefixも変更しない。

## Adapter invocation

この層はfrontier bindingが指定するbounded adapterを一回だけ呼び出す。

次を発行する。

```text
invocation record
adapter result envelope
lease consumption record
```

adapter result envelopeは次を明示する。

```text
invocation_outcome = bounded_effect_proposal_recorded
effect_commit_state = not_committed
external_effect_requested = false
tool_invocation_requested = false
observation_intake_required = true
verification_debt_open = true
```

したがって、adapter invocationの成功は外部作用の成功を意味しない。

adapter resultは観測と再検証を必要とする未commitの提案である。

## Lease reservationの消費

ActOS v0.6は一回分のlease useを予約している。

ActOS v0.8はその予約をadapter invocationに使用する。

```text
adapter_lease_reservation_consumed = true
adapter_lease_use_consumed = true
lease_consumption_record_issued = true
```

予約時にすでに次が成立している。

```text
remaining uses after reservation + 1
=
remaining uses before reservation
```

v0.8は同じuseを再度減算しない。

```text
remaining uses at invocation
=
remaining uses after reservation

adapter_lease_double_decremented = false
```

registry snapshot自体は履歴上の入力として不変に保つ。

lease消費は独立したconsumption recordへ記録する。

## Replay exclusion

次を一回限りとする。

```text
lease reservation digest
invocation nonce digest
frontier candidate ID
```

既に消費されたreservation、使用済みnonce、invocation済みfrontierはfail-closedとする。

## 苦低減の保持

adapter invocationは苦評価を再計算して別の目的関数へ置き換えない。

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

adapter都合によるcandidate再選択は行わない。

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false

adapter_invocation_performed = true
tool_invocation_performed = false
external_side_effect_performed = false
effect_commit_performed = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
active_now = false
```

adapter invocationはtool invocationではない。

adapter result envelopeの生成はeffect commitではない。

## Fail-closed条件

次の場合はinvocation receiptを発行しない。

- ActOS v0.7 receiptが存在しない。
- ActOS v0.6 receiptが存在しない。
- source receipt digestが一致しない。
- v0.7とv0.6のbindingが一致しない。
- frontierが`activated_not_invoked`ではない。
- adapter invocation intakeが受理されていない。
- adapter leaseがすでに消費されている。
- requested effectがeffect ceilingを越える。
- forbidden effectが含まれる。
- WORLD binding、state、revision、lineageが変化している。
- invocation delayが上限を超える。
- lease reservationが再利用されている。
- invocation nonceが再利用されている。
- frontierがすでにinvokeされている。
- operation digest、cycle digest、bundle digestが一致しない。

## Lean形式化

次を形式化する。

```text
activated_frontier_is_required_for_bounded_adapter_invocation
bounded_adapter_invocation_has_exact_uncommitted_transition
bounded_adapter_invocation_preserves_frontier_order
adapter_invocation_consumes_reserved_lease_once
adapter_invocation_closes_nonce_and_frontier_replay
adapter_invocation_records_effect_without_commit
adapter_invocation_preserves_dukkha_and_nonexternalization
adapter_invocation_preserves_alternatives_dissent_and_minority
adapter_invocation_preserves_lineage_and_responsibility
adapter_invocation_grants_no_selection_revision_or_minimization_authority
adapter_invocation_is_not_tool_external_effect_or_world_commit
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
```

次段は、未commitのadapter result envelopeを受け取り、effect commitの可否を独立に判定する層である。

その判定後も、外部host effect receiptとObserveOSによる観測を分離する。
