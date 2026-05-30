# Qi JSONL Persistent Daemon Wrapper Note v0.1

This note documents the first repeated bounded-tick wrapper for the Qi Persistent Process Tensor Daemon using the JSONL ledger backend.

## Position

```text
JSONL ledger backend adapter
  -> repeated bounded persistent daemon wrapper
  -> future systemd/docker safe stop/resume surface
```

## What it does

The wrapper runs a bounded number of daemon ticks. For each tick it:

1. runs the Qi persistent process tensor daemon tick
2. emits a heartbeat
3. routes the tick into the JSONL ledger backend
4. appends one event line
5. advances the replay cursor
6. records a one-shot token id

## Safety boundary

Allowed:

- repeated bounded ticks
- JSONL append-only event writes
- JSON sidecar cursor/token updates
- idempotency enforcement
- duplicate tick blocking

Still forbidden:

- probe execution
- MemoryOS write/append/overwrite
- world update
- control packet mutation
- granting probe execution authority

## Operational meaning

This is the first surface where the Qi Process Tensor Daemon can run for more than one tick while preserving persistent continuity. Re-running an already processed tick is blocked by idempotency and token ledger state.

## Next layer

The next layer should provide a deployment wrapper, such as systemd or Docker, with safe stop/resume using the JSONL event log and sidecar ledger state.
