# KuuOS PlanOS Bounded Multi-Generation Supervisor v0.6

PlanOS v0.6 supervises repeated PlanOS v0.5 generation receipts without permitting an unbounded automatic loop.

```text
v0.5 generation receipt
→ validate lineage and mission
→ validate exact successor cycle
→ validate previous-generation digest
→ evaluate bounded stop policy
→ CONTINUE | HOLD | STOPPED | HANDOVER
```

## Policy

The policy fixes:

- maximum generation count;
- convergence threshold;
- stagnation limit;
- oscillation limit;
- observation-debt limit;
- recovery-protection threshold.

## Decision priority

```text
handover request
→ boundary handover
→ mission complete
→ maximum generations
→ convergence
→ stagnation
→ oscillation
→ observation-debt hold
→ recovery hold
→ continue
```

The first satisfied condition wins. This makes the decision deterministic and replayable.

## Chaining

For generation `k + 1`, the supervisor requires:

```text
generation_index = completed_generations + 1
source_cycle      = current_cycle
next_cycle        = current_cycle + 1
previous_report   = last_generation_report_digest
```

Lineage ID and mission-contract digest must remain unchanged.

## Terminal behavior

`HOLD`, `STOPPED`, and `HANDOVER` all set:

```text
next_generation_authorized = false
automatic_continuation      = false
```

No later generation report can be admitted by the same terminal supervisor state.

## Boundaries

The supervisor does not execute actions and does not grant a host license. Execution remains owned by ActOS. Replanning remains owned by PlanOS. Candidate selection remains owned by DecisionOS.

## Persistence

```text
multi-generation-genesis.json
multi-generation-ledger.jsonl
multi-generation-snapshot.json
.plan-os-v06-supervisor.lock
```

The store provides append-only digest chaining, replay idempotence, exclusive writer locking, fsync, atomic snapshots, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## Runtime validation

The validation route covers:

- one continuing generation;
- convergence at the second generation;
- rejection of a third generation after stop;
- maximum-count stop;
- stagnation stop;
- oscillation stop;
- observation-debt hold;
- recovery hold;
- mission-complete stop;
- two handover routes;
- broken digest-chain rejection;
- replay non-duplication;
- snapshot corruption and repair.
