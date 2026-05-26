#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "qi_supervisorctl_v0_1.py"
EXAMPLE_PROFILE = ROOT / "examples" / "qi_persistent_supervisor_profile_v0_1" / "profile.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_ctl(args: list[str]):
    return subprocess.run([sys.executable, str(CLI), *args], cwd=str(ROOT), text=True, capture_output=True, check=False)


def main() -> int:
    errors: list[str] = []
    for path in [CLI, EXAMPLE_PROFILE]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        validation_out = root / "validation.json"
        status_json = root / "status.json"
        status_text = root / "status.txt"

        completed = run_ctl(["validate", "--profile", str(EXAMPLE_PROFILE), "--write", str(validation_out), "--quiet"])
        if completed.returncode != 0:
            errors.append(f"validate_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not validation_out.is_file():
            errors.append("validation output missing")
        elif not errors:
            validation = load(validation_out)
            if validation.get("validation_status") != "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID":
                errors.append("validation should be valid")
            if validation.get("grants_execution_authority") is not False:
                errors.append("validation execution authority mismatch")

        completed = run_ctl([
            "allow",
            "--profile", str(EXAMPLE_PROFILE),
            "--max-cycles", "1",
            "--sleep-seconds-between-cycles", "0",
            "--reason", "supervisorctl e2e allow",
            "--quiet",
        ])
        if completed.returncode != 0:
            errors.append(f"allow_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())

        profile = load(EXAMPLE_PROFILE)
        profile_dir = EXAMPLE_PROFILE.parent
        control_path = (profile_dir / profile["control_path"]).resolve()
        compiled_control = control_path.with_name(control_path.stem + "_compiled_v0_1.json")
        if not control_path.is_file():
            errors.append("allow control missing")
        if not compiled_control.is_file():
            errors.append("allow compiled control missing")
        if not errors:
            control = load(control_path)
            compiled = load(compiled_control)
            if control.get("mode") != "allow":
                errors.append("allow mode mismatch")
            if compiled.get("loop_allowed") is not True:
                errors.append("allow compiled should allow")

        completed = run_ctl(["run", "--profile", str(EXAMPLE_PROFILE), "--quiet"])
        if completed.returncode != 0:
            errors.append(f"run_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())

        out_dir = (profile_dir / profile["out_dir"]).resolve()
        result_path = out_dir / "qi_persistent_supervisor_profile_result_v0_1.json"
        manifest_path = out_dir / "qi_persistent_supervisor_profile_operator_manifest_v0_1.json"
        validation_path = out_dir / "qi_persistent_supervisor_profile_validation_result_v0_1.json"
        for path in [result_path, manifest_path, validation_path]:
            if not path.is_file():
                errors.append(f"profile run output missing:{path.name}")
        if not errors:
            result = load(result_path)
            manifest = load(manifest_path)
            validation = load(validation_path)
            if result.get("supervisor_status") != "QI_PERSISTENT_SUPERVISOR_COMPLETED":
                errors.append("run supervisor status mismatch")
            if result.get("iterations_run") != 1:
                errors.append("run iterations mismatch")
            if validation.get("validation_status") != "QI_PERSISTENT_SUPERVISOR_PROFILE_VALID":
                errors.append("run preflight validation mismatch")
            if manifest.get("authority") != "none":
                errors.append("run manifest authority mismatch")

        completed = run_ctl([
            "status",
            "--profile", str(EXAMPLE_PROFILE),
            "--write-json", str(status_json),
            "--write-text", str(status_text),
            "--quiet",
        ])
        if completed.returncode != 0:
            errors.append(f"status_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not status_json.is_file():
            errors.append("status json missing")
        if not status_text.is_file():
            errors.append("status text missing")
        if not errors:
            status = load(status_json)
            text = status_text.read_text(encoding="utf-8")
            if status.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY":
                errors.append("status view should be ready")
            if status.get("process_tensor_advantage_score") is None:
                errors.append("status advantage score missing")
            if status.get("process_tensor_advantage_level") is None:
                errors.append("status advantage level missing")
            if status.get("recommended_next_process_focus") is None:
                errors.append("status recommended focus missing")
            if status.get("recommended_probe_type") is None:
                errors.append("status recommended probe missing")
            if status.get("probe_target_time_slice") is None:
                errors.append("status probe target missing")
            if status.get("probe_risk_level") is None:
                errors.append("status probe risk missing")
            probe_plan = status.get("latest_process_tensor_probe_plan", {})
            if probe_plan.get("probe_plan_only") is not True:
                errors.append("status probe plan should be proposal-only")
            if probe_plan.get("read_only") is not True:
                errors.append("status probe plan should be read-only")
            if probe_plan.get("authority") != "none":
                errors.append("status probe plan authority should be none")
            if probe_plan.get("grants_probe_execution_authority") is not False:
                errors.append("status probe plan authority mismatch")
            if "Qi Supervisorctl Status v0.1" not in text:
                errors.append("status text title missing")
            if "authority: none" not in text:
                errors.append("status text authority missing")
            if "process_tensor_advantage_score:" not in text:
                errors.append("status text advantage score missing")
            if "process_tensor_advantage_level:" not in text:
                errors.append("status text advantage level missing")
            if "recommended_next_process_focus:" not in text:
                errors.append("status text recommended focus missing")
            if "recommended_probe_type:" not in text:
                errors.append("status text recommended probe missing")
            if "probe_target_time_slice:" not in text:
                errors.append("status text probe target missing")
            if "probe_risk_level:" not in text:
                errors.append("status text probe risk missing")

        completed = run_ctl([
            "stop",
            "--profile", str(EXAMPLE_PROFILE),
            "--max-cycles", "1",
            "--reason", "supervisorctl e2e stop",
            "--quiet",
        ])
        if completed.returncode != 0:
            errors.append(f"stop_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not errors:
            stop_packet = load(control_path)
            stop_compiled = load(compiled_control)
            if stop_packet.get("mode") != "stop":
                errors.append("stop mode mismatch")
            if stop_compiled.get("loop_allowed") is not False:
                errors.append("stop compiled should block")
            if stop_compiled.get("control_reason") != "stop_requested":
                errors.append("stop reason mismatch")

        completed = run_ctl([
            "disable",
            "--profile", str(EXAMPLE_PROFILE),
            "--max-cycles", "1",
            "--reason", "supervisorctl e2e disable",
            "--quiet",
        ])
        if completed.returncode != 0:
            errors.append(f"disable_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not errors:
            disable_packet = load(control_path)
            disable_compiled = load(compiled_control)
            if disable_packet.get("mode") != "disable":
                errors.append("disable mode mismatch")
            if disable_compiled.get("loop_allowed") is not False:
                errors.append("disable compiled should block")
            if disable_compiled.get("control_reason") != "loop_disabled":
                errors.append("disable reason mismatch")

        bad = run_ctl(["allow", "--max-cycles", "0", "--control", str(root / "bad_control.json"), "--quiet"])
        if bad.returncode != 2:
            errors.append("bad allow should return 2")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi supervisorctl check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
