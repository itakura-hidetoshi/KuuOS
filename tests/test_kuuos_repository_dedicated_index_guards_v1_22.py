from dataclasses import replace
import os
import tempfile
import unittest
from unittest.mock import patch

from runtime.kuuos_repository_dedicated_index_types_v1_22 import INDEX_REJECTED
from runtime.kuuos_repository_dedicated_index_v1_22 import (
    build_repository_dedicated_index_policy,
)
from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    repository_dedicated_index_request_digest,
)
from tests import test_kuuos_repository_dedicated_index_v1_22 as v122


class RepositoryDedicatedIndexGuardsV122Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v122.RepositoryDedicatedIndexV122Tests(
            methodName="test_exact_tree_is_loaded_into_dedicated_index_only"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_marker_rejects_before_git(self) -> None:
        marker = self.fixture.root / ".git" / "kuuos-dedicated-index-sandbox-v1_22"
        marker.unlink()
        result = self.fixture.execute()
        self.assertEqual(result.status, INDEX_REJECTED)
        self.assertFalse(result.sandbox_marker_exact)
        self.assertFalse(result.live_git_command_invoked)
        self.assertFalse(result.dedicated_index_write_performed)

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        policy = build_repository_dedicated_index_policy(
            "dedicated-index-v122-unauthorized",
            authorized_executor_ids=("another-executor",),
            allowed_repository_path_digests=(
                self.fixture.request.repository_path_digest,
            ),
        )
        result = self.fixture.execute(policy=policy)
        self.assertEqual(result.status, INDEX_REJECTED)
        self.assertFalse(result.executor_authorized)
        self.assertFalse(result.live_git_command_invoked)

    def test_mismatched_tree_binding_rejects_before_git(self) -> None:
        altered = replace(
            self.fixture.request,
            expected_tree_oid="f" * 40,
            request_digest="",
        )
        altered = replace(
            altered,
            request_digest=repository_dedicated_index_request_digest(altered),
        )
        result = self.fixture.execute(request=altered)
        self.assertEqual(result.status, INDEX_REJECTED)
        self.assertFalse(result.request_binding_exact)
        self.assertFalse(result.live_git_command_invoked)

    def test_nonliteral_git_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "v122_git_executable_not_allowed"):
            self.fixture.execute(git_executable="not-git")

    def test_inherited_git_index_file_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            external = os.path.join(directory, "external.index")
            with patch.dict(os.environ, {"GIT_INDEX_FILE": external}, clear=False):
                result = self.fixture.execute()
            self.assertFalse(os.path.exists(external))
        self.assertTrue(result.dedicated_index_write_performed)
        self.assertFalse(result.canonical_index_write_performed)


if __name__ == "__main__":
    unittest.main()
