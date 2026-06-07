#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_terminal_finalizer_v10_8.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_finalizer_enabled": True, "apply_github_actions_terminal_finalizer": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_LICENSE_READY", "terminal_source_read_allowed": True, "scheduler_packet_write_allowed": True, "terminal_receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = root / name
    for file_name, payload in files.items():
        dump(runtime / file_name, payload)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_terminal_scheduler_packet.json"), load_json(runtime / "qi_github_actions_terminal_final_receipt.json")


def assert_ready(case: str, code: int, out: dict[str, Any], scheduler: dict[str, Any], terminal: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_TERMINAL_FINALIZER_READY", case
    assert out["scheduler_packet_written"] is True, case
    assert out["terminal_receipt_written"] is True, case
    assert not out["blockers"], case
    assert scheduler["scheduler_packet_allowed"] is True, case
    assert terminal["terminal_receipt_allowed"] is True, case


def final_receipt() -> dict[str, Any]:
    return {"final_receipt_allowed": True, "action_kind": "merge_pull_request", "final_state": "action_completed", "next_expected": "close_autopilot_cycle", "connector_action": "GitHub.merge_pull_request"}


def closure() -> dict[str, Any]:
    return {"closure_allowed": True, "bridge_state": "cycle_closed_final"}


def dispatch_supercycle(state: str, status: str = "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_READY") -> dict[str, Any]:
    return {"status": status, "supercycle_state": state, "connector_action": "GitHub.get_pr_info", "action_prepared": "policy_reentry_pr_info", "stop_reason": state, "blockers": ["x"] if status.endswith("BLOCKED") else []}


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, scheduler, terminal = run(root, "done", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic())
        assert_ready("done", code, out, scheduler, terminal)
        assert out["terminal_kind"] == "done"
        assert scheduler["scheduler_action"] == "close_scheduler_cycle"

        code, out, scheduler, terminal = run(root, "closed", {"qi_github_actions_next_cycle_closure_packet.json": closure()}, lic())
        assert_ready("closed", code, out, scheduler, terminal)
        assert out["terminal_state"] == "cycle_closed"
        assert scheduler["scheduler_action"] == "close_scheduler_cycle"

        code, out, scheduler, terminal = run(root, "await", {"qi_github_actions_dispatch_supercycle_receipt.json": dispatch_supercycle("await_dispatch_external_result")}, lic())
        assert_ready("await", code, out, scheduler, terminal)
        assert out["terminal_kind"] == "await_external"
        assert scheduler["scheduler_action"] == "dispatch_external_connector"
        assert terminal["connector_action"] == "GitHub.get_pr_info"

        code, out, scheduler, terminal = run(root, "blocked", {"qi_github_actions_dispatch_supercycle_receipt.json": dispatch_supercycle("run_dispatch_router_blocked", "QI_GITHUB_ACTIONS_DISPATCH_SUPERCYCLE_BLOCKED")}, lic())
        assert_ready("blocked", code, out, scheduler, terminal)
        assert out["terminal_kind"] == "blocked"
        assert scheduler["scheduler_action"] == "surface_blockers"

        code, out, scheduler, terminal = run(root, "missing", {}, lic())
        assert code == 1
        assert "terminal_source_packet_missing_or_invalid" in out["blockers"]
        assert scheduler == {}
        assert terminal == {}

        code, out, scheduler, terminal = run(root, "license_block", {"qi_github_actions_policy_action_final_receipt_packet.json": final_receipt()}, lic(scheduler_packet_write_allowed=False))
        assert code == 1
        assert "scheduler_packet_write_not_allowed" in out["blockers"]
        assert scheduler == {}
        assert terminal == {}
    print("qi_github_actions_terminal_finalizer_v10_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
