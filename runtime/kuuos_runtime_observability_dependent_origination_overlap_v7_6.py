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

VERSION = "kuuos_runtime_observability_dependent_origination_overlap_v7_6"
PLAN_VERSION = "kuuos_observability_dependent_origination_overlap_plan_v7_6"
DESCENT_VERSION = "kuuos_runtime_observability_dependent_origination_descent_v7_4"
RESTRICTION_VERSION = "kuuos_runtime_observability_dependent_origination_restriction_v7_5"

READY = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_READY"
PARTIAL = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_BLOCKED"

OVERLAP_COMPATIBLE = "overlap_compatible"
OVERLAP_TRIVIAL = "overlap_trivial_single_presentation"
OVERLAP_EMPTY = "no_shared_presentation"
OVERLAP_HELD = "overlap_held"
OVERLAP_OBSTRUCTED = "overlap_restriction_obstructed"
OVERLAP_MISMATCH = "overlap_restriction_mismatch"

SECTOR_STABLE = "pairwise_overlap_coherent_stable_descent"
SECTOR_PAIRWISE_NOT_GLOBAL = (
    "pairwise_overlap_compatible_but_global_descent_obstructed"
)
SECTOR_PAIRWISE_UNRESOLVED = (
    "pairwise_overlap_compatible_but_global_descent_unresolved"
)
SECTOR_OVERLAP_OBSTRUCTED = "overlap_compatibility_obstruction"
SECTOR_OVERLAP_HELD = "overlap_compatibility_held"
SECTOR_GENERATOR_OBSTRUCTION = "generator_local_obstruction_precedes_overlap"
SECTOR_LOCAL_ONLY = "local_only_no_overlap"

V75_STABLE = "restriction_stable_descent"
V75_GENERATOR_OBSTRUCTION = "generator_local_obstruction"
V75_HIGHER_GLUING_OBSTRUCTION = "higher_gluing_obstruction"
V75_LOCAL_UNRESOLVED = "local_restriction_unresolved"
V75_HIGHER_UNRESOLVED = "higher_gluing_unresolved"
V75_LOCAL_ONLY = "local_only_no_restriction"

RESTRICTION_COMPATIBLE = "restriction_compatible"
RESTRICTION_HELD = "restriction_held"
RESTRICTION_OBSTRUCTED = "restriction_obstructed"
RESTRICTION_TRIVIAL = "restriction_trivial"


@dataclass(frozen=True)
class ObservabilityDependentOriginationOverlapResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    sector_count: int
    overlap_pair_count: int
    compatible_overlap_count: int
    trivial_overlap_count: int
    empty_overlap_count: int
    held_overlap_count: int
    obstructed_overlap_count: int
    mismatch_overlap_count: int
    pairwise_not_global_sector_count: int
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
    if plan.get("pairwise_overlap_implies_global_descent") is not False:
        blockers.append("pairwise_overlap_global_descent_must_be_false")
    if plan.get("higher_coherence_claim_allowed") is not False:
        blockers.append("higher_coherence_claim_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_theorem_authority") is not False:
        blockers.append("python_formal_theorem_authority_must_be_false")
    maximum = _i(plan.get("max_overlap_pairs"), 512)
    if maximum < 1 or maximum > 4096:
        blockers.append("max_overlap_pairs_out_of_bounds")
    return maximum


