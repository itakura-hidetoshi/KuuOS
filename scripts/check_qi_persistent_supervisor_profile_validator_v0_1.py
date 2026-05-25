#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_qi_persistent_supervisor_profile_v0_1.py"
EXAMPLE_PROFILE = ROOT / "examples" / "qi_persistent_supervisor_profile_v0_1" / "profile.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_validator(profile: pathlib.Path, write: pathlib.Path):
    return subprocess.run([
        sys.executable,
        str(VALIDATOR),
        "--profile",
        str(profile),
        "--write",
        str(write),
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)


def main() -> int:
    errors: list[str] = []
    for path in [VALIDATOR, EXAMPLE_PROFILE]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        valid_out = root / "valid_profile_result.json"
        completed = run_validator(EXAMPLE_PROFILE, valid_out)
        if completed.returncode != 0:
            errors.append(f"valid_validator_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not valid_out.is_file():
            errors.append("valid output missing")
        if not errors:
            result = load(valid_out)
            if result.get("validation_status") != "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID":
                errors.append("example profile should be valid")
            if result.get("blockers") != []:
                errors.append("example profile blockers should be empty")
            if result.get("profile_only") is not True:
                errors.append("profile_only mismatch")
            if result.get("read_only") is not True:
                errors.append("read_only mismatch")
            if result.get("grants_execution_authority") is not False:
                errors.append("execution authority mismatch")
            resolved = result.get("resolved_paths", {})
            for key in ["raw_state_path", "evidence_path", "control_path", "out_dir"]:
                if key not in resolved:
                    errors.append(f"resolved path missing: {key}")

        bad_profile = root / "bad_profile.json"
        bad_profile.write_text(json.dumps({
            "profile_version": "wrong_version",
            "raw_state_path": "missing_raw.json",
            "evidence_path": "missing_evidence.json",
            "control_path": "missing_control.json",
            "out_dir": "out",
            "max_outer_iterations": 0,
            "max_daemon_ticks": 0,
            "max_steps_per_tick": 0,
            "requested_max_reentry_cycles": -1,
            "sleep_seconds_between_iterations": -1,
            "authority": "run"
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        bad_out = root / "bad_profile_result.json"
        bad = run_validator(bad_profile, bad_out)
        if bad.returncode != 1:
            errors.append("bad profile should return 1")
        if not bad_out.is_file():
            errors.append("bad output missing")
        elif not errors:
            result = load(bad_out)
            blockers = result.get("blockers", [])
            expected = [
                "profile_version_mismatch",
                "path_not_found:raw_state_path",
                "path_not_found:evidence_path",
                "path_not_found:control_path",
                "max_outer_iterations_below_one",
                "max_daemon_ticks_below_one",
                "max_steps_per_tick_below_one",
                "requested_max_reentry_cycles_below_zero",
                "sleep_seconds_between_iterations_below_zero",
                "authority_not_none",
            ]
            for item in expected:
                if item not in blockers:
                    errors.append(f"bad profile missing blocker: {item}")
            if result.get("validation_status") != "QI_PERSISTENT_SUPERVISOR_PROFILE_BLOCKED":
                errors.append("bad profile should be blocked")
            if result.get("grants_memory_overwrite_authority") is not False:
                errors.append("bad profile memory overwrite authority mismatch")

        missing_out = root / "missing_profile_result.json"
        missing = run_validator(root / "missing_profile.json", missing_out)
        if missing.returncode != 1:
            errors.append("missing profile should return 1")
        if not missing_out.is_file():
            errors.append("missing profile output missing")
        elif not errors:
            result = load(missing_out)
            if "profile_not_found" not in result.get("blockers", []):
                errors.append("missing profile blocker missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent supervisor profile validator check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
