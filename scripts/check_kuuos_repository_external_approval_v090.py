#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_external_approval_v0_90 import (
    RepositoryExternalApprovalV090Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryExternalApprovalV090Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_EXTERNAL_APPROVAL_V0_90_VALIDATED",
        "admission_certificate_binding": True,
        "approval_policy_binding": True,
        "authorized_approver_binding": True,
        "authorized_signing_key_binding": True,
        "external_signature_verification_receipt": True,
        "authorized_verifier_binding": True,
        "revocation_registry_receipt": True,
        "authorized_revocation_authority_binding": True,
        "approval_expiry_enforced": True,
        "evidence_freshness_enforced": True,
        "distinct_approval_roles_enforced": True,
        "revoked_approval_rejected": True,
        "application_authorization_eligible_only": True,
        "patch_application_authority_granted": False,
        "commit_authority_granted": False,
        "reference_mutation_authority_granted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
