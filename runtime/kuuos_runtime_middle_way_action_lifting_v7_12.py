#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_middle_way_action_lifting_v7_12"
PLAN_VERSION = "kuuos_middle_way_action_lifting_plan_v7_12"
INPUT_VERSION = "kuuos_middle_way_action_candidates_input_v7_12"
SOURCE_VERSION = "kuuos_runtime_two_truths_noncollapse_v7_11"

READY = "KUUOS_MIDDLE_WAY_ACTION_LIFTING_READY"
PARTIAL = "KUUOS_MIDDLE_WAY_ACTION_LIFTING_PARTIAL"
BLOCKED = "KUUOS_MIDDLE_WAY_ACTION_LIFTING_BLOCKED"

EXECUTE_EXACT = "licensed_execution_candidate_exact_world"
EXECUTE_TRANSFERRED = "licensed_execution_candidate_transferred_world"
EXECUTE_WORLD_INDEPENDENT = "licensed_execution_candidate_world_independent"
BOUNDED_PROBE = "bounded_probe_candidate"
READY_NOT_REQUESTED = "execution_eligible_not_requested"
FRESH_AUTHORITY_REQUIRED = "fresh_authority_required"
AUTHORITY_RENEWAL_REQUIRED = "authority_renewal_or_replan_required"
EVIDENCE_REQUIRED = "evidence_required"
REVIEW_REQUIRED = "review_required"
WORLD_RESOLUTION_REQUIRED = "world_transfer_or_reconciliation_required"
REPLAN_REQUIRED = "review_or_replan_required"
ADVISORY_CANDIDATE = "advisory_or_plan_candidate"
EXPLICIT_PROHIBITION = "explicitly_prohibited"

PARAMARTHA_STABLE = "paramartha_equivalence_available"
SAMVRTI_OBSERVED = "observed"

AUTHORITY_STATES = {"valid", "absent", "held", "expired", "revoked"}
WORLD_DEPENDENCE = {"none", "contextual", "strong"}
TRANSFER_MODES = {"none", "certified", "action_invariant", "bounded_probe"}
EFFECT_MODES = {
    "read_only",
    "reversible_effect",
    "compensable_effect",
    "noncompensable_effect",
}


@dataclass(frozen=True)
class MiddleWayActionLiftingResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_count: int
    execution_candidate_count: int
    bounded_probe_count: int
    authority_required_count: int
    world_resolution_count: int
    review_or_replan_count: int
    advisory_count: int
    prohibited_count: int
    output_path: str
    receipt_path: str
    audit_path: str
    output_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def _b(value: Any, name: str, blockers: list[str]) -> bool:
    if not isinstance(value, bool):
        blockers.append(name + "_must_be_bool")
        return False
    return value


def _f(value: Any, name: str, blockers: list[str]) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        blockers.append(name + "_must_be_number")
        return 0.0
    out = float(value)
    if out < 0.0 or out > 1.0:
        blockers.append(name + "_out_of_range")
    return max(0.0, min(1.0, out))


