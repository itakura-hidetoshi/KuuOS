#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSBeliefStateManifold:
    manifold_version: str
    manifold_status: str
    belief_coordinates: dict[str, float]
    manifold_geometry_summary: dict[str, Any]
    manifold_reason: str
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


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def compile_belief_state_manifold(feature_bundle: Mapping[str, Any]) -> KuuOSBeliefStateManifold:
    inputs = feature_bundle.get("active_inference_inputs", {}) if isinstance(feature_bundle, Mapping) else {}
    priors = feature_bundle.get("preference_priors", {}) if isinstance(feature_bundle, Mapping) else {}
    constraints = feature_bundle.get("hard_constraints", {}) if isinstance(feature_bundle, Mapping) else {}

    tick_density = int(inputs.get("tick_density", 0) or 0)
    process_history_length = int(inputs.get("process_history_length", 0) or 0)
    transition_support_count = int(inputs.get("transition_support_count", 0) or 0)
    memory_support_count = int(inputs.get("memory_support_count", 0) or 0)
    nonmarkov_support_count = int(inputs.get("nonmarkov_support_count", 0) or 0)
    missing = int(inputs.get("missing_source_count", 0) or 0)

    yinyang = inputs.get("yinyang_polarity_state")
    four = inputs.get("four_image_phase")
    qique = inputs.get("qique_regime")
    emptiness = inputs.get("emptiness_action")
    wa = inputs.get("wa_posture")

    x_boundary = 1.0 if constraints.get("boundary_hard_constraint") else 0.0
    if emptiness == "HOLD_AND_COMPACT_TRACE":
        x_boundary = max(x_boundary, 0.75)

    x_uncertainty = _clamp(0.12 * missing)
    if constraints.get("observation_hard_constraint"):
        x_uncertainty = _clamp(x_uncertainty + 0.35)
    if yinyang in {"FALSE_YANG", "YIN_REOBSERVE_REQUIRED"}:
        x_uncertainty = _clamp(x_uncertainty + 0.2)

    x_density = _clamp(tick_density / 10.0)
    if four == "GREATER_YANG":
        x_density = _clamp(x_density + 0.25)
    if qique == "OVERDIFFUSION":
        x_density = _clamp(x_density + 0.25)

    x_recovery = 0.0
    if priors.get("prefer_recovery_path"):
        x_recovery = 0.8
    elif four == "GREATER_YIN":
        x_recovery = 0.6

    x_action = 0.0
    if wa in {"CONTINUE_HARMONIZED", "CONTINUE_AFTER_COMPACT", "CONTINUE_WITH_COMPACT_MONITOR"}:
        x_action = 0.7
    elif wa == "BRANCH_EXPLORE_LIGHTLY":
        x_action = 0.55

    continuity = transition_support_count + memory_support_count
    x_memory_continuity = _clamp(continuity / max(process_history_length, 1))

    x_nonmarkov_pressure = _clamp(nonmarkov_support_count / max(process_history_length, 1))
    if qique == "NONMARKOV_MEMORY_ACTIVE":
        x_nonmarkov_pressure = _clamp(x_nonmarkov_pressure + 0.2)

    coordinates = {
        "x_boundary": round(x_boundary, 6),
        "x_uncertainty": round(x_uncertainty, 6),
        "x_density": round(x_density, 6),
        "x_recovery": round(x_recovery, 6),
        "x_action": round(x_action, 6),
        "x_memory_continuity": round(x_memory_continuity, 6),
        "x_nonmarkov_pressure": round(x_nonmarkov_pressure, 6),
    }

    geometry = {
        "manifold_dimension": len(coordinates),
        "coordinate_system": "continuous_belief_coordinates",
        "geometry_mode": "nonmarkov_active_inference_state_space",
        "primary_driver": "qi_process_tensor",
        "optional_lenses_are_advisory": True,
        "hard_constraints_embedded": True,
        "preference_priors_embedded": True,
    }

    return KuuOSBeliefStateManifold(
        manifold_version="kuuos_runtime_daemon_belief_state_manifold_v0_1",
        manifold_status="BELIEF_STATE_MANIFOLD_COMPILED",
        belief_coordinates=coordinates,
        manifold_geometry_summary=geometry,
        manifold_reason="feature_bundle_compiled_into_continuous_belief_geometry",
        allowed_projection=["belief_state_manifold", "continuous_belief_coordinates"],
    )


def read_and_compile_belief_state_manifold(daemon_dir: Path) -> KuuOSBeliefStateManifold:
    feature_bundle = _read_json(daemon_dir / "daemon_active_inference_feature_bundle_v0_1.json") or {}
    return compile_belief_state_manifold(feature_bundle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS belief state manifold v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_belief_state_manifold(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_belief_state_manifold_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
