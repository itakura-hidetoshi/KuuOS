#!/usr/bin/env python3
"""v1.62 CodeAI: version-bound causal alternatives, direct Lean, real MCP, independent kernel audit.
Candidate source is patched only in a disposable GitHub Actions checkout, NEVER submitted as proof.
No statement, hypothesis, certified source, or frozen legacy byte may be weakened.
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

NS = 'KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = 'c3ad3eff708d86a5a5e944c5745c821b6dbf8ec4'
CANDIDATE = '09c295b65d56730d1ebe8d40898b8cf7e53cf6ee'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v162-codeai-boundary-prism-scaled-cells-real-mcp-v1.yml'
DEPENDENCIES = {
    'formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61.lean': '932d03cd7d4c33a5ffcc5cce03467c6a3a7bf3a3',
    'formal/KUOS/DependentOriginationStandardTypeAEndpointPrismPairingV1_60.lean': '3a039fc3eba760d2fb4bfbe62d8fac5ab3fa87b6',
    'formal/KUOS/DependentOriginationStandardTypeBThreeSimplexCompletionV1_57.lean': '735fc7afffc7806bf6eac41c6c8fdc60a6cea95a',
    'formal/KUOS/DependentOriginationScaledAnodyneAttachmentFactorizationV1_48.lean': '90f67bf0aefb6ecfe2dec7adfc8876ec2b39a31a',
}
NAMES = ["standardTypeABoundaryPrismCellScaling","standardTypeABoundaryPrismCellHornScaling","standardTypeABoundaryPrismScaledCellSource","standardTypeABoundaryPrismScaledCellTarget","standardTypeABoundaryPrismScaledCellHom","standardTypeABoundaryPrismScaledCellHom_map","standardTypeABoundaryPrismScaledCellToCylinder","standardTypeABoundaryPrism_cell_target_dim_ge_two","standardTypeABoundaryPrism_cell_no_outer_index","standardTypeABoundaryPrism_cell_horn_obj_two_eq_univ_of_four_le","standardTypeABoundaryPrism_cell_triangle_mem_horn_of_four_le","standardTypeABoundaryPrism_cell_target_dim_le_three_of_triangle_notMem_horn","standardTypeABoundaryPrism_cell_target_dim_eq_two_or_three_of_triangle_notMem_horn","standardTypeABoundaryPrism_cell_index_val_eq_one_of_target_dim_two","standardTypeABoundaryPrism_cell_index_val_eq_one_or_two_of_target_dim_three","standardTypeABoundaryPrismCellIndex3","standardTypeABoundaryPrismCellIndex3_eq_one_or_two","standardTypeABoundaryPrismCellMissingFace3","standardTypeABoundaryPrismCellMissingFace3_eq_023_of_index_one","standardTypeABoundaryPrismCellMissingFace3_eq_013_of_index_two","standardTypeABoundaryPrismCellMissingFace3_eq_typeB_frontier","standardTypeABoundaryPrismCellMissingFace3_typeB_completed_thin","standardTypeABoundaryPrism_cell_scaled_frontier"]
AUDIT_NAMES = NAMES.copy()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def inventory(source: str) -> list[str]:
    pat = (r'^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?'
           r'(?:def|theorem|lemma|structure|instance|abbrev)\s+([^\s(:]+)')
    return re.findall(pat, source, re.M)


def replacement(source: str, old: str, new: str, count: int = 1) -> str:
    assert source.count(old) == count, ('version-bound replace mismatch', old, count, source.count(old))
    return source.replace(old, new)


def candidates(baseline: str) -> dict[str, str]:
    assert blob(baseline.encode()) == BASE
    assert inventory(baseline) == NAMES and len(NAMES) == 23

    def fix_scope(s: str) -> str:
        return replacement(s,
            'open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40\n',
            'open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40\n'
            'open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48\n')

    def fix_reducible(s: str) -> str:
        s = replacement(s, 'def standardTypeABoundaryPrismCellScaling',
            '@[reducible] def standardTypeABoundaryPrismCellScaling')
        return replacement(s, 'def standardTypeABoundaryPrismCellHornScaling',
            '@[reducible] def standardTypeABoundaryPrismCellHornScaling')

    def fix_noncomputable(s: str) -> str:
        for name in (
            'standardTypeABoundaryPrismScaledCellSource',
            'standardTypeABoundaryPrismScaledCellTarget',
            'standardTypeABoundaryPrismScaledCellHom',
            'standardTypeABoundaryPrismScaledCellToCylinder',
        ):
            s = replacement(s, 'def ' + name, 'noncomputable def ' + name)
        return s

    variants = {
        'scope-only': fix_scope(baseline),
        'reducible-only': fix_reducible(baseline),
        'noncomputable-only': fix_noncomputable(baseline),
        'complete-v162': fix_noncomputable(fix_reducible(fix_scope(baseline))),
    }
    for name, source in variants.items():
        assert inventory(source) == NAMES, ('declaration inventory modified', name)
    assert blob(variants['complete-v162'].encode()) == CANDIDATE
    return variants


def pins(root: pathlib.Path) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
    assert require_pins(root)['mathlib_sha'] == '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
    assert blob((root / 'scripts/kuuos_lean_mcp_repair_loop_v1.py').read_bytes()) == CORE_BLOB
    for path, sha in DEPENDENCIES.items():
        assert blob((root / path).read_bytes()) == sha, ('changed dependency', path)
    assert blob((root / 'legacy/v5.291' / REL).read_bytes()) == BASE


def command(root: pathlib.Path, args: list[str], out: pathlib.Path, timeout: int = 600):
    p = subprocess.run(args, cwd=root, text=True, capture_output=True, timeout=timeout)
    out.write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
    print(p.stdout, p.stderr, flush=True)
    return p


def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = command(root,
        ['lake', '-KleanArgs=-DwarningAsError=true', '-KleanArgs=-DsorryAsError=true',
         'build', NS], out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'candidate dependency build failed'


def verify_mcp(receipt: dict, source: bytes) -> None:
    assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
    sha = hashlib.sha256(source).hexdigest()
    assert receipt['candidate_sha256'] == receipt['original_sha256'] == sha
    assert receipt['provider_calls'] == 0
    assert receipt['source_restored'] and not receipt['git_write_performed']
    assert not receipt['independent_ci_success'] and len(receipt['rounds']) == 1
    row = receipt['rounds'][0]
    assert row['semantic_success'] and not row['partial'] and row['errors'] == 0
    assert row['source_sha256'] == sha
    assert not any(d.get('severity') in {'warning', 'error'} for d in row['diagnostics'])
    assert row['direct_lean']['exit_code'] == 0 and row['forbidden_final_count'] == 0


def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import (
        run_loop, mcp_tactic_provider, mask_lean_comments, FORBIDDEN_NEW)
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert blob(original) == os.environ['CHECKOUT_BLOB']
    assert blob(original) in {BASE, CANDIDATE}
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    assert original == (variants['complete-v162'].encode() if blob(original) == CANDIDATE else baseline.encode())
    rows = []
    manifest = None
    try:
        for name, source in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)), ('forbidden code', name)
            target.write_text(source, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v162-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
                    '-Dweak.sorryAsError=true', '-o', str(olean), REL],
                    out / (name + '.log'), 900)
                log = p.stdout + '\n' + p.stderr
                errs = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {'candidate': name, 'blob': blob(source.encode()),
                    'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                    'head': os.environ['SOURCE_HEAD'], 'dependencies': DEPENDENCIES,
                    'lean': 'leanprover/lean4:v4.30.0-rc2',
                    'mathlib': '5450b53e5ddc75d46418fabb605edbf36bd0beb6',
                    'exit_code': p.returncode, 'errors': errs,
                    'success': p.returncode == 0 and olean.is_file()
                        and not errs and 'sorryAx' not in log}
                rows.append(row)
                (out / 'candidates.json').write_text(json.dumps(rows, indent=2),
                    encoding='utf-8')
                print('KUUOS_V162_DIRECT ' + json.dumps(row), flush=True)
        assert not rows[0]['success'] and rows[0]['exit_code'] != 0
        selected = next((r for r in rows if r['candidate'] == 'complete-v162'
            and r['success']), None)
        assert selected is not None, 'complete v1.59 candidate not yet Lean certified'
        source = variants['complete-v162'].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'real-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(),
            provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'candidate-script.py').write_bytes((root / 'scripts/ci_kuuos_v162_codeai.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / WORKFLOW).read_bytes())
        manifest = {'head': os.environ['SOURCE_HEAD'], 'checkout_blob': blob(original),
            'selected': selected, 'source_sha256': hashlib.sha256(source).hexdigest(),
            'dependencies': DEPENDENCIES, 'baseline_blob': BASE,
            'source_restored': False, 'git_write_performed': False,
            'independent_ci_success': False}
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    assert manifest is not None
    manifest['source_restored'] = True
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('KUUOS_V162_DIRECT_AND_REAL_MCP_SUCCESS '+json.dumps(manifest), flush=True)


def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments, FORBIDDEN_NEW
    pins(root)
    manifest = json.loads((out / 'manifest.json').read_text())
    receipt = json.loads((out / 'mcp.json').read_text())
    source = (out / 'source.lean').read_bytes()
    variants = candidates((root / 'legacy/v5.291' / REL).read_text(encoding='utf-8'))
    target = root / REL
    original = target.read_bytes()
    assert manifest['head'] == os.environ['SOURCE_HEAD']
    assert blob(original) == manifest['checkout_blob'] == os.environ['CHECKOUT_BLOB']
    assert blob(original) in {BASE, CANDIDATE}
    assert original == (variants['complete-v162'].encode() if blob(original) == CANDIDATE else (root / 'legacy/v5.291' / REL).read_bytes())
    assert manifest['dependencies'] == DEPENDENCIES and manifest['baseline_blob'] == BASE
    assert manifest['selected']['candidate'] == 'complete-v162'
    assert source == variants['complete-v162'].encode()
    assert blob(source) == manifest['selected']['blob'] == CANDIDATE
    assert hashlib.sha256(source).hexdigest() == manifest['source_sha256']
    assert manifest['selected']['success'] and manifest['selected']['exit_code'] == 0
    assert not manifest['selected']['errors']
    assert manifest['source_restored'] and not manifest['git_write_performed']
    assert not manifest['independent_ci_success']
    for output, repo_path in [
        ('candidate-script.py', 'scripts/ci_kuuos_v162_codeai.py'),
        ('workflow.yml', WORKFLOW)]:
        assert (out / output).read_bytes() == (root / repo_path).read_bytes()
    assert not FORBIDDEN_NEW.findall(mask_lean_comments(source.decode()))
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV162IndependentAudit.lean'
    assert not audit.exists()
    try:
        target.write_bytes(source)
        strict_build(root, out)
        audit.write_text('import ' + NS + '\n' +
            '\n'.join('#print axioms ' + NS + '.' + name for name in AUDIT_NAMES) + '\n',
            encoding='utf-8')
        p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
            '-Dweak.sorryAsError=true', str(audit)], out / 'axioms.log', 900)
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(
            r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
            log, re.S)
        assert len(rows) == len(AUDIT_NAMES) == 23, (len(rows), len(AUDIT_NAMES))
        assert {name for name, _ in rows} == {NS + '.' + name for name in AUDIT_NAMES}
        for _, axioms in rows:
            assert {v.strip() for v in axioms.split(',') if v.strip()} <= {
                'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V162_INDEPENDENT_23_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
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
        print(json.dumps({name: blob(s.encode()) for name, s in
            candidates(args.directory.read_text()).items()}, indent=2))
        return
    root = pathlib.Path('.').resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == 'direct' else independent)(root, out)


if __name__ == '__main__':
    main()
