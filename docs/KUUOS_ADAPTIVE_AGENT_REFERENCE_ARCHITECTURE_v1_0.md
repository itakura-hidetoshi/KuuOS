# KuuOS Adaptive Agent Reference Architecture v1.0

## Purpose

This document provides an organizing map for KuuOS components, runtime relations, and safety boundaries. It is descriptive and advisory: it does not restrict new ideas, require development to close model coverage, or act as a feature-admission gate. New functions may arise from research, clinical needs, implementation experience, or conceptual exploration; the architecture helps place them coherently without making the map the purpose of development.

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

These planes are explanatory boundaries, not exclusive ownership rules. A new capability may span several planes when its design requires it, provided the authority and safety consequences remain explicit.

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

These relations document and validate the current runtime spine. They may be extended when a new, justified design introduces another model or relation; the existing set is not a closed catalogue of all future KuuOS concepts.

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

Every currently modeled recovery decision has a contract containing:

- whether suspension is required;
- whether a separate authority receipt is required;
- whether a new lineage is required;
- whether a new session is required;
- whether the route is terminal.

A terminal session is never resumed. All nonterminal recovery from a suspended session creates a fresh lineage and requires a new activation and session.

The algebra is finite for validation of the present implementation, but it is not a policy forbidding future recovery concepts. Extensions require explicit semantics and safety review, not satisfaction of a coverage quota.

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

## Map of the existing implementation

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

This is a retrospective map of the current implementation. It does not redefine those modules, require all future work to fit one existing category, or turn architectural coverage into a development objective.

## Use of the reference architecture

The reference architecture may be used to:

- understand where a new idea touches existing state and authority boundaries;
- identify dependencies before implementation;
- avoid accidental duplication or contradictory state transitions;
- make safety and recovery consequences visible;
- compare alternative designs.

It must not be used to:

- block a feature because it is not already represented in the model;
- require development to close every uncovered transition or relation;
- make coverage completion the purpose of KuuOS development;
- replace exploratory, theoretical, clinical, or creative development;
- freeze the future vocabulary of KuuOS.

New work may use local versioning and may extend, revise, or bypass parts of this reference map when there is a sound reason. Changes to the map record an architectural understanding; they are not prerequisites for having a new idea.

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

These checks protect the implemented model. They do not define a coverage-closure roadmap.