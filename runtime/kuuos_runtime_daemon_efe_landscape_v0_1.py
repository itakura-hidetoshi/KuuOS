#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import math
from typing import Any, Mapping

POLICY_COORDINATES = {
    "CONTINUE_HARMONIZED": {"actioniveness": 0.90, "boundary_intensity": 0.10, "observation_depth": 0.15, "recovery_depth": 0.10},
    "CONTINUE_WITH_COMPACT_MONITOR": {"actioniveness": 0.70, "boundary_intensity": 0.25, "observation_depth": 0.35, "recovery_depth": 0.20},
    "CONTINUE_AFTER_COMPACT": {"actioniveness": 0.60, "boundary_intensity": 0.35, "observation_depth": 0.45, "recovery_depth": 0.25},
    "SLOW_DOWN_AND_REOBSERVE": {"actioniveness": 0.35, "boundary_intensity": 0.45, "observation_depth": 0.85, "recovery_depth": 0.35},
    "BRANCH_EXPLORE_LIGHTLY": {"actioniveness": 0.55, "boundary_intensity": 0.30, "observation_depth": 0.45, "recovery_depth": 0.55},
    "HOLD_WITH_RECOVERY": {"actioniveness": 0.20, "boundary_intensity": 0.65, "observation_depth": 0.65, "recovery_depth": 0.90},
    "QUARANTINE_WITH_RETURN_PATH": {"actioniveness": 0.05, "boundary_intensity": 0.95, "observation_depth": 0.80, "recovery_depth": 0.75},
}

@dataclass(frozen=True)
class KuuOSEFELandscape:
    landscape_version: str
    landscape_status: str
    selected_policy: str
    smoothed_selected_policy: str
    transition_distance: float
    curvature_barrier: float
    harmonic_smoothing_penalty: float
    landscape_table: dict[str, dict[str, float]]
    policy_coordinates: dict[str, dict[str, float]]
    landscape_reason: str
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


def _policy_distance(policy_a: str, policy_b: str) -> float:
    return _distance(POLICY_COORDINATES[policy_a], POLICY_COORDINATES[policy_b])


def compile_efe_landscape(
    active_inference_result: Mapping[str, Any],
    precision_geometry: Mapping[str, Any] | None = None,
    previous_policy: str | None = None,
) -> KuuOSEFELandscape:
    selected_policy = str(active_inference_result.get("selected_policy", "CONTINUE_HARMONIZED"))
    if selected_policy not in POLICY_COORDINATES:
        selected_policy = "CONTINUE_HARMONIZED"
    table = active_inference_result.get("policy_free_energy_table", {})
    if not isinstance(table, Mapping):
        table = {}
    precision = precision_geometry.get("precision_weights", {}) if isinstance(precision_geometry, Mapping) else {}
    g_boundary = float(precision.get("g_boundary", 0.65) or 0.65)
    g_density = float(precision.get("g_density", 0.35) or 0.35)
    g_recovery = float(precision.get("g_recovery", 0.35) or 0.35)
    g_nonmarkov = float(precision.get("g_nonmarkov", 0.35) or 0.35)

    prior_policy = previous_policy if previous_policy in POLICY_COORDINATES else selected_policy
    landscape_table: dict[str, dict[str, float]] = {}
    for policy, coord in POLICY_COORDINATES.items():
        efe = 1.0
        if policy in table and isinstance(table[policy], Mapping):
            efe = float(table[policy].get("expected_free_energy", 1.0) or 1.0)
        distance = _policy_distance(prior_policy, policy)
        curvature = (g_boundary * coord["boundary_intensity"] ** 2) + (g_density * coord["observation_depth"] * coord["actioniveness"]) + (g_nonmarkov * distance ** 2)
        smoothing = 0.25 * distance + 0.20 * g_nonmarkov * distance
        total = efe + curvature + smoothing - 0.10 * g_recovery * coord["recovery_depth"]
        landscape_table[policy] = {
            "expected_free_energy": round(efe, 6),
            "transition_distance": round(distance, 6),
            "curvature_barrier": round(curvature, 6),
            "harmonic_smoothing_penalty": round(smoothing, 6),
            "landscape_energy": round(max(0.0, total), 6),
        }

    smoothed = min(landscape_table, key=lambda p: landscape_table[p]["landscape_energy"])
    transition_distance = landscape_table[smoothed]["transition_distance"]
    curvature_barrier = landscape_table[smoothed]["curvature_barrier"]
    smoothing_penalty = landscape_table[smoothed]["harmonic_smoothing_penalty"]

    return KuuOSEFELandscape(
        landscape_version="kuuos_runtime_daemon_efe_landscape_v0_1",
        landscape_status="EFE_LANDSCAPE_COMPILED",
        selected_policy=selected_policy,
        smoothed_selected_policy=smoothed,
        transition_distance=round(transition_distance, 6),
        curvature_barrier=round(curvature_barrier, 6),
        harmonic_smoothing_penalty=round(smoothing_penalty, 6),
        landscape_table=landscape_table,
        policy_coordinates=POLICY_COORDINATES,
        landscape_reason="expected_free_energy_table_lifted_to_policy_manifold_with_precision_curvature",
        allowed_projection=["efe_landscape", "policy_manifold", "smoothed_policy_advisory"],
    )


def read_and_compile_efe_landscape(daemon_dir: Path) -> KuuOSEFELandscape:
    active = _read_json(daemon_dir / "daemon_active_inference_kernel_result_v0_1.json") or {}
    precision = _read_json(daemon_dir / "daemon_precision_geometry_v0_1.json") or {}
    daemon_result = _read_json(daemon_dir / "daemon_result_v0_1.json") or {}
    previous_policy = daemon_result.get("active_inference_selected_policy") if isinstance(daemon_result, Mapping) else None
    return compile_efe_landscape(active, precision, str(previous_policy) if previous_policy else None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS EFE landscape v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_efe_landscape(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_efe_landscape_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
