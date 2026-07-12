# ActOS苦低減保持atomic external host-effect intake kernel v0.1

## 位置づけ

このkernelはActOS v0.11のatomic external host-effect intake層である。

ActOS v0.10が内部commitしたeffectを、外部host driverが実行した一件のbounded effectへ結び付ける。

このkernel自身はtoolを再実行しない。

このkernel自身は外部副作用を再発生させない。

外部host driverが発行したcanonical application receiptを検証し、KuuOS内部のhost-effect receiptへ記録する。

## Source条件

入力sourceはActOS v0.10 receiptでなければならない。

要求状態は次である。

```text
host_effect_state_before
= effect_committed_host_not_applied
```

sourceは次を満たさなければならない。

```text
effect_commit_performed = true
exactly_one_effect_proposal_committed = true
committed_effect_envelope_issued = true
external_host_effect_intake_admitted = true
external_host_effect_receipt_required = true
external_host_effect_performed = false
tool_invocation_performed = false
external_side_effect_performed = false
persistent_world_state_unchanged = true
```

source receipt全体のdigestを再計算する。

次の内部artifactも再計算する。

```text
effect_commit_record_digest
committed_effect_envelope_digest
authorization_consumption_record_digest
```

sourceの構造、digest、状態、authority boundaryが一致しない場合はfail-closedとする。

## External host application receipt

外部host driverはcanonical application receiptを発行する。

receiptは次へ束縛される。

```text
source effect commit receipt
commit record
committed effect envelope
frontier candidate
frontier adapter
frontier binding
requested effect tags
host operation
host target
host driver
```

receiptは一件のbounded effectだけを表す。

```text
exactly_one_effect_applied = true
host_effect_outcome = bounded_external_host_effect_applied
tool_invocation_performed = true
external_side_effect_performed = true
```

host driverの実行時間は有限上限を持つ。

開始epoch、完了epoch、最大durationを検証する。

完了epochが開始epochより前の場合は受理しない。

最大durationを超過したreceiptは受理しない。

## Kernelとhost driverの分離

host driverはtool invocationと外部副作用を実行した主体である。

ActOS v0.11 kernelはそのreceiptを検証する主体である。

したがって次を分離する。

```text
host_driver_tool_invocation_performed = true
host_driver_external_side_effect_performed = true

kernel_tool_invocation_performed = false
kernel_external_side_effect_performed = false
```

この分離により、receipt検証を外部作用の再実行として扱わない。

## Exact state transition

許される状態遷移は次の一つである。

```text
effect_committed_host_not_applied
-> host_effect_recorded_unobserved
```

この遷移はhost effectが記録されたことを表す。

この遷移はWORLD上の事実確認を表さない。

この遷移は因果帰属の確定を表さない。

## Atomicity

一つのcommitted effect envelopeから一つのexternal host-effect recordを生成する。

```text
exactly_one_external_host_effect_recorded = true
external_host_effect_receipt_issued = true
external_host_effect_performed = true
```

複数effectへの展開は行わない。

別candidateへの差し替えは行わない。

別adapterへの差し替えは行わない。

effect tagsの追加や削除は行わない。

## Single-use consumption

committed effect envelopeを一度だけ消費する。

```text
committed_effect_envelope_consumed = true
committed_effect_envelope_marked_applied = true
committed_effect_envelope_replay_closed = true
committed_effect_envelope_double_applied = false
```

次を独立にreplay検査する。

```text
host effect intake session
host application receipt
host effect intake nonce
committed effect envelope
source effect commit receipt
```

既使用の値を含む場合はreceiptを発行しない。

## WORLD model境界

external host stateには変化が記録される。

```text
persistent_host_state_changed = true
```

一方、KuuOSのWORLD modelはこの段階では更新しない。

```text
persistent_world_model_state_unchanged = true
world_fact_confirmed = false
causal_attribution_confirmed = false
```

host driver receiptは観測証拠ではない。

host driver receiptは検証済みWORLD dispositionではない。

host driver receiptをWORLD modelの真値へ自動昇格させない。

## ObserveOS handoff

host effect記録後はObserveOS intakeを開く。

```text
observation_intake_admitted = true
observation_receipt_required = true
observation_performed = false
independent_world_evidence_present = false
```

