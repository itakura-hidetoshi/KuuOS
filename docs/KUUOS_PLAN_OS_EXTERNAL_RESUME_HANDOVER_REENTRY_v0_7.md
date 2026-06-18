# KuuOS PlanOS External Resume and Handover Re-entry v0.7

PlanOS v0.7 re-enters a PlanOS v0.6 supervisor only through an explicit external receipt.

A HOLD state can resume only under the same owner. A HANDOVER state requires delegation by the outgoing owner and acceptance by a distinct incoming owner. STOPPED states cannot re-enter.

The receipt binds the exact terminal-state digest, lineage, mission contract, policy, authority scope, evidence, issue time, expiry time, and single-use rule.

Re-entry preserves the terminal source and creates a separate ACTIVE v0.6 state. It authorizes the next PlanOS generation but grants no execution permission, host license, or memory overwrite.

Persistence uses an append-only digest ledger, exclusive lock, fsync, atomic snapshot, replay idempotence, corruption detection, and ledger-derived repair.
