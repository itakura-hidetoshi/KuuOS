# KuuOS Active Gauge Intervention Loop v0.3

## Purpose

v0.3 closes the first active autonomy loop above the commitment gauge runtime.
It consumes the exact covariant action prepared by v0.2, routes it to a domain
adapter, observes the committed effect, constructs a curvature receipt, re-enters
the gauge runtime, and returns the next covariant action in the same invocation.

```text
covariant action
  -> domain intervention
  -> committed local effect
  -> curvature receipt
  -> gauge correction / parallel transport
  -> next covariant action
```

This module is not a recommendation-only bridge. With the initial local backend,
it performs actual local state, ledger, and outbox effects through the existing
`qi_local_execution_adapter_v0_2`.

## Inputs

The loop binds the exact current artifacts:

```text
kuuos_open_horizon_commitment_gauge_state_v0_2.json
kuuos_open_horizon_commitment_gauge_bundle_v0_2.json
kuuos_open_horizon_covariant_action_v0_2.json
```

The action digest, active action ID, active section ID, bundle digest, gauge state
digest, agent identity, adapter profile, and intervention plan must agree.

## Routing

The default covariant-to-domain mapping is:

| Covariant step | Initial local domain action |
|---|---|
| `covariant_advance` | `advance_tick` |
| `covariant_micro_intervention` | `observe` |
| `curvature_probe` | `observe` |
| `effect_integration_transport` | `advance_tick` |
| `scaled_parallel_transport` | `advance_tick` |
| `local_repair_gauge` | `observe` |
| `chart_transition` | `handover` |
| `curvature_reobservation` | `observe` |
| `section_extension` | `advance_tick` |
| `handover_or_redesign` | `handover` |

A plan may replace individual routes. The adapter profile declares which domain
actions the backend supports. The runtime context declares which actions are
available in the current environment.

## Actual effects

The initial backend uses:

```text
runtime/kuuos_runtime_daemon_qi_local_execution_adapter_v0_2.py
```

It can commit:

- runtime state transitions such as `advance_tick`;
- execution-ledger records;
- notification, ticket, handover, and observation outbox entries.

The backend is replaceable. v0.3 keeps the adapter profile as an explicit input so
a network, EHR, GitHub, or other domain implementation can later satisfy the same
curvature-receipt contract.

## Effect receipt

A successful adapter execution is converted into the exact v0.2 effect schema:

```text
source action digest
action ID
section ID
outcome
continuation signal
progress delta
observed benefit
observed harm
recoverability
confidence
result digest
```

The current deterministic local mapping uses the committed adapter evidence:

```text
advance_tick -> success / continue
observe      -> partial / reobserve
handover     -> partial / expand
notify       -> partial / continue
ticket       -> partial / continue
hold         -> blocked / reobserve
freeze       -> blocked / repair
```

This packet is written as:

```text
kuuos_active_gauge_effect_receipt_v0_3.json
```

## Immediate gauge re-entry

After the domain effect is committed, v0.3 constructs an exactly bound child plan
for `Open-Horizon Commitment Gauge v0.2` and calls it immediately.

The receipt therefore becomes curvature in the same invocation. v0.2 updates the
local section, connection potential, frame, curvature history, and holonomy trace,
then prepares the next covariant action.

The v0.3 success condition is:

```text
domain effect committed
and effect receipt written
and gauge re-entry applied
and next gauge state persisted
```

A next action may be ready immediately. A locally flat or temporarily empty field
is also a valid open-horizon result.

## Idempotency

Before intervention, v0.3 appends a pending ledger phase. On completion it appends
a committed phase. The source covariant action digest is consumed once.

Replaying the same intervention run returns the committed result without a second
domain effect. The underlying local adapter also uses the action digest as its
execution nonce, providing a second idempotency layer.

## Gauge formulation

The formal artifact models an effect receipt with intended and realized transports:

```text
F = realized * intended^-1
```

Under a local frame transformation `g`, both transports are conjugated and:

```text
F^g = g F g^-1
```

Thus the statement that an effect is flat is gauge invariant. The proof surface is:

```text
formal/KUOS/OpenHorizon/ActiveGaugeInterventionV0_3.lean
```

## Outputs

```text
kuuos_active_gauge_intervention_state_v0_3.json
kuuos_active_gauge_effect_receipt_v0_3.json
kuuos_active_gauge_intervention_receipt_v0_3.json
kuuos_active_gauge_intervention_ledger_v0_3.jsonl
kuuos_active_gauge_intervention_audit_v0_3.jsonl
```

The updated v0.2 gauge bundle, gauge state, and covariant action are also persisted.

## Next layer

The next layer is `Renewable Gauge Autonomy Supervisor v0.4`:

```text
wake event
  -> Telos generation when needed
  -> commitment gauge transport
  -> active intervention
  -> curvature assimilation
  -> renewed wake condition
```

It should supervise repeated finite invocations without fixing a global generation
or task horizon.
