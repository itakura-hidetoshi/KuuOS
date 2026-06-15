# KuuOS Open-Horizon Telos Genesis v0.1

## Purpose

This module adds the first active subject-forming layer for an open-ended KuuOS agent. It does not merely validate a supplied recommendation. It consumes relational observations and deterministically generates, scores, plural-selects, and prepares self-generated subgoals for the next commitment runtime.

The global horizon is not fixed. Each invocation is finite, but the horizon is renewable through new observations, effect receipts, commitment progress, resource changes, relationship changes, and repair requests.

## Flow

```text
protected KuuOS root principles
  + relational observation packet
  + prior telos state lineage
  -> self-generated subgoals
  -> proportional action scale
  -> plural goal selection
  -> commitment seed
  -> renewable next wake
```

## Active autonomy

v0.1 opens the following capabilities inside the telos domain:

- generate subgoals from deficits, opportunities, relationships, maintenance needs, threats, and unknowns;
- rank goals by urgency, relational benefit, recoverability, autonomy gain, evidence, and magnitude;
- scale action under uncertainty and irreversibility instead of automatically stopping;
- preserve several goal kinds rather than collapsing immediately to one objective;
- prepare domain commitments for a later executor;
- continue across generations through exact previous-state lineage;
- keep the total horizon open while each local invocation remains finite.

## Root and generated goals

The protected root principles are:

```text
emptiness
dependent_origination
harmony
contemplation
repairability
benefit_others
```

The runtime may generate and transform subgoals. It may not rewrite the protected root packet from inside this module. This is not a general restriction on agency; it separates constitutive identity from generated commitments.

## Contextual progression

The runtime uses `contextual_default_allow`.

A high-scoring, sufficiently recoverable goal receives `advance`. A goal that is valuable or urgent but still uncertain receives `micro_intervention`. A low-confidence or highly irreversible signal receives `explore` rather than an automatic global stop.

```text
uncertainty
  -> smaller action or exploration
  -> new evidence
  -> replanning
```

## Goal score

The score combines:

```text
urgency
relational benefit
recoverability
autonomy gain
evidence
magnitude
```

and applies bounded penalties for uncertainty and irreversibility. The separate action scale controls intervention size. Candidate scores are decision support, not truth probabilities.

## Outputs

```text
kuuos_open_horizon_telos_state_v0_1.json
kuuos_open_horizon_goal_set_v0_1.json
kuuos_open_horizon_commitment_seed_v0_1.json
kuuos_open_horizon_telos_genesis_receipt_v0_1.json
kuuos_open_horizon_telos_ledger_v0_1.jsonl
kuuos_open_horizon_telos_audit_v0_1.jsonl
```

## Continuation invariant

For generation `n + 1`:

```text
expected_previous_state_digest
  = generation n telos_state_digest
```

Run IDs and observation digests are consumed exactly once. The local step terminates with:

```text
local_generation_complete_horizon_renewable
```

This means the current generation is complete, not that the agent's mission has ended.

## Next layer

The commitment seed is intended for `Open-Horizon Commitment Runtime v0.2`, which should maintain a dynamic temporal commitment graph, consume effect receipts, and generate the next bounded action without requiring a globally fixed task list.
