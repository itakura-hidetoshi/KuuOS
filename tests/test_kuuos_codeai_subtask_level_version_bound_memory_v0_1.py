from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_subtask_level_version_bound_memory_v0_1 import *
from scripts.build_codeai_subtask_level_version_bound_memory_fixture_v0_1 import build_reference_fixture


class SubtaskLevelVersionBoundMemoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = build_reference_fixture()

    def rebuild(self, fixture):
        return build_codeai_subtask_level_version_bound_memory(
            request=fixture["request"], policy=fixture["policy"], corpus=fixture["corpus"]
        )

    def reseal_request(self, fixture):
        fixture["request"] = seal(fixture["request"], REQUEST_DIGEST_FIELD)

    def reseal_policy(self, fixture):
        fixture["policy"] = seal(fixture["policy"], POLICY_DIGEST_FIELD)

    def reseal_corpus(self, fixture):
        fixture["corpus"] = seal(fixture["corpus"], CORPUS_DIGEST_FIELD)

    def reseal_entry(self, fixture, index):
        fixture["corpus"]["entries"][index] = seal(
            fixture["corpus"]["entries"][index], ENTRY_DIGEST_FIELD
        )
        self.reseal_corpus(fixture)

    def test_reference_ready(self):
        result = self.rebuild(self.fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.memory_pack["matched_entry_count"], 1)
        self.assertEqual(result.memory_pack["matched_entries"][0]["entry_id"], "memory-verify-current-001")

    def test_reference_boundaries(self):
        pack = self.fixture["memory_pack"]
        for field in (
            "repository_mutation_performed", "candidate_selected", "repair_executed",
            "execution_authority_granted", "git_authority_granted",
            "correctness_claimed", "future_success_claimed",
        ):
            self.assertFalse(pack[field])

    def test_request_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["subtask_kind"] = "edit"
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_digest_mismatch", result.issues)

    def test_policy_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["maximum_matched_entries"] = 3
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_digest_mismatch", result.issues)

    def test_entry_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["entries"][0]["subtask_summary"] = "tampered"
        self.reseal_corpus(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertTrue(any("entry:0:digest_mismatch" in issue for issue in result.issues))

    def test_corpus_digest_tamper_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["corpus"]["corpus_revision"] = "r2"
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("corpus_digest_mismatch", result.issues)

    def test_commit_mismatch_excluded(self):
        pack = self.fixture["memory_pack"]
        stale = next(
            item for item in pack["excluded_entries"]
            if "binding_mismatch:source_commit_sha" in item["reasons"]
        )
        self.assertIsNotNone(stale)

    def test_subtask_mismatch_excluded(self):
        self.assertEqual(
            self.fixture["memory_pack"]["exclusion_counts"]["binding_mismatch:subtask_kind"], 3
        )

    def test_dependency_mismatch_excluded(self):
        self.assertEqual(
            self.fixture["memory_pack"]["exclusion_counts"]["binding_mismatch:dependency_slice_digest"], 4
        )

    def test_holdout_entry_excluded(self):
        self.assertEqual(self.fixture["memory_pack"]["exclusion_counts"]["holdout_derived"], 1)

    def test_superseded_entry_excluded(self):
        self.assertEqual(self.fixture["memory_pack"]["exclusion_counts"]["superseded"], 1)

    def test_inconclusive_entry_excluded(self):
        self.assertEqual(self.fixture["memory_pack"]["exclusion_counts"]["outcome_not_allowed"], 1)

    def test_exact_entry_authority_claim_blocks_match(self):
        fixture = deepcopy(self.fixture)
        index = 3
        fixture["corpus"]["entries"][index]["candidate_selected"] = True
        self.reseal_entry(fixture, index)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.memory_pack["matched_entry_count"], 0)
        self.assertIn("forbidden_entry_claim:candidate_selected", result.memory_pack["exclusion_counts"])

    def test_holdout_policy_cannot_be_disabled(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["require_holdout_protection"] = False
        self.reseal_policy(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_required_guarantee_disabled", result.issues)

    def test_mutation_policy_cannot_be_enabled(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["allow_repository_mutation"] = True
        self.reseal_policy(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("policy_effect_or_authority_enabled", result.issues)

    def test_request_authority_claim_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["claims_git_authority"] = True
        self.reseal_request(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_claims_authority", result.issues)

    def test_unresolved_question_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["unresolved_questions"] = ["which-version"]
        self.reseal_request(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_unresolved_questions_present", result.issues)

    def test_future_request_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["request_created_epoch"] = fixture["policy"]["evaluation_epoch"] + 1
        self.reseal_request(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("request_window_invalid", result.issues)

    def test_entry_budget_blocks(self):
        fixture = deepcopy(self.fixture)
        fixture["policy"]["maximum_corpus_entries"] = 8
        self.reseal_policy(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("corpus_entry_budget_exceeded", result.issues)

    def test_no_match_is_bounded_no_hint(self):
        fixture = deepcopy(self.fixture)
        fixture["request"]["subtask_contract_digest"] = canonical_digest({"different": "contract"})
        self.reseal_request(fixture)
        fixture["policy"]["expected_subtask_contract_digest"] = fixture["request"]["subtask_contract_digest"]
        self.reseal_policy(fixture)
        result = self.rebuild(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.memory_pack["matched_entry_count"], 0)
        self.assertEqual(result.memory_pack["recommendation"], RECOMMENDATION_NONE)


if __name__ == "__main__":
    unittest.main()
