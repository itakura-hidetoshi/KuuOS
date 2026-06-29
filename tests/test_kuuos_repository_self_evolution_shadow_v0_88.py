from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_frontier_certificate_v0_86 import (
    certify_repository_frontier,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionObservation,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_repair_candidates_v0_79 import (
    generate_repository_repair_candidates,
)
from runtime.kuuos_repository_revision_dag_v0_85 import (
    certify_repository_revision_dag,
)
from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
    SHADOW_PASS,
    SHADOW_REJECT,
    SHADOW_STABLE_NO_CHANGE,
    RepositoryEvolutionShadowInput,
)
from runtime.kuuos_repository_self_evolution_shadow_v0_88 import (
    certify_repository_self_evolution_shadow,
    repository_self_evolution_shadow_certificate_issues,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositoryEvolutionCandidate,
    RepositoryEvolutionPolicy,
)
from runtime.kuuos_repository_self_evolution_v0_87 import (
    certify_repository_self_evolution_portfolio,
)
from runtime.kuuos_repository_shadow_repair_v0_79 import (
    compare_repository_candidate_in_shadow,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    LAKEFILE,
    RUNTIME_ROOT,
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryPatch,
    RepositoryRepairCandidate,
    RepositorySnapshot,
)
from tests.kuuos_repository_repair_fixture_v0_79 import (
    defective_repository_snapshot,
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
        "dag-self-evolution-shadow",
        (right, genesis, left),
    )
    _, frontier = certify_repository_frontier(
        "frontier-self-evolution-shadow",
        edges,
        dag,
    )
    return frontier


def snapshot_for_tip(tip: str) -> RepositorySnapshot:
    snapshot = defective_repository_snapshot()
    return replace(snapshot, root_label=f"fixture@{tip[:12]}")


def revision_for_tip(tip: str, snapshot: RepositorySnapshot) -> GitRevisionObservation:
    revision = GitRevisionObservation(
        "fixture",
        "",
        tip,
        (),
        (),
        snapshot.all_paths,
        snapshot.digest,
        snapshot.digest,
        True,
        False,
        "",
    )
    return replace(
        revision,
        observation_digest=git_revision_observation_digest(revision),
    )


def repair_for_path(
    snapshot: RepositorySnapshot,
    path: str,
) -> tuple[object, RepositoryRepairCandidate, int]:
    observation = observe_repository_structure(snapshot)
    repairs = generate_repository_repair_candidates(snapshot, observation)
    repair = next(item for item in repairs if item.patches[0].path == path)
    _, shadow_observation, _ = compare_repository_candidate_in_shadow(
        snapshot,
        observation,
        repair,
    )
    return observation, repair, shadow_observation.weighted_defect_score


def evolution_candidate(
    candidate_id: str,
    tip: str,
    repair: RepositoryRepairCandidate,
    baseline_score: int,
    predicted_score: int,
) -> RepositoryEvolutionCandidate:
    return RepositoryEvolutionCandidate(
        candidate_id,
        tip,
        repair.digest,
        tuple(sorted(patch.path for patch in repair.patches)),
        baseline_score,
        predicted_score,
        1,
        True,
        True,
        True,
        False,
    )


