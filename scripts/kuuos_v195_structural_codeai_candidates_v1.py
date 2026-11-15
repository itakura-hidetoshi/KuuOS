#!/usr/bin/env python3
"""Exact-source CodeAI portfolio and isolated pinned-Lean structural experiments.

Does NOT modify Git or admit any proof candidate. The input is an exact
v1.95 original Git blob, a CodeAI observation receipt for its PR HEAD, and
five externally proposed structural candidates. It executes the actual CodeAI
autonomous-unified-diff kernel, then directly checks every candidate against
the pinned Lean import closure. Only a later Lean MCP gate may admit a winner.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    POLICY_DIGEST_FIELD, seal, canonical_digest,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    build_codeai_autonomous_unified_diff_candidates, STATUS_READY,
    DISPOSITION_SYNTHESIZED, RECEIPT_DIGEST_FIELD,
)
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256, imports_of, declarations_of
from scripts.codeai_pr3522_live_v195_candidate_v0_1 import (
    TARGET, REPOSITORY, ASSOC_BEFORE,
)

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_BLOB = "f7dcf6d9cddf3820b78c91375f0ec460874a7734"
MODULE = "KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95"
WHISKERS_BEFORE = """  whiskerLeft := by
    intros
    assumption
  whiskerRight := by
    intros
    assumption"""
WHISKERS_AFTER = """  whiskerLeft := fun _ η => η
  whiskerRight := fun η _ => η"""

BASIC_PREFIX = """  map₂_associator := by
    intro a b c d f g h
    have hab : a.as ≤ b.as := f.as.le
    have hbc : b.as ≤ c.as := g.as.le
    have hcd : c.as ≤ d.as := h.as.le
"""
CASES = """    rcases a with ⟨a⟩
    rcases b with ⟨b⟩
    rcases c with ⟨c⟩
    rcases d with ⟨d⟩
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp_all [natTriangleMapComp] <;> omega"""
ARITH = """    change (natTriangleMapComp f g) + (natTriangleMapComp (f ≫ g) h) + (0 : Nat) =
      (0 : Nat) + (natTriangleMapComp g h) + (natTriangleMapComp f (g ≫ h))
"""
ARITH_PART = """    simp only [NatOneCell.comp_eq_add, NatOneCell.id_eq_zero]
"""


def checked_source() -> tuple[Path, bytes]:
    path = ROOT / TARGET
    raw = path.read_bytes()
    if git_blob(raw) != ORIGINAL_BLOB or raw.decode().count(ASSOC_BEFORE) != 1:
        raise RuntimeError("exact parent Lean source/blob mismatch")
    if raw.decode().count(WHISKERS_BEFORE) != 1:
        raise RuntimeError("bicategory whisker implementation changed")
    return path, raw


def variants(source: str) -> dict[str, str]:
    specs = {
      "original-simp-then-change": (False, BASIC_PREFIX + ARITH_PART + ARITH + CASES),
      "original-explicit-whisker-lemmas": (False, BASIC_PREFIX + """    have hR (η : Nat) :
      (show NatOneCell.star ⟶ NatOneCell.star from η) ▷ NatOneCell.star = η := by rfl
    have hL (η : Nat) :
      NatOneCell.star ◁ (show NatOneCell.star ⟶ NatOneCell.star from η) = η := by rfl
    simp only [hR, hL, NatOneCell.comp_eq_add, NatOneCell.id_eq_zero]
""" + ARITH + CASES),
      "explicit-whiskers-change": (True, BASIC_PREFIX + ARITH + CASES),
      "explicit-whiskers-simp": (True, BASIC_PREFIX + """    rcases a with ⟨a⟩
    rcases b with ⟨b⟩
    rcases c with ⟨c⟩
    rcases d with ⟨d⟩
    fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
      simp_all [natTriangleMapComp, NatOneCell.comp_eq_add] <;> omega"""),
      "original-dsimp-projections": (False, BASIC_PREFIX + """    dsimp only [Bicategory.whiskerRight, Bicategory.whiskerLeft, Bicategory.associator]
""" + ARITH + CASES),
      # The preceding exact Lean experiment established that dsimp eliminates
      # both whiskerings and exposes Iso.refl. Normalize the latter explicitly
      # before attempting finite ordinal arithmetic.
      "round6-dsimp-iso-simp-cases": (False, BASIC_PREFIX + """    dsimp only [Bicategory.whiskerRight, Bicategory.whiskerLeft, Bicategory.associator]
    simp only [Iso.refl_hom, NatOneCell.comp_eq_add, NatOneCell.id_eq_zero,
      Nat.add_zero, Nat.zero_add]
