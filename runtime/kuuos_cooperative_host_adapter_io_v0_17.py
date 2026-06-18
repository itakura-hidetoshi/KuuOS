from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_host_adapter_idempotent_tick_v0_17 import run_host_tick
from runtime.kuuos_cooperative_host_adapter_projection_v0_17 import project_host_work
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import BLOCKED


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


def project_host_work_files(
    *,
    supervisor_bundle_path: Path,
    projection_output_path: Path,
    now_ms: int,
    operation_allowlist: Sequence[str],
) -> dict[str, Any]:
    bundle = read_json(supervisor_bundle_path)
    projection = project_host_work(
        supervisor_bundle=bundle,
        now_ms=now_ms,
        operation_allowlist=operation_allowlist,
    )
    write_json_atomic(projection_output_path, projection)
    return projection


def run_host_tick_files(
    *,
    supervisor_bundle_path: Path,
    projection_path: Path,
    host_license_path: Path,
    output_bundle_path: Path,
    receipt_output_path: Path,
    audit_path: Path,
    worker_id: str,
    invocation_id: str,
    now_ms: int,
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
) -> dict[str, Any]:
    bundle = read_json(supervisor_bundle_path)
    projection = read_json(projection_path)
    license_packet = read_json(host_license_path)
    same_bundle_path = supervisor_bundle_path.resolve() == output_bundle_path.resolve()
    if same_bundle_path and license_packet.get("in_place_bundle_write_allowed") is not True:
        result = {
            "status": BLOCKED,
            "adapter_state": "blocked_before_claim",
            "blockers": ["in_place_bundle_write_not_allowed"],
            "result_supervisor_bundle": bundle,
            "slice_packet": {},
            "receipt": {
                "status": BLOCKED,
                "blockers": ["in_place_bundle_write_not_allowed"],
                "worker_id": str(worker_id),
                "invocation_id": str(invocation_id),
            },
        }
        write_json_atomic(receipt_output_path, result["receipt"])
        if license_packet.get("audit_append_allowed") is True:
            append_jsonl(audit_path, result["receipt"])
        return result

    result = run_host_tick(
        supervisor_bundle=bundle,
        projection=projection,
        host_license=license_packet,
        worker_id=worker_id,
        invocation_id=invocation_id,
        now_ms=now_ms,
        supervisor_policy=supervisor_policy,
        registry=registry,
    )
    receipt = result.get("receipt", {}) if isinstance(result.get("receipt", {}), Mapping) else {}
    if license_packet.get("receipt_write_allowed") is True:
        write_json_atomic(receipt_output_path, receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(
            audit_path,
            {
                **dict(receipt),
                "host_tick_digest": result.get("host_tick_digest", ""),
                "adapter_state": result.get("adapter_state", ""),
            },
        )
    if result.get("status") != BLOCKED and license_packet.get("bundle_output_write_allowed") is True:
        write_json_atomic(output_bundle_path, result["result_supervisor_bundle"])
    return result
