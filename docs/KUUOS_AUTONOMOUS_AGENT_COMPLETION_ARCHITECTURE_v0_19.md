# KuuOS Autonomous Agent Completion Architecture v0.19

## Status

This document structures the remaining work between the current KuuOS bounded-resumable runtime and an indefinitely continuing autonomous agent.

v0.19 is an architecture and contract release. It does **not** open new execution authority.

## Design summary / 設計要旨

KuuOS already has a durable execution substrate:

```text
v0.15 stop reason / feedback / checkpoint
v0.16 resumable supervised job and foreground yield
v0.17 one licensed host invocation -> one job -> one bounded slice
v0.18 fair multi-job / multi-worker orchestration, backpressure, dead-letter
```

The missing layer is not another scheduler. The missing layer is the persistent cognitive and governance order that decides:

```text
what should continue
why it should continue
what evidence changed
whether the result satisfies the mission
what should be learned
when to replan, ask, pause, renew, or terminate
```

The target is not unrestricted or resource-infinite agency.

```text
indefinite duration
  = an unbounded number of separately bounded, licensed, observable,
    replay-safe, interruptible cycles

indefinite duration
  != unbounded authority
  != unbounded resource use
  != irreversible self-modification
  != arbitrary shell or network execution
```

## 1. Existing substrate boundary

The following surfaces are treated as lower, already implemented authority boundaries:

| Layer | Existing responsibility | Must not be recomputed above |
|---|---|---|
| v0.15 | stop classification, feedback, checkpoint, foreground release | blocker classification and resumability truth |
| v0.16 | job state, completed prefix, bounded step execution, user commands | successful step receipts and completed-prefix history |
| v0.17 | host license, projection eligibility, ticket claim, one bounded slice | operation authority, lease validity, host replay |
| v0.18 | fairness, worker health, backpressure, dead-letter metadata | multi-job scheduling and worker dispatch bounds |

Higher autonomous layers may propose, observe, verify, and request execution. They cannot bypass these lower boundaries.

## 2. Five architectural planes

### Plane A — Mission and commitment

Owns the persistent answer to: **what is the agent trying to accomplish, under which limits, and when should the mission stop or renew?**

Components:

1. Mission Contract Kernel
2. Goal Portfolio and Conflict Arbitration
3. Mission Renewal and Termination Kernel

### Plane B — Cognition and epistemic control

Owns the answer to: **what is currently believed, what remains unknown, what plan should be attempted, and did the result actually satisfy the goal?**

Components:

4. Observation and Belief-State Kernel
5. Semantic Planner and Replanner
6. Outcome Verifier and Contradiction Detector

### Plane C — Memory and learning

Owns the answer to: **what should be retained, revised, forgotten, or reused after experience?**

Components:

7. Cognitive Memory Consolidator
8. Bounded Credit Assignment and Strategy Learning

### Plane D — Effects and environment

Owns the answer to: **how can a proposed action become a real external effect with evidence, idempotency, and compensation?**

Components:

9. Transactional Tool and Connector Fabric
10. World-State Observation and Effect Reconciliation

### Plane E — Control, resources, and evolution

Owns the answer to: **what wakes the agent, how can a user intervene, how are resources renewed, and how can the agent improve without self-authorizing?**

Components:

11. Event and Wake-up Fabric
12. User Control and Status Plane
13. Resource and Model Governor
14. Governed Self-Modification Gate
15. Integrated Indefinite Operation Kernel

## 3. Component contracts

### 3.1 Mission Contract Kernel

**Purpose**

Persist the reason for operation independently of a transient prompt or process.

**Consumes**

- user or institutional mission proposal
- current governance root
- resource envelope proposal
- applicable domain boundary

**Produces**

- digest-bound mission contract
- success and failure criteria
- invariants and prohibited outcomes
- renewal and termination conditions
- escalation and user-intervention policy

**Failure states**

```text
mission_ambiguous
success_criteria_missing
constraint_conflict
resource_envelope_missing
authority_scope_missing
mission_expired
renewal_required
```

**Non-authority rule**

A mission contract is not an execution license.

### 3.2 Goal Portfolio and Conflict Arbitration

**Purpose**

Maintain multiple active, suspended, and proposed goals without allowing one local objective to become sovereign.

**Consumes**

- active mission contracts
- goal proposals
- horizon sections and resource state
- user priorities

**Produces**

- bounded goal portfolio
- typed conflict residues
- priority recommendation
- hold, defer, split, or handover decision proposal

**Failure states**

```text
goal_conflict_unresolved
priority_collapse_risk
resource_contention
invariant_collision
human_arbitration_required
```

**Non-authority rule**

Priority ranking cannot grant effect authority.

### 3.3 Mission Renewal and Termination Kernel

**Purpose**

