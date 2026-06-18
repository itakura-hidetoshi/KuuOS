# KuuOS Cooperative Host Adapter v0.17

## Purpose

Cooperative Host Adapter v0.17 connects the resumable job and lease protocol from v0.16 to a real bounded host invocation.

The adapter does not introduce a second scheduler and does not call external connectors from inside the runtime. It projects eligible supervisor work into a digest-bound host packet. A trusted host may then claim exactly one eligible job, execute one bounded slice through the v0.16 allowlisted registry, persist the resulting bundle, and emit an append-only receipt.

## Runtime position

```text
existing bounded runtime daemon / GitHub Actions / trusted worker host
  -> v0.17 Cooperative Host Adapter
       -> work projection packet
       -> explicit host license
       -> one worker lease
       -> one bounded v0.16 slice
       -> atomic bundle output
       -> receipt and audit append
  -> v0.16 Cooperative Execution Supervisor
  -> v0.15 Resumable Execution Handoff
  -> v0.14 Context Gerbe Coherence
```

v0.17 is an adapter. It does not replace the existing runtime daemon, tick scheduler, reentry gate, or external bridge.

## Two-phase boundary

### Phase A: work projection

Projection is read-only. It examines a supervisor bundle and produces a packet containing:

- source bundle digest
- eligible and blocked candidate summaries
- deterministically selected job
- selected ticket, checkpoint, step, and operation digests
- boundary flags

Projection does not claim a lease, execute an operation, write a bundle, or call a connector.

### Phase B: host tick

A trusted host may consume the projection only when an explicit license is valid. One invocation may:

1. verify the projection against the current bundle
2. claim or reclaim the selected ticket
3. derive effective step and cost bounds from the license and supervisor policy
4. run one v0.16 background slice through a trusted allowlisted registry
5. commit the slice and close the consumed lease
6. preserve a replacement queued ticket when work remains
7. persist the result bundle and emit a receipt

The adapter never loops recursively. A new invocation is required for every subsequent slice.

## Eligibility

A job is eligible when all of the following hold:

- state is `background_queued`, or a `background_leased` ticket is expired
- active ticket digest is valid
- ticket job identity matches the job
- ticket checkpoint matches the job's latest checkpoint
- a next step exists
- the next operation is present in the host operation allowlist
- the job is not terminal

Invalid candidates remain visible with blocker reasons.

## Deterministic selection

Eligible candidates are ordered deterministically:

1. queued tickets
2. expired leased tickets
3. job identifier
4. ticket identifier

The projection selects at most one candidate. This is scheduling projection only and grants no execution authority.

## Host license

The license is digest-bound and explicitly controls:

- bundle read
- projection consumption
- ticket claim
- bounded slice execution
- bundle output write
- receipt write
- audit append
- maximum steps per slice
- maximum cost per slice
- lease duration
- operation allowlist

A missing, invalid, expired, or insufficient license blocks execution before lease claim.

## Persistence

The file adapter uses atomic JSON replacement for output packets and bundles. It appends receipts to JSONL audit history.

By default the input bundle is not overwritten. The caller supplies a distinct output bundle path. In-place replacement requires an explicit license field.

## Idempotency

Every host invocation is bound to:

- invocation identifier
- source supervisor bundle digest
- projection digest
- worker identifier

The result bundle records processed host invocation digests. Replaying the same invocation returns the stored outcome without running another step, consuming budget again, or producing another lease.

## Authority boundary

The adapter preserves these boundaries:

- no connector call from inside runtime
- no arbitrary source or shell execution
- only trusted registry operations may execute
- queue projection grants no authority
- at most one job is claimed per invocation
- every host invocation runs at most one bounded slice
- every later slice requires a new host invocation
- lower licenses and hard gates remain binding
- no truth, theorem, clinical, memory-overwrite, or final-commitment authority is granted
- graph semantics remain forbidden

## Acceptance cases

1. Projection selects one valid queued job without mutating the bundle.
2. A valid license claims the selected job and runs one bounded slice.
3. An unfinished slice returns the job to `background_queued` with a replacement ticket.
4. A later invocation completes the job.
5. An expired lease may be reclaimed by another worker.
6. Invalid ticket, checkpoint mismatch, or non-allowlisted operation remains visible and is not executed.
7. Missing license permission blocks before claim.
8. Duplicate invocation digest is replayed without duplicate work.
9. Output bundle, receipt, and audit files are written atomically or append-only as appropriate.
10. Existing v0.16 and lower semantics remain unchanged.
