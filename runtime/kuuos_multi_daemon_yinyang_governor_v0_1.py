#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

YANG_POSTURES = {
    "CONTINUE_HARMONIZED",
    "BRANCH_EXPLORE_LIGHTLY",
    "CONTINUE_AFTER_COMPACT",
}

YIN_POSTURES = {
    "SLOW_DOWN_AND_REOBSERVE",
    "HOLD_WITH_RECOVERY",
    "QUARANTINE_WITH_RETURN_PATH",
    "CONTINUE_WITH_COMPACT_MONITOR",
}

@dataclass(frozen=True)
class MultiDaemonYinYangDecision:
    daemon_id: str
    yin_yang_phase: str
    local_posture: str
    phase_reason: str
    recommended_local_adjustment: str
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class MultiDaemonYinYangGovernorResult:
    governor_version: str
    governor_status: str
    multi_daemon_posture: str
    governor_reason: str
    daemon_count: int
    yang_count: int
    yin_count: int
    neutral_count: int
    phase_balance_score: float
    synchronized_risk_score: float
    decisions: list[dict[str, Any]]
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


def _posture(record: Mapping[str, Any]) -> str:
    return str(record.get("recommended_runtime_posture") or record.get("wa_posture") or "UNKNOWN_POSTURE")


def _daemon_id(record: Mapping[str, Any], index: int) -> str:
    return str(record.get("daemon_id") or f"daemon_{index:03d}")


def _phase_for_record(record: Mapping[str, Any], index: int) -> tuple[str, str, str]:
    posture = _posture(record)
    qique = str(record.get("qique_regime") or "")
    density = int(record.get("tick_density", 0) or 0)
    if posture in {"QUARANTINE_WITH_RETURN_PATH", "HOLD_WITH_RECOVERY"}:
        return "YIN_HOLD", posture, "hold_or_quarantine_posture"
    if posture in {"SLOW_DOWN_AND_REOBSERVE", "CONTINUE_WITH_COMPACT_MONITOR"}:
        return "YIN_OBSERVE", posture, "observe_or_compact_posture"
    if posture == "BRANCH_EXPLORE_LIGHTLY":
        return "YANG_EXPLORE", posture, "light_branch_posture"
    if posture in YANG_POSTURES:
        return "YANG_ACTIVE", posture, "active_continue_posture"
    if posture in YIN_POSTURES:
        return "YIN_COMPACT", posture, "yin_conservation_posture"
    if qique in {"OVERDIFFUSION", "RECOVERY_PRESSURE_HIGH"} or density >= 10:
        return "YIN_COMPACT", posture, "density_or_qique_requires_compact"
    return "BALANCED_ROTATION", posture, "neutral_or_unknown_posture"


def _counts(phases: Sequence[str]) -> tuple[int, int, int]:
    yang = sum(1 for p in phases if p.startswith("YANG"))
    yin = sum(1 for p in phases if p.startswith("YIN"))
    neutral = len(phases) - yang - yin
    return yang, yin, neutral


def evaluate_multi_daemon_yinyang_governor(records: Sequence[Mapping[str, Any]]) -> MultiDaemonYinYangGovernorResult:
    normalized = [dict(r) for r in records]
    decisions: list[MultiDaemonYinYangDecision] = []
    phases: list[str] = []
    for index, record in enumerate(normalized):
        phase, posture, reason = _phase_for_record(record, index)
        phases.append(phase)
        adjustment = "KEEP_PHASE_ADVISORY"
        if phase == "YANG_ACTIVE":
            adjustment = "ALLOW_LIGHT_TICK_ONLY"
        elif phase == "YANG_EXPLORE":
            adjustment = "STAGGER_BRANCHING"
        elif phase in {"YIN_OBSERVE", "YIN_COMPACT"}:
            adjustment = "OBSERVE_OR_COMPACT"
        elif phase == "YIN_HOLD":
            adjustment = "HOLD_WITH_RETURN_PATH"
        decisions.append(MultiDaemonYinYangDecision(
            daemon_id=_daemon_id(record, index),
            yin_yang_phase=phase,
            local_posture=posture,
            phase_reason=reason,
            recommended_local_adjustment=adjustment,
        ))

    count = len(phases)
    yang_count, yin_count, neutral_count = _counts(phases)
    if count == 0:
        return MultiDaemonYinYangGovernorResult(
            governor_version="kuuos_multi_daemon_yinyang_governor_v0_1",
            governor_status="YY_NO_DAEMONS",
            multi_daemon_posture="HOLD_CLUSTER",
            governor_reason="no_daemon_records",
            daemon_count=0,
            yang_count=0,
            yin_count=0,
            neutral_count=0,
            phase_balance_score=0.0,
            synchronized_risk_score=0.0,
            decisions=[],
            allowed_projection=["multi_daemon_yinyang_result", "phase_advisory"],
        )

    yang_ratio = yang_count / count
    yin_ratio = yin_count / count
    phase_balance = _clamp(1.0 - abs(yang_ratio - yin_ratio))
    synchronized_risk = _clamp(max(yang_ratio, yin_ratio) if count >= 2 else 0.0)

    if yang_ratio >= 0.75:
        posture = "STAGGER_TICKS_AND_COOL_DOWN"
        reason = "yang_overdense_cluster"
        status = "YY_YANG_OVERDENSE"
    elif yin_ratio >= 0.75:
        posture = "RELEASE_LIGHT_BRANCH"
        reason = "yin_overdense_cluster"
        status = "YY_YIN_OVERDENSE"
    elif yang_count > 0 and yin_count > 0:
        posture = "BALANCED_ROTATION"
        reason = "yin_yang_phases_present"
        status = "YY_BALANCED_ROTATION"
    elif neutral_count == count:
        posture = "ROTATE_ACTIVE_DAEMON"
        reason = "all_neutral_rotate_one"
        status = "YY_NEUTRAL_ROTATION"
    else:
        posture = "STAGGER_TICKS"
        reason = "mixed_but_unbalanced"
        status = "YY_STAGGER"

    return MultiDaemonYinYangGovernorResult(
        governor_version="kuuos_multi_daemon_yinyang_governor_v0_1",
        governor_status=status,
        multi_daemon_posture=posture,
        governor_reason=reason,
        daemon_count=count,
        yang_count=yang_count,
        yin_count=yin_count,
        neutral_count=neutral_count,
        phase_balance_score=phase_balance,
        synchronized_risk_score=synchronized_risk,
        decisions=[d.to_dict() for d in decisions],
        allowed_projection=["multi_daemon_yinyang_result", "phase_advisory"],
    )


def _load_records(path: Path) -> list[Mapping[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, list):
        return [v for v in value if isinstance(v, Mapping)]
    if isinstance(value, Mapping) and isinstance(value.get("daemons"), list):
        return [v for v in value["daemons"] if isinstance(v, Mapping)]
    raise ValueError("expected a list or {'daemons': [...]} payload")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate KuuOS multi-daemon Yin-Yang governor v0.1")
    parser.add_argument("--records", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = evaluate_multi_daemon_yinyang_governor(_load_records(args.records))
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
