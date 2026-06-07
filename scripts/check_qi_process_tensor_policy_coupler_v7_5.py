#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_process_tensor_policy_coupler_v7_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path, depth: int = 5) -> dict[str, Any]:
    return {"qi_process_tensor_policy_coupler_enabled": True, "apply_qi_process_tensor_policy_coupler": True, "runtime_root": str(root), "process_memory_depth": depth}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_PROCESS_TENSOR_POLICY_COUPLER_LICENSE_READY", "policy_effectiveness_read_allowed": True, "lifecycle_trend_read_allowed": True, "lifecycle_ledger_read_allowed": True, "policy_outcome_ledger_read_allowed": True, "coupling_packet_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def base_files(root: pathlib.Path, effectiveness_hint: str, policy_hint: str) -> None:
    dump(root / "qi_github_actions_policy_effectiveness_packet.json", {"effectiveness_hint": effectiveness_hint, "records_used": 3})
    dump(root / "qi_github_actions_lifecycle_trend_packet.json", {"policy_hint": policy_hint, "records_used": 3})


def run(root: pathlib.Path, name: str, setup: str, license_packet: dict[str, Any], depth: int = 5) -> tuple[int, dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if setup == "stable":
        base_files(runtime, "prefer_stable_continue", "stable_continue")
        append_jsonl(runtime / "qi_github_actions_policy_outcome_ledger.jsonl", {"policy_hint": "stable_continue", "outcome_class": "runner_completed"})
    elif setup == "hold":
        base_files(runtime, "respect_hold_boundary", "hold_for_review")
        append_jsonl(runtime / "qi_github_actions_bridge_lifecycle_ledger.jsonl", {"stop_reason": "external_bridge_blocked", "external_selected_stage": "unknown"})
        append_jsonl(runtime / "qi_github_actions_policy_outcome_ledger.jsonl", {"policy_hint": "hold_for_review", "outcome_class": "held_by_policy"})
    elif setup == "retry":
        base_files(runtime, "prefer_retry_heavy", "retry_heavy")
        append_jsonl(runtime / "qi_github_actions_bridge_lifecycle_ledger.jsonl", {"stop_reason": "waiting_for_connector_operation", "external_selected_stage": "await_dispatch_result"})
    elif setup == "observe":
        base_files(runtime, "prefer_observe_more", "observe_more")
        append_jsonl(runtime / "qi_github_actions_bridge_lifecycle_ledger.jsonl", {"stop_reason": "waiting_for_external_observation", "external_selected_stage": "await_external_call"})
    elif setup == "missing_effectiveness":
        dump(runtime / "qi_github_actions_lifecycle_trend_packet.json", {"policy_hint": "stable_continue"})
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime, depth))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), load_json(runtime / "qi_process_tensor_policy_coupling_packet.json")


def assert_ready(case: str, code: int, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert code == 0, case
    assert out["status"] == "QI_PROCESS_TENSOR_POLICY_COUPLER_READY", case
    assert out["coupling_packet_written"] is True, case
    assert not out["blockers"], case
    assert packet["qi_process_tensor_considered"] is True, case
    assert packet["boundary"]["non_markov_history_visible"] is True, case


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, packet = run(root, "stable", "stable", lic())
        assert_ready("stable", code, out, packet)
        assert packet["qi_state"] == "smooth_circulation"
        assert packet["next_policy_bias"] == "stable_continue"

        code, out, packet = run(root, "hold", "hold", lic())
        assert_ready("hold", code, out, packet)
        assert packet["qi_state"] == "review_constraint"
        assert packet["next_policy_bias"] == "hold_for_review"

        code, out, packet = run(root, "retry", "retry", lic())
        assert_ready("retry", code, out, packet)
        assert packet["qi_state"] == "retry_stagnation"
        assert packet["next_policy_bias"] == "retry_heavy"

        code, out, packet = run(root, "observe", "observe", lic())
        assert_ready("observe", code, out, packet)
        assert packet["qi_state"] == "observation_deficiency"
        assert packet["next_policy_bias"] == "observe_more"

        code, out, packet = run(root, "missing", "missing_effectiveness", lic())
        assert code == 1
        assert "policy_effectiveness_packet_missing_or_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "bad_depth", "stable", lic(), 0)
        assert code == 1
        assert "process_memory_depth_invalid" in out["blockers"]
        assert packet == {}

        code, out, packet = run(root, "license_block", "stable", lic(coupling_packet_write_allowed=False))
        assert code == 1
        assert "coupling_packet_write_not_allowed" in out["blockers"]
        assert packet == {}
    print("qi_process_tensor_policy_coupler_v7_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
