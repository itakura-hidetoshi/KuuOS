#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_emptiness_gate_v0_1 import read_and_evaluate_daemon_emptiness_gate
except ModuleNotFoundError:
    from kuuos_runtime_daemon_emptiness_gate_v0_1 import read_and_evaluate_daemon_emptiness_gate

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
class KuuOSDaemonWaFunctionResult:
    wa_version: str
    wa_status: str
    recommended_runtime_posture: str
    wa_reason: str
    wa_score: float
    qi_scope_score: float
    emptiness_score: float
    harmony_score: float
    nihilism_risk_score: float
    over_density_penalty: float
    policy_mode: str | None
    emptiness_action: str | None
    qique_regime: str | None
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


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _qique_from_gate(gate: Mapping[str, Any]) -> Mapping[str, Any]:
    # Gate result keeps selected top-level qique fields; future richer payloads may include a nested gauge.
    return gate.get("daemon_qique_gauge", {}) if isinstance(gate.get("daemon_qique_gauge"), Mapping) else {}


def evaluate_daemon_wa_function(gate_result: Mapping[str, Any]) -> KuuOSDaemonWaFunctionResult:
    action = gate_result.get("recommended_emptiness_action")
    policy_mode = gate_result.get("policy_mode")
    qique_regime = gate_result.get("qique_regime")
    recovery_pressure = gate_result.get("qique_recovery_budget_pressure")
    pressure = float(recovery_pressure) if isinstance(recovery_pressure, (int, float)) else 0.0
    tick_density = int(gate_result.get("tick_density", 0) or 0)

    qi_scope_score = _clamp(0.75 if policy_mode in {"CONTINUE_WITH_QI_MEMORY_MONITOR", "CONTINUE_WITH_MEMORY_MONITOR", "CONTINUE_BOUNDED"} else 0.45)
    if policy_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS", "FOCUS_OR_REOBSERVE"}:
        qi_scope_score = 0.55
    if policy_mode in {"QUARANTINE_REVIEW", "HOLD_FOR_DAEMON_REPAIR"}:
        qi_scope_score = 0.2

    emptiness_score = _clamp(0.85 if action in {"CONTINUE_ADVISORY_ONLY", "CONTINUE_WITH_COMPACT_MONITOR", "COMPACT_TRACE_BEFORE_CONTINUE"} else 0.65)
    if action in {"HOLD_AND_COMPACT_TRACE", "HOLD_OR_QUARANTINE_NONFINAL"}:
        emptiness_score = 0.95

    over_density_penalty = _clamp(tick_density / 20.0)
    nihilism_risk = 0.0
    if action in {"HOLD_OR_QUARANTINE_NONFINAL", "HOLD_AND_COMPACT_TRACE"}:
        nihilism_risk += 0.35
    if qi_scope_score <= 0.25:
        nihilism_risk += 0.35
    if policy_mode in {"REQUEST_MORE_EVIDENCE", "REOBSERVE_QI_PROCESS"}:
        nihilism_risk += 0.15
    nihilism_risk_score = _clamp(nihilism_risk)

    harmony_score = _clamp((qi_scope_score + emptiness_score) / 2.0 - (over_density_penalty * 0.25) - (nihilism_risk_score * 0.35))
    wa_score = _clamp(harmony_score)

    if action == "HOLD_OR_QUARANTINE_NONFINAL":
        posture = "QUARANTINE_WITH_RETURN_PATH"
        reason = "emptiness_blocks_reification_with_return_path"
        status = "WA_HOLD_RETURN_PATH"
    elif action == "HOLD_AND_COMPACT_TRACE":
        posture = "HOLD_WITH_RECOVERY"
        reason = "pressure_hold_without_nihilism"
        status = "WA_HOLD_RECOVERY"
    elif action == "REOBSERVE_WITH_NON_REIFICATION":
        posture = "SLOW_DOWN_AND_REOBSERVE"
        reason = "reobserve_preserves_qi_without_reifying"
        status = "WA_REOBSERVE"
    elif action == "COMPACT_TRACE_BEFORE_CONTINUE":
        posture = "CONTINUE_AFTER_COMPACT"
        reason = "density_requires_compact_before_continue"
        status = "WA_COMPACT_CONTINUE"
    elif action == "CONTINUE_WITH_COMPACT_MONITOR":
        posture = "CONTINUE_WITH_COMPACT_MONITOR"
        reason = "memory_activity_needs_compact_middle_way"
        status = "WA_COMPACT_MONITOR"
    elif qique_regime == "LOCALIZED_MEMORY_CHANNEL":
        posture = "BRANCH_EXPLORE_LIGHTLY"
        reason = "localized_memory_channel_needs_light_branching"
        status = "WA_LIGHT_BRANCH"
    else:
        posture = "CONTINUE_HARMONIZED"
        reason = "qi_and_emptiness_balanced_continue"
        status = "WA_HARMONIZED_CONTINUE"

    return KuuOSDaemonWaFunctionResult(
        wa_version="kuuos_runtime_daemon_wa_function_v0_1",
        wa_status=status,
        recommended_runtime_posture=posture,
        wa_reason=reason,
        wa_score=wa_score,
        qi_scope_score=qi_scope_score,
        emptiness_score=emptiness_score,
        harmony_score=harmony_score,
        nihilism_risk_score=nihilism_risk_score,
        over_density_penalty=over_density_penalty,
        policy_mode=str(policy_mode) if policy_mode is not None else None,
        emptiness_action=str(action) if action is not None else None,
        qique_regime=str(qique_regime) if qique_regime is not None else None,
        allowed_projection=["daemon_wa_function_result", "middle_way_advisory"],
    )


def read_and_evaluate_daemon_wa_function(daemon_dir: Path) -> KuuOSDaemonWaFunctionResult:
    gate = read_and_evaluate_daemon_emptiness_gate(daemon_dir)
    return evaluate_daemon_wa_function(gate.to_dict())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon Wa function v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_wa_function(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
