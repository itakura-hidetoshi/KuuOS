# KuuOS Observability Event Alignment v7.3

## Purpose

v7.3 sits above the v7.2 temporal correlation layer.

v7.2 can say that two observations overlap in time or lie within a bounded tolerance. v7.3 adds exact shared-context evidence such as an identical commit SHA, workflow run ID, deployment ID, request ID, trace ID, correlation ID, or artifact digest.

The central invariant remains:

```text
shared exact identifier != causal direction
```

An identifier can establish shared context or identity. It does not by itself prove that one observed event caused another.

## Inputs

v7.3 consumes two already-bounded inputs:

1. the v7.2 temporal correlation packet;
2. a separate identity-binding packet keyed by `observation_id`.

This means the runtime never needs raw provider logs.

The identity packet is cryptographically bound to the exact v7.2 packet with:

```text
source_temporal_packet_digest = SHA256(v7.2 packet)
```

A stale or crossed temporal packet is rejected.

## Allowed identifier types

The allowlist is intentionally small:

- `commit_sha`
- `workflow_run_id`
- `workflow_job_id`
- `deployment_id`
- `request_id`
- `trace_id`
- `correlation_id`
- `artifact_digest`

Commit SHA, artifact digest and numeric workflow identifiers receive additional shape validation.

Arbitrary identifier keys are rejected rather than silently admitted.

## Privacy boundary

Identifier values may themselves reveal infrastructure or request details.

Therefore the v7.3 output does not emit a matching identifier value.

For an exact match, it stores only:

```text
identifier_type
SHA256(identifier_type, identifier_value)
```

For example:

```text
commit_sha = <exact value>
        |
        v
shared_identifier_evidence = {
  identifier_type: commit_sha,
  value_digest: <sha256>
}
```

The exact commit SHA is used for equality testing but is not copied into the v7.3 packet.

## Two independent axes

v7.3 keeps temporal evidence and identity evidence separate.

For every pair it records:

```text
temporal_relation
temporally_compatible
has_shared_exact_identifier
shared_identifier_evidence
same_type_distinct_value_identifiers
```

It then derives one bounded alignment state.

### exact_context_temporally_compatible

At least one exact identifier is shared and the time windows are compatible.

This is the strongest shared-context presentation in v7.3, but still not a causal claim.

### exact_context_temporally_disjoint

An exact identifier matches, but the time windows are disjoint beyond tolerance.

This is preserved as an inconsistency worth investigation rather than forcing either source to be “wrong.” Possible explanations include clock skew, batching, delayed export, identifier reuse, or an incorrectly scoped observation.

### exact_context_time_unresolved

The exact identifier matches, but the time metadata is insufficient.

### temporal_only

The observations are temporally compatible but share no exact allowlisted identifier.

### no_alignment_evidence

The bounded metadata establishes neither temporal compatibility nor an exact shared identifier.

This does not prove that the real-world events are unrelated.

### source_obstruction

At least one source is transient or unavailable.

## Same identifier type, different value

Suppose two providers both have a `correlation_id`, but the values differ.

v7.3 records:

```text
same_type_distinct_value_identifiers = [correlation_id]
has_shared_exact_identifier = false
```

It does not automatically turn this into a negative causal conclusion. Identifier scope can differ by service, span, retry, batch, or gateway.

## Causal boundary

Every pair fixes:

```text
causal_claim = not_inferred
causal_direction = not_inferred
causal_claim_permitted = false
```

The packet-level boundary also fixes:

```text
shared_identifier_is_context_evidence_not_causation = true
temporal_compatibility_is_not_causation = true
causal_inference_performed = false
causal_direction_inferred = false
identifier_values_exposed = false
source_authority_transferred = false
```

## Descent

The observability chain is now:

```text
GitHub bounded live-log v7.0
          |
          v
provider multiplexer v7.1
          |
          v
temporal correlation v7.2
          |
          v
exact-context event alignment v7.3
```

Each layer adds structure without granting the next layer more authority than the evidence supports.

## Validation

The focused checker verifies:

1. exact shared commit SHA + compatible time window;
2. exact shared request ID + temporally disjoint window produces PARTIAL rather than a causal claim;
3. temporal-only evidence;
4. same identifier type with distinct values is not a false match;
5. stale temporal-packet digest is rejected;
6. malformed commit SHA is rejected;
7. exact identifier values do not appear in the emitted packet.

No Lean theorem files are modified, so Strict Lean is intentionally not invoked by the focused validation.

## Next step

The next useful structure is a provenance graph where nodes are bounded observations and edges contain only explicit evidence:

- temporal relation;
- exact shared identifier digest;
- source observation digest;
- provider provenance;
- obstruction state.

That graph should remain descriptive. Any later causal model must be an explicit additional layer with its own assumptions and proofs.
