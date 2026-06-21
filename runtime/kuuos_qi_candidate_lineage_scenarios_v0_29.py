from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_candidate_lineage_entry_v0_29 import build_candidate_lineage
from runtime.kuuos_qi_candidate_lineage_fixtures_v0_29 import (
    make_packet,
    make_report,
    with_mode,
)
from runtime.kuuos_qi_candidate_lineage_ledger_v0_29 import CandidateLineageLedger
from runtime.kuuos_qi_candidate_lineage_state_fixture_v0_29 import make_source_state


def run_candidate_lineage_scenarios() -> dict:
    state = make_source_state()

    visible_packet = make_packet(state, "visible")
    visible_report = make_report(
        visible_packet,
        "visible",
        route="EVALUATE_RECOVERY_WINDOW",
        classification="HEALING_POTENTIAL_VISIBLE",
    )
    visible = build_candidate_lineage(
        binding_id="binding-visible",
        state=state,
        packet=visible_packet,
        report=visible_report,
        bound_at_ms=10_000,
    )
    assert visible["body"]["review_route"] == "HOLD"
    assert visible["body"]["route_activates_plan"] is False
    assert visible["body"]["route_invokes_actos"] is False
    assert len(visible["body"]["candidate_set"]) == 2

    insufficient_packet = make_packet(state, "insufficient")
    insufficient_report = make_report(
        insufficient_packet,
        "insufficient",
        route="REOBSERVE",
        classification="INSUFFICIENT_EVIDENCE",
    )
    insufficient = build_candidate_lineage(
        binding_id="binding-insufficient",
        state=state,
        packet=insufficient_packet,
        report=insufficient_report,
        bound_at_ms=10_100,
    )
    assert insufficient["body"]["review_route"] == "REOBSERVE"

    review_packet = make_packet(state, "review")
    review_report = make_report(
        review_packet,
        "review",
        route="CLINICIAN_REVIEW_HANDOFF",
        classification="CLINICIAN_REVIEW_REQUIRED",
        red_flags=["review-surface"],
    )
    review = build_candidate_lineage(
        binding_id="binding-review",
        state=state,
        packet=review_packet,
        report=review_report,
        bound_at_ms=10_200,
    )
    assert review["body"]["review_route"] == "REVIEW"

    terminated_state = with_mode(state, "TERMINATED")
    terminated_packet = make_packet(terminated_state, "terminated")
    terminated_report = make_report(
        terminated_packet,
        "terminated",
        route="HOLD",
        classification="HEALING_POTENTIAL_CONSTRAINED",
    )
    terminated = build_candidate_lineage(
        binding_id="binding-terminated",
        state=terminated_state,
        packet=terminated_packet,
        report=terminated_report,
        bound_at_ms=10_300,
    )
    assert terminated["body"]["review_route"] == "TERMINATE"

    handover_state = with_mode(state, "HANDED_OVER")
    handover_packet = make_packet(handover_state, "handover")
    handover_report = make_report(
        handover_packet,
        "handover",
        route="HOLD",
        classification="HEALING_POTENTIAL_UNCERTAIN",
    )
    handover = build_candidate_lineage(
        binding_id="binding-handover",
        state=handover_state,
        packet=handover_packet,
        report=handover_report,
        bound_at_ms=10_400,
    )
    assert handover["body"]["review_route"] == "HANDOVER"

    substituted = deepcopy(visible_packet)
    substituted["source_v027_state_digest"] = sha("other-state")
    packet_body = dict(substituted)
    packet_body.pop("diagnostic_packet_digest")
    substituted["diagnostic_packet_digest"] = sha(packet_body)
    substituted_report = make_report(
        substituted,
        "substituted",
        route="HOLD",
        classification="HEALING_POTENTIAL_UNCERTAIN",
    )
    try:
        build_candidate_lineage(
            binding_id="binding-substituted",
            state=state,
            packet=substituted,
            report=substituted_report,
            bound_at_ms=10_500,
        )
    except ValueError:
        substitution_rejected = True
    else:
        substitution_rejected = False
    assert substitution_rejected is True

    tampered_report = deepcopy(visible_report)
    tampered_report["diagnostic_hypothesis_summary"]["plural_hypotheses"][0][
        "support"
    ] = 1.0
    try:
        build_candidate_lineage(
            binding_id="binding-tampered",
            state=state,
            packet=visible_packet,
            report=tampered_report,
            bound_at_ms=10_600,
        )
    except ValueError:
        tamper_rejected = True
    else:
        tamper_rejected = False
    assert tamper_rejected is True

    with TemporaryDirectory(prefix="kuuos-lineage-v029-") as temporary:
        ledger = CandidateLineageLedger(Path(temporary))
        first = ledger.append(visible)
        replay = ledger.append(visible)
        second = ledger.append(insufficient)
        alternate_report = make_report(
            visible_packet,
            "visible-alternate",
            route="PRESERVE_PLURAL_HYPOTHESES",
            classification="HEALING_POTENTIAL_UNCERTAIN",
        )
        alternate = build_candidate_lineage(
            binding_id="binding-visible-alternate",
            state=state,
            packet=visible_packet,
            report=alternate_report,
            bound_at_ms=10_700,
        )
        try:
            ledger.append(alternate)
        except ValueError:
            packet_reuse_rejected = True
        else:
            packet_reuse_rejected = False
        assert first["status"] == "APPENDED"
        assert replay["status"] == "REPLAYED"
        assert second["ledger_count"] == 2
        assert packet_reuse_rejected is True

    return {
        "status": "KUUOS_QI_CANDIDATE_LINEAGE_V0_29_OK",
        "visible_route": visible["body"]["review_route"],
        "insufficient_route": insufficient["body"]["review_route"],
        "review_route": review["body"]["review_route"],
        "terminated_route": terminated["body"]["review_route"],
        "handover_route": handover["body"]["review_route"],
        "substitution_rejected": substitution_rejected,
        "tamper_rejected": tamper_rejected,
        "packet_reuse_rejected": packet_reuse_rejected,
        "replay_status": replay["status"],
    }


__all__ = ["run_candidate_lineage_scenarios"]
