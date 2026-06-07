#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_terminal_scheduler_executor_v10_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_terminal_scheduler_executor_enabled": True, "apply_github_actions_terminal_scheduler_executor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_LICENSE_READY", "scheduler_packet_read_allowed": True, "execution_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def scheduler(action: str, connector: str = "none") -> dict[str, Any]:
    return {"scheduler_packet_allowed": True, "terminal_state": "state", "terminal_kind": "kind", "scheduler_action": action, "connector_action": connector, "action_prepared": "prepared", "source_kind": "test"}


def run(root: pathlib.Path, name: str, packet: dict[str, Any], license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if packet:
        dump(runtime / "qi_github_actions_terminal_scheduler_packet.json", packet)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_github_actions_terminal_scheduler_execution_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_GITHUB_ACTIONS_TERMINAL_SCHEDULER_EXECUTOR_READY", case
    assert out["execution_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["terminal_scheduler_execution_allowed"] is True, case
    assert packet["boundary"]["execution_packet_only"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("close", scheduler("close_scheduler_cycle"), "scheduler_cycle_closed"),
            ("dispatch", scheduler("dispatch_external_connector", "GitHub.get_pr_info"), "external_dispatch_ready"),
            ("blockers", scheduler("surface_blockers"), "blockers_surface_ready"),
            ("hold", scheduler("hold_for_review"), "hold_for_review_ready"),
            ("continue", scheduler("continue_supercycle"), "continue_supercycle_ready"),
        ]
        for name, packet_in, expected_state in cases:
            code, out, packet = run(root, name, packet_in, lic())
            assert_ready(name, code, out, packet)
            assert out["execution_state"] == expected_state, name
            assert packet["execution_state"] == expected_state, name

        code, out, packet = run(root, "bad_action", scheduler("unknown"), lic())
        assert code == 1
        assert "scheduler_action_not_allowlisted" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing_connector", scheduler("dispatch_external_connector"), lic())
        assert code == 1
        assert "connector_action_missing_for_dispatch" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "missing", {}, lic())
        assert code == 1
        assert "scheduler_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", scheduler("close_scheduler_cycle"), lic(execution_packet_write_allowed=False))
        assert code == 1
        assert "execution_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_github_actions_terminal_scheduler_executor_v10_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
