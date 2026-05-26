#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_process_tensor_advantage_metrics_v0_1 import compute_qi_process_tensor_advantage_metrics
    from runtime.kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1 import plan_qi_process_tensor_probe
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_process_tensor_advantage_metrics_v0_1 import compute_qi_process_tensor_advantage_metrics
    from kuuos_runtime_daemon_qi_process_tensor_probe_planner_v0_1 import plan_qi_process_tensor_probe


@dataclass(frozen=True)
class KuuOSQiPersistentSupervisorStatusView:
    status_view_version: str
    status_view_status: str
    out_dir: str
    supervisor_manifest_path: str
    supervisor_status: str | None
    iterations_run: int
    total_cycles_run: int
    total_control_checks: int
    final_stop_reason: str | None
    latest_iteration_index: int | None
    latest_heartbeat_path: str | None
    latest_status_path: str | None
    latest_controlled_loop_result_path: str | None
    latest_heartbeat: dict[str, Any]
    latest_status: dict[str, Any]
    latest_process_tensor_advantage_metrics: dict[str, Any]
    process_tensor_advantage_score: float | None
    process_tensor_advantage_level: str | None
    recommended_next_process_focus: str | None
    latest_process_tensor_probe_plan: dict[str, Any]
    recommended_probe_type: str | None
    probe_target_time_slice: str | None
    probe_risk_level: str | None
    view_blockers: list[str]
    view_warnings: list[str]
    status_view_only: bool
    read_only: bool
    grants_execution_authority: bool = False
    grants_probe_execution_authority: bool = False
    grants_next_tick_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _latest_allowed_cycle_record(controlled_loop_result: dict[str, Any]) -> dict[str, Any] | None:
    records = controlled_loop_result.get("cycle_records")
    if not isinstance(records, list):
        return None
    for record in reversed(records):
        if isinstance(record, dict) and record.get("loop_allowed"):
            return record
    return None


def _process_tensor_surfaces_from_latest_iteration(
    latest_record: dict[str, Any] | None,
    warnings: list[str],
) -> tuple[str | None, dict[str, Any], dict[str, Any]]:
    if not latest_record:
        warnings.append("latest_iteration_record_missing_for_process_tensor_surfaces")
        return None, {}, {}
    loop_result_path = latest_record.get("controlled_loop_result_path")
    if not loop_result_path:
        warnings.append("controlled_loop_result_path_missing_for_process_tensor_surfaces")
        return None, {}, {}
    controlled_loop_result = _read_json(Path(loop_result_path))
    if not controlled_loop_result:
        warnings.append("controlled_loop_result_missing_for_process_tensor_surfaces")
        return str(loop_result_path), {}, {}
    cycle_record = _latest_allowed_cycle_record(controlled_loop_result)
    if not cycle_record:
        warnings.append("allowed_cycle_record_missing_for_process_tensor_surfaces")
        return str(loop_result_path), {}, {}
    raw_state_path = cycle_record.get("input_raw_state_path")
    projection_path = cycle_record.get("routed_projection_plan_result_path")
    if not raw_state_path:
        warnings.append("raw_state_path_missing_for_process_tensor_surfaces")
        return str(loop_result_path), {}, {}
    raw_state = _read_json(Path(raw_state_path))
    if not raw_state:
        warnings.append("raw_state_missing_for_process_tensor_surfaces")
        return str(loop_result_path), {}, {}
    projection = _read_json(Path(projection_path)) if projection_path else {}
    if not projection:
        warnings.append("projection_summary_missing_for_process_tensor_surfaces")
    metrics = compute_qi_process_tensor_advantage_metrics(raw_state=raw_state, projection_summary=projection).to_dict()
    probe_plan = plan_qi_process_tensor_probe(
        latest_process_tensor_advantage_metrics=metrics,
        raw_state=raw_state,
        projection_summary=projection,
    ).to_dict()
    return str(loop_result_path), metrics, probe_plan


