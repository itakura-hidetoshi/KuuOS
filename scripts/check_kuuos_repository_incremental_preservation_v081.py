#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_incremental_preservation_v0_81 import (
    preserve_repository_normal_form_incrementally,
)
from runtime.kuuos_repository_snapshot_adapter_v0_79 import (
    capture_explicit_repository_snapshot,
)
from scripts.check_kuuos_repository_live_v079 import contract_paths
from tests.test_kuuos_repository_incremental_preservation_v0_81 import (
    RepositoryIncrementalPreservationV081Tests,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryIncrementalPreservationV081Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    live_snapshot = capture_explicit_repository_snapshot(ROOT, contract_paths())
    live_normal_form = certify_repository_alignment_normal_form(live_snapshot)
    live_incremental = preserve_repository_normal_form_incrementally(
        live_snapshot,
        live_snapshot,
        live_normal_form,
    )
    if not (
        live_incremental.current_normal_form_preserved
        and live_incremental.current_score == 0
        and not live_incremental.full_recheck_performed
        and not live_incremental.rechecked_scope_ids
    ):
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_INCREMENTAL_PRESERVATION_V0_81_VALIDATED",
        "local_contract_recheck": True,
        "unchanged_scope_reuse": True,
        "global_change_forces_full_recheck": True,
        "missing_path_breaks_preservation": True,
        "stale_certificate_rejected": True,
        "live_repository_score": live_incremental.current_score,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