class RepositorySelfEvolutionShadowV088Tests(unittest.TestCase):
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
            protected_path_prefixes=(),
        )

        left_snapshot = snapshot_for_tip(LEFT_SHA)
        left_observation, left_repair, left_score = repair_for_path(
            left_snapshot,
            RUNTIME_ROOT,
        )
        right_snapshot = snapshot_for_tip(RIGHT_SHA)
        right_observation, right_repair, right_score = repair_for_path(
            right_snapshot,
            LAKEFILE,
        )
        left_evolution = evolution_candidate(
            "shadow-left-runtime",
            LEFT_SHA,
            left_repair,
            left_observation.weighted_defect_score,
            left_score,
        )
        right_evolution = evolution_candidate(
            "shadow-right-lake",
            RIGHT_SHA,
            right_repair,
            right_observation.weighted_defect_score,
            right_score,
        )
        selected, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-v088",
            self.frontier,
            (right_evolution, left_evolution),
            self.policy,
        )
        self.assertEqual(len(selected), 2)
        self.portfolio = portfolio
        by_digest = {
            left_evolution.digest: RepositoryEvolutionShadowInput(
                left_evolution,
                revision_for_tip(LEFT_SHA, left_snapshot),
                left_snapshot,
                left_observation,
                left_repair,
            ),
            right_evolution.digest: RepositoryEvolutionShadowInput(
                right_evolution,
                revision_for_tip(RIGHT_SHA, right_snapshot),
                right_snapshot,
                right_observation,
                right_repair,
            ),
        }
        self.inputs = tuple(by_digest[digest] for digest in portfolio.selected_candidate_digests)

    def test_exact_predictions_pass_shadow_replay(self) -> None:
        assessments, certificate = certify_repository_self_evolution_shadow(
            "shadow-exact",
            self.portfolio,
            self.inputs,
        )
        self.assertEqual(len(assessments), 2)
        self.assertEqual(certificate.status, SHADOW_PASS)
        self.assertTrue(certificate.portfolio_shadow_admissible)
        self.assertTrue(certificate.strict_score_descent_observed)
        self.assertTrue(certificate.predictions_within_tolerance)
        self.assertTrue(certificate.exact_shadow_rollback)
        self.assertTrue(certificate.normal_form_certified)
        self.assertFalse(certificate.patch_application_authority_granted)
        self.assertFalse(certificate.commit_authority_granted)
        self.assertFalse(certificate.reference_mutation_authority_granted)
        self.assertEqual(
            repository_self_evolution_shadow_certificate_issues(certificate),
            (),
        )

    def test_prediction_mismatch_is_certified_reject(self) -> None:
        first = self.inputs[0]
        mismatched_evolution = replace(
            first.evolution_candidate,
            predicted_score=first.evolution_candidate.predicted_score - 1,
        )
        selected, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-mismatch",
            self.frontier,
            (mismatched_evolution, self.inputs[1].evolution_candidate),
            self.policy,
        )
        self.assertEqual(len(selected), 2)
        inputs = (
            replace(first, evolution_candidate=mismatched_evolution),
            self.inputs[1],
        )
        assessments, certificate = certify_repository_self_evolution_shadow(
            "shadow-mismatch",
            portfolio,
            inputs,
        )
        self.assertEqual(certificate.status, SHADOW_REJECT)
        self.assertFalse(certificate.predictions_within_tolerance)
        self.assertFalse(certificate.portfolio_shadow_admissible)
        self.assertTrue(any(item.prediction_error == 1 for item in assessments))
        self.assertEqual(
            repository_self_evolution_shadow_certificate_issues(certificate),
            (),
        )

    def test_prediction_tolerance_can_admit_bounded_error(self) -> None:
        first = self.inputs[0]
        mismatched_evolution = replace(
            first.evolution_candidate,
            predicted_score=first.evolution_candidate.predicted_score - 1,
        )
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-tolerance",
            self.frontier,
            (mismatched_evolution, self.inputs[1].evolution_candidate),
            self.policy,
        )
        inputs = (
            replace(first, evolution_candidate=mismatched_evolution),
            self.inputs[1],
        )
        _, certificate = certify_repository_self_evolution_shadow(
            "shadow-tolerance",
            portfolio,
            inputs,
            prediction_tolerance=1,
        )
        self.assertEqual(certificate.status, SHADOW_PASS)
        self.assertTrue(certificate.predictions_within_tolerance)

    def test_nonimproving_patch_is_shadow_reject(self) -> None:
        base = snapshot_for_tip(LEFT_SHA)
        snapshot = RepositorySnapshot(
            base.root_label,
            tuple(sorted((*base.all_paths, "docs/note.md"))),
            tuple(sorted((*base.text_files, ("docs/note.md", "before\n")))),
        )
        observation = observe_repository_structure(snapshot)
        patch = RepositoryPatch(
            "docs/note.md",
            canonical_digest("before\n"),
            "after\n",
            "SHADOW_ONLY_NOTE",
            "does not repair a registered defect",
        )
        repair = RepositoryRepairCandidate(
            "shadow-nonimproving",
            snapshot.digest,
            observation.digest,
            (patch,),
            True,
        )
        evolution = evolution_candidate(
            "shadow-nonimproving",
            LEFT_SHA,
            repair,
            observation.weighted_defect_score,
            observation.weighted_defect_score - 1,
        )
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-nonimproving",
            self.frontier,
            (evolution,),
            self.policy,
        )
        input_value = RepositoryEvolutionShadowInput(
            evolution,
            revision_for_tip(LEFT_SHA, snapshot),
            snapshot,
            observation,
            repair,
        )
        assessments, certificate = certify_repository_self_evolution_shadow(
            "shadow-nonimproving",
            portfolio,
            (input_value,),
        )
        self.assertEqual(certificate.status, SHADOW_REJECT)
        self.assertFalse(certificate.strict_score_descent_observed)
        self.assertFalse(assessments[0].strict_improvement_observed)

    def test_stable_no_change_portfolio_is_fixed_point(self) -> None:
        selected, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-stable",
            self.frontier,
            (),
            self.policy,
        )
        self.assertEqual(selected, ())
        assessments, certificate = certify_repository_self_evolution_shadow(
            "shadow-stable",
            portfolio,
            (),
        )
        self.assertEqual(assessments, ())
        self.assertEqual(certificate.status, SHADOW_STABLE_NO_CHANGE)
        self.assertTrue(certificate.stable_no_change)
        self.assertTrue(certificate.portfolio_shadow_admissible)

    def test_stable_portfolio_rejects_realization(self) -> None:
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-shadow-stable-input",
            self.frontier,
            (),
            self.policy,
        )
        with self.assertRaisesRegex(ValueError, "stable_portfolio_realization_forbidden"):
            certify_repository_self_evolution_shadow(
                "shadow-stable-input",
                portfolio,
                (self.inputs[0],),
            )

    def test_missing_realization_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "shadow_realization_count_mismatch"):
            certify_repository_self_evolution_shadow(
                "shadow-missing",
                self.portfolio,
                (self.inputs[0],),
            )

    def test_duplicate_realization_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "shadow_realization_candidate_replay"):
            certify_repository_self_evolution_shadow(
                "shadow-replay",
                self.portfolio,
                (self.inputs[0], self.inputs[0]),
            )

    def test_source_commit_binding_fails_closed(self) -> None:
        first = self.inputs[0]
        revision = replace(
            first.revision_observation,
            current_commit_sha="f" * 40,
            observation_digest="",
        )
        revision = replace(
            revision,
            observation_digest=git_revision_observation_digest(revision),
        )
        broken = replace(first, revision_observation=revision)
        with self.assertRaisesRegex(ValueError, "source_commit_binding_mismatch"):
            certify_repository_self_evolution_shadow(
                "shadow-commit-binding",
                self.portfolio,
                (broken, self.inputs[1]),
            )

    def test_source_snapshot_binding_fails_closed(self) -> None:
        first = self.inputs[0]
        revision = replace(
            first.revision_observation,
            current_snapshot_digest="0" * 64,
            observation_digest="",
        )
        revision = replace(
            revision,
            observation_digest=git_revision_observation_digest(revision),
        )
        broken = replace(first, revision_observation=revision)
        with self.assertRaisesRegex(ValueError, "source_snapshot_binding_mismatch"):
            certify_repository_self_evolution_shadow(
                "shadow-snapshot-binding",
                self.portfolio,
                (broken, self.inputs[1]),
            )

    def test_working_tree_source_is_forbidden(self) -> None:
        first = self.inputs[0]
        revision = replace(
            first.revision_observation,
            working_tree_read=True,
            observation_digest="",
        )
        revision = replace(
            revision,
            observation_digest=git_revision_observation_digest(revision),
        )
        broken = replace(first, revision_observation=revision)
        with self.assertRaisesRegex(ValueError, "shadow_working_tree_source_forbidden"):
            certify_repository_self_evolution_shadow(
                "shadow-working-tree",
                self.portfolio,
                (broken, self.inputs[1]),
            )

    def test_object_database_source_is_required(self) -> None:
        first = self.inputs[0]
        revision = replace(
            first.revision_observation,
            object_database_read=False,
            observation_digest="",
        )
        revision = replace(
            revision,
            observation_digest=git_revision_observation_digest(revision),
        )
        broken = replace(first, revision_observation=revision)
        with self.assertRaisesRegex(ValueError, "shadow_source_not_from_object_database"):
            certify_repository_self_evolution_shadow(
                "shadow-object-database",
                self.portfolio,
                (broken, self.inputs[1]),
            )

    def test_revision_observation_tamper_is_rejected(self) -> None:
        broken = replace(
            self.inputs[0],
            revision_observation=replace(
                self.inputs[0].revision_observation,
                observation_digest="tampered",
            ),
        )
        with self.assertRaisesRegex(ValueError, "git_revision_observation_digest_mismatch"):
            certify_repository_self_evolution_shadow(
                "shadow-revision-tamper",
                self.portfolio,
                (broken, self.inputs[1]),
            )

    def test_portfolio_certificate_tamper_is_rejected(self) -> None:
        tampered = replace(self.portfolio, selected_candidate_count=3)
        with self.assertRaisesRegex(ValueError, "portfolio_certificate_invalid"):
            certify_repository_self_evolution_shadow(
                "shadow-portfolio-tamper",
                tampered,
                self.inputs,
            )

    def test_shadow_certificate_tamper_is_detected(self) -> None:
        _, certificate = certify_repository_self_evolution_shadow(
            "shadow-certificate-tamper",
            self.portfolio,
            self.inputs,
        )
        tampered = replace(certificate, assessment_count=3)
        issues = repository_self_evolution_shadow_certificate_issues(tampered)
        self.assertIn("certificate_digest_mismatch", issues)
        self.assertIn("assessment_count_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
