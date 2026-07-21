from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_reobservation_bounded_continuation_proposal_gate_v0_1 import *

SOURCE_COMMIT = "2944084ee7d415993f35c2bb8551c4fe83ee443d"
SOURCE_TREE_DIGEST = canonical_digest({"repository": "itakura-hidetoshi/KuuOS", "commit": SOURCE_COMMIT})
SELECTED_SPECIALIST_ID = "specialist-formal-001"
SELECTED_SPECIALIST_KIND = "formal"
SELECTED_SUBTASK_KIND = "verify"

PREDECESSOR_GATE_MANIFEST = {'capsule_reproducible': True,
 'continuation_authority_granted': False,
 'continuation_hint_only': True,
 'correctness_claimed': False,
 'cycle_count': 0,
 'cycle_detected': False,
 'distinct_state_count': 7,
 'efficiency_within_budget': True,
 'environment_capsule_digest': '60bec0429b6d113e1fffc3f4e7a98eaed0cc650ebf6a3ba884ba574342fb5be0',
 'environment_exact': True,
 'execution_authority_granted': False,
 'failed_action_count': 0,
 'gate_decision': 'progress_efficiency_admitted',
 'gate_pack_digest': 'e0b8aeea1179a999317e1a0092940c3cb062644c366e0a1700219d35f98debb8',
 'git_authority_granted': False,
 'hold_reasons': [],
 'livelock_free': True,
 'maximum_no_progress_streak': 0,
 'model_call_count': 6,
 'policy_digest': 'b68081d31c7ae11ddfee6737733630b2b69ed2fb894207a4ed93fed2a338cfc6',
 'predecessor_router_verified': True,
 'profile_version': 'CodeAI Environment Capsule and Livelock-Efficiency Gate v0.1',
 'progress_trace_digest': '9ea48de292b513393fa2ef91de33b93eb6c86e315304345f66b88362777f8755',
 'receipt_digest': '51e921bc13bd9a25ae7d7bae34e786e4c4e52d8377a29fe43e60b8b5100ef439',
 'repeated_zero_progress_transitions': 0,
 'repository_full_name': 'itakura-hidetoshi/KuuOS',
 'repository_mutation_performed': False,
 'request_digest': '1b5a979948df37eee196a94516595f215edcdf0715a85a88df745b8dccbfe9b7',
 'router_admission_manifest_digest': 'f7274e04f7f9f2ff3f2f0036dc276c9ae1e275e61399827c781a49377d65f664',
 'router_admission_pack_digest': 'fbd525e9fd5f68df0a52f540bdc97ffee1d728377947d77f76ea6b467ded2baa',
 'router_admission_receipt_digest': '1feee3b7102eb9b45b5b068337950f426de9217482918b7cdfdbb0c0be39298a',
 'schema_version': 'v0.1',
 'selected_specialist_id': 'specialist-formal-001',
 'selected_specialist_kind': 'formal',
 'selected_subtask_kind': 'verify',
 'source_commit_sha': '8d4950e8a9cf197684ef70b86dd35682153449c1',
 'step_count': 6,
 'token_units': 46000,
 'tool_call_count': 9,
 'total_progress_units': 20,
 'trace_grounded': True,
 'wall_clock_ms': 1380000}
PREDECESSOR_GATE_MANIFEST_DIGEST = canonical_digest(PREDECESSOR_GATE_MANIFEST)
PREDECESSOR_GATE_PACK_DIGEST = PREDECESSOR_GATE_MANIFEST["gate_pack_digest"]
PREDECESSOR_GATE_RECEIPT_DIGEST = PREDECESSOR_GATE_MANIFEST["receipt_digest"]

CONTINUATION_CONTRACT_DIGEST = canonical_digest({
    "profile": PROFILE_VERSION,
    "single_action": True,
    "read_only": True,
    "residual_budget_derived": True,
    "reservation": False,
    "execution": False,
})
OBSERVATION_RETURN_CONTRACT_DIGEST = canonical_digest({
    "observable_artifact": True,
    "new_checkpoint": True,
    "predecessor_gate_reentry": True,
    "self_report_only": False,
})
ADMISSION_POLICY_DIGEST = canonical_digest({
    "proposal_hint_only": True,
    "continuation_authority": False,
    "execution_authority": False,
    "repository_mutation": False,
    "git_authority": False,
    "correctness_claim": False,
})


def _digest(label: str) -> str:
    return canonical_digest({"label": label})


def _binding() -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": SOURCE_COMMIT,
        "source_tree_digest": SOURCE_TREE_DIGEST,
        "predecessor_gate_manifest_digest": PREDECESSOR_GATE_MANIFEST_DIGEST,
        "predecessor_gate_pack_digest": PREDECESSOR_GATE_PACK_DIGEST,
        "predecessor_gate_receipt_digest": PREDECESSOR_GATE_RECEIPT_DIGEST,
        "selected_specialist_id": SELECTED_SPECIALIST_ID,
        "selected_specialist_kind": SELECTED_SPECIALIST_KIND,
        "selected_subtask_kind": SELECTED_SUBTASK_KIND,
        "environment_capsule_digest": PREDECESSOR_GATE_MANIFEST["environment_capsule_digest"],
        "progress_trace_digest": PREDECESSOR_GATE_MANIFEST["progress_trace_digest"],
        "predecessor_policy_digest": PREDECESSOR_GATE_MANIFEST["policy_digest"],
        "continuation_contract_digest": CONTINUATION_CONTRACT_DIGEST,
        "observation_return_contract_digest": OBSERVATION_RETURN_CONTRACT_DIGEST,
        "admission_policy_digest": ADMISSION_POLICY_DIGEST,
    }


