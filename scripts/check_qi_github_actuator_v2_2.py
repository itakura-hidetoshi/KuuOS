#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_actuator_v2_2.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {"qi_github_actuator_enabled": True, "apply_github_actuator": True, "runtime_root": str(root)}


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_GITHUB_ACTUATOR_LICENSE_READY",
        "plan_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "branch_create_allowed": True,
        "file_patch_allowed": True,
        "pr_create_allowed": True,
        "merge_gate_allowed": True,
    }
    value.update(overrides)
    return value


def plan(**overrides: Any) -> dict[str, Any]:
    value = {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "pr_number": 345,
        "expected_head_sha": "abc123",
        "actual_head_sha": "abc123",
        "explicit_automerge_license": True,
        "allowed_repository": True,
        "allowed_base_branch": True,
        "pull_request_created": True,
        "pull_request_not_draft": True,
        "mergeable": True,
        "no_unresolved_blockers": True,
        "receipt_written": True,
        "audit_written": True,
        "merge_allowed": True,
        "merge_method": "merge",
        "required_checks": [{"name": "KuuOS Runtime Full Check", "status": "success"}],
        "actions": [
            {"kind": "create_branch"},
            {"kind": "file_patch"},
            {"kind": "create_pr"},
            {"kind": "merge_pr"}
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
        dump(r1 / "github_actuator_plan.json", plan())
        rc, out = run(root, "pass", ctx(r1), lic())
        if rc != 0 or out.get("status") != "QI_GITHUB_ACTUATOR_READY":
            errors.append("pass_status")
        if out.get("merge_gate_status") != "QI_PR_MERGE_GATE_PASSED" or out.get("merge_allowed") is not True:
            errors.append("pass_gate")
        if len(read_rows(r1 / "github_actuator_audit.jsonl")) != 4:
            errors.append("pass_audit")
        if load_json(r1 / "github_actuator_receipt.json").get("status") != "QI_GITHUB_ACTUATOR_READY":
            errors.append("pass_receipt")

        r2 = root / "blocked_gate"
        dump(r2 / "github_actuator_plan.json", plan(actual_head_sha="def456"))
        rc, out = run(root, "blocked_gate", ctx(r2), lic())
        if rc != 0 or out.get("status") != "QI_GITHUB_ACTUATOR_MERGE_BLOCKED":
            errors.append("blocked_gate_status")
        if out.get("merge_gate_status") != "QI_PR_MERGE_GATE_BLOCKED":
            errors.append("blocked_gate_value")

        r3 = root / "blocked_license"
        dump(r3 / "github_actuator_plan.json", plan())
        rc, out = run(root, "blocked_license", ctx(r3), lic(merge_gate_allowed=False))
        if rc != 1 or out.get("status") != "QI_GITHUB_ACTUATOR_BLOCKED":
            errors.append("blocked_license_status")
        if "merge_gate_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_license_reason")
    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi GitHub actuator v2.2 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
