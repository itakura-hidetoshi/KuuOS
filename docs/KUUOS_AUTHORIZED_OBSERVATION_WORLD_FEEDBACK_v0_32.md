# KuuOS Authorized Observation Acquisition and WORLD Feedback v0.32

## Purpose

v0.32 connects the v0.31 observation portfolio to actual ObserveOS acquisition without converting candidate ranking into execution authority.

```text
v0.31 observation candidate
→ external finite authorization receipt
→ single-use ObserveOS request
→ provenance-complete evidence receipt
→ WORLD update candidate or reobserve route
→ VerifyOS debt remains open
```

The kernel gives a narrowly scoped permission to perform one observation. It does not grant general ActOS effect authority, PlanOS activation, truth, verification, causal attribution, memory overwrite, root rewrite or automatic mission completion.

## Official runtime entry

```text
runtime/kuuos_authorized_observation_world_feedback_entry_v0_32.py
```

The entry extends the core runtime with mandatory authorization-window inheritance. Both request creation and evidence collection must occur inside the externally issued finite window.

## Authorization receipt

An observation authorization binds exactly:

- v0.31 source-report digest;
- v0.30 source-state digest;
- constitutional root-lineage digest;
- prior WORLD-fragment digest;
- mission candidate;
- observation candidate;
- observation channel;
- concrete tool identity;
- purpose/scope digest;
- host-license digest;
- issuing authority identity;
- not-before and expiry times;
- one permitted invocation.

The receipt contains:

```text
max_invocations = 1
single_use = true
grants_observe_invocation = true
```

while explicitly preserving:

```text
grants_actos_effect_authority = false
grants_plan_activation = false
grants_truth_authority = false
grants_verification_authority = false
grants_memory_overwrite_authority = false
```

A `CAPABILITY_DISCOVERY_CANDIDATE`, `HOLD`, `HANDOVER` or otherwise non-ready v0.31 report cannot be converted into an authorized observation request.

## Authorized ObserveOS request

The request inherits the complete authorization binding and records:

- deterministic request identity;
- exact authorization digest and ID;
- source report/state/root/WORLD digests;
- mission, observation and unresolved-item identity;
- channel, modality and tool;
- scope and host-license digests;
- invocation index `1`;
- the expected evidence fields;
- the complete authorization time window.

Creating the request does not execute the tool by itself. The request is the typed, externally licensed input to a host-side ObserveOS adapter.

The append-only request ledger enforces:

```text
one authorization receipt → at most one distinct ObserveOS request
```

Exact replay is idempotent.

## Evidence receipt

An evidence receipt binds the exact request and authorization and requires:

- immutable raw-artifact digest;
- value digest;
- collector identity;
- independent-source identity;
- collection time;
- uncertainty digest;
- calibration digest;
- context digest;
- tamper-evidence digest;
- provenance-chain digest;
- evidence relation.

Allowed relations are:

```text
SUPPORTS
CONTRADICTS
INCONCLUSIVE
CONFLICTED
```

Collection must complete before the authorization expiry. Starting inside the window is not sufficient.

Every receipt preserves:

```text
observation_recorded = true
observation_is_verification = false
verification_required = true
grants_truth_authority = false
grants_causal_attribution = false
```

The evidence ledger enforces:

```text
one ObserveOS request → at most one distinct evidence receipt
```

## WORLD feedback candidate

The evidence receipt is transformed into a candidate WORLD fragment, not a committed WORLD rewrite.

### Supporting evidence

```text
route = WORLD_UPDATE_CANDIDATE
candidate_state = SUPPORTED_UPDATE_CANDIDATE
```

### Contradicting evidence

```text
route = WORLD_UPDATE_CANDIDATE
candidate_state = CONTRADICTED_UPDATE_CANDIDATE
```

Prior counterevidence and uncertainty remain present.

### Inconclusive evidence

```text
route = REOBSERVE
candidate_state = UNRESOLVED_REOBSERVE
```

### Conflicted evidence

```text
route = REOBSERVE
candidate_state = CONFLICTED_REOBSERVE
```

The proposed WORLD-fragment digest is deterministically derived from the prior fragment, evidence receipt and candidate state.

Every route preserves:

```text
world_update_is_candidate = true
verification_required = true
automatic_truth_promotion = false
automatic_root_rewrite = false
automatic_mission_completion = false
```

The feedback ledger enforces:

```text
one evidence receipt → at most one distinct WORLD feedback candidate
```

## Core distinctions

```text
observation candidate != observation authorization
observation authorization != generic execution authority
authorized request != completed observation
observation receipt != verification
supporting evidence != truth
contradicting evidence != causal attribution
WORLD update candidate != WORLD root rewrite
observation success != mission completion
```

## Formal boundary

Lean module:

```text
KUOS.OpenHorizon.AuthorizedObservationWorldFeedbackKernelV0_32
```

The theorem `authorized_observation_world_feedback_boundary` preserves:

- open observation-seeking and WORLD-expansion horizons;
- exact candidate and authorization binding;
- finite, single-use authorization;
- scope, tool, host-license and same-root binding;
- exact evidence binding;
- raw-artifact and provenance preservation;
- authorization-window preservation;
- observation/verification separation;
- permanent verification debt;
- no truth or causal promotion;
- reobservation for inconclusive/conflicted evidence;
- WORLD update as candidate only;
- counterevidence and uncertainty;
- no automatic root rewrite or mission completion;
- append-only replay-safe ledgers.

The theorem verifies the declared typed contract. It does not prove the scientific truth of an observation, the reliability of a physical sensor, or the adequacy of a future VerifyOS result.

## Honest classification

```text
externally authorized single-use observation acquisition
and provenance-preserving WORLD feedback candidate kernel
```

The next layer should bind the WORLD feedback candidate to VerifyOS, produce a verification receipt, and only then generate a separately governed WORLD adoption/rejection/defer decision.
