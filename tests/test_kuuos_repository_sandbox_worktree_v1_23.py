import hashlib
from pathlib import Path
import unittest

from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    SANDBOX_MARKER_FILENAME,
    WORKTREE_MATERIALIZED,
    WORKTREE_REUSED,
)
from runtime.kuuos_repository_sandbox_worktree_v1_23 import (
    build_repository_sandbox_worktree_policy,
    build_repository_sandbox_worktree_request,
    execute_repository_sandbox_worktree,
)
from runtime.v123_sandbox_worktree_validation import git_blob_oid
from tests import test_kuuos_repository_dedicated_index_v1_22 as v122


class RepositorySandboxWorktreeV123Tests(unittest.TestCase):
    marker_token = "f" * 64

    def setUp(self) -> None:
        self.helper = v122.RepositoryDedicatedIndexV122Tests(
            methodName="test_exact_tree_is_loaded_into_dedicated_index_only"
        )
        self.helper.setUp()
        self.root = self.helper.root
        self.v122_result = self.helper.execute()
        marker = self.root / ".git" / SANDBOX_MARKER_FILENAME
        marker.write_text(self.marker_token + "\n", encoding="utf-8")
        self.policy = build_repository_sandbox_worktree_policy(
            "sandbox-worktree-v123-tests",
            authorized_executor_ids=(self.helper.request.executor_id,),
            allowed_repository_path_digests=(
                self.v122_result.repository_path_digest,
            ),
        )
        self.request = build_repository_sandbox_worktree_request(
            "sandbox-worktree-v123",
            str(self.root),
            self.helper.request,
            self.v122_result,
            executor_id=self.helper.request.executor_id,
            sandbox_marker_token=self.marker_token,
            requested_at_epoch_seconds=1_800_000_030,
        )

    def tearDown(self) -> None:
        self.helper.tearDown()

    def execute(self, request=None, policy=None, **kwargs):
        return execute_repository_sandbox_worktree(
            self.request if request is None else request,
            self.helper.request,
            self.v122_result,
            self.policy if policy is None else policy,
            **kwargs,
        )

    @staticmethod
    def digest_tree(root: Path):
        if not root.exists():
            return ()
        return tuple(
            (
                str(path.relative_to(root)),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        )

    @staticmethod
    def file_digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def protected_snapshot(self):
        git_dir = self.root / ".git"
        return {
            "objects": self.digest_tree(git_dir / "objects"),
            "refs": self.digest_tree(git_dir / "refs"),
            "logs": self.digest_tree(git_dir / "logs"),
            "canonical_index": self.file_digest(git_dir / "index"),
            "dedicated_index": self.file_digest(
                git_dir / self.request.dedicated_index_filename
            ),
            "working_tree": self.file_digest(self.root / "tracked.txt"),
        }

    def test_exact_index_is_reflected_in_sandbox_only(self) -> None:
        before = self.protected_snapshot()
        result = self.execute()
        after = self.protected_snapshot()
        sandbox = self.root / self.request.sandbox_directory_name
        target = sandbox / "checkpoint.txt"
        self.assertEqual(result.status, WORKTREE_MATERIALIZED)
        self.assertTrue(target.is_file())
        self.assertEqual(
            git_blob_oid(target.read_bytes()),
            self.request.tree_entries[0].blob_oid,
        )
        self.assertTrue(result.sandbox_files_exact)
        self.assertTrue(result.sandbox_modes_exact)
        self.assertTrue(result.sandbox_has_no_extra_entries)
        self.assertTrue(result.sandbox_working_tree_write_performed)
        self.assertTrue(result.live_repository_mutated)
        self.assertFalse(result.repository_root_working_tree_write_performed)
        self.assertFalse(result.dedicated_index_write_performed)
        self.assertFalse(result.canonical_index_write_performed)
        self.assertFalse(result.current_object_database_write_performed)
        self.assertFalse(result.current_reference_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertEqual(before, after)

    def test_exact_existing_sandbox_is_reused(self) -> None:
        first = self.execute()
        sandbox = self.root / self.request.sandbox_directory_name
        digest = self.digest_tree(sandbox)
        second = self.execute()
        self.assertEqual(first.status, WORKTREE_MATERIALIZED)
        self.assertEqual(second.status, WORKTREE_REUSED)
        self.assertTrue(second.exact_existing_sandbox_reused)
        self.assertFalse(second.checkout_command_attempted)
        self.assertFalse(second.sandbox_working_tree_write_performed)
        self.assertFalse(second.live_repository_mutated)
        self.assertEqual(digest, self.digest_tree(sandbox))


if __name__ == "__main__":
    unittest.main()
