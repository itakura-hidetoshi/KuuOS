#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_qi_world_indra_transport_receipt_intake_scenarios_v1_7 import (
    run_indra_transport_receipt_intake_scenarios,
)


def main() -> int:
    result = run_indra_transport_receipt_intake_scenarios()
    assert result["status"] == "KUUOS_QI_WORLD_INDRA_RECEIPT_INTAKE_V1_7_OK"
    assert result["receipt_count"] == 7
    assert result["semantic_review_required"] is True
    assert result["runtime_transport_realized"] is False
    assert result["disposition"] == (
        "EXTERNAL_ANALYTIC_RECEIPTS_HASH_BOUND_SEMANTIC_REVIEW_REQUIRED"
    )
    assert all(value is False for value in result["intake_non_authority"].values())
    print("PASS: Qi-WORLD Indra transport receipt intake v1.7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
