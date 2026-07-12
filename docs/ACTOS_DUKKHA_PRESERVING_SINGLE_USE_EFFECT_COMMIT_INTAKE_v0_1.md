# ActOS苦低減保持single-use effect commit intake kernel v0.1

## 位置づけ

このkernelはActOS v0.10のsingle-use effect commit層である。

入力はActOS v0.9が発行したreadyなeffect commit authorization receiptである。

v0.9はeffect commitを許可しただけであり、effect自体はまだcommitしていない。

v0.10は予約された単回authorization tokenを一度だけ消費し、adapter result envelopeを内部effect commit recordへ固定する。

ただし、external host effect、tool invocation、外部副作用、persistent WORLD mutation、ObserveOS observation、VerifyOS verification completionは行わない。

## Source authorizationの再検証

ActOS v0.9 receiptについて次を再検証する。

```text
authorization disposition = effect_commit_authorization_ready
effect commit state after = authorized_not_committed
effect commit authorization admitted = true
effect commit authorization receipt issued = true
single-use effect commit authorization reserved = true
effect commit intake admitted = true
effect commit performed = false
```

source receipt全体のdigestを再計算する。

次の内部recordも再計算する。

```text
effect commit authorization record digest
effect commit authorization token digest
adapter result envelope digest
```

authorization recordは正確なsource invocation、adapter result envelope、frontier candidate、adapter、binding、review certificate、authorization contextへ束縛される。

token digestはauthorization record、record digest、authorization policy、authorization requestへ束縛される。

これらが一致しない場合はcommit receiptを発行しない。

## Effect commit context

v0.10のeffect commit contextは次を束縛する。

```text
source effect commit authorization receipt digest
source invocation receipt digest
effect commit authorization record digest
effect commit authorization token digest
adapter result envelope digest
current WORLD binding
current WORLD state
current WORLD revision
current WORLD lineage
authorization receipt observed epoch
effect commit epoch
maximum effect commit delay
effect commit session ID
effect commit nonce digest
prior consumed authorization token digests
prior effect commit nonce digests
prior committed authorization receipt digests
requested effect commit operation digest
exact effect commit cycle digest
```

context全体はdigest-boundである。

WORLD条件が変化した場合はcommitしない。

authorization receiptが時間境界を越えた場合もcommitしない。

## Exact operation binding

requested effect commit operation digestは次を束縛する。

```text
source authorization receipt
source invocation receipt
authorization record
authorization token
adapter result envelope
frontier candidate
frontier adapter
frontier binding
requested effect tags
state before
state after
```

別candidate、別adapter、別binding、別effectへ差し替えることはできない。

## 状態遷移

この層が許す状態遷移は一つだけである。

```text
authorized_not_committed
→ effect_committed_host_not_applied
```

このcommitはActOS内部のeffect commitmentである。

外部hostへ作用が適用されたことを意味しない。

## Single-use authorizationの消費

v0.9が予約したauthorization tokenを一度だけ消費する。

```text
effect_commit_authorization_consumed = true
effect_commit_authorization_token_marked_consumed = true
single_use_effect_commit_authorization_replay_closed = true
effect_commit_authorization_double_consumed = false
```

次も一回限りとする。

```text
effect commit nonce
source authorization receipt
```

既に消費されたtoken、使用済みnonce、commit済みsource authorization receiptはfail-closedとする。

## Effect commit record

commit成立時に次を発行する。

```text
effect commit record
committed effect envelope
authorization consumption record
```

effect commit recordはauthorization、token、adapter result envelope、session、nonce、operation、cycle、commit epochを束縛する。

committed effect envelopeは次を明示する。

```text
effect_commit_state = committed
external_host_effect_state = not_applied
observation_state = not_observed
verification_state = verification_debt_open
external_host_effect_intake_required = true
external_host_effect_receipt_required = true
observation_intake_required = true
verification_intake_required = true
compensation_route_ready = true
```

## Exactly one effect commit

現在のfrontierに対応する一つのeffect proposalだけをcommitする。

```text
exactly_one_effect_proposal_committed = true
effect_commit_receipt_issued = true
committed_effect_envelope_issued = true
effect_commit_performed = true
```

後続candidateの選択や計画変更は行わない。

## External host effectとの分離

v0.10はexternal host effect intakeを次段へ渡す。

```text
external_host_effect_intake_admitted = true
external_host_effect_receipt_required = true
```

しかし、次はすべてfalseのままである。

```text
external_host_effect_performed
tool_invocation_performed
external_side_effect_performed
persistent_world_state_changed
```

したがって、effect commit receiptはexternal host effect receiptではない。

## ObserveOSとVerifyOSとの分離

commit後も観測と検証は未完了である。

```text
observation_intake_required = true
observation_performed = false
verification_intake_required = true
verification_completed = false
verification_debt_open = true
```

ActOS内部commitをWORLD上の事実として扱わない。

## 苦低減の保持

v0.10は苦評価を再計算して別の目的関数へ置き換えない。

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

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false
execution_authority_granted = false
execution_permission = false
active_now = false
```

ActOS内部commitはexecution authorityを発生させない。

WORLD mutation authorityも発生させない。

## Fail-closed条件

次の場合はcommit receiptを発行しない。

- ActOS v0.9 receiptが存在しない。
- source receiptがready authorizationではない。
- source receipt digestが一致しない。
- authorization record digestが一致しない。
- authorization token digestが一致しない。
- adapter result envelope digestが一致しない。
- effect commit contextが存在しない。
- context schemaまたはdigestが一致しない。
- WORLD binding、state、revision、lineageが変化している。
- effect commit delayが上限を超える。
- authorization tokenが再利用されている。
- effect commit nonceが再利用されている。
- source authorization receiptが再commitされている。
- requested operation digestが一致しない。
- exact cycle digestが一致しない。
- bundle digestが一致しない。
- source境界がすでにeffect commitへ昇格している。

## Lean形式化

次を形式化する。

```text
ready_authorization_is_required_for_single_use_effect_commit
single_use_effect_commit_has_exact_transition
effect_commit_consumes_single_use_authorization_once
effect_commit_closes_nonce_and_source_replay
effect_commit_records_exactly_one_committed_envelope
effect_commit_prepares_host_handoff_without_host_effect
effect_commit_preserves_observation_and_verification_debt
effect_commit_preserves_dukkha_and_nonexternalization
effect_commit_preserves_alternatives_dissent_and_minority
effect_commit_preserves_lineage_and_responsibility
effect_commit_grants_no_selection_revision_or_minimization_authority
internal_effect_commit_is_not_execution_or_active_world_mutation
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
→ ActOS single-use effect commit intake
```

次段はcommitted effect envelopeを受け取り、外部host effectを独立したatomic receiptとして扱う層である。

その後にObserveOS observationとVerifyOS verificationを接続する。
