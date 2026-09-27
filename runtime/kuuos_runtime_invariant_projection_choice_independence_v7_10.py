#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_invariant_projection_choice_independence_v7_10"
PLAN_VERSION = "kuuos_invariant_projection_choice_independence_plan_v7_10"
INPUT_VERSION = "kuuos_invariant_projection_family_input_v7_10"

READY = "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_READY"
PARTIAL = "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_PARTIAL"
OBSTRUCTED = "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_OBSTRUCTED"
BLOCKED = "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_BLOCKED"

CHOICE_INVARIANT = "projection_choice_invariant"
CHOICE_HELD = "projection_choice_invariance_held"
CHOICE_OBSTRUCTED = "projection_choice_invariance_obstructed"

ALLOWED_STATES = {"observed", "held", "unavailable"}


@dataclass(frozen=True)
class InvariantProjectionChoiceIndependenceResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    projection_count: int
    semantic_subject_count: int
    choice_invariant_subject_count: int
    held_subject_count: int
    obstructed_subject_count: int
    normalized_carrier_element_count: int
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


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, int]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("projection_choice_independence_required") is not True:
        blockers.append("projection_choice_independence_required_not_true")
    if plan.get("local_invariant_equality_required") is not False:
        blockers.append("local_invariant_equality_required_must_be_false")
    if plan.get("projection_id_may_define_semantic_identity") is not False:
        blockers.append("projection_id_semantic_identity_must_be_false")
    if plan.get("normalized_observable_defines_choice_independent_meaning") is not True:
        blockers.append("normalized_observable_choice_meaning_not_true")
    if plan.get("formal_normalization_equivalence_claim_allowed") is not False:
        blockers.append("formal_normalization_equivalence_claim_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    if plan.get("python_is_formal_theorem_authority") is not False:
        blockers.append("python_formal_theorem_authority_must_be_false")

    max_projections = _i(plan.get("max_projections"), 16)
    if max_projections < 2 or max_projections > 128:
        blockers.append("max_projections_out_of_bounds")

    max_value_bytes = _i(plan.get("max_value_bytes"), 8192)
    if max_value_bytes < 64 or max_value_bytes > 65536:
        blockers.append("max_value_bytes_out_of_bounds")

    return max_projections, max_value_bytes


def _parse_projection_family(
    packet: Mapping[str, Any],
    *,
    max_projections: int,
    max_value_bytes: int,
    blockers: list[str],
) -> tuple[str, str, list[dict[str, Any]], set[str]]:
    normalized_observable_id = str(
        packet.get("normalized_observable_id", "")
    ).strip()
    normalized_schema_digest = str(
        packet.get("normalized_schema_digest", "")
    ).strip()

    if not normalized_observable_id:
        blockers.append("normalized_observable_id_missing")
    if not normalized_schema_digest:
        blockers.append("normalized_schema_digest_missing")

    raw = packet.get("projections", [])
    if not isinstance(raw, list):
        blockers.append("projections_not_list")
        return normalized_observable_id, normalized_schema_digest, [], set()

    if len(raw) < 2:
        blockers.append("at_least_two_projections_required")
    if len(raw) > max_projections:
        blockers.append("projection_count_exceeds_plan_bound")

    projections: list[dict[str, Any]] = []
    seen_projection_ids: set[str] = set()
    subject_union: set[str] = set()

    for p_index, projection in enumerate(raw):
        if not isinstance(projection, Mapping):
            blockers.append(f"projection_{p_index}_not_object")
            continue

        projection_id = str(projection.get("projection_id", "")).strip()
        schema_digest = str(projection.get("projection_schema_digest", "")).strip()
        certificate_digest = str(
            projection.get("comparison_certificate_digest", "")
        ).strip()

        if not projection_id:
            blockers.append(f"projection_{p_index}_id_missing")
            continue
        if projection_id in seen_projection_ids:
            blockers.append("duplicate_projection_id")
            continue
        seen_projection_ids.add(projection_id)

        if not schema_digest:
            blockers.append(f"projection_{p_index}_schema_digest_missing")
        if not certificate_digest:
            blockers.append(f"projection_{p_index}_comparison_certificate_digest_missing")

        raw_subjects = projection.get("subjects", [])
        if not isinstance(raw_subjects, list):
            blockers.append(f"projection_{p_index}_subjects_not_list")
            raw_subjects = []

        subjects: dict[str, dict[str, Any]] = {}
        for s_index, subject in enumerate(raw_subjects):
            if not isinstance(subject, Mapping):
                blockers.append(f"projection_{p_index}_subject_{s_index}_not_object")
                continue

            subject_id = str(subject.get("semantic_subject_id", "")).strip()
            if not subject_id:
                blockers.append(
                    f"projection_{p_index}_subject_{s_index}_id_missing"
                )
                continue
            if subject_id in subjects:
                blockers.append(
                    f"projection_{p_index}_duplicate_semantic_subject_id"
                )
                continue

            state = str(subject.get("invariant_state", "")).strip()
            if state not in ALLOWED_STATES:
                blockers.append(
                    f"projection_{p_index}_subject_{s_index}_state_invalid"
                )

            local_present = "local_invariant_value" in subject
            normalized_present = "normalized_observable_value" in subject
            local_value = subject.get("local_invariant_value")
            normalized_value = subject.get("normalized_observable_value")

            if state == "observed":
                if not local_present:
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_local_value_missing"
                    )
                if not normalized_present:
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_normalized_value_missing"
                    )
                if local_present and _serialized_size(local_value) > max_value_bytes:
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_local_value_too_large"
                    )
                if (
                    normalized_present
                    and _serialized_size(normalized_value) > max_value_bytes
                ):
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_normalized_value_too_large"
                    )
            else:
                if local_present and local_value is not None:
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_nonobserved_local_value_must_be_null"
                    )
                if normalized_present and normalized_value is not None:
                    blockers.append(
                        f"projection_{p_index}_subject_{s_index}_nonobserved_normalized_value_must_be_null"
                    )

            local_digest = (
                _sha(
                    {
                        "projection_id": projection_id,
                        "projection_schema_digest": schema_digest,
                        "local_invariant_value": local_value,
                    }
                )
                if state == "observed" and local_present
                else ""
            )
            normalized_digest = (
                _sha(
                    {
                        "normalized_observable_id": normalized_observable_id,
                        "normalized_schema_digest": normalized_schema_digest,
                        "normalized_observable_value": normalized_value,
                    }
                )
                if state == "observed" and normalized_present
                else ""
            )

            subjects[subject_id] = {
                "semantic_subject_id": subject_id,
                "invariant_state": state,
                "local_invariant_digest": local_digest,
                "normalized_observable_digest": normalized_digest,
            }
            subject_union.add(subject_id)

        projections.append(
            {
                "projection_id": projection_id,
                "projection_schema_digest": schema_digest,
                "comparison_certificate_digest": certificate_digest,
                "subjects": subjects,
            }
        )

    return (
        normalized_observable_id,
        normalized_schema_digest,
        projections,
        subject_union,
    )


