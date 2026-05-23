#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "qi_bounded_tick_manual_runner_v0_1"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        daemon_dir = work / "daemon"
        out_dir = work / "out"
        shutil.copytree(EXAMPLE / "daemon", daemon_dir)
        raw_state = work / "raw_state.json"
        evidence = work / "evidence.json"
        shutil.copy2(EXAMPLE / "raw_state.json", raw_state)
        shutil.copy2(EXAMPLE / "evidence.json", evidence)

        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "run_qi_process_tensor_bounded_tick_from_daemon_v0_1.py"),
            "--daemon-dir",
            str(daemon_dir),
            "--raw-state",
            str(raw_state),
            "--evidence",
            str(evidence),
            "--output-dir",
            str(out_dir),
            "--write",
        ]
        completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if completed.returncode != 0:
            print(completed.stdout)
            print(completed.stderr)
            return completed.returncode

        receipt_path = daemon_dir / "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json"
        if not receipt_path.exists():
            print("ERROR: missing executor receipt")
            return 1
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        expected = {
            "executor_status": "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
            "source_invocation_decision": "SINGLE_TICK_INVOCATION_TOKEN_GRANTED",
            "single_tick_invocation_token": True,
            "tick_invoked": True,
            "grants_execution_authority": True,
            "grants_truth_authority": False,
            "grants_final_commitment_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_clinical_authority": False,
            "grants_theorem_authority": False,
            "grants_completed_identity_authority": False,
        }
        for key, value in expected.items():
            if receipt.get(key) != value:
                print(f"ERROR: {key} expected {value!r}, got {receipt.get(key)!r}")
                return 1
        for rel in [
            "run_manifest_v0_1.json",
            "next_raw_state_v0_1.json",
            "state_bundle_v0_1.json",
            "step_trace_v0_1.json",
        ]:
            if not (out_dir / rel).exists():
                print(f"ERROR: missing output {rel}")
                return 1
    print("PASS: Qi bounded tick manual runner example v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
