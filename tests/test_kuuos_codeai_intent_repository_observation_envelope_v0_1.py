from copy import deepcopy
import unittest

import runtime.kuuos_codeai_intent_repository_observation_envelope_v0_1 as m
from scripts.check_codeai_intent_repository_observation_envelope_v0_1 import (
    load_example,
    main as run_route_checker,
)


class CodeAIIntentRepositoryObservationEnvelopeV01Test(unittest.TestCase):
    def setUp(self):
        self.example = load_example()

    def build(self):
        return m.build_codeai_intent_repository_observation_envelope(
            intent_packet=self.example["intent_packet"],
            repository_observation=self.example["repository_observation"],
            observation_policy=self.example["observation_policy"],
        )

    def test_supported_example_is_read_only(self):
        result = self.build()
        self.assertEqual(m.STATUS_READY, result.status)
        self.assertEqual((), result.issues)
        self.assertIsNotNone(result.receipt)
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(m.DISPOSITION_SUPPORTED, receipt["codeai_disposition"])
        self.assertEqual(m.MODE_READ_ONLY, receipt["operating_mode"])
        self.assertTrue(receipt["codeai_profile_ready"])
        self.assertFalse(receipt["repository_mutation_performed"])
        self.assertFalse(receipt["execution_lease_issued"])

    def test_receipt_binds_exact_source_commit_and_path_partition(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        self.assertEqual(receipt["source_commit_sha"], receipt["resulting_commit_sha"])
        self.assertEqual(
            receipt["declared_path_count"],
            receipt["observed_path_count"] + receipt["unavailable_path_count"],
        )
        self.assertEqual(
            receipt[m.RECEIPT_DIGEST_FIELD],
            m.digest_without(receipt, m.RECEIPT_DIGEST_FIELD),
        )

    def test_receipt_grants_no_successor_authority(self):
        result = self.build()
        receipt = result.receipt
        assert receipt is not None
        for field in (
            "selection_authority_granted",
            "execution_authority_granted",
            "merge_authority_granted",
            "deployment_authority_granted",
            "secret_access_authority_granted",
        ):
            self.assertFalse(receipt[field], field)

    def test_tampered_example_fails_closed(self):
        intent = deepcopy(self.example["intent_packet"])
        intent["success_criteria"].append("unsealed criterion")
        result = m.build_codeai_intent_repository_observation_envelope(
            intent_packet=intent,
            repository_observation=self.example["repository_observation"],
            observation_policy=self.example["observation_policy"],
        )
        self.assertEqual(m.STATUS_BLOCKED, result.status)
        self.assertIsNone(result.receipt)
        self.assertIn("intent_packet_digest_mismatch", result.issues)

    def test_all_disposition_routes(self):
        run_route_checker()


if __name__ == "__main__":
    unittest.main()
