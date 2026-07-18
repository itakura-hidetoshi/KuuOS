#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD as PATCH_CANDIDATE_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    STATUS_READY as UNIFIED_DIFF_STATUS_READY,
    build_codeai_autonomous_unified_diff_candidates,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD as SELECTION_POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as SELECTION_REQUEST_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    STATUS_READY as SELECTION_STATUS_READY,
    build_codeai_autonomous_candidate_portfolio_selection,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    POLICY_DIGEST_FIELD as APPLICATION_POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as APPLICATION_REQUEST_DIGEST_FIELD,
    STATUS_READY as APPLICATION_STATUS_READY,
    build_codeai_autonomous_isolated_candidate_application,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    APPLICATION_RECEIPT_DIGEST_FIELD,
    CANDIDATE_DIGEST_FIELD,
    CANDIDATE_RECEIPT_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_autonomous_verification_execution,
)
from runtime.kuuos_codeai_independent_verification_envelope_v0_1 import (
    POLICY_DIGEST_FIELD as INDEPENDENT_POLICY_DIGEST_FIELD,
    STATUS_READY as INDEPENDENT_STATUS_READY,
    build_codeai_independent_verification_envelope,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proposal_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_unified_diff_candidates_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    candidate_data = json.loads(
        (ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    selection_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_candidate_portfolio_selection_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    application_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_isolated_candidate_application_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    execution_data = json.loads(
        (ROOT / "examples" / "codeai_autonomous_verification_execution_v0_1.json").read_text(
            encoding="utf-8"
        )
    )

    repository_files = proposal_data["repository_files"]
    repository_before = deepcopy(repository_files)
    upstream = build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=candidate_data["source_observation_receipt"],
        repository_files=repository_files,
        proposals=proposal_data["proposals"],
        candidate_policy=candidate_data["candidate_policy"],
    )
    assert upstream.status == UNIFIED_DIFF_STATUS_READY, upstream.issues
    assert upstream.receipt is not None

    selection_request = dict(selection_data["selection_request"])
    selection_request["source_portfolio_receipt_digest"] = upstream.receipt[
        UNIFIED_DIFF_RECEIPT_DIGEST_FIELD
    ]
    selection_request = seal(selection_request, SELECTION_REQUEST_DIGEST_FIELD)
    selection_policy = dict(selection_data["selection_policy"])
    selection_policy["expected_source_portfolio_receipt_digest"] = upstream.receipt[
        UNIFIED_DIFF_RECEIPT_DIGEST_FIELD
    ]
    selection_policy = seal(selection_policy, SELECTION_POLICY_DIGEST_FIELD)
    selection = build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=upstream.receipt,
        candidates=upstream.candidates,
        selection_request=selection_request,
        selection_policy=selection_policy,
    )
    assert selection.status == SELECTION_STATUS_READY, selection.issues
    assert selection.receipt is not None
    assert selection.selected_candidate is not None

    selected = selection.selected_candidate
    candidate = selected.patch_candidate
    source_snapshot_digest = canonical_digest(repository_files)
    application_request = dict(application_data["application_request"])
    application_request["source_selection_receipt_digest"] = selection.receipt[
        SELECTION_RECEIPT_DIGEST_FIELD
    ]
    application_request["selected_candidate_digest"] = candidate[PATCH_CANDIDATE_DIGEST_FIELD]
    application_request["source_repository_snapshot_digest"] = source_snapshot_digest
    application_request = seal(application_request, APPLICATION_REQUEST_DIGEST_FIELD)
    application_policy = dict(application_data["application_policy"])
    application_policy["expected_source_selection_receipt_digest"] = selection.receipt[
        SELECTION_RECEIPT_DIGEST_FIELD
    ]
    application_policy["expected_selected_candidate_digest"] = candidate[PATCH_CANDIDATE_DIGEST_FIELD]
    application_policy["expected_patch_artifact_digest"] = candidate["patch_artifact_digest"]
    application_policy["expected_repository_full_name"] = candidate["repository_full_name"]
    application_policy["expected_source_commit_sha"] = candidate["source_commit_sha"]
    application_policy["expected_source_repository_snapshot_digest"] = source_snapshot_digest
    application_policy = seal(application_policy, APPLICATION_POLICY_DIGEST_FIELD)
    application = build_codeai_autonomous_isolated_candidate_application(
        source_selection_receipt=selection.receipt,
        selected_candidate=selected,
        repository_files=repository_files,
        application_request=application_request,
        application_policy=application_policy,
    )
    assert application.status == APPLICATION_STATUS_READY, application.issues
    assert application.receipt is not None
    assert application.resulting_repository_files is not None

    plan = execution_data["verification_plan"]
    request = dict(execution_data["execution_request"])
    request.update(
        {
            "source_candidate_receipt_digest": selected.candidate_receipt[
                CANDIDATE_RECEIPT_DIGEST_FIELD
            ],
            "source_application_receipt_digest": application.receipt[
                APPLICATION_RECEIPT_DIGEST_FIELD
            ],
            "candidate_digest": selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
            "patch_artifact_digest": selected.candidate_receipt["patch_artifact_digest"],
            "source_repository_snapshot_digest": application.receipt[
                "source_repository_snapshot_digest"
            ],
            "resulting_repository_snapshot_digest": canonical_digest(
                application.resulting_repository_files
            ),
            "repository_full_name": selected.candidate_receipt["repository_full_name"],
            "source_commit_sha": selected.candidate_receipt["source_commit_sha"],
            "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
        }
    )
    request = seal(request, REQUEST_DIGEST_FIELD)
    policy = dict(execution_data["execution_policy"])
    policy.update(
        {
            "expected_source_candidate_receipt_digest": selected.candidate_receipt[
                CANDIDATE_RECEIPT_DIGEST_FIELD
            ],
            "expected_source_application_receipt_digest": application.receipt[
                APPLICATION_RECEIPT_DIGEST_FIELD
            ],
            "expected_candidate_digest": selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
            "expected_patch_artifact_digest": selected.candidate_receipt["patch_artifact_digest"],
            "expected_source_repository_snapshot_digest": application.receipt[
                "source_repository_snapshot_digest"
            ],
            "expected_resulting_repository_snapshot_digest": canonical_digest(
                application.resulting_repository_files
            ),
            "expected_repository_full_name": selected.candidate_receipt["repository_full_name"],
            "expected_source_commit_sha": selected.candidate_receipt["source_commit_sha"],
            "expected_verification_plan_digest": plan[PLAN_DIGEST_FIELD],
        }
    )
    policy = seal(policy, POLICY_DIGEST_FIELD)

    def runner_adapter(invocation):
        assert invocation.repository_files == application.resulting_repository_files
        assert invocation.network_access_allowed is False
        assert invocation.secrets_allowed is False
        assert invocation.live_repository_access_allowed is False
        assert invocation.git_operations_allowed is False
        return {
            "runner_id": "integration-in-memory-runner",
            "runner_session_id": "integration-" + invocation.check_id,
            "check_id": invocation.check_id,
            "exit_code": 0,
            "stdout": "PASS: " + invocation.check_id + "\n",
            "stderr": "",
            "duration_ms": 5,
            "timed_out": False,
            "exception_type": None,
            "started_epoch": execution_data["execution_policy"]["evaluation_epoch"] - 5,
            "completed_epoch": execution_data["execution_policy"]["evaluation_epoch"] - 4,
            "network_used": False,
            "secret_accessed": False,
            "live_repository_accessed": False,
            "git_effect_performed": False,
        }

    execution = build_codeai_autonomous_verification_execution(
        source_candidate_receipt=selected.candidate_receipt,
        source_application_receipt=application.receipt,
        resulting_repository_files=application.resulting_repository_files,
        verification_plan=plan,
        execution_request=request,
        execution_policy=policy,
        runner_adapter=runner_adapter,
    )
    assert execution.status == STATUS_READY, execution.issues
    assert execution.receipt is not None
    assert execution.evidence_bundle is not None
    assert execution.independent_verification_evidence is not None
    assert execution.receipt["failed_check_count"] == 0
    assert execution.receipt["repository_mutation_performed"] is False
    assert repository_files == repository_before

    independent_policy = seal(
        {
            "expected_source_candidate_receipt_digest": selected.candidate_receipt[
                CANDIDATE_RECEIPT_DIGEST_FIELD
            ],
            "expected_candidate_patch_digest": selected.candidate_receipt[CANDIDATE_DIGEST_FIELD],
            "expected_repository_full_name": selected.candidate_receipt["repository_full_name"],
            "expected_source_commit_sha": selected.candidate_receipt["source_commit_sha"],
            "allowed_evidence_formats": [request["evidence_format"]],
            "allowed_toolchain_digests": [request["toolchain_digest"]],
            "allowed_verifier_ids": [request["verifier_id"]],
            "required_check_ids": list(execution.evidence_bundle["check_ids"]),
            "minimum_reproduction_attempts": 1,
            "minimum_successful_reproduction_attempts": 1,
            "require_falsification_challenge": False,
            "require_isolated_verification": True,
            "require_distinct_candidate_producer": True,
            "require_distinct_reviewer": True,
            "allow_skipped_checks": False,
            "allow_inconclusive_degradation": False,
            "known_finding_labels": ["verification_execution_failure"],
            "handover_finding_labels": ["verification_execution_failure"],
            "evaluation_epoch": execution_data["execution_policy"]["evaluation_epoch"],
            "maximum_evidence_age": 300,
            "maximum_verification_duration": 300,
        },
        INDEPENDENT_POLICY_DIGEST_FIELD,
    )
    independent = build_codeai_independent_verification_envelope(
        source_candidate_receipt=selected.candidate_receipt,
        verification_evidence=execution.independent_verification_evidence,
        verification_policy=independent_policy,
    )
    assert independent.status == INDEPENDENT_STATUS_READY, independent.issues
    assert independent.receipt is not None
    assert independent.receipt["candidate_verification_passed"] is True
    print("PASS: generation -> selection -> isolated application -> bounded verification execution -> independent verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
