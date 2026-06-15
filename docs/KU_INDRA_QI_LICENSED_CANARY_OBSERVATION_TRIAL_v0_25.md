# Kū–Indra Qi Licensed Canary Observation Trial v0.25

## Purpose

v0.25 consumes the exact WORLD state and v0.24 bounded canary proposal artifacts. It validates a tiny, expiring, automatically revoked observation-copy trial. The trial may process digest-bound copies in an isolated replica surface, but it never activates a live canary route, changes a live response, feeds results back to the live path, updates the WORLD model, or actuates the external world.

## Exact inputs

Each trial binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_bounded_canary_observation_proposal_v0_24.json`;
- `indra_qi_bounded_canary_observation_state_v0_24.json`;
- `indra_qi_bounded_canary_observation_recommendation_v0_24.json`;
- a digest-bound v0.25 plan, trial report, and license.

All source artifacts remain byte-for-byte read-only.

## Trial lanes

Every trial lane is bound to one exact v0.24 lane and carries a smaller or equal fraction, event budget, expiry, return token, and rollback template. Observation-copy processing is enabled only inside the isolated trial surface. Live canary activation remains disabled.

## Event evidence

Each event binds:

```text
source_request_digest
redaction_receipt_digest
copied_request_digest
copy_delivery_digest
trial_output_digest
replay_output_digest
rollback_receipt_digest
revocation_receipt_digest
replica_snapshot_digest
live_response_digest_before
live_response_digest_after
```

Raw payload storage is forbidden. The copied-request digest is deterministically bound to the source-request digest, redaction receipt, and lane ID.

## Trial gates

v0.25 validates:

- exact source-lane binding;
- trial fraction, duration, expiry, and event budgets;
- recovery and minority lanes;
- lane service and Jain fairness;
- allocation error;
- latency and output divergence;
- redaction receipts;
- deterministic replay;
- rollback receipts;
- automatic revocation receipts;
- replica restoration;
- live-response immutability;
- absence of feedback, live activation, external actuation, and WORLD update.

## Decisions

```text
licensed_canary_observation_trial_ready
redesign_canary_observation_trial_recommended
restore_shadow_diversity_recommended
extend_mirror_observation_recommended
hold_for_observation
rollback_recommended
quarantine_recommended
```

A diversity, service, fairness, or allocation failure yields `restore_shadow_diversity_recommended`.

A fraction, duration, budget, expiry, latency, divergence, redaction, replay, rollback, revocation, delivery, or restore failure yields `redesign_canary_observation_trial_recommended`.

Any live canary activation, live-response influence, feedback to the live path, external actuation, WORLD update, winner selection, or boundary breach yields `quarantine_recommended`.

## Outputs

```text
indra_qi_licensed_canary_observation_trial_summary_v0_25.json
indra_qi_licensed_canary_observation_trial_state_v0_25.json
indra_qi_licensed_canary_observation_trial_recommendation_v0_25.json
indra_qi_licensed_canary_observation_trial_ledger_v0_25.jsonl
indra_qi_licensed_canary_observation_trial_receipt_v0_25.json
indra_qi_licensed_canary_observation_trial_audit_v0_25.jsonl
```

## Authority boundary

`licensed_canary_observation_trial_ready` means only that an isolated, bounded, expiring, automatically revoked observation-copy trial satisfies the declared policy. It grants no live canary activation, live-response influence, feedback-to-live-path, winner selection, lineage selection, live execution, WORLD update, external actuation, promotion, rollback, quarantine, or truth authority.
