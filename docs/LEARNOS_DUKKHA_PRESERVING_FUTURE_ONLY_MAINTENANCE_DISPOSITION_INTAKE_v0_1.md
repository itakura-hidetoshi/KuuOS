# LearnOS v0.5 Dukkha-Preserving Future-Only Maintenance Disposition Intake v0.1

## 目的

この層は、VerifyOS v0.11が発行したmaintenance-disposition handoffを受理する。

検証済みmaintenance-monitoring observationに基づき、future-only maintenance dispositionだけを記録する。

current policyをactivateしない。

maintenance actionを実行しない。

policy activation reviewは独立した後続層へ分離する。

## 入力状態

唯一のsupported source stateは次である。

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending
```

sourceはVerifyOS v0.11のsupported receiptでなければならない。

sourceは次を保持する。

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = true
future_only_learning_delta_recorded = true
future_only_learning_delta_activated = false
maintenance_monitoring_observation_recorded = true
maintenance_monitoring_observation_verified = true
maintenance_monitoring_verification_completed = true
maintenance_disposition_handoff_prepared = true
maintenance_disposition_completed = false
maintenance_disposition_debt_open = true
```

## supported transition

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending_future_only_maintenance_disposition_recorded_policy_activation_review_pending
```

supported routeはbounded maintenance dispositionを一度だけ記録する。

supported routeはmaintenance-disposition debtを閉じる。

supported routeはpolicy-activation review handoffを`review_debt_open`で準備する。

## source再検証

LearnOSはVerifyOS v0.11 receipt digestを完全再検証する。

加えて次を独立に再検証する。

- maintenance-monitoring verification evidence packet
- maintenance-monitoring verification review certificate
- maintenance-monitoring verification record
- verification-debt consumption record
- maintenance-disposition handoff envelope
- WORLD fact、relation、state、revision
- future-only learning delta
- maintenance-policy candidate
- lineageおよびresponsibility lineage

## disposition evidence

独立evidence packetは次を束縛する。

- exact VerifyOS v0.11 receipt
- exact monitoring-verification record
- exact maintenance-disposition handoff
- bounded WORLD factとrelation
- WORLD stateとrevision
- future-only learning delta
- maintenance-policy candidate
- verified baseline observation
- verified durability
- verified adverse-effect assessment
- verified distributional assessment
- future-only maintenance objective
- no-op threshold
- escalation trigger
- reobservation schedule
- evidence-retention window
- uncertainty
- calibration
- provenance
- tamper evidence
- protected-group impact
- future-subject impact

## disposition

runtimeは20 dispositionを分離する。

1. `future_only_maintenance_disposition_supported`
2. `world_refresh_required`
3. `maintenance_disposition_context_refresh_required`
4. `maintenance_disposition_review_refresh_required`
5. `additional_maintenance_disposition_evidence_required`
6. `source_verifyos_receipt_correspondence_repair_required`
7. `monitoring_verification_record_correspondence_repair_required`
8. `maintenance_disposition_handoff_correspondence_repair_required`
9. `maintenance_policy_candidate_correspondence_repair_required`
10. `maintenance_objective_repair_required`
11. `maintenance_noop_threshold_repair_required`
12. `maintenance_escalation_trigger_repair_required`
13. `reobservation_schedule_repair_required`
14. `uncertainty_repair_required`
15. `calibration_repair_required`
16. `provenance_repair_required`
17. `nonexternalization_review_required`
18. `current_state_mutation_rejected`
19. `authority_escalation_rejected`
20. `replay_conflict_rejected`

## supported receipt

supported routeは次を確定する。

```text
future_only_maintenance_disposition_recorded = true
future_only_maintenance_disposition_scope_exactly_bounded = true
future_only_maintenance_disposition_completed = true
future_only_maintenance_disposition_debt_open = false
maintenance_policy_candidate_retained_future_only = true
policy_activation_review_handoff_prepared = true
policy_activation_review_completed = false
policy_activation_review_debt_open = true
```

次はfalseのまま保持する。

```text
future_only_learning_delta_activated = false
maintenance_policy_candidate_activated = false
maintenance_monitoring_activated = false
current_policy_activated = false
maintenance_action_performed = false
active_now = false
```

## non-supported route

non-supported routeはsource stateを保持する。

maintenance-disposition debtはopenのままである。

source handoffをconsumeしない。

policy-activation review handoffを発行しない。

## 固定境界

```text
maintenance-monitoring observation
!= maintenance-monitoring verification
!= future-only maintenance disposition
!= policy activation review
!= current policy activation
!= maintenance action
```

maintenance dispositionはpolicy activationではない。

maintenance dispositionはmaintenance actionではない。

future-only candidateの保持はactive policyへの昇格ではない。

## current-state preservation

この層は次を行わない。

- persistent WORLD mutation
- WORLD revision increment
- current plan revision
- future-only learning delta activation
- maintenance monitoring activation
- maintenance-policy candidate activation
- current policy activation
- maintenance action
- tool invocation
- external side effect
- automatic rollback
- automatic compensation
- generalized benefit claim

## authority boundary

LearnOS v0.5には次の権限を付与しない。

- selection
- plan revision
- dukkha minimization
- general execution
- WORLD mutation
- current policy activation
- maintenance action

selection ownershipはDecisionOSに残る。

## 後続層

自然な後続は、prepared policy-activation review handoffを入力とする独立したpolicy activation review intakeである。

その層もreviewとactivationを分離しなければならない。
