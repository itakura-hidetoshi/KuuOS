# Kū–Indra Qi Licensed Mirror Observation Admission v0.22

## Purpose

v0.22 consumes the exact WORLD state and v0.21 dry-run artifacts. It admits a bounded mirror-observation stream that receives digest-only copies of selected live inputs while remaining causally disconnected from the live response path.

It never changes the live response, feeds results back to the live path, activates routing, selects a winner, executes a lineage live, updates the WORLD model, or actuates the external world.

## Exact inputs

Each admission binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json`;
- `indra_qi_licensed_plural_routing_dry_run_state_v0_21.json`;
- `indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json`;
- a digest-bound v0.22 plan, mirror report, and license.

All source artifacts remain byte-for-byte read-only.

## Privacy-preserving mirror events

Each mirror event contains digests and bounded metrics only:

```text
event_index
dry_run_tick_index
lineage_id
route_slot_id
source_request_digest
mirrored_request_digest
redaction_receipt_digest
dry_run_output_digest
mirror_output_digest
replay_output_digest
live_response_digest_before
live_response_digest_after
latency_delta_ratio
output_divergence_score
replica_restored
```

Raw payload storage is forbidden. The mirrored-request digest is deterministically bound to the source-request digest and redaction receipt.

## Admission evidence

v0.22 measures:

- mirror capture fraction;
- dry-run schedule agreement;
- allocation drift;
- Jain fairness preservation;
- latency delta;
- output divergence;
- redaction receipt completion;
- deterministic mirror replay;
- live-response immutability;
- replica restoration;
- mirror delivery completion.

Fairness or lineage-coverage loss yields `restore_shadow_diversity_recommended`.

Latency, divergence, replay, redaction, delivery, or restoration failure yields `redesign_mirror_observation_admission_recommended`.

Any live-response influence, feedback to the live path, routing activation, external actuation, WORLD update, or policy-boundary breach yields `quarantine_recommended`.

## Decisions

```text
mirror_observation_admission_ready
redesign_mirror_observation_admission_recommended
restore_shadow_diversity_recommended
extend_longitudinal_observation_recommended
hold_for_observation
rollback_recommended
quarantine_recommended
```

## Replay resistance

The runtime rejects repeated mirror-admission IDs, repeated v0.21 summary/recommendation pairs, repeated report digests, and broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_licensed_mirror_observation_admission_summary_v0_22.json
indra_qi_licensed_mirror_observation_admission_state_v0_22.json
indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json
indra_qi_licensed_mirror_observation_admission_ledger_v0_22.jsonl
indra_qi_licensed_mirror_observation_admission_receipt_v0_22.json
indra_qi_licensed_mirror_observation_admission_audit_v0_22.jsonl
```

## Authority boundary

`mirror_observation_admission_ready` means only that bounded, redacted, non-intervening observation satisfies the declared policy. It grants no live-response influence, feedback-to-live-path, routing activation, winner selection, lineage selection, live execution, WORLD update, external actuation, promotion, rollback, quarantine, or truth authority.