""" + CASES),
      "round6-dsimp-iso-simp-split": (False, BASIC_PREFIX + """    dsimp only [Bicategory.whiskerRight, Bicategory.whiskerLeft, Bicategory.associator]
    simp only [Iso.refl_hom, NatOneCell.comp_eq_add, NatOneCell.id_eq_zero,
      Nat.add_zero, Nat.zero_add, natTriangleMapComp]
    split_ifs <;> omega"""),
      "round6-dsimp-iso-change-cases": (False, BASIC_PREFIX + """    dsimp only [Bicategory.whiskerRight, Bicategory.whiskerLeft, Bicategory.associator]
    simp only [Iso.refl_hom, NatOneCell.comp_eq_add, NatOneCell.id_eq_zero]
""" + ARITH + CASES),
    }
    result = {}
    for name,(change_whiskers,assoc) in specs.items():
        # Round-5 outcomes are immutable in CI #43657758138. Probe only
        # newly derived round-6 variants; retain the earlier portfolio as data.
        if not name.startswith("round6-"):
            continue
        text = source.replace(ASSOC_BEFORE,assoc)
        if change_whiskers:
            text = text.replace(WHISKERS_BEFORE,WHISKERS_AFTER)
        if text == source or not text.endswith("\n"):
            raise RuntimeError("empty or malformed variant: " + name)
        if imports_of(text) != imports_of(source):
            raise RuntimeError("imports changed: " + name)
        sig = lambda x: [
            (d["kind"], d["name_lexical"], d["signature_sha256"])
            for d in declarations_of(x,MODULE)
        ]
        if sig(text) != sig(source):
            raise RuntimeError("theorem or declaration statement changed: " + name)
        if any(tok in text and tok not in source
               for tok in ("sorry", "admit", "axiom", "unsafe", "native_decide")):
            raise RuntimeError("new forbidden token in " + name)
        result[name] = text
    return result


def main() -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    if (event.get("number") != 3522
        or event.get("repository",{}).get("full_name") != REPOSITORY):
        raise RuntimeError("real parent PR event required")
    source_head = event["pull_request"]["head"]["sha"]
    codeai_path = ROOT / "artifacts/codeai-v195/pr3522-codeai-v195-candidate.json"
    real_codeai = json.loads(codeai_path.read_text(encoding="utf-8"))
    if real_codeai["source_head"] != source_head or real_codeai["source_blob"] != ORIGINAL_BLOB:
        raise RuntimeError("CodeAI external observation HEAD/blob mismatch")
    source_receipt = real_codeai["source_observation_receipt"]
    target, original = checked_source()
    cases = variants(original.decode())
    now = int(time.time())
    template = json.loads((ROOT/"examples/codeai_candidate_patch_envelope_v0_1.json").read_text())
    policy = deepcopy(template["candidate_policy"])
    policy.update({
        "expected_source_observation_receipt_digest":
            source_receipt["codeai_intent_repository_observation_receipt_digest"],
        "expected_repository_full_name": REPOSITORY,
        "expected_source_commit_sha": source_head,
        "allowed_patch_formats": ["unified_diff"],
        "allowed_path_prefixes": ["formal/KUOS"],
        "forbidden_path_prefixes": ["legacy"],
        "maximum_changed_paths": 1,
        "known_risk_labels": ["formal-proof"],
        "handover_risk_labels": [],
        "allow_deletions": False,
        "allow_renames": False,
        "allow_binary_patches": False,
        "allow_submodule_patches": False,
        "allow_mode_changes": False,
        "require_requirement_trace": True,
        "require_test_plan": True,
        "allow_evidence_degradation": False,
        "evaluation_epoch": now+30,
        "maximum_candidate_age": 3600,
    })
    policy = seal(policy,POLICY_DIGEST_FIELD)
    proposals = [
        {
          "proposal_id": "v195-"+key+"-"+source_head[:10],
          "candidate_revision": "r1",
          "producer_id": "external-structural-repair-research",
          "producer_session_id": "v195-structure-"+str(i)+"-"+source_head[:10],
          "candidate_created_epoch": now,
          "edits": [{"path":TARGET,"operation":"modify","new_content":body}],
          "requirement_trace_ids": ["v195:pinned-associator-whisker-normalization"],
          "test_plan_ids": ["v195:direct-pinned-lake-env-lean"],
          "risk_labels": ["formal-proof"],
          "unresolved_candidate_questions": [],
          "prior_candidate_digests": [],
          "prior_producer_session_ids": [],
        }
        for i,(key,body) in enumerate(cases.items())
    ]
    generated = build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=source_receipt,
        repository_files={TARGET:original.decode()},
        proposals=proposals,
        candidate_policy=policy,
    )
    if (generated.status != STATUS_READY or generated.receipt is None
        or generated.receipt["codeai_disposition"] != DISPOSITION_SYNTHESIZED
        or len(generated.candidates) != len(proposals)):
        raise RuntimeError("real CodeAI structural portfolio rejected: "+repr(generated.issues))
    output = Path("/tmp/kuuos-v195-structural")
    if output.exists():
        raise RuntimeError("append-only output path preexisting")
    output.mkdir(parents=True,exist_ok=False)
    receipt = {
        "source_head": source_head,
        "source_blob": ORIGINAL_BLOB,
        "source_tree": real_codeai["source_git_tree"],
        "source_sha256": sha256(original),
        "codeai_portfolio_receipt": generated.receipt[RECEIPT_DIGEST_FIELD],
        "codeai_actual_kernel": "build_codeai_autonomous_unified_diff_candidates",
        "candidates": [],
        "source_restored": False,
        "repository_mutated": False,
        "lean_mcp_verified": False,
        "independent_ci_certified": False,
        "merge_authority": False,
    }
    prev_mode = stat.S_IMODE(target.stat().st_mode)
    try:
        for candidate in generated.candidates:
            packet = candidate.patch_candidate
            key = next((k for k in cases if packet["candidate_id"].startswith("v195-"+k+"-")), None)
            if key is None: raise RuntimeError("CodeAI returned alien candidate")
            updated = cases[key].encode()
            if packet["changed_paths"] != [TARGET] or packet["patch_artifact_digest"] is None:
                raise RuntimeError("CodeAI variant wrong paths")
            name = key.replace("/","-")
            entry = {
                "name":key, "codeai_candidate_id":packet["candidate_id"],
                "codeai_rank":candidate.rank,
                "codeai_candidate_receipt":
                    candidate.candidate_receipt["codeai_candidate_patch_receipt_digest"],
                "source_git_blob":ORIGINAL_BLOB,
                "candidate_git_blob":git_blob(updated),
                "candidate_sha256":sha256(updated),
                "status":"NOT_TESTED",
            }
            try:
                target.write_bytes(updated)
                with tempfile.TemporaryDirectory(prefix="kuuos-v195-structural-") as td:
                    cmd=["lake","env","lean","-DwarningAsError=true",
                         "-Dweak.sorryAsError=true","-o",td+"/candidate.olean",TARGET]
                    try:
                        r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,
                                         timeout=240,check=False)
                    except subprocess.TimeoutExpired:
                        entry["status"]="TIMEOUT"
                        log="candidate compilation timed out"
                    else:
                        entry["status"]="SUCCESS" if r.returncode==0 else "FAILURE"
                        entry["exit_code"]=r.returncode
                        log=r.stdout+"\n"+r.stderr
                    (output/(name+".log")).write_text(log,encoding="utf-8")
                    entry["log_sha256"]=sha256(log.encode())
                    entry["error_lines"]=[x[:480] for x in log.splitlines()
                                          if "error:" in x][:12]
                    entry["olean_exists"]=Path(td+"/candidate.olean").is_file()
            finally:
                target.write_bytes(original)
                target.chmod(prev_mode)
                if target.read_bytes()!=original:
                    raise RuntimeError("original v1.95 source not restored")
            receipt["candidates"].append(entry)
            print("KUUOS_V195_STRUCTURAL_VARIANT "+json.dumps(entry,sort_keys=True))
    finally:
        target.write_bytes(original)
        target.chmod(prev_mode)
        receipt["source_restored"]=target.read_bytes()==original
    (output/"portfolio_receipt.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    success=[x for x in receipt["candidates"] if x["status"]=="SUCCESS"]
    print("KUUOS_V195_STRUCTURAL_PORTFOLIO "+json.dumps({
        "source_head":source_head,"candidate_count":len(receipt["candidates"]),
        "direct_lean_green_count":len(success),
        "source_restored":receipt["source_restored"],
        "codeai_receipt":receipt["codeai_portfolio_receipt"],
        "independent_ci_certified":False,
    },sort_keys=True))
    return 0 if receipt["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
