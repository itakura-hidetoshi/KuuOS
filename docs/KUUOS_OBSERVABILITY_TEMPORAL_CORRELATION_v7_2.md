# KuuOS Observability Temporal Correlation v7.2

## Purpose

v7.2 adds the first cross-provider comparison layer above the v7.1 Observability MCP Multiplexer.

The layer answers one narrow question:

> Were two provider-normalized observations temporally compatible within a bounded tolerance?

It explicitly does **not** answer:

> Did one event cause the other?

The invariant is therefore:

```text
temporal compatibility != causation
```

## Input model

v7.2 consumes already-normalized observation envelopes. It does not require raw GitHub, Vercel, Supabase, Neon, or future provider payloads.

Each observation contributes only bounded metadata such as:

- observation ID;
- provider;
- operation/data class;
- source digest;
- source status;
- first timestamp hint;
- last timestamp hint.

The timestamps may come from v7.1 `shape_summary.first_timestamp_hint` and `last_timestamp_hint`, or from a specialized observer that exposes equivalent bounded metadata.

Timestamps must either contain an explicit timezone or be Unix epoch seconds. Naive local timestamps are treated as insufficient metadata rather than silently assigned a timezone.

## Pairwise relation

For closed windows

```text
A = [a0, a1]
B = [b0, b1]
```

v7.2 computes one of five relations.

### overlap

```text
a0 <= b1 and b0 <= a1
```

The windows overlap.

### within_tolerance

The windows do not overlap, but the gap is no greater than the configured tolerance.

For example, with a five-second tolerance:

```text
A ends 11:00:10
B begins 11:00:14
gap = 4 s
=> within_tolerance
```

### disjoint

The windows are separated by more than the configured tolerance.

This is a statement about the observed time intervals only.

### insufficient_time_metadata

At least one source lacks enough time information for comparison.

This state is not converted to `disjoint`. Absence of a timestamp is absence of evidence, not evidence of temporal separation.

### source_obstruction

At least one observation reports a provider-local transient or unavailable state.

Examples include:

- GitHub log blob not yet materialized;
- provider rate limiting;
- provider 5xx;
- Datadog unavailable because connection/region compatibility is absent;
- Neon telemetry unavailable.

This does not become a negative correlation result.

## Causal boundary

Every emitted pair includes:

```text
causal_claim = not_inferred
causal_claim_permitted = false
```

The output packet also fixes:

```text
temporal_compatibility_is_not_causation = true
causal_inference_performed = false
source_authority_transferred = false
raw_provider_payloads_present = false
```

This distinction matters because two logs can be close in time for many reasons:

- shared upstream event;
- independent reactions to a third event;
- clock skew;
- batching;
- retry behavior;
- coincidence.

v7.2 intentionally preserves all of these presentations.

## Status semantics

`KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_READY`

All pairs have current, comparable time windows. Some pairs may still be disjoint.

`KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_PARTIAL`

At least one pair has insufficient time metadata or a provider-local obstruction. The packet remains useful for the pairs that were comparable.

`KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_BLOCKED`

A structural invariant failed, for example:

- authority mismatch;
- invalid plan;
- fewer than two observations;
- too many observations;
- duplicate observation IDs;
- invalid source digest;
- reversed time window;
- tolerance outside bounds.

## Relation to v7.0 and v7.1

```text
GitHub exact-head bounded live log v7.0
                    \
                     \
Vercel --------------+--> provider normalization v7.1
Supabase -------------+                 |
Neon -----------------+                 v
Datadog(optional) ----/       temporal correlation v7.2
                                      |
                                      v
                           compatibility graph only
                           no causal inference
```

v7.0 remains the stronger GitHub-specific temporal observer.

v7.1 supplies provider-local normalization and obstruction semantics.

v7.2 compares the bounded temporal projections of those observations without flattening provider provenance.

## Validation cases

The focused checker covers:

1. overlap plus clearly disjoint observations;
2. near-disjoint windows inside tolerance;
3. missing time metadata producing PARTIAL rather than a false negative;
4. transient source obstruction producing PARTIAL;
5. reversed windows fail closed;
6. timezone-naive timestamps remain insufficient rather than receiving an invented timezone.

This is a runtime-only extension. Lean theorem artifacts are not modified, so the focused validation does not invoke Strict Lean.

## Next descent

The next layer can add event-alignment evidence while retaining the same causal boundary.

Candidate evidence includes:

- shared exact commit SHA;
- deployment ID;
- request ID;
- trace ID;
- workflow run ID;
- explicit user-supplied correlation ID.

Those identifiers can strengthen **identity or shared-context evidence**, but even then the system should not assert causal direction without an independently justified causal model.
