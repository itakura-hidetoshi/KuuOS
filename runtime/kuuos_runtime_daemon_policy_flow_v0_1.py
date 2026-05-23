#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import math
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSPolicyFlow:
    flow_version: str
    flow_status: str
    from_policy: str
    to_policy: str
    flow_distance: float
    flow_velocity: float
    oscillation_damping: float
    geodesic_waypoints: list[dict[str, Any]]
    policy_flow_reason: str
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


def _distance(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    keys = sorted(set(a.keys()) | set(b.keys()))
    return math.sqrt(sum((float(a.get(k, 0.0)) - float(b.get(k, 0.0))) ** 2 for k in keys))


def _interpolate(a: Mapping[str, float], b: Mapping[str, float], t: float) -> dict[str, float]:
    keys = sorted(set(a.keys()) | set(b.keys()))
    return {k: round((1.0 - t) * float(a.get(k, 0.0)) + t * float(b.get(k, 0.0)), 6) for k in keys}


def compile_policy_flow(efe_landscape: Mapping[str, Any], previous_policy: str | None = None) -> KuuOSPolicyFlow:
    coordinates = efe_landscape.get("policy_coordinates", {}) if isinstance(efe_landscape, Mapping) else {}
    if not isinstance(coordinates, Mapping) or not coordinates:
        coordinates = {
            "CONTINUE_HARMONIZED": {"actioniveness": 0.9, "boundary_intensity": 0.1, "observation_depth": 0.15, "recovery_depth": 0.1},
        }
    selected = str(efe_landscape.get("smoothed_selected_policy") or efe_landscape.get("selected_policy") or "CONTINUE_HARMONIZED")
    if selected not in coordinates:
        selected = "CONTINUE_HARMONIZED"
    prior = previous_policy if previous_policy in coordinates else str(efe_landscape.get("selected_policy") or selected)
    if prior not in coordinates:
        prior = selected

    start = coordinates[prior]
    end = coordinates[selected]
    distance = _distance(start, end)
    transition_distance = float(efe_landscape.get("transition_distance", distance) or distance)
    curvature = float(efe_landscape.get("curvature_barrier", 0.0) or 0.0)
    smoothing = float(efe_landscape.get("harmonic_smoothing_penalty", 0.0) or 0.0)

    damping = max(0.0, min(1.0, 1.0 / (1.0 + curvature + smoothing + transition_distance)))
    velocity = max(0.05, min(1.0, damping * (1.0 - min(distance, 1.0) * 0.35)))

    steps = 1 if distance == 0 else 4
    waypoints = []
    for i in range(steps + 1):
        t = i / max(steps, 1)
        waypoints.append({
            "step_index": i,
            "t": round(t, 6),
            "coordinates": _interpolate(start, end, t),
        })

    if prior == selected:
        status = "POLICY_FLOW_STABLE"
        reason = "smoothed_policy_matches_previous_policy"
    elif distance <= 0.35:
        status = "POLICY_FLOW_SMOOTH_LOCAL"
        reason = "near_policy_transition_on_manifold"
    else:
        status = "POLICY_FLOW_DAMPED_TRANSITION"
        reason = "far_policy_transition_damped_by_landscape_geometry"

    return KuuOSPolicyFlow(
        flow_version="kuuos_runtime_daemon_policy_flow_v0_1",
        flow_status=status,
        from_policy=prior,
        to_policy=selected,
        flow_distance=round(distance, 6),
        flow_velocity=round(velocity, 6),
        oscillation_damping=round(damping, 6),
        geodesic_waypoints=waypoints,
        policy_flow_reason=reason,
        allowed_projection=["policy_flow", "geodesic_waypoints_advisory", "nonexecuting_flow"],
    )


def read_and_compile_policy_flow(daemon_dir: Path) -> KuuOSPolicyFlow:
    landscape = _read_json(daemon_dir / "daemon_efe_landscape_v0_1.json") or {}
    daemon_result = _read_json(daemon_dir / "daemon_result_v0_1.json") or {}
    previous = daemon_result.get("efe_smoothed_selected_policy") if isinstance(daemon_result, Mapping) else None
    return compile_policy_flow(landscape, str(previous) if previous else None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS policy flow v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_policy_flow(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_policy_flow_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
