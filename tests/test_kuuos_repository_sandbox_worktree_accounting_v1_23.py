from dataclasses import replace
import unittest

from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    WORKTREE_ERROR,
    repository_sandbox_worktree_result_digest,
)
from runtime.v123_sandbox_worktree_result import (
    repository_sandbox_worktree_result_issues,
)
from tests import test_kuuos_repository_sandbox_worktree_v1_23 as v123


class RepositorySandboxWorktreeAccountingV123Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v123.RepositorySandboxWorktreeV123Tests(
            methodName="test_exact_index_is_reflected_in_sandbox_only"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_error_preserves_completed_sandbox_write(self) -> None:
        materialized = self.fixture.execute()
        simulated = replace(
            materialized,
            status=WORKTREE_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            sandbox_files_exact=False,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_sandbox_worktree_result_digest(simulated),
        )
        self.assertEqual(repository_sandbox_worktree_result_issues(simulated), ())
        self.assertTrue(simulated.sandbox_working_tree_write_performed)
        self.assertTrue(simulated.live_repository_mutated)
        self.assertFalse(simulated.repository_root_working_tree_write_performed)
        self.assertFalse(simulated.dedicated_index_write_performed)
        self.assertFalse(simulated.current_object_database_write_performed)
        self.assertFalse(simulated.current_reference_write_performed)


if __name__ == "__main__":
    unittest.main()
