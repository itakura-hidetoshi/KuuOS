# Qi Process Tensor Bounded Tick Manual Runner v0.1

This example demonstrates the explicit outer invocation path from daemon receipts to one bounded State IO tick.

The daemon itself does not auto-invoke the executor. It exposes receipts and a single-tick invocation token. The manual runner is the explicit outer entrypoint.

## Inputs

- `raw_state.json`
- `evidence.json`
- `daemon/daemon_qi_process_tensor_reentry_license_gate_v0_1.json`
- `daemon/daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json`

## Command

```bash
python3 scripts/run_qi_process_tensor_bounded_tick_from_daemon_v0_1.py \
  --daemon-dir examples/qi_bounded_tick_manual_runner_v0_1/daemon \
  --raw-state examples/qi_bounded_tick_manual_runner_v0_1/raw_state.json \
  --evidence examples/qi_bounded_tick_manual_runner_v0_1/evidence.json \
  --output-dir /tmp/kuuos_qi_bounded_tick_manual_runner_out \
  --write
```

## Expected behavior

- A single bounded State IO tick is invoked only when `single_tick_invocation_token` is true.
- The executor writes `daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json` when `--write` is provided.
- The executor must not grant truth, final commitment, memory overwrite, clinical, theorem, or completed identity authority.
