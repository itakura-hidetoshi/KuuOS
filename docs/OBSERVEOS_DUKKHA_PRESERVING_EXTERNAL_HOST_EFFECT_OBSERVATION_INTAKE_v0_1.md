# ObserveOS苦低減保持external host-effect observation intake kernel v0.1

## 位置づけ

このkernelはObserveOS v0.5のexternal host-effect observation intake層である。

ActOS v0.11が記録した一件のexternal host effectを、独立観測証拠とprovenanceへ束縛する。

このkernelはhost operationを再実行しない。

このkernelはtool invocationを行わない。

このkernelはexternal side effectを発生させない。

このkernelは観測receiptを発行するが、VerifyOS verification、WORLD fact確定、因果帰属確定を行わない。

## Source条件

入力sourceはActOS v0.11 receiptでなければならない。

要求状態は次である。

```text
host_effect_state_after
= host_effect_recorded_unobserved
```

source receipt全体のdigestを再計算する。

次の内部artifact digestも再計算する。

```text
external_host_effect_application_receipt_digest
external_host_effect_record_digest
committed_effect_consumption_record_digest
observation_handoff_envelope_digest
```

sourceはexternal host effectが一件だけ記録済みであることを要求する。

sourceはobservation未実施、independent evidence不在、verification未実施であることを要求する。

sourceのWORLD model非更新、非真理昇格、権限分離を再検証する。

## 独立観測証拠

観測証拠packetは次へ厳密に束縛する。

```text
source host-effect receipt
external host-effect record
observation handoff envelope
frontier candidate
frontier adapter
frontier binding
requested effect tags
host target
```

観測証拠packetは次を含む。

```text
collector identity
evidence source identity
collection start epoch
collection completion epoch
maximum collection duration
raw artifact digest
observed value digest
uncertainty digest
calibration digest
observation context digest
tamper-evidence digest
provenance chain digests
```

collectorはhost driverと独立でなければならない。

evidence sourceはhost receiptと独立でなければならない。

host receipt used as independent evidence = false

観測証拠は一件のhost effectに対するexactly one observationだけを表す。

## Freshnessとprovenance

collection durationは有限上限を持つ。

collection completion epochがstart epochより前の場合は受理しない。

maximum collection durationを超過した場合は受理しない。

provenance chainは非空、重複なし、canonical順序で保持する。

raw artifact、observed value、uncertainty、calibration、context、tamper evidenceの各digestを欠損させない。

## Exact state transition

許される状態遷移は次の一つである。

```text
host_effect_recorded_unobserved
-> host_effect_observed_unverified
```

この遷移はexternal host effectが独立証拠により観測されたことだけを表す。

この遷移はeffectが計画どおりであったことを表さない。

この遷移は苦低減が実現したことを表さない。

この遷移は因果関係が成立したことを表さない。

この遷移はWORLD factとして確定したことを表さない。

## Observation debtの単回消費

観測成立時にobservation debtを一度だけ消費する。

```text
observation_debt_consumed = true
source_host_effect_receipt_marked_observed = true
observation_double_consumed = false
```

次を独立にreplay検査する。

```text
observation intake session
observation evidence packet
observation intake nonce
source host-effect receipt
```

既使用値を含む場合はreceiptを発行しない。

## Observation receipt

receiptは次を発行する。

```text
observation record
observation debt consumption record
verification handoff envelope
```

exactly one observation receiptだけを発行する。

observation recordはsource identity、evidence identity、collector identity、state transitionを保持する。

verification handoff envelopeはobserved value、uncertainty、calibration、provenanceを保持する。

## Host driverとObserveOS kernelの分離

host effectはActOS v0.11より前に外部host driverが実行済みである。

ObserveOS v0.5はそのhost operationを再実行しない。

```text
host_operation_reexecuted = false
tool_invocation_performed = false
external_side_effect_performed = false
persistent_host_state_changed_by_observation = false
```

観測receipt検証を新たな外部作用として扱わない。

## WORLD model境界

観測証拠が存在してもKuuOS WORLD modelを更新しない。

