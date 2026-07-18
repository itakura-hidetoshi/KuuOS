from tests.codeai_candidate_regeneration_test_support_v0_1 import *

class CandidateRegenerationTestsPart1(unittest.TestCase):
    def test_regenerates_two_novel_candidates_to_target(self):
        data = _inputs()
        adapters = [
            _adapter("a-gpt", "gpt", [_response(
                "r1", "s1", "novel-a", "docs/CodeAI/NOVEL_A.md",
                "# Novel A\n\nAlternative A.\n",
            )]),
            _adapter("b-local", "local_model", [_response(
                "r2", "s2", "novel-b", "docs/CodeAI/NOVEL_B.md",
                "# Novel B\n\nAlternative B.\n",
            )]),
        ]
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=adapters
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(len(result.regenerated_candidates), 2)
        self.assertEqual(len(result.combined_candidates), 3)
        self.assertTrue(result.receipt["target_reached"])
        self.assertEqual(result.receipt["provider_call_count"], 2)

    def test_semantic_duplicate_then_second_round_novel(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        prompts = []
        responses = [
            _response(
                "dup-r", "dup-s", "different-id-same-patch",
                "docs/CodeAI/PROVIDER_STRUCTURED_EDIT_EXAMPLE.md",
                "# Provider structured edit example\n\nThis file is proposed as candidate material and is not applied by synthesis.\n",
            ),
            _response(
                "new-r", "new-s", "novel-second-round",
                "docs/CodeAI/NOVEL_SECOND_ROUND.md",
                "# Novel second round\n\nGenerated after duplicate feedback.\n",
            ),
        ]
        def generate(prompt):
            prompts.append(prompt)
            return responses.pop(0)
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=[_adapter("a-gpt", "gpt", generate)]
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(len(result.attempts), 2)
        self.assertEqual(result.attempts[0].novelty_rejection_reason, "semantic_duplicate_patch_artifact")
        self.assertTrue(result.attempts[1].accepted_novel_candidate)
        self.assertIn("a-gpt:semantic_duplicate_patch_artifact", prompts[1]["feedback_reasons"])

    def test_repair_feedback_is_carried_into_next_round(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        prompts = []
        responses = [
            _response("bad-r", "bad-s", "ignored", "x", "", raw_output="not-json"),
            _response(
                "good-r", "good-s", "repaired-novel",
                "docs/CodeAI/REPAIRED_NOVEL.md",
                "# Repaired novel\n\nA governed regeneration.\n",
            ),
        ]
        def generate(prompt):
            prompts.append(prompt)
            return responses.pop(0)
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=[_adapter("a-gpt", "gpt", generate)]
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertIn("a-gpt:raw_output_json_invalid", prompts[1]["feedback_reasons"])
        self.assertEqual(result.receipt["no_progress_rounds"], 1)

    def test_provider_exception_isolated_from_supported_sibling(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["target_unique_candidate_count"] = 2
        data["regeneration_request"] = _reseal_request(request)
        def explode(_prompt):
            raise RuntimeError("boom")
        adapters = [
            _adapter("a-broken", "gpt", explode),
            _adapter("b-local", "local_model", [_response(
                "ok-r", "ok-s", "exception-sibling-novel",
                "docs/CodeAI/EXCEPTION_SIBLING.md",
                "# Exception sibling\n\nThe sibling candidate survives.\n",
            )]),
        ]
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=adapters
        )
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(len(result.regenerated_candidates), 1)
        self.assertIn("a-broken:provider_exception:RuntimeError", result.issues)

    def test_source_generation_receipt_tamper_blocks(self):
        data = _inputs()
        data["source_generation_receipt"]["generated_candidate_count"] = 99
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=[_adapter("a-gpt", "gpt", [])]
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_generation_receipt_digest_mismatch", result.issues)

    def test_seed_candidate_correspondence_is_exact(self):
        data = _inputs()
        data["seed_candidates"] = ()
        result = build_codeai_autonomous_candidate_regeneration(
            **data, provider_adapters=[_adapter("a-gpt", "gpt", [])]
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("source_generation_candidate_ids_mismatch", result.issues)

    def test_stale_request_blocks_before_provider_call(self):
        data = _inputs()
        request = data["regeneration_request"]
        request["request_created_epoch"] = 1
        data["regeneration_request"] = _reseal_request(request)
        calls = []
        result = build_codeai_autonomous_candidate_regeneration(
            **data,
            provider_adapters=[_adapter("a-gpt", "gpt", lambda prompt: calls.append(prompt))],
        )
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(calls, [])
        self.assertIn("regeneration_request_window_invalid", result.issues)

