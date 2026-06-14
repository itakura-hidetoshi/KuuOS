# Kū–Indra Qi Multi-Lineage Evolution v0.15

## Purpose

v0.15 consumes the read-only WORLD state and the exact v0.14 WORLD Qi-QUE path-ecology state and recommendation. It does not choose or execute a lineage. It evaluates whether a bounded candidate set preserves enough diversity, minority visibility, recoverability, re-observation capacity, and holonomy-scar avoidance to support a later licensed consumer.

The layer closes a gap left after v0.14: detecting false stability is not sufficient unless the runtime can also represent several non-equivalent, recoverable ways to reopen the WORLD ecology without collapsing immediately into a new single path.

## Inputs

Each run binds:

- `ku_indra_qi_noncommutative_mandala_world_state.json`;
- `indra_qi_world_qique_path_ecology_state_v0_14.json`;
- `indra_qi_world_qique_path_ecology_recommendation_v0_14.json`;
- a digest-bound v0.15 evolution plan;
- a digest-bound lineage proposal;
- a license bound to all source and proposal digests.

All source artifacts are read-only.

## Candidate lineage packet

A candidate lineage declares:

```text
lineage_id
lineage_kind
source_patch
target_patch
connection_ids
candidate_weight
rollback_corridor_digest
observation_projection_digest
process_tensor_context_digest
non_markov_context_digest
preserves_minority_path
recovery_path
reobserve_path
```

Connection paths must exist in the WORLD state, match the declared endpoints, and remain contiguous. Candidate weights are normalized for comparison but never interpreted as truth probabilities or automatic selection authority.

## Diversity-preserving analysis

v0.15 computes:

- normalized maximum candidate weight;
- pairwise connection-path overlap;
- target-patch diversity;
- lineage-kind diversity;
- combined lineage-diversity score;
- recovery-lineage count;
- minority-lineage count;
- reobserve-lineage count;
- dominant-patch egress count;
- holonomy-scar avoidance ratio.

A candidate set fails diversity preservation when it merely duplicates the same route under several identifiers, concentrates most weight in one lineage, omits minority or recovery corridors, or remains trapped inside the dominant holonomy scar cycle.

## Relation to v0.14

```text
v0.14 ecology_compatible_bounded_promotion
  + diverse candidate set
  -> diverse_bounded_evolution_ready

v0.14 reopen_branches_recommended
  + recovery + minority + dominant-patch egress
  -> branch_reopening_candidate_set_ready

v0.14 focus_or_reobserve_recommended
  + focus + reobserve candidates
  -> focus_reobserve_candidate_set_ready

candidate requirements fail
  -> redesign_candidate_set_recommended

v0.14 hold / rollback / quarantine
  -> preserve the same recommendation class
```

v0.15 never weakens a v0.14 rollback or quarantine recommendation.

## Replay and lineage integrity

The runtime rejects:

- a repeated evolution-run ID;
- a repeated WORLD-state and v0.14-recommendation source pair;
- a repeated lineage-proposal digest;
- broken ledger chaining;
- invalid source, plan, proposal, state, or license digests.

Boundary loss fails closed and yields a quarantine recommendation without committing a candidate set.

## Decisions

The runtime emits exactly one recommendation:

- `hold_for_observation`;
- `diverse_bounded_evolution_ready`;
- `branch_reopening_candidate_set_ready`;
- `focus_reobserve_candidate_set_ready`;
- `redesign_candidate_set_recommended`;
- `rollback_recommended`;
- `quarantine_recommended`.

A “ready” result means only that the candidate set satisfies the declared bounded ecology gates. It does not select, execute, promote, mutate, or actuate any lineage.

## Outputs

```text
indra_qi_multi_lineage_candidate_set_v0_15.json
indra_qi_multi_lineage_evolution_state_v0_15.json
indra_qi_multi_lineage_evolution_recommendation_v0_15.json
indra_qi_multi_lineage_evolution_ledger_v0_15.jsonl
indra_qi_multi_lineage_evolution_receipt_v0_15.json
indra_qi_multi_lineage_evolution_audit_v0_15.jsonl
```

## Authority boundary

v0.15 grants no lineage-selection, lineage-execution, WORLD-update, promotion, rollback, quarantine, external-actuation, or truth authority. It preserves multi-WORLD non-collapse, candidate-weighting-as-non-truth, non-Markov feedback, Process Tensor provenance, visible holonomy scars, minority paths, and recovery corridors.
