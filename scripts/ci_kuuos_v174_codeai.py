#!/usr/bin/env python3
"""v1.74 CodeAI exact-source candidate: direct pinned Lean + real MCP + independent 26-axiom audit.
A successful producer is not an independent certificate, and neither job adopts source.
The active source is restored byte-for-byte after each disposable Actions job.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import tempfile
from scripts import ci_kuuos_v164_codeai as prior
from scripts import ci_kuuos_v174_codeai_probe as probe

NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74"
REL = "formal/" + NS.replace(".", "/") + ".lean"
WORKFLOW = ".github/workflows/kuuos-v174-codeai-real-mcp-independent-v1.yml"
BASE = "f03e1d3aaba3803a77c50e935854ed215c0da0aa"
SELECTED_NAME = "v174-v3-raw-universe-exact"
SELECTED_BLOB = "db34c44b30cbd6c5bd4aa113e320643aba21577c"
SELECTED_SHA256 = "e56ca5e35ab0f9f0f1f2f9f4a146b1beed5bf8a542cd2802db078e205f30b5e9"
DEPENDENCIES = {
    "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73.lean":
        "08a532c2793a382a5a59f4aee887d5843704c2fd",
    "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72.lean":
        "79fd2591bf03e8b2dd2a49848a009699235eaef0",
    "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71.lean":
        "f7d1e61cefa8e448fb3a8eb6c825a66e9c88db65",
    "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66.lean":
        "689d0135a4a85d25afae2dbc209a02db0cbd30d8",
    "formal/KUOS/DependentOriginationStandardABCLeibnizCellularComparisonV1_59.lean":
        "9388efc5b44873409133e30fbe7b30fbabdf6b52",
}

def version_bound_source(root: pathlib.Path) -> tuple[bytes, bytes, list[str]]:
    prior.pins(root)
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    assert prior.blob(historical) == BASE
    for path, sha in DEPENDENCIES.items():
        assert prior.blob((root / path).read_bytes()) == sha, ("dependency changed", path)
    candidates = probe.candidates(historical.decode("utf-8"))
    assert SELECTED_NAME in candidates and len(candidates) == 19
    names = prior.inventory(historical.decode("utf-8"))
    assert len(names) == 26 and len(set(names)) == 26
    source = candidates[SELECTED_NAME].encode()
    assert prior.blob(source) == SELECTED_BLOB
    assert hashlib.sha256(source).hexdigest() == SELECTED_SHA256
    assert prior.inventory(source.decode()) == names
    from scripts.kuuos_lean_mcp_repair_loop_v1 import FORBIDDEN_NEW, mask_lean_comments
    assert not FORBIDDEN_NEW.findall(mask_lean_comments(source.decode()))
    return historical, source, names

def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = prior.command(root, [
        "lake", "-KleanArgs=-DwarningAsError=true", "-KleanArgs=-DsorryAsError=true",
        "build", NS], out / "strict-build.log", 3600)
    assert p.returncode == 0, "selected candidate strict pinned Lean build failed"

def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import (
        run_loop, mcp_tactic_provider)
    base, selected, names = version_bound_source(root)
    target = root / REL
    original = target.read_bytes()
    assert original in (base, selected)
    assert prior.blob(original) == os.environ["CHECKOUT_BLOB"]
    assert os.environ["SOURCE_HEAD"] and len(os.environ["SOURCE_HEAD"]) == 40
    assert os.environ["SELECTED_BLOB"] == SELECTED_BLOB
    assert os.environ["SELECTED_NAME"] == SELECTED_NAME
    manifest = None
    try:
        target.write_bytes(selected)
        with tempfile.TemporaryDirectory(prefix="kuuos-v174-exact-") as td:
            olean = pathlib.Path(td) / "candidate.olean"
            p = prior.command(root, [
                "lake", "env", "lean", "-DwarningAsError=true",
                "-Dweak.sorryAsError=true", "-o", str(olean), REL],
                out / "direct-lean.log", 1200)
            log = p.stdout + "\n" + p.stderr
            errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
            assert p.returncode == 0 and olean.is_file()
            assert not errors and "sorryAx" not in log
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL,
            output_dir=out / "real-mcp",
            expected_sha256=hashlib.sha256(selected).hexdigest(),
            provider=mcp_tactic_provider, max_iterations=1)
        prior.verify_mcp(receipt, selected)
        (out / "real-mcp.json").write_text(json.dumps(receipt, indent=2))
        (out / "source.lean").write_bytes(selected)
        (out / "source-script.py").write_bytes(
            (root / "scripts/ci_kuuos_v174_codeai.py").read_bytes())
        (out / "probe-script.py").write_bytes(
            (root / "scripts/ci_kuuos_v174_codeai_probe.py").read_bytes())
        for v in (1, 2, 3):
            src = root / f"scripts/kuuos_v174_codeai_cause_separated_hunks_v{v}.json"
            (out / src.name).write_bytes(src.read_bytes())
        (out / "workflow.yml").write_bytes((root / WORKFLOW).read_bytes())
        manifest = {
            "source_head": os.environ["SOURCE_HEAD"],
            "checkout_blob": prior.blob(original),
            "selected_name": SELECTED_NAME, "selected_blob": SELECTED_BLOB,
            "selected_sha256": SELECTED_SHA256, "public_declarations": names,
            "dependencies": DEPENDENCIES, "source_restored": False,
            "git_write_performed": False, "independent_ci_success": False,
        }
    finally:
        target.write_bytes(original)
    assert manifest is not None and target.read_bytes() == original
    manifest["source_restored"] = True
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("KUUOS_V174_DIRECT_PINNED_LEAN_REAL_MCP_SUCCESS " +
          json.dumps(manifest), flush=True)

def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    historical, selected, names = version_bound_source(root)
    manifest = json.loads((out / "manifest.json").read_text())
    source = (out / "source.lean").read_bytes()
    receipt = json.loads((out / "real-mcp.json").read_text())
    target = root / REL
    original = target.read_bytes()
    assert original in (historical, selected)
    assert manifest["source_head"] == os.environ["SOURCE_HEAD"]
    assert manifest["checkout_blob"] == os.environ["CHECKOUT_BLOB"] == prior.blob(original)
    assert manifest["selected_name"] == SELECTED_NAME
    assert manifest["selected_blob"] == os.environ["SELECTED_BLOB"] == SELECTED_BLOB
    assert manifest["selected_sha256"] == SELECTED_SHA256
    assert manifest["dependencies"] == DEPENDENCIES
    assert manifest["public_declarations"] == names
    assert manifest["source_restored"] and not manifest["git_write_performed"]
    assert not manifest["independent_ci_success"]
    assert source == selected
    assert prior.blob(source) == SELECTED_BLOB
    assert hashlib.sha256(source).hexdigest() == SELECTED_SHA256
    for filename, rel in [
        ("source-script.py", "scripts/ci_kuuos_v174_codeai.py"),
        ("probe-script.py", "scripts/ci_kuuos_v174_codeai_probe.py"),
        ("workflow.yml", WORKFLOW),
    ]:
        assert (out / filename).read_bytes() == (root / rel).read_bytes()
    prior.verify_mcp(receipt, selected)
    for v in (1, 2, 3):
        name = f"kuuos_v174_codeai_cause_separated_hunks_v{v}.json"
        assert (out / name).read_bytes() == (root / "scripts" / name).read_bytes()
    audit = root / "formal/KUOS/DependentOriginationV174IndependentAudit.lean"
    assert not audit.exists()
    try:
        target.write_bytes(selected)
        strict_build(root, out)
        audit.write_text("import " + NS + "\n" +
            "\n".join("#check " + NS + "." + n for n in names) + "\n" +
            "\n".join("#print axioms " + NS + "." + n for n in names) + "\n")
        result = prior.command(root, [
            "lake", "env", "lean", "-DwarningAsError=true", "-Dweak.sorryAsError=true",
            str(audit)], out / "axioms.log", 1200)
        log = result.stdout + "\n" + result.stderr
        assert result.returncode == 0 and "sorryAx" not in log
        assert "error:" not in log and "warning:" not in log
        rows = re.findall(
            r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
            log, re.S)
        assert len(rows) == len(names) == 26, ("public axiom count", len(rows))
        assert {n for n, _ in rows} == {NS + "." + n for n in names}
        allowed = {"propext", "Classical.choice", "Quot.sound"}
        for name, axioms in rows:
            assert {a.strip() for a in axioms.split(",") if a.strip()} <= allowed, name
        print("KUUOS_V174_INDEPENDENT_26_DECLARATIONS_STANDARD_AXIOMS_SUCCESS",
              flush=True)
    finally:
        target.write_bytes(original)
        audit.unlink(missing_ok=True)
    assert target.read_bytes() == original

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("direct", "independent"))
    ap.add_argument("directory", type=pathlib.Path)
    args = ap.parse_args()
    root = pathlib.Path(".").resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == "direct" else independent)(root, out)

if __name__ == "__main__":
    main()
