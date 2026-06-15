# KuuOS Adapter Portfolio and Shadow Comparison v0.7

## Purpose

v0.7 adds a capability-aware adapter portfolio above Adapter Capability Gauge v0.6.
Exactly one adapter is live in each cycle. Other eligible adapters receive a shared,
non-actuating shadow projection.

```text
source batch
  -> v0.6 capability scores
  -> resolved portfolio correction
  -> one live adapter
  -> one v0.6 live cycle
  -> observed live effect
  -> resolve an earlier shadow prediction when applicable
  -> create new non-actuating shadow projections
  -> portfolio holonomy
```

v0.7 does not execute every candidate. It does not treat an unobserved prediction as
capability evidence.

## Upstream stack

```text
v0.1  Open-Horizon Telos Genesis
v0.2  Open-Horizon Commitment Gauge
v0.3  Active Gauge Intervention Loop
v0.4  Renewable Gauge Supervisor
v0.5  Event Source and Adapter Federation
v0.6  Adapter Capability Gauge
v0.7  Adapter Portfolio and Shadow Comparison
```

## Live and shadow roles

Each invocation has two distinct roles.

```text
live adapter
  selected once
  delegated to one v0.6 cycle
  may produce one committed local effect
  supplies actual effect evidence

shadow adapters
  receive the same context and covariant step kind
  produce deterministic utility projections only
  do not invoke v0.6
  do not call an adapter
  do not append the local execution ledger
  do not update v0.6 capability connections
```

The derived child registry enables only the selected live adapter. Every other entry
is explicitly marked `shadow_non_actuating`.

## Portfolio selection

v0.7 first computes the ordinary v0.6 candidate scores from the current capability
bundle. A separate portfolio adjustment may then be added.

```text
adjusted_score =
  v0.6 capability score
  + bounded resolved-shadow adjustment
```

The adjustment is:

```text
raw_adjustment =
  resolved_evidence_weight
  * reliability
  * shadow_bias

portfolio_adjustment = clamp(
  raw_adjustment,
  -max_portfolio_adjustment,
  +max_portfolio_adjustment
)
```

Only errors that were later realized by a live effect can contribute to
`shadow_bias`. Pending predictions have zero authority over the adjustment.

Candidate ordering is:

1. descending adjusted score;
2. static registry priority only as a tie-break;
3. adapter ID.

## Shadow prediction

For a non-live candidate, v0.7 uses:

- the candidate's current v0.6 capability connection;
- the candidate-specific route for the shared covariant step;
- a bounded action-utility prior supplied by the v0.7 plan;
- a reliability-weighted bias learned only from resolved predictions.

```text
predicted_utility = clamp(
    (1 - shadow_model_weight) * capability_connection
  + shadow_model_weight * action_utility_prior
  + reliability * resolved_shadow_bias
)
```

The projection stores:

```text
adapter ID
adapter profile digest
context key
shared covariant step kind
predicted local domain action
connection component
action-utility component
resolved bias component
predicted utility
prediction confidence
relative residual against the current live result
source live effect digest
```

The relative residual is descriptive only:

```text
counterfactual_relative_residual =
  predicted_shadow_utility - observed_live_utility
```

It is not written into the v0.6 capability connection.

## Delayed realization

A shadow prediction becomes calibratable only when that same adapter is selected as a
live adapter in a later compatible context.

For a prediction `P` and later live utility `U`:

```text
realization_error = U - P
```

The portfolio bias update is:

```text
alpha_effective =
  shadow_learning_rate * prediction_confidence

bias_next = clamp_signed(
  bias + alpha_effective * (realization_error - bias)
)
```

Reliability increases only with resolved predictions:

```text
reliability =
  resolved_count / (resolved_count + reliability_prior_mass)
```

This separates three epistemic states:

```text
pending shadow prediction
  counterfactual estimate only

resolved shadow prediction
  compared with later live evidence

v0.6 capability evidence
  produced directly by a committed live effect
```

Only the third updates the v0.6 capability field. The second updates the independent
v0.7 portfolio bias.

## Context locality

Portfolio sections are keyed by:

```text
adapter ID × v0.6 context key
```

A prediction in one source/wake/signal context is not automatically transferred to a
different context. Context locality is inherited from v0.6.

## Recovery and replay

The v0.7 ledger has pending and committed phases.

1. portfolio selection is persisted;
2. a pending row binds the prior v0.6 and v0.7 state/bundle digests;
3. the selected live adapter is delegated to deterministic child run
   `<portfolio_run_id>:capability`;
4. the live effect is validated;
5. shadow resolution and projections are committed;
6. the portfolio bundle, state, ledger, receipt, and audit are written.

On retry:

- a committed v0.7 run returns replay without another live cycle;
- a pending run reuses the exact stored live selection;
- the v0.6 child run replays by its deterministic run ID;
- processed live effect digests prevent a duplicate portfolio update;
- shadow adapters still perform no execution.

## Outputs

```text
kuuos_adapter_portfolio_bundle_v0_7.json
kuuos_adapter_portfolio_selection_v0_7.json
kuuos_adapter_shadow_projection_v0_7.json
kuuos_adapter_shadow_resolution_v0_7.json
kuuos_adapter_portfolio_state_v0_7.json
kuuos_adapter_portfolio_receipt_v0_7.json
kuuos_adapter_portfolio_ledger_v0_7.jsonl
kuuos_adapter_portfolio_audit_v0_7.jsonl
```

All v0.1-v0.6 artifacts from the one live child cycle remain available.

## Demonstrated sequence

The integration test reuses the v0.6 adapters:

```text
adapter A
  high static priority
  prior capability 0.72
  route -> hold

adapter B
  low static priority
  prior capability 0.55
  route -> advance_tick
```

Expected behavior:

```text
cycle 1
  A live
  B shadow
  one local execution

cycle 2
  B live after v0.6 capability adaptation
  prior B shadow prediction is resolved when compatible
  A shadow
  one additional local execution

cycle 3
  B remains live
  resolved B evidence can produce only a bounded portfolio adjustment
  A shadow
  one additional local execution
```

Across three cycles:

```text
live effects = 3
local execution ledger rows = 3
shadow projections = 3
shadow executions = 0
```

## Formal surface

`formal/KUOS/OpenHorizon/AdapterPortfolioShadowV0_7.lean` defines:

```lean
realizationError prediction realizedUtility
resolveBias alpha oldBias prediction realizedUtility
boundedPortfolioAdjustment bound reliability bias
```

It proves:

- zero-rate resolution preserves the old bias;
- full-rate resolution reaches the realization error;
- exact predictions have zero realization error;
- shadow actuation count remains zero;
- portfolio adjustment lies between `-bound` and `bound`;
- a portfolio cycle has zero or one live adapter;
- live-cycle history grows monotonically.

## Authority boundary

v0.7 does not grant:

- multiple live adapter execution;
- shadow adapter execution;
- shadow network or external actuation;
- shadow WORLD mutation;
- shadow MemoryOS overwrite;
- direct shadow writes into v0.6 capability connections;
- truth authority to prediction scores;
- authority escalation from portfolio ranking.

The layer expands observation and comparison while keeping actual intervention finite
and singular.

## Next layer

A natural v0.8 is a bounded portfolio experiment scheduler:

```text
resolved portfolio uncertainty
  -> bounded information-gain opportunity
  -> licensed live exploration proposal
  -> one selected experiment
  -> actual effect
  -> portfolio and capability update
```

Unlike v0.7 shadow comparison, v0.8 would explicitly decide when a lower-confidence
adapter deserves one licensed live trial. The trial would remain single-adapter,
revocable, resource-bounded, and evidence-producing.
