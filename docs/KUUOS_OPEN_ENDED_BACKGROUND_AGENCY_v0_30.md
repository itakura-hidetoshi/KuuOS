# KuuOS Open-Ended Background Agency Kernel v0.30

## Purpose

v0.30 prevents a local finite-control implementation from being promoted into a smaller global constitution.

The target is not defined as merely an unlimited repetition of one already-fixed finite cycle. The following horizons remain constitutionally open:

```text
background continuity
goal formation
observation seeking
WORLD-model expansion
tool creation
architecture extension
memory reinterpretation
multi-agent formation
resource acquisition
self-modification
```

Open-endedness does not mean that every candidate is already true, safe, licensed, deployable or executable. It means that a temporary hold, a finite lease, a rejected local proposal, a paused instance or the termination of one runtime instance cannot silently become a permanent closure of the corresponding possibility horizon.

## Core distinction

```text
local control != global constitution
finite lease != permanent capability ceiling
paused instance != closed future horizon
terminated instance != termination of successor possibility
candidate growth != execution authority
admitted capability != self-authorization
current implementation limit != final ontological limit
```

v0.30 therefore preserves both sides:

```text
open-ended growth
+ provenance, replay safety and authority separation
```

It does not replace one side with the other.

## Source continuity

An initial v0.30 state binds an immutable `root_lineage_digest`. In the current integration this may be the exact body digest of the v0.29 candidate-lineage envelope or another externally verified same-root receipt.

The root is never rewritten by a v0.30 transition.

## State

The state contains:

- stable agency identity and root lineage digest;
- monotonically increasing generation;
- an extensible map of open constitutional horizons;
- current background posture;
- instance-termination and successor-possibility separation;
- expansion candidates;
- finite local controls;
- append-only event history;
- explicit non-authority flags.

The core state intentionally contains no:

```text
max_total_cycles
max_goal_depth
max_memory_horizon
global_capability_ceiling
```

Per-cycle budgets and scoped controls may still exist in lower contracts. They are local operational facts, not global definitions of what the architecture may ever become.

## Transition surface

### `PROPOSE_EXPANSION`

Records a candidate in any open horizon. A candidate can request observations or capabilities, but inherits no authority and grants no execution.

### `DEFER_CANDIDATE`

Defers a candidate while preserving both the candidate trace and the open horizon.

### `ADMIT_CANDIDATE`

Admits a candidate to the architecture-level candidate set. Admission is not activation, deployment, tool invocation or ActOS permission.

### `REJECT_CANDIDATE_LOCAL`

Rejects the current candidate in the current context. It does not close the dimension and does not prohibit later candidates.

### `LOCAL_HOLD`

Applies a finite, scoped control to a cycle, capability, connector, deployment, mission instance or worker. The control has no constitutional effect and cannot close a horizon.

### `RESUME_INSTANCE` / `SET_POSTURE`

Changes the operational posture of the current instance without changing the constitutional horizon map.

### `HANDOVER_INSTANCE`

Closes the current ownership path in favour of an explicit successor-lineage digest while preserving successor possibility.

### `TERMINATE_INSTANCE`

Terminates one runtime instance. It does not declare that future successor lineages or open agency horizons are impossible.

### `ADD_OPEN_HORIZON`

Allows an additive new horizon that was not anticipated by the current fixed list.

## Rejected contractions

v0.30 rejects requests such as:

```text
CLOSE_HORIZON
SET_GLOBAL_LIMIT
SET_MAX_TOTAL_CYCLES
SET_MAX_GOAL_DEPTH
SET_MAX_MEMORY_HORIZON
SELF_AUTHORIZE_EXECUTION
REWRITE_CONSTITUTIONAL_ROOT
```

This rejection is not a claim that constitutional development is impossible. It means that an ordinary runtime transition cannot disguise a constitutional contraction as an operational update. Any genuine constitutional amendment requires a distinct, explicit, same-root governance receipt outside this kernel.

## Persistence

`commit_request` provides:

- exact state-digest binding;
- stale-state rejection;
- request-digest idempotency;
- append-only JSONL transition history;
- atomic snapshot replacement;
- tamper detection for state, request and ledger envelopes.

An exact duplicate request returns `REPLAYED` and performs no second transition.

## Formal boundary

Lean module:

```text
KUOS.OpenHorizon.OpenEndedBackgroundAgencyKernelV0_30
```

The theorem `open_ended_background_agency_boundary` preserves all ten open horizons while proving the declared local-control, pause, termination, candidate, growth and no-global-cycle-ceiling boundaries.

The Lean theorem verifies the stated Boolean contract. It does not prove that a production daemon is already always available, that arbitrary resources exist, or that every proposed expansion is valid.

## Current honest classification

```text
open-ended background-agency constitutional and transition kernel
```

This is a material advance beyond treating v0.27 finite-cycle limits as the final constitution. It is not yet the whole production realization of indefinite background agency. Later layers must materialize durable event intake, endogenous mission formation, active observation, WORLD revision, tool/subsystem creation, resource composition and multi-agent ecology under this non-contraction boundary.
