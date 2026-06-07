#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_progress_outcome_ledger_v8_0.py"


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
    return {"qi_progress_outcome_ledger_enabled": True, "apply_qi_progress_outcome_ledger": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROGRESS_OUTCOME_LEDGER_LICENSE_READY", "runner_packet_read_allowed": True, "runner_receipt_read_allowed": True, "outcome_ledger_append_allowed": True, "summary_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def packet(mode: str, klass: str, action: str = "advance_light", review: bool = False, small: bool = False) -> dict[str, Any]:
    return {"version": "qi_progress_aware_runner_packet_v7_8", "runner_mode": mode, "progress_class": klass, "progress_action": action, "progress_required": True, "review_exit_required": review, "small_probe_required": small}


def receipt(mode: str, klass: str, execution: str, status: str = "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_READY") -> dict[str, Any]:
    return {"version": "kuuos_runtime_daemon_qi_progress_aware_integrated_runner_v7_9", "status": status, "runner_mode": mode, "progress_class": klass, "execution_class": execution, "integrated_runner_status": "HELD_WITH_EXIT" if execution == "progress_hold_with_exit" else "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY", "integrated_runner_invoked": execution == "progress_runner_completed"}


def run(root: pathlib.Path, name: str, p: dict[str, Any] | None, r: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    runtime = root / name
    if p is not None:
        dump(runtime / "qi_progress_aware_runner_packet.json", p)
    if r is not None:
        dump(runtime / "qi_progress_aware_integrated_runner_receipt.json", r)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), rows(runtime / "qi_progress_outcome_ledger.jsonl"), load_json(runtime / "qi_progress_outcome_summary.json")


def assert_ready(case: str, code: int, out: dict[str, Any], ledger_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROGRESS_OUTCOME_LEDGER_READY", case
    assert out["ledger_appended"] is True, case
    assert not out["blockers"], case
    assert len(ledger_rows) == 1, case
    assert summary["record_digest"] == ledger_rows[0]["record_digest"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        p = packet("continue", "safe_progress_continue")
        r = receipt("continue", "safe_progress_continue", "progress_runner_completed")
        code, out, ledger_rows, summary = run(root, "completed", p, r, lic())
        assert_ready("completed", code, out, ledger_rows, summary)
        assert out["progress_outcome_class"] == "progress_completed"
        assert ledger_rows[0]["prev_record_digest"] == "GENESIS"

        p = packet("hold", "hold_with_review_exit", "hold_but_require_exit_condition", review=True)
        r = receipt("hold", "hold_with_review_exit", "progress_hold_with_exit")
        code, out, ledger_rows, summary = run(root, "hold", p, r, lic())
        assert_ready("hold", code, out, ledger_rows, summary)
        assert out["progress_outcome_class"] == "exit_preserved_hold"

        p = packet("observe", "progress_gap_detected", "open_small_probe_or_review_exit", small=True)
        r = receipt("observe", "progress_gap_detected", "progress_runner_completed")
        code, out, ledger_rows, summary = run(root, "gap", p, r, lic())
        assert_ready("gap", code, out, ledger_rows, summary)
        assert out["progress_outcome_class"] == "gap_probe_completed"

        p = packet("retry", "retry_with_rebalance_probe", "rebalance_then_retry", small=True)
        r = receipt("retry", "retry_with_rebalance_probe", "progress_runner_blocked", "QI_PROGRESS_AWARE_INTEGRATED_RUNNER_BLOCKED")
        code, out, ledger_rows, summary = run(root, "blocked", p, r, lic())
        assert_ready("blocked", code, out, ledger_rows, summary)
        assert out["progress_outcome_class"] == "progress_blocked"

        code, out, ledger_rows, summary = run(root, "missing_packet", None, r, lic())
        assert code == 1
        assert "qi_progress_aware_runner_packet_missing_or_invalid" in out["blockers"]
        assert ledger_rows == []

        bad_p = packet("continue", "safe_progress_continue")
        bad_p["progress_required"] = False
        code, out, ledger_rows, summary = run(root, "no_progress", bad_p, receipt("continue", "safe_progress_continue", "progress_runner_completed"), lic())
        assert code == 1
        assert "progress_required_not_true" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "mismatch", packet("continue", "safe_progress_continue"), receipt("retry", "safe_progress_continue", "progress_runner_completed"), lic())
        assert code == 1
        assert "runner_mode_mismatch" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "license_block", packet("continue", "safe_progress_continue"), receipt("continue", "safe_progress_continue", "progress_runner_completed"), lic(summary_write_allowed=False))
        assert code == 1
        assert "summary_write_not_allowed" in out["blockers"]
        assert ledger_rows == []
    print("qi_progress_outcome_ledger_v8_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
