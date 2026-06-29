#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_object_materialization_authorization_v0_94 import (
    RepositoryObjectMaterializationAuthorizationV094Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryObjectMaterializationAuthorizationV094Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "status": "KUUOS_REPOSITORY_OBJECT_MATERIALIZATION_AUTHORIZATION_V0_94_VALIDATED",
        "commit_candidate_certificate_required": True,
        "candidate_object_payloads_recomputed": True,
        "candidate_objects_deduplicated": True,
        "dependency_order_deterministic": True,
        "target_repository_identity_bound": True,
        "object_database_observation_required": True,
        "working_tree_observation_allowed": False,
        "source_parent_object_required": True,
        "queried_object_set_exact": True,
        "existing_exact_objects_reused": True,
        "oid_payload_collisions_rejected": True,
        "single_use_nonce_required": True,
        "object_count_bounded": True,
        "payload_bytes_bounded": True,
        "object_database_write_authority_separate": True,
        "object_database_write_performed": False,
        "commit_object_written": False,
        "index_write_performed": False,
        "working_tree_write_performed": False,
        "reference_mutation_authority_granted": False,
        "reference_mutated": False,
        "signing_performed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
