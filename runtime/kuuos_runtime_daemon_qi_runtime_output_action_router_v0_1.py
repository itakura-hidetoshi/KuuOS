#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_runtime_output_surface_v0_1 import compile_qi_runtime_output_surface
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_runtime_output_surface_v0_1 import compile_qi_runtime_output_surface


@dataclass(frozen=True)
class KuuOSQiRuntimeOutputActionRoute:
    router_version: str
    router_status: str
    route_decision: str
    route_reason: str
    next_outer_action: str
    route_priority: str
    daemon_dir: str | None
    surface_path: str | None
    daemon_status: str | None
    daemon_stop_reason: str | None
    recoverability_status: str | None
    recommended_recovery_action: str | None
    recovery_unsafe: bool | None
    daemon_health_status: str | None
    next_operator_action: str | None
    observation_debt_status: str | None
    recommended_observation_action: str | None
    compaction_plan_status: str | None
    recommended_compaction_action: str | None
    grants_execution_authority: bool = False
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


def _s(surface: Mapping[str, Any], key: str) -> str | None:
    value = surface.get(key)
    return str(value) if value is not None else None


def route_qi_runtime_output_surface(
    *,
    surface: Mapping[str, Any],
    daemon_dir: Path | None = None,
    surface_path: Path | None = None,
) -> KuuOSQiRuntimeOutputActionRoute:
    recovery_unsafe = bool(surface.get("recovery_unsafe"))
    next_operator_action = _s(surface, "next_operator_action")
    recommended_recovery_action = _s(surface, "recommended_recovery_action")
    observation_action = _s(surface, "recommended_observation_action")
    compaction_action = _s(surface, "recommended_compaction_action")
    recoverability_status = _s(surface, "recoverability_status")
    observation_status = _s(surface, "observation_debt_status")
    compaction_status = _s(surface, "compaction_plan_status")

    route_decision = "ROUTE_NO_ACTION"
    next_outer_action = "no_action"
    reason = "surface_has_no_actionable_debt"
    priority = "low"

    if recovery_unsafe or next_operator_action == "hold":
        route_decision = "ROUTE_HOLD"
        next_outer_action = "hold"
        reason = "health_or_recovery_requests_hold"
        priority = "critical" if recovery_unsafe else "high"
    elif observation_action in {"observe", "reobserve"}:
        route_decision = "ROUTE_OBSERVATION"
        next_outer_action = observation_action
        reason = "observation_debt_requires_attention"
        priority = "high" if observation_status in {"OBSERVATION_DEBT_OPEN", "REOBSERVATION_DEBT_OPEN"} else "medium"
    elif compaction_action in {"compact_trace", "summarize_trace"}:
        route_decision = "ROUTE_COMPACTION"
        next_outer_action = compaction_action
        reason = "trace_compaction_plan_ready"
        priority = "high" if compaction_status == "COMPACTION_READY" else "medium"
    elif next_operator_action == "invoke_manual_runner" or recommended_recovery_action == "invoke_manual_runner":
        route_decision = "ROUTE_REENTRY"
        next_outer_action = "managed_reentry_chain"
        reason = "health_projection_allows_manual_reentry"
        priority = "high" if recoverability_status == "RECOVERABLE_BY_MANUAL_RUNNER" else "medium"
    elif next_operator_action in {"compact_trace", "reobserve", "observe"}:
        route_decision = "ROUTE_OPERATOR_ACTION"
        next_outer_action = next_operator_action
        reason = "health_projection_requests_operator_action"
        priority = "medium"

    return KuuOSQiRuntimeOutputActionRoute(
        router_version="kuuos_runtime_daemon_qi_runtime_output_action_router_v0_1",
        router_status="QI_RUNTIME_OUTPUT_ACTION_ROUTED",
        route_decision=route_decision,
        route_reason=reason,
        next_outer_action=next_outer_action,
        route_priority=priority,
        daemon_dir=str(daemon_dir) if daemon_dir is not None else _s(surface, "daemon_dir"),
        surface_path=str(surface_path) if surface_path is not None else None,
        daemon_status=_s(surface, "daemon_status"),
        daemon_stop_reason=_s(surface, "daemon_stop_reason"),
        recoverability_status=recoverability_status,
        recommended_recovery_action=recommended_recovery_action,
        recovery_unsafe=recovery_unsafe,
        daemon_health_status=_s(surface, "daemon_health_status"),
        next_operator_action=next_operator_action,
        observation_debt_status=observation_status,
        recommended_observation_action=observation_action,
        compaction_plan_status=compaction_status,
        recommended_compaction_action=compaction_action,
    )


def read_and_route_qi_runtime_output_surface(daemon_dir: Path) -> KuuOSQiRuntimeOutputActionRoute:
    daemon_dir = Path(daemon_dir)
    surface_path = daemon_dir / "daemon_qi_runtime_output_surface_v0_1.json"
    if surface_path.is_file():
        surface = _read_json(surface_path)
    else:
        surface = compile_qi_runtime_output_surface(daemon_dir).to_dict()
    return route_qi_runtime_output_surface(surface=surface, daemon_dir=daemon_dir, surface_path=surface_path if surface_path.is_file() else None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Route KuuOS Qi runtime output surface v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    route = read_and_route_qi_runtime_output_surface(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_qi_runtime_output_action_route_v0_1.json", route.to_dict())
    print(json.dumps(route.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
