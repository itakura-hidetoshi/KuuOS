#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_local_flow_v0_3.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def context(runtime_root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_local_flow_enabled": True,
        "apply_local_flow": True,
        "runtime_root": str(runtime_root),
        "max_rows": 100
    }


def license_packet(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_LOCAL_FLOW_LICENSE_READY",
        "queue_read_allowed": True,
        "state_write_allowed": True,
        "applied_log_append_allowed": True
    }
    value.update(overrides)
    return value


def run(root: pathlib.Path, name: str, c: dict[str, Any], l: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    cp = root / f"{name}_ctx.json"
    lp = root / f"{name}_lic.json"
    op = root / f"{name}_out.json"
    dump(cp, c)
    dump(lp, l)
    done = subprocess.run([
        sys.executable, str(CLI),
        "--context", str(cp),
        "--license", str(lp),
        "--write", str(op),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
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
        r1 = root / "r1"
        write_jsonl(r1 / "queue.jsonl", [
            {"item_id": "a", "item_kind": "kind_a"},
            {"item_id": "b", "item_kind": "kind_b"},
        ])
        rc, out = run(root, "first", context(r1), license_packet())
        if rc != 0 or out.get("flow_status") != "QI_LOCAL_FLOW_APPLIED":
            errors.append("first_status")
        if out.get("applied_count") != 2:
            errors.append("first_count")
        if load_json(r1 / "state.json").get("applied_total") != 2:
            errors.append("state_total")
        if len(read_rows(r1 / "applied.jsonl")) != 2:
            errors.append("applied_rows")

        rc, out = run(root, "second", context(r1), license_packet())
        if rc != 0 or out.get("flow_status") != "QI_LOCAL_FLOW_REPLAYED":
            errors.append("replay_status")
        if out.get("applied_count") != 0 or out.get("replay_count") != 2:
            errors.append("replay_count")
        if len(read_rows(r1 / "applied.jsonl")) != 2:
            errors.append("replay_duplicate")

        r2 = root / "r2"
        write_jsonl(r2 / "queue.jsonl", [{"item_id": "c", "item_kind": "kind_c"}])
        rc, out = run(root, "blocked", context(r2), license_packet(state_write_allowed=False))
        if rc != 1 or out.get("flow_status") != "QI_LOCAL_FLOW_BLOCKED":
            errors.append("blocked_status")
        if "state_write_not_allowed" not in out.get("blockers", []):
            errors.append("blocked_reason")
        if (r2 / "state.json").exists() or (r2 / "applied.jsonl").exists():
            errors.append("blocked_files")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi local flow v0.3 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
