# LearnOS Dukkha-Preserving Future-Only Learning Maintenance Disposition Intake v0.1

## Scope

This layer is LearnOS v0.4.

It accepts only the supported VerifyOS v0.10 realized-dukkha verification receipt in state:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed
```

The supported route records one future-only learning delta and prepares one maintenance-monitoring handoff:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed_future_only_learning_delta_recorded
```

The transition does not alter the current WORLD model, current plan, current policy, current execution state, or current authority distribution.

## Source revalidation

The runtime revalidates the complete VerifyOS v0.10 receipt and its nested artifacts:

- realized-dukkha evidence packet;
- realized-dukkha verification review certificate;
- realized-dukkha verification record;
- realized-dukkha verification debt-consumption record;
- bounded realized-dukkha confirmation binding;
- future-learning handoff envelope.

The source must preserve the exact bounded sequence:

```text
bounded WORLD fact confirmation
!= bounded causal attribution confirmation
!= bounded realized-dukkha confirmation
!= future-only learning
```

## Future-only learning evidence

The independent evidence packet binds:

- the source VerifyOS v0.10 receipt and nested artifact digests;
- candidate fact and relation digests;
- WORLD state and revision;
- realized-dukkha observation and effect estimate;
- exact learning target;
- future-only learning delta;
- bounded maintenance-policy candidate;
- maintenance and retention windows;
- durability, adverse-effect, and distributional monitoring specifications;
- reobservation trigger;
- uncertainty, calibration, provenance, and tamper evidence;
- protected-group and future-subject learning impact.

The evidence packet must state that it performed no current WORLD mutation, current plan revision, current policy activation, generalized benefit claim, or authority escalation.

## Review contract

The independent review verifies:

- source receipt correspondence;
- bounded fact, causal-attribution, and realized-dukkha correspondence;
- exact bounded learning target;
- validity of the future-only delta;
- boundedness of the maintenance-policy candidate;
- monitoring-window and reobservation adequacy;
- uncertainty, calibration, and provenance continuity;
- protected-group and future-subject nonexternalization;
- absence of current-state mutation and authority escalation.

## Dispositions

The runtime separates 20 dispositions:

1. `future_only_learning_maintenance_supported`
2. `world_refresh_required`
3. `learning_context_refresh_required`
4. `learning_review_refresh_required`
5. `additional_future_only_learning_evidence_required`
6. `source_receipt_correspondence_repair_required`
7. `bounded_fact_correspondence_repair_required`
8. `causal_attribution_correspondence_repair_required`
9. `realized_dukkha_correspondence_repair_required`
10. `maintenance_window_repair_required`
11. `durability_monitoring_review_required`
12. `adverse_effect_monitoring_review_required`
13. `distributional_monitoring_review_required`
14. `uncertainty_repair_required`
15. `calibration_repair_required`
16. `provenance_repair_required`
17. `nonexternalization_review_required`
18. `current_state_mutation_rejected`
19. `authority_escalation_rejected`
20. `replay_conflict_rejected`

## Supported boundary

Supported learning preserves:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = true
```

It adds only:

```text
future_only_learning_delta_recorded = true
future_only_learning_delta_activated = false
maintenance_monitoring_handoff_prepared = true
maintenance_monitoring_activated = false
```

The learning delta is evidence for possible future use.

It is not a current policy update, plan revision, execution instruction, generalized benefit claim, or automatic maintenance action.

## Non-supported boundary

A non-supported disposition keeps the input state unchanged.

The three bounded confirmations remain true.

The learning debt remains open.

No learning delta is recorded or activated.

## Authority boundary

LearnOS v0.4 receives no authority for:

- selection;
- plan revision;
- dukkha minimization;
- current policy activation;
- general execution;
- WORLD mutation;
- tool invocation;
- external side effects.

DecisionOS retains selection ownership.

## Formal invariants

The Lean package proves:

- supported learning preserves the three bounded confirmations;
- supported learning records but does not activate the future-only delta;
- non-supported routes preserve the confirmed source and open learning debt;
- current WORLD state, revision, plan, and policy remain unchanged;
- no authority is granted to LearnOS;
- evidence and responsibility lineages are monotone.
