# VerifyOS v0.12 — Dukkha-Preserving Future-Only Policy Activation Review Intake v0.1

## Purpose

This layer accepts only the supported LearnOS v0.5 future-only maintenance-disposition receipt and performs an independent, bounded policy-activation review.

It does not authorize or activate the policy candidate.

## Supported transition

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending_future_only_maintenance_disposition_recorded_policy_activation_review_pending
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded_maintenance_monitoring_observation_verified_maintenance_disposition_pending_future_only_maintenance_disposition_recorded_policy_activation_review_pending_policy_activation_reviewed_activation_authorization_pending
```

## Source-chain revalidation

The runtime revalidates:

- the LearnOS v0.5 receipt digest and supported boundary;
- the source maintenance-disposition evidence and review digests;
- the maintenance-disposition record;
- the maintenance-disposition debt-consumption record;
- the policy-activation-review handoff;
- WORLD state and revision;
- the future-only learning delta and maintenance-policy candidate;
- lineage and responsibility lineage.

## Independent review evidence

The review evidence binds the exact maintenance-policy candidate to:

- a proposed bounded activation scope;
- activation preconditions;
- bounded subject scope;
- activation duration limit;
- rollback plan;
- post-activation monitoring guard;
- uncertainty and calibration;
- provenance and tamper evidence;
- protected-group and future-subject impacts.

The kernel validates supplied evidence. It does not activate the candidate, grant authorization, or perform maintenance.

## Supported result

```text
policy_activation_review_supported = true
policy_activation_review_recorded = true
policy_activation_review_scope_exactly_bounded = true
policy_activation_review_completed = true
policy_activation_review_debt_open = false

activation_authorization_handoff_prepared = true
activation_authorization_completed = false
activation_authorization_debt_open = true
activation_authorization_granted = false
```

The following remain false:

```text
future_only_learning_delta_activated
maintenance_policy_candidate_activated
maintenance_monitoring_activated
current_policy_activated
maintenance_action_performed
active_now
```

## Fixed separation

```text
maintenance-monitoring observation
!= maintenance-monitoring verification
!= future-only maintenance disposition
!= policy activation review
!= activation authorization
!= current policy activation
!= maintenance action
```

## Dispositions

The runtime separates 20 routes:

1. supported review;
2. WORLD refresh;
3. context refresh;
4. review-certificate refresh;
5. additional evidence;
6. source receipt correspondence repair;
7. maintenance-disposition record repair;
8. review-handoff repair;
9. policy-candidate correspondence repair;
10. activation-scope repair;
11. activation-precondition repair;
12. rollback-plan repair;
13. post-activation monitoring-guard repair;
14. uncertainty repair;
15. calibration repair;
16. provenance repair;
17. nonexternalization review;
18. current-state mutation rejection;
19. authority-escalation rejection;
20. replay rejection.

## Authority boundary

VerifyOS v0.12 receives no selection, plan-revision, dukkha-minimization, general-execution, WORLD-mutation, policy-activation, activation-authorization, or maintenance-action authority.

No WORLD mutation, revision increment, plan revision, learning update, policy activation, monitoring activation, maintenance action, tool invocation, external side effect, rollback, or compensation occurs.
