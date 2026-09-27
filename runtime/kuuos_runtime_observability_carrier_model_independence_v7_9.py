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

VERSION = "kuuos_runtime_observability_carrier_model_independence_v7_9"
PLAN_VERSION = "kuuos_observability_carrier_model_independence_plan_v7_9"
MODELS_VERSION = "kuuos_observability_carrier_models_input_v7_9"
SOURCE_VERSION = "kuuos_runtime_observability_invariant_carrier_v7_8"

READY = "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_READY"
PARTIAL = "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_PARTIAL"
OBSTRUCTED = "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_OBSTRUCTED"
BLOCKED = "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_BLOCKED"

MODEL_COMPLETE = "complete_faithful_carrier_model"
MODEL_PARTIAL = "partial_carrier_model"
MODEL_OBSTRUCTED = "carrier_model_obstructed"

PAIR_EQUIVALENT = "same_invariant_carrier_meaning"
PAIR_HELD = "carrier_model_equivalence_held"
PAIR_OBSTRUCTED = "carrier_model_equivalence_obstructed"


@dataclass(frozen=True)
class ObservabilityCarrierModelIndependenceResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    carrier_element_count: int
    model_count: int
    complete_model_count: int
    partial_model_count: int
    obstructed_model_count: int
    model_pair_count: int
    equivalent_model_pair_count: int
    held_model_pair_count: int
    obstructed_model_pair_count: int
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


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> int:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("carrier_model_independence_required") is not True:
        blockers.append("carrier_model_independence_required_not_true")
    if plan.get("model_token_equality_required") is not False:
        blockers.append("model_token_equality_required_must_be_false")
    if plan.get("presentation_data_may_affect_model_equivalence") is not False:
        blockers.append("presentation_data_model_equivalence_must_be_false")
    if plan.get("formal_category_equivalence_claim_allowed") is not False:
        blockers.append("formal_category_equivalence_claim_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_universality_authority") is not False:
        blockers.append("python_formal_universality_authority_must_be_false")

    max_token_bytes = int(plan.get("max_model_token_bytes", 8192))
    if max_token_bytes < 64 or max_token_bytes > 65536:
        blockers.append("max_model_token_bytes_out_of_bounds")
    return max_token_bytes


def _canonical_carriers(
    source: Mapping[str, Any],
    blockers: list[str],
) -> tuple[str, str, dict[str, str]]:
    projection_id = str(source.get("invariant_projection_id", "")).strip()
    schema_digest = str(source.get("invariant_schema_digest", "")).strip()
    if not projection_id:
        blockers.append("source_invariant_projection_id_missing")
    if not schema_digest:
        blockers.append("source_invariant_schema_digest_missing")

    raw = source.get("carrier_elements", [])
    if not isinstance(raw, list):
        blockers.append("source_carrier_elements_not_list")
        return projection_id, schema_digest, {}

    carriers: dict[str, str] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"carrier_{index}_not_object")
            continue
        carrier_id = str(item.get("carrier_element_id", "")).strip()
        invariant_digest = str(item.get("invariant_digest", "")).strip()
        if not carrier_id:
            blockers.append(f"carrier_{index}_id_missing")
            continue
        if not invariant_digest:
            blockers.append(f"carrier_{index}_invariant_digest_missing")
            continue
        if carrier_id in carriers:
            blockers.append("duplicate_source_carrier_element_id")
            continue
        carriers[carrier_id] = invariant_digest

    return projection_id, schema_digest, carriers


def _semantic_carrier_signature(
    projection_id: str,
    schema_digest: str,
    carriers: Mapping[str, str],
) -> str:
    return _sha(
        {
            "invariant_projection_id": projection_id,
            "invariant_schema_digest": schema_digest,
            "carrier_semantics": sorted(
                {
                    "carrier_element_id": carrier_id,
                    "invariant_digest": invariant_digest,
                }
                for carrier_id, invariant_digest in carriers.items()
            ),
        }
    )


