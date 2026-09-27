#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    validate_transaction_state,
)

VERSION = "kuuos_runtime_samvrti_world_effect_update_v7_14"
PLAN_VERSION = "kuuos_samvrti_world_effect_update_plan_v7_14"
INPUT_VERSION = "kuuos_samvrti_world_effect_updates_input_v7_14"
SOURCE_VERSION = "kuuos_runtime_action_effect_lineage_binding_v7_13"

READY = "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_READY"
PARTIAL = "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_PARTIAL"
OBSTRUCTED = "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_OBSTRUCTED"
BLOCKED = "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_BLOCKED"

WORLD_TRANSITION_CONFIRMED = "samvrti_world_transition_confirmed"
WORLD_REOBSERVATION_OPEN = "samvrti_reobservation_open"
WORLD_COMPENSATION_OPEN = "samvrti_compensation_open"
WORLD_HANDOVER_OPEN = "samvrti_handover_open"
WORLD_NO_EFFECT = "samvrti_no_effect"
WORLD_EFFECT_PENDING = "samvrti_effect_pending"
WORLD_PROPOSAL_ONLY = "samvrti_proposal_only"
WORLD_UPDATE_OBSTRUCTED = "samvrti_world_update_obstructed"

SOURCE_EFFECT_CONFIRMED = "effect_confirmed"
SOURCE_REOBSERVATION_REQUIRED = "reobservation_required"
SOURCE_COMPENSATION_PROPOSED = "compensation_proposed"
SOURCE_HANDOVER_REQUIRED = "handover_required"
SOURCE_NO_EFFECT_RECORDED = "no_effect_recorded"
SOURCE_AUTHORIZED_PREPARED = "authorized_prepared"
SOURCE_TRANSACTION_IN_PROGRESS = "transaction_in_progress"
SOURCE_AWAITING_LOWER_AUTHORITY = "awaiting_lower_authority"
SOURCE_AWAITING_WORLD_RESOLUTION = "awaiting_world_resolution"
SOURCE_PROPOSAL_ONLY = "proposal_only"
SOURCE_BINDING_OBSTRUCTED = "binding_obstructed"

COMMITTED_SOURCE_TO_ROUTE = {
    SOURCE_EFFECT_CONFIRMED: "EFFECT_CONFIRMED",
    SOURCE_REOBSERVATION_REQUIRED: "REOBSERVATION_REQUIRED",
    SOURCE_COMPENSATION_PROPOSED: "COMPENSATION_PROPOSED",
    SOURCE_HANDOVER_REQUIRED: "HANDOVER_REQUIRED",
    SOURCE_NO_EFFECT_RECORDED: "NO_EFFECT_RECORDED",
}


@dataclass(frozen=True)
class SamvrtiWorldEffectUpdateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    update_count: int
    confirmed_transition_count: int
    reobservation_open_count: int
    compensation_open_count: int
    handover_open_count: int
    no_effect_count: int
    pending_count: int
    proposal_only_count: int
    obstructed_count: int
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


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("effect_confirmed_may_update_samvrti_world") is not True:
        blockers.append("effect_confirmed_world_update_not_true")
    if plan.get("nonconfirmed_effect_may_fabricate_world_update") is not False:
        blockers.append("nonconfirmed_fabricated_update_must_be_false")
    if plan.get("world_update_may_change_paramartha_class") is not False:
        blockers.append("world_update_paramartha_change_must_be_false")
    if plan.get("effect_confirmed_implies_mission_success") is not False:
        blockers.append("effect_confirmed_mission_success_must_be_false")
    if plan.get("reconciliation_is_truth") is not False:
        blockers.append("reconciliation_truth_must_be_false")
    if plan.get("world_update_overwrites_history") is not False:
        blockers.append("world_update_history_overwrite_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")


