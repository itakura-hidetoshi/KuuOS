# KuuOS Adaptive Agent Reference Architecture v1.0

## Purpose

This document freezes the upper architecture used to evolve KuuOS. New behavior is no longer admitted merely as the next sequential PlanOS version. Every implementation must refine an explicit plane, runtime model, event, transition, invariant, and recovery contract defined here.

## Research basis

The architecture combines five established ideas.

1. **MORPH** separates behavior adaptation from configuration adaptation while coordinating both through a reference architecture: <https://arxiv.org/abs/1504.08339>.
2. **Models and Megamodels at Runtime** treats runtime models and their relations as explicit managed objects rather than ad-hoc cross-links: <https://arxiv.org/abs/1805.07396>.
3. **ActivFORMS** makes the feedback-loop behavior itself a formally modeled and verified lifecycle artifact: <https://arxiv.org/abs/1908.11179>.
4. **Simplex runtime assurance** separates an advanced controller from a small assurance mechanism that can block or replace unsafe control: <https://arxiv.org/abs/2102.12981>.
5. KuuOS preserves its existing non-authority, future-only learning, observation/verification separation, bounded renewal, fresh-lineage recovery, and repairability constraints.

## Planes

```text
KuuOS Adaptive Agent
├─ Deliberation Plane
│  ├─ BeliefOS
│  ├─ DecisionOS
│  └─ PlanOS behavior planning
├─ Execution Plane
│  ├─ ActOS
│  ├─ ObserveOS
│  └─ VerifyOS
├─ Learning Plane
│  └─ LearnOS future-only updates
├─ Authority Plane
│  ├─ capability epoch
│  ├─ scoped lease
│  ├─ bounded renewal
│  ├─ escalation
│  └─ re-rotation
├─ Assurance Plane
│  ├─ runtime monitoring
│  ├─ anomaly classification
│  ├─ suspension
│  └─ safe halt
└─ Recovery Plane
   ├─ finite recovery algebra
   ├─ bounded routing
   ├─ human escalation
   ├─ abort
   └─ fresh-lineage bootstrap
```

Behavior adaptation and configuration/authority adaptation are separate planes. A planner may request authority but may not create it. An assurance monitor may suspend control but may not renew or rotate capabilities. A recovery router may select a recovery contract but may not execute the recovery itself.

## Runtime megamodel

The runtime megamodel contains twelve model kinds:

```text
MISSION
BELIEF
DECISION
PLAN
AUTHORITY
CAPABILITY_EPOCH
LEASE
SESSION
EVIDENCE
VERIFICATION
LEARNING
RECOVERY
```

Required relations are fixed:

```text
BELIEF supports DECISION
DECISION justifies PLAN
AUTHORITY constrains PLAN
CAPABILITY_EPOCH realizes AUTHORITY
LEASE scopes CAPABILITY_EPOCH
SESSION consumes LEASE
EVIDENCE observes SESSION
VERIFICATION evaluates EVIDENCE
LEARNING updates PLAN future-only
RECOVERY resolves SESSION suspension
RECOVERY requires a fresh CAPABILITY_EPOCH when re-rotation is selected
```

A digest is not sufficient merely because it exists. Its source and target models must be connected by one of these declared relations.

## Global state

The global adaptive-control state contains:

- task stage;
- control mode;
- authority mode;
- module status;
- owner and epoch;
- active and terminal session identities;
- plan, authority, evidence, and verification identities;
- observation and verification commitment flags;
- selected recovery decision;
- fresh-activation and fresh-session debt;
- runtime-megamodel identity;
- non-authority boundaries.

## Finite task and control states

Task stages:

```text
BELIEF → DECISION → PLAN → ACT → OBSERVE → VERIFY → LEARN
                                                       └→ PLAN
any stage → TERMINAL
```

Control modes:

```text
IDLE | ACTIVE | SUSPENDED | RECOVERING | TERMINATED
```

Authority modes:

```text
UNBOUND | BOUND | LEASED | RENEWAL_REVIEW | ESCALATION | REROTATION
```

Visible module status:

```text
IDLE | RUNNING | SUCCEEDED | FAILED | BLOCKED | SUSPENDED
```

## Finite recovery algebra

```text
CONTINUE
RETRY
REVALIDATE
REPLAN
RENEW
ESCALATE
REROTATE
REQUEST_HUMAN
ABORT
```

Every recovery decision has a fixed contract containing:

- whether suspension is required;
- whether a separate authority receipt is required;
- whether a new lineage is required;
- whether a new session is required;
- whether the route is terminal.

A terminal session is never resumed. All nonterminal recovery from a suspended session creates a fresh lineage and requires a new activation and session.

## Global invariants

### Safety

1. Execution is allowed only in `ACT`, with `ACTIVE` control, `LEASED` authority, a nonterminal active session, and a running module.
2. `SUSPENDED`, `RECOVERING`, and `TERMINATED` states cannot execute.
3. A terminal session digest cannot become active again.
4. Re-rotation increments the capability epoch by exactly one.
5. Abort clears execution and ends in `TERMINAL / TERMINATED`.

### Consistency

1. Verification cannot be committed before observation.
2. Session, lease, epoch, owner, evidence, verification, and recovery models remain connected through the runtime megamodel.
3. Recovery does not reactivate or overwrite the old session lineage.
4. Observation is evidence production, not verification or truth authority.

### Liveness boundary

1. A suspended state must be routed to a recovery decision or abort.
2. Nonterminal recovery completion returns to `PLAN` with fresh-lineage debt discharged but fresh activation/session still required.
3. Recovery that cannot satisfy its contract must escalate, request human review, or abort rather than loop without a bound.

### Non-authority

```text
planner does not grant execution
monitor does not grant renewal
router does not perform recovery
evidence does not grant truth
no architecture component grants memory overwrite by implication
```

## Refinement map for existing implementation

```text
PlanOS v0.1–v0.8   → Deliberation Plane
PlanOS v0.9–v0.14  → Authority Plane
PlanOS v0.15       → Execution/session boundary
PlanOS v0.16       → Assurance Plane
PlanOS v0.17       → Recovery Plane
BeliefOS           → Deliberation Plane
DecisionOS         → Deliberation Plane
ActOS/ObserveOS/
VerifyOS           → Execution Plane
LearnOS            → Learning Plane
```

The existing implementations remain valid. Their role changes from an ever-growing PlanOS sequence to plane-local refinements of this reference model.

## Feature admission rule

A new feature may be implemented only after all of the following are declared:

1. owning plane;
2. runtime model kind;
3. global event kind;
4. source-state precondition;
5. target-state postcondition;
6. safety, consistency, liveness, and non-authority effects;
7. recovery contract and terminality;
8. megamodel relations used;
9. refinement target in the existing implementation;
10. model-based positive and negative tests.

A proposal that cannot identify these ten items is an architecture question, not an implementation task.

## Versioning rule

The next missing capability is selected from an uncovered transition or unproved invariant in the global model. It is not selected by incrementing the latest PlanOS number.

Changes to plane-local implementation may keep their local versioning. Changes to the global state space, recovery algebra, or invariants require an explicit reference-architecture revision.

## Current v1.0 validation scenarios

The executable model validates:

- the nominal belief-to-learning cycle;
- observation before verification;
- execution only under an active leased session;
- lease anomaly causing terminal suspension of the old session;
- routing and completion of re-rotation with epoch successor and fresh lineage;
- rejection of terminal-session reactivation;
- abort reaching a non-executing terminal state;
- complete PlanOS v0.1–v0.17 plane coverage;
- complete runtime-megamodel relation coverage.
