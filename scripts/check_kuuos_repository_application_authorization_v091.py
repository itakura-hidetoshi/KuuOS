#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_application_authorization_v0_91 import (
    RepositoryApplicationAuthorizationV091Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryApplicationAuthorizationV091Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_APPLICATION_AUTHORIZATION_V0_91_VALIDATED",
        "external_approval_binding": True,
        "application_scope_binding": True,
        "patch_bundle_binding": True,
        "source_commit_binding": True,
        "source_snapshot_binding": True,
        "allowed_path_scope": True,
        "protected_paths_excluded": True,
        "single_use_nonce_registry": True,
        "nonce_unused_required": True,
        "nonce_not_revoked_required": True,
        "authorization_expiry_enforced": True,
        "source_and_nonce_freshness_enforced": True,
        "object_database_source": True,
        "working_tree_ignored": True,
        "application_authorization_granted": True,
        "patch_application_executed": False,
        "commit_authority_granted": False,
        "reference_mutation_authority_granted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
