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

VERSION = "kuuos_runtime_observability_dependent_origination_restriction_v7_5"
PLAN_VERSION = "kuuos_observability_dependent_origination_restriction_plan_v7_5"
SOURCE_VERSION = "kuuos_runtime_observability_dependent_origination_descent_v7_4"

READY = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_READY"
PARTIAL = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_BLOCKED"

RESTRICTION_COMPATIBLE = "restriction_compatible"
RESTRICTION_HELD = "restriction_held"
RESTRICTION_OBSTRUCTED = "restriction_obstructed"
RESTRICTION_TRIVIAL = "restriction_trivial"

STABLE_DESCENT = "restriction_stable_descent"
GENERATOR_LOCAL_OBSTRUCTION = "generator_local_obstruction"
HIGHER_GLUING_OBSTRUCTION = "higher_gluing_obstruction"
LOCAL_RESTRICTION_UNRESOLVED = "local_restriction_unresolved"
HIGHER_GLUING_UNRESOLVED = "higher_gluing_unresolved"
LOCAL_ONLY_NO_RESTRICTION = "local_only_no_restriction"

COMPATIBLE_TEMPORAL_RELATIONS = {"overlap", "within_tolerance"}
UNRESOLVED_TEMPORAL_RELATIONS = {
    "insufficient_time_metadata",
    "source_obstruction",
    "missing_pair_presentation",
}


@dataclass(frozen=True)
class ObservabilityDependentOriginationRestrictionResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    sector_count: int
    restriction_family_count: int
    stable_descent_count: int
    generator_local_obstruction_count: int
    higher_gluing_obstruction_count: int
    unresolved_count: int
    local_only_count: int
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


def _pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> int:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("global_collapse_allowed") is not False:
        blockers.append("global_collapse_must_be_false")
    if plan.get("causal_inference_allowed") is not False:
        blockers.append("causal_inference_must_be_false")
    if plan.get("higher_coherence_claim_allowed") is not False:
        blockers.append("higher_coherence_claim_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_theorem_authority") is not False:
        blockers.append("python_formal_theorem_authority_must_be_false")
    maximum = _i(plan.get("max_conditioning_families"), 128)
    if maximum < 1 or maximum > 512:
        blockers.append("max_conditioning_families_out_of_bounds")
    return maximum


