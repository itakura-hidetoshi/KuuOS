#!/usr/bin/env python3
"""KuuOS CodeAI exact-HEAD v1.102 type/universe structural repair portfolio.

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
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102"
ORIGINAL_BLOB = "7274ceba97bb4bf7b3aaffa9862952d79cf6f4c3"
PREFIX = "open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101\n"


def require_event() -> tuple[str,str]:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if event.get("number") != 3522 or event.get("repository",{}).get("full_name") != REPO:
        raise RuntimeError("exact parent PR event required")
    pr = event["pull_request"]
    source_head = pr["head"]["sha"]
    branch = pr["head"]["ref"]
    url = "https://api.github.com/repos/"+REPO+"/git/commits/"+source_head
    headers={"Accept":"application/vnd.github+json","User-Agent":"KuuOS-CodeAI-v1102"}
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("authenticated GitHub API token required for exact source/tree observation")
    headers["Authorization"]="Bearer "+token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req,timeout=30) as response:
        data = json.load(response)
    tree = data.get("tree",{}).get("sha")
    if data.get("sha") != source_head or not isinstance(tree,str) or not re.fullmatch("[a-f0-9]{40}",tree):
        raise RuntimeError("exact GitHub source/tree unverified")
    return source_head,branch,tree


def replace_once(source: str, old: str, new: str, name: str) -> str:
    occurrences = source.count(old)
    if occurrences != 1:
        raise RuntimeError(f"v1.102 source drift: {name}: {occurrences}")
    return source.replace(old, new, 1)


def replace_once(source: str, old: str, new: str, label: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("v1.102 exact source drift: "+label)
    return source.replace(old,new,1)


def replace_once(source: str, old: str, new: str, label: str) -> str:
    n = source.count(old)
    if n != 1:
        raise RuntimeError(f"v1.102 exact source drift {label}: {n}")
    return source.replace(old, new, 1)


def variants(source: str) -> dict[str,str]:
    """Pinned Lean 4.30 v1.102 low-dimensional type-A filler portfolio.

    Preserve imports, names, assumptions and each intended theorem. Test
    syntax errors separately from dependent-Hom elaboration; never promote
    a candidate without a real direct kernel success and independent CI.
    """
    if source.count(PREFIX)!=1:
        raise RuntimeError("v1.102 exact-source namespace drift")
    base=replace_once(source,
        "  attribute [local ext] StrictlyUnitaryLaxFunctor\n", "",
        "move ext attribute out of tactic mode")
    base=replace_once(base, "theorem natDuskinSimplex_eq_of_mapComp_eq",
        "attribute [local ext] StrictlyUnitaryLaxFunctor\n\n"
        "theorem natDuskinSimplex_eq_of_mapComp_eq",
        "pinned mathlib top-level ext attribute")
    typed=replace_once(base, "    sigma.mapId a = 0 := by",
        "    sigma.mapId a = (0 : Nat) := by","dependent mapId Nat zero")
    typed=replace_once(typed,
        "  exact NatDoubleDelooping.isIso_twoCell_eq_zero _",
        "  rw [StrictlyUnitaryLaxFunctor.mapId_eq_eqToHom]\n"
        "  exact NatDoubleDelooping.isIso_twoCell_eq_zero _",
        "mapId use explicit unit coherence")
    discrete=typed
    for old in (
        "    have hf : f = 𝟙 a := Subsingleton.elim _ _",
        "      have hg : g = 𝟙 b := Subsingleton.elim _ _",
        "      have hf : f = edge01 := Subsingleton.elim _ _",
        "      have hg : g = edge12 := Subsingleton.elim _ _",
    ):
        before,after=old.split(":= ",1)
        indent=" " * (len(old)-len(old.lstrip(" ")))
        discrete=replace_once(discrete,old,
            before+":= by\n"
            + indent+"  apply Discrete.ext\n"
            + indent+"  exact Subsingleton.elim _ _",
            "LocallyDiscrete Hom " + before.strip())
    # A field-notation error is not evidence that TypeADistinguishedZero
    # is missing. It is declared in v1.101's nested local namespace.
    full="KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.NatNormalizedDuskinCocycle.TypeADistinguishedZero"
    repaired=replace_once(discrete,
        "(natThreeCocycleOfLabels 0 a013 a023 a123 hcoh).\n"
        "      TypeADistinguishedZero (1 : Fin 4) := by",
        full+"\n"
        "      (natThreeCocycleOfLabels 0 a013 a023 a123 hcoh) (1 : Fin 4) := by",
        "type A inner i1 local declaration")
    repaired=replace_once(repaired,
        "(natThreeCocycleOfLabels a012 a013 a023 0 hcoh).\n"
        "      TypeADistinguishedZero (2 : Fin 4) := by",
        full+"\n"
        "      (natThreeCocycleOfLabels a012 a013 a023 0 hcoh) (2 : Fin 4) := by",
        "type A inner i2 local declaration")
    # The two horn comparison zeros are 2-hom expressions, definitionally
    # Nat; annotate *only* these typed occurrences.
    for target in (
        "    duskinComparison\n"
        "      (f.map.app (op ⦋2⦌)\n"
        "        (SSet.horn.face (1 : Fin 4) (3 : Fin 4) (by decide))) = 0 := by",
        "    duskinComparison\n"
        "      (f.map.app (op ⦋2⦌)\n"
        "        (SSet.horn.face (2 : Fin 4) (0 : Fin 4) (by decide))) = 0 := by",
    ):
        repaired=replace_once(repaired,target,
            target.replace("= 0 := by","= (0 : Nat) := by"),
            "typed horn comparison zero")
    simplified=repaired
    if simplified.count("  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle])")!=2:
        raise RuntimeError("distinguished triangle tactic scope drift")
    simplified=simplified.replace(
        "  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle])",
        "  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle,\n"
        "    SSet.stdSimplex.triangle])")
    finarith=simplified
    finarith=finarith.replace("        apply Fin.ext\n        omega",
        "        apply Fin.ext\n        simp only [Fin.val_zero, Fin.val_one, Fin.val_two]\n"
        "        omega")
    if finarith==simplified:
        raise RuntimeError("finite ordinal arithmetic candidate unchanged")
    # Round 2 uses the full exact pinned Lean log (CI #43679639281):
    # 1. `attribute [local ext]` is a COMMAND and must precede its
    #    documented declaration, never appear inside proof tactics or
    #    immediately after a doc comment attached to a theorem.
    # 2. On Fin 3, `Fin.ext` goals must normalize numeral values
    #    to actual Nat literals before Presburger/omega; otherwise omega
    #    treats Fin.ofNat as a fresh variable and admits countermodels.
    # 3. The failed map-comp rewrite was being tried on a 1-cell map goal.
    #    Explicitly force the NatOneCell type before subsingleton reasoning.
    fixed=replace_once(simplified,
        "attribute [local ext] StrictlyUnitaryLaxFunctor\n\n"
        "theorem natDuskinSimplex_eq_of_mapComp_eq",
        "theorem natDuskinSimplex_eq_of_mapComp_eq",
        "remove attached-doc attribute")
    fixed=replace_once(fixed,PREFIX,
        PREFIX+"\nattribute [local ext] StrictlyUnitaryLaxFunctor\n",
        "introduce top-level ext command before module docs")
    finite=fixed
    for context,value,num,label in (
        ("ha0 : a.as = (0 : Fin 3)", "a.as.val", "0", "Fin a zero"),
        ("hb1 : b.as = (1 : Fin 3)", "b.as.val", "1", "Fin b one"),
        ("hc2 : c.as = (2 : Fin 3)", "c.as.val", "2", "Fin c two"),
    ):
        old=("      have "+context+" := by\n"
             "        apply Fin.ext\n"
             "        omega")
        new=("      have "+context+" := by\n"
             "        apply Fin.ext\n"
             "        change "+value+" = "+num+"\n"
             "        omega")
        finite=replace_once(finite,old,new,label)
    extmap=replace_once(finite,
        "    first\n    | exact Subsingleton.elim _ _\n",
        "    first\n"
        "    | (change (_ : NatOneCell) = (_ : NatOneCell)\n"
        "       exact Subsingleton.elim _ _)\n"
        "    | exact Subsingleton.elim _ _\n",
        "typed map 1-cell ext target")
    # Unused omega follows simp_all on some normalized tetrahedron cases.
    # Use a bounded try, never weaken the arithmetic hypothesis.
    normalize=replace_once(extmap,
        "simp_all [NatTetrahedronEquation] <;> omega",
        "simp_all [NatTetrahedronEquation] <;> try omega",
        "avoid unnecessary omega after simp_all")
    if normalize.count(
        "  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle,\n"
        "    SSet.stdSimplex.triangle])")!=2:
        raise RuntimeError("two distinguished type A triangle proofs moved")
    concrete=normalize.replace(
        "  exact Or.inr (by simp [IsStandardTypeADistinguishedTriangle,\n"
        "    SSet.stdSimplex.triangle])",
        "  exact Or.inr (by decide)")
    simpall=replace_once(concrete,
        "  simp [natThreeCocycleOfLabels, ha1, hb, hc3]",
        "  simp_all [natThreeCocycleOfLabels]",
        "type A i2 normalized 1-2-3 strict label")
    # Alternative proof uses the explicit nonzero Fin witness rather than
    # relying on simp_all's rewriting order.
    nonzero=replace_once(concrete,
        "  simp [natThreeCocycleOfLabels, ha1, hb, hc3]",
        "  have ha_ne_zero : a ≠ (0 : Fin 4) := by\n"
        "    intro h\n"
        "    have hv : a.val = 0 := congrArg Fin.val h\n"
        "    omega\n"
        "  simp [natThreeCocycleOfLabels, ha_ne_zero, hb, hc3]",
        "type A i2 finite element not zero")
    # Round 3: from the exact round2 isolated kernel logs.
    # "omega tactic does nothing" is a STRICT linter failure: `simp_all`
    # already closed the branch. Keep the full arithmetic proof but do not
    # run a redundant final tactic. The only mathematical residual is i=2
    # where a.val=1 but `simp` leaves a spurious a=0 conditional.
    # Expose Fin a != 0 / a=1 before unfolding the normalized cocycle.
    tetra=replace_once(extmap,
        "simp_all [NatTetrahedronEquation] <;> omega",
        "simp_all [NatTetrahedronEquation]",
        "remove unused final omega")
    old_i2="  simp [natThreeCocycleOfLabels, ha1, hb, hc3]"
    direct_nonzero=(
        "  have ha_ne_zero : a ≠ (0 : Fin 4) := by\n"
        "    intro h\n"
        "    have hv : a.val = 0 := congrArg Fin.val h\n"
        "    omega\n"
        "  simp [natThreeCocycleOfLabels, ha_ne_zero, hb, hc3]"
    )
    nat_nonzero=(
        "  have ha_ne_zero : a.val ≠ 0 := by omega\n"
        "  simp [natThreeCocycleOfLabels, ha_ne_zero, ha1, hb, hc3]"
    )
    subst_fin=(
        "  have ha_eq_one : a = (1 : Fin 4) := by\n"
        "    apply Fin.ext\n"
        "    change a.val = 1\n"
        "    exact ha1\n"
        "  subst a\n"
        "  simp [natThreeCocycleOfLabels, hb, hc3]"
    )
    alt_simpall=(
        "  have ha_ne_zero : a ≠ (0 : Fin 4) := by\n"
        "    intro h\n"
        "    have hv : a.val = 0 := congrArg Fin.val h\n"
        "    omega\n"
        "  simp_all [natThreeCocycleOfLabels]"
    )
    i2_a=replace_once(tetra,old_i2,direct_nonzero,
        "type A i2 Fin not-zero")
    i2_b=replace_once(tetra,old_i2,nat_nonzero,
        "type A i2 Nat not-zero")
    i2_c=replace_once(tetra,old_i2,subst_fin,
        "type A i2 Fin successor substitution")
    i2_d=replace_once(tetra,old_i2,alt_simpall,
        "type A i2 simp all")
    return {
      "round1-move-ext-attribute":base,
      "round1-typed-mapId":typed,
      "round1-discrete-homs-and-local-typeA":repaired,
      "round1-distinguished-triangle-simp":simplified,
      "round1-finarith-simp-omega":finarith,
      "round2-attribute-before-doc":fixed,
      "round2-explicit-Fin-numerals":finite,
      "round2-explicit-one-cell-map":extmap,
      "round2-concrete-triangle-simp-all":simpall,
      "round2-concrete-triangle-finite-nonzero":nonzero,
      "round3-no-redundant-omega":tetra,
      "round3-i2-explicit-Fin-nonzero":i2_a,
      "round3-i2-explicit-Nat-nonzero":i2_b,
      "round3-i2-substitute-one":i2_c,
      "round3-i2-simp-all":i2_d,
    }


def read_example(filename: str) -> dict:
    return json.loads((ROOT/"examples"/filename).read_text(encoding="utf-8"))


def source_observation(head: str,branch: str,tree: str,source:bytes) -> dict:
    sample = read_example("codeai_intent_repository_observation_envelope_v0_1.json")
    t = int(time.time())
    intent = deepcopy(sample["intent_packet"])
    intent.update({
        "intent_id":"kuuos-v1102-typed-zero-"+head[:12],
        "source_actor_id":"codeai-proof-research",
        "source_channel":"github-parent-strict-lean-log",
        "requirements":["repair v1.102 typed Nat 2-cells and syntax without changing theorem statements"],
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
    paths=[TARGET,"formal/KUOS/DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.lean",
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
        "baseline_check_digests":["v1102-exact-blob:"+git_blob(source),"import-v199:"+git_blob((ROOT/paths[1]).read_bytes())],
        "baseline_checks_complete":True,
        "code_owner_scope_digest":"repo-owner:"+REPO,
        "crosses_unowned_boundary":False,
        "observation_started_epoch":t,
        "observation_completed_epoch":int(time.time()),
        "session_id":"v1102-"+head[:16],
        "nonce_digest":hashlib.sha256((head+":v1102-actual").encode()).hexdigest(),
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
        raise RuntimeError("real v1.102 CodeAI observation refused:"+repr(result.issues))
    return result.receipt


def main() -> int:
    head,branch,tree=require_event()
    source_path=ROOT/TARGET
    original=source_path.read_bytes()
    if git_blob(original)!=ORIGINAL_BLOB:
        raise RuntimeError("v1.102 original source blob drift")
    record=source_observation(head,branch,tree,original)
    candidate_source=variants(original.decode("utf-8"))
    statements=lambda s:[
        (x["kind"],x["name_lexical"],x["signature_sha256"])
        for x in declarations_of(s,MODULE)]
    for name,src in candidate_source.items():
        if imports_of(src)!=imports_of(original.decode()):
            raise RuntimeError("changed v1.102 imports:"+name)
        # Only explicit Nat ascriptions (definitionally Nat Hom in the fixed
        # kernel) or exact qualified name/universe corrections are proposed.
        # Any lexical change remains UNADMITTED until the kernel verifies it.
        deltas=[x for x in statements(src) if x not in statements(original.decode())]
        print("KUUOS_V1102_LEXICAL_SIGNATURE_RECHECK "+
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
        "proposal_id":"v1102-"+name+"-"+head[:10],
        "candidate_revision":"r1",
        "producer_id":"external-structural-Lean4-repair",
        "producer_session_id":"v1102-repair-"+str(i)+"-"+head[:10],
        "candidate_created_epoch":t,
        "edits":[{"path":TARGET,"operation":"modify","new_content":content}],
        "requirement_trace_ids":["v1102:NatHom-universe0-and-Lean-keyword"],
        "test_plan_ids":["v1102:exact-pinned-lake-env-lean"],
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
    output=Path("/tmp/kuuos-v1102-codeai-type-probes")
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
            expected={("v1102-"+name+"-"+head[:10]):name
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
                with tempfile.TemporaryDirectory(prefix="v1102-lean-") as td:
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
                    raise RuntimeError("v1.102 original not restored")
            result["candidates"].append(row)
            print("KUUOS_V1102_TYPED_CODEAI_CANDIDATE "+json.dumps(row,ensure_ascii=False,sort_keys=True))
    finally:
        source_path.write_bytes(original)
        source_path.chmod(mode)
        result["source_restored"]=source_path.read_bytes()==original
    (output/"portfolio_receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    passed=[x for x in result["candidates"] if x["status"]=="SUCCESS"]
    print("KUUOS_V1102_TYPED_CODEAI_SUMMARY "+json.dumps({
        "source_head":head,"candidate_count":len(result["candidates"]),
        "strict_direct_success_count":len(passed),"source_restored":result["source_restored"],
        "portfolio_receipt":result["portfolio_receipt"],"independent_ci_certified":False
    },sort_keys=True))
    return 0 if result["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
