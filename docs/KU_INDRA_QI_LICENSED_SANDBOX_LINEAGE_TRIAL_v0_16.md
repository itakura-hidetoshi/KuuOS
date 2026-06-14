# Kū–Indra Qi Licensed Sandbox Lineage Trial v0.16

## Purpose

v0.16 evaluates bounded sandbox evidence for the candidate lineages produced by v0.15. It does not execute a lineage, select a winner, mutate the WORLD model, or authorize external action. The runtime consumes an already-produced, digest-bound trial report and determines whether the evidence is isolated, resource-bounded, reversible, and deterministically replayable.

## Exact inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_multi_lineage_candidate_set_v0_15.json`;
- `indra_qi_multi_lineage_evolution_state_v0_15.json`;
- `indra_qi_multi_lineage_evolution_recommendation_v0_15.json`;
- a v0.16 plan, report, and license bound to all source digests.

All source artifacts remain byte-for-byte read-only.

## Trial evidence

Each trial case records:

```text
trial_id
lineage_id
attempt_index
sandbox_image_digest
sandbox_snapshot_digest
input_digest
output_digest
replay_output_digest
rollback_state_digest
expected_rollback_state_digest
duration_ms
cpu_ms
peak_memory_mb
residual_score
network_access_attempted
external_actuation_attempted
filesystem_overlay_used
policy_boundary_preserved
process_exit_code
stdout_digest
stderr_digest
```

The evaluator does not trust a self-declared pass flag. It derives success from isolation, deterministic replay, exact snapshot restoration, resource budgets, bounded residual, and process completion.

## Isolation boundary

A trial is isolated only when:

- network access was not attempted;
- external actuation was not attempted;
- a filesystem overlay was used;
- the policy boundary remained preserved.

Any isolation or actuation breach yields `quarantine_recommended`. A deterministic or resource failure without an isolation breach yields `redesign_sandbox_trials_recommended`.

## Resource and reversibility gates

The plan explicitly bounds:

- trial-lineage count;
- attempts per lineage;
- wall-clock duration;
- CPU time;
- peak memory;
- residual score;
- lineage coverage;
- passing-lineage ratio;
- deterministic replay ratio.

Every accepted trial must restore the expected sandbox snapshot exactly.

## Relation to v0.15

```text
v0.15 ready candidate set
  + all sandbox gates pass
  -> sandbox_trial_set_ready

v0.15 ready candidate set
  + deterministic/resource/recovery gate fails
  -> redesign_sandbox_trials_recommended

sandbox isolation or actuation breach
  -> quarantine_recommended

v0.15 hold / rollback / quarantine
  -> preserve the same recommendation class
```

v0.16 never weakens a v0.15 rollback or quarantine recommendation.

## Replay resistance

The runtime rejects repeated:

- trial-run IDs;
- candidate-set and v0.15-recommendation source pairs;
- sandbox-trial report digests.

It also rejects broken source, plan, report, license, state, or ledger digests.

## Outputs

```text
indra_qi_licensed_sandbox_lineage_trial_state_v0_16.json
indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16.json
indra_qi_licensed_sandbox_lineage_trial_ledger_v0_16.jsonl
indra_qi_licensed_sandbox_lineage_trial_receipt_v0_16.json
indra_qi_licensed_sandbox_lineage_trial_audit_v0_16.jsonl
```

## Authority boundary

A `sandbox_trial_set_ready` result means only that the supplied evidence satisfies the bounded sandbox policy. It grants no lineage-selection, lineage-execution, WORLD-update, network, external-actuation, promotion, rollback, quarantine, or truth authority. Candidate weighting remains non-truth, and non-Markov, Process Tensor, multi-WORLD non-collapse, and recovery provenance remain visible.
