# WORLD Dukkha-Preserving Verified Host-Effect Disposition Intake v0.1

## 目的

この層は、VerifyOS v0.7が支持した外部host effectを、WORLDへ直接書き込まず、単一のWORLD candidateへ変換する。

入力状態は`host_effect_verified_world_not_updated`である。

ready経路の出力状態は`verified_host_effect_world_candidate_prepared_not_committed`である。

WORLD candidateは`prepared_not_committed`であり、WORLD factでもWORLD mutation authorizationでもない。

## 責任境界

この層が行う処理は次である。

- VerifyOS v0.7 receipt全体の再検証
- verification recordの再検証
- verification debt consumption recordの再検証
- WORLD disposition handoff envelopeの再検証
- 独立WORLD disposition review certificateの束縛
- current WORLD bindingとrevisionの再確認
- WORLD candidateの準備
- 後続commit authorization intakeへのhandoff

この層は次を行わない。

- persistent WORLD modelの更新
- WORLD factの確定
- causal attributionの確定
- 実現した苦低減の確定
- host operationの再実行
- observationまたはverificationの再実行
- tool invocation
- external side effect
- plan completion
- rollback
- compensation

## 入力条件

source VerifyOS receiptは次を満たす必要がある。

- `verification_disposition = effect_verification_supported`
- `verification_state_after = host_effect_verified_world_not_updated`
- `verification_completed = true`
- `effect_conformance_verified = true`
- `dukkha_preservation_verified = true`
- `protected_group_nonexternalization_verified = true`
- `future_nonexternalization_verified = true`
- `verification_debt_consumed = true`
- `world_disposition_intake_admitted = true`
- `persistent_world_model_state_unchanged = true`
- `world_fact_confirmed = false`
- `causal_attribution_confirmed = false`
- `dukkha_reduction_realized_confirmed = false`

source receipt digest、verification record digest、verification debt consumption record digest、WORLD disposition handoff envelope digestを再計算する。

## WORLD disposition review certificate

review certificateは次へ束縛される。

- source verification receipt
- verification record
- WORLD disposition handoff envelope
- frontier materialization candidate
- frontier adapter
- frontier binding
- requested effect tags
- observed value
- uncertainty
- calibration
- provenance
- WORLD candidate fact
- WORLD candidate relation
- WORLD update patch
- update precondition
- update postcondition
- causal model claim
- realized dukkha assessment
- protected-group realized impact
- future-subject realized impact
- reviewer identity

WORLD candidate factは候補表現であり、真理値を昇格させない。

causal model claimは検査対象であり、因果確定ではない。

realized dukkha assessmentは検査対象であり、苦低減の実現確認ではない。

## disposition

有効なintakeは次の13経路へ分かれる。

- `world_candidate_admission_ready`
- `world_refresh_required`
- `world_disposition_context_refresh_required`
- `world_disposition_review_refresh_required`
- `additional_observation_required`
- `verification_repair_required`
- `calibration_repair_required`
- `provenance_repair_required`
- `world_patch_repair_required`
- `nonexternalization_review_required`
- `dukkha_realization_review_required`
- `truth_promotion_rejected`
- `replay_conflict_rejected`

schema、digest、source bindingの破損はroute receiptを発行せずfail closedとする。

## ready経路

`world_candidate_admission_ready`だけが次の遷移を許す。

```text
host_effect_verified_world_not_updated
→
verified_host_effect_world_candidate_prepared_not_committed
```

ready経路では、exactly one WORLD candidateを準備する。

candidate envelopeは次を保持する。

- source verification receipt digest
- verification record digest
- disposition record digest
- frontier identity
- requested effect tags
- observed value
- uncertainty
- calibration
- provenance
- candidate fact digest
- candidate relation digest
- update patch digest
- update precondition digest
- update postcondition digest
- causal model claim digest
- realized dukkha assessment digest

candidate stateは`prepared_not_committed`である。

WORLD fact stateは`candidate_only_not_fact`である。

causal attribution stateは`not_confirmed`である。

dukkha realization stateは`not_confirmed`である。

後続のWORLD commit authorization intakeだけをadmitする。

## non-ready経路

non-ready経路は入力状態を保持する。

```text
host_effect_verified_world_not_updated
→
host_effect_verified_world_not_updated
```

この場合、WORLD candidateを発行しない。

WORLD disposition debtはopenのまま保持する。

source verification receiptのdisposition replayも閉じない。

## single-use semantics

ready経路だけが次を行う。

- WORLD disposition debtの消費
- source verification receiptのdisposed marking
- source verification receipt replayのclose
- WORLD candidate envelopeの発行

review certificateとintake nonceは各intakeでsingle-useとして消費する。

double dispositionは常にfalseである。

## 真理昇格の拒否

reviewが次を主張する場合は`truth_promotion_rejected`へ送る。

- WORLD fact確定
- causal attribution確定
- realized dukkha reduction確定

したがって、次の不等式を保持する。

```text
verification receipt
!= WORLD candidate
!= WORLD fact
!= causal truth
!= realized dukkha confirmation
!= WORLD commit authorization
!= WORLD mutation
```

## 苦保持

この層は次を保持する。

- dukkha reduction support
- protected-group nonexternalization
- future-subject nonexternalization
- revision capacity
- persistent-loop reduction
- alternative candidates
- dissent
- minority evidence
- evidence lineage
- responsibility lineage

これらを単一scalar utilityへ縮約しない。

## 権限境界

DecisionOSはselection ownershipを保持する。

WORLD disposition intakeには次の権限を付与しない。

- selection authority
- plan revision authority
- dukkha minimization authority
- general execution authority
- execution permission
- WORLD mutation authority

`active_now`はfalseのままである。

## 実装

runtime：

`runtime/kuuos_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1.py`

actual-chain checker：

`scripts/check_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1.py`

Lean theorem package：

`formal/KUOS/WORLD/DukkhaPreservingVerifiedHostEffectDispositionIntakeV0_54.lean`

formal root：

`formal/KuuOSWORLDV0_54.lean`

manifest：

`manifests/kuuos_world_dukkha_preserving_verified_host_effect_disposition_intake_v0_1.json`

## 次層

次の自然な層は、prepared WORLD candidateに対するsingle-use commit authorization intakeである。

その層もauthorizationだけを扱い、persistent WORLD mutationはさらに後続のatomic commit receiptへ分離する。
