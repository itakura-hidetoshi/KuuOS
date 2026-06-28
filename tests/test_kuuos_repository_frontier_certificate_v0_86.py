from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_frontier_certificate_v0_86 import (
    certify_repository_frontier,
    repository_frontier_certificate_issues,
)
from runtime.kuuos_repository_revision_dag_types_v0_85 import (
    repository_revision_dag_certificate_digest,
)
from runtime.kuuos_repository_revision_dag_v0_85 import (
    certify_repository_revision_dag,
)
from tests.test_kuuos_repository_revision_dag_v0_85 import (
    LEFT_SHA,
    MERGE_SHA,
    RIGHT_SHA,
    ROOT_SHA,
    TAIL_SHA,
    child_record,
    genesis_record,
    merge_certificate,
)


def _seal_dag(certificate):
    return replace(
        certificate,
        certificate_digest=repository_revision_dag_certificate_digest(certificate),
    )


class RepositoryFrontierCertificateV086Tests(unittest.TestCase):
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

    def merged_dag(self):
        return certify_repository_revision_dag(
            "dag-frontier-merged",
            (self.right, self.genesis, self.left),
            (self.merge,),
        )

    def unmerged_dag(self):
        return certify_repository_revision_dag(
            "dag-frontier-open",
            (self.right, self.genesis, self.left),
        )

    def test_merged_branches_reduce_to_one_frontier_tip(self) -> None:
        edges, dag = self.merged_dag()
        paths, certificate = certify_repository_frontier(
            "frontier-merged",
            edges,
            dag,
        )
        self.assertEqual(repository_frontier_certificate_issues(certificate), ())
        self.assertEqual(certificate.frontier_commit_shas, (MERGE_SHA,))
        self.assertEqual(certificate.frontier_count, 1)
        self.assertEqual(len(paths), dag.node_count)
        self.assertTrue(certificate.exact_terminal_frontier)
        self.assertTrue(certificate.frontier_antichain)
        self.assertTrue(certificate.all_nodes_frontier_covered)
        self.assertTrue(certificate.merged_ancestors_excluded)
        self.assertFalse(certificate.external_approval_required)

    def test_unmerged_branches_remain_as_two_frontier_tips(self) -> None:
        edges, dag = self.unmerged_dag()
        paths, certificate = certify_repository_frontier(
            "frontier-open",
            edges,
            dag,
        )
        self.assertEqual(certificate.frontier_commit_shas, (LEFT_SHA, RIGHT_SHA))
        root_path = next(path for path in paths if path.source_commit_sha == ROOT_SHA)
        self.assertEqual(root_path.commit_shas, (ROOT_SHA, LEFT_SHA))
        self.assertEqual(root_path.frontier_commit_sha, LEFT_SHA)

    def test_linear_history_has_one_terminal_frontier(self) -> None:
        tail = child_record(
            self.left,
            TAIL_SHA,
            "snapshot-tail",
            "notes/tail.txt",
        )
        edges, dag = certify_repository_revision_dag(
            "dag-frontier-linear",
            (tail, self.genesis, self.left),
        )
        paths, certificate = certify_repository_frontier(
            "frontier-linear",
            edges,
            dag,
        )
        self.assertEqual(certificate.frontier_commit_shas, (TAIL_SHA,))
        root_path = next(path for path in paths if path.source_commit_sha == ROOT_SHA)
        self.assertEqual(root_path.commit_shas, (ROOT_SHA, LEFT_SHA, TAIL_SHA))

    def test_source_edges_are_digest_bound(self) -> None:
        edges, dag = self.merged_dag()
        with self.assertRaisesRegex(ValueError, "frontier_edge_binding_mismatch"):
            certify_repository_frontier(
                "frontier-missing-edge",
                edges[:-1],
                dag,
            )

    def test_edge_replay_is_rejected(self) -> None:
        edges, dag = self.merged_dag()
        with self.assertRaisesRegex(ValueError, "frontier_edge_replay_detected"):
            certify_repository_frontier(
                "frontier-edge-replay",
                edges + (edges[0],),
                dag,
            )

    def test_source_dag_tamper_is_rejected(self) -> None:
        edges, dag = self.merged_dag()
        tampered = replace(dag, node_count=dag.node_count + 1)
        with self.assertRaisesRegex(ValueError, "revision_dag_certificate_invalid"):
            certify_repository_frontier(
                "frontier-source-tamper",
                edges,
                tampered,
            )

    def test_source_tip_binding_is_recomputed(self) -> None:
        edges, dag = self.merged_dag()
        tampered = _seal_dag(replace(
            dag,
            tip_commit_shas=(LEFT_SHA,),
            certificate_digest="",
        ))
        with self.assertRaisesRegex(ValueError, "frontier_tip_binding_mismatch"):
            certify_repository_frontier(
                "frontier-tip-tamper",
                edges,
                tampered,
            )

    def test_frontier_bound_fails_closed(self) -> None:
        edges, dag = self.unmerged_dag()
        with self.assertRaisesRegex(ValueError, "repository_frontier_bound_exceeded"):
            certify_repository_frontier(
                "frontier-bound",
                edges,
                dag,
                max_frontier_size=1,
            )

    def test_coverage_paths_are_unique_per_source(self) -> None:
        edges, dag = self.merged_dag()
        paths, certificate = certify_repository_frontier(
            "frontier-paths",
            edges,
            dag,
        )
        self.assertEqual(
            tuple(path.source_commit_sha for path in paths),
            dag.node_commit_shas,
        )
        self.assertEqual(len(set(certificate.coverage_path_digests)), dag.node_count)

    def test_certificate_tamper_is_detected(self) -> None:
        edges, dag = self.merged_dag()
        _, certificate = certify_repository_frontier(
            "frontier-tamper",
            edges,
            dag,
        )
        tampered = replace(certificate, frontier_count=2)
        issues = repository_frontier_certificate_issues(tampered)
        self.assertIn("certificate_digest_mismatch", issues)
        self.assertIn("frontier_count_mismatch", issues)

    def test_coverage_path_replay_is_detected(self) -> None:
        edges, dag = self.merged_dag()
        _, certificate = certify_repository_frontier(
            "frontier-path-replay",
            edges,
            dag,
        )
        repeated = (certificate.coverage_path_digests[0],) * dag.node_count
        tampered = replace(certificate, coverage_path_digests=repeated)
        issues = repository_frontier_certificate_issues(tampered)
        self.assertIn("certificate_digest_mismatch", issues)
        self.assertIn("coverage_path_replay_detected", issues)


if __name__ == "__main__":
    unittest.main()
