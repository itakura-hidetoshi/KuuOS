#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_frontier_certificate_v0_86 import (
    RepositoryFrontierCertificateV086Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryFrontierCertificateV086Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_FRONTIER_CERTIFICATE_V0_86_VALIDATED",
        "source_dag_bound": True,
        "source_edges_bound": True,
        "exact_terminal_frontier": True,
        "frontier_nonempty": True,
        "frontier_antichain": True,
        "all_nodes_frontier_covered": True,
        "merged_ancestors_excluded": True,
        "normal_form_preserved": True,
        "finite_frontier_bound": True,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
