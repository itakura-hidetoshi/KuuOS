from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    seal,
)
from runtime.kuuos_codeai_autonomous_structured_edit_synthesis_v0_1 import (
    STATUS_READY as SYNTHESIS_READY,
    ProviderAdapter,
    build_codeai_autonomous_structured_edit_synthesis,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_v0_1 import (
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    build_codeai_autonomous_candidate_regeneration,
)

ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_EXAMPLE = ROOT / "examples" / "codeai_autonomous_structured_edit_synthesis_v0_1.json"
CANDIDATE_EXAMPLE = ROOT / "examples" / "codeai_candidate_patch_envelope_v0_1.json"
REGEN_EXAMPLE = ROOT / "examples" / "codeai_autonomous_candidate_regeneration_v0_1.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _seed():
    structured = _load(STRUCTURED_EXAMPLE)
    candidate = _load(CANDIDATE_EXAMPLE)
    item = structured["provider_adapters"][0]
    adapter = ProviderAdapter(
        item["adapter_id"], item["provider_id"], item["model_id"],
        lambda _prompt, response=item["response"]: copy.deepcopy(response),
    )
    result = build_codeai_autonomous_structured_edit_synthesis(
        source_observation_receipt=candidate["source_observation_receipt"],
        repository_files=structured["repository_files"],
        synthesis_request=structured["synthesis_request"],
        provider_adapters=[adapter],
        synthesis_policy=structured["synthesis_policy"],
        candidate_policy=candidate["candidate_policy"],
    )
    assert result.status == SYNTHESIS_READY, result.issues
    assert result.receipt is not None
    return structured, candidate, result


def _response(
    response_id: str,
    session_id: str,
    proposal_id: str,
    path: str,
    content: str,
    *,
    raw_output: str | None = None,
    claims_authority: bool = False,
    hides_uncertainty: bool = False,
    bypasses_governance: bool = False,
    evidence_missing: bool = False,
):
    if raw_output is None:
        raw_output = json.dumps({
            "proposal_id": proposal_id,
            "candidate_revision": "r1",
            "edits": [{"path": path, "operation": "add", "new_content": content}],
            "risk_labels": ["documentation"],
            "unresolved_candidate_questions": [],
        }, separators=(",", ":"))
    return {
        "provider_response_id": response_id,
        "producer_session_id": session_id,
        "response_created_epoch": 1784318700,
        "raw_output": raw_output,
        "claims_authority": claims_authority,
        "hides_uncertainty": hides_uncertainty,
        "bypasses_governance": bypasses_governance,
        "evidence_missing": evidence_missing,
    }


def _adapter(adapter_id: str, provider_id: str, responses):
    if callable(responses):
        generate = responses
    else:
        queue = [copy.deepcopy(item) for item in responses]
        generate = lambda _prompt: queue.pop(0)
    return ProviderAdapter(adapter_id, provider_id, provider_id + "-model", generate)


def _inputs():
    structured, candidate, seed = _seed()
    regen = _load(REGEN_EXAMPLE)
    return {
        "source_generation_receipt": copy.deepcopy(seed.receipt),
        "source_observation_receipt": copy.deepcopy(candidate["source_observation_receipt"]),
        "repository_files": copy.deepcopy(structured["repository_files"]),
        "seed_candidates": tuple(seed.candidates),
        "regeneration_request": copy.deepcopy(regen["regeneration_request"]),
        "regeneration_policy": copy.deepcopy(regen["regeneration_policy"]),
        "candidate_policy": copy.deepcopy(candidate["candidate_policy"]),
    }


def _reseal_request(request):
    return seal({k: v for k, v in request.items() if k != REQUEST_DIGEST_FIELD}, REQUEST_DIGEST_FIELD)


def _reseal_policy(policy):
    return seal({k: v for k, v in policy.items() if k != POLICY_DIGEST_FIELD}, POLICY_DIGEST_FIELD)



__all__ = [name for name in globals() if not name.startswith("__")]
