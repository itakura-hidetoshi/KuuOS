# Kū–Indra Qi Parent Cycle Assimilation Reentry v0.11

## Purpose

v0.11 completes the next closed-loop transition after v0.10. It consumes the exact v0.10 parent-cycle handoff, assimilates the new v0.5 Process Tensor cycle into the parent dynamic WORLD through v0.6, and creates a fresh isolated causal child through v0.7.

```text
v0.10 child feedback -> parent Process Tensor cycle
  -> v0.11 exact source validation
  -> v0.6 dynamic WORLD assimilation
  -> v0.7 post-assimilation causal reentry
  -> new isolated child v14 causal WORLD
```

## Exact source binding

The v0.11 plan binds:

- v0.10 bridge ID;
- v0.10 handoff packet digest;
- v0.10 bridge-record digest;
- v0.10 ledger-record digest;
- current parent WORLD digest;
- current v0.5 cycle ID and state digest;
- current v0.5 seed digest;
- expected previous dynamic WORLD digest;
- new v0.6 assimilation ID;
- new v0.7 reentry, projection, causal WORLD, and transaction IDs;
- v0.6 assimilation policy;
- v0.7 projection policy;
- canonical v0.11 plan digest.

## v0.6 assimilation

Only the existing v0.6 runtime may mutate the parent WORLD. Mutation remains restricted to the Process Tensor dynamic WORLD layer.

The following remain unchanged:

- operator algebra;
- base gauge connection identity;
- base holonomy identity;
- runtime observation-overlay history;
- Mandala non-collapse and two-truths boundary;
- external-world separation.

Observation debt, recoverability, effective transport, and effective holonomy conditions are updated as dynamic state, not as base structure replacement.

## v0.7 reentry

After successful v0.6 assimilation, v0.11 binds the new WORLD digest, dynamic-state digest, assimilation record, and post-assimilation seed into a new v0.7 plan.

v0.7 creates a new child runtime under:

```text
indra_qi_causal_reentry_cycles_v0_7/<reentry_id>/
```

The child receives a copy of the assimilated parent WORLD and initializes the existing v0.2 projection and v14 causal WORLD. Qi remains an observable projection, never a substance identity or gauge-connection replacement.

## Compensated transaction

v0.6 and v0.7 form one compensated transaction.

Before v0.6, v0.11 snapshots the bytes or absence of:

- parent WORLD;
- v0.6 rollback snapshot, seed, record, ledger, receipt, and audit;
- v0.7 record, ledger, receipt, and audit.

The target child runtime must not already exist.

If v0.6, v0.7, nested v0.2/v14, or post-write verification fails:

1. every touched parent file is restored to its exact prior bytes;
2. a partially created child runtime is removed;
3. no v0.11 success record or ledger line is written.

This prevents a parent WORLD from remaining assimilated when the next causal cycle was not successfully created.

## Replay protection

The v0.11 ledger consumes exactly once:

- loop ID;
- source v0.10 handoff packet digest.

Replay blocks before v0.6 invocation.

## Outputs

```text
indra_qi_parent_cycle_assimilation_reentry_handoff_v0_11.json
indra_qi_parent_cycle_assimilation_reentry_record_v0_11.json
indra_qi_parent_cycle_assimilation_reentry_ledger_v0_11.jsonl
indra_qi_parent_cycle_assimilation_reentry_receipt_v0_11.json
indra_qi_parent_cycle_assimilation_reentry_audit_v0_11.jsonl
```

The handoff packet links the v0.10 cycle, v0.6 WORLD update, v0.7 reentry, child projection, and child v14 WORLD digests.

## Authority boundary

v0.11 does not grant direct execution authority, truth authority, external-world actuation authority, or base gauge mutation authority. Candidate weighting remains non-truth, and the generated child causal WORLD remains runtime-local and internal.
