#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_evidence_weighted_selection_abstention_v0_1 import (
    build_codeai_evidence_weighted_selection_abstention,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_DIGEST_FIELD as SELECTION_DECISION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_v0_1 import (
    build_codeai_version_bound_repair_memory,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    MEMORY_SNAPSHOT_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as MEMORY_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as MEMORY_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as MEMORY_REQUEST_DIGEST_FIELD,
    VERSION_BINDING_FIELDS,
)
from runtime.kuuos_codeai_maintainability_trajectory_gate_schema_v0_1 import (
    EVIDENCE_PACKET_DIGEST_FIELD,
    EVIDENCE_RECORD_DIGEST_FIELD,
    MAINTAINABILITY_AXES,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from scripts.build_codeai_evidence_weighted_selection_abstention_fixture_v0_1 import (
    build_fixture as build_selection_fixture,
)
from scripts.build_codeai_version_bound_repair_memory_fixture_v0_1 import (
    build_fixture as build_memory_fixture,
)


def _rebind_memory_to_selected_candidate(
    memory_inputs: dict[str, Any],
    *,
    selected_candidate_digest: str,
) -> None:
    classification = memory_inputs["source_classification"]
    packet = memory_inputs["repair_evidence_packet"]
    candidate = next(
        (
            item
            for item in classification["typed_candidates"]
            if item["source_candidate_digest"] == selected_candidate_digest
        ),
        None,
    )
    if candidate is None:
        raise ValueError("selected candidate is absent from memory classification")

    if candidate["typed_errors"]:
        error = candidate["typed_errors"][0]
        record = next(
            (
                item
                for item in packet["records"]
                if item["source_candidate_digest"] == selected_candidate_digest
                and item["typed_error_digest"] == error["typed_error_digest"]
            ),
            None,
        )
        if record is None:
            raise ValueError("selected candidate has no repair-memory record")
        typed_error_digest = error["typed_error_digest"]
        error_fingerprint = error["error_fingerprint"]
    else:
        if not packet["records"]:
            raise ValueError("repair-memory packet has no environment binding record")
        record = packet["records"][0]
        typed_error_digest = canonical_digest(
            {
                "source_candidate_digest": selected_candidate_digest,
                "typed_error_state": "no_typed_error",
            }
        )
        error_fingerprint = "no_typed_error"

    binding = {
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_repository_snapshot_digest": classification[
            "source_repository_snapshot_digest"
        ],
        "source_candidate_digest": selected_candidate_digest,
        "typed_error_digest": typed_error_digest,
        "error_fingerprint": error_fingerprint,
        "classification_schema_version": classification["schema_version"],
        "toolchain_digest": record["toolchain_digest"],
        "dependency_manifest_digest": record["dependency_manifest_digest"],
        "repair_policy_digest": record["repair_policy_digest"],
    }
    request = memory_inputs["memory_request"]
    policy = memory_inputs["memory_policy"]
    for field in VERSION_BINDING_FIELDS:
        request[field] = binding[field]
        policy["expected_" + field] = binding[field]
    memory_inputs["memory_request"] = seal(
        request, MEMORY_REQUEST_DIGEST_FIELD
    )
    memory_inputs["memory_policy"] = seal(
        policy, MEMORY_POLICY_DIGEST_FIELD
    )


