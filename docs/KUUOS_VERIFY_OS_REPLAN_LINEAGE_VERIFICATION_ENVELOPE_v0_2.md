# KuuOS VerifyOS Replan-Lineage Verification Envelope v0.2

VerifyOS v0.2 preserves the complete PlanOS, ActOS, and ObserveOS lineage when a committed observation enters the existing VerifyOS v0.1 evidence-bound verification kernel.

```text
ObserveOS v0.2 handoff and completion receipts
  + committed ObserveOS v0.1 observation
  + exact Verify phase and cycle
        ↓
VerifyOS v0.2 lineage handoff
        ↓
VerifyOS v0.1
BIND → CRITERION → CHALLENGE
→ CORROBORATE → ADJUDICATE → COMMIT
        ↓
VerifyOS v0.2 lineage completion receipt
```

## Strict source boundary

The adapter accepts only:

- a committed ObserveOS v0.1 state with a non-pending route;
- `observation_recorded = true`;
- `verification_required = true`;
- canonical ObserveOS v0.2 handoff and completion receipts;
- exact equality of Observe state, Act state, evidence, quality, comparison, and criterion digests;
- `mission_cycle_phase = verify`;
- the same cycle used by the upstream Observe handoff.

Substituted Qi, DecisionOS, candidate, step, criterion, evidence, observation, or cycle identity is rejected.

## Preserved lineage

The envelope retains:

- PlanOS v0.3 compiler receipt;
- PlanOS v0.2 replan receipt;
- Qi condition packet;
- DecisionOS receipt;
- selected candidate and structured-plan step;
- ActOS v0.2 completion;
- ObserveOS v0.2 handoff and completion;
- committed Act and Observe states;
- host effect receipts;
- observation evidence, quality, comparison, and verification criterion.

Qi remains process context. It is not truth, verification, or causal authority.

## VerifyOS v0.1 reuse

No second verification kernel is introduced. VerifyOS v0.1 remains the sole verifier and retains the established sequence:

```text
BIND
→ CRITERION
→ CHALLENGE
→ CORROBORATE
→ ADJUDICATE
→ COMMIT
```

The lineage envelope requires explicit falsification attempts, preservation of counterevidence, independent assessment, corroboration, and criterion-bound adjudication.

## Verdict semantics

```text
PASSED
  verification debt discharged
  no corrective action
  learning required

FAILED
  verification debt discharged
  corrective action required
  learning required

INDETERMINATE
  verification debt remains open
  reobservation required
  learning required
```

Every verdict is a bounded verification result, not absolute truth or causal proof.

## Future-only LearnOS boundary

Every completion receipt states:

```text
learning_required = true
learning_must_be_future_only = true
automatic_learning = false
```

VerifyOS may produce evidence for LearnOS, but it cannot mutate existing belief, plan, action, observation, or verification records.

## Durable single-use persistence

The lineage store uses:

```text
verify-lineage-genesis.json
verify-lineage-ledger.jsonl
verify-lineage-snapshot.json
.verify-os-v02-lineage.lock
```

It provides writer locking, append-only digest chaining, fsync, atomic snapshots, replay idempotence, single-use handoff and completion, corruption detection, ledger reconstruction, and snapshot repair.

## Formal surface

The Lean surface proves:

- exact Verify phase and cycle gating;
- full upstream lineage preservation;
- criterion and evidence identity preservation;
- falsification, counterevidence, and independent-assessment preservation;
- route-specific verification debt semantics;
- verification is not absolute truth;
- Qi non-authority;
- future-only learning;
- single-use completion;
- recovery equality;
- no new truth, causal, execution, overwrite, or automatic-learning authority.

## Public boundary

VerifyOS v0.2 is a lineage-preserving verification adapter. It is not clinical authorization, legal authorization, theorem certification, autonomous rollback, automatic learning, or final truth authority.
