# KuuOS PlanOS Re-Rotation Materialization v0.13

PlanOS v0.13 turns a v0.12 `REROTATION_AUTHORIZED` decision into a fresh executable-control chain without reusing the old epoch.

```text
v0.12 re-rotation authorization
→ fresh v0.9-compatible capability epoch state
→ four fresh lower-authority capability bindings
→ fresh v0.10 scoped leases
→ fresh v0.11 renewal ceilings
```

The exact v0.12 decision digest, seed digest, owner, current epoch, next epoch, source v0.11 state, and source lease state are required.

All old capability digests are copied into the new epoch revocation set. A new capability digest or lower-authority receipt cannot be reused across kinds, and no old capability digest may appear in the new binding set.

The new lease state starts with empty consumption and renewal histories. The new renewal governance state starts with zero renewal count, zero added uses, and zero added cost for every capability kind.

Materialization does not grant execution, host access, automatic renewal, memory overwrite, truth authority, or professional authority.

Persistence is single-materialization, append-only, digest-bound, replay-idempotent, fsync-backed, atomically snapshotted, and recoverable from the ledger.
