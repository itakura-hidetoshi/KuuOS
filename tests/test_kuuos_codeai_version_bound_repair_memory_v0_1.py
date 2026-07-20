from __future__ import annotations

import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    MEMORY_SNAPSHOT_DIGEST_FIELD,
    OUTCOME_VERIFIED_EFFECTIVE,
    POLICY_DIGEST_FIELD,
    RECOMMENDATION_HINT_AVAILABLE,
    RECOMMENDATION_NO_HINT,
    RECEIPT_DIGEST_FIELD,
    REPAIR_PACKET_DIGEST_FIELD,
    REPAIR_RECORD_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    VERSION_BINDING_FIELDS,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_version_bound_repair_memory_v0_1 import (
    build_codeai_version_bound_repair_memory,
)
from scripts.build_codeai_version_bound_repair_memory_fixture_v0_1 import (
    build_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    def load(path: str) -> dict:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    return build_fixture(
        load("examples/codeai_version_bound_repair_memory_v0_1.json"),
        load("examples/codeai_typed_error_classification_v0_1.json"),
        load("examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json"),
        load("examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"),
    )


def run(data: dict):
    return build_codeai_version_bound_repair_memory(
        source_classification=data["source_classification"],
        source_classification_receipt=data["source_classification_receipt"],
        repair_evidence_packet=data["repair_evidence_packet"],
        memory_request=data["memory_request"],
        memory_policy=data["memory_policy"],
    )


def reseal_request(data: dict) -> None:
    data["memory_request"] = seal(data["memory_request"], REQUEST_DIGEST_FIELD)


def reseal_policy(data: dict) -> None:
    data["memory_policy"] = seal(data["memory_policy"], POLICY_DIGEST_FIELD)


def reseal_packet(data: dict) -> None:
    packet = seal(data["repair_evidence_packet"], REPAIR_PACKET_DIGEST_FIELD)
    data["repair_evidence_packet"] = packet
    data["memory_request"]["repair_evidence_packet_digest"] = packet[
        REPAIR_PACKET_DIGEST_FIELD
    ]
    data["memory_policy"]["expected_repair_evidence_packet_digest"] = packet[
        REPAIR_PACKET_DIGEST_FIELD
    ]
    reseal_request(data)
    reseal_policy(data)


def reseal_record(data: dict, index: int = 0) -> None:
    record = data["repair_evidence_packet"]["records"][index]
    data["repair_evidence_packet"]["records"][index] = seal(
        record, REPAIR_RECORD_DIGEST_FIELD
    )
    reseal_packet(data)


def binding_for_record(data: dict, index: int) -> dict:
    classification = data["source_classification"]
    record = data["repair_evidence_packet"]["records"][index]
    return {
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_repository_snapshot_digest": classification[
            "source_repository_snapshot_digest"
        ],
        "source_candidate_digest": record["source_candidate_digest"],
        "typed_error_digest": record["typed_error_digest"],
        "error_fingerprint": record["error_fingerprint"],
        "classification_schema_version": classification["schema_version"],
        "toolchain_digest": record["toolchain_digest"],
        "dependency_manifest_digest": record["dependency_manifest_digest"],
        "repair_policy_digest": record["repair_policy_digest"],
    }


def bind_query(data: dict, binding: dict) -> None:
    for field in VERSION_BINDING_FIELDS:
        data["memory_request"][field] = binding[field]
        data["memory_policy"]["expected_" + field] = binding[field]
    reseal_request(data)
    reseal_policy(data)


