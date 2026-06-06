#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_scheduler_overlay_v3_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_process_tensor_scheduler_overlay_enabled": True, "apply_process_tensor_scheduler_overlay": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_LICENSE_READY", "scheduled_packet_read_allowed": True, "process_tensor_packet_read_allowed": True, "scheduled_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def scheduled() -> dict[str, Any]:
    return {"initial_qi_packet": {"qi_flow": 0.72, "coherence_score": 0.74, "circulation_pressure": 0.44, "friction": 0.12}, "route_base": {"segment": "upper-middle-lower"}, "scheduler_handoff": {"source": "next_qi_circulation_scheduler_packet", "source_digest": "abc"}}


def pt(**overrides: Any) -> dict[str, Any]:
    value = {"process_tensor_ok": True, "process_tensor_visible": True, "transition_continuity_visible": True, "memory_continuity_visible": True, "nonmarkov_memory_visible": True, "memory_depth": 6, "execution_pressure": 0.40, "coherence_score": 0.82, "recovery_witness_present": True, "process_history": [{"transition_visible": True, "memory_link_visible": True}, {"transition_visible": True, "nonmarkov_link_visible": True}, {"transition_visible": True, "memory_link_visible": True}], "candidate_only": True, "nonfinal_marker": True, "two_truths_gap": True, "noncollapse_guard": True, "memory_overwrite_blocker": True, "world_identity_blocker": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, scheduled_packet: dict[str, Any], pt_packet: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    dump(runtime / "qi_scheduled_closed_loop_packet.json", scheduled_packet)
    dump(runtime / "qi_process_tensor_packet.json", pt_packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_scheduled_closed_loop_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_READY", case
    assert out["write_performed"] is True, case
    assert not out["blockers"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, after = run(root, "stable", scheduled(), pt(), lic())
        assert_ready("stable", code, out)
        assert out["overlay_class"] == "process_tensor_stabilize_overlay"
        assert after["initial_qi_packet"]["process_tensor_overlay_class"] == "process_tensor_stabilize_overlay"
        assert after["initial_qi_packet"]["qi_flow"] > 0.72
        assert after["route_base"]["process_tensor_memory_depth"] == 6

        code, out, after = run(root, "hold", scheduled(), pt(non_markov_unresolved=True), lic())
        assert_ready("hold", code, out)
        assert out["overlay_class"] == "process_tensor_hold_overlay"
        assert after["initial_qi_packet"]["critical_blocker_present"] is True
        assert "non_markov_unresolved_sets_hold_overlay" in out["warnings"]

        code, out, after = run(root, "recovery", scheduled(), pt(recovery_witness_present=False, recovery_witness_missing=True), lic())
        assert_ready("recovery", code, out)
        assert out["overlay_class"] == "process_tensor_recovery_overlay"
        assert after["initial_qi_packet"]["recovery_witness_missing"] is True
        assert after["initial_qi_packet"]["friction"] > 0.12

        code, out, after = run(root, "blocked_license", scheduled(), pt(), lic(scheduled_packet_write_allowed=False))
        assert code == 1
        assert out["status"] == "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_BLOCKED"
        assert "scheduled_packet_write_not_allowed" in out["blockers"]
        assert "process_tensor_overlay_class" not in after["initial_qi_packet"]

        code, out, _ = run(root, "not_ready", scheduled(), {"process_tensor_ok": False, "process_tensor_visible": False}, lic())
        assert code == 1
        assert "process_tensor_not_ready" in out["blockers"]

        rows = read_rows(root / "stable" / "qi_process_tensor_scheduler_overlay_audit.jsonl")
        assert len(rows) == 1
        assert rows[0]["status"] == "QI_PROCESS_TENSOR_SCHEDULER_OVERLAY_READY"
    print("qi_process_tensor_scheduler_overlay_v3_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
