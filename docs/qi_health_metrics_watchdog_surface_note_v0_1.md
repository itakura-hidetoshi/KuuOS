# Qi Health Metrics Watchdog Surface Note v0.1

This note documents the first read-only health, metrics, and watchdog surface for the Qi JSONL deployment wrapper.

## Position

```text
deployment entrypoint
  -> daemon_status.json
  -> event_log.jsonl
  -> ledger_state.json
  -> health / metrics / watchdog surface
```

## What it observes

The surface reads:

- daemon resume status
- heartbeat count
- JSONL event line count
- replay cursor position
- token ledger count
- process tensor pressure
- dominant probe type
- safe resume / no-op resume state
- idempotency and duplicate tick safety

## Prometheus metrics

The surface emits text-format metrics, including:

```text
kuos_qi_daemon_health_ok
kuos_qi_daemon_watchdog_ok
kuos_qi_daemon_heartbeat_count
kuos_qi_daemon_event_log_lines
kuos_qi_daemon_replay_cursor_position
kuos_qi_daemon_token_ledger_count
kuos_qi_process_tensor_pressure
```

`kuos_qi_process_tensor_pressure` is encoded as:

```text
high = 3
moderate = 2
low = 1
unknown = 0
```

## Safety boundary

Allowed:

- read daemon status
- read JSONL event log
- read sidecar ledger state
- emit health packet
- emit Prometheus text metrics
- classify watchdog status

Still forbidden:

- probe execution
- MemoryOS write/append/overwrite
- world update
- control packet mutation
- granting probe execution authority

## Operational meaning

This makes the Qi Process Tensor Daemon externally observable without giving the observability layer any execution or mutation authority.

## Next layer

The next layer should wire this surface to a long-running watchdog loop or systemd timer and optionally expose the Prometheus text through a local HTTP endpoint.
