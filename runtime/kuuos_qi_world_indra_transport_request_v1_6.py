from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping
import hashlib

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_cross_cycle_blocker_core_v1_5 import (
    build_cross_cycle_blocker_receipt,
    validate_cross_cycle_blocker_receipt,
)
from runtime.kuuos_world_gauge_categorical_indra_net_bridge_core_v0_42 import (
    READY as WORLD_V042_READY,
    REQUIRED_BOUNDARY as WORLD_V042_REQUIRED_BOUNDARY,
    REQUIRED_COMPONENTS as WORLD_V042_REQUIRED_COMPONENTS,
    VERSION as WORLD_V042_VERSION,
    build_world_gauge_categorical_indra_net_bridge,
    plan_digest as world_v042_plan_digest,
)

VERSION = "kuuos_qi_world_indra_transport_request_v1_6"
RECEIPT_VERSION = "kuuos_qi_world_indra_transport_request_receipt_v1_6"
CYCLE_ID = "qi-world-indra-transport-request-v16"

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORLD_V041_FORMAL = (
    REPOSITORY_ROOT
    / "formal/KUOS/WORLD/ModuleCategoryNimrepTubeCenterBridgeV0_41.lean"
)
WORLD_V042_FORMAL = (
    REPOSITORY_ROOT
    / "formal/KUOS/WORLD/GaugeCategoricalIndraNetBridgeV0_42.lean"
)

REQUEST_NON_AUTHORITY = {
    "request_grants_execution": False,
    "request_grants_truth": False,
    "request_issues_authority": False,
    "request_constructs_gauge_connection": False,
    "request_computes_physical_holonomy": False,
    "request_realizes_transport": False,
    "request_updates_exact_world": False,
    "request_collapses_world_branches": False,
    "request_overwrites_history": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def transport_request_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "transport_request_digest")


def transport_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "indra_transport_request_receipt_digest")


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _world_v042_plan(world_model_id: str) -> dict[str, Any]:
    plan = {
        "version": WORLD_V042_VERSION,
        "world_model_id": world_model_id,
        "source_v041_sha256": _file_sha256(WORLD_V041_FORMAL),
        "formal_module_sha256": _file_sha256(WORLD_V042_FORMAL),
        "components": sorted(WORLD_V042_REQUIRED_COMPONENTS),
        "boundary": dict(WORLD_V042_REQUIRED_BOUNDARY),
        "indra_gauge_connection_constructed_by_runtime": False,
        "physical_holonomy_computed_by_runtime": False,
        "ocneanu_flatness_solved_by_runtime": False,
        "bulk_topological_theory_reconstructed_by_runtime": False,
        "world_updated": False,
    }
    plan["plan_digest"] = world_v042_plan_digest(plan)
    return plan


def _source_cross_cycle(blocker_receipt: Mapping[str, Any]) -> dict[str, Any]:
    source = blocker_receipt.get("source_cross_cycle_receipt")
    if not isinstance(source, Mapping):
        raise ValueError("indra_request_cross_cycle_source_missing")
    return deepcopy(dict(source))


