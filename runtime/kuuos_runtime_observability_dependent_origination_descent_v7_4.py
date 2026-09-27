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

VERSION = "kuuos_runtime_observability_dependent_origination_descent_v7_4"
PLAN_VERSION = "kuuos_observability_dependent_origination_descent_plan_v7_4"
TEMPORAL_VERSION = "kuuos_runtime_observability_temporal_correlation_v7_2"
ALIGNMENT_VERSION = "kuuos_runtime_observability_event_alignment_v7_3"

READY = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_READY"
PARTIAL = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_BLOCKED"

DESCENDED = "descended_contextual_presentation"
HELD = "descent_held"
DESCENT_OBSTRUCTED = "descent_obstructed"
LOCAL_ONLY = "local_presentation_only"

TEMPORALLY_COMPATIBLE_RELATIONS = {"overlap", "within_tolerance"}
TEMPORALLY_UNRESOLVED_RELATIONS = {
    "insufficient_time_metadata",
    "source_obstruction",
}


@dataclass(frozen=True)
class ObservabilityDependentOriginationDescentResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    presentation_count: int
    conditioning_family_count: int
    descent_sector_count: int
    descended_sector_count: int
    held_sector_count: int
    obstructed_sector_count: int
    local_only_sector_count: int
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


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> int:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("global_collapse_allowed") is not False:
        blockers.append("global_collapse_must_be_false")
    if plan.get("substance_reification_allowed") is not False:
        blockers.append("substance_reification_must_be_false")
    if plan.get("causal_inference_allowed") is not False:
        blockers.append("causal_inference_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_theorem_authority") is not False:
        blockers.append("python_formal_theorem_authority_must_be_false")
    maximum = _i(plan.get("max_presentations"), 64)
    if maximum < 1 or maximum > 256:
        blockers.append("max_presentations_out_of_bounds")
    return maximum


class _UnionFind:
    def __init__(self, items: list[str]) -> None:
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: str, right: str) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1

    def classes(self) -> list[list[str]]:
        grouped: dict[str, list[str]] = {}
        for item in self.parent:
            grouped.setdefault(self.find(item), []).append(item)
        return sorted(
            (sorted(members) for members in grouped.values()),
            key=lambda members: (members[0], len(members)),
        )


