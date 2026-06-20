# KuuOS Qi–WORLD Indra Transport Request v1.6

## Purpose

v1.6 connects the protected Qi–WORLD cross-cycle transition to the read-only WORLD v0.42 gauge-categorical Indra-net sidecar.

It does **not** realize a gauge transport. It creates a hash-bound request for external analytic receipts.

```text
v1.4 cross-cycle re-entry receipt
→ v1.5 blocker certificate
→ WORLD v0.42 Indra-net sidecar readiness
→ source/target patch binding
→ branch + non-Markov history binding
→ external analytic transport request
```

## Inputs

The builder consumes only existing canonical artifacts:

- `build_cross_cycle_blocker_receipt` from v1.5;
- the embedded v1.4 cross-cycle receipt;
- the previous and next read-only WORLD projection digests;
- the cross-cycle Qi process-lineage digest and process history;
- the WORLD v0.42 plan and fail-closed runtime result;
- the v1.5 blocker certificate digest.

## Patch and branch binding

The request derives:

```text
source_patch_id
  = hash(source WORLD projection digest, role=source)

target_patch_id
  = hash(target WORLD projection digest, role=target)

branch_id
  = hash(cross-cycle Qi lineage, next PlanOS state)

history_digest
  = hash(cross-cycle receipt, complete Qi process history)
```

The source and target patches must be distinct. The complete path is exactly:

```text
[source_patch_id, target_patch_id]
```

## WORLD v0.42 binding

The request builds and validates the official WORLD v0.42 plan using the actual SHA-256 digests of:

- `ModuleCategoryNimrepTubeCenterBridgeV0_41.lean`;
- `GaugeCategoricalIndraNetBridgeV0_42.lean`.

The v0.42 runtime must return:

```text
WORLD_GAUGE_CATEGORICAL_INDRA_NET_BRIDGE_V0_42_READY
```

with a nonempty bridge-state digest.

This means only that the read-only analytic sidecar contract is internally complete. It does not mean that a physical or continuum gauge connection exists or has been computed.

## Required external receipts

The generated request explicitly requires external evidence for:

- normal star-isomorphism realization;
- pseudofunctor realization;
- stack descent;
- branch transport;
- coherence two-cells;
- history-dependent gauge phase;
- continuum non-Markov connection.

Until those receipts are supplied, the disposition is:

```text
EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED
```

## Blocker integration

The request is emitted only when the v1.5 certificate confirms all bounded cross-cycle blockers:

- present activation blocker;
- execution-authority blocker;
- memory-overwrite blocker;
- WORLD-identity blocker;
- truth-authority blocker;
- same-cycle self-loop blocker;
- multi-WORLD-collapse blocker.

The request does not remove those blockers. It remains a representation-level candidate.

## Runtime rejection cases

The validator rejects:

- target WORLD projection substitution;
- source or target patch substitution;
- patch-path mutation;
- branch-ID substitution;
- Qi history-digest substitution;
- blocker receipt or certificate substitution;
- WORLD v0.42 plan/result substitution;
- a blocked v0.42 sidecar;
- claims that transport was realized;
- claims that a gauge connection was constructed;
- claims that physical holonomy was computed;
- exact-WORLD identity claims;
- WORLD updates, branch collapse, or history overwrite;
- loss of the request-only boundary.

## Non-authority boundary

```text
request_grants_execution = false
request_grants_truth = false
request_issues_authority = false
request_constructs_gauge_connection = false
request_computes_physical_holonomy = false
request_realizes_transport = false
request_updates_exact_world = false
request_collapses_world_branches = false
request_overwrites_history = false
```

## Interpretation

v1.6 provides a precise interface between:

```text
Qi process lineage
WORLD projection transition
Indra-net analytic representation
cross-cycle safety blockers
```

It prepares an external analytic transport question. It does not answer that question by fabrication, and it does not turn gauge equivalence of representations into identity of WORLD branches.
