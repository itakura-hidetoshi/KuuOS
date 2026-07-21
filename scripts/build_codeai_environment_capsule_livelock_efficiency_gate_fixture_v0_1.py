from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_v0_1 import *

SOURCE_COMMIT = "8d4950e8a9cf197684ef70b86dd35682153449c1"
SOURCE_TREE_DIGEST = canonical_digest({"repository": "itakura-hidetoshi/KuuOS", "commit": SOURCE_COMMIT})
ROUTER_ADMISSION_PACK_DIGEST = "fbd525e9fd5f68df0a52f540bdc97ffee1d728377947d77f76ea6b467ded2baa"
ROUTER_ADMISSION_RECEIPT_DIGEST = "1feee3b7102eb9b45b5b068337950f426de9217482918b7cdfdbb0c0be39298a"
SELECTED_SPECIALIST_ID = "specialist-formal-001"
SELECTED_SPECIALIST_KIND = "formal"
SELECTED_SUBTASK_KIND = "verify"

ROUTER_ADMISSION_MANIFEST = {
    "admission_pack_digest": ROUTER_ADMISSION_PACK_DIGEST,
    "candidate_selected": False,
    "correctness_claimed": False,
    "eligible_specialist_count": 4,
    "exact_binding_verified": True,
    "excluded_specialist_count": 0,
    "execution_authority_granted": False,
    "execution_signal_count": 2,
    "exploration_turns": 4,
    "git_authority_granted": False,
    "grounding_source_count": 3,
    "independent_measurement_verified": True,
    "measurement_grounded": True,
    "memory_pack_binding_verified": True,
    "memory_pack_digest": "9826f4a6024cdad797c1acff2ead6156c93393f61f20a6f1bb7455f1c265c097",
    "memory_receipt_digest": "8c566cfb36967262d50b0879b01df042e371e2196a5e0f34cc50a3c6e775b969",
    "observable_artifact_count": 4,
    "observation_count": 7,
    "policy_digest": "67ae950afa2825b337aec222ef8a806391b250d2be6ffab5f6d1f3102874df85",
    "profile_version": PREDECESSOR_PROFILE_VERSION,
    "queried_subtask_kind": SELECTED_SUBTASK_KIND,
    "receipt_digest": ROUTER_ADMISSION_RECEIPT_DIGEST,
    "repository_full_name": "itakura-hidetoshi/KuuOS",
    "repository_mutation_performed": False,
    "request_digest": "3841932fea0b6aeb822a771ba9a6f6675329d47005803ac7c64d9b068b37a730",
    "route_decision": "specialist_route_admitted",
    "route_hint_only": True,
    "schema_version": SCHEMA_VERSION,
    "selected_specialist_id": SELECTED_SPECIALIST_ID,
    "selected_specialist_kind": SELECTED_SPECIALIST_KIND,
    "selected_utility_score": 154,
    "source_commit_sha": "ec125a6aa4b6e51650305ab7ddc7361a352a2848",
    "specialist_alignment_verified": True,
    "specialist_dispatched": False,
    "trajectory_digest": "e5607608284ae10313ec7796fd1b28bd82c4c52accd20455c9ea3ccc829fd176",
}
ROUTER_ADMISSION_MANIFEST_DIGEST = canonical_digest(ROUTER_ADMISSION_MANIFEST)

