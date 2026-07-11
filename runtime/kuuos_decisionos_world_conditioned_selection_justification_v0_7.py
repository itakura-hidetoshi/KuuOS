#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DECISIONOS_VERSION = "v0.6"
SOURCE_STATUS = "DECISIONOS_WORLD_CONDITIONED_RELATIONAL_DELIBERATION_READY"
CANDIDATE_FIELD = {
    "continue",
    "strengthen",
    "repair",
    "slow_down",
    "reobserve",
    "reroute",
    "hold",
    "terminate_candidate",
}


@dataclass
class DecisionOSWorldConditionedSelectionJustificationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _string_list(value: Any) -> tuple[bool, list[str]]:
    if not isinstance(value, list):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if len(value) != len(set(value)):
        return False, []
    return True, list(value)


def compute_source_deliberation_record_digest(record: Mapping[str, Any]) -> str:
    return canonical_digest(dict(record))


def compute_candidate_selection_justification_digest(
    item: Mapping[str, Any],
) -> str:
    payload = dict(item)
    payload.pop("candidate_selection_justification_digest", None)
    return canonical_digest(payload)


def compute_selection_bundle_digest(
    *,
    source_deliberation_receipt_digest: str,
    selection_policy_digest: str,
    selector_responsibility_digest: str,
    requested_selected_candidate_id: str,
    hold_guard_resolution_digest: str,
    candidate_selection_justification_items: list[dict],
) -> str:
    ordered = sorted(
        candidate_selection_justification_items,
        key=lambda item: str(item.get("candidate_id", "")),
    )
    return canonical_digest(
        {
            "source_deliberation_receipt_digest": source_deliberation_receipt_digest,
            "selection_policy_digest": selection_policy_digest,
            "selector_responsibility_digest": selector_responsibility_digest,
            "requested_selected_candidate_id": requested_selected_candidate_id,
            "hold_guard_resolution_digest": hold_guard_resolution_digest,
            "candidate_selection_justification_items": ordered,
        }
    )


