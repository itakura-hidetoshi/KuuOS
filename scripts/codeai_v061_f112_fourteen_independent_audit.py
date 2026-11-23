#!/usr/bin/env python3
"""Independent 14D F112 cert receipt: no first-runner .olean and no root promotion."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from scripts.codeai_v061_f112_fourteen_full_source_split import (
    ROOT, SOURCE, SOURCE_BLOB, OUT, assert_source, blob,
)
from scripts.codeai_v061_f112_fourteen_necessity_source_split import (
    SOURCE as NECESSITY_SOURCE,
    SOURCE_BLOB as NECESSITY_BLOB,
    EXPECTED as NECESSITY_DECLARATIONS,
    assert_original as assert_necessity_source,
)

FIRST = ROOT / "first-sandbox"
EXPECTED_SOURCE_FIELDS = (
    "parent_original_git_blob",
    "parent_original_sha256",
    "raw_original_stage_sha256",
    "exact_original_prefix_sha256",
    "scratch_core_sha256",
    "scratch_full_tail_sha256",
)


def main() -> None:
    raw = assert_source()
    assert blob(SOURCE.read_bytes()) == SOURCE_BLOB
    assert (ROOT / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.30.0-rc2"

    first = json.loads((FIRST / "manifest.json").read_text())
    independent = json.loads((OUT / "manifest.json").read_text())
    for key in EXPECTED_SOURCE_FIELDS:
        assert first[key] == independent[key], f"exact source mismatch: {key}"
    assert independent["parent_original_git_blob"] == SOURCE_BLOB
    assert independent["full_five_stage_statements_unchanged"] is True
    assert independent["all_original_axiom_audit_commands_retained"] is True
    assert independent["original_lean_file_unchanged"] is True

    mcp = json.loads((FIRST / "real-lean-mcp-receipt.json").read_text())
    assert mcp["status"] == "LOCAL_SPLIT_IMPORT_MCP_SUCCESS_ONLY"
    assert mcp["semantic_success"] is True and mcp["partial"] is False
    assert mcp["failed_dependencies"] == [] and mcp["error_count"] == 0
    assert mcp["original_blob"] == SOURCE_BLOB
    assert mcp["source_sha256"] == independent["parent_original_sha256"]
    assert mcp["independent_lean_ci"] is False

    # The local gate audits ALL Lean logs, including 13D and typed predecessors.
    first_gate = json.loads((FIRST / "sandbox-gate.json").read_text())
    current_gate = json.loads((OUT / "sandbox-gate.json").read_text())
    for gate in (first_gate, current_gate):
        assert gate["status"] == "CLEAN_LOCAL_LEAN_EVIDENCE_ONLY"
        assert gate["faults"] == []
        assert gate["original_14d_blob"] == SOURCE_BLOB
        assert gate["original_necessity_blob"] == NECESSITY_BLOB
        assert len(gate["stage_records"]) == 12
        assert gate["independent_ci_claimed"] is False
    assert first_gate["independent_runner"] is False
    assert current_gate["independent_runner"] is True

    # Six exact original Necessity declarations and the original axiom prints.
    necessity_original = assert_necessity_source()
    necessity_manifests = [
        json.loads((folder / "necessity/manifest.json").read_text())
        for folder in (FIRST, OUT)
    ]
    m1, m2 = necessity_manifests
    for key in ("canonical_source_blob", "canonical_source_sha256",
                "original_fragments_sha256", "stage_sha256", "stage_modules"):
        assert m1[key] == m2[key], "Necessity stage-source mismatch: " + key
    assert m1["canonical_source_blob"] == NECESSITY_BLOB
    assert m1["six_original_declarations_unchanged"] is True
    assert m2["all_six_original_axiom_audits_retained"] is True
    expected_necessity = re.findall(r"(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$",
                                    necessity_original)
    assert tuple(expected_necessity) == NECESSITY_DECLARATIONS
    necessity_log = (OUT / "fourteen_necessity_tail.log").read_text()
    for name in expected_necessity:
        assert "'Kuu.F112.Physical." + name + "'" in necessity_log, (
            "Necessity axiom audit absent: " + name)
    assert not re.search(r"(?i)PANIC at|Lean panicked|sorryAx|^\s*(?:error|warning):",
                         necessity_log, flags=re.M)

    for name in ("generic_core", "full_five_stage", "original_module_import_shim"):
        assert (FIRST / (name + "-exit.txt")).read_text().strip() == "0"
        assert (OUT / (name + "-exit.txt")).read_text().strip() == "0"
    assert (FIRST / "import-smoke-exit.txt").read_text().strip() == "0"
    assert (OUT / "import-smoke-exit.txt").read_text().strip() == "0"
    assert json.loads((OUT / "replay.json").read_text())["artifact_integrity_verified"] is True
    assert json.loads((OUT / "replay.json").read_text())["olean_count"] == 193

    # Audit print commands from ALL unchanged original 14D declarations, not a subset.
    expected = re.findall(r"(?m)^#print axioms ([A-Za-z0-9_.]+)\s*$", raw)
    assert len(expected) >= 20 and len(set(expected)) == len(expected), expected
    all_log = "\n".join((
        (OUT / "generic_core.log").read_text(),
        (OUT / "full_five_stage.log").read_text(),
    ))
    # Lean uses the fully-qualified declaration name in every printed axiom response.
    for name in expected:
        assert "'Kuu.F112.Physical." + name + "'" in all_log, (
            "missing axiom-audit print output: " + name
        )
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    actual = set()
    for record in re.findall(r"depends on axioms:\s*\[([^\]]*)\]", all_log, flags=re.S):
        actual.update(a.strip() for a in record.split(",") if a.strip())
    assert actual.issubset(allowed), ("unapproved axioms", sorted(actual - allowed))
    assert "sorryAx" not in actual and "sorryAx" not in all_log
    # Treat Lean internal PANIC / externally printed errors as HOLD even when
    # the executable returned 0 and managed to write an .olean.
    # Prior 13D logs demonstrate why process exit status alone is insufficient.
    unexpected = [line[:300] for line in all_log.splitlines() if
                  re.search(r"(?i)(?:PANIC at |Lean panicked|^\s*(?:error|warning):)", line)]
    assert not unexpected, ("Lean internal diagnostic obstruction", unexpected[:5])

    out = {
        "schema": "kuuos.codeai.v061.f112.fourteen.independent.v1",
        "scope": "ORIGINAL_14D_DECLARATIONS_RECOMPILED_IN_INDEPENDENT_SCRATCH_SPLIT",
        "source_blob": SOURCE_BLOB,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "independent_original_14d_monolith": False,
        "independent_split_success": True,
        "git_tree_checked": False,
        "full_strict_checked": False,
        "public_root_checked": False,
        "formal_adoption": False,
        "merge_authority": False,
        "memory_verified_useful": False,
        "axioms_audited": len(expected),
        "necessity_axioms_audited": len(NECESSITY_DECLARATIONS),
        "independent_predecessor_lean_gate": True,
        "allowed_axioms": sorted(actual),
        "lean_internal_panic_or_error": False,
        "source_invariant_fields": list(EXPECTED_SOURCE_FIELDS),
    }
    (OUT / "independent-receipt.json").write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print("CODEAI_F112_INDEPENDENT_SPLIT_14D", json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
