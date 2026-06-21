from __future__ import annotations


def derive_review_route(
    source_mode: str,
    lower_route: str,
    source_classification: str,
    red_flags_visible: bool,
) -> tuple[str, list[str]]:
    if source_mode == "TERMINATED":
        return "TERMINATE", ["v027_source_state_terminated"]
    if source_mode == "HANDED_OVER":
        return "HANDOVER", ["v027_source_state_handed_over"]
    if source_mode in {"PAUSED", "RENEWAL_REQUIRED"}:
        return "HOLD", [f"v027_source_state_{source_mode.lower()}"]
    if red_flags_visible or lower_route.endswith("REVIEW_HANDOFF"):
        return "REVIEW", ["v028_external_review_required"]
    if lower_route == "REOBSERVE" or source_classification == "INSUFFICIENT_EVIDENCE":
        return "REOBSERVE", ["v028_reobservation_required"]
    if lower_route == "HOLD":
        return "HOLD", ["v028_current_window_constrained"]
    return "HOLD", ["candidate_review_only_no_action_activation"]


__all__ = ["derive_review_route"]
