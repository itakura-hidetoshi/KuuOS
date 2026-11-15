"""Append-only Lean repair observations; MemoryOS advice, CodeAI replay control.

Memory is NOT a Lean kernel, a proof certificate, a model-weight update, or
execution authority. Hashes detect modification, not forged external evidence.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import base64
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any
import zlib

from examples.memoryos_github_external_memory_minimal import (
    GitHubExternalMemoryRecord, compile_context_candidate, validate_record,
)

SCHEMA = 'kuuos-codeai-memoryos-lean-repair-v0.1'
BINDING_FIELDS = (
    'repository', 'source_head', 'source_tree', 'target', 'lean', 'mathlib',
    'manifest_sha256', 'runner_sha256', 'imports_sha256', 'signatures_sha256', 'flags',
)
MAX_LOG_BYTES = 1024 * 1024
ERROR = re.compile(r'\berror(?:\([^\n]*?\))?:', re.I)
PATTERNS = (
    ('dependent_decide', r'Expected type must not contain free variables'),
    ('redundant_tactic', r'tactic does nothing|no goals to be solved'),
    ('namespace_resolution', r'Invalid field|Unknown identifier|unknown constant'),
    ('universe_or_hom', r'universe|synthInstanceFailed|failed to synthesize'),
    ('application_type', r'Application type mismatch|Type mismatch'),
    ('remaining_goals', r'unsolved goals|rfl.*failed|omega could not prove'),
    ('resource_limit', r'timeout|timed out|heartbeats|maximum recursion depth'),
)
LESSONS = {
    'dependent_decide': 'Inspect the full dependent expected type; reduce the index or supply a closed, explicitly typed witness before decide.',
    'redundant_tactic': 'Inspect whether the preceding tactic already closes every goal. Do not disable the warning.',
    'namespace_resolution': 'Check the declaration owner and fully qualified name in the pinned imported source; do not assume dot notation finds an opened sibling namespace.',
    'universe_or_hom': 'Compare source/target universes, Hom instances and endpoint types before changing an instance or annotation.',
    'application_type': 'Compare the complete expected/actual signatures, coercions and equality orientation; inspect upstream failures first.',
    'remaining_goals': 'Preserve every goal. Distinguish contradictory finite cases from required equalities; an error-count reduction is not proof completion.',
    'resource_limit': 'A resource limit is inconclusive. Inspect case growth and cached dependencies before increasing a bounded budget.',
    'unclassified': 'NO_DATA: retain the full diagnostic and inspect the pinned source; no repair cause has been established.',
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def _hex(value: Any, length: int) -> bool:
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{'+str(length)+'}', value) is not None


def _binding(value: Mapping[str, Any], *, complete: bool = False) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError('binding must be a mapping')
    result = {key: deepcopy(value.get(key)) for key in BINDING_FIELDS}
    if complete and any(v is None or v == '' or v == [] for v in result.values()):
        raise ValueError('NO_DATA: incomplete exact context')
    for key in ('source_head', 'source_tree', 'mathlib'):
        if result[key] is not None and not _hex(result[key], 40):
            raise ValueError('invalid context SHA: ' + key)
    for key in ('manifest_sha256','runner_sha256','imports_sha256','signatures_sha256'):
        if result[key] is not None and not _hex(result[key],64):
            raise ValueError('invalid context digest: ' + key)
    if result['repository'] is not None and not re.fullmatch(r'[\w.-]+/[\w.-]+', str(result['repository'])):
        raise ValueError('invalid repository')
    if result['target'] is not None:
        p=Path(str(result['target']))
        if p.is_absolute() or '..' in p.parts or not str(p).startswith('formal/') or p.suffix!='.lean':
            raise ValueError('invalid Lean target')
    if result['flags'] is not None and (not isinstance(result['flags'],list) or not all(isinstance(x,str) for x in result['flags'])):
        raise ValueError('compiler flags must be a list of strings')
    return result


def observe(binding: Mapping[str, Any], *, candidate_blob: str, variant: str,
            diagnostic: str, exit_code: int | None, olean_exists: bool | None,
            evidence: Mapping[str, Any], diagnostic_complete: bool = True,
            related_ids: Sequence[str] = ()) -> dict[str, Any]:
    """Record direct Lean output only; MCP/CI success cannot be inferred here."""
    bound = _binding(binding)
    if not _hex(candidate_blob,40) or not isinstance(variant,str) or not variant:
        raise ValueError('candidate identity missing')
    if not isinstance(diagnostic,str) or len(diagnostic.encode()) > MAX_LOG_BYTES:
        raise ValueError('diagnostic missing or exceeds evidence budget')
    if any(not _hex(x,64) for x in related_ids):
        raise ValueError('invalid related observation id')
    families=[name for name,pattern in PATTERNS if re.search(pattern,diagnostic,re.I)]
    has_error=bool(ERROR.search(diagnostic)) or 'sorryAx' in diagnostic
    outcome='inconclusive'
    if diagnostic_complete is True and type(exit_code) is int:
        if exit_code==0 and olean_exists is True and not has_error:
            outcome='direct_success'
        elif exit_code>0 and has_error and 'resource_limit' not in families:
            outcome='direct_failure'
    raw=diagnostic.encode()
    row={
        'schema':SCHEMA, 'binding':bound, 'candidate_blob':candidate_blob,
        'variant':variant, 'stage':'direct_lean', 'outcome':outcome,
        'exit_code':exit_code, 'olean_exists':olean_exists,
        'diagnostic_complete':diagnostic_complete,
        'diagnostic_sha256':hashlib.sha256(raw).hexdigest(),
        'diagnostic_zlib_base64':base64.b64encode(zlib.compress(raw)).decode(),
        'diagnostic_bytes':len(raw), 'families':families or ['unclassified'],
        'cause_status':'inferred', 'related_ids':sorted(set(related_ids)),
        'evidence':deepcopy(dict(evidence)),
        'error_fingerprint':digest({'binding':bound,'full_diagnostic':diagnostic}),
        'integrity_scope':'content_digest_not_external_authentication',
        'independent_ci_certified':False, 'proof_authority':False,
        'git_write_authority':False, 'memory_content_is_untrusted_data':True,
    }
    row['id']=digest(row)
    return row


def diagnostic(row: Mapping[str, Any]) -> str:
    try:
        packed=base64.b64decode(row['diagnostic_zlib_base64'],validate=True)
        obj=zlib.decompressobj()
        raw=obj.decompress(packed,MAX_LOG_BYTES+1)
        if len(raw)>MAX_LOG_BYTES or obj.unconsumed_tail or not obj.eof or obj.unused_data:
            raise ValueError('diagnostic compressed stream/budget invalid')
        if len(raw)!=row['diagnostic_bytes'] or hashlib.sha256(raw).hexdigest()!=row['diagnostic_sha256']:
            raise ValueError('diagnostic evidence digest mismatch')
        return raw.decode('utf-8')
    except (KeyError,TypeError,UnicodeError,zlib.error) as exc:
        raise ValueError('invalid diagnostic evidence') from exc


def validate(row: Mapping[str, Any]) -> None:
    if not isinstance(row,Mapping) or row.get('schema')!=SCHEMA:
        raise ValueError('invalid repair memory schema')
    payload={k:v for k,v in row.items() if k!='id'}
    if row.get('id')!=digest(payload):
        raise ValueError('repair memory was modified')
    rebuilt=observe(row['binding'],candidate_blob=row['candidate_blob'],variant=row['variant'],
                    diagnostic=diagnostic(row),exit_code=row['exit_code'],olean_exists=row['olean_exists'],
                    evidence=row['evidence'],diagnostic_complete=row['diagnostic_complete'],
                    related_ids=row['related_ids'])
    if canonical(rebuilt)!=canonical(row):
        raise ValueError('derived memory status or authority differs from raw evidence')


def append(directory: Path, row: Mapping[str, Any]) -> Path:
    """Immutable content-addressed record; atomic no-replace publication."""
    validate(row)
    directory.mkdir(parents=True,exist_ok=True)
    path=directory/(row['id']+'.json')
    raw=(canonical(row)+'\n').encode()
    if path.is_symlink():
        raise ValueError('memory symlink refused')
    fd,tmp=tempfile.mkstemp(prefix='.pending-',dir=directory)
    try:
        with os.fdopen(fd,'wb') as out:
            out.write(raw);out.flush();os.fsync(out.fileno())
        try:os.link(tmp,path)
        except FileExistsError:
            if path.is_symlink() or path.read_bytes()!=raw:
                raise ValueError('immutable record conflict')
    finally:
        Path(tmp).unlink(missing_ok=True)
    return path


def load(directory: Path) -> list[dict[str, Any]]:
    if not directory.is_dir():
        raise ValueError('NO_DATA: memory directory missing')
    records={}
    for path in sorted(directory.iterdir()):
        if not (path.name.endswith('.json') or path.name.endswith('.json.gz')):
            continue
        if path.is_symlink():raise ValueError('memory symlink refused')
        try:
            if path.name.endswith('.json.gz'):
                dec=zlib.decompressobj(31)
                raw=dec.decompress(path.read_bytes(),4*MAX_LOG_BYTES+1)
                if len(raw)>4*MAX_LOG_BYTES or not dec.eof or dec.unconsumed_tail or dec.unused_data:
                    raise ValueError('invalid compressed seed budget')
                if path.name!='seed-'+hashlib.sha256(raw).hexdigest()+'.json.gz':
                    raise ValueError('seed bundle content digest mismatch')
                rows=json.loads(raw)
                if not isinstance(rows,list) or len(rows)>500:
                    raise ValueError('invalid seed record list')
            else:
                rows=[json.loads(path.read_text())]
            for row in rows:
                validate(row)
                if path.name.endswith('.json') and path.name!=row['id']+'.json':
                    raise ValueError('record filename mismatch')
                records[row['id']]=row
        except (OSError,TypeError,KeyError,zlib.error) as exc:
            raise ValueError('invalid journal record: '+str(path)) from exc
    return [records[key] for key in sorted(records)]


def memoryos_context(row: Mapping[str, Any]) -> dict[str, Any]:
    """Call the existing MemoryOS external-pointer validator and compiler."""
    validate(row)
    b=row['binding'];run=row['evidence'].get('run_id')
    pointer=GitHubExternalMemoryRecord(
        memory_id='leanrepair_'+row['id'],memory_kind='repair_lineage_memory',
        created_at=str(row['evidence'].get('observed_at','NO_DATA')),
        source_system='github',repository=b['repository'],ref_type='workflow_run',
        ref=str(run) if run is not None else 'NO_DATA',commit_sha=b['source_head'],
        path=b['target'],url=f"https://github.com/{b['repository']}/actions/runs/{run}" if run else None,
        summary=f"{row['variant']}: {row['outcome']}; cause is inferred, not theorem authority",
        authority='external_pointer_only',uncertainty='high',
    )
    issues=validate_record(pointer)
    if issues:raise ValueError('MemoryOS refused: '+repr(issues))
    return compile_context_candidate(pointer)


def recall(records: Sequence[Mapping[str, Any]], binding: Mapping[str, Any]) -> dict[str, Any]:
    query=_binding(binding);items=[]
    for row in sorted(records,key=lambda r:r['id']):
        validate(row)
        if row['binding']['repository']!=query['repository']:
            continue
        mismatches=[key for key in BINDING_FIELDS
                    if not query[key] or not row['binding'][key] or query[key]!=row['binding'][key]]
        items.append({'id':row['id'],'match':'exact' if not mismatches else 'advisory_only',
                      'mismatches':mismatches,'outcome':row['outcome'],
                      'families':row['families'],'cause_status':'inferred',
                      'lessons':[LESSONS[x] for x in row['families']],
                      'memoryos':memoryos_context(row)})
    return {'schema':SCHEMA,'items':items,'context_digest':digest(query),
            'proof_authority':False,'memory_is_instructions':False,
            'must_reverify':['direct_lean','real_lean_mcp','independent_ci']}


def guard(records: Sequence[Mapping[str, Any]], binding: Mapping[str, Any],
          candidate_blob: str, *, retry_reason: str | None = None) -> dict[str, Any]:
    """CodeAI owns replay suppression; MemoryOS merely supplied observations."""
    if retry_reason is not None and (not isinstance(retry_reason,str) or not retry_reason.strip()):
        raise ValueError('explicit retry requires a nonempty reason')
    _hex_ok=_hex(candidate_blob,40)
    if not _hex_ok:raise ValueError('invalid candidate blob')
    advice=recall(records,binding)
    exact_ids={x['id'] for x in advice['items'] if x['match']=='exact'}
    matched=[r for r in records if r['id'] in exact_ids and r['candidate_blob']==candidate_blob]
    outcomes={r['outcome'] for r in matched}
    decision='TEST_REQUIRED'
    if {'direct_failure','direct_success'}<=outcomes:decision='CONFLICT_REVERIFY'
    elif 'direct_failure' in outcomes:decision='BLOCK_EXACT_FAILED'
    elif 'direct_success' in outcomes:decision='REVERIFY_NOT_CERTIFIED'
    if retry_reason is not None:decision='EXPLICIT_RETEST'
    return {'decision':decision,'evidence_ids':sorted({r['id'] for r in matched}),
            'retry_reason':retry_reason,'owner':'codeai_replay_guard',
            'proof_authority':False,'merge_authority':False}


def prepare(factory: Callable[[dict[str,Any]], dict[str,str]],
            records: Sequence[Mapping[str,Any]], binding: Mapping[str,Any],
            *, retry_reason: str | None = None) -> tuple[dict[str,str],dict[str,Any]]:
    advice=recall(records,binding)  # strictly before candidate generation
    proposals=factory(deepcopy(advice))
    if not isinstance(proposals,dict):raise ValueError('candidate factory must return a dict')
    accepted={}; decisions={};suppressed=[]
    for name,source in proposals.items():
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+',name) or not isinstance(source,str):
            raise ValueError('invalid candidate name or source')
        result=guard(records,binding,git_blob(source.encode()),retry_reason=retry_reason)
        decisions[name]=result
        if result['decision']=='BLOCK_EXACT_FAILED':suppressed.append(name)
        else:accepted[name]=source
    return accepted,{'advice':advice,'decisions':decisions,'suppressed':sorted(suppressed),
                     'status':'REGENERATE_REQUIRED' if not accepted else 'DIRECT_LEAN_REQUIRED',
                     'proof_authority':False,'independent_ci_certified':False}
