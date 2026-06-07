#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_bridge_lifecycle_ledger_v6_9.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_bridge_lifecycle_ledger_enabled": True, "apply_github_actions_bridge_lifecycle_ledger": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_BRIDGE_LIFECYCLE_LEDGER_LICENSE_READY", "integrated_runner_receipt_read_allowed": True, "lifecycle_ledger_append_allowed": True, "summary_write_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def source_receipt(status: str = "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY") -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_daemon_qi_github_actions_integrated_bridge_runner_v6_8",
        "status": status,
        "packet_id": "packet-1",
        "cycles_run": 2,
        "stop_reason": "await_dispatch_result",
        "final_internal_stage": "await_status_observation",
        "final_external_stage": "await_dispatch_result",
        "cycle_records": [
            {"index": 1, "internal_status": "READY", "internal_stop_reason": "waiting_for_external_observation", "internal_final_stage": "await_status_observation", "external_status": "READY", "external_selected_stage": "external_wait_resolve", "external_stage_result_class": "local_external_stage_completed", "internal_digest": "i1", "external_digest": "e1"},
            {"index": 2, "internal_status": "READY", "internal_stop_reason": "waiting_for_external_observation", "internal_final_stage": "await_status_observation", "external_status": "READY", "external_selected_stage": "await_dispatch_result", "external_stage_result_class": "await_dispatch_result", "internal_digest": "i2", "external_digest": "e2"},
        ],
    }


def run(root: pathlib.Path, name: str, receipt: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    runtime = root / name
    if receipt is not None:
        dump(runtime / "qi_github_actions_integrated_bridge_runner_receipt.json", receipt)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op), rows(runtime / "qi_github_actions_bridge_lifecycle_ledger.jsonl"), load_json(runtime / "qi_github_actions_bridge_lifecycle_summary.json")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        code, out, ledger_rows, summary = run(root, "ok", source_receipt(), lic())
        assert code == 0
        assert out["status"] == "QI_GITHUB_ACTIONS_BRIDGE_LIFECYCLE_LEDGER_READY"
        assert out["cycles_recorded"] == 2
        assert out["ledger_appended"] is True
        assert len(ledger_rows) == 3
        assert ledger_rows[0]["prev_record_digest"] == "GENESIS"
        assert ledger_rows[1]["prev_record_digest"] == ledger_rows[0]["record_digest"]
        assert ledger_rows[2]["record_type"] == "summary"
        assert summary["cycles_recorded"] == 2

        code, out, ledger_rows, summary = run(root, "blocked_source", source_receipt("BAD_STATUS"), lic())
        assert code == 1
        assert "integrated_runner_receipt_status_invalid" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "missing", None, lic())
        assert code == 1
        assert "integrated_runner_receipt_missing_or_invalid" in out["blockers"]
        assert ledger_rows == []

        code, out, ledger_rows, summary = run(root, "license_block", source_receipt(), lic(summary_write_allowed=False))
        assert code == 1
        assert "summary_write_not_allowed" in out["blockers"]
        assert ledger_rows == []
    print("qi_github_actions_bridge_lifecycle_ledger_v6_9 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
