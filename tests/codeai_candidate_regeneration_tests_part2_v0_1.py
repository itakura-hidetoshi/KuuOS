from tests.codeai_candidate_regeneration_test_support_v0_1 import *

class CandidateRegenerationTestsPart2(unittest.TestCase):
    def test_disallowed_provider_blocks(self):
        data = _inputs()
        result = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gemini", "gemini", [])],
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("provider_not_allowed:gemini", result.issues)

    def test_total_call_budget_bounds_regeneration(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 4
        request["maximum_rounds_requested"] = 2
        data["regeneration_request"] = _reseal_request(request)
        policy = data["regeneration_policy"]
        policy["maximum_total_provider_calls"] = 2
        policy["maximum_provider_calls_per_round"] = 1
        data["regeneration_policy"] = _reseal_policy(policy)
        duplicate = _response(
            "d1", "ds1", "dup1",
            "docs/CodeAI/PROVIDER_STRUCTURED_EDIT_EXAMPLE.md",
            "# Provider structured edit example\n\nThis file is proposed as candidate material and is not applied by synthesis.\n",
        )
        duplicate2 = copy.deepcopy(duplicate)
        duplicate2["provider_response_id"] = "d2"
        duplicate2["producer_session_id"] = "ds2"
        result = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gpt", "gpt", [duplicate, duplicate2])],
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(len(result.attempts), 2)
        self.assertEqual(result.receipt["provider_call_count"], 2)

    def test_regenerated_candidate_binds_seed_lineage(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        result = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gpt", "gpt", [_response(
                "lineage-r", "lineage-s", "lineage-novel",
                "docs/CodeAI/LINEAGE_NOVEL.md",
                "# Lineage novel\n\nCarries prior candidate lineage.\n",
            )])],
        )
        self.assertEqual(result.status, STATUS_READY)
        seed = data["seed_candidates"][0].patch_candidate
        regenerated = result.regenerated_candidates[0].patch_candidate
        self.assertIn(seed[CANDIDATE_DIGEST_FIELD], regenerated["prior_candidate_digests"])
        self.assertIn(seed["producer_session_id"], regenerated["prior_producer_session_ids"])

    def test_combined_portfolio_is_ranked_and_patch_unique(self):
        data = _inputs()
        adapters = [
            _adapter("a-gpt", "gpt", [_response(
                "r1", "s1", "z-larger", "docs/CodeAI/Z_LARGER.md",
                "# Larger\n\n" + "content\n" * 10,
            )]),
            _adapter("b-local", "local_model", [_response(
                "r2", "s2", "a-small", "docs/CoeAI/A_SMALL.md",
                "# Small\n",
            )]),
        ]
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=adapters
        )
        self.assertEqual([item.rank for item in result.combined_candidates], [1, 2, 3])
        artifacts = [item.patch_candidate["patch_artifact_digest"] for item in result.combined_candidates]
        self.assertEqual(len(artifacts), len(set(artifacts)))

    def test_regeneration_grants_no_selection_verification_or_git_effect(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        result = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gpt", "gpt", [_response(
                "r", "s", "no-effect-novel", "docs/CodeAI/NO_EFFECT.md",
                "# No effect\n",
            )])],
        )
        receipt = result.receipt
        self.assertFalse(receipt["candidate_selected"])
        self.assertFalse(receipt["verification_authority_granted"])
        self.assertFalse(receipt["execution_authority_granted"])
        self.assertFalse(receipt["patch_applied"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["git_ref_changed"])
        self.assertFalse(receipt["commit_created"])
        self.assertFalse(receipt["push_performed"])
        self.assertFalse(receipt["merge_performed"])
        self.assertFalse(receipt["novelty_treated_as_correctness"])

    def test_regeneration_receipt_can_seed_next_regeneration(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        first = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gpt", "gpt", [_response(
                "r1", "s1", "first-novel", "docs/CodeAI/FIRST_NOVEL.md",
                "# First novel\n",
            )])],
        )
        self.assertEqual(first.status, STATUS_READY)
        next_data = _inputs()
        next_data["source_generation_receipt"] = first.receipt
        next_data["seed_candidates"] = first.combined_candidates
        next_request = next_data["regeneration_request"]
        next_request["request_id"] = "codeai-candidate-regeneration-v0-1-002"
        next_request["request_revision"] = "r2"
        next_request["target_unique_candidate_count"] = 3
        next_data["regeneration_request"] = _reseal_request(next_request)
        second = build_codeai_autonomous_candidate_regeneration(
            **next_data,
            provider_adapters=[_adapter("a-gpt", "gpt", [_response(
                "r2", "s2", "second-novel", "docs/CodeAI/SECOND_NOVEL.md",
                "# Second novel\n",
            )])],
        )
        self.assertEqual(second.status, STATUS_READY)
        self.assertEqual(len(second.combined_candidates), 3)
        self.assertEqual(second.receipt["source_generation_profile_version"],
                         "CodeAI Autonomous Candidate Regeneration v0.1")

