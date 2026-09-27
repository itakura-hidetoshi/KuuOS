#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    DISPOSITION_SUPPORTED,
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    seal as candidate_seal,
)
from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
    MODE_PREFLIGHT_ONLY,
    RECEIPT_DIGEST_FIELD as PREFLIGHT_RECEIPT_DIGEST_FIELD,
    seal as preflight_seal,
)
from runtime.kuuos_runtime_semantic_first_repair_loop_v7_20 import (
    CANDIDATE_GENERATION_READY,
    CANDIDATE_HOLD,
    CANDIDATE_NO_IMPROVEMENT,
    CANDIDATE_PREFLIGHT_READY,
    CANDIDATE_REGRESSION,
    CANDIDATE_REJECTED,
    CANDIDATE_REPAIR_FEEDBACK,
    GIT_DIFF_REVIEW_READY,
    LEAN_REOBSERVE,
    LINEAGE_OBSTRUCTION,
    LOCAL_APPLICATION_CANDIDATE,
    LOCAL_GIT_ADMISSION_REQUIRED,
    NO_REPAIR_NEEDED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    REMOTE_RECONCILIATION_REQUIRED,
    REMOTE_SUBMISSION_CANDIDATE,
    build_semantic_first_repair_loop,
)

PLAN = "semantic_first_repair_loop_plan_v7_20.json"
FEDERATION = "development_mcp_federation_packet_v7_19.json"
OBS = "semantic_first_repair_observation_v7_20.json"
OUT = "semantic_first_repair_loop_packet_v7_20.json"


def h(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def plan() -> dict[str, Any]:
    return {
        "version": "kuuos_semantic_first_repair_loop_plan_v7_20",
        "semantic_improvement_grants_local_write_authority": False,
        "semantic_improvement_grants_remote_write_authority": False,
        "stale_diagnostic_may_apply_patch": False,
        "candidate_receipt_is_current_byte_binding": False,
        "static_preflight_is_correctness_proof": False,
        "candidate_rejection_erases_local_worktree": False,
        "remote_revision_mismatch_blocks_local_repair": False,
        "source_authority_transferred": False,
        "candidate_patch_bound_to_before_digest": True,
        "lean_observation_bound_to_source_digest": True,
        "candidate_result_requires_fresh_shadow_semantics": True,
        "remote_submission_requires_git_diff_review": True,
        "remote_submission_requires_revision_alignment": True,
        "remote_submission_requires_separate_authority_after_this_layer": True,
        "dirty_worktree_may_continue_semantic_repair": True,
    }


def authority() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_SEMANTIC_FIRST_REPAIR_LOOP_AUTHORITY_READY",
        "plan_read_allowed": True,
        "federation_packet_read_allowed": True,
        "repair_observation_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "semantic_first_repair_loop_enabled": True,
        "apply_semantic_first_repair_loop": True,
    }


def semantics(content_digest: str, *, errors: int, warnings: int = 0) -> dict[str, Any]:
    return {
        "source_content_digest": content_digest,
        "diagnostics_digest": h({"content": content_digest, "errors": errors, "warnings": warnings}),
        "error_count": errors,
        "warning_count": warnings,
        "goal_digest": h({"goal": content_digest}) if errors else "",
        "semantic_observation_digest": h(
            {"source": content_digest, "errors": errors, "warnings": warnings}
        ),
    }


def federation(
    content_digest: str,
    *,
    target: str = "formal/KUOS/Example.lean",
    clean: bool = False,
    remote_aligned: bool = True,
    local_allowed: bool = True,
    remote_eligible: bool = True,
) -> dict[str, Any]:
    return {
        "version": "kuuos_runtime_development_mcp_federation_v7_19",
        "status": "KUUOS_DEVELOPMENT_MCP_FEDERATION_READY",
        "workspace_state": "dirty_local_candidate_semantically_fresh",
        "workspace": {
            "target_path": target,
            "filesystem_content_digest": content_digest,
            "local_semantic_work_allowed": local_allowed,
            "remote_local_aligned": remote_aligned,
            "worktree_clean": clean,
            "remote_mutation_eligible_before_authority_check": remote_eligible,
        },
        "federation_boundary": {
            "dirty_worktree_is_error": False,
        },
    }


def candidate_receipt(*, corrupt: bool = False) -> dict[str, Any]:
    value = {
        "candidate_patch_ready": True,
        "codeai_disposition": DISPOSITION_SUPPORTED,
        "operating_mode": "proposal_only",
        "route_receipt_recorded": True,
        "execution_lease_issued": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
    }
    receipt = candidate_seal(value, CANDIDATE_RECEIPT_DIGEST_FIELD)
    if corrupt:
        receipt[CANDIDATE_RECEIPT_DIGEST_FIELD] = "0" * 64
    return receipt


