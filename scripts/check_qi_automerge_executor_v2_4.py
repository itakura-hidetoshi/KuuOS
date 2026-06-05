#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_automerge_executor_v2_4.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path, **overrides: Any) -> dict[str, Any]:
    value = {
        "qi_automerge_executor_enabled": True,
        "apply_automerge_executor": True,
        "runtime_root": str(root),
        "mode": "mock",
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_AUTOMERGE_EXECUTOR_LICENSE_READY",
        "packet_read_allowed": True,
        "gate_eval_allowed": True,
        "merge_bridge_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "pr_number": 347,
        "expected_head_sha": "abc123",
        "actual_head_sha": "abc123",
        "explicit_automerge_license": True,
        "allowed_repository": True,
        "allowed_base_branch": True,
        "allowed_base_branch_name": "main",
        "base_branch": "main",
        "pull_request_created": True,
        "pull_request_not_draft": True,
        "mergeable": True,
        "no_unresolved_blockers": True,
        "receipt_written": True,
        "audit_written": True,
        "merge_allowed": True,
        "merge_method": "merge",
        "mode": "mock",
        "execute_external_actions": False,
        "required_checks": [
            {"name": "KuuOS Runtime Full Check", "status": "success"},
            {"name": "Qi Process Tensor Review Checks", "status": "success"}
        ]
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, c: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, c)
    dump(lp, l)
    done = subprocess.run([sys.executable, str(CLI), "--context", str(cp), "--license", str(lp), "--write", str(op), "--quiet"], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load_json(op)


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("missing_cli")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        r1 = root / "pass"
        dump(r1 / "automerge_packet.json", packet())
        rc, out = run(root, "pass", ctx(r1), lic())
        if rc != 0 or out.get("status") != "QI_AUTOMERGE_EXECUTOR_MERGED":
            errors.append("pass_status")
        if out.get("gate_status") != "QI_PR_MERGE_GATE_PASSED" or out.get("bridge_status") != "QI_GITHUB_TOOL_BRIDGE_APPLIED":
            errors.append("pass_stages")
        if out.get("merge_attempted") is not True or out.get("merge_applied") is not True:
            errors.append("pass_flags")
        if load_json(r1 / "automerge_receipt.json").get("status") != "QI_AUTOMERGE_EXECUTOR_MERGED":
            errors.append("pass_receipt")
        if len(read_rows(r1 / "automerge_audit.jsonl")) != 1:
            errors.append("pass_audit")

        r2 = root / "sha"
        dump(r2 / "automerge_packet.json", packet(actual_head_sha="def456"))
        rc, out = run(root, "sha", ctx(r2), lic())
        if rc != 1 or out.get("status") != "QI_AUTOMERGE_EXECUTOR_BLOCKED":
            errors.append("sha_status")
        if "head_sha_mismatch" not in out.get("blockers", []):
            errors.append("sha_blocker")

        r3 = root / "checks"
        dump(r3 / "automerge_packet.json", packet(required_checks=[{"name": "KuuOS Runtime Full Check", "status": "failure"}]))
        rc, out = run(root, "checks", ctx(r3), lic())
        if rc != 1 or "required_checks_not_success" not in out.get("blockers", []):
            errors.append("checks_blocker")

        r4 = root / "real_no_execute"
        dump(r4 / "automerge_packet.json", packet(mode="real", execute_external_actions=False))
        rc, out = run(root, "real_no_execute", ctx(r4, mode="real"), lic())
        if rc != 1 or "real_mode_requires_execute_external_actions" not in out.get("blockers", []):
            errors.append("real_no_execute")

        r5 = root / "license"
        dump(r5 / "automerge_packet.json", packet())
        rc, out = run(root, "license", ctx(r5), lic(merge_bridge_allowed=False))
        if rc != 1 or "merge_bridge_not_allowed" not in out.get("blockers", []):
            errors.append("license_blocker")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi automerge executor v2.4 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
