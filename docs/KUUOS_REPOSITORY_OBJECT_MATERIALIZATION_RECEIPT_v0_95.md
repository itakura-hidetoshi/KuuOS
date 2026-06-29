# KuuOS Repository Object Materialization Receipt v0.95

v0.95 verifies the result of one bounded Git object-database materialization authorized by v0.94.

The layer certifies supplied execution evidence.

It does not itself invoke Git, write files, update an index, change a working tree, sign an object, or mutate a reference.

## Inputs

A receipt is reconstructed from the following evidence:

```text
valid v0.94 materialization authorization certificate
v0.94 authorization scope and pre-write object-database observation
v0.95 materialization policy
executor report
post-write object-database observation
nonce-consumption receipt
all upstream v0.92 and v0.93 evidence needed to revalidate v0.94
```

The v0.94 certificate is revalidated rather than accepted by digest alone.

## Exact execution plan

The executor report must contain exactly one item for every v0.94 plan item.

Each execution item binds:

```text
object kind
Git object identifier
payload size
SHA-256 payload digest
written or reused outcome
write order
```

The item set, item order, write set, reuse set, payload metadata, object count, and written payload byte total must all equal the v0.94 plan.

Objects marked `write_required` by v0.94 must be reported as written in the same dependency order.

Objects already present exactly must be reported as reused and must not receive a write order.

## Post-write observation

The post-write observation must come from the same repository identity, Git-directory fingerprint, object format, and source parent commit as the authorization.

It must query exactly the source parent commit and every candidate object identifier.

The post-write inventory must establish:

```text
source parent commit remains present and unchanged
every candidate blob is present with exact payload metadata
every candidate tree is present with exact payload metadata
candidate commit is present with exact payload metadata
objects designated for reuse remain unchanged
```

A missing object, altered payload digest, changed object kind, changed size, incomplete query set, or changed parent commit prevents a committed receipt.

## Commit presence and commit writing

The receipt distinguishes two propositions.

**Candidate commit present** means that the post-write object database contains the exact candidate commit object.

**Commit object written** means that the candidate commit was absent before the operation, was required by the v0.94 plan, and was reported as written in this operation.

If all candidate objects already existed exactly, the materialization may still commit as a verification-only reuse transition.

In that case:

```text
candidate_commit_present = true
commit_object_written = false
```

## Nonce transition

The nonce-consumption receipt must bind the same authorization certificate and authorization scope.

A committed materialization requires:

```text
consumed_before = false
consumed_after = true
revoked = false
materialization_committed = true
atomic_with_materialization = true
```

The nonce registry before and after digests must differ.

The execution report and nonce-consumption receipt must share one transaction identifier.

## Time boundary

The execution must start after scope issuance and complete no later than scope expiry.

The operation duration must remain within policy.

The post-write observation must occur after completion and within the permitted observation delay.

Therefore, an authorization that was valid when v0.94 evaluated it cannot be used after its scope expires.

## Atomic receipt status

The receipt status is `REPOSITORY_OBJECT_MATERIALIZATION_COMMITTED` only when every required invariant is true.

Any partial write report, missing post-write object, payload mismatch, nonce mismatch, stale observation, expired authorization, unauthorized executor, or forbidden side effect yields `REPOSITORY_OBJECT_MATERIALIZATION_ABORTED`.

An aborted receipt does not automatically prove failure without effects.

The separate `failure_no_effect` field is true only when no object-database write was attempted, the nonce remained unconsumed, and no forbidden effect occurred.

## Effect boundary

A committed receipt may certify object-database materialization and exact candidate commit presence.

It still requires the following values to remain false:

```text
index_write_performed
working_tree_write_performed
reference_mutated
signing_performed
```

The receipt does not grant or certify branch, tag, or `HEAD` mutation.

Reference mutation remains a distinct later authorization and execution domain.

## Security meaning

The receipt proves consistency of supplied receipts, reports, observations, and deterministic recomputation under the v0.95 contract.

It does not prove that an external Git implementation or filesystem reported honestly.

That external trust boundary is represented explicitly by the executor report and object-database observations.
