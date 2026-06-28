from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_repository_frontier_certificate_v0_86 import (
    certify_repository_frontier,
)
from runtime.kuuos_repository_revision_dag_v0_85 import (
    certify_repository_revision_dag,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositoryEvolutionCandidate,
    RepositoryEvolutionPolicy,
)
from runtime.kuuos_repository_self_evolution_v0_87 import (
    certify_repository_self_evolution_portfolio,
    repository_self_evolution_portfolio_certificate_issues,
)
from tests.test_kuuos_repository_revision_dag_v0_85 import (
    LEFT_SHA,
    RIGHT_SHA,
    child_record,
    genesis_record,
)


def open_frontier():
    genesis = genesis_record()
    left = child_record(genesis, LEFT_SHA, "snapshot-left", "notes/left.txt")
    right = child_record(genesis, RIGHT_SHA, "snapshot-right", "notes/right.txt")
    edges, dag = certify_repository_revision_dag(
        "dag-self-evolution-open",
        (right, genesis, left),
    )
    _, frontier = certify_repository_frontier(
        "frontier-self-evolution-open",
        edges,
        dag,
    )
    return frontier


def candidate(
    candidate_id: str,
    tip: str,
    changed_paths: tuple[str, ...],
    improvement: int,
    risk: int = 1,
    reversible: bool = True,
    protected_paths_preserved: bool = True,
    normal_form_preserved: bool = True,
    external_approval_required: bool = False,
) -> RepositoryEvolutionCandidate:
    baseline = 100
    return RepositoryEvolutionCandidate(
        candidate_id,
        tip,
        f"proposal-{candidate_id}",
        tuple(sorted(changed_paths)),
        baseline,
        baseline - improvement,
        risk,
        reversible,
        protected_paths_preserved,
        normal_form_preserved,
        external_approval_required,
    )


