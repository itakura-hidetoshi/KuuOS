#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_observability_event_alignment_v7_3"
PLAN_VERSION = "kuuos_observability_event_alignment_plan_v7_3"
INPUT_VERSION = "kuuos_observability_event_alignment_input_v7_3"
TEMPORAL_VERSION = "kuuos_runtime_observability_temporal_correlation_v7_2"
READY = "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_READY"
PARTIAL = "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_PARTIAL"
BLOCKED = "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_BLOCKED"

ALLOWED_IDENTIFIER_TYPES = frozenset(
    {
        "commit_sha",
        "workflow_run_id",
        "workflow_job_id",
        "deployment_id",
        "request_id",
        "trace_id",
        "correlation_id",
        "artifact_digest",
    }
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
NUMERIC_ID = re.compile(r"^[1-9][0-9]*$")


@dataclass(frozen=True)
class ObservabilityEventAlignmentResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    observation_count: int
    pair_count: int
    exact_context_compatible_count: int
    exact_context_disjoint_count: int
    exact_context_time_unresolved_count: int
    temporal_only_count: int
    no_alignment_evidence_count: int
    source_obstruction_count: int
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
    if plan.get("causal_inference_allowed") is not False:
        blockers.append("causal_inference_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    max_bindings = _i(plan.get("max_identity_bindings"), 128)
    if max_bindings < 2 or max_bindings > 256:
        blockers.append("max_identity_bindings_out_of_bounds")
    return max_bindings


def _canonical_identifier(
    identifier_type: str,
    value: Any,
    blockers: list[str],
    binding_index: int,
) -> str:
    text = str(value).strip()
    prefix = f"binding_{binding_index}_{identifier_type}"
    if not text:
        blockers.append(f"{prefix}_empty")
        return ""
    if len(text) > 512:
        blockers.append(f"{prefix}_too_long")
        return ""
    if identifier_type == "commit_sha":
        lowered = text.lower()
        if SHA40.fullmatch(lowered) is None:
            blockers.append(f"{prefix}_invalid")
            return ""
        return lowered
    if identifier_type == "artifact_digest":
        lowered = text.lower()
        if SHA256.fullmatch(lowered) is None:
            blockers.append(f"{prefix}_invalid")
            return ""
        return lowered
    if identifier_type in {"workflow_run_id", "workflow_job_id"}:
        if NUMERIC_ID.fullmatch(text) is None:
            blockers.append(f"{prefix}_invalid")
            return ""
        return text
    return text


def _binding_map(
    alignment_input: Mapping[str, Any],
    observation_ids: set[str],
    max_bindings: int,
    blockers: list[str],
) -> dict[str, dict[str, str]]:
    raw = alignment_input.get("identity_bindings", [])
    if not isinstance(raw, list):
        blockers.append("identity_bindings_not_list")
        return {}
    if len(raw) > max_bindings:
        blockers.append("identity_binding_count_exceeds_plan_bound")
    result: dict[str, dict[str, str]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"binding_{index}_not_object")
            continue
        observation_id = str(item.get("observation_id", "")).strip()
        if not observation_id:
            blockers.append(f"binding_{index}_observation_id_missing")
            continue
        if observation_id not in observation_ids:
            blockers.append(f"binding_{index}_observation_id_unknown")
        if observation_id in result:
            blockers.append("duplicate_identity_binding_observation_id")
        identifiers = item.get("identifiers", {})
        if not isinstance(identifiers, Mapping):
            blockers.append(f"binding_{index}_identifiers_not_object")
            continue
        canonical: dict[str, str] = {}
        for key, value in identifiers.items():
            identifier_type = str(key)
            if identifier_type not in ALLOWED_IDENTIFIER_TYPES:
                blockers.append(f"binding_{index}_identifier_type_not_allowlisted:{identifier_type}")
                continue
            canonical_value = _canonical_identifier(
                identifier_type,
                value,
                blockers,
                index,
            )
            if canonical_value:
                canonical[identifier_type] = canonical_value
        result[observation_id] = canonical
    return result


def _shared_identifier_evidence(
    left: Mapping[str, str],
    right: Mapping[str, str],
) -> tuple[list[dict[str, str]], list[str]]:
    shared: list[dict[str, str]] = []
    distinct_types: list[str] = []
    for identifier_type in sorted(set(left).intersection(right)):
        if left[identifier_type] == right[identifier_type]:
            shared.append(
                {
                    "identifier_type": identifier_type,
                    "value_digest": _sha(
                        {
                            "identifier_type": identifier_type,
                            "value": left[identifier_type],
                        }
                    ),
                }
            )
        else:
            distinct_types.append(identifier_type)
    return shared, distinct_types


def _alignment_state(
    temporal_relation: str,
    temporally_compatible: bool,
    has_shared_exact_identifier: bool,
) -> str:
    if temporal_relation == "source_obstruction":
        return "source_obstruction"
    if has_shared_exact_identifier:
        if temporal_relation == "disjoint":
            return "exact_context_temporally_disjoint"
        if temporal_relation == "insufficient_time_metadata":
            return "exact_context_time_unresolved"
        if temporally_compatible:
            return "exact_context_temporally_compatible"
        return "exact_context_time_unresolved"
    if temporally_compatible:
        return "temporal_only"
    return "no_alignment_evidence"


def build_observability_event_alignment(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityEventAlignmentResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_event_alignment_plan_v7_3.json"
    input_path = root / "observability_event_alignment_input_v7_3.json"
    temporal_path = root / "observability_temporal_correlation_packet_v7_2.json"
    output_path = root / "observability_event_alignment_packet_v7_3.json"
    receipt_path = root / "observability_event_alignment_receipt_v7_3.json"
    audit_path = root / "observability_event_alignment_audit_v7_3.jsonl"

    if ctx.get("observability_event_alignment_enabled") is not True:
        blockers.append("observability_event_alignment_enabled_not_true")
    if ctx.get("apply_observability_event_alignment") is not True:
        blockers.append("apply_observability_event_alignment_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_EVENT_ALIGNMENT_AUTHORITY_READY":
        blockers.append("observability_event_alignment_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "input_read_allowed",
        "temporal_packet_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    alignment_input = _read_json(input_path)
    temporal = _read_json(temporal_path)
    max_bindings = 128
    if not plan:
        blockers.append("event_alignment_plan_missing_or_invalid")
    else:
        max_bindings = _validate_plan(plan, blockers)
    if not alignment_input:
        blockers.append("event_alignment_input_missing_or_invalid")
    elif alignment_input.get("version") != INPUT_VERSION:
        blockers.append("event_alignment_input_version_invalid")
    if not temporal:
        blockers.append("temporal_correlation_packet_missing_or_invalid")
    elif temporal.get("version") != TEMPORAL_VERSION:
        blockers.append("temporal_correlation_packet_version_invalid")
    elif temporal.get("interpretation_boundary", {}).get("causal_inference_performed") is not False:
        blockers.append("temporal_packet_causal_boundary_invalid")

    observations = temporal.get("observations", []) if temporal else []
    pairs = temporal.get("pairs", []) if temporal else []
    if not isinstance(observations, list):
        blockers.append("temporal_observations_not_list")
        observations = []
    if not isinstance(pairs, list):
        blockers.append("temporal_pairs_not_list")
        pairs = []

    observation_ids: set[str] = set()
    providers: dict[str, str] = {}
    for index, observation in enumerate(observations):
        if not isinstance(observation, Mapping):
            blockers.append(f"temporal_observation_{index}_not_object")
            continue
        oid = str(observation.get("observation_id", "")).strip()
        if not oid:
            blockers.append(f"temporal_observation_{index}_id_missing")
            continue
        if oid in observation_ids:
            blockers.append("duplicate_temporal_observation_id")
        observation_ids.add(oid)
        providers[oid] = str(observation.get("provider", ""))

    bindings = (
        _binding_map(alignment_input, observation_ids, max_bindings, blockers)
        if alignment_input
        else {}
    )

    if alignment_input:
        expected_temporal_digest = str(
            alignment_input.get("source_temporal_packet_digest", "")
        )
        actual_temporal_digest = _sha(temporal)
        if expected_temporal_digest != actual_temporal_digest:
            blockers.append("source_temporal_packet_digest_mismatch")

    aligned_pairs: list[dict[str, Any]] = []
    if not blockers:
        for index, pair in enumerate(pairs):
            if not isinstance(pair, Mapping):
                blockers.append(f"temporal_pair_{index}_not_object")
                continue
            left_id = str(pair.get("left_observation_id", ""))
            right_id = str(pair.get("right_observation_id", ""))
            if left_id not in observation_ids or right_id not in observation_ids:
                blockers.append(f"temporal_pair_{index}_references_unknown_observation")
                continue
            left_identifiers = bindings.get(left_id, {})
            right_identifiers = bindings.get(right_id, {})
            shared, distinct_types = _shared_identifier_evidence(
                left_identifiers,
                right_identifiers,
            )
            temporal_relation = str(pair.get("relation", ""))
            temporally_compatible = pair.get("temporally_compatible") is True
            state = _alignment_state(
                temporal_relation,
                temporally_compatible,
                bool(shared),
            )
            aligned_pairs.append(
                {
                    "left_observation_id": left_id,
                    "right_observation_id": right_id,
                    "left_provider": providers.get(left_id, ""),
                    "right_provider": providers.get(right_id, ""),
                    "temporal_relation": temporal_relation,
                    "temporally_compatible": temporally_compatible,
                    "alignment_state": state,
                    "has_shared_exact_identifier": bool(shared),
                    "shared_identifier_evidence": shared,
                    "same_type_distinct_value_identifiers": distinct_types,
                    "identity_values_exposed": False,
                    "causal_claim": "not_inferred",
                    "causal_direction": "not_inferred",
                    "causal_claim_permitted": False,
                }
            )

    counts = {
        "exact_compatible": sum(
            1 for p in aligned_pairs
            if p["alignment_state"] == "exact_context_temporally_compatible"
        ),
        "exact_disjoint": sum(
            1 for p in aligned_pairs
            if p["alignment_state"] == "exact_context_temporally_disjoint"
        ),
        "exact_unresolved": sum(
            1 for p in aligned_pairs
            if p["alignment_state"] == "exact_context_time_unresolved"
        ),
        "temporal_only": sum(
            1 for p in aligned_pairs if p["alignment_state"] == "temporal_only"
        ),
        "no_evidence": sum(
            1 for p in aligned_pairs if p["alignment_state"] == "no_alignment_evidence"
        ),
        "source_obstruction": sum(
            1 for p in aligned_pairs if p["alignment_state"] == "source_obstruction"
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        partial = counts["exact_disjoint"] > 0 or counts["exact_unresolved"] > 0 or counts["source_obstruction"] > 0
        status = PARTIAL if partial else READY
        output = {
            "version": VERSION,
            "status": status,
            "source_temporal_packet_digest": _sha(temporal),
            "source_identity_input_digest": _sha(alignment_input),
            "observation_count": len(observation_ids),
            "pair_count": len(aligned_pairs),
            "pairs": aligned_pairs,
            "summary": counts,
            "interpretation_boundary": {
                "shared_identifier_is_context_evidence_not_causation": True,
                "temporal_compatibility_is_not_causation": True,
                "causal_inference_performed": False,
                "causal_direction_inferred": False,
                "causal_claim_permitted": False,
                "identifier_values_exposed": False,
                "source_authority_transferred": False,
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-event-alignment-" + _sha(
        {
            "plan": plan,
            "input": alignment_input,
            "temporal_digest": _sha(temporal),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "observation_count": len(observation_ids),
        "pair_count": len(aligned_pairs),
        "exact_context_compatible_count": counts["exact_compatible"],
        "exact_context_disjoint_count": counts["exact_disjoint"],
        "exact_context_time_unresolved_count": counts["exact_unresolved"],
        "temporal_only_count": counts["temporal_only"],
        "no_alignment_evidence_count": counts["no_evidence"],
        "source_obstruction_count": counts["source_obstruction"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "causal_inference_performed": False,
        "identifier_values_exposed": False,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ObservabilityEventAlignmentResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(observation_ids),
        len(aligned_pairs),
        counts["exact_compatible"],
        counts["exact_disjoint"],
        counts["exact_unresolved"],
        counts["temporal_only"],
        counts["no_evidence"],
        counts["source_obstruction"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
