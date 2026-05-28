#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_one_shot_probe_executor_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


GRANT = {
    "gate_status": "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY",
    "grant_outcome": "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED",
    "authorized_probe_type": "observation_debt_probe",
    "authority_scope": "single_probe_execution_candidate_review",
    "authority_token_kind": "single_use_probe_execution_authority",
    "grants_probe_execution_authority": True,
    "grants_execution_authority": True,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_scheduler_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "one_shot": True,
    "single_probe_only": True,
    "rollback_required": True,
    "reentry_window_bound": True,
    "authority_expires_after_use": True,
    "authority_revocable": True,
    "memory_write_allowed": False,
    "world_update_allowed": False,
    "control_packet_mutation_allowed": False,
    "probe_execution_performed": False,
    "dry_run_execution_performed": False,
    "next_tick_execution_performed": False,
    "scheduler_state_mutation_performed": False,
    "control_packet_mutation_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
}

PAYLOAD = {
    "probe_result_kind": "qi_probe_observation_debt_result",
    "probe_result_summary": "observation debt probe result artifact only",
    "token_already_consumed": False,
    "request_multi_probe": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        grant = root / "grant.json"
        payload = root / "payload.json"
        out = root / "result.json"
        dump(grant, GRANT)
        dump(payload, PAYLOAD)
        completed = subprocess.run([
            sys.executable, str(CLI), "--grant", str(grant), "--probe-payload", str(payload), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("result_output_missing")
        else:
            value = load(out)
            if value.get("execution_status") != "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED":
                errors.append("execution_status_mismatch")
            if value.get("probe_execution_performed") is not True:
                errors.append("probe_execution_performed_not_true")
            if value.get("one_shot_token_consumed") is not True:
                errors.append("one_shot_token_consumed_not_true")
            if value.get("token_reuse_allowed") is not False:
                errors.append("token_reuse_allowed_not_false")
            if value.get("probe_result_artifact_only") is not True:
                errors.append("probe_result_artifact_only_not_true")
            for key in [
                "grants_probe_execution_authority",
                "grants_execution_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
                "memory_write_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "scheduler_state_mutation_performed",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_payload = dict(PAYLOAD)
        bad_payload["token_already_consumed"] = True
        dump(payload, bad_payload)
        completed = subprocess.run([
            sys.executable, str(CLI), "--grant", str(grant), "--probe-payload", str(payload), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("execution_status") != "QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED":
                errors.append("blocked_execution_status_mismatch")
            if "token_already_consumed" not in value.get("execution_blockers", []):
                errors.append("token_reuse_blocker_missing")
            if value.get("probe_execution_performed") is not False:
                errors.append("blocked_probe_execution_performed_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi one-shot probe executor check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
