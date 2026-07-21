from __future__ import annotations

import json

from runtime.kuuos_codeai_independent_verifier_ensemble_schema_v0_2 import (
    ENSEMBLE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
)
from runtime.kuuos_codeai_independent_verifier_ensemble_v0_2 import evaluate_independent_verifier_ensemble
from scripts.build_codeai_independent_verifier_ensemble_fixture_v0_2 import build_fixture


def project() -> dict:
    fixture = build_fixture()
    result = evaluate_independent_verifier_ensemble(**fixture)
    assert result.ensemble is not None and result.receipt is not None
    return {
        "codeai_disposition": result.receipt["codeai_disposition"],
        "operating_mode": result.receipt["operating_mode"],
        "source_commit_sha": result.receipt["source_commit_sha"],
        "request_digest": fixture["request"][REQUEST_DIGEST_FIELD],
        "policy_digest": fixture["policy"][POLICY_DIGEST_FIELD],
        "ensemble_digest": result.ensemble[ENSEMBLE_DIGEST_FIELD],
        "receipt_digest": result.receipt[RECEIPT_DIGEST_FIELD],
        "verifier_count": result.ensemble["verifier_count"],
        "organization_count": result.ensemble["organization_count"],
        "method_count": result.ensemble["method_count"],
        "covered_check_families": result.ensemble["covered_check_families"],
        "pass_count": result.ensemble["pass_count"],
        "fail_count": result.ensemble["fail_count"],
        "inconclusive_count": result.ensemble["inconclusive_count"],
        "critical_failure_count": result.ensemble["critical_failure_count"],
        "conflict_detected": result.ensemble["conflict_detected"],
        "consensus_outcome": result.ensemble["consensus_outcome"],
        "verification_debt_open": result.receipt["verification_debt_open"],
        "candidate_selection_authority": result.receipt["candidate_selection_authority"],
        "execution_authority": result.receipt["execution_authority"],
        "git_authority": result.receipt["git_authority"],
        "correctness_proof": result.receipt["correctness_proof"],
    }


if __name__ == "__main__":
    print(json.dumps(project(), indent=2, sort_keys=True))
