# KuuOS LearnOS Replan-Lineage Future-Only Learning Envelope v0.2

LearnOS v0.2 preserves the complete PlanOS, ActOS, ObserveOS, and VerifyOS lineage while delegating evidence-bound learning to LearnOS v0.1.

```text
VerifyOS v0.2 handoff and completion receipts
  + committed VerifyOS v0.1 verification
  + exact Learn phase and cycle
        ↓
LearnOS v0.2 lineage handoff
        ↓
LearnOS v0.1
BIND → ABSTRACT → CHALLENGE
→ DELTA → MIDDLE_WAY_GATE → COMMIT
        ↓
LearnOS v0.2 future-only completion receipt
        ↓
PlanOS v0.2 replan input candidate
```

## Strict source boundary

The handoff accepts only a committed verification with:

- `verification_recorded = true`;
- `learning_required = true`;
- canonical VerifyOS v0.2 handoff and completion receipts;
- exact verification state, evidence, criterion, challenge, corroboration, and adjudication identity;
- preserved counterevidence, falsification attempts, and independent assessment;
- `mission_cycle_phase = learn`;
- the exact upstream Verify cycle.

Substituted Qi, DecisionOS, selected candidate, selected step, verification evidence, criterion, phase, or cycle is rejected.

## Preserved lineage

The envelope retains:

- PlanOS v0.3 compiler receipt;
- PlanOS v0.2 replan receipt;
- Qi condition packet;
- DecisionOS receipt;
- selected candidate and structured-plan step;
- ActOS v0.2 completion;
- ObserveOS v0.2 completion;
- VerifyOS v0.2 handoff and completion;
- committed Act, Observe, Verify, and Learn states;
- verification evidence and criterion;
- counterevidence, challenge, corroboration, and adjudication;
- LearnOS abstraction, challenge, delta, and middle-way report.

## LearnOS v0.1 reuse

No second learning kernel is introduced. LearnOS v0.1 remains the sole learning compiler:

```text
BIND
→ ABSTRACT
→ CHALLENGE
→ DELTA
→ MIDDLE_WAY_GATE
→ COMMIT
```

The abstraction may summarize evidence but cannot replace its source. Anti-overgeneralization testing, alternative explanations, distribution-shift risk, observer-bias risk, negative-transfer risk, counterevidence, and two-truths separation remain visible.

## Future-only delta

Every committed delta preserves:

```text
future_only = true
active_now = false
current_cycle_unchanged = true
past_records_unchanged = true
memory_overwrite = false
activation_requires_planos_replan = true
```

Therefore:

```text
LearnOS delta
  ≠ replan activation
  ≠ plan activation
  ≠ execution permission
  ≠ host license
```

## PlanOS compatibility

The completion receipt constrains the candidate types PlanOS v0.2 may generate:

```text
REINFORCEMENT
  → continue / strengthen / slow_down / hold

REPAIR
  → repair / slow_down / reroute / hold

REOBSERVATION
  → reobserve / hold

LEARNING_HOLD
  → hold / reobserve
```

This is an allowlist for future deliberation, not a DecisionOS selection or an activated plan.

## Ownership

```text
learning delta creation = LearnOS
replan ownership        = PlanOS
candidate selection     = DecisionOS
plan synthesis          = PlanOS
execution               = ActOS
```

Qi remains process context and grants no truth, causal, learning-activation, replan, plan, or execution authority.

## Durable persistence

The lineage store uses:

```text
learn-lineage-genesis.json
learn-lineage-ledger.jsonl
learn-lineage-snapshot.json
.learn-os-v02-lineage.lock
```

It provides append-only digest chaining, exclusive writer locking, fsync, atomic snapshots, exact replay idempotence, conflicting handoff rejection, single-use completion, restart reconstruction, snapshot-corruption detection, and ledger-derived repair.

## Formal surface

The Lean surface proves:

- exact Learn phase and cycle gating;
- complete upstream lineage preservation;
- verification evidence and criterion identity;
- counterevidence, falsification, independent-assessment, and anti-overgeneralization preservation;
- middle-way and two-truths preservation;
- route-specific PlanOS candidate compatibility;
- strict future-only delta semantics;
- OS ownership separation;
- learning commit is not activation or execution;
- Qi non-authority;
- single-use completion;
- recovery equality;
- no new authority.

## Public boundary

LearnOS v0.2 produces a bounded, reversible, future-only learning candidate for PlanOS replan. It does not rewrite memory, update the current plan, activate a replan, select an action, execute an action, or grant a host license.
