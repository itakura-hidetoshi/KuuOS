from dataclasses import replace
import unittest

from runtime.kuuos_repository_bounded_tree_commit_types_v1_20 import (
    TREE_COMMIT_ERROR,
    TREE_COMMIT_REJECTED,
    repository_bounded_tree_commit_result_digest,
)
from runtime.kuuos_repository_bounded_tree_commit_v1_20 import (
    repository_bounded_tree_commit_result_issues,
)
from tests import test_kuuos_repository_bounded_tree_commit_v1_20 as v120_tests


class RepositoryBoundedTreeCommitGuardsV120Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v120_tests.RepositoryBoundedTreeCommitV120Tests(
            methodName="test_tree_and_commit_objects_materialize_without_other_writes"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_marker_rejects_before_git(self) -> None:
        self.fixture.marker_path.unlink()
        result = self.fixture.execute()
        self.assertEqual(result.status, TREE_COMMIT_REJECTED)
        self.assertFalse(result.sandbox_marker_present)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_missing_retained_leaf_fails_before_tree_write(self) -> None:
        candidate_blob_oids = {
            blob.git_blob_oid for blob in self.fixture.candidate.blob_candidates
        }
        retained = next(
            entry
            for entry in self.fixture.parent_inventory.entries
            if entry.git_object_oid not in candidate_blob_oids
        )
        object_path = (
            self.fixture.root
            / ".git"
            / "objects"
            / retained.git_object_oid[:2]
            / retained.git_object_oid[2:]
        )
        object_path.unlink()
        result = self.fixture.execute()
        self.assertEqual(result.status, TREE_COMMIT_ERROR)
        self.assertFalse(result.referenced_objects_present)
        self.assertEqual(result.tree_write_count, 0)
        self.assertEqual(result.commit_write_count, 0)
        self.assertFalse(result.object_database_write_performed)

    def test_error_result_preserves_completed_writes(self) -> None:
        materialized = self.fixture.execute()
        checks = dict(materialized.checks)
        checks["commit_object_content_exact"] = False
        simulated = replace(
            materialized,
            status=TREE_COMMIT_ERROR,
            reason="SIMULATED_POSTCONDITION_ERROR",
            commit_object_content_exact=False,
            checks=checks,
            result_digest="",
        )
        simulated = replace(
            simulated,
            result_digest=repository_bounded_tree_commit_result_digest(simulated),
        )
        self.assertEqual(repository_bounded_tree_commit_result_issues(simulated), ())
        self.assertGreater(simulated.tree_write_count, 0)
        self.assertEqual(simulated.commit_write_count, 1)
        self.assertTrue(simulated.object_database_write_performed)
        self.assertTrue(simulated.live_repository_mutated)


if __name__ == "__main__":
    unittest.main()
