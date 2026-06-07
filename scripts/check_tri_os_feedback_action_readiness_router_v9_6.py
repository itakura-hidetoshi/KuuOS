#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_feedback_action_readiness_router_v9_6.py"


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
    return {"tri_os_feedback_action_readiness_router_enabled": True, "apply_tri_os_feedback_action_readiness_router": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_FEEDBACK_ACTION_READINESS_ROUTER_LICENSE_READY", "action_intake_summary_read_allowed": True, "action_intake_ledger_read_allowed": True, "readiness_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def summary(mem: str = "accept", plan: str = "accept", run: str = "accept") -> dict[str, Any]:
    return {"version": "tri_os_feedback_action_intake_decision_summary_v9_5", "decisions": {"MemoryOS": mem, "PlanOS": plan, "RunGovernance": run}, "boundary": {"does_not_authorize_execution": True, "action_intake_history_only": True}}


def record(os_name: str, decision: str, blockers: list[str] | None = None, warnings: list[str] | None = None) -> dict[str, Any]:
    return {"record_type": "tri_os_feedback_action_intake_decision", "target_os": os_name, "decision": decision, "blockers": blockers or [], "warnings": warnings or [], "record_digest": os_name + decision}


def run(root: pathlib.Path, name: str, s: dict[str, Any] | None, rows: list[dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if s is not None:
        dump(runtime / "tri_os_feedback_action_intake_decision_summary.json", s)
    for row in rows:
        append_jsonl(runtime / "tri_os_feedback_action_intake_decision_ledger.jsonl", row)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "tri_os_feedback_action_readiness_router_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_FEEDBACK_ACTION_READINESS_ROUTER_READY", case
    assert out["readiness_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["tri_os_feedback_action_readiness_considered"] is True, case
    assert packet["boundary"]["readiness_only"] is True, case
    assert packet["boundary"]["does_not_authorize_execution"] is True, case
    assert packet["boundary"]["repair_required_blocks_ready_state"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        rows = [record("MemoryOS", "accept"), record("PlanOS", "accept"), record("RunGovernance", "accept")]
        code, out, packet = run(root, "all_ready", summary(), rows, lic())
        assert_ready("all_ready", code, out, packet)
        assert out["memory_readiness"] == "ready"
        assert out["plan_readiness"] == "ready"
        assert out["run_governance_readiness"] == "ready"
        assert packet["readiness_counts"]["ready"] == 3

        mixed_rows = [record("MemoryOS", "hold", warnings=["memory_warn"]), record("PlanOS", "block", blockers=["plan_block"]), record("RunGovernance", "accept")]
        code, out, packet = run(root, "mixed", summary("hold", "block", "accept"), mixed_rows, lic())
        assert_ready("mixed", code, out, packet)
        assert out["memory_readiness"] == "needs_evidence"
        assert out["plan_readiness"] == "repair_required"
        assert out["run_governance_readiness"] == "ready"
        assert packet["readiness_counts"]["needs_evidence"] == 1
        assert packet["readiness_counts"]["repair_required"] == 1
        assert packet["readiness"]["PlanOS"]["next_stage_action"] == "stage_plan_handoff_repair_quarantine"

        code, out, packet = run(root, "empty_ledger", summary("accept", "hold", "block"), [], lic())
        assert_ready("empty_ledger", code, out, packet)
        assert "tri_os_feedback_action_intake_decision_ledger_empty_or_missing" in out["warnings"]

        code, out, packet = run(root, "missing_summary", None, rows, lic())
        assert code == 1
        assert "tri_os_feedback_action_intake_decision_summary_missing_or_invalid" in out["blockers"]
        assert packet == {}

        bad = summary()
        bad["boundary"]["action_intake_history_only"] = False
        code, out, packet = run(root, "bad_boundary", bad, rows, lic())
        assert code == 1
        assert "summary_action_intake_history_boundary_invalid" in out["blockers"]
        assert packet == {}

        bad_decision = summary("maybe", "accept", "accept")
        code, out, packet = run(root, "bad_decision", bad_decision, rows, lic())
        assert code == 1
        assert "memoryos_summary_decision_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", summary(), rows, lic(readiness_packet_write_allowed=False))
        assert code == 1
        assert "readiness_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("tri_os_feedback_action_readiness_router_v9_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
