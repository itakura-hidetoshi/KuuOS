# Qi Watchdog Supervisor Timer v0.1

This addendum places a bounded read-only supervisor/timer layer after the Qi health / metrics / watchdog surface.

## Position

```text
deployment entrypoint
  -> health / metrics / watchdog surface
  -> bounded supervisor timer
```

## What opens

- bounded timer pass
- repeated read-only health sampling
- supervisor report packet
- Prometheus metric forwarding
- watchdog-compatible exit code forwarding
- systemd service / timer examples

## What remains closed

- daemon restart
- daemon stop
- daemon resume
- probe execution
- MemoryOS write / append / overwrite
- world update
- control packet mutation
- daemon control authority

## Exit code contract

```text
0 -> QI_WATCHDOG_SUPERVISOR_OK
1 -> QI_WATCHDOG_SUPERVISOR_DEGRADED
2 -> QI_WATCHDOG_SUPERVISOR_BLOCKED
```

The timer is intentionally conservative. It may report attention required, but it does not repair, mutate, restart, or resume the daemon.

## Example command

```bash
python scripts/run_qi_watchdog_supervisor_timer_v0_1.py \
  --daemon-status /var/lib/kuuos/qi-jsonl/daemon_status.json \
  --event-log /var/lib/kuuos/qi-jsonl/event_log.jsonl \
  --ledger-state /var/lib/kuuos/qi-jsonl/ledger_state.json \
  --context examples/qi_watchdog_supervisor_timer_context_v0_1.json \
  --max-iterations 1 \
  --write /var/lib/kuuos/qi-jsonl/watchdog_report.json \
  --write-prometheus /var/lib/kuuos/qi-jsonl/watchdog_metrics.prom \
  --quiet
```

## Safety interpretation

This layer is an observation membrane. It reads health state and exports report/metrics, but it never crosses into daemon control or world mutation.
