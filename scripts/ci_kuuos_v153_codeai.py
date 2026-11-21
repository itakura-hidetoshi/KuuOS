#!/usr/bin/env python3
"""Exact-source v1.53 candidate experiments; no Git, API, or branch writes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile

NS = 'KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = 'df00e11c5c1b0addb21cfc9023fea9a445a3b3c1'
DEP = 'formal/KUOS/DependentOriginationScaledCartesianIntervalCylinderV1_52.lean'
DEP_BLOB = 'e12da806d1e8da9758c51b1c2139245b7f8e47b9'
NAMES = [
    'ScalingLE', 'ScalingLE.refl', 'ScalingLE.trans', 'scaling_eq_of_le_antisymm',
    'standardTypeAEndpointCylinderProductScaling',
    'standardTypeAEndpointInducedProductPullbackScaling',
    'standardTypeAEndpointPushoutProductSource_scaling_eq_inducedProductPullback',
    'standardTypeAEndpointSimplexEndpointLegScaling',
    'standardTypeAEndpointHornIntervalLegScaling',
    'standardTypeAEndpointGeneratedPushoutScaling',
    'standardTypeAEndpointGeneratedPushout_inl_scaled',
    'standardTypeAEndpointGeneratedPushout_inr_scaled',
    'standardTypeAEndpointGeneratedPushoutScaling_le_of_legs_scaled',
    'standardTypeAEndpointLegs_scaled_to_inducedProductPullback',
    'standardTypeAEndpointGeneratedPushoutScaling_le_induced',
    'standardTypeAEndpointGeneratedPushoutSource',
    'standardTypeAEndpointGeneratedToInduced',
    'standardTypeAEndpointGeneratedToInduced_map',
    'standardTypeAEndpointGeneratedPushoutProductHom',
    'standardTypeAEndpointGeneratedPushoutProductHom_map',
    'standardTypeAEndpointGeneratedPushoutProduct_factorization',
    'standardTypeAEndpointSourceEnrichments',
    'standardTypeAEndpointSourceEnrichment_mem',
]
CLASS_DEFS = [NAMES[i] for i in (4, 5, 7, 8, 9)]
LEG_DEFS = [NAMES[i] for i in (7, 8)]
OLD_EQ = '''    (standardTypeAEndpointPushoutProductSource g).scaling =
      standardTypeAEndpointInducedProductPullbackScaling g := by'''
NEW_EQ = '''    (standardTypeAEndpointPushoutProductSource.{u} g).scaling =
      standardTypeAEndpointInducedProductPullbackScaling.{u} g := by'''
OLD_MAP = '''  simp [standardTypeAEndpointGeneratedPushoutProductHom,
    standardTypeAEndpointGeneratedToInduced,
    standardTypeAEndpointPushoutProductHom]'''
NEW_MAP = '''  change (𝟙 ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint g.endpoint) : SSet.{u})) ≫
      ((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint)).ι =
    ((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint)).ι
  exact Category.id_comp _'''
EXPECTED = {
    'reducible': '2063b36e1f2dc77de5ff357a79e827031ce98c30',
    'noncomputable-legs': 'faae3e971bade507ad5a16f95ca0f4ff88b7fbf3',
    'universe-bound': '4dc66325b61b9634d35c58aa980d3fb1b2a21cfb',
    'typed-identity': '0fb96395844b6d993962020f7f7a1a79b9f97b85',
    'inferred-identity': 'e1101bc30b4e30a00a43a0ca6125cb1165c79227',
    'exact-identity': '056ae90a88d016efc5fcc5d7a6f64933197de6c5',
}


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def code_only(text: str) -> str:
    # Lean comments nest. Documentation containing the word 'axiom' is not code.
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith('/-', i):
            depth += 1; i += 2
        elif depth and text.startswith('-/', i):
            depth -= 1; i += 2
        elif not depth and text.startswith('--', i):
            i = text.find('\n', i)
            if i < 0:
                break
        else:
            if not depth or text[i] == '\n':
                out.append(text[i])
            i += 1
    assert depth == 0, 'unclosed Lean comment'
    return ''.join(out)


def replace_one(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, ('ambiguous patch', old)
    return text.replace(old, new, 1)


def candidates(baseline: str) -> dict[str, str]:
    assert blob(baseline.encode()) == BASE
    red = baseline
    for name in CLASS_DEFS:
        red = replace_one(red, 'def ' + name + '\n', '@[reducible] def ' + name + '\n')
    nc = red
    for name in LEG_DEFS:
        nc = replace_one(nc, '@[reducible] def ' + name + '\n',
                         '@[reducible] noncomputable def ' + name + '\n')
    uni = replace_one(nc, OLD_EQ, NEW_EQ)
    full = replace_one(uni, OLD_MAP, NEW_MAP)
    inferred = replace_one(uni, OLD_MAP, NEW_MAP.replace('SSet.{u}', 'SSet'))
    exact_identity = replace_one(uni, OLD_MAP, '  exact Category.id_comp _')
    result = {'reducible': red, 'noncomputable-legs': nc,
              'universe-bound': uni, 'typed-identity': full,
              'inferred-identity': inferred, 'exact-identity': exact_identity}
    pattern = r'^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?(?:def|theorem|lemma|structure|abbrev|instance)\s+([^\s(:]+)'
    original_inventory = re.findall(pattern, code_only(baseline), re.M)
    assert original_inventory == NAMES
    for name, text in result.items():
        code = code_only(text)
        assert re.findall(pattern, code, re.M) == original_inventory
        assert not re.search(r'\b(?:sorry|admit|axiom|unsafe|native_decide)\b|debug\.skipKernelTC', code)
        assert text.count('import ') == baseline.count('import ')
        if EXPECTED:
            assert blob(text.encode()) == EXPECTED[name]
    return result


def pins(root: pathlib.Path) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
    assert require_pins(root)['mathlib_sha'] == '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
    assert blob((root / DEP).read_bytes()) == DEP_BLOB


def run_command(root: pathlib.Path, args: list[str], logpath: pathlib.Path,
                timeout: int = 600) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(args, cwd=root, text=True, capture_output=True, timeout=timeout)
    logpath.write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
    print(p.stdout, p.stderr, flush=True)
    return p


def build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = run_command(root, ['lake', '-KleanArgs=-DwarningAsError=true',
                          '-KleanArgs=-DsorryAsError=true', 'build', NS],
                    out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'strict Lean build failed'


def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import digest, run_loop, mcp_tactic_provider
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert blob(original) == os.environ['CHECKOUT_BLOB']
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    rows = []
    try:
        for name, text in [('baseline', baseline), *variants.items()]:
            target.write_text(text, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v153-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = run_command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
                    '-Dweak.sorryAsError=true', '-o', str(olean), REL], out / (name + '.log'))
                log = p.stdout + '\n' + p.stderr
                errors = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {'candidate': name, 'blob': blob(text.encode()),
                    'sha256': digest(text), 'exit_code': p.returncode, 'errors': errors,
                    'success': p.returncode == 0 and olean.is_file() and not errors and 'sorryAx' not in log}
                rows.append(row)
                print('KUUOS_V153_DIRECT ' + json.dumps(row, ensure_ascii=False), flush=True)
        (out / 'candidates.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
        assert not rows[0]['success'] and 'must be marked with' in (out / 'baseline.log').read_text()
        selected = next((r for r in rows[1:] if r['success']), None)
        assert selected is not None, 'no directly verified candidate'
        source = variants[selected['candidate']].encode()
        target.write_bytes(source)
        build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'live-mcp',
            expected_sha256=digest(source), provider=mcp_tactic_provider, max_iterations=1)
        assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
        assert receipt['candidate_sha256'] == digest(source)
        assert receipt['source_restored'] and not receipt['git_write_performed'] and not receipt['independent_ci_success']
        assert receipt['rounds'][0]['semantic_success'] and not receipt['rounds'][0]['errors']
        assert receipt['rounds'][0]['direct_lean']['exit_code'] == 0
        (out / 'source.lean').write_bytes(source)
        (out / 'public-root-test.py').write_bytes((root / 'tests/test_public_root_restoration.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / '.github/workflows/kuuos-v153-codeai-source-enrichment-real-mcp-v1.yml').read_bytes())
        (out / 'mcp.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        manifest = {'head': os.environ['SOURCE_HEAD'], 'checkout_blob': blob(original),
            'selected': selected, 'source_sha256': digest(source), 'source_restored': True,
            'git_write_performed': False, 'independent_ci_success': False}
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
        print('KUUOS_V153_DIRECT_AND_REAL_MCP_SUCCESS ' + json.dumps(manifest), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original


def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    pins(root)
    m = json.loads((out / 'manifest.json').read_text())
    receipt = json.loads((out / 'mcp.json').read_text())
    source = (out / 'source.lean').read_bytes()
    target = root / REL
    original = target.read_bytes()
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    selected = m['selected']
    assert m['head'] == os.environ['SOURCE_HEAD']
    assert blob(original) == m['checkout_blob'] == os.environ['CHECKOUT_BLOB']
    assert source == variants[selected['candidate']].encode()
    assert blob(source) == selected['blob'] == EXPECTED[selected['candidate']]
    assert hashlib.sha256(source).hexdigest() == m['source_sha256'] == receipt['candidate_sha256']
    assert selected['success'] and selected['exit_code'] == 0 and not selected['errors']
    assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
    assert receipt['source_restored'] and not receipt['git_write_performed'] and not receipt['independent_ci_success']
    assert receipt['rounds'][0]['semantic_success'] and not receipt['rounds'][0]['errors']
    assert receipt['rounds'][0]['direct_lean']['exit_code'] == 0
    try:
        target.write_bytes(source)
        build(root, out)
        audit = root / 'formal/KUOS/DependentOriginationV153IndependentAudit.lean'
        audit.write_text('import ' + NS + '\n' + '\n'.join('#print axioms ' + NS + '.' + n for n in NAMES) + '\n')
        p = run_command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
            '-Dweak.sorryAsError=true', str(audit)], out / 'axioms.log')
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", log, re.S)
        assert len(rows) == len(NAMES) == 23
        assert {n for n, _ in rows} == {NS + '.' + n for n in NAMES}
        for _, axioms in rows:
            assert {x.strip() for x in axioms.split(',') if x.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V153_INDEPENDENT_23_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
    finally:
        target.write_bytes(original)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['direct', 'independent', 'plan'])
    ap.add_argument('directory', type=pathlib.Path)
    args = ap.parse_args()
    if args.mode == 'plan':
        variants = candidates(args.directory.read_text())
        print(json.dumps({n: blob(s.encode()) for n, s in variants.items()}, indent=2))
        return
    out = args.directory.resolve()
    out.mkdir(parents=True, exist_ok=True)
    root = pathlib.Path('.').resolve()
    assert not out.is_relative_to(root)
    (direct if args.mode == 'direct' else independent)(root, out)


if __name__ == '__main__':
    main()
