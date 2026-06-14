# Kū–Indra Qi → Causal WorldModel Projection Bridge v0.2

## Purpose

This bridge projects bounded observables from the noncommutative Indra–Qi Mandala WORLD substrate into the local conventional causal model used by KuuOS v14.0.

```text
Indra–Qi Mandala WORLD state
  -> select local observables and Qi-flow observables
  -> preserve source bindings and process-tensor lineage
  -> construct a bounded affine causal DAG
  -> invoke KuuOS v14.0 initialize
```

## Non-identity boundaries

```text
causal DAG != complete Mandala WORLD
causal edge != IndraNet gauge connection
causal variable != Qi itself
Qi-flow observable projection != Qi as substance
v14 internal state initialization != external-world actuation
```

A variable named `qi` is rejected. Qi can enter the causal layer only through a declared `qi_flow_observable_projection` binding with:

```text
qi_itself = false
projection_not_flow_identity = true
```

## Projection plan

The plan contains:

- source Indra–Qi WORLD id and digest;
- target v14 causal WORLD id;
- one-time projection and transaction ids;
- causal variables with source bindings;
- declarative affine mechanisms;
- an annotation for every causal edge;
- non-reification and non-authority boundaries.

Every causal edge annotation must state:

```text
edge_kind = local_causal_projection_only
not_indra_connection = true
not_gauge_equivalence_claim = true
not_qi_flow_identity = true
```

## Process-tensor lineage

The bridge aggregates the process-tensor context of the source Qi-flow channels into the v14 initialize command while retaining the original source values in the projection packet.

Required source context:

```text
process_tensor_digest
memory_kernel_digest
history_window_digest
instrument_trace_digest
non_markov_context_digest
```

## Mutation boundary

The bridge initializes the internal v14 causal WORLD model. It does not mutate:

- the source Indra–Qi WORLD state;
- local operator algebras;
- IndraNet gauge connections;
- Mandala inclusion;
- the external world.

Further changes to the gauge substrate require a stronger and separately bound license.

## Runtime outputs

```text
indra_qi_causal_projection_packet_v0_2.json
indra_qi_causal_projection_activation_record_v0_2.json
indra_qi_causal_projection_ledger_v0_2.jsonl
indra_qi_causal_projection_receipt_v0_2.json
indra_qi_causal_projection_audit_v0_2.jsonl
kuuos_causal_world_model_state_v14_0.json
```

## Fail-closed conditions

The bridge blocks on source digest loss, Qi substance reification, unknown source bindings, direct Qi identity variables, missing edge annotations, causal cycles, missing non-Markov context, replay, license mismatch, v14 initialization failure, or any change to the source Indra–Qi state during projection.
