# WORLD v0.63: Dukkha-Preserving WORLD Fact-Confirmation Disposition Intake v0.1

## Status

This layer consumes only a supported VerifyOS v0.8 WORLD postcondition-verification receipt as its primary source.

It independently revalidates the exact canonical WORLD v0.62 mutation-application receipt that the VerifyOS receipt binds.

It may confirm only the exact bounded proposition already carried by the persisted WORLD candidate.

It does not reapply the WORLD patch.

It does not increment the WORLD revision.

It does not confirm causal attribution or realized dukkha reduction.

## Source state

The only admissible source state is:

```text
world_candidate_commit_postcondition_verified_world_fact_confirmation_pending
```

The VerifyOS v0.8 source must have the supported disposition:

```text
world_postcondition_verification_supported
```

The source must show that postcondition-verification debt was consumed once, replay was closed, fact-confirmation intake was admitted, and WORLD fact confirmation remains incomplete.

The intake rejects any VerifyOS source that already claims a confirmed WORLD fact, causal attribution, realized dukkha reduction, repeated WORLD mutation, external execution, or authority escalation.

## Full source revalidation

The intake revalidates the canonical digest and boundary fields of the complete VerifyOS v0.8 receipt.

It revalidates the following VerifyOS artifacts:

- the post-application evidence packet;
- the postcondition-verification review certificate;
- the postcondition-verification record;
- the postcondition-verification debt-consumption record;
- the WORLD fact-confirmation handoff envelope;
- the VerifyOS intake-context digest binding.

The intake separately revalidates the exact WORLD v0.62 mutation-application receipt bound by VerifyOS.

It revalidates:

- the WORLD mutation record;
- the persisted WORLD candidate envelope;
- the postcondition-verification handoff envelope;
- the mutation transaction digest;
- the candidate fact digest;
- the candidate relation digest;
- the resulting WORLD state digest;
- the resulting WORLD revision;
- the persistent storage target;
- the expected WORLD update postcondition.

## Fact-confirmation review

The independent fact-confirmation review binds the exact source chain to:

- the candidate fact digest;
- the candidate relation digest;
- the resulting WORLD state digest;
- the resulting WORLD revision;
- the persistent storage target;
- the expected postcondition;
- uncertainty;
- calibration;
- provenance;
- protected-group impact;
- future-subject impact;
- the realized-dukkha observation.

The review must preserve the exact bounded scope of the candidate proposition.

It must not generalize beyond the bound carried by the candidate fact, relation, state, revision, evidence, calibration, and provenance.

It must not claim causal attribution.

It must not claim realized dukkha reduction.

## State transition

Only the supported disposition performs:

```text
world_candidate_commit_postcondition_verified_world_fact_confirmation_pending
->
world_candidate_bounded_fact_confirmed_causal_attribution_pending
```

Every other valid disposition preserves:

```text
world_candidate_commit_postcondition_verified_world_fact_confirmation_pending
```

## Dispositions

The intake routes to exactly one disposition:

1. `world_fact_confirmation_supported`
2. `world_refresh_required`
3. `fact_confirmation_context_refresh_required`
4. `fact_confirmation_review_refresh_required`
5. `additional_postcondition_evidence_required`
6. `candidate_fact_correspondence_repair_required`
7. `candidate_relation_correspondence_repair_required`
8. `world_state_correspondence_repair_required`
9. `world_revision_correspondence_repair_required`
10. `storage_persistence_repair_required`
11. `calibration_repair_required`
12. `provenance_repair_required`
13. `nonexternalization_review_required`
14. `causal_attribution_overclaim_rejected`
15. `dukkha_realization_overclaim_rejected`
16. `truth_promotion_rejected`
17. `replay_conflict_rejected`

## Supported fact confirmation

The supported route:

- issues exactly one bounded WORLD fact-confirmation receipt;
- consumes fact-confirmation debt once;
- closes source VerifyOS receipt replay;
- closes review, nonce, and session replay;
- binds confirmed status to the existing persisted candidate;
- records the exact bounded proposition as confirmed;
- prepares an independent causal-attribution verification handoff.

The supported receipt establishes:

```text
world_fact_confirmed = true
causal_attribution_confirmed = false
dukkha_reduction_realized_confirmed = false
```

The `world_fact_confirmed` field is restricted to the exact proposition bound by the candidate fact digest, candidate relation digest, resulting WORLD state digest, resulting WORLD revision, persistent storage target, expected postcondition, evidence, uncertainty, calibration, and provenance.

It does not establish generalized truth beyond that bound.

## Non-supported routes

Every non-supported route preserves:

```text
world_candidate_commit_postcondition_verified_world_fact_confirmation_pending
world_fact_confirmation_debt_open = true
source_world_postcondition_verification_receipt_replay_closed = false
world_fact_confirmed = false
causal_attribution_confirmed = false
dukkha_reduction_realized_confirmed = false
```

A routed disposition receipt is still issued for the valid intake evaluation.

No bounded fact-confirmation receipt is issued unless the disposition is supported.

## Fixed separation

The governing separation is:

```text
mutation receipt
!= evidence packet
!= postcondition verification receipt
!= fact-confirmation disposition receipt
!= confirmed bounded WORLD fact
!= causal attribution
!= realized dukkha confirmation
```

Therefore:

```text
WORLD fact confirmation != causal attribution
WORLD fact confirmation != realized dukkha confirmation
```

The confirmed bounded WORLD fact becomes an admissible source for a later independent causal-attribution verification or disposition intake.

Realized dukkha confirmation remains a still later and separately evidenced receipt.

## No mutation or authority escalation

WORLD v0.63 performs no:

- WORLD patch reapplication;
- WORLD revision increment;
- tool invocation;
- external side effect;
- compensation;
- causal-attribution confirmation;
- realized-dukkha confirmation;
- automatic truth generalization;
- automatic plan completion;
- automatic rollback;
- automatic compensation.

It grants no:

- selection authority;
- plan-revision authority;
- dukkha-minimization authority;
- general execution authority;
- general WORLD mutation authority.

DecisionOS retains selection ownership.

Evidence lineage and responsibility lineage grow monotonically.
