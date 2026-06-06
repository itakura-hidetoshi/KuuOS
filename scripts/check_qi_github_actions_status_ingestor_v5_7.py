#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actions_status_ingestor_v5_7.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actions_result_ingestor_enabled": True, "apply_github_actions_result_ingestor": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_ACTIONS_RESULT_INGESTOR_LICENSE_READY", "connector_request_read_allowed": True, "connector_result_read_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, req: dict[str, Any] | None, res: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    runtime = root / name
    if req is not None:
        dump(runtime / "qi_github_actions_connector_execution_request.json", req)
    if res is not None:
        dump(runtime / "qi_github_actions_connector_result_packet.json", res)
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, ctx(runtime))
    dump(lp, license_packet)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def main() -> int:
    action_merge = "merge" + "_pull" + "_request"
    action_job = "rerun" + "_workflow" + "_job"
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        req = {"action": action_merge, "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS"}}
        res = {"result_packet_allowed": True, "action": action_merge, "merged": True}
        code, out = run(root, "ok", req, res, lic())
        assert code == 0
        assert out["status"] == "QI_GITHUB_ACTIONS_RESULT_INGESTOR_READY"
        assert out["result_class"] == "github_pr_merge_accepted"

        req = {"action": action_job, "connector_payload": {"repo_full_name": "itakura-hidetoshi/KuuOS"}}
        res = {"result_packet_allowed": True, "action": action_job, "success": False, "http_status": 503}
        code, out = run(root, "retry", req, res, lic())
        assert code == 0
        assert out["result_class"] == "github_operation_retryable"
        assert out["reobserve_request_emitted"] is True

        code, out = run(root, "missing", req, None, lic())
        assert code == 1
        assert "connector_result_packet_missing_or_invalid" in out["blockers"]
    print("qi_github_actions_status_ingestor_v5_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
