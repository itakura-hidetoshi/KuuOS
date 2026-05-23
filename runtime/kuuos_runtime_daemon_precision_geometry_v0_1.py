#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
from typing import Any, Mapping

@dataclass(frozen=True)
class KuuOSPrecisionGeometry:
    geometry_version: str
    geometry_status: str
    precision_weights: dict[str, float]
    diagonal_metric: dict[str, float]
    coupling_hints: dict[str, float]
    geometry_reason: str
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


def _clamp(x: float, lo: float = 0.05, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def compile_precision_geometry(belief_manifold: Mapping[str, Any]) -> KuuOSPrecisionGeometry:
    coords = belief_manifold.get("belief_coordinates", {}) if isinstance(belief_manifold, Mapping) else {}
    xb = float(coords.get("x_boundary", 0.0) or 0.0)
    xu = float(coords.get("x_uncertainty", 0.0) or 0.0)
    xd = float(coords.get("x_density", 0.0) or 0.0)
    xr = float(coords.get("x_recovery", 0.0) or 0.0)
    xa = float(coords.get("x_action", 0.0) or 0.0)
    xm = float(coords.get("x_memory_continuity", 0.0) or 0.0)
    xn = float(coords.get("x_nonmarkov_pressure", 0.0) or 0.0)

    weights = {
        "g_boundary": _clamp(0.65 + 0.35 * xb),
        "g_uncertainty": _clamp(0.35 + 0.55 * xu),
        "g_density": _clamp(0.30 + 0.55 * xd),
        "g_recovery": _clamp(0.25 + 0.60 * xr),
        "g_action": _clamp(0.25 + 0.45 * xa - 0.20 * xb),
        "g_memory": _clamp(0.25 + 0.55 * xm),
        "g_nonmarkov": _clamp(0.20 + 0.65 * xn),
    }

    diagonal_metric = {
        "x_boundary": round(weights["g_boundary"], 6),
        "x_uncertainty": round(weights["g_uncertainty"], 6),
        "x_density": round(weights["g_density"], 6),
        "x_recovery": round(weights["g_recovery"], 6),
        "x_action": round(weights["g_action"], 6),
        "x_memory_continuity": round(weights["g_memory"], 6),
        "x_nonmarkov_pressure": round(weights["g_nonmarkov"], 6),
    }

    coupling_hints = {
        "boundary_action_coupling": round(_clamp(xb * (1.0 - xa), 0.0, 1.0), 6),
        "density_recovery_coupling": round(_clamp(xd * xr, 0.0, 1.0), 6),
        "memory_uncertainty_coupling": round(_clamp(xm * xu, 0.0, 1.0), 6),
        "nonmarkov_density_coupling": round(_clamp(xn * xd, 0.0, 1.0), 6),
    }

    return KuuOSPrecisionGeometry(
        geometry_version="kuuos_runtime_daemon_precision_geometry_v0_1",
        geometry_status="PRECISION_GEOMETRY_COMPILED",
        precision_weights={k: round(v, 6) for k, v in weights.items()},
        diagonal_metric=diagonal_metric,
        coupling_hints=coupling_hints,
        geometry_reason="belief_state_manifold_compiled_into_directional_precision_geometry",
        allowed_projection=["precision_geometry", "diagonal_metric_v0_1", "coupling_hints_advisory"],
    )


def read_and_compile_precision_geometry(daemon_dir: Path) -> KuuOSPrecisionGeometry:
    belief = _read_json(daemon_dir / "daemon_belief_state_manifold_v0_1.json") or {}
    return compile_precision_geometry(belief)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile KuuOS precision geometry v0.1")
    parser.add_argument("--daemon-dir", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = read_and_compile_precision_geometry(args.daemon_dir)
    if args.write:
        _write_json(args.daemon_dir / "daemon_precision_geometry_v0_1.json", result.to_dict())
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
