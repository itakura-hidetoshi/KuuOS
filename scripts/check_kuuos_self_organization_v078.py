#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_self_organization_v0_78 import SelfOrganizationV078Tests


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        SelfOrganizationV078Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "status": "KUUOS_SELF_ORGANIZATION_V0_78_VALIDATED",
        "flow": [
            "observation",
            "structural-diagnosis",
            "finite-candidate-generation",
            "shadow-comparison",
            "reobservation",
        ],
        "external_approval_required": False,
        "automatic_rollback_on_reobservation_failure": True,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
