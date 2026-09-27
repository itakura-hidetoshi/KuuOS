#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_observability_invariant_carrier_v7_8"
PLAN_VERSION = "kuuos_observability_invariant_carrier_plan_v7_8"
SOURCE_VERSION = "kuuos_runtime_observability_presentation_invariance_v7_7"

READY = "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_READY"
PARTIAL = "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_BLOCKED"

FACTORIZED = "factors_through_invariant_carrier"
FACTOR_HELD = "carrier_factorization_held"
FACTOR_OBSTRUCTED = "carrier_factorization_obstructed"
LOCAL_IMAGE = "local_presentation_canonical_image"

SOURCE_INVARIANT = "presentation_invariant"
SOURCE_HELD = "presentation_invariance_held"
SOURCE_OBSTRUCTED = "presentation_invariance_obstructed"
SOURCE_LOCAL = "local_presentation_only"


@dataclass(frozen=True)
class ObservabilityInvariantCarrierResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    presentation_count: int
    carrier_element_count: int
    canonical_image_count: int
    held_image_count: int
    factorized_sector_count: int
    held_sector_count: int
    obstructed_sector_count: int
    local_image_sector_count: int
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
    if plan.get("canonical_carrier_map_required") is not True:
        blockers.append("canonical_carrier_map_required_not_true")
    if plan.get("carrier_identity_depends_only_on_invariant") is not True:
        blockers.append("carrier_identity_invariant_only_not_true")
    if plan.get("presentation_id_may_affect_carrier_identity") is not False:
        blockers.append("presentation_id_carrier_identity_must_be_false")
    if plan.get("sector_id_may_affect_carrier_identity") is not False:
        blockers.append("sector_id_carrier_identity_must_be_false")
    if plan.get("provider_may_affect_carrier_identity") is not False:
        blockers.append("provider_carrier_identity_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_universality_authority") is not False:
        blockers.append("python_formal_universality_authority_must_be_false")


def _carrier_id(
    projection_id: str,
    schema_digest: str,
    invariant_digest: str,
) -> str:
    return "invariant-carrier-" + _sha(
        {
            "invariant_projection_id": projection_id,
            "invariant_schema_digest": schema_digest,
            "invariant_digest": invariant_digest,
        }
    )[:24]


def _invariant_rows(
    source: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, str, dict[str, dict[str, Any]]]:
    projection_id = str(source.get("invariant_projection_id", "")).strip()
    schema_digest = str(source.get("invariant_schema_digest", "")).strip()
    if not projection_id:
        blockers.append("source_invariant_projection_id_missing")
    if not schema_digest:
        blockers.append("source_invariant_schema_digest_missing")

    raw = source.get("presentation_invariants", [])
    if not isinstance(raw, list):
        blockers.append("source_presentation_invariants_not_list")
        return projection_id, schema_digest, {}

    rows: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"invariant_row_{index}_not_object")
            continue
        presentation_id = str(item.get("presentation_id", "")).strip()
        if not presentation_id:
            blockers.append(f"invariant_row_{index}_presentation_id_missing")
            continue
        if presentation_id in rows:
            blockers.append("duplicate_invariant_presentation_id")
            continue

        state = str(item.get("invariant_state", "")).strip()
        digest = str(item.get("invariant_digest", "")).strip()
        if state == "observed" and not digest:
            blockers.append(f"invariant_row_{index}_observed_digest_missing")
        if state != "observed" and digest:
            blockers.append(f"invariant_row_{index}_nonobserved_digest_present")

        rows[presentation_id] = {
            "presentation_id": presentation_id,
            "invariant_state": state,
            "invariant_digest": digest,
        }
    return projection_id, schema_digest, rows


def _canonical_map(
    rows: Mapping[str, Mapping[str, Any]],
    projection_id: str,
    schema_digest: str,
) -> tuple[list[dict[str, Any]], dict[str, str], dict[str, dict[str, Any]]]:
    mapping: list[dict[str, Any]] = []
    image_by_presentation: dict[str, str] = {}
    carriers: dict[str, dict[str, Any]] = {}

    for presentation_id in sorted(rows):
        row = rows[presentation_id]
        state = str(row.get("invariant_state", ""))
        digest = str(row.get("invariant_digest", ""))

        if state == "observed":
            carrier_element_id = _carrier_id(
                projection_id,
                schema_digest,
                digest,
            )
            image_by_presentation[presentation_id] = carrier_element_id
            carrier = carriers.setdefault(
                carrier_element_id,
                {
                    "carrier_element_id": carrier_element_id,
                    "invariant_digest": digest,
                    "presentation_witness_ids": [],
                    "presentation_witness_count": 0,
                    "carrier_identity_uses_presentation_id": False,
                    "carrier_identity_uses_sector_id": False,
                    "carrier_identity_uses_provider": False,
                    "carrier_element_is_substance": False,
                },
            )
            carrier["presentation_witness_ids"].append(presentation_id)
            carrier["presentation_witness_count"] += 1
            mapping.append(
                {
                    "presentation_id": presentation_id,
                    "invariant_state": state,
                    "carrier_element_id": carrier_element_id,
                    "canonical_image_defined": True,
                }
            )
        else:
            mapping.append(
                {
                    "presentation_id": presentation_id,
                    "invariant_state": state,
                    "carrier_element_id": "",
                    "canonical_image_defined": False,
                }
            )

    for carrier in carriers.values():
        carrier["presentation_witness_ids"] = sorted(
            carrier["presentation_witness_ids"]
        )

    return (
        mapping,
        image_by_presentation,
        carriers,
    )


