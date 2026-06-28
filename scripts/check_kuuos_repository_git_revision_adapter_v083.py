#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_repository_certificate_chain_v0_82 import (
    certificate_chain_record_issues,
)
from runtime.kuuos_repository_git_revision_adapter_v0_83 import (
    start_repository_certificate_chain_from_git,
)
from scripts.check_kuuos_repository_live_v079 import contract_paths
from tests.test_kuuos_repository_git_revision_adapter_v0_83 import (
    RepositoryGitRevisionAdapterV083Tests,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryGitRevisionAdapterV083Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    snapshot, observation, record, receipt = (
        start_repository_certificate_chain_from_git(
            "live-git-revision-adapter-v083",
            ROOT,
            "HEAD",
            contract_paths(),
            max_chain_length=4,
        )
    )
    if not (
        certificate_chain_record_issues(record) == ()
        and record.current_snapshot_digest == snapshot.digest
        and record.current_score == 0
        and record.current_normal_form_preserved
        and observation.object_database_read
        and not observation.working_tree_read
        and receipt.snapshots_from_object_database
        and receipt.working_tree_ignored
        and not receipt.external_approval_required
    ):
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_GIT_REVISION_ADAPTER_V0_83_VALIDATED",
        "git_object_database_read": True,
        "working_tree_ignored": True,
        "single_parent_required_for_advance": True,
        "changed_paths_from_git_diff": True,
        "inventory_escape_rejected": True,
        "merge_commit_rejected": True,
        "live_repository_score": record.current_score,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