class RepositorySelfEvolutionV087Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.frontier = open_frontier()
        self.policy = RepositoryEvolutionPolicy(
            max_candidates=8,
            max_selected_candidates=4,
            max_changed_paths_per_candidate=4,
            max_portfolios=256,
            minimum_score_improvement=1,
            maximum_risk_score=10,
            require_reversible=True,
            protected_path_prefixes=("formal/protected",),
        )

    def test_selects_maximum_coherent_improvement_across_frontier(self) -> None:
        left = candidate("left-runtime", LEFT_SHA, ("runtime/evolve.py",), 10, 2)
        right = candidate("right-doc", RIGHT_SHA, ("docs/evolve.md",), 8, 1)
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-coherent",
            self.frontier,
            (right, left),
            self.policy,
        )
        self.assertEqual({item.candidate_id for item in selected}, {
            "left-runtime", "right-doc",
        })
        self.assertEqual(certificate.aggregate_score_improvement, 18)
        self.assertEqual(certificate.aggregate_risk_score, 3)
        self.assertEqual(certificate.selected_candidate_count, 2)
        self.assertEqual(certificate.enumerated_portfolio_count, 4)
        self.assertTrue(certificate.strict_score_descent)
        self.assertTrue(certificate.selected_paths_nonconflicting)
        self.assertTrue(certificate.one_candidate_per_frontier)
        self.assertTrue(certificate.deterministic_optimum)
        self.assertFalse(certificate.stable_no_change)
        self.assertFalse(certificate.execution_authority_granted)
        self.assertEqual(
            repository_self_evolution_portfolio_certificate_issues(certificate),
            (),
        )

    def test_hierarchical_path_conflict_prevents_joint_selection(self) -> None:
        left = candidate("left-runtime", LEFT_SHA, ("runtime",), 10)
        right = candidate("right-runtime-child", RIGHT_SHA, ("runtime/core.py",), 9)
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-conflict",
            self.frontier,
            (left, right),
            self.policy,
        )
        self.assertEqual(tuple(item.candidate_id for item in selected), ("left-runtime",))
        self.assertEqual(certificate.aggregate_score_improvement, 10)

    def test_at_most_one_candidate_is_selected_per_frontier_tip(self) -> None:
        weaker = candidate("left-weaker", LEFT_SHA, ("runtime/weak.py",), 5)
        stronger = candidate("left-stronger", LEFT_SHA, ("runtime/strong.py",), 7)
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-one-per-tip",
            self.frontier,
            (weaker, stronger),
            self.policy,
        )
        self.assertEqual(tuple(item.candidate_id for item in selected), ("left-stronger",))
        self.assertTrue(certificate.one_candidate_per_frontier)

    def test_risk_limit_filters_candidate(self) -> None:
        risky = candidate("risky", LEFT_SHA, ("runtime/risky.py",), 20, risk=11)
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-risk",
            self.frontier,
            (risky,),
            self.policy,
        )
        self.assertEqual(selected, ())
        self.assertEqual(certificate.admissible_candidate_count, 0)
        self.assertTrue(certificate.stable_no_change)

    def test_protected_path_filters_candidate(self) -> None:
        protected = candidate(
            "protected",
            LEFT_SHA,
            ("formal/protected/kernel.lean",),
            20,
        )
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-protected",
            self.frontier,
            (protected,),
            self.policy,
        )
        self.assertEqual(selected, ())
        self.assertTrue(certificate.protected_paths_preserved)

    def test_nonreversible_and_external_candidates_are_filtered(self) -> None:
        nonreversible = candidate(
            "nonreversible",
            LEFT_SHA,
            ("runtime/nonreversible.py",),
            20,
            reversible=False,
        )
        external = candidate(
            "external",
            RIGHT_SHA,
            ("docs/external.md",),
            20,
            external_approval_required=True,
        )
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-authority-boundary",
            self.frontier,
            (nonreversible, external),
            self.policy,
        )
        self.assertEqual(selected, ())
        self.assertTrue(certificate.stable_no_change)
        self.assertFalse(certificate.execution_authority_granted)

    def test_no_strict_improvement_is_stable_fixed_point(self) -> None:
        flat = candidate("flat", LEFT_SHA, ("docs/flat.md",), 0)
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-fixed-point",
            self.frontier,
            (flat,),
            self.policy,
        )
        self.assertEqual(selected, ())
        self.assertTrue(certificate.stable_no_change)
        self.assertEqual(certificate.aggregate_score_improvement, 0)

    def test_source_frontier_tamper_is_rejected(self) -> None:
        tampered = replace(self.frontier, frontier_count=3)
        with self.assertRaisesRegex(ValueError, "frontier_certificate_invalid"):
            certify_repository_self_evolution_portfolio(
                "portfolio-frontier-tamper",
                tampered,
                (),
                self.policy,
            )

    def test_candidate_source_must_be_a_frontier_tip(self) -> None:
        broken = candidate("wrong-tip", "f" * 40, ("docs/wrong.md",), 5)
        with self.assertRaisesRegex(ValueError, "source_not_in_frontier"):
            certify_repository_self_evolution_portfolio(
                "portfolio-wrong-tip",
                self.frontier,
                (broken,),
                self.policy,
            )

    def test_candidate_bound_fails_closed(self) -> None:
        bounded = replace(self.policy, max_candidates=1)
        candidates = (
            candidate("first", LEFT_SHA, ("docs/first.md",), 2),
            candidate("second", RIGHT_SHA, ("docs/second.md",), 2),
        )
        with self.assertRaisesRegex(ValueError, "candidate_bound_exceeded"):
            certify_repository_self_evolution_portfolio(
                "portfolio-candidate-bound",
                self.frontier,
                candidates,
                bounded,
            )

    def test_portfolio_enumeration_bound_fails_closed(self) -> None:
        bounded = replace(self.policy, max_portfolios=2)
        candidates = (
            candidate("left", LEFT_SHA, ("docs/left.md",), 2),
            candidate("right", RIGHT_SHA, ("docs/right.md",), 2),
        )
        with self.assertRaisesRegex(ValueError, "portfolio_bound_exceeded"):
            certify_repository_self_evolution_portfolio(
                "portfolio-enumeration-bound",
                self.frontier,
                candidates,
                bounded,
            )

    def test_noncanonical_changed_paths_are_rejected(self) -> None:
        broken = candidate(
            "noncanonical",
            LEFT_SHA,
            ("docs/z.md", "docs/a.md"),
            5,
        )
        broken = replace(broken, changed_paths=("docs/z.md", "docs/a.md"))
        with self.assertRaisesRegex(ValueError, "changed_paths_not_canonical"):
            certify_repository_self_evolution_portfolio(
                "portfolio-path-order",
                self.frontier,
                (broken,),
                self.policy,
            )

    def test_certificate_tamper_is_detected(self) -> None:
        selected, certificate = certify_repository_self_evolution_portfolio(
            "portfolio-tamper",
            self.frontier,
            (candidate("selected", LEFT_SHA, ("docs/selected.md",), 5),),
            self.policy,
        )
        self.assertTrue(selected)
        tampered = replace(certificate, selected_candidate_count=2)
        issues = repository_self_evolution_portfolio_certificate_issues(tampered)
        self.assertIn("certificate_digest_mismatch", issues)
        self.assertIn("selected_candidate_count_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
