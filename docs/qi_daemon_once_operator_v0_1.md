# Qi Daemon Once Operator v0.1

`run_qi_daemon_once_v0_1.py` is the operator-facing entry point for one bounded Qi daemon run.

It is designed to make the current runtime usable as an OS surface without turning it into an autonomous daemon loop.

## Command

```bash
python scripts/run_qi_daemon_once_v0_1.py \
  --raw-state examples/qi_process_tensor_v0_1/raw_state_process_history.json \
  --evidence examples/qi_process_tensor_v0_1/evidence.json \
  --out-dir .out/qi-daemon-once \
  --max-daemon-ticks 1 \
  --max-steps-per-tick 1 \
  --requested-max-reentry-cycles 1
```

## Inputs

- `--raw-state`: raw Qi process tensor state input.
- `--evidence`: evidence packet input.
- `--out-dir`: output directory for daemon, dispatch, manifest, result, and readable summary artifacts.
- `--max-daemon-ticks`: maximum bounded daemon ticks for this one run.
- `--max-steps-per-tick`: maximum internal steps per tick.
- `--requested-max-reentry-cycles`: requested bounded reentry cap.
- `--state-bundle`: optional state bundle path.
- `--quiet`: suppress readable summary printing while still writing artifacts.

## Outputs

The operator CLI writes these top-level outputs under `--out-dir`:

- `qi_daemon_once_result_v0_1.json`
- `qi_daemon_once_readable_summary_v0_1.json`
- `qi_daemon_once_readable_summary_v0_1.txt`
- `qi_daemon_once_manifest_v0_1.json`

It also writes nested daemon and dispatch artifacts under:

- `daemon/`
- `dispatch/`

## Operator-readable summary

The readable text summary includes:

- `recommended_next_runtime_mode`
- `recommended_next_reason`
- `next_tick_preparation`
- `required_pre_tick_actions`
- `projection_statuses`
- `authority: none`
- `scope: readable-summary-only`

## What the one-shot run performs

The operator CLI performs this bounded chain:

```text
raw_state + evidence
  -> routed daemon cycle
  -> Qi projection outputs
  -> operational summary
  -> next runtime mode plan
  -> readable summary
  -> manifest
```

Projection outputs include:

- recoverability
- health
- observation debt
- trace compaction

## Boundary

This command is intentionally bounded and read-only at the authority layer:

- one-shot only
- operator-facing
- read-only summary surface
- no autonomous daemon loop
- no next tick execution authority
- no policy mutation authority
- no belief update authority
- no memory overwrite authority
- no truth authority
- no clinical authority
- no theorem authority

`next_tick_preparation` is a preparation label, not permission to execute the next tick.

## CI checks

The following check verifies that the CLI can run on the packaged Qi process tensor example and write all operator outputs:

```bash
python scripts/check_qi_daemon_once_operator_cli_v0_1.py
```

The runtime full check includes this operator check.
