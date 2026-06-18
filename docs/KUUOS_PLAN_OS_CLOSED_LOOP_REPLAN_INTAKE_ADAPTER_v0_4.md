# KuuOS PlanOS Closed-Loop Replan Intake Adapter v0.4

PlanOS v0.4 closes the first full generational control loop by consuming a committed LearnOS v0.2 result and constructing a pristine PlanOS v0.2 `BIND` state.

```text
PlanOS v0.3 compiled plan
→ ActOS v0.2
→ ObserveOS v0.2
→ VerifyOS v0.2
→ LearnOS v0.2
→ PlanOS v0.4 intake
→ PlanOS v0.2 BIND
→ HISTORY
```

## Required sources

The adapter requires all of the following at once:

- the currently committed PlanOS v0.1 plan;
- its canonical PlanOS v0.3 compiler receipt;
- the committed LearnOS v0.1 state;
- the LearnOS v0.2 handoff receipt;
- the LearnOS v0.2 completion receipt;
- the exact current mission-cycle index.

The compiler receipt must identify the exact current plan state, plan basis, route, lineage, and mission contract. The LearnOS completion must identify the exact committed learning state, learning delta, middle-way report, verification evidence, counterevidence, Qi lineage, DecisionOS lineage, and upstream Act/Observe/Verify completion receipts.

## Exact cycle rule

```text
intake cycle
  = compiler receipt cycle
  = LearnOS handoff cycle
```

The bound replan state is future-only:

```text
current_cycle_index = n
active_from_cycle   = n + 1
```

Early, late, stale, or cross-cycle intake is rejected.

## BIND-only materialization

PlanOS v0.4 delegates replan construction to the existing PlanOS v0.2 kernel. It creates only the initial pristine state:

```text
current_phase = bind
event_index   = 0
next_phase    = history
```

It does not generate candidates, select candidates, synthesize a plan, activate a plan, or execute an action.

## Preserved lineage

The intake receipt preserves:

- current compiled plan identity;
- PlanOS v0.3 compiler receipt;
- previous replan phase receipt;
- Qi condition packet;
- DecisionOS receipt;
- selected candidate;
- ActOS v0.2 completion;
- ObserveOS v0.2 completion;
- VerifyOS v0.2 completion;
- LearnOS v0.2 handoff and completion;
- committed Act, Observe, Verify, and Learn states;
- learning delta and middle-way report;
- verification evidence and counterevidence;
- `planos_replan_input_digest`.

## Authority boundary

```text
intake commit ≠ replan activation
BIND commit   ≠ plan activation
BIND commit   ≠ execution permission
BIND commit   ≠ host license
```

Ownership remains:

```text
replan            = PlanOS
candidate selection = DecisionOS
execution         = ActOS
```

Current-cycle state, past plans, and memory remain unchanged.

## Durable store

```text
closed-loop-intake-genesis.json
closed-loop-intake-ledger.jsonl
closed-loop-intake-snapshot.json
.plan-os-v04-intake.lock
```

The store provides append-only digest chaining, exclusive writer locking, fsync, atomic snapshots, exact replay idempotence, conflicting intake rejection, single-use binding, restart reconstruction, snapshot corruption detection, and ledger-derived repair.

## Formal surface

Lean proves:

- current-plan and learning-state identity preservation;
- exact compiler/Learn/intake cycle equality;
- next-cycle successor relation;
- complete runtime lineage preservation;
- pristine `BIND` entry with `event_index = 0`;
- future-only and non-mutating semantics;
- PlanOS/DecisionOS/ActOS ownership separation;
- BIND is neither activation nor execution;
- single-use binding;
- recovery count equality.
