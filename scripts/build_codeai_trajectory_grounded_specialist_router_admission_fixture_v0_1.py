from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_v0_1 import *

SOURCE_COMMIT = "ec125a6aa4b6e51650305ab7ddc7361a352a2848"
SOURCE_TREE_DIGEST = canonical_digest({"repository": "itakura-hidetoshi/KuuOS", "commit": SOURCE_COMMIT})
MEMORY_PACK_DIGEST = "9826f4a6024cdad797c1acff2ead6156c93393f61f20a6f1bb7455f1c265c097"
MEMORY_RECEIPT_DIGEST = "8c566cfb36967262d50b0879b01df042e371e2196a5e0f34cc50a3c6e775b969"
SUBTASK_CONTRACT_DIGEST = canonical_digest({"subtask": "verify", "contract": "trajectory-grounded-routing"})
PREDECESSOR_OUTPUT_DIGEST = MEMORY_PACK_DIGEST
DEPENDENCY_SLICE_DIGEST = canonical_digest({"paths": [
    "formal/KUOS/CodeAI/SubtaskLevelVersionBoundMemoryV0_1.lean",
    "runtime/kuuos_codeai_subtask_level_version_bound_memory_v0_1.py",
    "tests/test_kuuos_codeai_subtask_level_version_bound_memory_v0_1.py",
]})
TOOLCHAIN_DIGEST = canonical_digest({"lean": "v4.30.0-rc2", "python": "3.12"})
ENVIRONMENT_DIGEST = canonical_digest({"runner": "ubuntu-22.04", "network": False})
TRAJECTORY_CONTRACT_DIGEST = canonical_digest({
    "partial_trajectory": True,
    "observable_artifacts": True,
    "execution_signals": True,
    "self_report_only": False,
})
ROUTING_POLICY_DIGEST = canonical_digest({
    "router": PROFILE_VERSION,
    "decision": "admission-only",
    "specialist_dispatch": False,
})


def _digest(label: str) -> str:
    return canonical_digest({"label": label})


def _binding() -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": SOURCE_COMMIT,
        "source_tree_digest": SOURCE_TREE_DIGEST,
        "memory_pack_digest": MEMORY_PACK_DIGEST,
        "memory_receipt_digest": MEMORY_RECEIPT_DIGEST,
        "subtask_kind": "verify",
        "subtask_contract_digest": SUBTASK_CONTRACT_DIGEST,
        "predecessor_output_digest": PREDECESSOR_OUTPUT_DIGEST,
        "dependency_slice_digest": DEPENDENCY_SLICE_DIGEST,
        "toolchain_digest": TOOLCHAIN_DIGEST,
        "environment_digest": ENVIRONMENT_DIGEST,
        "trajectory_contract_digest": TRAJECTORY_CONTRACT_DIGEST,
        "routing_policy_digest": ROUTING_POLICY_DIGEST,
    }


def _specialist(
    specialist_id: str,
    specialist_kind: str,
    *,
    fit_score: int,
    reliability_score: int,
    estimated_cost_units: int,
    trajectory_digest: str,
) -> dict[str, Any]:
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "specialist_id": specialist_id,
        "specialist_revision": "r1",
        "specialist_kind": specialist_kind,
        "supported_subtask_kind": "verify",
        **_binding(),
        "measurement_packet_digest": trajectory_digest,
        "fit_score": fit_score,
        "reliability_score": reliability_score,
        "estimated_cost_units": estimated_cost_units,
        "utility_score": fit_score + reliability_score - estimated_cost_units,
        "independent_measurement": True,
        "evidence_created_epoch": 1784643605,
        "route_hint_only": True,
        "repository_mutation_performed": False,
        "specialist_dispatched": False,
        "candidate_selected": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(evidence, SPECIALIST_DIGEST_FIELD)


def build_reference_fixture() -> dict[str, Any]:
    request = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "trajectory-router-request-001",
        "request_revision": "r1",
        **_binding(),
        "requested_specialist_kinds": list(SPECIALIST_KINDS),
        "request_created_epoch": 1784643600,
        "unresolved_questions": [],
        "claims_selection_authority": False,
        "claims_dispatch_authority": False,
        "claims_execution_authority": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
    }
    request = seal(request, REQUEST_DIGEST_FIELD)

    policy = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + field: request[field] for field in BINDING_FIELDS},
        "evaluation_epoch": 1784643620,
        "maximum_request_age": 3600,
        "maximum_trajectory_age": 3600,
        "maximum_evidence_age": 3600,
        "maximum_candidates": 8,
        "minimum_exploration_turns": 3,
        "minimum_observation_count": 5,
        "minimum_execution_signal_count": 1,
        "minimum_grounding_sources": 3,
        "minimum_observable_artifacts": 3,
        "minimum_fit_score": 80,
        "minimum_reliability_score": 80,
        "maximum_cost_units": 40,
        "minimum_route_margin": 5,
        "require_exact_binding": True,
        "require_partial_trajectory": True,
        "require_observable_artifacts": True,
        "require_independent_measurement": True,
        "require_specialist_alignment": True,
        "require_memory_pack_binding": True,
        "allow_route_hint": True,
        "allow_specialist_dispatch": False,
        "allow_candidate_selection": False,
        "allow_execution_authority": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)

    trajectory = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "trajectory_id": "partial-trajectory-verify-001",
        "trajectory_revision": "r1",
        **_binding(),
        "exploration_turns": 4,
        "observation_count": 7,
        "execution_signal_count": 2,
        "grounding_sources": ["repository_state", "completed_ci", "version_bound_memory"],
        "observable_artifact_digests": [
            _digest("repository-snapshot"),
            _digest("completed-ci-log"),
            _digest("memory-pack"),
            _digest("formal-root"),
        ],
        "self_report_only": False,
        "measurement_complete": True,
        "repository_state_observed": True,
        "tests_observed": True,
        "trajectory_created_epoch": 1784643603,
        "repository_mutation_performed": False,
        "specialist_dispatched": False,
        "candidate_selected": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
    }
    trajectory = seal(trajectory, TRAJECTORY_DIGEST_FIELD)

    specialists = [
        _specialist("specialist-formal-001", "formal", fit_score=95, reliability_score=94, estimated_cost_units=35, trajectory_digest=trajectory[TRAJECTORY_DIGEST_FIELD]),
        _specialist("specialist-behavioral-001", "behavioral", fit_score=88, reliability_score=90, estimated_cost_units=30, trajectory_digest=trajectory[TRAJECTORY_DIGEST_FIELD]),
        _specialist("specialist-adversarial-001", "adversarial", fit_score=84, reliability_score=87, estimated_cost_units=28, trajectory_digest=trajectory[TRAJECTORY_DIGEST_FIELD]),
        _specialist("specialist-maintainability-001", "maintainability", fit_score=80, reliability_score=86, estimated_cost_units=25, trajectory_digest=trajectory[TRAJECTORY_DIGEST_FIELD]),
    ]

    result = build_codeai_trajectory_grounded_specialist_router_admission(
        request=request, policy=policy, trajectory=trajectory, specialists=specialists
    )
    if result.status != STATUS_READY or result.admission_pack is None or result.receipt is None:
        raise RuntimeError(result.issues)
    return {
        "request": request,
        "policy": policy,
        "trajectory": trajectory,
        "specialists": specialists,
        "admission_pack": result.admission_pack,
        "receipt": result.receipt,
    }


def deep_reference_fixture() -> dict[str, Any]:
    return deepcopy(build_reference_fixture())


__all__ = ["build_reference_fixture", "deep_reference_fixture"]
