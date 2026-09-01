# KuuOS OpenClaw audit cross-process serialization v0.6

## Purpose

v0.5 serialized only reconciliation calls owned by one supervisor process.  An independently started audit intake could still race the supervisor against the same `audit-observation-candidates.jsonl` and `audit-ingest-checkpoints.json` state.

v0.6 moves the serialization boundary into the stable v0.3 audit-intake public entrypoint itself.

```text
supervisor v0.5 --------\
manual v0.3 CLI ---------+--> data-dir OS lock --> retained v0.3 implementation
cron / second process ---/
```

The original v0.3 implementation is retained byte-for-byte as:

`runtime/kuuos_openclaw_audit_observation_ingest_v0_3_impl.py`

The stable existing path:

`runtime/kuuos_openclaw_audit_observation_ingest_v0_3.py`

is now the serialization wrapper, so existing callers do not need a new command.

## Lock identity

The lock is scoped by the exact KuuOS OpenClaw data directory and uses:

`audit-ingest-state.lock`

Every public `sync` and `status` operation acquires the same exclusive lock before reading or writing the observation ledger/checkpoint pair.

This is intentionally stronger than the v0.5 thread lock:

```text
v0.5 thread lock = one supervisor process
v0.6 OS lock     = cooperating audit-intake processes sharing one data-dir
```

## Kernel ownership and crash release

The lock file is persistent, but **lock ownership is not encoded by file existence**.

On POSIX, v0.6 uses `fcntl.flock(LOCK_EX | LOCK_NB)`.

On Windows, v0.6 uses one-byte `msvcrt.locking(LK_NBLCK, 1)`.

The open kernel handle owns the advisory lock. Closing the handle or terminating the process releases ownership. Therefore a crashed process does not leave a logical stale-lock claim merely because `audit-ingest-state.lock` remains on disk.

The lock file is created private (`0600`) on POSIX.

## Fail-closed timeout

Lock acquisition is bounded. The default is 30000 ms and can be changed with:

`KUUOS_OPENCLAW_AUDIT_LOCK_TIMEOUT_MS`

The accepted range is 1..600000 ms. Invalid configuration or timeout returns the existing audit-intake error path instead of running without serialization.

```text
lock unavailable != permission to bypass serialization
```

## Compatibility

The public v0.3 module continues to expose the established projection/checkpoint API used by existing tests and tooling. The retained implementation still owns the v0.3 wire/query semantics; v0.6 changes only concurrency ownership around state-touching operations.

The supervisor continues to invoke the same v0.3 filename and therefore inherits cross-process serialization automatically.

## Scope

This is a cooperating-process guarantee. A program that ignores the KuuOS public audit-intake module and directly mutates ledger/checkpoint files can still violate the protocol. v0.6 does not claim filesystem mandatory locking.

Likewise, serialization does not turn OpenClaw audit activity into a lossless source. The source remains metadata-only, best-effort, and bounded-retention.

## Authority boundary

```text
exclusive lock != ObserveOS commit
exclusive lock != verification
exclusive lock != WORLD truth
exclusive lock != PlanOS completion
exclusive lock != rollback proof
lock acquisition failure != rollback proof
```

The lock creates no effect permission and no memory overwrite authority. It only prevents cooperating KuuOS audit-intake processes from concurrently mutating one local observation/checkpoint state.

## Validation

The focused test launches a second Python process holding the data-dir lock, proves another process times out instead of entering, terminates the holder, and proves kernel ownership is released. It also checks independent data directories do not block each other and POSIX lock-file permissions are private.

CI on Ubuntu exercises the POSIX `fcntl.flock` path. The Windows `msvcrt.locking` branch is structurally validated in the implementation but is not claimed to have been exercised by that Ubuntu job.
