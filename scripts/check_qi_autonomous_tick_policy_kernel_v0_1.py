#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_autonomous_tick_policy_kernel_v0_1.py"
ROOT_ID = "qi-root-test-0001"


def packet(action: str = "advance_tick", uncertainty: float = 0.1):
    return {
        "decision": {"root_id": ROOT_ID, "decision_id": "d1", "decision_action": action, "uncertainty": uncertainty},
        "cbf": {"root_id": ROOT_ID, "cbf_id": "c1", "cbf_ok": True, "cbf_action": "advance_tick", "barrier_closed": False},
        "token": {"root_id": ROOT_ID, "token_ledger_id": "t1", "token_ledger_ok": True, "token_ledger_action": "advance_tick", "remaining_tokens": 10, "minimum_required_tokens": 1, "current_tick": 7},
        "pt": {"root_id": ROOT_ID, "process_tensor_id": "p1", "process_tensor_ok": True, "process_tensor_action": "advance_tick", "non_markov_unresolved": False, "recovery_witness_missing": False},
        "ctx": {"current_tick": 7, "tick_policy_enabled": True, "read_only_policy_surface": True, "notify_uncertainty_threshold": 0.45, "ticket_uncertainty_threshold": 0.65, "handover_uncertainty_threshold": 0.85},
    }


def dump(path: pathlib.Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_case(root: pathlib.Path, name: str, data: dict) -> tuple[int, dict]:
    files = {}
    for key in ("decision", "cbf", "token", "pt", "ctx"):
        files[key] = root / f"{name}_{key}.json"
        dump(files[key], data[key])
    out = root / f"{name}_out.json"
    done = subprocess.run([
        sys.executable, str(CLI),
        "--decisionos", str(files["decision"]),
        "--cbf", str(files["cbf"]),
        "--token-ledger", str(files["token"]),
        "--process-tensor", str(files["pt"]),
        "--context", str(files["ctx"]),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return done.returncode, json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, a = run_case(root, "advance", packet())
        if rc != 0 or a.get("selected_action") != "advance_tick" or a.get("next_tick_number") != 8:
            errors.append("advance_case_failed")

        low = packet()
        low["token"]["remaining_tokens"] = 0
        rc, h = run_case(root, "hold", low)
        if rc != 0 or h.get("selected_action") != "hold":
            errors.append("hold_case_failed")

        obs = packet()
        obs["pt"]["non_markov_unresolved"] = True
        rc, o = run_case(root, "observe", obs)
        if rc != 0 or o.get("selected_action") != "observe":
            errors.append("observe_case_failed")

        rc, tk = run_case(root, "ticket", packet(uncertainty=0.7))
        if rc != 0 or tk.get("selected_action") != "ticket":
            errors.append("ticket_case_failed")

        rc, ho = run_case(root, "handover", packet(uncertainty=0.9))
        if rc != 0 or ho.get("selected_action") != "handover":
            errors.append("handover_case_failed")

        fr = packet()
        fr["decision"]["freeze_required"] = True
        rc, f = run_case(root, "freeze", fr)
        if rc != 0 or f.get("selected_action") != "freeze" or f.get("advance_tick_allowed") is not False:
            errors.append("freeze_case_failed")

        bad = packet()
        bad["pt"]["root_id"] = "other-root"
        rc, b = run_case(root, "blocked", bad)
        if rc != 1 or b.get("policy_status") != "QI_AUTONOMOUS_TICK_POLICY_BLOCKED":
            errors.append("blocked_case_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi autonomous tick policy kernel check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
