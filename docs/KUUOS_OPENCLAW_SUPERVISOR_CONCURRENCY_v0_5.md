# KuuOS OpenClaw Supervisor v0.5 — concurrency correction

## Why this correction exists

The first v0.5 implementation had two independent reconciliation workers:

```text
periodic reconciliation
gap-triggered reconciliation
```

Both eventually called the same v0.3 audit intake.  Although v0.3 writes its checkpoint atomically, two supervisor-owned processes could still read the same old checkpoint concurrently, append overlapping candidates, and race the final checkpoint replacement.

That is not acceptable for the intended append-only observation lineage.

## single-writer boundary

The public v0.5 entrypoint now retains the original implementation in
`runtime/kuuos_openclaw_supervisor_v0_5_impl.py` and wraps every supervisor-owned `run_audit_once` call with one shared process-local lock.

```text
periodic reconciliation -----\
                              > shared audit lock -> v0.3 child process
gap-triggered reconciliation-/
initial reconciliation -------/
```

Therefore, inside one v0.5 supervisor process, v0.3 reconciliation is **single-writer**.

This lock does not create WORLD authority, verification authority, PlanOS completion authority, or rollback authority. It only serializes local observation-ledger maintenance.

## External process boundary

The lock is process-local by design. An **external manual v0.3 process** launched independently by an operator does not acquire this supervisor lock.

Therefore the guarantee is deliberately stated as:

```text
supervisor-internal audit writers are serialized
```

not:

```text
all possible processes on the machine are globally serialized
```

A future file-lock protocol shared directly by v0.3 may strengthen this boundary if cross-process concurrency becomes an operational requirement.

## unterminated JSONL tail

The live WebSocket subscriber appends JSONL concurrently with the supervisor reader. A reader can in principle reach EOF after seeing only part of the writer's final append.

The hardened reader therefore treats an **unterminated JSONL tail** as incomplete rather than corrupt:

```text
complete line ending in newline
  -> parse now

EOF tail without newline
  -> seek back to beginning of that record
  -> return only earlier complete records
  -> retry the tail on the next poll

complete line with invalid JSON
  -> fail closed as corruption
```

This distinguishes normal concurrent append timing from actual complete-record corruption.

## Authority remains unchanged

Serialization and tail deferral do not create WORLD authority. In particular:

```text
single-writer != WORLD commit
complete JSONL line != verified truth
successful reconciliation != PlanOS completion
component failure != rollback proof
```
