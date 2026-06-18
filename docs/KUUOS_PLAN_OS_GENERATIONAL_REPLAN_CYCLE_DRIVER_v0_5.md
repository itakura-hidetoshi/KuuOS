# KuuOS PlanOS Generational Replan Cycle Driver v0.5

PlanOS v0.5 advances the pristine PlanOS v0.2 `BIND` state produced by v0.4 through the complete replan state machine, compiles the successor plan through PlanOS v0.3, and prepares an ActOS v0.2 handoff for the next cycle.

```text
PlanOS v0.4 BIND
→ HISTORY
→ QI_CONDITION
→ GENERATE
→ CONSTRAIN
→ DELIBERATE
→ SYNTHESIZE
→ COMMIT_NEXT
→ PlanOS v0.3 compiler
→ second-generation committed plan
→ ActOS v0.2 handoff
```

## Exact phase order

The driver accepts only the seven-event sequence:

```text
history
qi_condition
generate
constrain
deliberate
synthesize
commit_next
```

The committed replan state must have `event_index = 7`, one committed next-plan basis, and an append-only event history matching this order exactly.

## Exact successor cycle

```text
source_cycle_index = n
next_cycle_index   = n + 1
```

The next plan is compiled only in the exact successor Plan phase. Early activation, skipped cycles, or stale activation are rejected by the existing PlanOS v0.3 compiler boundary.

## Identity preservation

The generational receipt binds:

- v0.4 closed-loop BIND receipt;
- current committed plan;
- committed LearnOS state and learning delta;
- `planos_replan_input_digest`;
- non-Markov history packet;
- Qi condition packet;
- candidate and constraint fields;
- DecisionOS receipt and selected candidate;
- synthesis packet and next-plan basis;
- PlanOS v0.3 compiler receipt;
- second-generation committed plan;
- PlanOS activation receipt;
- ActOS v0.2 handoff.

Candidate identity is checked at the DecisionOS → committed replan → PlanOS v0.3 compiler → ActOS v0.2 handoff boundaries. The v0.2 phase receipt itself is not extended with a field it does not own.

## Authority boundary

```text
replan commit      ≠ execution
plan compilation   ≠ execution
ActOS handoff      ≠ invocation
ActOS handoff      ≠ host license
```

Ownership remains:

```text
replan             = PlanOS
candidate selection = DecisionOS
execution          = ActOS
```

The current cycle and past plan stay unchanged while the successor basis is synthesized.

## Monotone timing adapter

The validation entry point projects two compatibility details without altering semantic identity:

1. the successor PlanOS v0.1 state is initialized before its compiler events, preventing time regression;
2. the canonical `plan_activation_receipt_digest` is projected to the legacy adapter field expected by the generational receipt builder.

Both projections preserve the original digest value.

## Durable generation store

```text
generational-cycle-genesis.json
generational-cycle-ledger.jsonl
generational-cycle-snapshot.json
.plan-os-v05-generation.lock
```

The store provides append-only digest chaining, exclusive writer locking, fsync, atomic snapshots, exact replay idempotence, single consumption of a source generation, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## Formal surface

Lean proves:

- the seven-phase sequence has length seven;
- the next cycle is the exact successor;
- source-plan identity is preserved through BIND, replan, and compiler boundaries;
- DecisionOS-selected candidate identity reaches ActOS transitively;
- the next-plan basis is preserved by the compiler;
- ActOS handoff preserves compiler and plan identity;
- no execution, host license, or memory overwrite is granted;
- PlanOS, DecisionOS, and ActOS ownership remains separated;
- a source generation is consumed at most once;
- recovery preserves committed generation count.
