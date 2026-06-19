from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_adaptive_agent_reference_types_v1_0 import (
    IMPLEMENTATION_REFINEMENT_MAP,
    PLANES,
    require_string,
)

MEGAMODEL_VERSION = "kuuos_runtime_megamodel_v1_0"

MODEL_KINDS = (
    "MISSION",
    "BELIEF",
    "DECISION",
    "PLAN",
    "AUTHORITY",
    "CAPABILITY_EPOCH",
    "LEASE",
    "SESSION",
    "EVIDENCE",
    "VERIFICATION",
    "LEARNING",
    "RECOVERY",
)

REQUIRED_RELATIONS = (
    ("BELIEF", "SUPPORTS", "DECISION"),
    ("DECISION", "JUSTIFIES", "PLAN"),
    ("AUTHORITY", "CONSTRAINS", "PLAN"),
    ("CAPABILITY_EPOCH", "REALIZES", "AUTHORITY"),
    ("LEASE", "SCOPES", "CAPABILITY_EPOCH"),
    ("SESSION", "CONSUMES", "LEASE"),
    ("EVIDENCE", "OBSERVES", "SESSION"),
    ("VERIFICATION", "EVALUATES", "EVIDENCE"),
    ("LEARNING", "UPDATES_FUTURE_ONLY", "PLAN"),
    ("RECOVERY", "RESOLVES", "SESSION"),
    ("RECOVERY", "REQUIRES_FRESH", "CAPABILITY_EPOCH"),
)


def build_runtime_megamodel(*, model_digests: Mapping[str, str]) -> dict[str, Any]:
    if set(model_digests) != set(MODEL_KINDS):
        raise ValueError("megamodel_inventory_incomplete")
    models = {
        kind: {
            "kind": kind,
            "digest": require_string(model_digests[kind], f"{kind}_digest"),
        }
        for kind in MODEL_KINDS
    }
    relations = [
        {"source": source, "relation": relation, "target": target}
        for source, relation, target in REQUIRED_RELATIONS
    ]
    value = {
        "version": MEGAMODEL_VERSION,
        "models": models,
        "relations": relations,
        "implementation_refinement_map": deepcopy(IMPLEMENTATION_REFINEMENT_MAP),
        "relation_count": len(relations),
        "model_count": len(models),
        "runtime_megamodel_digest": "",
    }
    value["runtime_megamodel_digest"] = megamodel_digest(value)
    errors = validate_runtime_megamodel(value)
    if errors:
        raise ValueError("runtime_megamodel_invalid:" + ";".join(errors))
    return value


def megamodel_digest(value: Mapping[str, Any]) -> str:
    packet = dict(value)
    packet.pop("runtime_megamodel_digest", None)
    return sha(packet)


def validate_runtime_megamodel(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != MEGAMODEL_VERSION:
            errors.append("megamodel_version_invalid")
        if value.get("runtime_megamodel_digest") != megamodel_digest(value):
            errors.append("megamodel_digest_invalid")
        models = dict(value.get("models", {}))
        if set(models) != set(MODEL_KINDS):
            errors.append("megamodel_models_invalid")
        for kind, model in models.items():
            if model.get("kind") != kind:
                errors.append("megamodel_kind_mismatch")
            require_string(model.get("digest"), f"{kind}_digest")
        relations = list(value.get("relations", []))
        triples = {
            (item.get("source"), item.get("relation"), item.get("target"))
            for item in relations
            if isinstance(item, dict)
        }
        if triples != set(REQUIRED_RELATIONS):
            errors.append("megamodel_relations_invalid")
        for source, _, target in triples:
            if source not in models or target not in models:
                errors.append("megamodel_relation_endpoint_missing")
        if value.get("model_count") != len(MODEL_KINDS):
            errors.append("megamodel_model_count_invalid")
        if value.get("relation_count") != len(REQUIRED_RELATIONS):
            errors.append("megamodel_relation_count_invalid")
        mapping = dict(value.get("implementation_refinement_map", {}))
        if mapping != IMPLEMENTATION_REFINEMENT_MAP:
            errors.append("megamodel_refinement_map_invalid")
        if any(plane not in PLANES for plane in mapping.values()):
            errors.append("megamodel_refinement_plane_invalid")
        for index in range(1, 18):
            if f"PlanOS_v0_{index}" not in mapping:
                errors.append("megamodel_planos_coverage_incomplete")
                break
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