```text
persistent_world_model_state_unchanged = true
world_fact_confirmed = false
causal_attribution_confirmed = false
```

observed valueはverified WORLD factではない。

uncertaintyとcalibrationを保持したままVerifyOSへ渡す。

## VerifyOS handoff

観測成立後にVerifyOS intakeを開く。

```text
verification_intake_required = true
verification_intake_admitted = true
verification_receipt_required = true
verification_completed = false
verification_debt_open = true
```

verification required = true

ObserveOSはverification verdictを生成しない。

ObserveOSは苦低減実現を判定しない。

ObserveOSは因果帰属を確定しない。

## 自動昇格と自動作用の禁止

次を禁止する。

```text
automatic_truth_promotion = false
automatic_plan_completion = false
automatic_rollback = false
automatic_compensation = false
compensation_performed = false
```

compensation routeは保持する。

観測receiptだけを理由にrollbackまたはcompensationを実行しない。

## 苦低減保持

sourceでsupportされた苦低減claimを保持する。

```text
dukkha_reduction_support_preserved = true
protected_group_nonexternalization_preserved = true
future_nonexternalization_preserved = true
revision_capacity_preserved = true
persistent_loop_reduction_preserved = true
single_scalar_utility_not_introduced = true
```

観測都合でeffect scopeまたはeffect ceilingを変更しない。

少数側または未来主体への外部化を追加しない。

## Alternatives、dissent、minority

次を保持する。

```text
alternative_candidates_preserved = true
dissent_preserved = true
minority_preserved = true
evidence_lineage_preserved = true
responsibility_lineage_preserved = true
```

観測値を理由にunselected alternativeを削除しない。

観測値を単一utilityへ圧縮しない。

異論と少数側証拠を保持する。

## Authority boundary

DecisionOSはselection ownershipを保持する。

```text
selection_remains_decisionos_owned = true
selection_authority_granted_to_observeos = false
plan_revision_authority_granted_to_observeos = false
dukkha_minimization_authority_granted_to_observeos = false
general_execution_authority_granted = false
execution_permission = false
world_mutation_authority_granted = false
active_now = false
```

観測能力は選択、計画改訂、苦最小化、一般実行、WORLD mutationの権限を発生させない。

## Fail-closed条件

次の場合はreceiptを発行しない。

- source receiptが欠損している場合。
- source receipt digestが一致しない場合。
- source内部artifact digestが一致しない場合。
- source stateが`host_effect_recorded_unobserved`でない場合。
- sourceがobservationまたはverification済みを主張する場合。
- independent observation evidence packetが欠損している場合。
- evidence packet digestが一致しない場合。
- collectorまたはevidence sourceの独立性が成立しない場合。
- host receiptをindependent evidenceとして代用した場合。
- host target、frontier identity、effect tagsがsourceと一致しない場合。
- collection durationが上限を超える場合。
- provenance chainが不正な場合。
- WORLD binding、state、revision、lineageが変化した場合。
- observation intake delayが上限を超える場合。
- session、evidence、nonce、source receiptのreplayが検出された場合。
- bundle digestが一致しない場合。

## Lean形式化

形式層では次を証明する。

- host-effect receiptがobservation intakeの前提であること。
- exact unverified transitionが成立すること。
- independent evidenceとprovenanceが束縛されること。
- exactly one observation receiptが発行されること。
- observation debt、nonce、source receiptのreplayが閉じられること。
- collector、host driver、kernel作用が分離されること。
- WORLD model非更新と非真理昇格が保持されること。
- VerifyOS intakeがadmitされ、verification debtが保持されること。
- automatic truth、completion、rollback、compensationが禁止されること。
- 苦低減と非外部化が保持されること。
- alternatives、dissent、minorityが保持されること。
- lineageとresponsibilityが単調に保持されること。
- selection、revision、minimization、execution、WORLD authorityが付与されないこと。

## 次層

次の自然な層はVerifyOS dukkha-preserving observed host-effect verification intakeである。

次層は`host_effect_observed_unverified`を受け取る。

次の分離を維持する。

```text
host-effect receipt
!= observation receipt
!= verification receipt
!= verified WORLD fact
```
