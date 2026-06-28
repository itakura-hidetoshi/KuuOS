from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    RepositoryCertificateChainRecord,
    certificate_chain_record_digest,
)
from runtime.kuuos_repository_merge_certificate_types_v0_84 import (
    RepositoryMergeCertificate,
    repository_merge_certificate_digest,
)
from runtime.kuuos_repository_revision_dag_v0_85 import (
    certify_repository_revision_dag,
    repository_revision_dag_certificate_issues,
)

CHAIN_ID = "fixture-revision-dag"
ROOT_SHA = "0" * 40
LEFT_SHA = "1" * 40
RIGHT_SHA = "2" * 40
MERGE_SHA = "3" * 40
TAIL_SHA = "4" * 40


def _seal_record(record: RepositoryCertificateChainRecord):
    return replace(record, record_digest=certificate_chain_record_digest(record))


def _seal_merge(certificate: RepositoryMergeCertificate):
    return replace(
        certificate,
        certificate_digest=repository_merge_certificate_digest(certificate),
    )


def genesis_record() -> RepositoryCertificateChainRecord:
    return _seal_record(RepositoryCertificateChainRecord(
        CHAIN_ID,
        0,
        ROOT_SHA,
        "",
        ROOT_SHA,
        "",
        "snapshot-root",
        "snapshot-root",
        (),
        (),
        "",
        (),
        (),
        ("normal-form-root",),
        True,
        0,
        True,
        (ROOT_SHA,),
        16,
        False,
        "",
    ))


def child_record(
    previous: RepositoryCertificateChainRecord,
    current_sha: str,
    snapshot_digest: str,
    changed_path: str,
) -> RepositoryCertificateChainRecord:
    return _seal_record(RepositoryCertificateChainRecord(
        previous.chain_id,
        previous.sequence + 1,
        previous.root_commit_sha,
        previous.current_commit_sha,
        current_sha,
        previous.record_digest,
        previous.current_snapshot_digest,
        snapshot_digest,
        (changed_path,),
        (changed_path,),
        f"delta-{current_sha[:8]}",
        (),
        (f"contract:{changed_path}",),
        (f"normal-form-{current_sha[:8]}",),
        False,
        0,
        True,
        previous.commit_shas + (current_sha,),
        previous.max_chain_length,
        False,
        "",
    ))


def merge_certificate(
    left: RepositoryCertificateChainRecord,
    right: RepositoryCertificateChainRecord,
) -> RepositoryMergeCertificate:
    return _seal_merge(RepositoryMergeCertificate(
        "merge-001",
        CHAIN_ID,
        ROOT_SHA,
        ROOT_SHA,
        left.record_digest,
        right.record_digest,
        left.current_commit_sha,
        right.current_commit_sha,
        MERGE_SHA,
        "merge-observation",
        "merge-normal-form",
        0,
        1,
        (left.current_commit_sha,),
        (right.current_commit_sha,),
        True,
        True,
        True,
        True,
        False,
        "",
    ))


