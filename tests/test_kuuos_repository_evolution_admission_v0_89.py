from __future__ import annotations

from dataclasses import replace
import unittest

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_evolution_admission_types_v0_89 import (
    ADMISSION_PROPOSED,
    ADMISSION_REJECTED,
    ADMISSION_STABLE_NO_CHANGE,
)
from runtime.kuuos_repository_evolution_admission_v0_89 import (
    build_repository_shadow_replay_receipt,
    certify_repository_evolution_admission,
    repository_evolution_admission_certificate_issues,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    git_revision_observation_digest,
)
from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
    SHADOW_REJECT,
)
from runtime.kuuos_repository_self_evolution_shadow_v0_88 import (
    certify_repository_self_evolution_shadow,
)
from runtime.kuuos_repository_self_evolution_types_v0_87 import (
    RepositoryEvolutionPolicy,
)
from runtime.kuuos_repository_self_evolution_v0_87 import (
    certify_repository_self_evolution_portfolio,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    LAKEFILE,
    RUNTIME_ROOT,
)
from tests.test_kuuos_repository_revision_dag_v0_85 import LEFT_SHA, RIGHT_SHA
from tests.test_kuuos_repository_self_evolution_shadow_v0_88 import (
    evolution_candidate,
    open_frontier,
    repair_for_path,
    revision_for_tip,
    snapshot_for_tip,
)


