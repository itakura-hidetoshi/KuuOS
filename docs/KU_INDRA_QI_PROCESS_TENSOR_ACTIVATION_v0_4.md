# Kū–Indra Qi Process Tensor Activation v0.4

## Purpose

This stage reviews v0.3 causal-feedback candidates through the Qi Process Tensor and applies only explicitly approved, licensed, history-supported candidates to the Indra–Qi WORLD state.

```text
v0.3 feedback candidates
  -> explicit human/governance review decisions
  -> Qi Process Tensor assessment
  -> bounded digest-bound mutation license
  -> rollback snapshot
  -> append-only runtime observation overlays
  -> post-write verification
```

## Qi and Process Tensor

```text
Qi = history-bearing relational flow
Process Tensor = the multi-time non-Markovian structure of that flow
```

The activation review treats Qi as a recoverability-aware process containing observations, interventions, memory links, unresolved observation debt, repair witnesses, and future branching capacity.

The Process Tensor conditions candidate admissibility but does not grant mutation authority. Authority requires a separate explicit license bound to the exact activation-plan digest.

## Required Process Tensor visibility

The existing `Qi Process Tensor evaluator v0.1` is used to require:

```text
process_tensor_visible
transition_continuity_visible
memory_continuity_visible
nonmarkov_memory_visible
```

The v0.4 review additionally calculates:

```text
history_depth
transition_continuity_score
memory_continuity_score
nonmarkov_link_density
recoverability_branching_capacity
observation_debt_pressure
```

These correspond to the established KuuOS interpretation of Qi stagnation and recovery:

```text
Qi stagnation
= process-history compression failure
+ observation debt accumulation
+ recoverability narrowing
+ memory-kernel degradation
```

## Mutation surface

The only writable WORLD surface is:

```text
/runtime_observation_overlays
```

The runtime adds this as an append-only top-level WORLD-state surface. Each overlay records:

- target local patch or Qi-flow observable;
- proposed observed value and uncertainty;
- candidate weight;
- source feedback and process-history digests;
- Process Tensor assessment digest;
- previous-overlay digest;
- rollback and non-authority boundaries.

The following structures are protected and must retain the same digest:

```text
local operator algebras
IndraNet gauge connections
Qi flow definitions
holonomy cycles
Kū-string correspondences
extended M-brane surfaces
Mandala inclusion
two-truths and governance boundaries
```

## Review decisions

Every v0.3 candidate must receive one explicit decision:

```text
approve
reject
```

An approved candidate is applied only when it also satisfies all Process Tensor thresholds and the candidate-weight threshold. A rejected candidate resolves its review debt but is not written to the WORLD overlay.

## Rollback corridor

Before mutation, the complete prior WORLD state is written to a digest-bearing rollback snapshot. After mutation, the runtime re-reads the WORLD state and verifies:

```text
WORLD digest is valid
protected-structure digest is unchanged
overlay count is correct
```

Verification failure restores the prior snapshot state.

## Non-authority boundaries

```text
Process Tensor support != mutation authority
candidate weight != truth
review record != execution authority
WORLD overlay != external-world actuation
receipt != theorem or clinical authority
```

## Runtime outputs

```text
indra_qi_process_tensor_review_v0_4.json
indra_qi_world_rollback_snapshot_v0_4_<activation_id>.json
indra_qi_process_tensor_activation_record_v0_4.json
indra_qi_world_observation_overlay_ledger_v0_4.jsonl
indra_qi_process_tensor_activation_receipt_v0_4.json
indra_qi_process_tensor_activation_audit_v0_4.jsonl
```

The source `ku_indra_qi_noncommutative_mandala_world_state.json` is directly updated only within the bounded observation-overlay surface.
