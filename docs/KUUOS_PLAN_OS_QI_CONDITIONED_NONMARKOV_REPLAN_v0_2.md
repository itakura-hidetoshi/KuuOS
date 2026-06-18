# KuuOS PlanOS Qi-Conditioned Non-Markov Replan v0.2

PlanOS v0.2 owns the Replan synthesis phase. It converts a committed current PlanOS v0.1 plan and a committed LearnOS future-only delta into a bounded next-cycle plan basis candidate. Replan is conditioned by non-Markov history and the Qi process tensor, deliberated through a DecisionOS-bound selection receipt, and remains inactive until the next Plan phase.

```text
current committed PlanOS v0.1
  + committed LearnOS delta
  + action / observation / verification / learning history
  + Qi process tensor and hysteresis
  + mission / resource / authority constraints
        ↓
PlanOS v0.2 Replan
        ↓
plan candidate set
        ↓
DecisionOS-bound deliberation receipt
        ↓
next-cycle plan basis candidate
        ↓
next Plan phase required before activation
```

## 1. Ownership and boundary

```text
Replan belongs to PlanOS
DecisionOS selects; PlanOS synthesizes
LearnOS delta != plan activation
Qi conditions Replan but grants no authority
Replan commit != execution
Replan commit != current-cycle mutation
```

PlanOS v0.2 is additive to PlanOS v0.1. v0.1 remains the structured plan compiler and Plan-phase activation boundary. v0.2 prepares the next-cycle basis that v0.1 may compile during the next Plan phase.

## 2. Strict phases

```text
BIND
  ↓
HISTORY
  ↓
QI_CONDITION
  ↓
GENERATE
  ↓
CONSTRAIN
  ↓
DELIBERATE
  ↓
SYNTHESIZE
  ↓
COMMIT_NEXT
```

Phase skipping, stale-state application, source-plan substitution, LearnOS-delta substitution, Qi-history substitution, unsupported candidate types, constraint bypass, hysteresis bypass, DecisionOS-selection substitution, current-cycle activation, and authority escalation are rejected.

## 3. Source binding

BIND accepts only:

- a committed PlanOS v0.1 state;
- a committed LearnOS state with `learning_recorded = true`;
- `future_only = true`;
- `active_now = false`;
- `replan_required = true`;
- canonical learning delta and Middle Way report;
- the same mission contract lineage.

It binds the exact current plan, LearnOS state, verification evidence, learning delta, Middle Way report, mission contract, and current cycle index.

## 4. Non-Markov history

HISTORY records a bounded but non-Markov summary:

```text
current_plan_digest
previous_plan_change_digests
successful_transition_digests
failed_transition_digests
oscillation_history_digests
recovery_history_digests
stagnation_history_digests
action_history_digest
observation_history_digest
verification_history_digest
learning_history_digest
history_window
path_dependence_digest
```

The present state is not treated as sufficient. The history packet preserves path dependence and cannot rewrite source records.

## 5. Qi process conditioning

QI_CONDITION records:

```text
process_tensor_digest
process_history_digest
activation
stagnation
tension
recovery
coherence
coupling
transition_readiness
local_global_balance
observation_debt
hysteresis
memory_horizon
intervention_history_digest
```

Qi is a conventional process-history context. It may condition timing, switch resistance, candidate priority, observation need, and transition expectations. It may not grant truth, causal, clinical, execution, or activation authority.

## 6. Candidate generation

GENERATE produces a finite candidate field. Allowed types are:

```text
continue
strengthen
repair
slow_down
reobserve
reroute
hold
terminate_candidate
```

Each candidate binds:

- the LearnOS delta;
- target scope;
- goal and step-template digests;
- expected observation and verification criterion digests;
- cost, risk, reversibility, transition distance, and switch benefit;
- stop and rollback conditions;
- stakeholder scope;
- `future_only = true` and `active_now = false`.

`terminate_candidate` and rollback-like changes remain candidates, never automatic actions.

## 7. Constraint and hysteresis gate

