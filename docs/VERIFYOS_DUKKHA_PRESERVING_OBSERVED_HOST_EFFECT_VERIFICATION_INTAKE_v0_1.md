# VerifyOS苦低減保持observed host-effect verification intake kernel v0.1

## 位置づけ

このkernelはVerifyOS v0.7のobserved host-effect verification intake層である。

ObserveOS v0.5が発行した`host_effect_observed_unverified` receiptを完全再検証し、独立verification review certificateへ束縛する。

このkernelはhost operationを再実行しない。

このkernelはobservationを再実施しない。

このkernelはtool invocationまたはexternal side effectを行わない。

verification receiptはverified WORLD factではない。

## Source条件

入力sourceはObserveOS v0.5 receiptでなければならない。

要求状態は次である。

```text
observation_state_after
= host_effect_observed_unverified
```

source receipt全体のdigestを再計算する。

次の内部artifactも再計算する。

```text
independent observation evidence packet
observation record
observation debt consumption record
verification handoff envelope
```

sourceが独立観測証拠を一件だけ記録済みであり、observation debtを一回消費し、verification debtを保持していることを要求する。

## Verification review certificate

独立verifierが発行するreview certificateを次へ束縛する。

```text
source observation receipt
observation record
verification handoff envelope
independent observation evidence packet
frontier candidate
frontier adapter
frontier binding
requested effect tags
observed value
uncertainty
calibration
provenance chain
```

certificateは次を含む。

```text
expected effect contract digest
verification method digest
verification evidence digest
dukkha impact assessment digest
protected-group impact assessment digest
future-subject impact assessment digest
verifier identity
bounded verification duration
```

certificateはWORLD factまたはcausal attributionを主張してはならない。

```text
world_fact_claimed = false
causal_attribution_claimed = false
```

## Verification disposition

構造、schema、digest、source bindingの破損はfail-closedとする。

構造が有効なintakeは次の一つへrouteする。

```text
effect_verification_supported
world_refresh_required
verification_context_refresh_required
verification_review_refresh_required
additional_observation_required
calibration_repair_required
provenance_repair_required
effect_contract_repair_required
nonexternalization_review_required
dukkha_preservation_contradicted
replay_conflict_rejected
```

supported以外のrouteをgeneric denialへ圧縮しない。

## Supported transition

supportedの場合だけ次の状態遷移を許す。

```text
host_effect_observed_unverified
-> host_effect_verified_world_not_updated
```

supported verificationは次を表す。

```text
effect conformance verified
dukkha preservation verified
protected-group nonexternalization verified
future-subject nonexternalization verified
```

ただし次は表さない。

```text
WORLD fact confirmed
causal attribution confirmed
dukkha reduction realized confirmed
WORLD model updated
```

## Non-supported routes

supported以外では状態を維持する。

```text
host_effect_observed_unverified
-> host_effect_observed_unverified
```

verification debtを消費しない。

fresh review、追加観測、calibration repair、provenance repair、effect contract repair、nonexternalization reviewの経路を保持する。

## Single-useとreplay exclusion

verification intake session、review certificate、verification nonceを独立にreplay検査する。

supportedの場合だけsource observation receiptとverification debtを一回消費する。

```text
verification_debt_consumed = true
verification_debt_replay_closed = true
source_observation_receipt_replay_closed = true
verification_double_consumed = false
```

non-supported routeではsource observation receiptを閉じず、修復後のfresh verificationを可能にする。

## WORLD境界

supported verificationでもWORLD modelを更新しない。

```text
persistent_world_model_state_unchanged = true
world_fact_confirmed = false
causal_attribution_confirmed = false
dukkha_reduction_realized_confirmed = false
world_disposition_completed = false
```

supportedの場合だけ次層のWORLD disposition intakeを開く。

```text
world_disposition_intake_admitted = true
world_disposition_receipt_required = true
```

WORLD disposition intakeは別receiptである。

## 自動作用の禁止

次を禁止する。

```text
host_operation_reexecuted = false
observation_reperformed = false
tool_invocation_performed = false
external_side_effect_performed = false
automatic_truth_promotion = false
automatic_plan_completion = false
automatic_rollback = false
automatic_compensation = false
compensation_performed = false
```

## 苦低減保持

source chainの次を保持する。

```text
dukkha reduction support
protected-group nonexternalization
future-subject nonexternalization
revision capacity
persistent-loop reduction
effect scope
effect ceiling
checkpoint guards
stop conditions
alternatives
dissent
minority evidence
evidence lineage
responsibility lineage
```

verification結果をsingle scalar utilityへ圧縮しない。

supported verificationは計画時の苦低減claimが現実に達成されたことを自動確定しない。

## Authority boundary

DecisionOSはselection ownershipを保持する。

```text
selection_authority_granted_to_verifyos = false
plan_revision_authority_granted_to_verifyos = false
dukkha_minimization_authority_granted_to_verifyos = false
general_execution_authority_granted = false
execution_permission = false
world_mutation_authority_granted = false
active_now = false
```

verification能力は選択、計画改訂、苦最小化、実行、WORLD mutationの権限を発生させない。

## Fail-closed条件

次の場合はreceiptを発行しない。

- source receiptが欠損している場合。
- source receiptまたは内部artifact digestが一致しない場合。
- source stateが`host_effect_observed_unverified`でない場合。
- sourceがverification済みまたはWORLD fact確定済みを主張する場合。
- review certificateが欠損している場合。
- certificate schemaまたはdigestが一致しない場合。
- observation、frontier、effect tags、value、uncertainty、calibration、provenanceのbindingが一致しない場合。
- verifier、method、evidence、impact assessmentが欠損している場合。
- certificateがWORLD factまたはcausal attributionを主張する場合。
- context schema、digest、operation、cycle、bundleが一致しない場合。

WORLD drift、stale context、stale review、evidence不足、repair requirement、replay conflictは有効なroute receiptとして保持する。

## Lean形式化

形式層では次を証明する。

- ObserveOS receiptがverification intakeの前提であること。
- supported verificationだけが`host_effect_verified_world_not_updated`へ遷移すること。
- non-supported routeがobserved-unverified状態とverification debtを保持すること。
- review method、evidence、effect contract、dukkha impact、protected-group impact、future-subject impactが束縛されること。
- supported verificationがverification debtを一回だけ消費すること。
- verification receiptがWORLD fact、因果帰属、実現済み苦低減ではないこと。
- host operation、observation、tool、external effectを再実行しないこと。
- automatic truth、completion、rollback、compensationを禁止すること。
- 苦低減、非外部化、alternatives、dissent、minority、lineage、responsibilityを保持すること。
- selection、revision、minimization、execution、WORLD authorityを付与しないこと。

## 次層

次の自然な層はWORLD dukkha-preserving verified host-effect disposition intakeである。

次の分離を維持する。

```text
host-effect receipt
!= observation receipt
!= verification receipt
!= verified WORLD fact
!= WORLD mutation authorization
```
