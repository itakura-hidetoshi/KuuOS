# KuuOS Authorized Atomic WORLD Commit v0.34

## Purpose

v0.34 connects the v0.33 `ADOPT_CANDIDATE` route to one externally authorized, optimistic-concurrency-checked, fenced and atomic WORLD-fragment commit.

```text
v0.33 ADOPT_CANDIDATE
→ external single-use commit authorization
→ exact commit request reconstruction
→ current WORLD-store compare
→ fencing / lease validation
→ one atomic store replacement
→ immutable commit receipt in append-only history
→ rollback reference requiring fresh authorization
```

This kernel commits a WORLD fragment pointer. It does not rewrite the constitutional root, erase prior WORLD history, declare truth or causality, activate PlanOS, invoke ActOS, complete a mission, or perform rollback automatically.

## Non-shrinking constitutional rule

The authorization is finite and single-use only at the local commit boundary.

```text
local commit authorization = finite
local commit count = one
```

The agent-level horizon remains open.

```text
global_cycle_limit = null
global_generation_limit = null
global_time_horizon_limit = null
open_horizon_preserved = true
```

Therefore:

```text
finite local authority != finite global agency
single-use commit != single-generation constitution
bounded effect != bounded future existence
```

v0.34 does not reintroduce a global cycle, generation, or duration cap.

## Official runtime entry

```text
runtime/kuuos_authorized_atomic_world_commit_entry_v0_34.py
```

Core runtime:

```text
runtime/kuuos_authorized_atomic_world_commit_v0_34.py
```

The official entry requires the effect-time caller to provide all three source artifacts:

1. the exact v0.33 `ADOPT_CANDIDATE` envelope;
2. the exact external commit-authorization envelope;
3. the exact authorized commit-request envelope.

The request is reconstructed from the first two artifacts at commit time. A mismatched or fabricated request cannot write the WORLD store.

## Commit authorization receipt

The external authorization binds:

- source disposition digest;
- verification receipt digest;
- feedback, evidence, report and state digests;
- constitutional root-lineage digest;
- prior, proposed and candidate WORLD-fragment digests;
- mission, observation and unresolved-item identities;
- WORLD-store identity;
- expected current generation;
- successor target generation;
- expected prior commit-receipt digest;
- strictly fresh fencing token;
- lease epoch;
- commit scope;
- host license;
- finite not-before and expiry times;
- one allowed commit.

```text
max_commits = 1
single_use = true
grants_world_fragment_commit = true
```

The authorization explicitly does not grant:

```text
constitutional root rewrite
memory-history overwrite
truth authority
causal attribution
PlanOS activation
ActOS invocation
automatic rollback
mission completion
```

## Accepted source disposition

Only the exact v0.33 route below is accepted:

```text
verification verdict = PASSED
source feedback route = WORLD_UPDATE_CANDIDATE
disposition route = ADOPT_CANDIDATE
candidate fragment = proposed fragment
```

`REJECT_CANDIDATE`, `DEFER_CANDIDATE`, and `REOBSERVE_CANDIDATE` cannot receive a WORLD commit authorization.

## WORLD-store model

The reference store is one JSON envelope containing:

```text
store identity
constitutional root lineage
genesis WORLD fragment
current WORLD fragment pointer
generation
last commit-receipt digest
last fencing token
last lease epoch
append-only immutable commit-receipt history
```

The current pointer may advance, but prior receipts and fragments remain referenced by the history chain.

```text
current pointer update != history overwrite
new WORLD generation != constitutional root rewrite
```

Every receipt binds the previous fragment and previous receipt digest, producing two linked chains:

```text
fragment_0 → fragment_1 → fragment_2 → ...
receipt_0 → receipt_1 → receipt_2 → ...
```

## Atomicity

The store and its newly appended receipt are serialized into one replacement state. The runtime:

1. acquires an exclusive POSIX file lock;
2. validates the complete existing store and history;
3. checks exact optimistic-concurrency expectations;
4. writes a temporary file;
5. flushes and `fsync`s the temporary file;
6. atomically replaces the target using `os.replace`;
7. `fsync`s the parent directory;
8. reads and validates the persisted store.

Because the current state and receipt history are one file, there is no split state/ledger commit window.

The reference implementation is a single-host POSIX adapter. A distributed database or object-store adapter must preserve the same typed contract with transactional compare-and-swap and fencing semantics.

## Optimistic concurrency

A new commit succeeds only when all expected values equal the current store:

```text
world_store_id
root_lineage_digest
generation
last_commit_digest
current_world_fragment_digest
```

Any stale prior fragment, generation, or receipt digest is rejected rather than merged silently.

## Fencing and lease epoch

```text
request fencing token > store last fencing token
request lease epoch >= store last lease epoch
```

A stale supervisor cannot overwrite a newer writer even if it still holds an old request.

Fencing is local to the WORLD store and does not create general execution authority.

## Immutable commit receipt

A successful receipt records:

- exact request, authorization and source-disposition digests;
- full v0.29–v0.33 lineage references;
- previous and committed WORLD-fragment digests;
- generation before and after;
- previous receipt digest;
- fencing token and lease epoch;
- host license and scope;
- request and commit times;
- rollback-reference digest;
- atomicity and concurrency evidence flags.

It also fixes:

```text
world_commit_is_truth = false
world_commit_is_causal_attribution = false
constitutional_root_rewritten = false
memory_history_overwritten = false
automatic_rollback_performed = false
automatic_mission_completion = false
```

## Replay

An exact request replay returns the already committed immutable receipt and does not append another generation.

Exact replay remains available after authorization expiry for crash recovery and audit reconstruction. Expiry blocks new effects, not retrieval of an already committed result.

A distinct request using an already consumed authorization is rejected. A new authorization cannot commit the same disposition twice.

## Rollback boundary

Each receipt contains a digest of the complete pre-commit state reference:

```text
store identity
root lineage
generation before commit
previous WORLD fragment
previous receipt digest
```

This is a rollback reference, not a rollback command.

```text
rollback reference != rollback authorization
rollback != deletion of the original receipt
rollback != rewriting history
```

A future rollback kernel must require fresh external authorization, a new fencing token, optimistic-concurrency checks, and a new append-only compensating receipt.

## Formal boundary

Lean module:

```text
KUOS.OpenHorizon.AuthorizedAtomicWorldCommitKernelV0_34
```

Central theorem:

```text
authorized_atomic_world_commit_boundary
```

Supporting theorems explicitly separate:

- finite local authorization from the unbounded global horizon;
- atomic pointer advancement from history or root overwrite;
- rollback reference from automatic rollback or history deletion.

The formal theorem verifies the declared typed contract. It does not prove scientific truth, institutional authorization quality, distributed-database linearizability, physical storage durability, or operator competence.

## Honest classification

```text
externally authorized, optimistic-concurrency-checked,
fenced, single-host atomic WORLD-fragment commit kernel
with append-only immutable provenance and an unbounded global horizon
```
