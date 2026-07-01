import hashlib
from pathlib import Path
import subprocess
import unittest

from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    LimitedTreeEntry,
    SANDBOX_MARKER_FILENAME,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
)
from runtime.kuuos_repository_tree_commit_materialization_v1_20 import (
    execute_repository_tree_commit_materialization,
)
from runtime.v120_tree_commit_materialization_policy import (
    build_repository_tree_commit_materialization_policy,
    build_repository_tree_commit_materialization_request,
)
from tests import test_kuuos_repository_bounded_blob_v1_19 as v119


class RepositoryTreeCommitV120Tests(unittest.TestCase):
    executor_id = "executor-v120"
    marker_token = "d" * 64
    message = "KuuOS limited tree and commit validation v1.20"

    def setUp(self) -> None:
        self.helper = v119.RepositoryBoundedBlobV119Tests(
            methodName="test_probe_normalization_is_fail_closed"
        )
        self.helper.setUp()
        self.root = self.helper.root
        self.prior = execute_v119(self.helper)
        marker = self.root / ".git" / SANDBOX_MARKER_FILENAME
        marker.write_text(self.marker_token + "\n", encoding="utf-8")
        self.parent_commit_oid = subprocess.run(
            ("git", "-C", str(self.root), "rev-parse", "HEAD"),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        self.entries = (
            LimitedTreeEntry(
                mode="100644",
                path="checkpoint.txt",
                blob_oid=self.prior.expected_blob_oid,
            ),
        )
        self.policy = build_repository_tree_commit_materialization_policy(
            "tree-commit-v120-tests",
            authorized_executor_ids=(self.executor_id,),
            allowed_repository_path_digests=(self.prior.repository_path_digest,),
        )
        self.request = build_repository_tree_commit_materialization_request(
            "tree-commit-v120",
            str(self.root),
            self.prior,
            self.entries,
            self.parent_commit_oid,
            self.message,
            executor_id=self.executor_id,
            sandbox_marker_token=self.marker_token,
            author_name="KuuOS Runtime",
            author_email="runtime@kuuos.invalid",
            committer_name="KuuOS Runtime",
            committer_email="runtime@kuuos.invalid",
            commit_epoch_seconds=1_800_000_200,
            requested_at_epoch_seconds=1_800_000_201,
        )

    def tearDown(self) -> None:
        self.helper.tearDown()

    @staticmethod
    def digest_tree(root: Path) -> tuple[tuple[str, str], ...]:
        if not root.exists():
            return ()
        return tuple(
            (
                str(path.relative_to(root)),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        )

    def non_object_snapshot(self):
        git_dir = self.root / ".git"
        index = git_dir / "index"
        return (
            self.digest_tree(git_dir / "refs"),
            self.digest_tree(git_dir / "logs"),
            hashlib.sha256(index.read_bytes()).hexdigest(),
            hashlib.sha256((self.root / "tracked.txt").read_bytes()).hexdigest(),
        )

    def test_new_tree_and_commit_are_materialized_without_other_writes(self) -> None:
        git_dir = self.root / ".git"
        before_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        before_other = self.non_object_snapshot()
        result = execute_repository_tree_commit_materialization(
            self.request,
            self.prior,
            self.message,
            self.policy,
        )
        after_objects = {path for path, _ in self.digest_tree(git_dir / "objects")}
        expected_paths = {
            f"{self.request.expected_tree_oid[:2]}/{self.request.expected_tree_oid[2:]}",
            f"{self.request.expected_commit_oid[:2]}/{self.request.expected_commit_oid[2:]}",
        }
        self.assertEqual(result.status, TREE_COMMIT_MATERIALIZED)
        self.assertEqual(after_objects - before_objects, expected_paths)
        self.assertEqual(before_other, self.non_object_snapshot())
        self.assertTrue(result.tree_object_database_write_performed)
        self.assertTrue(result.commit_object_database_write_performed)
        self.assertTrue(result.tree_content_exact)
        self.assertTrue(result.commit_content_exact)
        self.assertFalse(result.reference_write_performed)
        self.assertFalse(result.index_write_performed)
        self.assertFalse(result.working_tree_write_performed)
        self.assertFalse(result.reflog_write_performed)
        self.assertFalse(result.push_performed)
        self.assertFalse(result.signing_performed)
        self.assertTrue(result.result_digest)

    def test_exact_reuse_and_message_mismatch(self) -> None:
        first = execute_repository_tree_commit_materialization(
            self.request,
            self.prior,
            self.message,
            self.policy,
        )
        object_snapshot = self.digest_tree(self.root / ".git" / "objects")
        second = execute_repository_tree_commit_materialization(
            self.request,
            self.prior,
            self.message,
            self.policy,
        )
        self.assertEqual(first.status, TREE_COMMIT_MATERIALIZED)
        self.assertEqual(second.status, TREE_COMMIT_REUSED)
        self.assertFalse(second.tree_write_command_attempted)
        self.assertFalse(second.commit_write_command_attempted)
        self.assertFalse(second.object_database_write_performed)
        self.assertEqual(object_snapshot, self.digest_tree(self.root / ".git" / "objects"))
        rejected = execute_repository_tree_commit_materialization(
            self.request,
            self.prior,
            self.message + " tampered",
            self.policy,
        )
        self.assertEqual(rejected.status, TREE_COMMIT_REJECTED)
        self.assertFalse(rejected.commit_binding_exact)
        self.assertFalse(rejected.live_git_command_invoked)
        self.assertFalse(rejected.object_database_write_performed)


def execute_v119(helper):
    from runtime.kuuos_repository_live_object_materialization_v1_19 import (
        execute_repository_live_object_materialization,
    )

    return execute_repository_live_object_materialization(
        helper.request,
        helper.prior,
        helper.payload,
        helper.policy,
    )


if __name__ == "__main__":
    unittest.main()
