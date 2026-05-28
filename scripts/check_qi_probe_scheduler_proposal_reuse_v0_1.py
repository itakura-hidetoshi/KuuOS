#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_probe_scheduler_proposal_reuse_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


APPLY = {
    "apply_status": "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED",
    "next_scheduler_state": {
        "scheduler_update_kind": "memoryos_process_tensor_replay_hint",
        "replay_dominant_probe_type": "observation_debt_probe",
        "replay_scheduler_reuse_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
        "replay_probe_planner_reuse_hint": "prioritize_probe_family_observation_debt_probe",
        "lineage_preserved": True,
    },
}

CTX = {
    "reuse_scope": "proposal_only",
    "request_scheduler_state_mutation": False,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        apply = root / "apply.json"
        ctx = root / "ctx.json"
        out = root / "reuse.json"
        dump(apply, APPLY)
        dump(ctx, CTX)
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler-apply", str(apply), "--context", str(ctx), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("reuse_output_missing")
        else:
            value = load(out)
            if value.get("reuse_status") != "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY":
                errors.append("reuse_status_mismatch")
            if value.get("proposal_reuse_only") is not True:
                errors.append("proposal_reuse_only_not_true")
            if value.get("schedule_proposal_only") is not True:
                errors.append("schedule_proposal_only_not_true")
            if value.get("scheduler_state_read_performed") is not True:
                errors.append("scheduler_state_read_not_true")
            if value.get("scheduler_state_mutation_performed") is not False:
                errors.append("scheduler_state_mutation_not_false")
            if value.get("reused_probe_family") != "observation_debt_probe":
                errors.append("reused_probe_family_mismatch")
            if value.get("proposed_revisit_after_ticks") != 1:
                errors.append("proposed_revisit_ticks_mismatch")
            for key in [
                "memory_write_performed",
                "world_update_performed",
                "control_packet_mutation_performed",
                "probe_execution_performed",
                "grants_scheduler_authority",
                "grants_memory_write_authority",
                "grants_world_update_authority",
                "grants_probe_execution_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_ctx = dict(CTX)
        bad_ctx["request_probe_execution"] = True
        dump(ctx, bad_ctx)
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler-apply", str(apply), "--context", str(ctx), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("reuse_status") != "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_BLOCKED":
                errors.append("blocked_reuse_status_mismatch")
            if "request_probe_execution" not in value.get("reuse_blockers", []):
                errors.append("probe_execution_blocker_missing")
            if value.get("probe_execution_performed") is not False:
                errors.append("blocked_probe_execution_not_false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi probe scheduler proposal reuse check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
