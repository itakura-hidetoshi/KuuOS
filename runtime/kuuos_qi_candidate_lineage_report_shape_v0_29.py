from __future__ import annotations

from typing import Any, Mapping


def _mapping_with_key(
    report: Mapping[str, Any], key: str, name: str
) -> tuple[str, Mapping[str, Any]]:
    matches = [
        (field, value)
        for field, value in report.items()
        if isinstance(value, Mapping) and key in value
    ]
    if len(matches) != 1:
        raise ValueError(f"{name}_unique_mapping_required")
    return matches[0]


def validate_report_shape(
    report: Mapping[str, Any],
) -> tuple[list[str], str, str]:
    errors: list[str] = []
    summary_field = ""
    potential_field = ""
    try:
        summary_field, summary = _mapping_with_key(
            report, "plural_hypotheses", "source_v028_candidate_summary"
        )
        candidates = summary.get("plural_hypotheses")
        if not isinstance(candidates, list) or not candidates:
            errors.append("source_v028_plural_candidates_required")
        if summary.get("leading_hypothesis_is_truth") is not False:
            errors.append("source_v028_truth_promotion_forbidden")
        if summary.get("single_winner_forced") is not False:
            errors.append("source_v028_single_winner_forbidden")
        potential_field, potential = _mapping_with_key(
            report, "classification", "source_v028_potential"
        )
        if not isinstance(potential.get("classification"), str):
            errors.append("source_v028_classification_required")
        for field in (
            "source_history_preserved",
            "counterevidence_preserved",
            "uncertainty_preserved",
        ):
            if report.get(field) is not True:
                errors.append(f"source_v028_{field}_required")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors, summary_field, potential_field


__all__ = ["validate_report_shape"]