CONSTRAIN evaluates every candidate against:

- mission invariants;
- authority and safety boundaries;
- resource envelope;
- LearnOS applicability, reversal, and expiration conditions;
- observation and verification debt;
- scope compatibility;
- Qi transition readiness;
- hysteresis switch margin.

The switch rule is:

```text
required_switch_margin
  = base_switch_threshold
  + qi_hysteresis
  + oscillation_penalty
  + recovery_protection_penalty
```

A switching candidate must have `switch_benefit >= required_switch_margin`. This prevents repeated plan reversal during oscillation, recovery, or transient noise. `continue`, `hold`, and evidence-seeking `reobserve` may remain admissible without a switching benefit.

## 8. DecisionOS deliberation

DELIBERATE requires a canonical DecisionOS-bound receipt containing:

```text
decision_os_state_digest
decision_basis_digest
wa_relational_harmony_digest
selected_candidate_id
retained_candidate_ids
dissent_evidence_digests
minority_stakeholder_digests
all_candidates_considered = true
minority_preserved = true
decision_not_execution = true
```

The selected candidate must be admissible and must belong to the generated field. Retained alternatives remain visible. DecisionOS selects; PlanOS does not silently substitute the selection.

## 9. Synthesis

SYNTHESIZE converts the selected candidate into a next-cycle plan basis with:

```text
next_plan_goal_digest
next_plan_step_template_digests
next_observation_point_digests
next_verification_criterion_digests
next_stop_condition_digests
next_rollback_point_digests
resource_envelope_digest
authority_boundary_digest
active_from_cycle = current_cycle + 1
future_only = true
active_now = false
```

The synthesis packet preserves the selected candidate identity, DecisionOS receipt, Qi condition, non-Markov history, LearnOS lineage, and mission contract.

## 10. Commit-next semantics

COMMIT_NEXT records the next-cycle plan basis candidate only:

```text
next_plan_basis_committed = true
next_plan_phase_required = true
active_now = false
current_cycle_unchanged = true
past_plan_unchanged = true
memory_overwrite = false
host_license_granted = false
```

The next Plan phase remains responsible for compiling and activating a structured plan. ActOS remains responsible for any later licensed invocation.

## 11. Route semantics

```text
continue / strengthen / slow_down
  → NEXT_PLAN_CANDIDATE

repair
  → REPAIR_PLAN_CANDIDATE

reobserve
  → REOBSERVATION_PLAN_CANDIDATE

reroute
  → REROUTE_PLAN_CANDIDATE

hold
  → HOLD

terminate_candidate
  → TERMINATION_PLAN_CANDIDATE
```

No route grants execution or termination authority.

## 12. Two truths and Middle Way

Conventional truth: the selected basis is usable for the next Plan phase under declared conditions.

Ultimate boundary: it is not the unique true plan, not a self-existing policy, and not execution authority.

The Middle Way avoids:

- rigid persistence despite new evidence;
- overreaction to a single failure or transient fluctuation;
- oscillatory plan switching;
- nihilistic deletion of inconclusive evidence;
- reification of a passed verification into a universal rule.

## 13. Persistence

```text
replan-genesis.json
replan-ledger.jsonl
replan-snapshot.json
.plan-os-v02-replan.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, exact event replay idempotence, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## 14. Formal surface

The Lean surface proves:

- Replan belongs to PlanOS;
- strict phase progression and event-index growth;
- exact current-plan and LearnOS binding;
- history and Qi context preservation;
- Qi grants no authority;
- switching candidates require hysteresis margin;
- DecisionOS selects and PlanOS preserves that identity;
- synthesis applies only from the next cycle;
- Replan commit does not activate or execute;
- current cycle and past plan remain unchanged;
- append-only recovery count equals committed replan records.

## 15. Public boundary

PlanOS v0.2 is a future-cycle plan-synthesis and governance kernel. It is not an autonomous controller, clinical planning system, legal decision maker, safety certification engine, or execution authority.
