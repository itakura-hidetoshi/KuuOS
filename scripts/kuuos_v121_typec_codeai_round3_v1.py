#!/usr/bin/env python3
"""CodeAI Type-C round3: eliminate the unique no-op simplification observed in
all four exact pinned round2 candidates (#43840610460). Preserve imports,
theorem statements, cocycle geometry, and the original file; test all direct
Lean candidates first, then real Lean MCP and a second direct check. Independent
source-bound CI remains separate. This experiment is not proof certification.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from scripts import kuuos_v121_typec_codeai_round2_v1 as prev
from scripts import kuuos_v121_codeai_concrete_induced_endpoint_repaired_v1 as base
from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
from runtime.kuuos_codeai_lean_observation_intake_v0_1 import read_observation_seed

ROOT = prev.ROOT
TARGET = prev.TARGET
ORIGINAL_BLOB = prev.ORIGINAL_BLOB
BRIDGE = prev.BRIDGE
BRIDGE_BLOB = prev.BRIDGE_BLOB
OUT = Path("/tmp/kuuos-v121-typec-codeai-round3")
MCP = Path("/tmp/kuuos-v121-typec-real-mcp-round3")
MEM = ROOT / "memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v121_typec_round2_v1.json"
PREV_HEAD = "cc3b8aca7eb53281f4a4a794b3ed4b947b26b261"
PREV_RUN = 43840610460
PREV_TREE = "eae5bb9356b6d5bf82a4f3d8daa765ddda397a47"

def check(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("KUUOS_V121_TYPEC_ROUND3_FAIL_CLOSED: " + why)

def make_variants(original: str) -> dict[str, str]:
    older = prev.make_variants(original)
    check(len(older) == 4, "four source-bound round2 candidates required")
    old_names = [m.group(1) for m in re.finditer(r"(?m)^theorem\s+(\w+)", original)]
    result = {}
    for name, source in older.items():
        # Lean already closed this branch; -DwarningAsError treats an
        # otherwise unused simp as a direct elaboration error.
        needle = "        all_goals simp\n"
        check(source.count(needle) == 1, "no-op simp location drift: " + name)
        repaired = source.replace(needle, "", 1)
        check(repaired != source, "no actual source change")
        check([m.group(1) for m in re.finditer(r"(?m)^theorem\s+(\w+)", repaired)] == old_names,
              "theorem inventory changed: " + name)
        check(repaired.split("\n", 1)[0] == original.split("\n", 1)[0],
              "import boundary changed: " + name)
        check(base.FORBIDDEN_NEW.search(repaired) is None,
              "forbidden Lean construct: " + name)
        result["round3-" + name.removeprefix("round2-") + "-drop-noop-simp"] = repaired
    check(len({base.blob(v.encode()) for v in result.values()}) == 4,
          "not four source-distinct candidates")
    return result

def main() -> int:
    head, tree = base.event_source()
    require_pins(ROOT)
    original = (ROOT / TARGET).read_bytes()
    check(base.blob(original) == ORIGINAL_BLOB, "original type-C source changed")
    check(base.blob((ROOT / BRIDGE).read_bytes()) == BRIDGE_BLOB,
          "pinned bridge changed")
    observed = read_observation_seed(MEM)
    check(len(observed) == 4, "missing prior four observed failures")
    check(all(x["producer_run"] == PREV_RUN and x["source_head"] == PREV_HEAD
              and x["outcome"] == "DIRECT_LEAN_FAILURE" for x in observed),
          "prior failure provenance does not match")
    raw_memory = json.loads(MEM.read_text())
    check(all(x["source_tree"] == PREV_TREE for x in raw_memory["observations"]),
          "prior source tree drift")
    versions = make_variants(original.decode("utf-8"))
    base.TARGET = TARGET
    base.OUT = OUT
    base.MCP = MCP
    OUT.mkdir(parents=True, exist_ok=False)
    rows = []
    try:
        for name, src in versions.items():
            try:
                rows.append(base.direct(name, src))
            finally:
                (ROOT / TARGET).write_bytes(original)
        mcp = base.mcp_verify(head, rows, versions)
    finally:
        (ROOT / TARGET).write_bytes(original)
    check(base.blob((ROOT / TARGET).read_bytes()) == ORIGINAL_BLOB,
          "original type-C proof source not restored")
    MCP.mkdir(parents=True, exist_ok=True)
    mcp["source_restored"] = True
    (MCP / "receipt.json").write_text(json.dumps(mcp, sort_keys=True, indent=2) + "\n")
    (OUT / "portfolio.json").write_text(json.dumps({
        "source_head": head, "source_tree": tree,
        "previous_fail_run": PREV_RUN, "previous_fail_source_head": PREV_HEAD,
        "original_v105_blob": ORIGINAL_BLOB, "bridge_blob": BRIDGE_BLOB,
        "candidate_count": len(rows), "candidates": rows,
        "source_restored": True, "git_write_performed": False,
        "independent_ci_certified": False
    }, sort_keys=True, indent=2) + "\n")
    print("KUUOS_V121_TYPEC_ROUND3 " + json.dumps({
        "head": head, "tested": len(rows),
        "direct_green": [x["variant"] for x in rows if x["status"] == "SUCCESS"],
        "error_counts": {x["variant"]: x.get("error_count") for x in rows},
        "selected": mcp.get("selected"), "mcp_status": mcp["status"],
        "source_restored": True
    }, sort_keys=True))
    return 0 if mcp["status"] == "LOCAL_MCP_AND_DIRECT_LEAN_GREEN_NOT_INDEPENDENT_CI" else 2

if __name__ == "__main__":
    raise SystemExit(main())
