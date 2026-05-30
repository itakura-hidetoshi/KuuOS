# Qi JSONL Ledger Backend Adapter Note v0.1

This note documents the first real backend adapter for the Qi Persistent Process Tensor Daemon ledger.

The adapter writes one append-only event per line to a JSONL file and keeps replay cursor plus token ledger state in a JSON sidecar file.

## Position

```text
packet-level persistent event log / replay cursor / token ledger
  -> JSONL event log backend
  -> JSON sidecar ledger state
```

## Files

- `event_log.jsonl`: append-only event stream
- `ledger_state.json`: replay cursor and token ledger sidecar

## Safety boundary

Allowed:

- append one event line
- write sidecar cursor/token state
- enforce idempotency key uniqueness
- block token double consumption
- preserve monotone replay cursor

Still forbidden:

- MemoryOS overwrite
- world update
- control packet mutation
- probe execution
- granting probe execution authority

## Why JSONL first

JSONL gives the minimal durable append-only surface before introducing SQLite WAL or object-lock/WORM storage. It is easy to inspect, replay, diff, and migrate.

## Next layer

The next layer should add a daemon wrapper that uses this adapter as its state backend during repeated bounded ticks.
