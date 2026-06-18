from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_durable_host_orchestrator_cycle_v0_18 import run_orchestrator_cycle
from runtime.kuuos_durable_host_orchestrator_plan_v0_18 import build_orchestrator_plan
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import BLOCKED


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"json_input_missing:{path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"json_input_invalid:{path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"json_input_not_object:{path}")
    return value


def read_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"json_input_missing:{path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"json_input_invalid:{path}") from error
    if not isinstance(value, list):
        raise ValueError(f"json_input_not_list:{path}")
    return [dict(item) for item in value if isinstance(item, Mapping)]


def write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def build_orchestrator_plan_files(
    *,
    cycle_id: str,
    supervisor_bundle_path: Path,
    orchestrator_state_path: Path,
    worker_reports_path: Path,
    host_license_path: Path,
    policy_path: Path,
    plan_output_path: Path,
    registry: Mapping[str, Executor],
    now_ms: int,
) -> dict[str, Any]:
    plan = build_orchestrator_plan(
        cycle_id=cycle_id,
        supervisor_bundle=read_json(supervisor_bundle_path),
        orchestrator_state=read_json(orchestrator_state_path),
        worker_reports=read_json_list(worker_reports_path),
        host_license=read_json(host_license_path),
        policy=read_json(policy_path),
        registry=registry,
        now_ms=now_ms,
    )
    write_json_atomic(plan_output_path, plan)
    return plan


def run_orchestrator_cycle_files(
    *,
    supervisor_bundle_path: Path,
    orchestrator_state_path: Path,
    plan_path: Path,
    worker_reports_path: Path,
    host_license_path: Path,
    policy_path: Path,
    supervisor_output_path: Path,
    orchestrator_output_path: Path,
    receipt_output_path: Path,
    audit_path: Path,
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
    now_ms: int,
) -> dict[str, Any]:
    supervisor_bundle = read_json(supervisor_bundle_path)
    orchestrator_state = read_json(orchestrator_state_path)
    plan = read_json(plan_path)
    worker_reports = read_json_list(worker_reports_path)
    host_license = read_json(host_license_path)
    policy = read_json(policy_path)

    same_supervisor = supervisor_bundle_path.resolve() == supervisor_output_path.resolve()
    same_orchestrator = orchestrator_state_path.resolve() == orchestrator_output_path.resolve()
    path_blockers: list[str] = []
    if same_supervisor and policy.get("in_place_supervisor_write_allowed") is not True:
        path_blockers.append("in_place_supervisor_write_not_allowed")
    if same_orchestrator and policy.get("in_place_orchestrator_write_allowed") is not True:
        path_blockers.append("in_place_orchestrator_write_not_allowed")
    if path_blockers:
        receipt = {
            "status": BLOCKED,
            "cycle_id": str(plan.get("cycle_id", "")),
            "blockers": path_blockers,
        }
        write_json_atomic(receipt_output_path, receipt)
        append_jsonl(audit_path, receipt)
        return {
            "status": BLOCKED,
            "result_supervisor_bundle": supervisor_bundle,
            "result_orchestrator_state": orchestrator_state,
            "receipt": receipt,
            "blockers": path_blockers,
        }

    result = run_orchestrator_cycle(
        supervisor_bundle=supervisor_bundle,
        orchestrator_state=orchestrator_state,
        plan=plan,
        worker_reports=worker_reports,
        host_license=host_license,
        policy=policy,
        supervisor_policy=supervisor_policy,
        registry=registry,
        now_ms=now_ms,
    )
    receipt = result.get("receipt", {}) if isinstance(result.get("receipt", {}), Mapping) else {}
    write_json_atomic(receipt_output_path, receipt)
    append_jsonl(
        audit_path,
        {
            **dict(receipt),
            "orchestrator_cycle_digest": result.get("orchestrator_cycle_digest", ""),
        },
    )
    if result.get("status") != BLOCKED:
        write_json_atomic(supervisor_output_path, result["result_supervisor_bundle"])
        write_json_atomic(orchestrator_output_path, result["result_orchestrator_state"])
    return result