def build_reference_fixture() -> dict[str, Any]:
    request = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "reobservation-bounded-continuation-request-001",
        "request_revision": "r1",
        **_binding(),
        "requested_continuation_round": 1,
        "request_created_epoch": 1784668000,
        "unresolved_questions": [],
        "claims_continuation_authority": False,
        "claims_execution_authority": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
        "claims_correctness": False,
    }
    request = seal(request, REQUEST_DIGEST_FIELD)

    policy = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + field: request[field] for field in BINDING_FIELDS},
        "evaluation_epoch": 1784668100,
        "maximum_request_age": 3600,
        "maximum_proposal_age": 3600,
        "expected_continuation_round": 1,
        "maximum_action_count": 1,
        "allowed_action_kinds": [
            "observe_repository",
            "inspect_artifact",
            "run_read_only_check",
            "run_formal_verification",
        ],
        "maximum_total_steps": 8,
        "maximum_total_tool_calls": 12,
        "maximum_total_model_calls": 8,
        "maximum_total_token_units": 60000,
        "maximum_total_wall_clock_ms": 1800000,
        "maximum_total_failed_actions": 0,
        "maximum_proposal_steps": 1,
        "maximum_proposal_tool_calls": 2,
        "maximum_proposal_model_calls": 1,
        "maximum_proposal_token_units": 12000,
        "maximum_proposal_wall_clock_ms": 300000,
        "maximum_proposal_failed_actions": 0,
        "require_exact_binding": True,
        "require_predecessor_admitted": True,
        "require_predecessor_hint_only": True,
        "require_predecessor_trace_grounded": True,
        "require_predecessor_capsule_reproducible": True,
        "require_predecessor_livelock_free": True,
        "require_predecessor_efficiency": True,
        "require_proposal_grounded": True,
        "require_read_only_action": True,
        "require_observable_return": True,
        "require_new_checkpoint": True,
        "require_predecessor_gate_reentry": True,
        "allow_proposal_hint": True,
        "allow_continuation_authority": False,
        "allow_execution_authority": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
        "allow_correctness_claim": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)

    continuation_proposal = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "proposal_id": "bounded-continuation-proposal-001",
        "proposal_revision": "r1",
        **_binding(),
        "continuation_round": 1,
        "action_count": 1,
        "action_kind": "run_formal_verification",
        "action_target_digest": canonical_digest({
            "target": "KuuOSCodeAIReobservationBoundedContinuationProposalGateV0_1",
            "source_commit": SOURCE_COMMIT,
        }),
        "pre_state_digest": canonical_digest({
            "source_commit": SOURCE_COMMIT,
            "predecessor_receipt": PREDECESSOR_GATE_RECEIPT_DIGEST,
        }),
        "expected_observation_contract_digest": OBSERVATION_RETURN_CONTRACT_DIGEST,
        "expected_artifact_contract_digest": canonical_digest({
            "artifact": "strict-lean-build-log",
            "machine_observable": True,
            "source_commit": SOURCE_COMMIT,
        }),
        "requested_steps": 1,
        "requested_tool_calls": 1,
        "requested_model_calls": 1,
        "requested_token_units": 7000,
        "requested_wall_clock_ms": 180000,
        "requested_failed_actions": 0,
        "proposal_grounded": True,
        "read_only_action": True,
        "observable_return_required": True,
        "new_checkpoint_required": True,
        "predecessor_gate_reentry_required": True,
        "self_report_only": False,
        "proposal_created_epoch": 1784668010,
        "claims_continuation_authority": False,
        "claims_execution_authority": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
        "claims_correctness": False,
    }
    continuation_proposal = seal(continuation_proposal, PROPOSAL_DIGEST_FIELD)

    result = build_codeai_reobservation_bounded_continuation_proposal_gate(
        request=request,
        policy=policy,
        predecessor_gate=PREDECESSOR_GATE_MANIFEST,
        continuation_proposal=continuation_proposal,
    )
    if result.status != STATUS_READY or result.gate_pack is None or result.receipt is None:
        raise RuntimeError(result.issues)
    return {
        "request": request,
        "policy": policy,
        "predecessor_gate": deepcopy(PREDECESSOR_GATE_MANIFEST),
        "continuation_proposal": continuation_proposal,
        "gate_pack": result.gate_pack,
        "receipt": result.receipt,
    }


def deep_reference_fixture() -> dict[str, Any]:
    return deepcopy(build_reference_fixture())


__all__ = [
    "PREDECESSOR_GATE_MANIFEST",
    "PREDECESSOR_GATE_MANIFEST_DIGEST",
    "build_reference_fixture",
    "deep_reference_fixture",
]
