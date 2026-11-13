#!/usr/bin/env python3
"""Gate existing bounded Lean MCP repair behind entire-source evidence.

On a disposable checkout only. Source observation and local proof repair are
separate; neither outcome automatically authorizes a GitHub write or CI claim.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from collections.abc import Callable

from scripts.check_kuuos_lean_mcp_fullsource_v1 import (
    EvidenceObstruction, create_report, declarations_of, imports_of, sha256,
)


class RepairPreflightObstruction(EvidenceObstruction):
    pass


def gate_repair(*, root: pathlib.Path, plan: dict,
                output_dir: pathlib.Path, target: str, acknowledged_isolated: bool,
                ci_log: str | None = None, max_iterations: int = 3,
                runner: Callable | None = None, provider: Callable | None = None,
                previous_casebook: pathlib.Path | None = None) -> dict:
    root = root.resolve(strict=True)
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RepairPreflightObstruction('append-only repair: output directory must be fresh')
    # The scanner checks exact source blobs, all declared targets, transitive
    # local imports, output containment and pins before the repair runner starts.
    evidence = create_report(root, plan, ci_log, output_dir / 'full_source',
                             max_deps=1800, probe_api=acknowledged_isolated, api_timeout=90,
                             previous_casebook=previous_casebook)
    record = {
        'source_head_claimed': plan['source_head'],
        'evidence_status': evidence['status'],
        'evidence_obstructions': evidence['obstructions'],
        'target': target,
        'repair_status': 'NO_DATA_NOT_RUN',
        'source_restored': None,
        'source_signature_unchanged': None,
        'imports_unchanged': None,
        'ci_certified': False,
        'source_test_merge_tree_certified': False,
        'github_write_performed': False,
    }
    def save():
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'repair_preflight_receipt.json').write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + '\n')
        return record

    if evidence['status'] != 'SOURCE_OBSERVATION_READY':
        record['repair_status'] = 'OBSTRUCTION_IN_FULL_SOURCE_OR_DEPENDENCIES'
        return save()
    checked = evidence['sources'].get(target)
    original = {x['path']: x for x in evidence['changed_targets']}
    if target not in original or checked is None:
        record['repair_status'] = 'TARGET_OUTSIDE_EXACT_CHANGED_SOURCE_SET'
        return save()
    if not acknowledged_isolated:
        record['repair_status'] = 'READ_ONLY_FULL_SOURCE_PREFLIGHT_COMPLETE'
        return save()
    identifiers = {'field_missing', 'unresolved_identifier'}
    if (any(e['kind'] in identifiers for e in evidence['ci_errors'])
            and not plan.get('api_probes')):
        record['repair_status'] = 'PINNED_API_PROBE_REQUIRED_FOR_IDENTIFIER_ERROR'
        return save()
    if not 1 <= max_iterations <= 5:
        raise RepairPreflightObstruction('iteration budget must be 1..5')
    source = root / target
    baseline = (output_dir / 'full_source' / checked['snapshot_relative']).read_bytes()
    if sha256(source.read_bytes()) != checked['source_sha256'] or source.read_bytes() != baseline:
        raise RepairPreflightObstruction('source changed after full-source scan')
    if runner is None:
        from scripts.kuuos_lean_mcp_repair_loop_v1 import mcp_tactic_provider, run_loop
        runner = run_loop
        if provider is None:
            provider = mcp_tactic_provider
    if provider is None:
        provider = lambda _src, _obs: {'status': 'NO_PROVIDER'}

    result = runner(root=root, rel_file=target, output_dir=output_dir / 'candidate',
                    expected_sha256=original[target]['sha256'], provider=provider,
                    max_iterations=max_iterations)
    record['local_repair_receipt'] = result
    record['source_restored'] = source.read_bytes() == baseline
    if not record['source_restored']:
        record['repair_status'] = 'ROLLBACK_OBSTRUCTION'
        return save()
    if result.get('status') != 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY' or not result.get('source_restored'):
        record['repair_status'] = 'LOCAL_LEAN_CANDIDATE_UNCERTIFIED'
        return save()
    candidate_path = output_dir / 'candidate' / 'candidate.lean'
    if not candidate_path.is_file() or candidate_path.is_symlink():
        record['repair_status'] = 'MISSING_LOCAL_CANDIDATE'
        return save()
    candidate_bytes = candidate_path.read_bytes()
    original_text, candidate_text = baseline.decode('utf-8'), candidate_bytes.decode('utf-8')
    record['candidate_sha256'] = sha256(candidate_bytes)
    record['imports_unchanged'] = imports_of(candidate_text) == imports_of(original_text)
    module = target.removeprefix('formal/').removesuffix('.lean').replace('/', '.')
    a = declarations_of(original_text, module)
    b = declarations_of(candidate_text, module)
    record['source_signature_unchanged'] = [
        (d['kind'], d['name_lexical'], d['signature_sha256']) for d in a
    ] == [(d['kind'], d['name_lexical'], d['signature_sha256']) for d in b]
    record['new_forbidden_constructs'] = any(
        x in candidate_text and x not in original_text
        for x in ('sorry', 'admit', 'axiom', 'unsafe', 'native_decide', 'debug.skipKernelTC')
    )
    if (not record['imports_unchanged'] or
            not record['source_signature_unchanged'] or
            record['new_forbidden_constructs']):
        record['repair_status'] = 'PROOF_INTERFACE_OBSTRUCTION'
        return save()
    record['repair_status'] = 'LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY'
    return save()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project-root', required=True)
    p.add_argument('--plan', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--ci-log')
    p.add_argument('--previous-casebook')
    p.add_argument('--repair-target', required=True)
    p.add_argument('--max-iterations', type=int, default=3)
    p.add_argument('--ack-isolated-checkout', action='store_true')
    args = p.parse_args()
    try:
        plan = json.loads(pathlib.Path(args.plan).read_text())
        ci_log = pathlib.Path(args.ci_log).read_text() if args.ci_log else None
        record = gate_repair(
            root=pathlib.Path(args.project_root), plan=plan,
            output_dir=pathlib.Path(args.output_dir), target=args.repair_target,
            acknowledged_isolated=args.ack_isolated_checkout, ci_log=ci_log,
            max_iterations=args.max_iterations,
            previous_casebook=(pathlib.Path(args.previous_casebook)
                               if args.previous_casebook else None),
        )
    except (OSError, EvidenceObstruction, ValueError, UnicodeError) as exc:
        print('KUUOS FULLSOURCE REPAIR BLOCKED: ' + str(exc))
        return 2
    print(json.dumps({k: v for k, v in record.items() if k != 'local_repair_receipt'},
                     ensure_ascii=False))
    return 0 if record['repair_status'] in (
        'READ_ONLY_FULL_SOURCE_PREFLIGHT_COMPLETE',
        'LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY',
    ) else 1


if __name__ == '__main__':
    raise SystemExit(main())
