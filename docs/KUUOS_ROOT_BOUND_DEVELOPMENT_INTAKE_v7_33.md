# KuuOS Root-Bound Development Intake v7.33

## Purpose

v7.32 produces a fresh development-lineage root from current main.

v7.33 binds the next concrete task to that root.

```text
fresh lineage root
+ task intent
+ task scope
+ current-main freshness
-> minimum required MCP fact planes
```

This stage is intake and routing only.

It does not edit files, commit, publish, merge, or issue write authority.

## Mutation intent is preserved

A task may explicitly request a future mutation.

v7.33 does not treat that as an error and does not erase the request.

Instead it records:

```text
mutation_requested = true
write_authority_granted = false
```

and returns:

```text
root_bound_task_intake_ready_future_mutation_authority_required
```

Thus request is neither authority nor prohibition.

## Exact root binding

The intake request must bind:

- the exact v7.32 packet digest;
- the lineage root ID;
- the root main SHA;
- an intent digest;
- a scope digest;
- task ID and task kind;
- bounded repository-relative target paths.

A task cannot silently migrate to another root.

## Current-main freshness

The request also contains a fresh current-main observation.

If current main moved after the v7.32 root was formed:

```text
root_main_reobservation_required
```

The task is retained but must return through v7.32 so that the task is attached to current repository reality.

## Reuse v7.24 task-aware routing

v7.33 does not invent another MCP selector.

It reuses `KuuOS Development MCP Capability Routing v7.24` in route-preview mode.

Important:

```text
routing request_write = false
```

even when mutation was requested.

This lets v7.33 discover the fact planes needed for the task without causing the routing layer to imply that write authority exists.

For example a Lean CI repair normally requires:

```text
GitHub MCP      -> remote CI
Filesystem MCP  -> working bytes
Lean-LSP MCP    -> Lean semantics
Git MCP         -> local diff/revision
```

Context7 or MCP Docs are added only when the task says they are needed.

## Missing MCP capability

If a required plane is temporarily unavailable, the task is retained as:

```text
root_bound_task_intake_route_degraded
```

with PARTIAL status.

The system does not discard the task simply because one provider is unavailable.

## Local reconciliation

v7.32 may form a valid remote root even while local Git is stale.

For a task that actually needs local Git/Filesystem/Lean planes, v7.33 records:

```text
root_bound_task_intake_ready_local_reconciliation_required
```

For a remote-only task, the same stale local state does not pollute the intake.

## Authority non-carryover

The predecessor closure and re-root receipts are provenance.

They are not reusable licenses.

v7.33 rejects any request that claims predecessor authority should carry into the new task.

Every later mutation must acquire fresh task-specific authority.

## Validation

Focused tests verify:

1. a Lean mutation intent is accepted while future authority remains required;
2. a read-only remote observation task is immediately intake-ready;
3. a moved main requests re-rooting rather than stale execution;
4. local reconciliation keeps a local task alive;
5. local reconciliation does not contaminate remote-only intake;
6. a missing required MCP plane degrades routing without losing the task;
7. wrong root binding is obstructed;
8. predecessor authority reuse is obstructed;
9. repository path escape is obstructed;
10. nonready v7.32 source is not applicable;
11. task binding identity changes with task identity.

> **A new development lineage starts by binding intent to freshly observed reality; capability selection may follow, but authority must be earned again.**
