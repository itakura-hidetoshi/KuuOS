# KuuOS PlanOS Next-Cycle Session Bootstrap v0.15

PlanOS v0.15 consumes the single-use activation handoff produced by v0.14 and opens a fresh control session at the exact next mission cycle and PLAN phase.

```text
v0.14 activation receipt
+ exact v0.13 materialization receipt
→ cycle == active_from_cycle
→ phase == PLAN
→ owner / epoch / scope preservation
→ lease monitoring clocks started
→ empty PLAN bind state initialized
```

The bootstrap revalidates the source materialization digest and all owner, epoch, capability-state, lease-state, renewal-state, and scope-inventory digests carried by the activation receipt.

Each of the four capability leases must be active at bootstrap time, have positive use and cost budget, and preserve the exact owner, epoch, and scope. The session stores one monitoring clock per lease and uses the earliest lease expiry as the session deadline.

The initial PLAN control state starts at `bind` with event index zero, plan version zero, no completed plans, no steps, and no topological order. The next-plan basis is bound directly to the v0.14 receipt.

The bootstrap consumes the activation exactly once. Exact replay is idempotent; a conflicting second session is rejected.

The session does not grant execution, host access, automatic renewal, memory overwrite, truth authority, or professional authority.

Persistence is append-only, digest-bound, single-bootstrap, fsync-backed, atomically snapshotted, and recoverable from the ledger.