def build_fixture(
    gate_spec: dict[str, Any],
    selection_spec: dict[str, Any],
    strengthening_spec: dict[str, Any],
    memory_spec: dict[str, Any],
    classification_spec: dict[str, Any],
    portfolio_spec: dict[str, Any],
    baseline_spec: dict[str, Any],
) -> dict[str, Any]:
    selection_inputs = build_selection_fixture(
        selection_spec,
        strengthening_spec,
        classification_spec,
        portfolio_spec,
        baseline_spec,
    )
    selection_result = build_codeai_evidence_weighted_selection_abstention(
        strengthening_plan=selection_inputs["strengthening_plan"],
        strengthening_receipt=selection_inputs["strengthening_receipt"],
        evidence_packet=selection_inputs["evidence_packet"],
        selection_request=selection_inputs["selection_request"],
        selection_policy=selection_inputs["selection_policy"],
    )
    if selection_result.decision is None or selection_result.receipt is None:
        raise ValueError(
            "selection fixture blocked: " + ",".join(selection_result.issues)
        )
    selection = selection_result.decision
    selection_receipt = selection_result.receipt
    if not selection["candidate_selected"]:
        raise ValueError("maintainability fixture requires a selected candidate")

    memory_inputs = build_memory_fixture(
        memory_spec,
        classification_spec,
        portfolio_spec,
        baseline_spec,
    )
    _rebind_memory_to_selected_candidate(
        memory_inputs,
        selected_candidate_digest=selection["selected_candidate_digest"],
    )
    memory_result = build_codeai_version_bound_repair_memory(
        source_classification=memory_inputs["source_classification"],
        source_classification_receipt=memory_inputs[
            "source_classification_receipt"
        ],
        repair_evidence_packet=memory_inputs["repair_evidence_packet"],
        memory_request=memory_inputs["memory_request"],
        memory_policy=memory_inputs["memory_policy"],
    )
    if memory_result.snapshot is None or memory_result.receipt is None:
        raise ValueError(
            "memory fixture blocked: " + ",".join(memory_result.issues)
        )
    memory = memory_result.snapshot
    memory_receipt = memory_result.receipt

    if memory["repository_full_name"] != selection["repository_full_name"]:
        raise ValueError("selection and memory repository mismatch")
    if memory["source_commit_sha"] != selection["source_commit_sha"]:
        raise ValueError("selection and memory source commit mismatch")
    if (
        memory["source_repository_snapshot_digest"]
        != selection["source_repository_snapshot_digest"]
    ):
        raise ValueError("selection and memory source snapshot mismatch")
    if (
        memory["query_version_binding"]["source_candidate_digest"]
        != selection["selected_candidate_digest"]
    ):
        raise ValueError("selection and memory candidate binding mismatch")

    assessor_id = gate_spec["independent_assessor_id"]
    reviewer_id = gate_spec["independent_reviewer_id"]
    records: list[dict[str, Any]] = []
    axis_values = gate_spec["axis_values"]
    if list(axis_values) != list(MAINTAINABILITY_AXES):
        raise ValueError("axis_values must preserve the canonical axis order")
    for index, axis in enumerate(MAINTAINABILITY_AXES, start=1):
        values = axis_values[axis]
        baseline_value = int(values["baseline_value"])
        candidate_value = int(values["candidate_value"])
        artifact_digest = canonical_digest(
            {
                "axis": axis,
                "selected_candidate_digest": selection[
                    "selected_candidate_digest"
                ],
                "baseline_value": baseline_value,
                "candidate_value": candidate_value,
                "measurement_label": values["measurement_label"],
                "assessor_id": assessor_id,
                "reviewer_id": reviewer_id,
            }
        )
        record = seal(
            {
                "measurement_record_id": f"trajectory-record-{index:03d}",
                "axis": axis,
                "baseline_value": baseline_value,
                "candidate_value": candidate_value,
                "observed_delta": candidate_value - baseline_value,
                "measurement_artifact_digest": artifact_digest,
                "assessor_id": assessor_id,
                "reviewer_id": reviewer_id,
                "completed": True,
                "external_measurement": True,
                "independent_assessor": True,
                "independent_reviewer": True,
                "isolated_candidate_evaluation": True,
                "source_correspondence": True,
                "candidate_producer_involved": False,
                "repository_mutation_performed": False,
                "git_effect_performed": False,
            },
            EVIDENCE_RECORD_DIGEST_FIELD,
        )
        records.append(record)

    selection_digest = selection[SELECTION_DECISION_DIGEST_FIELD]
    selection_receipt_digest = selection_receipt[
        SELECTION_RECEIPT_DIGEST_FIELD
    ]
    memory_digest = memory[MEMORY_SNAPSHOT_DIGEST_FIELD]
    memory_receipt_digest = memory_receipt[MEMORY_RECEIPT_DIGEST_FIELD]
    packet = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Maintainability Trajectory Gate v0.1",
            "evidence_packet_id": gate_spec["evidence_packet_id"],
            "evidence_packet_revision": gate_spec["evidence_packet_revision"],
            "selection_decision_digest": selection_digest,
            "selection_receipt_digest": selection_receipt_digest,
            "memory_snapshot_digest": memory_digest,
            "memory_receipt_digest": memory_receipt_digest,
            "repository_full_name": selection["repository_full_name"],
            "source_commit_sha": selection["source_commit_sha"],
            "source_repository_snapshot_digest": selection[
                "source_repository_snapshot_digest"
            ],
            "selected_candidate_id": selection["selected_candidate_id"],
            "selected_candidate_digest": selection[
                "selected_candidate_digest"
            ],
            "evidence_created_epoch": gate_spec["evidence_created_epoch"],
            "candidate_producer_id": gate_spec["candidate_producer_id"],
            "independent_assessor_id": assessor_id,
            "independent_reviewer_id": reviewer_id,
            "records": records,
            "record_count": len(records),
            "external_measurement_reported": True,
            "independent_assessor_verified": True,
            "independent_reviewer_verified": True,
            "isolated_candidate_evaluation_verified": True,
            "source_correspondence_verified": True,
            "live_repository_unchanged": True,
            "candidate_producer_involved_in_measurement": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
        },
        EVIDENCE_PACKET_DIGEST_FIELD,
    )

    identity = {
        "repository_full_name": selection["repository_full_name"],
        "source_commit_sha": selection["source_commit_sha"],
        "source_repository_snapshot_digest": selection[
            "source_repository_snapshot_digest"
        ],
        "selected_candidate_id": selection["selected_candidate_id"],
        "selected_candidate_digest": selection["selected_candidate_digest"],
    }
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Maintainability Trajectory Gate v0.1",
            "gate_request_id": gate_spec["gate_request_id"],
            "gate_request_revision": gate_spec["gate_request_revision"],
            "selection_decision_digest": selection_digest,
            "selection_receipt_digest": selection_receipt_digest,
            "memory_snapshot_digest": memory_digest,
            "memory_receipt_digest": memory_receipt_digest,
            "trajectory_evidence_packet_digest": packet[
                EVIDENCE_PACKET_DIGEST_FIELD
            ],
            **identity,
            "request_created_epoch": gate_spec["request_created_epoch"],
            "unresolved_maintainability_questions": [],
            "claims_selection_authority": False,
            "claims_verification_authority": False,
            "claims_repair_authority": False,
            "claims_execution_authority": False,
            "claims_git_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Maintainability Trajectory Gate v0.1",
            "expected_selection_decision_digest": selection_digest,
            "expected_selection_receipt_digest": selection_receipt_digest,
            "expected_memory_snapshot_digest": memory_digest,
            "expected_memory_receipt_digest": memory_receipt_digest,
            "expected_trajectory_evidence_packet_digest": packet[
                EVIDENCE_PACKET_DIGEST_FIELD
            ],
            **{"expected_" + key: value for key, value in identity.items()},
            "evaluation_epoch": gate_spec["evaluation_epoch"],
            "maximum_request_age": gate_spec["maximum_request_age"],
            "maximum_evidence_age": gate_spec["maximum_evidence_age"],
            "maximum_trajectory_records": gate_spec[
                "maximum_trajectory_records"
            ],
            "required_axes": list(MAINTAINABILITY_AXES),
            "maximum_allowed_increase": gate_spec[
                "maximum_allowed_increase"
            ],
            "maximum_total_regression": gate_spec[
                "maximum_total_regression"
            ],
            "minimum_improved_axes": gate_spec["minimum_improved_axes"],
            "require_source_selection_selected": True,
            "require_exact_lineage": True,
            "require_complete_axis_coverage": True,
            "require_independent_assessor": True,
            "require_independent_reviewer": True,
            "require_isolated_candidate_evaluation": True,
            "require_source_correspondence": True,
            "require_exact_memory_binding": True,
            "require_live_repository_unchanged": True,
            "allow_maintainability_gate_decision": True,
            "allow_memory_threshold_waiver": False,
            "allow_test_execution": False,
            "allow_repair_execution": False,
            "allow_repository_mutation": False,
            "allow_selection_authority": False,
            "allow_verification_authority": False,
            "allow_repair_authority": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return {
        "selection_decision": selection,
        "selection_receipt": selection_receipt,
        "memory_snapshot": memory,
        "memory_receipt": memory_receipt,
        "trajectory_evidence_packet": packet,
        "gate_request": request,
        "gate_policy": policy,
    }


__all__ = ["build_fixture"]