# Kū–Indra Qi Bounded Plural Shadow Routing Proposal v0.20

## Purpose

v0.20 consumes the exact WORLD state and v0.19 longitudinal evidence artifacts. It produces a bounded allocation proposal for observation-only shadow traffic across several persistent lineages. It does not activate routing, execute a lineage, select a winner, update the WORLD model, or actuate the external world.

The purpose is to translate plural longitudinal evidence into a reversible proposal surface while preserving recovery and minority lineages.

## Exact inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_longitudinal_shadow_evidence_summary_v0_19.json`;
- `indra_qi_longitudinal_shadow_evidence_state_v0_19.json`;
- `indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json`;
- a digest-bound v0.20 plan, proposal report, and license.

All source artifacts remain byte-for-byte read-only.

## Proposal entries

Each route entry contains:

```text
route_slot_id
lineage_id
allocation_share
requested_route_cycles
observation_budget
shadow_return_token_digest
route_overlay_digest
observation_scope_digest
routing_activation_enabled = false
live_route_enabled = false
external_actuation_enabled = false
world_update_enabled = false
```

The return token and overlay material preserve a path back to the prior shadow state. They do not grant execution authority.

## Bounded plural allocation gates

v0.20 validates:

- minimum and maximum routed lineage counts;
- exact allocation sum of one;
- minimum allocation share;
- maximum single-lineage share;
- maximum total observation-traffic fraction;
- route-cycle and observation-budget limits;
- persistent-frontier membership;
- sustained-benefit qualification;
- recovery-lineage preservation;
- minority-lineage preservation;
- proposal-only and routing-disabled boundaries.

A concentrated allocation, missing recovery path, or missing minority path yields `restore_shadow_diversity_recommended`.

A budget, coverage, or allocation-integrity failure yields `redesign_plural_shadow_routing_proposal_recommended`.

Any routing activation, external actuation, WORLD update, or policy-boundary breach yields `quarantine_recommended`.

## Relation to v0.19

```text
v0.19 longitudinal_shadow_evidence_ready
  + plural diversity and proposal gates pass
  -> plural_shadow_routing_proposal_ready

v0.19 ready
  + diversity or allocation-concentration gate fails
  -> restore_shadow_diversity_recommended

v0.19 ready
  + budget, coverage, or proposal-integrity gate fails
  -> redesign_plural_shadow_routing_proposal_recommended

routing activation or actuation boundary breach
  -> quarantine_recommended

v0.19 hold / extend / restore / rollback / quarantine
  -> preserve the corresponding recommendation class
```

## Replay resistance

The runtime rejects repeated proposal-run IDs, repeated summary/recommendation source pairs, repeated report digests, and broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json
indra_qi_bounded_plural_shadow_routing_state_v0_20.json
indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json
indra_qi_bounded_plural_shadow_routing_ledger_v0_20.jsonl
indra_qi_bounded_plural_shadow_routing_receipt_v0_20.json
indra_qi_bounded_plural_shadow_routing_audit_v0_20.jsonl
```

## Authority boundary

`plural_shadow_routing_proposal_ready` means only that the proposed bounded allocation satisfies the declared policy. It does not activate routing. v0.20 grants no routing-activation, winner-selection, lineage-selection, lineage-execution, WORLD-update, external-actuation, promotion, rollback, quarantine, or truth authority. Multi-WORLD non-collapse, Process Tensor provenance, non-Markov feedback, recovery paths, and minority paths remain visible.