Prevent an indefinitely running agent from silently converting persistence into permanent mission authority.

**Consumes**

- mission contract
- verifier evidence
- resource state
- elapsed horizon
- user and institutional commands

**Produces**

```text
continue
renewal_required
pause
complete
terminate
handover
```

**Invariant**

Every mission has an explicit renewal or termination boundary.

### 3.4 Observation and Belief-State Kernel

**Purpose**

Separate observed evidence, inferred belief, uncertainty, contradiction, and stale assumptions.

**Consumes**

- tool and environment observations
- source provenance
- temporal validity
- prior belief state

**Produces**

- local belief sections
- confidence and uncertainty
- contradiction and staleness residues
- observation requests

**Core rule**

```text
unknown != false
missing evidence != negative evidence
belief != truth authority
```

### 3.5 Semantic Planner and Replanner

**Purpose**

Transform mission and belief state into bounded executable proposals.

**Consumes**

- mission contract
- selected goal
- belief state
- available capabilities
- resource envelope
- prior plan and failure evidence

**Produces**

- subgoal decomposition
- bounded plan proposal
- typed dependencies
- alternative plans
- expected observations
- stale-plan invalidation receipt

**Invariant**

A plan remains proposal-level until lower licenses and gates authorize each effect.

### 3.6 Outcome Verifier and Contradiction Detector

**Purpose**

Decide whether completed steps and external effects actually satisfy the mission criteria.

**Consumes**

- mission success criteria
- plan claims
- step and effect receipts
- independent observations
- regression evidence

**Produces**

```text
verified_success
partial_success
inconclusive
contradicted
regression_detected
verification_requires_human
```

**Invariant**

Execution success does not imply mission success.

### 3.7 Cognitive Memory Consolidator

**Purpose**

Convert append-only experience into provenance-preserving episodic, semantic, procedural, negative, and working memory.

**Consumes**

- observations
- plans
- verifier outcomes
- contradictions
- mission lineage

**Produces**

- memory candidates
- confidence and provenance
- supersession links
- retention and forgetting proposals
- contradiction-preserving revisions

**Invariant**

Memory persistence cannot become belief sovereignty or root overwrite authority.

### 3.8 Bounded Credit Assignment and Strategy Learning

**Purpose**

Learn which strategies, tools, and plan templates were useful without unrestricted model or policy self-rewrite.

**Consumes**

- verified outcomes
- cost and latency
- strategy and tool provenance
- counterfactual and failure evidence

**Produces**

- bounded strategy scores
- tool reliability estimates
- plan-template rankings
- retry and resource-allocation recommendations

**Invariant**

Learning output is advisory and reversible. It cannot widen its own license.

### 3.9 Transactional Tool and Connector Fabric

**Purpose**

Turn authorized proposals into external effects with evidence and compensation.

**Protocol**

```text
prepare
validate
license
execute
observe
verify
commit receipt
compensate or handover
```

**Required properties**

- idempotency key
- capability lease
- exact input and output binding
- effect receipt
- timeout and retry semantics
- compensation or explicit non-compensability
- no hidden connector call

### 3.10 World-State Observation and Effect Reconciliation

**Purpose**

Compare intended effects with observed external state.

**Produces**

```text
effect_confirmed
effect_partial
effect_not_observed
effect_conflicted
external_state_changed
compensation_required
```

**Invariant**

Tool response success is not sufficient evidence that the world reached the intended state.

### 3.11 Event and Wake-up Fabric

**Purpose**

Provide an external always-on trigger surface without making the conversational model itself a hidden daemon.

**Trigger classes**

- clock and schedule
- queue availability
- lease expiry
- dependency completion
- resource replenishment
- webhook or connector event
- user command
- monitoring condition

**Invariant**

Every wake-up starts a new bounded, licensed cycle. Wake-up does not inherit unlimited authority.

### 3.12 User Control and Status Plane

**Purpose**

Keep the primary interaction channel available while jobs continue elsewhere.

**Commands**

```text
inspect
explain
pause
resume
cancel
reprioritize
revise mission
revise constraint
approve permission
increase budget
force replan
release dead-letter
handover
```

**Status contract**

```text
state
reason
completed work
checkpoint
next condition
resource state
worker state
valid user actions
```

### 3.13 Resource and Model Governor

**Purpose**

Manage finite budgets across indefinite duration.

**Controls**

- token and API budgets
- reserve floors
- model tier selection
- storage growth
- worker scaling and degradation
- expensive verification thresholds
- replenishment requests

**Invariant**

Indefinite continuation is achieved through renewable finite envelopes, never by removing resource bounds.

### 3.14 Governed Self-Modification Gate

**Purpose**

Allow bounded improvement proposals while preventing self-authorizing removal of constraints.

**Protocol**

```text
proposal
static analysis
sandbox
regression suite
formal/property checks
canary
external approval when required
limited deployment
rollback window
```

