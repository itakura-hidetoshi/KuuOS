from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_indra_transport_request_v1_6 import (
    build_indra_transport_request_receipt,
    validate_indra_transport_request_receipt,
)

VERSION = "kuuos_qi_world_indra_transport_receipt_intake_v1_7"
EXTERNAL_RECEIPT_VERSION = "kuuos_external_indra_analytic_receipt_v1_7"
INTAKE_RECEIPT_VERSION = "kuuos_qi_world_indra_transport_receipt_intake_receipt_v1_7"
CYCLE_ID = "qi-world-indra-transport-receipt-intake-v17"

REQUIRED_RECEIPT_KINDS = (
    "NORMAL_STAR_ISOMORPHISM",
    "PSEUDOFUNCTOR_REALIZATION",
    "STACK_DESCENT",
    "BRANCH_TRANSPORT",
    "COHERENCE_TWO_CELL",
    "HISTORY_DEPENDENT_PHASE",
    "CONTINUUM_NONMARKOV_CONNECTION",
)

CLAIM_NAMES = {
    "NORMAL_STAR_ISOMORPHISM": "normal_star_isomorphism",
    "PSEUDOFUNCTOR_REALIZATION": "pseudofunctor_realization",
    "STACK_DESCENT": "stack_descent",
    "BRANCH_TRANSPORT": "branch_transport",
    "COHERENCE_TWO_CELL": "coherence_two_cell",
    "HISTORY_DEPENDENT_PHASE": "history_dependent_phase",
    "CONTINUUM_NONMARKOV_CONNECTION": "continuum_nonmarkov_connection",
}

EXPECTED_DEPENDENCIES = {
    "NORMAL_STAR_ISOMORPHISM": (),
    "PSEUDOFUNCTOR_REALIZATION": ("NORMAL_STAR_ISOMORPHISM",),
    "STACK_DESCENT": ("PSEUDOFUNCTOR_REALIZATION",),
    "BRANCH_TRANSPORT": (
        "NORMAL_STAR_ISOMORPHISM",
        "PSEUDOFUNCTOR_REALIZATION",
        "STACK_DESCENT",
    ),
    "COHERENCE_TWO_CELL": (
        "PSEUDOFUNCTOR_REALIZATION",
        "BRANCH_TRANSPORT",
    ),
    "HISTORY_DEPENDENT_PHASE": (
        "BRANCH_TRANSPORT",
        "COHERENCE_TWO_CELL",
    ),
    "CONTINUUM_NONMARKOV_CONNECTION": (
        "HISTORY_DEPENDENT_PHASE",
    ),
}

EXTERNAL_RECEIPT_NON_AUTHORITY = {
    "receipt_grants_execution": False,
    "receipt_grants_truth": False,
    "receipt_issues_authority": False,
    "receipt_constructs_runtime_gauge_connection": False,
    "receipt_computes_physical_holonomy": False,
    "receipt_identifies_exact_world": False,
    "receipt_updates_world": False,
    "receipt_collapses_world_branches": False,
    "receipt_overwrites_history": False,
    "runtime_asserts_semantic_validity": False,
}

INTAKE_NON_AUTHORITY = {
    "intake_grants_execution": False,
    "intake_grants_truth": False,
    "intake_issues_authority": False,
    "intake_realizes_transport": False,
    "intake_constructs_gauge_connection": False,
    "intake_computes_physical_holonomy": False,
    "intake_identifies_exact_world": False,
    "intake_updates_world": False,
    "intake_collapses_world_branches": False,
    "intake_overwrites_history": False,
    "intake_performs_semantic_review": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def external_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "external_analytic_receipt_digest")


def intake_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "indra_transport_receipt_intake_digest")


def _request_payload(source_receipt: Mapping[str, Any]) -> dict[str, Any]:
    request = source_receipt.get("transport_request")
    if not isinstance(request, Mapping):
        raise ValueError("indra_intake_transport_request_missing")
    return deepcopy(dict(request))


