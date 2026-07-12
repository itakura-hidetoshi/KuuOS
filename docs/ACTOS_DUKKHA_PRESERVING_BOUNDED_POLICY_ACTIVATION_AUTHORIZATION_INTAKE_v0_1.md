# ActOS v0.12 — Dukkha-Preserving Bounded Policy Activation Authorization Intake v0.1

## Purpose

This layer consumes only a supported VerifyOS v0.12 future-only policy activation review receipt and independently decides whether one exact, bounded, single-use policy activation authorization may be reserved.

It does **not** activate the maintenance-policy candidate, current policy, monitoring, or any maintenance action.

## Supported transition

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending_future_only_maintenance_disposition_recorded_policy_activation_review_pending_policy_activation_reviewed_activation_authorization_pending
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending_future_only_maintenance_disposition_recorded_policy_activation_review_pending_policy_activation_reviewed_activation_authorization_pending_bounded_policy_activation_authorization_granted_policy_activation_pending
```

## Source-chain revalidation

The runtime revalidates the complete VerifyOS v0.12 receipt digest and the following nested artifacts independently:

- policy activation review evidence packet;
- policy activation review certificate;
- policy activation review record;
- review-debt consumption record;
- activation-authorization handoff envelope;
- resulting evidence and responsibility lineage.

The source must preserve the previously confirmed bounded WORLD fact, causal attribution, realized dukkha reduction, future-only learning delta, maintenance-monitoring observation and verification, future-only maintenance disposition, and completed policy activation review.

## Independent authorization evidence

The authorization packet binds the exact reviewed maintenance-policy candidate to:

- reviewed activation scope;
- activation precondition set;
- bounded subject scope;
- activation duration limit;
- rollback plan;
- post-activation monitoring guard;
- single-use authorization lease;
- effect ceiling;
- uncertainty and calibration;
- provenance and tamper evidence;
- protected-group and future-subject nonexternalization.

The authorization assessor and evidence source are distinct responsibility-lineage entries.

## Dispositions

The actual-chain checker validates 20 routes:

1. bounded policy activation authorization supported;
2. WORLD refresh required;
3. authorization context refresh required;
4. authorization review refresh required;
5. additional authorization evidence required;
6. source VerifyOS receipt repair required;
7. policy activation review record repair required;
8. activation-authorization handoff repair required;
9. maintenance-policy candidate repair required;
10. authorization scope repair required;
11. activation precondition repair required;
12. rollback plan repair required;
13. post-activation monitoring guard repair required;
14. uncertainty repair required;
15. calibration repair required;
16. provenance repair required;
17. nonexternalization review required;
18. current-state mutation rejected;
19. authority escalation rejected;
20. replay conflict rejected.

## Supported result

```text
bounded_policy_activation_authorization_granted = true
bounded_policy_activation_authorization_scope_exactly_bounded = true
bounded_policy_activation_authorization_completed = true
bounded_policy_activation_authorization_debt_open = false

single_use_policy_activation_authorization_reserved = true
policy_activation_authorization_token_issued = true
policy_activation_authorization_token_consumed = false

policy_activation_handoff_prepared = true
policy_activation_completed = false
policy_activation_debt_open = true
```

## Boundary

```text
completed policy activation review
!= bounded policy activation authorization
!= authorization token consumption
!= policy activation
!= current policy activation
!= maintenance action
```

The supported receipt performs no:

- WORLD mutation or revision increment;
- plan revision;
- policy activation;
- monitoring activation;
- maintenance action;
- tool invocation or external side effect;
- rollback or compensation;
- selection or dukkha-minimization authority transfer;
- general execution authority grant.

The authorization is exact, future-only, single-use, and unconsumed. The next layer must separately validate and consume it before any bounded policy activation state transition can be recorded.

## Implementation

- `runtime/kuuos_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1.py`
- `scripts/check_actos_dukkha_preserving_bounded_policy_activation_authorization_fixture_v0_1.py`
- `scripts/check_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1.py`
- `formal/KUOS/ActOS/DukkhaPreservingBoundedPolicyActivationAuthorizationIntakeV0_12.lean`
- `formal/KuuOSActOSV0_12.lean`
- `manifests/kuuos_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1.json`
- cumulative Evidence Cycle connection
