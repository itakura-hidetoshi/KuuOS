# Qi Local Metrics HTTP Exporter Contract v0.1

This addendum follows the bounded Qi watchdog supervisor timer and prepares a read-only metrics export / alerting surface.

## Position

```text
bounded supervisor timer
  -> watchdog_metrics.prom
  -> local metrics HTTP exporter contract
  -> Prometheus scrape / alert rule examples
```

## What opens

- local metrics exporter contract
- rendered metrics response snapshot
- Prometheus scrape example
- Prometheus alert rule examples
- systemd oneshot example for exporter snapshot generation

## What remains closed

- HTTP server startup in this PR
- daemon restart
- daemon stop
- daemon resume
- probe execution
- MemoryOS write / append / overwrite
- world update
- control packet mutation
- daemon control authority

## Important boundary

This PR intentionally does not start a long-running HTTP server. It defines the read-only exporter contract and renders the response packet that a future service can serve.

This keeps the operational surface narrow:

```text
read .prom file
read watchdog report
render metrics response
emit snapshot
```

No repair, mutation, restart, or resume path is introduced.

## Alert rule meaning

The provided Prometheus rules are notification surfaces only. They should create review / incident handoff signals, not automatic daemon control actions.

## Validation

```bash
python scripts/run_qi_local_metrics_http_exporter_checks_v0_1.py
```

Expected result:

```text
PASS: Qi local metrics HTTP exporter checks
```

## Next layer

The next addendum may add external alert routing / incident handoff packets while preserving the same read-only boundary.