class VersionBoundRepairMemoryTests(unittest.TestCase):
    def test_reference_exact_match(self):
        result = run(fixture())
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.snapshot["memory_entry_count"], 4)
        self.assertEqual(result.snapshot["matched_entry_count"], 1)
        self.assertEqual(result.snapshot["excluded_entry_count"], 3)
        self.assertEqual(
            result.snapshot["recommendation"], RECOMMENDATION_HINT_AVAILABLE
        )

    def test_deterministic_and_sealed(self):
        data = fixture()
        left = run(data)
        right = run(data)
        self.assertEqual(left.snapshot, right.snapshot)
        self.assertEqual(
            left.snapshot[MEMORY_SNAPSHOT_DIGEST_FIELD],
            seal(left.snapshot, MEMORY_SNAPSHOT_DIGEST_FIELD)[
                MEMORY_SNAPSHOT_DIGEST_FIELD
            ],
        )
        self.assertEqual(
            left.receipt[RECEIPT_DIGEST_FIELD],
            seal(left.receipt, RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD],
        )

    def test_legacy_toolchain_is_excluded(self):
        snapshot = run(fixture()).snapshot
        legacy = snapshot["memory_entries"][-1]
        self.assertNotEqual(
            legacy["toolchain_digest"],
            snapshot["query_version_binding"]["toolchain_digest"],
        )
        exclusion = next(
            item
            for item in snapshot["excluded_entries"]
            if item["memory_entry_digest"] == legacy[
                "codeai_version_bound_repair_memory_entry_digest"
            ]
        )
        self.assertIn("version_binding_mismatch:toolchain_digest", exclusion["reasons"])

    def test_unknown_toolchain_returns_no_hint(self):
        data = fixture()
        binding = dict(data["memory_request"])
        binding["toolchain_digest"] = canonical_digest({"toolchain": "unknown"})
        bind_query(data, binding)
        result = run(data)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.snapshot["matched_entry_count"], 0)
        self.assertEqual(result.snapshot["recommendation"], RECOMMENDATION_NO_HINT)

    def test_verified_ineffective_query_returns_no_hint(self):
        data = fixture()
        bind_query(data, binding_for_record(data, 2))
        result = run(data)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.snapshot["matched_entry_count"], 0)
        self.assertEqual(result.snapshot["recommendation"], RECOMMENDATION_NO_HINT)

    def test_policy_can_observe_ineffective_history_without_authority(self):
        data = fixture()
        bind_query(data, binding_for_record(data, 2))
        data["memory_policy"]["allowed_repair_outcomes"] = [
            OUTCOME_VERIFIED_EFFECTIVE,
            "verified_ineffective",
        ]
        reseal_policy(data)
        result = run(data)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.snapshot["matched_entry_count"], 1)
        self.assertFalse(result.snapshot["repair_authority_granted"])

    def test_memory_has_no_downstream_authority_or_effect(self):
        snapshot = run(fixture()).snapshot
        self.assertTrue(snapshot["history_read_only"])
        for field in (
            "repair_executed_by_memory",
            "repository_mutation_performed_by_memory",
            "git_effect_performed_by_memory",
            "repair_authority_granted",
            "verification_authority_granted",
            "execution_authority_granted",
            "git_authority_granted",
            "historical_outcome_treated_as_probability",
            "historical_success_treated_as_future_success_proof",
            "memory_hint_treated_as_correctness_proof",
            "version_mismatch_treated_as_transferable",
        ):
            self.assertFalse(snapshot[field], field)

    def test_stale_and_future_windows_block(self):
        for container, field, resealer in (
            ("memory_request", "request_created_epoch", reseal_request),
            ("repair_evidence_packet", "evidence_created_epoch", reseal_packet),
        ):
            with self.subTest(container=container, mode="stale"):
                data = fixture()
                data[container][field] = 1
                resealer(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)
            with self.subTest(container=container, mode="future"):
                data = fixture()
                data[container][field] = data["memory_policy"]["evaluation_epoch"] + 1
                resealer(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_role_collisions_block(self):
        cases = (
            ("independent_verifier_id", "repair_producer_id"),
            ("memory_curator_id", "repair_producer_id"),
            ("memory_curator_id", "independent_verifier_id"),
        )
        for target, source in cases:
            with self.subTest(target=target, source=source):
                data = fixture()
                data["repair_evidence_packet"][target] = data[
                    "repair_evidence_packet"
                ][source]
                reseal_packet(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_record_correspondence_mismatch_blocks(self):
        data = fixture()
        data["repair_evidence_packet"]["records"][0]["error_fingerprint"] += "X"
        reseal_record(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_live_mutation_and_git_effect_block(self):
        for field in ("live_repository_mutation", "git_effect"):
            with self.subTest(field=field):
                data = fixture()
                data["repair_evidence_packet"]["records"][0][field] = True
                reseal_record(data)
                self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_budgets_block(self):
        data = fixture()
        data["memory_policy"]["maximum_memory_entries"] = 1
        reseal_policy(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

        data = fixture()
        data["memory_policy"]["maximum_matched_entries"] = 1
        duplicate = dict(data["repair_evidence_packet"]["records"][0])
        duplicate["repair_record_id"] = "repair-record-current-duplicate"
        duplicate = seal(duplicate, REPAIR_RECORD_DIGEST_FIELD)
        data["repair_evidence_packet"]["records"].append(duplicate)
        data["repair_evidence_packet"]["record_count"] += 1
        reseal_packet(data)
        self.assertEqual(run(data).status, STATUS_BLOCKED)

    def test_source_digest_tampering_blocks(self):
        data = fixture()
        data["source_classification"]["typed_error_count"] = 99
        self.assertEqual(run(data).status, STATUS_BLOCKED)


def _install_dynamic_tests() -> None:
    mapping_inputs = (
        "source_classification",
        "source_classification_receipt",
        "repair_evidence_packet",
        "memory_request",
        "memory_policy",
    )
    for field in mapping_inputs:
        def test(self, field=field):
            data = fixture()
            data[field] = []
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_non_mapping_{field}_blocks", test)

    digest_cases = (
        ("memory_request", "memory_request_id", "tampered"),
        ("memory_policy", "maximum_memory_entries", 999),
        ("repair_evidence_packet", "record_count", 999),
        ("source_classification", "candidate_count", 999),
        ("source_classification_receipt", "candidate_count", 999),
    )
    for container, field, value in digest_cases:
        def test(self, container=container, field=field, value=value):
            data = fixture()
            data[container][field] = value
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(
            VersionBoundRepairMemoryTests,
            f"test_tampered_{container}_{field}_blocks",
            test,
        )

    required_policy = (
        "require_exact_version_binding",
        "require_complete_typed_error_correspondence",
        "require_independent_verification",
        "require_isolated_candidate_repair",
        "require_live_repository_unchanged",
        "allow_memory_hint",
    )
    for field in required_policy:
        def test(self, field=field):
            data = fixture()
            data["memory_policy"][field] = False
            reseal_policy(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_required_{field}_blocks", test)

    forbidden_policy = (
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    for field in forbidden_policy:
        def test(self, field=field):
            data = fixture()
            data["memory_policy"][field] = True
            reseal_policy(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_forbidden_{field}_blocks", test)

    packet_required_true = (
        "external_repair_execution_reported",
        "independent_verification_verified",
        "isolated_candidate_repair_verified",
        "live_repository_unchanged",
    )
    for field in packet_required_true:
        def test(self, field=field):
            data = fixture()
            data["repair_evidence_packet"][field] = False
            reseal_packet(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_packet_{field}_false_blocks", test)

    record_required_true = (
        "completed",
        "external_repair_execution",
        "independent_verification",
        "isolated_candidate_repair",
    )
    for field in record_required_true:
        def test(self, field=field):
            data = fixture()
            data["repair_evidence_packet"]["records"][0][field] = False
            reseal_record(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_record_{field}_false_blocks", test)

    claims = (
        "claims_repair_authority",
        "claims_execution_authority",
        "claims_git_authority",
    )
    for field in claims:
        def test(self, field=field):
            data = fixture()
            data["memory_request"][field] = True
            reseal_request(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(VersionBoundRepairMemoryTests, f"test_request_{field}_blocks", test)

    for field in VERSION_BINDING_FIELDS:
        def test(self, field=field):
            data = fixture()
            if field == "source_commit_sha":
                replacement = "f" * 40
            elif field in {
                "repository_full_name",
                "error_fingerprint",
                "classification_schema_version",
            }:
                replacement = str(data["memory_request"][field]) + "-mismatch"
            else:
                replacement = canonical_digest({"mismatch": field})
            data["memory_policy"]["expected_" + field] = replacement
            reseal_policy(data)
            self.assertEqual(run(data).status, STATUS_BLOCKED)
        setattr(
            VersionBoundRepairMemoryTests,
            f"test_request_policy_binding_mismatch_{field}_blocks",
            test,
        )


_install_dynamic_tests()


if __name__ == "__main__":
    unittest.main()
