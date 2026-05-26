#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_CLI = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_artifact_index_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def artifact(probe_type: str, target: str, risk: str, gain: float, debt: float) -> dict:
    return {
        "artifact_status": "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY",
        "recommended_probe_type": probe_type,
        "probe_target_time_slice": target,
        "probe_risk_level": risk,
        "probe_expected_recoverability_gain": gain,
        "probe_expected_observation_debt_reduction": debt,
        "proposal_artifact_only": True,
        "read_only": True,
        "authority": "none",
        "grants_probe_execution_authority": False,
        "grants_next_tick_execution_authority": False,
        "grants_control_packet_authority": False,
        "grants_memory_overwrite_authority": False,
    }


def main() -> int:
    errors: list[str] = []
    if not INDEX_CLI.is_file():
        errors.append(f"missing:{INDEX_CLI}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        a0 = root / "a0.json"
        a1 = root / "a1.json"
        a2 = root / "a2.json"
        index_path = root / "index.json"
        bad = root / "bad.json"
        bad_index_path = root / "bad_index.json"
        dump(a0, artifact("observation_debt_probe", "t0", "medium", 0.1, 0.6))
        dump(a1, artifact("recoverability_branch_probe", "t1", "low", 0.5, 0.2))
        dump(a2, artifact("observation_debt_probe", "t2", "medium", 0.2, 0.7))

        completed = subprocess.run([
            sys.executable,
            str(INDEX_CLI),
            "--artifact", str(a0),
            "--artifact", str(a1),
            "--artifact", str(a2),
            "--write", str(index_path),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"index_cli_ready_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not index_path.is_file():
            errors.append("index output missing")
        else:
            index = load(index_path)
            if index.get("index_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY":
                errors.append("index should be ready")
            if index.get("dominant_probe_type") != "observation_debt_probe":
                errors.append("dominant probe mismatch")
            if index.get("latest_recommended_probe_type") != "observation_debt_probe":
                errors.append("latest probe mismatch")
            if index.get("latest_probe_target_time_slice") != "t2":
                errors.append("latest target mismatch")
            if index.get("repeated_probe_types") != ["observation_debt_probe"]:
                errors.append("repeated probe mismatch")
            if index.get("index_only") is not True:
                errors.append("index_only mismatch")
            if index.get("read_only") is not True:
                errors.append("read_only mismatch")
            if index.get("authority") != "none":
                errors.append("authority mismatch")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
            ]:
                if index.get(key) is not False:
                    errors.append(f"{key} should be false")

        bad_payload = artifact("observation_debt_probe", "t3", "high", 0.3, 0.8)
        bad_payload["grants_probe_execution_authority"] = True
        dump(bad, bad_payload)
        completed = subprocess.run([
            sys.executable,
            str(INDEX_CLI),
            "--artifact", str(bad),
            "--write", str(bad_index_path),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("bad index should return nonzero")
        if not bad_index_path.is_file():
            errors.append("bad index output missing")
        else:
            bad_index = load(bad_index_path)
            if bad_index.get("index_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_BLOCKED":
                errors.append("bad index status mismatch")
            if "artifact_0_grants_probe_execution_authority_not_false" not in bad_index.get("index_blockers", []):
                errors.append("bad index authority blocker missing")
            if bad_index.get("authority") != "none":
                errors.append("bad index authority mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor probe plan artifact index check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
