# KuuOS PlanOS Next-Cycle Basis Compiler Adapter v0.3

PlanOS v0.3 closes the cycle boundary between the future-only basis produced by PlanOS v0.2 and the structured plan compiler already implemented by PlanOS v0.1.

```text
PlanOS v0.2 committed Replan
  + canonical Replan phase receipt
  + exact next-cycle index
  + Mission Cycle Plan-phase receipt
  + selected-candidate materialization packet
        ↓
PlanOS v0.3 adapter
        ↓
legacy-compatible PlanOS v0.1 activation receipt
        ↓
PlanOS v0.1 structured compiler
        ↓
committed next-cycle structured plan
```

## 1. Purpose

PlanOS v0.2 commits a candidate basis but deliberately leaves it inactive. PlanOS v0.3 is the only adapter that may present that basis to the v0.1 structured compiler during the exact next Plan phase.

It does not execute the plan, mutate the previous plan, or treat the selected basis as uniquely true.

## 2. Strict boundary

The adapter accepts only:

- a committed current PlanOS v0.1 plan;
- the exact source DecisionOS Wa state used by that plan, retained solely as authorization provenance;
- a committed PlanOS v0.2 Replan state whose source plan digest equals the current plan digest;
- a canonical PlanOS v0.2 Replan phase receipt;
- `mission_cycle_phase = plan`;
- `mission_cycle_cycle_index = active_from_cycle`;
- a materialization packet whose template digests exactly match the v0.2 synthesis packet;
- a final v0.1 plan whose basis is bound to the same next-plan basis digest.

## 3. Dual lineage

PlanOS v0.3 preserves two lineages without collapsing them:

```text
Wa lineage
  = authorization and governance provenance required by v0.1

Replan lineage
  = selected next-cycle candidate, Qi condition, LearnOS delta,
    DecisionOS receipt, synthesis packet, and next-plan basis
```

The legacy Wa option identifier is not treated as the newly selected plan identity. The selected Replan candidate remains explicit in the v0.3 activation and compiler receipts.

## 4. Cycle gate

Activation is accepted only when:

```text
mission_cycle_phase = plan
mission_cycle_cycle_index = replan.active_from_cycle
replan.active_from_cycle = replan.current_cycle_index + 1
```

The following are rejected:

- activation in the Replan phase;
- activation in the old cycle;
- activation after the declared next cycle;
- a stale Mission Cycle state digest;
- a substituted Replan receipt;
- a substituted next-plan basis;
- a mismatched current-plan digest.

## 5. Template materialization

PlanOS v0.2 stores abstract step-template digests. PlanOS v0.3 requires an explicit materialization packet:

```text
template_digest
step_id
step_class
rank
depends_on
precondition_digests
expected_observation_digest
verification_criterion_digest
estimated_cost
estimated_risk
reversibility
rollback_step_id
rollback_point_digest
stop_condition_digests
requires_external_license
requires_human_review
effectful
stakeholder_scope_digests
```

For active routes, template digests must match exactly in count, order, and identity. Observation, verification, stop, and rollback digests required by the v0.2 synthesis packet must be covered by the structured steps.

For `HOLD`, no executable step is created. Template digests remain visible as withheld, non-executable material.

## 6. Route projection

```text
NEXT_PLAN_CANDIDATE          → PLAN_CANDIDATE
REPAIR_PLAN_CANDIDATE        → REPAIR_PLAN
REOBSERVATION_PLAN_CANDIDATE → OBSERVATION_PLAN
REROUTE_PLAN_CANDIDATE       → HANDOVER_PLAN
TERMINATION_PLAN_CANDIDATE   → HANDOVER_PLAN
HOLD                         → HOLD
```

Termination remains a planning or handover candidate and never becomes direct termination authority.

## 7. Compiler reuse

The adapter does not introduce a second plan compiler. It constructs a canonical legacy-compatible activation receipt and then invokes the existing v0.1 phases:

```text
BIND
→ DECOMPOSE
→ ORDER
→ RESOURCE
→ GUARD
→ CHECKPOINT
→ VERIFY
→ COMMIT
```

Thus dependency validation, resource bounds, effect guards, rollback or escalation requirements, observation checkpoints, verification checkpoints, append-only persistence, and Plan-phase activation semantics remain those of PlanOS v0.1.

## 8. Single-use activation

A durable adapter ledger records each consumed:

```text
replan_phase_receipt_digest
next_plan_activation_receipt_digest
next_plan_basis_digest
compiled_plan_state_digest
compiled_plan_basis_digest
```

The same Replan receipt or next-plan basis cannot activate two different plans. Exact receipt replay is idempotent; conflicting replay is rejected.

## 9. Non-authority

```text
next-plan activation ≠ execution
compiled plan ≠ host license
compiled plan ≠ truth
compiled plan ≠ clinical authority
compiled plan ≠ legal authority
compiled plan ≠ memory overwrite
```

The previous plan and source records remain immutable.

## 10. Persistence

```text
next-cycle-adapter-genesis.json
next-cycle-adapter-ledger.jsonl
next-cycle-adapter-snapshot.json
.plan-os-v03-adapter.lock
```

The ledger is authoritative and append-only. The snapshot is derived and repairable. Writer locking, digest chains, fsync, atomic replacement, replay idempotence, restart reconstruction, corruption detection, and ledger-derived repair are required.

## 11. Formal surface

The Lean surface proves:

- the adapter activates only in the exact next Plan cycle;
- Replan receipt and next-plan basis identity are preserved;
- abstract templates are materialized without substitution;
- Wa authorization lineage and Replan plan identity remain distinct;
- v0.1 remains the sole structured compiler;
- activation is single-use;
- compilation does not execute or grant authority;
- the previous plan remains unchanged;
- recovered activation count equals committed adapter records.

## 12. Public boundary

PlanOS v0.3 is a compiler adapter and governance boundary. It is not an autonomous executor, clinical planner, legal decision maker, safety certification engine, or host authorization service.