def build_decisionos_world_conditioned_selection_justification_receipt(
    *,
    source_deliberation_receipt: Mapping[str, Any],
    selection_policy_digest: str,
    selector_responsibility_digest: str,
    requested_selected_candidate_id: str,
    hold_guard_resolution_digest: str,
    candidate_selection_justification_items: list[dict],
    selection_bundle_digest: str,
) -> DecisionOSWorldConditionedSelectionJustificationResult:
    blockers: list[str] = []
    source = (
        dict(source_deliberation_receipt)
        if isinstance(source_deliberation_receipt, Mapping)
        else {}
    )
    if not source:
        blockers.append("source_deliberation_receipt_missing")

    for name, value in {
        "selection_policy_digest": selection_policy_digest,
        "selector_responsibility_digest": selector_responsibility_digest,
        "requested_selected_candidate_id": requested_selected_candidate_id,
        "selection_bundle_digest": selection_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    if not isinstance(hold_guard_resolution_digest, str):
        blockers.append("hold_guard_resolution_digest_invalid")

    all_candidate_ids: set[str] = set()
    admissible_ids: set[str] = set()
    retained_nonadmissible_ids: set[str] = set()
    frontier_ids: set[str] = set()
    required_review_ids: set[str] = set()
    dissent_review_ids: set[str] = set()
    minority_review_ids: set[str] = set()
    uncertainty_review_ids: set[str] = set()
    evidence_blocked_ids: set[str] = set()
    record_map: dict[str, dict] = {}

    if source:
        if source.get("decisionos_version") != SOURCE_DECISIONOS_VERSION:
            blockers.append("source_decisionos_version_invalid")
        if source.get("status") != SOURCE_STATUS:
            blockers.append("source_deliberation_not_ready")
        source_digest = source.get(
            "decisionos_relational_deliberation_receipt_digest"
        )
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append("source_deliberation_receipt_digest_missing")
        else:
            unsigned = dict(source)
            unsigned.pop(
                "decisionos_relational_deliberation_receipt_digest",
                None,
            )
            if source_digest != canonical_digest(unsigned):
                blockers.append("source_deliberation_receipt_digest_mismatch")

        required_true = (
            "source_probability_used_as_advisory_only",
            "source_action_used_as_advisory_only",
            "relational_partial_order_used",
            "single_scalar_utility_selection_forbidden",
            "all_candidates_considered",
            "candidate_identity_preserved",
            "retained_alternatives_preserved",
            "wa_evidence_preserved",
            "stakeholder_context_preserved",
            "relational_context_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "relational_deliberation_performed",
            "decisionos_owns_selection",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "world_mutation_not_granted",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        )
        required_false = (
            "silent_substitution_detected",
            "selection_authority_granted_by_deliberation",
            "decision_selection_performed",
            "decision_receipt_issued",
            "plan_synthesis_performed",
            "active_now",
            "execution_permission",
        )
        for name in required_true:
            if source.get(name) is not True:
                blockers.append(f"source_boundary_{name}_missing")
        for name in required_false:
            if source.get(name) is not False:
                blockers.append(f"source_boundary_{name}_promoted")
        if source.get("selected_candidate_id") != "":
            blockers.append("source_selected_candidate_forbidden")

        for name in (
            "source_intake_receipt_digest",
            "source_planos_handoff_certificate_digest",
            "source_world_binding_digest",
            "source_world_model_state_digest",
            "source_world_lineage_digest",
            "deliberation_policy_digest",
            "deliberation_bundle_digest",
        ):
            if not isinstance(source.get(name), str) or not source.get(name):
                blockers.append(f"source_{name}_missing")
        revision = source.get("source_world_model_revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
            blockers.append("source_world_model_revision_invalid")

        all_ids = source.get("all_candidate_ids")
        admissible = source.get("admissible_candidate_ids")
        nonadmissible = source.get("retained_nonadmissible_candidate_ids")
        frontier = source.get("relational_frontier_candidate_ids")
        required_review = source.get("required_review_candidate_ids")
        if (
            not isinstance(all_ids, list)
            or not all_ids
            or len(all_ids) != len(set(all_ids))
            or any(item not in CANDIDATE_FIELD for item in all_ids)
        ):
            blockers.append("source_all_candidate_ids_invalid")
        else:
            all_candidate_ids = set(all_ids)
        if (
            not isinstance(admissible, list)
            or not admissible
            or len(admissible) != len(set(admissible))
            or any(item not in all_candidate_ids for item in admissible)
        ):
            blockers.append("source_admissible_candidate_ids_invalid")
        else:
            admissible_ids = set(admissible)
        if (
            not isinstance(nonadmissible, list)
            or set(nonadmissible) != all_candidate_ids - admissible_ids
        ):
            blockers.append("source_retained_nonadmissible_ids_mismatch")
        else:
            retained_nonadmissible_ids = set(nonadmissible)
        if (
            not isinstance(frontier, list)
            or not frontier
            or len(frontier) != len(set(frontier))
            or any(item not in admissible_ids for item in frontier)
        ):
            blockers.append("source_relational_frontier_invalid")
        else:
            frontier_ids = set(frontier)
        if (
            not isinstance(required_review, list)
            or len(required_review) != len(set(required_review))
            or any(item not in all_candidate_ids for item in required_review)
        ):
            blockers.append("source_required_review_candidate_ids_invalid")
        else:
            required_review_ids = set(required_review)

        review_fields = {
            "dissent_review_candidate_ids": dissent_review_ids,
            "minority_protection_candidate_ids": minority_review_ids,
            "uncertainty_review_candidate_ids": uncertainty_review_ids,
            "evidence_blocked_candidate_ids": evidence_blocked_ids,
        }
        for field, target in review_fields.items():
            value = source.get(field)
            if (
                not isinstance(value, list)
                or len(value) != len(set(value))
                or any(item not in all_candidate_ids for item in value)
            ):
                blockers.append(f"source_{field}_invalid")
            else:
                target.update(value)

        records = source.get("candidate_deliberation_records")
        if not isinstance(records, list) or len(records) != len(all_candidate_ids):
            blockers.append("source_candidate_deliberation_records_incomplete")
        else:
            for index, raw_record in enumerate(records):
                if not isinstance(raw_record, dict):
                    blockers.append(
                        f"source_candidate_deliberation_record_invalid_{index}"
                    )
                    continue
                candidate_id = raw_record.get("candidate_id")
                if (
                    not isinstance(candidate_id, str)
                    or candidate_id not in all_candidate_ids
                ):
                    blockers.append(
                        f"source_candidate_deliberation_id_invalid_{index}"
                    )
                    continue
                if candidate_id in record_map:
                    blockers.append(
                        "source_candidate_deliberation_id_duplicate"
                    )
                record = dict(raw_record)
                record_map[candidate_id] = record
                if record.get("source_admissible") is not (
                    candidate_id in admissible_ids
                ):
                    blockers.append(
                        f"source_candidate_admissibility_mismatch_{candidate_id}"
                    )
                if candidate_id in frontier_ids and (
                    record.get("relationally_reviewable") is not True
                ):
                    blockers.append(
                        f"source_frontier_candidate_not_reviewable_{candidate_id}"
                    )
            if set(record_map) != all_candidate_ids:
                blockers.append(
                    "source_candidate_deliberation_record_field_not_complete"
                )

        if source.get("hold_guard_active") is True:
            if (
                "hold" not in admissible_ids
                or "hold" not in required_review_ids
            ):
                blockers.append("source_hold_guard_inconsistent")
            if not hold_guard_resolution_digest:
                blockers.append("hold_guard_resolution_digest_missing")
        elif source.get("hold_guard_active") is not False:
            blockers.append("source_hold_guard_flag_invalid")
        elif hold_guard_resolution_digest:
            blockers.append("hold_guard_resolution_digest_forbidden")

    if requested_selected_candidate_id:
        if requested_selected_candidate_id not in all_candidate_ids:
            blockers.append("requested_selected_candidate_outside_field")
        if requested_selected_candidate_id not in admissible_ids:
            blockers.append("requested_selected_candidate_not_admissible")
        if requested_selected_candidate_id not in frontier_ids:
            blockers.append(
                "requested_selected_candidate_not_relational_frontier"
            )

    if (
        not isinstance(candidate_selection_justification_items, list)
        or not candidate_selection_justification_items
    ):
        blockers.append("candidate_selection_justification_items_empty")
        raw_items: list[dict] = []
    else:
        raw_items = list(candidate_selection_justification_items)

    required_item_fields = {
        "candidate_id",
        "source_deliberation_record_digest",
        "selected",
        "support_rationale_digests",
        "opposition_rationale_digests",
        "dissent_preservation_digests",
        "minority_preservation_digests",
        "review_resolution_digests",
        "nonselection_reason_digest",
        "candidate_selection_justification_digest",
    }
    item_map: dict[str, dict] = {}
    selected_flags: list[str] = []
    for index, raw_item in enumerate(raw_items):
        if (
            not isinstance(raw_item, dict)
            or set(raw_item) != required_item_fields
        ):
            blockers.append(
                f"candidate_selection_justification_schema_invalid_{index}"
            )
            continue
        item = dict(raw_item)
        candidate_id = item.get("candidate_id")
        if (
            not isinstance(candidate_id, str)
            or candidate_id not in all_candidate_ids
        ):
            blockers.append(
                f"candidate_selection_justification_id_invalid_{index}"
            )
            continue
        if candidate_id in item_map:
            blockers.append(
                "candidate_selection_justification_id_duplicate"
            )
        item_map[candidate_id] = item
        source_record = record_map.get(candidate_id)
        if source_record is not None:
            if item.get(
                "source_deliberation_record_digest"
            ) != compute_source_deliberation_record_digest(source_record):
                blockers.append(
                    f"candidate_source_record_digest_mismatch_{candidate_id}"
                )

        list_values: dict[str, list[str]] = {}
        for field in (
            "support_rationale_digests",
            "opposition_rationale_digests",
            "dissent_preservation_digests",
            "minority_preservation_digests",
            "review_resolution_digests",
        ):
            valid, values = _string_list(item.get(field))
            if not valid:
                blockers.append(
                    f"candidate_{field}_invalid_{candidate_id}"
                )
            list_values[field] = values

        if not isinstance(item.get("selected"), bool):
            blockers.append(f"candidate_selected_flag_invalid_{candidate_id}")
        elif item["selected"]:
            selected_flags.append(candidate_id)
            if candidate_id != requested_selected_candidate_id:
                blockers.append(
                    f"candidate_selected_flag_mismatch_{candidate_id}"
                )
            if not list_values["support_rationale_digests"]:
                blockers.append(
                    f"selected_candidate_support_rationale_missing_{candidate_id}"
                )
            if item.get("nonselection_reason_digest") != "":
                blockers.append(
                    f"selected_candidate_nonselection_reason_forbidden_{candidate_id}"
                )
            if candidate_id not in frontier_ids:
                blockers.append(
                    f"selected_candidate_not_frontier_{candidate_id}"
                )
            if source_record and source_record.get(
                "relationally_reviewable"
            ) is not True:
                blockers.append(
                    f"selected_candidate_not_reviewable_{candidate_id}"
                )
        else:
            reason = item.get("nonselection_reason_digest")
            if not isinstance(reason, str) or not reason:
                blockers.append(
                    f"nonselected_candidate_reason_missing_{candidate_id}"
                )

        if candidate_id in dissent_review_ids and not list_values[
            "dissent_preservation_digests"
        ]:
            blockers.append(
                f"candidate_dissent_preservation_missing_{candidate_id}"
            )
        if candidate_id in minority_review_ids and not list_values[
            "minority_preservation_digests"
        ]:
            blockers.append(
                f"candidate_minority_preservation_missing_{candidate_id}"
            )
        if item.get(
            "candidate_selection_justification_digest"
        ) != compute_candidate_selection_justification_digest(item):
            blockers.append(
                f"candidate_selection_justification_digest_mismatch_{candidate_id}"
            )

    if set(item_map) != all_candidate_ids:
        blockers.append("candidate_selection_justification_field_not_complete")
    if selected_flags != [requested_selected_candidate_id]:
        blockers.append("selected_candidate_flag_not_unique")

    if not blockers:
        expected_bundle = compute_selection_bundle_digest(
            source_deliberation_receipt_digest=source[
                "decisionos_relational_deliberation_receipt_digest"
            ],
            selection_policy_digest=selection_policy_digest,
            selector_responsibility_digest=selector_responsibility_digest,
            requested_selected_candidate_id=requested_selected_candidate_id,
            hold_guard_resolution_digest=hold_guard_resolution_digest,
            candidate_selection_justification_items=list(item_map.values()),
        )
        if selection_bundle_digest != expected_bundle:
            blockers.append("selection_bundle_digest_mismatch")

    if blockers:
        return DecisionOSWorldConditionedSelectionJustificationResult(
            STATUS_BLOCKED,
            sorted(set(blockers)),
            None,
        )

    normalized_items = [
        item_map[candidate_id] for candidate_id in sorted(item_map)
    ]
    selected_item = item_map[requested_selected_candidate_id]
    retained_alternatives = sorted(
        admissible_ids - {requested_selected_candidate_id}
    )
    nonselection_reason_map = {
        candidate_id: item_map[candidate_id]["nonselection_reason_digest"]
        for candidate_id in sorted(
            all_candidate_ids - {requested_selected_candidate_id}
        )
    }
    dissent_preservation_map = {
        candidate_id: list(
            item_map[candidate_id]["dissent_preservation_digests"]
        )
        for candidate_id in sorted(dissent_review_ids)
    }
    minority_preservation_map = {
        candidate_id: list(
            item_map[candidate_id]["minority_preservation_digests"]
        )
        for candidate_id in sorted(minority_review_ids)
    }
    review_resolution_map = {
        candidate_id: list(
            item_map[candidate_id]["review_resolution_digests"]
        )
        for candidate_id in sorted(required_review_ids)
    }

    receipt = {
        "kernel": (
            "DecisionOS WORLD-Conditioned Selection Justification Kernel"
        ),
        "kernel_version": "v0.1",
        "decisionos_version": "v0.7",
        "status": (
            "DECISIONOS_WORLD_CONDITIONED_SELECTION_JUSTIFICATION_ISSUED"
        ),
        "source_decisionos_version": source["decisionos_version"],
        "source_deliberation_receipt_digest": source[
            "decisionos_relational_deliberation_receipt_digest"
        ],
        "source_intake_receipt_digest": source[
            "source_intake_receipt_digest"
        ],
        "source_planos_handoff_certificate_digest": source[
            "source_planos_handoff_certificate_digest"
        ],
        "source_world_binding_digest": source[
            "source_world_binding_digest"
        ],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source[
            "source_world_model_revision"
        ],
        "source_world_lineage_digest": source[
            "source_world_lineage_digest"
        ],
        "selection_policy_digest": selection_policy_digest,
        "selector_responsibility_digest": selector_responsibility_digest,
        "selection_bundle_digest": selection_bundle_digest,
        "hold_guard_resolution_digest": hold_guard_resolution_digest,
        "candidate_selection_justification_items": normalized_items,
        "selected_candidate_id": requested_selected_candidate_id,
        "selected_candidate_source_record_digest": (
            selected_item["source_deliberation_record_digest"]
        ),
        "selected_candidate_support_rationale_digests": list(
            selected_item["support_rationale_digests"]
        ),
        "selected_candidate_opposition_rationale_digests": list(
            selected_item["opposition_rationale_digests"]
        ),
        "relational_frontier_candidate_ids": sorted(frontier_ids),
        "required_review_candidate_ids": sorted(required_review_ids),
        "retained_alternative_candidate_ids": retained_alternatives,
        "retained_nonadmissible_candidate_ids": sorted(
            retained_nonadmissible_ids
        ),
        "nonselection_reason_map": nonselection_reason_map,
        "dissent_preservation_map": dissent_preservation_map,
        "minority_preservation_map": minority_preservation_map,
        "review_resolution_map": review_resolution_map,
        "all_candidates_considered": True,
        "candidate_identity_preserved": True,
        "retained_alternatives_preserved": True,
        "nonselected_reasons_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "required_review_field_preserved": True,
        "silent_substitution_detected": False,
        "source_probability_used_as_advisory_only": True,
        "source_action_used_as_advisory_only": True,
        "relational_partial_order_used": True,
        "single_scalar_utility_selection_forbidden": True,
        "selected_candidate_from_relational_frontier": True,
        "selection_authority_exercised_by_decision_os": True,
        "selection_authority_inherited_from_planos": False,
        "selection_authority_inherited_from_world_model": False,
        "selection_authority_inherited_from_qi": False,
        "decision_selection_performed": True,
        "selected_candidate_present": True,
        "decision_receipt_issued": True,
        "selection_is_not_plan_synthesis": True,
        "selection_is_not_execution": True,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "plan_synthesis_performed": False,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["decisionos_selection_justification_receipt_digest"] = (
        canonical_digest(receipt)
    )
    return DecisionOSWorldConditionedSelectionJustificationResult(
        STATUS_READY,
        [],
        receipt,
    )
