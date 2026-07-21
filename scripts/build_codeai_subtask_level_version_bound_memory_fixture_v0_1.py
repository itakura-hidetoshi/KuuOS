from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_subtask_level_version_bound_memory_v0_1 import *

SOURCE_COMMIT = "2e3801430959946c1d2ecc784cf9e37dab139632"
CONTEXT_PACK_DIGEST = "9f8d9d91bd51ee67ef93ff5b45274cbc4b1e303073d60795381f7154f307966c"
VERIFIER_ENSEMBLE_DIGEST = "6faaa86813a1d72f9f12301024999b7c254a723135e6eb0e70e60da4a45cb218"
TEMPORAL_CORPUS_DIGEST = canonical_digest({"stage": "temporal-holdout-replay-corpus-v0.1", "frozen": True})
TREE_DIGEST = canonical_digest({"repository": "itakura-hidetoshi/KuuOS", "commit": SOURCE_COMMIT})
TOOLCHAIN_DIGEST = canonical_digest({"lean": "v4.30.0-rc2", "python": "3.12"})
ENVIRONMENT_DIGEST = canonical_digest({"runner": "ubuntu-22.04", "network": False})
MEMORY_POLICY_DIGEST = canonical_digest({"policy": PROFILE_VERSION, "mode": "exact-subtask-only"})
VERIFY_CONTRACT = canonical_digest({"subtask": "verify", "requires": ["ensemble", "context", "holdout-protection"]})
VERIFY_PREDECESSOR = canonical_digest({"subtask": "edit", "output": "candidate-patch"})
VERIFY_DEPENDENCY = canonical_digest({"paths": ["runtime/memory.py", "formal/Memory.lean", "tests/test_memory.py"]})


def _digest(label: str) -> str:
    return canonical_digest({"label": label})


def _binding(kind: str, *, commit: str = SOURCE_COMMIT, contract: str | None = None,
             predecessor: str | None = None, dependency: str | None = None) -> dict[str, Any]:
    defaults = {
        "localize": (_digest("localize-contract"), _digest("task-root"), _digest("repo-index")),
        "diagnose": (_digest("diagnose-contract"), _digest("localized-slice"), _digest("diagnostic-slice")),
        "edit": (_digest("edit-contract"), _digest("typed-diagnosis"), _digest("edit-slice")),
        "verify": (VERIFY_CONTRACT, VERIFY_PREDECESSOR, VERIFY_DEPENDENCY),
    }
    d_contract, d_predecessor, d_dependency = defaults[kind]
    return {
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "source_commit_sha": commit,
        "source_tree_digest": TREE_DIGEST if commit == SOURCE_COMMIT else _digest("stale-tree"),
        "temporal_corpus_digest": TEMPORAL_CORPUS_DIGEST,
        "context_pack_digest": CONTEXT_PACK_DIGEST,
        "verifier_ensemble_digest": VERIFIER_ENSEMBLE_DIGEST,
        "subtask_kind": kind,
        "subtask_contract_digest": contract or d_contract,
        "predecessor_output_digest": predecessor or d_predecessor,
        "dependency_slice_digest": dependency or d_dependency,
        "toolchain_digest": TOOLCHAIN_DIGEST,
        "environment_digest": ENVIRONMENT_DIGEST,
        "memory_policy_digest": MEMORY_POLICY_DIGEST,
    }


def _entry(entry_id: str, kind: str, *, outcome: str = OUTCOME_VERIFIED_USEFUL,
           holdout: bool = False, superseded: bool = False, epoch: int = 1784640000,
           **binding_overrides: Any) -> dict[str, Any]:
    entry = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "entry_id": entry_id,
        "entry_revision": "r1",
        **_binding(kind, **binding_overrides),
        "outcome": outcome,
        "evidence_created_epoch": epoch,
        "subtask_summary": f"Verified reusable {kind} procedure",
        "input_artifact_digest": _digest(entry_id + ":input"),
        "output_artifact_digest": _digest(entry_id + ":output"),
        "verification_evidence_digest": _digest(entry_id + ":verification"),
        "derived_from_holdout": holdout,
        "superseded": superseded,
        "repository_mutation_performed": False,
        "candidate_selected": False,
        "repair_executed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "future_success_claimed": False,
    }
    return seal(entry, ENTRY_DIGEST_FIELD)


def build_reference_fixture() -> dict[str, Any]:
    request = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "subtask-memory-request-001",
        "request_revision": "r1",
        **_binding("verify"),
        "request_created_epoch": 1784640010,
        "unresolved_questions": [],
        "claims_selection_authority": False,
        "claims_repair_authority": False,
        "claims_execution_authority": False,
        "claims_git_authority": False,
    }
    request = seal(request, REQUEST_DIGEST_FIELD)

    policy = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + field: request[field] for field in VERSION_BINDING_FIELDS},
        "evaluation_epoch": 1784640020,
        "maximum_request_age": 3600,
        "maximum_entry_age": 86400,
        "maximum_corpus_entries": 16,
        "maximum_matched_entries": 2,
        "allowed_outcomes": [OUTCOME_VERIFIED_USEFUL],
        "required_subtask_kinds": list(SUBTASK_KINDS),
        "require_exact_version_binding": True,
        "require_subtask_alignment": True,
        "require_dependency_alignment": True,
        "require_verifier_grounding": True,
        "require_holdout_protection": True,
        "require_not_superseded": True,
        "allow_memory_hint": True,
        "allow_repository_mutation": False,
        "allow_candidate_selection": False,
        "allow_repair_execution": False,
        "allow_execution_authority": False,
        "allow_git_authority": False,
    }
    policy = seal(policy, POLICY_DIGEST_FIELD)

    entries = [
        _entry("memory-localize-001", "localize"),
        _entry("memory-diagnose-001", "diagnose"),
        _entry("memory-edit-001", "edit"),
        _entry("memory-verify-current-001", "verify"),
        _entry("memory-verify-stale-001", "verify", commit="7566e188174d8e36880b6cfbc77fe164d0637f9c"),
        _entry("memory-verify-dependency-001", "verify", dependency=_digest("different-dependency-slice")),
        _entry("memory-verify-holdout-001", "verify", holdout=True),
        _entry("memory-verify-superseded-001", "verify", superseded=True),
        _entry("memory-verify-inconclusive-001", "verify", outcome=OUTCOME_INCONCLUSIVE),
    ]
    corpus = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "corpus_id": "subtask-memory-corpus-001",
        "corpus_revision": "r1",
        "repository_full_name": request["repository_full_name"],
        "temporal_corpus_digest": request["temporal_corpus_digest"],
        "context_pack_digest": request["context_pack_digest"],
        "verifier_ensemble_digest": request["verifier_ensemble_digest"],
        "entries": entries,
    }
    corpus = seal(corpus, CORPUS_DIGEST_FIELD)
    result = build_codeai_subtask_level_version_bound_memory(
        request=request, policy=policy, corpus=corpus
    )
    if result.status != STATUS_READY or result.memory_pack is None or result.receipt is None:
        raise RuntimeError(result.issues)
    return {
        "request": request, "policy": policy, "corpus": corpus,
        "memory_pack": result.memory_pack, "receipt": result.receipt,
    }


def deep_reference_fixture() -> dict[str, Any]:
    return deepcopy(build_reference_fixture())


__all__ = ["build_reference_fixture", "deep_reference_fixture"]
