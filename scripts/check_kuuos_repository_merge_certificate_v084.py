#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_merge_certificate_v0_84 import (
    RepositoryMergeCertificateV084Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryMergeCertificateV084Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_MERGE_CERTIFICATE_V0_84_VALIDATED",
        "two_parent_order_exact": True,
        "common_root_required": True,
        "branch_suffixes_disjoint": True,
        "changed_paths_disjoint": True,
        "merge_tree_normal_form_required": True,
        "inventory_escape_rejected": True,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
