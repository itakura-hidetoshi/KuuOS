#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_object_materialization_receipt_v0_95 import (
    RepositoryObjectMaterializationReceiptV095Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryObjectMaterializationReceiptV095Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "status": "KUUOS_REPOSITORY_OBJECT_MATERIALIZATION_RECEIPT_V0_95_VALIDATED",
        "authorization_revalidated": True,
        "exact_plan_execution_required": True,
        "write_and_reuse_sets_exact": True,
        "post_object_database_observation_required": True,
        "parent_commit_preserved": True,
        "all_candidate_objects_present": True,
        "all_candidate_payloads_exact": True,
        "candidate_commit_present": True,
        "nonce_consumed_atomically": True,
        "authorization_valid_at_completion": True,
        "partial_materialization_rejected": True,
        "all_existing_objects_may_be_reused": True,
        "index_write_performed": False,
        "working_tree_write_performed": False,
        "reference_mutated": False,
        "signing_performed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
