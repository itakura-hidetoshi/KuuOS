# Kū–Indra Qi Reversible Shadow Admission v0.17

## Purpose

v0.17 consumes the exact WORLD state, the v0.15 multi-lineage candidate set, and the v0.16 sandbox-trial state and recommendation. It admits a small, bounded set of sandbox-passed lineages into a shadow roster without selecting a winner, enabling a live route, mutating the WORLD model, or authorizing external action.

A shadow admission is an observation-only representation. It creates a reversible comparison surface for several lineages while preserving minority, recovery, and non-Markov provenance.

## Exact inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_multi_lineage_candidate_set_v0_15.json`;
- `indra_qi_licensed_sandbox_lineage_trial_state_v0_16.json`;
- `indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json`;
- a digest-bound v0.17 plan, proposal, and license.

All source artifacts remain byte-for-byte read-only.

## Shadow admission entry

Each proposed shadow entry declares:

```text
shadow_slot_id
lineage_id
requested_shadow_cycles
observation_budget
shadow_weight
rollback_corridor_digest
shadow_baseline_digest
shadow_overlay_digest
live_route_enabled
external_actuation_enabled
world_update_enabled
policy_boundary_preserved
```

The rollback corridor must exactly match the source candidate lineage. The lineage must have a passing v0.16 sandbox trial. Baseline and overlay digests are mandatory so the shadow state remains isolated and reversible.

## Bounded roster gates

v0.17 verifies:

- minimum and maximum shadow-lineage counts;
- maximum shadow cycles;
- per-lineage and total observation budgets;
- normalized maximum shadow weight;
- lineage-kind diversity;
- recovery-lineage preservation;
- minority-lineage preservation;
- exact rollback-corridor binding;
- sandbox-pass coverage;
- live-route, external-actuation, and WORLD-update disablement.

A roster that merely concentrates almost all shadow weight in one lineage is rejected even when every lineage passed its sandbox trial.

## Relation to v0.16

```text
v0.16 sandbox_trial_set_ready
  + all reversible shadow gates pass
  -> reversible_shadow_admission_ready

v0.16 sandbox_trial_set_ready
  + roster/budget/diversity/reversibility gate fails
  -> redesign_shadow_roster_recommended

live route, external actuation, WORLD update, or policy boundary breach
  -> quarantine_recommended

v0.16 hold / rollback / quarantine
  -> preserve the same recommendation class
```

v0.17 never weakens a v0.16 rollback or quarantine recommendation.

## Replay resistance

The runtime rejects repeated:

- admission-run IDs;
- candidate-set and v0.16 recommendation source pairs;
- shadow-admission proposal digests.

It also rejects broken source, plan, proposal, license, state, or ledger digests.

## Outputs

```text
indra_qi_reversible_shadow_roster_v0_17.json
indra_qi_reversible_shadow_admission_state_v0_17.json
indra_qi_reversible_shadow_admission_recommendation_v0_17.json
indra_qi_reversible_shadow_admission_ledger_v0_17.jsonl
indra_qi_reversible_shadow_admission_receipt_v0_17.json
indra_qi_reversible_shadow_admission_audit_v0_17.jsonl
```

## Authority boundary

`reversible_shadow_admission_ready` means only that the proposed roster satisfies the declared bounded and reversible observation policy. It does not activate traffic, select or execute a lineage, update the WORLD model, actuate the external world, or assert truth. Candidate and shadow weights remain non-truth. Multi-WORLD non-collapse, minority paths, recovery corridors, Process Tensor provenance, and non-Markov feedback remain visible.
