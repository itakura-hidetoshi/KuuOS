from copy import deepcopy
import unittest

from runtime.kuuos_codeai_frozen_cohort_prediction_pack_execution_shard_contract_v0_1 import (
    COHORTS,
    TARGET,
    build_contract,
    digest,
    validate_contract,
)


def reseal(contract: dict) -> None:
    contract["contract_digest"] = digest(
        {key: value for key, value in contract.items() if key != "contract_digest"}
    )


class FrozenCohortContractTests(unittest.TestCase):
    def test_reference_admitted_not_ready(self):
        result = validate_contract(build_contract())
        self.assertTrue(result.admitted)
        self.assertFalse(result.ready)

    def test_five_cohorts(self):
        self.assertEqual(
            tuple(item["cohort"] for item in build_contract()["cohorts"]),
            COHORTS,
        )

    def test_100_unique_opaque_slots(self):
        slots = build_contract()["opaque_slot_digests"]
        self.assertEqual(len(slots), TARGET)
        self.assertEqual(len(set(slots)), TARGET)

    def test_50_shards(self):
        self.assertEqual(len(build_contract()["execution_shards"]), 50)

    def test_smoke_excluded(self):
        pack = next(
            pack
            for pack in build_contract()["prediction_packs"]
            if pack["cohort"] == "codeai-full"
        )
        self.assertEqual(pack["smoke_predictions"], 1)
        self.assertFalse(pack["smoke_counts_as_performance"])

    def test_no_execution_authority(self):
        contract = build_contract()
        self.assertFalse(contract["external_execution_authority"])
        self.assertFalse(contract["kernel_execution_authority"])

    def test_no_claims(self):
        contract = build_contract()
        self.assertFalse(contract["correctness_claimed"])
        self.assertFalse(contract["performance_claimed"])

    def test_tamper_blocked(self):
        contract = build_contract()
        contract["decision"] = "tampered"
        self.assertFalse(validate_contract(contract).admitted)

    def test_label_relabeling_blocked(self):
        contract = build_contract()
        contract["prediction_packs"][0]["label_only_relabeling"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_smoke_promotion_blocked(self):
        contract = build_contract()
        contract["prediction_packs"][1]["smoke_counts_as_performance"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_gold_derived_blocked(self):
        contract = build_contract()
        contract["prediction_packs"][0]["gold_derived"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_raw_test_names_blocked(self):
        contract = build_contract()
        contract["prediction_packs"][0]["raw_test_names"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_kernel_shard_blocked(self):
        contract = build_contract()
        contract["execution_shards"][0]["external_harness_only"] = False
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_shard_gap_blocked(self):
        contract = build_contract()
        contract["execution_shards"][0]["start_slot"] = 1
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_repository_authority_blocked(self):
        contract = build_contract()
        contract["repository_mutation_authority"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)

    def test_performance_claim_blocked(self):
        contract = build_contract()
        contract["performance_claimed"] = True
        reseal(contract)
        self.assertFalse(validate_contract(contract).admitted)


if __name__ == "__main__":
    unittest.main()
