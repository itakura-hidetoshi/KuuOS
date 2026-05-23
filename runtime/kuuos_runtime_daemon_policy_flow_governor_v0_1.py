#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSPolicyFlowGovernor:
    governor_version: str
    governor_status: str
    current_policy: str
    target_policy: str
    governed_policy_advisory: str
    transition_mode: str
    ramp_fraction: float
    max_step_fraction: float
    flow_distance: float
    flow_velocity: float
    oscillation_damping: float
    governor_reason: str
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


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def compile_policy_flow_governor(policy_flow: Mapping[str, Any]) -> KuuOSPolicyFlowGovernor:
    current = str(policy_flow.get("from_policy") or "CONTINUE_HARMONIZED")
    target = str(policy_flow.get("to_policy") or current)
    distance = float(policy_flow.get("flow_distance", 0.0) or 0.0)
    velocity = float(policy_flow.get("flow_velocity", 0.0) or 0.0)
    damping = float(policy_flow.get("oscillation_damping", 1.0) or 1.0)

    if current == target or distance <= 0.05:
        governed = target
        mode = "STABLE_NO_RAMP"
        ramp = 1.0
        max_step = 1.0
        status = "POLICY_FLOW_GOVERNOR_STABLE"
        reason = "policy_flow_already_stable"
    elif distance <= 0.35 and damping >= 0.5:
        governed = target
        mode = "LOCAL_SMOOTH_ADOPT"
        ramp = _clamp(velocity)
        max_step = 1.0
        status = "POLICY_FLOW_GOVERNOR_LOCAL_ADVISORY"
        reason = "near_policy_transition_advisory_can_be_adopted"
    elif damping >= 0.35:
        governed = current
        mode = "RAMP_TOWARD_TARGET"
        ramp = _clamp(velocity * damping)
        max_step = 0.5
        status = "POLICY_FLOW_GOVERNOR_RAMP"
        reason = "far_policy_transition_requires_ramp"
    else:
        governed = current
        mode = "HOLD_TRANSITION_REOBSERVE"
        ramp = 0.0
        max_step = 0.0
        status = "POLICY_FLOW_GOVERNOR_HOLD_TRANSITION"
        reason = "low_damping_blocks_policy_jump"

    return KuuOSPolicyFlowGovernor(
        governor_version="kuuos_runtime_daemon_policy_flow_governor_v0_1",
        governor_status=status,
        current_policy=current,
        target_policy=target,
        governed_policy_advisory=governed,
        transition_mode=mode,
        ramp_fraction=round(ramp, 6),
        max_step_fraction=round(max_step, 6),
        flow_distance=round(distance, 6),
        flow_velocity=round(velocity, 6),
        oscillation_damping=round(damping, 6),
        governor_reason=reason,
        allowed_projection=["policy_flow_governor", "nonexecuting_policy_advisory", "transition_ramp_advisory"],
    )


def read_and_compile_policy_flow_governor(daemon_dir: Path) -> KuuOSPolicyFlowGovernor:
    flow = _read_json(daemon_dir / "daemon_policy_flow_v0_1.json") or {}
    return compile_policy_flow_governor(flow)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS policy flow governor v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_policy_flow_governor(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_policy_flow_governor_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
