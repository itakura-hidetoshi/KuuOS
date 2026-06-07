#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_outcome_ledger_v7_3.py"


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
    return {"qi_github_actions_policy_outcome_ledger_enabled": True, "apply_github_actions_policy_outcome_ledger": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_OUTCOME_LEDGER_LICENSE_READY", "policy_packet_read_allowed": True, "policy_aware_runner_receipt_read_allowed": True, "outcome_ledger_append_allowed": True, "summary_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def policy(mode: str, hint: str, hold: bool = False) -> dict[str, Any]:
    return {"version": "qi_github_actions_lifecycle_policy_packet_v7_1", "runner_mode": mode, "policy_hint": hint, "hold_required": hold, "max_bridge_cycles": 2, "max_loop_steps_per_cycle": 2}


def runner(mode: str, hint: str, execution_class: str, status: str = "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_READY") -> dict[str, Any]:
    return {"version": "kuuos_runtime_daemon_qi_github_actions_policy_aware_runner_v7_2", "status": status, "packet_id": "runner-1", "runner_mode": mode, "policy_hint": hint, "execution_class": execution_class, "integrated_runner_status": "HELD" if execution_class == "policy_hold" else "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY", "integrated_runner_invoked": execution_class != "policy_hold"}


def run(root: pathlib.Path, name: str, policy_packet: dict[str, Any] | None, runner_receipt: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    runtime = root / name
    if policy_packet is not None:
        dump(runtime / "qi_github_actions_lifecycle_policy_packet.json", policy_packet)
    if runner_receipt is not None:
        dump(runtime / "qi_github_actions_policy_aware_runner_receipt.json", runner_receipt)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), rows(runtime / "qi_github_actions_policy_outcome_ledger.jsonl"), load_json(runtime / "qi_github_actions_policy_outcome_summary.json")


def assert_ready(case: str, code: int, out: dict[str, Any], ledger_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_OUTCOME_LEDGER_READY", case
    assert out["ledger_appended"] is True, case
    assert not out["blockers"], case
    assert len(ledger_rows) == 1, case
    assert summary["record_digest"] == ledger_rows[0]["record_digest"], case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, ledger_rows, summary = run(root, "hold", policy("hold", "hold_for_review", True), runner("hold", "hold_for_review", "policy_hold"), lic())
        assert_ready("hold", code, out, ledger_rows, summary)
        assert out["outcome_class"] == "held_by_policy"
        assert ledger_rows[0]["prev_record_digest"] == "GENESIS"

        code, out, ledger_rows, summary = run(root, "completed", policy("continue", "stable_continue"), runner("continue", "stable_continue", "policy_runner_completed"), lic())
        assert_ready("completed", code, out, ledger_rows, summary)
        assert out["outcome_class"] == "runner_completed"

        code, out, ledger_rows, summary = run(root, "blocked", policy("observe", "observe_more"), runner("observe", "observe_more", "policy_runner_blocked", "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_BLOCKED"), lic())
        assert_ready("blocked", code, out, ledger_rows, summary)
        assert out["outcome_class"] == "blocked_or_not_run"

        code, out, ledger_rows, summary = run(root, "mismatch", policy("continue", "stable_continue"), runner("retry", "stable_continue", "policy_runner_completed"), lic())
        assert code == 1
        assert "runner_mode_mismatch" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "missing_policy", None, runner("continue", "stable_continue", "policy_runner_completed"), lic())
        assert code == 1
        assert "lifecycle_policy_packet_missing_or_invalid" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "missing_runner", policy("continue", "stable_continue"), None, lic())
        assert code == 1
        assert "policy_aware_runner_receipt_missing_or_invalid" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "license_block", policy("continue", "stable_continue"), runner("continue", "stable_continue", "policy_runner_completed"), lic(summary_write_allowed=False))
        assert code == 1
        assert "summary_write_not_allowed" in out["blockers"]
        assert ledger_rows == []
    print("qi_github_actions_policy_outcome_ledger_v7_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
