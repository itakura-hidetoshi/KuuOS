#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 import (
    STATUS_READY,
    build_planos_middle_way_bounded_synthesis_intake_certificate,
    canonical_digest,
    compute_planos_middle_way_intake_bundle_digest,
)
from scripts.check_verifyos_middle_way_conditional_continuity_verification_v0_4 import (
    _build as build_verifyos_case,
)

CERT_DIGEST_FIELD = (
    "verifyos_middle_way_conditional_continuity_certificate_digest"
)


def _source(transition_kind: str = "retain") -> dict:
    result = build_verifyos_case(transition_kind)
    assert result.status == STATUS_READY, result.blockers
    assert result.certificate is not None
    return deepcopy(result.certificate)


def _redigest_source(source: dict) -> dict:
    value = deepcopy(source)
    value.pop(CERT_DIGEST_FIELD, None)
    value[CERT_DIGEST_FIELD] = canonical_digest(value)
    return value


def _replace_spec(source: dict, spec: dict) -> dict:
    value = deepcopy(source)
    value["transition_spec"] = spec
    value["transition_spec_digest"] = canonical_digest(spec)
    value["transition_kind"] = spec.get("transition_kind", "")
    value["conditional_validity_status"] = spec.get(
        "conditional_validity_status", ""
    )
    value["transition_reason_digest"] = spec.get(
        "transition_reason_digest", ""
    )
    return _redigest_source(value)


def _build(transition_kind: str = "retain", **overrides):
    source = overrides.pop("source_verifyos_certificate", _source(transition_kind))
    policy = overrides.pop("intake_policy_digest", "planos-intake-policy-v103")
    owner = overrides.pop(
        "planos_intake_responsibility_digest", "planos-owner-v103"
    )
    request_id = overrides.pop("intake_request_id", "planos-intake-v103-001")
    args = {
        "source_verifyos_certificate": source,
        "expected_source_verifyos_certificate_digest": source.get(
            CERT_DIGEST_FIELD, ""
        ),
        "expected_source_handoff_receipt_digest": source.get(
            "source_handoff_receipt_digest", ""
        ),
        "expected_world_binding_digest": source.get(
            "source_world_binding_digest", ""
        ),
        "expected_world_model_state_digest": source.get(
            "source_world_model_state_digest", ""
        ),
        "expected_world_model_revision": source.get(
            "source_world_model_revision", -1
        ),
        "expected_world_lineage_digest": source.get(
            "source_world_lineage_digest", ""
        ),
        "expected_selected_candidate_id": source.get(
            "selected_candidate_id", ""
        ),
        "expected_selected_candidate_plan_intent_digest": source.get(
            "selected_candidate_plan_intent_digest", ""
        ),
        "expected_synthesis_constraint_digest": source.get(
            "source_synthesis_constraint_digest", ""
        ),
        "intake_policy_digest": policy,
        "planos_intake_responsibility_digest": owner,
        "intake_request_id": request_id,
    }
    args.update(overrides)
    args.setdefault(
        "intake_bundle_digest",
        compute_planos_middle_way_intake_bundle_digest(
            source_verifyos_certificate_digest=source.get(
                CERT_DIGEST_FIELD, ""
            ),
            expected_source_verifyos_certificate_digest=args[
                "expected_source_verifyos_certificate_digest"
            ],
            expected_source_handoff_receipt_digest=args[
                "expected_source_handoff_receipt_digest"
            ],
            expected_world_binding_digest=args["expected_world_binding_digest"],
            expected_world_model_state_digest=args[
                "expected_world_model_state_digest"
            ],
            expected_world_model_revision=args[
                "expected_world_model_revision"
            ],
            expected_world_lineage_digest=args[
                "expected_world_lineage_digest"
            ],
            expected_selected_candidate_id=args[
                "expected_selected_candidate_id"
            ],
            expected_selected_candidate_plan_intent_digest=args[
                "expected_selected_candidate_plan_intent_digest"
            ],
            expected_synthesis_constraint_digest=args[
                "expected_synthesis_constraint_digest"
            ],
            intake_policy_digest=policy,
            planos_intake_responsibility_digest=owner,
            intake_request_id=request_id,
        ),
    )
    return build_planos_middle_way_bounded_synthesis_intake_certificate(**args)


