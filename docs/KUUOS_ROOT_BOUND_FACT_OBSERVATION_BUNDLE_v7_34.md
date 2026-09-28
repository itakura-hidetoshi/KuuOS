# KuuOS Root-Bound Fact Observation Bundle v7.34

## Purpose

v7.33 binds a new task to a fresh development-lineage root and selects the MCP fact planes needed for that task.

v7.34 materializes those planes as one root/task-bound observation bundle.

```text
root-bound task
+ selected fact planes
+ fresh provider observations
-> root-bound fact bundle
```

The bundle is evidence, not authority and not execution.

## Exact task and root binding

Every observation bundle binds:

- the exact v7.33 packet digest;
- task ID;
- lineage root ID;
- lineage root main SHA;
- v7.33 task-binding digest;
- task scope digest;
- a fresh current-main observation.

If main moved after task intake, v7.34 does not reinterpret the task against the new head.

It returns:

```text
root_bound_fact_bundle_root_reobservation_required
```

and routes back through v7.32/v7.33.

## Missing observations are partial, not task rejection

If a selected fact plane has not yet been observed, the bundle is:

```text
root_bound_fact_bundle_missing_observations
```

The task candidate is retained.

This also lets a v7.33 `route_degraded` task recover later when a missing MCP provider comes back.

## Stale observations

A stale provider observation may be retained for provenance when it is explicitly marked non-fresh.

It does not satisfy the selected fact plane.

If an observation claims to be fresh while its bound head differs from the task root, the evidence contradicts itself and becomes a binding obstruction.

Thus:

```text
stale + declared stale -> partial
wrong head + declared fresh -> obstruction
```

## Filesystem and Lean semantic coherence

For a Lean task, current semantics must describe current bytes.

v7.34 requires:

```text
Filesystem content digest
=
Lean-LSP semantic source-content digest
```

for every covered target.

If they differ:

```text
root_bound_fact_bundle_semantic_reobservation_required
```

The current filesystem bytes are preserved; Lean is simply re-observed on those bytes.

## Selected planes only

An observation from a plane not selected by v7.33 is not silently injected into the task bundle.

This prevents an unrelated provider from changing the task's evidentiary surface after intake.

## No raw provider payload persistence

v7.34 stores bounded digests and typed observation metadata.

It requires:

```text
raw_payload_persisted = false
source_authority_transferred = false
```

for provider observations.

## No mutation or authority

Even a complete bundle has:

```text
observation_bundle_executes_mutation = false
observation_bundle_grants_write_authority = false
observation_bundle_grants_merge_authority = false
```

The bundle only establishes that the task has the required fresh evidence.

## Validation

Focused tests verify:

1. a complete Lean fact bundle is READY;
2. a missing selected plane is PARTIAL and retains the task;
3. explicitly stale provider evidence remains partial;
4. claimed-fresh wrong-head evidence is obstructed;
5. Lean/Filesystem digest mismatch requests semantic re-observation;
6. current-main movement returns to re-rooting;
7. wrong task binding is obstructed;
8. unselected fact-plane injection is obstructed;
9. raw provider payload persistence is obstructed;
10. a route-degraded v7.33 intake can become complete after provider recovery;
11. a nonapplicable intake remains nonapplicable.

> **Fresh evidence is conditioned by the root, task, provider plane, and current bytes; incompleteness is recoverable, but contradictory bindings are not silently collapsed.**
