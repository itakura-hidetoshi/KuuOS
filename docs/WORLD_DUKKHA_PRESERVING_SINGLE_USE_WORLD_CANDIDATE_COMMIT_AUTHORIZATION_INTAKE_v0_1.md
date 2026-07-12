# WORLD Dukkha-Preserving Single-Use World-Candidate Commit Authorization Intake v0.1

## 目的

この層は、WORLD v0.60が準備した`prepared_not_committed` candidateを再検証し、単回かつ境界付きのcommit authorizationへ変換する。

この層はWORLD mutationを実行しない。

この層はWORLD fact、因果的真理、苦低減の実現確認を成立させない。

## 入力

入力状態は次である。

```text
verified_host_effect_world_candidate_prepared_not_committed
```

入力receiptはWORLD v0.60のready経路から発行される。

必須入力artifactは次である。

- WORLD disposition receipt
- WORLD disposition record
- WORLD disposition debt consumption record
- WORLD candidate envelope
- WORLD disposition review certificate
- evidence lineage
- responsibility lineage

## authorization review

authorization review certificateは、次を同一candidateへ束縛する。

- candidate fact digest
- candidate relation digest
- WORLD update patch digest
- update precondition digest
- update postcondition digest
- authorization scope digest
- authorization constraints digest
- authorization owner
- authorization expiry
- mutation application policy
- rollback route
- compensation route
- protected-group impact
- future-subject impact

reviewは、WORLD fact、causal attribution、realized dukkha reduction、WORLD mutationの実行を主張してはならない。

## ready遷移

ready経路の状態遷移は次である。

```text
verified_host_effect_world_candidate_prepared_not_committed
→
world_candidate_commit_authorized_not_applied
```

ready経路では次が成立する。

```text
world_candidate_commit_authorization_granted = true
bounded_world_candidate_commit_authorization_granted = true
single_use_world_candidate_commit_authorization_granted = true
world_mutation_application_intake_admitted = true
world_mutation_application_receipt_required = true
```

同時に次は未成立である。

```text
world_mutation_application_completed = false
world_candidate_commit_completed = false
persistent_world_model_state_unchanged = true
world_fact_confirmed = false
causal_attribution_confirmed = false
dukkha_reduction_realized_confirmed = false
world_mutation_authority_granted = false
execution_permission = false
active_now = false
```

`world_mutation_authority_granted = false`は、一般的または再利用可能なWORLD mutation authorityを付与しないことを表す。

ready経路で付与されるのは、同一candidate、同一patch、同一owner、同一expiryへ限定された単回authorizationだけである。

## mutation application handoff

ready経路では、後続層へ次のhandoffを発行する。

```text
authorization_state = authorized_single_use_not_applied
candidate_commit_state = authorized_not_applied
world_mutation_application_intake_admitted = true
world_mutation_application_receipt_required = true
single_use_authorization = true
```

handoffはmutation resultではない。

handoffはpersistent WORLD stateを書き換えない。

## disposition

有効なintakeは次のいずれかへrouteされる。

```text
world_candidate_commit_authorization_ready
world_refresh_required
world_commit_authorization_context_refresh_required
world_commit_authorization_review_refresh_required
world_commit_authorization_expired
world_candidate_revalidation_required
world_patch_repair_required
world_precondition_repair_required
world_postcondition_verification_repair_required
provenance_repair_required
authorization_owner_rejected
nonexternalization_review_required
dukkha_preservation_review_required
compensation_route_repair_required
truth_promotion_rejected
replay_conflict_rejected
```

non-ready経路では入力状態を保持する。

```text
verified_host_effect_world_candidate_prepared_not_committed
→
verified_host_effect_world_candidate_prepared_not_committed
```

この場合、authorization debtは開いたままであり、mutation application intakeは開かれない。

## replay closure

ready経路だけが次を消費する。

- authorization intake session
- authorization review certificate
- authorization nonce
- source WORLD candidate
- authorization debt

同一candidateの再authorizationは`replay_conflict_rejected`へrouteされる。

## 固定境界

```text
WORLD disposition receipt != WORLD candidate
WORLD candidate != WORLD candidate commit authorization
WORLD candidate commit authorization != WORLD mutation application
WORLD mutation application != WORLD fact
WORLD fact != causal truth
causal truth != realized dukkha confirmation
bounded single-use authorization != general WORLD mutation authority
authorization receipt != mutation application receipt
```

## 外部作用

この層は次を実行しない。

- host operation replay
- observation replay
- verification replay
- WORLD disposition replay
- tool invocation
- external side effect
- persistent host state mutation
- persistent WORLD state mutation
- rollback
- compensation
- automatic truth promotion

## 実装面

```text
runtime/kuuos_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1.py
scripts/check_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1.py
formal/KUOS/WORLD/DukkhaPreservingSingleUseWorldCandidateCommitAuthorizationIntakeV0_61.lean
formal/KuuOSWORLDV0_61.lean
manifests/kuuos_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1.json
```

## 次層

自然な後続層は、authorization receiptを単回消費するWORLD mutation application intakeである。

その層でも、mutation application、postcondition verification、WORLD fact promotion、causal attribution、realized dukkha confirmationを別artifactとして保持する。