class RepositoryRevisionDagV085Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.genesis = genesis_record()
        self.left = child_record(
            self.genesis,
            LEFT_SHA,
            "snapshot-left",
            "notes/left.txt",
        )
        self.right = child_record(
            self.genesis,
            RIGHT_SHA,
            "snapshot-right",
            "notes/right.txt",
        )
        self.merge = merge_certificate(self.left, self.right)

    def test_branch_and_merge_form_one_finite_dag(self) -> None:
        edges, certificate = certify_repository_revision_dag(
            "dag-001",
            (self.right, self.genesis, self.left),
            (self.merge,),
        )
        self.assertEqual(repository_revision_dag_certificate_issues(certificate), ())
        self.assertEqual(certificate.node_count, 4)
        self.assertEqual(certificate.edge_count, 4)
        self.assertEqual(certificate.root_commit_sha, ROOT_SHA)
        self.assertEqual(certificate.tip_commit_shas, (MERGE_SHA,))
        self.assertEqual(
            certificate.topological_commit_shas,
            (ROOT_SHA, LEFT_SHA, RIGHT_SHA, MERGE_SHA),
        )
        self.assertEqual(
            tuple((edge.parent_commit_sha, edge.child_commit_sha) for edge in edges),
            (
                (ROOT_SHA, LEFT_SHA),
                (ROOT_SHA, RIGHT_SHA),
                (LEFT_SHA, MERGE_SHA),
                (RIGHT_SHA, MERGE_SHA),
            ),
        )
        self.assertTrue(certificate.source_reference_closure)
        self.assertTrue(certificate.single_root)
        self.assertTrue(certificate.parent_arity_valid)
        self.assertTrue(certificate.all_nodes_reachable)
        self.assertTrue(certificate.acyclic)
        self.assertTrue(certificate.normal_form_preserved)
        self.assertFalse(certificate.external_approval_required)

    def test_linear_history_is_a_valid_dag(self) -> None:
        tail = child_record(
            self.left,
            TAIL_SHA,
            "snapshot-tail",
            "notes/tail.txt",
        )
        _, certificate = certify_repository_revision_dag(
            "dag-linear",
            (tail, self.genesis, self.left),
        )
        self.assertEqual(certificate.node_count, 3)
        self.assertEqual(certificate.edge_count, 2)
        self.assertEqual(certificate.tip_commit_shas, (TAIL_SHA,))
        self.assertEqual(
            certificate.topological_commit_shas,
            (ROOT_SHA, LEFT_SHA, TAIL_SHA),
        )

    def test_previous_record_must_be_present(self) -> None:
        tail = child_record(
            self.left,
            TAIL_SHA,
            "snapshot-tail",
            "notes/tail.txt",
        )
        with self.assertRaisesRegex(ValueError, "previous_record_not_in_dag"):
            certify_repository_revision_dag(
                "dag-missing-parent",
                (self.genesis, tail),
            )

    def test_previous_snapshot_binding_is_exact(self) -> None:
        broken = _seal_record(replace(
            self.left,
            previous_snapshot_digest="wrong-snapshot",
            record_digest="",
        ))
        with self.assertRaisesRegex(ValueError, "record_previous_snapshot_mismatch"):
            certify_repository_revision_dag(
                "dag-snapshot-binding",
                (self.genesis, broken),
            )

    def test_merge_parent_record_must_be_present(self) -> None:
        with self.assertRaisesRegex(ValueError, "merge_right_record_not_in_dag"):
            certify_repository_revision_dag(
                "dag-missing-merge-parent",
                (self.genesis, self.left),
                (self.merge,),
            )

    def test_merge_suffix_is_recomputed(self) -> None:
        broken = _seal_merge(replace(
            self.merge,
            right_suffix_commit_shas=(LEFT_SHA,),
            certificate_digest="",
        ))
        with self.assertRaisesRegex(ValueError, "merge_right_suffix_mismatch"):
            certify_repository_revision_dag(
                "dag-merge-suffix",
                (self.genesis, self.left, self.right),
                (broken,),
            )

    def test_multiple_genesis_records_are_rejected(self) -> None:
        other_root = _seal_record(replace(
            self.genesis,
            current_commit_sha="a" * 40,
            root_commit_sha="a" * 40,
            previous_snapshot_digest="snapshot-other",
            current_snapshot_digest="snapshot-other",
            commit_shas=("a" * 40,),
            record_digest="",
        ))
        with self.assertRaisesRegex(ValueError, "revision_dag_root_mismatch"):
            certify_repository_revision_dag(
                "dag-multiple-root",
                (self.genesis, other_root),
            )

    def test_non_preserved_record_is_rejected(self) -> None:
        broken = _seal_record(replace(
            self.left,
            current_normal_form_preserved=False,
            record_digest="",
        ))
        with self.assertRaisesRegex(
            ValueError,
            "chain_record_normal_form_not_preserved",
        ):
            certify_repository_revision_dag(
                "dag-broken-normal-form",
                (self.genesis, broken),
            )

    def test_node_bound_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "revision_dag_node_bound_exceeded"):
            certify_repository_revision_dag(
                "dag-node-bound",
                (self.genesis, self.left, self.right),
                max_nodes=2,
            )

    def test_edge_bound_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "revision_dag_edge_bound_exceeded"):
            certify_repository_revision_dag(
                "dag-edge-bound",
                (self.genesis, self.left, self.right),
                (self.merge,),
                max_edges=3,
            )

    def test_certificate_tamper_is_detected(self) -> None:
        _, certificate = certify_repository_revision_dag(
            "dag-tamper",
            (self.genesis, self.left, self.right),
            (self.merge,),
        )
        tampered = replace(certificate, edge_count=3)
        self.assertIn(
            "certificate_digest_mismatch",
            repository_revision_dag_certificate_issues(tampered),
        )
        self.assertIn(
            "edge_count_mismatch",
            repository_revision_dag_certificate_issues(tampered),
        )


if __name__ == "__main__":
    unittest.main()
