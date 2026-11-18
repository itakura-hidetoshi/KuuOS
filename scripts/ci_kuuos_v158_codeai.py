#!/usr/bin/env python3
"""CodeAI source-bound v1.58 Type-C collapsed edge, fixed universe and pushout API candidates.
Only a disposable Actions checkout is patched; GitHub proof files are never written.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile

NS = 'KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = 'bf3215c269144bfe075816e35b04ae26c616d7ed'
REFERENCE_BLOB = '05c257663da028e4cca7907c9d5b7e7221468ac8'
DEP = 'formal/KUOS/DependentOriginationStandardTypeBThreeSimplexCompletionV1_57.lean'
DEP_BLOB = '735fc7afffc7806bf6eac41c6c8fdc60a6cea95a'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v158-codeai-typec-collapsed-edge-real-mcp-v1.yml'
NAMES = ["standardTypeCEdgeFace","standardTypeCEdgeFace_le_horn","standardTypeCEdgeToHorn","standardTypeCEdgeToSimplex","standardTypeCEdgeCollapseToPoint","standardTypeCEdgeToHorn_comp_hornInclusion","standardTypeCSourceCarrier","standardTypeCTargetCarrier","standardTypeCSourceCarrier_isPushout","standardTypeCTargetCarrier_isPushout","standardTypeCSource_edge_collapsed","standardTypeCTarget_edge_collapsed","standardTypeCCarrierMap","standardTypeCCarrierMap_inl_horn","standardTypeCCarrierMap_inr_point","standardTypeCTriangle01n","standardTypeCTriangle01nInHorn","standardTypeCSourceDistinguishedTriangle","standardTypeCTargetDistinguishedTriangle","standardTypeCCarrierMap_distinguishedTriangle","minimalPlusTriangleScaling","standardTypeCSourceScaling","standardTypeCTargetScaling","standardTypeCSource","standardTypeCTarget","standardTypeCGeneratorHom","standardTypeCTarget_distinguished_thin","standardTypeCSource_distinguished_thin","standardTypeCScaledAnodyneGenerators","standardTypeCGenerator_mem","standardTypeC_dimension_gt_two","exists_standardTypeC_index_of_dimension_gt_two","standardScaledAnodyneGeneratorsABC","standardTypeAGenerators_le_ABC","standardTypeBGenerators_le_ABC","standardTypeCGenerators_le_ABC","standardTypeAGenerator_mem_ABC","standardTypeBGenerator_mem_ABC","standardTypeCGenerator_mem_ABC","standardGeneratedScaledAnodyneABC","standardGeneratedScaledFibrationABC","standardScaledAnodyneGeneratorsABC_le_generated","standardTypeAGenerator_mem_standardGenerated","standardTypeBGenerator_mem_standardGenerated","standardTypeCGenerator_mem_standardGenerated","standardTypeBCollapse12Completion_mem_standardGenerated","standardTypeBCollapse23Completion_mem_standardGenerated","standardTypeBThreeSimplexCompletionStable_standardGenerated","standardGeneratedScaledAnodyneABC_eq_external","standardGeneratedScaledFibrationABC_eq_external"]
# Version-bound line-aligned 57-hunk difference against the unchanged historic source.
# Reference proof source is a candidate, not certification.
HUNKS = [{"at":73,"old":["    standardTypeCEdgeFace m ≤"],"new":["    standardTypeCEdgeFace.{u} m ≤"]},{"at":76,"old":["      standardTypeCEdgeFace m ≤"],"new":["      standardTypeCEdgeFace.{u} m ≤"]},{"at":84,"old":["    rcases hj with rfl | rfl <;> simp"],"new":["    rcases hj with rfl | rfl","    · simp only [Finset.mem_compl, Finset.mem_singleton]","      intro h","      have hv := congrArg Fin.val h","      have hlt : 2 < m + 4 := by omega","      norm_num [Nat.mod_eq_of_lt hlt] at hv","    · simp only [Finset.mem_compl, Finset.mem_singleton]","      intro h","      have hv := congrArg Fin.val h","      have hlt : 2 < m + 4 := by omega","      norm_num [Nat.mod_eq_of_lt hlt] at hv"]},{"at":87,"old":["      (2 : Fin (m + 4)) (0 : Fin (m + 4)) (by omega))"],"new":["      (2 : Fin (m + 4)) (0 : Fin (m + 4)) (by","        intro h","        have hv := congrArg Fin.val h","        have hlt : 2 < m + 4 := by omega","        norm_num [Nat.mod_eq_of_lt hlt] at hv))"]},{"at":91,"old":["    (standardTypeCEdgeFace m : SSet.{u}) ⟶"],"new":["    (standardTypeCEdgeFace.{u} m : SSet.{u}) ⟶"]},{"at":97,"old":["    (standardTypeCEdgeFace m : SSet.{u}) ⟶"],"new":["    (standardTypeCEdgeFace.{u} m : SSet.{u}) ⟶"]},{"at":99,"old":["  (standardTypeCEdgeFace m).ι"],"new":["  (standardTypeCEdgeFace.{u} m).ι"]},{"at":104,"old":["    (standardTypeCEdgeFace m : SSet.{u}) ⟶"],"new":["    (standardTypeCEdgeFace.{u} m : SSet.{u}) ⟶"]},{"at":110,"old":["    standardTypeCEdgeToHorn m ≫"],"new":["    standardTypeCEdgeToHorn.{u} m ≫"]},{"at":112,"old":["      standardTypeCEdgeToSimplex m := by"],"new":["      standardTypeCEdgeToSimplex.{u} m := by"]},{"at":120,"old":["    (standardTypeCEdgeToHorn m)","    (standardTypeCEdgeCollapseToPoint m)"],"new":["    (standardTypeCEdgeToHorn.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":126,"old":["    (standardTypeCEdgeToSimplex m)","    (standardTypeCEdgeCollapseToPoint m)"],"new":["    (standardTypeCEdgeToSimplex.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":131,"old":["    IsPushout","      (standardTypeCEdgeToHorn m)","      (standardTypeCEdgeCollapseToPoint m)"],"new":["    IsPushout (C := SSet.{u})","      (standardTypeCEdgeToHorn.{u} m)","      (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":135,"old":["        (standardTypeCEdgeToHorn m)","        (standardTypeCEdgeCollapseToPoint m))"],"new":["        (standardTypeCEdgeToHorn.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m))"]},{"at":138,"old":["        (standardTypeCEdgeToHorn m)","        (standardTypeCEdgeCollapseToPoint m)) :=","  pushoutIsPushout _ _"],"new":["        (standardTypeCEdgeToHorn.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m)) :=","  by","    exact IsPushout.of_hasPushout","      (standardTypeCEdgeToHorn.{u} m)","      (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":144,"old":["    IsPushout","      (standardTypeCEdgeToSimplex m)","      (standardTypeCEdgeCollapseToPoint m)"],"new":["    IsPushout (C := SSet.{u})","      (standardTypeCEdgeToSimplex.{u} m)","      (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":148,"old":["        (standardTypeCEdgeToSimplex m)","        (standardTypeCEdgeCollapseToPoint m))"],"new":["        (standardTypeCEdgeToSimplex.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m))"]},{"at":151,"old":["        (standardTypeCEdgeToSimplex m)","        (standardTypeCEdgeCollapseToPoint m)) :=","  pushoutIsPushout _ _"],"new":["        (standardTypeCEdgeToSimplex.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m)) :=","  by","    exact IsPushout.of_hasPushout","      (standardTypeCEdgeToSimplex.{u} m)","      (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":157,"old":["    standardTypeCEdgeToHorn m ≫"],"new":["    standardTypeCEdgeToHorn.{u} m ≫"]},{"at":159,"old":["          (standardTypeCEdgeToHorn m)","          (standardTypeCEdgeCollapseToPoint m) =","      standardTypeCEdgeCollapseToPoint m ≫"],"new":["          (standardTypeCEdgeToHorn.{u} m)","          (standardTypeCEdgeCollapseToPoint.{u} m) =","      standardTypeCEdgeCollapseToPoint.{u} m ≫"]},{"at":163,"old":["          (standardTypeCEdgeToHorn m)","          (standardTypeCEdgeCollapseToPoint m) :="],"new":["          (standardTypeCEdgeToHorn.{u} m)","          (standardTypeCEdgeCollapseToPoint.{u} m) :="]},{"at":169,"old":["    standardTypeCEdgeToSimplex m ≫"],"new":["    standardTypeCEdgeToSimplex.{u} m ≫"]},{"at":171,"old":["          (standardTypeCEdgeToSimplex m)","          (standardTypeCEdgeCollapseToPoint m) =","      standardTypeCEdgeCollapseToPoint m ≫"],"new":["          (standardTypeCEdgeToSimplex.{u} m)","          (standardTypeCEdgeCollapseToPoint.{u} m) =","      standardTypeCEdgeCollapseToPoint.{u} m ≫"]},{"at":175,"old":["          (standardTypeCEdgeToSimplex m)","          (standardTypeCEdgeCollapseToPoint m) :="],"new":["          (standardTypeCEdgeToSimplex.{u} m)","          (standardTypeCEdgeCollapseToPoint.{u} m) :="]},{"at":181,"old":["    standardTypeCSourceCarrier m ⟶ standardTypeCTargetCarrier m :="],"new":["    standardTypeCSourceCarrier.{u} m ⟶ standardTypeCTargetCarrier.{u} m :="]},{"at":183,"old":["    (standardTypeCEdgeToHorn m)","    (standardTypeCEdgeCollapseToPoint m)","    (standardTypeCEdgeToSimplex m)","    (standardTypeCEdgeCollapseToPoint m)"],"new":["    (standardTypeCEdgeToHorn.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)","    (standardTypeCEdgeToSimplex.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)"]},{"at":189,"old":["    (𝟙 (standardTypeCEdgeFace m : SSet.{u}))"],"new":["    (𝟙 (standardTypeCEdgeFace.{u} m : SSet.{u}))"]},{"at":197,"old":["        (standardTypeCEdgeToHorn m)","        (standardTypeCEdgeCollapseToPoint m) ≫","      standardTypeCCarrierMap m ="],"new":["        (standardTypeCEdgeToHorn.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m) ≫","      standardTypeCCarrierMap.{u} m ="]},{"at":202,"old":["        (standardTypeCEdgeToSimplex m)","        (standardTypeCEdgeCollapseToPoint m) := by","  simp [standardTypeCCarrierMap]"],"new":["        (standardTypeCEdgeToSimplex.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m) := by","  dsimp only [standardTypeCCarrierMap, pushout.map]","  exact pushout.inl_desc _ _ _"]},{"at":210,"old":["        (standardTypeCEdgeToHorn m)","        (standardTypeCEdgeCollapseToPoint m) ≫","      standardTypeCCarrierMap m ="],"new":["        (standardTypeCEdgeToHorn.{u} m)","        (standardTypeCEdgeCollapseToPoint.{u} m) ≫","      standardTypeCCarrierMap.{u} m ="]},{"at":214,"old":["      (standardTypeCEdgeToSimplex m)","      (standardTypeCEdgeCollapseToPoint m) := by","  simp [standardTypeCCarrierMap]"],"new":["      (standardTypeCEdgeToSimplex.{u} m)","      (standardTypeCEdgeCollapseToPoint.{u} m) := by","  dsimp only [standardTypeCCarrierMap, pushout.map]","  exact pushout.inr_desc _ _ _"]},{"at":227,"old":["    (by omega)","    (by omega)"],"new":["    (Fin.zero_le _)","    (Fin.le_last _)"]},{"at":234,"old":["  ⟨standardTypeCTriangle01n m, by"],"new":["  ⟨standardTypeCTriangle01n.{u} m, by"]},{"at":236,"old":["        standardTypeCTriangle01n m ∈"],"new":["        standardTypeCTriangle01n.{u} m ∈"]},{"at":240,"old":["      fin_cases j <;>","        simp [standardTypeCTriangle01n, Fin.ext_iff] <;> omega"],"new":["      have hlt : 2 < m + 4 := by omega","      have hlast :","          (Fin.last (m + 3) : Fin (m + 4)) ≠ (2 : Fin (m + 4)) := by","        intro h","        have hv := congrArg Fin.val h","        norm_num [Fin.val_last, Nat.mod_eq_of_lt hlt] at hv <;> omega","      fin_cases j","      · simp only [standardTypeCTriangle01n, SSet.stdSimplex.triangle,","          SSet.stdSimplex.objMk_apply, Finset.mem_compl, Finset.mem_singleton]","        intro h","        have hv := congrArg Fin.val h","        norm_num [Nat.mod_eq_of_lt hlt] at hv","      · simp only [standardTypeCTriangle01n, SSet.stdSimplex.triangle,","          SSet.stdSimplex.objMk_apply, Finset.mem_compl, Finset.mem_singleton]","        intro h","        have hv := congrArg Fin.val h","        norm_num [Nat.mod_eq_of_lt hlt] at hv","      · simpa [standardTypeCTriangle01n, SSet.stdSimplex.triangle,","          SSet.stdSimplex.objMk_apply] using hlast"]},{"at":244,"old":["        (2 : Fin (m + 4)) (0 : Fin (m + 4)) (by omega)) _ ht⟩"],"new":["        (2 : Fin (m + 4)) (0 : Fin (m + 4)) (by","          intro h","          have hv := congrArg Fin.val h","          have hlt : 2 < m + 4 := by omega","          norm_num [Nat.mod_eq_of_lt hlt] at hv)) _ ht⟩"]},{"at":248,"old":["    (standardTypeCSourceCarrier m).obj (op ⦋2⦌) :="],"new":["    (standardTypeCSourceCarrier.{u} m).obj (op ⦋2⦌) :="]},{"at":250,"old":["    (standardTypeCEdgeToHorn m)","    (standardTypeCEdgeCollapseToPoint m)).app (op ⦋2⦌)","      (standardTypeCTriangle01nInHorn m)"],"new":["    (standardTypeCEdgeToHorn.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)).app (op ⦋2⦌)","      (standardTypeCTriangle01nInHorn.{u} m)"]},{"at":257,"old":["    (standardTypeCTargetCarrier m).obj (op ⦋2⦌) :="],"new":["    (standardTypeCTargetCarrier.{u} m).obj (op ⦋2⦌) :="]},{"at":259,"old":["    (standardTypeCEdgeToSimplex m)","    (standardTypeCEdgeCollapseToPoint m)).app (op ⦋2⦌)","      (standardTypeCTriangle01n m)"],"new":["    (standardTypeCEdgeToSimplex.{u} m)","    (standardTypeCEdgeCollapseToPoint.{u} m)).app (op ⦋2⦌)","      (standardTypeCTriangle01n.{u} m)"]},{"at":266,"old":["    (standardTypeCCarrierMap m).app (op ⦋2⦌)","        (standardTypeCSourceDistinguishedTriangle m) =","      standardTypeCTargetDistinguishedTriangle m := by"],"new":["    (standardTypeCCarrierMap.{u} m).app (op ⦋2⦌)","        (standardTypeCSourceDistinguishedTriangle.{u} m) =","      standardTypeCTargetDistinguishedTriangle.{u} m := by"]},{"at":272,"old":["          standardTypeCTargetCarrier m =>","      k.app (op ⦋2⦌) (standardTypeCTriangle01nInHorn m))"],"new":["          standardTypeCTargetCarrier.{u} m =>","      k.app (op ⦋2⦌) (standardTypeCTriangle01nInHorn.{u} m))"]},{"at":282,"old":["def minimalPlusTriangleScaling"],"new":["@[reducible] def minimalPlusTriangleScaling"]},{"at":294,"old":["def standardTypeCSourceScaling (m : Nat) :","    ScaledSimplicialSet (standardTypeCSourceCarrier m) :=","  minimalPlusTriangleScaling (standardTypeCSourceDistinguishedTriangle m)"],"new":["@[reducible] def standardTypeCSourceScaling (m : Nat) :","    ScaledSimplicialSet (standardTypeCSourceCarrier.{u} m) :=","  minimalPlusTriangleScaling (standardTypeCSourceDistinguishedTriangle.{u} m)"]},{"at":299,"old":["def standardTypeCTargetScaling (m : Nat) :","    ScaledSimplicialSet (standardTypeCTargetCarrier m) :=","  minimalPlusTriangleScaling (standardTypeCTargetDistinguishedTriangle m)"],"new":["@[reducible] def standardTypeCTargetScaling (m : Nat) :","    ScaledSimplicialSet (standardTypeCTargetCarrier.{u} m) :=","  minimalPlusTriangleScaling (standardTypeCTargetDistinguishedTriangle.{u} m)"]},{"at":305,"old":["  ScaledSSet.of (standardTypeCSourceCarrier m) (standardTypeCSourceScaling m)"],"new":["  ScaledSSet.of (standardTypeCSourceCarrier.{u} m) (standardTypeCSourceScaling.{u} m)"]},{"at":309,"old":["  ScaledSSet.of (standardTypeCTargetCarrier m) (standardTypeCTargetScaling m)"],"new":["  ScaledSSet.of (standardTypeCTargetCarrier.{u} m) (standardTypeCTargetScaling.{u} m)"]},{"at":313,"old":["    standardTypeCSource m ⟶ standardTypeCTarget m where","  map := standardTypeCCarrierMap m"],"new":["    standardTypeCSource.{u} m ⟶ standardTypeCTarget.{u} m where","  map := standardTypeCCarrierMap.{u} m"]},{"at":320,"old":["          (standardTypeCTargetScaling m)","          (standardTypeCCarrierMap m)) t ht)"],"new":["          (minimalScaling (standardTypeCTargetCarrier.{u} m))","          (standardTypeCCarrierMap.{u} m)) t ht)"]},{"at":327,"old":["    (standardTypeCTargetScaling m).thin","      (standardTypeCTargetDistinguishedTriangle m) := by"],"new":["    (standardTypeCTargetScaling.{u} m).thin","      (standardTypeCTargetDistinguishedTriangle.{u} m) := by"]},{"at":333,"old":["    (standardTypeCSourceScaling m).thin","      (standardTypeCSourceDistinguishedTriangle m) := by"],"new":["    (standardTypeCSourceScaling.{u} m).thin","      (standardTypeCSourceDistinguishedTriangle.{u} m) := by"]},{"at":342,"old":["  MorphismProperty.ofHoms (fun m : Nat => standardTypeCGeneratorHom m)"],"new":["  MorphismProperty.ofHoms (fun m : Nat => standardTypeCGeneratorHom.{u} m)"]},{"at":348,"old":["      (standardTypeCGeneratorHom m) :="],"new":["      (standardTypeCGeneratorHom.{u} m) :="]},{"at":419,"old":["    standardScaledAnodyneGeneratorsABC (standardTypeCGeneratorHom m) :="],"new":["    standardScaledAnodyneGeneratorsABC (standardTypeCGeneratorHom.{u} m) :="]},{"at":457,"old":["    standardGeneratedScaledAnodyneABC (standardTypeCGeneratorHom m) :="],"new":["    standardGeneratedScaledAnodyneABC (standardTypeCGeneratorHom.{u} m) :="]},{"at":464,"old":["    standardGeneratedScaledAnodyneABC","      standardTypeBCollapse12CompletionHom := by","  change","    (standardScaledAnodyneGeneratorsABC :","      MorphismProperty (ScaledSSet.{u})).rlp.llp","      standardTypeBCollapse12CompletionHom"],"new":["    (standardGeneratedScaledAnodyneABC.{u} :","      MorphismProperty (ScaledSSet.{u}))","      (standardTypeBCollapse12CompletionHom.{u}) := by","  unfold standardGeneratedScaledAnodyneABC"]},{"at":478,"old":["    standardGeneratedScaledAnodyneABC","      standardTypeBCollapse23CompletionHom := by","  change","    (standardScaledAnodyneGeneratorsABC :","      MorphismProperty (ScaledSSet.{u})).rlp.llp","      standardTypeBCollapse23CompletionHom"],"new":["    (standardGeneratedScaledAnodyneABC.{u} :","      MorphismProperty (ScaledSSet.{u}))","      (standardTypeBCollapse23CompletionHom.{u}) := by","  unfold standardGeneratedScaledAnodyneABC"]}]
DEPENDENCIES = {
    DEP: DEP_BLOB,
    'formal/KUOS/DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.lean':
        'e560cd98ae0ca54d177347bc5b0043fe34a66fa7',
    'formal/KUOS/DependentOriginationNativeInfinityTwoScaledV1_19.lean':
        'd05efb10005d646752b8cca90f5fdcc11267c101',
}

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def inventory(s: str) -> list[str]:
    pat = (r'^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?'
           r'(?:def|theorem|lemma|structure|instance)\s+([^\s(:]+)')
    return re.findall(pat, s, re.M)

def candidates(baseline: str) -> dict[str, str]:
    assert blob(baseline.encode()) == BASE, 'historical baseline mismatch'
    assert inventory(baseline) == NAMES and len(NAMES) == 50
    assert len(HUNKS) == 57
    # Separate the evident universe/typing repairs, arithmetic proof terms,
    # and the full categorical proof. Every variant preserves the 50 names.
    substantive = {2, 3, 14, 17, 28, 30, 34, 35, 48, 55, 56}
    groups = {
        'universe-and-scaling': sorted(set(range(57)) - substantive),
        'finite-arithmetic-and-pushout': sorted(substantive),
        'complete-typec-reference': list(range(57)),
    }
    lines = baseline.split('\n')
    result = {}
    for name, indices in groups.items():
        selected = set(indices)
        out = []
        cursor = 0
        for index, patch in enumerate(HUNKS):
            at, old, newer = patch['at'], patch['old'], patch['new']
            assert at >= cursor and lines[at:at + len(old)] == old, (
                'misaligned version-bound patch', index)
            out.extend(lines[cursor:at])
            out.extend(newer if index in selected else old)
            cursor = at + len(old)
        out.extend(lines[cursor:])
        candidate = '\n'.join(out)
        assert inventory(candidate) == NAMES, ('declaration inventory changed', name)
        result[name] = candidate
    assert blob(result['complete-typec-reference'].encode()) == REFERENCE_BLOB
    return result

def pins(root: pathlib.Path) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
    assert require_pins(root)['mathlib_sha'] == '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
    assert blob((root / 'scripts/kuuos_lean_mcp_repair_loop_v1.py').read_bytes()) == CORE_BLOB
    for path, expected in DEPENDENCIES.items():
        assert blob((root / path).read_bytes()) == expected, ('dependency blob changed', path)
    assert blob((root / 'legacy/v5.291' / REL).read_bytes()) == BASE

def command(root: pathlib.Path, argv: list[str], logfile: pathlib.Path, timeout=600):
    p = subprocess.run(argv, cwd=root, text=True, capture_output=True, timeout=timeout)
    logfile.write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
    print(p.stdout, p.stderr, flush=True)
    return p

def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = command(root, ['lake', '-KleanArgs=-DwarningAsError=true',
        '-KleanArgs=-DsorryAsError=true', 'build', NS], out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'strict dependency build failed'

def verify_mcp(receipt: dict, source: bytes) -> None:
    assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
    sha = hashlib.sha256(source).hexdigest()
    assert receipt['candidate_sha256'] == sha == receipt['original_sha256']
    assert receipt['provider_calls'] == 0
    assert receipt['source_restored'] and not receipt['git_write_performed']
    assert not receipt['independent_ci_success']
    assert len(receipt['rounds']) == 1
    r = receipt['rounds'][0]
    assert r['semantic_success'] and not r['partial'] and r['errors'] == 0
    assert r['source_sha256'] == sha
    assert not any(d.get('severity') in {'warning', 'error'} for d in r['diagnostics'])
    assert r['direct_lean']['exit_code'] == 0 and r['forbidden_final_count'] == 0

def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import (
        run_loop, mcp_tactic_provider, mask_lean_comments, FORBIDDEN_NEW)
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert blob(original) == os.environ['CHECKOUT_BLOB']
    assert blob(original) in {BASE, REFERENCE_BLOB}
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    rows = []
    manifest = None
    try:
        for name, source in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)), ('forbidden code', name)
            target.write_text(source, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v158-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
                    '-Dweak.sorryAsError=true', '-o', str(olean), REL],
                    out / (name + '.log'))
                log = p.stdout + '\n' + p.stderr
                errors = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {'candidate': name, 'blob': blob(source.encode()),
                    'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                    'head': os.environ['SOURCE_HEAD'], 'dependencies': DEPENDENCIES,
                    'lean': 'leanprover/lean4:v4.30.0-rc2',
                    'mathlib': '5450b53e5ddc75d46418fabb605edbf36bd0beb6',
                    'exit_code': p.returncode, 'errors': errors,
                    'success': p.returncode == 0 and olean.is_file()
                        and not errors and 'sorryAx' not in log}
                rows.append(row)
                (out / 'candidates.json').write_text(
                    json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
                print('KUUOS_V158_DIRECT ' + json.dumps(row, ensure_ascii=False), flush=True)
        assert not rows[0]['success'] and rows[0]['exit_code'] != 0
        selected = next((row for row in rows if row['candidate'] ==
            'complete-typec-reference' and row['success']), None)
        assert selected is not None, 'no complete directly verified candidate'
        source = variants[selected['candidate']].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'live-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(),
            provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'public-root-test.py').write_bytes(
            (root / 'tests/test_public_root_restoration.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / WORKFLOW).read_bytes())
        (out / 'candidate-script.py').write_bytes(
            (root / 'scripts/ci_kuuos_v158_codeai.py').read_bytes())
        manifest = {'head': os.environ['SOURCE_HEAD'],
            'checkout_blob': blob(original), 'selected': selected,
            'source_sha256': hashlib.sha256(source).hexdigest(),
            'dependencies': DEPENDENCIES, 'baseline_blob': BASE,
            'source_restored': False, 'git_write_performed': False,
            'independent_ci_success': False}
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    assert manifest is not None
    manifest['source_restored'] = True
    (out / 'manifest.json').write_text(
        json.dumps(manifest, indent=2), encoding='utf-8')
    print('KUUOS_V158_DIRECT_AND_REAL_MCP_SUCCESS '+json.dumps(manifest), flush=True)

def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    pins(root)
    m = json.loads((out / 'manifest.json').read_text())
    receipt = json.loads((out / 'mcp.json').read_text())
    source = (out / 'source.lean').read_bytes()
    target = root / REL
    original = target.read_bytes()
    variants = candidates((root / 'legacy/v5.291' / REL).read_text(encoding='utf-8'))
    selected = m['selected']
    assert m['head'] == os.environ['SOURCE_HEAD']
    assert blob(original) == m['checkout_blob'] == os.environ['CHECKOUT_BLOB']
    assert m['dependencies'] == DEPENDENCIES and m['baseline_blob'] == BASE
    assert selected['candidate'] == 'complete-typec-reference'
    assert source == variants[selected['candidate']].encode()
    assert blob(source) == selected['blob'] == REFERENCE_BLOB
    assert hashlib.sha256(source).hexdigest() == m['source_sha256']
    assert selected['success'] and selected['exit_code'] == 0 and not selected['errors']
    assert m['source_restored'] and not m['git_write_performed'] and not m['independent_ci_success']
    for outname, repo_path in [
        ('candidate-script.py', 'scripts/ci_kuuos_v158_codeai.py'),
        ('workflow.yml', WORKFLOW),
        ('public-root-test.py', 'tests/test_public_root_restoration.py')]:
        assert (out / outname).read_bytes() == (root / repo_path).read_bytes()
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV158IndependentAudit.lean'
    assert not audit.exists()
    try:
        target.write_bytes(source)
        strict_build(root, out)
        audit.write_text('import ' + NS + '\n' +
            '\n'.join('#print axioms ' + NS + '.' + n for n in NAMES) + '\n',
            encoding='utf-8')
        p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
            '-Dweak.sorryAsError=true', str(audit)], out / 'axioms.log')
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", log, re.S)
        assert len(rows) == len(NAMES) == 50, (len(rows), len(NAMES))
        assert {n for n, _ in rows} == {NS + '.' + n for n in NAMES}
        for _, axioms in rows:
            assert {x.strip() for x in axioms.split(',') if x.strip()} <= {
                'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V158_INDEPENDENT_50_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
    finally:
        target.write_bytes(original)
        audit.unlink(missing_ok=True)
    assert target.read_bytes() == original

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['direct', 'independent', 'plan'])
    ap.add_argument('directory', type=pathlib.Path)
    args = ap.parse_args()
    if args.mode == 'plan':
        print(json.dumps({name: blob(source.encode()) for name, source in
            candidates(args.directory.read_text()).items()}, indent=2))
        return
    root = pathlib.Path('.').resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == 'direct' else independent)(root, out)

if __name__ == '__main__':
    main()
