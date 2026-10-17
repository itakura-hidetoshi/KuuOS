#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "world_kuu_vacuum_central_reference_state_v0_54"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    manifest_path = ROOT / "manifests/world_kuu_vacuum_central_reference_state_v0_54.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["manifest_version"] == VERSION, "manifest version mismatch")
    require(
        manifest["predecessor"]
        == "world_vacuum_expectation_observeos_commit_verify_handoff_v0_53",
        "predecessor mismatch",
    )
    for key in (
        "formal_module",
        "formal_root",
        "aggregate_formal_root",
        "documentation",
        "validator",
        "full_check",
        "workflow",
    ):
        require((ROOT / manifest[key]).is_file(), f"manifest file missing: {key}")

    require(
        manifest["central_spine"]
        == [
            "reflection_positivity",
            "vacuum_correlations",
            "modular_reference_state",
            "araki_relative_entropy",
            "petz_recovery",
            "excitation_vectors",
            "excited_states",
        ],
        "central spine mismatch",
    )
    for field, value in manifest["boundaries"].items():
        require(value is False, f"authority or runtime boundary promoted: {field}")

    formal = ROOT / manifest["formal_module"]
    require_tokens(
        formal,
        (
            "WorldKuuVacuumCentralReferenceStateBridge",
            "centralReferenceState",
            "vacuumCorrelation",
            "vacuumTwoPoint",
            "excitationVector",
            "excitedState",
            "os_form_is_central_two_point",
            "central_reference_modular_invariant",
            "central_reference_exactly_recovered",
            "vacuum_recovery_entropy_equality",
            "central_reference_boundary_preserved",
        ),
    )
    require_tokens(
        ROOT / manifest["formal_root"],
        ("KuuVacuumCentralReferenceStateBridgeV0_54",),
    )
    require_tokens(
        ROOT / manifest["aggregate_formal_root"],
        ("KUOS.WORLD.KuuVacuumCentralReferenceStateBridgeV0_54",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_54",))

    documentation = ROOT / manifest["documentation"]
    require_tokens(
        documentation,
        (
            "中心基準状態",
            "反射陽性",
            "真空相関",
            "モジュラー理論",
            "相対エントロピー",
            "Petz回復",
            "励起状態",
            "central reference state != exact WORLD",
            "modular time != physical time",
        ),
    )

    predecessor = json.loads(
        (ROOT / "manifests/world_vacuum_expectation_observeos_commit_verify_handoff_v0_53.json").read_text(
            encoding="utf-8"
        )
    )
    require(
        predecessor["manifest_version"] == manifest["predecessor"],
        "v0.53 predecessor manifest mismatch",
    )

    print("WORLD Kuu vacuum central reference state v0.54 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
