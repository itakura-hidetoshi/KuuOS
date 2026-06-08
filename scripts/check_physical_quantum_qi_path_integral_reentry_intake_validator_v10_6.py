#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_path_integral_reentry_intake_validator_v10_6.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"physical_quantum_qi_path_integral_reentry_intake_validator_enabled": True, "apply_physical_quantum_qi_path_integral_reentry_intake_validator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_VALIDATOR_LICENSE_READY", "reentry_packet_read_allowed": True, "reentry_intake_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def os_item(os_name: str, mode: str = "reinforce_path_weight", *, execute: bool = False, candidate: bool = True, probe_visible: bool = True, barrier_visible: bool = True, barrier_blocks: bool = True, delta: int | None = None) -> dict[str, Any]:
    if delta is None:
        delta = {"reinforce_path_weight": 3, "open_probe_potential": 1, "add_barrier_potential": -4}.get(mode, -4)
    return {
        "target_os": os_name,
        "source_final_readiness": {"reinforce_path_weight": "final_ready", "open_probe_potential": "final_needs_evidence", "add_barrier_potential": "final_repair_required"}.get(mode, "final_repair_required"),
        "reentry_mode": mode,
        "path_integral_effect": {
            "dominant_path_hint": "light_progress",
            "path_weight_delta": delta,
            "probe_potential_required": mode == "open_probe_potential" and probe_visible,
            "barrier_potential_required": mode == "add_barrier_potential" and barrier_visible,
            "stationary_phase_preserved": mode == "reinforce_path_weight",
        },
        "boundary": {
            "reentry_only": True,
            "does_not_execute_path": not execute,
            "does_not_authorize_execution": not execute,
            "path_integral_candidate_weighting_only": candidate,
            "barrier_blocks_ready_weight": mode == "add_barrier_potential" and barrier_blocks,
        },
    }


def reentry(mem: str = "reinforce_path_weight", plan: str = "reinforce_path_weight", run: str = "reinforce_path_weight") -> dict[str, Any]:
    return {
        "version": "physical_quantum_qi_path_integral_reentry_packet_v10_5",
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": "add_barrier_potential" if "add_barrier_potential" in {mem, plan, run} else ("open_probe_potential" if "open_probe_potential" in {mem, plan, run} else "reinforce_path_weight"),
        "os_reentry": {
            "MemoryOS": os_item("MemoryOS", mem),
            "PlanOS": os_item("PlanOS", plan),
            "RunGovernance": os_item("RunGovernance", run),
        },
        "boundary": {
            "router_only": True,
            "reentry_only": True,
            "does_not_execute_path": True,
            "does_not_authorize_execution": True,
            "candidate_weighting_not_truth": True,
            "barrier_potential_can_only_block_or_probe": True,
        },
    }


def run_case(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_path_integral_reentry_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "physical_quantum_qi_path_integral_reentry_intake_decision_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PATH_INTEGRAL_REENTRY_INTAKE_VALIDATOR_READY", case
    assert out["reentry_intake_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["physical_quantum_qi_path_integral_reentry_intake_considered"] is True, case
    assert packet["boundary"]["reentry_intake_validation_only"] is True, case
    assert packet["boundary"]["does_not_execute_path"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["barrier_potential_can_only_block_or_probe"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run_case(root, "accept", reentry(), lic())
        assert_ready("accept", code, out, packet)
        assert out["reentry_intake_decision"] == "accept"
        assert out["ready_count"] == 3 and out["probe_count"] == 0 and out["barrier_count"] == 0
        assert packet["os_decisions"]["PlanOS"]["decision"] == "accept"

        code, out, packet = run_case(root, "hold", reentry("reinforce_path_weight", "open_probe_potential", "reinforce_path_weight"), lic())
        assert_ready("hold", code, out, packet)
        assert out["reentry_intake_decision"] == "hold"
        assert out["probe_count"] == 1
        assert packet["os_decisions"]["PlanOS"]["decision"] == "hold"

        code, out, packet = run_case(root, "barrier", reentry("reinforce_path_weight", "add_barrier_potential", "reinforce_path_weight"), lic())
        assert_ready("barrier", code, out, packet)
        assert out["reentry_intake_decision"] == "block"
        assert out["barrier_count"] == 1
        assert packet["os_decisions"]["PlanOS"]["decision"] == "block"

        warn = reentry()
        warn["os_reentry"]["PlanOS"] = os_item("PlanOS", "reinforce_path_weight", delta=0)
        code, out, packet = run_case(root, "warn_nonpositive", warn, lic())
        assert_ready("warn_nonpositive", code, out, packet)
        assert out["reentry_intake_decision"] == "hold"
        assert "planos_reinforce_weight_nonpositive" in packet["warnings"]

        bad_inner = reentry()
        bad_inner["os_reentry"]["PlanOS"] = os_item("PlanOS", "add_barrier_potential", barrier_visible=False)
        code, out, packet = run_case(root, "bad_inner_barrier", bad_inner, lic())
        assert_ready("bad_inner_barrier", code, out, packet)
        assert out["reentry_intake_decision"] == "block"
        assert "planos_barrier_potential_not_visible" in packet["blockers"]

        bad_boundary = reentry()
        bad_boundary["boundary"]["barrier_potential_can_only_block_or_probe"] = False
        code, out, packet = run_case(root, "bad_top_boundary", bad_boundary, lic())
        assert code == 1
        assert "barrier_potential_boundary_invalid" in out["blockers"]
        assert packet == {}

        bad_considered = reentry()
        bad_considered["physical_quantum_qi_path_integral_reentry_considered"] = False
        code, out, packet = run_case(root, "bad_considered", bad_considered, lic())
        assert code == 1
        assert "physical_quantum_qi_path_integral_reentry_considered_not_true" in out["blockers"]
        assert packet == {}

        bad_missing = None
        code, out, packet = run_case(root, "missing", bad_missing, lic())
        assert code == 1
        assert "physical_quantum_qi_path_integral_reentry_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run_case(root, "license_block", reentry(), lic(reentry_intake_packet_write_allowed=False))
        assert code == 1
        assert "reentry_intake_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("physical_quantum_qi_path_integral_reentry_intake_validator_v10_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
