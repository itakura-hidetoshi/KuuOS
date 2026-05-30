# Qi Persistent Process Tensor Daemon Note v0.1

This note documents the first persistent runtime surface for the Qi Process Tensor Daemon.

The daemon tick lifts the v0.2 closed-loop from CI-only validation into a bounded persistent runtime tick. It emits a heartbeat and performs one closed-loop scheduler update using MemoryOS process-tensor replay.

## Tick path

```text
append-only MemoryOS process-tensor entries
  -> MemoryOS retrieval/replay
  -> scheduler replay-hint apply
  -> probe scheduler proposal reuse
  -> process-tensor-aware scheduler state v0.2
  -> persistent daemon heartbeat
```

## Boundary

Allowed in v0.1:

- bounded persistent tick
- heartbeat emission
- MemoryOS read
- scheduler state update with `replay_hint_only`
- process tensor pressure classification

Still forbidden:

- probe execution
- MemoryOS write or append
- MemoryOS overwrite or delete
- world update
- control packet mutation
- granting probe execution authority

## Process tensor signals

The daemon tick reports:

- `history_depth`
- `observation_debt_resolution_priority`
- `safe_reentry_window_score`
- `nonmarkov_link_density`
- `memory_kernel_preservation_score`
- `process_tensor_pressure`

## Next layer

The next persistent OS layer should add:

- event log
- replay cursor
- one-shot token ledger
- idempotency key
- safe resume marker
