# KuuOS Repository Reference Stability and Reachability Certificate v0.99

v0.99 verifies that the candidate commit confirmed by a valid v0.98 receipt remains retained by the same direct local branch after a bounded time interval.

The delayed branch tip may remain equal to the candidate commit or advance to a descendant commit.

A branch advance is accepted only when a bounded object-database-derived parent path connects the delayed tip back to the candidate commit.

## Required evidence

A committed certificate requires:

- a completely revalidated and committed v0.98 reference update receipt
- the exact repository identity and Git-directory fingerprint
- the exact direct local branch reference
- the exact candidate commit OID and transaction
- a delayed reference-store observation after the configured minimum interval
- a bounded commit reachability certificate observed at the same time
- a complete path whose first OID is the delayed branch tip and whose last OID is the candidate commit
- exact consecutive child-parent edges for the complete path
- an exact queried OID set
- object-database confirmation that every queried path object is a commit
- presence of both the delayed tip and the candidate commit
- a monotone reference observation sequence
- an authorized common observer

The path has child-to-parent orientation.

A one-node path proves that the candidate commit remains the exact branch tip.

A longer path proves that the branch has advanced while retaining the candidate commit as an ancestor.

## Observation boundary

The certificate uses the reference store and Git object database.

It rejects working-tree, reflog, and remote-reference observations as evidence sources.

The absence of an observed force update is an evidence condition, not a reconstruction of all historical reference operations.

The certificate proves bounded present-state retention and reachability.

It does not prove that no unobserved historical mutation ever occurred.

## Forbidden authority and effects

v0.99 grants no force-update, delete, or push authority.

The certificate performs no repository mutation.

The following remain false:

```text
force_update_authorized
reference_delete_authorized
push_authorized
reference_mutation_performed
object_database_write_performed
working_tree_write_performed
index_write_performed
reflog_write_performed
remote_reference_updated
push_performed
signing_performed
```

## Layer separation

The v0.98 receipt confirms the bounded reference update transaction.

The delayed observation records a later direct branch state.

The reachability certificate records a bounded commit graph path from that later tip to the candidate commit.

The v0.99 certificate verifies these artifacts but creates none of their effects.

## Validation

Focused validation:

```bash
python3 -m unittest -v tests.test_kuuos_repository_reference_stability_v0_99
```

Cumulative validation:

```bash
python3 runtime/kuuos_v099_check.py
```
