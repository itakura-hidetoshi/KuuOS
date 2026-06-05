#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_forward_change_runner_v2_6.py"


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
        "qi_forward_change_runner_enabled": True,
        "apply_forward_change_runner": True,
        "runtime_root": str(root),
    }
    value.update(overrides)
    return value


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_FORWARD_CHANGE_RUNNER_LICENSE_READY",
        "packet_read_allowed": True,
        "packet_write_allowed": True,
        "loop_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "branch": "qi-forward-test",
        "base_branch": "main",
        "base_sha": "abc123",
        "pr_number": 1,
        "expected_head_sha": "abc123",
        "actual_head_sha": "abc123",
        "title": "Qi forward test",
        "body": "forward loop",
        "mode": "mock",
        "forward_intent": True,
        "required_checks": [
            {"name": "KuuOS Runtime Full Check", "status": "success"},
            {"name": "Qi Process Tensor Review Checks", "status": "success"}
        ],
        "files": [
            {"kind": "create_file", "path": "tmp/qi-forward-test.txt", "content": "ok", "message": "Qi forward test"}
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
        dump(r1 / "forward_change_packet.json", packet())
        rc, out = run(root, "pass", ctx(r1), lic())
        if rc != 0 or out.get("status") != "QI_FORWARD_CHANGE_RUNNER_MERGED":
            errors.append("pass_status")
        if out.get("forward_intent_seen") is not True or out.get("normalized") is not True:
            errors.append("pass_forward_flags")
        if out.get("downstream_status") != "QI_AUTONOMOUS_CHANGE_LOOP_MERGED":
            errors.append("pass_downstream")
        normalized = load_json(r1 / "autonomous_change_loop_packet.json")
        if normalized.get("explicit_change_loop_license") is not True or normalized.get("merge_allowed") is not True:
            errors.append("normalization")
        if load_json(r1 / "forward_change_receipt.json").get("status") != "QI_FORWARD_CHANGE_RUNNER_MERGED":
            errors.append("receipt")
        if len(read_rows(r1 / "forward_change_audit.jsonl")) != 1:
            errors.append("audit")

        r2 = root / "missing_intent"
        dump(r2 / "forward_change_packet.json", packet(forward_intent=False, explicit_change_loop_license=False))
        rc, out = run(root, "missing_intent", ctx(r2), lic())
        if rc != 1 or out.get("status") != "QI_FORWARD_CHANGE_RUNNER_BLOCKED":
            errors.append("missing_intent_status")
        if "forward_intent_missing" not in out.get("blockers", []):
            errors.append("missing_intent_reason")

        r3 = root / "checks"
        dump(r3 / "forward_change_packet.json", packet(required_checks=[{"name": "KuuOS Runtime Full Check", "status": "failure"}]))
        rc, out = run(root, "checks", ctx(r3), lic())
        if rc != 1 or out.get("status") != "QI_FORWARD_CHANGE_RUNNER_BLOCKED":
            errors.append("checks_status")
        if "downstream_loop_not_merged" not in out.get("blockers", []):
            errors.append("checks_reason")

        r4 = root / "license"
        dump(r4 / "forward_change_packet.json", packet())
        rc, out = run(root, "license", ctx(r4), lic(loop_run_allowed=False))
        if rc != 1 or "loop_run_not_allowed" not in out.get("blockers", []):
            errors.append("license_reason")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi forward change runner v2.6 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
