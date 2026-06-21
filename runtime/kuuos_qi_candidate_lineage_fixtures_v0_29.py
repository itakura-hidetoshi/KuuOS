from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import state_digest


def make_packet(state: Mapping[str, Any], label: str) -> dict[str, Any]:
    value = {
        "version": "kuuos_qi_healing_potential_diagnostic_packet_v0_28",
        "packet_id": f"packet-{label}",
        "source_v027_state_digest": state["integrated_operation_state_digest"],
        "candidate_only": True,
        "diagnostic_packet_digest": "",
    }
    body = dict(value)
    body.pop("diagnostic_packet_digest")
    value["diagnostic_packet_digest"] = sha(body)
    return value


def make_report(
    packet: Mapping[str, Any],
    label: str,
    *,
    route: str,
    classification: str,
    red_flags: list[str] | None = None,
) -> dict[str, Any]:
    value = {
        "version": "kuuos_qi_healing_potential_diagnostic_report_v0_28",
        "packet_id": packet["packet_id"],
        "source_packet_digest": packet["diagnostic_packet_digest"],
        "diagnostic_hypothesis_summary": {
            "plural_hypotheses": [
                {
                    "hypothesis_id": f"{label}-a",
                    "support": 0.70,
                    "counterevidence": 0.20,
                    "uncertainty": 0.25,
                    "candidate_only": True,
                },
                {
                    "hypothesis_id": f"{label}-b",
                    "support": 0.45,
                    "counterevidence": 0.30,
                    "uncertainty": 0.40,
                    "candidate_only": True,
                },
            ],
            "leading_hypothesis_id": f"{label}-a",
            "leading_hypothesis_is_truth": False,
            "single_winner_forced": False,
        },
        "healing_potential": {
            "classification": classification,
            "interval_lower": 0.30,
            "interval_center": 0.50,
            "interval_upper": 0.70,
        },
        "red_flags": list(red_flags or []),
        "route": route,
        "route_is_clinical_instruction": False,
        "treatment_route_generated": False,
        "candidate_only": True,
        "source_history_preserved": True,
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "diagnostic_report_digest": "",
    }
    body = deepcopy(value)
    body.pop("diagnostic_report_digest")
    value["diagnostic_report_digest"] = sha(body)
    return value


def with_mode(state: Mapping[str, Any], mode: str) -> dict[str, Any]:
    value = deepcopy(dict(state))
    value["mode"] = mode
    value["integrated_operation_state_digest"] = state_digest(value)
    return value


__all__ = ["make_packet", "make_report", "with_mode"]