**Permanently forbidden self-actions**

- widening its own authority
- deleting hard gates
- disabling audit
- erasing provenance
- removing rollback
- granting unrestricted shell or network access
- redefining success to hide failure

### 3.15 Integrated Indefinite Operation Kernel

**Purpose**

Compose the preceding components into:

```text
Mission
  -> Observe
  -> Believe
  -> Plan
  -> License
  -> Act
  -> Reconcile
  -> Verify
  -> Learn
  -> Replan / Pause / Ask / Renew / Terminate
```

**Definition of completion**

The kernel is complete only when it can continue for an unbounded number of cycles while every individual cycle remains bounded, licensed, observable, interruptible, replay-safe, and renewable.

## 4. Typed implementation order

The remaining work is ordered by dependency rank, not by a global context graph.

| Rank | Target release | Components | Depends on |
|---:|---|---|---|
| 0 | existing v0.15–v0.18 | resumable execution and durable orchestration substrate | none |
| 1 | v0.20 | Mission Contract; Goal Portfolio; Renewal/Termination | rank 0 |
| 2 | v0.21 | Observation and Belief State | ranks 0–1 |
| 3 | v0.22 | Semantic Planner/Replanner; Outcome Verifier | ranks 0–2 |
| 4 | v0.23 | Cognitive Memory; Credit Assignment | ranks 0–3 |
| 5 | v0.24 | Transactional Tool Fabric; Effect Reconciliation | ranks 0–4 |
| 6 | v0.25 | Event/Wake-up; User Control; Resource Governor | ranks 0–5 |
| 7 | v0.26 | Governed Self-Modification Gate | ranks 0–6 |
| 8 | v0.27 | Integrated Indefinite Operation Kernel | ranks 0–7 |

No higher-rank component may silently reimplement or bypass a lower-rank authority decision.

## 5. Cross-cutting invariants

Every future release must preserve:

```text
bounded cycle
explicit authority
append-only lineage
checkpoint before handoff
foreground user control remains available
unknown != false
execution success != mission success
plan != permission
memory != truth
learning != self-license
wake-up != authority
queue != running
running != verified
verified != permanent mission renewal
resource exhaustion -> feedback + pause/replan
self-modification -> externalized gate + rollback
```

## 6. Readiness dimensions

The architecture is evaluated independently across these dimensions:

1. mission persistence
2. epistemic state
3. planning and replanning
4. verification
5. cognitive memory
6. bounded learning
7. transactional effects
8. world-state reconciliation
9. wake-up continuity
10. user control
11. resource renewal
12. self-modification governance
13. integration and long-duration recovery

A high score in execution durability cannot compensate for a missing mission, verifier, or user-control layer.

## 7. Current readiness assessment

| Dimension | Current state | Evidence boundary |
|---|---|---|
| durable bounded execution | implemented | v0.15–v0.18 |
| multi-job / multi-worker orchestration | implemented | v0.18 |
| mission persistence | open gap | transient prompts and job manifests are insufficient |
| semantic replanning | open gap | execution plans are predeclared rather than autonomously synthesized |
| epistemic belief state | open gap | operational job state is not world belief |
| independent verification | open gap | step success is not mission verification |
| cognitive memory consolidation | partial substrate | append-only lineage exists; cognitive consolidation does not |
| bounded learning | open gap | no verified long-horizon credit assignment |
| transactional external effects | partial substrate | bounded adapters exist; common prepare/commit/compensate protocol does not |
| always-on wake-up | host-dependent gap | each later slice or cycle still requires a new host invocation |
| asynchronous user control | partial substrate | commands exist; independent status stream and control service do not |
| resource renewal | partial substrate | finite budgets exist; renewal and portfolio allocation remain incomplete |
| governed self-modification | partial governance only | proposal-to-canary-to-rollback kernel remains open |

## 8. Release acceptance rule

A future component may move from `open_gap` to `implemented` only when it has:

- a versioned contract
- typed inputs and outputs
- explicit failure states
- non-authority boundary
- digest or equivalent identity binding
- replay and stale-state behavior
- persistence semantics
- kernel validation
- integration validation with all lower layers
- an honest formal status statement

## 9. Immediate next implementation

The next executable release is **v0.20 Mission Contract Kernel**.

It should implement:

1. immutable mission identity and lineage
2. success, failure, invariant, and prohibited-outcome clauses
3. resource envelope and renewal boundary
4. user and institutional override policy
5. active, paused, renewal-required, completed, terminated, and handed-over states
6. exact binding from mission to goal portfolio and future plan proposals
7. explicit proof that mission persistence grants no effect authority

Until v0.20 exists, KuuOS should be described as a durable bounded autonomous execution substrate, not a complete indefinitely continuing autonomous agent.
