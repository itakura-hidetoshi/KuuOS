from __future__ import annotations

import copy
from typing import Any

from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    POLICY_DIGEST_FIELD,
    PREFLIGHT_RECEIPT_DIGEST_FIELD,
    PREFLIGHT_REPORT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    seal,
)
from tests import test_kuuos_codeai_candidate_static_admissibility_preflight_v0_1 as preflight_tests


def _preflight_result(mode: str):
    data = preflight_tests.fixture()
    if mode == "repairable":
        preflight_tests.set_text(data, "def greet(:\n")
    elif mode == "hold":
        preflight_tests.set_text(
            data,
            "import requests\n\ndef greet(name: str) -> str:\n    return name\n",
        )
    elif mode == "rejected":
        operation = copy.deepcopy(data["typed_edit_ir"]["operations"][0])
        operation["operation_id"] = "second"
        operation["application_sequence"] = 2
        data["typed_edit_ir"]["operations"].append(operation)
        preflight_tests.reseal(data)
    elif mode != "admissible":
        raise ValueError("unsupported candidate mode: " + mode)
    result = preflight_tests.run(data)
    if result.report is None or result.receipt is None:
        raise ValueError("preflight fixture blocked: " + ",".join(result.issues))
    return result


def build_fixture(spec: dict[str, Any]) -> dict[str, Any]:
    bundles = []
    request_items = []
    for candidate in spec["candidates"]:
        result = _preflight_result(candidate["mode"])
        bundle = {
            "candidate_id": candidate["candidate_id"],
            "preflight_report": result.report,
            "preflight_receipt": result.receipt,
        }
        bundles.append(bundle)
        request_items.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate_sequence": candidate["candidate_sequence"],
                "expected_typed_edit_ir_digest": result.report["typed_edit_ir_digest"],
                "expected_static_admissibility_report_digest": result.report[PREFLIGHT_REPORT_DIGEST_FIELD],
                "expected_preflight_receipt_digest": result.receipt[PREFLIGHT_RECEIPT_DIGEST_FIELD],
            }
        )

    first_report = bundles[0]["preflight_report"]
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Evidence-Bearing Candidate Portfolio v0.1",
            "portfolio_id": spec["portfolio_id"],
            "portfolio_revision": spec["portfolio_revision"],
            "repository_full_name": first_report["repository_full_name"],
            "source_commit_sha": first_report["source_commit_sha"],
            "source_repository_snapshot_digest": first_report["source_repository_snapshot_digest"],
            "request_created_epoch": spec["request_created_epoch"],
            "candidate_requests": request_items,
            "claims_authority": False,
            "unresolved_portfolio_questions": [],
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Evidence-Bearing Candidate Portfolio v0.1",
            "expected_repository_full_name": first_report["repository_full_name"],
            "expected_source_commit_sha": first_report["source_commit_sha"],
            "expected_source_repository_snapshot_digest": first_report["source_repository_snapshot_digest"],
            "evaluation_epoch": spec["evaluation_epoch"],
            "maximum_request_age": spec["maximum_request_age"],
            "maximum_candidates": spec["maximum_candidates"],
            "maximum_total_findings": spec["maximum_total_findings"],
            "maximum_total_changed_paths": spec["maximum_total_changed_paths"],
            "require_exact_lineage": True,
            "require_classification_preservation": True,
            "require_finding_evidence_preservation": True,
            "allow_ranking": False,
            "allow_candidate_selection": False,
            "allow_verification_runner_invocation": False,
            "allow_repair_execution": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return {
        "portfolio_request": request,
        "portfolio_policy": policy,
        "candidate_preflight_bundles": bundles,
    }
