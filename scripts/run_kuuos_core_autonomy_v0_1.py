#!/usr/bin/env python3
"""
run_kuuos_core_autonomy_v0_1.py

Stdlib-only minimal local autonomy loop for KuuOS core governance.

Autonomy here means bounded local self-checking:
  sense -> validate -> decide -> audit

It does not call external APIs, does not execute world actions, and does not grant
clinical, theorem, truth, institutional, or execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "specs" / "kuuos_core_autonomy_contract_v0_1.json"
DEFAULT_AUDIT_LOG = ROOT / "audit" / "kuuos_core_autonomy_audit_v0_1.jsonl"
CONTRACT_ID = "kuuos_core_autonomy_contract_v0_1"
AUDIT_SCHEMA = "kuuos_core_autonomy_audit_event_v0_1"
DEFAULT_CORE_COMMAND = [sys.executable, "scripts/run_core_governance_full_checks_v0_1.py"]


@dataclass(frozen=True)
class PhaseResult:
    phase: str
    status: str
    detail: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {"phase": self.phase, "status": self.status, "detail": self.detail}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_event_hash(event: dict[str, Any]) -> str:
    body = dict(event)
    body.pop("event_hash", None)
    return sha256_text(canonical_json(body))


def read_previous_event_hash(audit_log: pathlib.Path) -> str | None:
    if not audit_log.exists():
        return None
    last: str | None = None
    with audit_log.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line
    if last is None:
        return None
    try:
        data = json.loads(last)
    except json.JSONDecodeError:
        return "CORRUPT_AUDIT_LOG"
    value = data.get("event_hash")
    return value if isinstance(value, str) else "MISSING_EVENT_HASH"


def append_audit_event(audit_log: pathlib.Path, event: dict[str, Any]) -> None:
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    with audit_log.open("a", encoding="utf-8") as f:
        f.write(canonical_json(event) + "\n")


def phase_sense() -> PhaseResult:
    required = [
        ROOT / "README.md",
        ROOT / "Makefile",
        ROOT / "scripts" / "run_core_governance_full_checks_v0_1.py",
        CONTRACT_PATH,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    detail = {
        "root": str(ROOT),
        "required_files": [str(path.relative_to(ROOT)) for path in required],
        "missing_files": missing,
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
    }
    return PhaseResult("sense", "PASS" if not missing else "HOLD", detail)


def phase_contract_check(contract: dict[str, Any]) -> PhaseResult:
    errors: list[str] = []
    if contract.get("contract_id") != CONTRACT_ID:
        errors.append("unexpected contract_id")
    if contract.get("status") != "CORE_AUTONOMY_MINIMAL_BASELINE":
        errors.append("unexpected status")
    if contract.get("runtime_entrypoint") != "scripts/run_kuuos_core_autonomy_v0_1.py":
        errors.append("unexpected runtime_entrypoint")
    boundary = contract.get("authority_boundary", {})
    for key in [
        "grants_execution_authority",
        "grants_clinical_authority",
        "grants_diagnosis_authority",
        "grants_treatment_authority",
        "grants_prescription_authority",
        "grants_triage_authority",
        "grants_theorem_authority",
        "grants_truth_authority",
        "grants_memory_overwrite_authority",
        "grants_governance_bypass_authority",
        "uses_external_services",
    ]:
        if boundary.get(key) is not False:
            errors.append(f"authority boundary must be false: {key}")
    for key in ["validation_only", "candidate_only", "local_runtime_only", "audit_receipt_only"]:
        if boundary.get(key) is not True:
            errors.append(f"authority boundary must be true: {key}")
    default_policy = contract.get("default_policy", {})
    if default_policy.get("external_api_calls_allowed") is not False:
        errors.append("external_api_calls_allowed must be false")
    if default_policy.get("stdlib_only") is not True:
        errors.append("stdlib_only must be true")
    return PhaseResult("contract_check", "PASS" if not errors else "HOLD", {"errors": errors})


def phase_validate(command: Sequence[str], timeout_seconds: int) -> PhaseResult:
    started = time.time()
    try:
        completed = subprocess.run(
            list(command),
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
        )
        output = completed.stdout or ""
        status = "PASS" if completed.returncode == 0 else "HOLD"
        detail = {
            "command": list(command),
            "returncode": completed.returncode,
            "duration_seconds": round(time.time() - started, 3),
            "output_tail": output[-4000:],
        }
        return PhaseResult("validate", status, detail)
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return PhaseResult(
            "validate",
            "HOLD",
            {
                "command": list(command),
                "timeout_seconds": timeout_seconds,
                "duration_seconds": round(time.time() - started, 3),
                "output_tail": output[-4000:],
            },
        )


def phase_self_test_validate() -> PhaseResult:
    return PhaseResult(
        "validate",
        "PASS",
        {
            "command": ["self-test"],
            "returncode": 0,
            "duration_seconds": 0,
            "output_tail": "PASS: self-test validation stub completed",
        },
    )


def decide(phases: list[PhaseResult]) -> tuple[str, bool]:
    if all(phase.status == "PASS" for phase in phases):
        return "PASS", False
    return "HOLD", True


def build_event(
    *,
    cycle_id: str,
    runtime_mode: str,
    phases: list[PhaseResult],
    decision_state: str,
    safety_stop: bool,
    previous_event_hash: str | None,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "timestamp_utc": utc_now(),
        "cycle_id": cycle_id,
        "contract_id": CONTRACT_ID,
        "runtime_mode": runtime_mode,
        "phase_results": [phase.to_json() for phase in phases],
        "decision_state": decision_state,
        "safety_stop": safety_stop,
        "previous_event_hash": previous_event_hash,
        "authority_boundary": {
            "validation_only": True,
            "candidate_only": True,
            "local_runtime_only": True,
            "grants_execution_authority": False,
            "grants_clinical_authority": False,
            "grants_theorem_authority": False,
            "grants_truth_authority": False,
            "uses_external_services": False,
        },
    }
    event["event_hash"] = compute_event_hash(event)
    return event


def run_cycle(args: argparse.Namespace, contract: dict[str, Any], runtime_mode: str) -> dict[str, Any]:
    cycle_id = str(uuid.uuid4())
    phases: list[PhaseResult] = [phase_sense(), phase_contract_check(contract)]

    if runtime_mode == "contract-check":
        pass
    elif args.self_test_check:
        phases.append(phase_self_test_validate())
    elif all(phase.status == "PASS" for phase in phases):
        command = args.command if args.command else DEFAULT_CORE_COMMAND
        phases.append(phase_validate(command, args.timeout_seconds))

    decision_state, safety_stop = decide(phases)
    previous_hash = read_previous_event_hash(args.audit_log)
    if previous_hash in {"CORRUPT_AUDIT_LOG", "MISSING_EVENT_HASH"}:
        phases.append(PhaseResult("audit", "HOLD", {"error": previous_hash}))
        decision_state, safety_stop = "HOLD", True
        previous_hash = previous_hash

    event = build_event(
        cycle_id=cycle_id,
        runtime_mode=runtime_mode,
        phases=phases,
        decision_state=decision_state,
        safety_stop=safety_stop,
        previous_event_hash=previous_hash,
    )
    append_audit_event(args.audit_log, event)
    print(canonical_json(event))
    return event


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the KuuOS core autonomy v0.1 local loop")
    parser.add_argument("--mode", choices=["contract-check", "once", "daemon"], default="once")
    parser.add_argument("--audit-log", type=pathlib.Path, default=DEFAULT_AUDIT_LOG)
    parser.add_argument("--timeout-seconds", type=positive_int, default=900)
    parser.add_argument("--interval-seconds", type=positive_int, default=300)
    parser.add_argument("--max-cycles", type=positive_int, default=1)
    parser.add_argument("--self-test-check", action="store_true", help="Use a local validation stub for fast runner self-test")
    parser.add_argument("--command", nargs=argparse.REMAINDER, help="Override validation command; place after all runner flags")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    contract = load_json(CONTRACT_PATH)

    mode = args.mode
    max_cycles = args.max_cycles if mode == "daemon" else 1
    exit_code = 0

    for index in range(max_cycles):
        event = run_cycle(args, contract, mode)
        if event["decision_state"] != "PASS":
            exit_code = 1
            break
        if mode == "daemon" and index < max_cycles - 1:
            time.sleep(args.interval_seconds)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
