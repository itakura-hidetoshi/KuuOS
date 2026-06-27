#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT, DEFER, DEFERRED, READY, REJECT, REJECTED
from runtime.kuuos_connection_admission_v0_63 import evaluate_connection_admission
from tests.kuuos_connection_review_fixture_v0_63 import review_fixture


def main() -> int:
    checks: list[str] = []
    for decision, expected in (
        (ADMIT, READY),
        (REJECT, REJECTED),
        (DEFER, DEFERRED),
    ):
        proposal, request, packet = review_fixture(decision)
        receipt = evaluate_connection_admission(
            proposal,
            request,
            packet,
            current_epoch=15,
        )
        assert receipt.status == expected
        assert receipt.production_apply_ready is False
        assert receipt.state_write_performed is False
        assert receipt.authority_widened is False
        checks.append(decision)
    print(json.dumps({"status": "KUUOS_V0_63_VALIDATED", "checks": checks}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
