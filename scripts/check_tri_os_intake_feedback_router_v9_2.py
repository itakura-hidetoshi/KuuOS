#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_intake_feedback_router_v9_2.py"


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
    return {"tri_os_intake_feedback_router_enabled": True, "apply_tri_os_intake_feedback_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_INTAKE_FEEDBACK_ROUTER_LICENSE_READY", "intake_summary_read_allowed": True, "intake_ledger_read_allowed": True, "feedback_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def summary(mem: str = "accept", plan: str = "accept", run: str = "accept") -> dict[str, Any]:
    return {"version": "tri_os_intake_decision_summary_v9_1", "decisions": {"MemoryOS": mem, "PlanOS": plan, "RunGovernance": run}, "boundary": {"does_not_authorize_execution": True}}


def record(os_name: str, decision: str, blockers: list[str] | None = None, warnings: list[str] | None = None) -> dict[str, Any]:
    return {"record_type": "tri_os_intake_decision", "target_os": os_name, "decision": decision, "blockers": blockers or [], "warnings": warnings or [], "record_digest": os_name + decision}


def run_case(root: pathlib.Path, name: str, s: dict[str, Any] | None, rows: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if s is not None:
        dump(runtime / "tri_os_intake_decision_summary.json", s)
    for row in rows:
        append_jsonl(runtime / "tri_os_intake_decision_ledger.jsonl", row)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "tri_os_intake_feedback_router_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_INTAKE_FEEDBACK_ROUTER_READY", case
    assert out["feedback_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["tri_os_intake_feedback_considered"] is True, case
    assert packet["boundary"]["feedback_only"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["blocks_remain_blocks_until_repaired"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        rows = [record("MemoryOS", "accept"), record("PlanOS", "accept"), record("RunGovernance", "accept")]
        code, out, packet = run_case(root, "all_accept", summary(), rows, lic())
        assert_ready("all_accept", code, out, packet)
        assert out["memory_feedback_action"] == "open_append_only_recall_anchor"
        assert out["plan_feedback_action"] == "open_weighted_candidate_planning"
        assert out["run_governance_feedback_action"] == "open_bounded_queue_gate"
        assert packet["feedback_counts"]["open_next_stage"] == 3

        mixed_rows = [record("MemoryOS", "hold", warnings=["memory_warn"]), record("PlanOS", "block", blockers=["plan_block"]), record("RunGovernance", "accept")]
        code, out, packet = run_case(root, "mixed", summary("hold", "block", "accept"), mixed_rows, lic())
        assert_ready("mixed", code, out, packet)
        assert out["memory_feedback_action"] == "request_memory_reobserve_anchor"
        assert out["plan_feedback_action"] == "block_plan_handoff_input"
        assert out["run_governance_feedback_action"] == "open_bounded_queue_gate"
        assert packet["feedback_counts"]["request_more_evidence"] == 1
        assert packet["feedback_counts"]["quarantine_or_repair"] == 1

        code, out, packet = run_case(root, "empty_ledger", summary("accept", "hold", "block"), [], lic())
        assert_ready("empty_ledger", code, out, packet)
        assert "tri_os_intake_decision_ledger_empty_or_missing" in out["warnings"]

        code, out, packet = run_case(root, "missing_summary", None, rows, lic())
        assert code == 1
        assert "tri_os_intake_decision_summary_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = summary()
        bad["boundary"]["does_not_authorize_execution"] = False
        code, out, packet = run_case(root, "bad_boundary", bad, rows, lic())
        assert code == 1
        assert "summary_execution_boundary_invalid" in out["blockers"]
        assert packet == {}

        bad_decision = summary("maybe", "accept", "accept")
        code, out, packet = run_case(root, "bad_decision", bad_decision, rows, lic())
        assert code == 1
        assert "memoryos_summary_decision_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run_case(root, "license_block", summary(), rows, lic(feedback_packet_write_allowed=False))
        assert code == 1
        assert "feedback_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("tri_os_intake_feedback_router_v9_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
