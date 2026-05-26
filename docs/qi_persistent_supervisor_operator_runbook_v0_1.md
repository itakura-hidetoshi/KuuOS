# Qi Persistent Supervisor Operator Runbook v0.1

This runbook describes the bounded operator workflow for the Qi persistent supervisor.

It is not an unbounded autonomous daemon procedure. Every run is bounded by explicit control and outer iteration limits.

## 0. Comparison with the original runbook

The original runbook covered the bounded supervisor path:

```text
allow control
  -> bounded persistent supervisor
  -> status view
  -> stop / disable
```

The current process-tensor extension keeps that path unchanged and adds only a read-only review path after status:

```text
status view
  -> probe plan artifact
  -> artifact index
  -> trend summary
  -> operator review only
```

The extension does not introduce probe execution, next-tick execution authority, control-packet mutation, or memory overwrite authority.

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

The status view reports the bounded supervisor surface:

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

It also reports the current process-tensor review surface:

- `latest_process_tensor_advantage_metrics`
- `process_tensor_advantage_score`
- `process_tensor_advantage_level`
- `recommended_next_process_focus`
- `latest_process_tensor_probe_plan`
- `recommended_probe_type`
- `probe_target_time_slice`
- `probe_risk_level`

## 3a. Optional: read the same status through supervisorctl

```bash
python scripts/qi_supervisorctl_v0_1.py status \
  --out-dir .out/qi-supervisor/run \
  --write-json .out/qi-supervisor/supervisorctl_status.json \
  --write-text .out/qi-supervisor/supervisorctl_status.txt
```

This is still a read-only status surface. It is useful when the operator wants one unified entry point for `validate`, `allow`, `run`, `status`, `stop`, and `disable`.

## 3b. Write a probe plan artifact

```bash
python scripts/write_qi_process_tensor_probe_plan_artifact_v0_1.py \
  --status-view .out/qi-supervisor/status_view.json \
  --write .out/qi-supervisor/probe_plan_artifact_001.json
```

Alternatively, the artifact can be generated directly from the supervisor output directory:

```bash
python scripts/write_qi_process_tensor_probe_plan_artifact_v0_1.py \
  --out-dir .out/qi-supervisor/run \
  --write .out/qi-supervisor/probe_plan_artifact_001.json
```

The artifact is a proposal artifact only. It preserves:

- `recommended_probe_type`
- `probe_target_time_slice`
- `probe_risk_level`
- `probe_expected_recoverability_gain`
- `probe_expected_observation_debt_reduction`
- `latest_process_tensor_probe_plan`

## 3c. Build a probe plan artifact index

After multiple bounded runs, build an index from proposal artifacts:

```bash
python scripts/write_qi_process_tensor_probe_plan_artifact_index_v0_1.py \
  --artifact .out/qi-supervisor/probe_plan_artifact_001.json \
  --artifact .out/qi-supervisor/probe_plan_artifact_002.json \
  --artifact .out/qi-supervisor/probe_plan_artifact_003.json \
  --write .out/qi-supervisor/probe_plan_artifact_index.json
```

The index reports:

- `artifact_count`
- `ready_artifact_count`
- `blocked_artifact_count`
- `probe_type_counts`
- `risk_level_counts`
- `dominant_probe_type`
- `latest_recommended_probe_type`
- `latest_probe_target_time_slice`
- `repeated_probe_types`
- `mean_expected_recoverability_gain`
- `mean_expected_observation_debt_reduction`

## 3d. Write a trend summary

```bash
python scripts/write_qi_process_tensor_probe_plan_trend_summary_v0_1.py \
  --index .out/qi-supervisor/probe_plan_artifact_index.json \
  --write-json .out/qi-supervisor/probe_plan_trend_summary.json \
  --write-text .out/qi-supervisor/probe_plan_trend_summary.txt
```

The trend summary translates index fields into operator-readable Qi process tensor language:

- `qi_process_tensor_characterization`
- `trend_interpretation`
- `recommended_operator_focus`

Examples:

- `observation_debt_probe` -> `observation_debt_limited_qi_process_tensor`
- `recoverability_branch_probe` -> `recoverability_branch_limited_qi_process_tensor`
- `memory_kernel_probe` -> `memory_kernel_fragile_qi_process_tensor`
- `safe_reentry_window_probe` -> `safe_reentry_window_narrow_qi_process_tensor`
- `nonmarkov_memory_link_probe` -> `nonmarkov_link_sparse_qi_process_tensor`
- `multi_time_correlation_probe` -> `multi_time_correlation_low_visibility_qi_process_tensor`
- `continue_process_tensor_supervision_probe` -> `stable_supervision_qi_process_tensor`

## 3e. Review-only rule

The process-tensor review extension ends at trend summary.

The operator may review the summary, compare repeated probe recommendations, and decide whether more observation is needed. The summary does not authorize a probe executor.

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

The persistent supervisor and process-tensor review surfaces are bounded and read-only at the authority layer:

- no unbounded daemon loop
- `max_outer_iterations` required
- control packet required
- heartbeat/status output required
- status view is read-only
- probe plan artifact is proposal-only
- artifact index is read-only
- trend summary is read-only
- no probe execution authority
- no next tick execution authority
- no control packet authority from review artifacts
- no policy mutation authority
- no belief update authority
- no memory overwrite authority
- no truth authority
- no clinical authority
- no theorem authority

## CI checks

The runtime full check covers the original bounded operator path with:

```bash
python scripts/check_qi_supervisor_control_writer_v0_1.py
python scripts/check_qi_persistent_supervisor_operator_cli_v0_1.py
python scripts/check_qi_persistent_supervisor_status_view_cli_v0_1.py
python scripts/check_qi_supervisorctl_v0_1.py
```

The process-tensor review extension is covered with individual checks:

```bash
python scripts/check_qi_process_tensor_probe_planner_v0_1.py
python scripts/check_qi_process_tensor_probe_plan_artifact_writer_v0_1.py
python scripts/check_qi_process_tensor_probe_plan_artifact_index_v0_1.py
python scripts/check_qi_process_tensor_probe_plan_trend_summary_v0_1.py
python scripts/check_qi_process_tensor_review_flow_e2e_v0_1.py
```

The process-tensor review checks can also be run as one suite:

```bash
python scripts/run_qi_process_tensor_review_checks_v0_1.py \
  --write-json .out/qi-supervisor/process_tensor_review_check_suite.json
```

The same suite is wired to GitHub Actions as `Qi Process Tensor Review Checks`:

```text
.github/workflows/qi-process-tensor-review.yml
```

The workflow is manually runnable with `workflow_dispatch` and also runs on pull requests that touch the Qi process-tensor review surface.
