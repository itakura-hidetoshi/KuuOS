# KuuOS Adaptive Agent Reference Architecture v1.0

## Purpose

This document is an organizing map for KuuOS components, runtime relations, and safety boundaries. It supports design review and communication while remaining open to revision as research, clinical needs, implementation experience, and conceptual exploration develop.

## Research basis

The architecture draws on several established ideas.

1. **MORPH** separates behavior adaptation from configuration adaptation while coordinating both through a reference architecture: <https://arxiv.org/abs/1504.08339>.
2. **Models and Megamodels at Runtime** treats runtime models and their relations as explicit managed objects rather than scattered cross-links: <https://arxiv.org/abs/1805.07396>.
3. **ActivFORMS** makes feedback-loop behavior itself a formally modeled and verified lifecycle artifact: <https://arxiv.org/abs/1908.11179>.
4. **Simplex runtime assurance** separates a flexible controller from a small assurance mechanism capable of blocking unsafe control: <https://arxiv.org/abs/2102.12981>.
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
   ├─ recovery decisions
   ├─ bounded routing
   ├─ human escalation
   ├─ abort
   └─ fresh-lineage bootstrap
```

Behavior adaptation and configuration/authority adaptation are represented separately so their interactions can be inspected. A planner may request authority but may not create it. An assurance monitor may suspend control but may not renew or rotate capabilities. A recovery router may select a recovery path but may not execute the recovery itself.

The planes are explanatory boundaries rather than exclusive ownership rules. A capability may span several planes when its design requires it, provided its state, authority, and safety consequences remain explicit.

## Runtime megamodel

The current runtime megamodel contains twelve model kinds:

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

The current reference relations are:

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

These relations describe the present runtime spine and may be revised or extended when the design evolves.

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

## Task and control states

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

## Recovery decisions

The current implementation models:

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

Each modeled decision records:

- whether suspension is required;
- whether a separate authority receipt is required;
- whether a new lineage is required;
- whether a new session is required;
- whether the route is terminal.

A terminal session is never resumed. Nonterminal recovery from a suspended session creates a fresh lineage and requires a new activation and session.

## Global invariants

### Safety

1. Execution is allowed only in `ACT`, with `ACTIVE` control, `LEASED` authority, a nonterminal active session, and a running module.
2. `SUSPENDED`, `RECOVERING`, and `TERMINATED` states cannot execute.
3. A terminal session digest cannot become active again.
4. Re-rotation increments the capability epoch by exactly one.
5. Abort clears execution and ends in `TERMINAL / TERMINATED`.

### Consistency

1. Verification cannot be committed before observation.
2. Session, lease, epoch, owner, evidence, verification, and recovery models remain coherently related.
3. Recovery does not reactivate or overwrite the old session lineage.
4. Observation is evidence production, not verification or truth authority.

### Liveness boundary

1. A suspended state must be routed to a recovery decision or abort.
2. Nonterminal recovery completion returns to `PLAN` with a fresh lineage while a fresh activation and session remain required.
3. Recovery that cannot satisfy its contract must escalate, request human review, or abort rather than loop without a bound.

### Non-authority

```text
planner does not grant execution
monitor does not grant renewal
router does not perform recovery
evidence does not grant truth
no architecture component grants memory overwrite by implication
```

## Map of the current implementation

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

This is a retrospective map of the current implementation. It does not redefine the modules or determine the direction of future development.

## Use of the reference architecture

The reference architecture can help:

- show how a new idea touches existing state and authority boundaries;
- reveal dependencies before implementation;
- avoid accidental duplication or contradictory transitions;
- make safety and recovery consequences visible;
- compare alternative designs.

New work may extend, revise, or bypass parts of this map when there is a sound reason. The architecture records current understanding and remains subordinate to the purposes of KuuOS.

## Current v1.0 validation scenarios

The executable model validates:

- the nominal belief-to-learning cycle;
- observation before verification;
- execution only under an active leased session;
- lease anomaly causing terminal suspension of the old session;
- routing and completion of re-rotation with epoch successor and fresh lineage;
- rejection of terminal-session reactivation;
- abort reaching a non-executing terminal state;
- consistency of the current PlanOS v0.1–v0.17 mapping;
- consistency of the current runtime-megamodel relations.
