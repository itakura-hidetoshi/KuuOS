# KuuOS Transactional Effect Reconciliation Kernel v0.24

## Purpose

v0.24 completes the first part of Plane D in the autonomous-agent architecture:

```text
bounded plan proposal
→ exact ActOS step authorization
→ prepare transaction intent
→ licensed lower host invocation
→ canonical ActOS effect receipt
→ independent ObserveOS world evidence
→ world-effect reconciliation
→ independent VerifyOS adjudication
→ commit / reobserve / compensate-proposal / handover
```

The release does not create a new connector executor. It wraps the existing ActOS and cooperative host adapter authority surfaces with a common transactional protocol and a separate world-state reconciliation record.

## Why the additional layer is necessary

A lower tool or host receipt can establish that a licensed invocation ran and emitted a bounded effect record. It cannot by itself establish that the external world reached the intended state.

```text
host invocation success
!= intended world state confirmed
!= mission success
!= truth authority
```

v0.24 therefore binds three different identities without collapsing them:

1. intended effect
2. lower execution receipt
3. independently observed world state

## Transaction protocol

```text
prepared
→ effect_bound
→ observed
→ reconciled
→ verified
→ decided
→ committed
```

When the lower ActOS invocation is blocked before an effect is recorded, the route is shortened:

```text
prepared
→ effect_bound
→ decided
→ committed
```

No observation or verification record is fabricated for an effect that was not recorded.

## Connector contract

The connector contract is a read-only capability description. It contains:

- connector identity and trusted registry binding
- operation allowlist
- observation channels
- explicit compensation mode
- compensation operation allowlist when applicable
- idempotency and exact-receipt capabilities

It performs no connector call and grants no execution authority.

Supported compensation modes:

```text
explicit_operation
manual_handover
noncompensable
```

`manual_handover` and `noncompensable` require an explicit non-compensability reason digest.

## Prepare boundary

A transaction intent can be prepared only from an ActOS state in the `project` phase. It binds:

- exact plan and selected step
- exact operation and input digest
- exact step authorization
- exact host capability lease
- exact host projection
- intended effect digest
- expected observation digest
- verification criterion digest
- lower invocation ID as the idempotency key
- timeout and bounded retry policy
- compensation operation or explicit non-compensability

Preparation precedes the effect and performs no hidden connector call.

## Effect binding

The `effect_bound` phase accepts only the committed ActOS state descended from the prepared state.

It verifies:

- plan, step, operation, and input identity
- authorization and capability-lease identity
- projection and source supervisor bundle identity
- canonical lower host receipt
- exact lower invocation identity

A lower replay receipt cannot create a new transaction. It must be resolved through the existing transaction receipt associated with that idempotency key.

## Independent world observation

ObserveOS remains the owner of effect-grounded evidence collection.

The transaction accepts only a committed ObserveOS state bound to the same:

- ActOS state
- host receipt
- host invocation
- expected observation target
- verification criterion

Observation remains distinct from verification.

## World-effect reconciliation

The reconciliation receipt compares the intended effect against independently observed external state.

Possible verdicts:

```text
EFFECT_CONFIRMED
EFFECT_PARTIAL
EFFECT_NOT_OBSERVED
EFFECT_CONFLICTED
EXTERNAL_STATE_CHANGED
COMPENSATION_REQUIRED
```

A confirmed effect requires:

- an ObserveOS `OBSERVATION_MATCHED` route
- at least two independent world sources
- immutable evidence digests
- exact equality between intended and observed effect digests

The reconciliation layer grants neither truth nor causal authority.

## VerifyOS binding

VerifyOS independently adjudicates the observation evidence. The final transaction route depends on both reconciliation and verification:

```text
EFFECT_CONFIRMED + VERIFICATION_PASSED
→ EFFECT_CONFIRMED

open observation debt or VERIFICATION_INDETERMINATE
→ REOBSERVATION_REQUIRED

failure/conflict + explicit compensation operation
→ COMPENSATION_PROPOSED

failure/conflict + no executable compensation
→ HANDOVER_REQUIRED

lower ActOS recorded no effect
→ NO_EFFECT_RECORDED
```

## Compensation boundary

Compensation is never executed inside the failed transaction.

A compensation request is proposal-only and requires:

```text
new PlanOS synthesis
→ new DecisionOS selection
→ new ActOS authorization
→ new capability lease
→ new idempotency key
→ separately observable and verifiable transaction
```

This prevents rollback from becoming an implicit or self-authorized world rewrite.

## Commit semantics

The final receipt preserves all lower receipts as canonical evidence and appends a new transaction-level interpretation.

It does not overwrite:

- ActOS execution history
- ObserveOS evidence
- VerifyOS adjudication
- MemoryOS roots
- world-state history

The commit grants no execution, final commitment, truth, wake-up, or world-rewrite authority.

## Persistence

The companion store uses:

```text
transaction-initial.json
transaction-ledger.jsonl
transaction-snapshot.json
```

The ledger is the recovery source of truth. Duplicate events are replayed without a second append. Stale events are rejected. Snapshot disagreement fails closed and can be repaired only by explicit replay from the ledger.

## Formal boundary

The Lean module composes existing lower theorems from:

- `ActOS.AuthorityBoundInvocationV0_1`
- `ObserveOS.EffectGroundedObservationV0_1`
- `VerifyOS.EvidenceBoundVerificationV0_1`
- `OpenHorizon.NonMarkovCognitiveLoopKernelV0_23`

The final theorem is:

```lean
transactional_effect_reconciliation_boundary
```

It jointly establishes:

- exact lower capability binding
- post-effect observation and verification debt
- observation is not verification
- verification is not truth or causal authority
- prepare performs no hidden connector call
- compensation requires a new authorized transaction
- automatic compensation and rollback remain forbidden
- append-only commit preserves lower receipts
- commit grants no execution, final, world-rewrite, or wake-up authority

## Validation

```bash
PYTHONPATH=. python scripts/check_transactional_effect_reconciliation_v0_24.py
PYTHONPATH=. python -m unittest -v tests.test_transactional_effect_reconciliation_v0_24
PYTHONPATH=. python scripts/check_act_os_authority_bound_invocation_v0_1.py
PYTHONPATH=. python scripts/check_observe_os_effect_grounded_observation_v0_1.py
PYTHONPATH=. python scripts/check_verify_os_evidence_bound_verification_v0_1.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.TransactionalEffectReconciliationKernelV0_24
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
