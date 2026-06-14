# Kū–Indra Qi Process Tensor Cycle Evolution v0.5

## Purpose

v0.5 assimilates the runtime observation overlays activated by v0.4 into a persistent, non-Markovian Qi Process Tensor cycle state.

```text
v0.4 WORLD observation overlays
  -> verify activation / review / ledger / WORLD digest lineage
  -> evolve per-target Process Tensor channels
  -> preserve prior cycle memory
  -> emit next-cycle causal-projection seeds
```

This stage does not mutate the Indra–Qi WORLD. Its outputs are runtime-local external conditioning state.

## Per-channel state

Every activated local-patch or Qi-flow observation becomes a Process Tensor channel containing:

```text
memory_kernel_strength
intervention_residue
nonmarkov_coupling
recoverability_reserve
observation_debt
relational_resonance
next_cycle_prior_weight
```

Each channel is linked to:

- the source WORLD overlay digest;
- the v0.4 Process Tensor assessment digest;
- the source process-history digest;
- the previous channel-state digest.

## Evolution

The cycle update retains part of the previous state and assimilates the new observation:

```text
new memory
= retention * previous memory
+ (1 - retention) * observed influence
```

The same bounded pattern is used for intervention residue, non-Markov coupling, recoverability, and observation debt. The source v14 event kind controls the intervention-residue contribution:

```text
observe < counterfactual < undo < intervene
```

These values are operational conditioning signals, not physical substances or truth values.

## Observation debt and recovery

Observation debt increases with uncertainty, low candidate weight, and unresolved Process Tensor debt. Recoverability reserve is propagated from the v0.4 assessment and prior cycle state.

A channel may remain in the Process Tensor state while being withheld from the next-cycle seed packet when:

- prior weight is too low;
- observation debt is too high;
- recoverability reserve is too low.

## Next-cycle seed

The seed packet contains only channels satisfying the configured thresholds. Every entry declares:

```text
seed_not_fact = true
seed_not_truth = true
seed_not_direct_execution_authority = true
seed_requires_new_projection_license = true
```

The packet can condition a later v0.2-style projection, but cannot initialize or mutate a causal WORLD by itself.

## Digest chain

The cycle state records:

```text
previous_cycle_state_digest
source_activation_record_digest
source_process_tensor_review_digest
source_feedback_packet_digest
source_world_state_digest
```

The append-only cycle ledger additionally links each cycle record through `prev_record_digest`.

## Protected boundaries

```text
source WORLD state is unchanged
operator algebra is unchanged
gauge connections are unchanged
holonomy is preserved
two-truths gap is preserved
candidate weighting is not truth
Process Tensor state is not execution authority
```

## Runtime outputs

```text
indra_qi_process_tensor_cycle_state_v0_5.json
indra_qi_next_cycle_projection_seed_v0_5.json
indra_qi_process_tensor_cycle_ledger_v0_5.jsonl
indra_qi_process_tensor_cycle_receipt_v0_5.json
indra_qi_process_tensor_cycle_audit_v0_5.jsonl
```
