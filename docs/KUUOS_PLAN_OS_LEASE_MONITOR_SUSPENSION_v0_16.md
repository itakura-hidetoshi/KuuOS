# KuuOS PlanOS Lease Monitor Tick and Session Suspension v0.16

PlanOS v0.16 revalidates every capability lease while a v0.15 PLAN control session is active.

```text
active v0.15 session
→ complete four-lease observation
→ owner / epoch / scope / expiry / budget checks
→ healthy tick: PLAN progress may continue
→ anomalous tick: SESSION_SUSPENDED
```

Suspension reasons are explicit: expiry, empty use budget, empty cost budget, owner mismatch, epoch mismatch, scope mismatch, lease-window mismatch, budget increase, or observation-time mismatch.

Routes are classified without granting the route itself:

- expiry or budget exhaustion → `RENEW_OR_ESCALATE`
- observation or accounting inconsistency → `REVALIDATE`
- owner, epoch, or scope mismatch → `REROTATE_REQUIRED`

A healthy tick has no suspension reason and permits PLAN progress. Any anomaly immediately blocks PLAN progress and makes suspension terminal for that session. A suspended session accepts only exact replay of an already committed tick.

The monitor does not renew a lease, rotate a capability, invoke a host operation, grant execution, or overwrite memory.

Persistence uses an append-only digest chain, strictly increasing tick index and time, exclusive locking, fsync, atomic snapshots, deterministic recovery, and ledger-derived snapshot repair.
