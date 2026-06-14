# Kū–Indra Qi Recoverability-Gated Action Envelope v0.8

## Purpose

v0.8 converts the Process Tensor-conditioned state of `WORLD_{t+1}` into a bounded candidate surface for the next causal cycle.

```text
WORLD_{t+1}
  + v0.7 reentered causal WORLD
  + observation debt
  + recoverability corridor
  + intervention residue
  -> v0.8 recoverability gate
  -> observation / counterfactual / bounded intervention candidates
```

The envelope is not an execution surface. It does not invoke a v14 command, mutate the parent WORLD, mutate the child causal WORLD, or actuate an external system.

## Gate modes

Each observed causal variable receives one of three modes.

### `observe_only`

Used when:

- the target is a Qi-flow observable;
- the recoverability corridor is critical; or
- the integrated risk exceeds the observe-only threshold.

Only a fresh observation request is emitted. A predicted value cannot be reused as an observation.

### `counterfactual_first`

Used when:

- the corridor is constrained;
- risk is intermediate;
- debt is too high for intervention;
- recoverability is insufficient; or
- corridor openness is below the intervention threshold.

A fresh observation request and a non-mutating counterfactual candidate may be emitted. No intervention candidate is admitted.

### `bounded_intervention_candidate`

Used only for a local WORLD patch when all intervention gates are satisfied:

```text
corridor status = open
recoverability >= minimum
observation debt <= maximum
corridor openness >= minimum
risk below counterfactual threshold
```

The output contains only a maximum admissible delta. It does not choose a goal, execute a command, or mutate the causal WORLD.

## Risk surface

The gate integrates:

```text
risk
= debt_weight * observation_debt
+ residue_weight * intervention_residue
+ tension_weight * relational_tension
+ recovery_loss_weight * (1 - recoverability)
```

Candidate priority is a planning score, not a truth value.

## Qi-flow boundary

Qi-flow variables are always observation-only in v0.8.

```text
Qi-flow observable != Qi itself
causal variable != gauge connection
observation request != transport mutation
```

No intervention candidate may target a base Qi-flow channel, IndraNet connection, holonomy, or operator algebra.

## Undo reserve

Every bounded intervention candidate must have a matching undo reserve.

```text
intervention candidate
  -> snapshot required
  -> fresh intervention license required
  -> matching undo reserve required
```

The reserve is incomplete until an approved intervention transaction exists. It is not an executable undo command.

## Lineage validation

v0.8 verifies:

- v0.6 assimilated WORLD digest;
- v0.6 dynamic WORLD-state digest;
- v0.6 assimilation record, seed, and ledger;
- v0.7 reentry record and ledger;
- isolated child runtime location;
- child WORLD digest and protected constitution;
- generated projection plan digest;
- v0.2 projection packet and activation digests;
- v14 causal WORLD digest and initialize event.

The parent WORLD and child causal WORLD are re-read after envelope construction and must remain unchanged.

## Outputs

```text
indra_qi_recoverability_action_envelope_v0_8.json
indra_qi_recoverability_action_envelope_record_v0_8.json
indra_qi_recoverability_action_envelope_ledger_v0_8.jsonl
indra_qi_recoverability_action_envelope_receipt_v0_8.json
indra_qi_recoverability_action_envelope_audit_v0_8.jsonl
```

## Next boundary

A later stage may consume one candidate only after:

- fresh observation evidence;
- explicit approval;
- an exact candidate digest binding;
- a fresh v14 action license;
- snapshot and undo readiness for intervention;
- confirmation that the action still fits the current WORLD digest.
