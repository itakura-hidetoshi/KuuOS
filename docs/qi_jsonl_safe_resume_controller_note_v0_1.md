# Qi JSONL Safe Resume Controller Note v0.1

This note documents the safe stop/resume surface for the Qi JSONL Persistent Daemon Wrapper.

## Position

```text
JSONL persistent daemon wrapper
  -> safe resume controller
  -> future systemd/docker deployment wrapper
```

## What it does

The controller reads:

- `event_log.jsonl`
- `ledger_state.json`

It detects already processed ticks by `tick_id`, skips them, and runs only the contiguous unprocessed suffix.

Example:

```text
processed: tick 1, tick 2
desired:   tick 1, tick 2, tick 3, tick 4
resume:    tick 3, tick 4 only
```

If all desired ticks are already processed, the controller performs a no-op resume.

## Safety boundary

Allowed:

- read JSONL event log
- read sidecar ledger state
- skip processed ticks
- run unprocessed suffix through the JSONL wrapper
- no-op resume when all ticks are complete

Still forbidden:

- probe execution
- MemoryOS write/append/overwrite
- world update
- control packet mutation
- granting probe execution authority

## Required invariants

- replay cursor remains monotone
- idempotency remains enforced
- processed ticks are skipped
- pending ticks must form a contiguous suffix
- no-op resume is allowed
- resume cannot be used to bypass token ledger state

## Next layer

The next layer should provide deployment files for a real persistent OS process, such as systemd or Docker, using this resume controller on startup.
