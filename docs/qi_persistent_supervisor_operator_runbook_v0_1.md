# Qi Persistent Supervisor Operator Runbook v0.1

This runbook describes the bounded operator workflow for the Qi persistent supervisor.

It is not an unbounded autonomous daemon procedure. Every run is bounded by explicit control and outer iteration limits.

## 1. Write an allow control packet

```bash
python scripts/write_qi_supervisor_control_v0_1.py \
  --allow \
  --write .out/qi-supervisor/control.json \
  --max-cycles 1 \
  --sleep-seconds-between-cycles 0 \
  --reason "operator allow bounded run"
```

This writes:

- `.out/qi-supervisor/control.json`
- `.out/qi-supervisor/control_compiled_v0_1.json`

## 2. Start the bounded persistent supervisor

```bash
python scripts/run_qi_persistent_supervisor_v0_1.py \
  --raw-state examples/qi_process_tensor_v0_1/raw_state_process_history.json \
  --evidence examples/qi_process_tensor_v0_1/evidence.json \
  --control .out/qi-supervisor/control.json \
  --out-dir .out/qi-supervisor/run \
  --max-outer-iterations 3 \
  --max-daemon-ticks 1 \
  --max-steps-per-tick 1 \
  --requested-max-reentry-cycles 1 \
  --sleep-seconds-between-iterations 0
```

This writes:

- `.out/qi-supervisor/run/qi_persistent_supervisor_result_v0_1.json`
- `.out/qi-supervisor/run/qi_persistent_supervisor_overview_v0_1.txt`
- `.out/qi-supervisor/run/qi_persistent_supervisor_operator_manifest_v0_1.json`
- `.out/qi-supervisor/run/qi_persistent_supervisor_manifest_v0_1.json`
- per-iteration heartbeat files
- per-iteration status files

## 3. View supervisor status

```bash
python scripts/view_qi_persistent_supervisor_status_v0_1.py \
  --out-dir .out/qi-supervisor/run \
  --write-json .out/qi-supervisor/status_view.json \
  --write-text .out/qi-supervisor/status_view.txt
```

The status view reports:

- `supervisor_status`
- `iterations_run`
- `total_cycles_run`
- `total_control_checks`
- `final_stop_reason`
- `latest_iteration_index`
- `latest_heartbeat_path`
- `latest_status_path`
- `view_blockers`
- `view_warnings`

## 4. Request stop

```bash
python scripts/write_qi_supervisor_control_v0_1.py \
  --stop \
  --write .out/qi-supervisor/control.json \
  --max-cycles 1 \
  --reason "operator stop requested"
```

A controlled loop reads the control file before entering each cycle. A persistent supervisor also performs a control precheck before each outer iteration.

## 5. Disable loop start

```bash
python scripts/write_qi_supervisor_control_v0_1.py \
  --disable \
  --write .out/qi-supervisor/control.json \
  --max-cycles 1 \
  --reason "operator disabled supervisor"
```

Use disable when the operator wants the supervisor to remain off until an explicit allow packet is written again.

## Boundary

The persistent supervisor surface is bounded and read-only at the authority layer:

- no unbounded daemon loop
- `max_outer_iterations` required
- control packet required
- heartbeat/status output required
- status view is read-only
- no next tick execution authority
- no policy mutation authority
- no belief update authority
- no memory overwrite authority
- no truth authority
- no clinical authority
- no theorem authority

## CI checks

The runtime full check covers the operator path with:

```bash
python scripts/check_qi_supervisor_control_writer_v0_1.py
python scripts/check_qi_persistent_supervisor_operator_cli_v0_1.py
python scripts/check_qi_persistent_supervisor_status_view_cli_v0_1.py
```
