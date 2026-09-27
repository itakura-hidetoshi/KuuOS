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

VERSION = "kuuos_runtime_observability_presentation_invariance_v7_7"
PLAN_VERSION = "kuuos_observability_presentation_invariance_plan_v7_7"
SEMANTICS_VERSION = "kuuos_observability_presentation_semantics_input_v7_7"
DESCENT_VERSION = "kuuos_runtime_observability_dependent_origination_descent_v7_4"

READY = "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_READY"
PARTIAL = "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_BLOCKED"

INVARIANT = "presentation_invariant"
INVARIANCE_HELD = "presentation_invariance_held"
INVARIANCE_OBSTRUCTED = "presentation_invariance_obstructed"
LOCAL_ONLY = "local_presentation_only"

DESCENT_AUTHORIZED = "presentation_invariant_descent"
DESCENT_HELD = "descent_held_for_missing_semantics"
DESCENT_DENIED = "descent_denied_by_presentation_variance"
LOCAL_SEMANTIC = "local_semantic_presentation_only"

ALLOWED_SEMANTIC_STATES = {"observed", "held", "unavailable"}


@dataclass(frozen=True)
class ObservabilityPresentationInvarianceResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    presentation_count: int
    sector_count: int
    invariant_sector_count: int
    held_sector_count: int
    obstructed_sector_count: int
    local_only_sector_count: int
    quotient_semantic_witness_count: int
    obstruction_witness_count: int
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


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _serialized_size(value: Any) -> int:
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, int]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("presentation_invariance_required_for_descent") is not True:
        blockers.append("presentation_invariance_required_for_descent_not_true")
    if plan.get("compatibility_may_substitute_for_invariance") is not False:
        blockers.append("compatibility_substitution_must_be_false")
    if plan.get("global_collapse_allowed") is not False:
        blockers.append("global_collapse_must_be_false")
    if plan.get("causal_inference_allowed") is not False:
        blockers.append("causal_inference_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_theorem_authority") is not False:
        blockers.append("python_formal_theorem_authority_must_be_false")

    max_presentations = _i(plan.get("max_presentations"), 128)
    if max_presentations < 1 or max_presentations > 512:
        blockers.append("max_presentations_out_of_bounds")

    max_semantic_bytes = _i(plan.get("max_semantic_value_bytes"), 8192)
    if max_semantic_bytes < 64 or max_semantic_bytes > 65536:
        blockers.append("max_semantic_value_bytes_out_of_bounds")

    return max_presentations, max_semantic_bytes


def _presentation_ids(
    descent: Mapping[str, Any],
    blockers: list[str],
) -> set[str]:
    raw = descent.get("presentations", [])
    if not isinstance(raw, list):
        blockers.append("descent_presentations_not_list")
        return set()

    result: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"presentation_{index}_not_object")
            continue
        presentation_id = str(item.get("presentation_id", "")).strip()
        if not presentation_id:
            blockers.append(f"presentation_{index}_id_missing")
            continue
        if presentation_id in result:
            blockers.append("duplicate_descent_presentation_id")
            continue
        result.add(presentation_id)
    return result


def _semantic_table(
    semantics_packet: Mapping[str, Any],
    presentation_ids: set[str],
    *,
    max_semantic_bytes: int,
    blockers: list[str],
) -> tuple[str, str, dict[str, dict[str, Any]]]:
    projection_id = str(semantics_packet.get("semantic_projection_id", "")).strip()
    schema_digest = str(semantics_packet.get("semantic_schema_digest", "")).strip()
    if not projection_id:
        blockers.append("semantic_projection_id_missing")
    if not schema_digest:
        blockers.append("semantic_schema_digest_missing")

    raw = semantics_packet.get("presentation_semantics", [])
    if not isinstance(raw, list):
        blockers.append("presentation_semantics_not_list")
        return projection_id, schema_digest, {}

    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"semantic_{index}_not_object")
            continue

        presentation_id = str(item.get("presentation_id", "")).strip()
        if not presentation_id:
            blockers.append(f"semantic_{index}_presentation_id_missing")
            continue
        if presentation_id not in presentation_ids:
            blockers.append(f"semantic_{index}_unknown_presentation_id")
        if presentation_id in result:
            blockers.append("duplicate_semantic_presentation_id")
            continue

        state = str(item.get("semantic_state", "")).strip()
        if state not in ALLOWED_SEMANTIC_STATES:
            blockers.append(f"semantic_{index}_state_invalid")

        semantic_value_present = "semantic_value" in item
        semantic_value = item.get("semantic_value")

        if state == "observed":
            if not semantic_value_present:
                blockers.append(f"semantic_{index}_observed_value_missing")
            elif _serialized_size(semantic_value) > max_semantic_bytes:
                blockers.append(f"semantic_{index}_value_too_large")
        elif semantic_value_present and semantic_value is not None:
            blockers.append(f"semantic_{index}_nonobserved_value_must_be_null")

        semantic_digest = (
            _sha(
                {
                    "semantic_projection_id": projection_id,
                    "semantic_schema_digest": schema_digest,
                    "semantic_value": semantic_value,
                }
            )
            if state == "observed" and semantic_value_present
            else ""
        )

        result[presentation_id] = {
            "presentation_id": presentation_id,
            "semantic_state": state,
            "semantic_digest": semantic_digest,
        }

    missing = sorted(presentation_ids.difference(result))
    if missing:
        blockers.append("presentation_semantics_incomplete")

    return projection_id, schema_digest, result


