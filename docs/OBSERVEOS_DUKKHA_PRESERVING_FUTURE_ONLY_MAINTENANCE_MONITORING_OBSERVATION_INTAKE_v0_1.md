# ObserveOS v0.6 Dukkha-Preserving Future-Only Maintenance-Monitoring Observation Intake v0.1

## Purpose

This layer accepts the supported LearnOS v0.4 future-only learning maintenance disposition receipt.

It records exactly one bounded maintenance-monitoring observation.

It does not activate the future-only learning delta.

It does not activate the maintenance policy candidate.

It does not perform a maintenance action.

It does not verify the observation.

It prepares a separate verification handoff.

## Source state

The only supported source state is:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded
```

The source receipt must be a supported LearnOS v0.4 receipt.

The source must preserve:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = true
future_only_learning_delta_recorded = true
future_only_learning_delta_activated = false
maintenance_monitoring_handoff_prepared = true
maintenance_monitoring_activated = false
```

## Supported transition

The supported route is:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded_maintenance_monitoring_observation_recorded
```

The supported route records an observation receipt.

The supported route opens a distinct verification debt.

The supported route does not complete verification.

## Source revalidation

ObserveOS revalidates the complete LearnOS v0.4 receipt digest.

ObserveOS also revalidates the nested:

- future-only learning evidence packet;
- future-only learning review certificate;
- future-only learning record;
- future-only learning debt-consumption record;
- future-only learning delta binding;
- maintenance-monitoring handoff envelope.

The source maintenance-monitoring handoff must remain:

```text
state = prepared_not_activated
automatic_action = false
```

The source future-only learning delta binding must remain:

```text
future_only = true
active_now = false
world_changed = false
plan_changed = false
policy_activated = false
```

## Observation evidence

The evidence packet binds:

- the exact LearnOS source receipt;
- the exact future-only learning delta;
- the exact maintenance-policy candidate;
- the exact maintenance window;
- the durability-monitoring specification;
- the adverse-effect-monitoring specification;
- the distributional-monitoring specification;
- the reobservation trigger;
- the retention window;
- the observation window;
- the baseline observation;
- the durability observation;
- the adverse-effect observation;
- the distributional observation;
- raw artifacts;
- uncertainty;
- calibration;
- provenance;
- tamper evidence;
- protected-group impact;
- future-subject impact;
- collector identity;
- evidence-source identity;
- collection interval.

The collector must be independent from the LearnOS evidence collector and reviewer.

The evidence source must be independent from the LearnOS evidence source.

The evidence packet describes a completed external observation collection.

The intake kernel does not repeat that collection.

## Observation review

The review certificate checks:

- source-receipt correspondence;
- future-only learning-delta correspondence;
- maintenance-handoff correspondence;
- maintenance-window adequacy;
- durability-observation adequacy;
- adverse-effect-observation adequacy;
- distributional-observation adequacy;
- reobservation-trigger adequacy;
- uncertainty adequacy;
- calibration adequacy;
- provenance continuity;
- protected-group nonexternalization;
- future-subject nonexternalization;
- absence of current-state mutation;
- absence of a maintenance action;
- absence of authority escalation.

## Dispositions

The runtime separates twenty dispositions:

1. `maintenance_monitoring_observation_supported`
2. `world_refresh_required`
3. `monitoring_context_refresh_required`
4. `monitoring_review_refresh_required`
5. `additional_maintenance_monitoring_evidence_required`
6. `source_receipt_correspondence_repair_required`
7. `future_only_learning_delta_correspondence_repair_required`
8. `maintenance_handoff_correspondence_repair_required`
9. `maintenance_window_repair_required`
10. `durability_observation_repair_required`
11. `adverse_effect_observation_repair_required`
12. `distributional_observation_repair_required`
13. `reobservation_trigger_repair_required`
14. `uncertainty_repair_required`
15. `calibration_repair_required`
16. `provenance_repair_required`
17. `nonexternalization_review_required`
18. `current_state_mutation_rejected`
19. `authority_escalation_rejected`
20. `replay_conflict_rejected`

## Supported receipt

The supported route issues exactly one observation receipt.

The supported route consumes the observation debt once.

The supported route consumes the source maintenance-monitoring handoff for observation once.

The supported route closes source, evidence, review, nonce, and session replay.

The supported route records:

```text
maintenance_monitoring_observation_recorded = true
maintenance_monitoring_observation_scope_exactly_bounded = true
maintenance_monitoring_verification_handoff_prepared = true
verification_intake_admitted = true
verification_receipt_required = true
verification_completed = false
verification_debt_open = true
```

## Non-supported routes

A non-supported route preserves the source state.

A non-supported route keeps the observation debt open.

A non-supported route does not consume the source handoff.

A non-supported route does not issue a verification handoff.

A non-supported route preserves:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = true
future_only_learning_delta_recorded = true
future_only_learning_delta_activated = false
maintenance_monitoring_observation_recorded = false
maintenance_monitoring_observation_debt_open = true
```

## Fixed separation

```text
confirmed bounded WORLD fact
!= confirmed bounded causal attribution
!= confirmed bounded realized dukkha
!= future-only learning delta
!= maintenance-monitoring handoff
!= maintenance-monitoring observation evidence
!= maintenance-monitoring observation receipt
!= maintenance-monitoring verification
!= current policy activation
!= maintenance action
```

Observation is not verification.

Observation is not learning activation.

Observation is not policy activation.

Observation is not a maintenance action.

Observation is not a generalized benefit claim.

## Current-state preservation

The intake does not:

- mutate persistent WORLD state;
- increment WORLD revision;
- revise the current plan;
- activate the current policy;
- activate the future-only learning delta;
- invoke a tool;
- perform an external side effect;
- perform compensation;
- perform rollback;
- complete verification;
- generalize the bounded result.

The evidence collection described by the packet occurred outside the intake kernel.

The kernel only validates and records the supplied evidence.

## Authority boundary

ObserveOS v0.6 receives no authority for:

- selection;
- plan revision;
- dukkha minimization;
- current policy activation;
- maintenance action;
- general execution;
- WORLD mutation;
- tool invocation;
- external side effects.

DecisionOS retains selection ownership.

## Formal invariants

The Lean package proves:

- supported observation preserves the confirmed source;
- supported observation records only the bounded monitoring observation;
- supported observation does not complete verification;
- non-supported routes preserve the source and open observation debt;
- current WORLD state, revision, plan, policy, and learning activation remain unchanged;
- ObserveOS receives no execution, mutation, policy-activation, or maintenance-action authority;
- observation remains distinct from verification and learning activation;
- evidence and responsibility lineages are monotone.

## Natural successor

The natural successor is an independent VerifyOS maintenance-monitoring verification disposition intake.

That layer may verify the bounded observation.

It must not automatically activate the learning delta or maintenance policy.

Any later learning revision or policy activation requires a separate receipt and authority boundary.
