from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import json
import os

from runtime import kuuos_endogenous_mission_observation_v0_31 as v031

VERSION = "v0.32"
AUTH_VERSION = "observation_authorization_receipt_v0_32"
REQUEST_VERSION = "authorized_observe_request_v0_32"
EVIDENCE_VERSION = "observation_evidence_receipt_v0_32"
FEEDBACK_VERSION = "world_feedback_candidate_v0_32"

EVIDENCE_RELATIONS = {"SUPPORTS", "CONTRADICTS", "INCONCLUSIVE", "CONFLICTED"}
FEEDBACK_ROUTES = {"WORLD_UPDATE_CANDIDATE", "REOBSERVE", "HOLD", "HANDOVER"}


def canonical_json(value: Any) -> str:
    return v031.canonical_json(value)


def digest(value: Any) -> str:
    return v031.digest(value)


def make_envelope(body: Mapping[str, Any]) -> dict[str, Any]:
    return v031.make_envelope(body)


def validate_envelope(envelope: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    return v031.validate_envelope(envelope, label=label)


def _hex_digest(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field}_invalid")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field}_invalid") from exc
    return value


def _text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _find_observation(report: Mapping[str, Any], observation_candidate_id: str) -> dict[str, Any]:
    for observation in report["observation_portfolio"]:
        if observation.get("observation_candidate_id") == observation_candidate_id:
            return observation
    raise ValueError("observation_candidate_not_found")


def _find_mission(report: Mapping[str, Any], mission_candidate_id: str) -> dict[str, Any]:
    for mission in report["mission_candidates"]:
        if mission.get("mission_candidate_id") == mission_candidate_id:
            return mission
    raise ValueError("mission_candidate_not_found")


