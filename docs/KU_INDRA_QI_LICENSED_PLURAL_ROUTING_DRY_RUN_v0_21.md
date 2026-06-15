# Kū–Indra Qi Licensed Plural Routing Dry Run v0.21

## Purpose

v0.21 consumes the exact WORLD state and v0.20 bounded plural routing artifacts. It validates a proposed scheduler on isolated replica observation streams. It never activates routing, selects a winner, executes a lineage in the live environment, mutates the WORLD model, or actuates the external world.

## Exact inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json`;
- `indra_qi_bounded_plural_shadow_routing_state_v0_20.json`;
- `indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json`;
- a digest-bound v0.21 plan, dry-run report, and license.

All source artifacts remain byte-for-byte read-only.

## Isolated scheduler evidence

Every schedule tick binds:

```text
tick_index
lineage_id
route_slot_id
replica_input_digest
replica_snapshot_digest
output_digest
replay_output_digest
rollback_receipt_digest
expected_rollback_receipt_digest
replica_restored
```

All ticks use one exact replica-input digest. Output and replay-output digests must match. Rollback receipts must match their expected receipts, and every replica must be restored.

## Fairness and allocation

v0.21 computes:

- realized allocation share per lineage;
- maximum allocation error relative to the v0.20 proposal;
- Jain fairness index;
- lineage service ratio;
- maximum consecutive ticks assigned to one lineage;
- deterministic replay completion;
- rollback receipt completion;
- replica restoration completion;
- replica failure ratio.

Starvation or inadequate fairness yields `restore_shadow_diversity_recommended`. Allocation drift, replay failure, rollback mismatch, or restore failure yields `redesign_plural_routing_schedule_recommended`.

Any attempted routing activation, live routing, external actuation, WORLD update, or policy-boundary breach yields `quarantine_recommended`.

## Decisions

```text
plural_routing_dry_run_ready
redesign_plural_routing_schedule_recommended
restore_shadow_diversity_recommended
extend_longitudinal_observation_recommended
hold_for_observation
rollback_recommended
quarantine_recommended
```

## Replay resistance

The runtime rejects repeated dry-run IDs, repeated proposal/recommendation source pairs, repeated dry-run report digests, and broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json
indra_qi_licensed_plural_routing_dry_run_state_v0_21.json
indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json
indra_qi_licensed_plural_routing_dry_run_ledger_v0_21.jsonl
indra_qi_licensed_plural_routing_dry_run_receipt_v0_21.json
indra_qi_licensed_plural_routing_dry_run_audit_v0_21.jsonl
```

## Authority boundary

`plural_routing_dry_run_ready` means only that the isolated scheduler evidence satisfies the declared policy. It grants no routing activation, winner selection, lineage selection, live lineage execution, WORLD update, external actuation, promotion, rollback, quarantine, or truth authority.
