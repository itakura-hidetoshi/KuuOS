#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_selective_repository_semantic_context_pack_v0_1 import (
    PACK_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_selective_repository_semantic_context_pack,
    digest_without,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_selective_repository_semantic_context_pack_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_selective_repository_semantic_context_pack_v0_1.json"


def main() -> int:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = build_codeai_selective_repository_semantic_context_pack(
        source_observation_receipt=data["source_observation_receipt"],
        repository_files=data["repository_files"],
        context_request=data["context_request"],
        context_policy=data["context_policy"],
    )
    assert result.status == STATUS_READY, result.issues
    assert result.context_pack is not None
    assert result.receipt is not None
    assert result.context_pack == data["expected_context_pack"]
    assert result.receipt == data["expected_receipt"]
    assert result.context_pack[PACK_DIGEST_FIELD] == digest_without(
        result.context_pack, PACK_DIGEST_FIELD
    )
    assert result.receipt[RECEIPT_DIGEST_FIELD] == digest_without(
        result.receipt, RECEIPT_DIGEST_FIELD
    )
    assert result.context_pack["selected_file_count"] == 3
    assert [entry["path"] for entry in result.context_pack["selected_entries"]] == [
        "runtime/context_builder.py",
        "tests/test_context_builder.py",
        "docs/CONTEXT.md",
    ]
    assert result.context_pack["full_repository_forwarded"] is False
    assert result.receipt["provider_invoked"] is False
    assert result.receipt["repository_mutation_performed"] is False
    assert result.receipt["candidate_selection_authority_granted"] is False
    assert manifest["profile_version"] == data["profile_version"]
    print(
        json.dumps(
            {
                "status": result.status,
                "selected_paths": result.receipt["selected_paths"],
                "context_pack_digest": result.context_pack[PACK_DIGEST_FIELD],
                "receipt_digest": result.receipt[RECEIPT_DIGEST_FIELD],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
