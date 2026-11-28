"""Additive CI evidence audit for the unmerged v0.24 synthetic integration.

This is not an execution attestation or signature. Trust the GitHub workflow,
runner and artifact transport. Never issue production admission. Read-only
local checkout inspection; no network, GitHub writes or CI dispatch here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MANIFEST_SHA = 'fc3c4ef23b348784f03a6d863b162e21dccccb9c70d5bcd2607435274bc08f65'
RUNNER_SHA = 'bfab76357b28ba3e818aaf8d5231d294ea111d440f1f5d6f48b0e1da5f9c7ff6'
GROUPS = (('local_protocol',247), ('actual_v017',10), ('actual_v024',3))
SCHEMA = 'kuuos.verifyos.v024.ci-evidence.r2'
REPO = 'itakura-hidetoshi/KuuOS'
BASE = 'd1df31cba81423868a21bda9a952b89586b8b87d'
WORKFLOW = '.github/workflows/verifyos-v024-real-integration-r2.yml'
HEX = re.compile(r'[0-9a-f]+\Z')


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def digest_string(s, n):
    return type(s) is str and len(s)==n and HEX.fullmatch(s) is not None


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def read_json(raw):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    def bad(_):
        raise ValueError('NONFINITE_JSON')
    require(type(raw) is bytes and len(raw)<=2_000_000,'JSON_SIZE')
    return json.loads(raw.decode('utf-8', errors='strict'),object_pairs_hook=unique,parse_constant=bad)


def read_file(root, name, limit=16_000_000):
    root=root.resolve(); p=root/name
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'MISSING_OR_UNSAFE:'+name)
    require(p.stat().st_size<=limit,'FILE_SIZE:'+name)
    data=p.read_bytes()
    require(len(data)<=limit,'FILE_SIZE:'+name)
    return data


def source_identity(repo):
    """Check exact observed upstream and candidate bytes, not just a label."""
    repo=repo.resolve(); here=repo/'research/verifyos_v024_integration'
    mraw=read_file(here,'manifest.json'); runner=read_file(here,'run_candidate.py')
    require(sha(mraw)==MANIFEST_SHA,'MANIFEST_PIN'); require(sha(runner)==RUNNER_SHA,'RUNNER_PIN')
    m=read_json(mraw)
    require(m['source_head']==BASE and m['repository']==REPO,'MANIFEST_SOURCE')
    require(len(m['base_git_blobs'])==23 and len(m['candidate_sha256'])==19,'MANIFEST_COUNT')
    entries={}
    for path,expected in m['base_git_blobs'].items():
        raw=read_file(repo,path); require(blob(raw)==expected,'BASE_BLOB:'+path)
        if path in m['lean_sha256']:
            require(sha(raw)==m['lean_sha256'][path],'LEAN_SOURCE_SHA:'+path)
        entries[path]=sha(raw)
    for path,expected in m['candidate_sha256'].items():
        raw=read_file(here,path); require(sha(raw)==expected,'CANDIDATE_SHA:'+path)
        entries['research/verifyos_v024_integration/'+path]=sha(raw)
    for path in ('manifest.json','run_candidate.py','audit_ci_evidence_r2.py','test_audit_ci_evidence_r2.py'):
        entries['research/verifyos_v024_integration/'+path]=sha(read_file(here,path))
    entries[WORKFLOW]=sha(read_file(repo,WORKFLOW))
    return sha(canonical(entries))


def ci_identity(repo, expected_job):
    """Require the actual PR merge checkout and identical submitted/merge trees.

    Uses git only to read the local Actions checkout, never to access the remote.
    A stale base or a checkout without both parents is a HOLD.
    """
    env=os.environ
    require(env.get('GITHUB_ACTIONS')=='true' and env.get('GITHUB_EVENT_NAME')=='pull_request','CI_CONTEXT_REQUIRED')
    require(env.get('GITHUB_REPOSITORY','').lower()==REPO.lower(),'CI_REPOSITORY')
    require(env.get('GITHUB_JOB')==expected_job,'CI_JOB')
    event=read_json(Path(env['GITHUB_EVENT_PATH']).read_bytes()); pr=event['pull_request']
    head,base,merge=pr['head']['sha'],pr['base']['sha'],env.get('GITHUB_SHA')
    require(all(digest_string(v,40) for v in (head,base,merge)),'CI_SHA')
    require(base==BASE,'CI_BASE_NOT_FIXED_PREDECESSOR')
    require(pr['head']['repo']['full_name'].lower()==REPO.lower(),'CI_HEAD_REPOSITORY')
    require(pr['base']['repo']['full_name'].lower()==REPO.lower(),'CI_BASE_REPOSITORY')
    require(type(pr['number']) is int and pr['number']>0,'CI_PR')
    def git(*args):
        proc=subprocess.run(['git','-C',str(repo),*args],capture_output=True,timeout=30,check=False)
        require(proc.returncode==0,'LOCAL_CHECKOUT_UNAVAILABLE')
        return proc.stdout.decode('ascii',errors='strict').strip()
    require(git('rev-parse','HEAD')==merge,'CI_CHECKOUT_SHA')
    require(git('status','--porcelain','--untracked-files=no')=='','CI_TRACKED_SOURCE_DRIFT')
    require(git('rev-parse','HEAD^1')==base and git('rev-parse','HEAD^2')==head,'CI_MERGE_PARENTS')
    tree=git('rev-parse',head+'^{tree}'); merge_tree=git('rev-parse',merge+'^{tree}')
    require(digest_string(tree,40) and tree==merge_tree,'CI_TREE_MISMATCH')
    run=env.get('GITHUB_RUN_ID',''); attempt=env.get('GITHUB_RUN_ATTEMPT','')
    require(run.isascii() and run.isdecimal() and int(run)>0 and attempt.isascii() and attempt.isdecimal() and int(attempt)>0,'CI_RUN')
    return {'repository':REPO,'pr':pr['number'],'run_id':run,'run_attempt':attempt,'head_sha':head,'base_sha':base,
            'test_merge_sha':merge,'source_tree':tree,'test_merge_tree':merge_tree,'job':expected_job}


def audit_result(directory):
    """Verify all three exact group receipts against their actual log bytes."""
    directory=directory.resolve(); receipt_raw=read_file(directory,'receipt.json'); r=read_json(receipt_raw)
    fields={'classification','production_status','mode','source_head','manifest_sha256','base_files_checked',
            'candidate_files_checked','groups','status','obstructions','lean_version','lean_binary_sha256','exit_code'}
    require(type(r) is dict and set(r)==fields,'RECEIPT_SCHEMA')
    require(r['classification']=='SYNTHETIC_ONLY' and r['production_status']=='HOLD' and r['mode']=='real'
            and r['source_head']==BASE and r['manifest_sha256']==MANIFEST_SHA and r['status']=='ACTUAL_SYNTHETIC_INTEGRATION_MATCHED','RECEIPT_SCOPE')
    require(type(r['exit_code']) is int and r['exit_code']==0 and r['obstructions']==[],'RECEIPT_FAILURE')
    require(type(r['base_files_checked']) is int and r['base_files_checked']==23 and type(r['candidate_files_checked']) is int and r['candidate_files_checked']==19,'RECEIPT_SOURCE_COUNTS')
    require(r['lean_version']=='Lean (version 4.30.0-rc2, x86_64-unknown-linux-gnu, commit 3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc, Release)' and digest_string(r['lean_binary_sha256'],64),'RECEIPT_LEAN')
    groups=r['groups']; require(type(groups) is list and len(groups)==len(GROUPS),'GROUP_COUNT')
    hashes={}
    for rec,(name,n) in zip(groups,GROUPS):
        require(type(rec) is dict and set(rec)=={'group','exit_code','expected_count','observed_count','log_sha256','matched'},'GROUP_SCHEMA')
        require(rec['group']==name and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['matched'] is True,'GROUP_FAILURE:'+name)
        require(type(rec['expected_count']) is int and rec['expected_count']==n and type(rec['observed_count']) is int and rec['observed_count']==n,'GROUP_TEST_COUNT:'+name)
        raw=read_file(directory,name+'.log'); h=sha(raw); require(h==rec['log_sha256'],'GROUP_LOG_SHA:'+name)
        s=raw.decode('utf-8',errors='strict')
        passed=re.findall(r'^(test_\S+ \([^\r\n]+\)) \.\.\. ok\r?$',s,re.M)
        require(re.findall(r'^Ran (\d+) tests? in ',s,re.M)==[str(n)] and re.search(r'^OK\s*\Z',s,re.M) is not None
                and re.search(r'\b(?:skipped|expected failure|unexpected success)\b',s,re.I) is None,'GROUP_LOG_RESULT:'+name)
        require(len(passed)==n and len(set(passed))==n,'GROUP_LOG_TEST_ROWS:'+name)
        hashes[name+'.log']=h
    return {'receipt_sha256':sha(receipt_raw),'logs':hashes,'lean_binary_sha256':r['lean_binary_sha256'],'total_tests':sum(n for _,n in GROUPS)}


def envelope(directory, identity, sources):
    require(digest_string(sources,64),'SOURCE_FINGERPRINT')
    return {'schema':SCHEMA,'classification':'SYNTHETIC_ONLY','production_status':'HOLD',
            'identity':identity,'source_fingerprint_sha256':sources,'result':audit_result(directory)}


def verify_prior(directory, current_identity, sources):
    """Trust same-workflow artifact transport; reject stale/missing evidence."""
    expected_id={**current_identity,'job':'sandbox'}
    observed=read_json(read_file(directory,'runner_evidence.json'))
    expected=envelope(directory,expected_id,sources)
    require(canonical(observed)==canonical(expected),'SANDBOX_EVIDENCE_MISMATCH')
    return expected['result']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('preflight','seal','verify-prior'))
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--job',choices=('sandbox','independent'),required=True)
    parser.add_argument('--evidence',type=Path);parser.add_argument('--prior',type=Path)
    a=parser.parse_args()
    try:
        ident=ci_identity(a.repo,a.job); sources=source_identity(a.repo)
        if a.operation=='verify-prior':
            require(a.job=='independent' and a.evidence is not None,'PRIOR_ARGUMENTS')
            result=verify_prior(a.evidence,ident,sources)
        elif a.operation=='seal':
            require(a.evidence is not None,'EVIDENCE_ARGUMENT')
            result=envelope(a.evidence,ident,sources)
            if a.job=='independent':
                require(a.prior is not None,'PRIOR_ARGUMENTS')
                prior=verify_prior(a.prior,ident,sources)
                require(prior['lean_binary_sha256']==result['result']['lean_binary_sha256'],'RUNNER_BINARY_MISMATCH')
            # Append a separate receipt; never overwrite an earlier observation.
            with (a.evidence/'runner_evidence.json').open('xb') as out:out.write(canonical(result))
        else:
            result={'identity':ident,'source_fingerprint_sha256':sources}
        print(json.dumps({'status':'CI_EVIDENCE_CHECKED_ONLY','production_status':'HOLD','result':result},sort_keys=True));return 0
    except Exception as exc:
        print(json.dumps({'status':'HOLD','production_status':'HOLD','reason':str(exc)},sort_keys=True));return 2


if __name__=='__main__':sys.exit(main())
