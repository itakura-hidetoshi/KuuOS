"""Same-run CI evidence comparison for v0.25. Not an execution signature.
Trust the workflow, runner and artifact transport; never grant production authority.
"""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from run_actual_v025 import LEAN_SHA, MANIFEST_SHA, NEW

REPO='itakura-hidetoshi/KuuOS'
GROUPS=(('protocol',266),('actual_v025',3))
def require(ok,reason):
    if not ok:raise ValueError(reason)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read_json(path):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'DUPLICATE_KEY');out[k]=v
        return out
    def bad(_):raise ValueError('NONFINITE')
    return json.loads(path.read_bytes().decode('utf-8',errors='strict'),object_pairs_hook=unique,parse_constant=bad)
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(root,job):
    env=os.environ
    require(env.get('GITHUB_ACTIONS')=='true' and env.get('GITHUB_EVENT_NAME')=='pull_request','CI_CONTEXT_REQUIRED')
    require(env.get('GITHUB_REPOSITORY')==REPO and env.get('GITHUB_JOB')==job,'CI_IDENTITY')
    p=read_json(Path(env['GITHUB_EVENT_PATH']))['pull_request'];head,base,merge=p['head']['sha'],p['base']['sha'],env['GITHUB_SHA']
    require(p['head']['repo']['full_name']==p['base']['repo']['full_name']==REPO and p['base']['ref']=='main','CI_REPOSITORY_OR_BASE')
    require(all(re.fullmatch(r'[0-9a-f]{40}',s) for s in (head,base,merge)),'CI_SHA')
    def git(*a):
        p=subprocess.run(['git','-C',str(root),*a],capture_output=True,timeout=30)
        require(p.returncode==0,'CHECKOUT_UNAVAILABLE');return p.stdout.decode('utf-8').strip()
    require(git('rev-parse','HEAD')==merge and git('rev-parse','HEAD^1')==base and git('rev-parse','HEAD^2')==head,'CI_CHECKOUT')
    require(not git('status','--porcelain','--untracked-files=no'),'TRACKED_SOURCE_DRIFT')
    tree=git('rev-parse',head+'^{tree}');require(tree==git('rev-parse',merge+'^{tree}'),'MERGE_TREE_MISMATCH')
    run,attempt=env['GITHUB_RUN_ID'],env['GITHUB_RUN_ATTEMPT']
    require(all(re.fullmatch(r'[1-9][0-9]*',x) for x in (run,attempt)),'RUN_ID')
    return {'repository':REPO,'pr':p['number'],'run_id':run,'attempt':attempt,'head':head,'base':base,'merge':merge,'tree':tree,'job':job}
def result(directory):
    receipt=directory/'receipt.json';r=read_json(receipt)
    require(r.get('classification')=='SYNTHETIC_ONLY' and r.get('production_status')=='HOLD' and r.get('mode')=='real' and r.get('status')=='ACTUAL_SYNTHETIC_IPC_MATCHED' and r.get('actual_lean_positive_executed') is True,'RECEIPT_SCOPE')
    require(type(r.get('exit_code')) is int and r['exit_code']==0 and r.get('obstructions')==[],'RECEIPT_FAILURE')
    require(r.get('manifest_sha256')==MANIFEST_SHA and r.get('lean_binary_sha256')==LEAN_SHA,'RECEIPT_PINS')
    require((r.get('base_files_checked'),r.get('predecessor_files_checked'),r.get('new_sources_checked'))==(23,19,len(NEW)),'SOURCE_COUNTS')
    require(type(r.get('groups')) is list and len(r['groups'])==len(GROUPS),'GROUP_COUNT')
    logs={}
    for rec,(name,n) in zip(r['groups'],GROUPS):
        require(rec.get('group')==name and rec.get('matched') is True and type(rec.get('exit_code')) is int and rec['exit_code']==0 and rec.get('expected_count')==rec.get('observed_count')==n,'GROUP_FAILURE:'+name)
        raw=(directory/(name+'.log')).read_bytes();require(sha(raw)==rec.get('log_sha256'),'LOG_DIGEST:'+name)
        s=raw.decode('utf-8',errors='strict');rows=re.findall(r'^(test_\S+ \([^\r\n]+\)) \.\.\. ok\r?$',s,re.M)
        require(re.findall(r'^Ran (\d+) tests? in ',s,re.M)==[str(n)] and len(rows)==len(set(rows))==n and re.search(r'^OK\s*\Z',s,re.M) is not None and not re.search(r'\b(?:skipped|expected failure|unexpected success)\b',s,re.I),'LOG_RESULT:'+name)
        logs[name]=sha(raw)
    return {'receipt_sha256':sha(receipt.read_bytes()),'log_sha256':logs,'lean_binary_sha256':LEAN_SHA,'total_tests':269}
def envelope(directory,ident):
    return {'schema':'kuuos.verifyos.v025.ci-evidence','identity':ident,'classification':'SYNTHETIC_ONLY','production_status':'HOLD','result':result(directory)}
def prior(directory,ident):
    expected=envelope(directory,{**ident,'job':'sandbox'})
    require(canon(read_json(directory/'ci_evidence.json'))==canon(expected),'SANDBOX_EVIDENCE_MISMATCH')
    return expected

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('preflight','seal','verify-prior'));p.add_argument('--repo',type=Path,required=True);p.add_argument('--job',choices=('sandbox','independent'),required=True);p.add_argument('--evidence',type=Path);p.add_argument('--prior',type=Path);a=p.parse_args()
    try:
        ident=identity(a.repo,a.job)
        if a.action=='preflight':out={'identity':ident}
        elif a.action=='verify-prior':
            require(a.job=='independent' and a.evidence is not None,'PRIOR_ARGUMENTS');out=prior(a.evidence,ident)
        else:
            require(a.evidence is not None,'EVIDENCE_REQUIRED');out=envelope(a.evidence,ident)
            if a.job=='independent':require(a.prior is not None,'PRIOR_REQUIRED');prior(a.prior,ident)
            with (a.evidence/'ci_evidence.json').open('xb') as f:f.write(canon(out))
        print(json.dumps({'status':'CI_EVIDENCE_CHECKED_ONLY','production_status':'HOLD','result':out},sort_keys=True));return 0
    except Exception as e:print(json.dumps({'status':'HOLD','production_status':'HOLD','reason':str(e)},sort_keys=True));return 2
if __name__=='__main__':sys.exit(main())