def preflight_receipt(disposition: str) -> dict[str, Any]:
    value = {
        "codeai_disposition": disposition,
        "operating_mode": MODE_PREFLIGHT_ONLY,
        "route_receipt_recorded": True,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "candidate_selected": False,
        "candidate_selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "static_preflight_treated_as_correctness_proof": False,
    }
    return preflight_seal(value, PREFLIGHT_RECEIPT_DIGEST_FIELD)


def candidate(
    before: str,
    result: str,
    *,
    before_errors: int,
    result_errors: int | None = None,
    disposition: str | None = DISPOSITION_ADMISSIBLE,
    git_diff_reviewed: bool = False,
    corrupt_receipt: bool = False,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "before_content_digest": before,
        "result_content_digest": result,
        "before_error_count": before_errors,
        "candidate_patch_receipt": candidate_receipt(corrupt=corrupt_receipt),
        "static_preflight_receipt": (
            preflight_receipt(disposition) if disposition is not None else {}
        ),
        "git_diff_reviewed": git_diff_reviewed,
        "git_diff_digest": h({"before": before, "result": result})
        if git_diff_reviewed
        else "",
    }
    if result_errors is not None:
        value["shadow_semantics"] = semantics(result, errors=result_errors)
    return value


def observation(
    current: str,
    *,
    errors: int,
    target: str = "formal/KUOS/Example.lean",
    candidate_value: dict[str, Any] | None = None,
    semantic_source: str | None = None,
) -> dict[str, Any]:
    return {
        "version": "kuuos_semantic_first_repair_observation_v7_20",
        "target_path": target,
        "current_content_digest": current,
        "current_semantics": semantics(
            semantic_source if semantic_source is not None else current,
            errors=errors,
        ),
        "candidate": candidate_value or {},
    }


def write(
    root: pathlib.Path,
    *,
    federation_packet: dict[str, Any],
    repair_observation: dict[str, Any],
) -> None:
    (root / PLAN).write_text(json.dumps(plan()), encoding="utf-8")
    (root / FEDERATION).write_text(json.dumps(federation_packet), encoding="utf-8")
    (root / OBS).write_text(json.dumps(repair_observation), encoding="utf-8")


def run(root: pathlib.Path):
    return build_semantic_first_repair_loop(
        runtime_context=ctx(root),
        authority_packet=authority(),
    )


def out(root: pathlib.Path) -> dict[str, Any]:
    return json.loads((root / OUT).read_text())


def test_errors_with_no_candidate_routes_to_generation() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        current = h("broken")
        write(
            root,
            federation_packet=federation(current),
            repair_observation=observation(current, errors=2),
        )
        result = run(root)
        assert result.status == READY, result.to_dict()
        assert result.route == CANDIDATE_GENERATION_READY
        assert result.local_semantic_work_allowed is True


def test_stale_lean_diagnostic_routes_to_reobservation() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        current = h("edited-v2")
        write(
            root,
            federation_packet=federation(current),
            repair_observation=observation(
                current,
                errors=2,
                semantic_source=h("edited-v1"),
            ),
        )
        result = run(root)
        assert result.status == PARTIAL
        assert result.route == LEAN_REOBSERVE
        assert result.local_application_authority_granted is False


