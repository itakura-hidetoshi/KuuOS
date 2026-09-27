#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_samvrti_world_version_dynamics_v7_15"
PLAN_VERSION = "kuuos_samvrti_world_version_dynamics_plan_v7_15"
INPUT_VERSION = "kuuos_samvrti_world_version_diagnostics_input_v7_15"
SOURCE_VERSION = "kuuos_runtime_samvrti_world_effect_update_v7_14"

READY = "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_READY"
PARTIAL = "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_PARTIAL"
OBSTRUCTED = "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_OBSTRUCTED"
BLOCKED = "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_BLOCKED"

REVERSIBLE_LOCAL = "reversible_local_samvrti_dynamics"
CUMULATIVE_DRIFT = "cumulative_samvrti_drift"
STRUCTURAL_DRIFT = "structural_world_drift_rebind_required"
SINGLE_VERSION = "single_world_transition_observed"
INDETERMINATE = "samvrti_dynamics_indeterminate"
HISTORY_DISCONNECTED = "samvrti_world_history_disconnected"
FIBER_OBSTRUCTED = "paramartha_fiber_obstructed"


@dataclass(frozen=True)
class SamvrtiWorldVersionDynamicsResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    world_version_count: int
    fiber_count: int
    reversible_local_fiber_count: int
    cumulative_drift_fiber_count: int
    structural_drift_fiber_count: int
    single_version_fiber_count: int
    indeterminate_fiber_count: int
    obstructed_fiber_count: int
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


def _unit(value: Any, name: str, blockers: list[str]) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        blockers.append(name + "_must_be_number")
        return 0.0
    out = float(value)
    if out < 0.0 or out > 1.0:
        blockers.append(name + "_out_of_range")
    return max(0.0, min(1.0, out))


def _nonnegative(value: Any, name: str, blockers: list[str]) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        blockers.append(name + "_must_be_number")
        return 0.0
    out = float(value)
    if out < 0.0:
        blockers.append(name + "_negative")
        return 0.0
    return out


