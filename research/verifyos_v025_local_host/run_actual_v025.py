"""Append-only v0.25 candidate runner. All positive tests are synthetic.
The exact v0.24 sources are checked and staged without editing the checkout.
No deployment, private ledger access, MCP registration or production admission.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
OLD='research/verifyos_v024_integration'
MANIFEST_SHA='fc3c4ef23b348784f03a6d863b162e21dccccb9c70d5bcd2607435274bc08f65'
LEAN_SHA='3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf'
NEW={
 'kuuos_verifyos_local_host_v0_25.py':'6201a74e72511ced121343143b33da630792ad6d1f90f9d6a6e2f6a46d319f71',
 'test_kuuos_verifyos_local_host_v0_25.py':'9a29ec72d81f4eb944004f74b2c8f48759f7e22819d5071a5a31dcfde9f158fb',
 'test_kuuos_verifyos_local_host_v0_25_integration.py':'3fbb03f7cde7933350da4c2ce21e162f98e3edc9aeddce515148060c02ee0741',
}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def require(condition,reason):
    if not condition:raise ValueError(reason)
def checked(root,name,digest,fn=sha):
    root=root.resolve();p=root/name
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'SOURCE_MISSING_OR_UNSAFE:'+name)
    raw=p.read_bytes();require(fn(raw)==digest,'SOURCE_MISMATCH:'+name);return raw

def group(name,cwd,paths,modules,count,out,lean=None):
    env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join(str(p) for p in paths);env['PYTHONDONTWRITEBYTECODE']='1'
    if lean is not None:
        env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','');env['KUUOS_V024_LEAN_BINARY']=str(lean)
    p=subprocess.run([sys.executable,'-B','-W','error::ResourceWarning','-m','unittest','-v',*modules],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1200)
    raw=p.stdout;(out/(name+'.log')).write_bytes(raw);sys.stdout.buffer.write(raw);sys.stdout.flush()
    s=raw.decode('utf-8',errors='strict');n=re.findall(r'^Ran (\d+) tests? in ',s,re.M)
    rows=re.findall(r'^(test_\S+ \([^\r\n]+\)) \.\.\. ok\r?$',s,re.M)
    ok=p.returncode==0 and n==[str(count)] and len(rows)==len(set(rows))==count and re.search(r'^OK\s*\Z',s,re.M) is not None and not re.search(r'\b(?:skipped|expected failure|unexpected success)\b',s,re.I)
    result={'group':name,'exit_code':p.returncode,'expected_count':count,'observed_count':int(n[0]) if len(n)==1 else None,'matched':ok,'log_sha256':sha(raw)}
    print(json.dumps(result,sort_keys=True),flush=True);return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',required=True,choices=('protocol','real'));parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--lean',type=Path);parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    r={'classification':'SYNTHETIC_ONLY','production_status':'HOLD','mode':a.mode,'status':'HOLD','groups':[],'obstructions':[],'new_sources_checked':0,'base_files_checked':0,'predecessor_files_checked':0,'actual_lean_positive_executed':False}
    try:
        new={}
        for name,digest in NEW.items():new[name]=checked(HERE,name,digest);r['new_sources_checked']+=1
        oldroot=repo/OLD
        if a.mode=='real':
            path=a.lean or shutil.which('lean')
            lean=Path(path).resolve() if path else None
            if lean is None or not lean.is_file() or not os.access(lean,os.X_OK):r['obstructions'].append('PINNED_LEAN_UNAVAILABLE')
            elif sha(lean.read_bytes())!=LEAN_SHA:r['obstructions'].append('LEAN_BINARY_PIN_MISMATCH')
        manifest=json.loads(checked(oldroot,'manifest.json',MANIFEST_SHA));r['manifest_sha256']=MANIFEST_SHA
        require(len(manifest['base_git_blobs'])==23 and len(manifest['candidate_sha256'])==19,'MANIFEST_COUNT')
        old={}
        for name,digest in manifest['candidate_sha256'].items():old[name]=checked(oldroot,name,digest);r['predecessor_files_checked']+=1
        dirs=sorted({oldroot/Path(n).parent for n in old})
        modules=sorted(Path(n).stem for n in old if Path(n).name.startswith('test_') and n.endswith('.py') and not n.endswith('_integration.py'))
        modules.append('test_kuuos_verifyos_local_host_v0_25')
        if a.mode=='real':
            base={}
            for name,digest in manifest['base_git_blobs'].items():
                raw=checked(repo,name,digest,blob)
                if name in manifest['lean_sha256']:require(sha(raw)==manifest['lean_sha256'][name],'LEAN_SOURCE_PIN:'+name)
                base[name]=raw;r['base_files_checked']+=1
            require(not r['obstructions'],'REAL_PREFLIGHT_HOLD')
            proc=subprocess.run([str(lean),'--version'],capture_output=True,timeout=30)
            require(proc.returncode==0 and not proc.stderr and proc.stdout.decode().strip()==manifest['lean_version'],'LEAN_VERSION_MISMATCH')
            r['lean_binary_sha256']=LEAN_SHA;r['lean_version']=manifest['lean_version']
        r['groups'].append(group('protocol',HERE,[HERE,*dirs],modules,266,out))
        require(r['groups'][-1]['matched'],'PROTOCOL_FAILURE')
        if a.mode=='real':
            with tempfile.TemporaryDirectory(prefix='v025-exact-') as td:
                work=Path(td)
                def put(name,raw):
                    p=work/name;require(not p.exists(),'STAGING_COLLISION:'+str(name));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
                for n,raw in base.items():put(n,raw)
                for n,raw in {**old,**new}.items():
                    f=Path(n).name
                    if f.startswith('kuuos_') and f.endswith('.py'):put('runtime/'+f,raw)
                    elif f.endswith('_integration.py'):put('tests/'+f,raw)
                r['groups'].append(group('actual_v025',work,[work,work/'tests'],['test_kuuos_verifyos_local_host_v0_25_integration'],3,out,lean))
                require(r['groups'][-1]['matched'],'ACTUAL_INTEGRATION_FAILURE')
                require(all((work/n).read_bytes()==raw for n,raw in base.items()),'STAGED_BASE_DRIFT')
            require(sha(lean.read_bytes())==LEAN_SHA,'LEAN_BINARY_DRIFT')
            for n,d in manifest['base_git_blobs'].items():checked(repo,n,d,blob)
            r['actual_lean_positive_executed']=True
        for n,d in manifest['candidate_sha256'].items():checked(oldroot,n,d)
        for n,d in NEW.items():checked(HERE,n,d)
        r['status']='ACTUAL_SYNTHETIC_IPC_MATCHED' if a.mode=='real' else 'PROTOCOL_ONLY_MATCHED'
    except Exception as exc:
        r['status']='HOLD';r['obstructions'].append(type(exc).__name__+':'+str(exc))
    r['exit_code']=0 if r['status']!='HOLD' else 2
    (out/'receipt.json').write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True));return r['exit_code']
if __name__=='__main__':sys.exit(main())