def _source_lineages(
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = source.get("action_effect_lineages", [])
    if not isinstance(raw, list):
        blockers.append("source_action_effect_lineages_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"source_lineage_{index}_not_object")
            continue
        action_id = str(item.get("action_id", "")).strip()
        if not action_id:
            blockers.append(f"source_lineage_{index}_action_id_missing")
            continue
        if action_id in result:
            blockers.append("duplicate_source_action_id")
            continue
        result[action_id] = dict(item)
    return result


def _validated_transaction(raw: Any, errors: list[str]) -> dict[str, Any]:
    if raw in (None, {}):
        return {}
    if not isinstance(raw, Mapping):
        errors.append("transaction_state_not_object")
        return {}
    state = dict(raw)
    tx_errors = validate_transaction_state(state)
    if tx_errors:
        errors.extend("transaction:" + item for item in tx_errors)
    return state


def _bind_transaction(
    lineage: Mapping[str, Any],
    transaction: Mapping[str, Any],
    errors: list[str],
) -> None:
    if not transaction:
        return
    source_state_digest = str(lineage.get("transaction_state_digest", ""))
    source_final_digest = str(
        lineage.get("transaction_final_receipt_digest", "")
    )
    source_intent_digest = str(lineage.get("transaction_intent_digest", ""))

    if source_state_digest and transaction.get("transaction_state_digest") != source_state_digest:
        errors.append("transaction_state_digest_mismatch")
    if source_intent_digest and transaction.get("transaction_intent_digest") != source_intent_digest:
        errors.append("transaction_intent_digest_mismatch")
    if source_final_digest and transaction.get("transaction_final_receipt_digest") != source_final_digest:
        errors.append("transaction_final_receipt_digest_mismatch")

    expected_route = COMMITTED_SOURCE_TO_ROUTE.get(
        str(lineage.get("action_effect_lineage_state", ""))
    )
    if expected_route is not None:
        if transaction.get("current_phase") != "committed":
            errors.append("source_committed_outcome_requires_committed_transaction")
        if transaction.get("route") != expected_route:
            errors.append("source_lineage_transaction_route_mismatch")


def _confirmed_transition(
    *,
    lineage: Mapping[str, Any],
    transaction: Mapping[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    reconciliation = _m(transaction.get("reconciliation_receipt"))
    if not reconciliation:
        errors.append("confirmed_transition_reconciliation_receipt_missing")
        return {}
    if reconciliation.get("verdict") != "EFFECT_CONFIRMED":
        errors.append("confirmed_transition_reconciliation_not_confirmed")
    if transaction.get("verification_route") != "VERIFICATION_PASSED":
        errors.append("confirmed_transition_verification_not_passed")
    if transaction.get("route") != "EFFECT_CONFIRMED":
        errors.append("confirmed_transition_transaction_route_invalid")

    prior_digest = str(reconciliation.get("prior_world_state_digest", "")).strip()
    observed_digest = str(
        reconciliation.get("observed_world_state_digest", "")
    ).strip()
    observed_effect_digest = str(
        reconciliation.get("observed_effect_digest", "")
    ).strip()
    evidence = reconciliation.get("independent_world_evidence_digests", [])
    if not prior_digest:
        errors.append("prior_world_state_digest_missing")
    if not observed_digest:
        errors.append("observed_world_state_digest_missing")
    if not observed_effect_digest:
        errors.append("observed_effect_digest_missing")
    if not isinstance(evidence, list) or len(evidence) < 1:
        errors.append("independent_world_evidence_missing")

    target_world_id = str(lineage.get("target_samvrti_world_id", "")).strip()
    if not target_world_id:
        target_world_id = "WORLD_INDEPENDENT"

    paramartha_carrier = str(
        lineage.get("paramartha_carrier_element_id", "")
    ).strip()
    if not paramartha_carrier:
        errors.append("paramartha_carrier_element_id_missing")

    version_id = "samvrti-world-version-" + _sha(
        {
            "target_samvrti_world_id": target_world_id,
            "prior_world_state_digest": prior_digest,
            "observed_world_state_digest": observed_digest,
            "transaction_final_receipt_digest": transaction.get(
                "transaction_final_receipt_digest"
            ),
        }
    )[:24]

    transition_digest = _sha(
        {
            "semantic_subject_id": lineage.get("semantic_subject_id"),
            "paramartha_carrier_element_id": paramartha_carrier,
            "target_samvrti_world_id": target_world_id,
            "prior_world_state_digest": prior_digest,
            "observed_world_state_digest": observed_digest,
            "observed_effect_digest": observed_effect_digest,
            "reconciliation_receipt_digest": transaction.get(
                "reconciliation_receipt_digest"
            ),
            "verify_state_digest": transaction.get("verify_state_digest"),
            "transaction_final_receipt_digest": transaction.get(
                "transaction_final_receipt_digest"
            ),
        }
    )

    return {
        "samvrti_world_version_id": version_id,
        "samvrti_world_transition_digest": transition_digest,
        "target_samvrti_world_id": target_world_id,
        "prior_world_state_digest": prior_digest,
        "observed_world_state_digest": observed_digest,
        "observed_effect_digest": observed_effect_digest,
        "independent_world_evidence_digest": _sha(sorted(str(x) for x in evidence)),
        "reconciliation_receipt_digest": str(
            transaction.get("reconciliation_receipt_digest", "")
        ),
        "verify_state_digest": str(transaction.get("verify_state_digest", "")),
        "transaction_final_receipt_digest": str(
            transaction.get("transaction_final_receipt_digest", "")
        ),
        "paramartha_carrier_element_id_before": paramartha_carrier,
        "paramartha_carrier_element_id_after": paramartha_carrier,
        "paramartha_class_changed": False,
        "world_transition_is_observed_conventional_record": True,
        "world_transition_is_ultimate_truth": False,
        "mission_success": "undetermined",
        "mission_success_implied": False,
    }


def _record(
    *,
    lineage: Mapping[str, Any],
    update: Mapping[str, Any],
    transaction: Mapping[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    _bind_transaction(lineage, transaction, errors)

    source_state = str(lineage.get("action_effect_lineage_state", ""))

    transition: dict[str, Any] = {}
    residue_digest = ""

    if source_state == SOURCE_EFFECT_CONFIRMED:
        if not transaction:
            errors.append("effect_confirmed_requires_transaction_state")
            state = WORLD_UPDATE_OBSTRUCTED
        else:
            transition = _confirmed_transition(
                lineage=lineage,
                transaction=transaction,
                errors=errors,
            )
            state = (
                WORLD_UPDATE_OBSTRUCTED
                if errors
                else WORLD_TRANSITION_CONFIRMED
            )
    elif source_state == SOURCE_REOBSERVATION_REQUIRED:
        state = WORLD_REOBSERVATION_OPEN
        residue_digest = _sha(
            {
                "action_id": lineage.get("action_id"),
                "transaction_final_receipt_digest": lineage.get(
                    "transaction_final_receipt_digest"
                ),
                "residue": "reobservation_required",
            }
        )
    elif source_state == SOURCE_COMPENSATION_PROPOSED:
        state = WORLD_COMPENSATION_OPEN
        residue_digest = _sha(
            {
                "action_id": lineage.get("action_id"),
                "transaction_final_receipt_digest": lineage.get(
                    "transaction_final_receipt_digest"
                ),
                "residue": "compensation_proposed",
            }
        )
    elif source_state == SOURCE_HANDOVER_REQUIRED:
        state = WORLD_HANDOVER_OPEN
        residue_digest = _sha(
            {
                "action_id": lineage.get("action_id"),
                "transaction_final_receipt_digest": lineage.get(
                    "transaction_final_receipt_digest"
                ),
                "residue": "handover_required",
            }
        )
    elif source_state == SOURCE_NO_EFFECT_RECORDED:
        state = WORLD_NO_EFFECT
        residue_digest = _sha(
            {
                "action_id": lineage.get("action_id"),
                "transaction_final_receipt_digest": lineage.get(
                    "transaction_final_receipt_digest"
                ),
                "residue": "no_effect_recorded",
            }
        )
    elif source_state in {SOURCE_AUTHORIZED_PREPARED, SOURCE_TRANSACTION_IN_PROGRESS}:
        state = WORLD_EFFECT_PENDING
    elif source_state in {
        SOURCE_AWAITING_LOWER_AUTHORITY,
        SOURCE_AWAITING_WORLD_RESOLUTION,
        SOURCE_PROPOSAL_ONLY,
    }:
        state = WORLD_PROPOSAL_ONLY
    elif source_state == SOURCE_BINDING_OBSTRUCTED:
        state = WORLD_UPDATE_OBSTRUCTED
        errors.append("source_action_effect_lineage_obstructed")
    else:
        state = WORLD_UPDATE_OBSTRUCTED
        errors.append("source_action_effect_lineage_state_unrecognized")

    if source_state != SOURCE_EFFECT_CONFIRMED and transition:
        errors.append("nonconfirmed_source_may_not_materialize_transition")
        state = WORLD_UPDATE_OBSTRUCTED

    declared_paramartha = str(
        update.get("expected_paramartha_carrier_element_id", "")
    ).strip()
    source_paramartha = str(
        lineage.get("paramartha_carrier_element_id", "")
    ).strip()
    if declared_paramartha and declared_paramartha != source_paramartha:
        errors.append("expected_paramartha_carrier_mismatch")
        state = WORLD_UPDATE_OBSTRUCTED

    return {
        "action_id": lineage.get("action_id"),
        "action_digest": lineage.get("action_digest"),
        "semantic_subject_id": lineage.get("semantic_subject_id"),
        "source_action_effect_lineage_state": source_state,
        "samvrti_world_effect_state": state,
        "paramartha_carrier_element_id": source_paramartha,
        "target_samvrti_world_id": lineage.get("target_samvrti_world_id"),
        "samvrti_world_transition": transition,
        "world_transition_residue_digest": residue_digest,
        "transaction_state_digest": (
            str(transaction.get("transaction_state_digest", ""))
            if transaction
            else str(lineage.get("transaction_state_digest", ""))
        ),
        "transaction_final_receipt_digest": (
            str(transaction.get("transaction_final_receipt_digest", ""))
            if transaction
            else str(lineage.get("transaction_final_receipt_digest", ""))
        ),
        "world_update_errors": sorted(set(errors)),
        "world_update_overwrites_history": False,
        "paramartha_class_changed": False,
        "effect_confirmed_implies_mission_success": False,
        "reconciliation_is_truth": False,
    }


def build_samvrti_world_effect_update(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> SamvrtiWorldEffectUpdateResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "samvrti_world_effect_update_plan_v7_14.json"
    source_path = root / "action_effect_lineage_binding_packet_v7_13.json"
    input_path = root / "samvrti_world_effect_updates_input_v7_14.json"
    output_path = root / "samvrti_world_effect_update_packet_v7_14.json"
    receipt_path = root / "samvrti_world_effect_update_receipt_v7_14.json"
    audit_path = root / "samvrti_world_effect_update_audit_v7_14.jsonl"

    if ctx.get("samvrti_world_effect_update_enabled") is not True:
        blockers.append("samvrti_world_effect_update_enabled_not_true")
    if ctx.get("apply_samvrti_world_effect_update") is not True:
        blockers.append("apply_samvrti_world_effect_update_not_true")
    if (
        authority_packet.get("authority_status")
        != "KUUOS_SAMVRTI_WORLD_EFFECT_UPDATE_AUTHORITY_READY"
    ):
        blockers.append("samvrti_world_effect_update_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "source_lineage_packet_read_allowed",
        "world_update_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    updates_packet = _read_json(input_path)

    if not plan:
        blockers.append("samvrti_world_update_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)

    if not source:
        blockers.append("action_effect_lineage_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("action_effect_lineage_packet_version_invalid")

    if not updates_packet:
        blockers.append("samvrti_world_updates_input_missing_or_invalid")
    elif updates_packet.get("version") != INPUT_VERSION:
        blockers.append("samvrti_world_updates_input_version_invalid")

    if plan and source and updates_packet:
        source_digest = _sha(source)
        if str(plan.get("source_lineage_packet_digest", "")) != source_digest:
            blockers.append("source_lineage_packet_digest_mismatch")
        if (
            str(updates_packet.get("source_lineage_packet_digest", ""))
            != source_digest
        ):
            blockers.append("updates_source_lineage_packet_digest_mismatch")

        boundary = _m(source.get("dependent_origination_effect_boundary"))
        if boundary.get("semantic_route_is_execution_authority") is not False:
            blockers.append("source_semantic_route_authority_invalid")
        if boundary.get("binding_layer_executes_effect") is not False:
            blockers.append("source_binding_execution_boundary_invalid")
        if boundary.get("execution_success_implies_mission_success") is not False:
            blockers.append("source_mission_success_boundary_invalid")

    lineages = _source_lineages(source, blockers) if source else {}

    raw_updates = updates_packet.get("updates", []) if updates_packet else []
    if updates_packet and not isinstance(raw_updates, list):
        blockers.append("updates_not_list")
        raw_updates = []
    if updates_packet and not raw_updates:
        blockers.append("updates_empty")

    records: list[dict[str, Any]] = []
    seen: set[str] = set()

    if not blockers:
        for index, raw in enumerate(raw_updates):
            if not isinstance(raw, Mapping):
                blockers.append(f"update_{index}_not_object")
                continue
            action_id = str(raw.get("action_id", "")).strip()
            if not action_id:
                blockers.append(f"update_{index}_action_id_missing")
                continue
            if action_id in seen:
                blockers.append("duplicate_update_action_id")
                continue
            seen.add(action_id)

            lineage = lineages.get(action_id)
            if lineage is None:
                blockers.append(f"update_{index}_unknown_action_id")
                continue

            transaction_errors: list[str] = []
            transaction = _validated_transaction(
                raw.get("transaction_state"),
                transaction_errors,
            )
            record = _record(
                lineage=lineage,
                update=raw,
                transaction=transaction,
            )
            if transaction_errors:
                record["world_update_errors"] = sorted(
                    set(record["world_update_errors"] + transaction_errors)
                )
                record["samvrti_world_effect_state"] = WORLD_UPDATE_OBSTRUCTED
            records.append(record)

    counts = {
        "confirmed": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_TRANSITION_CONFIRMED
        ),
        "reobserve": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_REOBSERVATION_OPEN
        ),
        "compensation": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_COMPENSATION_OPEN
        ),
        "handover": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_HANDOVER_OPEN
        ),
        "no_effect": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_NO_EFFECT
        ),
        "pending": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_EFFECT_PENDING
        ),
        "proposal": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_PROPOSAL_ONLY
        ),
        "obstructed": sum(
            1 for r in records
            if r["samvrti_world_effect_state"] == WORLD_UPDATE_OBSTRUCTED
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif counts["pending"] > 0 or counts["proposal"] > 0 or counts["reobserve"] > 0:
            status = PARTIAL
        else:
            status = READY

        materialized_versions = [
            r["samvrti_world_transition"]
            for r in records
            if r["samvrti_world_effect_state"] == WORLD_TRANSITION_CONFIRMED
        ]

        output = {
            "version": VERSION,
            "status": status,
            "source_lineage_packet_digest": _sha(source),
            "samvrti_world_effect_records": records,
            "materialized_samvrti_world_versions": materialized_versions,
            "summary": {
                "update_count": len(records),
                "confirmed_transition_count": counts["confirmed"],
                "reobservation_open_count": counts["reobserve"],
                "compensation_open_count": counts["compensation"],
                "handover_open_count": counts["handover"],
                "no_effect_count": counts["no_effect"],
                "pending_count": counts["pending"],
                "proposal_only_count": counts["proposal"],
                "obstructed_count": counts["obstructed"],
            },
            "two_truths_effect_return_boundary": {
                "effect_confirmed_may_update_samvrti_world": True,
                "nonconfirmed_effect_may_fabricate_world_update": False,
                "world_update_may_change_paramartha_class": False,
                "paramartha_carrier_preserved_across_samvrti_transition": True,
                "effect_confirmed_implies_mission_success": False,
                "reconciliation_is_truth": False,
                "world_update_overwrites_history": False,
                "samvrti_world_versions_are_append_only": True,
                "observed_world_transition_is_conventional_not_ultimate": True,
                "compensation_proposal_is_not_world_rollback": True,
                "reobservation_residue_is_preserved": True,
                "source_authority_transferred": False,
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-samvrti-world-effect-update-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "updates_digest": _sha(updates_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "update_count": len(records),
        "confirmed_transition_count": counts["confirmed"],
        "reobservation_open_count": counts["reobserve"],
        "compensation_open_count": counts["compensation"],
        "handover_open_count": counts["handover"],
        "no_effect_count": counts["no_effect"],
        "pending_count": counts["pending"],
        "proposal_only_count": counts["proposal"],
        "obstructed_count": counts["obstructed"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "world_update_may_change_paramartha_class": False,
        "effect_confirmed_implies_mission_success": False,
        "reconciliation_is_truth": False,
        "world_update_overwrites_history": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return SamvrtiWorldEffectUpdateResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(records),
        counts["confirmed"],
        counts["reobserve"],
        counts["compensation"],
        counts["handover"],
        counts["no_effect"],
        counts["pending"],
        counts["proposal"],
        counts["obstructed"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
