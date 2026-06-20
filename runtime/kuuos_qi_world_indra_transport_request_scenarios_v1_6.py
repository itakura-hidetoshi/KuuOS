from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_indra_transport_request_v1_6 import (
    build_indra_transport_request_receipt,
    transport_receipt_digest,
    transport_request_digest,
    validate_indra_transport_request_receipt,
)
from runtime.kuuos_world_gauge_categorical_indra_net_bridge_core_v0_42 import (
    build_world_gauge_categorical_indra_net_bridge,
    plan_digest as world_v042_plan_digest,
)


def _retag_request(receipt: dict) -> None:
    request = receipt["transport_request"]
    request["transport_request_digest"] = ""
    request["transport_request_digest"] = transport_request_digest(request)


def _retag_receipt(receipt: dict) -> dict:
    receipt["indra_transport_request_receipt_digest"] = ""
    receipt["indra_transport_request_receipt_digest"] = transport_receipt_digest(
        receipt
    )
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_indra_transport_request_receipt(_retag_receipt(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_indra_transport_request_scenarios() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-indra-request-v16-") as temporary:
        receipt = build_indra_transport_request_receipt(Path(temporary))
        assert validate_indra_transport_request_receipt(receipt) == []
        request = receipt["transport_request"]
        world_result = receipt["world_v042_result"]

        assert receipt["all_cross_cycle_blockers_active"] is True
        assert receipt["world_v042_sidecar_ready"] is True
        assert receipt["runtime_transport_realized"] is False
        assert request["source_patch_id"] != request["target_patch_id"]
        assert request["patch_path"] == [
            request["source_patch_id"],
            request["target_patch_id"],
        ]
        assert request["analytic_transport_external"] is True
        assert request["transport_realized"] is False
        assert world_result["decision"] == "ready"

        target_substitution = deepcopy(receipt)
        target_substitution["transport_request"][
            "target_world_projection_digest"
        ] = sha("substituted-target-projection")
        _retag_request(target_substitution)
        _require_error(
            target_substitution,
            "indra_request_target_projection_mismatch",
        )

        patch_substitution = deepcopy(receipt)
        patch_substitution["transport_request"]["target_patch_id"] = sha(
            "substituted-target-patch"
        )
        patch_substitution["transport_request"]["patch_path"][1] = patch_substitution[
            "transport_request"
        ]["target_patch_id"]
        _retag_request(patch_substitution)
        _require_error(patch_substitution, "indra_request_target_patch_invalid")

        branch_substitution = deepcopy(receipt)
        branch_substitution["transport_request"]["branch_id"] = sha(
            "substituted-branch"
        )
        _retag_request(branch_substitution)
        _require_error(branch_substitution, "indra_request_branch_id_invalid")

        history_substitution = deepcopy(receipt)
        history_substitution["transport_request"]["history_digest"] = sha(
            "substituted-history"
        )
        _retag_request(history_substitution)
        _require_error(history_substitution, "indra_request_history_digest_invalid")

        transport_forgery = deepcopy(receipt)
        transport_forgery["transport_request"]["transport_realized"] = True
        _retag_request(transport_forgery)
        _require_error(
            transport_forgery,
            "indra_request_transport_realized_forbidden",
        )

        gauge_forgery = deepcopy(receipt)
        gauge_forgery["transport_request"][
            "gauge_connection_constructed"
        ] = True
        _retag_request(gauge_forgery)
        _require_error(
            gauge_forgery,
            "indra_request_gauge_connection_constructed_forbidden",
        )

        holonomy_forgery = deepcopy(receipt)
        holonomy_forgery["transport_request"][
            "physical_holonomy_computed"
        ] = True
        _retag_request(holonomy_forgery)
        _require_error(
            holonomy_forgery,
            "indra_request_physical_holonomy_computed_forbidden",
        )

        world_identity_forgery = deepcopy(receipt)
        world_identity_forgery["transport_request"][
            "exact_world_identity_asserted"
        ] = True
        _retag_request(world_identity_forgery)
        _require_error(
            world_identity_forgery,
            "indra_request_exact_world_identity_asserted_forbidden",
        )

        blocker_flag_loss = deepcopy(receipt)
        blocker_flag_loss["all_cross_cycle_blockers_active"] = False
        _require_error(
            blocker_flag_loss,
            "indra_request_all_blockers_flag_invalid",
        )

        world_plan_mutation = deepcopy(receipt)
        world_plan_mutation["world_v042_plan"]["world_updated"] = True
        world_plan_mutation["world_v042_plan"]["plan_digest"] = world_v042_plan_digest(
            world_plan_mutation["world_v042_plan"]
        )
        world_plan_mutation["world_v042_result"] = (
            build_world_gauge_categorical_indra_net_bridge(
                world_plan_mutation["world_v042_plan"]
            ).to_dict()
        )
        _require_error(
            world_plan_mutation,
            "indra_request_world_sidecar_not_ready",
        )

        request_only_loss = deepcopy(receipt)
        request_only_loss["transport_request"]["request_only"] = False
        _retag_request(request_only_loss)
        _require_error(request_only_loss, "indra_request_request_only_invalid")

        return {
            "status": "KUUOS_QI_WORLD_INDRA_TRANSPORT_REQUEST_V1_6_OK",
            "source_patch_id": request["source_patch_id"],
            "target_patch_id": request["target_patch_id"],
            "branch_id": request["branch_id"],
            "history_digest": request["history_digest"],
            "world_v042_bridge_state_digest": request[
                "world_v042_bridge_state_digest"
            ],
            "blocker_certificate_digest": request[
                "source_blocker_certificate_digest"
            ],
            "disposition": receipt["disposition"],
            "runtime_transport_realized": receipt[
                "runtime_transport_realized"
            ],
            "request_non_authority": receipt["request_non_authority"],
        }
