#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_atomic_application_v0_92 import (
    RepositoryAtomicApplicationV092Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryAtomicApplicationV092Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "status": "KUUOS_REPOSITORY_ATOMIC_APPLICATION_V0_92_VALIDATED",
        "authorization_revalidated": True,
        "source_commit_rechecked": True,
        "source_snapshot_rechecked": True,
        "object_database_source": True,
        "working_tree_ignored": True,
        "exact_changed_paths_required": True,
        "result_normal_form_required": True,
        "rollback_material_exact": True,
        "nonce_and_snapshot_commit_atomic": True,
        "failure_no_effect": True,
        "isolated_snapshot_only": True,
        "live_repository_write_performed": False,
        "commit_created": False,
        "reference_mutated": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