def _model_records(
    models_packet: Mapping[str, Any],
    canonical_carriers: Mapping[str, str],
    *,
    max_token_bytes: int,
    blockers: list[str],
) -> list[dict[str, Any]]:
    raw_models = models_packet.get("models", [])
    if not isinstance(raw_models, list):
        blockers.append("models_not_list")
        return []
    if len(raw_models) < 2:
        blockers.append("at_least_two_carrier_models_required")

    result: list[dict[str, Any]] = []
    seen_model_ids: set[str] = set()
    canonical_ids = set(canonical_carriers)

    for model_index, model in enumerate(raw_models):
        if not isinstance(model, Mapping):
            blockers.append(f"model_{model_index}_not_object")
            continue
        model_id = str(model.get("model_id", "")).strip()
        if not model_id:
            blockers.append(f"model_{model_index}_id_missing")
            continue
        if model_id in seen_model_ids:
            blockers.append("duplicate_model_id")
            continue
        seen_model_ids.add(model_id)

        raw_elements = model.get("elements", [])
        if not isinstance(raw_elements, list):
            blockers.append(f"model_{model_index}_elements_not_list")
            continue

        by_carrier: dict[str, str] = {}
        token_to_carriers: dict[str, list[str]] = {}
        duplicate_carrier_ids: set[str] = set()
        unknown_carrier_ids: set[str] = set()

        for element_index, element in enumerate(raw_elements):
            if not isinstance(element, Mapping):
                blockers.append(
                    f"model_{model_index}_element_{element_index}_not_object"
                )
                continue
            carrier_id = str(element.get("carrier_element_id", "")).strip()
            if not carrier_id:
                blockers.append(
                    f"model_{model_index}_element_{element_index}_carrier_id_missing"
                )
                continue
            if carrier_id not in canonical_ids:
                unknown_carrier_ids.add(carrier_id)

            if "model_element_value" not in element:
                blockers.append(
                    f"model_{model_index}_element_{element_index}_value_missing"
                )
                continue
            model_value = element.get("model_element_value")
            if _serialized_size(model_value) > max_token_bytes:
                blockers.append(
                    f"model_{model_index}_element_{element_index}_value_too_large"
                )
                continue

            token_digest = _sha(
                {
                    "model_element_value": model_value,
                }
            )
            if carrier_id in by_carrier:
                duplicate_carrier_ids.add(carrier_id)
            else:
                by_carrier[carrier_id] = token_digest
            token_to_carriers.setdefault(token_digest, []).append(carrier_id)

        collision_witnesses: list[dict[str, Any]] = []
        for token_digest, carrier_ids in sorted(token_to_carriers.items()):
            distinct = sorted(set(carrier_ids))
            if len(distinct) > 1:
                collision_witnesses.append(
                    {
                        "obstruction_kind": "model_collapses_distinct_invariants",
                        "model_token_digest": token_digest,
                        "carrier_element_ids": distinct,
                    }
                )

        missing = sorted(canonical_ids.difference(by_carrier))
        extras = sorted(unknown_carrier_ids)
        duplicate = sorted(duplicate_carrier_ids)

        if collision_witnesses or duplicate or extras:
            model_status = MODEL_OBSTRUCTED
        elif missing:
            model_status = MODEL_PARTIAL
        else:
            model_status = MODEL_COMPLETE

        result.append(
            {
                "model_id": model_id,
                "model_status": model_status,
                "canonical_carrier_count": len(canonical_ids),
                "represented_carrier_count": len(
                    canonical_ids.intersection(by_carrier)
                ),
                "missing_carrier_element_ids": missing,
                "unknown_carrier_element_ids": extras,
                "duplicate_carrier_element_ids": duplicate,
                "collision_witnesses": collision_witnesses,
                "collision_witness_count": len(collision_witnesses),
                "carrier_to_model_token_digest": {
                    carrier_id: by_carrier[carrier_id]
                    for carrier_id in sorted(by_carrier)
                    if carrier_id in canonical_ids
                },
                "raw_model_values_persisted": False,
                "model_tokens_define_semantic_identity": False,
            }
        )

    return result


