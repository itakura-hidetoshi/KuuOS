from dataclasses import replace
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

from runtime.kuuos_repository_checkpoint_atomic_cas_transition_types_v1_16 import (
    repository_checkpoint_atomic_cas_transition_result_digest,
)
from runtime.kuuos_repository_checkpoint_live_git_preflight_types_v1_17 import (
    PREFLIGHT_READY,
    PREFLIGHT_REJECTED,
)
from runtime.kuuos_repository_checkpoint_live_git_preflight_v1_17 import (
    build_repository_checkpoint_live_git_preflight_policy,
    build_repository_checkpoint_live_git_preflight_request,
    execute_repository_checkpoint_live_git_preflight,
)
from tests import test_kuuos_repository_checkpoint_atomic_cas_transition_v1_16 as v116_tests


class RepositoryCheckpointLiveGitPreflightV117Tests(unittest.TestCase):
    checkpoint_reference = "refs/kuuos/checkpoints/live-v117"

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self._git("init", "-b", "main")
        self._git("config", "user.name", "KuuOS Test")
        self._git("config", "user.email", "kuuos-test@example.invalid")
        tracked = self.root / "tracked.txt"
        tracked.write_text("first\n", encoding="utf-8")
        self._git("add", "tracked.txt")
        self._git("commit", "-m", "first")
        self.first_oid = self._git("rev-parse", "HEAD").strip().lower()
        tracked.write_text("second\n", encoding="utf-8")
        self._git("add", "tracked.txt")
        self._git("commit", "-m", "second")
        self.second_oid = self._git("rev-parse", "HEAD").strip().lower()
        self._git("update-ref", self.checkpoint_reference, self.first_oid)

        helper = v116_tests.RepositoryCheckpointAtomicCasTransitionV116Tests(
            methodName="test_same_input_is_deterministic"
        )
        helper.setUp()
        base_transition, _, _ = helper.apply()
        self.transition = self._transition(
            base_transition,
            expected_oid=self.first_oid,
            proposed_oid=self.second_oid,
        )
        self.policy = build_repository_checkpoint_live_git_preflight_policy(
            "checkpoint-live-git-preflight-policy-v117-tests"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ("git", "-C", str(self.root), *arguments),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            shell=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"git failed: {arguments}: {completed.stderr.strip()}"
            )
        return completed.stdout

    def _transition(self, base, *, expected_oid: str, proposed_oid: str):
        transition = replace(
            base,
            checkpoint_reference=self.checkpoint_reference,
            expected_current_oid=expected_oid,
            proposed_checkpoint_oid=proposed_oid,
            result_digest="",
        )
        return replace(
            transition,
            result_digest=repository_checkpoint_atomic_cas_transition_result_digest(
                transition
            ),
        )

    def _request(self, transition=None):
        current = self.transition if transition is None else transition
        return build_repository_checkpoint_live_git_preflight_request(
            "checkpoint-live-git-preflight-v117",
            str(self.root),
            current,
            requested_at_epoch_seconds=1_800_000_000,
        )

    def _git_storage_snapshot(self):
        git_dir = self.root / ".git"
        selected_roots = ("objects", "refs", "logs")
        payload: list[tuple[str, str]] = []
        for selected in selected_roots:
            root = git_dir / selected
            if not root.exists():
                continue
            for path in sorted(item for item in root.rglob("*") if item.is_file()):
                payload.append(
                    (
                        str(path.relative_to(git_dir)),
                        hashlib.sha256(path.read_bytes()).hexdigest(),
                    )
                )
        index = git_dir / "index"
        index_digest = (
            hashlib.sha256(index.read_bytes()).hexdigest()
            if index.exists()
            else ""
        )
        return tuple(payload), index_digest

    def test_live_read_only_preflight_is_ready_without_repository_writes(self) -> None:
        before = self._git_storage_snapshot()
        receipt = execute_repository_checkpoint_live_git_preflight(
            self._request(),
            self.transition,
            self.policy,
        )
        after = self._git_storage_snapshot()
        self.assertEqual(receipt.status, PREFLIGHT_READY)
        self.assertEqual(receipt.observed_current_oid, self.first_oid)
        self.assertEqual(len(receipt.command_receipts), 7)
        self.assertTrue(receipt.live_git_command_invoked)
        self.assertTrue(receipt.all_commands_read_only)
        self.assertTrue(receipt.optional_locks_disabled)
        self.assertFalse(receipt.shell_used)
        self.assertFalse(receipt.live_repository_mutated)
        self.assertFalse(receipt.object_database_write_performed)
        self.assertFalse(receipt.index_write_performed)
        self.assertFalse(receipt.working_tree_write_performed)
        self.assertFalse(receipt.reflog_write_performed)
        self.assertEqual(before, after)

    def test_current_oid_conflict_is_rejected(self) -> None:
        transition = self._transition(
            self.transition,
            expected_oid=self.second_oid,
            proposed_oid=self.first_oid,
        )
        receipt = execute_repository_checkpoint_live_git_preflight(
            self._request(transition),
            transition,
            self.policy,
        )
        self.assertEqual(receipt.status, PREFLIGHT_REJECTED)
        self.assertFalse(receipt.observed_oid_matches_expected)
        self.assertFalse(receipt.live_repository_mutated)

    def test_missing_proposed_commit_object_is_rejected(self) -> None:
        transition = self._transition(
            self.transition,
            expected_oid=self.first_oid,
            proposed_oid="f" * 40,
        )
        receipt = execute_repository_checkpoint_live_git_preflight(
            self._request(transition),
            transition,
            self.policy,
        )
        self.assertEqual(receipt.status, PREFLIGHT_REJECTED)
        self.assertFalse(receipt.proposed_object_exists)
        self.assertFalse(receipt.live_repository_mutated)

    def test_symbolic_checkpoint_reference_is_rejected(self) -> None:
        self._git(
            "symbolic-ref",
            self.checkpoint_reference,
            "refs/heads/main",
        )
        transition = self._transition(
            self.transition,
            expected_oid=self.second_oid,
            proposed_oid=self.first_oid,
        )
        receipt = execute_repository_checkpoint_live_git_preflight(
            self._request(transition),
            transition,
            self.policy,
        )
        self.assertEqual(receipt.status, PREFLIGHT_REJECTED)
        self.assertFalse(receipt.checkpoint_reference_direct)
        self.assertFalse(receipt.live_repository_mutated)

    def test_same_repository_state_is_deterministic(self) -> None:
        request = self._request()
        first = execute_repository_checkpoint_live_git_preflight(
            request,
            self.transition,
            self.policy,
        )
        second = execute_repository_checkpoint_live_git_preflight(
            request,
            self.transition,
            self.policy,
        )
        self.assertEqual(first.to_dict(), second.to_dict())


if __name__ == "__main__":
    unittest.main()
