#!/usr/bin/env python3
"""R3: raw single-part olean discovery, calibrated against the certified R2 frontier.

Read only verified-cache objects at the exact R2 canonical source/pins.
Do not interpret a negative syntactic marker as an applicable obstruction.
A missing, multipart, ambiguous, or unobserved module is explicitly HOLD.
The additional frontier is discovery only; no theorem is reproved here.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import check_codeai_kernel_obstruction_index_v1_r2 as r2
v = r2.v
ROOT = v.ROOT
REFERENCE = "778616a511407b854dd105c1613f436196020831b16be54579f95559aa3fc60c"
REFERENCE_TYPES = "25a1497c8b2a2e8418e34718e153be1660d2593a1fe2628b22f23230ded716ff"
EXTRA = 18
BATCH = 6
MARK = "KUUOS_OLEAN_R3_EXPORT"
SCHEMA = "kuuos.codeai.kernel-obstruction-index.olean-calibration.v1-r3"
# The original Expr serializer is reused verbatim. The only import is Lean.
TAIL = r'''
set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
run_cmd do
  Lean.Elab.Command.liftIO do
    let manifest ← IO.FS.readFile "__MODULE_FILE__"
    let (readModules, splitModules, count) ←
      IO.FS.withFile "__ROWS_FILE__" .write fun handle => do
        let mut doneModules : Array String := #[]
        let mut unsupported : Array String := #[]
        let mut count : Nat := 0
        for entry in manifest.splitOn "\n" do
          unless entry.isEmpty do
            match entry.splitOn "\t" with
            | [moduleName, path] =>
              let (data, _region) ← Lean.readModuleData (System.FilePath.mk path)
              if data.isModule then
                unsupported := unsupported.push moduleName
              else
                unless data.constNames == data.constants.map (·.name) do
                  throw <| IO.userError s!"constant name inventory mismatch: {moduleName}"
                for info in data.constants do
                  if info.isTheorem then
                    handle.putStr ((theoremRow info.name moduleName info).compress ++ "\n")
                    count := count + 1
                doneModules := doneModules.push moduleName
            | _ => throw <| IO.userError "malformed artifact manifest"
        return (doneModules, unsupported, count)
    let inventory := Json.mkObj [
      ("read_modules", toJson readModules),
      ("unsupported_module_system", toJson splitModules),
      ("selected_theorems", toJson count)]
    IO.FS.writeFile "__META_FILE__" (inventory.compress ++ "\n")
    IO.println s!"KUUOS_OLEAN_R3_EXPORT {count}"
end KuuOSKernelObstructionIndexProbe
'''

def filehash(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def run_batch(folder, modules, sources, artifacts):
    folder.mkdir()
    wanted = folder / "modules.txt"
    meta_path = folder / "environment.json"
    raw = folder / "kernel-types.jsonl"
    wanted.write_text("".join(m + "\t" + artifacts[m]["path"] + "\n" for m in modules), encoding="utf-8")
    old = v.TEMPLATE.read_text(encoding="utf-8")
    v.need(old.startswith("import KuuOSFormal\n"), "original serializer import changed")
    marker = "set_option maxRecDepth 8192 in\n"
    v.need(old.count(marker) == 1, "original serializer boundary changed")
    lean = old.split(marker, 1)[0].replace("import KuuOSFormal\n", "import Lean\n", 1) + TAIL
    for key, path in (("__MODULE_FILE__", wanted), ("__META_FILE__", meta_path), ("__ROWS_FILE__", raw)):
        v.need(lean.count(key) == 1, "unexpected serializer placeholder")
        lean = lean.replace(key, path.relative_to(ROOT).as_posix())
    log = r2.run_lean(folder / "OleanExport.lean", lean, timeout=600)
    meta = load(meta_path)
    good = meta["read_modules"]
    split = meta["unsupported_module_system"]
    v.need(len(good) + len(split) == len(modules)
           and set(good).isdisjoint(split) and set(good + split) == set(modules)
           and f"{MARK} {meta['selected_theorems']}" in log, "raw module inventory incomplete")
    # Adapter to R2 row validation only; the raw exporter has NOT imported
    # these modules. The actual receipt uses read_modules, not imported_modules.
    if meta["selected_theorems"]:
        rows = v.read_rows(raw, {"imported_modules": good, "selected_theorems": meta["selected_theorems"]},
                           {m: sources[m] for m in good}, folder)
    else:
        v.need(not raw.read_text(encoding="utf-8").strip(), "unexpected raw rows")
        rows = []
    raw.unlink()
    for m in modules:
        v.need(filehash(ROOT / artifacts[m]["path"]) == artifacts[m]["sha256"], "artifact changed while reading")
    v.save(folder / "kernel-index.json", rows)
    result = {"read_modules": good, "unsupported_module_system": split,
              "artifact_bindings": [artifacts[m] for m in modules],
              "type_count": len(rows), "type_digest": v.digest(rows),
              "probe_sha256": v.sha(lean.encode())}
    v.save(folder / "receipt.json", result)
    print("KUUOS_OLEAN_R3_SHARD", json.dumps({k: z for k, z in result.items() if k != "artifact_bindings"}, sort_keys=True), flush=True)
    return rows, result

def direct(head, out):
    prior = load(out / "direct.json")
    reference = load(out / "kernel-index.json")
    v.need(v.digest(prior) == REFERENCE and prior["source_head"] == head
           and v.digest(reference) == REFERENCE_TYPES and len(reference) == 124
           and set(prior["indexed_modules"]) == set(r2.MODULES),
           "R2 direct reference changed")
    obs, cat, inv = v.snapshot(head)
    sources = r2.module_sources(cat)
    counts = Counter(x["module"] for x in inv["hints"])
    ordered = sorted((m for m in counts if m not in r2.MODULES), key=lambda m: (-counts[m], m))
    requested = list(r2.MODULES) + ordered[:EXTRA]
    v.need(len(requested) == len(r2.MODULES) + EXTRA, "additional frontier incomplete")
    work = out / "fast-r3"
    work.mkdir()
    v.save(work / "lexical-inventory.json", inv)
    states = {}
    artifacts = {}
    for m in requested:
        if m not in sources or len(sources[m]) != 1:
            states[m] = "HOLD_AMBIGUOUS_SOURCE"
            continue
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", m):
            states[m] = "HOLD_UNSUPPORTED_MODULE_PATH"
            continue
        path = ROOT / ".lake/build/lib/lean" / (m.replace(".", "/") + ".olean")
        if not path.is_file():
            states[m] = "HOLD_MISSING_OLEAN"
            continue
        # Do not read private/server parts individually; they can share
        # objects with earlier parts. No claim of completeness for them.
        if Path(str(path) + ".server").exists() or Path(str(path) + ".private").exists():
            states[m] = "HOLD_MULTIPART_OLEAN"
            continue
        artifacts[m] = {"module": m, "source": sources[m][0],
                        "path": path.relative_to(ROOT).as_posix(),
                        "sha256": filehash(path)}
    v.need(set(r2.MODULES) <= set(artifacts), "mandatory R2 modules unavailable as single-part artifacts")
    v.save(work / "plan.json", {"requested": requested, "preflight_holds": states, "artifacts": artifacts})
    candidates = [m for m in requested if m in artifacts]
    rows = []
    receipts = []
    for i in range(0, len(candidates), BATCH):
        local, receipt = run_batch(work / f"batch-{i // BATCH + 1:02}", candidates[i:i+BATCH], sources, artifacts)
        rows.extend(local)
        receipts.append(receipt)
        for m in receipt["read_modules"]:
            states[m] = "RAW_OLEAN_TYPE_OBSERVED"
        for m in receipt["unsupported_module_system"]:
            states[m] = "HOLD_MODULE_SYSTEM"
    rows.sort(key=lambda x: (x["module"], x["name"]))
    v.need(len({x["name"] for x in rows}) == len(rows), "duplicate raw kernel names")
    calibrated = [x for x in rows if x["module"] in r2.MODULES]
    if calibrated != reference:
        v.save(work / "calibration-mismatch.json", {"reference": reference, "raw": calibrated})
        raise ValueError("raw olean types do not exactly match R2 imported environment")
    for m in r2.MODULES:
        states[m] = "R2_IMPORTED_TYPE_EQUAL"
    # Retain every original lexical row, including unresolved or not-indexed
    # candidates. Additional raw observations are discovery, not proof authority.
    joined, unmatched = v.reconcile(inv, rows)
    v.need(len(joined) == 6380, "lexical obstruction inventory lost")
    by_module = Counter(x["module"] for x in rows)
    coverage = [{"module": m, "sources": sources[m], "state": states.get(m, "HOLD_NOT_REQUESTED"),
                 "type_count": by_module[m]} for m in sorted(sources)]
    v.save(work / "kernel-index.json", rows)
    v.save(work / "lexical-join.json", joined)
    v.save(work / "unmatched-negative-types.json", unmatched)
    v.save(work / "module-coverage.json", coverage)
    v.need(v.github_observation(head, "canonical_main") == obs, "canonical source changed")
    stable = {"schema": SCHEMA, "source_head": head, "source_tree": obs["source_tree"],
              "scope_digest": v.SCOPE, "r2_direct_digest": REFERENCE,
              "r2_type_digest": REFERENCE_TYPES, "calibrated_theorems": len(calibrated),
              "calibrated_modules": list(r2.MODULES),
              "requested_modules": requested, "raw_index_type_count": len(rows),
              "additional_raw_type_count": len(rows) - len(calibrated),
              "state_counts": dict(sorted(Counter(x["state"] for x in coverage).items())),
              "coverage_digest": v.digest(coverage), "raw_type_digest": v.digest(rows),
              "lexical_hint_count": len(joined), "lexical_join_digest": v.digest(joined),
              "unmatched_negative_digest": v.digest(unmatched),
              "batch_receipt_digests": [v.digest(x) for x in receipts],
              "proof_authority": False, "applicability_certified": False,
              "all_axioms_audited": False, "semantic_search_complete": False,
              "full_corpus_kernel_coverage_claimed": False}
    v.save(work / "direct.json", stable)
    print("KUUOS_OLEAN_R3_DIRECT_GREEN", json.dumps({**stable, "digest": v.digest(stable)}, sort_keys=True), flush=True)
    return stable

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--head", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--first", type=Path)
    a = p.parse_args()
    out = a.out.resolve()
    v.need(out.is_relative_to(ROOT / "artifacts"), "isolated output required")
    receipt = direct(a.head, out)
    if a.first is not None:
        first = load(a.first / "fast-r3/direct.json")
        mp = load(a.first / "mcp.json")
        r2_independent = load(out / "independent.json")
        v.need(first == receipt and mp["direct_digest"] == REFERENCE
               and len(mp["selected_observations"]) == 12
               and r2_independent["status"] == "INDEPENDENT_KERNEL_OBSTRUCTION_INDEX_R2_GREEN"
               and r2_independent["direct_digest"] == REFERENCE
               and r2_independent["mcp_digest"] == v.digest(mp), "independent R3/R2 receipts differ")
        proof = {"status": "INDEPENDENT_OLEAN_R3_GREEN", "direct_digest": v.digest(receipt),
                 "r2_direct_digest": REFERENCE, "mcp_digest": v.digest(mp),
                 "calibrated_theorems": receipt["calibrated_theorems"],
                 "additional_raw_type_count": receipt["additional_raw_type_count"],
                 "state_counts": receipt["state_counts"], "proof_authority": False,
                 "applicability_certified": False, "semantic_search_complete": False}
        v.save(out / "fast-r3/independent.json", proof)
        print("KUUOS_OLEAN_R3_INDEPENDENT", json.dumps(proof, sort_keys=True), flush=True)

if __name__ == "__main__":
    main()
