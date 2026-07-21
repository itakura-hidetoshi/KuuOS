#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_checks_v0_2 import canonical_digest, digest_without
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2 import (
    PACK_DIGEST_FIELD,
    QUERY_NODE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    SELECTED_FILE_DIGEST_FIELD,
)
from scripts.project_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2 import build_projection
from scripts.build_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2 import build_reference_result


def main() -> None:
    result = build_reference_result()
    pack = result["context_pack"]
    receipt = result["receipt"]
    if pack[PACK_DIGEST_FIELD] != digest_without(pack, PACK_DIGEST_FIELD):
        raise SystemExit("context pack digest mismatch")
    if receipt[RECEIPT_DIGEST_FIELD] != digest_without(receipt, RECEIPT_DIGEST_FIELD):
        raise SystemExit("receipt digest mismatch")
    for node in pack["query_lineage"]:
        if node[QUERY_NODE_DIGEST_FIELD] != digest_without(node, QUERY_NODE_DIGEST_FIELD):
            raise SystemExit("query node digest mismatch: " + node["node_id"])
    for item in pack["selected_files"]:
        if item[SELECTED_FILE_DIGEST_FIELD] != digest_without(item, SELECTED_FILE_DIGEST_FIELD):
            raise SystemExit("selected file evidence digest mismatch: " + item["path"])
        if item["symbol_digest"] != canonical_digest(item["symbols"]):
            raise SystemExit("symbol digest mismatch: " + item["path"])
        if item["excerpt_digest"] != canonical_digest(item["excerpt"]):
            raise SystemExit("excerpt digest mismatch: " + item["path"])
        if not item["dependency_path"]:
            raise SystemExit("dependency path missing: " + item["path"])
    expected = build_projection()
    path = Path("examples/codeai_intent_aligned_dataflow_context_pack_v0_2.json")
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit("compact example does not match deterministic projection")
    if expected["query_stages"] != [
        "intent",
        "hypothesis",
        "hypothesis",
        "symbol",
        "dependency",
        "dataflow",
    ]:
        raise SystemExit("unexpected query lineage")
    if expected["resolved_dependency_path_count"] < 4:
        raise SystemExit("insufficient resolved dependency evidence")
    if expected["dataflow_edge_count"] < 4:
        raise SystemExit("insufficient dataflow evidence")
    if expected["repository_mutation_performed"] or expected["network_access_performed"]:
        raise SystemExit("forbidden effect reported")
    print("intent-aligned dataflow context pack v0.2: ok")


if __name__ == "__main__":
    main()