observation handoff envelopeは次を保持する。

```text
source effect commit receipt digest
committed effect envelope digest
host application receipt digest
external host-effect record digest
frontier identity
requested effect tags
```

ObserveOSは独立した観測証拠を収集する責任を持つ。

ActOSは観測結果を生成しない。

## VerifyOS debt

検証は観測後の別層で行う。

```text
verification_intake_required = true
verification_intake_admitted = false
verification_completed = false
verification_debt_open = true
```

観測receiptがない段階ではVerifyOS intakeへ昇格しない。

## Compensation boundary

compensation routeは保持する。

```text
compensation_route_ready = true
compensation_performed = false
```

host effect記録だけを理由に自動rollbackしない。

観測や検証の失敗だけを推測して自動補償しない。

## 自動昇格の禁止

次を禁止する。

```text
automatic_truth_promotion = false
automatic_plan_completion = false
automatic_rollback = false
```

host effectが記録されてもplan全体は完了しない。

観測と検証が完了するまでverification debtを閉じない。

## 苦低減の保持

sourceでsupportされた苦低減claimを保持する。

```text
dukkha_reduction_support_preserved = true
protected_group_nonexternalization_preserved = true
future_nonexternalization_preserved = true
revision_capacity_preserved = true
persistent_loop_reduction_preserved = true
single_scalar_utility_not_introduced = true
```

host driverの都合でeffect scopeを拡張しない。

host driverの都合でeffect ceilingを変更しない。

少数側や未来主体へ苦を転嫁する別effectを追加しない。

## Alternativesとdissent

次を保持する。

```text
alternative_candidates_preserved = true
dissent_preserved = true
minority_preserved = true
evidence_lineage_preserved = true
```

host effect記録によってunselected alternativeを削除しない。

異論と少数側証拠を実行成功の物語へ圧縮しない。

## Authority boundary

DecisionOSはselection ownershipを保持する。

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_actos = false
plan_revision_authority_granted_to_actos = false
dukkha_minimization_authority_granted_to_actos = false
```

一件のbounded host-effect authorityは消費済みとして閉じる。

```text
bounded_host_effect_authority_consumed = true
general_execution_authority_granted = false
execution_permission = false
world_mutation_authority_granted = false
active_now = false
```

external host effectの完了は一般実行権限を新たに発生させない。

## Fail-closed条件

次の場合はreceiptを発行しない。

- source receiptが欠損している場合。
- source digestが一致しない場合。
- source内部artifact digestが一致しない場合。
- sourceが既にhost effect実行済みを主張する場合。
- committed effect envelopeがnot-applied状態でない場合。
- host application receiptが欠損している場合。
- host application receipt digestが一致しない場合。
- candidate、adapter、binding、effect tagsがsourceと一致しない場合。
- host operation digestが一致しない場合。
- exactly-one条件が成立しない場合。
- host durationが上限を超える場合。
- WORLD binding、state、revision、lineageが変化した場合。
- intake delayが上限を超える場合。
- session、receipt、nonce、committed envelopeのreplayが検出された場合。
- bundle digestが一致しない場合。

## Lean形式化

形式層では次を証明する。

- committed effectがhost-effect intakeの前提であること。
- exact unobserved transitionが成立すること。
- committed effect envelopeが一回だけ消費されること。
- receipt、nonce、source replayが閉じられること。
- exactly one external host effectが記録されること。
- host driver effectとkernel非実行が分離されること。
- WORLD modelと事実確認が未更新であること。
- observationとverification debtが残ること。
- automatic truth promotion、completion、rollbackが禁止されること。
- 苦低減と非外部化が保持されること。
- alternatives、dissent、minorityが保持されること。
- lineageとresponsibilityが単調に保持されること。
- selection、revision、minimization authorityが付与されないこと。
- bounded host-effect authorityの消費が一般実行権限へ昇格しないこと。

## 次層

次の自然な層はObserveOSの外部host-effect observation intakeである。

次層は`host_effect_recorded_unobserved`を受け取り、独立観測証拠とprovenanceを束縛する。

次の分離を維持する。

```text
external host-effect receipt
!= observation receipt
!= verification receipt
!= verified WORLD disposition
```
