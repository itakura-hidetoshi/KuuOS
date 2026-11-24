#!/usr/bin/env python3
"""Source-bound v1.54 CodeAI experiments; no git/gh, paid API, or branch writes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile

NS = 'KUOS.DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = '04e97878e278a722ffadf02fd04bcc927c5c537d'
DEP = 'formal/KUOS/DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53.lean'
DEP_BLOB = 'e1101bc30b4e30a00a43a0ca6125cb1165c79227'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v154-codeai-generated-llp-descent-real-mcp-v1.yml'
NAMES = [
    'hasLiftingProperty_of_epi_precomp',
    'standardTypeAEndpointGeneratedToInduced_epi',
    'standardTypeAEndpointPushoutProduct_hasLiftingProperty_of_generated',
    'standardTypeAEndpointGeneratedPushoutProductGenerators',
    'standardTypeAEndpointGeneratedPushoutProductGenerator_mem',
    'StandardTypeAEndpointGeneratedPushoutProductStable',
    'standardTypeAEndpointPushoutProductStable_of_generated',
    'StandardTypeAExternalGeneratedPushoutComparison',
    'StandardTypeAExternalGeneratedPushoutComparison.toStandardTypeAExternalGeneratedComparison',
    'StandardTypeAExternalGeneratedPushoutComparison.inducedTypeAAttachments_le_externalGenerated',
    'StandardTypeAExternalGeneratedPushoutComparison.endpointPushoutProducts_le_externalGenerated',
]
HORN = '(KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50.StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)'
ANCHOR = '    (K : StandardTypeAExternalGeneratedPushoutComparison E)\n'
EXPECTED = {
    'qualified-only': '8441ec7d9f696e50cf686315dae43459330629f4',
    'include-only': 'e2bdb237f0d9e6a019727d73aab438b9fb7db094',
    'qualified-and-include': 'f30f6065fa272873dbf7e1f2ad15a1237511f823',
    'qualified-include-intro': '32af6b08ac20bf1cba1f2b6f4a54e4762c9d6a72',
    'explicit-comparison': '72d318ccb09a307251d7f204b9c0120e78bc7e26',
    'adjacent-projections': 'ae25d6249785070767722984d4010e8b58942c22',
}


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def candidates(baseline: str) -> dict[str, str]:
    assert blob(baseline.encode()) == BASE, 'baseline SHA mismatch'
    assert baseline.count('g.toHornGenerator') == baseline.count(ANCHOR) == 1
    qualified = baseline.replace('g.toHornGenerator', HORN, 1)
    included = baseline.replace(ANCHOR, ANCHOR + '\ninclude K\n', 1)
    both = qualified.replace(ANCHOR, ANCHOR + '\ninclude K\n', 1)
    result = {'qualified-only': qualified, 'include-only': included, 'qualified-and-include': both}
    intro_old = '    intro g hHorn\n    intro X Y p hp'
    assert both.count(intro_old) == 1
    compact = both.replace(intro_old, '    intro g hHorn X Y p hp', 1)
    explicit, adjacent = compact, compact
    for name in ('inducedTypeAAttachments_le_externalGenerated', 'endpointPushoutProducts_le_externalGenerated'):
        old = '  K.toStandardTypeAExternalGeneratedComparison\n    .' + name
        assert compact.count(old) == 1
        new = ('  KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50.'
               'StandardTypeAExternalGeneratedComparison.' + name +
               '\n    (toStandardTypeAExternalGeneratedComparison K)')
        explicit = explicit.replace(old, new, 1)
        adjacent = adjacent.replace(old, '  (toStandardTypeAExternalGeneratedComparison K).' + name, 1)
    result.update({'qualified-include-intro': compact, 'explicit-comparison': explicit,
                   'adjacent-projections': adjacent})
    pattern = r'^(?:def|theorem|lemma|structure|instance)\s+([^\s(:]+)'
    inventory = re.findall(pattern, baseline, re.M)
    assert inventory == [n.rsplit('.', 1)[-1] for n in NAMES]
    for name, text in result.items():
        assert blob(text.encode()) == EXPECTED[name], ('candidate SHA mismatch', name)
        assert re.findall(pattern, text, re.M) == inventory
    return result


def pins(root: pathlib.Path) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
    assert require_pins(root)['mathlib_sha'] == '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
    assert blob((root / DEP).read_bytes()) == DEP_BLOB
    assert blob((root / 'scripts/kuuos_lean_mcp_repair_loop_v1.py').read_bytes()) == CORE_BLOB
    assert blob((root / 'formal/KUOS/DependentOriginationStandardTypeAEndpointPushoutProductV1_50.lean').read_bytes()) == '48ae0b637350ee8bfb63926327a4285d05b79af5'


def command(root: pathlib.Path, args: list[str], logfile: pathlib.Path, timeout: int = 600):
    p = subprocess.run(args, cwd=root, text=True, capture_output=True, timeout=timeout)
    logfile.write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
    print(p.stdout, p.stderr, flush=True)
    return p


def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = command(root, ['lake', '-KleanArgs=-DwarningAsError=true',
        '-KleanArgs=-DsorryAsError=true', 'build', NS], out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'strict dependency build failed'


def verify_mcp(receipt: dict, source: bytes) -> None:
    assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
    assert receipt['candidate_sha256'] == hashlib.sha256(source).hexdigest()
    assert receipt['source_restored'] and not receipt['git_write_performed']
    assert not receipt['independent_ci_success']
    assert len(receipt['rounds']) == 1
    r = receipt['rounds'][0]
    assert r['semantic_success'] and not r['partial'] and r['errors'] == 0
    assert r['direct_lean']['exit_code'] == 0 and r['forbidden_final_count'] == 0


def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import run_loop, mcp_tactic_provider, mask_lean_comments, FORBIDDEN_NEW
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert blob(original) == os.environ['CHECKOUT_BLOB']
    assert blob(original) in {BASE, *EXPECTED.values()}
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    rows = []
    manifest = None
    try:
        for name, text in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(text))
            target.write_text(text, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v154-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
                    '-Dweak.sorryAsError=true', '-o', str(olean), REL], out / (name + '.log'))
                log = p.stdout + '\n' + p.stderr
                errors = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {'candidate': name, 'blob': blob(text.encode()), 'exit_code': p.returncode,
                    'errors': errors, 'success': p.returncode == 0 and olean.is_file() and not errors and 'sorryAx' not in log}
                rows.append(row)
                (out / 'candidates.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
                print('KUUOS_V154_DIRECT ' + json.dumps(row, ensure_ascii=False), flush=True)
        assert not rows[0]['success'] and 'Invalid field' in (out / 'baseline.log').read_text()
        selected = next((r for r in rows[1:] if r['success']), None)
        assert selected is not None, 'no directly verified candidate'
        source = variants[selected['candidate']].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'live-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(), provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'public-root-test.py').write_bytes((root / 'tests/test_public_root_restoration.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / WORKFLOW).read_bytes())
        (out / 'candidate-script.py').write_bytes((root / 'scripts/ci_kuuos_v154_codeai.py').read_bytes())
        manifest = {'head': os.environ['SOURCE_HEAD'], 'checkout_blob': blob(original),
            'selected': selected, 'source_sha256': hashlib.sha256(source).hexdigest(),
            'git_write_performed': False, 'independent_ci_success': False}
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    assert manifest is not None
    manifest['source_restored'] = True
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('KUUOS_V154_DIRECT_AND_REAL_MCP_SUCCESS ' + json.dumps(manifest), flush=True)


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
    assert source == variants[selected['candidate']].encode()
    assert blob(source) == selected['blob'] == EXPECTED[selected['candidate']]
    assert hashlib.sha256(source).hexdigest() == m['source_sha256']
    assert selected['success'] and selected['exit_code'] == 0 and not selected['errors']
    assert m['source_restored'] and not m['git_write_performed'] and not m['independent_ci_success']
    assert (out / 'candidate-script.py').read_bytes() == (root / 'scripts/ci_kuuos_v154_codeai.py').read_bytes()
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV154IndependentAudit.lean'
    assert not audit.exists()
    try:
        target.write_bytes(source)
        strict_build(root, out)
        audit.write_text('import ' + NS + '\n' + '\n'.join('#print axioms ' + NS + '.' + n for n in NAMES) + '\n')
        p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
            '-Dweak.sorryAsError=true', str(audit)], out / 'axioms.log')
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", log, re.S)
        assert len(rows) == len(NAMES) == 11
        assert {n for n, _ in rows} == {NS + '.' + n for n in NAMES}
        for _, axioms in rows:
            assert {x.strip() for x in axioms.split(',') if x.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V154_INDEPENDENT_11_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
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
        print(json.dumps({n: blob(s.encode()) for n, s in candidates(args.directory.read_text()).items()}, indent=2))
        return
    root = pathlib.Path('.').resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == 'direct' else independent)(root, out)


if __name__ == '__main__':
    main()
