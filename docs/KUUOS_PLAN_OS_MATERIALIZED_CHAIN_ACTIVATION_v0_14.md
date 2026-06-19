# KuuOS PlanOS Materialized Chain Activation Gate v0.14

PlanOS v0.14 validates a v0.13 materialized control chain before issuing a handoff to the next PLAN cycle.

```text
v0.13 materialization receipt
→ BOUND capability state
→ all four leases ACTIVE and current
→ owner / epoch / capability / binding cross-links
→ fresh renewal governance
→ single-use next-cycle PLAN handoff
```

Activation is allowed only while every lease satisfies `not_before <= now < expires_at`, has positive use and cost budget, and remains bound to the exact capability and binding digest from the materialized v0.9 state.

The v0.11 governance state must still have zero renewal count, zero cumulative added uses, zero cumulative added cost, no governed renewal receipt, and no consumption or renewal history.

The receipt binds the exact v0.13 materialization digest, source escalation and decision digests, owner, epoch, all state digests, the complete lease-scope inventory, current cycle, next cycle, mission-cycle state, and activation authority receipt.

The handoff is active only from `current_cycle + 1` and targets the PLAN phase. It does not grant execution, host access, automatic renewal, memory overwrite, truth authority, or professional authority.

Persistence is single-activation, append-only, digest-bound, replay-idempotent, fsync-backed, atomically snapshotted, and recoverable from the ledger.
