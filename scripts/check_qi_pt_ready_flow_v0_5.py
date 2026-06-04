#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_pt_ready_flow_v0_5.py"


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_rows(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_rows(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(runtime_root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_pt_ready_flow_enabled": True,
        "apply_ready_flow": True,
        "runtime_root": str(runtime_root),
        "max_apply": 100,
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "QI_PT_READY_FLOW_LICENSE_READY",
        "ready_queue_read_allowed": True,
        "state_write_allowed": True,
        "applied_log_append_allowed": True,
        "feedback_append_allowed": True,
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
        write_rows(r1 / "queue.ready.jsonl", [
            {"policy_key": "p1", "item_kind": "kind_a", "policy_score": 1.0},
            {"policy_key": "p2", "item_kind": "kind_b", "policy_score": 3.0},
        ])
        rc, out = run(root, "first", ctx(r1), lic())
        if rc != 0 or out.get("ready_flow_status") != "QI_PT_READY_FLOW_APPLIED":
            errors.append("first_status")
        if out.get("applied_count") != 2 or out.get("feedback_count") != 2:
            errors.append("first_counts")
        if read_rows(r1 / "applied.jsonl")[0].get("source_key") != "p2":
            errors.append("order")
        state = load_json(r1 / "state.json")
        if state.get("pt_ready_applied_total") != 2:
            errors.append("state")
        if len(read_rows(r1 / "pt_feedback.jsonl")) != 2:
            errors.append("fb")

        rc, out = run(root, "again", ctx(r1), lic())
        if rc != 0 or out.get("ready_flow_status") != "QI_PT_READY_FLOW_REPLAYED":
            errors.append("again_status")
        if out.get("applied_count") != 0 or out.get("replay_count") != 2:
            errors.append("again_counts")
        if len(read_rows(r1 / "applied.jsonl")) != 2:
            errors.append("again_dup")

        r2 = root / "r2"
        write_rows(r2 / "queue.ready.jsonl", [{"policy_key": "p3", "item_kind": "kind_c", "policy_score": 0.5}])
        rc, out = run(root, "no_fb", ctx(r2), lic(feedback_append_allowed=False))
        if rc != 1 or out.get("ready_flow_status") != "QI_PT_READY_FLOW_BLOCKED":
            errors.append("no_fb_status")
        if "feedback_append_not_allowed" not in out.get("blockers", []):
            errors.append("no_fb_reason")
        if (r2 / "applied.jsonl").exists() or (r2 / "state.json").exists():
            errors.append("no_fb_files")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi PT ready flow v0.5 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
