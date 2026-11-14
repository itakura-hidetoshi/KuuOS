"""Fail-closed, source-bound *precommit* gate for CodeAI Lean candidates.

It assesses observed CodeAI, Lean MCP, and pinned direct Lean evidence. It
never compiles, patches, mutates Git or promotes a local result to independent
repository CI certification. Valid evidence is necessary, not merge authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_lean_mcp_precommit_gate_v0_1"
STATUS_READY = "LOCAL_PRECOMMIT_MCP_AND_DIRECT_LEAN_GREEN"
STATUS_BLOCKED = "LOCAL_PRECOMMIT_NOT_CERTIFIED"
RECEIPT_FIELD = "codeai_lean_mcp_precommit_gate_receipt_digest"
_SHA40 = re.compile(r"^[a-f0-9]{40}$")
_SHA64 = re.compile(r"^[a-f0-9]{64}$")


def digest(data: Any) -> str:
    """CodeAI's canonical JSON digest (receipts and snapshot strings)."""
    return hashlib.sha256(json.dumps(
        data, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _mapping(obj: Any) -> Mapping[str, Any]:
    return obj if isinstance(obj, Mapping) else {}


def _receipt(obj: Mapping[str, Any], field: str, issues: list[str], prefix: str) -> bool:
    if not obj or not isinstance(obj.get(field), str) or not _SHA64.fullmatch(obj[field]):
        issues.append(prefix + ":receipt_missing")
        return False
    if obj[field] != digest({k: v for k, v in obj.items() if k != field}):
        issues.append(prefix + ":receipt_digest_mismatch")
        return False
    return True


@dataclass(frozen=True)
class GateResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any]


def evaluate(
    *, codeai_record: Any, mcp_precommit_record: Any,
    source: bytes, candidate: bytes, target: str,
    source_head: str, source_git_tree: str, direct_lean_log: str,
) -> GateResult:
    """Evaluate exact evidence; do not infer unavailable Lean results.

    Caller obtains source_head/tree from authenticated GitHub PR observations
    and checks all changed sources with the existing full-source scanner.
    """
    issues: list[str] = []
    codeai = _mapping(codeai_record)
    checked = _mapping(mcp_precommit_record)
    if not _SHA40.fullmatch(source_head) or not _SHA40.fullmatch(source_git_tree):
        issues.append("source_head_or_tree_not_exact_sha")
    if not isinstance(target, str) or not target.startswith("formal/") or not target.endswith(".lean"):
        issues.append("not_a_formal_lean_target")
    source_sha, candidate_sha = sha256(source), sha256(candidate)
    old_blob, new_blob = git_blob(source), git_blob(candidate)
    if old_blob == new_blob:
        issues.append("candidate_is_semantic_noop")
    if codeai.get("source_head") != source_head or checked.get("source_head") != source_head:
        issues.append("source_head_mismatch")
    if codeai.get("source_git_tree") != source_git_tree:
        issues.append("source_git_tree_mismatch")
    if codeai.get("source_blob") != old_blob or checked.get("source_git_blob") != old_blob:
        issues.append("source_git_blob_mismatch")
    if codeai.get("candidate_blob") != new_blob or checked.get("codeai_candidate_git_blob") != new_blob:
        issues.append("candidate_git_blob_mismatch")
    if codeai.get("source_repo") != "itakura-hidetoshi/KuuOS":
        issues.append("repository_identity_mismatch")
    if codeai.get("git_effect") is not False or checked.get("git_write_performed") is not False:
        issues.append("unexpected_git_effect")

    field_specs = (
        ("source_observation_receipt", "codeai_intent_repository_observation_receipt_digest"),
        ("candidate_receipt", "codeai_candidate_patch_receipt_digest"),
        ("generated_candidate_receipt", "codeai_autonomous_unified_diff_candidates_receipt_digest"),
        ("selection_receipt", "codeai_autonomous_candidate_selection_receipt_digest"),
        ("isolated_application_receipt", "codeai_autonomous_isolated_candidate_application_receipt_digest"),
    )
    parts: dict[str, Mapping[str, Any]] = {}
    for name, field in field_specs:
        value = _mapping(codeai.get(name))
        parts[name] = value
        _receipt(value, field, issues, name)
    observation = parts["source_observation_receipt"]
    patch = parts["candidate_receipt"]
    generated = parts["generated_candidate_receipt"]
    selected = parts["selection_receipt"]
    applied = parts["isolated_application_receipt"]

    obs_id = observation.get("codeai_intent_repository_observation_receipt_digest")
    patch_id = patch.get("codeai_candidate_patch_receipt_digest")
    portfolio_id = generated.get("codeai_autonomous_unified_diff_candidates_receipt_digest")
    selection_id = selected.get("codeai_autonomous_candidate_selection_receipt_digest")
    application_id = applied.get("codeai_autonomous_isolated_candidate_application_receipt_digest")
    if observation.get("source_commit_sha") != source_head or observation.get("tree_digest") != source_git_tree:
        issues.append("CodeAI_observation_source_mismatch")
    if patch.get("source_observation_receipt_digest") != obs_id or patch.get("source_commit_sha") != source_head:
        issues.append("CodeAI_candidate_lineage_mismatch")
    if patch.get("codeai_disposition") != "candidate_patch_supported" or patch.get("patch_candidate_only") is not True:
        issues.append("CodeAI_candidate_not_proposal_supported")
    if generated.get("source_observation_receipt_digest") != obs_id:
        issues.append("CodeAI_generation_source_mismatch")
    if patch.get("candidate_patch_digest") not in generated.get("generated_candidate_digests", []):
        issues.append("CodeAI_candidate_not_in_generated_portfolio")
    if selected.get("source_portfolio_receipt_digest") != portfolio_id or selected.get("selected_candidate_digest") != patch.get("candidate_patch_digest"):
        issues.append("CodeAI_selection_lineage_mismatch")
    if selected.get("selected_patch_artifact_digest") != patch.get("patch_artifact_digest") or selected.get("candidate_selected") is not True:
        issues.append("CodeAI_selection_not_verified")
    if applied.get("source_selection_receipt_digest") != selection_id or applied.get("source_candidate_receipt_digest") != patch_id:
        issues.append("CodeAI_isolated_lineage_mismatch")
    if applied.get("source_commit_sha") != source_head or applied.get("repository_full_name") != "itakura-hidetoshi/KuuOS":
        issues.append("CodeAI_isolated_source_mismatch")
    if applied.get("changed_paths") != [target] or applied.get("modified_paths") != [target] or applied.get("added_paths") != [] or applied.get("deleted_paths") != []:
        issues.append("CodeAI_isolated_changed_path_mismatch")
    for key in ("isolated_patch_applied", "isolated_snapshot_materialized", "source_snapshot_verified", "selection_correspondence_verified"):
        if applied.get(key) is not True:
            issues.append("CodeAI_isolated_required_flag_missing:" + key)
    for key in ("repository_mutation_performed", "git_ref_changed", "live_repository_patch_applied", "verification_executed", "merge_performed"):
        if applied.get(key) is not False:
            issues.append("CodeAI_isolated_forbidden_flag:" + key)
    expected_src = digest({target: source.decode("utf-8")})
    expected_dst = digest({target: candidate.decode("utf-8")})
    if applied.get("source_repository_snapshot_digest") != expected_src or applied.get("resulting_repository_snapshot_digest") != expected_dst:
        issues.append("CodeAI_isolated_source_or_candidate_snapshot_mismatch")
    changed_digests = applied.get("resulting_changed_path_digests", [])
    if changed_digests != [{"path": target, "content_digest": digest(candidate.decode("utf-8"))}]:
        issues.append("CodeAI_isolated_candidate_text_digest_mismatch")
    if checked.get("codeai_receipt") != application_id:
        issues.append("CodeAI_isolation_receipt_not_sealed_in_MCP_record")

    if checked.get("full_source_status") != "SOURCE_OBSERVATION_READY":
        issues.append("full_source_or_import_closure_unverified")
    if checked.get("lean_mcp_status") != "LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY":
        issues.append("lean_mcp_direct_observation_not_green")
    for key in ("imports_unchanged", "source_signature_unchanged", "source_restored_by_mcp", "source_restored_final"):
        if checked.get(key) is not True:
            issues.append("Lean_MCP_source_or_interface_guard_failed:" + key)
    if checked.get("new_forbidden_constructs") is not False:
        issues.append("Lean_MCP_forbidden_constructs_not_certified_absent")
    local = _mapping(checked.get("mcp_local_receipt"))
    if local.get("status") != "LOCAL_LEAN_GREEN_CANDIDATE_ONLY":
        issues.append("Lean_MCP_candidate_kernel_not_green")
    if local.get("original_sha256") != source_sha or local.get("candidate_sha256") != candidate_sha or local.get("source_restored") is not True:
        issues.append("Lean_MCP_source_or_candidate_sha_mismatch")
    if local.get("independent_ci_success") is not False or local.get("git_write_performed") is not False:
        issues.append("Lean_MCP_unexpected_authority_claim")
    rounds = local.get("rounds")
    if not isinstance(rounds, list) or len(rounds) < 2:
        issues.append("Lean_MCP_missing_pre_and_post_elaboration")
    else:
        if not any(r.get("goal_digest") and isinstance(r.get("preliminary_tactic_details"), list)
                   and len(r["preliminary_tactic_details"]) > 0 for r in rounds if isinstance(r, Mapping)):
            issues.append("Lean_MCP_goal_or_multi_attempt_absent")
        last = _mapping(rounds[-1])
        if last.get("semantic_success") is not True or last.get("partial") is not False or last.get("errors") != 0 or last.get("source_sha256") != candidate_sha:
            issues.append("Lean_MCP_final_diagnostics_not_verified_on_candidate")
        direct = _mapping(last.get("direct_lean"))
        if direct.get("exit_code") != 0:
            issues.append("Lean_MCP_local_direct_lean_gate_not_green")
        if last.get("forbidden_final_count") != 0:
            issues.append("Lean_MCP_final_forbidden_markers")

    if checked.get("strict_lean_status") != "SUCCESS" or checked.get("strict_lean_returncode") != 0:
        issues.append("independent_direct_strict_Lean_not_green")
    if checked.get("strict_candidate_log_sha256") != sha256(direct_lean_log.encode("utf-8")):
        issues.append("independent_direct_strict_log_digest_mismatch")
    if "error:" in direct_lean_log or "sorryAx" in direct_lean_log:
        issues.append("independent_direct_strict_log_contains_errors_or_sorryAx")

    passed = not issues
    output: dict[str, Any] = {
        "schema_version": "v0.1",
        "profile": VERSION,
        "source_repo": "itakura-hidetoshi/KuuOS",
        "source_head": source_head,
        "source_git_tree": source_git_tree,
        "target": target,
        "original_git_blob": old_blob,
        "candidate_git_blob": new_blob,
        "original_sha256": source_sha,
        "candidate_sha256": candidate_sha,
        "source_observation_receipt_digest": obs_id,
        "codeai_isolated_application_receipt_digest": application_id,
        "mcp_source_sha256": local.get("original_sha256"),
        "mcp_candidate_sha256": local.get("candidate_sha256"),
        "direct_lean_log_sha256": checked.get("strict_candidate_log_sha256"),
        "status": STATUS_READY if passed else STATUS_BLOCKED,
        "issues": sorted(set(issues)),
        "local_precommit_evidence_passed": passed,
        "independent_ci_certified": False,
        "merge_authority_granted": False,
        "repository_mutation_performed": False,
        "git_write_performed": False,
    }
    output[RECEIPT_FIELD] = digest(output)
    return GateResult(output["status"], tuple(output["issues"]), output)
