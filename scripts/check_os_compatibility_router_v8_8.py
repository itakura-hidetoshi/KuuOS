#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_os_compatibility_router_v8_8.py"


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
    return {"os_compatibility_router_enabled": True, "apply_os_compatibility_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "OS_COMPATIBILITY_ROUTER_LICENSE_READY", "qi_process_tensor_read_allowed": True, "path_integral_read_allowed": True, "motion_bias_read_allowed": True, "progress_outcome_read_allowed": True, "qi_que_read_allowed": True, "compatibility_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def coupling() -> dict[str, Any]:
    return {"version": "qi_process_tensor_policy_coupling_packet_v7_5", "qi_process_tensor_considered": True, "qi_state": "smooth_circulation", "boundary": {"non_markov_history_visible": True}}


def path_integral() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_path_integral_packet_v8_3", "physical_quantum_qi_path_integral_considered": True, "observe_only_bounded_motion_candidate": True, "dominant_path": "light_progress", "boundary": {"path_integral_is_candidate_weighting_not_truth": True}}


def motion() -> dict[str, Any]:
    return {"version": "physical_quantum_qi_motion_bias_packet_v8_4", "motion_mode": "continue", "boundary": {"does_not_authorize_execution": True, "path_integral_candidate_weighting_preserved": True}}


def qi_que() -> dict[str, Any]:
    return {"version": "qi_que_governance_packet_v0_1", "queued_bounded_execution": True, "exit_gate_visible": True}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], outcomes: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
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
    return done.returncode, load_json(op), load_json(runtime / "os_compatibility_router_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "OS_COMPATIBILITY_ROUTER_READY", case
    assert out["compatibility_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["os_compatibility_considered"] is True, case
    assert packet["boundary"]["router_only"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["does_not_convert_candidate_weighting_to_truth"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        all_files = {
            "qi_process_tensor_policy_coupling_packet.json": coupling(),
            "physical_quantum_qi_path_integral_packet.json": path_integral(),
            "physical_quantum_qi_motion_bias_packet.json": motion(),
            "qi_que_governance_packet.json": qi_que(),
        }
        code, out, packet = run(root, "all_high", all_files, [{"record_type": "progress_outcome", "progress_outcome_class": "progress_completed"}], lic())
        assert_ready("all_high", code, out, packet)
        assert packet["routes"]["memory_route"]["fit"] == "high"
        assert packet["routes"]["plan_route"]["fit"] == "high"
        assert packet["routes"]["run_governance_route"]["fit"] == "high"
        assert packet["dominant_route"] == "run_governance_route"

        code, out, packet = run(root, "memory_only", {"qi_process_tensor_policy_coupling_packet.json": coupling()}, [], lic())
        assert_ready("memory_only", code, out, packet)
        assert packet["dominant_route"] == "memory_route"
        assert packet["routes"]["memory_route"]["fit"] == "high"

        code, out, packet = run(root, "plan_only", {"physical_quantum_qi_path_integral_packet.json": path_integral()}, [], lic())
        assert_ready("plan_only", code, out, packet)
        assert packet["dominant_route"] == "plan_route"
        assert packet["routes"]["plan_route"]["fit"] == "high"

        code, out, packet = run(root, "partial_motion", {"physical_quantum_qi_motion_bias_packet.json": {"version": "x"}}, [], lic())
        assert_ready("partial_motion", code, out, packet)
        assert packet["routes"]["run_governance_route"]["fit"] == "partial"

        code, out, packet = run(root, "empty", {}, [], lic())
        assert code == 1
        assert "no_compatibility_sources_available" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", all_files, [], lic(compatibility_packet_write_allowed=False))
        assert code == 1
        assert "compatibility_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("os_compatibility_router_v8_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
