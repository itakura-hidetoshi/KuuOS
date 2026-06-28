from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from runtime.kuuos_repository_certificate_chain_v0_82 import (
    certificate_chain_record_issues,
)
from runtime.kuuos_repository_git_revision_adapter_v0_83 import (
    advance_repository_certificate_chain_from_git,
    capture_git_object_snapshot,
    observe_git_revision,
    start_repository_certificate_chain_from_git,
)
from tests.kuuos_repository_incremental_fixture_v0_81 import (
    normal_dual_contract_snapshot,
)

CHAIN_ID = "fixture-git-revision-chain"


def _git(root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"git {' '.join(arguments)} failed: {completed.stderr}"
        )
    return completed.stdout.strip()


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _materialize_fixture(root: Path) -> tuple[str, ...]:
    snapshot = normal_dual_contract_snapshot()
    texts = snapshot.texts
    for relative in snapshot.all_paths:
        _write(root, relative, texts.get(relative, ""))
    return snapshot.all_paths


def _commit(root: Path, message: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "-m", message)
    return _git(root, "rev-parse", "HEAD")


class RepositoryGitRevisionAdapterV083Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "fixture-repository"
        self.root.mkdir(parents=True)
        _git(self.root, "init", "-b", "main")
        _git(self.root, "config", "user.name", "KuuOS Test")
        _git(self.root, "config", "user.email", "kuuos@example.invalid")
        self.inventory = _materialize_fixture(self.root)
        self.sha0 = _commit(self.root, "initial normal form")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_genesis_uses_object_database_snapshot(self) -> None:
        snapshot, observation, record, receipt = (
            start_repository_certificate_chain_from_git(
                CHAIN_ID,
                self.root,
                self.sha0,
                self.inventory,
                max_chain_length=8,
            )
        )
        self.assertEqual(record.current_commit_sha, self.sha0)
        self.assertEqual(record.current_snapshot_digest, snapshot.digest)
        self.assertEqual(certificate_chain_record_issues(record), ())
        self.assertTrue(observation.object_database_read)
        self.assertFalse(observation.working_tree_read)
        self.assertTrue(receipt.snapshots_from_object_database)
        self.assertTrue(receipt.working_tree_ignored)
        self.assertFalse(receipt.external_approval_required)

    def test_unrelated_commit_reuses_all_scopes(self) -> None:
        _, _, genesis, _ = start_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.root,
            self.sha0,
            self.inventory,
        )
        _write(self.root, "notes/unrelated.txt", "unrelated-v2\n")
        sha1 = _commit(self.root, "change unrelated note")
        _, _, observation, record, receipt = (
            advance_repository_certificate_chain_from_git(
                CHAIN_ID,
                genesis,
                self.root,
                self.sha0,
                sha1,
                self.inventory,
            )
        )
        self.assertEqual(observation.changed_paths, ("notes/unrelated.txt",))
        self.assertEqual(record.declared_changed_paths, observation.changed_paths)
        self.assertEqual(len(record.reused_scope_ids), 3)
        self.assertEqual(record.rechecked_scope_ids, ())
        self.assertFalse(record.full_recheck_performed)
        self.assertTrue(record.current_normal_form_preserved)
        self.assertTrue(receipt.changed_paths_exact)

    def test_contract_commit_rechecks_only_affected_contract(self) -> None:
        _, _, genesis, _ = start_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.root,
            self.sha0,
            self.inventory,
        )
        _write(self.root, "runtime/alpha_v0_81.py", "ALPHA = 2\n")
        sha1 = _commit(self.root, "change alpha runtime")
        _, _, _, record, _ = advance_repository_certificate_chain_from_git(
            CHAIN_ID,
            genesis,
            self.root,
            self.sha0,
            sha1,
            self.inventory,
        )
        self.assertEqual(
            record.rechecked_scope_ids,
            ("contract:manifests/alpha_v0_81.json",),
        )
        self.assertFalse(record.full_recheck_performed)
        self.assertTrue(record.current_normal_form_preserved)

    def test_dirty_working_tree_is_ignored(self) -> None:
        _write(self.root, "notes/unrelated.txt", "committed-v2\n")
        sha1 = _commit(self.root, "commit note")
        _write(self.root, "notes/unrelated.txt", "dirty-v3\n")
        captured = capture_git_object_snapshot(
            self.root,
            sha1,
            self.inventory,
        )
        self.assertEqual(
            captured.texts["notes/unrelated.txt"],
            "committed-v2\n",
        )
        self.assertEqual(
            (self.root / "notes/unrelated.txt").read_text(encoding="utf-8"),
            "dirty-v3\n",
        )

    def test_changed_path_outside_inventory_is_rejected(self) -> None:
        _write(self.root, "outside.txt", "outside\n")
        sha1 = _commit(self.root, "outside inventory")
        with self.assertRaisesRegex(
            ValueError,
            "git_changed_path_outside_inventory:outside.txt",
        ):
            observe_git_revision(
                self.root,
                self.sha0,
                sha1,
                self.inventory,
            )

    def test_wrong_parent_revision_is_rejected(self) -> None:
        _write(self.root, "notes/unrelated.txt", "v2\n")
        sha1 = _commit(self.root, "second")
        _write(self.root, "notes/unrelated.txt", "v3\n")
        sha2 = _commit(self.root, "third")
        with self.assertRaisesRegex(
            ValueError,
            "current_commit_parent_mismatch",
        ):
            observe_git_revision(
                self.root,
                self.sha0,
                sha2,
                self.inventory,
            )
        parent_snapshot, current_snapshot, observation = observe_git_revision(
            self.root,
            sha1,
            sha2,
            self.inventory,
        )
        self.assertNotEqual(parent_snapshot.digest, current_snapshot.digest)
        self.assertEqual(observation.current_parent_shas, (sha1,))

    def test_merge_commit_is_rejected(self) -> None:
        _git(self.root, "checkout", "-b", "side", self.sha0)
        _write(self.root, "notes/side.txt", "side\n")
        side_sha = _commit(self.root, "side change")
        _git(self.root, "checkout", "main")
        _write(self.root, "notes/main.txt", "main\n")
        main_sha = _commit(self.root, "main change")
        _git(self.root, "merge", "--no-ff", "side", "-m", "merge side")
        merge_sha = _git(self.root, "rev-parse", "HEAD")
        self.assertNotEqual(side_sha, main_sha)
        merge_inventory = tuple(sorted(set(self.inventory) | {
            "notes/main.txt",
            "notes/side.txt",
        }))
        with self.assertRaisesRegex(
            ValueError,
            "current_commit_parent_mismatch",
        ):
            observe_git_revision(
                self.root,
                main_sha,
                merge_sha,
                merge_inventory,
            )

    def test_deleted_path_is_observed(self) -> None:
        _, _, genesis, _ = start_repository_certificate_chain_from_git(
            CHAIN_ID,
            self.root,
            self.sha0,
            self.inventory,
        )
        (self.root / "runtime/alpha_v0_81.py").unlink()
        sha1 = _commit(self.root, "delete alpha runtime")
        _, _, observation, record, _ = (
            advance_repository_certificate_chain_from_git(
                CHAIN_ID,
                genesis,
                self.root,
                self.sha0,
                sha1,
                self.inventory,
            )
        )
        self.assertEqual(
            observation.changed_paths,
            ("runtime/alpha_v0_81.py",),
        )
        self.assertEqual(record.current_score, 100)
        self.assertFalse(record.current_normal_form_preserved)

    def test_invalid_inventory_path_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "inventory_path_invalid"):
            capture_git_object_snapshot(
                self.root,
                self.sha0,
                ("../outside",),
            )

    def test_non_git_directory_is_rejected(self) -> None:
        plain = Path(self.temporary.name) / "plain"
        plain.mkdir()
        with self.assertRaisesRegex(ValueError, "git_command_failed"):
            capture_git_object_snapshot(
                plain,
                "HEAD",
                self.inventory,
            )


if __name__ == "__main__":
    unittest.main()
