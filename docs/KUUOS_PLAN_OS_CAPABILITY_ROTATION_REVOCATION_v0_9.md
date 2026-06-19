# KuuOS PlanOS Capability Rotation and Revocation v0.9

PlanOS v0.9 runs immediately after v0.8 ownership continuity and before the first PLAN stage.

```text
v0.8 ownership root
→ invalidate the previous epoch
→ record all previous capability digests as revoked
→ create the next monotone epoch
→ bind newly issued lower-layer receipts to the current owner
```

The rotated set covers host access, human approval, step authorization, and operation authorization.

After HANDOVER, the previous owner cannot bind or use a new-epoch capability. HOLD also rotates the epoch, so stale pre-resume receipts cannot be reused.

A v0.9 binding records an already issued lower-layer receipt. The wrapper itself grants no execution, host access, approval, memory overwrite, truth, legal, clinical, or institutional authority.

Persistence uses an append-only digest ledger, exclusive locking, fsync, atomic snapshots, deterministic replay, corruption detection, and ledger-derived repair.
