from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_decision_os_wa_kernel_v0_3 import build_replan_wa_activation_receipt
from runtime.kuuos_decision_os_wa_state_v0_3 import validate_wa_state
from runtime.kuuos_plan_os_kernel_v0_1 import build_initial_plan_state
from runtime.kuuos_plan_os_replan_kernel_v0_2 import validate_replan_state
from runtime.kuuos_plan_os_replan_types_v0_2 import (
    REPLAN_PHASE_RECEIPT_VERSION,
    replan_phase_receipt_digest,
)
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
    ACTIVATION_RECEIPT_VERSION,
    COMPILER_RECEIPT_VERSION,
    MATERIALIZATION_PACKET_VERSION,
    NON_AUTHORITY_FLAGS,
    ROUTE_PROJECTION,
    copy_non_authority,
    materialization_packet_digest,
    next_cycle_compiler_receipt_digest,
    next_plan_activation_receipt_digest,
    require_int,
    require_string,
    unique_strings,
)


def project_replan_route(route: str) -> str:
    projected = ROUTE_PROJECTION.get(require_string(route, "replan_route"))
    if projected is None:
        raise ValueError("replan_route_projection_unsupported")
    return projected


def _validate_replan_receipt(
    replan_state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> None:
    if receipt.get("version") != REPLAN_PHASE_RECEIPT_VERSION:
        raise ValueError("replan_phase_receipt_version_invalid")
    if receipt.get("replan_phase_receipt_digest") != replan_phase_receipt_digest(receipt):
        raise ValueError("replan_phase_receipt_digest_invalid")
    bindings = {
        "replan_id": replan_state.get("replan_id"),
        "replan_state_digest": replan_state.get("replan_state_digest"),
        "source_plan_state_digest": replan_state.get("source_plan_state_digest"),
        "source_learn_state_digest": replan_state.get("source_learn_state_digest"),
        "source_learning_delta_digest": replan_state.get("source_learning_delta_digest"),
        "qi_condition_packet_digest": replan_state.get("qi_condition_packet_digest"),
        "decision_receipt_digest": replan_state.get("decision_receipt_digest"),
        "synthesis_packet_digest": replan_state.get("synthesis_packet_digest"),
        "next_plan_basis_digest": replan_state.get("next_plan_basis_digest"),
        "route": replan_state.get("route"),
        "current_cycle_index": replan_state.get("current_cycle_index"),
        "active_from_cycle": replan_state.get("active_from_cycle"),
    }
    for field, expected in bindings.items():
        if receipt.get(field) != expected:
            raise ValueError(f"replan_phase_receipt_{field}_mismatch")
    required = {
        "mission_cycle_phase": "replan",
        "future_only": True,
        "active_now": False,
        "next_plan_phase_required": True,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "plan_not_execution": True,
        "host_license_granted": False,
    }
    for field, expected in required.items():
        if receipt.get(field) != expected:
            raise ValueError(f"replan_phase_receipt_{field}_invalid")
    if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        raise ValueError("replan_phase_receipt_authority_escalation")


def validate_adapter_sources(
    *,
    current_plan_state: Mapping[str, Any],
    source_wa_state: Mapping[str, Any],
    replan_state: Mapping[str, Any],
    replan_phase_receipt: Mapping[str, Any],
) -> None:
    plan_errors = validate_plan_state(current_plan_state)
    if plan_errors:
        raise ValueError("invalid_current_plan_state:" + ";".join(plan_errors))
    if current_plan_state.get("current_phase") != "commit":
        raise ValueError("current_plan_not_committed")
    wa_errors = validate_wa_state(source_wa_state)
    if wa_errors:
        raise ValueError("invalid_source_wa_state:" + ";".join(wa_errors))
    if source_wa_state.get("current_phase") != "commit":
        raise ValueError("source_wa_not_committed")
    replan_errors = validate_replan_state(replan_state)
    if replan_errors:
        raise ValueError("invalid_replan_state:" + ";".join(replan_errors))
    if replan_state.get("current_phase") != "commit_next":
        raise ValueError("replan_not_committed")
    if replan_state.get("next_plan_basis_committed") is not True:
        raise ValueError("next_plan_basis_not_committed")
    if replan_state.get("next_plan_phase_required") is not True:
        raise ValueError("next_plan_phase_debt_missing")
    if replan_state.get("active_now") is not False:
        raise ValueError("replan_basis_already_active")

    plan_wa_bindings = {
        "source_wa_state_digest": source_wa_state.get("wa_state_digest"),
        "source_committed_wa_digest": source_wa_state.get("latest_committed_wa_digest"),
        "source_wa_basis_digest": source_wa_state.get("wa_basis_digest"),
        "source_wa_id": source_wa_state.get("wa_id"),
    }
    for field, expected in plan_wa_bindings.items():
        if current_plan_state.get(field) != expected:
            raise ValueError(f"current_plan_{field}_mismatch")
    if current_plan_state.get("plan_state_digest") != replan_state.get(
        "source_plan_state_digest"
    ):
        raise ValueError("replan_source_plan_state_mismatch")
    if current_plan_state.get("latest_committed_plan_digest") != replan_state.get(
        "source_committed_plan_digest"
    ):
        raise ValueError("replan_source_committed_plan_mismatch")
    if current_plan_state.get("plan_basis_digest") != replan_state.get(
        "source_plan_basis_digest"
    ):
        raise ValueError("replan_source_plan_basis_mismatch")
    if current_plan_state.get("lineage_id") != replan_state.get("lineage_id"):
        raise ValueError("adapter_lineage_mismatch")
    if current_plan_state.get("mission_contract_digest") != replan_state.get(
        "mission_contract_digest"
    ):
        raise ValueError("adapter_mission_contract_mismatch")
    if source_wa_state.get("lineage_id") != replan_state.get("lineage_id"):
        raise ValueError("adapter_wa_replan_lineage_mismatch")
    if source_wa_state.get("mission_contract_digest") != replan_state.get(
        "mission_contract_digest"
    ):
        raise ValueError("adapter_wa_replan_mission_mismatch")
    if replan_state.get("active_from_cycle") != int(
        replan_state.get("current_cycle_index", -1)
    ) + 1:
        raise ValueError("adapter_replan_cycle_successor_invalid")
    _validate_replan_receipt(replan_state, replan_phase_receipt)


def build_next_plan_activation_receipt(
    *,
    current_plan_state: Mapping[str, Any],
    source_wa_state: Mapping[str, Any],
    replan_state: Mapping[str, Any],
    replan_phase_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_cycle_index: int,
    mission_cycle_state_digest: str,
    mission_plan_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    validate_adapter_sources(
        current_plan_state=current_plan_state,
        source_wa_state=source_wa_state,
        replan_state=replan_state,
        replan_phase_receipt=replan_phase_receipt,
    )
    if mission_cycle_phase != "plan":
        raise ValueError("next_cycle_plan_phase_required")
    cycle = require_int(mission_cycle_cycle_index, "mission_cycle_cycle_index")
    expected_cycle = int(replan_state["active_from_cycle"])
    if cycle < expected_cycle:
        raise ValueError("next_cycle_activation_too_early")
    if cycle > expected_cycle:
        raise ValueError("next_cycle_activation_window_missed")
    packet = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "lineage_id": replan_state["lineage_id"],
        "mission_contract_digest": replan_state["mission_contract_digest"],
        "current_plan_id": current_plan_state["plan_id"],
        "current_plan_state_digest": current_plan_state["plan_state_digest"],
        "current_committed_plan_digest": current_plan_state[
            "latest_committed_plan_digest"
        ],
        "source_wa_id": source_wa_state["wa_id"],
        "source_wa_state_digest": source_wa_state["wa_state_digest"],
        "source_committed_wa_digest": source_wa_state["latest_committed_wa_digest"],
        "source_wa_basis_digest": source_wa_state["wa_basis_digest"],
        "wa_lineage_role": "authorization_provenance_only",
        "replan_id": replan_state["replan_id"],
        "replan_state_digest": replan_state["replan_state_digest"],
        "replan_phase_receipt_digest": replan_phase_receipt[
            "replan_phase_receipt_digest"
        ],
        "source_learning_delta_digest": replan_state[
            "source_learning_delta_digest"
        ],
        "qi_condition_packet_digest": replan_state["qi_condition_packet_digest"],
        "decision_receipt_digest": replan_state["decision_receipt_digest"],
        "synthesis_packet_digest": replan_state["synthesis_packet_digest"],
        "selected_candidate_id": replan_state["selected_candidate_id"],
        "selected_candidate_digest": replan_state["selected_candidate_digest"],
        "replan_route": replan_state["route"],
        "projected_plan_route": project_replan_route(str(replan_state["route"])),
        "next_plan_basis_digest": replan_state["next_plan_basis_digest"],
        "replan_lineage_role": "next_plan_identity",
        "mission_cycle_phase": "plan",
        "previous_cycle_index": replan_state["current_cycle_index"],
        "mission_cycle_cycle_index": cycle,
        "active_from_cycle": expected_cycle,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "mission_plan_phase_event_digest": require_string(
            mission_plan_phase_event_digest, "mission_plan_phase_event_digest"
        ),
        "basis_eligible_now": True,
        "compilation_required": True,
        "plan_active_now": False,
        "previous_plan_unchanged": True,
        "past_records_unchanged": True,
        "execution_granted": False,
        "host_license_granted": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "next_plan_activation_receipt_digest": "",
    }
    packet["next_plan_activation_receipt_digest"] = next_plan_activation_receipt_digest(
        packet
    )
    return packet


def build_legacy_compat_activation_receipt(
    *,
    source_wa_state: Mapping[str, Any],
    replan_phase_receipt: Mapping[str, Any],
    next_plan_activation_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    if next_plan_activation_receipt.get("version") != ACTIVATION_RECEIPT_VERSION:
        raise ValueError("next_plan_activation_version_invalid")
    if next_plan_activation_receipt.get(
        "next_plan_activation_receipt_digest"
    ) != next_plan_activation_receipt_digest(next_plan_activation_receipt):
        raise ValueError("next_plan_activation_digest_invalid")
    if next_plan_activation_receipt.get("mission_cycle_phase") != "plan":
        raise ValueError("next_plan_activation_plan_phase_required")
    return build_replan_wa_activation_receipt(
        state=source_wa_state,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=require_string(
            replan_phase_receipt.get("mission_cycle_state_digest"),
            "replan_mission_cycle_state_digest",
        ),
        replan_receipt_digest=next_plan_activation_receipt[
            "next_plan_activation_receipt_digest"
        ],
        next_plan_basis_digest=next_plan_activation_receipt[
            "next_plan_basis_digest"
        ],
        now_ms=require_int(now_ms, "now_ms"),
    )


def _normalize_materialized_step(
    *,
    raw: Mapping[str, Any],
    expected_template_digest: str,
    selected_candidate_id: str,
    source_option_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if raw.get("template_digest") != expected_template_digest:
        raise ValueError("materialization_template_digest_mismatch")
    if raw.get("source_replan_candidate_id") != selected_candidate_id:
        raise ValueError("materialization_selected_candidate_mismatch")
    adapter_step = deepcopy(dict(raw))
    adapter_step["source_option_id"] = source_option_id
    v01_step = {
        key: deepcopy(value)
        for key, value in adapter_step.items()
        if key
        not in {
            "template_digest",
            "source_replan_candidate_id",
            "rollback_point_digest",
        }
    }
    return adapter_step, v01_step


def build_materialization_packet(
    *,
    current_plan_state: Mapping[str, Any],
    replan_state: Mapping[str, Any],
    next_plan_activation_receipt: Mapping[str, Any],
    steps: Sequence[Mapping[str, Any]],
    withheld_template_digests: Sequence[str] = (),
) -> dict[str, Any]:
    if next_plan_activation_receipt.get(
        "next_plan_activation_receipt_digest"
    ) != next_plan_activation_receipt_digest(next_plan_activation_receipt):
        raise ValueError("next_plan_activation_digest_invalid")
    if next_plan_activation_receipt.get("replan_state_digest") != replan_state.get(
        "replan_state_digest"
    ):
        raise ValueError("materialization_replan_state_mismatch")
    if next_plan_activation_receipt.get("next_plan_basis_digest") != replan_state.get(
        "next_plan_basis_digest"
    ):
        raise ValueError("materialization_basis_mismatch")
    synthesis = replan_state.get("synthesis_packet")
    if not isinstance(synthesis, Mapping):
        raise ValueError("materialization_synthesis_packet_required")
    templates = list(synthesis.get("next_plan_step_template_digests", []))
    selected_id = require_string(
        replan_state.get("selected_candidate_id"), "selected_candidate_id"
    )
    source_option_id = str(current_plan_state.get("source_selected_option_id", ""))
    if not source_option_id:
        source_ids = list(current_plan_state.get("source_option_ids", []))
        if not source_ids:
            raise ValueError("materialization_source_option_id_missing")
        source_option_id = str(source_ids[0])

    normalized_adapter: list[dict[str, Any]] = []
    normalized_v01: list[dict[str, Any]] = []
    withheld = list(withheld_template_digests)
    if replan_state.get("route") == "HOLD":
        if steps:
            raise ValueError("hold_materialization_must_not_create_steps")
        if withheld != templates:
            raise ValueError("hold_withheld_templates_mismatch")
    else:
        if withheld:
            raise ValueError("active_materialization_withheld_templates_forbidden")
        if len(steps) != len(templates):
            raise ValueError("materialization_template_count_mismatch")
        for raw, expected in zip(steps, templates, strict=True):
            if not isinstance(raw, Mapping):
                raise ValueError("materialization_step_object_required")
            adapter_step, v01_step = _normalize_materialized_step(
                raw=raw,
                expected_template_digest=expected,
                selected_candidate_id=selected_id,
                source_option_id=source_option_id,
            )
            normalized_adapter.append(adapter_step)
            normalized_v01.append(v01_step)

        observations = {
            str(step.get("expected_observation_digest", ""))
            for step in normalized_adapter
        }
        verifications = {
            str(step.get("verification_criterion_digest", ""))
            for step in normalized_adapter
        }
        stops = {
            str(item)
            for step in normalized_adapter
            for item in step.get("stop_condition_digests", [])
        }
        rollbacks = {
            str(step.get("rollback_point_digest", ""))
            for step in normalized_adapter
            if step.get("rollback_point_digest")
        }
        if not set(synthesis.get("next_observation_point_digests", [])).issubset(
            observations
        ):
            raise ValueError("materialization_observation_coverage_missing")
        if not set(
            synthesis.get("next_verification_criterion_digests", [])
        ).issubset(verifications):
            raise ValueError("materialization_verification_coverage_missing")
        if not set(synthesis.get("next_stop_condition_digests", [])).issubset(stops):
            raise ValueError("materialization_stop_coverage_missing")
        if not set(synthesis.get("next_rollback_point_digests", [])).issubset(
            rollbacks
        ):
            raise ValueError("materialization_rollback_coverage_missing")

    packet = {
        "version": MATERIALIZATION_PACKET_VERSION,
        "lineage_id": replan_state["lineage_id"],
        "replan_id": replan_state["replan_id"],
        "replan_state_digest": replan_state["replan_state_digest"],
        "next_plan_activation_receipt_digest": next_plan_activation_receipt[
            "next_plan_activation_receipt_digest"
        ],
        "next_plan_basis_digest": replan_state["next_plan_basis_digest"],
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": replan_state["selected_candidate_digest"],
        "replan_route": replan_state["route"],
        "projected_plan_route": project_replan_route(str(replan_state["route"])),
        "expected_template_digests": templates,
        "materialized_steps": normalized_adapter,
        "v01_steps": normalized_v01,
        "withheld_template_digests": withheld,
        "exact_template_order_preserved": True,
        "selected_candidate_identity_preserved": True,
        "wa_identity_role": "authorization_provenance_only",
        "replan_identity_role": "next_plan_identity",
        "plan_not_execution": True,
        "host_license_granted": False,
        "non_authority": copy_non_authority(),
        "materialization_packet_digest": "",
    }
    packet["materialization_packet_digest"] = materialization_packet_digest(packet)
    return packet


def build_next_cycle_initial_plan_state(
    *,
    plan_id: str,
    source_wa_state: Mapping[str, Any],
    legacy_compat_activation_receipt: Mapping[str, Any],
    replan_state: Mapping[str, Any],
    next_plan_activation_receipt: Mapping[str, Any],
    plan_budget: float,
    maximum_step_risk: float,
    now_ms: int,
) -> dict[str, Any]:
    if legacy_compat_activation_receipt.get("next_plan_basis_digest") != replan_state.get(
        "next_plan_basis_digest"
    ):
        raise ValueError("legacy_activation_basis_mismatch")
    if legacy_compat_activation_receipt.get("replan_receipt_digest") != next_plan_activation_receipt.get(
        "next_plan_activation_receipt_digest"
    ):
        raise ValueError("legacy_activation_adapter_receipt_mismatch")
    state = build_initial_plan_state(
        plan_id=plan_id,
        source_wa_state=source_wa_state,
        replan_activation_receipt=legacy_compat_activation_receipt,
        plan_budget=plan_budget,
        maximum_step_risk=maximum_step_risk,
        now_ms=now_ms,
    )
    projected = project_replan_route(str(replan_state["route"]))
    if state.get("route") != projected:
        raise ValueError("legacy_compiler_route_projection_mismatch")
    return state


def build_next_cycle_compiler_receipt(
    *,
    previous_plan_state: Mapping[str, Any],
    replan_state: Mapping[str, Any],
    next_plan_activation_receipt: Mapping[str, Any],
    materialization_packet: Mapping[str, Any],
    compiled_plan_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    previous_errors = validate_plan_state(previous_plan_state)
    compiled_errors = validate_plan_state(compiled_plan_state)
    if previous_errors:
        raise ValueError("previous_plan_state_invalid:" + ";".join(previous_errors))
    if compiled_errors:
        raise ValueError("compiled_plan_state_invalid:" + ";".join(compiled_errors))
    if compiled_plan_state.get("current_phase") != "commit":
        raise ValueError("compiled_plan_not_committed")
    if materialization_packet.get("version") != MATERIALIZATION_PACKET_VERSION:
        raise ValueError("materialization_packet_version_invalid")
    if materialization_packet.get(
        "materialization_packet_digest"
    ) != materialization_packet_digest(materialization_packet):
        raise ValueError("materialization_packet_digest_invalid")
    bindings = {
        "lineage_id": replan_state.get("lineage_id"),
        "next_plan_basis_digest": replan_state.get("next_plan_basis_digest"),
        "selected_candidate_id": replan_state.get("selected_candidate_id"),
        "selected_candidate_digest": replan_state.get("selected_candidate_digest"),
    }
    for field, expected in bindings.items():
        if materialization_packet.get(field) != expected:
            raise ValueError(f"compiler_materialization_{field}_mismatch")
    if compiled_plan_state.get("next_plan_basis_digest") != replan_state.get(
        "next_plan_basis_digest"
    ):
        raise ValueError("compiled_plan_basis_mismatch")
    if compiled_plan_state.get("route") != project_replan_route(
        str(replan_state.get("route"))
    ):
        raise ValueError("compiled_plan_route_mismatch")
    if compiled_plan_state.get("replan_receipt_digest") != next_plan_activation_receipt.get(
        "next_plan_activation_receipt_digest"
    ):
        raise ValueError("compiled_plan_activation_binding_mismatch")
    if compiled_plan_state.get("lineage_id") != previous_plan_state.get("lineage_id"):
        raise ValueError("compiled_plan_lineage_mismatch")
    if compiled_plan_state.get("mission_contract_digest") != previous_plan_state.get(
        "mission_contract_digest"
    ):
        raise ValueError("compiled_plan_mission_mismatch")

    packet = {
        "version": COMPILER_RECEIPT_VERSION,
        "lineage_id": replan_state["lineage_id"],
        "mission_contract_digest": replan_state["mission_contract_digest"],
        "previous_plan_id": previous_plan_state["plan_id"],
        "previous_plan_state_digest": previous_plan_state["plan_state_digest"],
        "previous_committed_plan_digest": previous_plan_state[
            "latest_committed_plan_digest"
        ],
        "previous_plan_unchanged": True,
        "replan_id": replan_state["replan_id"],
        "replan_state_digest": replan_state["replan_state_digest"],
        "replan_phase_receipt_digest": next_plan_activation_receipt[
            "replan_phase_receipt_digest"
        ],
        "next_plan_activation_receipt_digest": next_plan_activation_receipt[
            "next_plan_activation_receipt_digest"
        ],
        "materialization_packet_digest": materialization_packet[
            "materialization_packet_digest"
        ],
        "next_plan_basis_digest": replan_state["next_plan_basis_digest"],
        "selected_candidate_id": replan_state["selected_candidate_id"],
        "selected_candidate_digest": replan_state["selected_candidate_digest"],
        "qi_condition_packet_digest": replan_state["qi_condition_packet_digest"],
        "decision_receipt_digest": replan_state["decision_receipt_digest"],
        "synthesis_packet_digest": replan_state["synthesis_packet_digest"],
        "replan_route": replan_state["route"],
        "projected_plan_route": project_replan_route(str(replan_state["route"])),
        "compiled_plan_id": compiled_plan_state["plan_id"],
        "compiled_plan_state_digest": compiled_plan_state["plan_state_digest"],
        "compiled_plan_basis_digest": compiled_plan_state["plan_basis_digest"],
        "compiled_plan_route": compiled_plan_state["route"],
        "mission_cycle_cycle_index": next_plan_activation_receipt[
            "mission_cycle_cycle_index"
        ],
        "active_from_cycle": replan_state["active_from_cycle"],
        "structured_compiler": "PlanOS_v0_1",
        "single_use_activation": True,
        "plan_committed": True,
        "plan_not_execution": True,
        "host_license_granted": False,
        "memory_overwrite": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "next_cycle_compiler_receipt_digest": "",
    }
    packet["next_cycle_compiler_receipt_digest"] = next_cycle_compiler_receipt_digest(
        packet
    )
    return packet
