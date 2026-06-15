# KuuOS Event Source and Adapter Federation v0.5

## Purpose

v0.5 adds a federation layer above Renewable Gauge Supervisor v0.4.

```text
several event sources
  -> deterministic source normalization
  -> one digest-bound wake packet
  -> one explicitly selected local adapter
  -> one v0.4 supervisor cycle
  -> provenance-preserving effect evidence
  -> shared gauge field
```

The federation is a fan-in / single-selection layer. It does not grant every source
or every registered adapter the right to act during the same cycle.

## Upstream stack

```text
v0.1  Open-Horizon Telos Genesis
v0.2  Open-Horizon Commitment Gauge
v0.3  Active Gauge Intervention Loop
v0.4  Renewable Gauge Supervisor
v0.5  Event Source and Adapter Federation
```

v0.5 delegates exactly one bounded cycle to v0.4. All lower-layer replay,
curvature, holonomy, and next-wake artifacts remain authoritative.

## Federated source packets

Each source packet contains:

- source identity;
- source-local event identity;
- event kind;
- priority and trust weight;
- world, process-tensor, and non-Markov context digests;
- zero or more Telos signals;
- a Telos-renewal request;
- a local-intervention request;
- an exact packet digest.

Supported source kinds are:

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

A source event can be consumed only once. Reusing the same
`source_id :: source_event_id` in a later federation run is rejected.

## Deterministic normalization

Source order in the input list is not semantic. The normalizer sorts sources by:

1. descending source priority;
2. descending trust weight;
3. wake-kind precedence;
4. source ID;
5. source event ID.

The highest-ranked source determines the normalized wake kind. Renewal and
intervention requests are aggregated by logical OR.

Signals are namespaced:

```text
source_id:signal_id
```

The source trust weight scales only the signal's evidence field. It does not turn a
source weight into truth. Original source identity, packet digest, priority, and
trust remain attached as provenance.

World, process-tensor, and non-Markov contexts are each re-digested over the sorted
source lineage. Reversing the source input order therefore produces the same wake
digest.

## Adapter registry

A registry entry contains:

- federation adapter ID;
- enabled state;
- local priority;
- accepted source kinds;
- optional accepted source IDs;
- an embedded v0.3 adapter profile;
- an explicit denial of external-network effects.

The initial v0.5 registry accepts only the existing local execution backend:

```text
qi_local_execution_adapter_v0_2
```

Registration does not transfer authority. A source cannot acquire adapter rights,
and one adapter cannot inherit another adapter's permissions merely by sharing a
registry.

## Selection rule

An adapter is eligible when:

- it is enabled;
- it accepts the normalized dominant wake kind;
- its optional source-ID filter intersects the current source set;
- its embedded adapter profile and digest are valid.

Eligible adapters are ordered deterministically by:

1. source-ID affinity coverage;
2. source-kind coverage;
3. adapter priority;
4. supported local-action coverage;
5. federation adapter ID.

Exactly one adapter is selected for the delegated v0.4 cycle. If no adapter is
eligible, the federation cycle is blocked before local intervention.

## Shared gauge evidence

After v0.4 completes, v0.5 writes a federated evidence packet that binds:

- the source batch digest;
- every source provenance record;
- the normalized wake digest;
- the selected federation adapter;
- the selected v0.3 profile digest;
- the v0.4 supervisor receipt digest;
- the effect receipt digest;
- the resulting gauge-state digest;
- the next-wake digest.

The evidence explicitly records:

```text
source_authority_transferred = false
adapter_authority_inherited = false
external_network_effect_performed = false
shared_gauge_evidence = true
```

Thus several observations can contribute to one field update without collapsing
their origins or merging their permissions.

## Replay and recovery

The v0.5 ledger uses pending and committed phases.

- a committed federation run replays without another v0.4 cycle;
- a source event cannot be consumed twice;
- a source event claimed by another pending run is rejected;
- deterministic child supervisor run IDs allow pending recovery;
- v0.4 and lower-layer replay protections remain active.

## Outputs

```text
kuuos_federated_normalized_wake_v0_5.json
kuuos_federated_effect_evidence_v0_5.json
kuuos_event_adapter_federation_state_v0_5.json
kuuos_event_adapter_federation_receipt_v0_5.json
kuuos_event_adapter_federation_ledger_v0_5.jsonl
kuuos_event_adapter_federation_audit_v0_5.jsonl
```

Normal v0.1-v0.4 artifacts are updated by the delegated supervisor cycle.

## Formal surface

`formal/KUOS/OpenHorizon/EventAdapterFederationV0_5.lean` separates source
assimilation from adapter selection.

```lean
structure AdapterSelection where
  selectedAdapterCount : ℕ
  uniqueSelection : selectedAdapterCount ≤ 1
```

It proves that the selected adapter count is zero or one. It also defines a
federation-state transition that adds several source events while increasing the
adapter-selection count by one.

The iteration theorem is:

```lean
iterate_assimilate_sourceEvents
```

so repeated finite federation cycles preserve an explicit countable source
lineage.

## Next layer

A natural v0.6 is `Adapter Capability Gauge and Evidence Calibration`:

```text
adapter-specific effect history
  -> calibrated capability section
  -> context-dependent adapter connection
  -> selected adapter
  -> effect evidence
  -> capability curvature update
```

Selection would then depend not only on declared registry priority but also on
observed, recoverable, context-specific adapter performance.