def _positive_int(value: Any, name: str, blockers: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        blockers.append(name + "_must_be_positive_int")
        return 1
    return value


def _validate_plan(
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, float | int]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("read_only") is not True:
        blockers.append("read_only_not_true")
    if plan.get("policy_thresholds_are_semantic_truth") is not False:
        blockers.append("policy_thresholds_semantic_truth_must_be_false")
    if plan.get("world_digest_change_alone_is_structural_drift") is not False:
        blockers.append("world_digest_change_structural_drift_must_be_false")
    if plan.get("structural_drift_changes_paramartha_class") is not False:
        blockers.append("structural_drift_paramartha_change_must_be_false")
    if plan.get("structural_drift_blocks_world_independent_action") is not False:
        blockers.append("structural_drift_world_independent_block_must_be_false")
    if plan.get("history_composition_required") is not True:
        blockers.append("history_composition_required_not_true")
    if plan.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_must_be_false")

    return {
        "max_local_change_score": _unit(
            plan.get("max_local_change_score"),
            "max_local_change_score",
            blockers,
        ),
        "minimum_local_reversibility": _unit(
            plan.get("minimum_local_reversibility"),
            "minimum_local_reversibility",
            blockers,
        ),
        "minimum_local_recoverability": _unit(
            plan.get("minimum_local_recoverability"),
            "minimum_local_recoverability",
            blockers,
        ),
        "maximum_local_impact": _unit(
            plan.get("maximum_local_impact"),
            "maximum_local_impact",
            blockers,
        ),
        "cumulative_drift_score_threshold": _nonnegative(
            plan.get("cumulative_drift_score_threshold"),
            "cumulative_drift_score_threshold",
            blockers,
        ),
        "repeated_axis_count_threshold": _positive_int(
            plan.get("repeated_axis_count_threshold"),
            "repeated_axis_count_threshold",
            blockers,
        ),
    }


def _source_versions(
    source: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = source.get("materialized_samvrti_world_versions", [])
    if not isinstance(raw, list):
        blockers.append("source_materialized_world_versions_not_list")
        return {}

    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"source_world_version_{index}_not_object")
            continue

        version_id = str(item.get("samvrti_world_version_id", "")).strip()
        if not version_id:
            blockers.append(f"source_world_version_{index}_id_missing")
            continue
        if version_id in result:
            blockers.append("duplicate_source_world_version_id")
            continue

        before = str(
            item.get("paramartha_carrier_element_id_before", "")
        ).strip()
        after = str(
            item.get("paramartha_carrier_element_id_after", "")
        ).strip()
        if not before or not after:
            blockers.append(f"source_world_version_{index}_paramartha_missing")
        if before != after:
            blockers.append(
                f"source_world_version_{index}_paramartha_class_changed"
            )
        if item.get("paramartha_class_changed") is not False:
            blockers.append(
                f"source_world_version_{index}_paramartha_boundary_invalid"
            )
        if item.get("world_transition_is_ultimate_truth") is not False:
            blockers.append(
                f"source_world_version_{index}_ultimate_truth_boundary_invalid"
            )
        if item.get("mission_success_implied") is not False:
            blockers.append(
                f"source_world_version_{index}_mission_success_boundary_invalid"
            )

        for field in (
            "target_samvrti_world_id",
            "prior_world_state_digest",
            "observed_world_state_digest",
            "observed_effect_digest",
            "samvrti_world_transition_digest",
            "transaction_final_receipt_digest",
        ):
            if not str(item.get(field, "")).strip():
                blockers.append(
                    f"source_world_version_{index}_{field}_missing"
                )

        result[version_id] = dict(item)

    return result


def _diagnostics(
    packet: Mapping[str, Any],
    source_versions: Mapping[str, Mapping[str, Any]],
    blockers: list[str],
) -> dict[str, dict[str, Any]]:
    raw = packet.get("diagnostics", [])
    if not isinstance(raw, list):
        blockers.append("diagnostics_not_list")
        return {}

    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            blockers.append(f"diagnostic_{index}_not_object")
            continue
        version_id = str(item.get("samvrti_world_version_id", "")).strip()
        if not version_id:
            blockers.append(f"diagnostic_{index}_version_id_missing")
            continue
        if version_id not in source_versions:
            blockers.append(f"diagnostic_{index}_unknown_world_version")
            continue
        if version_id in result:
            blockers.append("duplicate_diagnostic_world_version_id")
            continue

        sequence_index = item.get("sequence_index")
        if (
            isinstance(sequence_index, bool)
            or not isinstance(sequence_index, int)
            or sequence_index < 0
        ):
            blockers.append(f"diagnostic_{index}_sequence_index_invalid")
            sequence_index = 0

        local_change = _unit(
            item.get("local_change_score"),
            f"diagnostic_{index}_local_change_score",
            blockers,
        )
        reversibility = _unit(
            item.get("reversibility"),
            f"diagnostic_{index}_reversibility",
            blockers,
        )
        recoverability = _unit(
            item.get("recoverability"),
            f"diagnostic_{index}_recoverability",
            blockers,
        )
        impact = _unit(
            item.get("impact_radius"),
            f"diagnostic_{index}_impact_radius",
            blockers,
        )

        drift_axis_digest = str(item.get("drift_axis_digest", "")).strip()
        binding_signature = str(
            item.get("world_binding_signature_digest", "")
        ).strip()
        structural_context = str(
            item.get("structural_context_digest", "")
        ).strip()

        if not drift_axis_digest:
            blockers.append(f"diagnostic_{index}_drift_axis_digest_missing")
        if not binding_signature:
            blockers.append(
                f"diagnostic_{index}_world_binding_signature_digest_missing"
            )
        if not structural_context:
            blockers.append(
                f"diagnostic_{index}_structural_context_digest_missing"
            )

        result[version_id] = {
            "samvrti_world_version_id": version_id,
            "sequence_index": sequence_index,
            "local_change_score": local_change,
            "reversibility": reversibility,
            "recoverability": recoverability,
            "impact_radius": impact,
            "drift_axis_digest": drift_axis_digest,
            "world_binding_signature_digest": binding_signature,
            "structural_context_digest": structural_context,
            "binding_revalidation_requested": item.get(
                "binding_revalidation_requested"
            )
            is True,
            "diagnostic_receipt_digest": str(
                item.get("diagnostic_receipt_digest", "")
            ).strip(),
        }
        if not result[version_id]["diagnostic_receipt_digest"]:
            blockers.append(
                f"diagnostic_{index}_diagnostic_receipt_digest_missing"
            )

    if set(result) != set(source_versions):
        missing = sorted(set(source_versions).difference(result))
        extra = sorted(set(result).difference(source_versions))
        if missing:
            blockers.append(
                "diagnostics_missing_for_world_versions:" + ",".join(missing)
            )
        if extra:
            blockers.append(
                "diagnostics_unknown_world_versions:" + ",".join(extra)
            )
    return result


def _max_run(values: list[str]) -> int:
    if not values:
        return 0
    best = 1
    current = 1
    for left, right in zip(values, values[1:]):
        if left == right:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best


def _fiber_record(
    *,
    paramartha_carrier: str,
    world_id: str,
    versions: list[Mapping[str, Any]],
    diagnostics: Mapping[str, Mapping[str, Any]],
    policy: Mapping[str, float | int],
) -> dict[str, Any]:
    ordered = sorted(
        versions,
        key=lambda version: diagnostics[
            str(version["samvrti_world_version_id"])
        ]["sequence_index"],
    )

    errors: list[str] = []
    sequence_indices = [
        int(diagnostics[str(v["samvrti_world_version_id"])]["sequence_index"])
        for v in ordered
    ]
    if len(sequence_indices) != len(set(sequence_indices)):
        errors.append("duplicate_sequence_index")

    chain_continuous = True
    for previous, current in zip(ordered, ordered[1:]):
        if (
            str(current["prior_world_state_digest"])
            != str(previous["observed_world_state_digest"])
        ):
            chain_continuous = False
            errors.append(
                "world_history_chain_break:"
                + str(previous["samvrti_world_version_id"])
                + "->"
                + str(current["samvrti_world_version_id"])
            )

    paramartha_values = {
        str(v.get("paramartha_carrier_element_id_before", ""))
        for v in ordered
    } | {
        str(v.get("paramartha_carrier_element_id_after", ""))
        for v in ordered
    }
    if paramartha_values != {paramartha_carrier}:
        errors.append("paramartha_fiber_inconsistent")

    diags = [
        diagnostics[str(v["samvrti_world_version_id"])]
        for v in ordered
    ]
    cumulative_change = sum(float(d["local_change_score"]) for d in diags)
    axis_values = [str(d["drift_axis_digest"]) for d in diags]
    max_axis_run = _max_run(axis_values)
    binding_signatures = {
        str(d["world_binding_signature_digest"]) for d in diags
    }
    structural_contexts = {
        str(d["structural_context_digest"]) for d in diags
    }
    explicit_rebind = any(
        bool(d["binding_revalidation_requested"]) for d in diags
    )

    local_reversible = all(
        float(d["local_change_score"])
        <= float(policy["max_local_change_score"])
        and float(d["reversibility"])
        >= float(policy["minimum_local_reversibility"])
        and float(d["recoverability"])
        >= float(policy["minimum_local_recoverability"])
        and float(d["impact_radius"])
        <= float(policy["maximum_local_impact"])
        for d in diags
    )

    structural_signal = (
        len(binding_signatures) > 1
        or len(structural_contexts) > 1
        or explicit_rebind
    )
    cumulative_signal = (
        cumulative_change
        >= float(policy["cumulative_drift_score_threshold"])
        or max_axis_run >= int(policy["repeated_axis_count_threshold"])
    )

    if "paramartha_fiber_inconsistent" in errors:
        dynamics = FIBER_OBSTRUCTED
    elif not chain_continuous or "duplicate_sequence_index" in errors:
        dynamics = HISTORY_DISCONNECTED
    elif len(ordered) == 1:
        dynamics = SINGLE_VERSION
    elif structural_signal:
        dynamics = STRUCTURAL_DRIFT
    elif cumulative_signal:
        dynamics = CUMULATIVE_DRIFT
    elif local_reversible:
        dynamics = REVERSIBLE_LOCAL
    else:
        dynamics = INDETERMINATE

    if dynamics == STRUCTURAL_DRIFT:
        binding_recheck = True
        existing_binding_status = "recheck_world_dependent_bindings"
        world_independent_action_reuse = True
        planning_feedback = "refresh_world_model_and_replan_world_dependent_steps"
    elif dynamics == CUMULATIVE_DRIFT:
        binding_recheck = False
        existing_binding_status = "provisional_binding_reuse_with_fresh_observation"
        world_independent_action_reuse = True
        planning_feedback = "refresh_observation_and_consider_replan"
    elif dynamics == REVERSIBLE_LOCAL:
        binding_recheck = False
        existing_binding_status = "binding_reuse_eligible"
        world_independent_action_reuse = True
        planning_feedback = "ordinary_feedback_update"
    elif dynamics == SINGLE_VERSION:
        binding_recheck = False
        existing_binding_status = "insufficient_history_for_drift_classification"
        world_independent_action_reuse = True
        planning_feedback = "accumulate_more_verified_history"
    elif dynamics in {HISTORY_DISCONNECTED, FIBER_OBSTRUCTED}:
        binding_recheck = True
        existing_binding_status = "history_repair_or_rebinding_required"
        world_independent_action_reuse = True
        planning_feedback = "repair_history_binding_before_world_dependent_reuse"
    else:
        binding_recheck = False
        existing_binding_status = "binding_status_undetermined"
        world_independent_action_reuse = True
        planning_feedback = "fresh_observation_and_context_review"

    return {
        "fiber_id": "samvrti-dynamics-fiber-"
        + _sha(
            {
                "paramartha_carrier_element_id": paramartha_carrier,
                "target_samvrti_world_id": world_id,
            }
        )[:20],
        "paramartha_carrier_element_id": paramartha_carrier,
        "target_samvrti_world_id": world_id,
        "world_version_ids": [
            str(v["samvrti_world_version_id"]) for v in ordered
        ],
        "transition_count": len(ordered),
        "initial_world_state_digest": (
            str(ordered[0]["prior_world_state_digest"]) if ordered else ""
        ),
        "latest_world_state_digest": (
            str(ordered[-1]["observed_world_state_digest"]) if ordered else ""
        ),
        "history_chain_continuous": chain_continuous,
        "cumulative_change_score": cumulative_change,
        "maximum_repeated_drift_axis_run": max_axis_run,
        "distinct_world_binding_signature_count": len(binding_signatures),
        "distinct_structural_context_count": len(structural_contexts),
        "explicit_binding_revalidation_requested": explicit_rebind,
        "all_steps_locally_reversible": local_reversible,
        "samvrti_dynamics": dynamics,
        "world_dependent_binding_recheck_required": binding_recheck,
        "existing_world_binding_status": existing_binding_status,
        "world_independent_action_reuse_allowed": world_independent_action_reuse,
        "planning_feedback": planning_feedback,
        "paramartha_class_changed": False,
        "paramartha_reclassification_required": False,
        "policy_thresholds_are_semantic_truth": False,
        "fiber_errors": sorted(set(errors)),
    }


def build_samvrti_world_version_dynamics(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> SamvrtiWorldVersionDynamicsResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "samvrti_world_version_dynamics_plan_v7_15.json"
    source_path = root / "samvrti_world_effect_update_packet_v7_14.json"
    input_path = root / "samvrti_world_version_diagnostics_input_v7_15.json"
    output_path = root / "samvrti_world_version_dynamics_packet_v7_15.json"
    receipt_path = root / "samvrti_world_version_dynamics_receipt_v7_15.json"
    audit_path = root / "samvrti_world_version_dynamics_audit_v7_15.jsonl"

    if ctx.get("samvrti_world_version_dynamics_enabled") is not True:
        blockers.append("samvrti_world_version_dynamics_enabled_not_true")
    if ctx.get("apply_samvrti_world_version_dynamics") is not True:
        blockers.append("apply_samvrti_world_version_dynamics_not_true")
    if (
        authority_packet.get("authority_status")
        != "KUUOS_SAMVRTI_WORLD_VERSION_DYNAMICS_AUTHORITY_READY"
    ):
        blockers.append("samvrti_world_version_dynamics_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "source_world_update_packet_read_allowed",
        "diagnostics_input_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    source = _read_json(source_path)
    diagnostics_packet = _read_json(input_path)

    policy: dict[str, float | int] = {}
    if not plan:
        blockers.append("samvrti_dynamics_plan_missing_or_invalid")
    else:
        policy = _validate_plan(plan, blockers)

    if not source:
        blockers.append("samvrti_world_update_packet_missing_or_invalid")
    elif source.get("version") != SOURCE_VERSION:
        blockers.append("samvrti_world_update_packet_version_invalid")

    if not diagnostics_packet:
        blockers.append("samvrti_world_diagnostics_input_missing_or_invalid")
    elif diagnostics_packet.get("version") != INPUT_VERSION:
        blockers.append("samvrti_world_diagnostics_input_version_invalid")

    if plan and source and diagnostics_packet:
        source_digest = _sha(source)
        if str(plan.get("source_world_update_packet_digest", "")) != source_digest:
            blockers.append("source_world_update_packet_digest_mismatch")
        if (
            str(
                diagnostics_packet.get(
                    "source_world_update_packet_digest",
                    "",
                )
            )
            != source_digest
        ):
            blockers.append("diagnostics_source_world_update_packet_digest_mismatch")

        boundary = _m(source.get("two_truths_effect_return_boundary"))
        if boundary.get("world_update_may_change_paramartha_class") is not False:
            blockers.append("source_paramartha_noncollapse_boundary_invalid")
        if boundary.get("samvrti_world_versions_are_append_only") is not True:
            blockers.append("source_append_only_world_history_missing")
        if boundary.get("observed_world_transition_is_conventional_not_ultimate") is not True:
            blockers.append("source_conventional_world_boundary_missing")

    source_versions = _source_versions(source, blockers) if source else {}
    diagnostics = (
        _diagnostics(
            diagnostics_packet,
            source_versions,
            blockers,
        )
        if diagnostics_packet
        else {}
    )

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    if not blockers:
        for version in source_versions.values():
            key = (
                str(version["paramartha_carrier_element_id_after"]),
                str(version["target_samvrti_world_id"]),
            )
            grouped.setdefault(key, []).append(version)

    fibers: list[dict[str, Any]] = []
    if not blockers:
        for (paramartha, world_id), versions in sorted(grouped.items()):
            fibers.append(
                _fiber_record(
                    paramartha_carrier=paramartha,
                    world_id=world_id,
                    versions=versions,
                    diagnostics=diagnostics,
                    policy=policy,
                )
            )

    counts = {
        "local": sum(1 for f in fibers if f["samvrti_dynamics"] == REVERSIBLE_LOCAL),
        "cumulative": sum(1 for f in fibers if f["samvrti_dynamics"] == CUMULATIVE_DRIFT),
        "structural": sum(1 for f in fibers if f["samvrti_dynamics"] == STRUCTURAL_DRIFT),
        "single": sum(1 for f in fibers if f["samvrti_dynamics"] == SINGLE_VERSION),
        "indeterminate": sum(1 for f in fibers if f["samvrti_dynamics"] == INDETERMINATE),
        "obstructed": sum(
            1
            for f in fibers
            if f["samvrti_dynamics"] in {HISTORY_DISCONNECTED, FIBER_OBSTRUCTED}
        ),
    }

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        if counts["obstructed"] > 0:
            status = OBSTRUCTED
        elif counts["single"] > 0 or counts["indeterminate"] > 0:
            status = PARTIAL
        else:
            status = READY

        output = {
            "version": VERSION,
            "status": status,
            "source_world_update_packet_digest": _sha(source),
            "samvrti_dynamics_fibers": fibers,
            "summary": {
                "world_version_count": len(source_versions),
                "fiber_count": len(fibers),
                "reversible_local_fiber_count": counts["local"],
                "cumulative_drift_fiber_count": counts["cumulative"],
                "structural_drift_fiber_count": counts["structural"],
                "single_version_fiber_count": counts["single"],
                "indeterminate_fiber_count": counts["indeterminate"],
                "obstructed_fiber_count": counts["obstructed"],
            },
            "dependent_origination_dynamics_boundary": {
                "history_composition_required": True,
                "world_digest_change_alone_is_structural_drift": False,
                "policy_thresholds_are_semantic_truth": False,
                "structural_drift_changes_paramartha_class": False,
                "structural_drift_requires_world_dependent_binding_recheck": True,
                "structural_drift_blocks_world_independent_action": False,
                "cumulative_drift_preserves_paramartha_fiber": True,
                "reversible_local_change_is_first_class": True,
                "history_discontinuity_is_not_filled_by_fabrication": True,
                "world_history_remains_append_only": True,
                "source_authority_transferred": False,
            },
            "formal_correspondence_note": {
                "structural_mirror_only": True,
                "formal_reference": "formal/KUOS/DependentOriginationRelationalFeedbackSemanticsV0_1.lean",
                "history_reference": "formal/KUOS/DependentOriginationMemoryLiftedHistoryTransportV0_7.lean",
                "runtime_policy_note": "numeric thresholds classify bounded operational diagnostics only and are not theorem-level semantic truths",
                "formal_gap": "does not instantiate the abstract RelationalFeedbackSystem or prove runtime drift classes as Lean theorems",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True
    else:
        status = BLOCKED

    packet_id = "kuuos-samvrti-world-version-dynamics-" + _sha(
        {
            "plan": plan,
            "source_digest": _sha(source),
            "diagnostics_digest": _sha(diagnostics_packet),
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "world_version_count": len(source_versions),
        "fiber_count": len(fibers),
        "reversible_local_fiber_count": counts["local"],
        "cumulative_drift_fiber_count": counts["cumulative"],
        "structural_drift_fiber_count": counts["structural"],
        "single_version_fiber_count": counts["single"],
        "indeterminate_fiber_count": counts["indeterminate"],
        "obstructed_fiber_count": counts["obstructed"],
        "output_written": output_written,
        "output_digest": _sha(output),
        "policy_thresholds_are_semantic_truth": False,
        "structural_drift_changes_paramartha_class": False,
        "structural_drift_blocks_world_independent_action": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return SamvrtiWorldVersionDynamicsResult(
        VERSION,
        status,
        packet_id,
        str(root),
        len(source_versions),
        len(fibers),
        counts["local"],
        counts["cumulative"],
        counts["structural"],
        counts["single"],
        counts["indeterminate"],
        counts["obstructed"],
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