def _presentation_table(
    descent: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = descent.get("presentations", [])
    if not isinstance(raw, list):
        blockers.append("descent_presentations_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"presentation_{index}_not_object")
            continue
        pid = str(item.get("presentation_id", "")).strip()
        if not pid:
            blockers.append(f"presentation_{index}_id_missing")
            continue
        if pid in result:
            blockers.append("duplicate_presentation_id")
            continue
        result[pid] = {
            "presentation_id": pid,
            "provider": str(item.get("provider", "")),
            "operation": str(item.get("operation", "")),
            "source_digest": str(item.get("source_digest", "")),
            "source_status": str(item.get("source_status", "")),
            "availability": str(item.get("availability", "")),
            "window_start": str(item.get("window_start", "")),
            "window_end": str(item.get("window_end", "")),
        }
    return result


def _descent_sector_table(
    descent: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = descent.get("descent_sectors", [])
    if not isinstance(raw, list):
        blockers.append("descent_sectors_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"descent_sector_{index}_not_object")
            continue
        sector_id = str(item.get("sector_id", "")).strip()
        if not sector_id:
            blockers.append(f"descent_sector_{index}_id_missing")
            continue
        if sector_id in result:
            blockers.append("duplicate_descent_sector_id")
            continue
        result[sector_id] = dict(item)
    return result


def _restriction_sector_list(
    restriction: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    raw = restriction.get("restriction_sectors", [])
    if not isinstance(raw, list):
        blockers.append("restriction_sectors_not_list")
        return []
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"restriction_sector_{index}_not_object")
            continue
        sector_id = str(item.get("sector_id", "")).strip()
        if not sector_id:
            blockers.append(f"restriction_sector_{index}_id_missing")
            continue
        if sector_id in seen:
            blockers.append("duplicate_restriction_sector_id")
            continue
        seen.add(sector_id)
        result.append(dict(item))
    return result


def _canonical_comparison_table(
    descent_sector: Mapping[str, Any],
    blockers: list[str],
    sector_id: str,
) -> dict[tuple[str, str], dict[str, Any]]:
    raw = descent_sector.get("comparisons", [])
    if not isinstance(raw, list):
        blockers.append(f"{sector_id}_descent_comparisons_not_list")
        return {}
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"{sector_id}_descent_comparison_{index}_not_object")
            continue
        left = str(item.get("left_presentation_id", "")).strip()
        right = str(item.get("right_presentation_id", "")).strip()
        if not left or not right:
            blockers.append(f"{sector_id}_descent_comparison_{index}_ids_missing")
            continue
        key = _pair_key(left, right)
        if key in result:
            blockers.append(f"{sector_id}_duplicate_descent_comparison")
            continue
        result[key] = {
            "left_presentation_id": key[0],
            "right_presentation_id": key[1],
            "temporal_relation": str(
                item.get("temporal_relation", item.get("relation", ""))
            ),
            "temporally_compatible": item.get("temporally_compatible") is True,
        }
    return result


def _local_comparison_table(
    family_restriction: Mapping[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    raw = family_restriction.get("local_comparisons", [])
    if not isinstance(raw, list):
        return {}
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        left = str(item.get("left_presentation_id", "")).strip()
        right = str(item.get("right_presentation_id", "")).strip()
        if not left or not right:
            continue
        key = _pair_key(left, right)
        result[key] = {
            "left_presentation_id": key[0],
            "right_presentation_id": key[1],
            "temporal_relation": str(
                item.get("temporal_relation", item.get("relation", ""))
            ),
            "temporally_compatible": item.get("temporally_compatible") is True,
        }
    return result


def _overlap_projection(
    *,
    overlap_ids: list[str],
    presentations: Mapping[str, Mapping[str, Any]],
    local_comparisons: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    projection_presentations = []
    for pid in overlap_ids:
        presentation = presentations.get(pid, {})
        projection_presentations.append(
            {
                "presentation_id": pid,
                "source_digest": str(presentation.get("source_digest", "")),
                "source_status": str(presentation.get("source_status", "")),
                "availability": str(presentation.get("availability", "")),
                "window_start": str(presentation.get("window_start", "")),
                "window_end": str(presentation.get("window_end", "")),
            }
        )

    projection_comparisons = []
    for left, right in itertools.combinations(overlap_ids, 2):
        comparison = local_comparisons.get(_pair_key(left, right))
        if comparison is not None:
            projection_comparisons.append(dict(comparison))

    return {
        "presentation_semantics": projection_presentations,
        "local_comparisons": projection_comparisons,
    }


def _validate_family_projection_against_canonical(
    *,
    overlap_ids: list[str],
    family_table: Mapping[tuple[str, str], Mapping[str, Any]],
    canonical_table: Mapping[tuple[str, str], Mapping[str, Any]],
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    for left, right in itertools.combinations(overlap_ids, 2):
        key = _pair_key(left, right)
        family_cmp = family_table.get(key)
        canonical_cmp = canonical_table.get(key)
        if canonical_cmp is None:
            reasons.append(f"canonical_comparison_missing:{left}:{right}")
            continue
        if family_cmp is None:
            reasons.append(f"family_comparison_missing:{left}:{right}")
            continue
        if (
            str(family_cmp.get("temporal_relation", ""))
            != str(canonical_cmp.get("temporal_relation", ""))
        ):
            reasons.append(f"temporal_relation_mismatch:{left}:{right}")
        if (
            family_cmp.get("temporally_compatible") is True
        ) != (
            canonical_cmp.get("temporally_compatible") is True
        ):
            reasons.append(f"temporal_compatibility_mismatch:{left}:{right}")
    return not reasons, reasons


def _overlap_status(
    *,
    left_restriction: Mapping[str, Any],
    right_restriction: Mapping[str, Any],
    overlap_ids: list[str],
    presentations: Mapping[str, Mapping[str, Any]],
    canonical_table: Mapping[tuple[str, str], Mapping[str, Any]],
) -> dict[str, Any]:
    left_status = str(left_restriction.get("restriction_status", ""))
    right_status = str(right_restriction.get("restriction_status", ""))

    if not overlap_ids:
        return {
            "overlap_status": OVERLAP_EMPTY,
            "overlap_presentation_ids": [],
            "overlap_presentation_count": 0,
            "left_projection_digest": "",
            "right_projection_digest": "",
            "projection_equal": True,
            "projection_validation_reasons": [],
        }

    left_table = _local_comparison_table(left_restriction)
    right_table = _local_comparison_table(right_restriction)

    left_projection = _overlap_projection(
        overlap_ids=overlap_ids,
        presentations=presentations,
        local_comparisons=left_table,
    )
    right_projection = _overlap_projection(
        overlap_ids=overlap_ids,
        presentations=presentations,
        local_comparisons=right_table,
    )

    left_valid, left_reasons = _validate_family_projection_against_canonical(
        overlap_ids=overlap_ids,
        family_table=left_table,
        canonical_table=canonical_table,
    )
    right_valid, right_reasons = _validate_family_projection_against_canonical(
        overlap_ids=overlap_ids,
        family_table=right_table,
        canonical_table=canonical_table,
    )

    left_digest = _sha(left_projection)
    right_digest = _sha(right_projection)
    projection_equal = left_projection == right_projection

    reasons = [f"left:{reason}" for reason in left_reasons] + [
        f"right:{reason}" for reason in right_reasons
    ]

    if left_status == RESTRICTION_OBSTRUCTED or right_status == RESTRICTION_OBSTRUCTED:
        status = OVERLAP_OBSTRUCTED
    elif left_status == RESTRICTION_HELD or right_status == RESTRICTION_HELD:
        status = OVERLAP_HELD
    elif not left_valid or not right_valid or not projection_equal:
        status = OVERLAP_MISMATCH
    elif len(overlap_ids) == 1:
        status = OVERLAP_TRIVIAL
    else:
        status = OVERLAP_COMPATIBLE

    return {
        "overlap_status": status,
        "overlap_presentation_ids": overlap_ids,
        "overlap_presentation_count": len(overlap_ids),
        "left_projection_digest": left_digest,
        "right_projection_digest": right_digest,
        "projection_equal": projection_equal,
        "projection_validation_reasons": reasons,
    }


def _sector_diagnosis(
    source_diagnosis: str,
    overlap_records: list[dict[str, Any]],
) -> str:
    statuses = {record["overlap_status"] for record in overlap_records}

    if source_diagnosis == V75_LOCAL_ONLY:
        return SECTOR_LOCAL_ONLY
    if source_diagnosis == V75_GENERATOR_OBSTRUCTION:
        return SECTOR_GENERATOR_OBSTRUCTION
    if OVERLAP_OBSTRUCTED in statuses or OVERLAP_MISMATCH in statuses:
        return SECTOR_OVERLAP_OBSTRUCTED
    if OVERLAP_HELD in statuses:
        return SECTOR_OVERLAP_HELD
    if source_diagnosis == V75_HIGHER_GLUING_OBSTRUCTION:
        return SECTOR_PAIRWISE_NOT_GLOBAL
    if source_diagnosis in {V75_LOCAL_UNRESOLVED, V75_HIGHER_UNRESOLVED}:
        return SECTOR_PAIRWISE_UNRESOLVED
    if source_diagnosis == V75_STABLE:
        return SECTOR_STABLE
    return SECTOR_PAIRWISE_UNRESOLVED


def _diagnose_sector(
    *,
    restriction_sector: Mapping[str, Any],
    descent_sector: Mapping[str, Any],
    presentations: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sector_id = str(restriction_sector.get("sector_id", ""))
    source_diagnosis = str(restriction_sector.get("restriction_diagnosis", ""))

    raw_families = restriction_sector.get("conditioning_family_restrictions", [])
    if not isinstance(raw_families, list):
        blockers.append(f"{sector_id}_conditioning_family_restrictions_not_list")
        raw_families = []

    families: list[dict[str, Any]] = [
        dict(item) for item in raw_families if isinstance(item, Mapping)
    ]
    canonical_table = _canonical_comparison_table(
        descent_sector,
        blockers,
        sector_id,
    )

    overlap_records: list[dict[str, Any]] = []
    for left, right in itertools.combinations(families, 2):
        left_id = str(left.get("condition_family_id", ""))
        right_id = str(right.get("condition_family_id", ""))
        left_members = {
            str(x) for x in left.get("presentation_ids", []) if str(x)
        }
        right_members = {
            str(x) for x in right.get("presentation_ids", []) if str(x)
        }
        overlap_ids = sorted(left_members.intersection(right_members))
        status_record = _overlap_status(
            left_restriction=left,
            right_restriction=right,
            overlap_ids=overlap_ids,
            presentations=presentations,
            canonical_table=canonical_table,
        )
        overlap_records.append(
            {
                "left_condition_family_id": left_id,
                "right_condition_family_id": right_id,
                **status_record,
                "common_restriction_witness_present": (
                    status_record["overlap_status"]
                    in {OVERLAP_COMPATIBLE, OVERLAP_TRIVIAL}
                ),
                "common_restriction_is_substance": False,
                "global_descent_inferred_from_pairwise_overlap": False,
            }
        )

    diagnosis = _sector_diagnosis(source_diagnosis, overlap_records)
    nonempty_overlap_count = sum(
        1 for record in overlap_records if record["overlap_presentation_count"] > 0
    )
    compatible_or_trivial_count = sum(
        1
        for record in overlap_records
        if record["overlap_status"] in {OVERLAP_COMPATIBLE, OVERLAP_TRIVIAL}
    )

    return (
        {
            "sector_id": sector_id,
            "source_restriction_diagnosis": source_diagnosis,
            "overlap_diagnosis": diagnosis,
            "conditioning_family_count": len(families),
            "conditioning_family_pair_count": len(overlap_records),
            "nonempty_overlap_count": nonempty_overlap_count,
            "compatible_or_trivial_overlap_count": compatible_or_trivial_count,
            "pairwise_overlap_compatibility_sufficient_for_global_descent": False,
            "overlap_records": overlap_records,
            "formal_global_amalgamation_claimed": False,
            "higher_coherence_claimed": False,
        },
        overlap_records,
    )


def build_observability_dependent_origination_overlap(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityDependentOriginationOverlapResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_dependent_origination_overlap_plan_v7_6.json"
    descent_path = root / "observability_dependent_origination_descent_packet_v7_4.json"
    restriction_path = root / "observability_dependent_origination_restriction_packet_v7_5.json"
    output_path = root / "observability_dependent_origination_overlap_packet_v7_6.json"
    receipt_path = root / "observability_dependent_origination_overlap_receipt_v7_6.json"
    audit_path = root / "observability_dependent_origination_overlap_audit_v7_6.jsonl"

    if ctx.get("observability_dependent_origination_overlap_enabled") is not True:
        blockers.append("dependent_origination_overlap_enabled_not_true")
    if ctx.get("apply_observability_dependent_origination_overlap") is not True:
        blockers.append("apply_dependent_origination_overlap_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_OVERLAP_AUTHORITY_READY":
        blockers.append("dependent_origination_overlap_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "descent_packet_read_allowed",
        "restriction_packet_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    descent = _read_json(descent_path)
    restriction = _read_json(restriction_path)
    max_overlap_pairs = 512

    if not plan:
        blockers.append("dependent_origination_overlap_plan_missing_or_invalid")
    else:
        max_overlap_pairs = _validate_plan(plan, blockers)

    if not descent:
        blockers.append("descent_packet_missing_or_invalid")
    elif descent.get("version") != DESCENT_VERSION:
        blockers.append("descent_packet_version_invalid")

    if not restriction:
        blockers.append("restriction_packet_missing_or_invalid")
    elif restriction.get("version") != RESTRICTION_VERSION:
        blockers.append("restriction_packet_version_invalid")

    if plan and descent and restriction:
        descent_digest = _sha(descent)
        restriction_digest = _sha(restriction)
        if str(plan.get("source_descent_packet_digest", "")) != descent_digest:
            blockers.append("source_descent_packet_digest_mismatch")
        if str(plan.get("source_restriction_packet_digest", "")) != restriction_digest:
            blockers.append("source_restriction_packet_digest_mismatch")
        if str(restriction.get("source_descent_packet_digest", "")) != descent_digest:
            blockers.append("restriction_source_descent_packet_digest_mismatch")
        restriction_boundary = _m(restriction.get("dependent_origination_boundary"))
        if restriction_boundary.get("global_collapse_performed") is not False:
            blockers.append("restriction_global_collapse_boundary_invalid")
        if restriction_boundary.get("causal_inference_performed") is not False:
            blockers.append("restriction_causal_boundary_invalid")
        if restriction_boundary.get("source_authority_transferred") is not False:
            blockers.append("restriction_authority_boundary_invalid")

    presentations = _presentation_table(descent, blockers) if descent else {}
    descent_sectors = _descent_sector_table(descent, blockers) if descent else {}
    restriction_sectors = (
        _restriction_sector_list(restriction, blockers) if restriction else []
    )

    diagnosed_sectors: list[dict[str, Any]] = []
    all_overlap_records: list[dict[str, Any]] = []

    if not blockers:
        for sector in restriction_sectors:
            sector_id = str(sector.get("sector_id", ""))
            descent_sector = descent_sectors.get(sector_id)
            if descent_sector is None:
                blockers.append(f"restriction_sector_missing_in_descent:{sector_id}")
                continue
            diagnosed, overlap_records = _diagnose_sector(
                restriction_sector=sector,
                descent_sector=descent_sector,
                presentations=presentations,
                blockers=blockers,
            )
            diagnosed_sectors.append(diagnosed)
            all_overlap_records.extend(overlap_records)

    if len(all_overlap_records) > max_overlap_pairs:
        blockers.append("overlap_pair_count_exceeds_plan_bound")

    overlap_counts = {
        "compatible": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_COMPATIBLE
        ),
        "trivial": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_TRIVIAL
        ),
        "empty": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_EMPTY
        ),
        "held": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_HELD
        ),
        "obstructed": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_OBSTRUCTED
        ),
        "mismatch": sum(
            1 for record in all_overlap_records
            if record.get("overlap_status") == OVERLAP_MISMATCH
        ),
    }

    sector_counts = {
        "pairwise_not_global": sum(
            1 for sector in diagnosed_sectors
            if sector.get("overlap_diagnosis") == SECTOR_PAIRWISE_NOT_GLOBAL
        ),
        "overlap_obstructed": sum(
            1 for sector in diagnosed_sectors
            if sector.get("overlap_diagnosis") == SECTOR_OVERLAP_OBSTRUCTED
        ),
        "overlap_held": sum(
            1 for sector in diagnosed_sectors
            if sector.get("overlap_diagnosis") in {
                SECTOR_OVERLAP_HELD,
                SECTOR_PAIRWISE_UNRESOLVED,
            }
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        if (
            sector_counts["overlap_obstructed"] > 0
            or sector_counts["pairwise_not_global"] > 0
        ):
            status = OBSTRUCTED
        elif sector_counts["overlap_held"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_descent_packet_digest": _sha(descent),
            "source_restriction_packet_digest": _sha(restriction),
            "overlap_sectors": diagnosed_sectors,
            "summary": {
                "sector_count": len(diagnosed_sectors),
                "overlap_pair_count": len(all_overlap_records),
                "compatible_overlap_count": overlap_counts["compatible"],
                "trivial_overlap_count": overlap_counts["trivial"],
                "empty_overlap_count": overlap_counts["empty"],
                "held_overlap_count": overlap_counts["held"],
                "obstructed_overlap_count": overlap_counts["obstructed"],
                "mismatch_overlap_count": overlap_counts["mismatch"],
                "pairwise_not_global_sector_count": sector_counts[
                    "pairwise_not_global"
                ],
            },
            "dependent_origination_boundary": {
                "primary_model_is_graph": False,
                "many_presentations_preserved": True,
                "condition_families_preserved": True,
                "pairwise_overlap_checked_on_common_restrictions": True,
                "pairwise_overlap_compatibility_sufficient_for_global_descent": False,
                "pairwise_overlap_does_not_imply_global_amalgamation": True,
                "global_collapse_performed": False,
                "causal_inference_performed": False,
                "causal_direction_inferred": False,
                "source_authority_transferred": False,
                "python_formal_theorem_authority": False,
                "formal_v3_13_overlap_theorem_replaced": False,
                "formal_v3_16_global_gluing_theorem_replaced": False,
                "formal_v4_61_higher_coherence_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_shadow_only": True,
                "v3_13_reference": "pairwise overlap compatibility has concrete shared-coordinate consequences",
                "v3_16_reference": "a globally compatible chosen local family can glue, while weaker pairwise-existence quantifiers do not automatically supply that family",
                "runtime_overlap": "conditioning-family restrictions compared only on shared presentations",
                "runtime_gap": "pairwise-compatible overlaps can coexist with v7.5 higher gluing obstruction",
                "lean_theorem_authority": "formal/KUOS only",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-dependent-origination-overlap-" + _sha(
        {
            "plan": plan,
            "descent_digest": _sha(descent),
            "restriction_digest": _sha(restriction),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "sector_count": len(diagnosed_sectors),
        "overlap_pair_count": len(all_overlap_records),
        "compatible_overlap_count": overlap_counts["compatible"],
        "trivial_overlap_count": overlap_counts["trivial"],
        "empty_overlap_count": overlap_counts["empty"],
        "held_overlap_count": overlap_counts["held"],
        "obstructed_overlap_count": overlap_counts["obstructed"],
        "mismatch_overlap_count": overlap_counts["mismatch"],
        "pairwise_not_global_sector_count": sector_counts[
            "pairwise_not_global"
        ],
        "output_written": output_written,
        "output_digest": _sha(output),
        "pairwise_overlap_compatibility_sufficient_for_global_descent": False,
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

    return ObservabilityDependentOriginationOverlapResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(diagnosed_sectors),
        len(all_overlap_records),
        overlap_counts["compatible"],
        overlap_counts["trivial"],
        overlap_counts["empty"],
        overlap_counts["held"],
        overlap_counts["obstructed"],
        overlap_counts["mismatch"],
        sector_counts["pairwise_not_global"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
