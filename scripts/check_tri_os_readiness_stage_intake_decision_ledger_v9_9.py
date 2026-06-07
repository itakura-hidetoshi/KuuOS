#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_tri_os_readiness_stage_intake_decision_ledger_v9_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"tri_os_readiness_stage_intake_decision_ledger_enabled": True, "apply_tri_os_readiness_stage_intake_decision_ledger": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "TRI_OS_READINESS_STAGE_INTAKE_DECISION_LEDGER_LICENSE_READY", "stage_intake_packet_read_allowed": True, "unified_ledger_append_allowed": True, "os_ledger_append_allowed": True, "summary_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def packet(mem: str = "accept", plan: str = "accept", run: str = "accept") -> dict[str, Any]:
    return {
        "version": "tri_os_readiness_stage_intake_decision_packet_v9_8",
        "tri_os_readiness_stage_intake_considered": True,
        "decisions": {
            "MemoryOS": {"decision": mem, "blockers": [] if mem != "block" else ["memory_block"], "warnings": [] if mem != "hold" else ["memory_warn"]},
            "PlanOS": {"decision": plan, "blockers": [] if plan != "block" else ["plan_block"], "warnings": [] if plan != "hold" else ["plan_warn"]},
            "RunGovernance": {"decision": run, "blockers": [] if run != "block" else ["run_block"], "warnings": [] if run != "hold" else ["run_warn"]},
        },
        "boundary": {"does_not_authorize_execution": True, "fail_closed_on_boundary_loss": True},
    }


def run(root: pathlib.Path, name: str, p: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runtime = root / name
    if p is not None:
        dump(runtime / "tri_os_readiness_stage_intake_decision_packet.json", p)
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
        rows(runtime / "tri_os_readiness_stage_intake_decision_ledger.jsonl"),
        load_json(runtime / "tri_os_readiness_stage_intake_decision_summary.json"),
        rows(runtime / "memory_os_readiness_stage_intake_ledger.jsonl"),
        rows(runtime / "plan_os_readiness_stage_intake_ledger.jsonl"),
        rows(runtime / "run_governance_readiness_stage_intake_ledger.jsonl"),
    )


def assert_ready(case: str, code: int, out: dict[str, Any], unified: list[dict[str, Any]], summary: dict[str, Any], mem_rows: list[dict[str, Any]], plan_rows: list[dict[str, Any]], run_rows: list[dict[str, Any]]) -> None:
    assert code == 0, case
    assert out["status"] == "TRI_OS_READINESS_STAGE_INTAKE_DECISION_LEDGER_READY", case
    assert out["ledger_appended"] is True, case
    assert not out["blockers"], case
    assert len(unified) == 3, case
    assert len(mem_rows) == 1 and len(plan_rows) == 1 and len(run_rows) == 1, case
    assert summary["boundary"]["ledger_only"] is True, case
    assert summary["boundary"]["stage_intake_history_only"] is True, case
    assert summary["boundary"]["does_not_authorize_execution"] is True, case
    assert unified[0]["target_os"] == "MemoryOS", case
    assert unified[1]["target_os"] == "PlanOS", case
    assert unified[2]["target_os"] == "RunGovernance", case
    assert unified[0]["prev_unified_record_digest"] == "GENESIS", case
    assert unified[1]["prev_unified_record_digest"] == unified[0]["record_digest"], case
    assert unified[2]["prev_unified_record_digest"] == unified[1]["record_digest"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "all_accept", packet(), lic())
        assert_ready("all_accept", code, out, unified, summary, mem_rows, plan_rows, run_rows)
        assert out["accepted_count"] == 3
        assert out["held_count"] == 0
        assert out["blocked_count"] == 0

        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "mixed", packet("hold", "block", "accept"), lic())
        assert_ready("mixed", code, out, unified, summary, mem_rows, plan_rows, run_rows)
        assert out["accepted_count"] == 1
        assert out["held_count"] == 1
        assert out["blocked_count"] == 1
        assert summary["decisions"]["PlanOS"] == "block"

        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "missing", None, lic())
        assert code == 1
        assert "tri_os_readiness_stage_intake_decision_packet_missing_or_invalid" in out["blockers"]
        assert unified == []

        bad = packet()
        bad["tri_os_readiness_stage_intake_considered"] = False
        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "bad_considered", bad, lic())
        assert code == 1
        assert "tri_os_readiness_stage_intake_considered_not_true" in out["blockers"]
        assert unified == []

        bad_decision = packet()
        bad_decision["decisions"]["PlanOS"]["decision"] = "maybe"
        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "bad_decision", bad_decision, lic())
        assert code == 1
        assert "planos_stage_decision_invalid" in out["blockers"]
        assert unified == []

        code, out, unified, summary, mem_rows, plan_rows, run_rows = run(root, "license_block", packet(), lic(summary_write_allowed=False))
        assert code == 1
        assert "summary_write_not_allowed" in out["blockers"]
        assert unified == []
    print("tri_os_readiness_stage_intake_decision_ledger_v9_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
