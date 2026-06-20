from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_indra_transport_receipt_intake_v1_7 import (
    REQUIRED_RECEIPT_KINDS,
    build_fixture_indra_transport_receipt_intake,
    external_receipt_digest,
    intake_receipt_digest,
    validate_indra_transport_receipt_intake,
)


def _retag_external(receipt: dict) -> None:
    receipt["external_analytic_receipt_digest"] = ""
    receipt["external_analytic_receipt_digest"] = external_receipt_digest(
        receipt
    )


def _retag_intake(intake: dict) -> dict:
    intake["indra_transport_receipt_intake_digest"] = ""
    intake["indra_transport_receipt_intake_digest"] = intake_receipt_digest(
        intake
    )
    return intake


def _require_error(intake: dict, expected_fragment: str) -> None:
    errors = validate_indra_transport_receipt_intake(_retag_intake(intake))
    if not any(expected_fragment in error for error in errors):
        raise AssertionError({"expected": expected_fragment, "errors": errors})


def run_indra_transport_receipt_intake_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-indra-intake-v17-") as temporary:
        intake = build_fixture_indra_transport_receipt_intake(Path(temporary))
        assert validate_indra_transport_receipt_intake(intake) == []
        receipts = intake["external_receipts"]
        assert [item["receipt_kind"] for item in receipts] == list(
            REQUIRED_RECEIPT_KINDS
        )
        assert all(item["fixture_only"] is True for item in receipts)
        assert intake["semantic_review_required"] is True
        assert intake["runtime_transport_realized"] is False

        missing = deepcopy(intake)
        missing["external_receipts"] = missing["external_receipts"][:-1]
        missing["receipt_kinds"] = [
            item["receipt_kind"] for item in missing["external_receipts"]
        ]
        missing["all_required_receipts_present"] = False
        _require_error(missing, "indra_intake_required_receipt_missing")

        reordered = deepcopy(intake)
        reordered["external_receipts"][1], reordered["external_receipts"][2] = (
            reordered["external_receipts"][2],
            reordered["external_receipts"][1],
        )
        reordered["receipt_kinds"] = [
            item["receipt_kind"] for item in reordered["external_receipts"]
        ]
        _require_error(reordered, "indra_intake_receipt_kind_order_invalid")

        wrong_request = deepcopy(intake)
        target = wrong_request["external_receipts"][0]
        target["source_transport_request_digest"] = sha("wrong-request")
        _retag_external(target)
        _require_error(wrong_request, "indra_external_request_binding_invalid")

        wrong_patch = deepcopy(intake)
        target = wrong_patch["external_receipts"][3]
        target["target_patch_id"] = sha("wrong-target-patch")
        target["patch_path"] = [target["source_patch_id"], target["target_patch_id"]]
        _retag_external(target)
        _require_error(wrong_patch, "target_patch_id_binding_invalid")

        wrong_branch = deepcopy(intake)
        target = wrong_branch["external_receipts"][4]
        target["branch_id"] = sha("wrong-branch")
        _retag_external(target)
        _require_error(wrong_branch, "branch_id_binding_invalid")

        wrong_history = deepcopy(intake)
        target = wrong_history["external_receipts"][5]
        target["history_digest"] = sha("wrong-history")
        _retag_external(target)
        _require_error(wrong_history, "history_digest_binding_invalid")

        dependency_mutation = deepcopy(intake)
        target = dependency_mutation["external_receipts"][4]
        target["dependency_receipt_digests"] = [sha("wrong-dependency")]
        _retag_external(target)
        _require_error(
            dependency_mutation,
            "COHERENCE_TWO_CELL_dependency_invalid",
        )

        proof_missing = deepcopy(intake)
        target = proof_missing["external_receipts"][2]
        target["proof_object_digest"] = ""
        _retag_external(target)
        _require_error(proof_missing, "indra_external_proof_object_missing")

        runtime_semantic_claim = deepcopy(intake)
        target = runtime_semantic_claim["external_receipts"][6]
        target["semantic_validity_asserted_by_runtime"] = True
        _retag_external(target)
        _require_error(
            runtime_semantic_claim,
            "semantic_validity_asserted_by_runtime_forbidden",
        )

        world_update = deepcopy(intake)
        target = world_update["external_receipts"][3]
        target["world_updated"] = True
        _retag_external(target)
        _require_error(world_update, "world_updated_forbidden")

        physical_holonomy = deepcopy(intake)
        target = physical_holonomy["external_receipts"][1]
        target["physical_holonomy_computed_by_runtime"] = True
        _retag_external(target)
        _require_error(
            physical_holonomy,
            "physical_holonomy_computed_by_runtime_forbidden",
        )

        intake_realization = deepcopy(intake)
        intake_realization["runtime_transport_realized"] = True
        _require_error(
            intake_realization,
            "indra_intake_runtime_transport_realized_forbidden",
        )

        return {
            "status": "KUUOS_QI_WORLD_INDRA_RECEIPT_INTAKE_V1_7_OK",
            "receipt_count": len(receipts),
            "receipt_kinds": list(intake["receipt_kinds"]),
            "receipt_set_digest": intake["receipt_set_digest"],
            "source_request_receipt_digest": intake[
                "source_request_receipt_digest"
            ],
            "disposition": intake["disposition"],
            "semantic_review_required": intake[
                "semantic_review_required"
            ],
            "runtime_transport_realized": intake[
                "runtime_transport_realized"
            ],
            "intake_non_authority": intake["intake_non_authority"],
        }
