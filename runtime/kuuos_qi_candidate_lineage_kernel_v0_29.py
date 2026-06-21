from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_envelope_v0_29 import make_envelope
from runtime.kuuos_qi_candidate_lineage_match_all_v0_29 import all_sources_match
from runtime.kuuos_qi_candidate_lineage_record_v0_29 import make_lineage_record
from runtime.kuuos_qi_candidate_lineage_routing_v0_29 import derive_review_route
from runtime.kuuos_qi_candidate_lineage_snapshot_v0_29 import make_source_snapshot
from runtime.kuuos_qi_candidate_lineage_sources_v0_29 import validate_sources


def build_candidate_lineage(
    *,
    binding_id: str,
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    report: Mapping[str, Any],
    bound_at_ms: int,
) -> dict[str, Any]:
    errors, fields = validate_sources(state, packet, report)
    snapshot = make_source_snapshot(
        state,
        packet,
        report,
        fields["packet_digest"],
        fields["report_digest"],
        fields["summary"],
        fields["potential"],
    )
    if not all_sources_match(snapshot["packet_digest"], state, packet, report):
        errors.append("source_lineage_mismatch")
    if errors:
        raise ValueError("candidate_lineage_invalid:" + ";".join(errors))
    classification = str(snapshot["potential"].get("classification", ""))
    route, reasons = derive_review_route(
        str(state["mode"]),
        str(report["route"]),
        classification,
        bool(report.get("red_flags", [])),
    )
    record = make_lineage_record(
        binding_id=binding_id,
        state=state,
        packet=packet,
        snapshot=snapshot,
        route=route,
        reasons=reasons,
        bound_at_ms=bound_at_ms,
    )
    return make_envelope(record)


__all__ = ["build_candidate_lineage"]