DEPENDENCY_SLICE_DIGEST = canonical_digest({"paths": [
    "formal/KUOS/CodeAI/TrajectoryGroundedSpecialistRouterAdmissionV0_1.lean",
    "runtime/kuuos_codeai_trajectory_grounded_specialist_router_admission_v0_1.py",
    "tests/test_kuuos_codeai_trajectory_grounded_specialist_router_admission_v0_1.py",
    "lakefile.toml",
]})
TOOLCHAIN_DIGEST = canonical_digest({
    "runner": "ubuntu-22.04",
    "python": "3.12",
    "lean": "leanprover/lean4:v4.30.0-rc2",
    "mathlib": "v4.30.0-rc2",
})
ENVIRONMENT_CONTRACT_DIGEST = canonical_digest({
    "immutable": True,
    "complete": True,
    "observed": True,
    "dependency_lock": True,
    "network_access": False,
})
PROGRESS_CONTRACT_DIGEST = canonical_digest({
    "state_transition_checkpoints": True,
    "observable_artifacts": True,
    "cycle_detection": True,
    "zero_progress_repetition_detection": True,
    "resource_budgets": True,
})
GATE_POLICY_DIGEST = canonical_digest({
    "profile": PROFILE_VERSION,
    "decision": "continuation-hint-only",
    "execution_authority": False,
    "repository_mutation": False,
})


def _digest(label: str) -> str:
    return canonical_digest({"label": label})


def _binding() -> dict[str, Any]:
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": SOURCE_COMMIT,
        "source_tree_digest": SOURCE_TREE_DIGEST,
        "router_admission_manifest_digest": ROUTER_ADMISSION_MANIFEST_DIGEST,
        "router_admission_pack_digest": ROUTER_ADMISSION_PACK_DIGEST,
        "router_admission_receipt_digest": ROUTER_ADMISSION_RECEIPT_DIGEST,
        "selected_specialist_id": SELECTED_SPECIALIST_ID,
        "selected_specialist_kind": SELECTED_SPECIALIST_KIND,
        "selected_subtask_kind": SELECTED_SUBTASK_KIND,
        "dependency_slice_digest": DEPENDENCY_SLICE_DIGEST,
        "toolchain_digest": TOOLCHAIN_DIGEST,
        "environment_contract_digest": ENVIRONMENT_CONTRACT_DIGEST,
        "progress_contract_digest": PROGRESS_CONTRACT_DIGEST,
        "gate_policy_digest": GATE_POLICY_DIGEST,
    }


def _checkpoint(
    step_index: int,
    phase: str,
    *,
    progress_units: int,
    tool_calls: int,
    model_calls: int,
    input_tokens: int,
    output_tokens: int,
    wall_clock_ms: int,
    failed_action: bool = False,
) -> dict[str, Any]:
    return {
        "step_index": step_index,
        "phase": phase,
        "state_before_digest": _digest(f"state-{step_index}"),
        "action_digest": _digest(f"action-{step_index}"),
        "observation_digest": _digest(f"observation-{step_index}"),
        "state_after_digest": _digest(f"state-{step_index + 1}"),
        "observable_artifact_digest": _digest(f"artifact-{step_index}"),
        "progress_units": progress_units,
        "tool_calls": tool_calls,
        "model_calls": model_calls,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "wall_clock_ms": wall_clock_ms,
        "failed_action": failed_action,
    }


