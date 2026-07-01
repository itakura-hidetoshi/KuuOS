from dataclasses import replace
import unittest

from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    TREE_COMMIT_ERROR,
    repository_tree_commit_materialization_result_digest,
)
from runtime.kuuos_repository_tree_commit_materialization_v1_20 import (
    execute_repository_tree_commit_materialization,
)
from runtime.v120_tree_commit_materialization_result import (
    repository_tree_commit_materialization_result_issues,
)
from tests import test_kuuos_repository_tree_commit_v1_20 as v120


class RepositoryTreeCommitAccountingV120Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v120.RepositoryTreeCommitV120Tests(
            methodName="test_exact_reuse_and_message_mismatch"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_tree_and_commit_writes(self) -> None:
        materialized = execute_repository_tree_commit_materialization(
            self.fixture.request,
            self.fixture.prior,
            self.fixture.message,
            self.fixture.policy,
        )
        simulated = replace(
            materialized,
            status=TREE_COMMIT_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            tree_present_after=False,
            commit_present_after=False,
            tree_type_exact=False,
            commit_type_exact=False,
            tree_content_exact=False,
            commit_content_exact=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_tree_commit_materialization_result_digest(simulated),
        )
        self.assertEqual(repository_tree_commit_materialization_result_issues(simulated), ())
        self.assertTrue(simulated.tree_write_command_succeeded)
        self.assertTrue(simulated.commit_write_command_succeeded)
        self.assertTrue(simulated.object_database_write_performed)
        self.assertTrue(simulated.live_repository_mutated)


if __name__ == "__main__":
    unittest.main()
