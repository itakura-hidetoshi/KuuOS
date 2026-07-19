#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    STATUS_READY,
    build_codeai_reobservation_gated_git_lifecycle_continuation,
)

EXAMPLE = Path("examples/codeai_reobservation_gated_git_lifecycle_continuation_v0_1.json")


def main() -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    expected = payload.pop("expected")
    result = build_codeai_reobservation_gated_git_lifecycle_continuation(**payload)
    if result.status != STATUS_READY or result.receipt is None or result.next_registry is None:
        raise SystemExit(f"continuation blocked: {result.issues}")
    actual = {
        "status": result.status,
        "next_effect_phase": result.receipt["next_effect_phase"],
        "codeai_disposition": result.receipt["codeai_disposition"],
        "one_effect_lease_issued": result.receipt["one_effect_lease_issued"],
        "push_authority_granted": result.receipt["push_authority_granted"],
        "state_projection_performed": result.receipt["state_projection_performed"],
        "source_reobservation_receipt_consumed": result.receipt["source_reobservation_receipt_consumed"],
        "continuation_nonce_consumed": result.receipt["continuation_nonce_consumed"],
        "automatic_effect_execution_performed": result.receipt["automatic_effect_execution_performed"],
        "next_registry_revision": result.next_registry["registry_revision"],
        "next_consumed_count": result.next_registry["consumed_count"],
    }
    if actual != expected:
        raise SystemExit(f"continuation example mismatch: expected={expected!r} actual={actual!r}")
    if result.delegated_lifecycle_receipt is None:
        raise SystemExit("delegated lifecycle receipt missing")
    if result.receipt["general_git_authority_granted"]:
        raise SystemExit("general Git authority must remain denied")
    if result.receipt["reobservation_state_treated_as_authority"]:
        raise SystemExit("re-observation state must not be treated as authority")
    print(json.dumps(actual, sort_keys=True))


if __name__ == "__main__":
    main()