class RepositoryEvolutionAdmissionV089Tests(unittest.TestCase):
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
        left = evolution_candidate(
            "admission-left-runtime",
            LEFT_SHA,
            left_repair,
            left_observation.weighted_defect_score,
            left_score,
        )
        right = evolution_candidate(
            "admission-right-lake",
            RIGHT_SHA,
            right_repair,
            right_observation.weighted_defect_score,
            right_score,
        )
        _, self.portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-admission-v089",
            self.frontier,
            (right, left),
            self.policy,
        )
        by_digest = {
            left.digest: (
                left,
                revision_for_tip(LEFT_SHA, left_snapshot),
                left_snapshot,
                left_observation,
                left_repair,
            ),
            right.digest: (
                right,
                revision_for_tip(RIGHT_SHA, right_snapshot),
                right_snapshot,
                right_observation,
                right_repair,
            ),
        }
        from runtime.kuuos_repository_self_evolution_shadow_types_v0_88 import (
            RepositoryEvolutionShadowInput,
        )
        self.inputs = tuple(
            RepositoryEvolutionShadowInput(*by_digest[digest])
            for digest in self.portfolio.selected_candidate_digests
        )
        self.current = tuple(item.revision_observation for item in self.inputs)
        self.approval_policy_digest = canonical_digest({
            "policy": "external-human-approval-required",
            "version": "v0.89",
        })
        self.receipts = self._pass_receipts()

    def _pass_receipts(self):
        result = []
        for index, issued in enumerate((1000, 1010), start=1):
            assessments, certificate = certify_repository_self_evolution_shadow(
                f"admission-shadow-{index}",
                self.portfolio,
                self.inputs,
            )
            result.append(build_repository_shadow_replay_receipt(
                f"replay-{index}",
                issued,
                assessments,
                certificate,
            ))
        return tuple(result)

    def _certify(self, receipts=None, current=None, **kwargs):
        return certify_repository_evolution_admission(
            "admission-v089",
            self.receipts if receipts is None else receipts,
            self.current if current is None else current,
            approval_policy_digest=self.approval_policy_digest,
            evaluated_at_epoch_seconds=kwargs.pop("evaluated_at_epoch_seconds", 1100),
            max_certificate_age_seconds=kwargs.pop("max_certificate_age_seconds", 500),
            required_replay_count=kwargs.pop("required_replay_count", 2),
            **kwargs,
        )

    def test_two_fresh_identical_replays_generate_proposal(self) -> None:
        certificate = self._certify()
        self.assertEqual(certificate.status, ADMISSION_PROPOSED)
        self.assertTrue(certificate.all_shadow_pass)
        self.assertTrue(certificate.replay_count_satisfied)
        self.assertTrue(certificate.replay_results_identical)
        self.assertTrue(certificate.certificates_fresh)
        self.assertTrue(certificate.source_revisions_unchanged)
        self.assertTrue(certificate.source_snapshots_unchanged)
        self.assertTrue(certificate.admission_proposal_generated)
        self.assertTrue(certificate.external_approval_required)
        self.assertFalse(certificate.external_approval_granted)
        self.assertFalse(certificate.patch_application_authority_granted)
        self.assertFalse(certificate.commit_authority_granted)
        self.assertFalse(certificate.reference_mutation_authority_granted)
        self.assertEqual(repository_evolution_admission_certificate_issues(certificate), ())

    def test_one_replay_is_certified_reject(self) -> None:
        certificate = self._certify(receipts=(self.receipts[0],))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.replay_count_satisfied)
        self.assertFalse(certificate.admission_proposal_generated)

    def test_expired_receipt_is_certified_reject(self) -> None:
        certificate = self._certify(
            evaluated_at_epoch_seconds=2000,
            max_certificate_age_seconds=100,
        )
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.certificates_fresh)

    def test_future_receipt_is_certified_reject(self) -> None:
        certificate = self._certify(evaluated_at_epoch_seconds=900)
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.no_future_certificates)
        self.assertFalse(certificate.certificates_fresh)

    def test_source_snapshot_change_is_certified_reject(self) -> None:
        first = self.current[0]
        changed = replace(
            first,
            current_snapshot_digest="0" * 64,
            observation_digest="",
        )
        changed = replace(
            changed,
            observation_digest=git_revision_observation_digest(changed),
        )
        certificate = self._certify(current=(changed, self.current[1]))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertTrue(certificate.source_revisions_unchanged)
        self.assertFalse(certificate.source_snapshots_unchanged)

    def test_source_revision_change_is_certified_reject(self) -> None:
        first = self.current[0]
        changed = replace(
            first,
            current_commit_sha="f" * 40,
            observation_digest="",
        )
        changed = replace(
            changed,
            observation_digest=git_revision_observation_digest(changed),
        )
        certificate = self._certify(current=(changed, self.current[1]))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.current_revision_observations_complete)
        self.assertFalse(certificate.source_revisions_unchanged)

    def test_missing_current_revision_is_certified_reject(self) -> None:
        certificate = self._certify(current=(self.current[0],))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.current_revision_observations_complete)

    def test_working_tree_observation_is_certified_reject(self) -> None:
        first = replace(
            self.current[0],
            working_tree_read=True,
            observation_digest="",
        )
        first = replace(
            first,
            observation_digest=git_revision_observation_digest(first),
        )
        certificate = self._certify(current=(first, self.current[1]))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.working_tree_ignored)

    def test_object_database_observation_is_required(self) -> None:
        first = replace(
            self.current[0],
            object_database_read=False,
            observation_digest="",
        )
        first = replace(
            first,
            observation_digest=git_revision_observation_digest(first),
        )
        certificate = self._certify(current=(first, self.current[1]))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.object_database_sources_only)

    def test_nonidentical_replay_results_are_certified_reject(self) -> None:
        first_input = self.inputs[0]
        _, other_portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-admission-other",
            self.frontier,
            (first_input.evolution_candidate,),
            self.policy,
        )
        assessments, shadow = certify_repository_self_evolution_shadow(
            "admission-shadow-other",
            other_portfolio,
            (first_input,),
        )
        other = build_repository_shadow_replay_receipt(
            "replay-other",
            1020,
            assessments,
            shadow,
        )
        certificate = self._certify(receipts=(self.receipts[0], other))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.replay_results_identical)

    def test_shadow_reject_cannot_generate_admission(self) -> None:
        first = self.inputs[0]
        mismatched = replace(
            first.evolution_candidate,
            predicted_score=first.evolution_candidate.predicted_score - 1,
        )
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-admission-reject",
            self.frontier,
            (mismatched, self.inputs[1].evolution_candidate),
            self.policy,
        )
        inputs = (replace(first, evolution_candidate=mismatched), self.inputs[1])
        receipts = []
        for index in (1, 2):
            assessments, shadow = certify_repository_self_evolution_shadow(
                f"admission-shadow-reject-{index}",
                portfolio,
                inputs,
            )
            self.assertEqual(shadow.status, SHADOW_REJECT)
            receipts.append(build_repository_shadow_replay_receipt(
                f"replay-reject-{index}",
                1000 + index,
                assessments,
                shadow,
            ))
        certificate = self._certify(receipts=tuple(receipts))
        self.assertEqual(certificate.status, ADMISSION_REJECTED)
        self.assertFalse(certificate.all_shadow_pass)

    def test_repeated_stable_no_change_is_preserved(self) -> None:
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-admission-stable",
            self.frontier,
            (),
            self.policy,
        )
        receipts = []
        for index in (1, 2):
            assessments, shadow = certify_repository_self_evolution_shadow(
                f"admission-stable-shadow-{index}",
                portfolio,
                (),
            )
            receipts.append(build_repository_shadow_replay_receipt(
                f"stable-replay-{index}",
                1000 + index,
                assessments,
                shadow,
            ))
        certificate = self._certify(receipts=tuple(receipts), current=())
        self.assertEqual(certificate.status, ADMISSION_STABLE_NO_CHANGE)
        self.assertTrue(certificate.stable_no_change)
        self.assertFalse(certificate.admission_proposal_generated)

    def test_stable_and_nonstable_receipts_fail_closed(self) -> None:
        _, portfolio = certify_repository_self_evolution_portfolio(
            "portfolio-admission-mixed",
            self.frontier,
            (),
            self.policy,
        )
        assessments, shadow = certify_repository_self_evolution_shadow(
            "admission-mixed-stable",
            portfolio,
            (),
        )
        stable = build_repository_shadow_replay_receipt(
            "stable-mixed",
            1000,
            assessments,
            shadow,
        )
        with self.assertRaisesRegex(ValueError, "shadow_status_mode_mismatch"):
            self._certify(receipts=(stable, self.receipts[0]))

    def test_receipt_tamper_fails_closed(self) -> None:
        tampered = replace(self.receipts[0], issued_at_epoch_seconds=999)
        with self.assertRaisesRegex(ValueError, "shadow_replay_receipt_invalid"):
            self._certify(receipts=(tampered, self.receipts[1]))

    def test_current_revision_tamper_fails_closed(self) -> None:
        tampered = replace(self.current[0], observation_digest="tampered")
        with self.assertRaisesRegex(ValueError, "current_revision_observation_digest_mismatch"):
            self._certify(current=(tampered, self.current[1]))

    def test_required_replay_count_cannot_be_one(self) -> None:
        with self.assertRaisesRegex(ValueError, "required_replay_count_too_small"):
            self._certify(required_replay_count=1)

    def test_certificate_tamper_is_detected(self) -> None:
        certificate = self._certify()
        tampered = replace(certificate, replay_count=3)
        issues = repository_evolution_admission_certificate_issues(tampered)
        self.assertIn("replay_count_mismatch", issues)
        self.assertIn("certificate_digest_mismatch", issues)


if __name__ == "__main__":
    unittest.main()
