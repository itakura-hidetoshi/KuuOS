from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import IntEnum
from typing import Any, Mapping

VERSION = "kuuos_adaptive_retrieval_policy_v0_1"
RECEIPT_VERSION = "kuuos_adaptive_retrieval_receipt_v0_1"


class RetrievalMode(IntEnum):
    LEXICAL = 0
    LEXICAL_REWRITE = 1
    SEMANTIC_ON_DEMAND = 2
    HYBRID = 3
    PREEMBEDDED = 4
    GRAPH_RELATIONAL = 5


MODE_NAMES = tuple(mode.name for mode in RetrievalMode)
AUTHORITY_FIELDS = (
    "truth_authority_granted",
    "world_commit_authority_granted",
    "belief_authority_granted",
    "decision_authority_granted",
    "execution_authority_granted",
    "clinical_authority_granted",
    "theorem_authority_granted",
)


@dataclass(frozen=True)
class RetrievalContext:
    query_id: str
    freshness_requirement: str
    corpus_churn: str
    query_pattern: str
    request_scale: str
    latency_cost_budget: str
    operational_capability: str
    provenance_requirement: str

    def validate(self) -> None:
        values = asdict(self)
        for key, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key} must be a non-empty string")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_payload(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _normalize_assessments(assessments: Mapping[str, bool]) -> dict[str, bool]:
    keys = set(assessments)
    expected = set(MODE_NAMES)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise ValueError(
            "adequacy assessments must cover every retrieval mode exactly; "
            f"missing={missing}, extra={extra}"
        )
    normalized: dict[str, bool] = {}
    for name in MODE_NAMES:
        value = assessments[name]
        if type(value) is not bool:
            raise ValueError(f"assessment for {name} must be bool")
        normalized[name] = value
    return normalized


def _normalize_reasons(reasons: Mapping[str, str] | None) -> dict[str, str]:
    if reasons is None:
        return {name: "explicit adequacy assessment supplied" for name in MODE_NAMES}
    keys = set(reasons)
    expected = set(MODE_NAMES)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise ValueError(
            "assessment reasons must cover every retrieval mode exactly; "
            f"missing={missing}, extra={extra}"
        )
    normalized: dict[str, str] = {}
    for name in MODE_NAMES:
        value = reasons[name]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"reason for {name} must be a non-empty string")
        normalized[name] = value.strip()
    return normalized


def select_least_sufficient(
    context: RetrievalContext,
    assessments: Mapping[str, bool],
    reasons: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Select the least-complex explicitly adequate mode.

    This function is effect-free. It does not perform retrieval and it does not
    infer adequacy from built-in churn, scale, freshness, or latency thresholds.
    """

    context.validate()
    normalized = _normalize_assessments(assessments)
    normalized_reasons = _normalize_reasons(reasons)

    selected: RetrievalMode | None = None
    for mode in RetrievalMode:
        if normalized[mode.name]:
            selected = mode
            break

    assessed = [
        {
            "rank": int(mode),
            "mode": mode.name,
            "adequate": normalized[mode.name],
            "reason": normalized_reasons[mode.name],
        }
        for mode in RetrievalMode
    ]

    context_payload = asdict(context)
    assessment_payload = {
        "context": context_payload,
        "assessments": assessed,
    }

    if selected is None:
        route = "NO_DATA"
        selected_mode = None
        selected_rank = None
        next_observation_target = (
            "obtain new evidence or revise explicit adequacy assessments; "
            "do not silently escalate retrieval complexity"
        )
    else:
        route = "CANDIDATE"
        selected_mode = selected.name
        selected_rank = int(selected)
        next_observation_target = None

    receipt: dict[str, Any] = {
        "version": RECEIPT_VERSION,
        "policy_version": VERSION,
        "query_id": context.query_id,
        "route": route,
        "selected_mode": selected_mode,
        "selected_rank": selected_rank,
        "context": context_payload,
        "assessments": assessed,
        "assessment_digest": digest_payload(assessment_payload),
        "least_sufficient": selected is not None,
        "all_modes_explicitly_assessed": True,
        "graph_relational_is_default": False,
        "hardcoded_engineering_thresholds_used": False,
        "next_observation_target": next_observation_target,
        "truth_authority_granted": False,
        "world_commit_authority_granted": False,
        "belief_authority_granted": False,
        "decision_authority_granted": False,
        "execution_authority_granted": False,
        "clinical_authority_granted": False,
        "theorem_authority_granted": False,
    }
    receipt["receipt_digest"] = digest_payload(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    validate_receipt(receipt)
    return receipt


def validate_receipt(receipt: Mapping[str, Any]) -> None:
    if receipt.get("version") != RECEIPT_VERSION:
        raise ValueError("unexpected receipt version")
    if receipt.get("policy_version") != VERSION:
        raise ValueError("unexpected policy version")
    if receipt.get("all_modes_explicitly_assessed") is not True:
        raise ValueError("receipt must record complete adequacy assessment")
    if receipt.get("graph_relational_is_default") is not False:
        raise ValueError("GraphRAG/relational retrieval cannot be the default")
    if receipt.get("hardcoded_engineering_thresholds_used") is not False:
        raise ValueError("selector must not hard-code calibration heuristics")
    for field in AUTHORITY_FIELDS:
        if receipt.get(field) is not False:
            raise ValueError(f"retrieval receipt cannot grant {field}")

    rows = receipt.get("assessments")
    if not isinstance(rows, list) or len(rows) != len(RetrievalMode):
        raise ValueError("receipt must retain one assessment per retrieval mode")

    adequacy: dict[str, bool] = {}
    for expected_mode, row in zip(RetrievalMode, rows, strict=True):
        if not isinstance(row, Mapping):
            raise ValueError("assessment rows must be mappings")
        if row.get("mode") != expected_mode.name or row.get("rank") != int(expected_mode):
            raise ValueError("assessment order/rank mismatch")
        if type(row.get("adequate")) is not bool:
            raise ValueError("assessment adequacy must be bool")
        adequacy[expected_mode.name] = row["adequate"]

    selected_name = receipt.get("selected_mode")
    route = receipt.get("route")
    if selected_name is None:
        if route != "NO_DATA" or any(adequacy.values()):
            raise ValueError("NO_DATA requires all modes explicitly inadequate")
        if receipt.get("least_sufficient") is not False:
            raise ValueError("NO_DATA cannot claim a selected least-sufficient mode")
    else:
        try:
            selected = RetrievalMode[selected_name]
        except (KeyError, TypeError) as exc:
            raise ValueError("unknown selected retrieval mode") from exc
        if route != "CANDIDATE":
            raise ValueError("selected retrieval mode requires CANDIDATE route")
        if receipt.get("selected_rank") != int(selected):
            raise ValueError("selected rank mismatch")
        if not adequacy[selected.name]:
            raise ValueError("selected mode must be adequate")
        for mode in RetrievalMode:
            if int(mode) < int(selected) and adequacy[mode.name]:
                raise ValueError("selected mode is not least-sufficient")

    expected_digest = digest_payload(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    if receipt.get("receipt_digest") != expected_digest:
        raise ValueError("receipt digest mismatch")


def example_context(query_id: str = "example-query") -> RetrievalContext:
    return RetrievalContext(
        query_id=query_id,
        freshness_requirement="deployment-declared",
        corpus_churn="deployment-measured",
        query_pattern="query-specific",
        request_scale="deployment-measured",
        latency_cost_budget="deployment-declared",
        operational_capability="deployment-declared",
        provenance_requirement="explicit",
    )
