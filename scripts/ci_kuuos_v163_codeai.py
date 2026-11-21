#!/usr/bin/env python3
"""v1.63 CodeAI: version-bound causal alternatives, direct Lean, real MCP, independent kernel audit.
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

NS = 'KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = 'cdf63af6d96baa33bb0fe9db97936bfdfccfaef5'
CANDIDATE = 'e9e164f1e71c726de1b5fb7a33a2eb57f98fb6b9'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v163-codeai-prism-dimension-dichotomy-real-mcp-v1.yml'
DEPENDENCIES = {
    'formal/KUOS/DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62.lean': 'f90bbb80115cea04267c4a76b995a512d7239aa9',
    'formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61.lean': '932d03cd7d4c33a5ffcc5cce03467c6a3a7bf3a3',
    'formal/KUOS/PinnedMathlibUnionProdProofPortV1_61.lean': 'ba703c0dd48e4e437cb968e077611fb50e5a154e',
}
NAMES = ["unionProdPairingCore_typeOne_fst_surjective","unionProdPairingCore_typeTwo_target_dim_ge_left","unionProdPairing_typeTwo_target_dim_ge_left","standardTypeAHornAttachmentGenerator_dim_ge_two","standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim","standardTypeABoundaryPrism_cell_target_dim_le_generator_succ","standardTypeABoundaryPrism_cell_target_dim_eq_generator_or_succ","standardTypeABoundaryPrism_cell_triangle_mem_horn_of_generator_four_le","standardTypeABoundaryPrism_generator_dim_eq_two_of_cell_target_dim_two","standardTypeABoundaryPrism_generator_dim_eq_two_or_three_of_cell_target_dim_three","standardTypeABoundaryPrism_cell_scaled_frontier_refined"]
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
    assert inventory(baseline) == NAMES and len(NAMES) == 11

    def card(s: str) -> str:
        return replacement(s, '  simp only [Fintype.card_fin] at hcard\n  omega',
            '  simp only [Fintype.card_fin] at hcard\n'
            '  have hdim : (s.x.cast s.hd).dim = s.d + 1 := rfl\n'
            '  rw [hdim] at hcard\n'
            '  omega')

    def pairing(s: str) -> str:
        old = (
            "/-- The same lower bound for Mathlib's public `pairing k.castSucc 1` rather\n"
            "than its implementation-level pairing core. -/\n"
            "theorem unionProdPairing_typeTwo_target_dim_ge_left\n"
            "    {m : ℕ}\n"
            "    (k : Fin (m + 1))\n"
            "    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :\n"
            "    m + 1 ≤ z.val.dim + 1 := by\n"
            "  have z' :\n"
            "      (SSet.prodStdSimplex.pairingCore.{u} k 1).pairing.II := by\n"
            "    simpa only [SSet.prodStdSimplex.pairing_castSucc] using z\n"
            "  have h := unionProdPairingCore_typeTwo_target_dim_ge_left k z'\n"
            "  simpa only [SSet.prodStdSimplex.pairing_castSucc] using h"
        )
        new = (
            "/-- The same lower bound for the exact pinned `pairingCore k 1` pairing used in\n"
            "v1.61.  The pinned Mathlib API does not expose a separate public\n"
            "`prodStdSimplex.pairing`; no nonexistent theorem is invoked. -/\n"
            "theorem unionProdPairing_typeTwo_target_dim_ge_left\n"
            "    {m : ℕ}\n"
            "    (k : Fin (m + 1))\n"
            "    (z : (SSet.prodStdSimplex.pairingCore.{u} k 1).pairing.II) :\n"
            "    m + 1 ≤ z.val.dim + 1 := by\n"
            "  exact unionProdPairingCore_typeTwo_target_dim_ge_left k z"
        )
        return replacement(s, old, new)

    def finite_and_tensor(s: str) -> str:
        s = replacement(s, 'open CategoryTheory\nopen Opposite',
            'open CategoryTheory\nopen MonoidalCategory\nopen Opposite')
        return replacement(s,
            '  | zero =>\n'
            '      have hi : i = 0 := Subsingleton.elim _ _\n'
            '      subst i\n'
            '      simp at h0',
            '  | zero =>\n'
            '      have hbad : i.val < 0 := hn\n'
            '      exact False.elim (Nat.not_lt_zero _ hbad)')

    def upper_dimension(s: str) -> str:
        s = replacement(s,
            'theorem standardTypeABoundaryPrism_cell_target_dim_le_generator_succ\n'
            '    (g : StandardTypeAHornAttachmentGeneratorIndex)\n'
            '    (j : ℕ)\n'
            '    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :',
            'theorem standardTypeABoundaryPrism_cell_target_dim_le_generator_succ\n'
            '    (g : StandardTypeAHornAttachmentGeneratorIndex)\n'
            '    (j : ℕ)\n'
            '    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :')
        s = replacement(s,
            '  let P := standardTypeABoundaryPrismPairing g',
            '  let P := standardTypeABoundaryPrismPairing.{u} g')
        return replacement(s,
            '  simpa [z] using\n'
            '    (SSet.dim_le_of_nonDegenerate z (g.n + 1))',
            '  simpa [z] using\n'
            '    (SSet.dim_le_of_nonDegenerate\n'
            '      ((Δ[g.n] : SSet.{u}) ⊗ (Δ[1] : SSet.{u}))\n'
            '      z (g.n + 1))')

    prior = finite_and_tensor(pairing(card(baseline)))
    variants = {
        'cardinality-only': card(baseline),
        'pinned-pairing-only': pairing(baseline),
        'finite-and-tensor-only': finite_and_tensor(baseline),
        'prior-complete-missing-upper-dimension': prior,
        'upper-dimension-only': upper_dimension(baseline),
        'complete-v163': upper_dimension(prior),
    }
    for name, source in variants.items():
        assert inventory(source) == NAMES, ('declaration names changed', name)
    assert blob(variants['complete-v163'].encode()) == CANDIDATE
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
    assert original == (variants['complete-v163'].encode() if blob(original) == CANDIDATE else baseline.encode())
    rows = []
    manifest = None
    try:
        for name, source in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)), ('forbidden code', name)
            target.write_text(source, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v163-') as tmp:
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
                print('KUUOS_V163_DIRECT ' + json.dumps(row), flush=True)
        assert not rows[0]['success'] and rows[0]['exit_code'] != 0
        selected = next((r for r in rows if r['candidate'] == 'complete-v163'
            and r['success']), None)
        assert selected is not None, 'complete v1.62 candidate not yet Lean certified'
        source = variants['complete-v163'].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'real-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(),
            provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'candidate-script.py').write_bytes((root / 'scripts/ci_kuuos_v163_codeai.py').read_bytes())
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
    print('KUUOS_V163_DIRECT_AND_REAL_MCP_SUCCESS '+json.dumps(manifest), flush=True)


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
    assert original == (variants['complete-v163'].encode() if blob(original) == CANDIDATE else (root / 'legacy/v5.291' / REL).read_bytes())
    assert manifest['dependencies'] == DEPENDENCIES and manifest['baseline_blob'] == BASE
    assert manifest['selected']['candidate'] == 'complete-v163'
    assert source == variants['complete-v163'].encode()
    assert blob(source) == manifest['selected']['blob'] == CANDIDATE
    assert hashlib.sha256(source).hexdigest() == manifest['source_sha256']
    assert manifest['selected']['success'] and manifest['selected']['exit_code'] == 0
    assert not manifest['selected']['errors']
    assert manifest['source_restored'] and not manifest['git_write_performed']
    assert not manifest['independent_ci_success']
    for output, repo_path in [
        ('candidate-script.py', 'scripts/ci_kuuos_v163_codeai.py'),
        ('workflow.yml', WORKFLOW)]:
        assert (out / output).read_bytes() == (root / repo_path).read_bytes()
    assert not FORBIDDEN_NEW.findall(mask_lean_comments(source.decode()))
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV163IndependentAudit.lean'
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
        assert len(rows) == len(AUDIT_NAMES) == 11, (len(rows), len(AUDIT_NAMES))
        assert {name for name, _ in rows} == {NS + '.' + name for name in AUDIT_NAMES}
        for _, axioms in rows:
            assert {v.strip() for v in axioms.split(',') if v.strip()} <= {
                'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V163_INDEPENDENT_11_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
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
