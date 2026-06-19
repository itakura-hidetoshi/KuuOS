# KuuOS PlanOS Renewal Escalation and Re-Rotation v0.12

PlanOS v0.12 resolves a v0.11 renewal ceiling through exactly one explicit route.

```text
ESCALATION_REQUIRED
├─ DENY
├─ HUMAN_HANDOVER
└─ RE_ROTATE
```

`DENY` closes the old lease lineage and grants no continuation.

`HUMAN_HANDOVER` requires a distinct target owner and a human acceptance receipt. It does not automatically start a new capability chain.

`RE_ROTATE` keeps the current owner, closes the old lease lineage, increments the capability epoch strictly, and emits a seed digest for a new v0.9 capability-rotation chain. It does not itself issue a capability or grant execution.

Every route binds the exact v0.11 state, current owner, current epoch, capability kind, governance authority, and governance receipt. Resolution is single-use and append-only.

Persistence uses a digest-chained ledger, exclusive locking, fsync, atomic snapshots, deterministic recovery, replay idempotence, corruption detection, and ledger-derived repair.
