#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_evolution_admission_v0_89 import (
    RepositoryEvolutionAdmissionV089Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryEvolutionAdmissionV089Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_EVOLUTION_ADMISSION_V0_89_VALIDATED",
        "minimum_replay_count": 2,
        "replay_result_identity": True,
        "certificate_freshness": True,
        "future_certificate_rejected": True,
        "source_revision_unchanged": True,
        "source_snapshot_unchanged": True,
        "git_object_database_source": True,
        "working_tree_ignored": True,
        "shadow_reject_not_admitted": True,
        "stable_no_change_preserved": True,
        "external_approval_required": True,
        "external_approval_granted": False,
        "admission_is_proposal_only": True,
        "patch_application_authority_granted": False,
        "commit_authority_granted": False,
        "reference_mutation_authority_granted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
