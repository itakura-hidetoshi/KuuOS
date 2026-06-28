#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from tests.test_kuuos_repository_revision_dag_v0_85 import (
    RepositoryRevisionDagV085Tests,
)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        RepositoryRevisionDagV085Tests
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1

    print(json.dumps({
        "status": "KUUOS_REPOSITORY_REVISION_DAG_V0_85_VALIDATED",
        "single_root_required": True,
        "source_reference_closure": True,
        "parent_arity_checked": True,
        "all_nodes_reachable": True,
        "acyclicity_checked": True,
        "normal_form_preserved": True,
        "finite_node_bound": True,
        "finite_edge_bound": True,
        "external_approval_required": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
