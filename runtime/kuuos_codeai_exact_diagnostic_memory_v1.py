"""Read-only exact compiler diagnostic recall, separate from verified-useful memory.

The immutable packet records a *particular* failed candidate and separately
verified alternatives. An external caller must freshly observe canonical main
and its proof scope. The current local proof corpus, selected historical type
and source blob are independently checked by the existing v0.5 recall.
A metadata-only HEAD change may match the exact proof scope; the historical
HEAD is never relabelled. No novelty, repair, execution or merge authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from collections.abc import Mapping
from typing import Any

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import recall_kernel_memory
from runtime.kuuos_codeai_prior_proof_recall_gate_v0_1 import digest, git_blob
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import (
    REQUEST_DIGEST_FIELD, digest_ok, seal,
)
from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import SOURCE_RECEIPT_DIGEST_FIELD
from scripts.ci_verified_lean_project_cache_v1 import make_scope

PACKET_PATH = "memoryos/codeai_exact_diagnostic_observation_v1.json"
PACKET_BLOB = "499eaafc7724cb77d82d2bde7b6686fcb0574b62"
INSTALL_ROOT = Path(__file__).resolve().parents[1]

def load_packet() -> dict:
    path = INSTALL_ROOT / PACKET_PATH
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(INSTALL_ROOT):
        raise ValueError("missing or unsafe diagnostic packet")
    raw = path.read_bytes()
    if git_blob(raw) != PACKET_BLOB:
        raise ValueError("immutable diagnostic packet blob mismatch")
    packet = json.loads(raw)
    if (packet["schema"] != "kuuos.codeai.exact-diagnostic-observation.v1"
            or packet["global_verifier_ensemble"] != "HOLD"
            or packet["general_repair_usefulness"] != "NO_DATA"
            or any(packet[k] is not False for k in (
                "verified_useful", "proof_authority", "execution_authority",
                "merge_authority", "new_mathematical_result", "external_model"))):
        raise ValueError("diagnostic packet authority mismatch")
    return packet

def _hold(reason: str) -> dict:
    return {"status": "HOLD_REOBSERVE_DIAGNOSTIC", "issues": [reason],
            "context": None, "verified_useful": False, "proof_authority": False,
            "execution_authority": False, "merge_authority": False}

def observed_patch_sha256s(packet: Mapping) -> set[str]:
    return {packet[k]["patch_sha256"] for k in ("failed", "successful_alternative", "regenerated")}

def recall_exact_diagnostic(*, root: Path, observation: Mapping,
                            proof_scope: Mapping, target: str,
                            failed_source: bytes, failed_patch: bytes) -> dict:
    """Use a fresh externally observed main and materialized matching source.

    This function does not fetch GitHub, authenticate an external caller,
    execute Lean, or issue a new verifier certificate. On a scope mismatch
    it returns HOLD; a new snapshot may require actual re-observation.
    """
    try:
        packet = load_packet()
        root = root.resolve()
        if observation.get("scope") != "canonical_main" or observation.get("repository") != packet["repository"]:
            return _hold("noncanonical_observation")
        if target != packet["target"]:
            return _hold("target_changed")
        if (not isinstance(failed_source, bytes) or not isinstance(failed_patch, bytes)
                or hashlib.sha256(failed_source).hexdigest() != packet["failed"]["source_sha256"]
                or hashlib.sha256(failed_patch).hexdigest() != packet["failed"]["patch_sha256"]):
            return _hold("failed_candidate_or_patch_changed")
        if (make_scope({k: tuple(v) for k, v in proof_scope["entries"].items()}) != proof_scope
                or digest(proof_scope) != packet["proof_scope_digest"]):
            return _hold("proof_scope_changed")
        entries = {row["path"]: row for row in observation["root_entries"]}
        # The original v0.5 catalog reconstructs both source subtrees and
        # verifies all three committed pin/config files against the observed
        # root. Bind the broader cache scope's remaining local file inputs too.
        for name, (mode, kind, blob) in proof_scope["entries"].items():
            if "/" not in name and (name not in entries or entries[name]["sha"] != blob
                                    or entries[name]["mode"] != mode):
                return _hold("proof_root_entry_changed:" + name)
            if kind == "blob":
                path = root / name
                if (not path.is_file() or path.is_symlink()
                        or not path.resolve().is_relative_to(root)
                        or git_blob(path.read_bytes()) != blob
                        or ("100755" if path.stat().st_mode & 0o100 else "100644") != mode):
                    return _hold("proof_scope_file_changed:" + name)
        if (root / "lakefile.lean").exists():
            return _hold("alternate_lake_configuration")
        short = target.rsplit(".", 1)[-1]
        receipt = recall_kernel_memory(root, observation, short, terms=[short], limit=500)
        if (receipt["status"] != "REVIEW_REQUIRED" or receipt["without_kernel_observation"]
                or receipt["stale_observations"] or receipt["scope_issues"]
                or len(receipt["matched_observations"]) != 1):
            return _hold("exact_kernel_recall_incomplete")
        row = receipt["matched_observations"][0]["observation"]
        if (row["name"] != target or row["path"] != packet["source_path"]
                or row["blob"] != packet["source_blob"]
                or row["type_expr_sha256"] != packet["type_expr_sha256"]
                or row["axioms"] != []):
            return _hold("source_or_type_changed")
        context = {
            "schema": "kuuos.codeai.exact-diagnostic-advisory.v1",
            "packet_blob": PACKET_BLOB, "historical_source_head": packet["historical_source_head"],
            "historical_source_tree": packet["historical_source_tree"],
            "current_source_head": observation["source_head"], "current_source_tree": observation["source_tree"],
            "current_kernel_recall_digest": receipt["receipt_digest"],
            "proof_scope_digest": packet["proof_scope_digest"], "target": target,
            "source_path": row["path"], "source_blob": row["blob"],
            "type_expr_sha256": row["type_expr_sha256"],
            "failed_observation": packet["failed"],
            "successful_alternative_observation": packet["successful_alternative"],
            "regenerated_observation": packet["regenerated"],
            "historical_diagnostic_digest": packet["provenance"]["memory"]["diagnostic_digest"],
            "historical_memory_receipt_digest": packet["provenance"]["memory"]["receipt_digest"],
            "observed_difference": packet["observed_difference"],
            "scope": "exact-historical-observation-only",
            "general_repair_usefulness": "NO_DATA", "global_verifier_ensemble": "HOLD",
            "verified_useful": False, "proof_authority": False,
            "execution_authority": False, "merge_authority": False,
            "future_success_claimed": False,
        }
        return {"status": "EXACT_DIAGNOSTIC_OBSERVED_TEST_REQUIRED", "issues": [],
                "context": context, "context_digest": digest(context),
                "verified_useful": False, "proof_authority": False,
                "execution_authority": False, "merge_authority": False}
    except (ValueError, TypeError, KeyError, OSError, AttributeError, RuntimeError) as exc:
        return _hold(type(exc).__name__ + ":" + str(exc))

def prepare_exact_diagnostic_regeneration(*, root: Path, observation: Mapping,
        proof_scope: Mapping, target: str, failed_source: bytes, failed_patch: bytes,
        source_observation_receipt: Mapping, repository_files: Mapping,
        seed_candidates: Any, regeneration_request: Mapping) -> dict:
    """Append exact observations to a sealed *proposal-only* regeneration request.

    Require all known historical patch artifacts in the original regeneration
    seed inventory, so its native duplicate filter can reject re-presentations.
    This preparation never invokes a provider, applies a patch or verifies Lean.
    The unchanged original regeneration kernel must validate its own full
    generation receipt, seed correspondence, request and policy afterwards.
    """
    result = recall_exact_diagnostic(root=root, observation=observation,
        proof_scope=proof_scope, target=target, failed_source=failed_source,
        failed_patch=failed_patch)
    if result["context"] is None:
        return {**result, "request": None}
    try:
        packet = load_packet()
        ctx = result["context"]
        src = source_observation_receipt
        if (not digest_ok(src, SOURCE_RECEIPT_DIGEST_FIELD)
                or src.get("repository_full_name") != packet["repository"]
                or src.get("source_branch") != "main"
                or src.get("source_commit_sha") != ctx["current_source_head"]
                or src.get("tree_digest") != ctx["current_source_tree"]
                or src.get("repository_observation_read_only") is not True):
            return {**_hold("source_observation_receipt_mismatch"), "request": None}
        if repository_files.get(ctx["source_path"]) != (root / ctx["source_path"]).read_text(encoding="utf-8"):
            return {**_hold("exact_source_context_missing"), "request": None}
        supplied = {hashlib.sha256(item.patch_artifact.encode("utf-8")).hexdigest()
                    for item in seed_candidates}
        if not observed_patch_sha256s(packet).issubset(supplied):
            return {**_hold("historical_seed_inventory_incomplete"), "request": None}
        if not digest_ok(regeneration_request, REQUEST_DIGEST_FIELD):
            return {**_hold("unsealed_regeneration_request"), "request": None}
        request = dict(regeneration_request)
        suffix = "\nExact historical diagnostic observation (not a verified-useful hint):\n" + json.dumps(
            ctx, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        if suffix in request["intent_text"]:
            return {**_hold("diagnostic_context_already_attached"), "request": None}
        request["intent_text"] += suffix
        request["feedback_reasons"] = list(dict.fromkeys([
            *request["feedback_reasons"],
            "exact_historical_diagnostic:" + ctx["historical_diagnostic_digest"],
            "require_fresh_lean_validation",
        ]))
        request = seal(request, REQUEST_DIGEST_FIELD)
        return {**result, "request": request, "native_regeneration_required": True}
    except (ValueError, TypeError, KeyError, OSError, AttributeError, RuntimeError) as exc:
        return {**_hold(type(exc).__name__ + ":" + str(exc)), "request": None}