def _sector_list(
    descent: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    raw = descent.get("descent_sectors", [])
    if not isinstance(raw, list):
        blockers.append("descent_sectors_not_list")
        return []

    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"sector_{index}_not_object")
            continue
        sector_id = str(item.get("sector_id", "")).strip()
        if not sector_id:
            blockers.append(f"sector_{index}_id_missing")
            continue
        if sector_id in seen:
            blockers.append("duplicate_sector_id")
            continue
        seen.add(sector_id)
        result.append(dict(item))
    return result


def _pair_obstruction_witnesses(
    members: list[str],
    semantic_table: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    witnesses: list[dict[str, Any]] = []
    for left, right in itertools.combinations(sorted(members), 2):
        left_sem = semantic_table.get(left, {})
        right_sem = semantic_table.get(right, {})
        if (
            left_sem.get("semantic_state") == "observed"
            and right_sem.get("semantic_state") == "observed"
            and left_sem.get("semantic_digest")
            != right_sem.get("semantic_digest")
        ):
            witnesses.append(
                {
                    "obstruction_kind": "related_presentations_have_unequal_semantics",
                    "left_presentation_id": left,
                    "right_presentation_id": right,
                    "left_semantic_digest": str(
                        left_sem.get("semantic_digest", "")
                    ),
                    "right_semantic_digest": str(
                        right_sem.get("semantic_digest", "")
                    ),
                }
            )
    return witnesses


def _diagnose_sector(
    sector: Mapping[str, Any],
    semantic_table: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
    index: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
    sector_id = str(sector.get("sector_id", f"sector-{index}"))

    raw_members = sector.get("presentation_ids", [])
    if not isinstance(raw_members, list):
        blockers.append(f"sector_{index}_presentation_ids_not_list")
        raw_members = []
    members = sorted({str(x) for x in raw_members if str(x)})

    missing_members = [
        presentation_id
        for presentation_id in members
        if presentation_id not in semantic_table
    ]
    if missing_members:
        blockers.append(f"sector_{index}_semantic_member_missing")

    preinvariant_status = str(sector.get("descent_status", ""))

    if len(members) <= 1:
        state = LOCAL_ONLY
        descent_conclusion = LOCAL_SEMANTIC
        common_digest = (
            str(
                semantic_table.get(members[0], {}).get(
                    "semantic_digest",
                    "",
                )
            )
            if members
            else ""
        )
        return (
            {
                "sector_id": sector_id,
                "presentation_ids": members,
                "presentation_count": len(members),
                "preinvariant_v7_4_status": preinvariant_status,
                "presentation_invariance_status": state,
                "presentation_invariant": True,
                "all_related_presentations_semantically_equal": True,
                "runtime_descent_conclusion": descent_conclusion,
                "common_semantic_digest": common_digest,
                "semantic_state_counts": {
                    "observed": sum(
                        1
                        for member in members
                        if semantic_table.get(member, {}).get("semantic_state")
                        == "observed"
                    ),
                    "held": 0,
                    "unavailable": 0,
                },
                "compatibility_promoted_to_invariance": False,
                "formal_factorization_claimed": False,
            },
            [],
            None,
        )

    states = [
        str(semantic_table.get(member, {}).get("semantic_state", ""))
        for member in members
    ]

    obstruction_witnesses = _pair_obstruction_witnesses(
        members,
        semantic_table,
    )

    observed_digests = {
        str(semantic_table.get(member, {}).get("semantic_digest", ""))
        for member in members
        if semantic_table.get(member, {}).get("semantic_state") == "observed"
    }

    if obstruction_witnesses:
        invariance_status = INVARIANCE_OBSTRUCTED
        invariant = False
        descent_conclusion = DESCENT_DENIED
        common_digest = ""
        quotient_witness = None
    elif any(state != "observed" for state in states):
        invariance_status = INVARIANCE_HELD
        invariant = False
        descent_conclusion = DESCENT_HELD
        common_digest = (
            next(iter(observed_digests))
            if len(observed_digests) == 1
            else ""
        )
        quotient_witness = None
    elif len(observed_digests) == 1:
        invariance_status = INVARIANT
        invariant = True
        descent_conclusion = DESCENT_AUTHORIZED
        common_digest = next(iter(observed_digests))
        quotient_witness = {
            "quotient_semantic_witness_id": "quotient-semantic-"
            + _sha(
                {
                    "sector_id": sector_id,
                    "presentation_ids": members,
                    "semantic_digest": common_digest,
                }
            )[:16],
            "sector_id": sector_id,
            "representative_presentation_ids": members,
            "semantic_digest": common_digest,
            "representative_count": len(members),
            "finite_runtime_factorization_witness": True,
            "formal_quotient_factorization_proof": False,
        }
    else:
        invariance_status = INVARIANCE_OBSTRUCTED
        invariant = False
        descent_conclusion = DESCENT_DENIED
        common_digest = ""
        quotient_witness = None
        blockers.append(f"sector_{index}_unexpected_semantic_partition")

    return (
        {
            "sector_id": sector_id,
            "presentation_ids": members,
            "presentation_count": len(members),
            "preinvariant_v7_4_status": preinvariant_status,
            "presentation_invariance_status": invariance_status,
            "presentation_invariant": invariant,
            "all_related_presentations_semantically_equal": invariant,
            "runtime_descent_conclusion": descent_conclusion,
            "common_semantic_digest": common_digest,
            "semantic_state_counts": {
                "observed": states.count("observed"),
                "held": states.count("held"),
                "unavailable": states.count("unavailable"),
            },
            "obstruction_witness_count": len(obstruction_witnesses),
            "compatibility_promoted_to_invariance": False,
            "formal_factorization_claimed": False,
        },
        obstruction_witnesses,
        quotient_witness,
    )


def build_observability_presentation_invariance(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityPresentationInvarianceResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_presentation_invariance_plan_v7_7.json"
    descent_path = root / "observability_dependent_origination_descent_packet_v7_4.json"
    semantics_path = root / "observability_presentation_semantics_input_v7_7.json"
    output_path = root / "observability_presentation_invariance_packet_v7_7.json"
    receipt_path = root / "observability_presentation_invariance_receipt_v7_7.json"
    audit_path = root / "observability_presentation_invariance_audit_v7_7.jsonl"

    if ctx.get("observability_presentation_invariance_enabled") is not True:
        blockers.append("presentation_invariance_enabled_not_true")
    if ctx.get("apply_observability_presentation_invariance") is not True:
        blockers.append("apply_presentation_invariance_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_PRESENTATION_INVARIANCE_AUTHORITY_READY":
        blockers.append("presentation_invariance_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "descent_packet_read_allowed",
        "semantics_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    descent = _read_json(descent_path)
    semantics_packet = _read_json(semantics_path)

    max_presentations = 128
    max_semantic_bytes = 8192
    if not plan:
        blockers.append("presentation_invariance_plan_missing_or_invalid")
    else:
        max_presentations, max_semantic_bytes = _validate_plan(plan, blockers)

    if not descent:
        blockers.append("dependent_origination_descent_packet_missing_or_invalid")
    elif descent.get("version") != DESCENT_VERSION:
        blockers.append("dependent_origination_descent_packet_version_invalid")

    if not semantics_packet:
        blockers.append("presentation_semantics_input_missing_or_invalid")
    elif semantics_packet.get("version") != SEMANTICS_VERSION:
        blockers.append("presentation_semantics_input_version_invalid")

    presentation_ids = _presentation_ids(descent, blockers) if descent else set()
    if len(presentation_ids) > max_presentations:
        blockers.append("presentation_count_exceeds_plan_bound")

    projection_id = ""
    schema_digest = ""
    semantic_table: dict[str, dict[str, Any]] = {}

    if plan and descent and semantics_packet:
        descent_digest = _sha(descent)
        if str(plan.get("source_descent_packet_digest", "")) != descent_digest:
            blockers.append("plan_source_descent_packet_digest_mismatch")
        if (
            str(semantics_packet.get("source_descent_packet_digest", ""))
            != descent_digest
        ):
            blockers.append("semantics_source_descent_packet_digest_mismatch")
        if (
            str(plan.get("semantic_projection_id", ""))
            != str(semantics_packet.get("semantic_projection_id", ""))
        ):
            blockers.append("semantic_projection_id_mismatch")
        if (
            str(plan.get("semantic_schema_digest", ""))
            != str(semantics_packet.get("semantic_schema_digest", ""))
        ):
            blockers.append("semantic_schema_digest_mismatch")

        projection_id, schema_digest, semantic_table = _semantic_table(
            semantics_packet,
            presentation_ids,
            max_semantic_bytes=max_semantic_bytes,
            blockers=blockers,
        )

    sectors = _sector_list(descent, blockers) if descent else []

    diagnosed_sectors: list[dict[str, Any]] = []
    obstruction_witnesses: list[dict[str, Any]] = []
    quotient_semantic_witnesses: list[dict[str, Any]] = []

    if not blockers:
        for index, sector in enumerate(sectors):
            diagnosed, obstructions, quotient_witness = _diagnose_sector(
                sector,
                semantic_table,
                blockers,
                index,
            )
            diagnosed_sectors.append(diagnosed)
            obstruction_witnesses.extend(obstructions)
            if quotient_witness is not None:
                quotient_semantic_witnesses.append(quotient_witness)

    counts = {
        "invariant": sum(
            1
            for sector in diagnosed_sectors
            if sector.get("presentation_invariance_status") == INVARIANT
        ),
        "held": sum(
            1
            for sector in diagnosed_sectors
            if sector.get("presentation_invariance_status") == INVARIANCE_HELD
        ),
        "obstructed": sum(
            1
            for sector in diagnosed_sectors
            if sector.get("presentation_invariance_status")
            == INVARIANCE_OBSTRUCTED
        ),
        "local_only": sum(
            1
            for sector in diagnosed_sectors
            if sector.get("presentation_invariance_status") == LOCAL_ONLY
        ),
    }

    output: dict[str, Any] = {}
    output_written = False

    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif counts["held"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_descent_packet_digest": _sha(descent),
            "semantic_projection_id": projection_id,
            "semantic_schema_digest": schema_digest,
            "presentation_semantics": [
                semantic_table[presentation_id]
                for presentation_id in sorted(semantic_table)
            ],
            "presentation_invariance_sectors": diagnosed_sectors,
            "quotient_semantic_witnesses": quotient_semantic_witnesses,
            "obstruction_witnesses": obstruction_witnesses,
            "summary": {
                "presentation_count": len(presentation_ids),
                "sector_count": len(diagnosed_sectors),
                "invariant_sector_count": counts["invariant"],
                "held_sector_count": counts["held"],
                "obstructed_sector_count": counts["obstructed"],
                "local_only_sector_count": counts["local_only"],
                "quotient_semantic_witness_count": len(
                    quotient_semantic_witnesses
                ),
                "obstruction_witness_count": len(obstruction_witnesses),
            },
            "dependent_origination_boundary": {
                "presentation_invariance_required_for_descent": True,
                "related_presentations_must_have_equal_semantics": True,
                "compatibility_is_not_presentation_invariance": True,
                "temporal_compatibility_is_not_semantic_equality": True,
                "overlap_compatibility_is_not_semantic_equality": True,
                "shared_context_is_not_semantic_equality": True,
                "v7_4_descent_status_is_preinvariance_candidate_only": True,
                "runtime_descent_authorized_only_after_invariance": True,
                "semantic_projection_is_not_ultimate_truth": True,
                "semantic_projection_is_not_substance": True,
                "global_collapse_performed": False,
                "causal_inference_performed": False,
                "source_authority_transferred": False,
                "python_formal_theorem_authority": False,
                "formal_v4_49_factorization_theorem_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "runtime_presentation_relation": "v7.4 generated presentation sectors",
                "runtime_semantic_map": "one explicit bounded semantic projection applied to every presentation",
                "runtime_invariance_predicate": "all representatives in each related sector have equal canonical semantic digests",
                "runtime_obstruction": "a related pair with unequal canonical semantic digests",
                "finite_runtime_factorization_witness": "one common semantic digest assigned to an invariant finite presentation sector",
                "lean_theorem_authority": "formal/KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-presentation-invariance-" + _sha(
        {
            "plan": plan,
            "descent_digest": _sha(descent),
            "semantics_digest": _sha(semantics_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "presentation_count": len(presentation_ids),
        "sector_count": len(diagnosed_sectors),
        "invariant_sector_count": counts["invariant"],
        "held_sector_count": counts["held"],
        "obstructed_sector_count": counts["obstructed"],
        "local_only_sector_count": counts["local_only"],
        "quotient_semantic_witness_count": len(quotient_semantic_witnesses),
        "obstruction_witness_count": len(obstruction_witnesses),
        "output_written": output_written,
        "output_digest": _sha(output),
        "presentation_invariance_required_for_descent": True,
        "compatibility_may_substitute_for_invariance": False,
        "raw_semantic_values_persisted": False,
        "global_collapse_performed": False,
        "causal_inference_performed": False,
        "source_authority_transferred": False,
        "python_formal_theorem_authority": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ObservabilityPresentationInvarianceResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(presentation_ids),
        len(diagnosed_sectors),
        counts["invariant"],
        counts["held"],
        counts["obstructed"],
        counts["local_only"],
        len(quotient_semantic_witnesses),
        len(obstruction_witnesses),
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
