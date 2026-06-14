#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import re
from typing import Any, Mapping

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,127}$")


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def model_digest(state: Mapping[str, Any]) -> str:
    return sha(without(state, "world_model_digest"))


def command_digest(command: Mapping[str, Any]) -> str:
    return sha(without(command, "command_digest"))


def valid_name(value: str) -> bool:
    return bool(NAME_RE.fullmatch(value))


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def normalize_variable(value: Mapping[str, Any], status: str = "observed") -> dict[str, Any]:
    raw = value.get("value")
    if isinstance(raw, bool) or not isinstance(raw, (int, float, str, type(None))):
        raw = None
    uncertainty = max(number(value.get("uncertainty")), 0.0)
    provenance = value.get("provenance", [])
    return {
        "value": raw,
        "uncertainty": uncertainty,
        "status": str(value.get("status", status)),
        "unit": str(value.get("unit", "")),
        "provenance": list(provenance) if isinstance(provenance, list) else [],
    }


def validate_graph(
    variables: Mapping[str, Any], mechanisms: Mapping[str, Any], blockers: list[str]
) -> list[str]:
    indegree = {str(name): 0 for name in variables}
    children = {str(name): [] for name in variables}
    for target, raw in mechanisms.items():
        target = str(target)
        mechanism = raw if isinstance(raw, Mapping) else {}
        if target not in variables:
            blockers.append("causal_mechanism_target_missing")
            continue
        if mechanism.get("type") != "affine":
            blockers.append("causal_mechanism_type_not_allowed")
        parents_raw = mechanism.get("parents", [])
        parents = [str(value) for value in parents_raw] if isinstance(parents_raw, list) else []
        weights = mechanism.get("weights", {}) if isinstance(mechanism.get("weights"), Mapping) else {}
        if not parents or len(set(parents)) != len(parents):
            blockers.append("causal_mechanism_parents_invalid")
        for parent in parents:
            if parent not in variables:
                blockers.append("causal_mechanism_parent_missing")
                continue
            if parent == target:
                blockers.append("causal_mechanism_self_cycle")
            weight = weights.get(parent)
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                blockers.append("causal_mechanism_weight_invalid")
            children[parent].append(target)
            indegree[target] += 1
        if set(str(key) for key in weights) != set(parents):
            blockers.append("causal_mechanism_weight_parent_mismatch")
        for key in ("bias", "noise"):
            value = mechanism.get(key, 0.0)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                blockers.append(f"causal_mechanism_{key}_invalid")
        if number(mechanism.get("noise")) < 0:
            blockers.append("causal_mechanism_noise_negative")

    queue = sorted(name for name, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(order) != len(variables):
        blockers.append("causal_graph_cycle_detected")
    return order


def propagate(state: dict[str, Any], blockers: list[str]) -> None:
    variables = state.get("variables", {})
    mechanisms = state.get("mechanisms", {})
    if not isinstance(variables, dict) or not isinstance(mechanisms, dict):
        blockers.append("causal_world_model_structure_invalid")
        return
    order = validate_graph(variables, mechanisms, blockers)
    if blockers:
        return
    active = set(str(key) for key in state.get("active_interventions", {}))
    for target in order:
        if target in active or target not in mechanisms:
            continue
        mechanism = mechanisms[target]
        value = number(mechanism.get("bias"))
        variance = number(mechanism.get("noise")) ** 2
        trace: dict[str, str] = {}
        for parent in mechanism.get("parents", []):
            entry = variables[parent]
            parent_value = entry.get("value")
            if isinstance(parent_value, bool) or not isinstance(parent_value, (int, float)):
                blockers.append("causal_parent_value_not_numeric")
                return
            weight = number(mechanism["weights"].get(parent))
            value += weight * float(parent_value)
            variance += (weight * number(entry.get("uncertainty"))) ** 2
            trace[parent] = sha(entry)
        entry = dict(variables[target])
        entry.update(
            {
                "value": value,
                "uncertainty": math.sqrt(max(variance, 0.0)),
                "status": "derived",
                "derived_from": trace,
            }
        )
        variables[target] = entry
    state["graph_digest"] = sha({"variables": sorted(variables), "mechanisms": mechanisms})


def apply_observation(
    state: Mapping[str, Any], values: Mapping[str, Any], uncertainties: Mapping[str, Any], release: set[str],
    transaction_id: str, blockers: list[str]
) -> dict[str, Any]:
    out = deepcopy(dict(state))
    active = dict(out.get("active_interventions", {}))
    for name in release:
        active.pop(name, None)
    out["active_interventions"] = active
    for name, raw in values.items():
        if name not in out["variables"]:
            blockers.append("causal_observation_variable_missing")
            continue
        if isinstance(raw, bool) or not isinstance(raw, (int, float, str, type(None))):
            blockers.append("causal_observation_value_invalid")
            continue
        entry = dict(out["variables"][name])
        entry.update(
            {
                "value": raw,
                "uncertainty": max(number(uncertainties.get(name), number(entry.get("uncertainty"))), 0.0),
                "status": "observed",
                "provenance": list(entry.get("provenance", [])) + [transaction_id],
            }
        )
        out["variables"][name] = entry
    if not blockers:
        propagate(out, blockers)
    return out


def apply_intervention(
    state: Mapping[str, Any], values: Mapping[str, Any], uncertainties: Mapping[str, Any], release: set[str],
    transaction_id: str, blockers: list[str], projection_only: bool = False
) -> dict[str, Any]:
    out = deepcopy(dict(state))
    active = dict(out.get("active_interventions", {}))
    for name in release:
        active.pop(name, None)
    for name, raw in values.items():
        if name not in out["variables"]:
            blockers.append("causal_intervention_variable_missing")
            continue
        if isinstance(raw, bool) or not isinstance(raw, (int, float, str, type(None))):
            blockers.append("causal_intervention_value_invalid")
            continue
        uncertainty = max(number(uncertainties.get(name)), 0.0)
        active[name] = {
            "value": raw,
            "uncertainty": uncertainty,
            "transaction_id": transaction_id,
            "projection_only": projection_only,
        }
        entry = dict(out["variables"][name])
        entry.update(
            {
                "value": raw,
                "uncertainty": uncertainty,
                "status": "counterfactual_intervened" if projection_only else "intervened",
                "provenance": list(entry.get("provenance", [])) + [transaction_id],
            }
        )
        out["variables"][name] = entry
    out["active_interventions"] = active
    if not blockers:
        propagate(out, blockers)
    return out


def variable_deltas(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    old = before.get("variables", {}) if isinstance(before.get("variables"), Mapping) else {}
    new = after.get("variables", {}) if isinstance(after.get("variables"), Mapping) else {}
    result: dict[str, Any] = {}
    for name in sorted(set(old) | set(new)):
        if old.get(name) != new.get(name):
            result[name] = {"before": deepcopy(old.get(name)), "after": deepcopy(new.get(name))}
    return result
