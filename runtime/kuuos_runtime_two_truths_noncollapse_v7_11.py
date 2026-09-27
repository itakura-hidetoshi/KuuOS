#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
import os
import pathlib
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_two_truths_noncollapse_v7_11"
PLAN_VERSION = "kuuos_two_truths_noncollapse_plan_v7_11"
SAMVRTI_INPUT_VERSION = "kuuos_two_truths_samvrti_worlds_input_v7_11"
SOURCE_VERSION = "kuuos_runtime_invariant_projection_choice_independence_v7_10"

READY = "KUUOS_TWO_TRUTHS_NONCOLLAPSE_READY"
PARTIAL = "KUUOS_TWO_TRUTHS_NONCOLLAPSE_PARTIAL"
BLOCKED = "KUUOS_TWO_TRUTHS_NONCOLLAPSE_BLOCKED"

PARAMARTHA_STABLE = "paramartha_equivalence_available"
PARAMARTHA_HELD = "paramartha_equivalence_held"
PARAMARTHA_OBSTRUCTED = "paramartha_equivalence_obstructed"

SAMVRTI_OBSERVED = "observed"
SAMVRTI_HELD = "held"
SAMVRTI_UNAVAILABLE = "unavailable"

SAME_PARAMARTHA_SAME_SAMVRTI = "same_paramartha_same_samvrti_operation"
SAME_PARAMARTHA_DISTINCT_SAMVRTI = "same_paramartha_distinct_samvrti_worlds"
SAME_PARAMARTHA_SAMVRTI_UNRESOLVED = "same_paramartha_samvrti_unresolved"
DISTINCT_PARAMARTHA = "distinct_paramartha_meaning"

SOURCE_CHOICE_INVARIANT = "projection_choice_invariant"
SOURCE_CHOICE_HELD = "projection_choice_invariance_held"
SOURCE_CHOICE_OBSTRUCTED = "projection_choice_invariance_obstructed"


@dataclass(frozen=True)
class TwoTruthsNoncollapseResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    semantic_subject_count: int
    stable_paramartha_subject_count: int
    held_paramartha_subject_count: int
    obstructed_paramartha_subject_count: int
    samvrti_world_count: int
    same_paramartha_pair_count: int
    same_paramartha_same_samvrti_count: int
    same_paramartha_distinct_samvrti_count: int
    unresolved_samvrti_pair_count: int
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