def _family_table(
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = source.get("conditioning_families", [])
    if not isinstance(raw, list):
        blockers.append("conditioning_families_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"conditioning_family_{index}_not_object")
            continue
        family_id = str(item.get("condition_family_id", "")).strip()
        if not family_id:
            blockers.append(f"conditioning_family_{index}_id_missing")
            continue
        if family_id in result:
            blockers.append("duplicate_conditioning_family_id")
            continue
        presentation_ids = item.get("presentation_ids", [])
        if not isinstance(presentation_ids, list):
            blockers.append(f"conditioning_family_{index}_presentation_ids_not_list")
            continue
        result[family_id] = {
            "condition_family_id": family_id,
            "condition_kind": str(item.get("condition_kind", "")),
            "condition_digest": str(item.get("condition_digest", "")),
            "presentation_ids": sorted({str(x) for x in presentation_ids}),
            "non_reified": item.get("non_reified") is True,
        }
    return result


def _comparison_table(
    sector: Mapping[str, Any],
    blockers: list[str],
    sector_index: int,
) -> dict[tuple[str, str], dict[str, Any]]:
    raw = sector.get("comparisons", [])
    if not isinstance(raw, list):
        blockers.append(f"sector_{sector_index}_comparisons_not_list")
        return {}
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"sector_{sector_index}_comparison_{index}_not_object")
            continue
        left = str(item.get("left_presentation_id", "")).strip()
        right = str(item.get("right_presentation_id", "")).strip()
        if not left or not right:
            blockers.append(f"sector_{sector_index}_comparison_{index}_ids_missing")
            continue
        key = _pair_key(left, right)
        if key in result:
            blockers.append(f"sector_{sector_index}_duplicate_comparison")
            continue
        result[key] = dict(item)
    return result


def _restriction_status(
    members: list[str],
    comparisons: Mapping[tuple[str, str], Mapping[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    if len(members) < 2:
        return RESTRICTION_TRIVIAL, []

    local_records: list[dict[str, Any]] = []
    obstructed = False
    unresolved = False

    for left, right in itertools.combinations(sorted(members), 2):
        comparison = comparisons.get(_pair_key(left, right))
        if comparison is None:
            unresolved = True
            local_records.append(
                {
                    "left_presentation_id": left,
                    "right_presentation_id": right,
                    "temporal_relation": "missing_pair_presentation",
                    "temporally_compatible": False,
                }
            )
            continue

        temporal_relation = str(
            comparison.get(
                "temporal_relation",
                comparison.get("relation", ""),
            )
        )
        temporally_compatible = comparison.get("temporally_compatible") is True
        local_records.append(
            {
                "left_presentation_id": left,
                "right_presentation_id": right,
                "temporal_relation": temporal_relation,
                "temporally_compatible": temporally_compatible,
            }
        )

        if temporal_relation == "disjoint":
            obstructed = True
        elif temporal_relation in UNRESOLVED_TEMPORAL_RELATIONS:
            unresolved = True
        elif (
            temporal_relation in COMPATIBLE_TEMPORAL_RELATIONS
            and temporally_compatible
        ):
            continue
        else:
            unresolved = True

    if obstructed:
        return RESTRICTION_OBSTRUCTED, local_records
    if unresolved:
        return RESTRICTION_HELD, local_records
    return RESTRICTION_COMPATIBLE, local_records


def _sector_obstructions(
    source: Mapping[str, Any],
    members: set[str],
) -> list[dict[str, Any]]:
    raw = source.get("obstruction_witnesses", [])
    if not isinstance(raw, list):
        return []
    result: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        left = str(item.get("left_presentation_id", ""))
        right = str(item.get("right_presentation_id", ""))
        if left in members and right in members:
            result.append(dict(item))
    return result


def _condition_family_contains_pair(
    family_restrictions: list[dict[str, Any]],
    left: str,
    right: str,
) -> bool:
    wanted = {left, right}
    for restriction in family_restrictions:
        members = set(str(x) for x in restriction.get("presentation_ids", []))
        if wanted.issubset(members):
            return True
    return False


def _diagnose_sector(
    *,
    source: Mapping[str, Any],
    sector: Mapping[str, Any],
    sector_index: int,
    families: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> tuple[dict[str, Any], int]:
    sector_id = str(sector.get("sector_id", f"sector-{sector_index}"))
    members_raw = sector.get("presentation_ids", [])
    if not isinstance(members_raw, list):
        blockers.append(f"sector_{sector_index}_presentation_ids_not_list")
        members_raw = []
    members = sorted({str(x) for x in members_raw})
    member_set = set(members)
    descent_status = str(sector.get("descent_status", ""))

    comparisons = _comparison_table(sector, blockers, sector_index)

    family_ids_raw = sector.get("condition_family_ids", [])
    if not isinstance(family_ids_raw, list):
        blockers.append(f"sector_{sector_index}_condition_family_ids_not_list")
        family_ids_raw = []

    family_restrictions: list[dict[str, Any]] = []
    for family_id_any in sorted({str(x) for x in family_ids_raw}):
        family = families.get(family_id_any)
        if family is None:
            blockers.append(f"sector_{sector_index}_unknown_condition_family:{family_id_any}")
            continue
        restricted_members = sorted(
            member_set.intersection(set(family["presentation_ids"]))
        )
        status, local_records = _restriction_status(
            restricted_members,
            comparisons,
        )
        family_restrictions.append(
            {
                "condition_family_id": family_id_any,
                "condition_kind": str(family.get("condition_kind", "")),
                "condition_digest": str(family.get("condition_digest", "")),
                "presentation_ids": restricted_members,
                "presentation_count": len(restricted_members),
                "restriction_status": status,
                "local_comparison_count": len(local_records),
                "local_comparisons": local_records,
                "condition_is_substance": False,
            }
        )

    restriction_statuses = {
        restriction["restriction_status"] for restriction in family_restrictions
    }
    sector_obstructions = _sector_obstructions(source, member_set)
    higher_gluing_witnesses: list[dict[str, Any]] = []

    if descent_status == "local_presentation_only":
        diagnosis = LOCAL_ONLY_NO_RESTRICTION
    elif descent_status == "descended_contextual_presentation":
        if RESTRICTION_OBSTRUCTED in restriction_statuses or RESTRICTION_HELD in restriction_statuses:
            blockers.append(f"sector_{sector_index}_descended_but_restriction_not_compatible")
            diagnosis = STABLE_DESCENT
        else:
            diagnosis = STABLE_DESCENT
    elif descent_status == "descent_obstructed":
        if RESTRICTION_OBSTRUCTED in restriction_statuses:
            diagnosis = GENERATOR_LOCAL_OBSTRUCTION
        elif RESTRICTION_HELD in restriction_statuses:
            diagnosis = LOCAL_RESTRICTION_UNRESOLVED
        else:
            diagnosis = HIGHER_GLUING_OBSTRUCTION
            for witness in sector_obstructions:
                left = str(witness.get("left_presentation_id", ""))
                right = str(witness.get("right_presentation_id", ""))
                if not _condition_family_contains_pair(
                    family_restrictions,
                    left,
                    right,
                ):
                    higher_gluing_witnesses.append(
                        {
                            "obstruction_kind": str(
                                witness.get("obstruction_kind", "")
                            ),
                            "left_presentation_id": left,
                            "right_presentation_id": right,
                            "scope": "across_conditioning_families",
                        }
                    )
    elif descent_status == "descent_held":
        if RESTRICTION_HELD in restriction_statuses:
            diagnosis = LOCAL_RESTRICTION_UNRESOLVED
        else:
            diagnosis = HIGHER_GLUING_UNRESOLVED
    else:
        blockers.append(f"sector_{sector_index}_descent_status_unknown")
        diagnosis = HIGHER_GLUING_UNRESOLVED

    return (
        {
            "sector_id": sector_id,
            "presentation_ids": members,
            "source_descent_status": descent_status,
            "restriction_diagnosis": diagnosis,
            "conditioning_family_restrictions": family_restrictions,
            "conditioning_family_restriction_count": len(family_restrictions),
            "higher_gluing_witnesses": higher_gluing_witnesses,
            "higher_gluing_witness_count": len(higher_gluing_witnesses),
            "restriction_preservation_is_formal_v4_61_theorem_claim": False,
            "higher_coherence_claimed": False,
        },
        len(family_restrictions),
    )


def build_observability_dependent_origination_restriction(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityDependentOriginationRestrictionResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_dependent_origination_restriction_plan_v7_5.json"
    source_path = root / "observability_dependent_origination_descent_packet_v7_4.json"
    output_path = root / "observability_dependent_origination_restriction_packet_v7_5.json"
    receipt_path = root / "observability_dependent_origination_restriction_receipt_v7_5.json"
    audit_path = root / "observability_dependent_origination_restriction_audit_v7_5.jsonl"

    if ctx.get("observability_dependent_origination_restriction_enabled") is not True:
        blockers.append("dependent_origination_restriction_enabled_not_true")
    if ctx.get("apply_observability_dependent_origination_restriction") is not True:
        blockers.append("apply_dependent_origination_restriction_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_RESTRICTION_AUTHORITY_READY":
        blockers.append("dependent_origination_restriction_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "source_descent_packet_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    max_families = 128

    if not plan:
        blockers.append("dependent_origination_restriction_plan_missing_or_invalid")
    else:
        max_families = _validate_plan(plan, blockers)

    if not source:
        blockers.append("dependent_origination_descent_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("dependent_origination_descent_packet_version_invalid")

    if source and plan:
        source_digest = _sha(source)
        if str(plan.get("source_descent_packet_digest", "")) != source_digest:
            blockers.append("source_descent_packet_digest_mismatch")
        boundary = _m(source.get("dependent_origination_boundary"))
        if boundary.get("global_collapse_performed") is not False:
            blockers.append("source_global_collapse_boundary_invalid")
        if boundary.get("causal_inference_performed") is not False:
            blockers.append("source_causal_boundary_invalid")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("source_authority_boundary_invalid")

    families = _family_table(source, blockers) if source else {}
    if len(families) > max_families:
        blockers.append("conditioning_family_count_exceeds_plan_bound")

    raw_sectors = source.get("descent_sectors", []) if source else []
    if not isinstance(raw_sectors, list):
        blockers.append("descent_sectors_not_list")
        raw_sectors = []

    restriction_sectors: list[dict[str, Any]] = []
    restriction_family_count = 0
    if not blockers:
        for index, sector in enumerate(raw_sectors):
            if not isinstance(sector, Mapping):
                blockers.append(f"sector_{index}_not_object")
                continue
            diagnosed, count = _diagnose_sector(
                source=source,
                sector=sector,
                sector_index=index,
                families=families,
                blockers=blockers,
            )
            restriction_sectors.append(diagnosed)
            restriction_family_count += count

    counts = {
        "stable_descent": sum(
            1
            for sector in restriction_sectors
            if sector.get("restriction_diagnosis") == STABLE_DESCENT
        ),
        "generator_local_obstruction": sum(
            1
            for sector in restriction_sectors
            if sector.get("restriction_diagnosis") == GENERATOR_LOCAL_OBSTRUCTION
        ),
        "higher_gluing_obstruction": sum(
            1
            for sector in restriction_sectors
            if sector.get("restriction_diagnosis") == HIGHER_GLUING_OBSTRUCTION
        ),
        "unresolved": sum(
            1
            for sector in restriction_sectors
            if sector.get("restriction_diagnosis")
            in {LOCAL_RESTRICTION_UNRESOLVED, HIGHER_GLUING_UNRESOLVED}
        ),
        "local_only": sum(
            1
            for sector in restriction_sectors
            if sector.get("restriction_diagnosis") == LOCAL_ONLY_NO_RESTRICTION
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        if (
            counts["generator_local_obstruction"] > 0
            or counts["higher_gluing_obstruction"] > 0
        ):
            status = OBSTRUCTED
        elif counts["unresolved"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_descent_packet_digest": _sha(source),
            "restriction_sectors": restriction_sectors,
            "summary": {
                "sector_count": len(restriction_sectors),
                "restriction_family_count": restriction_family_count,
                "stable_descent_count": counts["stable_descent"],
                "generator_local_obstruction_count": counts[
                    "generator_local_obstruction"
                ],
                "higher_gluing_obstruction_count": counts[
                    "higher_gluing_obstruction"
                ],
                "unresolved_count": counts["unresolved"],
                "local_only_count": counts["local_only"],
            },
            "dependent_origination_boundary": {
                "restriction_preserves_local_presentation_context": True,
                "local_compatibility_checked_before_higher_gluing": True,
                "higher_gluing_obstruction_is_not_reduced_to_graph_connectivity": True,
                "global_collapse_performed": False,
                "causal_inference_performed": False,
                "causal_direction_inferred": False,
                "source_authority_transferred": False,
                "python_formal_theorem_authority": False,
                "formal_v4_61_restriction_whiskering_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_shadow_only": True,
                "runtime_restriction": "conditioning-family restriction of a v7.4 presentation sector",
                "runtime_preservation_question": "does local bounded compatibility survive restriction",
                "higher_gluing_obstruction": "all generator restrictions compatible while quotient-like sector descent remains obstructed",
                "lean_higher_coherence_authority": "formal/KUOS/DependentOriginationExactUniversalRestrictionWhiskeringV4_61.lean and successors",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-dependent-origination-restriction-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "sector_count": len(restriction_sectors),
        "restriction_family_count": restriction_family_count,
        "stable_descent_count": counts["stable_descent"],
        "generator_local_obstruction_count": counts[
            "generator_local_obstruction"
        ],
        "higher_gluing_obstruction_count": counts["higher_gluing_obstruction"],
        "unresolved_count": counts["unresolved"],
        "local_only_count": counts["local_only"],
        "output_written": output_written,
        "output_digest": _sha(output),
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

    return ObservabilityDependentOriginationRestrictionResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(restriction_sectors),
        restriction_family_count,
        counts["stable_descent"],
        counts["generator_local_obstruction"],
        counts["higher_gluing_obstruction"],
        counts["unresolved"],
        counts["local_only"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
