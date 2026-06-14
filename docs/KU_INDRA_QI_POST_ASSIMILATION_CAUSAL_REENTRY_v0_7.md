# Kū–Indra Qi Post-Assimilation Causal Reentry v0.7

## Purpose

v0.7 closes the loop from the Process Tensor-assimilated WORLD back into a new causal WORLD cycle.

```text
WORLD_t
  -> causal projection / observation / intervention
  -> feedback / Process Tensor / debt and recoverability
  -> WORLD_{t+1}
  -> v0.7 causal reentry
  -> a new isolated v14 causal WORLD
```

The reentry is conditioned by the new WORLD digest produced by v0.6. It cannot use the pre-assimilation WORLD digest.

## Isolated cycle runtime

A new child runtime root is created for every reentry:

```text
indra_qi_causal_reentry_cycles_v0_7/<reentry_id>/
```

The assimilated WORLD is copied without changing its digest. The existing v0.2 causal-projection bridge and v14 initialize command run inside that isolated root. Earlier causal cycles are not overwritten.

## Projection values

The post-assimilation seed is joined to the matching dynamic WORLD state.

For a local WORLD patch:

```text
projected value = effective_response_capacity
```

For a Qi-flow observation:

```text
projected value = effective_transport_coefficient
```

Projection uncertainty is derived from the assimilated WORLD:

```text
uncertainty
= debt_gain * observation_debt
+ residue_gain * intervention_residue
```

Thus debt and recoverability do not merely annotate the next cycle. They alter its initial observable state and uncertainty surface.

## Causal mechanism

All admitted post-assimilation variables become parents of a derived adaptive-response variable. Mechanism weights are bounded versions of the assimilated prior weights. Mechanism noise is conditioned by the mean debt-residue uncertainty.

A causal edge remains a local projection only. It is not an IndraNet connection and cannot rewrite a gauge connection.

## Non-Markov lineage

The reentry record links:

```text
v0.6 assimilation record digest
v0.6 post-assimilation seed digest
new WORLD digest
new dynamic WORLD-state digest
generated projection-plan digest
v0.2 projection packet digest
v0.2 activation digest
v14 causal WORLD digest
```

The parent WORLD is re-read after initialization and must remain unchanged.

## Authority boundaries

```text
post-assimilation seed != fact
causal WORLD != complete ontology
candidate weight != truth
v14 internal state != external-world actuation
causal edge != gauge connection
Process Tensor conditioning != execution authority
```

A new projection license and a nested v14 initialize license are required for every cycle.

## Outputs

Parent runtime:

```text
indra_qi_post_assimilation_causal_reentry_record_v0_7.json
indra_qi_post_assimilation_causal_reentry_ledger_v0_7.jsonl
indra_qi_post_assimilation_causal_reentry_receipt_v0_7.json
indra_qi_post_assimilation_causal_reentry_audit_v0_7.jsonl
```

Child runtime:

```text
ku_indra_qi_noncommutative_mandala_world_state.json
indra_qi_generated_causal_projection_plan_v0_7.json
indra_qi_causal_projection_packet_v0_2.json
indra_qi_causal_projection_activation_record_v0_2.json
kuuos_causal_world_model_state_v14_0.json
```