def test_candidate_without_preflight_routes_to_static_preflight() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        result_digest = h("candidate")
        write(
            root,
            federation_packet=federation(before),
            repair_observation=observation(
                before,
                errors=2,
                candidate_value=candidate(
                    before,
                    result_digest,
                    before_errors=2,
                    disposition=None,
                ),
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.route == CANDIDATE_PREFLIGHT_READY


def test_repairable_preflight_preserves_codeai_repair_route() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        result_digest = h("candidate")
        write(
            root,
            federation_packet=federation(before),
            repair_observation=observation(
                before,
                errors=2,
                candidate_value=candidate(
                    before,
                    result_digest,
                    before_errors=2,
                    disposition=DISPOSITION_REPAIRABLE,
                ),
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.route == CANDIDATE_REPAIR_FEEDBACK


def test_hold_and_reject_are_not_collapsed() -> None:
    for disposition, expected in (
        (DISPOSITION_HOLD, CANDIDATE_HOLD),
        (DISPOSITION_REJECTED, CANDIDATE_REJECTED),
    ):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            before = h("broken")
            result_digest = h("candidate")
            write(
                root,
                federation_packet=federation(before),
                repair_observation=observation(
                    before,
                    errors=2,
                    candidate_value=candidate(
                        before,
                        result_digest,
                        before_errors=2,
                        disposition=disposition,
                    ),
                ),
            )
            result = run(root)
            assert result.status == READY
            assert result.route == expected


def test_admissible_semantically_improved_shadow_becomes_local_application_candidate() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        result_digest = h("fixed")
        write(
            root,
            federation_packet=federation(before),
            repair_observation=observation(
                before,
                errors=3,
                candidate_value=candidate(
                    before,
                    result_digest,
                    before_errors=3,
                    result_errors=0,
                ),
            ),
        )
        result = run(root)
        assert result.status == READY, result.to_dict()
        assert result.route == LOCAL_APPLICATION_CANDIDATE
        assert result.semantic_improvement is True
        assert result.local_application_authority_granted is False
        assert result.remote_mutation_authority_granted is False
        packet = out(root)
        assert packet["semantic_first_boundary"][
            "semantic_improvement_grants_local_write_authority"
        ] is False


def test_semantic_regression_and_no_improvement_are_typed() -> None:
    for post_errors, expected in (
        (4, CANDIDATE_REGRESSION),
        (3, CANDIDATE_NO_IMPROVEMENT),
    ):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            before = h("broken")
            result_digest = h({"post": post_errors})
            write(
                root,
                federation_packet=federation(before),
                repair_observation=observation(
                    before,
                    errors=3,
                    candidate_value=candidate(
                        before,
                        result_digest,
                        before_errors=3,
                        result_errors=post_errors,
                    ),
                ),
            )
            result = run(root)
            assert result.status == READY
            assert result.route == expected


def test_applied_candidate_requires_git_diff_review_before_remote_submission() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        applied = h("fixed")
        write(
            root,
            federation_packet=federation(applied, remote_eligible=True),
            repair_observation=observation(
                applied,
                errors=0,
                candidate_value=candidate(
                    before,
                    applied,
                    before_errors=2,
                    result_errors=0,
                    git_diff_reviewed=False,
                ),
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.route == GIT_DIFF_REVIEW_READY


def test_reviewed_candidate_needs_remote_reconciliation_when_head_diverged() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        applied = h("fixed")
        write(
            root,
            federation_packet=federation(
                applied,
                remote_aligned=False,
                remote_eligible=False,
            ),
            repair_observation=observation(
                applied,
                errors=0,
                candidate_value=candidate(
                    before,
                    applied,
                    before_errors=2,
                    result_errors=0,
                    git_diff_reviewed=True,
                ),
            ),
        )
        result = run(root)
        assert result.status == PARTIAL
        assert result.route == REMOTE_RECONCILIATION_REQUIRED
        assert result.local_semantic_work_allowed is True


def test_reviewed_aligned_candidate_becomes_remote_submission_candidate_not_authority() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        applied = h("fixed")
        write(
            root,
            federation_packet=federation(
                applied,
                remote_aligned=True,
                remote_eligible=True,
            ),
            repair_observation=observation(
                applied,
                errors=0,
                candidate_value=candidate(
                    before,
                    applied,
                    before_errors=2,
                    result_errors=0,
                    git_diff_reviewed=True,
                ),
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.route == REMOTE_SUBMISSION_CANDIDATE
        assert result.remote_mutation_authority_granted is False


def test_untracked_or_unadmitted_candidate_requires_local_git_admission() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("new-broken")
        applied = h("new-fixed")
        write(
            root,
            federation_packet=federation(
                applied,
                remote_aligned=True,
                remote_eligible=False,
            ),
            repair_observation=observation(
                applied,
                errors=0,
                candidate_value=candidate(
                    before,
                    applied,
                    before_errors=1,
                    result_errors=0,
                    git_diff_reviewed=True,
                ),
            ),
        )
        result = run(root)
        assert result.status == PARTIAL
        assert result.route == LOCAL_GIT_ADMISSION_REQUIRED


def test_corrupt_codeai_candidate_receipt_is_lineage_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        before = h("broken")
        result_digest = h("candidate")
        write(
            root,
            federation_packet=federation(before),
            repair_observation=observation(
                before,
                errors=2,
                candidate_value=candidate(
                    before,
                    result_digest,
                    before_errors=2,
                    result_errors=0,
                    corrupt_receipt=True,
                ),
            ),
        )
        result = run(root)
        assert result.status == OBSTRUCTED
        assert result.route == LINEAGE_OBSTRUCTION


def test_zero_error_clean_workspace_needs_no_repair() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        current = h("good")
        write(
            root,
            federation_packet=federation(current, clean=True),
            repair_observation=observation(current, errors=0),
        )
        result = run(root)
        assert result.status == READY
        assert result.route == NO_REPAIR_NEEDED


def main() -> int:
    test_errors_with_no_candidate_routes_to_generation()
    test_stale_lean_diagnostic_routes_to_reobservation()
    test_candidate_without_preflight_routes_to_static_preflight()
    test_repairable_preflight_preserves_codeai_repair_route()
    test_hold_and_reject_are_not_collapsed()
    test_admissible_semantically_improved_shadow_becomes_local_application_candidate()
    test_semantic_regression_and_no_improvement_are_typed()
    test_applied_candidate_requires_git_diff_review_before_remote_submission()
    test_reviewed_candidate_needs_remote_reconciliation_when_head_diverged()
    test_reviewed_aligned_candidate_becomes_remote_submission_candidate_not_authority()
    test_untracked_or_unadmitted_candidate_requires_local_git_admission()
    test_corrupt_codeai_candidate_receipt_is_lineage_obstruction()
    test_zero_error_clean_workspace_needs_no_repair()
    print("PASS: KuuOS Semantic-First Repair Loop v7.20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
