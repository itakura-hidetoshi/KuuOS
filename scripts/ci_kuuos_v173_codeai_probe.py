#!/usr/bin/env python3
"""v1.73 CodeAI version-bound candidate probes, isolated from exact adopted v1.72.

This is a disposable pinned Lean *probe*. A green result grants no proof authority.
Never change the historical file, another PR, a canonical branch, or any axiom.
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

REL = "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73.lean"
NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73"
BASE = "29c6caed55abb5ed3ae35d5ed5f457d1ce1731aa"
V172 = "79fd2591bf03e8b2dd2a49848a009699235eaef0"
UNIVERSE_LOCK = "a71c8c3cb21dd34cc1985fa2cbc5cac66cfbb3f4"
OLD = "(standardTypeABoundaryPrismRankFunction g)"
NEW = "(standardTypeABoundaryPrismRankFunction.{u} g)"

def candidates(historical: str) -> dict[str, str]:
    assert prior.blob(historical.encode()) == BASE
    assert historical.count(OLD) == 23
    locked = historical.replace(OLD, NEW)
    assert prior.blob(locked.encode()) == UNIVERSE_LOCK
    names = prior.inventory(historical)
    assert len(names) == 21 and len(set(names)) == 21
    assert prior.inventory(locked) == names
    variants = {"original-baseline": historical, "rank-function-universe-locked": locked}
    manifest = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v1.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v1"
    assert manifest["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest["public_declarations_preserved"] == 21
    assert manifest["source_unmodified"] is True
    base_lines = locked.split("\n")
    for item in manifest["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Second CodeAI generation: isolate Lean elaboration normal forms while
    # preserving all 21 published declaration names and exact historical source.
    manifest_v2 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v2.json").read_text(encoding="utf-8"))
    assert manifest_v2["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v2"
    assert manifest_v2["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v2["public_declarations_preserved"] == 21
    assert manifest_v2["source_unmodified"] is True
    for item in manifest_v2["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Third CodeAI generation: alternatives for final rank pushout transport.
    # Both produce exact, public-signature-preserving disposable Lean variants.
    manifest_v3 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v3.json").read_text(encoding="utf-8"))
    assert manifest_v3["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v3"
    assert manifest_v3["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v3["public_declarations_preserved"] == 21
    assert manifest_v3["source_unmodified"] is True
    for item in manifest_v3["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Fourth cause-separated CodeAI group: final IsPushout universe lock,
    # explicit homOfLE monotone witness, and alternative Eq transport tactics.
    manifest_v4 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v4.json").read_text(encoding="utf-8"))
    assert manifest_v4["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v4"
    assert manifest_v4["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v4["public_declarations_preserved"] == 21
    assert manifest_v4["source_unmodified"] is True
    for item in manifest_v4["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Fifth CodeAI group: pinned mathlib homOfLE_ι is rfl, avoid unnecessary rw;
    # explicitly lock IsPushout.{u, u+1} so proof universe matches the source.
    manifest_v5 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v5.json").read_text(encoding="utf-8"))
    assert manifest_v5["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v5"
    assert manifest_v5["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v5["public_declarations_preserved"] == 21
    assert manifest_v5["source_unmodified"] is True
    for item in manifest_v5["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Sixth CodeAI generation: source-level final pushout arrow-iso coherence.
    # All four alternatives are exact deterministic blobs, not adopted proofs.
    manifest_v6 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v6.json").read_text(encoding="utf-8"))
    assert manifest_v6["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v6"
    assert manifest_v6["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v6["public_declarations_preserved"] == 21
    assert manifest_v6["source_unmodified"] is True
    for item in manifest_v6["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Seventh CodeAI generation: exact source-ledger transport of the terminal
    # isomorphism's underlying map, preserving every public Lean declaration.
    manifest_v7 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v7.json").read_text(encoding="utf-8"))
    assert manifest_v7["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v7"
    assert manifest_v7["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v7["public_declarations_preserved"] == 21
    assert manifest_v7["source_unmodified"] is True
    for item in manifest_v7["variants"]:
        assert item["name"] not in variants
        assert item["expected_blob"]
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    # Eighth CodeAI generation: make the underlying SSet composition goal
    # explicit before transporting the generated scaling equality morphism.
    manifest_v8 = json.loads(
        pathlib.Path("scripts/kuuos_v173_codeai_cause_separated_hunks_v8.json").read_text(encoding="utf-8"))
    assert manifest_v8["schema"] == "kuuos_v173_codeai_cause_separated_hunks_v8"
    assert manifest_v8["base_universe_blob"] == UNIVERSE_LOCK
    assert manifest_v8["public_declarations_preserved"] == 21
    assert manifest_v8["source_unmodified"] is True
    for item in manifest_v8["variants"]:
        assert item["name"] not in variants
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        candidate = "\n".join(result_lines)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        assert prior.inventory(candidate) == names
        variants[item["name"]] = candidate
    return variants

def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72.lean").read_bytes()) == V172
    current = (root / REL).read_bytes()
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    assert prior.blob(historical) == BASE
    results = candidates(historical.decode("utf-8"))
    assert current in (historical, results["rank-function-universe-locked"].encode())
    assert os.environ["CHECKOUT_BLOB"] == prior.blob(current)
    assert len(os.environ["SOURCE_HEAD"]) == 40
    out = pathlib.Path("/tmp/kuuos-v173-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    target = root / REL
    summary = []
    try:
        for name, text in results.items():
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(text)), name
            target.write_text(text, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="v173-lean-") as td:
                olean = pathlib.Path(td) / "candidate.olean"
                command = ["lake", "env", "lean", "-DwarningAsError=true",
                           "-Dweak.sorryAsError=true", "-o", str(olean), REL]
                p = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=1200)
                log = p.stdout + "\n" + p.stderr
                (out / (name + ".log")).write_text(log, encoding="utf-8")
                errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                clean = p.returncode == 0 and olean.is_file() and not errors and "sorryAx" not in log
                record = {
                    "candidate": name, "blob": prior.blob(text.encode()),
                    "sha256": hashlib.sha256(text.encode()).hexdigest(),
                    "source_head": os.environ["SOURCE_HEAD"], "errors": len(errors),
                    "first_errors": errors[:35], "returncode": p.returncode,
                    "direct_lean_success": clean, "real_mcp_certified": False,
                    "independent_axiom_certified": False, "adopted": current == text.encode(),
                }
                summary.append(record)
                (out / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
                print("KUUOS_V173_UNCERTIFIED_PROBE " + json.dumps(record), flush=True)
    finally:
        target.write_bytes(current)
    assert target.read_bytes() == current
    print("KUUOS_V173_PROBE_FINISHED " + json.dumps({
        "tried": len(summary),
        "direct_green": [r["candidate"] for r in summary if r["direct_lean_success"]],
        "source_restored": True, "certified": False, "main_modified": False,
    }), flush=True)

if __name__ == "__main__":
    main()
