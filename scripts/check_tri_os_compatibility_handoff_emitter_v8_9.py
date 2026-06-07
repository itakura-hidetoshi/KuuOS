#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_compatibility_handoff_emitter_v8_9.py"


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
    return {"tri_os_compatibility_handoff_emitter_enabled": True, "apply_tri_os_compatibility_handoff_emitter": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_LICENSE_READY", "router_packet_read_allowed": True, "source_packets_read_allowed": True, "memory_handoff_write_allowed": True, "plan_handoff_write_allowed": True, "run_governance_handoff_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def router() -> dict[str, Any]:
    return {"version": "os_compatibility_router_packet_v8_8", "os_compatibility_considered": True, "dominant_route": "run_governance_route", "routes": {"memory_route": {"fit": "high"}, "plan_route": {"fit": "high"}, "run_governance_route": {"fit": "high"}}, "boundary": {"does_not_authorize_execution": True}}


def coupling() -> dict[str, Any]:
    return {"version": "qi_process_tensor_policy_coupling_packet_v7_5", "qi_state": "smooth_circulation", "process_memory_depth": 5, "boundary": {"non_markov_history_visible": True}}


def path_integral() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_path_integral_packet_v8_3", "dominant_path": "light_progress", "stationary_path": "light_progress", "next_motion_bias": "stable_continue", "path_action_scores": {"light_progress": 0.7}, "path_amplitude_weights": {"light_progress": 0.6}}


def motion() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_motion_bias_packet_v8_4", "dominant_path": "light_progress", "next_motion_bias": "stable_continue", "motion_mode": "continue", "progress_action": "advance_light", "small_probe_required": False, "review_exit_required": False}


def qi_que() -> dict[str, Any]:
    return {"version": "qi_que_governance_packet_v0_1", "queued_bounded_execution": True, "exit_gate_visible": True}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], outcomes: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    for row in outcomes:
        append_jsonl(runtime / "qi_progress_outcome_ledger.jsonl", row)
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
        load_json(runtime / "memory_os_qi_process_tensor_handoff_packet.json"),
        load_json(runtime / "plan_os_physical_quantum_qi_handoff_packet.json"),
        load_json(runtime / "run_governance_qi_que_handoff_packet.json"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], mem: dict[str, Any], plan: dict[str, Any], run_packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_COMPATIBILITY_HANDOFF_EMITTER_READY", case
    assert out["handoffs_written"] == 3, case
    assert not out["blockers"], case
    assert mem["boundary"]["does_not_overwrite_memory"] is True, case
    assert plan["boundary"]["candidate_weighting_not_truth"] is True, case
    assert run_packet["boundary"]["queue_gate_required"] is True, case
    assert run_packet["boundary"]["does_not_authorize_execution"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        files = {
            "os_compatibility_router_packet.json": router(),
            "qi_process_tensor_policy_coupling_packet.json": coupling(),
            "physical_quantum_qi_path_integral_packet.json": path_integral(),
            "physical_quantum_qi_motion_bias_packet.json": motion(),
            "qi_que_governance_packet.json": qi_que(),
        }
        code, out, mem, plan, run_packet = run(root, "all", files, [{"record_type": "progress_outcome", "progress_outcome_class": "progress_completed"}], lic())
        assert_ready("all", code, out, mem, plan, run_packet)
        assert mem["target_os"] == "MemoryOS"
        assert plan["target_os"] == "PlanOS"
        assert run_packet["target_os"] == "RunGovernance"
        assert plan["plan_candidates"]["dominant_path"] == "light_progress"

        code, out, mem, plan, run_packet = run(root, "router_only", {"os_compatibility_router_packet.json": router()}, [], lic())
        assert_ready("router_only", code, out, mem, plan, run_packet)
        assert "qi_process_tensor_coupling_missing" in out["warnings"]
        assert mem["route_fit"] == "high"

        code, out, mem, plan, run_packet = run(root, "missing_router", {}, [], lic())
        assert code == 1
        assert "os_compatibility_router_packet_missing_or_invalid" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        bad_router = router()
        bad_router["os_compatibility_considered"] = False
        code, out, mem, plan, run_packet = run(root, "bad_router", {"os_compatibility_router_packet.json": bad_router}, [], lic())
        assert code == 1
        assert "os_compatibility_considered_not_true" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}

        code, out, mem, plan, run_packet = run(root, "license_block", files, [], lic(plan_handoff_write_allowed=False))
        assert code == 1
        assert "plan_handoff_write_not_allowed" in out["blockers"]
        assert mem == {} and plan == {} and run_packet == {}
    print("tri_os_compatibility_handoff_emitter_v8_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
