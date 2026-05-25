#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_persistent_supervisor_profile_v0_1.py"
EXAMPLE_PROFILE = ROOT / "examples" / "qi_persistent_supervisor_profile_v0_1" / "profile.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for path in [CLI, EXAMPLE_PROFILE]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--profile",
        str(EXAMPLE_PROFILE),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        errors.append(f"profile_cli_returned:{completed.returncode}")
        errors.append(completed.stderr.strip() or completed.stdout.strip())

    profile = load(EXAMPLE_PROFILE)
    out_dir = (EXAMPLE_PROFILE.parent / profile["out_dir"]).resolve()
    result_path = out_dir / "qi_persistent_supervisor_profile_result_v0_1.json"
    overview_path = out_dir / "qi_persistent_supervisor_profile_overview_v0_1.txt"
    operator_manifest_path = out_dir / "qi_persistent_supervisor_profile_operator_manifest_v0_1.json"
    supervisor_manifest_path = out_dir / "qi_persistent_supervisor_manifest_v0_1.json"
    for path in [result_path, overview_path, operator_manifest_path, supervisor_manifest_path]:
        if not path.is_file():
            errors.append(f"missing profile output:{path.name}")
    if not errors:
        result = load(result_path)
        operator_manifest = load(operator_manifest_path)
        overview = overview_path.read_text(encoding="utf-8")
        if result.get("supervisor_status") != "QI_PERSISTENT_SUPERVISOR_COMPLETED":
            errors.append("profile supervisor status mismatch")
        if result.get("iterations_run") != 1:
            errors.append("profile iterations mismatch")
        if result.get("persistent_supervisor_only") is not True:
            errors.append("profile persistent flag mismatch")
        if result.get("grants_execution_authority") is not False:
            errors.append("profile execution authority mismatch")
        if operator_manifest.get("scope") != "persistent_supervisor_profile_bounded_read_only":
            errors.append("profile operator scope mismatch")
        if operator_manifest.get("authority") != "none":
            errors.append("profile operator authority mismatch")
        if "Qi Persistent Supervisor Profile" not in overview:
            errors.append("profile overview title missing")
        if "authority: none" not in overview:
            errors.append("profile overview authority missing")

    with tempfile.TemporaryDirectory() as tmp:
        bad_profile = pathlib.Path(tmp) / "bad_profile.json"
        bad_profile.write_text(json.dumps({
            "profile_version": "qi_persistent_supervisor_profile_v0_1",
            "raw_state_path": "missing_raw.json",
            "evidence_path": "missing_evidence.json",
            "control_path": "missing_control.json",
            "out_dir": "out",
            "max_outer_iterations": 0
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        bad = subprocess.run([
            sys.executable,
            str(CLI),
            "--profile",
            str(bad_profile),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if bad.returncode != 2:
            errors.append("bad profile should return 2")
        if not bad.stderr:
            errors.append("bad profile should print errors")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent supervisor profile runner check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
