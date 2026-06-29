from __future__ import annotations

from dataclasses import replace
import hashlib
import unittest

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    repository_atomic_application_receipt_digest,
)
from runtime.kuuos_repository_commit_candidate_strict_v0_93 import (
    certify_repository_commit_candidate,
    repository_commit_candidate_certificate_issues,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    CANDIDATE_CERTIFIED,
    EXECUTABLE_FILE_MODE,
    REGULAR_FILE_MODE,
    RepositoryCommitIdentity,
    RepositoryParentTreeEntry,
    repository_commit_candidate_certificate_digest,
    repository_parent_tree_inventory_digest,
)
from runtime.kuuos_repository_commit_candidate_v0_93 import (
    build_repository_commit_candidate_policy,
    build_repository_parent_tree_inventory,
    git_object_oid,
    normalize_commit_message,
    repository_snapshot_commit_candidate_issues,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot
from tests.test_kuuos_repository_atomic_application_v0_92 import (
    RepositoryAtomicApplicationV092Tests,
)


class RepositoryCommitCandidateV093Tests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = RepositoryAtomicApplicationV092Tests(
            methodName="test_success_commits_snapshot_and_nonce_together"
        )
        fixture.setUp()
        self.snapshot, _, self.application_receipt, _, _ = fixture._apply()
        self.parent_inventory = self._parent_inventory()
        self.policy = build_repository_commit_candidate_policy(
            "commit-candidate-policy-v093",
            max_file_count=64,
            max_total_utf8_bytes=1_000_000,
        )
        self.author = RepositoryCommitIdentity(
            name="KuuOS Repository Agent",
            email="repository-agent@example.invalid",
            timestamp=1_788_000_000,
            timezone="+0900",
        )
        self.committer = RepositoryCommitIdentity(
            name="KuuOS Commit Candidate Certifier",
            email="commit-certifier@example.invalid",
            timestamp=1_788_000_030,
            timezone="+0900",
        )

    def _parent_inventory(self, *, entries=None, **overrides):
        inventory_entries = entries or tuple(
            RepositoryParentTreeEntry(
                path=path,
                mode=REGULAR_FILE_MODE,
                git_object_oid=hashlib.sha1(
                    f"parent-entry:{path}".encode("utf-8")
                ).hexdigest(),
            )
            for path in self.snapshot.all_paths
        )
        values = {
            "parent_commit_sha": self.application_receipt.source_commit_sha,
            "entries": inventory_entries,
            "object_database_read": True,
            "working_tree_read": False,
        }
        values.update(overrides)
        return build_repository_parent_tree_inventory(
            values["parent_commit_sha"],
            values["entries"],
            object_database_read=values["object_database_read"],
            working_tree_read=values["working_tree_read"],
        )

    def _certify(self, **overrides):
        values = {
            "candidate_id": "commit-candidate-v093-001",
            "application_receipt": self.application_receipt,
            "snapshot": self.snapshot,
            "parent_tree_inventory": self.parent_inventory,
            "policy": self.policy,
            "author": self.author,
            "committer": self.committer,
            "message": "Certify repository commit candidate v0.93",
        }
        values.update(overrides)
        return certify_repository_commit_candidate(
            values["candidate_id"],
            values["application_receipt"],
            values["snapshot"],
            values["parent_tree_inventory"],
            values["policy"],
            author=values["author"],
            committer=values["committer"],
            message=values["message"],
        )

    def _issues(self, certificate, **overrides):
        values = {
            "application_receipt": self.application_receipt,
            "snapshot": self.snapshot,
            "parent_tree_inventory": self.parent_inventory,
            "policy": self.policy,
        }
        values.update(overrides)
        return repository_commit_candidate_certificate_issues(
            certificate,
            values["application_receipt"],
            values["snapshot"],
            values["parent_tree_inventory"],
            values["policy"],
        )

    def test_known_empty_git_object_ids(self) -> None:
        self.assertEqual(
            git_object_oid("blob", b""),
            "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
        )
        self.assertEqual(
            git_object_oid("tree", b""),
            "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
        )

    def test_candidate_is_deterministic_and_exactly_bound(self) -> None:
        first = self._certify()
        second = self._certify()
        self.assertEqual(first, second)
        self.assertEqual(first.status, CANDIDATE_CERTIFIED)
        self.assertEqual(
            first.application_receipt_digest,
            self.application_receipt.receipt_digest,
        )
        self.assertEqual(
            first.parent_tree_inventory_digest,
            self.parent_inventory.inventory_digest,
        )
        self.assertEqual(first.parent_commit_sha, self.application_receipt.source_commit_sha)
        self.assertEqual(first.final_snapshot_digest, self.snapshot.digest)
        self.assertEqual(first.file_count, len(self.snapshot.all_paths))
        self.assertEqual(first.text_blob_candidate_count, len(self.snapshot.text_files))
        self.assertEqual(
            first.retained_parent_entry_count,
            len(self.snapshot.all_paths) - len(self.snapshot.text_files),
        )
        self.assertEqual(first.message, "Certify repository commit candidate v0.93\n")
        self.assertEqual(self._issues(first), ())

    def test_tree_contains_nested_directories_and_sorted_entries(self) -> None:
        certificate = self._certify()
        directories = tuple(tree.directory for tree in certificate.tree_candidates)
        self.assertIn("", directories)
        self.assertIn("scripts", directories)
        self.assertIn("formal", directories)
        for tree in certificate.tree_candidates:
            combined = tuple(zip(tree.entry_names, tree.entry_modes, tree.entry_oids))
            self.assertEqual(len(combined), len(set(tree.entry_names)))
            self.assertTrue(all(len(oid) == 40 for _, _, oid in combined))

    def test_text_paths_receive_new_blobs_and_non_text_paths_retain_parent_oids(self) -> None:
        certificate = self._certify()
        parent_by_path = {entry.path: entry for entry in self.parent_inventory.entries}
        blobs_by_path = {blob.path: blob for blob in certificate.blob_candidates}
        for path, text in self.snapshot.text_files:
            self.assertEqual(
                blobs_by_path[path].git_blob_oid,
                git_object_oid("blob", text.encode("utf-8")),
            )
        non_text_paths = tuple(
            path for path in self.snapshot.all_paths if path not in self.snapshot.texts
        )
        self.assertTrue(non_text_paths)
        candidate_oids = {
            oid
            for tree in certificate.tree_candidates
            for oid in tree.entry_oids
        }
        for path in non_text_paths:
            self.assertIn(parent_by_path[path].git_object_oid, candidate_oids)

    def test_parent_file_mode_is_preserved_for_text_overlay(self) -> None:
        text_path = self.snapshot.text_files[0][0]
        entries = tuple(
            replace(entry, mode=EXECUTABLE_FILE_MODE)
            if entry.path == text_path
            else entry
            for entry in self.parent_inventory.entries
        )
        inventory = self._parent_inventory(entries=entries)
        certificate = self._certify(parent_tree_inventory=inventory)
        blob = next(item for item in certificate.blob_candidates if item.path == text_path)
        self.assertEqual(blob.mode, EXECUTABLE_FILE_MODE)
        self.assertTrue(certificate.parent_modes_preserved)

    def test_candidate_grants_no_git_write_or_reference_authority(self) -> None:
        certificate = self._certify()
        self.assertFalse(certificate.object_database_write_performed)
        self.assertFalse(certificate.index_write_performed)
        self.assertFalse(certificate.working_tree_write_performed)
        self.assertFalse(certificate.commit_created)
        self.assertFalse(certificate.reference_mutated)
        self.assertFalse(certificate.signing_performed)

    def test_message_normalization_is_deterministic(self) -> None:
        self.assertEqual(normalize_commit_message("subject"), "subject\n")
        self.assertEqual(normalize_commit_message("subject\n\n"), "subject\n")
        certificate = self._certify(message="subject\n\n")
        self.assertEqual(certificate.message, "subject\n")

    def test_carriage_return_and_empty_messages_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "commit_message_control_character_invalid"):
            self._certify(message="subject\r\n")
        with self.assertRaisesRegex(ValueError, "commit_message_empty"):
            self._certify(message="\n\n")

    def test_snapshot_digest_mismatch_fails_closed(self) -> None:
        drifted = RepositorySnapshot(
            root_label=self.snapshot.root_label + "-drift",
            all_paths=self.snapshot.all_paths,
            text_files=self.snapshot.text_files,
        )
        with self.assertRaisesRegex(ValueError, "commit_candidate_snapshot_binding_mismatch"):
            self._certify(snapshot=drifted)

    def test_application_receipt_tamper_fails_closed(self) -> None:
        tampered = replace(
            self.application_receipt,
            candidate_snapshot_digest="0" * 64,
        )
        with self.assertRaisesRegex(ValueError, "atomic_application_receipt_invalid"):
            self._certify(application_receipt=tampered)

    def test_invalid_parent_sha_fails_closed(self) -> None:
        invalid = replace(
            self.application_receipt,
            source_commit_sha="not-a-commit",
            receipt_digest="",
        )
        invalid = replace(
            invalid,
            receipt_digest=repository_atomic_application_receipt_digest(invalid),
        )
        with self.assertRaisesRegex(ValueError, "commit_candidate_parent_sha_invalid"):
            self._certify(application_receipt=invalid)

    def test_invalid_identity_fails_closed(self) -> None:
        invalid_author = replace(self.author, name="bad\nname")
        with self.assertRaisesRegex(ValueError, "commit_candidate_identity_invalid"):
            self._certify(author=invalid_author)
        invalid_committer = replace(self.committer, timezone="+1460")
        with self.assertRaisesRegex(ValueError, "commit_candidate_identity_invalid"):
            self._certify(committer=invalid_committer)

    def test_text_path_outside_snapshot_inventory_fails_closed(self) -> None:
        invalid = RepositorySnapshot(
            root_label="invalid-v093",
            all_paths=("a.txt",),
            text_files=(("a.txt", "a"), ("outside.txt", "outside")),
        )
        self.assertIn(
            "commit_snapshot_text_path_outside_inventory",
            repository_snapshot_commit_candidate_issues(invalid),
        )

    def test_path_topology_conflict_fails_closed(self) -> None:
        conflicted = RepositorySnapshot(
            root_label="topology-v093",
            all_paths=("a", "a/b.txt"),
            text_files=(("a", "file"), ("a/b.txt", "nested")),
        )
        self.assertIn(
            "repository_path_topology_invalid",
            repository_snapshot_commit_candidate_issues(conflicted),
        )

    def test_parent_inventory_commit_mismatch_fails_closed(self) -> None:
        inventory = self._parent_inventory(parent_commit_sha="e" * 40)
        with self.assertRaisesRegex(
            ValueError,
            "commit_candidate_parent_inventory_commit_mismatch",
        ):
            self._certify(parent_tree_inventory=inventory)

    def test_parent_inventory_missing_path_fails_closed(self) -> None:
        inventory = self._parent_inventory(entries=self.parent_inventory.entries[:-1])
        with self.assertRaisesRegex(
            ValueError,
            "commit_candidate_parent_path_coverage_mismatch",
        ):
            self._certify(parent_tree_inventory=inventory)

    def test_parent_inventory_working_tree_source_fails_closed(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "parent_tree_inventory_working_tree_read",
        ):
            self._parent_inventory(working_tree_read=True)

    def test_parent_inventory_digest_tamper_fails_closed(self) -> None:
        tampered = replace(self.parent_inventory, inventory_digest="0" * 64)
        with self.assertRaisesRegex(ValueError, "parent_tree_inventory_invalid"):
            self._certify(parent_tree_inventory=tampered)
        self.assertNotEqual(
            tampered.inventory_digest,
            repository_parent_tree_inventory_digest(tampered),
        )

    def test_file_count_policy_is_enforced_before_certification(self) -> None:
        restrictive = build_repository_commit_candidate_policy(
            "file-count-v093",
            max_file_count=1,
            max_total_utf8_bytes=1_000_000,
        )
        with self.assertRaisesRegex(ValueError, "commit_candidate_file_count_exceeds_policy"):
            self._certify(policy=restrictive)

    def test_byte_count_policy_is_enforced_before_certification(self) -> None:
        restrictive = build_repository_commit_candidate_policy(
            "byte-count-v093",
            max_file_count=64,
            max_total_utf8_bytes=1,
        )
        with self.assertRaisesRegex(ValueError, "commit_candidate_byte_count_exceeds_policy"):
            self._certify(policy=restrictive)

    def test_tree_oid_tamper_is_detected_by_full_recomputation(self) -> None:
        certificate = self._certify()
        tampered_trees = list(certificate.tree_candidates)
        tampered_trees[0] = replace(tampered_trees[0], git_tree_oid="0" * 40)
        tampered = replace(
            certificate,
            tree_candidates=tuple(tampered_trees),
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=repository_commit_candidate_certificate_digest(tampered),
        )
        self.assertIn("commit_candidate_recomputation_mismatch", self._issues(tampered))

    def test_candidate_oid_tamper_is_detected_even_with_new_certificate_digest(self) -> None:
        certificate = self._certify()
        tampered = replace(
            certificate,
            candidate_commit_oid="f" * 40,
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=repository_commit_candidate_certificate_digest(tampered),
        )
        self.assertIn("commit_candidate_recomputation_mismatch", self._issues(tampered))

    def test_write_authority_tamper_is_detected(self) -> None:
        certificate = self._certify()
        tampered = replace(
            certificate,
            commit_created=True,
            reference_mutated=True,
            certificate_digest="",
        )
        tampered = replace(
            tampered,
            certificate_digest=repository_commit_candidate_certificate_digest(tampered),
        )
        issues = self._issues(tampered)
        self.assertIn("commit_candidate_commit_created", issues)
        self.assertIn("commit_candidate_reference_mutated", issues)


if __name__ == "__main__":
    unittest.main()
