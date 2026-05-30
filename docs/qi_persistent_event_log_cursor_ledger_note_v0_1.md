# Qi Persistent Event Log / Replay Cursor / Token Ledger Note v0.1

This note documents the persistent ledger layer after the bounded Qi Process Tensor Daemon tick.

The ledger layer is not an external database yet. It defines the packet shape and safety invariants needed before wiring a real storage backend.

## Position

```text
Qi Persistent Process Tensor Daemon tick
  -> append-only event log
  -> monotone replay cursor
  -> one-shot token ledger
```

## Purpose

The persistent tick can emit a closed-loop heartbeat, but an autonomous OS also needs durable continuity:

- which tick was already processed
- which MemoryOS stream position has already been replayed
- which one-shot authority token has already been consumed
- which idempotency key prevents duplicate event append

## Boundaries

Allowed:

- append-only event append
- monotone replay cursor advance
- one-shot token consumption record
- idempotency check

Still forbidden:

- MemoryOS overwrite
- MemoryOS append by this ledger layer
- world update
- control packet mutation
- probe execution
- granting probe execution authority

## Required invariants

- event log is append-only
- replay cursor is monotone
- idempotency key is unique
- consumed token cannot be consumed again
- ledger update does not execute probes
- ledger update does not mutate world or control packets

## Next layer

The next layer should wire this packet-level ledger into a real backend such as JSONL, SQLite WAL, or object-lock storage, while preserving the same invariants.
