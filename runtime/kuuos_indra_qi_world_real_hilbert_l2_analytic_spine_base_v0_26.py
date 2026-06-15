#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
import pathlib
import time
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_plan_v0_26"
LICENSE_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_license_v0_26"
REPORT_VERSION = "indra_qi_world_real_hilbert_l2_embedding_report_v0_26"
STATE_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_state_v0_26"
RECOMMENDATION_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_recommendation_v0_26"
LEDGER_VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_ledger_record_v0_26"
WORLD_VERSION = "indra_qi_world_model_v0_1"
VERSION = "indra_qi_world_real_hilbert_l2_analytic_spine_v0_26"
READY = "INDRA_QI_WORLD_REAL_HILBERT_L2_ANALYTIC_SPINE_V0_26_READY"
BLOCKED = "INDRA_QI_WORLD_REAL_HILBERT_L2_ANALYTIC_SPINE_V0_26_BLOCKED"

SOURCE_KIND_FIELDS = {
    "local_patch": ("local_world_patches", "patch_id"),
    "indra_connection": ("indra_connections", "connection_id"),
    "qi_flow": ("qi_flow_channels", "flow_id"),
    "holonomy_cycle": ("holonomy_cycles", "cycle_id"),
    "ku_string": ("ku_string_correspondences", "string_id"),
    "m_brane_surface": ("extended_m_brane_surfaces", "surface_id"),
}
REQUIRED_PROJECTION_ROLES = {"scar", "recovery", "minority_preservation"}
DECISIONS = {
    "world_l2_analytic_spine_ready",
    "redesign_world_l2_embedding_recommended",
    "restore_multi_world_coverage_recommended",
    "hold_for_observation",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_world_state_read_only": True,
    "world_not_identified_with_hilbert_vector": True,
    "representation_map_not_required_linear": True,
    "representation_map_not_required_injective": True,
    "representation_map_not_required_surjective": True,
    "real_scalar_field_required": True,
    "ell2_countable_basis_required": True,
    "finite_energy_required": True,
    "finite_support_runtime_witness_only": True,
    "inner_product_is_real": True,
    "weighted_energy_positive": True,
    "coercive_lower_bound_required": True,
    "rayleigh_lower_bound_required": True,
    "orthogonal_projection_diagnostics_only": True,
    "self_adjointness_not_claimed_by_runtime": True,
    "dense_core_template_not_operator_execution": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "candidate_weighting_not_truth": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_external_world_actuation_authority": True,
    "not_unbounded_operator_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(float(value))


def number(value: Any, default: float = 0.0) -> float:
    return float(value) if finite_number(value) else default


def sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    output = dict(value)
    output.pop(field, None)
    return output


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "world_l2_spine_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "world_l2_embedding_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "world_l2_spine_state_digest"))


def read_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return dict(value) if isinstance(value, Mapping) else {}


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    output: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid": True}
        output.append(dict(value) if isinstance(value, Mapping) else {"_invalid": True})
    return output


def write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _positive_int(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str]) -> None:
    for field in fields:
        value = policy.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            blockers.append(f"world_l2_policy_{field}_invalid")


def _bounded_nonnegative(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str]) -> None:
    for field in fields:
        value = policy.get(field)
        if not finite_number(value) or float(value) < 0:
            blockers.append(f"world_l2_policy_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("world_l2_plan_version_invalid")
    if plan.get("world_l2_spine_plan_digest") != plan_digest(plan):
        blockers.append("world_l2_plan_digest_invalid")
    for field in (
        "spine_id",
        "analysis_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"world_l2_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"world_l2_boundary_{field}_mismatch")

    policy = mapping(plan.get("analytic_policy"))
    _positive_int(policy, ("minimum_coordinate_count", "maximum_coordinate_count"), blockers)
    if (
        isinstance(policy.get("minimum_coordinate_count"), int)
        and isinstance(policy.get("maximum_coordinate_count"), int)
        and policy["minimum_coordinate_count"] > policy["maximum_coordinate_count"]
    ):
        blockers.append("world_l2_coordinate_count_order_invalid")
    _bounded_nonnegative(
        policy,
        (
            "maximum_absolute_coordinate",
            "minimum_coercivity_lower_bound",
            "maximum_norm_squared",
            "maximum_weighted_energy",
            "numeric_tolerance",
        ),
        blockers,
    )
    required_kinds = policy.get("required_source_kinds")
    if not isinstance(required_kinds, list) or set(required_kinds) != set(SOURCE_KIND_FIELDS):
        blockers.append("world_l2_required_source_kinds_invalid")
    for field in (
        "require_full_source_coverage",
        "require_unique_basis_ids",
        "require_unique_source_coordinates",
        "require_finite_support_witness",
        "require_positive_diagonal_weights",
        "require_declared_observables_match",
        "require_projection_roles",
        "require_projection_contractive",
        "require_dense_core_template",
        "forbid_self_adjointness_runtime_claim",
        "forbid_unbounded_operator_execution",
    ):
        if policy.get(field) is not True:
            blockers.append(f"world_l2_policy_{field}_not_true")


def collect_world_entities(world: Mapping[str, Any]) -> dict[str, set[str]]:
    output: dict[str, set[str]] = {}
    for source_kind, (collection_field, id_field) in SOURCE_KIND_FIELDS.items():
        identifiers = {
            str(mapping(value).get(id_field, ""))
            for value in items(world.get(collection_field))
            if str(mapping(value).get(id_field, ""))
        }
        output[source_kind] = identifiers
    return output


def validate_source_world(
    world: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION:
        blockers.append("world_l2_source_world_version_invalid")
    if not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("world_l2_source_world_digest_invalid")
    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    if plan.get("expected_source_world_state_digest") != world_digest:
        blockers.append("world_l2_expected_world_digest_mismatch")
    if plan.get("world_model_id") != world.get("world_model_id"):
        blockers.append("world_l2_world_model_id_mismatch")
    if world.get("build_status") != "indra_qi_world_model_ready":
        blockers.append("world_l2_source_world_not_ready")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True:
        blockers.append("world_l2_multi_world_noncollapse_missing")
    if mandala.get("single_ontology_forced") is not False:
        blockers.append("world_l2_single_ontology_forced")
    two_truths = mapping(world.get("two_truths_boundary"))
    if two_truths.get("two_truths_gap_preserved") is not True:
        blockers.append("world_l2_two_truths_gap_missing")
    return {
        "world_digest": world_digest,
        "world_model_id": str(world.get("world_model_id", "")),
        "entities": collect_world_entities(world),
    }


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    report: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_world_l2_spine_plan_digest": str(plan.get("world_l2_spine_plan_digest", "")),
        "bound_world_l2_embedding_report_digest": str(report.get("world_l2_embedding_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"world_l2_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("world_l2_license_id_missing")
    for field in (
        "state_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"world_l2_license_{field}_not_true")
    for field in (
        "world_update_authority_granted",
        "external_actuation_authority_granted",
        "truth_authority_granted",
        "unbounded_operator_execution_authority_granted",
        "self_adjointness_theorem_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"world_l2_license_{field}_not_false")
