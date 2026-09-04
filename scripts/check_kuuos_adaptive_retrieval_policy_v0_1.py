#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_adaptive_retrieval_policy_v0_1 import (
    MODE_NAMES,
    RetrievalMode,
    example_context,
    select_least_sufficient,
    validate_receipt,
)


def assessments(**adequate: bool) -> dict[str, bool]:
    result = {name: False for name in MODE_NAMES}
    for name, value in adequate.items():
        result[name] = value
    return result


def main() -> None:
    context = example_context("adaptive-retrieval-check")

    lexical = select_least_sufficient(
        context,
        assessments(LEXICAL=True, GRAPH_RELATIONAL=True),
    )
    assert lexical["selected_mode"] == RetrievalMode.LEXICAL.name
    assert lexical["route"] == "CANDIDATE"

    hybrid = select_least_sufficient(
        context,
        assessments(HYBRID=True, GRAPH_RELATIONAL=True),
    )
    assert hybrid["selected_mode"] == RetrievalMode.HYBRID.name

    graph = select_least_sufficient(
        context,
        assessments(GRAPH_RELATIONAL=True),
    )
    assert graph["selected_mode"] == RetrievalMode.GRAPH_RELATIONAL.name
    assert all(
        not row["adequate"]
        for row in graph["assessments"]
        if row["rank"] < int(RetrievalMode.GRAPH_RELATIONAL)
    )

    no_data = select_least_sufficient(context, assessments())
    assert no_data["route"] == "NO_DATA"
    assert no_data["selected_mode"] is None
    assert no_data["next_observation_target"]

    try:
        select_least_sufficient(context, {"LEXICAL": True})
    except ValueError:
        pass
    else:
        raise AssertionError("partial adequacy assessment must fail closed")

    tampered = deepcopy(lexical)
    tampered["truth_authority_granted"] = True
    try:
        validate_receipt(tampered)
    except ValueError:
        pass
    else:
        raise AssertionError("authority escalation must be rejected")

    print(
        {
            "status": "ok",
            "policy": "kuuos_adaptive_retrieval_policy_v0_1",
            "least_sufficient": True,
            "graph_not_default": True,
            "no_data_fail_closed": True,
            "authority_granted": False,
        }
    )


if __name__ == "__main__":
    main()
