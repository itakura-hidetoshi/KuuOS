#!/usr/bin/env python3
"""Synthetic-only, append-only integration runner. No repository mutation or CI dispatch."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'manifest.json'
M=json.loads(MANIFEST.read_bytes())

def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def checked_bytes(root,name,digest,fn):
    p=root/name
    if not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError('SOURCE_MISSING_OR_UNSAFE:'+name)
    raw=p.read_bytes()
    if fn(raw)!=digest: raise ValueError('SOURCE_MISMATCH:'+name)
    return raw

def protocol_env(roots):
    env=os.environ.copy()
    env['PYTHONPATH']=os.pathsep.join(str(p) for p in roots)
    env['PYTHONDONTWRITEBYTECODE']='1'
    return env

def run_group(name,cwd,env,modules,expected,logdir):
    argv=[sys.executable,'-B','-W','error::ResourceWarning','-m','unittest','-v',*modules]
    p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1200)
    raw=p.stdout; (logdir/(name+'.log')).write_bytes(raw)
    sys.stdout.buffer.write(raw);sys.stdout.flush()
    s=raw.decode('utf-8',errors='replace')
    count=re.findall(r'^Ran (\d+) tests? in ',s,re.M)
    ok=(p.returncode==0 and count==[str(expected)] and re.search(r'^OK\s*$',s,re.M) is not None
        and re.search(r'\b(?:skipped|expected failure|unexpected success)\b',s,re.I) is None)
    result={'group':name,'exit_code':p.returncode,'expected_count':expected,'observed_count':int(count[0]) if len(count)==1 else None,'log_sha256':sha(raw),'matched':ok}
    print(json.dumps(result,sort_keys=True),flush=True)
    return result

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--mode',choices=('protocol','real'),required=True)
    a.add_argument('--repo',type=Path);a.add_argument('--lean',type=Path);a.add_argument('--out',type=Path,required=True)
    a.add_argument('--expect-sandbox-receipt',type=Path)
    args=a.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    receipt={'classification':'SYNTHETIC_ONLY','production_status':'HOLD','mode':args.mode,'source_head':M['source_head'],'manifest_sha256':sha(MANIFEST.read_bytes()),'base_files_checked':0,'candidate_files_checked':0,'groups':[],'status':'HOLD','obstructions':[]}
    try:
        src={}
        for name,digest in M['candidate_sha256'].items():
            src[name]=checked_bytes(HERE,name,digest,sha);receipt['candidate_files_checked']+=1
        dirs=sorted(p for p in HERE.iterdir() if p.is_dir() and p.name.startswith('verifyos_v0'))
        tests=sorted(Path(n).stem for n in src if Path(n).name.startswith('test_') and n.endswith('.py') and not n.endswith('_integration.py'))
        if args.mode=='protocol':
            receipt['groups'].append(run_group('local_protocol',HERE,protocol_env(dirs),tests,247,out))
            if all(g['matched'] for g in receipt['groups']):receipt['status']='PROTOCOL_ONLY_MATCHED'
            else:receipt['obstructions'].append('PROTOCOL_TEST_FAILURE')
        else:
            base={};root=args.repo.resolve() if args.repo else None
            if root is None or not root.is_dir():receipt['obstructions'].append('EXACT_REPOSITORY_CHECKOUT_REQUIRED')
            else:
                for name,digest in M['base_git_blobs'].items():
                    try:
                        raw=checked_bytes(root,name,digest,blob)
                        if name in M['lean_sha256'] and sha(raw)!=M['lean_sha256'][name]:raise ValueError('LEAN_SOURCE_SHA256_MISMATCH:'+name)
                        base[name]=raw;receipt['base_files_checked']+=1
                    except ValueError as e:receipt['obstructions'].append(str(e))
            lean=args.lean if args.lean else shutil.which('lean')
            if not lean:receipt['obstructions'].append('PINNED_LEAN_UNAVAILABLE')
            else:
                lean=Path(lean).resolve()
                if not lean.is_file() or not os.access(lean,os.X_OK):receipt['obstructions'].append('PINNED_LEAN_UNAVAILABLE')
                else:
                    # Executable must be provisioned by the trusted CI/bootstrap or user.
                    p=subprocess.run([str(lean),'--version'],capture_output=True,timeout=30)
                    version=p.stdout.decode('utf-8',errors='replace').strip()
                    receipt['lean_version']=version;receipt['lean_binary_sha256']=sha(lean.read_bytes())
                    if p.returncode or p.stderr or version!=M['lean_version']:receipt['obstructions'].append('LEAN_VERSION_MISMATCH')
            if args.expect_sandbox_receipt:
                prior=json.loads(args.expect_sandbox_receipt.read_bytes())
                if not (prior.get('status')=='ACTUAL_SYNTHETIC_INTEGRATION_MATCHED' and prior.get('manifest_sha256')==receipt['manifest_sha256'] and prior.get('source_head')==receipt['source_head'] and prior.get('base_files_checked')==len(M['base_git_blobs']) and prior.get('candidate_files_checked')==len(src) and prior.get('lean_binary_sha256')==receipt.get('lean_binary_sha256') and prior.get('production_status')=='HOLD'):
                    receipt['obstructions'].append('SANDBOX_RECEIPT_MISMATCH')
            if not receipt['obstructions']:
                receipt['groups'].append(run_group('local_protocol',HERE,protocol_env(dirs),tests,247,out))
                if not receipt['groups'][-1]['matched']:raise ValueError('PROTOCOL_TEST_FAILURE')
                with tempfile.TemporaryDirectory(prefix='verifyos-exact-tree-') as work:
                    work=Path(work)
                    for name,raw in base.items():
                        path=work/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
                    for name,raw in src.items():
                        filename=Path(name).name
                        if filename.startswith('kuuos_') and filename.endswith('.py'):target=work/'runtime'/filename
                        elif filename.endswith('_integration.py'):target=work/'tests'/filename
                        else:continue
                        if target.exists():raise ValueError('STAGING_COLLISION:'+str(target))
                        target.write_bytes(raw)
                    env=protocol_env([work,work/'tests']);env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','');env['KUUOS_V024_LEAN_BINARY']=str(lean)
                    receipt['groups'].append(run_group('actual_v017',work,env,['test_kuuos_verifyos_lean_egress_v0_17'],10,out))
                    if not receipt['groups'][-1]['matched']:raise ValueError('ACTUAL_V017_BASELINE_FAILURE')
                    receipt['groups'].append(run_group('actual_v024',work,env,['test_kuuos_verifyos_mcp_bridge_v0_24_integration'],3,out))
                    if not receipt['groups'][-1]['matched']:raise ValueError('ACTUAL_V024_INTEGRATION_FAILURE')
                    for name,raw in base.items():
                        if (work/name).read_bytes()!=raw:raise ValueError('STAGED_BASE_DRIFT:'+name)
                    for name,digest in M['candidate_sha256'].items():checked_bytes(HERE,name,digest,sha)
                    if sha(lean.read_bytes())!=receipt['lean_binary_sha256']:raise ValueError('LEAN_BINARY_DRIFT')
                    receipt['status']='ACTUAL_SYNTHETIC_INTEGRATION_MATCHED'
    except Exception as e:receipt['status']='HOLD';receipt['obstructions'].append(type(e).__name__+':'+str(e))
    receipt['exit_code']=0 if receipt['status'] in ('PROTOCOL_ONLY_MATCHED','ACTUAL_SYNTHETIC_INTEGRATION_MATCHED') else 2
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True),flush=True)
    return receipt['exit_code']
if __name__=='__main__':sys.exit(main())
