#!/usr/bin/env python3
"""Run migrated high-cost PR checks without repeating global Lean/runtime gates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time
from collections.abc import Sequence
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK_IDS = {"world-v053-v059", "memoryos-world-observe-v039"}


def build_commands(check_id: str) -> list[list[str]]:
    python = sys.executable
    if check_id == "world-v053-v059":
        return [
            [
                python,
                "-m",
                "compileall",
                "-q",
                "scripts/check_world_vacuum_expectation_observeos_commit_verify_handoff_v0_53.py",
                "scripts/check_world_kuu_vacuum_central_reference_state_v0_54.py",
                "scripts/check_world_kuu_vacuum_information_geometry_v0_55.py",
                "scripts/check_world_kuu_vacuum_araki_hessian_physical_realization_v0_56.py",
                "scripts/check_world_four_great_phase_dynamics_v0_59.py",
            ],
            [python, "scripts/check_world_vacuum_expectation_observeos_commit_verify_handoff_v0_53.py"],
            [python, "scripts/check_world_kuu_vacuum_central_reference_state_v0_54.py"],
            [python, "scripts/check_world_kuu_vacuum_information_geometry_v0_55.py"],
            [python, "scripts/check_world_kuu_vacuum_araki_hessian_physical_realization_v0_56.py"],
            [python, "scripts/check_world_four_great_phase_dynamics_v0_59.py"],
        ]
    if check_id == "memoryos-world-observe-v039":
        return [
            [
                python,
                "-m",
                "compileall",
                "-q",
                "runtime/kuuos_memoryos_world_observe_intake_v0_39.py",
                "tests/test_memoryos_world_observe_intake_v0_39.py",
                "scripts/check_memoryos_world_observe_intake_v0_39.py",
                "runtime/kuuos_memoryos_analytic_hilbert_context_v0_38.py",
                "tests/test_memoryos_analytic_hilbert_context_v0_38.py",
                "scripts/check_memoryos_analytic_hilbert_context_v0_38.py",
            ],
            [python, "-m", "json.tool", "manifests/kuuos_memoryos_world_observe_intake_v0_39.json"],
            [python, "-m", "json.tool", "manifests/kuuos_memoryos_analytic_hilbert_context_v0_38.json"],
            [python, "scripts/check_memoryos_world_observe_intake_v0_39.py"],
            [python, "-m", "unittest", "-v", "tests.test_memoryos_world_observe_intake_v0_39"],
            [python, "scripts/check_memoryos_analytic_hilbert_context_v0_38.py"],
            [python, "-m", "unittest", "-v", "tests.test_memoryos_analytic_hilbert_context_v0_38"],
            [python, "scripts/check_world_vacuum_expectation_observation_candidate_v0_50.py"],
        ]
    raise ValueError(f"unsupported check id: {check_id}")


REQUIRED_MARKERS = {
    "world-v053-v059": {
        "formal/KUOS.lean": [
            "import KUOS.WORLD.VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_53",
            "import KUOS.WORLD.KuuVacuumCentralReferenceStateBridgeV0_54",
            "import KUOS.WORLD.KuuVacuumInformationGeometryBridgeV0_55",
            "import KUOS.WORLD.KuuVacuumArakiHessianOSTransportV0_56",
            "import KUOS.WORLD.TomitaClosedGraphIsometryV0_57",
            "import KUOS.WORLD.TomitaConjugateAdjointClosedV0_58",
            "import KUOS.WORLD.FourGreatPhaseDynamicsCoreBridgeV0_59",
        ],
        "formal/KuuOSFormal.lean": [
            "import KUOS.WORLD.TomitaClosedGraphIsometryV0_57",
            "import KUOS.WORLD.TomitaConjugateAdjointClosedV0_58",
            "import KUOS.WORLD.FourGreatPhaseDynamicsCoreBridgeV0_59",
        ],
    },
    "memoryos-world-observe-v039": {
        "formal/KUOS.lean": [
            "import KUOS.OpenHorizon.MemoryOSWorldObserveIntakeKernelV0_39",
            "import KUOS.OpenHorizon.MemoryOSAnalyticHilbertContextKernelV0_38",
        ]
    },
}


def run_command(command: Sequence[str]) -> dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    start_clock = time.monotonic()
    print("\n>>> " + " ".join(command), flush=True)
    completed = subprocess.run(list(command), cwd=ROOT, check=False)
    return {
        "command": list(command),
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
        "duration_seconds": round(time.monotonic() - start_clock, 3),
        "started_at": started.isoformat(),
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def check_markers(check_id: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for relative, markers in REQUIRED_MARKERS[check_id].items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for marker in markers:
            passed = marker in text
            results.append(
                {
                    "file": relative,
                    "marker": marker,
                    "status": "passed" if passed else "failed",
                }
            )
            print(f"{'PASS' if passed else 'FAIL'}: {relative}: {marker}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-id", choices=sorted(CHECK_IDS), required=True)
    parser.add_argument("--output-root", type=pathlib.Path, default=ROOT / "artifacts/checks")
    args = parser.parse_args()

    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output_dir = output_root / args.check_id
    output_dir.mkdir(parents=True, exist_ok=True)

    command_results = [run_command(command) for command in build_commands(args.check_id)]
    marker_results = check_markers(args.check_id)
    failed_commands = [item for item in command_results if item["status"] != "passed"]
    failed_markers = [item for item in marker_results if item["status"] != "passed"]
    status = "passed" if not failed_commands and not failed_markers else "failed"
    summary = {
        "schema_version": "0.5",
        "check_id": args.check_id,
        "status": status,
        "commands": command_results,
        "markers": marker_results,
        "failed_command_count": len(failed_commands),
        "failed_marker_count": len(failed_markers),
        "delegated_global_checks": ["runtime-full", "lean-formal"],
        "authority_boundary": (
            "deduplication != validation weakening; validation != truth; "
            "CI pass != theorem authority"
        ),
    }
    (output_dir / "subsystem-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
