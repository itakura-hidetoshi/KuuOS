#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_cbf_gate_certificate_v0_1.py"

GOOD_RECEIPT = {
    "receipt_status": "QI_CONNECTOR_CASE_RECEIPT_READY",
    "receipt_id": "qi-connector-case-test-0001",
    "incident_id": "qi-incident-test-0001",
    "connector_kind": "github_issue",
    "target_repo": "itakura-hidetoshi/KuuOS",
    "connector_call_performed": True,
    "external_case_created": True,
    "outbound_delivery_performed": True,
    "external_case_number": 999,
    "external_case_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/999",
    "idempotency_key": "qi-connector-case-example-0001"
}

CTX = {
    "cbf_profile": "qi_connector_live_result_ingestion_v0_1",
    "connector_cbf_gate_enabled": True,
    "duplicate_risk_score": 0.0,
    "max_duplicate_risk": 0.0,
    "scope_risk_score": 0.0,
    "max_scope_risk": 0.0
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_case(root: pathlib.Path, receipt: dict, context: dict, name: str) -> tuple[int, dict]:
    receipt_path = root / f"{name}_receipt.json"
    context_path = root / f"{name}_context.json"
    out = root / f"{name}_certificate.json"
    dump(receipt_path, receipt)
    dump(context_path, context)
    completed = subprocess.run([
        sys.executable,
        str(CLI),
        "--receipt", str(receipt_path),
        "--context", str(context_path),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    return completed.returncode, load(out) if out.is_file() else {}


def barrier_map(cert: dict) -> dict:
    return {item.get("name"): item for item in cert.get("cbf_barriers", [])}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append("cli_missing")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, good = run_case(root, GOOD_RECEIPT, CTX, "good")
        if rc != 0:
            errors.append("good_returncode_mismatch")
        if good.get("cbf_ok") is not True:
            errors.append("good_cbf_not_true")
        if good.get("connector_result_ingested") is not True:
            errors.append("good_ingested_not_true")
        if good.get("cbf_margin_min", -1) < 0:
            errors.append("good_margin_negative")

        missing_live = {**GOOD_RECEIPT, "external_case_url": None}
        rc, missing = run_case(root, missing_live, CTX, "missing")
        if rc != 1:
            errors.append("missing_returncode_mismatch")
        if missing.get("cbf_ok") is not False:
            errors.append("missing_cbf_not_false")
        if barrier_map(missing).get("h_live_result_present", {}).get("ok") is not False:
            errors.append("missing_live_barrier_not_false")

        risky_ctx = {**CTX, "duplicate_risk_score": 0.2, "max_duplicate_risk": 0.0}
        rc, risky = run_case(root, GOOD_RECEIPT, risky_ctx, "risky")
        if rc != 1:
            errors.append("risky_returncode_mismatch")
        if risky.get("cbf_ok") is not False:
            errors.append("risky_cbf_not_false")
        if barrier_map(risky).get("h_duplicate_risk", {}).get("ok") is not False:
            errors.append("risky_duplicate_barrier_not_false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi CBF gate certificate check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
