# Kū–Indra Qi Bounded Generational Cycle v0.12

## Purpose

v0.12 turns the single closed loop completed by v0.11 into a bounded, replay-protected generational runtime. One invocation advances exactly one generation:

```text
source v0.11 child
  -> v0.8 recoverability-gated candidate envelope
  -> v0.9 fresh evidence, approval, child action, and feedback
  -> v0.10 parent Process Tensor activation and cycle evolution
  -> v0.11 dynamic WORLD assimilation and a new isolated child
  -> v0.12 generation state and digest lineage
```

## One generation per invocation

A v0.12 plan binds the exact source v0.11 handoff, record, and ledger digests together with:

- runner ID and generation-run ID;
- monotone generation index;
- maximum generation count;
- exact previous runner-state digest;
- selected action kind;
- all v0.8 through v0.11 IDs and policies;
- convergence thresholds;
- canonical plan digest.

The next invocation must use the target v0.11 handoff written by the previous generation and the latest runner-state digest.

## Bounded stopping

The runner stops after a committed generation when either:

1. `completed_generations == max_generations`; or
2. dynamic WORLD metrics satisfy all configured convergence thresholds:
   - maximum observation debt;
   - minimum recoverability reserve;
   - maximum intervention residue.

A stopped runner cannot start another v0.8 stage.

## Global compensated transaction

Before v0.8, v0.12 snapshots:

- every non-v0.12 root-level runtime file;
- the complete source child runtime tree.

If any v0.8, v0.9, v0.10, v0.11, nested v14/v0.3, or post-write validation fails:

- root-level runtime files are restored byte-for-byte;
- the source child runtime is restored byte-for-byte;
- a partial target child is removed;
- no successful v0.12 state or generation-ledger entry is written.

Thus an action cannot remain in the source child unless its feedback is accepted into the parent Process Tensor cycle and a new child is successfully created.

## Replay protection

The append-only ledger consumes exactly once:

- generation-run ID;
- source v0.11 handoff packet digest.

The runner state also enforces runner ID, maximum generation count, monotone generation index, and previous-state digest continuity.

## Outputs

```text
indra_qi_bounded_cycle_state_v0_12.json
indra_qi_bounded_cycle_handoff_v0_12.json
indra_qi_bounded_cycle_record_v0_12.json
indra_qi_bounded_cycle_ledger_v0_12.jsonl
indra_qi_bounded_cycle_receipt_v0_12.json
indra_qi_bounded_cycle_audit_v0_12.jsonl
```

## Authority boundary

v0.12 does not create truth authority, direct unlicensed execution authority, external-world actuation authority, or base gauge mutation authority. Candidate weighting remains non-truth. All causal children and action effects remain runtime-local and license-gated. Non-Markov feedback and Process Tensor provenance are retained across every generation.
