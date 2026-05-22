#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

try:
    from runtime.kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1 import read_and_evaluate_daemon_yinyang_polarity
except ModuleNotFoundError:
    from kuuos_runtime_daemon_yinyang_polarity_gauge_v0_1 import read_and_evaluate_daemon_yinyang_polarity


@dataclass(frozen=True)
class KuuOSDaemonFourImagePhaseResult:
    gauge_version: str
    yinyang_polarity_state: str | None
    four_image_phase: str
    phase_reason: str
    phase_policy_hint: str
    phase_maturity_score: float
    yin_load: float | None
    yang_drive: float | None
    polarity_balance: float | None
    switch_risk: float | None
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


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def evaluate_daemon_four_image_phase(yinyang_result: Mapping[str, Any]) -> KuuOSDaemonFourImagePhaseResult:
    state = yinyang_result.get("yinyang_polarity_state")
    hint = yinyang_result.get("recommended_policy_hint")
    yin_load = yinyang_result.get("yin_load")
    yang_drive = yinyang_result.get("yang_drive")
    balance = yinyang_result.get("polarity_balance")
    switch_risk = yinyang_result.get("switch_risk")

    yin = float(yin_load) if isinstance(yin_load, (int, float)) else 0.0
    yang = float(yang_drive) if isinstance(yang_drive, (int, float)) else 0.0
    sw = float(switch_risk) if isinstance(switch_risk, (int, float)) else 0.0
    maturity = _clamp(max(yin, yang, sw))

    if state in {"BOUNDARY_YIN_REQUIRED", "YIN_REOBSERVE_REQUIRED"}:
        phase = "LESSER_YIN"
        phase_hint = str(hint or "REOBSERVE_QI_PROCESS")
        reason = "yin_observation_or_boundary_required"
    elif state == "YANG_OVERDRIVE":
        phase = "GREATER_YANG"
        phase_hint = "SLOW_DOWN_AND_REOBSERVE"
        reason = "yang_matured_into_overdrive"
    elif state == "YIN_STAGNATION":
        phase = "GREATER_YIN"
        phase_hint = "REOPEN_RECOVERY_PATH"
        reason = "yin_matured_into_stagnation"
    elif state == "FALSE_YANG":
        phase = "GREATER_YANG"
        phase_hint = "REOBSERVE_WITH_NON_REIFICATION"
        reason = "yang_claim_requires_reobservation"
    elif state == "FALSE_YIN":
        phase = "LESSER_YIN"
        phase_hint = "CONTINUE_WITH_COMPACT_MONITOR"
        reason = "yin_bias_requires_light_continuation"
    elif state == "SWITCHING_UNSTABLE":
        phase = "GREATER_YIN"
        phase_hint = "HOLD_WITH_RECOVERY"
        reason = "unstable_switch_requires_recovery_yin"
    elif state == "RECOVERY_YANG_PRESENT":
        phase = "LESSER_YANG"
        phase_hint = "CONTINUE_WITH_QI_MEMORY_MONITOR"
        reason = "recovery_yang_present_but_not_overdrive"
    elif state == "BALANCED_FLOW":
        if yang >= yin:
            phase = "LESSER_YANG"
            phase_hint = "CONTINUE_HARMONIZED"
            reason = "balanced_flow_with_light_yang"
        else:
            phase = "LESSER_YIN"
            phase_hint = "CONTINUE_WITH_COMPACT_MONITOR"
            reason = "balanced_flow_with_light_yin"
    else:
        phase = "LESSER_YIN"
        phase_hint = "REOBSERVE_QI_PROCESS"
        reason = "unknown_polarity_defaults_to_observation"

    return KuuOSDaemonFourImagePhaseResult(
        gauge_version="kuuos_runtime_daemon_four_image_phase_gauge_v0_1",
        yinyang_polarity_state=str(state) if state is not None else None,
        four_image_phase=phase,
        phase_reason=reason,
        phase_policy_hint=phase_hint,
        phase_maturity_score=maturity,
        yin_load=float(yin_load) if isinstance(yin_load, (int, float)) else None,
        yang_drive=float(yang_drive) if isinstance(yang_drive, (int, float)) else None,
        polarity_balance=float(balance) if isinstance(balance, (int, float)) else None,
        switch_risk=float(switch_risk) if isinstance(switch_risk, (int, float)) else None,
        allowed_projection=["daemon_four_image_phase_result", "phase_advisory"],
    )


def read_and_evaluate_daemon_four_image_phase(daemon_dir: Path) -> KuuOSDaemonFourImagePhaseResult:
    yy = read_and_evaluate_daemon_yinyang_polarity(daemon_dir)
    return evaluate_daemon_four_image_phase(yy.to_dict())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS daemon Four-Image phase gauge v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_evaluate_daemon_four_image_phase(args.daemon_dir)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
