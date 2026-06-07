#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_readiness_stage_emitter_v9_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_readiness_stage_emitter_enabled": True, "apply_tri_os_readiness_stage_emitter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_READINESS_STAGE_EMITTER_LICENSE_READY", "readiness_packet_read_allowed": True, "memory_stage_write_allowed": True, "plan_stage_write_allowed": True, "run_governance_stage_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def readiness(mem: str = "ready", plan: str = "ready", run: str = "ready") -> dict[str, Any]:
    action = {
        "MemoryOS": {"ready": "stage_append_only_recall_anchor", "needs_evidence": "stage_memory_reobserve_request", "repair_required": "stage_memory_repair_quarantine"},
        "PlanOS": {"ready": "stage_weighted_candidate_front", "needs_evidence": "stage_redecomposition_evidence_request", "repair_required": "stage_plan_handoff_repair_quarantine"},
        "RunGovernance": {"ready": "stage_bounded_queue_gate_candidate", "needs_evidence": "stage_exit_blocker_review_request", "repair_required": "stage_governance_repair_quarantine"},
    }
    return {
        "version": "tri_os_feedback_action_readiness_router_packet_v9_6",
        "tri_os_feedback_action_readiness_considered": True,
        "readiness": {
            "MemoryOS": {"readiness": mem, "next_stage_action": action["MemoryOS"].get(mem, "bad"), "history": {}},
            "PlanOS": {"readiness": plan, "next_stage_action": action["PlanOS"].get(plan, "bad"), "history": {}},
            "RunGovernance": {"readiness": run, "next_stage_action": action["RunGovernance"].get(run, "bad"), "history": {}},
        },
        "boundary": {"readiness_only": True, "does_not_authorize_execution": True},
    }


def run_case(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "tri_os_feedback_action_readiness_router_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return (
        done.returncode,
        load_json(op),
        load_json(runtime / "memory_os_readiness_stage_packet.json"),
        load_json(runtime / "plan_os_readiness_stage_packet.json"),
        load_json(runtime / "run_governance_readiness_stage_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], mem: dict[str, Any], plan: dict[str, Any], run_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_READINESS_STAGE_EMITTER_READY", case
    assert out["stage_packets_written"] == 3, case
    assert not out["blockers"], case
    assert mem["boundary"]["does_not_overwrite_memory"] is True, case
    assert plan["boundary"]["does_not_commit_plan"] is True, case
    assert run_packet["boundary"]["does_not_run_runner"] is True, case
    assert run_packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, mem, plan, run_packet = run_case(root, "all_ready", readiness(), lic())
        assert_ready("all_ready", code, out, mem, plan, run_packet)
        assert mem["stage_mode"] == "stage_candidate"
        assert plan["stage_mode"] == "stage_candidate"
        assert run_packet["stage_mode"] == "stage_candidate"

        code, out, mem, plan, run_packet = run_case(root, "mixed", readiness("needs_evidence", "repair_required", "ready"), lic())
        assert_ready("mixed", code, out, mem, plan, run_packet)
        assert mem["stage_mode"] == "stage_reobserve_request"
        assert plan["stage_mode"] == "stage_repair_quarantine"
        assert run_packet["stage_mode"] == "stage_candidate"
        assert plan["boundary"]["repair_required_blocks_ready_state"] is True

        code, out, mem, plan, run_packet = run_case(root, "missing", None, lic())
        assert code == 1
        assert "tri_os_feedback_action_readiness_router_packet_missing_or_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad = readiness()
        bad["tri_os_feedback_action_readiness_considered"] = False
        code, out, mem, plan, run_packet = run_case(root, "bad_considered", bad, lic())
        assert code == 1
        assert "tri_os_feedback_action_readiness_considered_not_true" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad_value = readiness("bad", "ready", "ready")
        code, out, mem, plan, run_packet = run_case(root, "bad_readiness", bad_value, lic())
        assert code == 1
        assert "memoryos_readiness_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        code, out, mem, plan, run_packet = run_case(root, "license_block", readiness(), lic(plan_stage_write_allowed=False))
        assert code == 1
        assert "plan_stage_write_not_allowed" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}
    print("tri_os_readiness_stage_emitter_v9_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
