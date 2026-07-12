# WORLD Dukkha-Preserving Single-Use World Mutation Application Intake v0.1

## Purpose

This layer consumes a WORLD v0.61 candidate-specific single-use commit authorization and applies the bound WORLD patch exactly once.

The application is atomic and bounded to the authorized candidate, patch, owner, constraints, transaction, and expiry.

Application does not by itself establish a WORLD fact, causal truth, or realized dukkha reduction.

## State transition

```text
world_candidate_commit_authorized_not_applied
->
world_candidate_mutation_applied_unverified
```

The transition occurs only for `world_mutation_application_ready`.

Every non-ready disposition preserves the authorized-not-applied state and leaves application debt open.

## Ready-path effects

The ready path:

- fully revalidates the WORLD v0.61 authorization receipt and mutation-application handoff;
- binds an independent application review certificate;
- verifies candidate, patch, scope, constraints, owner, expiry, preconditions, engine admission, atomicity, provenance, nonexternalization, dukkha preservation, and compensation readiness;
- consumes the single-use authorization once;
- applies the bounded patch atomically;
- increments the WORLD model revision exactly once;
- emits an application receipt;
- emits a post-application observation and verification handoff.

## Deferred claims

After application, the following remain false:

```text
post_application_verification_completed
world_fact_confirmed
causal_attribution_confirmed
dukkha_reduction_realized_confirmed
```

The persistent WORLD model has changed, but the change remains an applied, unverified candidate update.

## Authority boundary

```text
commit authorization
!= mutation application
!= post-application observation
!= post-application verification
!= WORLD fact
!= causal truth
!= realized dukkha confirmation
```

The layer does not grant general WORLD mutation authority.

It does not rerun the host operation, observation, verification, disposition, or authorization layers.

It does not perform automatic truth promotion, plan completion, rollback, or compensation.

## Dispositions

- `world_mutation_application_ready`
- `world_refresh_required`
- `world_mutation_application_context_refresh_required`
- `world_mutation_application_review_refresh_required`
- `world_candidate_commit_authorization_expired`
- `world_candidate_commit_authorization_revalidation_required`
- `world_patch_repair_required`
- `world_precondition_repair_required`
- `world_mutation_engine_rejected`
- `world_mutation_atomicity_repair_required`
- `world_postcondition_observation_required`
- `provenance_repair_required`
- `nonexternalization_review_required`
- `dukkha_preservation_review_required`
- `compensation_route_repair_required`
- `truth_promotion_rejected`
- `replay_conflict_rejected`

## Next boundary

The next natural layer is post-application WORLD observation intake, followed by independent verification and only then a separate fact-disposition layer.
