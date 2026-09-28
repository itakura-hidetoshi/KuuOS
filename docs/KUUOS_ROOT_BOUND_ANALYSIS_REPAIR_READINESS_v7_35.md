# KuuOS Root-Bound Analysis / Repair Readiness v7.35

## Purpose

v7.34 establishes a complete, fresh fact bundle for one exact root-bound task.

v7.35 asks a narrower question:

> What can be done next with those facts, and does the bound task actually require an effect?

The layer does not execute anything.

```text
v7.33 intake
+
v7.34 complete fact bundle
->
task-specific readiness
```

## Exact re-binding

v7.35 consumes both the original v7.33 intake packet and the v7.34 bundle.

It requires the bundle's:

```text
source_intake_packet_digest
task_binding_digest
scope_digest
task/root/target/fact-plane bindings
```

to match the original intake exactly.

This prevents a complete bundle from being reused for another task or scope.

## Analysis does not need mutation authority

If:

```text
mutation_requested = false
```

and facts are complete, the task becomes:

```text
root_bound_task_analysis_ready
```

No write authority is requested.

For a Lean repair task this still permits a bounded repair plan to be derived from current diagnostics without editing yet.

## Repair readiness is not edit authority

For a bound Lean repair with:

```text
mutation_requested = true
```

and a complete coherent fact bundle, v7.35 derives:

```text
effect_class = workspace_source_edit
requested_authority_class = workspace_write_authority
root_bound_task_repair_ready_authority_pending
```

But it keeps:

```text
mutation_executed = false
write_authority_granted = false
merge_authority_granted = false
```

Thus repair readiness identifies the next authority class without manufacturing that authority.

## Mutation intent alone is insufficient

Some task kinds are explicitly analytical:

```text
external_library_docs
mcp_spec_research
```

If such a task arrives with `mutation_requested = true`, v7.35 does not guess an effect surface and does not request a broad authority.

It returns:

```text
root_bound_task_reclassification_required
```

while retaining the analysis result.

This is not rejection. It means the requested effect must be represented by a task kind whose effect surface is explicit.

## Effect classes

For task kinds that have a defined effect surface, v7.35 derives only the authority class needed for that surface.

Examples:

```text
lean_ci_repair
-> workspace_write_authority

remote_repository_observation + mutation intent
-> github_write_authority

browser_debugging + mutation intent
-> browser_effect_authority

database_debugging + mutation intent
-> database_provider_write_authority
```

The next layer must still bind the concrete provider/scope/target and validate a fresh authority receipt.

## Incomplete evidence

A partial/stale v7.34 bundle remains:

```text
root_bound_task_fact_reobservation_required
```

The task is retained and no authority request is generated.

This prevents authority acquisition from racing ahead of missing facts.

## Lean semantic coherence

When the task uses both working bytes and Lean semantics:

```text
Filesystem content digest
=
Lean-LSP source-content digest
```

must already hold in v7.34.

If not, v7.35 returns to semantic re-observation rather than requesting edit authority against stale semantics.

## Validation

Focused tests verify:

1. complete Lean repair facts derive workspace authority class but grant no authority;
2. Lean analysis-only mode requires no authority;
3. analysis-only task kinds with mutation intent are reclassified, not over-authorized;
4. remote repository effects derive GitHub authority only;
5. incomplete fact bundles remain partial and retain the task;
6. Lean/Filesystem incoherence prevents authority request;
7. wrong intake/bundle binding is obstructed;
8. bundle-carried write/merge authority is rejected;
9. database effects derive provider-specific authority class.

> **Fresh facts determine what is knowable; task semantics determine what effect is relevant; only then may a fresh authority class be requested.**
