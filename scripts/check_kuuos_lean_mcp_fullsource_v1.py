#!/usr/bin/env python3
"""KuuOS pinned Lean4 full-source evidence before proof repair.

Read-only, exact source blob-bound and fail-closed. This tool is an evidence
collector, NOT an AI proof generator, Lean kernel or CI authority. Web
references are advisory and cannot replace an actual pinned API probe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from collections import deque
from dataclasses import dataclass
from typing import Any

SCHEMA = 'kuuos-lean-fullsource-v1'
TOOLCHAIN = 'leanprover/lean4:v4.30.0-rc2'
MATHLIB_REV = '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
MAX_TARGETS = 150
MAX_DEPENDENCIES = 3000
MAX_API_PROBES = 30
HEX40 = re.compile(r'^[0-9a-f]{40}$')
LEANSYM = re.compile(r"^[^\W\d_][\w₀-₉']*(?:\.[^\W\d_][\w₀-₉']*)*$", re.UNICODE)
ERROR_LINE = re.compile(r'error: (?P<path>formal/[^:\s]+\.lean):(?P<line>\d+):(?P<column>\d+):\s*(?P<message>.*)')
DECL = re.compile(r'^\s*(?:(?:private|protected|noncomputable|unsafe|partial|scoped)\s+)*(theorem|lemma|def|abbrev|opaque|instance|structure|class|inductive)\s+([^\s(:{]+)')
EXTERNAL_REFERENCE = {
    'lean-tactic-reference': 'https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference',
    'lean-tactics-manual': 'https://leanprover.github.io/theorem_proving_in_lean4/Tactics/',
    'lean-language-reference': 'https://lean-lang.org/doc/reference/latest/',
    'pinned-mathlib-revision': 'https://github.com/leanprover-community/mathlib4/tree/' + MATHLIB_REV,
}
CASES = (
    ('field_missing', re.compile(r'Invalid field|environment does not contain', re.I),
     'Named field may not exist in the pinned imported namespace, or the receiver type differs.',
     ['Read whole import chain and local definitions', '#check the fully qualified candidate against pinned mathlib', 'Check the receiver type before replacing the name']),
    ('unresolved_identifier', re.compile(r'Unknown identifier|unknown constant|unknown declaration', re.I),
     'A name may be out of namespace, absent from imported API, or absent due to an earlier failed declaration.',
     ['Read all imports and enclosing namespace', '#check candidate fully qualified name with the exact imports', 'Investigate preceding compilation errors before touching the reported line']),
    ('universe_mismatch', re.compile(r'level params|universe|Type u[_\d]*.*Type u', re.I | re.S),
     'A fresh explicit universe may be independent of the source term universe.',
     ['Inspect whole declaration including universe binders', 'Compare exact expected/actual sorts and implicit arguments', 'Try dependent type inference in a scratch proof, then kernel-verify']),
    ('type_mismatch', re.compile(r'Type mismatch|Application type mismatch|has type.*expected', re.I | re.S),
     'Unification may fail due to casts, implicit instances, codomain, coercions or universe levels.',
     ['Read full theorem statement and dependent signatures', 'Inspect #check and pp.explicit/pp.coercions in the exact environment', 'Propose separate typed equalities and test with Lean MCP']),
    ('rewrite_normal_form', re.compile(r'[Rr]ewrite.*failed|Did not find an occurrence|simp.*failed', re.I | re.S),
     'Target or hypothesis has already normalized, or the rewrite is aimed at a hidden instance.',
     ['Use Lean MCP lean_goal at the actual tactic position', 'Compare goal before/after simp and the exact equality direction', 'Try change, show or a typed congrArg on an existing proof in scratch']),
    ('remaining_goals', re.compile(r'unsolved goals|no goals to be solved', re.I),
     'A diagnostic location can precede the actual unfinished tactic; branch structure and goal states matter.',
     ['Read entire enclosing by proof and neighboring declarations', 'Inspect lean_goal for each candidate tactic line, not only the reported line', 'Use lean_multi_attempt with bounded candidates and check all remaining goals']),
    ('timeout', re.compile(r'timed out|return_code["\s:]+124|exit code 124|timeout', re.I),
     'Resource deadline, not proof acceptance or a Lean elaboration contradiction.',
     ['Read last completed Lean job and cache receipts', 'Retry same exact source after cache restoration', 'Do not relax warning/error or sorry checking']),
    ('other', re.compile(r'.*', re.S),
     'Cause unresolved: retain source and compiler observation without guessing.',
     ['Read complete source and pinned dependency signatures', 'Use exact environment to request more elaborator state']),
)


class EvidenceObstruction(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def rel_file(root: pathlib.Path, value: str) -> pathlib.Path:
    if not isinstance(value, str) or '\\' in value:
        raise EvidenceObstruction('invalid path type or slash')
    p = pathlib.PurePosixPath(value)
    if p.is_absolute() or p.parts[:1] != ('formal',) or p.suffix != '.lean' or '.' in p.parts or '..' in p.parts:
        raise EvidenceObstruction('Lean source path must be contained under formal/: ' + repr(value))
    candidate = root / value
    if not candidate.is_file() or candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
        raise EvidenceObstruction('missing/unsafe Lean source: ' + value)
    return candidate


def get_pins(root: pathlib.Path) -> dict:
    toolchain = (root / 'lean-toolchain').read_text(encoding='utf-8').strip()
    if toolchain != TOOLCHAIN:
        raise EvidenceObstruction('Lean pin mismatch: ' + toolchain)
    manifest = json.loads((root / 'lake-manifest.json').read_text(encoding='utf-8'))
    packages = [x for x in manifest.get('packages', []) if x.get('name') == 'mathlib']
    if len(packages) != 1 or packages[0].get('rev') != MATHLIB_REV:
        raise EvidenceObstruction('mathlib manifest pin mismatch')
    return {'lean': toolchain, 'mathlib': MATHLIB_REV}


def validate_plan(root: pathlib.Path, plan: Any) -> tuple[list[dict], bool]:
    if not isinstance(plan, dict) or plan.get('schema_version') != SCHEMA:
        raise EvidenceObstruction('unsupported evidence plan schema')
    head = plan.get('source_head')
    if not isinstance(head, str) or not HEX40.fullmatch(head):
        raise EvidenceObstruction('exact 40-character claimed source HEAD required')
    targets = plan.get('targets')
    if not isinstance(targets, list) or not (1 <= len(targets) <= MAX_TARGETS):
        raise EvidenceObstruction('1..150 exact source targets required')
    seen: set[str] = set()
    verified: list[dict] = []
    for item in targets:
        if not isinstance(item, dict) or set(item) != {'path', 'git_blob_sha'}:
            raise EvidenceObstruction('each target must have exact path and Git blob SHA')
        path, blob = item['path'], item['git_blob_sha']
        if not isinstance(blob, str) or not HEX40.fullmatch(blob):
            raise EvidenceObstruction('invalid exact source Git blob SHA')
        p = rel_file(root, path)
        if path in seen:
            raise EvidenceObstruction('duplicate exact source path: ' + path)
        seen.add(path)
        raw = p.read_bytes()
        actual = git_blob(raw)
        if actual != blob:
            raise EvidenceObstruction(f'exact source blob mismatch for {path}: got {actual} expected {blob}')
        verified.append({'path': path, 'git_blob_sha': actual, 'sha256': sha256(raw),
                         'line_count': len(raw.splitlines()), 'bytes': len(raw)})
    changed = plan.get('changed_lean_files')
    exhaustive = isinstance(changed, list) and len(changed) == len(set(changed)) and set(changed) == seen
    if plan.get('scope') == 'all-changed' and not exhaustive:
        raise EvidenceObstruction('all-changed claim requires complete identical changed_lean_files set')
    if plan.get('scope') not in ('all-changed', 'scoped'):
        raise EvidenceObstruction('explicit all-changed or scoped mode required')
    return verified, exhaustive and plan['scope'] == 'all-changed'


def imports_of(content: str) -> list[str]:
    # Lexical import extraction, not a replacement for the Lean import resolver.
    result: list[str] = []
    for ln in content.splitlines():
        if not ln.startswith('import '):
            continue
        for module in ln.partition('--')[0].split()[1:]:
            if module and module not in result:
                result.append(module)
    return result


def namespace_of(content: str, line: int) -> list[str]:
    stack: list[str] = []
    for s in content.splitlines()[:max(0, line)]:
        if s.startswith('namespace '):
            stack.append(s.partition(' ')[2].strip())
        elif s.strip() == 'end' and stack:
            stack.pop()
        elif s.startswith('end ') and stack:
            stack.pop()
    return stack


def declarations_of(content: str, module: str, *, max_signature_lines: int = 150) -> list[dict]:
    lines = content.splitlines()
    matches = [(i, DECL.match(s)) for i, s in enumerate(lines) if DECL.match(s)]
    out: list[dict] = []
    for index, (start, match) in enumerate(matches):
        end = matches[index + 1][0] if index + 1 < len(matches) else len(lines)
        # A signature is the full statement up to the defining := or 'where'.
        sigend = end
        for j in range(start, min(end, start + max_signature_lines)):
            if ':=' in lines[j] or re.search(r'\bwhere\s*$', lines[j]):
                sigend = j + 1
                break
        truncated = sigend == end and end - start > max_signature_lines
        if truncated:
            sigend = start + max_signature_lines
        text = '\n'.join(lines[start:sigend])
        out.append({'kind': match.group(1), 'name': match.group(2),
                    'name_lexical': module + '.' + match.group(2),
                    'line': start + 1, 'end_line': end,
                    'signature_end_line': sigend, 'signature_lexical': text,
                    'signature_sha256': sha256(text.encode()),
                    'truncated': truncated,
                    'namespaces_at_declaration': namespace_of(content, start)})
    return out


def classify_diagnostic(message: str) -> dict:
    for kind, pattern, hypothesis, checks in CASES:
        if pattern.search(message):
            return {'kind': kind, 'cause_hypothesis': hypothesis,
                    'next_experiments_not_proofs': checks,
                    'authority': 'INFERRED_NOT_KERNEL_VERIFIED',
                    'reference_urls': [EXTERNAL_REFERENCE['lean-tactic-reference'],
                                       EXTERNAL_REFERENCE['lean-tactics-manual']]}
    raise AssertionError('other case is total')


def ci_diagnostics(log: str) -> tuple[list[dict], bool]:
    """Preserve bounded *complete compiler diagnostic blocks*, not error lines.

    GitHub Actions stamps each line. Subgoals, actual/expected types, and
    unfolding context are normally in following lines, so a single-line
    parser would discard the very elaboration evidence the repair needs.
    """
    errors: list[dict] = []
    active: dict | None = None
    continuation: list[str] = []

    def finish() -> None:
        nonlocal active, continuation
        if active is not None:
            active['message'] = '\n'.join(continuation)[:6500]
            active['diagnostic_truncated'] = len(continuation) >= 55 or len('\n'.join(continuation)) > 6500
            active.update(classify_diagnostic(active['message']))
            errors.append(active)
        active = None
        continuation = []

    for raw in log.splitlines():
        row = re.sub(r'^20\d\d-\d\d-\d\dT[^\s]+Z\s+', '', raw)
        m = ERROR_LINE.search(row)
        if m:
            finish()
            active = {'path': m.group('path'), 'line': int(m.group('line')),
                      'column': int(m.group('column'))}
            continuation = [m.group('message')]
        elif active is not None:
            if (row.startswith(('error: ', 'Some required targets', '##[error]',
                                'Build completed', 'error Lean'))
                    or len(continuation) >= 55):
                finish()
            else:
                continuation.append(row)
    finish()
    timeout = bool(re.search(r'"return_code"\s*:\s*124|exit code 124|timed out', log, re.I))
    return errors, timeout


def api_probes(root: pathlib.Path, candidates: Any, *, execute: bool,
               timeout: int) -> list[dict]:
    if candidates is None:
        return []
    if not isinstance(candidates, list) or len(candidates) > MAX_API_PROBES:
        raise EvidenceObstruction('at most 30 explicit API probes')
    observed: list[dict] = []
    for entry in candidates:
        if not isinstance(entry, dict) or set(entry) != {'name', 'import_module'}:
            raise EvidenceObstruction('API probe must name exact symbol and Lean module')
        name, imp = entry['name'], entry['import_module']
        if not all(isinstance(v, str) and LEANSYM.fullmatch(v) for v in (name, imp)):
            raise EvidenceObstruction('invalid/injectable API probe syntax')
        evidence = {'symbol': name, 'import_module': imp,
                    'status': 'NO_DATA_NOT_RUN', 'authority': 'NO_DATA'}
        if execute:
            with tempfile.TemporaryDirectory(prefix='kuuos-lean-api-') as td:
                path = pathlib.Path(td) / 'PinnedAPIProbe.lean'
                path.write_text(f'import {imp}\nset_option pp.explicit true\n#check {name}\n')
                try:
                    done = subprocess.run(['lake', 'env', 'lean', str(path)], cwd=root,
                                          capture_output=True, text=True, timeout=timeout)
                except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
                    evidence['status'] = 'OBSTRUCTION_EXECUTION_UNAVAILABLE'
                    evidence['compiler_obstruction'] = type(exc).__name__
                else:
                    evidence['status'] = 'COMPILER_PRESENT' if done.returncode == 0 else 'COMPILER_REJECTED'
                    evidence['authority'] = 'PINNED_LEAN_COMMAND_OBSERVED'
                    evidence['exit_code'] = done.returncode
                    evidence['compiler_output_excerpt'] = (done.stdout + '\n' + done.stderr)[-2500:]
        observed.append(evidence)
    return observed


def create_report(root: pathlib.Path, plan: dict, ci_log: str | None, outdir: pathlib.Path,
                  *, max_deps: int, probe_api: bool, api_timeout: int,
                  previous_casebook: pathlib.Path | None = None) -> dict:
    root = root.resolve(strict=True)
    outdir = outdir.resolve()
    if outdir.is_relative_to(root):
        raise EvidenceObstruction('output must be outside source tree')
    if max_deps < 1 or max_deps > MAX_DEPENDENCIES:
        raise EvidenceObstruction('max local dependency budget out of range')
    pins = get_pins(root)
    checked, exhaustive = validate_plan(root, plan)
    # Fail closed against accidental overwrites: each run has a fresh immutable
    # evidence directory; reuse prior learning via --previous-casebook instead.
    if outdir.exists() and any(outdir.iterdir()):
        raise EvidenceObstruction('append-only evidence: output directory already contains files')
    # No partial snapshots are emitted until the entire source manifest passes.
    outdir.mkdir(parents=True, exist_ok=True)
    snapshots = outdir / 'full_sources'
    queue: deque[str] = deque(x['path'] for x in checked)
    scanned: dict[str, dict] = {}
    errors, timeout = ci_diagnostics(ci_log) if ci_log is not None else ([], False)
    all_changed = {x['path'] for x in checked}
    deps_exceeded = False
    missing_local: set[str] = set()
    while queue:
        relative = queue.popleft()
        if relative in scanned:
            continue
        if len(scanned) >= max_deps + len(checked):
            deps_exceeded = True
            break
        path = rel_file(root, relative)
        raw = path.read_bytes()
        contents = raw.decode('utf-8')
        module = relative.removeprefix('formal/').removesuffix('.lean').replace('/', '.')
        deps = imports_of(contents)
        local: list[str] = []
        external: list[str] = []
        for dep in deps:
            dep_path = 'formal/' + dep.replace('.', '/') + '.lean'
            if (root / dep_path).is_file():
                # Validates containment and rejects symlink later.
                local.append(dep_path)
                if dep_path not in scanned:
                    queue.append(dep_path)
            else:
                external.append(dep)
                if dep.startswith(('KUOS.', 'KuuOSFormal.', 'Kuu.')):
                    missing_local.add(dep)
        source = snapshots / relative
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(raw)
        scanned[relative] = {
            'path': relative, 'source_sha256': sha256(raw), 'git_blob_sha': git_blob(raw),
            'line_count': len(contents.splitlines()), 'all_lines_read': True,
            'snapshot_relative': str(source.relative_to(outdir)),
            'imports_lexical': deps, 'direct_imports_local': local,
            'external_imports_not_verified': external,
            'declarations_lexical': declarations_of(contents, module),
        }
    for target in checked:
        evidence = scanned.get(target['path'])
        if evidence is None or evidence['git_blob_sha'] != target['git_blob_sha']:
            raise EvidenceObstruction('changed source unexpectedly disappeared/mutated during scan')
    for err in errors:
        data = scanned.get(err['path'])
        if data:
            n = err['line']
            statements = [x for x in data['declarations_lexical'] if x['line'] <= n <= x['end_line']]
            err['enclosing_declaration_lexical'] = statements[-1]['name_lexical'] if statements else None
            err['full_source_sha256'] = data['source_sha256']
            err['file_read_in_full'] = True
        else:
            err['file_read_in_full'] = False
            err['obstruction'] = 'CI error is outside the exact captured local import closure'
    signatures = []
    for target in checked:
        source = scanned[target['path']]
        text = (snapshots / target['path']).read_text()
        for p in source['direct_imports_local']:
            dependency = scanned.get(p)
            if dependency is None:
                continue
            for d in dependency['declarations_lexical']:
                name = d['name']
                if re.search(r'(?<![\w])' + re.escape(name) + r'(?![\w])', text):
                    signatures.append({'target': target['path'], 'dependency': p,
                                       'referenced_name_lexical': name,
                                       'signature_sha256': d['signature_sha256'],
                                       'signature': d['signature_lexical'],
                                       'authority': 'LEXICAL_REFERENCE_NOT_TYPE_RESOLUTION'})
    historical: list[dict] = []
    if previous_casebook is not None:
        for row in previous_casebook.read_text(encoding='utf-8').splitlines():
            if row.strip():
                e = json.loads(row)
                if not isinstance(e, dict):
                    raise EvidenceObstruction('casebook entry is not an object')
                historical.append(e)
                if len(historical) > 2000:
                    raise EvidenceObstruction('casebook evidence history too large')
    matched_prior = 0
    for err in errors:
        matches = [z for z in historical
                   if z.get('classification') == err['kind']
                   and z.get('location', {}).get('path') == err['path']
                   and z.get('source_blob_sha256') == err.get('full_source_sha256')]
        err['prior_attempts_same_source_unverified'] = matches[-12:]
        matched_prior += len(matches)
    probes = api_probes(root, plan.get('api_probes', []), execute=probe_api, timeout=api_timeout)
    obstruction = []
    if deps_exceeded:
        obstruction.append('local source import closure exceeded explicitly bounded max-deps')
    if missing_local:
        obstruction.append('local-looking import modules lack formal source: ' + ', '.join(sorted(missing_local)[:12]))
    if any(not e['file_read_in_full'] for e in errors):
        obstruction.append('CI diagnostic references source outside captured import closure')
    if timeout:
        obstruction.append('CI process had timeout; zero diagnostic errors is NOT a Lean success')
    if probe_api and any(z['status'] != 'COMPILER_PRESENT' for z in probes):
        obstruction.append('one or more pinned API probe symbols were not compiler-confirmed')
    report = {
        'schema_version': SCHEMA,
        'status': 'SOURCE_OBSERVATION_WITH_OBSTRUCTIONS' if obstruction else 'SOURCE_OBSERVATION_READY',
        'source_head_claimed_by_plan': plan['source_head'],
        'head_verified_using_live_git_ref': False,
        'source_file_git_blobs_verified': True,
        'changed_lean_coverage_all_claimed': exhaustive,
        'changed_targets_count': len(checked), 'changed_targets': checked,
        'full_source_snapshot_count': len(scanned),
        'full_import_closure_captured': not deps_exceeded and not missing_local,
        'sources': scanned,
        'dependent_signatures_lexical': signatures,
        'ci_errors': errors,
        'historical_casebook_entries_read': len(historical),
        'prior_cases_matched_same_source': matched_prior,
        'ci_log_status': ('NO_DATA' if ci_log is None else
                          ('CI_TIMEOUT_OBSERVED' if timeout else 'TEXT_DIAGNOSTICS_PARSED_NOT_CI_CERTIFIED')),
        'ci_log_bound_to_test_merge_tree': False,
        'api_probes': probes,
        'reference_urls_advisory_only': EXTERNAL_REFERENCE,
        'pins': pins,
        'obstructions': obstruction,
        'theorem_proof_certified': False,
        'ci_certified': False,
        'repair_patch_applied': False,
        'learning_scope': 'APPEND_ONLY_OBSERVATIONAL_CASES_NOT_MODEL_WEIGHTS',
        'next_authority_gate': 'Pinned Lean MCP diagnostic + isolated proof candidate + strict Lean CI + axiom audit',
    }
    # JSON evidence includes every full source's declaration header. Full text is
    # in its independently hashed full_sources/ snapshot, not truncated excerpt.
    (outdir / 'full_source_evidence.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    with (outdir / 'causal_casebook.jsonl').open('a', encoding='utf-8') as fp:
        for err in errors:
            event = {'source_head_claimed': plan['source_head'], 'source_blob_sha256': err.get('full_source_sha256'),
                     'location': {'path': err['path'], 'line': err['line'], 'column': err['column']},
                     'classification': err['kind'], 'cause_hypothesis': err['cause_hypothesis'],
                     'result': 'UNTESTED_HYPOTHESIS', 'kernel_certified': False,
                     'retained_obstruction': err.get('obstruction')}
            fp.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + '\n')
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-root', required=True)
    p.add_argument('--plan', required=True)
    p.add_argument('--ci-log')
    p.add_argument('--output-dir', required=True)
    p.add_argument('--max-local-deps', type=int, default=900)
    p.add_argument('--probe-pinned-api', action='store_true')
    p.add_argument('--api-timeout', type=int, default=90)
    p.add_argument('--previous-casebook', type=pathlib.Path)
    opts = p.parse_args()
    try:
        plan = json.loads(pathlib.Path(opts.plan).read_text())
        log = pathlib.Path(opts.ci_log).read_text() if opts.ci_log else None
        result = create_report(pathlib.Path(opts.project_root), plan, log,
                               pathlib.Path(opts.output_dir),
                               max_deps=opts.max_local_deps,
                               probe_api=opts.probe_pinned_api,
                               api_timeout=opts.api_timeout,
                               previous_casebook=opts.previous_casebook)
    except (EvidenceObstruction, OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print('KUUOS FULLSOURCE BLOCKED: ' + type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps({'status': result['status'],
                      'targets': result['changed_targets_count'],
                      'full_sources': result['full_source_snapshot_count'],
                      'errors': len(result['ci_errors']),
                      'obstructions': result['obstructions'],
                      'theorem_proof_certified': False,
                      'ci_certified': False}, ensure_ascii=False))
    return 0 if not result['obstructions'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
