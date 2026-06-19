# KuuOS PlanOS Suspension Recovery Router v0.17

PlanOS v0.17 consumes a terminal v0.16 suspension and produces exactly one canonical recovery handoff.

```text
terminal v0.16 suspension
+ exact v0.15 session
+ exact v0.13 materialization
→ REVALIDATE
→ RENEW_OR_ESCALATE
→ REROTATE_REQUIRED
```

The old session is always closed. It is never resumed, even after successful recovery. Every route requires a new lineage, a new activation receipt, and a new control session.

`REVALIDATE` binds the exact observation digest and sends the anomaly to a revalidation intake.

`RENEW_OR_ESCALATE` rechecks the v0.11 renewal policy for each affected capability. Renewal remains a candidate only while count, added-use, added-cost, absolute-expiry, and cooldown constraints remain open. If every affected capability is eligible, the handoff targets v0.11 renewal review. If any affected capability is ineligible, the handoff targets v0.12 escalation.

`REROTATE_REQUIRED` targets the v0.12 re-rotation path. The router does not itself rotate capabilities.

The handoff binds the source session, terminal tick, materialization receipt, renewal state, lease state, owner, epoch, mission cycle, affected capabilities, complete reason inventory, and recovery authority receipt.

The router does not perform revalidation, renewal, escalation, re-rotation, activation, host invocation, execution, or memory overwrite.

Persistence is single-route, append-only, digest-bound, replay-idempotent, fsync-backed, atomically snapshotted, and recoverable from the ledger.
