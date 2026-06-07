#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_policy_effectiveness_assessor_v7_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {"qi_github_actions_policy_effectiveness_assessor_enabled": True, "apply_github_actions_policy_effectiveness_assessor": True, "runtime_root": str(root), "effectiveness_window_records": 50}
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_POLICY_EFFECTIVENESS_ASSESSOR_LICENSE_READY", "policy_outcome_ledger_read_allowed": True, "effectiveness_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def outcome(hint: str, outcome_class: str) -> dict[str, Any]:
    return {"record_type": "policy_outcome", "policy_hint": hint, "runner_mode": "continue", "execution_class": "policy_runner_completed", "outcome_class": outcome_class, "record_digest": hint + outcome_class}


def run(root: pathlib.Path, name: str, ledger_rows: list[dict[str, Any]] | None, license_packet: dict[str, Any], context_overrides: dict[str, Any] | None = None) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if ledger_rows is not None:
        for row in ledger_rows:
            append_jsonl(runtime / "qi_github_actions_policy_outcome_ledger.jsonl", row)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, **(context_overrides or {})))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_policy_effectiveness_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_POLICY_EFFECTIVENESS_ASSESSOR_READY", case
    assert out["effectiveness_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["records_used"] >= 1, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        stable_rows = [outcome("stable_continue", "runner_completed"), outcome("stable_continue", "runner_completed"), outcome("stable_continue", "blocked_or_not_run")]
        code, out, packet = run(root, "stable", stable_rows, lic())
        assert_ready("stable", code, out, packet)
        assert packet["effectiveness_hint"] == "prefer_stable_continue"
        assert packet["policy_stats"]["stable_continue"]["total"] == 3

        hold_rows = [outcome("hold_for_review", "held_by_policy"), outcome("hold_for_review", "held_by_policy"), outcome("hold_for_review", "held_by_policy")]
        code, out, packet = run(root, "hold", hold_rows, lic())
        assert_ready("hold", code, out, packet)
        assert packet["effectiveness_hint"] == "respect_hold_boundary"

        blocked_rows = [outcome("stable_continue", "blocked_or_not_run"), outcome("observe_more", "blocked_or_not_run"), outcome("retry_heavy", "runner_completed")]
        code, out, packet = run(root, "reduce", blocked_rows, lic())
        assert_ready("reduce", code, out, packet)
        assert packet["effectiveness_hint"] == "reduce_autonomy_and_observe"

        observe_rows = [outcome("observe_more", "runner_completed"), outcome("observe_more", "held_by_policy")]
        code, out, packet = run(root, "observe", observe_rows, lic())
        assert_ready("observe", code, out, packet)
        assert packet["effectiveness_hint"] == "prefer_observe_more"

        code, out, packet = run(root, "empty", [], lic())
        assert code == 1
        assert "policy_outcome_ledger_empty_or_missing" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_window", stable_rows, lic(), {"effectiveness_window_records": 0})
        assert code == 1
        assert "effectiveness_window_records_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", stable_rows, lic(effectiveness_packet_write_allowed=False))
        assert code == 1
        assert "effectiveness_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_policy_effectiveness_assessor_v7_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
