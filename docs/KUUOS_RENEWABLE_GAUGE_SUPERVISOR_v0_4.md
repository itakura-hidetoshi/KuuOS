# KuuOS Renewable Gauge Supervisor v0.4

## Purpose

v0.4 supervises one finite open-horizon cycle per invocation.

```text
wake event
  -> decide whether Telos renewal is required
  -> synchronize the commitment gauge bundle
  -> perform at most one local intervention
  -> assimilate the effect as curvature
  -> persist one explicit next-wake packet
```

The runtime does not run an internal endless loop. Continuation is represented by
an explicit, digest-bound wake packet. A later invocation consumes that packet or a
new contextual event.

## Upstream layers

```text
v0.1 Open-Horizon Telos Genesis
v0.2 Open-Horizon Commitment Gauge
v0.3 Active Gauge Intervention Loop
v0.4 Renewable Gauge Supervisor
```

v0.4 composes the three lower layers without replacing their ledgers, digests, or
replay protections.

## Wake events

Supported wake kinds are:

```text
bootstrap
observation
timer
effect_followup
resource_change
relationship_change
recovery
manual
```

A wake packet binds:

- wake event identity and kind;
- world, process-tensor, and non-Markov context digests;
- optional signals for Telos renewal;
- whether renewal is requested;
- whether one local intervention is requested.

Bootstrap, observation, resource, relationship, and recovery events request Telos
renewal by default. Renewal can also occur when the configured local-step window is
reached.

## One finite cycle

Each invocation admits:

```text
at most one Telos generation
at most one gauge synchronization
at most one local domain intervention
exactly one next-wake decision
```

The state records:

```text
local_intervention_limit = 1
one_finite_cycle_completed = true
```

This keeps every invocation finite and replayable.

## Telos renewal

When renewal is required, the wake packet is converted into the exact v0.1
observation schema. A child Telos plan binds:

- the protected root-principles digest;
- the derived observation digest;
- the previous Telos state digest;
- a deterministic child run ID.

The resulting generation is contiguous. If a pending supervisor cycle is resumed
after Telos generation already completed, v0.4 recognizes the matching observation
digest and continues without generating the same Telos state twice.

## Gauge synchronization

After renewal, v0.4 compares the newest Telos state digest with the digest last
integrated by v0.2.

If they differ, the new local sections are admitted to the existing gauge bundle.
The bundle is extended, not replaced. An outstanding covariant action remains
byte-stable while unrelated sections are added.

## Local intervention

When the wake packet requests intervention and a covariant action is ready, v0.4
constructs an exactly bound v0.3 child plan.

The initial backend remains the local execution adapter. Therefore the supervisor
can commit local runtime-state, ledger, and outbox effects, but does not add direct
external-network authority.

The resulting effect receipt re-enters the same v0.2 gauge field as curvature.
Holonomy therefore continues across supervisor cycles.

## Explicit continuation

At the end of every successful cycle, v0.4 writes:

```text
kuuos_renewable_gauge_next_wake_v0_4.json
```

When another covariant action is ready:

```text
wake_kind = effect_followup
intervention_requested = true
telos_renewal_requested = false
```

When no action is ready:

```text
wake_kind = observation
intervention_requested = false
telos_renewal_requested = true
```

The second state waits for new context rather than declaring the mission globally
complete.

## Recovery and replay

The supervisor ledger contains pending and committed phases.

- the same committed supervisor run returns its prior result;
- the same wake digest cannot be consumed by a different run;
- a pending run may resume deterministic child run IDs;
- lower-layer replay protections remain active;
- v0.3 curvature receipts are stable across local-adapter replay.

The v0.3 recovery fix removes invocation-replay metadata from the physical effect
receipt and keeps effect confidence stable. Thus one committed local effect maps to
one reproducible curvature digest.

## Outputs

```text
kuuos_renewable_gauge_supervisor_state_v0_4.json
kuuos_renewable_gauge_next_wake_v0_4.json
kuuos_renewable_gauge_supervisor_receipt_v0_4.json
kuuos_renewable_gauge_supervisor_ledger_v0_4.jsonl
kuuos_renewable_gauge_supervisor_audit_v0_4.jsonl
```

The normal v0.1, v0.2, and v0.3 artifacts are also updated during the cycle.

## Formal surface

`formal/KUOS/OpenHorizon/RenewableGaugeSupervisorV0_4.lean` proves two complementary
properties:

1. each local invocation contains at most one intervention;
2. repeated renewal can pass every finite bound on the generation index.

The second property is expressed by:

```lean
theorem arbitrarily_many_renewals (s : SupervisorState) (bound : ℕ) :
    ∃ n : ℕ, bound < (Function.iterate renew n s).generation
```

This distinguishes renewable continuation from an endless computation inside one
runtime call.

## Next layer

The next layer can add `Event Source and Adapter Federation v0.5`:

```text
multiple local event sources
  -> normalized wake packet
  -> one v0.4 cycle
  -> adapter-specific effect evidence
  -> shared gauge curvature
```

External adapters should remain separately licensed and should not inherit local
execution authority merely by joining the federation.
