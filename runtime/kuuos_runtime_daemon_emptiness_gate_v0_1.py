#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_qi_policy_v0_1 import read_and_evaluate_daemon_qi_policy
except ModuleNotFoundError:
    from kuuos_runtime_daemon_qi_policy_v0_1 import read_and_evaluate_daemon_qi_policy

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

@dataclass(frozen=True)
class KuuOSDaemonEmptinessGateResult:
    gate_version: str
    gate_status: str
    recommended_emptiness_action: str
    gate_reason: str
    tick_density: int
    policy_mode: str | None
    qique_regime: str | None
    qique_recovery_budget_pressure: float | None
    non_reification_assertions: dict[str, bool]
    allowed_projection: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _tick_density_from_daemon_dir(daemon_dir: Path) -> int:
    tick_log = daemon_dir / "daemon_tick_log_v0_1.json"
    if not tick_log.is_file():
        return 0
    value = _read_json(tick_log)
    return len(value) if isinstance(value, list) else 0


def _non_reification_assertions() -> dict[str, bool]:
    return {
        "receipt_is_not_truth": True,
        "status_is_not_identity": True,
        "policy_hint_is_not_command": True,
        "qique_regime_is_not_essence": True,
        "process_tensor_summary_is_not_self": True,
        "compact_trace_is_allowed": True,
        "hold_is_legitimate": True,
        "reobserve_is_legitimate": True,
        "quarantine_is_legitimate": True,
    }


def evaluate_daemon_emptiness_gate(policy_result: Mapping[str, Any], tick_density: int) -> KuuOSDaemonEmptinessGateResult:
    policy_mode = policy_result.get("recommended_tick_mode")
    qique = policy_result.get("daemon_qique_gauge") if isinstance(policy_result.get("daemon_qique_gauge"), Mapping) else {}
    qique_regime = qique.get("qique_regime")
    recovery_pressure = qique.get("recovery_budget_pressure")
    pressure = float(recovery_pressure) if isinstance(recovery_pressure, (int, float)) else None

    if policy_mode in {"HOLD_FOR_DAEMON_REPAIR", "QUARANTINE_REVIEW"}:
        action = "HOLD_OR_QUARANTINE_NONFINAL"
        reason = "policy_requires_hold_or_quarantine"
        status = "EMPTINESS_GATE_BLOCKING_REIFICATION"
    elif policy_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS", "FOCUS_OR_REOBSERVE"}:
        action = "REOBSERVE_WITH_NON_REIFICATION"
        reason = "policy_requires_reobserve_or_evidence"
        status = "EMPTINESS_GATE_REOBSERVE"
    elif pressure is not None and pressure >= 0.75:
        action = "HOLD_AND_COMPACT_TRACE"
        reason = "qique_recovery_pressure_high"
        status = "EMPTINESS_GATE_PRESSURE_HOLD"
    elif tick_density >= 10:
        action = "COMPACT_TRACE_BEFORE_CONTINUE"
        reason = "tick_density_high"
        status = "EMPTINESS_GATE_COMPACT"
    elif qique_regime in {"LOCALIZED_MEMORY_CHANNEL", "NONMARKOV_MEMORY_ACTIVE"} and tick_density >= 3:
        action = "CONTINUE_WITH_COMPACT_MONITOR"
        reason = "memory_active_requires_compact_monitor"
        status = "EMPTINESS_GATE_CONTINUE_ADVISORY"
    else:
        action = "CONTINUE_ADVISORY_ONLY"
        reason = "bounded_non_reifying_continue"
        status = "EMPTINESS_GATE_PASS"

    return KuuOSDaemonEmptinessGateResult(
        gate_version="kuuos_runtime_daemon_emptiness_gate_v0_1",
        gate_status=status,
        recommended_emptiness_action=action,
        gate_reason=reason,
        tick_density=int(tick_density),
        policy_mode=str(policy_mode) if policy_mode is not None else None,
        qique_regime=str(qique_regime) if qique_regime is not None else None,
        qique_recovery_budget_pressure=pressure,
        non_reification_assertions=_non_reification_assertions(),
        allowed_projection=["daemon_emptiness_gate_result", "non_reification_advisory"],
    )


def read_and_evaluate_daemon_emptiness_gate(daemon_dir: Path) -> KuuOSDaemonEmptinessGateResult:
    policy = read_and_evaluate_daemon_qi_policy(daemon_dir)
    return evaluate_daemon_emptiness_gate(policy.to_dict(), _tick_density_from_daemon_dir(daemon_dir))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon emptiness gate v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_emptiness_gate(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.recommended_emptiness_action not in {"HOLD_OR_QUARANTINE_NONFINAL", "HOLD_AND_COMPACT_TRACE"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
