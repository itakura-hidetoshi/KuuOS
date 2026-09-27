#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_observability_temporal_correlation_v7_2"
PLAN_VERSION = "kuuos_observability_temporal_correlation_plan_v7_2"
INPUT_VERSION = "kuuos_observability_temporal_correlation_input_v7_2"
READY = "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_READY"
PARTIAL = "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_PARTIAL"
BLOCKED = "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_BLOCKED"

INGESTED_STATUSES = {
    "KUUOS_OBSERVABILITY_MCP_MULTIPLEXER_INGESTED",
    "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_TERMINAL",
    "QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_BOUNDED",
}
TRANSIENT_STATUSES = {
    "KUUOS_OBSERVABILITY_MCP_TRANSIENT_OBSTRUCTION",
}
UNAVAILABLE_STATUSES = {
    "KUUOS_OBSERVABILITY_MCP_PROVIDER_UNAVAILABLE",
}

DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ObservabilityTemporalCorrelationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    observation_count: int
    pair_count: int
    compatible_pair_count: int
    disjoint_pair_count: int
    insufficient_pair_count: int
    transient_pair_count: int
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


def _parse_time(value: Any) -> datetime | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        try:
            return datetime.fromtimestamp(float(text), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _iso(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.isoformat().replace("+00:00", "Z")


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> int:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("causal_inference_allowed") is not False:
        blockers.append("causal_inference_must_be_false")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")
    tolerance = _i(plan.get("temporal_tolerance_seconds"), 5)
    if tolerance < 0 or tolerance > 3600:
        blockers.append("temporal_tolerance_seconds_out_of_bounds")
    return tolerance


def _extract_time_hint(observation: Mapping[str, Any], key: str) -> Any:
    direct = observation.get(key)
    if direct not in (None, ""):
        return direct
    shape = _m(observation.get("shape_summary"))
    direct = shape.get(key)
    if direct not in (None, ""):
        return direct
    if key == "first_timestamp_hint":
        return observation.get("started_at", observation.get("epoch"))
    return observation.get("finished_at", observation.get("epoch"))


def _normalize_observation(
    raw: Mapping[str, Any],
    index: int,
    blockers: list[str],
) -> dict[str, Any]:
    observation_id = str(raw.get("observation_id", f"observation-{index + 1}")).strip()
    provider = str(raw.get("provider", "")).strip()
    operation = str(raw.get("operation", raw.get("data_class", ""))).strip()
    source_digest = str(
        raw.get(
            "observed_value_digest",
            raw.get("source_digest", raw.get("latest_log_digest", "")),
        )
    ).strip()
    source_status = str(raw.get("status", "")).strip()

    if not observation_id:
        blockers.append(f"observation_{index}_id_missing")
    if not provider:
        blockers.append(f"observation_{index}_provider_missing")
    if source_digest and DIGEST_RE.fullmatch(source_digest) is None:
        blockers.append(f"observation_{index}_source_digest_invalid")

    first_raw = _extract_time_hint(raw, "first_timestamp_hint")
    last_raw = _extract_time_hint(raw, "last_timestamp_hint")
    start = _parse_time(first_raw)
    end = _parse_time(last_raw)
    if start is not None and end is None:
        end = start
    if end is not None and start is None:
        start = end
    if start is not None and end is not None and end < start:
        blockers.append(f"observation_{index}_time_window_reversed")

    availability = "observed"
    if source_status in TRANSIENT_STATUSES:
        availability = "transient"
    elif source_status in UNAVAILABLE_STATUSES:
        availability = "unavailable"
    elif source_status and source_status not in INGESTED_STATUSES:
        availability = "other_status"

    return {
        "observation_id": observation_id,
        "provider": provider,
        "operation": operation,
        "source_digest": source_digest,
        "source_status": source_status,
        "availability": availability,
        "window_start": _iso(start),
        "window_end": _iso(end),
        "_start": start,
        "_end": end,
    }


def _pair_relation(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    tolerance_seconds: int,
) -> dict[str, Any]:
    left_start = left.get("_start")
    left_end = left.get("_end")
    right_start = right.get("_start")
    right_end = right.get("_end")

    relation = "insufficient_time_metadata"
    gap_seconds: float | None = None
    temporally_compatible = False
    reason = "one_or_both_time_windows_missing"

    if left.get("availability") in {"transient", "unavailable"} or right.get(
        "availability"
    ) in {"transient", "unavailable"}:
        relation = "source_obstruction"
        reason = "one_or_both_sources_not_currently_observed"
    elif all(
        isinstance(value, datetime)
        for value in (left_start, left_end, right_start, right_end)
    ):
        if left_start <= right_end and right_start <= left_end:
            relation = "overlap"
            gap_seconds = 0.0
            temporally_compatible = True
            reason = "closed_time_windows_overlap"
        elif left_end < right_start:
            gap_seconds = (right_start - left_end).total_seconds()
            if gap_seconds <= tolerance_seconds:
                relation = "within_tolerance"
                temporally_compatible = True
                reason = "left_precedes_right_within_tolerance"
            else:
                relation = "disjoint"
                reason = "left_precedes_right_beyond_tolerance"
        else:
            gap_seconds = (left_start - right_end).total_seconds()
            if gap_seconds <= tolerance_seconds:
                relation = "within_tolerance"
                temporally_compatible = True
                reason = "right_precedes_left_within_tolerance"
            else:
                relation = "disjoint"
                reason = "right_precedes_left_beyond_tolerance"

    return {
        "left_observation_id": left["observation_id"],
        "right_observation_id": right["observation_id"],
        "left_provider": left["provider"],
        "right_provider": right["provider"],
        "relation": relation,
        "temporally_compatible": temporally_compatible,
        "gap_seconds": gap_seconds,
        "tolerance_seconds": tolerance_seconds,
        "reason": reason,
        "causal_claim": "not_inferred",
        "causal_claim_permitted": False,
    }


def build_observability_temporal_correlation(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> ObservabilityTemporalCorrelationResult:
    ctx = _m(runtime_context)
    authority = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "observability_temporal_correlation_plan_v7_2.json"
    input_path = root / "observability_temporal_correlation_input_v7_2.json"
    output_path = root / "observability_temporal_correlation_packet_v7_2.json"
    receipt_path = root / "observability_temporal_correlation_receipt_v7_2.json"
    audit_path = root / "observability_temporal_correlation_audit_v7_2.jsonl"

    if ctx.get("observability_temporal_correlation_enabled") is not True:
        blockers.append("observability_temporal_correlation_enabled_not_true")
    if ctx.get("apply_observability_temporal_correlation") is not True:
        blockers.append("apply_observability_temporal_correlation_not_true")
    if authority.get("authority_status") != "KUUOS_OBSERVABILITY_TEMPORAL_CORRELATION_AUTHORITY_READY":
        blockers.append("observability_temporal_correlation_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    correlation_input = _read_json(input_path)
    if not plan:
        blockers.append("temporal_correlation_plan_missing_or_invalid")
        tolerance = 5
    else:
        tolerance = _validate_plan(plan, blockers)
    if not correlation_input:
        blockers.append("temporal_correlation_input_missing_or_invalid")
    elif correlation_input.get("version") != INPUT_VERSION:
        blockers.append("temporal_correlation_input_version_invalid")

    raw_observations = correlation_input.get("observations", []) if correlation_input else []
    if not isinstance(raw_observations, list):
        blockers.append("observations_not_list")
        raw_observations = []
    max_observations = _i(plan.get("max_observations"), 32) if plan else 32
    if max_observations < 2 or max_observations > 128:
        blockers.append("max_observations_out_of_bounds")
    if len(raw_observations) < 2:
        blockers.append("at_least_two_observations_required")
    if len(raw_observations) > max_observations:
        blockers.append("observation_count_exceeds_plan_bound")

    observations: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, item in enumerate(raw_observations):
        if not isinstance(item, Mapping):
            blockers.append(f"observation_{index}_not_object")
            continue
        normalized = _normalize_observation(item, index, blockers)
        oid = normalized["observation_id"]
        if oid in ids:
            blockers.append("duplicate_observation_id")
        ids.add(oid)
        observations.append(normalized)

    pairs: list[dict[str, Any]] = []
    if not blockers:
        for i, left in enumerate(observations):
            for right in observations[i + 1 :]:
                pairs.append(_pair_relation(left, right, tolerance))

    counts = {
        "compatible": sum(1 for p in pairs if p["temporally_compatible"]),
        "disjoint": sum(1 for p in pairs if p["relation"] == "disjoint"),
        "insufficient": sum(
            1 for p in pairs if p["relation"] == "insufficient_time_metadata"
        ),
        "transient": sum(1 for p in pairs if p["relation"] == "source_obstruction"),
    }

    public_observations = [
        {k: v for k, v in observation.items() if not k.startswith("_")}
        for observation in observations
    ]

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        output = {
            "version": VERSION,
            "status": READY if counts["insufficient"] == 0 and counts["transient"] == 0 else PARTIAL,
            "temporal_tolerance_seconds": tolerance,
            "observations": public_observations,
            "pairs": pairs,
            "summary": {
                "observation_count": len(public_observations),
                "pair_count": len(pairs),
                "compatible_pair_count": counts["compatible"],
                "disjoint_pair_count": counts["disjoint"],
                "insufficient_pair_count": counts["insufficient"],
                "transient_pair_count": counts["transient"],
            },
            "interpretation_boundary": {
                "temporal_compatibility_is_not_causation": True,
                "causal_inference_performed": False,
                "causal_claim_permitted": False,
                "source_authority_transferred": False,
                "raw_provider_payloads_present": False,
            },
            "source_input_digest": _sha(correlation_input),
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
        status = str(output["status"])
    else:
        status = BLOCKED

    packet_id = "kuuos-observability-temporal-correlation-" + _sha(
        {
            "plan": plan,
            "input": correlation_input,
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "observation_count": len(public_observations),
        "pair_count": len(pairs),
        "compatible_pair_count": counts["compatible"],
        "disjoint_pair_count": counts["disjoint"],
        "insufficient_pair_count": counts["insufficient"],
        "transient_pair_count": counts["transient"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "causal_inference_performed": False,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return ObservabilityTemporalCorrelationResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(public_observations),
        len(pairs),
        counts["compatible"],
        counts["disjoint"],
        counts["insufficient"],
        counts["transient"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
