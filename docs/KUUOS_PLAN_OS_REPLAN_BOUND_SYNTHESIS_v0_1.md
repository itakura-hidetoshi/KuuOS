# KuuOS PlanOS Replan-Bound Structured Plan Synthesis v0.1

PlanOS v0.1 converts an activated DecisionOS Wa v0.3 basis into an auditable, dependency-ordered plan candidate. It does not execute steps, grant a host license, or reinterpret the upstream decision.

```text
v0.20 Mission Contract
  + BeliefOS v0.3
  + DecisionOS v0.1 relational deliberation
  + DecisionOS v0.2 plural harmony / veto / appeal
  + DecisionOS v0.3 Wa relational harmony
  + v0.21 Replan activation receipt
        ↓
PlanOS v0.1 structured plan synthesis
        ↓
PLAN_CANDIDATE / OBSERVATION_PLAN / REPAIR_PLAN / HANDOVER_PLAN
/ HOLD / REJECT / QUARANTINE
        ↓
Plan-phase activation receipt
        ↓
licensed Act boundary
```

## 1. Role boundary

PlanOS proposes structure. It does not:

- choose a different decision option;
- erase stakeholder-local values, vetoes, appeals, or Wa findings;
- execute a step;
- grant tool, shell, network, clinical, institutional, legal, or host authority;
- overwrite MemoryOS;
- treat successful validation as proof of real-world success.

```text
belief != decision
decision != plan
plan != execution
plan validation != effect receipt
```

## 2. Source binding

Genesis binds exact digests for:

```text
committed Wa state
committed Wa receipt
Wa basis
source plural decision basis
mission contract
mission-cycle Replan state
Replan receipt
next-plan basis
source Wa route
endorsed / review option identities
```

A plan may only elaborate the upstream route. It cannot silently replace the selected option or change the stakeholder field.

## 3. Route-to-plan mapping

```text
Wa ENDORSE   -> PLAN_CANDIDATE
Wa REOBSERVE -> OBSERVATION_PLAN
Wa REPAIR    -> REPAIR_PLAN
Wa ESCALATE  -> HANDOVER_PLAN
Wa HOLD      -> HOLD
Wa REJECT    -> REJECT
Wa QUARANTINE-> QUARANTINE
```

The route mapping is deterministic and non-escalatory. In particular, `ENDORSE` does not mean execution authorization.

## 4. Strict synthesis phases

```text
BIND
  ↓
DECOMPOSE
  ↓
ORDER
  ↓
RESOURCE
  ↓
GUARD
  ↓
CHECKPOINT
  ↓
VERIFY
  ↓
COMMIT
```

Phase skipping, stale state, event-index regression, time regression, source digest mismatch, duplicate step IDs, missing dependencies, cyclic dependencies, and authority escalation are rejected.

## 5. Plan step model

Each step declares:

```text
step_id
step_digest
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
stop_condition_digests
requires_external_license
requires_human_review
effectful
source_option_id
stakeholder_scope_digests
```

Initial step classes:

```text
observe
prepare
act_candidate
verify
repair
handover
hold
```

`act_candidate` remains only a proposed action step. It is not a live invocation.

## 6. Dependency order

Every dependency must exist and have strictly lower rank:

```text
for each dependency d of step s:
  rank(d) < rank(s)
```

This rank certificate implies:

- no self-dependency;
- no two-step cycle;
- no directed cycle;
- deterministic topological ordering after tie-breaking by step ID.

The plan stores the complete dependency graph and its topological order.

## 7. Resource boundary

For plan steps `s_i`:

```text
total_cost = Σ estimated_cost(s_i)
peak_step_risk = max estimated_risk(s_i)
```

Plan synthesis requires:

```text
total_cost <= plan_budget
peak_step_risk <= maximum_step_risk
```

Resource validation does not grant resources. It only checks declared bounds.

## 8. Reversibility and license guards

Every effectful step must satisfy one of:

```text
reversible with explicit rollback step
or
requires_human_review = true
and requires_external_license = true
and irreversible-risk escalation is visible
```

Every effectful step must also declare:

- at least one stop condition;
- an expected observation;
- a verification criterion;
- a later observation or verification checkpoint.

No step may claim authority merely because it appears in an endorsed plan.

## 9. Checkpoints

PlanOS inserts or verifies explicit checkpoints for:

```text
precondition review
post-step observation
verification
rollback / repair readiness
stakeholder and Wa continuity
```

An effectful step without a later checkpoint is rejected. Observation debt cannot be hidden inside a successful plan status.

## 10. Plan routes

### PLAN_CANDIDATE

The exact Wa-endorsed option has a valid, bounded, guarded, checkpointed DAG.

### OBSERVATION_PLAN

The upstream route is `REOBSERVE`; steps must be observation, preparation, verification, or hold only.

### REPAIR_PLAN

The upstream route is `REPAIR`; the plan is limited to repair, observation, verification, preparation, or hold.

### HANDOVER_PLAN

The upstream route is `ESCALATE`; the plan may prepare and hand over but cannot contain an effectful local action.

### HOLD / REJECT / QUARANTINE

No active plan candidate is produced.

## 11. Commit semantics

Commit requires:

```text
future_only = true
memory_overwrite = false
plan_not_execution = true
plan_not_host_license = true
source_identity_preserved = true
activation_boundary = mission_plan_phase_only
```

## 12. Persistent store

```text
plan-genesis.json
plan-ledger.jsonl
plan-snapshot.json
.plan-os.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, replay idempotence, restart recovery, and explicit snapshot repair from verified ledger history.

## 13. Plan-phase activation

A committed plan is activatable only when:

```text
mission_cycle_phase = plan
Replan activation receipt digest is present
next-plan basis digest matches genesis
plan route is active
future_only = true
memory_overwrite = false
plan_not_execution = true
host_license_granted = false
```

This activation exposes a plan to the Plan phase. It still does not authorize Act.

## 14. Formal surface

The Lean surface proves:

- strict phase progression and event-index growth;
- dependency rank strictly decreases along every dependency;
- self-dependency and two-cycle are impossible;
- total cost and peak risk remain within declared bounds;
- effectful steps require rollback or explicit human/external-license escalation;
- active routes preserve source option identity;
- observation, repair, and handover routes cannot masquerade as effectful endorsed plans;
- commit is future-only, non-overwriting, and non-executing;
- Plan-phase activation grants no host license or execution authority;
- append-only recovery count matches committed plan count.

## 15. Public boundary

PlanOS v0.1 is a structural planning kernel. It is not medical advice, treatment authorization, legal approval, institutional authority, proof authority, or unrestricted autonomous execution authority.
