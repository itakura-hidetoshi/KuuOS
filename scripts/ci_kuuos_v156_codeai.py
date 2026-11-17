#!/usr/bin/env python3
"""CodeAI exact-version experiments for v1.56 Type-B scaled pushout.
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

NS = 'KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = 'f5b4c1c505e86fbb4986f3ef1b89f5fb2fb07876'
REFERENCE_BLOB = 'eb3f6d6105989fe07f7bba70e8c7fc7c84b5e67a'
DEP = 'formal/KUOS/DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55.lean'
DEP_BLOB = 'be2fb30122c82a086304845cedc9a0964b524148'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v156-codeai-typeb-scaling-real-mcp-v1.yml'
NAMES = ["scalingEnrichmentPushoutScaling","scalingEnrichmentHom","scalingEnrichmentPushoutLowerMap","scalingEnrichmentPushoutUpperMap","scalingEnrichmentPushoutTargetEnrichment","scalingEnrichmentPushout_commutes","scalingEnrichmentPushout_compatibility_map","scalingEnrichmentPushoutDesc","scalingEnrichmentPushout_target_desc","scalingEnrichmentPushout_upper_desc","scalingEnrichmentPushout_hom_ext","scalingEnrichmentPushout_isPushout","scalingEnrichmentPushoutTarget_hasLiftingProperty","scalingEnrichmentPushoutTarget_mem_llp","IsStandardVertexTriangle","IsStandardTypeBSourceTriangle","standardTypeBSourceScaling","standardTypeBTargetScaling","standardTypeBSourceScaling_le_target","standardTypeBSource","standardTypeBTarget","standardTypeBGeneratorHom","standardTypeBGeneratorHom_map","standardTypeBScaledAnodyneGenerators","standardTypeBGenerator_mem","standardTypeB_triangle_014_thin","standardTypeB_triangle_034_thin","standardTypeBPushoutScaling","standardTypeBPushoutEnrichment","standardTypeBPushout_isPushout","standardTypeBPushoutEnrichment_mem_llp","standardTypeBPushoutEnrichment_mem_externalGenerated"]
# Nine byte-specific, source-position-sensitive, invertible edits from the
# historical file to a research reference. A reference is a CANDIDATE, not proof.
EDITS = [["open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41","open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\nopen KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"],["scaling `sX'`. -/\ndef scalingEnrichmentPushoutScaling\n    {X Y : SSet.{u}}","scaling `sX'`. -/\n@[reducible] def scalingEnrichmentPushoutScaling\n    {X Y : SSet.{u}}"],["  apply ScaledSSet.ScaledMap.ext\n  simp [scalingEnrichmentPushoutLowerMap,\n    scalingEnrichmentPushoutTargetEnrichment,\n    scalingEnrichmentHom, scalingEnrichmentPushoutUpperMap]\n","  apply ScaledSSet.ScaledMap.ext\n  change f ≫ 𝟙 Y = 𝟙 X ≫ f\n  simp\n"],["        (congr_app hmap (op ⦋2⦌)) x\n      change W.scaling.thin (b.map.app (op ⦋2⦌) (f.app (op ⦋2⦌) x))\n      rw [← hpoint]\n      exact a.scaled x hx","        (congr_app hmap (op ⦋2⦌)) x\n      change W.scaling.thin ((f ≫ b.map).app (op ⦋2⦌) x)\n      rw [hpoint]\n      exact a.scaled x hx"],["  apply ScaledSSet.ScaledMap.ext\n  simp [scalingEnrichmentPushoutTargetEnrichment,\n    scalingEnrichmentPushoutDesc]\n","  apply ScaledSSet.ScaledMap.ext\n  change 𝟙 Y ≫ b.map = b.map\n  simp\n"],["  }\n  apply PushoutCocone.IsColimit.mk _\n  · intro s\n    exact scalingEnrichmentPushoutDesc\n      hXX' sY f hf s.inl s.inr s.condition\n  · intro s\n    exact scalingEnrichmentPushout_target_desc\n      hXX' sY f hf s.inl s.inr s.condition\n  · intro s\n    exact scalingEnrichmentPushout_upper_desc\n      hXX' sY f hf s.inl s.inr s.condition\n  · intro s m hm₁ hm₂\n    apply scalingEnrichmentPushout_hom_ext sX' sY f\n    rw [hm₁, scalingEnrichmentPushout_target_desc]\n","  }\n  exact PushoutCocone.IsColimit.mk\n    (scalingEnrichmentPushout_commutes hXX' sY f hf)\n    (fun s => scalingEnrichmentPushoutDesc\n      hXX' sY f hf s.inl s.inr s.condition)\n    (fun s => scalingEnrichmentPushout_target_desc\n      hXX' sY f hf s.inl s.inr s.condition)\n    (fun s => scalingEnrichmentPushout_upper_desc\n      hXX' sY f hf s.inl s.inr s.condition)\n    (by\n      intro s m hm₁ hm₂\n      apply scalingEnrichmentPushout_hom_ext sX' sY f\n      exact hm₁.trans\n        (scalingEnrichmentPushout_target_desc\n          hXX' sY f hf s.inl s.inr s.condition).symm)\n"],["/-- Source scaling `T` of the standard type-(B) generator. -/\ndef standardTypeBSourceScaling :\n    ScaledSimplicialSet (Δ[4] : SSet.{u}) where","/-- Source scaling `T` of the standard type-(B) generator. -/\n@[reducible] def standardTypeBSourceScaling :\n    ScaledSimplicialSet (Δ[4] : SSet.{u}) where"],["source scaling, the triangles `014` and `034` are thin. -/\ndef standardTypeBTargetScaling :\n    ScaledSimplicialSet (Δ[4] : SSet.{u}) where","source scaling, the triangles `014` and `034` are thin. -/\n@[reducible] def standardTypeBTargetScaling :\n    ScaledSimplicialSet (Δ[4] : SSet.{u}) where"],["type-(B) generator along a scaled map from its source. -/\ndef standardTypeBPushoutScaling\n    {Y : SSet.{u}}","type-(B) generator along a scaled map from its source. -/\n@[reducible] def standardTypeBPushoutScaling\n    {Y : SSet.{u}}"]]
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
    # First isolate namespace and four class-valued scaling reductions.
    groups = {
        'namespace-and-classes': [0, 1, 6, 7, 8],
        'underlying-equalities': [0, 1, 2, 3, 4, 6, 7, 8],
        'complete-categorical-reference': list(range(len(EDITS))),
    }
    out = {}
    for name, indices in groups.items():
        result = baseline
        for index in indices:
            old, new = EDITS[index]
            assert result.count(old) == 1, (name, index, 'nonunique patch')
            result = result.replace(old, new, 1)
        assert inventory(result) == NAMES, ('declaration interface changed', name)
        out[name] = result
    assert blob(out['complete-categorical-reference'].encode()) == REFERENCE_BLOB
    assert inventory(baseline) == NAMES and len(NAMES) == 32
    assert len(EDITS) == 9
    return out

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
            with tempfile.TemporaryDirectory(prefix='kuuos-v156-') as tmp:
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
                print('KUUOS_V156_DIRECT ' + json.dumps(row, ensure_ascii=False), flush=True)
        assert not rows[0]['success'] and rows[0]['exit_code'] != 0
        selected = next((row for row in rows if row['candidate'] ==
            'complete-categorical-reference' and row['success']), None)
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
            (root / 'scripts/ci_kuuos_v156_codeai.py').read_bytes())
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
    print('KUUOS_V156_DIRECT_AND_REAL_MCP_SUCCESS '+json.dumps(manifest), flush=True)

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
    assert selected['candidate'] == 'complete-categorical-reference'
    assert source == variants[selected['candidate']].encode()
    assert blob(source) == selected['blob'] == REFERENCE_BLOB
    assert hashlib.sha256(source).hexdigest() == m['source_sha256']
    assert selected['success'] and selected['exit_code'] == 0 and not selected['errors']
    assert m['source_restored'] and not m['git_write_performed'] and not m['independent_ci_success']
    for outname, repo_path in [
        ('candidate-script.py', 'scripts/ci_kuuos_v156_codeai.py'),
        ('workflow.yml', WORKFLOW),
        ('public-root-test.py', 'tests/test_public_root_restoration.py')]:
        assert (out / outname).read_bytes() == (root / repo_path).read_bytes()
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV156IndependentAudit.lean'
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
        assert len(rows) == len(NAMES) == 32, (len(rows), len(NAMES))
        assert {n for n, _ in rows} == {NS + '.' + n for n in NAMES}
        for _, axioms in rows:
            assert {x.strip() for x in axioms.split(',') if x.strip()} <= {
                'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V156_INDEPENDENT_32_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
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
