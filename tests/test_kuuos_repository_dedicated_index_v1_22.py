import hashlib
import os
from pathlib import Path
import unittest

from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_MATERIALIZED,
    INDEX_REUSED,
    SANDBOX_MARKER_FILENAME,
)
from runtime.kuuos_repository_dedicated_index_v1_22 import (
    build_repository_dedicated_index_policy,
    build_repository_dedicated_index_request,
    execute_repository_dedicated_index,
)
from tests import test_kuuos_repository_constructed_commit_publication_v1_21 as v121


class RepositoryDedicatedIndexV122Tests(unittest.TestCase):
    marker_token = "e" * 64

    def setUp(self) -> None:
        self.helper = v121.RepositoryConstructedCommitPublicationV121Tests(
            methodName="test_constructed_commit_publication"
        )
        self.helper.setUp()
        self.root = self.helper.fixture.root
        self.v121_result = self.helper.execute()
        marker = self.root / ".git" / SANDBOX_MARKER_FILENAME
        marker.write_text(self.marker_token + "\n", encoding="utf-8")
        self.policy = build_repository_dedicated_index_policy(
            "dedicated-index-v122-tests",
            authorized_executor_ids=(self.helper.executor_id,),
            allowed_repository_path_digests=(
                self.helper.v120_result.repository_path_digest,
            ),
        )
        self.request = build_repository_dedicated_index_request(
            "dedicated-index-v122",
            str(self.root),
            self.helper.fixture.request,
            self.helper.v120_result,
            self.v121_result,
            executor_id=self.helper.executor_id,
            sandbox_marker_token=self.marker_token,
            requested_at_epoch_seconds=1_800_000_020,
        )

    def tearDown(self) -> None:
        self.helper.tearDown()

    def execute(self, request=None, policy=None, **kwargs):
        return execute_repository_dedicated_index(
            self.request if request is None else request,
            self.helper.fixture.request,
            self.helper.v120_result,
            self.v121_result,
            self.policy if policy is None else policy,
            **kwargs,
        )

    @staticmethod
    def file_digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def protected_snapshot(self):
        git_dir = self.root / ".git"
        return {
            "objects": self.helper.fixture.digest_tree(git_dir / "objects"),
            "refs": self.helper.fixture.digest_tree(git_dir / "refs"),
            "logs": self.helper.fixture.digest_tree(git_dir / "logs"),
            "canonical_index": self.file_digest(git_dir / "index"),
            "working_tree": self.file_digest(self.root / "tracked.txt"),
        }

    def test_exact_tree_is_loaded_into_dedicated_index_only(self) -> None:
        before = self.protected_snapshot()
        result = self.execute()
        after = self.protected_snapshot()
        index_path = self.root / ".git" / self.request.dedicated_index_filename
        self.assertEqual(result.status, INDEX_MATERIALIZED)
        self.assertTrue(index_path.is_file())
        self.assertTrue(result.index_entries_exact)
        self.assertTrue(result.dedicated_index_write_performed)
        self.assertTrue(result.live_repository_mutated)
        self.assertFalse(result.canonical_index_write_performed)
        self.assertFalse(result.current_object_database_write_performed)
        self.assertFalse(result.current_reference_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertEqual(before, after)

    def test_exact_existing_dedicated_index_is_reused(self) -> None:
        first = self.execute()
        index_path = self.root / ".git" / self.request.dedicated_index_filename
        digest = self.file_digest(index_path)
        second = self.execute()
        self.assertEqual(first.status, INDEX_MATERIALIZED)
        self.assertEqual(second.status, INDEX_REUSED)
        self.assertTrue(second.exact_existing_index_reused)
        self.assertFalse(second.read_tree_command_attempted)
        self.assertFalse(second.dedicated_index_write_performed)
        self.assertFalse(second.live_repository_mutated)
        self.assertEqual(digest, self.file_digest(index_path))


if __name__ == "__main__":
    unittest.main()
