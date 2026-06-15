# Kū–Indra Qi Longitudinal Shadow Evidence v0.19

## Purpose

v0.19 aggregates several v0.18 shadow counterfactual observation cycles into a bounded longitudinal evidence surface. It separates transient advantage from persistent improvement while preventing the evidence layer from collapsing into a single winner, live route, or truth claim.

The layer does not execute a lineage. It asks whether improvement persists across time while recovery and minority lineages remain visible and at least two lineages continue to participate in the Pareto frontier.

## Exact inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_shadow_counterfactual_comparison_v0_18.json`;
- `indra_qi_shadow_counterfactual_observation_state_v0_18.json`;
- `indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json`;
- a digest-bound v0.19 plan, longitudinal report, and license.

All source artifacts remain byte-for-byte read-only.

## Longitudinal cycle chain

Each evidence cycle includes a monotonic index and epoch, a digest of the previous cycle, the exact shadow-roster digest, the v0.18 comparison digest, the Pareto frontier, and per-lineage benefit vectors.

The five benefit axes are:

```text
observation_debt_reduction
recoverability_gain
intervention_residue_reduction
scar_pressure_reduction
branch_energy_gain
```

Each lineage observation also preserves its counterfactual signature, deterministic replay result, Process Tensor provenance, and non-Markov context.

## Stability without collapse

v0.19 computes:

- lineage coverage across cycles;
- Pareto-frontier participation ratio;
- persistent-frontier lineage count;
- aggregate sustained-benefit ratio;
- per-metric temporal volatility and trend;
- maximum single-lineage frontier share;
- maximum consecutive single-lineage-only frontier streak;
- recovery-lineage persistence;
- minority-lineage persistence.

Persistent improvement is accepted only when the evidence remains plural. A single lineage may repeatedly appear, but it cannot monopolize frontier membership or become the sole frontier for longer than the bounded streak.

## Decisions

```text
v0.18 shadow_counterfactual_cycle_ready
  + persistence, volatility, recovery, minority, and plurality gates pass
  -> longitudinal_shadow_evidence_ready

v0.18 ready
  + evidence is incomplete or volatile
  -> extend_longitudinal_observation_recommended

v0.18 ready
  + single-lineage collapse pressure appears
  -> restore_shadow_diversity_recommended

route, actuation, WORLD update, winner, or policy-boundary breach
  -> quarantine_recommended

v0.18 hold / rollback / quarantine
  -> preserve the same recommendation class
```

## Replay resistance

The runtime rejects repeated evidence-run IDs, repeated latest-comparison/recommendation source pairs, repeated longitudinal-report digests, broken cycle chains, non-monotonic indexes or epochs, changed shadow-roster digests, and broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_longitudinal_shadow_evidence_summary_v0_19.json
indra_qi_longitudinal_shadow_evidence_state_v0_19.json
indra_qi_longitudinal_shadow_evidence_recommendation_v0_19.json
indra_qi_longitudinal_shadow_evidence_ledger_v0_19.jsonl
indra_qi_longitudinal_shadow_evidence_receipt_v0_19.json
indra_qi_longitudinal_shadow_evidence_audit_v0_19.jsonl
```

## Authority boundary

`longitudinal_shadow_evidence_ready` is an evidence-quality result, not a winner selection or execution license. v0.19 grants no winner-selection, lineage-selection, lineage-execution, live-routing, WORLD-update, external-actuation, promotion, rollback, quarantine, or truth authority. Multi-WORLD non-collapse, minority paths, recovery paths, Process Tensor provenance, and non-Markov feedback remain visible.