def _required_dependency_digests(
    kind: str,
    receipts_by_kind: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    return [
        str(receipts_by_kind[dependency]["external_analytic_receipt_digest"])
        for dependency in EXPECTED_DEPENDENCIES[kind]
    ]


def build_external_analytic_receipt(
    *,
    kind: str,
    source_request_receipt: Mapping[str, Any],
    issuer_id: str,
    proof_object_digest: str,
    verifier_receipt_digest: str,
    dependency_receipt_digests: Sequence[str],
    issued_at_ms: int,
    fixture_only: bool = False,
) -> dict[str, Any]:
    if kind not in REQUIRED_RECEIPT_KINDS:
        raise ValueError("indra_external_receipt_kind_invalid")
    source_errors = validate_indra_transport_request_receipt(source_request_receipt)
    if source_errors:
        raise ValueError(
            "indra_external_receipt_source_invalid:" + ";".join(source_errors)
        )
    request = _request_payload(source_request_receipt)
    if not isinstance(issuer_id, str) or not issuer_id.strip():
        raise ValueError("indra_external_receipt_issuer_required")
    if not isinstance(proof_object_digest, str) or not proof_object_digest:
        raise ValueError("indra_external_receipt_proof_object_required")
    if not isinstance(verifier_receipt_digest, str) or not verifier_receipt_digest:
        raise ValueError("indra_external_receipt_verifier_required")
    if isinstance(issued_at_ms, bool) or not isinstance(issued_at_ms, int) or issued_at_ms < 0:
        raise ValueError("indra_external_receipt_issued_at_invalid")

    receipt = {
        "version": EXTERNAL_RECEIPT_VERSION,
        "receipt_kind": kind,
        "claim_name": CLAIM_NAMES[kind],
        "claim_supported_by_external_evidence": True,
        "issuer_id": issuer_id,
        "issued_at_ms": issued_at_ms,
        "fixture_only": bool(fixture_only),
        "source_request_receipt_digest": source_request_receipt[
            "indra_transport_request_receipt_digest"
        ],
        "source_transport_request_digest": request["transport_request_digest"],
        "world_v042_bridge_state_digest": request[
            "world_v042_bridge_state_digest"
        ],
        "source_world_projection_digest": request[
            "source_world_projection_digest"
        ],
        "target_world_projection_digest": request[
            "target_world_projection_digest"
        ],
        "source_patch_id": request["source_patch_id"],
        "target_patch_id": request["target_patch_id"],
        "patch_path": deepcopy(request["patch_path"]),
        "overlap_evidence_request_digest": request[
            "overlap_evidence_request_digest"
        ],
        "branch_id": request["branch_id"],
        "process_lineage_digest": request["process_lineage_digest"],
        "history_digest": request["history_digest"],
        "dependency_receipt_digests": list(dependency_receipt_digests),
        "proof_object_digest": proof_object_digest,
        "verifier_receipt_digest": verifier_receipt_digest,
        "representation_level_only": True,
        "branch_preserving": True,
        "history_preserving": True,
        "source_target_patch_distinct": request["source_patch_id"]
        != request["target_patch_id"],
        "semantic_review_external": True,
        "semantic_validity_asserted_by_runtime": False,
        "transport_realized_by_runtime": False,
        "gauge_connection_constructed_by_runtime": False,
        "physical_holonomy_computed_by_runtime": False,
        "exact_world_identity_asserted": False,
        "world_updated": False,
        "branch_collapsed": False,
        "history_overwritten": False,
        "external_receipt_non_authority": deepcopy(
            EXTERNAL_RECEIPT_NON_AUTHORITY
        ),
        "external_analytic_receipt_digest": "",
    }
    receipt["external_analytic_receipt_digest"] = external_receipt_digest(
        receipt
    )
    errors = validate_external_analytic_receipt(
        receipt,
        source_request_receipt=source_request_receipt,
    )
    if errors:
        raise ValueError("indra_external_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_external_analytic_receipt(
    receipt: Mapping[str, Any],
    *,
    source_request_receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        source_errors = validate_indra_transport_request_receipt(
            source_request_receipt
        )
        errors.extend("indra_external_source_" + error for error in source_errors)
        request = _request_payload(source_request_receipt)
        kind = str(receipt.get("receipt_kind", ""))
        require(
            receipt.get("version") == EXTERNAL_RECEIPT_VERSION,
            "indra_external_version_invalid",
        )
        require(kind in REQUIRED_RECEIPT_KINDS, "indra_external_kind_invalid")
        if kind in CLAIM_NAMES:
            require(
                receipt.get("claim_name") == CLAIM_NAMES[kind],
                "indra_external_claim_name_invalid",
            )
        require(
            receipt.get("external_analytic_receipt_digest")
            == external_receipt_digest(receipt),
            "indra_external_digest_invalid",
        )
        require(
            bool(receipt.get("issuer_id")),
            "indra_external_issuer_missing",
        )
        require(
            isinstance(receipt.get("issued_at_ms"), int)
            and not isinstance(receipt.get("issued_at_ms"), bool)
            and int(receipt.get("issued_at_ms", -1)) >= 0,
            "indra_external_issued_at_invalid",
        )
        require(
            bool(receipt.get("proof_object_digest")),
            "indra_external_proof_object_missing",
        )
        require(
            bool(receipt.get("verifier_receipt_digest")),
            "indra_external_verifier_receipt_missing",
        )
        require(
            receipt.get("source_request_receipt_digest")
            == source_request_receipt.get(
                "indra_transport_request_receipt_digest"
            ),
            "indra_external_source_receipt_binding_invalid",
        )
        require(
            receipt.get("source_transport_request_digest")
            == request.get("transport_request_digest"),
            "indra_external_request_binding_invalid",
        )
        for field in (
            "world_v042_bridge_state_digest",
            "source_world_projection_digest",
            "target_world_projection_digest",
            "source_patch_id",
            "target_patch_id",
            "overlap_evidence_request_digest",
            "branch_id",
            "process_lineage_digest",
            "history_digest",
        ):
            require(
                receipt.get(field) == request.get(field),
                f"indra_external_{field}_binding_invalid",
            )
        require(
            receipt.get("patch_path") == request.get("patch_path"),
            "indra_external_patch_path_invalid",
        )
        require(
            isinstance(receipt.get("dependency_receipt_digests"), list),
            "indra_external_dependencies_invalid",
        )
        for key in (
            "claim_supported_by_external_evidence",
            "representation_level_only",
            "branch_preserving",
            "history_preserving",
            "source_target_patch_distinct",
            "semantic_review_external",
        ):
            require(receipt.get(key) is True, f"indra_external_{key}_invalid")
        for key in (
            "semantic_validity_asserted_by_runtime",
            "transport_realized_by_runtime",
            "gauge_connection_constructed_by_runtime",
            "physical_holonomy_computed_by_runtime",
            "exact_world_identity_asserted",
            "world_updated",
            "branch_collapsed",
            "history_overwritten",
        ):
            require(receipt.get(key) is False, f"indra_external_{key}_forbidden")
        require(
            dict(receipt.get("external_receipt_non_authority", {}))
            == EXTERNAL_RECEIPT_NON_AUTHORITY,
            "indra_external_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_indra_transport_receipt_intake(
    *,
    source_request_receipt: Mapping[str, Any],
    external_receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    source_errors = validate_indra_transport_request_receipt(
        source_request_receipt
    )
    if source_errors:
        raise ValueError("indra_intake_source_invalid:" + ";".join(source_errors))
    normalized = [deepcopy(dict(item)) for item in external_receipts]
    input_kinds = [str(item.get("receipt_kind", "")) for item in normalized]
    if len(input_kinds) != len(set(input_kinds)):
        raise ValueError("indra_intake_duplicate_receipt_kind")
    if any(kind not in REQUIRED_RECEIPT_KINDS for kind in input_kinds):
        raise ValueError("indra_intake_unknown_receipt_kind")
    receipt_map = {str(item.get("receipt_kind")): item for item in normalized}
    ordered = [receipt_map[kind] for kind in REQUIRED_RECEIPT_KINDS if kind in receipt_map]
    receipt_set_digest = sha(
        [item.get("external_analytic_receipt_digest") for item in ordered]
    )
    intake = {
        "version": INTAKE_RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "source_request_receipt": deepcopy(dict(source_request_receipt)),
        "source_request_receipt_digest": source_request_receipt[
            "indra_transport_request_receipt_digest"
        ],
        "external_receipts": ordered,
        "receipt_set_digest": receipt_set_digest,
        "receipt_kinds": [item.get("receipt_kind") for item in ordered],
        "all_required_receipts_present": len(ordered)
        == len(REQUIRED_RECEIPT_KINDS),
        "all_receipts_hash_bound": True,
        "dependency_chain_valid": True,
        "branch_preserving": True,
        "history_preserving": True,
        "request_only_boundary_preserved": True,
        "schema_level_request_satisfied": True,
        "semantic_review_required": True,
        "runtime_transport_realized": False,
        "physical_transport_verified": False,
        "exact_world_identity_asserted": False,
        "world_updated": False,
        "branch_collapsed": False,
        "history_overwritten": False,
        "disposition": (
            "EXTERNAL_ANALYTIC_RECEIPTS_HASH_BOUND_"
            "SEMANTIC_REVIEW_REQUIRED"
        ),
        "intake_non_authority": deepcopy(INTAKE_NON_AUTHORITY),
        "indra_transport_receipt_intake_digest": "",
    }
    intake["indra_transport_receipt_intake_digest"] = intake_receipt_digest(
        intake
    )
    errors = validate_indra_transport_receipt_intake(intake)
    if errors:
        raise ValueError("indra_transport_intake_invalid:" + ";".join(errors))
    return intake


def validate_indra_transport_receipt_intake(
    intake: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(
            intake.get("version") == INTAKE_RECEIPT_VERSION,
            "indra_intake_version_invalid",
        )
        require(
            intake.get("indra_transport_receipt_intake_digest")
            == intake_receipt_digest(intake),
            "indra_intake_digest_invalid",
        )
        source = dict(intake.get("source_request_receipt", {}))
        source_errors = validate_indra_transport_request_receipt(source)
        errors.extend("indra_intake_source_" + error for error in source_errors)
        require(
            intake.get("source_request_receipt_digest")
            == source.get("indra_transport_request_receipt_digest"),
            "indra_intake_source_receipt_binding_invalid",
        )
        source_request = _request_payload(source)
        require(
            source.get("disposition")
            == "EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED",
            "indra_intake_source_disposition_invalid",
        )
        require(
            source_request.get("request_only") is True,
            "indra_intake_source_request_only_missing",
        )

        receipts = list(intake.get("external_receipts", []))
        require(
            all(isinstance(item, Mapping) for item in receipts),
            "indra_intake_receipt_list_invalid",
        )
        kinds = [str(item.get("receipt_kind", "")) for item in receipts]
        require(
            len(kinds) == len(set(kinds)),
            "indra_intake_duplicate_receipt_kind",
        )
        require(
            kinds == list(REQUIRED_RECEIPT_KINDS),
            "indra_intake_receipt_kind_order_invalid",
        )
        require(
            len(receipts) == len(REQUIRED_RECEIPT_KINDS),
            "indra_intake_required_receipt_missing",
        )
        receipt_map = {
            str(item.get("receipt_kind")): dict(item) for item in receipts
        }
        issued_times: list[int] = []
        all_hash_bound = True
        for receipt in receipts:
            receipt_errors = validate_external_analytic_receipt(
                receipt,
                source_request_receipt=source,
            )
            if receipt_errors:
                all_hash_bound = False
                errors.extend(
                    f"indra_intake_{receipt.get('receipt_kind')}_" + error
                    for error in receipt_errors
                )
            issued_times.append(int(receipt.get("issued_at_ms", -1)))
        require(
            issued_times == sorted(issued_times)
            and len(set(issued_times)) == len(issued_times),
            "indra_intake_receipt_time_order_invalid",
        )

        dependency_valid = True
        for kind in REQUIRED_RECEIPT_KINDS:
            if kind not in receipt_map:
                dependency_valid = False
                continue
            expected = _required_dependency_digests(kind, receipt_map)
            actual = list(
                receipt_map[kind].get("dependency_receipt_digests", [])
            )
            if actual != expected:
                dependency_valid = False
                errors.append(f"indra_intake_{kind}_dependency_invalid")

        expected_set_digest = sha(
            [
                receipt_map[kind]["external_analytic_receipt_digest"]
                for kind in REQUIRED_RECEIPT_KINDS
                if kind in receipt_map
            ]
        )
        require(
            intake.get("receipt_set_digest") == expected_set_digest,
            "indra_intake_receipt_set_digest_invalid",
        )
        require(
            list(intake.get("receipt_kinds", []))
            == list(REQUIRED_RECEIPT_KINDS),
            "indra_intake_receipt_kinds_invalid",
        )
        require(
            intake.get("all_required_receipts_present") is True,
            "indra_intake_completeness_flag_invalid",
        )
        require(
            intake.get("all_receipts_hash_bound") is all_hash_bound,
            "indra_intake_hash_bound_flag_invalid",
        )
        require(
            intake.get("dependency_chain_valid") is dependency_valid,
            "indra_intake_dependency_flag_invalid",
        )
        for key in (
            "branch_preserving",
            "history_preserving",
            "request_only_boundary_preserved",
            "schema_level_request_satisfied",
            "semantic_review_required",
        ):
            require(intake.get(key) is True, f"indra_intake_{key}_invalid")
        for key in (
            "runtime_transport_realized",
            "physical_transport_verified",
            "exact_world_identity_asserted",
            "world_updated",
            "branch_collapsed",
            "history_overwritten",
        ):
            require(intake.get(key) is False, f"indra_intake_{key}_forbidden")
        require(
            intake.get("disposition")
            == (
                "EXTERNAL_ANALYTIC_RECEIPTS_HASH_BOUND_"
                "SEMANTIC_REVIEW_REQUIRED"
            ),
            "indra_intake_disposition_invalid",
        )
        require(
            dict(intake.get("intake_non_authority", {}))
            == INTAKE_NON_AUTHORITY,
            "indra_intake_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_fixture_indra_transport_receipt_intake(root: Path) -> dict[str, Any]:
    source = build_indra_transport_request_receipt(root / "source-v16")
    receipts_by_kind: dict[str, dict[str, Any]] = {}
    for index, kind in enumerate(REQUIRED_RECEIPT_KINDS):
        dependencies = _required_dependency_digests(kind, receipts_by_kind)
        receipt = build_external_analytic_receipt(
            kind=kind,
            source_request_receipt=source,
            issuer_id="external-analytic-fixture-issuer",
            proof_object_digest=sha(
                {"kind": kind, "fixture": "proof-object"}
            ),
            verifier_receipt_digest=sha(
                {"kind": kind, "fixture": "verifier-receipt"}
            ),
            dependency_receipt_digests=dependencies,
            issued_at_ms=100_000 + index,
            fixture_only=True,
        )
        receipts_by_kind[kind] = receipt
    return build_indra_transport_receipt_intake(
        source_request_receipt=source,
        external_receipts=[receipts_by_kind[kind] for kind in REQUIRED_RECEIPT_KINDS],
    )