def _sector_factorizations(
    source: Mapping[str, Any],
    image_by_presentation: Mapping[str, str],
    blockers: list[str],
) -> list[dict[str, Any]]:
    raw = source.get("presentation_invariance_sectors", [])
    if not isinstance(raw, list):
        blockers.append("source_presentation_invariance_sectors_not_list")
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

        members = sorted(
            {
                str(x)
                for x in item.get("presentation_ids", [])
                if str(x)
            }
        )
        source_status = str(
            item.get("presentation_invariance_status", "")
        )
        common_invariant_digest = str(
            item.get("common_invariant_digest", "")
        )
        images = sorted(
            {
                image_by_presentation[presentation_id]
                for presentation_id in members
                if presentation_id in image_by_presentation
            }
        )
        missing = sorted(
            presentation_id
            for presentation_id in members
            if presentation_id not in image_by_presentation
        )

        if source_status == SOURCE_INVARIANT:
            if missing:
                blockers.append(f"sector_{index}_invariant_but_image_missing")
                factorization_status = FACTOR_HELD
                carrier_element_id = ""
            elif len(images) == 1:
                expected = _carrier_id(
                    str(source.get("invariant_projection_id", "")),
                    str(source.get("invariant_schema_digest", "")),
                    common_invariant_digest,
                )
                if images[0] != expected:
                    blockers.append(f"sector_{index}_carrier_identity_mismatch")
                factorization_status = FACTORIZED
                carrier_element_id = images[0]
            else:
                blockers.append(f"sector_{index}_invariant_not_single_carrier")
                factorization_status = FACTOR_OBSTRUCTED
                carrier_element_id = ""
        elif source_status == SOURCE_HELD:
            factorization_status = FACTOR_HELD
            carrier_element_id = images[0] if len(images) == 1 else ""
        elif source_status == SOURCE_OBSTRUCTED:
            factorization_status = FACTOR_OBSTRUCTED
            carrier_element_id = ""
        elif source_status == SOURCE_LOCAL:
            factorization_status = LOCAL_IMAGE
            carrier_element_id = images[0] if len(images) == 1 else ""
        else:
            blockers.append(f"sector_{index}_unknown_source_invariance_status")
            factorization_status = FACTOR_HELD
            carrier_element_id = ""

        result.append(
            {
                "sector_id": sector_id,
                "presentation_ids": members,
                "source_presentation_invariance_status": source_status,
                "carrier_factorization_status": factorization_status,
                "carrier_element_id": carrier_element_id,
                "distinct_observed_carrier_element_ids": images,
                "missing_canonical_image_presentation_ids": missing,
                "presentation_count": len(members),
                "presentation_identity_erased_in_carrier": True,
                "sector_identity_erased_in_carrier": True,
                "formal_universal_factorization_claimed": False,
            }
        )

    return result


