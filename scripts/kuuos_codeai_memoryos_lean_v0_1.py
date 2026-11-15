#!/usr/bin/env python3
"""Opt-in additive CodeAI entrypoint: recall -> proposals -> Lean -> MCP -> record.

Wraps the existing v1.104-family runner without changing it or any Lean source.
Independent CI remains a separate last stage. Does not write Git refs or call
paid models. Persistent repository admission is a separate GitHub-MCP action.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import importlib
import inspect
import json
import os
from pathlib import Path
import re
from typing import Any

from runtime import kuuos_codeai_memoryos_lean_repair_v0_1 as memory


def capture(directory: Path, bindings: dict[str,dict[str,Any]],
            evidence: dict[str,Any]) -> list[dict[str,Any]]:
    """Read complete per-candidate logs, not the 40-line portfolio excerpts."""
    portfolio=json.loads((directory/'portfolio.json').read_text())
    if portfolio.get('source_restored') is not True:
        raise ValueError('source restoration is not verified')
    if portfolio.get('git_write_performed') is True:
        raise ValueError('unexpected Git mutation in proposal experiment')
    rows=[];seen=set()
    for candidate in portfolio['candidates']:
        name=candidate['variant']
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+',name) or name in seen:
            raise ValueError('unsafe or duplicate candidate identity')
        seen.add(name)
        if name not in bindings:raise ValueError('missing candidate binding')
        binding=bindings[name]
        if binding['source_head']!=portfolio['source_head'] or binding['source_tree']!=portfolio['source_tree']:
            raise ValueError('CodeAI source HEAD/tree mismatch')
        path=directory/(name+'.log')
        if path.is_symlink():raise ValueError('untrusted log symlink')
        complete=path.is_file()
        text=path.read_text() if complete else ''
        if complete and hashlib.sha256(text.encode()).hexdigest()!=candidate.get('log_sha256'):
            raise ValueError('compiler log digest mismatch')
        ev={**deepcopy(evidence),'portfolio_digest':memory.digest(portfolio),
            'codeai_receipt':candidate.get('codeai_receipt'),
            'reported_status':candidate.get('status'),'log_sha256':candidate.get('log_sha256'),
            'stage':'direct_lean','mcp_status':'NO_DATA','independent_ci_status':'NO_DATA'}
        rows.append(memory.observe(binding,candidate_blob=candidate['candidate_blob'],
                    variant=name,diagnostic=text,exit_code=candidate.get('exit_code'),
                    olean_exists=candidate.get('olean_exists'),evidence=ev,
                    diagnostic_complete=complete))
    return rows


def _save(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as out:
        json.dump(value,out,ensure_ascii=False,indent=2,sort_keys=True);out.write('\n')


def run(generator_name: str, history: Path, output: Path,
        retry_reason: str | None = None) -> int:
    if not re.fullmatch(r'scripts\.kuuos_v\d+_codeai_[a-z0-9_]+',generator_name):
        raise ValueError('only an explicit repository CodeAI generator is accepted')
    if output.exists():raise ValueError('append-only evidence output already exists')
    records=memory.load(history)  # missing/corrupt memory is not silently ignored
    generator=importlib.import_module(generator_name)
    core=importlib.import_module('scripts.kuuos_v1104_codeai_four_cocycle_v1')
    scanner=importlib.import_module('scripts.check_kuuos_lean_mcp_fullsource_v1')
    original_main=core.main
    output.mkdir(parents=True)
    report={'generator':generator_name,'memory_records':len(records),
            'memory_status':'READ','independent_ci_certified':False,
            'git_write_performed':False,'status':'NOT_RUN'}

    def memory_main() -> int:
        original_factory=core.proposals
        head,branch,tree=core.require_event()
        core.require_pins(core.ROOT)
        manifest=(core.ROOT/'lake-manifest.json').read_bytes()
        runner=(Path(inspect.getfile(core)).read_bytes()+
                Path(inspect.getfile(generator)).read_bytes())
        base={
            'repository':core.REPO,'source_head':head,'source_tree':tree,
            'target':core.TARGET,'lean':(core.ROOT/'lean-toolchain').read_text().strip(),
            'mathlib':next(p['rev'] for p in json.loads(manifest)['packages'] if p['name']=='mathlib'),
            'manifest_sha256':hashlib.sha256(manifest).hexdigest(),
            'runner_sha256':hashlib.sha256(runner).hexdigest(),
            'imports_sha256':None,'signatures_sha256':None,
            'flags':['-DwarningAsError=true','-Dweak.sorryAsError=true'],
        }
        bindings={}

        def remembered_factory() -> dict[str,str]:
            advice=memory.recall(records,base)
            _save(output/'before_generation.json',advice)
            # A new provider may consume this context explicitly. Legacy static
            # portfolios still receive exact replay filtering, never fake learning.
            hook=getattr(generator,'candidates_with_memory',None)
            sources=hook(deepcopy(advice)) if callable(hook) else original_factory()
            if not isinstance(sources,dict):raise ValueError('invalid candidate factory result')
            accepted={};decisions={}
            for name,source in sources.items():
                if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+',name) or not isinstance(source,str):
                    raise ValueError('candidate source/name invalid')
                binding={**base,
                    'imports_sha256':memory.digest(scanner.imports_of(source)),
                    'signatures_sha256':memory.digest([
                        (d['kind'],d['name_lexical'],d['signature_sha256'])
                        for d in scanner.declarations_of(source,core.MODULE)])}
                decision=memory.guard(records,binding,memory.git_blob(source.encode()),retry_reason=retry_reason)
                decisions[name]=decision;bindings[name]=binding
                if decision['decision']!='BLOCK_EXACT_FAILED':accepted[name]=source
            report['decisions']=decisions
            _save(output/'candidate_replay_decisions.json',decisions)
            if not accepted:
                report['status']='REGENERATE_REQUIRED'
                raise ValueError('all exact candidates previously failed; generate new candidates or give explicit retry reason')
            return accepted

        core.proposals=remembered_factory
        try:
            result=original_main()  # unchanged CodeAI -> direct Lean -> actual MCP
            evidence={'run_id':int(os.environ['GITHUB_RUN_ID']),
                      'run_attempt':int(os.environ.get('GITHUB_RUN_ATTEMPT','1')),
                      'generator':generator_name,'job_id':None,'artifact_id':None}
            captured=capture(core.OUT,bindings,evidence)
            for row in captured:
                memory.append(output/'observations',row)
            report['recorded_candidates']=len(captured)
            # The earlier runner may return 0 merely for experiment completion.
            # Never promote that to successful proof or a successful MCP gate.
            mcp=json.loads((core.MCP_OUT/'receipt.json').read_text())
            local_green=(mcp.get('source_head')==head and mcp.get('mcp_success') is True
                         and mcp.get('mcp_errors')==0 and mcp.get('second_direct_exit')==0
                         and mcp.get('second_direct_success') is True
                         and mcp.get('source_restored') is True)
            report['status']='LOCAL_GREEN_REQUIRES_INDEPENDENT_CI' if local_green else 'LOCAL_UNCERTIFIED'
            return result if result else (0 if local_green else 4)
        finally:
            core.proposals=original_factory

    core.main=memory_main
    try:
        return generator.main()
    except Exception as exc:
        report['obstruction']=type(exc).__name__+': '+str(exc)
        if report['status']=='NOT_RUN':report['status']='MEMORY_OR_EXECUTION_OBSTRUCTION'
        raise
    finally:
        core.main=original_main
        _save(output/'receipt.json',report)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generator',required=True)
    parser.add_argument('--history',type=Path,default=Path('memoryos/lean_repairs/v0_1'))
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--retry-reason')
    args=parser.parse_args()
    return run(args.generator,args.history,args.output,args.retry_reason)

if __name__=='__main__':raise SystemExit(main())
