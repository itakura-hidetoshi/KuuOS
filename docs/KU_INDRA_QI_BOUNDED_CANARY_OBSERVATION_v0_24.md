# Kū–Indra Qi Bounded Canary Observation Proposal v0.24

## Purpose

v0.24 consumes the exact WORLD state and v0.23 longitudinal mirror non-interference artifacts. It produces a bounded proposal for a tiny, time-limited, automatically revocable canary observation surface.

The proposal does not activate canary traffic. It does not modify a live response, feed results back to the live path, select or execute a lineage, update the WORLD model, or actuate the external world.

## Exact inputs

Each proposal binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json`;
- `indra_qi_longitudinal_mirror_noninterference_state_v0_23.json`;
- `indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json`;
- a digest-bound v0.24 plan, proposal report, and license.

All source artifacts remain byte-for-byte read-only.

## Canary lanes

Each proposed lane includes:

```text
lane_id
lineage_id
lineage_kind
canary_fraction
event_budget
expiry_epoch
shadow_return_token_digest
rollback_receipt_template_digest
latency_guardrail_ratio
output_divergence_guardrail
fairness_guardrail_ratio
```

Every lane remains disabled. The proposal carries no activation token and grants no execution authority.

## Bounded proposal gates

v0.24 validates:

- minimum and maximum lane counts;
- recovery-lane preservation;
- minority-lane preservation;
- total canary-fraction cap;
- single-lane fraction cap;
- duration and event-budget caps;
- expiry epoch;
- automatic revocation;
- shadow-return material;
- rollback receipt template;
- latency, divergence, and fairness guardrails;
- proposal-only and non-intervention boundaries.

A diversity failure yields `restore_shadow_diversity_recommended`.

A fraction, duration, budget, expiry, rollback, or guardrail failure yields `redesign_bounded_canary_observation_proposal_recommended`.

Any canary activation, live-response influence, feedback to the live path, external actuation, WORLD update, winner selection, or policy-boundary breach yields `quarantine_recommended`.

## Decisions

```text
bounded_canary_observation_proposal_ready
redesign_bounded_canary_observation_proposal_recommended
restore_shadow_diversity_recommended
extend_mirror_observation_recommended
hold_for_observation
rollback_recommended
quarantine_recommended
```

## Replay resistance

The runtime rejects repeated proposal-run IDs, repeated v0.23 summary/recommendation pairs, repeated proposal-report digests, and broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_bounded_canary_observation_proposal_v0_24.json
indra_qi_bounded_canary_observation_state_v0_24.json
indra_qi_bounded_canary_observation_recommendation_v0_24.json
indra_qi_bounded_canary_observation_ledger_v0_24.jsonl
indra_qi_bounded_canary_observation_receipt_v0_24.json
indra_qi_bounded_canary_observation_audit_v0_24.jsonl
```

## Authority boundary

`bounded_canary_observation_proposal_ready` means only that a disabled, bounded, expiring, revocable proposal satisfies the declared policy. It grants no canary activation, live-response influence, feedback-to-live-path, routing activation, winner selection, lineage selection, live execution, WORLD update, external actuation, promotion, rollback, quarantine, or truth authority.