def _normalized_carrier_id(
    normalized_observable_id: str,
    normalized_schema_digest: str,
    normalized_digest: str,
) -> str:
    return "choice-independent-invariant-" + _sha(
        {
            "normalized_observable_id": normalized_observable_id,
            "normalized_schema_digest": normalized_schema_digest,
            "normalized_observable_digest": normalized_digest,
        }
    )[:24]


def _diagnose_subject(
    subject_id: str,
    projections: list[dict[str, Any]],
    *,
    normalized_observable_id: str,
    normalized_schema_digest: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    presentations: list[dict[str, Any]] = []
    observed_normalized: dict[str, list[str]] = {}

    for projection in projections:
        row = projection["subjects"].get(subject_id)
        if row is None:
            presentations.append(
                {
                    "projection_id": projection["projection_id"],
                    "projection_schema_digest": projection[
                        "projection_schema_digest"
                    ],
                    "comparison_certificate_digest": projection[
                        "comparison_certificate_digest"
                    ],
                    "invariant_state": "missing",
                    "local_invariant_digest": "",
                    "normalized_observable_digest": "",
                }
            )
            continue

        presentation = {
            "projection_id": projection["projection_id"],
            "projection_schema_digest": projection["projection_schema_digest"],
            "comparison_certificate_digest": projection[
                "comparison_certificate_digest"
            ],
            "invariant_state": row["invariant_state"],
            "local_invariant_digest": row["local_invariant_digest"],
            "normalized_observable_digest": row[
                "normalized_observable_digest"
            ],
        }
        presentations.append(presentation)

        if row["invariant_state"] == "observed":
            observed_normalized.setdefault(
                row["normalized_observable_digest"],
                [],
            ).append(projection["projection_id"])

    missing_or_held = any(
        p["invariant_state"] != "observed" for p in presentations
    )
    obstruction_witnesses: list[dict[str, Any]] = []

    if len(observed_normalized) > 1:
        status = CHOICE_OBSTRUCTED
        normalized_digest = ""
        carrier_id = ""
        digests = sorted(observed_normalized)
        for left_index in range(len(digests)):
            for right_index in range(left_index + 1, len(digests)):
                obstruction_witnesses.append(
                    {
                        "obstruction_kind": "projection_choices_disagree_after_common_normalization",
                        "left_normalized_digest": digests[left_index],
                        "right_normalized_digest": digests[right_index],
                        "left_projection_ids": sorted(
                            observed_normalized[digests[left_index]]
                        ),
                        "right_projection_ids": sorted(
                            observed_normalized[digests[right_index]]
                        ),
                    }
                )
    elif missing_or_held:
        status = CHOICE_HELD
        normalized_digest = (
            next(iter(observed_normalized))
            if len(observed_normalized) == 1
            else ""
        )
        carrier_id = (
            _normalized_carrier_id(
                normalized_observable_id,
                normalized_schema_digest,
                normalized_digest,
            )
            if normalized_digest
            else ""
        )
    elif len(observed_normalized) == 1:
        status = CHOICE_INVARIANT
        normalized_digest = next(iter(observed_normalized))
        carrier_id = _normalized_carrier_id(
            normalized_observable_id,
            normalized_schema_digest,
            normalized_digest,
        )
    else:
        status = CHOICE_HELD
        normalized_digest = ""
        carrier_id = ""

    local_digests = sorted(
        {
            p["local_invariant_digest"]
            for p in presentations
            if p["local_invariant_digest"]
        }
    )

    return (
        {
            "semantic_subject_id": subject_id,
            "projection_choice_status": status,
            "projection_presentations": presentations,
            "projection_count": len(presentations),
            "distinct_local_invariant_digest_count": len(local_digests),
            "local_invariants_may_differ": True,
            "normalized_observable_digest": normalized_digest,
            "choice_independent_carrier_element_id": carrier_id,
            "projection_id_defines_semantic_identity": False,
            "local_invariant_equality_required": False,
            "normalized_observable_defines_choice_independent_meaning": True,
        },
        obstruction_witnesses,
    )


def build_invariant_projection_choice_independence(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> InvariantProjectionChoiceIndependenceResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "invariant_projection_choice_independence_plan_v7_10.json"
    input_path = root / "invariant_projection_family_input_v7_10.json"
    output_path = root / "invariant_projection_choice_independence_packet_v7_10.json"
    receipt_path = root / "invariant_projection_choice_independence_receipt_v7_10.json"
    audit_path = root / "invariant_projection_choice_independence_audit_v7_10.jsonl"

    if ctx.get("invariant_projection_choice_independence_enabled") is not True:
        blockers.append("projection_choice_independence_enabled_not_true")
    if ctx.get("apply_invariant_projection_choice_independence") is not True:
        blockers.append("apply_projection_choice_independence_not_true")
    if authority.get("authority_status") != "KUUOS_INVARIANT_PROJECTION_CHOICE_INDEPENDENCE_AUTHORITY_READY":
        blockers.append("projection_choice_independence_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "projection_family_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    packet = _read_json(input_path)

    max_projections = 16
    max_value_bytes = 8192
    if not plan:
        blockers.append("projection_choice_plan_missing_or_invalid")
    else:
        max_projections, max_value_bytes = _validate_plan(plan, blockers)

    if not packet:
        blockers.append("projection_family_input_missing_or_invalid")
    elif packet.get("version") != INPUT_VERSION:
        blockers.append("projection_family_input_version_invalid")

    normalized_observable_id = ""
    normalized_schema_digest = ""
    projections: list[dict[str, Any]] = []
    subject_union: set[str] = set()

    if packet:
        (
            normalized_observable_id,
            normalized_schema_digest,
            projections,
            subject_union,
        ) = _parse_projection_family(
            packet,
            max_projections=max_projections,
            max_value_bytes=max_value_bytes,
            blockers=blockers,
        )

    if plan and packet:
        if (
            str(plan.get("normalized_observable_id", ""))
            != normalized_observable_id
        ):
            blockers.append("normalized_observable_id_mismatch")
        if (
            str(plan.get("normalized_schema_digest", ""))
            != normalized_schema_digest
        ):
            blockers.append("normalized_schema_digest_mismatch")

    subjects: list[dict[str, Any]] = []
    obstruction_witnesses: list[dict[str, Any]] = []

    if not blockers:
        for subject_id in sorted(subject_union):
            diagnosed, obstructions = _diagnose_subject(
                subject_id,
                projections,
                normalized_observable_id=normalized_observable_id,
                normalized_schema_digest=normalized_schema_digest,
            )
            subjects.append(diagnosed)
            obstruction_witnesses.extend(obstructions)

    counts = {
        "invariant": sum(
            1
            for subject in subjects
            if subject["projection_choice_status"] == CHOICE_INVARIANT
        ),
        "held": sum(
            1
            for subject in subjects
            if subject["projection_choice_status"] == CHOICE_HELD
        ),
        "obstructed": sum(
            1
            for subject in subjects
            if subject["projection_choice_status"] == CHOICE_OBSTRUCTED
        ),
    }

    carrier_ids = sorted(
        {
            subject["choice_independent_carrier_element_id"]
            for subject in subjects
            if subject["choice_independent_carrier_element_id"]
        }
    )

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
            "normalized_observable_id": normalized_observable_id,
            "normalized_schema_digest": normalized_schema_digest,
            "projection_presentations": [
                {
                    "projection_id": projection["projection_id"],
                    "projection_schema_digest": projection[
                        "projection_schema_digest"
                    ],
                    "comparison_certificate_digest": projection[
                        "comparison_certificate_digest"
                    ],
                    "projection_is_substance": False,
                }
                for projection in projections
            ],
            "semantic_subjects": subjects,
            "choice_independent_carrier_element_ids": carrier_ids,
            "obstruction_witnesses": obstruction_witnesses,
            "summary": {
                "projection_count": len(projections),
                "semantic_subject_count": len(subjects),
                "choice_invariant_subject_count": counts["invariant"],
                "held_subject_count": counts["held"],
                "obstructed_subject_count": counts["obstructed"],
                "normalized_carrier_element_count": len(carrier_ids),
                "obstruction_witness_count": len(obstruction_witnesses),
            },
            "dependent_origination_boundary": {
                "projection_choice_is_presentation": True,
                "projection_id_defines_semantic_identity": False,
                "local_invariant_equality_required": False,
                "different_local_invariants_may_share_normalized_meaning": True,
                "normalized_observable_defines_choice_independent_meaning": True,
                "choice_independent_carrier_identity_ignores_projection_id": True,
                "normalization_choice_is_substance": False,
                "normalized_observable_is_ultimate_truth": False,
                "formal_normalization_equivalence_claimed": False,
                "source_authority_transferred": False,
                "python_formal_theorem_authority": False,
                "formal_v1_28_normalization_choice_theorem_replaced": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "runtime_projection_choice": "alternative invariant presentations",
                "runtime_comparison_certificate": "opaque provenance digest for the comparison that maps a local invariant into the common normalized observable",
                "runtime_choice_independence": "all observed projection presentations of one semantic subject have one common normalized observable digest",
                "formal_reference": "formal/KUOS/DependentOriginationNormalizationChoiceInvariantV1_28.lean",
                "formal_gap": "does not construct Mathlib strong transformations, intrinsic adjoint equivalences, naturality isomorphisms, or prove coherent observable invariance",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-invariant-projection-choice-independence-" + _sha(
        {
            "plan": plan,
            "input_digest": _sha(packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "projection_count": len(projections),
        "semantic_subject_count": len(subjects),
        "choice_invariant_subject_count": counts["invariant"],
        "held_subject_count": counts["held"],
        "obstructed_subject_count": counts["obstructed"],
        "normalized_carrier_element_count": len(carrier_ids),
        "output_written": output_written,
        "output_digest": _sha(output),
        "projection_id_defines_semantic_identity": False,
        "local_invariant_equality_required": False,
        "normalized_observable_defines_choice_independent_meaning": True,
        "raw_local_invariant_values_persisted": False,
        "raw_normalized_observable_values_persisted": False,
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

    return InvariantProjectionChoiceIndependenceResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(projections),
        len(subjects),
        counts["invariant"],
        counts["held"],
        counts["obstructed"],
        len(carrier_ids),
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
