#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_physical_quantum_qi_progress_outcome_bridge_ledger_v8_7.py"


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
    return {"physical_quantum_qi_progress_outcome_bridge_ledger_enabled": True, "apply_physical_quantum_qi_progress_outcome_bridge_ledger": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "PHYSICAL_QUANTUM_QI_PROGRESS_OUTCOME_BRIDGE_LEDGER_LICENSE_READY", "runner_packet_read_allowed": True, "physical_runner_receipt_read_allowed": True, "physical_ledger_append_allowed": True, "qi_ledger_append_allowed": True, "summary_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def packet(mode: str, klass: str) -> dict[str, Any]:
    return {"version": "qi_progress_aware_runner_packet_v8_5_from_physical_quantum_qi", "physical_quantum_qi_motion_bias_used": True, "runner_mode": mode, "progress_class": klass, "progress_action": "advance_light", "progress_required": True, "review_exit_required": mode == "hold", "small_probe_required": mode in {"observe", "retry"}}


def receipt(mode: str, klass: str, execution: str, status: str = "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY") -> dict[str, Any]:
    return {"version": "kuuos_runtime_daemon_physical_quantum_qi_progress_aware_integrated_runner_v8_6", "status": status, "runner_mode": mode, "progress_class": klass, "execution_class": execution, "delegated_runner_status": "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY", "delegated_runner_invoked": execution == "progress_runner_completed", "physical_quantum_qi_motion_bias_used": True, "path_integral_candidate_weighting_preserved": True}


def run(root: pathlib.Path, name: str, p: dict[str, Any] | None, r: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    runtime = root / name
    if p is not None:
        dump(runtime / "qi_progress_aware_runner_packet.json", p)
    if r is not None:
        dump(runtime / "physical_quantum_qi_progress_aware_integrated_runner_receipt.json", r)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), rows(runtime / "physical_quantum_qi_progress_outcome_ledger.jsonl"), rows(runtime / "qi_progress_outcome_ledger.jsonl"), load_json(runtime / "physical_quantum_qi_progress_outcome_summary.json")


def assert_ready(case: str, code: int, out: dict[str, Any], physical_rows: list[dict[str, Any]], qi_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROGRESS_OUTCOME_BRIDGE_LEDGER_READY", case
    assert out["physical_ledger_appended"] is True, case
    assert out["qi_ledger_appended"] is True, case
    assert not out["blockers"], case
    assert len(physical_rows) == 1, case
    assert len(qi_rows) == 1, case
    assert physical_rows[0]["record_digest"] == qi_rows[0]["record_digest"], case
    assert summary["record_digest"] == physical_rows[0]["record_digest"], case
    assert physical_rows[0]["source"] == "physical_quantum_qi", case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, phy, qi, summary = run(root, "completed", packet("continue", "safe_progress_continue"), receipt("continue", "safe_progress_continue", "progress_runner_completed"), lic())
        assert_ready("completed", code, out, phy, qi, summary)
        assert out["progress_outcome_class"] == "progress_completed"

        code, out, phy, qi, summary = run(root, "hold", packet("hold", "hold_with_review_exit"), receipt("hold", "hold_with_review_exit", "progress_hold_with_exit"), lic())
        assert_ready("hold", code, out, phy, qi, summary)
        assert out["progress_outcome_class"] == "exit_preserved_hold"

        code, out, phy, qi, summary = run(root, "gap", packet("observe", "progress_gap_detected"), receipt("observe", "progress_gap_detected", "progress_runner_completed"), lic())
        assert_ready("gap", code, out, phy, qi, summary)
        assert out["progress_outcome_class"] == "gap_probe_completed"

        code, out, phy, qi, summary = run(root, "blocked", packet("retry", "retry_with_rebalance_probe"), receipt("retry", "retry_with_rebalance_probe", "physical_qi_delegated_runner_blocked", "PHYSICAL_QUANTUM_QI_PROGRESS_AWARE_INTEGRATED_RUNNER_BLOCKED"), lic())
        assert_ready("blocked", code, out, phy, qi, summary)
        assert out["progress_outcome_class"] == "progress_blocked"

        code, out, phy, qi, summary = run(root, "missing_packet", None, receipt("continue", "safe_progress_continue", "progress_runner_completed"), lic())
        assert code == 1
        assert "qi_progress_aware_runner_packet_missing_or_invalid" in out["blockers"]
        assert phy == [] and qi == []

        bad_receipt = receipt("continue", "safe_progress_continue", "progress_runner_completed")
        bad_receipt["path_integral_candidate_weighting_preserved"] = False
        code, out, phy, qi, summary = run(root, "bad_boundary", packet("continue", "safe_progress_continue"), bad_receipt, lic())
        assert code == 1
        assert "path_integral_candidate_weighting_not_preserved" in out["blockers"]
        assert phy == [] and qi == []

        code, out, phy, qi, summary = run(root, "license_block", packet("continue", "safe_progress_continue"), receipt("continue", "safe_progress_continue", "progress_runner_completed"), lic(qi_ledger_append_allowed=False))
        assert code == 1
        assert "qi_ledger_append_not_allowed" in out["blockers"]
        assert phy == [] and qi == []
    print("physical_quantum_qi_progress_outcome_bridge_ledger_v8_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
