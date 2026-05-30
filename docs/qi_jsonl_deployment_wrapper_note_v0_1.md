# Qi JSONL Deployment Wrapper Note v0.1

This note documents the first deployment-oriented entrypoint for the Qi JSONL Persistent Process Tensor Daemon.

## Position

```text
safe resume controller
  -> deployment entrypoint
  -> systemd / Docker examples
  -> future health and watchdog surface
```

## Entrypoint

```bash
python scripts/qi_jsonl_daemon_entrypoint_v0_1.py \
  --config examples/qi_jsonl_daemon_config_v0_1.json
```

The entrypoint reads a config file, creates the state/input directories if needed, and invokes the JSONL safe resume controller.

## State files

- `event_log.jsonl`
- `ledger_state.json`
- `daemon_status.json`

## Input files

- `memory.json`
- `scheduler_state.json`
- `scheduler_proposal.json`
- `process_tensor_metrics.json`

## Safety boundary

Allowed:

- safe resume
- bounded ticks
- JSONL append-only state
- JSON sidecar cursor/token state
- no-op resume when all requested ticks are already processed

Still forbidden:

- probe execution
- MemoryOS write/append/overwrite
- world update
- control packet mutation
- granting probe execution authority

## Deployment examples

Examples are provided for:

- `deploy/systemd/qi-jsonl-daemon.service.example`
- `deploy/docker/Dockerfile.qi-jsonl-daemon.example`

The systemd example is intentionally `Type=oneshot` for v0.1. Continuous scheduling should be added through a timer or a later long-running watchdog surface.
