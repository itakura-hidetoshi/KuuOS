#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_lifecycle_policy_applier_v7_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_lifecycle_policy_applier_enabled": True, "apply_github_actions_lifecycle_policy_applier": True, "runtime_root": str(root)}


def lic(hint: str | None = None, **overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_LIFECYCLE_POLICY_APPLIER_LICENSE_READY", "trend_packet_read_allowed": True, "policy_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    if hint:
        value[f"allow_{hint}_policy"] = True
    value.update(overrides)
    return value


def trend(hint: str, summary_records: int = 3) -> dict[str, Any]:
    return {"version": "qi_github_actions_lifecycle_trend_packet_v7_0", "policy_hint": hint, "records_used": 5, "summary_records_used": summary_records, "cycle_records_used": 2}


def run(root: pathlib.Path, name: str, trend_packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if trend_packet is not None:
        dump(runtime / "qi_github_actions_lifecycle_trend_packet.json", trend_packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_lifecycle_policy_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_LIFECYCLE_POLICY_APPLIER_READY", case
    assert out["policy_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["boundary"]["does_not_run_loop_inside_applier"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "stable", trend("stable_continue"), lic("stable_continue"))
        assert_ready("stable", code, out, packet)
        assert packet["runner_mode"] == "continue"
        assert packet["hold_required"] is False

        code, out, packet = run(root, "observe", trend("observe_more"), lic("observe_more"))
        assert_ready("observe", code, out, packet)
        assert packet["runner_mode"] == "observe"
        assert packet["prefer_observation"] is True

        code, out, packet = run(root, "retry", trend("retry_heavy"), lic("retry_heavy"))
        assert_ready("retry", code, out, packet)
        assert packet["runner_mode"] == "retry"
        assert packet["prefer_retry"] is True

        code, out, packet = run(root, "hold", trend("hold_for_review"), lic("hold_for_review"))
        assert_ready("hold", code, out, packet)
        assert packet["runner_mode"] == "hold"
        assert packet["hold_required"] is True

        code, out, packet = run(root, "unknown", trend("unknown"), lic("stable_continue"))
        assert code == 1
        assert "policy_hint_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing", None, lic("stable_continue"))
        assert code == 1
        assert "lifecycle_trend_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", trend("stable_continue"), lic())
        assert code == 1
        assert "stable_continue_not_allowed_by_lifecycle_policy_applier_license" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_lifecycle_policy_applier_v7_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