def _pair_records(
    models: list[dict[str, Any]],
    semantic_signature: str,
    canonical_carriers: Mapping[str, str],
) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []

    for left, right in itertools.combinations(
        sorted(models, key=lambda model: model["model_id"]),
        2,
    ):
        left_status = left["model_status"]
        right_status = right["model_status"]

        correspondences: list[dict[str, Any]] = []
        if left_status == MODEL_COMPLETE and right_status == MODEL_COMPLETE:
            for carrier_id in sorted(canonical_carriers):
                correspondences.append(
                    {
                        "carrier_element_id": carrier_id,
                        "invariant_digest": canonical_carriers[carrier_id],
                        "left_model_token_digest": left[
                            "carrier_to_model_token_digest"
                        ][carrier_id],
                        "right_model_token_digest": right[
                            "carrier_to_model_token_digest"
                        ][carrier_id],
                        "same_semantic_carrier_element": True,
                        "model_token_equality_required": False,
                    }
                )
            pair_status = PAIR_EQUIVALENT
        elif (
            left_status == MODEL_OBSTRUCTED
            or right_status == MODEL_OBSTRUCTED
        ):
            pair_status = PAIR_OBSTRUCTED
        else:
            pair_status = PAIR_HELD

        pairs.append(
            {
                "left_model_id": left["model_id"],
                "right_model_id": right["model_id"],
                "pair_status": pair_status,
                "semantic_carrier_signature": semantic_signature,
                "carrier_correspondences": correspondences,
                "carrier_correspondence_count": len(correspondences),
                "same_invariant_meaning": pair_status == PAIR_EQUIVALENT,
                "model_token_equality_required": False,
                "presentation_data_used_for_equivalence": False,
                "finite_runtime_bijection_witness": (
                    pair_status == PAIR_EQUIVALENT
                ),
                "formal_category_equivalence_claimed": False,
            }
        )

    return pairs