def make_observation_authorization_receipt(
    *,
    authorization_id: str,
    source_report_envelope: Mapping[str, Any],
    observation_candidate_id: str,
    tool_id: str,
    scope_digest: str,
    host_license_digest: str,
    issued_by: str,
    issued_at_ms: int,
    not_before_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    report = v031.validate_report(source_report_envelope)
    authorization_id = _text(authorization_id, field="authorization_id")
    observation_candidate_id = _text(observation_candidate_id, field="observation_candidate_id")
    tool_id = _text(tool_id, field="tool_id")
    issued_by = _text(issued_by, field="issued_by")
    scope_digest = _hex_digest(scope_digest, field="scope_digest")
    host_license_digest = _hex_digest(host_license_digest, field="host_license_digest")
    if not all(isinstance(value, int) and value >= 0 for value in (issued_at_ms, not_before_ms, expires_at_ms)):
        raise ValueError("authorization_time_invalid")
    if not issued_at_ms <= not_before_ms < expires_at_ms:
        raise ValueError("authorization_window_invalid")
    if report["route"] != "MISSION_PORTFOLIO_READY":
        raise ValueError("report_not_ready_for_observation_authorization")
    observation = _find_observation(report, observation_candidate_id)
    if observation.get("channel_id") is None:
        raise ValueError("capability_discovery_candidate_not_authorizable")
    mission = _find_mission(report, observation["mission_candidate_id"])
    body = {
        "authorization_version": AUTH_VERSION,
        "authorization_id": authorization_id,
        "source_report_digest": source_report_envelope["body_digest"],
        "source_state_digest": report["source_state_digest"],
        "root_lineage_digest": report["root_lineage_digest"],
        "world_fragment_digest": report["world_fragment_digest"],
        "mission_candidate_id": mission["mission_candidate_id"],
        "observation_candidate_id": observation_candidate_id,
        "channel_id": observation["channel_id"],
        "tool_id": tool_id,
        "scope_digest": scope_digest,
        "host_license_digest": host_license_digest,
        "issued_by": issued_by,
        "issued_at_ms": issued_at_ms,
        "not_before_ms": not_before_ms,
        "expires_at_ms": expires_at_ms,
        "max_invocations": 1,
        "single_use": True,
        "grants_observe_invocation": True,
        "grants_actos_effect_authority": False,
        "grants_plan_activation": False,
        "grants_truth_authority": False,
        "grants_verification_authority": False,
        "grants_memory_overwrite_authority": False,
    }
    receipt = make_envelope(body)
    validate_authorization_receipt(receipt)
    return receipt


def validate_authorization_receipt(receipt_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(receipt_envelope, label="observation_authorization")
    if body.get("authorization_version") != AUTH_VERSION:
        raise ValueError("authorization_version_invalid")
    for field in (
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "world_fragment_digest",
        "scope_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "authorization_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "channel_id",
        "tool_id",
        "issued_by",
    ):
        _text(body.get(field), field=field)
    if body.get("max_invocations") != 1 or body.get("single_use") is not True:
        raise ValueError("authorization_not_single_use")
    if not (
        isinstance(body.get("issued_at_ms"), int)
        and isinstance(body.get("not_before_ms"), int)
        and isinstance(body.get("expires_at_ms"), int)
        and body["issued_at_ms"] <= body["not_before_ms"] < body["expires_at_ms"]
    ):
        raise ValueError("authorization_window_invalid")
    if body.get("grants_observe_invocation") is not True:
        raise ValueError("observe_invocation_not_granted")
    for field in (
        "grants_actos_effect_authority",
        "grants_plan_activation",
        "grants_truth_authority",
        "grants_verification_authority",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"authorization_boundary_invalid:{field}")
    return body


def build_authorized_observe_request(
    source_report_envelope: Mapping[str, Any],
    authorization_receipt_envelope: Mapping[str, Any],
    *,
    requested_at_ms: int,
) -> dict[str, Any]:
    report = v031.validate_report(source_report_envelope)
    authorization = validate_authorization_receipt(authorization_receipt_envelope)
    if authorization["source_report_digest"] != source_report_envelope.get("body_digest"):
        raise ValueError("authorization_report_mismatch")
    if authorization["source_state_digest"] != report["source_state_digest"]:
        raise ValueError("authorization_source_state_mismatch")
    if authorization["root_lineage_digest"] != report["root_lineage_digest"]:
        raise ValueError("authorization_root_lineage_mismatch")
    if authorization["world_fragment_digest"] != report["world_fragment_digest"]:
        raise ValueError("authorization_world_fragment_mismatch")
    if not isinstance(requested_at_ms, int):
        raise ValueError("requested_at_ms_invalid")
    if not authorization["not_before_ms"] <= requested_at_ms < authorization["expires_at_ms"]:
        raise ValueError("authorization_not_current")
    observation = _find_observation(report, authorization["observation_candidate_id"])
    mission = _find_mission(report, authorization["mission_candidate_id"])
    if observation["mission_candidate_id"] != mission["mission_candidate_id"]:
        raise ValueError("authorization_mission_observation_mismatch")
    if observation["channel_id"] != authorization["channel_id"]:
        raise ValueError("authorization_channel_mismatch")
    request_id = "observe-" + digest({
        "authorization_digest": authorization_receipt_envelope["body_digest"],
        "source_report_digest": source_report_envelope["body_digest"],
        "requested_at_ms": requested_at_ms,
    })[:24]
    body = {
        "request_version": REQUEST_VERSION,
        "request_id": request_id,
        "source_report_digest": source_report_envelope["body_digest"],
        "authorization_digest": authorization_receipt_envelope["body_digest"],
        "authorization_id": authorization["authorization_id"],
        "source_state_digest": report["source_state_digest"],
        "root_lineage_digest": report["root_lineage_digest"],
        "world_fragment_digest": report["world_fragment_digest"],
        "mission_candidate_id": mission["mission_candidate_id"],
        "observation_candidate_id": observation["observation_candidate_id"],
        "source_item_id": observation["source_item_id"],
        "channel_id": observation["channel_id"],
        "modality": observation["modality"],
        "tool_id": authorization["tool_id"],
        "scope_digest": authorization["scope_digest"],
        "host_license_digest": authorization["host_license_digest"],
        "requested_at_ms": requested_at_ms,
        "invocation_index": 1,
        "single_use": True,
        "expected_evidence_fields": [
            "raw_artifact_digest",
            "value_digest",
            "collector_identity",
            "independent_source_identity",
            "collected_at_ms",
            "uncertainty_digest",
            "calibration_digest",
            "context_digest",
            "tamper_evidence_digest",
            "provenance_chain_digest",
        ],
        "grants_observe_invocation": True,
        "grants_actos_effect_authority": False,
        "grants_plan_activation": False,
        "grants_truth_authority": False,
        "grants_verification_authority": False,
    }
    request = make_envelope(body)
    validate_observe_request(request)
    return request


def validate_observe_request(request_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(request_envelope, label="authorized_observe_request")
    if body.get("request_version") != REQUEST_VERSION:
        raise ValueError("request_version_invalid")
    for field in (
        "source_report_digest",
        "authorization_digest",
        "source_state_digest",
        "root_lineage_digest",
        "world_fragment_digest",
        "scope_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "request_id",
        "authorization_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "channel_id",
        "modality",
        "tool_id",
    ):
        _text(body.get(field), field=field)
    if body.get("invocation_index") != 1 or body.get("single_use") is not True:
        raise ValueError("observe_request_not_single_use")
    if body.get("grants_observe_invocation") is not True:
        raise ValueError("observe_invocation_not_granted")
    for field in (
        "grants_actos_effect_authority",
        "grants_plan_activation",
        "grants_truth_authority",
        "grants_verification_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"request_boundary_invalid:{field}")
    return body


def make_observation_evidence_receipt(
    request_envelope: Mapping[str, Any],
    *,
    evidence_id: str,
    collected_at_ms: int,
    raw_artifact_digest: str,
    value_digest: str,
    collector_identity: str,
    independent_source_identity: str,
    uncertainty_digest: str,
    calibration_digest: str,
    context_digest: str,
    tamper_evidence_digest: str,
    provenance_chain_digest: str,
    relation: str,
) -> dict[str, Any]:
    request = validate_observe_request(request_envelope)
    evidence_id = _text(evidence_id, field="evidence_id")
    collector_identity = _text(collector_identity, field="collector_identity")
    independent_source_identity = _text(
        independent_source_identity, field="independent_source_identity"
    )
    for field, value in (
        ("raw_artifact_digest", raw_artifact_digest),
        ("value_digest", value_digest),
        ("uncertainty_digest", uncertainty_digest),
        ("calibration_digest", calibration_digest),
        ("context_digest", context_digest),
        ("tamper_evidence_digest", tamper_evidence_digest),
        ("provenance_chain_digest", provenance_chain_digest),
    ):
        _hex_digest(value, field=field)
    if not isinstance(collected_at_ms, int) or collected_at_ms < request["requested_at_ms"]:
        raise ValueError("collected_at_ms_invalid")
    if relation not in EVIDENCE_RELATIONS:
        raise ValueError("evidence_relation_invalid")
    body = {
        "evidence_version": EVIDENCE_VERSION,
        "evidence_id": evidence_id,
        "request_digest": request_envelope["body_digest"],
        "authorization_digest": request["authorization_digest"],
        "source_report_digest": request["source_report_digest"],
        "source_state_digest": request["source_state_digest"],
        "root_lineage_digest": request["root_lineage_digest"],
        "prior_world_fragment_digest": request["world_fragment_digest"],
        "mission_candidate_id": request["mission_candidate_id"],
        "observation_candidate_id": request["observation_candidate_id"],
        "source_item_id": request["source_item_id"],
        "channel_id": request["channel_id"],
        "tool_id": request["tool_id"],
        "raw_artifact_digest": raw_artifact_digest,
        "value_digest": value_digest,
        "collector_identity": collector_identity,
        "independent_source_identity": independent_source_identity,
        "collected_at_ms": collected_at_ms,
        "uncertainty_digest": uncertainty_digest,
        "calibration_digest": calibration_digest,
        "context_digest": context_digest,
        "tamper_evidence_digest": tamper_evidence_digest,
        "provenance_chain_digest": provenance_chain_digest,
        "relation": relation,
        "observation_recorded": True,
        "observation_is_verification": False,
        "verification_required": True,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_memory_overwrite_authority": False,
    }
    receipt = make_envelope(body)
    validate_evidence_receipt(receipt)
    return receipt


def validate_evidence_receipt(receipt_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(receipt_envelope, label="observation_evidence")
    if body.get("evidence_version") != EVIDENCE_VERSION:
        raise ValueError("evidence_version_invalid")
    for field in (
        "request_digest",
        "authorization_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "raw_artifact_digest",
        "value_digest",
        "uncertainty_digest",
        "calibration_digest",
        "context_digest",
        "tamper_evidence_digest",
        "provenance_chain_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "evidence_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "channel_id",
        "tool_id",
        "collector_identity",
        "independent_source_identity",
    ):
        _text(body.get(field), field=field)
    if body.get("relation") not in EVIDENCE_RELATIONS:
        raise ValueError("evidence_relation_invalid")
    if body.get("observation_recorded") is not True:
        raise ValueError("observation_not_recorded")
    if body.get("observation_is_verification") is not False:
        raise ValueError("observation_verification_boundary_invalid")
    if body.get("verification_required") is not True:
        raise ValueError("verification_debt_not_preserved")
    for field in (
        "grants_truth_authority",
        "grants_causal_attribution",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"evidence_boundary_invalid:{field}")
    return body


def build_world_feedback_candidate(
    source_report_envelope: Mapping[str, Any],
    evidence_receipt_envelope: Mapping[str, Any],
    *,
    generated_at_ms: int,
) -> dict[str, Any]:
    report = v031.validate_report(source_report_envelope)
    evidence = validate_evidence_receipt(evidence_receipt_envelope)
    if evidence["source_report_digest"] != source_report_envelope.get("body_digest"):
        raise ValueError("evidence_report_mismatch")
    if evidence["source_state_digest"] != report["source_state_digest"]:
        raise ValueError("evidence_source_state_mismatch")
    if evidence["root_lineage_digest"] != report["root_lineage_digest"]:
        raise ValueError("evidence_root_lineage_mismatch")
    if evidence["prior_world_fragment_digest"] != report["world_fragment_digest"]:
        raise ValueError("evidence_world_fragment_mismatch")
    observation = _find_observation(report, evidence["observation_candidate_id"])
    mission = _find_mission(report, evidence["mission_candidate_id"])
    if observation["mission_candidate_id"] != mission["mission_candidate_id"]:
        raise ValueError("evidence_mission_observation_mismatch")
    if observation["source_item_id"] != evidence["source_item_id"]:
        raise ValueError("evidence_source_item_mismatch")
    if not isinstance(generated_at_ms, int) or generated_at_ms < evidence["collected_at_ms"]:
        raise ValueError("generated_at_ms_invalid")

    if report["route"] == "HOLD":
        route = "HOLD"
    elif report["route"] == "HANDOVER":
        route = "HANDOVER"
    elif evidence["relation"] in {"INCONCLUSIVE", "CONFLICTED"}:
        route = "REOBSERVE"
    else:
        route = "WORLD_UPDATE_CANDIDATE"

    unresolved_item = None
    for item in report["unresolved_trace"]:
        if item.get("item_id") == evidence["source_item_id"]:
            unresolved_item = item
            break
    if unresolved_item is None:
        raise ValueError("unresolved_item_not_found")

    relation_to_candidate_state = {
        "SUPPORTS": "SUPPORTED_UPDATE_CANDIDATE",
        "CONTRADICTS": "CONTRADICTED_UPDATE_CANDIDATE",
        "INCONCLUSIVE": "UNRESOLVED_REOBSERVE",
        "CONFLICTED": "CONFLICTED_REOBSERVE",
    }
    proposed_world_fragment_digest = digest({
        "prior_world_fragment_digest": evidence["prior_world_fragment_digest"],
        "evidence_receipt_digest": evidence_receipt_envelope["body_digest"],
        "candidate_state": relation_to_candidate_state[evidence["relation"]],
    })
    body = {
        "feedback_version": FEEDBACK_VERSION,
        "source_report_digest": source_report_envelope["body_digest"],
        "evidence_receipt_digest": evidence_receipt_envelope["body_digest"],
        "source_state_digest": report["source_state_digest"],
        "root_lineage_digest": report["root_lineage_digest"],
        "prior_world_fragment_digest": report["world_fragment_digest"],
        "proposed_world_fragment_digest": proposed_world_fragment_digest,
        "mission_candidate_id": evidence["mission_candidate_id"],
        "observation_candidate_id": evidence["observation_candidate_id"],
        "source_item_id": evidence["source_item_id"],
        "generated_at_ms": generated_at_ms,
        "route": route,
        "relation": evidence["relation"],
        "candidate_state": relation_to_candidate_state[evidence["relation"]],
        "unresolved_item": unresolved_item,
        "new_evidence_ref": evidence_receipt_envelope["body_digest"],
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "verification_required": True,
        "world_update_is_candidate": True,
        "automatic_truth_promotion": False,
        "automatic_root_rewrite": False,
        "automatic_mission_completion": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_memory_overwrite_authority": False,
    }
    feedback = make_envelope(body)
    validate_world_feedback_candidate(feedback)
    return feedback


def validate_world_feedback_candidate(feedback_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(feedback_envelope, label="world_feedback_candidate")
    if body.get("feedback_version") != FEEDBACK_VERSION:
        raise ValueError("feedback_version_invalid")
    if body.get("route") not in FEEDBACK_ROUTES:
        raise ValueError("feedback_route_invalid")
    if body.get("relation") not in EVIDENCE_RELATIONS:
        raise ValueError("feedback_relation_invalid")
    for field in (
        "source_report_digest",
        "evidence_receipt_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "new_evidence_ref",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "candidate_state",
    ):
        _text(body.get(field), field=field)
    for field in (
        "counterevidence_preserved",
        "uncertainty_preserved",
        "verification_required",
        "world_update_is_candidate",
    ):
        if body.get(field) is not True:
            raise ValueError(f"feedback_preservation_invalid:{field}")
    for field in (
        "automatic_truth_promotion",
        "automatic_root_rewrite",
        "automatic_mission_completion",
        "grants_plan_activation",
        "grants_actos_invocation",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"feedback_boundary_invalid:{field}")
    if body["relation"] in {"INCONCLUSIVE", "CONFLICTED"} and body["route"] != "REOBSERVE":
        raise ValueError("reobserve_route_required")
    return body


def _read_jsonl(path: Path, validator) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("ledger_entry_invalid")
            validator(value)
            entries.append(value)
    return entries


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(value) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


@dataclass(frozen=True)
class CommitResult:
    status: str
    artifact: dict[str, Any]
    ledger_entries: int


def commit_observe_request(*, ledger_path: Path, request_envelope: Mapping[str, Any]) -> CommitResult:
    ledger_path = Path(ledger_path)
    request = validate_observe_request(request_envelope)
    entries = _read_jsonl(ledger_path, validate_observe_request)
    for entry in entries:
        body = validate_observe_request(entry)
        if entry["body_digest"] == request_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["authorization_id"] == request["authorization_id"]:
            raise ValueError("authorization_already_consumed")
        if body["authorization_digest"] == request["authorization_digest"]:
            raise ValueError("authorization_digest_already_consumed")
    _append_jsonl(ledger_path, request_envelope)
    return CommitResult("COMMITTED", dict(request_envelope), len(entries) + 1)


def commit_evidence_receipt(*, ledger_path: Path, receipt_envelope: Mapping[str, Any]) -> CommitResult:
    ledger_path = Path(ledger_path)
    receipt = validate_evidence_receipt(receipt_envelope)
    entries = _read_jsonl(ledger_path, validate_evidence_receipt)
    for entry in entries:
        body = validate_evidence_receipt(entry)
        if entry["body_digest"] == receipt_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["request_digest"] == receipt["request_digest"]:
            raise ValueError("request_already_has_evidence_receipt")
        if body["evidence_id"] == receipt["evidence_id"]:
            raise ValueError("evidence_id_reuse")
    _append_jsonl(ledger_path, receipt_envelope)
    return CommitResult("COMMITTED", dict(receipt_envelope), len(entries) + 1)


def commit_world_feedback(*, ledger_path: Path, feedback_envelope: Mapping[str, Any]) -> CommitResult:
    ledger_path = Path(ledger_path)
    feedback = validate_world_feedback_candidate(feedback_envelope)
    entries = _read_jsonl(ledger_path, validate_world_feedback_candidate)
    for entry in entries:
        body = validate_world_feedback_candidate(entry)
        if entry["body_digest"] == feedback_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["evidence_receipt_digest"] == feedback["evidence_receipt_digest"]:
            raise ValueError("evidence_receipt_already_has_world_feedback")
    _append_jsonl(ledger_path, feedback_envelope)
    return CommitResult("COMMITTED", dict(feedback_envelope), len(entries) + 1)


__all__ = [
    "CommitResult",
    "build_authorized_observe_request",
    "build_world_feedback_candidate",
    "commit_evidence_receipt",
    "commit_observe_request",
    "commit_world_feedback",
    "make_observation_authorization_receipt",
    "make_observation_evidence_receipt",
    "validate_authorization_receipt",
    "validate_evidence_receipt",
    "validate_observe_request",
    "validate_world_feedback_candidate",
]
