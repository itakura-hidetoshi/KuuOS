# VerifyOS v0.9: Dukkha-Preserving WORLD Causal-Attribution Verification Intake v0.1

## Status

This layer connects the canonical WORLD v0.63 bounded fact-confirmation receipt to independent causal-attribution verification.

It is an actual runtime intake.

It preserves the confirmed bounded WORLD fact.

It does not mutate the WORLD model.

It does not confirm realized dukkha reduction.

## Source contract

The only admissible source state is:

```text
world_candidate_bounded_fact_confirmed_causal_attribution_pending
```

The source must be a supported WORLD v0.63 receipt with:

- exactly one bounded WORLD fact-confirmation receipt;
- the fact-confirmation debt consumed exactly once;
- a confirmed exact bounded proposition;
- no truth generalization beyond the candidate fact and relation;
- an unchanged persistent WORLD state;
- an unchanged WORLD revision;
- open independent causal-attribution verification debt;
- no confirmed causal attribution;
- no confirmed realized dukkha reduction.

The intake separately receives and revalidates the exact source chain:

```text
WORLD v0.62 mutation-application receipt
->
VerifyOS v0.8 postcondition-verification receipt
->
WORLD v0.63 bounded fact-confirmation receipt
```

It revalidates the canonical digests of:

- the WORLD v0.63 fact-confirmation review certificate;
- the fact-confirmation record;
- the fact-confirmation debt-consumption record;
- the bounded WORLD fact-status binding;
- the causal-attribution verification handoff;
- the VerifyOS v0.8 evidence packet and verification review;
- the WORLD v0.62 mutation record and persisted candidate.

## Independent causal evidence

The causal evidence packet binds the exact confirmed bounded WORLD fact to:

- the candidate fact digest;
- the candidate relation digest;
- the resulting WORLD state;
- the resulting WORLD revision;
- the persistent WORLD storage target;
- the expected WORLD postcondition;
- a bounded causal model;
- a bounded causal query;
- the exact intervention;
- the exposure;
- the outcome;
- the counterfactual estimand;
- explicit identification assumptions;
- an explicit confounder set;
- an adjustment strategy;
- temporal-ordering evidence;
- intervention-correspondence evidence;
- counterfactual-support evidence;
- an alternative-cause assessment;
- a selection-bias assessment;
- a measurement-validity assessment;
- uncertainty;
- calibration;
- provenance;
- tamper evidence;
- protected-group causal impact;
- future-subject causal impact;
- the existing realized-dukkha observation without promoting it to a realized-dukkha fact.

The causal evidence collector and evidence source remain independent of the WORLD v0.63 fact-confirmation reviewer.

Evidence collection performs no WORLD mutation.

The evidence packet does not preconfirm causal attribution.

## Independent verification review

The verification review binds the exact source and causal evidence to:

- causal-model adequacy;
- exact boundedness of the causal query;
- intervention correspondence;
- temporal ordering;
- confounding control;
- counterfactual support;
- alternative-cause assessment;
- selection-bias adequacy;
- measurement validity;
- uncertainty adequacy;
- calibration adequacy;
- provenance continuity;
- protected-group nonexternalization;
- future-subject nonexternalization.

The review must not:

- generalize the confirmed fact beyond its bounded proposition;
- preconfirm causal attribution before disposition;
- claim realized dukkha reduction.

## State transition

Only the supported disposition performs:

```text
world_candidate_bounded_fact_confirmed_causal_attribution_pending
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending
```

Every other valid disposition preserves:

```text
world_candidate_bounded_fact_confirmed_causal_attribution_pending
```

On every non-supported route, the bounded WORLD fact remains confirmed while causal attribution remains pending.

## Dispositions

The intake routes to exactly one disposition:

1. `world_causal_attribution_verification_supported`
2. `world_refresh_required`
3. `causal_attribution_context_refresh_required`
4. `causal_attribution_review_refresh_required`
5. `additional_causal_evidence_required`
6. `causal_model_repair_required`
7. `intervention_correspondence_repair_required`
8. `temporal_ordering_repair_required`
9. `confounding_control_repair_required`
10. `counterfactual_support_repair_required`
11. `alternative_cause_review_required`
12. `selection_bias_review_required`
13. `measurement_validity_repair_required`
14. `uncertainty_repair_required`
15. `calibration_repair_required`
16. `provenance_repair_required`
17. `nonexternalization_review_required`
18. `truth_generalization_rejected`
19. `dukkha_realization_overclaim_rejected`
20. `replay_conflict_rejected`

## Supported verification

The supported route:

- issues exactly one causal-attribution verification receipt;
- consumes causal-attribution verification debt once;
- closes source fact-confirmation receipt replay;
- closes causal evidence, review, nonce, and session replay;
- records an exact bounded causal-attribution binding;
- prepares a separate realized-dukkha verification handoff.

The supported result is:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = false
```

The confirmed causal scope is limited to:

- the exact candidate fact;
- the exact candidate relation;
- the exact WORLD mutation transaction lineage;
- the supplied causal query;
- the supplied intervention;
- the supplied counterfactual estimand;
- the declared identification assumptions;
- the declared confounder set;
- the supplied uncertainty, calibration, and provenance.

It does not establish unrestricted or universal causality.

## Causal boundary

The governing separation is:

```text
WORLD mutation application
!= post-application evidence
!= postcondition verification
!= bounded WORLD fact confirmation
!= causal evidence
!= causal-attribution verification
!= realized dukkha confirmation
```

Therefore:

```text
confirmed bounded WORLD fact != causal attribution
```

and:

```text
confirmed causal attribution != realized dukkha reduction
```

WORLD v0.63 establishes the bounded fact.

VerifyOS v0.9 may establish only the exact bounded causal relation under the supplied identification assumptions.

A later independent layer must verify whether realized dukkha reduction is confirmed.

## No state mutation or authority escalation

VerifyOS v0.9 performs no:

- WORLD patch reapplication;
- WORLD revision increment;
- tool invocation;
- external side effect;
- compensation;
- automatic truth generalization;
- automatic causal attribution outside the verified disposition;
- automatic realized-dukkha confirmation;
- automatic plan completion;
- automatic rollback;
- automatic compensation.

It grants no:

- selection authority;
- plan-revision authority;
- dukkha-minimization authority;
- general execution authority;
- WORLD mutation authority.

DecisionOS retains selection ownership.

Evidence lineage and responsibility lineage grow monotonically.
