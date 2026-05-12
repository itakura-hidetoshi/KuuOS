#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AI_PROVIDER_BOUNDARY_AUDIT_EVENT_v0_1.md"
FIXTURES = ROOT / "specs" / "ai_provider_boundary_fixtures_v0_1.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "memory_truth_granted",
    "decision_authority_granted",
    "teni_authority_granted",
]


def status_for(case: dict) -> str:
    if case.get("bypasses_governance"):
        return "QUARANTINE"
    if case.get("claims_authority"):
        return "REJECT"
    if case.get("hides_uncertainty"):
        return "REPAIR"
    return "CANDIDATE"


def make_event(case: dict) -> dict:
    status = status_for(case)
    payload = {
        "provider": case.get("provider"),
        "boundary_version": "0.1",
        "input_status": "RAW_OUTPUT",
        "output_status": status,
        "claims_authority": bool(case.get("claims_authority")),
        "hides_uncertainty": bool(case.get("hides_uncertainty")),
        "bypasses_governance": bool(case.get("bypasses_governance")),
        "required_route": status.lower(),
        "reason": "provider_boundary_applied",
        **{field: False for field in FALSE_FIELDS},
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "event_id": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "timestamp": "2026-05-12T00:00:00Z",
        **payload,
    }


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing AI Provider Boundary audit event doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["record surfaces only", "execution_authority_granted: false"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for case in data.get("fixtures", []):
        event = make_event(case)
        if event["output_status"] != case.get("expected_status"):
            errors.append(f"{case.get('id')}: output_status mismatch")
        if len(event["event_id"]) != 64:
            errors.append(f"{case.get('id')}: event_id must be sha256 hex")
        for field in FALSE_FIELDS:
            if event[field] is not False:
                errors.append(f"{case.get('id')}: {field} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: AI Provider Boundary audit events validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
