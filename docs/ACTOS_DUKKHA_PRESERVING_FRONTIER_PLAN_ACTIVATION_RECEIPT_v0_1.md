# ActOS苦低減保持frontier plan activation receipt kernel v0.1

## 位置づけ

このkernelはActOS v0.7のplan activation層である。

入力はActOS v0.6が発行した単回activation authorization receiptと、activation時点のWORLD、token消費履歴、frontier activation履歴を束縛したactivation contextである。

この層は現在のfrontierを`bound_not_invoked`から`activated_not_invoked`へ遷移させる。

ただし、adapter invocation、tool invocation、外部作用、persistent WORLD mutationは行わない。

## Source authorization

ActOS v0.6 receiptについて次を再検証する。

```text
authorization disposition = activation_authorization_ready
activation authorization admitted = true
authorization receipt issued = true
single-use authorization reserved = true
activation authorization token digest
authorization record digest
frontier candidate ID
frontier adapter ID
frontier binding digest
frontier lease ID
WORLD binding and state
session, intent, nonce
remaining-use reservation arithmetic
```

source receiptがready以外のdispositionである場合はactivationしない。

source receiptがadapter invocation、tool invocation、外部作用、execution permissionへ昇格している場合もfail-closedとする。

## 単回authorizationの消費

ActOS v0.6では一回分のauthorizationを予約した。

ActOS v0.7はそのauthorization tokenをactivation時に消費済みとして記録する。

```text
activation_authorization_consumed = true
activation_authorization_token_marked_consumed = true
single_use_authorization_replay_closed = true
```

同じtokenを二回目のactivationに使用することはできない。

authorization tokenの消費はadapter leaseの使用回数消費ではない。

```text
adapter_lease_use_consumed = false
adapter_registry_snapshot_unchanged = true
```

adapter leaseは実際のadapter invocation段階まで消費しない。

## Activation context

activation contextは次を保持する。

```text
source authorization receipt digest
activation token digest
frontier candidate ID
frontier binding digest
frontier adapter ID
frontier lease ID
session ID
intent digest
authorization nonce digest
current WORLD binding digest
current WORLD state digest
current WORLD revision
current WORLD lineage digest
authorization receipt observed epoch
activation epoch
maximum activation delay
prior consumed authorization tokens
prior activated frontier candidates
requested state transition digest
exact activation cycle digest
```

context自体もdigest-boundである。

## WORLDと時間境界

activation時点のWORLDはsource authorization receiptが束縛したWORLDと一致しなければならない。

```text
current WORLD binding = source WORLD binding
current WORLD state = source WORLD state
current WORLD revision = source WORLD revision
current WORLD lineage = source WORLD lineage
```

不一致の場合はactivationせず、ActOS v0.6以前の再authorization経路へ戻す。

authorization receipt観測からactivationまでの遅延は、明示された有限上限以内でなければならない。

```text
0 <= activation epoch - authorization observed epoch
activation epoch - authorization observed epoch <= maximum activation delay
```

期限を越えたauthorizationは再利用しない。

## Exact activation cycle

次を一つのexact activation cycle digestへ束縛する。

```text
source authorization receipt digest
source authorization record digest
activation token digest
frontier candidate
frontier binding
frontier adapter
frontier lease
session
intent
nonce
activation epoch
WORLD revision
requested state transition
```

これにより、別frontier、別binding、別WORLD revisionへのtoken転用を防ぐ。

## Frontier state transition

許される状態遷移は一つだけである。

```text
bound_not_invoked
→ activated_not_invoked
```

次を保証する。

```text
plan_activation_performed = true
frontier_candidate_activated = true
exactly_one_frontier_activated = true
activation_frontier_sequence_preserved = true
completed_prefix_preserved = true
later_candidates_remain_inactive = true
```

後続candidateを先にactivationすることはできない。

activation済みfrontierを同じcycleで再activationすることもできない。

## Adapter invocationとの分離

plan activationはadapter invocationではない。

```text
adapter_invocation_intake_admitted = true
adapter_invocation_performed = false
tool_invocation_performed = false
external_side_effect_performed = false
execution_authority_granted = false
execution_permission = false
persistent_world_state_unchanged = true
active_now = false
```

`adapter_invocation_intake_admitted`は後続のinvocation intakeへ進めることを表す。

実行権限や外部作用の開始を表さない。

## 苦低減と関係構造の保持

activationによって苦評価を再計算し、adapter都合の単一効用へ置き換えない。

次を保持する。

```text
dukkha_reduction_support_preserved
protected_group_nonexternalization_preserved
future_nonexternalization_preserved
revision_capacity_preserved
persistent_loop_reduction_preserved
single_scalar_utility_not_introduced
alternative_candidates_preserved
dissent_preserved
minority_preserved
```

選択されなかった候補と異論は、activation後も改訂可能性としてlineage上に残る。

## 権限境界

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false
```

ActOS v0.7は既にauthorizationされたfrontierをactivationする。

候補を再選択せず、計画を改訂せず、苦最小化権限を取得しない。

## Fail-closed条件

次の場合はactivation receiptを発行しない。

- source authorization receiptが存在しない。
- source receipt digestが不正または期待値と不一致である。
- authorization dispositionがreadyではない。
- authorization tokenまたはauthorization record digestが不正である。
- frontier bindingが一意でない、またはdigestが不正である。
- tokenが既に消費されている。
- frontierが既にactivationされている。
- WORLD binding、state、revision、lineageが変化している。
- authorization delayが上限を越えている。
- session、intent、nonceがsource authorization recordと一致しない。
- requested state transition digestが一致しない。
- exact activation cycle digestが一致しない。
- activation bundle digestが一致しない。
- source receiptが既にadapter invocationまたはexecutionへ昇格している。

## Lean形式化

```text
ready_authorization_is_required_for_frontier_activation
frontier_activation_consumes_single_use_authorization
frontier_activation_has_exact_noninvoked_transition
frontier_activation_preserves_sequence_and_later_inactivity
frontier_activation_preserves_dukkha_and_nonexternalization
frontier_activation_preserves_alternatives_dissent_and_minority
frontier_activation_preserves_lineage_and_responsibility
frontier_activation_grants_no_selection_revision_or_minimization_authority
activation_does_not_consume_adapter_lease
plan_activation_is_not_adapter_invocation_or_execution
```

## 接続

```text
DecisionOS justified selection
→ PlanOS bounded synthesis
→ VerifyOS bounded plan verification
→ VerifyOS dukkha reduction claim verification
→ ActOS materialization intake
→ ActOS adapter binding and activation authorization intake
→ ActOS frontier plan activation receipt
```

次段は、`activated_not_invoked` frontierと未消費のadapter leaseを受け取り、bounded adapter invocation intakeを行う層である。

invocation receiptと外部効果の観測も、その後の別段階として分離する。