def _pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def _presentation_table(
    temporal: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = temporal.get("observations", [])
    if not isinstance(raw, list):
        blockers.append("temporal_observations_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"presentation_{index}_not_object")
            continue
        presentation_id = str(item.get("observation_id", "")).strip()
        if not presentation_id:
            blockers.append(f"presentation_{index}_id_missing")
            continue
        if presentation_id in result:
            blockers.append("duplicate_presentation_id")
            continue
        result[presentation_id] = {
            "presentation_id": presentation_id,
            "provider": str(item.get("provider", "")),
            "operation": str(item.get("operation", "")),
            "source_digest": str(item.get("source_digest", "")),
            "source_status": str(item.get("source_status", "")),
            "availability": str(item.get("availability", "")),
            "window_start": str(item.get("window_start", "")),
            "window_end": str(item.get("window_end", "")),
        }
    return result


def _alignment_pair_table(
    alignment: Mapping[str, Any],
    presentation_ids: set[str],
    blockers: list[str],
) -> dict[tuple[str, str], dict[str, Any]]:
    raw = alignment.get("pairs", [])
    if not isinstance(raw, list):
        blockers.append("alignment_pairs_not_list")
        return {}
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"alignment_pair_{index}_not_object")
            continue
        left = str(item.get("left_observation_id", ""))
        right = str(item.get("right_observation_id", ""))
        if left not in presentation_ids or right not in presentation_ids:
            blockers.append(f"alignment_pair_{index}_references_unknown_presentation")
            continue
        key = _pair_key(left, right)
        if key in result:
            blockers.append("duplicate_alignment_pair")
            continue
        result[key] = dict(item)
    return result


def _conditioning_families(
    pair_table: Mapping[tuple[str, str], Mapping[str, Any]],
    union_find: _UnionFind,
) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    families: dict[str, dict[str, Any]] = {}
    membership: dict[str, set[str]] = {}

    for (left, right), pair in pair_table.items():
        evidence = pair.get("shared_identifier_evidence", [])
        if not isinstance(evidence, list) or not evidence:
            continue
        union_find.union(left, right)
        for witness in evidence:
            if not isinstance(witness, Mapping):
                continue
            identifier_type = str(witness.get("identifier_type", ""))
            value_digest = str(witness.get("value_digest", ""))
            condition_digest = _sha(
                {
                    "identifier_type": identifier_type,
                    "value_digest": value_digest,
                }
            )
            family_id = "condition-" + condition_digest[:16]
            family = families.setdefault(
                family_id,
                {
                    "condition_family_id": family_id,
                    "condition_kind": identifier_type,
                    "condition_digest": condition_digest,
                    "presentation_ids": set(),
                    "witness_pair_count": 0,
                    "non_reified": True,
                },
            )
            family["presentation_ids"].update((left, right))
            family["witness_pair_count"] += 1
            membership.setdefault(left, set()).add(family_id)
            membership.setdefault(right, set()).add(family_id)

    public: list[dict[str, Any]] = []
    for family_id in sorted(families):
        family = families[family_id]
        public.append(
            {
                **{k: v for k, v in family.items() if k != "presentation_ids"},
                "presentation_ids": sorted(family["presentation_ids"]),
                "presentation_count": len(family["presentation_ids"]),
            }
        )
    return public, membership


def _classify_sector(
    members: list[str],
    pair_table: Mapping[tuple[str, str], Mapping[str, Any]],
    condition_membership: Mapping[str, set[str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    condition_family_ids = sorted(
        set().union(*(condition_membership.get(member, set()) for member in members))
        if members
        else set()
    )

    if len(members) == 1:
        sector_seed = {
            "members": members,
            "condition_family_ids": condition_family_ids,
            "status": LOCAL_ONLY,
        }
        return (
            {
                "sector_id": "descent-sector-" + _sha(sector_seed)[:16],
                "presentation_ids": members,
                "presentation_count": 1,
                "condition_family_ids": condition_family_ids,
                "condition_family_count": len(condition_family_ids),
                "local_compatibility": "not_applicable_singleton",
                "descent_status": LOCAL_ONLY,
                "descended_presentation_id": "",
                "formal_factorization_claimed": False,
                "higher_coherence_claimed": False,
            },
            [],
        )

    comparisons: list[dict[str, Any]] = []
    obstructions: list[dict[str, Any]] = []
    unresolved = False
    obstructed = False

    for left, right in itertools.combinations(members, 2):
        pair = pair_table.get(_pair_key(left, right))
        if pair is None:
            unresolved = True
            comparisons.append(
                {
                    "left_presentation_id": left,
                    "right_presentation_id": right,
                    "relation": "missing_pair_presentation",
                    "compatible": False,
                }
            )
            continue

        temporal_relation = str(pair.get("temporal_relation", ""))
        temporally_compatible = pair.get("temporally_compatible") is True
        alignment_state = str(pair.get("alignment_state", ""))

        comparison = {
            "left_presentation_id": left,
            "right_presentation_id": right,
            "temporal_relation": temporal_relation,
            "temporally_compatible": temporally_compatible,
            "alignment_state": alignment_state,
            "has_shared_exact_identifier": pair.get("has_shared_exact_identifier") is True,
        }
        comparisons.append(comparison)

        if temporal_relation == "disjoint":
            obstructed = True
            obstructions.append(
                {
                    "obstruction_kind": "related_presentations_temporally_disjoint",
                    "left_presentation_id": left,
                    "right_presentation_id": right,
                    "temporal_relation": temporal_relation,
                    "alignment_state": alignment_state,
                }
            )
        elif temporal_relation in TEMPORALLY_UNRESOLVED_RELATIONS:
            unresolved = True
        elif temporal_relation in TEMPORALLY_COMPATIBLE_RELATIONS and temporally_compatible:
            continue
        else:
            unresolved = True

    if obstructed:
        descent_status = DESCENT_OBSTRUCTED
        local_compatibility = "obstructed"
    elif unresolved:
        descent_status = HELD
        local_compatibility = "unresolved"
    else:
        descent_status = DESCENDED
        local_compatibility = "compatible"

    sector_seed = {
        "members": members,
        "condition_family_ids": condition_family_ids,
        "descent_status": descent_status,
    }
    sector_id = "descent-sector-" + _sha(sector_seed)[:16]
    descended_presentation_id = ""
    if descent_status == DESCENDED:
        descended_presentation_id = "descended-presentation-" + _sha(
            {
                "members": members,
                "condition_family_ids": condition_family_ids,
                "compatibility": comparisons,
            }
        )[:16]

    return (
        {
            "sector_id": sector_id,
            "presentation_ids": members,
            "presentation_count": len(members),
            "condition_family_ids": condition_family_ids,
            "condition_family_count": len(condition_family_ids),
            "local_compatibility": local_compatibility,
            "descent_status": descent_status,
            "descended_presentation_id": descended_presentation_id,
            "comparison_count": len(comparisons),
            "comparisons": comparisons,
            "formal_factorization_claimed": False,
            "higher_coherence_claimed": False,
        },
        obstructions,
    )


def build_observability_dependent_origination_descent(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityDependentOriginationDescentResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_dependent_origination_descent_plan_v7_4.json"
    temporal_path = root / "observability_temporal_correlation_packet_v7_2.json"
    alignment_path = root / "observability_event_alignment_packet_v7_3.json"
    output_path = root / "observability_dependent_origination_descent_packet_v7_4.json"
    receipt_path = root / "observability_dependent_origination_descent_receipt_v7_4.json"
    audit_path = root / "observability_dependent_origination_descent_audit_v7_4.jsonl"

    if ctx.get("observability_dependent_origination_descent_enabled") is not True:
        blockers.append("dependent_origination_descent_enabled_not_true")
    if ctx.get("apply_observability_dependent_origination_descent") is not True:
        blockers.append("apply_dependent_origination_descent_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_DEPENDENT_ORIGINATION_DESCENT_AUTHORITY_READY":
        blockers.append("dependent_origination_descent_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "temporal_packet_read_allowed",
        "alignment_packet_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    temporal = _read_json(temporal_path)
    alignment = _read_json(alignment_path)

    max_presentations = 64
    if not plan:
        blockers.append("dependent_origination_descent_plan_missing_or_invalid")
    else:
        max_presentations = _validate_plan(plan, blockers)
    if not temporal:
        blockers.append("temporal_packet_missing_or_invalid")
    elif temporal.get("version") != TEMPORAL_VERSION:
        blockers.append("temporal_packet_version_invalid")
    if not alignment:
        blockers.append("alignment_packet_missing_or_invalid")
    elif alignment.get("version") != ALIGNMENT_VERSION:
        blockers.append("alignment_packet_version_invalid")

    if temporal and alignment:
        temporal_digest = _sha(temporal)
        alignment_digest = _sha(alignment)
        if str(alignment.get("source_temporal_packet_digest", "")) != temporal_digest:
            blockers.append("alignment_source_temporal_packet_digest_mismatch")
        if str(plan.get("source_temporal_packet_digest", "")) != temporal_digest:
            blockers.append("plan_source_temporal_packet_digest_mismatch")
        if str(plan.get("source_alignment_packet_digest", "")) != alignment_digest:
            blockers.append("plan_source_alignment_packet_digest_mismatch")
        boundary = _m(alignment.get("interpretation_boundary"))
        if boundary.get("causal_inference_performed") is not False:
            blockers.append("alignment_causal_boundary_invalid")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("alignment_authority_boundary_invalid")

    presentations = _presentation_table(temporal, blockers) if temporal else {}
    if len(presentations) > max_presentations:
        blockers.append("presentation_count_exceeds_plan_bound")

    pair_table = (
        _alignment_pair_table(alignment, set(presentations), blockers)
        if alignment
        else {}
    )

    conditioning_families: list[dict[str, Any]] = []
    membership: dict[str, set[str]] = {}
    sectors: list[dict[str, Any]] = []
    obstruction_witnesses: list[dict[str, Any]] = []

    if not blockers:
        uf = _UnionFind(sorted(presentations))
        conditioning_families, membership = _conditioning_families(pair_table, uf)
        for members in uf.classes():
            sector, obstructions = _classify_sector(
                members,
                pair_table,
                membership,
            )
            sectors.append(sector)
            obstruction_witnesses.extend(obstructions)

    public_presentations: list[dict[str, Any]] = []
    for presentation_id in sorted(presentations):
        presentation = presentations[presentation_id]
        public_presentations.append(
            {
                **presentation,
                "condition_family_ids": sorted(membership.get(presentation_id, set())),
                "presentation_is_substance": False,
                "provider_is_ultimate_authority": False,
            }
        )

    counts = {
        "descended": sum(1 for s in sectors if s.get("descent_status") == DESCENDED),
        "held": sum(1 for s in sectors if s.get("descent_status") == HELD),
        "obstructed": sum(
            1 for s in sectors if s.get("descent_status") == DESCENT_OBSTRUCTED
        ),
        "local_only": sum(1 for s in sectors if s.get("descent_status") == LOCAL_ONLY),
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
            "source_temporal_packet_digest": _sha(temporal),
            "source_alignment_packet_digest": _sha(alignment),
            "presentations": public_presentations,
            "conditioning_families": conditioning_families,
            "descent_sectors": sectors,
            "obstruction_witnesses": obstruction_witnesses,
            "summary": {
                "presentation_count": len(public_presentations),
                "conditioning_family_count": len(conditioning_families),
                "descent_sector_count": len(sectors),
                "descended_sector_count": counts["descended"],
                "held_sector_count": counts["held"],
                "obstructed_sector_count": counts["obstructed"],
                "local_only_sector_count": counts["local_only"],
                "obstruction_witness_count": len(obstruction_witnesses),
            },
            "dependent_origination_boundary": {
                "many_presentations_preserved": True,
                "conditioning_relation_is_not_substance": True,
                "descent_requires_local_compatibility": True,
                "obstruction_witnesses_preserved": True,
                "global_collapse_performed": False,
                "single_provider_privileged": False,
                "causal_inference_performed": False,
                "causal_direction_inferred": False,
                "source_authority_transferred": False,
                "runtime_descent_is_formal_theorem_proof": False,
                "formal_v4_49_factorization_theorem_replaced": False,
                "formal_v4_61_higher_coherence_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "presentation_relation": "generated_by_shared_exact_condition_witnesses",
                "quotient_like_classes": "equivalence_closure_of_runtime_condition_relation",
                "semantic_compatibility": "bounded_temporal_compatibility_from_v7_2",
                "descent_obstruction": "related_runtime_presentations_with_incompatible_or_unresolved_local_semantics",
                "lean_theorem_authority": "formal/KUOS only",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-dependent-origination-descent-" + _sha(
        {
            "plan": plan,
            "temporal_digest": _sha(temporal),
            "alignment_digest": _sha(alignment),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "presentation_count": len(public_presentations),
        "conditioning_family_count": len(conditioning_families),
        "descent_sector_count": len(sectors),
        "descended_sector_count": counts["descended"],
        "held_sector_count": counts["held"],
        "obstructed_sector_count": counts["obstructed"],
        "local_only_sector_count": counts["local_only"],
        "obstruction_witness_count": len(obstruction_witnesses),
        "output_written": output_written,
        "output_digest": _sha(output),
        "global_collapse_performed": False,
        "substance_reification_performed": False,
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

    return ObservabilityDependentOriginationDescentResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(public_presentations),
        len(conditioning_families),
        len(sectors),
        counts["descended"],
        counts["held"],
        counts["obstructed"],
        counts["local_only"],
        len(obstruction_witnesses),
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
