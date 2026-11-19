#!/usr/bin/env python3
"""KuuOS v1.75 bounded CodeAI full-source candidate comparison (NOT proof).

Never adopts source: historical originals and fixed dependencies must match.
Probe job success means only the selected comparison ran; per-candidate Lean results
are advisory until actual Lean MCP and independent 31-axiom certification.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile
from scripts import ci_kuuos_v164_codeai as prior
from scripts.kuuos_lean_mcp_repair_loop_v1 import FORBIDDEN_NEW, mask_lean_comments

NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75"
REL = "formal/" + NS.replace(".", "/") + ".lean"
BASE = "ac0abc7aa8f7c52c45ac0e2ed13d0cae71ada978"
V174 = "db34c44b30cbd6c5bd4aa113e320643aba21577c"
EXPECTED = {
    "baseline": "ac0abc7aa8f7c52c45ac0e2ed13d0cae71ada978",
    "explicit-universe": "e2604f4d4f215b1006b32fbdea826a216ef6289b",
    "class-reducible": "5754d9899f42f342c8bc1a35362b3952f31997a8",
    "raw-cellular-typed": "69f5fe2b78510ef3b7d36fbb7b0c210202a02e62",
    "scaled-pushout-universe": "f73c98a18e055140f75aeea012b168d0f37df2cb",
    "open-v149": "d6b6db23842aafd4a54aae1f3f43a1f3a40a00b5",
    "open-v149-inductive-where": "9eaf7fe74615bbd58ca4484c584b239656aba5f5",
    "inductive-where-only": "e4bd12d79ecbc2f519a177329dcf98437aeebb2e",
    "v175-v2-first-typed-pattern": "5171aa38dc1f9c779ad836d332125eb76e3fd4fa",
    "v175-v2-cofan-descent": "bb4e5d6e2aa4e7ba89b05fa385a039a5e821eb2a",
    "v175-v2-bmap-desc": "217ca069b5a1a6e7310c2ca0f32bcc452c92cd09",
    "v175-v3-typed-source-target": "206162efc208d705a2f074a249a086d70bc2ce7d",
    "v175-v3-typed-first-square": "74681fd75168c505d252da799598462d12e9cd7b",
    "v175-v3-cofan-universe": "b5d360052904bd982290874c007cd928dcea0dfb",
    "v175-v3-bmap-universe": "423f0246d9635433645dcb54f0cf8c3fb19d6ede"
}
OLD_FUNCTION = "(standardTypeABoundaryPrismRankFunction g)"
NEW_FUNCTION = "(standardTypeABoundaryPrismRankFunction.{u} g)"
OLD_RAW = "    standardABCRawCellularStep\n      (standardTypeABoundaryPrismRankAPhaseToSucc g j) := by\n  exact MorphismProperty.pushouts_mk\n    (standardTypeABoundaryPrism_rankB_scaled_isPushout g j)\n    (standardTypeABoundaryPrismRankBSigmaGeneratorHom_mem_coproductsABC g j)"
NEW_RAW = "    standardABCRawCellularStep.{u}\n      (standardTypeABoundaryPrismRankAPhaseToSucc.{u} g j) := by\n  exact MorphismProperty.pushouts_mk\n    (MorphismProperty.coproducts.{u}\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u})))\n    (standardTypeABoundaryPrism_rankB_scaled_isPushout g j)\n    (standardTypeABoundaryPrismRankBSigmaGeneratorHom_mem_coproductsABC g j)"
OLD_PUSHOUT = "    IsPushout\n      (standardTypeABoundaryPrismRankBSourceSigmaToAPhase g j)\n      (standardTypeABoundaryPrismRankBSigmaGeneratorHom g j)\n      (standardTypeABoundaryPrismRankAPhaseToSucc g j)\n      (standardTypeABoundaryPrismRankBTargetSigmaToSucc g j) := by"
NEW_PUSHOUT = "    IsPushout.{u, u+1}\n      (standardTypeABoundaryPrismRankBSourceSigmaToAPhase.{u} g j)\n      (standardTypeABoundaryPrismRankBSigmaGeneratorHom.{u} g j)\n      (standardTypeABoundaryPrismRankAPhaseToSucc.{u} g j)\n      (standardTypeABoundaryPrismRankBTargetSigmaToSucc.{u} g j) := by"


def replace_once(source: str, old: str, new: str) -> str:
    assert source.count(old) == 1, ("source mismatch", old, source.count(old))
    return source.replace(old, new, 1)


def candidates(source: str) -> dict[str, str]:
    assert prior.blob(source.encode()) == BASE
    assert source.count(OLD_FUNCTION) == 35
    one = source.replace(OLD_FUNCTION, NEW_FUNCTION)
    two = one
    for name in (
        "standardTypeABoundaryPrismRankBSourceSigmaScaling",
        "standardTypeABoundaryPrismRankBTargetSigmaScaling",
    ):
        two = replace_once(two, "def " + name + "\n", "@[reducible] def " + name + "\n")
    three = replace_once(two, OLD_RAW, NEW_RAW)
    four = replace_once(three, OLD_PUSHOUT, NEW_PUSHOUT)
    result = {
        "baseline": source,
        "explicit-universe": one,
        "class-reducible": two,
        "raw-cellular-typed": three,
        "scaled-pushout-universe": four,
    }
    # Independent structural causes: missing v1.49 namespace and Lean4
    # inductive constructor syntax. Preserve all original 31 declarations.
    five = replace_once(four,
        "open KUOS.DependentOriginationScaledTerminalRLPV1_41\n",
        "open KUOS.DependentOriginationScaledTerminalRLPV1_41\n"
        "open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49\n")
    six = replace_once(five,
        "    (j : ℕ) : Type u\n  | q12\n",
        "    (j : ℕ) : Type u where\n  | q12\n")
    seven = replace_once(four,
        "    (j : ℕ) : Type u\n  | q12\n",
        "    (j : ℕ) : Type u where\n  | q12\n")
    result["open-v149"] = five
    result["open-v149-inductive-where"] = six
    result["inductive-where-only"] = seven
    # Second cause-separated group: reproduce new candidates from the
    # exact earlier near-green source; no original-source modification.
    manifest = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_cause_separated_hunks_v2.json"
    ).read_text(encoding="utf-8"))
    assert manifest["schema"] == "kuuos_v175_codeai_cause_separated_hunks_v2"
    assert manifest["base_candidate_blob"] == EXPECTED["open-v149-inductive-where"]
    assert manifest["original_blob"] == BASE
    assert manifest["historical_unchanged"] is True
    assert manifest["public_declarations_preserved"] == 31
    assert len(manifest["variants"]) == 3
    for item in manifest["variants"]:
        assert item["name"] not in result
        candidate = result["open-v149-inductive-where"]
        for hunk in item["patches"]:
            old, newer = hunk["old"], hunk["new"]
            assert candidate.count(old) == 1, ("stale v1.75", item["name"], hunk["name"])
            candidate = candidate.replace(old, newer, 1)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        result[item["name"]] = candidate
    # v3: isolate universe inference for source/target type B copies.
    # Use complete historical source-derived v2 candidates as exact bases.
    universe_manifest = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_universe_hunks_v3.json"
    ).read_text(encoding="utf-8"))
    assert universe_manifest["schema"] == "kuuos_v175_codeai_universe_hunks_v3"
    assert universe_manifest["baseline_blob"] == BASE
    assert universe_manifest["historical_unchanged"] is True
    assert universe_manifest["public_declarations_preserved"] == 31
    assert len(universe_manifest["variants"]) == 4
    for base_name, base_blob in universe_manifest["source_blobs"].items():
        assert prior.blob(result[base_name].encode()) == base_blob
    for item in universe_manifest["variants"]:
        assert item["name"] not in result
        candidate = result[item["base"]]
        for patch in item["patches"]:
            if patch["mode"] == "literal":
                assert candidate.count(patch["old"]) == patch["count"] == 1
                candidate = candidate.replace(patch["old"], patch["new"], 1)
            else:
                pattern = r"\b" + re.escape(patch["old"]) + r"\b(?!\.\{)"
                candidate, n = re.subn(pattern, patch["new"], candidate)
                assert n == patch["count"], (item["name"], patch["old"], n)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        result[item["name"]] = candidate
    assert set(result) == set(EXPECTED)
    # v4: additive and strictly source-bound root-cause comparisons.
    v4 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_structural_hunks_v4.json"
    ).read_text(encoding="utf-8"))
    assert v4["schema"] == "kuuos_v175_codeai_structural_hunks_v4"
    assert v4["source_base"] == EXPECTED["open-v149-inductive-where"]
    assert v4["original_blob"] == BASE
    assert v4["historical_unchanged"] is True
    assert v4["public_declarations_preserved"] == 31
    assert len(v4["variants"]) == 4
    expected = dict(EXPECTED)
    for variant in v4["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            old, new = patch["old"], patch["new"]
            assert patch["count"] >= 1
            assert candidate.count(old) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(old, new)
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v5: independent parser and type-universe causes, derived from verified v4 blobs.
    v5 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_typed_universe_hunks_v5.json"
    ).read_text(encoding="utf-8"))
    assert v5["schema"] == "kuuos_v175_codeai_typed_universe_hunks_v5"
    assert v5["original_blob"] == BASE
    assert v5["historical_unchanged"] is True
    assert v5["public_declarations_preserved"] == 31
    assert len(v5["variants"]) == 5
    for variant in v5["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            old, new = patch["old"], patch["new"]
            if patch["mode"] == "literal":
                assert candidate.count(old) == patch["count"]
                candidate = candidate.replace(old, new)
            else:
                pattern = r"\b" + re.escape(old) + r"\b(?!\.\{)"
                candidate, count = re.subn(pattern, new, candidate)
                assert count == patch["count"], (variant["name"], patch["name"], count)
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v6: strictly source-derived interface-level universe probes.
    v6 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_signature_level_hunks_v6.json"
    ).read_text(encoding="utf-8"))
    assert v6["schema"] == "kuuos_v175_codeai_signature_level_hunks_v6"
    assert v6["original_blob"] == BASE
    assert v6["historical_unchanged"] is True
    assert v6["public_declarations_preserved"] == 31
    assert len(v6["variants"]) == 4
    for variant in v6["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert candidate.count(patch["old"]) == patch["count"]
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v7: source-bound independent repairs for category equality, Sigma.desc,
    # range surjectivity, and dependent q12/q23 transports.
    v7 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_dep_transport_hunks_v7.json"
    ).read_text(encoding="utf-8"))
    assert v7["schema"] == "kuuos_v175_codeai_dep_transport_hunks_v7"
    assert v7["original_blob"] == BASE
    assert v7["historical_unchanged"] is True
    assert v7["public_declarations_preserved"] == 31
    assert len(v7["variants"]) == 5
    assert prior.blob(result["v175-v6-cofan-closure-levels"].encode()) == v7["baseline_blob"]
    for variant in v7["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"], variant["name"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v8: source-checked equality transport through coproduct, rank coverage and pushout.
    v8 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_gluing_hunks_v8.json"
    ).read_text(encoding="utf-8"))
    assert v8["schema"] == "kuuos_v175_codeai_gluing_hunks_v8"
    assert v8["original_blob"] == BASE
    assert v8["historical_unchanged"] is True
    assert v8["public_declarations_preserved"] == 31
    assert len(v8["variants"]) == 5
    assert prior.blob(result["v175-v7-combined"].encode()) == v8["baseline_blob"]
    for variant in v8["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"], variant["name"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v9: exact universe levels of theorem statements, not copied implicit ones.
    v9 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_source_universe_hunks_v9.json"
    ).read_text(encoding="utf-8"))
    assert v9["schema"] == "kuuos_v175_codeai_source_universe_hunks_v9"
    assert v9["original_blob"] == BASE
    assert v9["historical_unchanged"] is True
    assert v9["public_declarations_preserved"] == 31
    assert len(v9["variants"]) == 5
    assert prior.blob(result["v175-v8-sigma-congrArg"].encode()) == v9["source_base_v8_sigma"]
    assert prior.blob(result["v175-v7-combined"].encode()) == v9["source_base_v7"]
    for variant in v9["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"], variant["name"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v10: independent q-transport, IsPushout.of_iso and rank-domain probes.
    v10 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_cast_pushout_hunks_v10.json"
    ).read_text(encoding="utf-8"))
    assert v10["schema"] == "kuuos_v175_codeai_cast_pushout_hunks_v10"
    assert v10["historical_unchanged"] is True
    assert v10["original_blob"] == BASE
    assert v10["public_declarations_preserved"] == 31
    assert len(v10["variants"]) == 6
    assert prior.blob(result["v175-v9-sigma-u"].encode()) == v10["baseline_blob"]
    for variant in v10["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"], variant["name"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v11: independently validated prerequisite signatures and free-dimension bridge.
    v11 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_dimension_bridge_hunks_v11.json"
    ).read_text(encoding="utf-8"))
    assert v11["schema"] == "kuuos_v175_codeai_dimension_bridge_hunks_v11"
    assert v11["original_blob"] == BASE
    assert v11["historical_unchanged"] is True
    assert v11["public_declarations_preserved"] == 31
    assert len(v11["variants"]) == 5
    for name, blob in v11["base_blobs"].items():
        assert prior.blob(result[name].encode()) == blob
    for variant in v11["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v12: source-bound free-dimension map equality, new source-target gluing,
    # and v1.73 certified reverse-scaling decomposition (hypothesis until Lean check).
    v12 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_glued_bridge_rank_hunks_v12.json"
    ).read_text(encoding="utf-8"))
    assert v12["schema"] == "kuuos_v175_codeai_glued_bridge_rank_hunks_v12"
    assert v12["original_blob"] == BASE
    assert v12["historical_unchanged"] is True
    assert v12["public_declarations_preserved"] == 31
    assert len(v12["variants"]) == 8
    for name, sha in v12["base_blobs"].items():
        assert prior.blob(result[name].encode()) == sha
    for variant in v12["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v13: preserve source-bound causes while comparing rank descent paths.
    # These are hypotheses until direct Lean, real MCP and independent audit.
    v13 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_rank_descent_hunks_v13.json"
    ).read_text(encoding="utf-8"))
    assert v13["schema"] == "kuuos_v175_codeai_rank_descent_hunks_v13"
    assert v13["original_blob"] == BASE
    assert v13["historical_unchanged"] is True
    assert v13["public_declarations_preserved"] == 31
    assert len(v13["variants"]) == 3
    for name, sha in v13["base_blobs"].items():
        assert prior.blob(result[name].encode()) == sha
    for variant in v13["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    # v14: isolate goal normalization from predicate equality transport.
    # Pretty-printed equality is not rewriting compatibility or proof authority.
    v14 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_rank_predicate_hunks_v14.json"
    ).read_text(encoding="utf-8"))
    assert v14["schema"] == "kuuos_v175_codeai_rank_predicate_hunks_v14"
    assert v14["original_blob"] == BASE
    assert v14["historical_unchanged"] is True
    assert v14["public_declarations_preserved"] == 31
    assert len(v14["variants"]) == 2
    for name, sha in v14["base_blobs"].items():
        assert prior.blob(result[name].encode()) == sha
    for variant in v14["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            assert patch["mode"] == "literal"
            assert patch["count"] >= 1
            assert candidate.count(patch["old"]) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    names = prior.inventory(source)
    assert len(names) == len(set(names)) == 31
    assert "inductive StandardTypeABoundaryPrismRankBCell" in source
    for name, candidate in result.items():
        assert prior.blob(candidate.encode()) == expected[name], name
        assert prior.inventory(candidate) == names, name
        assert "inductive StandardTypeABoundaryPrismRankBCell" in candidate
        assert not FORBIDDEN_NEW.findall(mask_lean_comments(candidate)), name
    return result


def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74.lean").read_bytes()) == V174
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    original = (root / REL).read_bytes()
    assert prior.blob(historical) == BASE
    assert prior.blob(original) == os.environ["CHECKOUT_BLOB"] == BASE
    assert len(os.environ["SOURCE_HEAD"]) == 40
    result = candidates(historical.decode())
    target = root / REL
    out = pathlib.Path("/tmp/kuuos-v175-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    records = []
    try:
        for name, source in result.items():
            if os.environ.get("V14_ONLY", "0") == "1" and not (
                name.startswith("v175-v14-") or name in {
                    "v175-v13-range-gluing", "v175-v13-v173-gluing"}):
                continue
            if os.environ.get("V13_ONLY", "0") == "1" and not name.startswith("v175-v13-"):
                continue
            if os.environ.get("V12_ONLY", "0") == "1" and not name.startswith("v175-v12-"):
                continue
            if os.environ.get("V11_ONLY", "0") == "1" and not name.startswith("v175-v11-"):
                continue
            if os.environ.get("V10_ONLY", "0") == "1" and not name.startswith("v175-v10-"):
                continue
            if os.environ.get("V9_ONLY", "0") == "1" and not name.startswith("v175-v9-"):
                continue
            if os.environ.get("V8_ONLY", "0") == "1" and not name.startswith("v175-v8-"):
                continue
            if os.environ.get("V7_ONLY", "0") == "1" and not name.startswith("v175-v7-"):
                continue
            if os.environ.get("V6_ONLY", "0") == "1" and not name.startswith("v175-v6-"):
                continue
            if os.environ.get("V5_ONLY", "0") == "1" and not name.startswith("v175-v5-"):
                continue
            if os.environ.get("V4_ONLY", "0") == "1" and not name.startswith("v175-v4-"):
                continue
            target.write_text(source, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="kuuos-v175-probe-") as directory:
                olean = pathlib.Path(directory) / "candidate.olean"
                cmd = [
                    "lake", "env", "lean", "-DwarningAsError=true",
                    "-Dpp.universes=true", "-Dpp.explicit=true", "-Dpp.coercions.types=true",
                    "-Dweak.sorryAsError=true", "-o", str(olean), REL,
                ]
                p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=1800)
                log = p.stdout + "\n" + p.stderr
                (out / (name + ".log")).write_text(log)
                errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                entry = {
                    "name": name,
                    "blob": prior.blob(source.encode()),
                    "sha256": hashlib.sha256(source.encode()).hexdigest(),
                    "head": os.environ["SOURCE_HEAD"],
                    "returncode": p.returncode,
                    "error_count": len(errors),
                    "first_errors": errors[:45],
                    "direct_lean_success": (p.returncode == 0 and olean.is_file()
                        and not errors and "sorryAx" not in log),
                    "real_mcp_certified": False,
                    "independent_axiom_certified": False,
                    "adopted": False,
                }
                records.append(entry)
                (out / "results.json").write_text(json.dumps(records, indent=2))
                print("KUUOS_V175_UNCERTIFIED_PROBE " + json.dumps(entry), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    print("KUUOS_V175_PROBE_FINISHED " + json.dumps({
        "tried": len(records),
        "direct_green": [x["name"] for x in records if x["direct_lean_success"]],
        "source_restored": True,
        "certified": False,
        "git_write_performed": False,
    }), flush=True)


if __name__ == "__main__":
    main()
