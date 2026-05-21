# KuuOS Qi State IO Example v0.1

This example runs the bounded KuuOS Qi/OS loop from JSON files.

## Inputs

- `raw_state.json`
- `evidence.json`

## Run

```bash
python3 scripts/run_kuuos_state_io_example_v0_1.py
```

Optional:

```bash
python3 scripts/run_kuuos_state_io_example_v0_1.py \
  --raw-state examples/qi_state_io_v0_1/raw_state.json \
  --evidence examples/qi_state_io_v0_1/evidence.json \
  --output-dir runs/qi_state_io_v0_1/manual \
  --max-steps 2
```

## Outputs

The runner writes:

- `kuuos_driver_result_v0_1.json`
- `next_raw_state_v0_1.json`
- `state_bundle_v0_1.json`
- `step_trace_v0_1.json`
- `run_manifest_v0_1.json`

## Qi process tensor summary

Quick audit locations:

```text
step_trace_v0_1.json -> [i].qi_process_tensor_summary
state_bundle_v0_1.json -> loop_log[i].qi_process_tensor_summary
```

The summary reports process visibility, continuity, memory continuity, non-Markov memory, history length, support counts, missing requirements, and reason.

## Continue from previous state

```bash
python3 scripts/run_kuuos_state_io_example_v0_1.py \
  --raw-state runs/qi_state_io_v0_1/manual/next_raw_state_v0_1.json \
  --evidence examples/qi_state_io_v0_1/evidence.json \
  --state-bundle runs/qi_state_io_v0_1/manual/state_bundle_v0_1.json \
  --output-dir runs/qi_state_io_v0_1/manual_next \
  --max-steps 2
```

## Boundary

This example is non-authoritative. It does not execute actions, finalize truth, overwrite memory, make clinical decisions, prove theorems, or create completed OS identity.
