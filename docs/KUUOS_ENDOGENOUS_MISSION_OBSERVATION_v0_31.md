# KuuOS Endogenous Mission Formation and Autonomous Observation Seeking v0.31

## Purpose

v0.31 materializes the first operational layer above the v0.30 open-ended background-agency constitution.

The kernel accepts unresolved WORLD evidence and produces:

```text
unresolved WORLD evidence
→ plural mission candidates
→ plural observation candidates
→ deterministic priority portfolio
→ ready / capability discovery / hold / handover
```

The generated objects remain candidates. This kernel does not activate PlanOS, invoke an observation tool, call ActOS or promote a hypothesis to truth.

## Exact source binding

Every evidence packet binds:

- the exact v0.30 source-state digest;
- a WORLD-fragment digest;
- a stable packet identity;
- observation time;
- unresolved questions;
- supporting evidence;
- counterevidence;
- uncertainty and severity;
- currently available observation channels.

A packet cannot be applied to another source state. Packet or report tampering is detected by the immutable envelope digest.

## Endogenous mission formation

For each unresolved item, v0.31 creates a deterministic mission candidate.

- no counterevidence → `INVESTIGATE`;
- counterevidence present → `DISAMBIGUATE`.

Priority is determined from severity, uncertainty, counterevidence and evidence count. The score orders the portfolio but does not grant truth or authority.

Each mission candidate explicitly carries:

```text
status = CANDIDATE
grants_activation_authority = false
grants_execution_authority = false
grants_truth_authority = false
```

## Autonomous observation seeking

For every mission candidate, each compatible observation channel becomes a separate observation candidate. This preserves plurality instead of collapsing immediately to one method.

An observation candidate records:

- target mission and unresolved item;
- channel and modality;
- cost, risk and latency classes;
- expected-information-gain score;
- proposal status;
- explicit non-invocation boundaries.

```text
observation candidate != tool invocation
observation candidate != ActOS invocation
```

When no compatible channel exists, v0.31 creates a `CAPABILITY_DISCOVERY_CANDIDATE`. Missing capability therefore remains an open architectural problem rather than becoming evidence that the mission is impossible.

## Routes

### `MISSION_PORTFOLIO_READY`

Unresolved evidence exists and at least one compatible observation channel is available for every item.

### `CAPABILITY_DISCOVERY`

At least one unresolved item lacks a compatible observation channel. The generated capability candidate has no self-authorizing power.

### `NO_NEW_MISSION`

The packet contains no unresolved items.

### `HOLD`

The v0.30 source instance is paused. Candidate generation is retained, but no activation follows.

### `HANDOVER`

The source instance is terminated or already handed over. Candidate and observation traces are retained for successor review.

## Preserved non-collapse

v0.31 preserves:

- all unresolved items;
- counterevidence;
- uncertainty;
- plural mission candidates;
- plural observation candidates;
- exact source-state lineage;
- exact WORLD-fragment lineage.

It does not rewrite the v0.30 constitutional horizon map.

## Persistence

Reports can be appended to a JSONL ledger.

- exact replay returns `REPLAYED`;
- the same packet ID cannot bind to a different report;
- the same packet digest cannot bind to a different report;
- existing ledger entries are validated before append.

## Formal boundary

Lean module:

```text
KUOS.OpenHorizon.EndogenousMissionObservationKernelV0_31
```

The theorem `endogenous_mission_observation_boundary` proves the declared contract:

- goal formation, observation seeking and WORLD expansion remain open;
- unresolved evidence, counterevidence and uncertainty are retained;
- plural mission and observation candidates are generated;
- source and WORLD fragment are bound exactly;
- mission candidate is not activation;
- observation candidate is neither tool nor ActOS invocation;
- capability-gap, hold, handover and persistence boundaries are present.

The theorem verifies the typed contract. It does not prove that every observation channel exists or that any generated mission is scientifically correct.

## Honest classification

```text
endogenous mission-candidate formation
and autonomous observation-portfolio generation kernel
```

The next layer should transform an admitted observation candidate into a separately authorized ObserveOS request and feed the resulting evidence back into WORLD without converting proposal ranking into execution authority.