def build_reference_fixture() -> dict[str, Any]:
    request = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "environment-efficiency-gate-request-001",
        "request_revision": "r1",
        **_binding(),
        "request_created_epoch": 1784643300,
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
        "evaluation_epoch": 1784643400,
        "maximum_request_age": 3600,
        "maximum_capsule_age": 3600,
        "maximum_trace_age": 3600,
        "maximum_steps": 12,
        "maximum_tool_calls": 20,
        "maximum_model_calls": 12,
        "maximum_token_units": 80000,
        "maximum_wall_clock_ms": 3600000,
        "maximum_failed_actions": 2,
        "maximum_no_progress_streak": 2,
        "maximum_repeated_zero_progress_transitions": 0,
        "maximum_cycle_count": 0,
        "minimum_total_progress_units": 15,
        "minimum_distinct_state_count": 5,
        "require_exact_binding": True,
        "require_immutable_capsule": True,
        "require_complete_capsule": True,
        "require_observed_capsule": True,
        "require_dependency_lock": True,
        "require_network_disabled": True,
        "require_observable_trace": True,
        "require_cycle_free": True,
        "allow_continuation_hint": True,
        "allow_continuation_authority": False,
        "allow_execution_authority": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
        "allow_correctness_claim": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)

    environment_capsule = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "capsule_id": "environment-capsule-main-8d4950e8-001",
        "capsule_revision": "r1",
        **_binding(),
        "runner_image_digest": _digest("ubuntu-22.04-runner-image"),
        "operating_system_digest": _digest("ubuntu-22.04-os-release"),
        "architecture": "x86_64",
        "python_version": "3.12",
        "lean_toolchain": "leanprover/lean4:v4.30.0-rc2",
        "dependency_manifest_digest": canonical_digest({"path": "lake-manifest.json", "source_commit": SOURCE_COMMIT}),
        "workflow_definition_digest": canonical_digest({
            "checkout": "actions/checkout@v6",
            "python": "actions/setup-python@v5",
            "lean": "leanprover/lean-action@v1",
        }),
        "environment_variables_digest": canonical_digest({"MATHLIB_NO_CACHE_ON_UPDATE": "1"}),
        "locale": "C.UTF-8",
        "timezone": "UTC",
        "network_access_allowed": False,
        "root_filesystem_immutable": True,
        "dependency_lock_verified": True,
        "capsule_complete": True,
        "capsule_observed": True,
        "self_report_only": False,
        "capsule_created_epoch": 1784643310,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    environment_capsule = seal(environment_capsule, CAPSULE_DIGEST_FIELD)

    checkpoints = [
        _checkpoint(0, "observe", progress_units=2, tool_calls=1, model_calls=1, input_tokens=4500, output_tokens=1500, wall_clock_ms=120000),
        _checkpoint(1, "plan", progress_units=2, tool_calls=1, model_calls=1, input_tokens=4500, output_tokens=1500, wall_clock_ms=120000),
        _checkpoint(2, "execute", progress_units=3, tool_calls=2, model_calls=1, input_tokens=6000, output_tokens=2000, wall_clock_ms=240000),
        _checkpoint(3, "verify", progress_units=4, tool_calls=2, model_calls=1, input_tokens=7000, output_tokens=2000, wall_clock_ms=300000),
        _checkpoint(4, "verify", progress_units=5, tool_calls=2, model_calls=1, input_tokens=8000, output_tokens=2000, wall_clock_ms=420000),
        _checkpoint(5, "govern", progress_units=4, tool_calls=1, model_calls=1, input_tokens=5500, output_tokens=1500, wall_clock_ms=180000),
    ]
    progress_trace = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "trace_id": "progress-efficiency-trace-001",
        "trace_revision": "r1",
        **_binding(),
        "environment_capsule_digest": environment_capsule[CAPSULE_DIGEST_FIELD],
        "checkpoints": checkpoints,
        "trace_observable": True,
        "trace_complete": True,
        "self_report_only": False,
        "trace_created_epoch": 1784643320,
        "continuation_authority_granted": False,
        "execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    progress_trace = seal(progress_trace, TRACE_DIGEST_FIELD)

    result = build_codeai_environment_capsule_livelock_efficiency_gate(
        request=request,
        policy=policy,
        router_admission=ROUTER_ADMISSION_MANIFEST,
        environment_capsule=environment_capsule,
        progress_trace=progress_trace,
    )
    if result.status != STATUS_READY or result.gate_pack is None or result.receipt is None:
        raise RuntimeError(result.issues)
    return {
        "request": request,
        "policy": policy,
        "router_admission": deepcopy(ROUTER_ADMISSION_MANIFEST),
        "environment_capsule": environment_capsule,
        "progress_trace": progress_trace,
        "gate_pack": result.gate_pack,
        "receipt": result.receipt,
    }


def deep_reference_fixture() -> dict[str, Any]:
    return deepcopy(build_reference_fixture())


__all__ = [
    "ROUTER_ADMISSION_MANIFEST",
    "build_reference_fixture",
    "deep_reference_fixture",
]
