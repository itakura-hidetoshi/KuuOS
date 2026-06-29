from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_fixture_v0_1 import host_inputs
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    authority_packet_digest,
)
from runtime.kuuos_qi_world_successor_cycle_materialization_v2_0 import (
    build_successor_cycle_materialization_receipt,
    materialization_receipt_digest,
    second_cycle_receipt_digest,
    successor_blocker_certificate_digest,
    successor_blocker_receipt_digest,
    successor_closure_receipt_digest,
    validate_second_cycle_receipt,
    validate_successor_blocker_receipt,
    validate_successor_closure_receipt,
    validate_successor_cycle_materialization_receipt,
    validate_successor_external_authority,
)


def _host_license() -> dict:
    _, _, host_license, _ = host_inputs(
        job_id="qi-world-v20-job",
        expires_at_ms=480_000,
    )
    return host_license


def _retag_materialization(receipt: dict) -> dict:
    receipt["successor_cycle_materialization_receipt_digest"] = ""
    receipt["successor_cycle_materialization_receipt_digest"] = (
        materialization_receipt_digest(receipt)
    )
    return receipt


def _expect(errors: list[str], expected: str) -> None:
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_successor_cycle_materialization_scenarios() -> dict:
    with tempfile.TemporaryDirectory(
        prefix="kuuos-successor-cycle-v20-"
    ) as temporary:
        receipt = build_successor_cycle_materialization_receipt(
            Path(temporary)
        )
        host_license = _host_license()
        assert (
            validate_successor_cycle_materialization_receipt(
                receipt,
                host_license=host_license,
            )
            == []
        )

        predecessor = receipt["predecessor_cycle_receipt"]
        blocker = receipt["successor_blocker_receipt"]
        handoff = receipt["successor_handoff_receipt"]
        closure = receipt["successor_closure_receipt"]
        second = receipt["second_cycle_receipt"]
        requirement = receipt["successor_authority_requirement"]
        intake = receipt["successor_authority_intake"]
        authority = handoff["external_authority_packet"]
        first_authority = predecessor[
            "source_v17_handoff_receipt"
        ]["external_authority_packet"]

        assert receipt["first_cycle_ordinal"] == 1
        assert receipt["second_cycle_ordinal"] == 2
        assert receipt["cycle_ordinals_strictly_increasing"] is True
        assert authority["external_authority_packet_digest"] != first_authority[
            "external_authority_packet_digest"
        ]
        assert authority["human_approval_receipt_digest"] != first_authority[
            "human_approval_receipt_digest"
        ]
        assert authority["host_license_digest"] != first_authority[
            "host_license_digest"
        ]
        assert handoff["release_consumption_count"] == 1
        assert handoff["effect_recorded"] is True
        assert closure["observation_debt_discharged"] is True
        assert closure["verification_debt_discharged"] is True
        assert closure["replan_debt_discharged"] is True
        assert second["cycle_closed"] is True
        assert second["all_post_effect_blockers_active"] is True
        assert receipt["third_act_started"] is False

        reused_authority = deepcopy(authority)
        reused_authority["external_authority_packet_digest"] = first_authority[
            "external_authority_packet_digest"
        ]
        reused_errors = validate_successor_external_authority(
            reused_authority,
            predecessor_cycle_receipt=predecessor,
            successor_blocker_receipt=blocker,
            host_license=host_license,
            now_ms=290_002,
        )
        _expect(reused_errors, "successor_authority_digest_invalid")
        _expect(reused_errors, "successor_authority_digest_reuse_forbidden")

        self_issued = deepcopy(authority)
        self_issued["self_issued"] = True
        self_issued["external_authority_packet_digest"] = ""
        self_issued["external_authority_packet_digest"] = authority_packet_digest(
            self_issued
        )
        _expect(
            validate_successor_external_authority(
                self_issued,
                predecessor_cycle_receipt=predecessor,
                successor_blocker_receipt=blocker,
                host_license=host_license,
                now_ms=290_002,
            ),
            "successor_authority_self_issue_forbidden",
        )

        blocker_loss = deepcopy(blocker)
        certificate = blocker_loss["blocker_certificate"]
        certificate["composed_blocker_vector"][
            "world_identity_blocker"
        ] = False
        certificate["successor_blocker_certificate_digest"] = ""
        certificate["successor_blocker_certificate_digest"] = (
            successor_blocker_certificate_digest(certificate)
        )
        blocker_loss["successor_blocker_receipt_digest"] = ""
        blocker_loss["successor_blocker_receipt_digest"] = (
            successor_blocker_receipt_digest(blocker_loss)
        )
        _expect(
            validate_successor_blocker_receipt(blocker_loss),
            "successor_blocker_vector_substitution",
        )

        observe_substitution = deepcopy(closure)
        observe_substitution["native_evidence_states"]["ObserveOS"][
            "source_act_state_digest"
        ] = "substituted-second-act"
        observe_substitution[
            "licensed_effect_evidence_closure_receipt_digest"
        ] = ""
        observe_substitution[
            "licensed_effect_evidence_closure_receipt_digest"
        ] = successor_closure_receipt_digest(observe_substitution)
        _expect(
            validate_successor_closure_receipt(
                observe_substitution,
                predecessor_cycle_receipt=predecessor,
                authority_requirement=requirement,
                authority_intake=intake,
                host_license=host_license,
            ),
            "successor_closure_observe_act_mismatch",
        )

        replayed_second = deepcopy(second)
        replayed_second["receipt_consumption_count"] = 1
        replayed_second["second_cycle_receipt_digest"] = ""
        replayed_second["second_cycle_receipt_digest"] = (
            second_cycle_receipt_digest(replayed_second)
        )
        _expect(
            validate_second_cycle_receipt(
                replayed_second,
                predecessor_cycle_receipt=predecessor,
                successor_handoff_receipt=handoff,
                successor_closure_receipt=closure,
            ),
            "second_cycle_receipt_consumption_count_invalid",
        )

        wrong_chain = deepcopy(receipt)
        wrong_chain["two_cycle_chain_digest"] = "substituted-chain"
        _retag_materialization(wrong_chain)
        _expect(
            validate_successor_cycle_materialization_receipt(
                wrong_chain,
                host_license=host_license,
            ),
            "materialization_chain_digest_mismatch",
        )

        inherited = deepcopy(receipt)
        inherited["predecessor_authority_inherited"] = True
        _retag_materialization(inherited)
        _expect(
            validate_successor_cycle_materialization_receipt(
                inherited,
                host_license=host_license,
            ),
            "materialization_predecessor_authority_inherited_invalid",
        )

        third_act = deepcopy(receipt)
        third_act["third_act_started"] = True
        _retag_materialization(third_act)
        _expect(
            validate_successor_cycle_materialization_receipt(
                third_act,
                host_license=host_license,
            ),
            "materialization_third_act_started_invalid",
        )

        return {
            "status": (
                "KUUOS_QI_WORLD_SUCCESSOR_CYCLE_MATERIALIZATION_V2_0_OK"
            ),
            "first_cycle_receipt_digest": predecessor[
                "licensed_cycle_receipt_digest"
            ],
            "second_cycle_receipt_digest": second[
                "second_cycle_receipt_digest"
            ],
            "two_cycle_chain_digest": receipt["two_cycle_chain_digest"],
            "successor_blocker_receipt_digest": blocker[
                "successor_blocker_receipt_digest"
            ],
            "successor_authority_packet_digest": authority[
                "external_authority_packet_digest"
            ],
            "successor_handoff_receipt_digest": handoff[
                "licensed_act_handoff_receipt_digest"
            ],
            "successor_closure_receipt_digest": closure[
                "licensed_effect_evidence_closure_receipt_digest"
            ],
            "first_cycle_ordinal": receipt["first_cycle_ordinal"],
            "second_cycle_ordinal": receipt["second_cycle_ordinal"],
            "second_act_materialized": receipt["second_act_materialized"],
            "second_cycle_closed": receipt["second_cycle_closed"],
            "all_second_post_effect_blockers_active": receipt[
                "all_second_post_effect_blockers_active"
            ],
            "third_act_started": receipt["third_act_started"],
            "indra_transport_still_unrealized": receipt[
                "indra_transport_still_unrealized"
            ],
            "exact_world_updated": receipt["exact_world_updated"],
        }
