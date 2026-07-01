from dataclasses import replace
import unittest

from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    WORKTREE_REJECTED,
    repository_sandbox_worktree_request_digest,
)
from runtime.kuuos_repository_sandbox_worktree_v1_23 import (
    build_repository_sandbox_worktree_policy,
)
from tests import test_kuuos_repository_sandbox_worktree_v1_23 as v123


class RepositorySandboxWorktreeGuardsV123Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = v123.RepositorySandboxWorktreeV123Tests(
            methodName="test_exact_index_is_reflected_in_sandbox_only"
        )
        self.fixture.setUp()

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def test_missing_marker_rejects_before_git(self) -> None:
        marker = self.fixture.root / ".git" / "kuuos-sandbox-worktree-authority-v1_23"
        marker.unlink()
        result = self.fixture.execute()
        self.assertEqual(result.status, WORKTREE_REJECTED)
        self.assertFalse(result.sandbox_marker_exact)
        self.assertFalse(result.live_git_command_invoked)

    def test_unauthorized_executor_rejects_before_git(self) -> None:
        policy = build_repository_sandbox_worktree_policy(
            "sandbox-worktree-v123-unauthorized",
            authorized_executor_ids=("another-executor",),
            allowed_repository_path_digests=(
                self.fixture.request.repository_path_digest,
            ),
        )
        result = self.fixture.execute(policy=policy)
        self.assertEqual(result.status, WORKTREE_REJECTED)
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
            request_digest=repository_sandbox_worktree_request_digest(altered),
        )
        result = self.fixture.execute(request=altered)
        self.assertEqual(result.status, WORKTREE_REJECTED)
        self.assertFalse(result.request_binding_exact)
        self.assertFalse(result.live_git_command_invoked)

    def test_existing_mismatched_sandbox_is_not_overwritten(self) -> None:
        sandbox = self.fixture.root / self.fixture.request.sandbox_directory_name
        sandbox.mkdir()
        target = sandbox / "checkpoint.txt"
        target.write_text("mismatch\n", encoding="utf-8")
        before = target.read_bytes()
        result = self.fixture.execute()
        self.assertEqual(result.status, WORKTREE_REJECTED)
        self.assertFalse(result.sandbox_files_exact)
        self.assertFalse(result.live_git_command_invoked)
        self.assertEqual(before, target.read_bytes())

    def test_nonliteral_git_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "v123_git_executable_not_allowed"):
            self.fixture.execute(git_executable="not-git")


if __name__ == "__main__":
    unittest.main()