def _serialized_size(value: Any) -> int:
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def _i(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> int:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("two_truths_noncollapse_required") is not True:
        blockers.append("two_truths_noncollapse_required_not_true")
    if plan.get("paramartha_equivalence_may_erase_samvrti_difference") is not False:
        blockers.append("paramartha_may_erase_samvrti_difference_must_be_false")
    if plan.get("samvrti_difference_is_error") is not False:
        blockers.append("samvrti_difference_is_error_must_be_false")
    if plan.get("conventional_substitution_requires_samvrti_equivalence") is not True:
        blockers.append("conventional_substitution_samvrti_equivalence_not_true")
    if plan.get("paramartha_carrier_is_ultimate_substance") is not False:
        blockers.append("paramartha_carrier_substance_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")

    max_value_bytes = _i(plan.get("max_samvrti_value_bytes"), 16384)
    if max_value_bytes < 128 or max_value_bytes > 131072:
        blockers.append("max_samvrti_value_bytes_out_of_bounds")
    return max_value_bytes


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

        source_status = str(item.get("projection_choice_status", "")).strip()
        carrier_id = str(
            item.get("choice_independent_carrier_element_id", "")
        ).strip()

        if source_status == SOURCE_CHOICE_INVARIANT:
            paramartha_state = PARAMARTHA_STABLE
            if not carrier_id:
                blockers.append(f"source_subject_{index}_stable_carrier_missing")
        elif source_status == SOURCE_CHOICE_HELD:
            paramartha_state = PARAMARTHA_HELD
        elif source_status == SOURCE_CHOICE_OBSTRUCTED:
            paramartha_state = PARAMARTHA_OBSTRUCTED
        else:
            blockers.append(f"source_subject_{index}_choice_status_invalid")
            paramartha_state = PARAMARTHA_HELD

        result[subject_id] = {
            "semantic_subject_id": subject_id,
            "paramartha_state": paramartha_state,
            "paramartha_carrier_element_id": carrier_id,
            "source_projection_choice_status": source_status,
        }

    return result


def _samvrti_rows(
    packet: Mapping[str, Any],
    source_subjects: Mapping[str, Mapping[str, Any]],
    *,
    max_value_bytes: int,
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = packet.get("world_presentations", [])
    if not isinstance(raw, list):
        blockers.append("samvrti_world_presentations_not_list")
        return {}

    result: dict[str, dict[str, Any]] = {}

    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"samvrti_world_{index}_not_object")
            continue

        subject_id = str(item.get("semantic_subject_id", "")).strip()
        world_id = str(item.get("samvrti_world_id", "")).strip()
        state = str(item.get("samvrti_state", "")).strip()

        if not subject_id:
            blockers.append(f"samvrti_world_{index}_subject_id_missing")
            continue
        if subject_id not in source_subjects:
            blockers.append(f"samvrti_world_{index}_unknown_subject_id")
        if subject_id in result:
            blockers.append("duplicate_samvrti_subject_id")
            continue
        if not world_id:
            blockers.append(f"samvrti_world_{index}_world_id_missing")
        if state not in {SAMVRTI_OBSERVED, SAMVRTI_HELD, SAMVRTI_UNAVAILABLE}:
            blockers.append(f"samvrti_world_{index}_state_invalid")

        conventional_present = "conventional_operational_value" in item
        conventional_value = item.get("conventional_operational_value")

        scope = item.get("scope")
        conditions = item.get("conditions")
        governance_boundary = item.get("governance_boundary")
        action_constraints = item.get("action_constraints")
        visible_residuals = item.get("visible_residuals")
        lineage_digest = str(item.get("lineage_digest", "")).strip()

        if state == SAMVRTI_OBSERVED:
            if not conventional_present:
                blockers.append(
                    f"samvrti_world_{index}_conventional_operational_value_missing"
                )
            for field_name, field_value in (
                ("conventional_operational_value", conventional_value),
                ("scope", scope),
                ("conditions", conditions),
                ("governance_boundary", governance_boundary),
                ("action_constraints", action_constraints),
                ("visible_residuals", visible_residuals),
            ):
                if _serialized_size(field_value) > max_value_bytes:
                    blockers.append(
                        f"samvrti_world_{index}_{field_name}_too_large"
                    )
            if not lineage_digest:
                blockers.append(f"samvrti_world_{index}_lineage_digest_missing")

            samvrti_signature = _sha(
                {
                    "conventional_operational_value": conventional_value,
                    "scope": scope,
                    "conditions": conditions,
                    "governance_boundary": governance_boundary,
                    "action_constraints": action_constraints,
                    "visible_residuals": visible_residuals,
                    "lineage_digest": lineage_digest,
                }
            )
        else:
            if conventional_present and conventional_value is not None:
                blockers.append(
                    f"samvrti_world_{index}_nonobserved_conventional_value_must_be_null"
                )
            samvrti_signature = ""

        result[subject_id] = {
            "semantic_subject_id": subject_id,
            "samvrti_world_id": world_id,
            "samvrti_state": state,
            "samvrti_operational_signature": samvrti_signature,
            "lineage_digest": lineage_digest,
        }

    return result


def _subject_records(
    source_subjects: Mapping[str, Mapping[str, Any]],
    samvrti: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for subject_id in sorted(source_subjects):
        source = source_subjects[subject_id]
        world = samvrti.get(subject_id)
        if world is None:
            world_state = SAMVRTI_HELD
            world_id = ""
            world_signature = ""
            lineage_digest = ""
        else:
            world_state = str(world.get("samvrti_state", SAMVRTI_HELD))
            world_id = str(world.get("samvrti_world_id", ""))
            world_signature = str(
                world.get("samvrti_operational_signature", "")
            )
            lineage_digest = str(world.get("lineage_digest", ""))

        records.append(
            {
                "semantic_subject_id": subject_id,
                "paramartha_state": source["paramartha_state"],
                "paramartha_carrier_element_id": source[
                    "paramartha_carrier_element_id"
                ],
                "samvrti_world_id": world_id,
                "samvrti_state": world_state,
                "samvrti_operational_signature": world_signature,
                "lineage_digest": lineage_digest,
                "paramartha_equivalence_erases_samvrti_world": False,
                "samvrti_world_is_ultimate_substance": False,
            }
        )
    return records


def _pair_records(subjects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []

    for left, right in itertools.combinations(subjects, 2):
        left_paramartha = left["paramartha_carrier_element_id"]
        right_paramartha = right["paramartha_carrier_element_id"]

        left_stable = left["paramartha_state"] == PARAMARTHA_STABLE
        right_stable = right["paramartha_state"] == PARAMARTHA_STABLE

        same_paramartha = (
            left_stable
            and right_stable
            and left_paramartha
            and left_paramartha == right_paramartha
        )

        if not same_paramartha:
            relation = DISTINCT_PARAMARTHA
            substitution_allowed = False
            distinction_required = True
        else:
            left_samvrti_observed = left["samvrti_state"] == SAMVRTI_OBSERVED
            right_samvrti_observed = right["samvrti_state"] == SAMVRTI_OBSERVED

            if not left_samvrti_observed or not right_samvrti_observed:
                relation = SAME_PARAMARTHA_SAMVRTI_UNRESOLVED
                substitution_allowed = False
                distinction_required = True
            elif (
                left["samvrti_operational_signature"]
                == right["samvrti_operational_signature"]
            ):
                relation = SAME_PARAMARTHA_SAME_SAMVRTI
                substitution_allowed = True
                distinction_required = False
            else:
                relation = SAME_PARAMARTHA_DISTINCT_SAMVRTI
                substitution_allowed = False
                distinction_required = True

        pairs.append(
            {
                "left_semantic_subject_id": left["semantic_subject_id"],
                "right_semantic_subject_id": right["semantic_subject_id"],
                "left_samvrti_world_id": left["samvrti_world_id"],
                "right_samvrti_world_id": right["samvrti_world_id"],
                "two_truths_relation": relation,
                "same_paramartha_meaning": same_paramartha,
                "conventional_substitution_allowed": substitution_allowed,
                "samvrti_distinction_required": distinction_required,
                "paramartha_equivalence_may_erase_samvrti_difference": False,
                "samvrti_difference_is_error": False,
            }
        )

    return pairs


def build_two_truths_noncollapse(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> TwoTruthsNoncollapseResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "two_truths_noncollapse_plan_v7_11.json"
    source_path = root / "invariant_projection_choice_independence_packet_v7_10.json"
    samvrti_path = root / "two_truths_samvrti_worlds_input_v7_11.json"
    output_path = root / "two_truths_noncollapse_packet_v7_11.json"
    receipt_path = root / "two_truths_noncollapse_receipt_v7_11.json"
    audit_path = root / "two_truths_noncollapse_audit_v7_11.jsonl"

    if ctx.get("two_truths_noncollapse_enabled") is not True:
        blockers.append("two_truths_noncollapse_enabled_not_true")
    if ctx.get("apply_two_truths_noncollapse") is not True:
        blockers.append("apply_two_truths_noncollapse_not_true")
    if authority.get("authority_status") != "KUUOS_TWO_TRUTHS_NONCOLLAPSE_AUTHORITY_READY":
        blockers.append("two_truths_noncollapse_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "source_choice_packet_read_allowed",
        "samvrti_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    samvrti_packet = _read_json(samvrti_path)

    max_value_bytes = 16384
    if not plan:
        blockers.append("two_truths_plan_missing_or_invalid")
    else:
        max_value_bytes = _validate_plan(plan, blockers)

    if not source:
        blockers.append("projection_choice_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("projection_choice_packet_version_invalid")

    if not samvrti_packet:
        blockers.append("samvrti_worlds_input_missing_or_invalid")
    elif samvrti_packet.get("version") != SAMVRTI_INPUT_VERSION:
        blockers.append("samvrti_worlds_input_version_invalid")

    if plan and source and samvrti_packet:
        source_digest = _sha(source)
        if str(plan.get("source_choice_packet_digest", "")) != source_digest:
            blockers.append("source_choice_packet_digest_mismatch")
        if (
            str(samvrti_packet.get("source_choice_packet_digest", ""))
            != source_digest
        ):
            blockers.append("samvrti_source_choice_packet_digest_mismatch")

        boundary = _m(source.get("dependent_origination_boundary"))
        if boundary.get("projection_choice_is_presentation") is not True:
            blockers.append("source_projection_choice_boundary_missing")
        if boundary.get("projection_id_defines_semantic_identity") is not False:
            blockers.append("source_projection_identity_boundary_invalid")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("source_authority_boundary_invalid")

    source_subjects = _source_subjects(source, blockers) if source else {}
    samvrti = (
        _samvrti_rows(
            samvrti_packet,
            source_subjects,
            max_value_bytes=max_value_bytes,
            blockers=blockers,
        )
        if samvrti_packet
        else {}
    )

    subjects = _subject_records(source_subjects, samvrti) if not blockers else []
    pairs = _pair_records(subjects) if not blockers else []

    counts = {
        "paramartha_stable": sum(
            1 for s in subjects if s["paramartha_state"] == PARAMARTHA_STABLE
        ),
        "paramartha_held": sum(
            1 for s in subjects if s["paramartha_state"] == PARAMARTHA_HELD
        ),
        "paramartha_obstructed": sum(
            1 for s in subjects if s["paramartha_state"] == PARAMARTHA_OBSTRUCTED
        ),
        "same_paramartha": sum(
            1 for p in pairs if p["same_paramartha_meaning"]
        ),
        "same_samvrti": sum(
            1 for p in pairs
            if p["two_truths_relation"] == SAME_PARAMARTHA_SAME_SAMVRTI
        ),
        "distinct_samvrti": sum(
            1 for p in pairs
            if p["two_truths_relation"] == SAME_PARAMARTHA_DISTINCT_SAMVRTI
        ),
        "unresolved_samvrti": sum(
            1 for p in pairs
            if p["two_truths_relation"] == SAME_PARAMARTHA_SAMVRTI_UNRESOLVED
        ),
    }

    output: dict[str, Any] = {}
    output_written = False

    if not blockers:
        if counts["paramartha_held"] > 0 or counts["unresolved_samvrti"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_choice_packet_digest": _sha(source),
            "semantic_subjects": subjects,
            "two_truths_relations": pairs,
            "summary": {
                "semantic_subject_count": len(subjects),
                "stable_paramartha_subject_count": counts["paramartha_stable"],
                "held_paramartha_subject_count": counts["paramartha_held"],
                "obstructed_paramartha_subject_count": counts[
                    "paramartha_obstructed"
                ],
                "samvrti_world_count": len(samvrti),
                "same_paramartha_pair_count": counts["same_paramartha"],
                "same_paramartha_same_samvrti_count": counts["same_samvrti"],
                "same_paramartha_distinct_samvrti_count": counts[
                    "distinct_samvrti"
                ],
                "unresolved_samvrti_pair_count": counts["unresolved_samvrti"],
            },
            "two_truths_boundary": {
                "paramartha_and_samvrti_are_separate_surfaces": True,
                "paramartha_equivalence_may_erase_samvrti_difference": False,
                "same_paramartha_does_not_imply_conventional_substitutability": True,
                "samvrti_difference_is_error": False,
                "samvrti_difference_can_be_operationally_required": True,
                "conventional_substitution_requires_samvrti_equivalence": True,
                "nihilistic_collapse_into_paramartha_allowed": False,
                "reification_of_samvrti_allowed": False,
                "paramartha_carrier_is_ultimate_substance": False,
                "samvrti_world_is_ultimate_substance": False,
                "world_id_defines_paramartha_identity": False,
                "raw_conventional_operational_values_persisted": False,
                "source_authority_transferred": False,
            },
            "middle_way_note": {
                "non_reification": "paramartha equivalence does not turn the carrier into substance",
                "non_nihilism": "paramartha equivalence does not erase conventional responsibility, scope, action constraints, lineage, or residuals",
                "operational_rule": "preserve samvrti distinctions whenever conventional operational signatures differ",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-two-truths-noncollapse-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "samvrti_input_digest": _sha(samvrti_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "semantic_subject_count": len(subjects),
        "stable_paramartha_subject_count": counts["paramartha_stable"],
        "held_paramartha_subject_count": counts["paramartha_held"],
        "obstructed_paramartha_subject_count": counts["paramartha_obstructed"],
        "samvrti_world_count": len(samvrti),
        "same_paramartha_pair_count": counts["same_paramartha"],
        "same_paramartha_same_samvrti_count": counts["same_samvrti"],
        "same_paramartha_distinct_samvrti_count": counts["distinct_samvrti"],
        "unresolved_samvrti_pair_count": counts["unresolved_samvrti"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "paramartha_equivalence_may_erase_samvrti_difference": False,
        "same_paramartha_does_not_imply_conventional_substitutability": True,
        "samvrti_difference_is_error": False,
        "raw_conventional_operational_values_persisted": False,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return TwoTruthsNoncollapseResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(subjects),
        counts["paramartha_stable"],
        counts["paramartha_held"],
        counts["paramartha_obstructed"],
        len(samvrti),
        counts["same_paramartha"],
        counts["same_samvrti"],
        counts["distinct_samvrti"],
        counts["unresolved_samvrti"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
