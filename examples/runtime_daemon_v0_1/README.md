# KuuOS Runtime Daemon Example v0.1

This example runs the bounded KuuOS runtime daemon.

## Run

```bash
python3 scripts/run_kuuos_runtime_daemon_example_v0_1.py
```

Optional:

```bash
python3 scripts/run_kuuos_runtime_daemon_example_v0_1.py \
  --raw-state examples/qi_process_tensor_v0_1/raw_state_process_history.json \
  --evidence examples/qi_process_tensor_v0_1/evidence.json \
  --daemon-dir runs/runtime_daemon_v0_1/manual \
  --max-ticks 2 \
  --max-steps-per-tick 1 \
  --sleep-seconds 0
```

## Outputs

The daemon writes:

```text
daemon_tick_log_v0_1.json
daemon_result_v0_1.json
tick_0000_*/
tick_0001_*/
```

Each tick directory contains the normal State IO outputs:

```text
kuuos_driver_result_v0_1.json
next_raw_state_v0_1.json
state_bundle_v0_1.json
step_trace_v0_1.json
run_manifest_v0_1.json
```

## Stop reasons

```text
MAX_TICKS_REACHED
WAITING_FOR_MORE_EVIDENCE
QUARANTINE_RETAINED
UNKNOWN_RESULT_HELD
```

## Boundary

This daemon is bounded and non-authoritative. It does not execute actions, finalize truth, overwrite memory, prove theorems, make clinical decisions, or create completed OS identity.