def _qi_history(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    qi = source.get("cross_cycle_qi_receipt")
    if not isinstance(qi, Mapping):
        raise ValueError("indra_request_qi_receipt_missing")
    enriched = qi.get("enriched_state")
    if not isinstance(enriched, Mapping):
        raise ValueError("indra_request_qi_enriched_state_missing")
    history = enriched.get("process_history")
    if not isinstance(history, list) or not history:
        raise ValueError("indra_request_qi_history_missing")
    return [deepcopy(dict(item)) for item in history if isinstance(item, Mapping)]


def _expected_source_patch_id(source: Mapping[str, Any]) -> str:
    previous = source.get("previous_cycle_receipt")
    if not isinstance(previous, Mapping):
        raise ValueError("indra_request_previous_cycle_missing")
    previous_projection = str(previous.get("world_projection_digest", ""))
    if not previous_projection:
        raise ValueError("indra_request_previous_world_projection_missing")
    return sha(
        {
            "patch_role": "source",
            "world_projection_digest": previous_projection,
        }
    )


def _expected_target_patch_id(source: Mapping[str, Any]) -> str:
    target_projection = str(source.get("cross_cycle_world_projection_digest", ""))
    if not target_projection:
        raise ValueError("indra_request_target_world_projection_missing")
    return sha(
        {
            "patch_role": "target",
            "world_projection_digest": target_projection,
        }
    )


def _expected_history_digest(source: Mapping[str, Any]) -> str:
    return sha(
        {
            "cross_cycle_receipt_digest": source.get("cross_cycle_receipt_digest"),
            "process_history": _qi_history(source),
        }
    )


def _expected_branch_id(source: Mapping[str, Any]) -> str:
    next_artifacts = source.get("next_cycle_artifacts")
    if not isinstance(next_artifacts, Mapping):
        raise ValueError("indra_request_next_artifacts_missing")
    plan = next_artifacts.get("PlanOS")
    if not isinstance(plan, Mapping):
        raise ValueError("indra_request_next_plan_missing")
    return sha(
        {
            "branch_role": "cross_cycle_candidate",
            "process_lineage_digest": source.get(
                "cross_cycle_process_lineage_digest"
            ),
            "next_plan_state_digest": plan.get("plan_state_digest"),
        }
    )


def _build_transport_request(
    *,
    blocker_receipt: Mapping[str, Any],
    source: Mapping[str, Any],
    world_plan: Mapping[str, Any],
    world_result: Mapping[str, Any],
) -> dict[str, Any]:
    previous = dict(source["previous_cycle_receipt"])
    source_projection = str(previous["world_projection_digest"])
    target_projection = str(source["cross_cycle_world_projection_digest"])
    source_patch = _expected_source_patch_id(source)
    target_patch = _expected_target_patch_id(source)
    history_digest = _expected_history_digest(source)
    branch_id = _expected_branch_id(source)
    request = {
        "version": VERSION,
        "cycle_id": CYCLE_ID,
        "source_cross_cycle_receipt_digest": source["cross_cycle_receipt_digest"],
        "source_blocker_receipt_digest": blocker_receipt[
            "cross_cycle_blocker_receipt_digest"
        ],
        "source_blocker_certificate_digest": blocker_receipt[
            "blocker_certificate"
        ]["blocker_certificate_digest"],
        "world_v042_plan_digest": world_plan["plan_digest"],
        "world_v042_bridge_state_digest": world_result["bridge_state_digest"],
        "source_world_projection_digest": source_projection,
        "target_world_projection_digest": target_projection,
        "source_patch_id": source_patch,
        "target_patch_id": target_patch,
        "patch_path": [source_patch, target_patch],
        "branch_id": branch_id,
        "process_lineage_digest": source[
            "cross_cycle_process_lineage_digest"
        ],
        "history_digest": history_digest,
        "overlap_evidence_request_digest": sha(
            {
                "source_patch_id": source_patch,
                "target_patch_id": target_patch,
                "world_v042_bridge_state_digest": world_result[
                    "bridge_state_digest"
                ],
            }
        ),
        "normal_star_isomorphism_receipt_required": True,
        "pseudofunctor_realization_receipt_required": True,
        "stack_descent_receipt_required": True,
        "branch_transport_receipt_required": True,
        "coherence_two_cell_receipt_required": True,
        "history_dependent_phase_receipt_required": True,
        "continuum_nonmarkov_connection_receipt_required": True,
        "analytic_transport_external": True,
        "request_only": True,
        "transport_realized": False,
        "gauge_connection_constructed": False,
        "physical_holonomy_computed": False,
        "exact_world_identity_asserted": False,
        "world_updated": False,
        "branch_collapsed": False,
        "history_overwritten": False,
        "candidate_only": True,
        "nonfinal_marker": True,
        "branch_preserving_required": True,
        "history_dependent_phase_required": True,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "transport_request_digest": "",
    }
    request["transport_request_digest"] = transport_request_digest(request)
    return request


def build_indra_transport_request_receipt(root: Path) -> dict[str, Any]:
    blocker_receipt = build_cross_cycle_blocker_receipt(root / "blocker-v15")
    blocker_errors = validate_cross_cycle_blocker_receipt(blocker_receipt)
    if blocker_errors:
        raise ValueError(
            "indra_request_blocker_source_invalid:" + ";".join(blocker_errors)
        )
    source = _source_cross_cycle(blocker_receipt)
    world_model_id = sha(
        {
            "source_world_projection_digest": source[
                "previous_cycle_receipt"
            ]["world_projection_digest"],
            "target_world_projection_digest": source[
                "cross_cycle_world_projection_digest"
            ],
            "process_lineage_digest": source[
                "cross_cycle_process_lineage_digest"
            ],
        }
    )
    world_plan = _world_v042_plan(world_model_id)
    result = build_world_gauge_categorical_indra_net_bridge(world_plan)
    world_result = result.to_dict()
    if result.status != WORLD_V042_READY:
        raise ValueError(
            "indra_request_world_v042_not_ready:" + ";".join(result.blockers)
        )
    request = _build_transport_request(
        blocker_receipt=blocker_receipt,
        source=source,
        world_plan=world_plan,
        world_result=world_result,
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "source_cross_cycle_blocker_receipt": deepcopy(blocker_receipt),
        "source_cross_cycle_blocker_receipt_digest": blocker_receipt[
            "cross_cycle_blocker_receipt_digest"
        ],
        "world_v042_plan": deepcopy(world_plan),
        "world_v042_result": deepcopy(world_result),
        "transport_request": request,
        "disposition": "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED",
        "all_cross_cycle_blockers_active": True,
        "world_v042_sidecar_ready": True,
        "runtime_transport_realized": False,
        "exact_world_updated": False,
        "request_non_authority": deepcopy(REQUEST_NON_AUTHORITY),
        "indra_transport_request_receipt_digest": "",
    }
    receipt["indra_transport_request_receipt_digest"] = transport_receipt_digest(
        receipt
    )
    errors = validate_indra_transport_request_receipt(receipt)
    if errors:
        raise ValueError("indra_transport_request_invalid:" + ";".join(errors))
    return receipt


def validate_indra_transport_request_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == RECEIPT_VERSION, "indra_request_version_invalid")
        require(
            receipt.get("indra_transport_request_receipt_digest")
            == transport_receipt_digest(receipt),
            "indra_request_receipt_digest_invalid",
        )
        blocker_receipt = dict(
            receipt.get("source_cross_cycle_blocker_receipt", {})
        )
        errors.extend(
            "indra_request_source_" + error
            for error in validate_cross_cycle_blocker_receipt(blocker_receipt)
        )
        require(
            receipt.get("source_cross_cycle_blocker_receipt_digest")
            == blocker_receipt.get("cross_cycle_blocker_receipt_digest"),
            "indra_request_source_blocker_digest_mismatch",
        )
        require(
            blocker_receipt.get("all_required_blockers_active") is True,
            "indra_request_blockers_not_all_active",
        )
        require(
            blocker_receipt.get("unlicensed_transition_blocked") is True,
            "indra_request_unlicensed_transition_not_blocked",
        )
        source = _source_cross_cycle(blocker_receipt)

        world_plan = dict(receipt.get("world_v042_plan", {}))
        require(
            world_plan.get("version") == WORLD_V042_VERSION,
            "indra_request_world_plan_version_invalid",
        )
        require(
            world_plan.get("plan_digest") == world_v042_plan_digest(world_plan),
            "indra_request_world_plan_digest_invalid",
        )
        expected_world_result = build_world_gauge_categorical_indra_net_bridge(
            world_plan
        ).to_dict()
        world_result = dict(receipt.get("world_v042_result", {}))
        require(
            world_result == expected_world_result,
            "indra_request_world_result_invalid",
        )
        require(
            world_result.get("status") == WORLD_V042_READY,
            "indra_request_world_sidecar_not_ready",
        )
        require(
            bool(world_result.get("bridge_state_digest")),
            "indra_request_world_bridge_state_missing",
        )

        request = dict(receipt.get("transport_request", {}))
        require(request.get("version") == VERSION, "indra_request_payload_version_invalid")
        require(
            request.get("transport_request_digest")
            == transport_request_digest(request),
            "indra_request_payload_digest_invalid",
        )
        require(
            request.get("source_cross_cycle_receipt_digest")
            == source.get("cross_cycle_receipt_digest"),
            "indra_request_cross_cycle_binding_invalid",
        )
        require(
            request.get("source_blocker_receipt_digest")
            == blocker_receipt.get("cross_cycle_blocker_receipt_digest"),
            "indra_request_blocker_binding_invalid",
        )
        require(
            request.get("source_blocker_certificate_digest")
            == blocker_receipt.get("blocker_certificate", {}).get(
                "blocker_certificate_digest"
            ),
            "indra_request_blocker_certificate_binding_invalid",
        )
        require(
            request.get("world_v042_plan_digest") == world_plan.get("plan_digest"),
            "indra_request_world_plan_binding_invalid",
        )
        require(
            request.get("world_v042_bridge_state_digest")
            == world_result.get("bridge_state_digest"),
            "indra_request_world_result_binding_invalid",
        )

        previous = dict(source.get("previous_cycle_receipt", {}))
        require(
            request.get("source_world_projection_digest")
            == previous.get("world_projection_digest"),
            "indra_request_source_projection_mismatch",
        )
        require(
            request.get("target_world_projection_digest")
            == source.get("cross_cycle_world_projection_digest"),
            "indra_request_target_projection_mismatch",
        )
        expected_source_patch = _expected_source_patch_id(source)
        expected_target_patch = _expected_target_patch_id(source)
        require(
            request.get("source_patch_id") == expected_source_patch,
            "indra_request_source_patch_invalid",
        )
        require(
            request.get("target_patch_id") == expected_target_patch,
            "indra_request_target_patch_invalid",
        )
        require(
            request.get("patch_path")
            == [expected_source_patch, expected_target_patch],
            "indra_request_patch_path_invalid",
        )
        require(
            expected_source_patch != expected_target_patch,
            "indra_request_patch_transition_degenerate",
        )
        require(
            request.get("branch_id") == _expected_branch_id(source),
            "indra_request_branch_id_invalid",
        )
        require(
            request.get("process_lineage_digest")
            == source.get("cross_cycle_process_lineage_digest"),
            "indra_request_process_lineage_mismatch",
        )
        require(
            request.get("history_digest") == _expected_history_digest(source),
            "indra_request_history_digest_invalid",
        )

        for key in (
            "normal_star_isomorphism_receipt_required",
            "pseudofunctor_realization_receipt_required",
            "stack_descent_receipt_required",
            "branch_transport_receipt_required",
            "coherence_two_cell_receipt_required",
            "history_dependent_phase_receipt_required",
            "continuum_nonmarkov_connection_receipt_required",
            "analytic_transport_external",
            "request_only",
            "candidate_only",
            "nonfinal_marker",
            "branch_preserving_required",
            "history_dependent_phase_required",
            "multi_world_noncollapse",
            "two_truths_gap",
        ):
            require(request.get(key) is True, f"indra_request_{key}_invalid")
        for key in (
            "transport_realized",
            "gauge_connection_constructed",
            "physical_holonomy_computed",
            "exact_world_identity_asserted",
            "world_updated",
            "branch_collapsed",
            "history_overwritten",
        ):
            require(request.get(key) is False, f"indra_request_{key}_forbidden")

        require(
            receipt.get("disposition")
            == "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED",
            "indra_request_disposition_invalid",
        )
        require(
            receipt.get("all_cross_cycle_blockers_active") is True,
            "indra_request_all_blockers_flag_invalid",
        )
        require(
            receipt.get("world_v042_sidecar_ready") is True,
            "indra_request_world_ready_flag_invalid",
        )
        require(
            receipt.get("runtime_transport_realized") is False,
            "indra_request_runtime_transport_realized_forbidden",
        )
        require(
            receipt.get("exact_world_updated") is False,
            "indra_request_exact_world_update_forbidden",
        )
        require(
            dict(receipt.get("request_non_authority", {}))
            == REQUEST_NON_AUTHORITY,
            "indra_request_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
