from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_certificate_chain_v0_82 import (
    advance_repository_certificate_chain,
    certificate_chain_record_issues,
    start_repository_certificate_chain,
)
from tests.kuuos_repository_incremental_fixture_v0_81 import (
    normal_dual_contract_snapshot,
    remove_path,
    replace_text,
)

CHAIN_ID = "main-repository-certificate-chain"
SHA0 = "0" * 40
SHA1 = "1" * 40
SHA2 = "2" * 40


class RepositoryCertificateChainV082Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = normal_dual_contract_snapshot()
        self.normal_form = certify_repository_alignment_normal_form(
            self.snapshot
        )
        self.genesis = start_repository_certificate_chain(
            CHAIN_ID,
            SHA0,
            self.snapshot,
            self.normal_form,
            max_chain_length=8,
        )

    def test_genesis_is_bound_to_commit_snapshot_and_certificate(self) -> None:
        self.assertEqual(certificate_chain_record_issues(self.genesis), ())
        self.assertEqual(self.genesis.sequence, 0)
        self.assertEqual(self.genesis.root_commit_sha, SHA0)
        self.assertEqual(self.genesis.current_commit_sha, SHA0)
        self.assertEqual(self.genesis.commit_shas, (SHA0,))
        self.assertEqual(
            self.genesis.current_snapshot_digest,
            self.snapshot.digest,
        )
        self.assertTrue(self.genesis.current_normal_form_preserved)
        self.assertFalse(self.genesis.external_approval_required)

    def test_unrelated_change_reuses_all_scopes(self) -> None:
        current = replace_text(
            self.snapshot,
            "notes/unrelated.txt",
            "unrelated-v2\n",
        )
        record = advance_repository_certificate_chain(
            CHAIN_ID,
            self.genesis,
            self.snapshot,
            current,
            SHA0,
            SHA1,
            ("notes/unrelated.txt",),
        )
        self.assertEqual(certificate_chain_record_issues(record), ())
        self.assertEqual(record.sequence, 1)
        self.assertEqual(len(record.reused_scope_ids), 3)
        self.assertEqual(record.rechecked_scope_ids, ())
        self.assertFalse(record.full_recheck_performed)
        self.assertEqual(record.current_score, 0)
        self.assertTrue(record.current_normal_form_preserved)
        self.assertEqual(record.previous_record_digest, self.genesis.record_digest)

    def test_single_contract_change_is_rechecked_locally(self) -> None:
        current = replace_text(
            self.snapshot,
            "runtime/alpha_v0_81.py",
            "ALPHA = 2\n",
        )
        record = advance_repository_certificate_chain(
            CHAIN_ID,
            self.genesis,
            self.snapshot,
            current,
            SHA0,
            SHA1,
            ("runtime/alpha_v0_81.py",),
        )
        self.assertEqual(
            record.rechecked_scope_ids,
            ("contract:manifests/alpha_v0_81.json",),
        )
        self.assertIn(
            "repository-global-alignment-scope",
            record.reused_scope_ids,
        )
        self.assertIn(
            "contract:manifests/beta_v0_81.json",
            record.reused_scope_ids,
        )
        self.assertFalse(record.full_recheck_performed)
        self.assertTrue(record.current_normal_form_preserved)

    def test_shared_root_change_forces_full_recheck(self) -> None:
        current = replace_text(
            self.snapshot,
            "lakefile.toml",
            self.snapshot.texts["lakefile.toml"] + "\n# metadata\n",
        )
        record = advance_repository_certificate_chain(
            CHAIN_ID,
            self.genesis,
            self.snapshot,
            current,
            SHA0,
            SHA1,
            ("lakefile.toml",),
        )
        self.assertTrue(record.full_recheck_performed)
        self.assertEqual(len(record.rechecked_scope_ids), 3)
        self.assertEqual(len(record.rechecked_certificate_digests), 1)
        self.assertTrue(record.current_normal_form_preserved)

    def test_missing_contract_path_stops_the_chain(self) -> None:
        current = remove_path(
            self.snapshot,
            "runtime/alpha_v0_81.py",
        )
        record = advance_repository_certificate_chain(
            CHAIN_ID,
            self.genesis,
            self.snapshot,
            current,
            SHA0,
            SHA1,
            ("runtime/alpha_v0_81.py",),
        )
        self.assertEqual(record.current_score, 100)
        self.assertFalse(record.current_normal_form_preserved)
        with self.assertRaisesRegex(
            ValueError,
            "previous_normal_form_not_preserved",
        ):
            advance_repository_certificate_chain(
                CHAIN_ID,
                record,
                current,
                current,
                SHA1,
                SHA2,
                (),
            )

    def test_declared_diff_must_equal_snapshot_diff(self) -> None:
        current = replace_text(
            self.snapshot,
            "notes/unrelated.txt",
            "unrelated-v2\n",
        )
        with self.assertRaisesRegex(
            ValueError,
            "declared_changed_paths_mismatch",
        ):
            advance_repository_certificate_chain(
                CHAIN_ID,
                self.genesis,
                self.snapshot,
                current,
                SHA0,
                SHA1,
                (),
            )

    def test_changed_paths_must_be_canonical(self) -> None:
        current = replace_text(
            self.snapshot,
            "notes/unrelated.txt",
            "unrelated-v2\n",
        )
        with self.assertRaisesRegex(
            ValueError,
            "declared_changed_paths_not_canonical",
        ):
            advance_repository_certificate_chain(
                CHAIN_ID,
                self.genesis,
                self.snapshot,
                current,
                SHA0,
                SHA1,
                ("notes/unrelated.txt", "notes/unrelated.txt"),
            )

    def test_parent_commit_and_chain_id_are_exact(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "parent_commit_binding_mismatch",
        ):
            advance_repository_certificate_chain(
                CHAIN_ID,
                self.genesis,
                self.snapshot,
                self.snapshot,
                SHA2,
                SHA1,
                (),
            )
        with self.assertRaisesRegex(
            ValueError,
            "chain_id_binding_mismatch",
        ):
            advance_repository_certificate_chain(
                "other-chain",
                self.genesis,
                self.snapshot,
                self.snapshot,
                SHA0,
                SHA1,
                (),
            )

    def test_commit_replay_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "commit_replay_detected"):
            advance_repository_certificate_chain(
                CHAIN_ID,
                self.genesis,
                self.snapshot,
                self.snapshot,
                SHA0,
                SHA0,
                (),
            )

    def test_tampered_previous_record_is_rejected(self) -> None:
        tampered = replace(self.genesis, current_score=1)
        with self.assertRaisesRegex(
            ValueError,
            "previous_record_invalid:record_digest_mismatch",
        ):
            advance_repository_certificate_chain(
                CHAIN_ID,
                tampered,
                self.snapshot,
                self.snapshot,
                SHA0,
                SHA1,
                (),
            )

    def test_chain_length_is_bounded(self) -> None:
        genesis = start_repository_certificate_chain(
            CHAIN_ID,
            SHA0,
            self.snapshot,
            self.normal_form,
            max_chain_length=2,
        )
        next_snapshot = replace_text(
            self.snapshot,
            "notes/unrelated.txt",
            "unrelated-v2\n",
        )
        first = advance_repository_certificate_chain(
            CHAIN_ID,
            genesis,
            self.snapshot,
            next_snapshot,
            SHA0,
            SHA1,
            ("notes/unrelated.txt",),
        )
        with self.assertRaisesRegex(ValueError, "chain_length_exceeded"):
            advance_repository_certificate_chain(
                CHAIN_ID,
                first,
                next_snapshot,
                next_snapshot,
                SHA1,
                SHA2,
                (),
            )

    def test_invalid_commit_sha_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "commit_sha_invalid"):
            start_repository_certificate_chain(
                CHAIN_ID,
                "not-a-sha",
                self.snapshot,
                self.normal_form,
            )


if __name__ == "__main__":
    unittest.main()
