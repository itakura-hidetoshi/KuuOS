import os
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    SANDBOX_MARKER_FILENAME,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
)
from runtime.kuuos_repository_tree_commit_materialization_v1_20 import (
    execute_repository_tree_commit_materialization,
)
from runtime.v120_tree_commit_materialization_policy import (
    build_repository_tree_commit_materialization_request,
)
from tests import test_kuuos_repository_tree_commit_v1_20 as v120


class RepositoryTreeCommitGuardsV120Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v120.RepositoryTreeCommitV120Tests(
            methodName="test_exact_reuse_and_message_mismatch"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_marker_rejects_before_git(self) -> None:
        marker = self.fixture.root / ".git" / SANDBOX_MARKER_FILENAME
        marker.unlink()
        result = execute_repository_tree_commit_materialization(
            self.fixture.request,
            self.fixture.prior,
            self.fixture.message,
            self.fixture.policy,
        )
        self.assertEqual(result.status, TREE_COMMIT_REJECTED)
        self.assertFalse(result.sandbox_marker_present)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        request = build_repository_tree_commit_materialization_request(
            "tree-commit-v120-unauthorized",
            str(self.fixture.root),
            self.fixture.prior,
            self.fixture.entries,
            self.fixture.parent_commit_oid,
            self.fixture.message,
            executor_id="unauthorized-v120",
            sandbox_marker_token=self.fixture.marker_token,
            author_name="KuuOS Runtime",
            author_email="runtime@kuuos.invalid",
            committer_name="KuuOS Runtime",
            committer_email="runtime@kuuos.invalid",
            commit_epoch_seconds=1_800_000_200,
            requested_at_epoch_seconds=1_800_000_202,
        )
        result = execute_repository_tree_commit_materialization(
            request,
            self.fixture.prior,
            self.fixture.message,
            self.fixture.policy,
        )
        self.assertEqual(result.status, TREE_COMMIT_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.object_database_write_performed)

    def test_nonliteral_git_is_rejected_before_process_launch(self) -> None:
        with patch("runtime.v120_tree_commit_git_adapter.subprocess.run") as process:
            with self.assertRaisesRegex(ValueError, "v120_git_executable_not_allowed"):
                execute_repository_tree_commit_materialization(
                    self.fixture.request,
                    self.fixture.prior,
                    self.fixture.message,
                    self.fixture.policy,
                    git_executable="not-git",
                )
            process.assert_not_called()

    def test_git_environment_override_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"GIT_OBJECT_DIRECTORY": directory}, clear=False):
                result = execute_repository_tree_commit_materialization(
                    self.fixture.request,
                    self.fixture.prior,
                    self.fixture.message,
                    self.fixture.policy,
                )
            self.assertEqual(result.status, TREE_COMMIT_MATERIALIZED)
            self.assertEqual(os.listdir(directory), [])


if __name__ == "__main__":
    unittest.main()
