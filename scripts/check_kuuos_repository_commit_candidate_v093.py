#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_commit_candidate_v0_93 import (
    RepositoryCommitCandidateV093Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryCommitCandidateV093Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "status": "KUUOS_REPOSITORY_COMMIT_CANDIDATE_V0_93_VALIDATED",
        "atomic_application_receipt_required": True,
        "final_snapshot_exactly_bound": True,
        "single_parent_exactly_bound": True,
        "parent_tree_inventory_required": True,
        "parent_tree_object_database_read": True,
        "parent_tree_working_tree_read": False,
        "complete_parent_path_coverage": True,
        "parent_modes_preserved": True,
        "non_text_parent_oids_retained": True,
        "git_blob_candidates_exact": True,
        "git_tree_candidates_exact": True,
        "commit_payload_exact": True,
        "candidate_oid_deterministic": True,
        "payload_sha256_retained": True,
        "object_database_write_performed": False,
        "index_write_performed": False,
        "working_tree_write_performed": False,
        "commit_created": False,
        "reference_mutated": False,
        "signing_performed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
