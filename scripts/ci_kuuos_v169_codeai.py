#!/usr/bin/env python3
"""KuuOS v1.69 CodeAI: isolate cause-separated research variants, real Lean/MCP, independent 13-axiom audit.
All testing runs in a disposable Actions checkout; a green variant is only a candidate, not an adopted source.
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

NS = 'KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
WORKFLOW = '.github/workflows/kuuos-v169-codeai-three-residual-table-real-mcp-v1.yml'
BASE = '88a39a4aa6c51593a3b578a07e2a054b04c5d541'
RESEARCH_EXACT = '8d235658c173045070a056dd9fac7627059847ed'
PATCH_PATH = 'scripts/kuuos_v169_codeai_version_bound_hunks_v1.json'
PATCH_BLOB = '1092f0c398c201b1b269fe27fae41f1d02707df7'
DEPENDENCIES = {
    'formal/KUOS/DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68.lean':
        'a2cd5dd5978b0ee9c5858f559670df9c1704ebe5',
    'formal/KUOS/DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67.lean':
        'b75410426cadb22421191a4a4be4641f787b6669',
    'formal/KUOS/DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53.lean':
        'e1101bc30b4e30a00a43a0ca6125cb1165c79227',
}
NAMES = [
    "standardTypeBSourceTriangle123",
    "standardTypeBSourceTriangle012",
    "standardTypeBSourceTriangle123_isSourceTriangle",
    "standardTypeBSourceTriangle012_isSourceTriangle",
    "standardTypeBSourceTriangle123_source_thin",
    "standardTypeBSourceTriangle012_source_thin",
    "isStandardVertexTriangle_eq_triangle",
    "standardTypeBSourceScaling_thin_cases",
    "standardTypeBCollapse12_map_minimal",
    "standardTypeBCollapse23_map_minimal",
    "standardTypeBCollapse12_triangle_source123_minimal",
    "standardTypeBCollapse12_triangle_source012_minimal",
    "standardTypeBCollapse23_triangle_source123_minimal",
    "standardTypeBCollapse23_triangle_source012",
    "standardTypeBCollapse12Base_thin_iff",
    "standardTypeBCollapse23Base_thin_iff",
    "standardTypeAThreeHornSaturatedScaling",
    "standardTypeBThreeTriangle012_eq_delta3",
    "standardTypeBThreeTriangle013_eq_delta2",
    "standardTypeBThreeTriangle023_eq_delta1",
    "standardTypeBThreeTriangle123_eq_delta0",
    "standardTypeBThreeTriangle012_mem_horn_one",
    "standardTypeBThreeTriangle013_mem_horn_one",
    "standardTypeBThreeTriangle123_mem_horn_one",
    "standardTypeBThreeTriangle023_notMem_horn_one",
    "standardTypeBThreeTriangle012_mem_horn_two",
    "standardTypeBThreeTriangle023_mem_horn_two",
    "standardTypeBThreeTriangle123_mem_horn_two",
    "standardTypeBThreeTriangle013_notMem_horn_two",
    "standardTypeAThree_index_one_triangle_012_thin",
    "standardTypeAThree_index_two_triangle_123_thin",
    "standardTypeAThreeHornSaturatedScaling_one_eq_q12Base",
    "standardTypeAThreeHornSaturatedScaling_two_eq_q23Base",
    "StandardTypeAThreeResidualTable",
    "standardTypeAThreeResidualTable",
    "standardTypeABoundaryPrism_cell_target_dim_three_residual_table",
    "standardTypeABoundaryPrism_generator_two_target_three_complete_local_table",
]

def candidates(baseline: str) -> dict[str, str]:
    assert prior.blob(baseline.encode()) == BASE
    assert prior.inventory(baseline) == NAMES and len(NAMES) == 37
    data = json.loads(pathlib.Path(PATCH_PATH).read_text(encoding="utf-8"))
    assert data["schema"] == "kuuos_v169_version_bound_hunks_v1"
    assert data["source_relative_path"] == REL
    assert data["baseline_blob"] == BASE and data["research_candidate_blob"] == RESEARCH_EXACT
    assert data["preserve_historical_source"] is True
    assert data["public_declarations"] == 37
    hunks = data["hunks"]
    assert len(hunks) == 15
    lines = baseline.split("\n")
    def apply_hunks(selected: set[int]) -> str:
        cursor = 0
        out: list[str] = []
        for k, h in enumerate(hunks):
            if k not in selected:
                continue
            start, old, new = h["start"], h["old"], h["new"]
            assert isinstance(start, int) and isinstance(old, list) and isinstance(new, list)
            assert all(isinstance(s, str) for s in old + new)
            assert cursor <= start <= len(lines)
            assert lines[start:start + len(old)] == old, ("hunk source mismatch", k)
            out.extend(lines[cursor:start])
            out.extend(new)
            cursor = start + len(old)
        out.extend(lines[cursor:])
        return "\n".join(out)
    groups = {
        "namespace-reducible-only": {0, 1},
        "concrete-horn-carriers-only": set(range(2, 11)),
        "universe-explicit-only": {11, 12, 13, 14},
        "namespace-reducible-and-horns": set(range(11)),
        "research-exact-all-15-hunks": set(range(15)),
    }
    out = {name: apply_hunks(selected) for name, selected in groups.items()}
    assert prior.blob(out["research-exact-all-15-hunks"].encode()) == RESEARCH_EXACT
    for name, source in out.items():
        assert prior.inventory(source) == NAMES, ("public declaration inventory altered", name)
    return out


def pins(root: pathlib.Path) -> None:
    prior.pins(root)
    assert prior.blob((root / PATCH_PATH).read_bytes()) == PATCH_BLOB
    assert prior.blob((root / 'legacy/v5.291' / REL).read_bytes()) == BASE
    for p, sha in DEPENDENCIES.items():
        assert prior.blob((root / p).read_bytes()) == sha, ('dependency SHA mismatch', p)


def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = prior.command(root, ['lake', '-KleanArgs=-DwarningAsError=true',
        '-KleanArgs=-DsorryAsError=true', 'build', NS], out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'direct exact-source Strict Lean failed'


def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import (
        run_loop, mcp_tactic_provider, mask_lean_comments, FORBIDDEN_NEW)
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert prior.blob(original) == os.environ['CHECKOUT_BLOB']
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    assert original in {baseline.encode(), *(s.encode() for s in variants.values())}
    records = []
    manifest = None
    try:
        for name, source in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)), name
            target.write_text(source, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v169-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = prior.command(root, ['lake', 'env', 'lean',
                    '-DwarningAsError=true', '-Dweak.sorryAsError=true',
                    '-o', str(olean), REL], out / (name + '.log'), 900)
                log = p.stdout + '\n' + p.stderr
                errors = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {
                    'candidate': name, 'head': os.environ['SOURCE_HEAD'],
                    'blob': prior.blob(source.encode()),
                    'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                    'exit_code': p.returncode, 'errors': errors,
                    'success': p.returncode == 0 and olean.is_file()
                        and not errors and 'sorryAx' not in log,
                }
                records.append(row)
                (out / 'candidates.json').write_text(json.dumps(records, indent=2))
                print('KUUOS_V169_DIRECT ' + json.dumps(row), flush=True)
        assert not records[0]['success'], 'the broken baseline unexpectedly passed'
        chosen = next((row for row in records[1:] if row['success']
            and row['candidate'] == 'research-exact-all-15-hunks'), None)
        assert chosen is not None, 'The lint-compliant v1.69 candidate did not pass direct pinned Lean'
        source = variants[chosen['candidate']].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL,
            output_dir=out / 'real-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(),
            provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(json.dumps(receipt, indent=2))
        prior.verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'candidate-script.py').write_bytes(
            (root / 'scripts/ci_kuuos_v169_codeai.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / WORKFLOW).read_bytes())
        (out / 'repair-hunks.json').write_bytes((root / PATCH_PATH).read_bytes())
        manifest = {
            'head': os.environ['SOURCE_HEAD'], 'checkout_blob': prior.blob(original),
            'selected': chosen, 'source_sha256': hashlib.sha256(source).hexdigest(),
            'dependencies': DEPENDENCIES, 'baseline_blob': BASE,
            'source_restored': False, 'git_write_performed': False,
            'independent_ci_success': False,
        }
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original and manifest is not None
    manifest['source_restored'] = True
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('KUUOS_V169_DIRECT_AND_REAL_MCP_SUCCESS ' + json.dumps(manifest), flush=True)


def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments, FORBIDDEN_NEW
    pins(root)
    manifest = json.loads((out / 'manifest.json').read_text())
    receipt = json.loads((out / 'mcp.json').read_text())
    source = (out / 'source.lean').read_bytes()
    original = (root / REL).read_bytes()
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    chosen = manifest['selected']
    assert manifest['head'] == os.environ['SOURCE_HEAD']
    assert manifest['checkout_blob'] == os.environ['CHECKOUT_BLOB'] == prior.blob(original)
    assert original in {baseline.encode(), *(s.encode() for s in variants.values())}
    assert manifest['dependencies'] == DEPENDENCIES and manifest['baseline_blob'] == BASE
    assert chosen['candidate'] == 'research-exact-all-15-hunks' and chosen['success'] and chosen['exit_code'] == 0
    assert not chosen['errors']
    assert source == variants[chosen['candidate']].encode()
    assert prior.blob(source) == RESEARCH_EXACT
    assert prior.blob(source) == chosen['blob']
    assert hashlib.sha256(source).hexdigest() == chosen['source_sha256'] == manifest['source_sha256']
    assert manifest['source_restored'] and not manifest['git_write_performed']
    assert not manifest['independent_ci_success']
    for output, path in [
        ('candidate-script.py', 'scripts/ci_kuuos_v169_codeai.py'),
        ('workflow.yml', WORKFLOW),
        ('repair-hunks.json', PATCH_PATH),
    ]:
        assert (out / output).read_bytes() == (root / path).read_bytes()
    assert not FORBIDDEN_NEW.findall(mask_lean_comments(source.decode()))
    prior.verify_mcp(receipt, source)
    target = root / REL
    audit = root / 'formal/KUOS/DependentOriginationV169IndependentAudit.lean'
    assert not audit.exists()
    try:
        target.write_bytes(source)
        strict_build(root, out)
        audit.write_text('import ' + NS + '\n'
            + '\n'.join('#check ' + NS + '.' + n for n in NAMES) + '\n'
            + '\n'.join('#print axioms ' + NS + '.' + n for n in NAMES) + '\n')
        p = prior.command(root, ['lake', 'env', 'lean',
            '-DwarningAsError=true', '-Dweak.sorryAsError=true',
            str(audit)], out / 'axioms.log', 900)
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(
            r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
            log, re.S)
        assert len(rows) == len(NAMES) == 37, ('axiom count', len(rows))
        assert {n for n, _ in rows} == {NS + '.' + name for name in NAMES}
        for _, axioms in rows:
            assert {a.strip() for a in axioms.split(',') if a.strip()} <= {
                'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V169_INDEPENDENT_37_DECLARATIONS_STANDARD_AXIOMS_SUCCESS',
            flush=True)
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
        print(json.dumps({name: prior.blob(s.encode()) for name, s in
            candidates(args.directory.read_text()).items()}, indent=2))
        return
    root = pathlib.Path('.').resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == 'direct' else independent)(root, out)


if __name__ == '__main__':
    main()
