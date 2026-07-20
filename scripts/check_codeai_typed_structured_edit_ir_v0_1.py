#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import runtime.kuuos_codeai_typed_structured_edit_ir_v0_1 as m

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_typed_structured_edit_ir_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_typed_structured_edit_ir_v0_1.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def main() -> int:
    data = load_example()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = m.build_codeai_typed_structured_edit_ir(
        context_pack=data["context_pack"],
        context_receipt=data["context_receipt"],
        repository_files=data["repository_files"],
        typed_edit_proposal=data["typed_edit_proposal"],
        typed_edit_policy=data["typed_edit_policy"],
    )
    if result.status != m.STATUS_READY:
        raise AssertionError("typed edit IR example blocked: " + ",".join(result.issues))
    if result.typed_edit_ir != data["expected_typed_edit_ir"]:
        raise AssertionError("typed edit IR example drift")
    if result.receipt != data["expected_receipt"]:
        raise AssertionError("typed edit IR receipt drift")
    if result.typed_edit_ir is None or result.receipt is None:
        raise AssertionError("typed edit IR outputs missing")
    if result.typed_edit_ir[m.IR_DIGEST_FIELD] != manifest["example_ir_digest"]:
        raise AssertionError("manifest IR digest drift")
    if result.receipt[m.RECEIPT_DIGEST_FIELD] != manifest["example_receipt_digest"]:
        raise AssertionError("manifest receipt digest drift")
    if result.typed_edit_ir["whole_file_modify_allowed"] is not False:
        raise AssertionError("whole-file modification unexpectedly allowed")
    if result.typed_edit_ir["symbol_preconditions_verified"] is not True:
        raise AssertionError("symbol preconditions not verified")
    if result.receipt["repository_mutation_performed"] is not False:
        raise AssertionError("repository mutation reported")
    if result.receipt["provider_invoked"] is not False:
        raise AssertionError("provider invocation reported")
    if result.receipt["verification_runner_invoked"] is not False:
        raise AssertionError("verification runner invocation reported")
    if result.receipt["candidate_selection_authority_granted"] is not False:
        raise AssertionError("candidate selection authority granted")
    if result.receipt["execution_authority_granted"] is not False:
        raise AssertionError("execution authority granted")
    print(
        json.dumps(
            {
                "status": result.status,
                "operation_count": result.typed_edit_ir["operation_count"],
                "operation_ids": result.receipt["operation_ids"],
                "typed_edit_ir_digest": result.typed_edit_ir[m.IR_DIGEST_FIELD],
                "receipt_digest": result.receipt[m.RECEIPT_DIGEST_FIELD],
                "whole_file_modify_allowed": False,
                "repository_mutation_performed": False,
                "execution_authority_granted": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
