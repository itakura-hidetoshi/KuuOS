#!/usr/bin/env python3
"""KuuOS CodeAI exact-HEAD v1.97 type/universe structural repair portfolio.

Read-only from Git; only temporarily edits source bytes in an isolated Actions
checkout and always restores originals. Independently compiles every proposal
with fixed Lean. CodeAI candidate generation is NOT theorem certification.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import time
import urllib.request

from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as obs
from runtime import kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as diff
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256, imports_of, declarations_of

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97"
ORIGINAL_BLOB = "cbbcb93978571ab45df9708e9da3ca2b52ac42f5"
PREFIX = "open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96\n"


def require_event() -> tuple[str,str]:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if event.get("number") != 3522 or event.get("repository",{}).get("full_name") != REPO:
        raise RuntimeError("exact parent PR event required")
    pr = event["pull_request"]
    source_head = pr["head"]["sha"]
    branch = pr["head"]["ref"]
    url = "https://api.github.com/repos/"+REPO+"/git/commits/"+source_head
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"KuuOS-CodeAI-v197"})
    with urllib.request.urlopen(req,timeout=30) as response:
        data = json.load(response)
    tree = data.get("tree",{}).get("sha")
    if data.get("sha") != source_head or not isinstance(tree,str) or not re.fullmatch("[a-f0-9]{40}",tree):
        raise RuntimeError("exact GitHub source/tree unverified")
    return source_head,branch,tree


def replace_once(source: str, old: str, new: str, name: str) -> str:
    occurrences = source.count(old)
    if occurrences != 1:
        raise RuntimeError(f"v1.97 source drift: {name}: {occurrences}")
    return source.replace(old, new, 1)


def variants(source: str) -> dict[str, str]:
    """Four independent CodeAI repair hypotheses, original theorem obligations retained.

    v1.96 proves the Quiver.Hom of any NatOneCell pair is definitionally Nat.
    But Lean 4.30.0-rc2 will not synthesize HAdd/OfNat on dependent Hom
    arguments without elaborating into Nat first. No typeclass axiom added.
    """
    if source.count(PREFIX) != 1:
        raise RuntimeError("wrong v1.97 source/namespace")
    lines = source.splitlines(keepends=True)
    anchors = [
        48, 63, 64, 65, 76, 77, 78, 79,
        145, 146, 147, 155, 157, 171, 172, 173, 174,
        182, 184, 186, 200, 201, 202, 203, 204,
    ]
    for idx in anchors:
        if "= 0" not in lines[idx-1]:
            raise RuntimeError("v1.97 zero annotation drift: "+str(idx))
        lines[idx-1] = lines[idx-1].replace("= 0", "= (0 : Nat)")
    typed = "".join(lines)

    typed_add = replace_once(typed,
        "    sigma.mapComp f g + sigma.mapComp (f ≫ g) h =\n"
        "      sigma.mapComp g h + sigma.mapComp f (g ≫ h) := by",
        "    Nat.add (sigma.mapComp f g) (sigma.mapComp (f ≫ g) h) =\n"
        "      Nat.add (sigma.mapComp g h) (sigma.mapComp f (g ≫ h)) := by",
        "cocycle statement Nat.add")

    add_raw = replace_once(typed_add,
        "  change\n"
        "    sigma.mapComp f g + sigma.mapComp (f ≫ g) h + 0 =\n"
        "      0 + sigma.mapComp g h + sigma.mapComp f (g ≫ h) at hcoh\n"
        "  omega",
        "  change\n"
        "    Nat.add (Nat.add (sigma.mapComp f g)\n"
        "      (sigma.mapComp (f ≫ g) h)) (0 : Nat) =\n"
        "      Nat.add (Nat.add (0 : Nat) (sigma.mapComp g h))\n"
        "        (sigma.mapComp f (g ≫ h)) at hcoh\n"
        "  simpa only [Nat.add_zero, Nat.zero_add] using hcoh",
        "exact Nat.add associator normal form")

    add_simp = replace_once(typed_add,
        "  change\n"
        "    sigma.mapComp f g + sigma.mapComp (f ≫ g) h + 0 =\n"
        "      0 + sigma.mapComp g h + sigma.mapComp f (g ≫ h) at hcoh\n"
        "  omega",
        "  simpa only [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] using hcoh",
        "simp associator normal form")

    add_omega = replace_once(add_raw,
        "  simpa only [Nat.add_zero, Nat.zero_add] using hcoh",
        "  omega",
        "omega after explicit Nat change")

    # Round 2 is driven by the complete round-1 exact Lean errors, not merely
    # line edits: the associator is an invertible Nat 2-cell, so it is zero.
    # LocallyDiscrete first morphisms are Discrete wrappers, and the underlying
    # Fin preorder category is thin. Only after Discrete.ext may subsingleton
    # elimination be used. These do not change the theorem assumptions.
    round2 = replace_once(add_simp,
        "  rw [hmap₂] at hcoh\n"
        "  simpa only [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] using hcoh",
        "  have hassoc :\n"
        "      (α_ (sigma.map f) (sigma.map g) (sigma.map h)).hom = (0 : Nat) :=\n"
        "    NatDoubleDelooping.isIso_twoCell_eq_zero _\n"
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  simpa only [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] using hcoh",
        "associator IsIso zero normalization")

    old_omega = (
        "  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h\n"
        "  omega"
    )
    if round2.count(old_omega) != 2:
        raise RuntimeError("unexpected v1.97 number of tetrahedron omega goals")
    first = (
        "  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h\n"
        "  have hsum :\n"
        "      Nat.add (sigma.mapComp g h) (sigma.mapComp f (g ≫ h)) = (0 : Nat) := by\n"
        "    calc\n"
        "      _ = Nat.add (sigma.mapComp f g) (sigma.mapComp (f ≫ g) h) := hcocycle.symm\n"
        "      _ = Nat.add (0 : Nat) (0 : Nat) := by rw [hfg, hfg_h]\n"
        "      _ = 0 := by rfl\n"
        "  exact Nat.eq_zero_of_add_eq_zero hsum"
    )
    second = (
        "  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h\n"
        "  have hsum :\n"
        "      Nat.add (sigma.mapComp f g) (sigma.mapComp (f ≫ g) h) = (0 : Nat) := by\n"
        "    calc\n"
        "      _ = Nat.add (sigma.mapComp g h) (sigma.mapComp f (g ≫ h)) := hcocycle\n"
        "      _ = Nat.add (0 : Nat) (0 : Nat) := by rw [hgh, houter]\n"
        "      _ = 0 := by rfl\n"
        "  exact (Nat.eq_zero_of_add_eq_zero hsum).2"
    )
    round2 = round2.replace(old_omega, first, 1)
    round2 = round2.replace(old_omega, second, 1)
    for signature in (
        "he02 : e01 ≫ e12 = e02",
        "he14 : e12 ≫ e24 = e14",
        "he03 : e01 ≫ e13 = e03",
        "he14 : e13 ≫ e34 = e14",
    ):
        round2 = replace_once(round2,
            "  have " + signature + " := Subsingleton.elim _ _",
            "  have " + signature + " := by\n"
            "    apply Discrete.ext\n"
            "    exact Subsingleton.elim _ _",
            "Discrete.ext " + signature)

    round2_rfl = replace_once(round2,
        "  have hassoc :\n"
        "      (α_ (sigma.map f) (sigma.map g) (sigma.map h)).hom = (0 : Nat) :=\n"
        "    NatDoubleDelooping.isIso_twoCell_eq_zero _",
        "  have hassoc :\n"
        "      (α_ (sigma.map f) (sigma.map g) (sigma.map h)).hom = (0 : Nat) := by\n"
        "    rfl",
        "direct strict associator rfl comparison")

    # Round 3: the full kernel goal after round 2 is
    #   a + (b + 0) = 0 + (c + d)
    # rather than a + b = c + d. Keep the necessary
    # CategoryStruct/whisker reduction separate from Nat.zero_add.
    # Also actually use hfg in the second propagation lemma; disabling
    # the unused-variable linter is explicitly forbidden.
    second_old = (
        "  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h\n"
        "  have hsum :\n"
        "      Nat.add (sigma.mapComp f g) (sigma.mapComp (f ≫ g) h) = (0 : Nat) := by\n"
        "    calc\n"
        "      _ = Nat.add (sigma.mapComp g h) (sigma.mapComp f (g ≫ h)) := hcocycle\n"
        "      _ = Nat.add (0 : Nat) (0 : Nat) := by rw [hgh, houter]\n"
        "      _ = 0 := by rfl\n"
        "  exact (Nat.eq_zero_of_add_eq_zero hsum).2"
    )
    second_new = (
        "  have hcocycle := natDuskin_mapComp_additive_cocycle sigma f g h\n"
        "  rw [hfg] at hcocycle\n"
        "  have hsum :\n"
        "      Nat.add (0 : Nat) (sigma.mapComp (f ≫ g) h) = (0 : Nat) := by\n"
        "    calc\n"
        "      _ = Nat.add (sigma.mapComp g h) (sigma.mapComp f (g ≫ h)) := hcocycle\n"
        "      _ = Nat.add (0 : Nat) (0 : Nat) := by rw [hgh, houter]\n"
        "      _ = 0 := by rfl\n"
        "  exact (Nat.eq_zero_of_add_eq_zero hsum).2"
    )
    base3 = replace_once(round2, second_old, second_new, "use hfg in strict proof")
    simpl_old = (
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  simpa only [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] using hcoh"
    )
    round3_fullsimp = replace_once(base3, simpl_old,
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  simpa [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] using hcoh",
        "round3 full simp")

    round3_twophase = replace_once(base3, simpl_old,
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  simp only [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft] at hcoh\n"
        "  simpa only [Nat.add_zero, Nat.zero_add] using hcoh",
        "round3 two-stage simp")

    round3_explicit = replace_once(base3, simpl_old,
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  change Nat.add (sigma.mapComp f g)\n"
        "      (Nat.add (sigma.mapComp (f ≫ g) h) (0 : Nat)) =\n"
        "    Nat.add (0 : Nat) (Nat.add (sigma.mapComp g h)\n"
        "      (sigma.mapComp f (g ≫ h))) at hcoh\n"
        "  simpa only [Nat.add_zero, Nat.zero_add] using hcoh",
        "round3 explicit raw Nat hypothesis")

    round3_lemma_simp = replace_once(base3, simpl_old,
        "  rw [hmap₂, hassoc] at hcoh\n"
        "  simp [CategoryStruct.comp, Bicategory.whiskerRight,\n"
        "    Bicategory.whiskerLeft, Nat.add_zero, Nat.zero_add] at hcoh\n"
        "  exact hcoh",
        "round3 simp at hcoh")

    return {
        "round1-typed-dependent-hom-zeros": typed,
        "round1-explicit-nat-add-change-simp": add_raw,
        "round1-explicit-nat-add-simp": add_simp,
        "round1-explicit-nat-add-change-omega": add_omega,
        "round2-associator-isIso-discrete-ext-nat-split": round2,
        "round2-associator-rfl-discrete-ext-nat-split": round2_rfl,
        "round3-associator-simp-nat": round3_fullsimp,
        "round3-associator-two-phase": round3_twophase,
        "round3-associator-explicit-change": round3_explicit,
        "round3-associator-simp-at": round3_lemma_simp,
    }


def read_example(filename: str) -> dict:
    return json.loads((ROOT/"examples"/filename).read_text(encoding="utf-8"))


def source_observation(head: str,branch: str,tree: str,source:bytes) -> dict:
    sample = read_example("codeai_intent_repository_observation_envelope_v0_1.json")
    t = int(time.time())
    intent = deepcopy(sample["intent_packet"])
    intent.update({
        "intent_id":"kuuos-v197-typed-zero-"+head[:12],
        "source_actor_id":"codeai-proof-research",
        "source_channel":"github-parent-strict-lean-log",
        "requirements":["repair v1.97 typed Nat 2-cells and syntax without changing theorem statements"],
        "assumptions":["CodeAI proposals require pinned Lean4 direct check and independent CI"],
        "unresolved_questions":[],
        "preserved_invariants":["same root", "theorem statements unchanged", "no sorry or new axiom"],
        "forbidden_changes":["no theorem weakening", "no main merge", "no legacy changes"],
        "success_criteria":["exact source-bound candidate audit only"],
        "intent_created_epoch":t,
        "prior_intent_digests":[],
        "intent_provenance_confirmed":True,
    })
    intent = obs.seal(intent,obs.INTENT_DIGEST_FIELD)
    paths=[TARGET,"formal/KUOS/DependentOriginationDoubleDeloopingThinComparisonZeroV1_96.lean",
           "lean-toolchain","lake-manifest.json"]
    if any(not (ROOT/x).is_file() for x in paths):
        raise RuntimeError("required observed predecessor missing")
    toolchain=(ROOT/"lean-toolchain").read_text().strip()
    if toolchain!="leanprover/lean4:v4.30.0-rc2":
        raise RuntimeError("Lean pin changed")
    manifest=json.loads((ROOT/"lake-manifest.json").read_text())
    pinned=[x for x in manifest["packages"] if x.get("name")=="mathlib"]
    if len(pinned)!=1 or pinned[0].get("rev")!="5450b53e5ddc75d46418fabb605edbf36bd0beb6":
        raise RuntimeError("mathlib pin changed")
    repo = deepcopy(sample["repository_observation"])
    repo.update({
        "repository_full_name":REPO,
        "source_commit_sha":head,
        "source_branch":branch,
        "tree_digest":tree,
        "dependency_lock_digest":sha256((ROOT/"lake-manifest.json").read_bytes()),
        "toolchain_digest":"lean-4.30.0-rc2-python-3.12",
        "toolchain_supported":True,
        "observed_paths":paths,
        "unavailable_paths":[],
        "declared_path_count":len(paths),
        "baseline_check_digests":["v197-exact-blob:"+git_blob(source),"import-v196:"+git_blob((ROOT/paths[1]).read_bytes())],
        "baseline_checks_complete":True,
        "code_owner_scope_digest":"repo-owner:"+REPO,
        "crosses_unowned_boundary":False,
        "observation_started_epoch":t,
        "observation_completed_epoch":int(time.time()),
        "session_id":"v197-"+head[:16],
        "nonce_digest":hashlib.sha256((head+":v197-actual").encode()).hexdigest(),
        "prior_session_ids":[],
        "prior_nonce_digests":[],
        "prior_observation_digests":[],
    })
    repo=obs.seal(repo,obs.REPOSITORY_OBSERVATION_DIGEST_FIELD)
    policy=deepcopy(sample["observation_policy"])
    policy.update({
        "expected_repository_full_name":REPO,
        "expected_source_commit_sha":head,
        "allowed_source_branches":[branch],
        "supported_toolchain_digests":["lean-4.30.0-rc2-python-3.12"],
        "require_complete_baseline":True,
        "require_code_owner_scope":True,
        "allow_partial_observation":False,
    })
    policy=obs.seal(policy,obs.POLICY_DIGEST_FIELD)
    result=obs.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent,repository_observation=repo,observation_policy=policy)
    if result.status!=obs.STATUS_READY or result.receipt is None or result.receipt["codeai_disposition"]!=obs.DISPOSITION_SUPPORTED:
        raise RuntimeError("real v1.97 CodeAI observation refused:"+repr(result.issues))
    return result.receipt


def main() -> int:
    head,branch,tree=require_event()
    source_path=ROOT/TARGET
    original=source_path.read_bytes()
    if git_blob(original)!=ORIGINAL_BLOB:
        raise RuntimeError("v1.97 original exact-source blob drift")
    record=source_observation(head,branch,tree,original)
    candidate_source=variants(original.decode("utf-8"))
    statements=lambda s:[
        (x["kind"],x["name_lexical"],x["signature_sha256"])
        for x in declarations_of(s,MODULE)]
    for name,src in candidate_source.items():
        if imports_of(src)!=imports_of(original.decode()):
            raise RuntimeError("changed v1.97 imports:"+name)
        # Only explicit Nat ascriptions (definitionally Nat Hom in the fixed
        # kernel) or exact qualified name/universe corrections are proposed.
        # Any lexical change remains UNADMITTED until the kernel verifies it.
        deltas=[x for x in statements(src) if x not in statements(original.decode())]
        print("KUUOS_V197_LEXICAL_SIGNATURE_RECHECK "+
              json.dumps({"candidate":name,"changed_declaration_signatures":len(deltas),
                          "kernel_equivalence_required":bool(deltas)},sort_keys=True))
        for forbidden in ("sorry","admit","axiom","unsafe","native_decide"):
            if forbidden in src and forbidden not in original.decode():
                raise RuntimeError("new forbidden content:"+name)
    t=int(time.time())
    template=read_example("codeai_candidate_patch_envelope_v0_1.json")
    policy=deepcopy(template["candidate_policy"])
    policy.update({
        "expected_source_observation_receipt_digest":record[obs.RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name":REPO,
        "expected_source_commit_sha":head,
        "allowed_patch_formats":["unified_diff"],
        "maximum_changed_paths":1,
        "allowed_path_prefixes":["formal/KUOS"],
        "forbidden_path_prefixes":["legacy"],
        "allow_deletions":False,
        "allow_renames":False,
        "allow_binary_patches":False,
        "allow_submodule_patches":False,
        "allow_mode_changes":False,
        "require_requirement_trace":True,
        "require_test_plan":True,
        "allow_evidence_degradation":False,
        "known_risk_labels":["formal-proof"],
        "handover_risk_labels":[],
        "evaluation_epoch":t+30,
        "maximum_candidate_age":3600,
    })
    policy=patch.seal(policy,patch.POLICY_DIGEST_FIELD)
    proposals=[{
        "proposal_id":"v197-"+name+"-"+head[:10],
        "candidate_revision":"r1",
        "producer_id":"external-structural-Lean4-repair",
        "producer_session_id":"v197-repair-"+str(i)+"-"+head[:10],
        "candidate_created_epoch":t,
        "edits":[{"path":TARGET,"operation":"modify","new_content":content}],
        "requirement_trace_ids":["v197:NatHom-universe0-and-Lean-keyword"],
        "test_plan_ids":["v197:exact-pinned-lake-env-lean"],
        "risk_labels":["formal-proof"],
        "unresolved_candidate_questions":[],
        "prior_candidate_digests":[],
        "prior_producer_session_ids":[],
    } for i,(name,content) in enumerate(candidate_source.items())]
    generated=diff.build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=record,repository_files={TARGET:original.decode()},
        proposals=proposals,candidate_policy=policy)
    if generated.status!=diff.STATUS_READY or generated.receipt is None or len(generated.candidates)!=len(proposals):
        raise RuntimeError("CodeAI generation blocked:"+repr(generated.issues))
    output=Path("/tmp/kuuos-v197-codeai-type-probes")
    if output.exists():
        raise RuntimeError("append-only output path already present")
    output.mkdir(parents=True,exist_ok=False)
    result={"head":head,"source_tree":tree,"original_blob":ORIGINAL_BLOB,
        "observation_receipt":record[obs.RECEIPT_DIGEST_FIELD],
        "portfolio_receipt":generated.receipt[diff.RECEIPT_DIGEST_FIELD],
        "candidates":[],"source_restored":False,"independent_ci_certified":False,
        "kernel_signature_equivalence_pending":True,"git_written":False}
    mode=stat.S_IMODE(source_path.stat().st_mode)
    try:
        for item in generated.candidates:
            expected={("v197-"+name+"-"+head[:10]):name
                      for name in candidate_source}
            key=expected.get(item.patch_candidate["candidate_id"])
            if key is None:
                raise RuntimeError("CodeAI returned alien/ambiguous candidate ID")
            if item.patch_candidate["changed_paths"] != [TARGET]:
                raise RuntimeError("CodeAI altered candidate changed-path scope")
            updated=candidate_source[key].encode()
            row={"variant":key,"candidate_blob":git_blob(updated),
                 "candidate_sha256":sha256(updated),
                 "candidate_receipt":item.candidate_receipt["codeai_candidate_patch_receipt_digest"],
                 "status":"NOT_RUN"}
            try:
                source_path.write_bytes(updated)
                with tempfile.TemporaryDirectory(prefix="v197-lean-") as td:
                    try:
                        done=subprocess.run([
                            "lake","env","lean","-DwarningAsError=true",
                            "-Dweak.sorryAsError=true","-o",td+"/probe.olean",TARGET
                        ],cwd=ROOT,capture_output=True,text=True,check=False,timeout=300)
                        outputText=done.stdout+"\n"+done.stderr
                        row["status"]="SUCCESS" if done.returncode==0 else "FAILURE"
                        row["exit_code"]=done.returncode
                        row["olean_exists"]=Path(td+"/probe.olean").is_file()
                    except subprocess.TimeoutExpired as ex:
                        row["status"]="TIMEOUT"
                        outputText=str(ex.stdout or "")+"\n"+str(ex.stderr or "")
                    (output/(key+".log")).write_text(outputText)
                    row["log_sha256"]=sha256(outputText.encode())
                    error_lines=[x for x in outputText.splitlines()
                        if "error:" in x or "error(" in x]
                    row["errors"]=[x[:480] for x in error_lines][:80]
                    row["error_count"]=len(error_lines)
            finally:
                source_path.write_bytes(original)
                source_path.chmod(mode)
                if source_path.read_bytes()!=original:
                    raise RuntimeError("v1.97 original not restored")
            result["candidates"].append(row)
            print("KUUOS_V197_TYPED_CODEAI_CANDIDATE "+json.dumps(row,ensure_ascii=False,sort_keys=True))
    finally:
        source_path.write_bytes(original)
        source_path.chmod(mode)
        result["source_restored"]=source_path.read_bytes()==original
    (output/"portfolio_receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    passed=[x for x in result["candidates"] if x["status"]=="SUCCESS"]
    print("KUUOS_V197_TYPED_CODEAI_SUMMARY "+json.dumps({
        "source_head":head,"candidate_count":len(result["candidates"]),
        "strict_direct_success_count":len(passed),"source_restored":result["source_restored"],
        "portfolio_receipt":result["portfolio_receipt"],"independent_ci_certified":False
    },sort_keys=True))
    return 0 if result["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