def compile_qi_persistent_supervisor_status_view(*, out_dir: Path) -> KuuOSQiPersistentSupervisorStatusView:
    out_dir = Path(out_dir)
    manifest_path = out_dir / "qi_persistent_supervisor_manifest_v0_1.json"
    blockers: list[str] = []
    warnings: list[str] = []
    manifest = _read_json(manifest_path)
    if not manifest:
        blockers.append("supervisor_manifest_missing")

    records = manifest.get("iteration_records", []) if isinstance(manifest, dict) else []
    if not isinstance(records, list):
        records = []
        warnings.append("iteration_records_not_list")
    latest_record = records[-1] if records and isinstance(records[-1], dict) else None
    latest_index = _safe_int(latest_record.get("iteration_index"), None) if latest_record else None
    latest_heartbeat_path = latest_record.get("heartbeat_path") if latest_record else None
    latest_status_path = latest_record.get("status_path") if latest_record else None
    heartbeat = _read_json(Path(latest_heartbeat_path)) if latest_heartbeat_path else {}
    status = _read_json(Path(latest_status_path)) if latest_status_path else {}
    if latest_record and not heartbeat:
        warnings.append("latest_heartbeat_missing")
    if latest_record and not status:
        warnings.append("latest_status_missing")

    loop_result_path, advantage_metrics, probe_plan = _process_tensor_surfaces_from_latest_iteration(latest_record, warnings) if manifest else (None, {}, {})
    advantage_score = advantage_metrics.get("process_tensor_advantage_score") if advantage_metrics else None
    advantage_level = advantage_metrics.get("process_tensor_advantage_level") if advantage_metrics else None
    next_focus = advantage_metrics.get("recommended_next_process_focus") if advantage_metrics else None
    recommended_probe_type = probe_plan.get("recommended_probe_type") if probe_plan else None
    probe_target_time_slice = probe_plan.get("probe_target_time_slice") if probe_plan else None
    probe_risk_level = probe_plan.get("probe_risk_level") if probe_plan else None

    status_view_status = "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY" if not blockers else "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_BLOCKED"
    return KuuOSQiPersistentSupervisorStatusView(
        status_view_version="kuuos_runtime_daemon_qi_persistent_supervisor_status_view_v0_1",
        status_view_status=status_view_status,
        out_dir=str(out_dir),
        supervisor_manifest_path=str(manifest_path),
        supervisor_status=manifest.get("supervisor_status") if manifest else None,
        iterations_run=_safe_int(manifest.get("iterations_run"), 0) if manifest else 0,
        total_cycles_run=_safe_int(manifest.get("total_cycles_run"), 0) if manifest else 0,
        total_control_checks=_safe_int(manifest.get("total_control_checks"), 0) if manifest else 0,
        final_stop_reason=manifest.get("final_stop_reason") if manifest else None,
        latest_iteration_index=latest_index,
        latest_heartbeat_path=str(latest_heartbeat_path) if latest_heartbeat_path else None,
        latest_status_path=str(latest_status_path) if latest_status_path else None,
        latest_controlled_loop_result_path=loop_result_path,
        latest_heartbeat=heartbeat,
        latest_status=status,
        latest_process_tensor_advantage_metrics=advantage_metrics,
        process_tensor_advantage_score=float(advantage_score) if advantage_score is not None else None,
        process_tensor_advantage_level=str(advantage_level) if advantage_level is not None else None,
        recommended_next_process_focus=str(next_focus) if next_focus is not None else None,
        latest_process_tensor_probe_plan=probe_plan,
        recommended_probe_type=str(recommended_probe_type) if recommended_probe_type is not None else None,
        probe_target_time_slice=str(probe_target_time_slice) if probe_target_time_slice is not None else None,
        probe_risk_level=str(probe_risk_level) if probe_risk_level is not None else None,
        view_blockers=blockers,
        view_warnings=warnings,
        status_view_only=True,
        read_only=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="View KuuOS Qi persistent supervisor status v0.1")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--write", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = compile_qi_persistent_supervisor_status_view(out_dir=args.out_dir)
    if args.write:
        _write_json(args.write, result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
