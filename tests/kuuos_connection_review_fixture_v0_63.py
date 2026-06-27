from __future__ import annotations

from runtime.kuuos_connection_admission_types_v0_63 import ADMIT
from runtime.kuuos_connection_admission_v0_63 import build_connection_admission_request, seal_supervisor_admission_license
from runtime.kuuos_connection_candidate_search_v0_62 import search_connection_candidates
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture


def review_fixture(decision: str = ADMIT):
    bundle, _, _ = fixture()
    identity = bundle.group.identity()
    proposal = search_connection_candidates(bundle, {
        ("observe", "verify"): [identity],
        ("verify", "memory"): [identity],
    })
    request = build_connection_admission_request(
        proposal,
        request_id="connection-review-request-v063",
        requested_by="KuuOSGaugeCandidateReview",
    )
    license_packet = seal_supervisor_admission_license(
        request,
        license_id="connection-review-license-v063",
        supervisor_id="external-supervisor-v063",
        decision=decision,
        valid_from_epoch=10,
        valid_through_epoch=20,
    )
    return proposal, request, license_packet
