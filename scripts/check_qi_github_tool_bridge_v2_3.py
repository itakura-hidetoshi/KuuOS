#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_github_tool_bridge_v2_3.py"


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
    value = {"qi_github_tool_bridge_enabled": True, "apply_github_tool_bridge": True, "runtime_root": str(root), "mode": "mock", "execute_external_actions": False}
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {"license_status": "QI_GITHUB_TOOL_BRIDGE_LICENSE_READY", "plan_read_allowed": True, "external_action_allowed": True, "receipt_write_allowed": True, "audit_append_allowed": True}
    value.update(overrides)
    return value


def plan(**overrides: Any) -> dict[str, Any]:
    value = {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "mode": "mock",
        "base_branch": "main",
        "allowed_base_branch": "main",
        "execute_external_actions": False,
        "actions": [
            {"kind": "create_branch", "branch": "qi-test", "sha": "abc123"},
            {"kind": "create_file", "branch": "qi-test", "path": "tmp/a.txt", "content": "a"},
            {"kind": "create_pr", "branch": "qi-test", "head": "qi-test", "base": "main", "title": "test"},
            {"kind": "merge_pr", "pr_number": 1, "expected_head_sha": "abc123", "merge_method": "merge"}
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
        r1 = root / "mock"
        dump(r1 / "github_tool_bridge_plan.json", plan())
        rc, out = run(root, "mock", ctx(r1), lic())
        if rc != 0 or out.get("status") != "QI_GITHUB_TOOL_BRIDGE_APPLIED":
            errors.append("mock_status")
        if out.get("applied_count") != 4 or out.get("blocked_count") != 0:
            errors.append("mock_counts")
        if len(read_rows(r1 / "github_tool_bridge_audit.jsonl")) != 4:
            errors.append("mock_audit")
        if load_json(r1 / "github_tool_bridge_receipt.json").get("status") != "QI_GITHUB_TOOL_BRIDGE_APPLIED":
            errors.append("mock_receipt")

        r2 = root / "real_no_token"
        dump(r2 / "github_tool_bridge_plan.json", plan(mode="real", execute_external_actions=True, token_env="MISSING_TOKEN_FOR_TEST"))
        rc, out = run(root, "real_no_token", ctx(r2, mode="real", execute_external_actions=True), lic())
        if rc != 1 or out.get("status") != "QI_GITHUB_TOOL_BRIDGE_BLOCKED":
            errors.append("real_no_token_status")
        if "github_token_missing" not in out.get("blockers", []):
            errors.append("real_no_token_blocker")

        r3 = root / "real_no_execute"
        dump(r3 / "github_tool_bridge_plan.json", plan(mode="real", execute_external_actions=False))
        rc, out = run(root, "real_no_execute", ctx(r3, mode="real", execute_external_actions=False), lic())
        if rc != 1 or "real_mode_requires_execute_external_actions" not in out.get("blockers", []):
            errors.append("real_no_execute_blocker")

        r4 = root / "license"
        dump(r4 / "github_tool_bridge_plan.json", plan())
        rc, out = run(root, "license", ctx(r4), lic(external_action_allowed=False))
        if rc != 1 or "external_action_not_allowed" not in out.get("blockers", []):
            errors.append("license_blocker")
    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi GitHub tool bridge v2.3 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