def build_observability_invariant_carrier(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityInvariantCarrierResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_invariant_carrier_plan_v7_8.json"
    source_path = root / "observability_presentation_invariance_packet_v7_7.json"
    output_path = root / "observability_invariant_carrier_packet_v7_8.json"
    receipt_path = root / "observability_invariant_carrier_receipt_v7_8.json"
    audit_path = root / "observability_invariant_carrier_audit_v7_8.jsonl"

    if ctx.get("observability_invariant_carrier_enabled") is not True:
        blockers.append("invariant_carrier_enabled_not_true")
    if ctx.get("apply_observability_invariant_carrier") is not True:
        blockers.append("apply_invariant_carrier_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_INVARIANT_CARRIER_AUTHORITY_READY":
        blockers.append("invariant_carrier_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "source_invariance_packet_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)

    if not plan:
        blockers.append("invariant_carrier_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)

    if not source:
        blockers.append("presentation_invariance_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("presentation_invariance_packet_version_invalid")

    if plan and source:
        source_digest = _sha(source)
        if str(plan.get("source_invariance_packet_digest", "")) != source_digest:
            blockers.append("source_invariance_packet_digest_mismatch")

        boundary = _m(source.get("dependent_origination_boundary"))
        if boundary.get("presentation_invariance_required_for_descent") is not True:
            blockers.append("source_presentation_invariance_boundary_missing")
        if boundary.get("invariant_match_erases_presentation_dependence") is not True:
            blockers.append("source_presentation_erasure_boundary_missing")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("source_authority_boundary_invalid")

    projection_id = ""
    schema_digest = ""
    rows: dict[str, dict[str, Any]] = {}
    mapping: list[dict[str, Any]] = []
    image_by_presentation: dict[str, str] = {}
    carriers: dict[str, dict[str, Any]] = {}
    sector_factorizations: list[dict[str, Any]] = []

    if source:
        projection_id, schema_digest, rows = _invariant_rows(
            source,
            blockers,
        )

    if plan and source:
        if (
            str(plan.get("invariant_projection_id", ""))
            != projection_id
        ):
            blockers.append("invariant_projection_id_mismatch")
        if (
            str(plan.get("invariant_schema_digest", ""))
            != schema_digest
        ):
            blockers.append("invariant_schema_digest_mismatch")

    if not blockers:
        mapping, image_by_presentation, carriers = _canonical_map(
            rows,
            projection_id,
            schema_digest,
        )
        sector_factorizations = _sector_factorizations(
            source,
            image_by_presentation,
            blockers,
        )

    counts = {
        "canonical_images": sum(
            1 for record in mapping if record["canonical_image_defined"]
        ),
        "held_images": sum(
            1 for record in mapping if not record["canonical_image_defined"]
        ),
        "factorized": sum(
            1
            for sector in sector_factorizations
            if sector["carrier_factorization_status"] == FACTORIZED
        ),
        "held": sum(
            1
            for sector in sector_factorizations
            if sector["carrier_factorization_status"] == FACTOR_HELD
        ),
        "obstructed": sum(
            1
            for sector in sector_factorizations
            if sector["carrier_factorization_status"] == FACTOR_OBSTRUCTED
        ),
        "local": sum(
            1
            for sector in sector_factorizations
            if sector["carrier_factorization_status"] == LOCAL_IMAGE
        ),
    }

    output: dict[str, Any] = {}
    output_written = False

    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif counts["held"] > 0 or counts["held_images"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_invariance_packet_digest": _sha(source),
            "invariant_projection_id": projection_id,
            "invariant_schema_digest": schema_digest,
            "carrier_elements": [
                carriers[carrier_id]
                for carrier_id in sorted(carriers)
            ],
            "canonical_presentation_map": mapping,
            "sector_factorizations": sector_factorizations,
            "summary": {
                "presentation_count": len(rows),
                "carrier_element_count": len(carriers),
                "canonical_image_count": counts["canonical_images"],
                "held_image_count": counts["held_images"],
                "factorized_sector_count": counts["factorized"],
                "held_sector_count": counts["held"],
                "obstructed_sector_count": counts["obstructed"],
                "local_image_sector_count": counts["local"],
            },
            "dependent_origination_boundary": {
                "same_invariant_same_carrier_element": True,
                "carrier_identity_depends_only_on_invariant": True,
                "presentation_id_affects_carrier_identity": False,
                "sector_id_affects_carrier_identity": False,
                "provider_affects_carrier_identity": False,
                "presentation_local_differences_erased_after_invariance": True,
                "carrier_preserves_invariant_not_presentation": True,
                "carrier_element_is_substance": False,
                "canonical_map_is_runtime_construction_not_formal_universality_proof": True,
                "source_authority_transferred": False,
                "python_formal_universality_authority": False,
                "formal_v2_0_universal_property_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "canonical_runtime_map": "presentation -> carrier element determined only by the common invariant projection value",
                "carrier_uniqueness_rule": "equal invariant digests induce exactly equal runtime carrier element ids",
                "formal_reference": "formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean",
                "formal_gap": "runtime hash-carrier construction does not prove the Mathlib localization universal mapping property or essential uniqueness up to natural isomorphism",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-invariant-carrier-" + _sha(
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
        "presentation_count": len(rows),
        "carrier_element_count": len(carriers),
        "canonical_image_count": counts["canonical_images"],
        "held_image_count": counts["held_images"],
        "factorized_sector_count": counts["factorized"],
        "held_sector_count": counts["held"],
        "obstructed_sector_count": counts["obstructed"],
        "local_image_sector_count": counts["local"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "carrier_identity_depends_only_on_invariant": True,
        "presentation_id_affects_carrier_identity": False,
        "sector_id_affects_carrier_identity": False,
        "provider_affects_carrier_identity": False,
        "source_authority_transferred": False,
        "python_formal_universality_authority": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ObservabilityInvariantCarrierResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(rows),
        len(carriers),
        counts["canonical_images"],
        counts["held_images"],
        counts["factorized"],
        counts["held"],
        counts["obstructed"],
        counts["local"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
