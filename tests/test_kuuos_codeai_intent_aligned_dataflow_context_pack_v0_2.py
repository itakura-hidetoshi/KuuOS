from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_checks_v0_2 import canonical_digest, seal
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2 import (
    HYPOTHESIS_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_v0_2 import (
    build_intent_aligned_dataflow_context_pack,
)
from scripts.build_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2 import (
    build_reference_inputs,
    build_reference_result,
)


class IntentAlignedDataflowContextPackV02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.inputs = build_reference_inputs()

    def build(self):
        return build_intent_aligned_dataflow_context_pack(**self.inputs)

    def reseal_request(self) -> None:
        self.inputs["request"] = seal(self.inputs["request"], REQUEST_DIGEST_FIELD)

    def reseal_policy(self) -> None:
        self.inputs["policy"] = seal(self.inputs["policy"], POLICY_DIGEST_FIELD)

    def reseal_source(self) -> None:
        self.inputs["source_observation_receipt"] = seal(
            self.inputs["source_observation_receipt"], SOURCE_RECEIPT_DIGEST_FIELD
        )

    def test_01_reference_builds(self) -> None:
        result = self.build()
        self.assertEqual(result.status, "ready")
        self.assertEqual(result.issues, ())
        self.assertIsNotNone(result.context_pack)
        self.assertIsNotNone(result.receipt)

    def test_02_reference_is_deterministic(self) -> None:
        first = build_reference_result()
        second = build_reference_result()
        self.assertEqual(first["context_pack"], second["context_pack"])
        self.assertEqual(first["receipt"], second["receipt"])

    def test_03_query_lineage_has_all_stages(self) -> None:
        pack = build_reference_result()["context_pack"]
        self.assertEqual(
            [item["stage"] for item in pack["query_lineage"]],
            ["intent", "hypothesis", "hypothesis", "symbol", "dependency", "dataflow"],
        )

    def test_04_every_selected_file_has_symbol_digest(self) -> None:
        pack = build_reference_result()["context_pack"]
        for item in pack["selected_files"]:
            self.assertEqual(item["symbol_digest"], canonical_digest(item["symbols"]))

    def test_05_runtime_dependency_resolves_to_pricing(self) -> None:
        pack = build_reference_result()["context_pack"]
        order = next(item for item in pack["selected_files"] if item["path"] == "runtime/order_pipeline.py")
        self.assertIn(
            ["runtime/order_pipeline.py", "runtime/pricing.py"],
            order["resolved_dependency_paths"],
        )

    def test_06_formal_dependency_resolves_to_pricing(self) -> None:
        pack = build_reference_result()["context_pack"]
        order = next(
            item
            for item in pack["selected_files"]
            if item["path"] == "formal/KUOS/CodeAI/OrderPipelineReferenceV0_2.lean"
        )
        self.assertIn(
            [
                "formal/KUOS/CodeAI/OrderPipelineReferenceV0_2.lean",
                "formal/KUOS/CodeAI/PricingReferenceV0_2.lean",
            ],
            order["resolved_dependency_paths"],
        )

    def test_07_runtime_dataflow_is_extracted(self) -> None:
        pack = build_reference_result()["context_pack"]
        order = next(item for item in pack["selected_files"] if item["path"] == "runtime/order_pipeline.py")
        self.assertIn(["compute_subtotal", "subtotal"], order["dataflow_edges"])
        self.assertIn(["subtotal", "taxed_total"], order["dataflow_edges"])

    def test_08_budget_evidence_is_bounded(self) -> None:
        pack = build_reference_result()["context_pack"]
        budget = pack["budget_evidence"]
        self.assertLessEqual(budget["selected_file_count"], budget["maximum_selected_files"])
        self.assertLessEqual(budget["total_context_bytes"], budget["maximum_total_context_bytes"])

    def test_09_unrelated_file_is_not_selected(self) -> None:
        pack = build_reference_result()["context_pack"]
        paths = {item["path"] for item in pack["selected_files"]}
        self.assertNotIn("config/unrelated_feature.json", paths)

    def test_10_request_digest_tamper_blocks(self) -> None:
        self.inputs["request"]["intent_text"] += " tampered"
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_digest_mismatch", result.issues)

    def test_11_policy_digest_tamper_blocks(self) -> None:
        self.inputs["policy"]["maximum_selected_files"] += 1
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_policy_digest_mismatch", result.issues)

    def test_12_hypothesis_digest_tamper_blocks(self) -> None:
        self.inputs["request"]["candidate_hypotheses"][0]["statement"] += " tampered"
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(issue.endswith("_digest_mismatch") for issue in result.issues))

    def test_13_stale_request_blocks(self) -> None:
        self.inputs["policy"]["evaluation_epoch"] = 200
        self.reseal_policy()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_stale", result.issues)

    def test_14_future_request_blocks(self) -> None:
        self.inputs["request"]["request_created_epoch"] = 200
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_from_future", result.issues)

    def test_15_source_receipt_digest_mismatch_blocks(self) -> None:
        self.inputs["request"]["expected_source_observation_receipt_digest"] = "0" * 64
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_source_receipt_digest_mismatch", result.issues)

    def test_16_repository_mismatch_blocks(self) -> None:
        self.inputs["source_observation_receipt"]["repository_full_name"] = "other/repo"
        self.reseal_source()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("source_observation_receipt_repository_mismatch", result.issues)

    def test_17_commit_mismatch_blocks(self) -> None:
        self.inputs["source_observation_receipt"]["source_commit_sha"] = "0" * 40
        self.reseal_source()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("source_observation_receipt_commit_mismatch", result.issues)

    def test_18_snapshot_digest_mismatch_blocks(self) -> None:
        self.inputs["repository_snapshot"]["docs/order_pipeline_dataflow.md"] += "changed\n"
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_repository_snapshot_digest_mismatch", result.issues)

    def test_19_path_traversal_blocks(self) -> None:
        self.inputs["repository_snapshot"]["../secret.py"] = "value = 1\n"
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(issue.startswith("repository_file_path_invalid") for issue in result.issues))

    def test_20_forbidden_prefix_blocks(self) -> None:
        repository = self.inputs["repository_snapshot"]
        repository[".secrets/token.md"] = "not-a-secret\n"
        digest = canonical_digest(repository)
        self.inputs["request"]["repository_snapshot_digest"] = digest
        self.reseal_request()
        self.inputs["source_observation_receipt"]["tree_digest"] = digest
        self.reseal_source()
        self.inputs["request"]["expected_source_observation_receipt_digest"] = (
            self.inputs["source_observation_receipt"][SOURCE_RECEIPT_DIGEST_FIELD]
        )
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("repository_file_forbidden_prefix:.secrets/token.md", result.issues)

    def test_21_unsupported_suffix_blocks(self) -> None:
        repository = self.inputs["repository_snapshot"]
        repository["runtime/native.bin"] = "text\n"
        digest = canonical_digest(repository)
        self.inputs["request"]["repository_snapshot_digest"] = digest
        self.reseal_request()
        self.inputs["source_observation_receipt"]["tree_digest"] = digest
        self.reseal_source()
        self.inputs["request"]["expected_source_observation_receipt_digest"] = (
            self.inputs["source_observation_receipt"][SOURCE_RECEIPT_DIGEST_FIELD]
        )
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("repository_file_unsupported_suffix:runtime/native.bin", result.issues)

    def test_22_snapshot_byte_budget_blocks(self) -> None:
        self.inputs["policy"]["maximum_repository_snapshot_bytes"] = 10
        self.reseal_policy()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("repository_snapshot_byte_budget_exceeded", result.issues)

    def test_23_hypothesis_budget_blocks(self) -> None:
        for suffix in ("2", "3", "4"):
            extra = deepcopy(self.inputs["request"]["candidate_hypotheses"][0])
            extra["hypothesis_id"] = "h-extra-" + suffix
            self.inputs["request"]["candidate_hypotheses"].append(
                seal(extra, HYPOTHESIS_DIGEST_FIELD)
            )
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_hypothesis_budget_exceeded", result.issues)

    def test_24_query_term_budget_blocks(self) -> None:
        self.inputs["policy"]["maximum_query_terms"] = 2
        self.reseal_policy()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("context_request_query_term_budget_exceeded", result.issues)

    def test_25_no_relevant_seed_blocks(self) -> None:
        self.inputs["request"]["initial_query_terms"] = ["zzzznever"]
        self.inputs["request"]["target_symbols"] = ["NeverSymbol"]
        for index, hypothesis in enumerate(self.inputs["request"]["candidate_hypotheses"]):
            hypothesis["query_terms"] = [f"never{index}"]
            hypothesis["expected_symbols"] = [f"NeverExpected{index}"]
            self.inputs["request"]["candidate_hypotheses"][index] = seal(
                hypothesis, HYPOTHESIS_DIGEST_FIELD
            )
        self.reseal_request()
        result = self.build()
        self.assertEqual(result.status, "blocked")
        self.assertIn("no_intent_aligned_context_seed", result.issues)

    def test_26_forbidden_authorities_block(self) -> None:
        for field in (
            "allow_repository_mutation",
            "allow_network_access",
            "allow_secret_access",
            "allow_candidate_selection_authority",
            "allow_execution_authority",
        ):
            with self.subTest(field=field):
                inputs = build_reference_inputs()
                inputs["policy"][field] = True
                inputs["policy"] = seal(inputs["policy"], POLICY_DIGEST_FIELD)
                result = build_intent_aligned_dataflow_context_pack(**inputs)
                self.assertEqual(result.status, "blocked")


if __name__ == "__main__":
    unittest.main()
