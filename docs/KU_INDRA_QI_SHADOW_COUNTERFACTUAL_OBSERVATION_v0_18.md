# Kū–Indra Qi Shadow Counterfactual Observation Cycle v0.18

## Purpose

v0.18 projects one identical observation input across every admitted v0.17 shadow lineage. It compares the resulting conventional-side changes in observation debt, recoverability reserve, intervention residue, scar pressure, and branch energy without activating a live route, selecting a winner, executing a lineage, or mutating the WORLD model.

The output is a bounded counterfactual comparison surface. A Pareto frontier remains a set of non-dominated observations, not a truth ranking or automatic selection mechanism.

## Exact inputs

Each cycle binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_reversible_shadow_roster_v0_17.json`;
- `indra_qi_reversible_shadow_admission_state_v0_17.json`;
- `indra_qi_reversible_shadow_admission_recommendation_v0_17.json`;
- a v0.18 plan, projection report, and license bound to all source digests.

All source artifacts remain byte-for-byte read-only.

## Shared observation projection

Every projection must bind the same `shared_observation_input_digest`. It also binds the exact v0.17 `shadow_baseline_digest`, `shadow_overlay_digest`, `shadow_slot_id`, lineage ID, shadow-cycle budget, and observation budget.

Each projection records baseline and projected values for:

```text
observation_debt
recoverability_reserve
intervention_residue
scar_pressure
branch_energy
```

The evaluator derives a five-axis counterfactual benefit vector:

```text
observation_debt_reduction
recoverability_gain
intervention_residue_reduction
scar_pressure_reduction
branch_energy_gain
```

These values are diagnostic comparisons, not truth values.

## Determinism and isolation

A projection is acceptable only when:

- output and replay-output digests match;
- the common observation-input digest is preserved;
- baseline and overlay bindings are exact;
- the shadow-cycle and observation budgets remain bounded;
- no live route, external actuation, or WORLD update was attempted;
- the policy boundary remained preserved.

A routing or actuation boundary breach yields `quarantine_recommended`. Ordinary projection, replay, coverage, diversity, or metric failures yield `redesign_shadow_observation_recommended`.

## Pareto frontier without winner selection

v0.18 computes the non-dominated lineage set over all five benefit axes. It requires a bounded minimum frontier size and distinct counterfactual signatures so that the comparison does not collapse immediately to one lineage.

The frontier is explicitly marked:

```text
pareto_frontier_not_winner_selection = true
winner_selected = false
```

Recovery and minority-preservation projections must remain represented.

## Relation to v0.17

```text
v0.17 reversible_shadow_admission_ready
  + shared-input projection gates pass
  -> shadow_counterfactual_cycle_ready

v0.17 reversible_shadow_admission_ready
  + replay/coverage/diversity/metric gate fails
  -> redesign_shadow_observation_recommended

live route, external actuation, WORLD update, or policy boundary breach
  -> quarantine_recommended

v0.17 hold / rollback / quarantine
  -> preserve the same recommendation class
```

v0.18 never weakens a v0.17 rollback or quarantine recommendation.

## Replay resistance

The runtime rejects repeated:

- observation-cycle IDs;
- shadow-roster and v0.17-recommendation source pairs;
- counterfactual-observation report digests.

It also rejects broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_shadow_counterfactual_comparison_v0_18.json
indra_qi_shadow_counterfactual_observation_state_v0_18.json
indra_qi_shadow_counterfactual_observation_recommendation_v0_18.json
indra_qi_shadow_counterfactual_observation_ledger_v0_18.jsonl
indra_qi_shadow_counterfactual_observation_receipt_v0_18.json
indra_qi_shadow_counterfactual_observation_audit_v0_18.jsonl
```

## Authority boundary

`shadow_counterfactual_cycle_ready` means only that the supplied shared-input projection evidence satisfies the bounded comparison policy. It grants no lineage-selection, lineage-execution, live-routing, WORLD-update, external-actuation, promotion, rollback, quarantine, or truth authority. Multi-WORLD non-collapse, minority paths, recovery paths, Process Tensor provenance, and non-Markov feedback remain visible.
