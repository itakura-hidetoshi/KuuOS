from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import tempfile
import unittest

from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    certificate_chain_record_digest,
)
from runtime.kuuos_repository_git_revision_adapter_v0_83 import (
    advance_repository_certificate_chain_from_git,
    start_repository_certificate_chain_from_git,
)
from runtime.kuuos_repository_merge_certificate_v0_84 import (
    certify_repository_merge_from_git,
    observe_repository_merge_from_git,
    repository_merge_certificate_issues,
)
from tests.kuuos_repository_incremental_fixture_v0_81 import (
    normal_dual_contract_snapshot,
)

CHAIN_ID = "fixture-merge-certificate-chain"


def _git(root: Path, *arguments: str, allow_failure: bool = False) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0 and not allow_failure:
        raise AssertionError(
            f"git {' '.join(arguments)} failed: {completed.stderr}"
        )
    return completed.stdout.strip()


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD")


class RepositoryMergeCertificateV084Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "merge-repository"
        self.root.mkdir(parents=True)
        _git(self.root, "init", "-b", "main")
        _git(self.root, "config", "user.name", "KuuOS Test")
        _git(self.root, "config", "user.email", "kuuos@example.invalid")
        snapshot = normal_dual_contract_snapshot()
        texts = snapshot.texts
        for relative in snapshot.all_paths:
            _write(self.root, relative, texts.get(relative, ""))
        for relative in (
            "notes/left.txt",
            "notes/right.txt",
            "notes/shared.txt",
        ):
            _write(self.root, relative, "")
        self.inventory = tuple(sorted(set(snapshot.all_paths) | {
            "notes/left.txt",
            "notes/right.txt",
            "notes/shared.txt",
        }))
        self.sha0 = _commit(self.root, "initial merge normal form")
        _, _, self.genesis, _ = start_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.root,
            self.sha0,
            self.inventory,
            max_chain_length=16,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _make_disjoint_merge(self):
        _git(self.root, "checkout", "-b", "left", self.sha0)
        _write(self.root, "notes/left.txt", "left-v1\n")
        left_sha = _commit(self.root, "left branch")
        _, _, _, left_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            left_sha,
            self.inventory,
        )

        _git(self.root, "checkout", "-b", "right", self.sha0)
        _write(self.root, "notes/right.txt", "right-v1\n")
        right_sha = _commit(self.root, "right branch")
        _, _, _, right_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            right_sha,
            self.inventory,
        )

        _git(self.root, "checkout", "left")
        _git(self.root, "merge", "--no-ff", "right", "-m", "merge right")
        merge_sha = _git(self.root, "rev-parse", "HEAD")
        return left_sha, right_sha, merge_sha, left_record, right_record

    def test_disjoint_merge_has_valid_certificate(self) -> None:
        left_sha, right_sha, merge_sha, left_record, right_record = (
            self._make_disjoint_merge()
        )
        merge_snapshot, observation, certificate = (
            certify_repository_merge_from_git(
                "merge-001",
                CHAIN_ID,
                left_record,
                right_record,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )
        )
        self.assertEqual(repository_merge_certificate_issues(certificate), ())
        self.assertEqual(observation.merge_parent_shas, (left_sha, right_sha))
        self.assertEqual(observation.overlapping_changed_paths, ())
        self.assertEqual(certificate.root_commit_sha, self.sha0)
        self.assertEqual(certificate.fork_commit_sha, self.sha0)
        self.assertEqual(certificate.common_prefix_length, 1)
        self.assertEqual(certificate.left_suffix_commit_shas, (left_sha,))
        self.assertEqual(certificate.right_suffix_commit_shas, (right_sha,))
        self.assertEqual(certificate.merge_score, 0)
        self.assertTrue(certificate.merge_normal_form_preserved)
        self.assertEqual(
            merge_snapshot.digest,
            observation.merge_snapshot_digest,
        )
        self.assertFalse(certificate.external_approval_required)

    def test_parent_order_is_exact(self) -> None:
        left_sha, right_sha, merge_sha, left_record, right_record = (
            self._make_disjoint_merge()
        )
        with self.assertRaisesRegex(ValueError, "merge_parent_order_mismatch"):
            certify_repository_merge_from_git(
                "merge-order",
                CHAIN_ID,
                right_record,
                left_record,
                self.root,
                right_sha,
                left_sha,
                merge_sha,
                self.inventory,
            )

    def test_record_commit_binding_is_exact(self) -> None:
        left_sha, right_sha, merge_sha, left_record, right_record = (
            self._make_disjoint_merge()
        )
        with self.assertRaisesRegex(ValueError, "left_record_commit_mismatch"):
            certify_repository_merge_from_git(
                "merge-record-binding",
                CHAIN_ID,
                right_record,
                left_record,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_changed_path_overlap_is_rejected(self) -> None:
        _git(self.root, "checkout", "-b", "left", self.sha0)
        _write(self.root, "notes/shared.txt", "left\n")
        left_sha = _commit(self.root, "left shared")
        _, _, _, left_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            left_sha,
            self.inventory,
        )

        _git(self.root, "checkout", "-b", "right", self.sha0)
        _write(self.root, "notes/shared.txt", "right\n")
        right_sha = _commit(self.root, "right shared")
        _, _, _, right_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            right_sha,
            self.inventory,
        )

        _git(self.root, "checkout", "left")
        _git(
            self.root,
            "merge",
            "--no-ff",
            "right",
            "-m",
            "conflicting merge",
            allow_failure=True,
        )
        _write(self.root, "notes/shared.txt", "resolved\n")
        merge_sha = _commit(self.root, "resolve shared")
        with self.assertRaisesRegex(ValueError, "merge_changed_path_overlap"):
            certify_repository_merge_from_git(
                "merge-overlap",
                CHAIN_ID,
                left_record,
                right_record,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_inventory_escape_in_merge_commit_is_rejected(self) -> None:
        left_sha, right_sha, _, left_record, right_record = (
            self._make_disjoint_merge()
        )
        _git(self.root, "reset", "--hard", left_sha)
        _git(self.root, "merge", "--no-ff", "--no-commit", right_sha)
        _write(self.root, "outside-merge.txt", "outside\n")
        merge_sha = _commit(self.root, "merge with outside path")
        with self.assertRaisesRegex(
            ValueError,
            "merge_changed_path_outside_inventory:outside-merge.txt",
        ):
            certify_repository_merge_from_git(
                "merge-outside",
                CHAIN_ID,
                left_record,
                right_record,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_different_chain_is_rejected(self) -> None:
        left_sha, right_sha, merge_sha, left_record, _ = (
            self._make_disjoint_merge()
        )
        _, _, other_genesis, _ = start_repository_certificate_chain_from_git(
            "other-chain",
            self.root,
            self.sha0,
            self.inventory,
        )
        _, _, _, other_right, _ = advance_repository_certificate_chain_from_git(
            "other-chain",
            other_genesis,
            self.root,
            self.sha0,
            right_sha,
            self.inventory,
        )
        with self.assertRaisesRegex(ValueError, "merge_chain_id_mismatch"):
            certify_repository_merge_from_git(
                "merge-other-chain",
                CHAIN_ID,
                left_record,
                other_right,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_non_preserved_branch_is_rejected(self) -> None:
        _git(self.root, "checkout", "-b", "broken", self.sha0)
        (self.root / "runtime/alpha_v0_81.py").unlink()
        broken_sha = _commit(self.root, "break alpha")
        _, _, _, broken_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            broken_sha,
            self.inventory,
        )
        self.assertFalse(broken_record.current_normal_form_preserved)

        _git(self.root, "checkout", "-b", "right", self.sha0)
        _write(self.root, "notes/right.txt", "right\n")
        right_sha = _commit(self.root, "right normal")
        _, _, _, right_record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.genesis,
            self.root,
            self.sha0,
            right_sha,
            self.inventory,
        )
        _git(self.root, "checkout", "broken")
        _git(self.root, "merge", "--no-ff", "right", "-m", "merge right")
        merge_sha = _git(self.root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "left_normal_form_not_preserved"):
            certify_repository_merge_from_git(
                "merge-broken",
                CHAIN_ID,
                broken_record,
                right_record,
                self.root,
                broken_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_tampered_record_is_rejected(self) -> None:
        left_sha, right_sha, merge_sha, left_record, right_record = (
            self._make_disjoint_merge()
        )
        tampered = replace(left_record, current_score=1)
        with self.assertRaisesRegex(
            ValueError,
            "left_record_invalid:record_digest_mismatch",
        ):
            certify_repository_merge_from_git(
                "merge-tampered",
                CHAIN_ID,
                tampered,
                right_record,
                self.root,
                left_sha,
                right_sha,
                merge_sha,
                self.inventory,
            )

    def test_certificate_tamper_is_detected(self) -> None:
        left_sha, right_sha, merge_sha, left_record, right_record = (
            self._make_disjoint_merge()
        )
        _, _, certificate = certify_repository_merge_from_git(
            "merge-tamper-certificate",
            CHAIN_ID,
            left_record,
            right_record,
            self.root,
            left_sha,
            right_sha,
            merge_sha,
            self.inventory,
        )
        tampered = replace(certificate, merge_score=1)
        self.assertIn(
            "certificate_digest_mismatch",
            repository_merge_certificate_issues(tampered),
        )


if __name__ == "__main__":
    unittest.main()
