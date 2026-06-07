#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_terminal_execution_bridge_v11_1.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_execution_bridge_enabled": True, "apply_github_actions_terminal_execution_bridge": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_LICENSE_READY", "terminal_execution_packet_read_allowed": True, "dispatch_packet_read_allowed": True, "output_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def execution(state: str, connector: str = "none") -> dict[str, Any]:
    return {"terminal_scheduler_execution_allowed": True, "scheduler_action": "action", "execution_state": state, "connector_action": connector, "action_prepared": "prepared", "source_kind": "test", "terminal_kind": "kind"}


def dispatch(connector: str = "GitHub.get_pr_info") -> dict[str, Any]:
    return {"dispatch_allowed": True, "dispatch_kind": "policy_reentry_pr_info", "connector_action": connector, "connector_payload": {"repository_full_name": "itakura-hidetoshi/KuuOS", "pr_number": 1}, "raw_result_expected_file": "qi_github_actions_dispatch_pr_info_raw_result_packet.json"}


def run(root: pathlib.Path, name: str, files: dict[str, dict[str, Any]], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
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
    out = load_json(op)
    return done.returncode, out, load_json(pathlib.Path(out.get("output_packet_path", ""))) if out.get("output_packet_path") else {}


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_TERMINAL_EXECUTION_BRIDGE_READY", case
    assert out["output_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["terminal_execution_output_allowed"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("closed", execution("scheduler_cycle_closed"), "cycle_closed_final"),
            ("blockers", execution("blockers_surface_ready"), "blockers_ready"),
            ("hold", execution("hold_for_review_ready"), "hold_ready"),
            ("continue", execution("continue_supercycle_ready"), "continue_ready"),
        ]
        for name, packet_in, expected_state in cases:
            code, out, packet = run(root, name, {"qi_github_actions_terminal_scheduler_execution_packet.json": packet_in}, lic())
            assert_ready(name, code, out, packet)
            assert out["output_state"] == expected_state, name
            assert packet["output_state"] == expected_state, name

        files = {"qi_github_actions_terminal_scheduler_execution_packet.json": execution("external_dispatch_ready", "GitHub.get_pr_info"), "qi_github_actions_unified_dispatch_packet.json": dispatch()}
        code, out, packet = run(root, "external", files, lic())
        assert_ready("external", code, out, packet)
        assert out["output_state"] == "external_dispatch_ready"
        assert packet["dispatch_allowed"] is True
        assert packet["connector_payload"]["pr_number"] == 1

        code, out, packet = run(root, "external_missing_dispatch", {"qi_github_actions_terminal_scheduler_execution_packet.json": execution("external_dispatch_ready", "GitHub.get_pr_info")}, lic())
        assert code == 1
        assert "unified_dispatch_packet_missing_for_external_dispatch" in out["blockers"]
        assert packet == {}

        files = {"qi_github_actions_terminal_scheduler_execution_packet.json": execution("external_dispatch_ready", "GitHub.get_pr_info"), "qi_github_actions_unified_dispatch_packet.json": dispatch("GitHub.merge_pull_request")}
        code, out, packet = run(root, "external_mismatch", files, lic())
        assert code == 1
        assert "dispatch_connector_action_mismatch" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_state", {"qi_github_actions_terminal_scheduler_execution_packet.json": execution("bad")}, lic())
        assert code == 1
        assert "execution_state_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", {"qi_github_actions_terminal_scheduler_execution_packet.json": execution("scheduler_cycle_closed")}, lic(output_packet_write_allowed=False))
        assert code == 1
        assert "output_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_terminal_execution_bridge_v11_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
