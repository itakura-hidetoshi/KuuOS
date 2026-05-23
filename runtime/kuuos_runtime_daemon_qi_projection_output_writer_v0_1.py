#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any

try:
    from runtime.kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
        read_and_compile_qi_process_tensor_recoverability_projection,
    )
    from runtime.kuuos_runtime_daemon_qi_process_tensor_health_projection_v0_1 import (
        read_and_compile_qi_process_tensor_health_projection,
    )
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
        read_and_compile_qi_process_tensor_recoverability_projection,
    )
    from kuuos_runtime_daemon_qi_process_tensor_health_projection_v0_1 import (
        read_and_compile_qi_process_tensor_health_projection,
    )


@dataclass(frozen=True)
class KuuOSQiProjectionOutputWriterResult:
    writer_version: str
    writer_status: str
    daemon_dir: str
    recoverability_projection_path: str
    health_projection_path: str
    recoverability_status: str
    dominant_recovery_path: str
    recommended_recovery_action: str
    recoverability_score: float
    recovery_unsafe: bool
    local_recovery_allowed: bool
    qi_process_tensor_phase: str
    daemon_health_status: str
    next_operator_action: str
    health_reason: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_qi_projection_outputs(daemon_dir: Path) -> KuuOSQiProjectionOutputWriterResult:
    daemon_dir = Path(daemon_dir)
    recoverability = read_and_compile_qi_process_tensor_recoverability_projection(daemon_dir)
    recoverability_path = daemon_dir / "daemon_qi_process_tensor_recoverability_projection_v0_1.json"
    _write_json(recoverability_path, recoverability.to_dict())

    health = read_and_compile_qi_process_tensor_health_projection(daemon_dir)
    health_path = daemon_dir / "daemon_qi_process_tensor_health_projection_v0_1.json"
    _write_json(health_path, health.to_dict())

    return KuuOSQiProjectionOutputWriterResult(
        writer_version="kuuos_runtime_daemon_qi_projection_output_writer_v0_1",
        writer_status="QI_PROJECTION_OUTPUTS_WRITTEN",
        daemon_dir=str(daemon_dir),
        recoverability_projection_path=str(recoverability_path),
        health_projection_path=str(health_path),
        recoverability_status=recoverability.recoverability_status,
        dominant_recovery_path=recoverability.dominant_recovery_path,
        recommended_recovery_action=recoverability.recommended_recovery_action,
        recoverability_score=recoverability.recoverability_score,
        recovery_unsafe=recoverability.recovery_unsafe,
        local_recovery_allowed=recoverability.local_recovery_allowed,
        qi_process_tensor_phase=health.qi_process_tensor_phase,
        daemon_health_status=health.daemon_health_status,
        next_operator_action=health.next_operator_action,
        health_reason=health.health_reason,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write KuuOS Qi projection outputs v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write-summary", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = write_qi_projection_outputs(args.daemon_dir)
    if args.write_summary:
        _write_json(args.daemon_dir / "daemon_qi_projection_output_writer_result_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
