# KuuOS PlanOS Bounded Renewal Governance v0.11

PlanOS v0.11 governs the explicit lease-renewal mechanism introduced in v0.10.

```text
v0.10 lease state
→ validate renewal authority identity
→ validate owner / epoch / scope again
→ enforce cooldown
→ enforce cumulative renewal ceilings
→ apply the v0.10 renewal
→ require escalation when any ceiling is reached
```

Each capability kind has fixed limits for renewal count, cumulative added uses, cumulative added cost, and an absolute expiry horizon. A renewal cannot move beyond those limits even when an external renewal receipt exists.

The authority identity is fixed per capability kind. Automatic renewal is forbidden. Exact replay is idempotent. After a ceiling is reached, the policy enters `ESCALATION_REQUIRED`; further continuation requires a new capability rotation, handover, or explicit higher-level intervention.

The governance receipt does not grant execution, host access, approval, truth authority, memory overwrite, or professional authority.

Persistence uses an append-only digest chain, exclusive locking, fsync, atomic snapshots, deterministic reconstruction, corruption detection, and ledger-derived repair.
