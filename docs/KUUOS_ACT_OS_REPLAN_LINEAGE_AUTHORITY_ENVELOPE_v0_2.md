# KuuOS ActOS Replan-Lineage Authority Envelope v0.2

ActOS v0.2 preserves the complete Replan lineage when a next-cycle structured plan produced by PlanOS v0.3 crosses into ActOS v0.1.

```text
PlanOS v0.3 compiler receipt
  + committed PLAN_CANDIDATE plan
  + canonical Plan-phase activation receipt
  + exact Act-phase cycle
        ↓
ActOS v0.2 handoff receipt
        ↓
ActOS v0.1 select
        ↓
lineage-bound step authorization envelope
        ↓
ActOS v0.1 authorize / project / invoke / verify / commit
        ↓
ActOS v0.2 completion receipt
```

## 1. Purpose

PlanOS v0.3 preserves Replan, Qi, DecisionOS, selected-candidate, materialization, and next-plan-basis digests in its compiler receipt. ActOS v0.1 correctly enforces bounded invocation but stores only the compiled Plan and Wa provenance. ActOS v0.2 closes that lineage gap without replacing the v0.1 invocation kernel.

## 2. Ownership

- Plan selection and synthesis remain owned by PlanOS.
- Effectful step selection and bounded invocation remain owned by ActOS.
- Host execution remains bounded by the v0.17 host license and lower host receipt.
- Qi remains process context and never becomes execution authority.
- The envelope cannot widen Plan, Act, human-approval, host-license, tool, shell, or network authority.

## 3. Strict boundary

The handoff accepts only:

- a canonical PlanOS v0.3 compiler receipt;
- its exact committed `PLAN_CANDIDATE` PlanOS v0.1 state;
- the canonical Plan-phase activation receipt for that plan;
- one exact effectful `act_candidate` step from the committed plan;
- `mission_cycle_phase = act`;
- `mission_cycle_cycle_index = compiler_receipt.mission_cycle_cycle_index`;
- a nonempty operation ID and operation-input digest;
- preserved stop, observation, verification, rollback, and human-review boundaries.

It rejects stale cycles, non-Act phases, non-effectful steps, step substitution, plan substitution, compiler-receipt substitution, next-plan-basis substitution, Replan/Qi/Decision/materialization substitution, operation substitution, and authority widening.

## 4. Handoff receipt

The receipt binds:

```text
compiler receipt
compiled Plan state and basis
Plan-phase activation receipt
Replan phase receipt
next-plan activation receipt
materialization packet
next-plan basis
selected Replan candidate
Qi condition
DecisionOS receipt
synthesis packet
selected effectful Plan step
operation ID and input digest
Act-phase cycle and event
```

It declares:

```text
plan_activation_is_not_execution = true
act_phase_receipt_still_required = true
step_authorization_still_required = true
human_approval_still_required_when_declared = true
host_license_still_required = true
single_use = true
execution_granted = false
host_license_granted = false
```

## 5. Lineage-bound authorization envelope

After ActOS v0.1 selects the exact step and constructs its ordinary step authorization, v0.2 wraps that authorization without modifying it.

The envelope binds:

- the Act handoff receipt;
- the exact ActOS state at `select`;
- the inner v0.1 step authorization digest;
- the exact selected step and operation;
- the Act-phase receipt;
- the host license digest;
- human approval when required;
- the complete upstream Replan lineage.

The inner authorization remains canonical. The envelope cannot alter its operation, expiry, host job, host step, invocation ID, approval, or license.

## 6. Completion receipt

After ActOS v0.1 commits, the completion receipt binds:

```text
Act handoff receipt
lineage-bound authorization envelope
committed Act state
inner authorization
host projection
host tick and lower host receipt
host invocation digest
result supervisor bundle
route and effect_recorded
observation debt
verification debt
```

A successful effect must preserve both observation and verification debt. `BLOCKED` and `REPLAYED` outcomes remain explicit and cannot be promoted to successful effects.

## 7. Single-use persistence

```text
act-lineage-genesis.json
act-lineage-ledger.jsonl
act-lineage-snapshot.json
.act-os-v02-lineage.lock
```

The store records two append-only stages:

```text
HANDOFF_ISSUED
COMPLETION_COMMITTED
```

The same PlanOS v0.3 compiler receipt and selected step may issue at most one distinct handoff. Exact replay is idempotent. A conflicting step, operation, plan, or invocation is rejected. A completion requires a previously issued handoff and may be committed once.

## 8. Two Truths and Middle Way

Conventionally, the receipt makes one Plan step eligible for bounded ActOS authorization. Ultimately, neither the plan, the Replan lineage, the Qi condition, nor the handoff is self-existing execution authority.

The Middle Way avoids both:

- treating Plan activation as immediate execution; and
- losing the causal and governance lineage when bounded execution becomes possible.

## 9. Public boundary

ActOS v0.2 is an authority-preserving lineage envelope. It is not autonomous authority, clinical authorization, legal authorization, host permission, proof of safety, or proof of real-world effectiveness.