def _strings(value: Any, name: str, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append(name + "_must_be_list")
        return []
    out = [str(item).strip() for item in value if str(item).strip()]
    if len(out) != len(set(out)):
        blockers.append(name + "_duplicates")
    return sorted(set(out))


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> dict[str, float]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("direct_execution_request_is_block_reason") is not False:
        blockers.append("direct_execution_request_block_reason_must_be_false")
    if plan.get("paramartha_only_action_is_automatically_blocked") is not False:
        blockers.append("paramartha_only_auto_block_must_be_false")
    if plan.get("world_binding_mismatch_is_automatically_blocked") is not False:
        blockers.append("world_mismatch_auto_block_must_be_false")
    if plan.get("fresh_external_authority_required_for_effect") is not True:
        blockers.append("fresh_external_authority_requirement_not_true")
    if plan.get("runtime_assessment_executes_action") is not False:
        blockers.append("runtime_assessment_executes_action_must_be_false")

    keys = (
        "maximum_execution_risk",
        "minimum_execution_reversibility",
        "minimum_execution_recoverability",
        "maximum_execution_impact",
        "probe_maximum_risk",
        "probe_minimum_reversibility",
        "probe_minimum_recoverability",
        "probe_maximum_impact",
        "noncompensable_maximum_impact",
    )
    thresholds: dict[str, float] = {}
    for key in keys:
        thresholds[key] = _f(plan.get(key), key, blockers)
    return thresholds


def _source_subjects(
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = source.get("semantic_subjects", [])
    if not isinstance(raw, list):
        blockers.append("source_semantic_subjects_not_list")
        return {}

    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"source_subject_{index}_not_object")
            continue
        subject_id = str(item.get("semantic_subject_id", "")).strip()
        if not subject_id:
            blockers.append(f"source_subject_{index}_id_missing")
            continue
        if subject_id in result:
            blockers.append("duplicate_source_subject_id")
            continue
        result[subject_id] = {
            "semantic_subject_id": subject_id,
            "paramartha_state": str(item.get("paramartha_state", "")),
            "paramartha_carrier_element_id": str(
                item.get("paramartha_carrier_element_id", "")
            ),
            "samvrti_world_id": str(item.get("samvrti_world_id", "")),
            "samvrti_state": str(item.get("samvrti_state", "")),
            "samvrti_operational_signature": str(
                item.get("samvrti_operational_signature", "")
            ),
            "lineage_digest": str(item.get("lineage_digest", "")),
        }
    return result


def _authority_record(
    raw: Mapping[str, Any],
    *,
    action_class: str,
    effective_world_id: str,
    blockers: list[str],
    prefix: str,
) -> dict[str, Any]:
    state = str(raw.get("state", "")).strip()
    if state not in AUTHORITY_STATES:
        blockers.append(prefix + "_authority_state_invalid")
    fresh = _b(raw.get("fresh"), prefix + "_authority_fresh", blockers)
    authorization_digest = str(raw.get("authorization_digest", "")).strip()
    lease_digest = str(raw.get("capability_lease_digest", "")).strip()
    authorized_world_ids = _strings(
        raw.get("authorized_world_ids", []),
        prefix + "_authorized_world_ids",
        blockers,
    )
    authorized_action_classes = _strings(
        raw.get("authorized_action_classes", []),
        prefix + "_authorized_action_classes",
        blockers,
    )
    probe_authorized = _b(
        raw.get("probe_authorized"),
        prefix + "_probe_authorized",
        blockers,
    )

    digest_complete = bool(authorization_digest and lease_digest)
    action_covered = (
        "*" in authorized_action_classes or action_class in authorized_action_classes
    )
    world_covered = (
        "*" in authorized_world_ids
        or "WORLD_INDEPENDENT" in authorized_world_ids
        and effective_world_id == "WORLD_INDEPENDENT"
        or effective_world_id in authorized_world_ids
    )
    valid = (
        state == "valid"
        and fresh
        and digest_complete
        and action_covered
        and world_covered
    )
    return {
        "authority_state": state,
        "fresh": fresh,
        "authorization_digest": authorization_digest,
        "capability_lease_digest": lease_digest,
        "action_covered": action_covered,
        "world_covered": world_covered,
        "probe_authorized": probe_authorized,
        "valid_for_action_and_world": valid,
    }


def _execution_fit(
    *,
    risk: float,
    reversibility: float,
    recoverability: float,
    impact: float,
    effect_mode: str,
    thresholds: Mapping[str, float],
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if risk > thresholds["maximum_execution_risk"]:
        reasons.append("execution_risk_above_threshold")
    if reversibility < thresholds["minimum_execution_reversibility"]:
        reasons.append("execution_reversibility_below_threshold")
    if recoverability < thresholds["minimum_execution_recoverability"]:
        reasons.append("execution_recoverability_below_threshold")
    if impact > thresholds["maximum_execution_impact"]:
        reasons.append("execution_impact_above_threshold")
    if (
        effect_mode == "noncompensable_effect"
        and impact > thresholds["noncompensable_maximum_impact"]
    ):
        reasons.append("noncompensable_impact_above_threshold")
    return not reasons, reasons


def _probe_fit(
    *,
    risk: float,
    reversibility: float,
    recoverability: float,
    impact: float,
    thresholds: Mapping[str, float],
) -> bool:
    return (
        risk <= thresholds["probe_maximum_risk"]
        and reversibility >= thresholds["probe_minimum_reversibility"]
        and recoverability >= thresholds["probe_minimum_recoverability"]
        and impact <= thresholds["probe_maximum_impact"]
    )


def _assess_action(
    raw: Mapping[str, Any],
    *,
    index: int,
    subjects: Mapping[str, Mapping[str, Any]],
    thresholds: Mapping[str, float],
    blockers: list[str],
) -> dict[str, Any]:
    prefix = f"action_{index}"
    action_id = str(raw.get("action_id", "")).strip()
    subject_id = str(raw.get("semantic_subject_id", "")).strip()
    action_class = str(raw.get("action_class", "")).strip()
    effect_mode = str(raw.get("effect_mode", "")).strip()
    world_dependence = str(raw.get("world_dependence", "")).strip()
    transfer_mode = str(raw.get("transfer_mode", "none")).strip()

    if not action_id:
        blockers.append(prefix + "_id_missing")
    if not subject_id:
        blockers.append(prefix + "_subject_id_missing")
    if subject_id not in subjects:
        blockers.append(prefix + "_unknown_subject_id")
    if not action_class:
        blockers.append(prefix + "_action_class_missing")
    if effect_mode not in EFFECT_MODES:
        blockers.append(prefix + "_effect_mode_invalid")
    if world_dependence not in WORLD_DEPENDENCE:
        blockers.append(prefix + "_world_dependence_invalid")
    if transfer_mode not in TRANSFER_MODES:
        blockers.append(prefix + "_transfer_mode_invalid")

    direct_requested = _b(
        raw.get("direct_execution_requested"),
        prefix + "_direct_execution_requested",
        blockers,
    )
    invariant_across_worlds = _b(
        raw.get("action_invariant_across_samvrti"),
        prefix + "_action_invariant_across_samvrti",
        blockers,
    )
    requires_human_review = _b(
        raw.get("requires_human_review"),
        prefix + "_requires_human_review",
        blockers,
    )
    explicitly_prohibited = _b(
        raw.get("explicitly_prohibited"),
        prefix + "_explicitly_prohibited",
        blockers,
    )

    risk = _f(raw.get("estimated_risk"), prefix + "_estimated_risk", blockers)
    reversibility = _f(
        raw.get("reversibility"), prefix + "_reversibility", blockers
    )
    recoverability = _f(
        raw.get("recoverability"), prefix + "_recoverability", blockers
    )
    impact = _f(raw.get("impact_radius"), prefix + "_impact_radius", blockers)

    required_evidence = set(
        _strings(
            raw.get("required_evidence_digests", []),
            prefix + "_required_evidence_digests",
            blockers,
        )
    )
    available_evidence = set(
        _strings(
            raw.get("available_evidence_digests", []),
            prefix + "_available_evidence_digests",
            blockers,
        )
    )
    evidence_complete = required_evidence.issubset(available_evidence)

    subject = subjects.get(subject_id, {})
    paramartha_stable = subject.get("paramartha_state") == PARAMARTHA_STABLE
    source_world_observed = subject.get("samvrti_state") == SAMVRTI_OBSERVED
    source_world_id = str(subject.get("samvrti_world_id", ""))
    target_world_id = str(raw.get("target_samvrti_world_id", "")).strip()
    transfer_witness_digest = str(raw.get("transfer_witness_digest", "")).strip()

    if world_dependence == "none":
        effective_world_id = "WORLD_INDEPENDENT"
        world_relation = "world_independent"
        world_usable = True
    elif source_world_observed:
        if not target_world_id:
            target_world_id = source_world_id
        effective_world_id = target_world_id
        if target_world_id == source_world_id:
            world_relation = "exact_world"
            world_usable = True
        else:
            certified = (
                transfer_mode == "certified" and bool(transfer_witness_digest)
            )
            invariant_transfer = (
                transfer_mode == "action_invariant" and invariant_across_worlds
            )
            if certified or invariant_transfer:
                world_relation = "transferred_world"
                world_usable = True
            else:
                world_relation = "world_mismatch"
                world_usable = False
    else:
        effective_world_id = target_world_id or "UNRESOLVED_WORLD"
        if invariant_across_worlds and world_dependence != "strong":
            world_relation = "paramartha_supported_world_invariant"
            world_usable = True
        else:
            world_relation = "world_unresolved"
            world_usable = False

    authority_raw = _m(raw.get("authority"))
    authority = _authority_record(
        authority_raw,
        action_class=action_class,
        effective_world_id=effective_world_id,
        blockers=blockers,
        prefix=prefix,
    )

    execution_fit, fit_reasons = _execution_fit(
        risk=risk,
        reversibility=reversibility,
        recoverability=recoverability,
        impact=impact,
        effect_mode=effect_mode,
        thresholds=thresholds,
    )
    probe_fit = _probe_fit(
        risk=risk,
        reversibility=reversibility,
        recoverability=recoverability,
        impact=impact,
        thresholds=thresholds,
    )

    reasons: list[str] = []
    if not paramartha_stable:
        reasons.append("paramartha_basis_not_stable")
    if not evidence_complete:
        reasons.append("required_evidence_missing")
    reasons.extend(fit_reasons)

    if explicitly_prohibited:
        route = EXPLICIT_PROHIBITION
        reasons.append("explicit_prohibition")
    elif requires_human_review:
        route = REVIEW_REQUIRED
        reasons.append("human_review_required")
    elif not evidence_complete:
        route = EVIDENCE_REQUIRED
    elif authority["authority_state"] in {"expired", "revoked"}:
        route = AUTHORITY_RENEWAL_REQUIRED
        reasons.append("authority_expired_or_revoked")
    elif direct_requested:
        if authority["valid_for_action_and_world"] and world_usable and execution_fit:
            if world_relation == "exact_world":
                route = EXECUTE_EXACT
            elif world_relation in {
                "transferred_world",
                "paramartha_supported_world_invariant",
            }:
                route = EXECUTE_TRANSFERRED
            else:
                route = EXECUTE_WORLD_INDEPENDENT
        elif (
            authority["valid_for_action_and_world"]
            and authority["probe_authorized"]
            and probe_fit
            and world_relation in {"world_mismatch", "world_unresolved"}
        ):
            route = BOUNDED_PROBE
            reasons.append("world_binding_resolved_by_bounded_probe_candidate")
        elif authority["authority_state"] in {"absent", "held"} or not authority[
            "valid_for_action_and_world"
        ]:
            route = FRESH_AUTHORITY_REQUIRED
            reasons.append("fresh_action_world_authority_required")
        elif not world_usable:
            route = WORLD_RESOLUTION_REQUIRED
            reasons.append("world_transfer_or_reconciliation_required")
        else:
            route = REPLAN_REQUIRED
            reasons.append("execution_conditions_not_yet_sufficient")
    else:
        if authority["valid_for_action_and_world"] and world_usable and execution_fit:
            route = READY_NOT_REQUESTED
        elif probe_fit and world_relation in {"world_mismatch", "world_unresolved"}:
            route = BOUNDED_PROBE if authority["probe_authorized"] else ADVISORY_CANDIDATE
        elif not world_usable and world_dependence != "none":
            route = ADVISORY_CANDIDATE
            reasons.append("world_binding_not_yet_actionable")
        else:
            route = ADVISORY_CANDIDATE

    execution_candidate = route in {
        EXECUTE_EXACT,
        EXECUTE_TRANSFERRED,
        EXECUTE_WORLD_INDEPENDENT,
        READY_NOT_REQUESTED,
    }

    return {
        "action_id": action_id,
        "action_digest": _sha(
            {
                "action_id": action_id,
                "semantic_subject_id": subject_id,
                "action_class": action_class,
                "effect_mode": effect_mode,
                "target_samvrti_world_id": target_world_id,
                "world_dependence": world_dependence,
                "transfer_mode": transfer_mode,
            }
        ),
        "semantic_subject_id": subject_id,
        "paramartha_basis_stable": paramartha_stable,
        "paramartha_carrier_element_id": str(
            subject.get("paramartha_carrier_element_id", "")
        ),
        "source_samvrti_world_id": source_world_id,
        "target_samvrti_world_id": target_world_id,
        "world_relation": world_relation,
        "world_usable_for_requested_action": world_usable,
        "world_dependence": world_dependence,
        "action_invariant_across_samvrti": invariant_across_worlds,
        "transfer_mode": transfer_mode,
        "transfer_witness_present": bool(transfer_witness_digest),
        "direct_execution_requested": direct_requested,
        "action_class": action_class,
        "effect_mode": effect_mode,
        "estimated_risk": risk,
        "reversibility": reversibility,
        "recoverability": recoverability,
        "impact_radius": impact,
        "evidence_complete": evidence_complete,
        "requires_human_review": requires_human_review,
        "authority_state": authority["authority_state"],
        "fresh_authority": authority["fresh"],
        "authority_action_covered": authority["action_covered"],
        "authority_world_covered": authority["world_covered"],
        "authority_valid_for_action_and_world": authority[
            "valid_for_action_and_world"
        ],
        "probe_authorized": authority["probe_authorized"],
        "execution_fit": execution_fit,
        "bounded_probe_fit": probe_fit,
        "action_route": route,
        "execution_candidate": execution_candidate,
        "reasons": sorted(set(reasons)),
        "direct_execution_request_was_not_used_as_block_reason": True,
        "world_mismatch_was_not_used_as_automatic_block_reason": True,
        "paramartha_only_was_not_used_as_automatic_block_reason": True,
        "assessment_executes_action": False,
    }


def build_middle_way_action_lifting(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> MiddleWayActionLiftingResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "middle_way_action_lifting_plan_v7_12.json"
    source_path = root / "two_truths_noncollapse_packet_v7_11.json"
    input_path = root / "middle_way_action_candidates_input_v7_12.json"
    output_path = root / "middle_way_action_lifting_packet_v7_12.json"
    receipt_path = root / "middle_way_action_lifting_receipt_v7_12.json"
    audit_path = root / "middle_way_action_lifting_audit_v7_12.jsonl"

    if ctx.get("middle_way_action_lifting_enabled") is not True:
        blockers.append("middle_way_action_lifting_enabled_not_true")
    if ctx.get("apply_middle_way_action_lifting") is not True:
        blockers.append("apply_middle_way_action_lifting_not_true")
    if authority_packet.get("authority_status") != "KUUOS_MIDDLE_WAY_ACTION_LIFTING_AUTHORITY_READY":
        blockers.append("middle_way_action_lifting_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "source_two_truths_packet_read_allowed",
        "action_candidates_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    action_packet = _read_json(input_path)

    thresholds: dict[str, float] = {}
    if not plan:
        blockers.append("middle_way_action_plan_missing_or_invalid")
    else:
        thresholds = _validate_plan(plan, blockers)

    if not source:
        blockers.append("two_truths_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("two_truths_packet_version_invalid")

    if not action_packet:
        blockers.append("action_candidates_input_missing_or_invalid")
    elif action_packet.get("version") != INPUT_VERSION:
        blockers.append("action_candidates_input_version_invalid")

    if plan and source and action_packet:
        source_digest = _sha(source)
        if str(plan.get("source_two_truths_packet_digest", "")) != source_digest:
            blockers.append("source_two_truths_packet_digest_mismatch")
        if (
            str(action_packet.get("source_two_truths_packet_digest", ""))
            != source_digest
        ):
            blockers.append("actions_source_two_truths_packet_digest_mismatch")

        boundary = _m(source.get("two_truths_boundary"))
        if boundary.get("paramartha_and_samvrti_are_separate_surfaces") is not True:
            blockers.append("source_two_truths_separation_missing")
        if boundary.get("same_paramartha_does_not_imply_conventional_substitutability") is not True:
            blockers.append("source_noncollapse_boundary_missing")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("source_authority_boundary_invalid")

    subjects = _source_subjects(source, blockers) if source else {}

    raw_actions = action_packet.get("actions", []) if action_packet else []
    if action_packet and not isinstance(raw_actions, list):
        blockers.append("actions_not_list")
        raw_actions = []
    if action_packet and not raw_actions:
        blockers.append("actions_empty")

    assessments: list[dict[str, Any]] = []
    seen_action_ids: set[str] = set()
    if not blockers:
        for index, raw in enumerate(raw_actions):
            if not isinstance(raw, Mapping):
                blockers.append(f"action_{index}_not_object")
                continue
            assessment = _assess_action(
                raw,
                index=index,
                subjects=subjects,
                thresholds=thresholds,
                blockers=blockers,
            )
            action_id = assessment["action_id"]
            if action_id in seen_action_ids:
                blockers.append("duplicate_action_id")
            seen_action_ids.add(action_id)
            assessments.append(assessment)

    route_counts = {
        "execution": sum(1 for a in assessments if a["execution_candidate"]),
        "probe": sum(1 for a in assessments if a["action_route"] == BOUNDED_PROBE),
        "authority": sum(
            1
            for a in assessments
            if a["action_route"] in {FRESH_AUTHORITY_REQUIRED, AUTHORITY_RENEWAL_REQUIRED}
        ),
        "world": sum(
            1 for a in assessments if a["action_route"] == WORLD_RESOLUTION_REQUIRED
        ),
        "review": sum(
            1
            for a in assessments
            if a["action_route"] in {REVIEW_REQUIRED, REPLAN_REQUIRED, EVIDENCE_REQUIRED}
        ),
        "advisory": sum(
            1 for a in assessments if a["action_route"] == ADVISORY_CANDIDATE
        ),
        "prohibited": sum(
            1 for a in assessments if a["action_route"] == EXPLICIT_PROHIBITION
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        unresolved = (
            route_counts["authority"]
            + route_counts["world"]
            + route_counts["review"]
        )
        status = PARTIAL if unresolved > 0 else READY
        output = {
            "version": VERSION,
            "status": status,
            "source_two_truths_packet_digest": _sha(source),
            "action_assessments": assessments,
            "summary": {
                "action_count": len(assessments),
                "execution_candidate_count": route_counts["execution"],
                "bounded_probe_count": route_counts["probe"],
                "authority_required_count": route_counts["authority"],
                "world_resolution_count": route_counts["world"],
                "review_or_replan_count": route_counts["review"],
                "advisory_count": route_counts["advisory"],
                "prohibited_count": route_counts["prohibited"],
            },
            "middle_way_action_boundary": {
                "direct_execution_request_is_block_reason": False,
                "paramartha_only_action_is_automatically_blocked": False,
                "world_binding_mismatch_is_automatically_blocked": False,
                "fresh_external_authority_required_for_effect": True,
                "paramartha_meaning_does_not_grant_execution_authority": True,
                "world_transfer_witness_can_support_cross_world_lifting": True,
                "world_invariant_action_can_cross_samvrti_presentations": True,
                "bounded_reversible_probe_can_resolve_world_uncertainty": True,
                "direct_execution_request_can_become_licensed_candidate": True,
                "runtime_assessment_executes_action": False,
                "transactional_effect_reconciliation_still_required_after_effect": True,
                "execution_success_does_not_imply_mission_success": True,
            },
            "formal_and_runtime_references": {
                "decision_os": "runtime/kuuos_decision_os_phase_v0_1.py",
                "two_truths": "runtime/kuuos_runtime_two_truths_noncollapse_v7_11.py",
                "transactional_effects": "docs/KUUOS_TRANSACTIONAL_EFFECT_RECONCILIATION_KERNEL_v0_24.md",
                "autonomous_architecture": "docs/KUUOS_AUTONOMOUS_AGENT_COMPLETION_ARCHITECTURE_v0_19.md",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-middle-way-action-lifting-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "actions_digest": _sha(action_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "action_count": len(assessments),
        "execution_candidate_count": route_counts["execution"],
        "bounded_probe_count": route_counts["probe"],
        "authority_required_count": route_counts["authority"],
        "world_resolution_count": route_counts["world"],
        "review_or_replan_count": route_counts["review"],
        "advisory_count": route_counts["advisory"],
        "prohibited_count": route_counts["prohibited"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "direct_execution_request_is_block_reason": False,
        "paramartha_only_action_is_automatically_blocked": False,
        "world_binding_mismatch_is_automatically_blocked": False,
        "assessment_executes_action": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return MiddleWayActionLiftingResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(assessments),
        route_counts["execution"],
        route_counts["probe"],
        route_counts["authority"],
        route_counts["world"],
        route_counts["review"],
        route_counts["advisory"],
        route_counts["prohibited"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
