# KuuOS Autonomous Mission Cycle Kernel v0.21

v0.21 persists the complete cycle:

```text
Mission → Plan → Act → Observe → Verify → Learn → Replan
```

Each accepted phase transition is bound to the active v0.20 mission contract, the current v0.20 mission-state digest, the current v0.21 cycle-state digest, and one phase artifact digest.

## Phase order

Only these transitions are legal:

```text
Mission → Plan
Plan → Act
Act → Observe
Observe → Verify
Verify → Learn
Learn → Replan
Replan → Plan
```

No phase can be skipped. Replan closes the current cycle, appends a cycle summary, increments the cycle index, resets only the per-cycle cost, and opens the next Plan phase.

## Persistent state

The state records mission identity, contract digest, latest mission-state digest, cycle index, current phase, event index, current and cumulative cost, phase artifact digests, processed event digests, event history, cycle summaries, predecessor digest, and current state digest.

## Real Act receipt

Act is not represented as a dry run. `Plan → Act` requires:

- `action_receipt_digest`
- `lower_authority_receipt_digest`
- `licensed_effect_applied = true`

The lower receipt is produced by the existing licensed host invocation path. v0.21 stores the result but does not broaden that license.

## Verify and Learn

Verify records `passed`, `failed`, or `indeterminate` together with a verification evidence digest.

Learn is accepted only with:

```text
future_only = true
memory_overwrite = false
```

Historical events remain immutable. Learning can affect a later plan only through Replan.

## Durable store

```text
genesis.json
snapshot.json
cycle-ledger.jsonl
.mission-cycle.lock
```

`genesis.json` is the immutable starting point. `cycle-ledger.jsonl` is the append-only record. `snapshot.json` is reconstructed from genesis plus the ledger.

For every event the store:

1. recovers the current state;
2. validates source digests, phase order, evidence, and budget;
3. computes the next state;
4. appends and fsyncs one commit record;
5. atomically replaces the snapshot.

A stale snapshot can be repaired only from the verified ledger. A broken digest chain, malformed ledger line, stale event, duplicate non-idempotent update, or phase-order violation fails closed.

## Replay and budget

A previously committed event returns `REPLAYED` without another ledger append. New events carrying an old state digest are rejected.

Each event cost must be finite and non-negative. The kernel enforces both the v0.20 per-cycle limit and the usable total budget after the reserve floor.

## Boundary

v0.21 preserves the lower execution boundary. It persists actual licensed action receipts and the learning cycle; it does not create new tool, network, shell, theorem, clinical, truth, memory-overwrite, or final-commitment permissions.
