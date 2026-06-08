#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_path_integral_reentry_router_v10_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"physical_quantum_qi_path_integral_reentry_router_enabled": True, "apply_physical_quantum_qi_path_integral_reentry_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_ROUTER_LICENSE_READY", "final_readiness_packet_read_allowed": True, "path_integral_packet_read_allowed": True, "motion_bias_packet_read_allowed": True, "stage_feedback_action_intake_ledger_read_allowed": True, "reentry_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def final_packet(mem: str = "final_ready", plan: str = "final_ready", run: str = "final_ready") -> dict[str, Any]:
    action = {
        "MemoryOS": {"final_ready": "final_stage_append_only_recall_anchor_candidate", "final_needs_evidence": "final_stage_memory_evidence_request", "final_repair_required": "final_stage_memory_repair_quarantine"},
        "PlanOS": {"final_ready": "final_stage_weighted_candidate_front", "final_needs_evidence": "final_stage_plan_evidence_request", "final_repair_required": "final_stage_plan_repair_quarantine"},
        "RunGovernance": {"final_ready": "final_stage_bounded_queue_gate_candidate", "final_needs_evidence": "final_stage_run_governance_evidence_request", "final_repair_required": "final_stage_run_governance_repair_quarantine"},
    }
    return {
        "version": "tri_os_final_stage_readiness_router_packet_v10_4",
        "tri_os_final_stage_readiness_considered": True,
        "final_readiness": {
            "MemoryOS": {"final_readiness": mem, "final_stage_action": action["MemoryOS"].get(mem, "bad"), "history": {}},
            "PlanOS": {"final_readiness": plan, "final_stage_action": action["PlanOS"].get(plan, "bad"), "history": {}},
            "RunGovernance": {"final_readiness": run, "final_stage_action": action["RunGovernance"].get(run, "bad"), "history": {}},
        },
        "boundary": {"final_readiness_only": True, "does_not_authorize_execution": True, "final_ready_is_not_execution_authority": True},
    }


def path_integral() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_path_integral_packet_v8_3", "dominant_path": "light_progress", "stationary_path": "light_progress", "next_motion_bias": "stable_continue", "path_action_scores": {"light_progress": 0.7}, "path_amplitude_weights": {"light_progress": 0.6}, "boundary": {"path_integral_is_candidate_weighting_not_truth": True}}


def motion_bias() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_motion_bias_packet_v8_4", "motion_mode": "continue", "next_motion_bias": "stable_continue", "boundary": {"does_not_authorize_execution": True}}


def row(os_name: str, decision: str) -> dict[str, Any]:
    return {"record_type": "tri_os_stage_feedback_action_intake_decision", "target_os": os_name, "decision": decision, "record_digest": os_name + decision}


def run_case(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], rows: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    for r in rows:
        append_jsonl(runtime / "tri_os_stage_feedback_action_intake_decision_ledger.jsonl", r)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "physical_quantum_qi_path_integral_reentry_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_ROUTER_READY", case
    assert out["reentry_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["physical_quantum_qi_path_integral_reentry_considered"] is True, case
    assert packet["boundary"]["reentry_only"] is True, case
    assert packet["boundary"]["does_not_execute_path"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["candidate_weighting_not_truth"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        base = {"tri_os_final_stage_readiness_router_packet.json": final_packet(), "physical_quantum_qi_path_integral_packet.json": path_integral(), "physical_quantum_qi_motion_bias_packet.json": motion_bias()}
        rows = [row("MemoryOS", "accept"), row("PlanOS", "accept"), row("RunGovernance", "accept")]
        code, out, packet = run_case(root, "all_ready", base, rows, lic())
        assert_ready("all_ready", code, out, packet)
        assert out["dominant_reentry_mode"] == "reinforce_path_weight"
        assert packet["path_integral_reentry_counts"]["reinforce_path_weight"] == 3
        assert packet["os_reentry"]["PlanOS"]["path_integral_effect"]["path_weight_delta"] == 3

        mixed = {"tri_os_final_stage_readiness_router_packet.json": final_packet("final_ready", "final_needs_evidence", "final_ready"), "physical_quantum_qi_path_integral_packet.json": path_integral(), "physical_quantum_qi_motion_bias_packet.json": motion_bias()}
        code, out, packet = run_case(root, "probe", mixed, rows, lic())
        assert_ready("probe", code, out, packet)
        assert out["dominant_reentry_mode"] == "open_probe_potential"
        assert packet["os_reentry"]["PlanOS"]["path_integral_effect"]["probe_potential_required"] is True

        barrier = {"tri_os_final_stage_readiness_router_packet.json": final_packet("final_ready", "final_repair_required", "final_ready"), "physical_quantum_qi_path_integral_packet.json": path_integral(), "physical_quantum_qi_motion_bias_packet.json": motion_bias()}
        code, out, packet = run_case(root, "barrier", barrier, rows, lic())
        assert_ready("barrier", code, out, packet)
        assert out["dominant_reentry_mode"] == "add_barrier_potential"
        assert packet["os_reentry"]["PlanOS"]["path_integral_effect"]["barrier_potential_required"] is True
        assert packet["os_reentry"]["PlanOS"]["boundary"]["barrier_blocks_ready_weight"] is True

        no_pi = {"tri_os_final_stage_readiness_router_packet.json": final_packet(), "physical_quantum_qi_motion_bias_packet.json": motion_bias()}
        code, out, packet = run_case(root, "missing_path_integral_warn", no_pi, [], lic())
        assert_ready("missing_path_integral_warn", code, out, packet)
        assert "physical_quantum_qi_path_integral_packet_missing" in out["warnings"]
        assert "stage_feedback_action_intake_ledger_empty_or_missing" in out["warnings"]

        bad_final = final_packet()
        bad_final["tri_os_final_stage_readiness_considered"] = False
        code, out, packet = run_case(root, "bad_final", {"tri_os_final_stage_readiness_router_packet.json": bad_final, "physical_quantum_qi_path_integral_packet.json": path_integral()}, rows, lic())
        assert code == 1
        assert "tri_os_final_stage_readiness_considered_not_true" in out["blockers"]
        assert packet == {}

        bad_pi = path_integral()
        bad_pi["boundary"]["path_integral_is_candidate_weighting_not_truth"] = False
        code, out, packet = run_case(root, "bad_path_integral_boundary", {"tri_os_final_stage_readiness_router_packet.json": final_packet(), "physical_quantum_qi_path_integral_packet.json": bad_pi}, rows, lic())
        assert code == 1
        assert "path_integral_candidate_weighting_boundary_invalid" in out["blockers"]
        assert packet == {}

        bad_readiness = final_packet("bad", "final_ready", "final_ready")
        code, out, packet = run_case(root, "bad_readiness", {"tri_os_final_stage_readiness_router_packet.json": bad_readiness, "physical_quantum_qi_path_integral_packet.json": path_integral()}, rows, lic())
        assert code == 1
        assert "memoryos_final_readiness_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run_case(root, "license_block", base, rows, lic(reentry_packet_write_allowed=False))
        assert code == 1
        assert "reentry_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("physical_quantum_qi_path_integral_reentry_router_v10_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
