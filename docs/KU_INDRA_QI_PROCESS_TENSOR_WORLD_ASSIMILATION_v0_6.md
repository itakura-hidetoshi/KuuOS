# Kū–Indra Qi Process Tensor WORLD Assimilation v0.6

## Purpose

v0.6 assimilates the debt, recoverability, memory, intervention residue, and non-Markov coupling produced by v0.5 into the Indra–Qi WORLD itself.

```text
v0.5 Process Tensor cycle state
  -> validate cycle / seed / ledger / WORLD lineage
  -> rollback snapshot
  -> mutate dynamic WORLD state
  -> verify constitution and overlay history
  -> emit a seed bound to the new WORLD digest
```

Unlike v0.5, this stage changes the WORLD state. It does not change the constitutional structure of the WORLD.

## WORLD layers

The WORLD is divided into:

```text
constitutional structure
  operator algebras
  IndraNet identities and base gauge connections
  base Qi-flow definitions
  base holonomy cycles
  Mandala inclusion
  two-truths and governance boundaries

dynamic WORLD state
  local-patch effective state
  Qi-flow effective transport state
  observation debt ledger
  recoverability corridors
  effective holonomy residue state
```

v0.6 writes only the dynamic layer.

## Local-patch dynamic state

Each local-patch channel may update:

```text
memory_kernel_strength
intervention_residue
nonmarkov_coupling
recoverability_reserve
observation_debt
relational_resonance
relational_tension
effective_response_capacity
observation_sensitivity
recoverability corridor openness and branch capacity
```

Debt and recoverability therefore alter the patch's present response possibilities, not only the priority of a later decision.

## Qi-flow effective state

Each Qi-flow channel may update:

```text
effective_transport_resistance
effective_transport_coefficient
effective_holonomy_residue_pressure
```

This is an effective historical state of transport. It does not replace or silently rewrite the base IndraNet connection.

## Observation debt

Every assimilation appends an observation-debt transition containing:

```text
previous debt
current debt
debt delta
source cycle digest
source dynamic-state digest
```

Debt is unresolved observation and intervention burden. It is not moral blame, punishment, or truth.

## Recoverability corridors

Recoverability is represented as a structured possibility surface:

```text
corridor openness
branch capacity
status = open / constrained / critical
```

A corridor describes available repair branches. It is not permission to execute an intervention and is not a guaranteed outcome.

## Effective holonomy

The base holonomy digest is preserved. v0.6 adds an effective historical state derived from flow residue, debt, and recoverability:

```text
base holonomy remains unchanged
effective residue pressure changes
recoverability modulation changes
historical status changes
```

## Mutation and rollback

Before changing the WORLD, v0.6 writes a complete rollback snapshot. After writing it verifies:

```text
WORLD digest
Process Tensor dynamic-state digest
constitutional-structure digest
runtime observation-overlay history digest
```

Any verification failure restores the prior WORLD state.

## Post-assimilation seed

The v0.5 seed is reweighted using the assimilated WORLD state. The resulting packet is bound to the new WORLD digest.

```text
post-assimilation seed
  = prior seed
  conditioned by memory, debt, recoverability,
    tension, residue, and effective capacity
```

The seed remains non-factual and requires a new causal-projection license.

## Runtime outputs

```text
indra_qi_world_assimilation_rollback_snapshot_v0_6_<assimilation_id>.json
indra_qi_process_tensor_world_assimilation_record_v0_6.json
indra_qi_process_tensor_world_assimilation_ledger_v0_6.jsonl
indra_qi_post_assimilation_projection_seed_v0_6.json
indra_qi_process_tensor_world_assimilation_receipt_v0_6.json
indra_qi_process_tensor_world_assimilation_audit_v0_6.jsonl
```

The source `ku_indra_qi_noncommutative_mandala_world_state.json` receives the dynamic WORLD fields and a new WORLD digest.
