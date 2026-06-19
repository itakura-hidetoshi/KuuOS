# KuuOS PlanOS Scoped Capability Lease v0.10

PlanOS v0.10 consumes the new-epoch capability bindings produced by v0.9 through explicit leases.

Each lease binds the current owner and epoch together with an allowed mission stage, operation allowlist, exact scope digest, use budget, cost budget, activation time, and expiry time.

```text
v0.9 BOUND capability state
→ create four scoped leases
→ validate owner / epoch / stage / operation / scope / time
→ consume one use and cost units
→ EXHAUSTED or EXPIRED when the lease can no longer be used
```

Consumption receipts are single-use and append-only. Exact replay is idempotent. A lease cannot increase its own budget.

Renewal requires a separate external renewal receipt and revalidates the same current owner, current epoch, and scope. Automatic renewal is forbidden.

The lease wrapper records eligibility and consumption only. It does not grant execution, host access, approval, truth authority, memory overwrite, or any professional authority.

Persistence uses a digest-chained ledger, exclusive writer lock, fsync, atomic snapshots, deterministic reconstruction, corruption detection, and ledger-derived repair.