def main() -> int:
    routes = {
        "retain": ("bounded_synthesis_intake_ready", True),
        "suspend": ("await_condition_change", False),
        "request_revision": ("return_to_decisionos_revision", False),
        "supersede_with_lineage": (
            "successor_lineage_reverification_required",
            False,
        ),
        "complete": ("close_without_synthesis", False),
        "terminate": ("terminate_without_synthesis", False),
    }
    for kind, (disposition, admitted) in routes.items():
        result = _build(kind)
        assert result.status == STATUS_READY, result.blockers
        assert result.certificate is not None
        certificate = result.certificate
        assert certificate["intake_disposition"] == disposition
        assert certificate["bounded_synthesis_request_admitted"] is admitted
        assert certificate["bounded_synthesis_intake_ready"] is admitted
        assert certificate["only_valid_status_admitted"] is True
        assert certificate["nonvalid_status_not_synthesized"] is True
        for name in (
            "source_conditions_preserved",
            "source_changed_conditions_preserved",
            "source_lineage_preserved",
            "source_predecessor_preserved",
            "source_responsibility_preserved",
            "source_dissent_preserved",
            "source_minority_evidence_preserved",
            "responsibility_extended_not_replaced",
            "selection_remains_decisionos_owned",
            "persistent_world_state_unchanged",
            "world_model_prediction_not_truth",
            "history_read_only",
            "qi_grants_no_authority",
            "future_only",
        ):
            assert certificate[name] is True
        for name in (
            "selection_authority_granted_to_planos",
            "plan_synthesis_performed",
            "concrete_plan_issued",
            "plan_receipt_issued",
            "execution_authority_granted",
            "execution_permission",
            "world_mutation_not_granted",
            "active_now",
        ):
            expected = True if name == "world_mutation_not_granted" else False
            assert certificate[name] is expected
        responsibility = certificate[
            "resulting_responsibility_lineage_digests"
        ]
        assert "verify-owner-v04" in responsibility
        assert "planos-owner-v103" in responsibility

    retain = _source("retain")
    revision = _source("request_revision")
    retain_digest = retain[CERT_DIGEST_FIELD]
    revision_digest = revision[CERT_DIGEST_FIELD]

    bad_digest = deepcopy(retain)
    bad_digest[CERT_DIGEST_FIELD] = "wrong"

    promoted = deepcopy(retain)
    promoted["plan_synthesis_performed"] = True
    promoted = _redigest_source(promoted)

    wrong_status = deepcopy(retain)
    wrong_status["conditional_validity_status"] = "terminated"
    wrong_status = _redigest_source(wrong_status)

    missing_lineage_spec = deepcopy(revision["transition_spec"])
    missing_lineage_spec["resulting_lineage_digests"].remove(
        revision["source_handoff_receipt_digest"]
    )
    missing_lineage = _replace_spec(revision, missing_lineage_spec)

    missing_owner_spec = deepcopy(retain["transition_spec"])
    missing_owner_spec["resulting_responsibility_lineage_digests"] = [
        "decision-owner-v08"
    ]
    missing_owner = _replace_spec(retain, missing_owner_spec)

    silent_spec = deepcopy(revision["transition_spec"])
    silent_spec["silent_rewrite_requested"] = True
    silent = _replace_spec(revision, silent_spec)

    blocked = [
        _build(source_verifyos_certificate={}),
        _build(intake_policy_digest=""),
        _build(planos_intake_responsibility_digest=""),
        _build(intake_request_id=""),
        _build(intake_bundle_digest="wrong"),
        _build(source_verifyos_certificate=bad_digest),
        _build(
            source_verifyos_certificate=promoted,
            expected_source_verifyos_certificate_digest=retain_digest,
        ),
        _build(
            source_verifyos_certificate=wrong_status,
            expected_source_verifyos_certificate_digest=retain_digest,
        ),
        _build(
            source_verifyos_certificate=missing_lineage,
            expected_source_verifyos_certificate_digest=revision_digest,
        ),
        _build(
            source_verifyos_certificate=missing_owner,
            expected_source_verifyos_certificate_digest=retain_digest,
        ),
        _build(
            source_verifyos_certificate=silent,
            expected_source_verifyos_certificate_digest=revision_digest,
        ),
        _build(expected_world_binding_digest="wrong-world-binding"),
        _build(expected_world_model_state_digest="wrong-world-state"),
        _build(expected_world_model_revision=9),
        _build(expected_world_lineage_digest="wrong-world-lineage"),
        _build(expected_selected_candidate_id="hold"),
        _build(
            expected_selected_candidate_plan_intent_digest="wrong-plan-intent"
        ),
        _build(expected_synthesis_constraint_digest="wrong-constraints"),
    ]
    for result in blocked:
        assert result.status != STATUS_READY
        assert result.blockers
        assert result.certificate is None

    print("PASS: PlanOS Middle-Way Bounded Synthesis Intake Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
