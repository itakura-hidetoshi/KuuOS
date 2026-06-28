#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_snapshot_adapter_v0_79 import (
    capture_explicit_repository_snapshot,
)
from scripts.check_kuuos_repository_live_v079 import contract_paths
from tests.test_kuuos_repository_alignment_normal_form_v0_80 import (
    RepositoryAlignmentNormalFormV080Tests,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryAlignmentNormalFormV080Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    live_snapshot = capture_explicit_repository_snapshot(ROOT, contract_paths())
    live_certificate = certify_repository_alignment_normal_form(live_snapshot)
    if not (
        live_certificate.initial_score == 0
        and live_certificate.unique_terminal
        and live_certificate.unique_terminal_digest == live_snapshot.digest
        and live_certificate.explored_state_count == 1
    ):
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_NORMAL_FORM_V0_80_VALIDATED",
        "fixture_explored_states": 16,
        "fixture_explored_transitions": 32,
        "fixture_unique_terminal_score": 0,
        "live_repository_score": live_certificate.initial_score,
        "live_repository_is_normal_form": True,
        "strict_descent_required": True,
        "candidate_order_confluence_required": True,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