def build_observability_carrier_model_independence(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityCarrierModelIndependenceResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_carrier_model_independence_plan_v7_9.json"
    source_path = root / "observability_invariant_carrier_packet_v7_8.json"
    models_path = root / "observability_carrier_models_input_v7_9.json"
    output_path = root / "observability_carrier_model_independence_packet_v7_9.json"
    receipt_path = root / "observability_carrier_model_independence_receipt_v7_9.json"
    audit_path = root / "observability_carrier_model_independence_audit_v7_9.jsonl"

    if ctx.get("observability_carrier_model_independence_enabled") is not True:
        blockers.append("carrier_model_independence_enabled_not_true")
    if ctx.get("apply_observability_carrier_model_independence") is not True:
        blockers.append("apply_carrier_model_independence_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_CARRIER_MODEL_INDEPENDENCE_AUTHORITY_READY":
        blockers.append("carrier_model_independence_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "source_carrier_packet_read_allowed",
        "models_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    models_packet = _read_json(models_path)

    max_token_bytes = 8192
    if not plan:
        blockers.append("carrier_model_independence_plan_missing_or_invalid")
    else:
        max_token_bytes = _validate_plan(plan, blockers)

    if not source:
        blockers.append("invariant_carrier_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("invariant_carrier_packet_version_invalid")

    if not models_packet:
        blockers.append("carrier_models_input_missing_or_invalid")
    elif models_packet.get("version") != MODELS_VERSION:
        blockers.append("carrier_models_input_version_invalid")

    projection_id = ""
    schema_digest = ""
    canonical_carriers: dict[str, str] = {}

    if source:
        projection_id, schema_digest, canonical_carriers = _canonical_carriers(
            source,
            blockers,
        )

    if plan and source and models_packet:
        source_digest = _sha(source)
        if str(plan.get("source_carrier_packet_digest", "")) != source_digest:
            blockers.append("source_carrier_packet_digest_mismatch")
        if (
            str(models_packet.get("source_carrier_packet_digest", ""))
            != source_digest
        ):
            blockers.append("models_source_carrier_packet_digest_mismatch")
        if str(plan.get("invariant_projection_id", "")) != projection_id:
            blockers.append("invariant_projection_id_mismatch")
        if str(plan.get("invariant_schema_digest", "")) != schema_digest:
            blockers.append("invariant_schema_digest_mismatch")

        boundary = _m(source.get("dependent_origination_boundary"))
        if boundary.get("same_invariant_same_carrier_element") is not True:
            blockers.append("source_same_invariant_carrier_boundary_missing")
        if boundary.get("carrier_identity_depends_only_on_invariant") is not True:
            blockers.append("source_invariant_only_carrier_boundary_missing")
        if boundary.get("source_authority_transferred") is not False:
            blockers.append("source_authority_boundary_invalid")

    semantic_signature = _semantic_carrier_signature(
        projection_id,
        schema_digest,
        canonical_carriers,
    )

    models: list[dict[str, Any]] = []
    model_pairs: list[dict[str, Any]] = []

    if not blockers:
        models = _model_records(
            models_packet,
            canonical_carriers,
            max_token_bytes=max_token_bytes,
            blockers=blockers,
        )

    if not blockers:
        model_pairs = _pair_records(
            models,
            semantic_signature,
            canonical_carriers,
        )

    counts = {
        "complete": sum(
            1 for model in models if model["model_status"] == MODEL_COMPLETE
        ),
        "partial": sum(
            1 for model in models if model["model_status"] == MODEL_PARTIAL
        ),
        "obstructed": sum(
            1 for model in models if model["model_status"] == MODEL_OBSTRUCTED
        ),
        "equivalent_pairs": sum(
            1 for pair in model_pairs if pair["pair_status"] == PAIR_EQUIVALENT
        ),
        "held_pairs": sum(
            1 for pair in model_pairs if pair["pair_status"] == PAIR_HELD
        ),
        "obstructed_pairs": sum(
            1 for pair in model_pairs if pair["pair_status"] == PAIR_OBSTRUCTED
        ),
    }

    output: dict[str, Any] = {}
    output_written = False

    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif counts["partial"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_carrier_packet_digest": _sha(source),
            "invariant_projection_id": projection_id,
            "invariant_schema_digest": schema_digest,
            "semantic_carrier_signature": semantic_signature,
            "canonical_carrier_elements": [
                {
                    "carrier_element_id": carrier_id,
                    "invariant_digest": canonical_carriers[carrier_id],
                }
                for carrier_id in sorted(canonical_carriers)
            ],
            "carrier_models": models,
            "carrier_model_pairs": model_pairs,
            "summary": {
                "carrier_element_count": len(canonical_carriers),
                "model_count": len(models),
                "complete_model_count": counts["complete"],
                "partial_model_count": counts["partial"],
                "obstructed_model_count": counts["obstructed"],
                "model_pair_count": len(model_pairs),
                "equivalent_model_pair_count": counts["equivalent_pairs"],
                "held_model_pair_count": counts["held_pairs"],
                "obstructed_model_pair_count": counts["obstructed_pairs"],
            },
            "dependent_origination_boundary": {
                "presentation_independent_carrier_precedes_model_comparison": True,
                "same_invariant_meaning_independent_of_carrier_model_tokens": True,
                "model_token_equality_required": False,
                "model_id_defines_semantic_identity": False,
                "presentation_data_used_for_model_equivalence": False,
                "semantic_carrier_signature_depends_only_on_invariant_carrier": True,
                "alternative_complete_models_are_runtime_bijective_via_canonical_carrier": True,
                "carrier_model_is_substance": False,
                "formal_category_equivalence_claimed": False,
                "source_authority_transferred": False,
                "python_formal_universality_authority": False,
                "formal_v2_0_universal_carrier_equivalence_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "runtime_equivalence": "finite bijection between complete faithful encodings mediated by canonical invariant carrier elements",
                "formal_reference": "formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean",
                "formal_gap": "does not prove equivalence of categories, localization universality, triangle natural isomorphisms, or essential uniqueness in Mathlib",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-carrier-model-independence-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "models_digest": _sha(models_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "carrier_element_count": len(canonical_carriers),
        "model_count": len(models),
        "complete_model_count": counts["complete"],
        "partial_model_count": counts["partial"],
        "obstructed_model_count": counts["obstructed"],
        "model_pair_count": len(model_pairs),
        "equivalent_model_pair_count": counts["equivalent_pairs"],
        "held_model_pair_count": counts["held_pairs"],
        "obstructed_model_pair_count": counts["obstructed_pairs"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "model_token_equality_required": False,
        "presentation_data_used_for_model_equivalence": False,
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

    return ObservabilityCarrierModelIndependenceResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(canonical_carriers),
        len(models),
        counts["complete"],
        counts["partial"],
        counts["obstructed"],
        len(model_pairs),
        counts["equivalent_pairs"],
        counts["held_pairs"],
        counts["obstructed_pairs"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
