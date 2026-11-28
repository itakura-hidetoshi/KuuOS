#!/usr/bin/env python3
"""R84 R1 candidate verifier. No claim of successful execution.
Run only in the pinned research runner with R83 verified artifacts.
Preserve parent bytes; compile exactly one new module per direct runner.
"""
from __future__ import annotations
import argparse, json, shutil, hashlib, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
FORMAL=HERE/'lean_probes'/'codeai_registry_stream_cache_v1.lean'
TESTS=HERE/'lean_probes'/'codeai_registry_stream_cache_v1_tests.lean'
CONFIG=HERE/'lean_probes'/'R84_candidate_manifest.json'
MODULE='StreamCacheR84'
IMPORT_DIR=Path('artifacts/olean-r84')
IMPORT_MODULE='artifacts.«olean-r84».StreamCacheR84'
SOURCE=MODULE+'.lean'
VIEW='McpCapsuleApplication.lean'
VIEW_TEXT='import '+IMPORT_MODULE+'\n'
CAP='audit-capsule'
MANIFEST='r84-audit-capsule.json'
REPLAY='r84-imported-replay.json'
RECORD='registry-stream-cache-v1.json'
PARENT='parent-r83-receipts'
PARENT_CAP='parent-r83-audit-capsule'
CHECKS={'empty_stream','empty_chunk','finite_stream_exact','chunk_split_exact','complete_trace_length','complete_terminal_bindings','fresh_cache_exact','fresh_frontier_exact','blocked_stream_exact','blocked_pending_suffix','blocked_cache_unchanged','blocked_position_unchanged','blocked_atomic_no_later','none_is_not_empty','actual_stream_cache_exact','actual_stream_hold_and_frontier'}
BOUNDARY=('proof_authority','action_authority','release_authorized','active_policy_changed','semantic_search_complete','complete_transitive_closure','all_repository_dependencies_observed','python_general_correctness_proved','policy_is_refutation','live_main_admission','current_main_certification_transferred','identity_authentication_proved','registry_authentication_proved','unknown_registration_is_refutation','registry_updated','automatic_registration_authority','batch_applied_to_live_registry','registration_correctness_implied_by_readiness','execution_history_order_independent','automatic_recovery_authority','cross_route_replacement_proved','search_of_unlisted_routes_complete','ordered_binding_list_refresh_proved','arbitrary_cache_refresh_proved','general_r77_projection_equality_proved')

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def file_hash(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def config_check():
    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    need(file_hash(CONFIG)=='322d3d56f99701d12eb53bd35350b35060664e82cb010bf95b9466ae2d4ba07c','fixed R84 candidate manifest')
    for item,p in zip(cfg['files'],(FORMAL,TESTS),strict=True):
        need(item['name']==p.name and item['sha256']==file_hash(p) and item['bytes']==p.stat().st_size,'R84 exact source '+p.name)
    import re
    names=cfg['new_theorem_candidates']; refs=cfg['required_direct_references']
    declared=['KuuOSR84.'+n for n in re.findall(r'^theorem ([A-Za-z0-9_]+)',FORMAL.read_text(encoding='utf-8'),re.M)]
    declared_checks=re.findall(r'^\s*\("([a-z0-9_]+)",',TESTS.read_text(encoding='utf-8'),re.M)
    need(declared==names,'R84 source declaration list matches manifest')
    need(len(declared_checks)==len(set(declared_checks))==16 and set(declared_checks)==CHECKS,'R84 source comparison list matches verifier')
    need(len(names)==len(set(names))==14 and set(refs)<=set(names),'R84 declaration inventory')
    need(cfg['expected_comparison_count']==len(CHECKS)==16 and set(cfg['expected_comparison_names'])==CHECKS,'R84 comparison inventory')
    return cfg

def activate():
    global r83,r82,r81,r80,r76,r75,r63,v,root,load,sha,digest,normalize,pin,cfg,fields,files,history,parents
    import check_codeai_olean_registry_checked_chunks_v1_r83 as r83
    r83.activate()
    r82,r81,r80,r76,r75,r63,v=r83.r82,r83.r81,r83.r80,r83.r76,r83.r75,r83.r63,r83.v
    root,load,sha,digest,normalize,fields=r83.root,r83.load,r83.sha,r83.digest,r83.normalize,r83.fields
    cfg=config_check(); pin=cfg['parent']
    files=r83.files+(r83.RECORD,)
    history=r83.history+('parent-r83-raw-replay.json',)
    parents=(*r83.parents[:-2],PARENT_CAP,'capsule','joint-capsule')
    need(str(r81.r66.PINNED_HEAD)==cfg['fixed_scope']['canonical_head'] and str(r81.r66.PINNED_TREE)==cfg['fixed_scope']['canonical_tree'],'R84 historical root')

def copy_file(src,dest):
    need(src.is_file() and not src.is_symlink() and not dest.exists(),'immutable file copy '+str(dest))
    dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dest)
    need(file_hash(src)==file_hash(dest),'copied bytes '+str(dest))

def tree_inventory(path):
    need(path.is_dir() and not path.is_symlink(),'required directory '+str(path))
    inv={}
    for p in path.rglob('*'):
        need(not p.is_symlink(),'symlink in artifact '+str(p))
        if p.is_file(): inv[str(p.relative_to(path))]=(p.stat().st_size,file_hash(p))
        else: need(p.is_dir(),'unexpected artifact node '+str(p))
    return inv

def tree_equal(a,b):
    left,right=tree_inventory(a),tree_inventory(b)
    need(left==right,'exact tree mismatch '+str(a))
    for name in left: compare_file(a/name,b/name)

def copy_tree(a,b,dest):
    tree_equal(a,b);need(not dest.exists(),'existing artifact directory '+str(dest));shutil.copytree(a,dest);tree_equal(a,dest)

def compare_file(a,b):
    need(a.is_file() and b.is_file() and not a.is_symlink() and not b.is_symlink() and a.read_bytes()==b.read_bytes(),'exact file mismatch '+str(a))

def parent_api():
    api=v.cache.api; run=api('actions/runs/'+str(pin['run_id']))
    need(run['id']==pin['run_id'] and run['head_sha']==pin['head'] and run['head_commit']['tree_id']==pin['tree'] and run['run_attempt']==1 and run['status']=='completed' and run['conclusion']=='success','R83 exact parent run')
    for jid,steps in ((pin['sandbox_job_id'],('Verify fixed R83 candidate source hashes','Verify R83 checked registry chunk composition','Actual Lean MCP R83 new declarations and exact prior receipt reuse')),(pin['independent_job_id'],('Verify fixed R83 candidate source hashes','Independently verify R83 checked registry chunk composition'))):
        j=api('actions/jobs/'+str(jid));need(j['id']==jid and j['run_id']==pin['run_id'] and j['head_sha']==pin['head'] and j['status']=='completed' and j['conclusion']=='success' and all(any(s['name']==name and s['status']=='completed' and s['conclusion']=='success' for s in j['steps']) for name in steps),'R83 exact parent job')
    for tag in ('local','independent'):
        aid=pin['artifact_'+tag+'_id']; x=api('actions/artifacts/'+str(aid))
        need(x['id']==aid and x['name']==pin['artifact_'+tag+'_name'] and x['digest']=='sha256:'+pin['artifact_'+tag+'_sha256'] and not x['expired'] and x['workflow_run']['id']==pin['run_id'] and x['workflow_run']['head_sha']==pin['head'],'R83 exact parent artifact')

def admit(a,out,scope,bridge,extension):
    parent_api(); left,right=a.r83_local,a.r83_independent
    d,mp,ind=load(left/'direct.json'),load(left/'mcp.json'),load(right/'independent.json')
    need(d==load(right/'direct.json') and digest(d)==pin['direct_digest'] and digest(mp)==pin['mcp_digest'],'R83 fixed direct and MCP digests')
    need(mp['status']=='R83_REAL_MCP_GREEN' and mp['direct_digest']==pin['direct_digest'] and ind['status']=='R83_INDEPENDENT_CHECKED_CHUNKS_GREEN' and ind['direct_digest']==pin['direct_digest'] and ind['mcp_digest']==pin['mcp_digest'],'R83 independent binding')
    need(ind['mcp_audits']==439 and ind['mcp_new_audits']==12 and ind['mcp_reused_audits']==427 and ind['imported_complete_proofs']==340 and all(ind[k] is True for k in ('parent_bytes_preserved','raw_new_proofs_equal','actual_computation_bytes_equal','raw_type_and_proof_equal','compiled_file_bytes_equal','imported_replay_equal')),'R83 certified counters and byte checks')
    need(d['parent_source_recompiled'] is False and ind['parent_source_recompiled'] is False and d['delta_compilation_count']==ind['independent_delta_compilation_count']==1,'R83 compilation history')
    rows=d['fresh_application']['observations'];need(len(rows)==len({x['name'] for x in rows})==439 and [{'name':x['name'],'axioms':x['axioms']} for x in rows]==mp['audits'],'R83 audit inventory')
    for name in files:
        compare_file(left/name,right/name);copy_file(left/name,out/name)
    rec=load(out/r83.RECORD)
    need(rec['key']==pin['key']==r63.r62.gate.base.portable.seal(rec)['key'] and len(rec['original_routes'])==2 and len(rec['empty_inventory_holds'])==5,'R83 sealed research record')
    need(rec['historical_scope_digest']==r81.SCOPE==digest(scope) and rec['script_bridge_digest']==r81.BRIDGE==digest(bridge) and rec['r69_additive_observation_digest']==r81.EXTENSION==digest(extension),'R83 historical scope')
    need({n:digest(x) for n,x in rec['raw_theorems'].items()}==d['raw_theorem_digests'] and all(d.get(k) is False and rec.get(k) is False for k in BOUNDARY),'R83 raw proofs and authority limits')
    m1,replay1=r83.check_capsule(left,d);m2,replay2=r83.check_capsule(right,d)
    pfiles=[{'name':'CheckedChunksR83.olean','sha256':pin['olean_sha256'],'bytes':pin['olean_bytes']}]
    need(m1==m2 and digest(m1)==pin['manifest_digest'] and replay1==replay2 and digest(replay1)==pin['replay_digest'] and m1['files']==pfiles,'R83 compiled certificate')
    need(d['r82_r1_failure_evidence_digest']==rec['r82_r1_failure_evidence_digest']==ind['r82_r1_failure_evidence_digest']==pin['r1_failure_evidence_digest'],'R83 immutable R82 R1 failure identity')
    coverage=r83.verify_diagnostics(left,d,mp)
    need(digest(coverage)==pin['diagnostics_digest']==ind['diagnostic_coverage_digest'] and mp['reused_audit_count']==427 and mp['new_audit_count']==12 and len(mp['audit_origins'])==439 and mp['audit_capsule_digest']==pin['manifest_digest'] and mp['imported_replay_digest']==pin['replay_digest'] and mp['fresh_full_source_diagnostics'] is True,'R83 diagnostic receipt')
    receipts=out/PARENT;receipts.mkdir()
    for name,src in (('direct.json',left),('mcp.json',left),('independent.json',right)):
        copy_file(src/name,receipts/name)
    for name in ('formal-source.lean','checked-chunks-computation.lean','checked-chunks-computation.json','candidate-manifest.json','historical-scope.json','script-bridge.json','script-observation-bridge-r69.json',r83.SOURCE,r83.VIEW,r83.MANIFEST,r83.REPLAY,'CapsuleObservation.lean','mcp-diagnostic-coverage.json','mcp-diagnostics.json','mcp-diagnostics-warning.json',*r83.history):
        compare_file(left/name,right/name);copy_file(left/name,receipts/name)
    for name,field in (('formal-source.lean','formal_source_sha256'),('checked-chunks-computation.lean','computation_source_sha256'),('candidate-manifest.json','candidate_manifest_sha256')):
        need(file_hash(receipts/name)==rec[field],'R83 source lineage')
    need(load(receipts/'checked-chunks-computation.json')==rec['actual_computations'],'R83 comparison lineage')
    for label,src in (('sandbox',left),('independent',right)):
        obs=load(src/'main-observations.json');r81.r69.observation_pair_valid(scope,obs['before'],obs['after']);copy_file(src/'main-observations.json',receipts/(label+'-main-observations.json'))
    for j,row in enumerate(rows):
        name=f'mcp-verify-{j}.json';raw=load(left/name);val=v.structured(raw);origin=mp['audit_origins'][j]
        need(raw['result']['isError'] is False and val['warnings']==[] and normalize(val['axioms'])==row['axioms']==mp['audits'][j]['axioms'] and row['name']==mp['audits'][j]['name']==origin['name'] and origin['receipt_sha256']==file_hash(left/name),'R83 exact prior MCP '+row['name'])
        copy_file(left/name,receipts/name)
    copy_tree(left/'r82-r1-failure',right/'r82-r1-failure',out/'r82-r1-failure')
    need(digest(load(out/'r82-r1-failure'/'repair-evidence.json'))==pin['r1_failure_evidence_digest'],'R83 failure evidence copy')
    pd82=load(left/r83.PARENT/'direct.json');pd81=load(left/r82.PARENT/'direct.json')
    need(digest(pd82)==r83.pin['direct_digest']==d['parent_direct_digest'] and digest(pd81)==r82.pin['direct_digest']==pd82['parent_direct_digest'],'R83 exact parent direct receipts')
    for folder in ('capsule','joint-capsule'):
        mf=pd81['capsule_manifest' if folder=='capsule' else 'joint_capsule_manifest'];tool=r63.r62.r39 if folder=='capsule' else r63.r62.r45
        need(tool.capsule_files(left/folder)==tool.capsule_files(right/folder)==mf['files'],'R83 base capsule')
        copy_tree(left/folder,right/folder,out/folder);need(file_hash(out/folder/(mf['module']+'.lean'))==mf['source_sha256'],'R83 base source');tool.install(out/folder,mf)
    for folder in r83.parents[:-2]: copy_tree(left/folder,right/folder,out/folder)
    base=[{'name':'RecoveryDualityR62.olean','sha256':r75.PARENT_OLEAN,'bytes':5972832}]
    need(r81.transport.capsule_files(out/r81.BASE_CAP)==base,'R83 recovery base');r81.transport.install(out/r81.BASE_CAP,base)
    for tool,folder,fs in ((r75,r81.R75_CAP,[{'name':'RegistryRecoveryR75.olean','sha256':r76.PARENT_OLEAN,'bytes':236464}]),(r76,r81.R76_CAP,r81.r77.PARENT_FILES),(r81.r77,r81.R77_CAP,r81.r78.PARENT_FILES),(r81.r78,r81.R78_CAP,r81.r79.PARENT_FILES),(r81.r79,r81.R79_CAP,r80.PARENT_FILES),(r80,r81.PARENT_CAP,r81.PARENT_FILES),(r81,r82.PARENT_CAP,[{'name':'FiniteChainR81.olean','sha256':r82.pin['olean_sha256'],'bytes':r82.pin['olean_bytes']}])):
        need(tool.module_files(out/folder)==fs,'R83 dependency module identity '+folder);tool.install_module(out/folder,fs)
    copy_tree(left/r83.CAP,right/r83.CAP,out/PARENT_CAP)
    for tool,folder,fs in ((r82,r83.PARENT_CAP,[{'name':'CheckedChainR82.olean','sha256':r83.pin['olean_sha256'],'bytes':r83.pin['olean_bytes']}]),(r83,PARENT_CAP,pfiles)):
        need(tool.module_files(out/folder)==fs,'R83 exact compiled parent bytes '+folder)
        dest=root/'.lake/build/lib/lean'/tool.IMPORT_DIR;dest.mkdir(parents=True,exist_ok=False)
        for item in fs:copy_file(out/folder/item['name'],dest/item['name'])
        tool.installed_matches(fs)
    for i in range(54,83):
        folder='parent-r'+str(i)+'-receipts';copy_tree(left/folder,right/folder,out/folder)
    for name in r83.history:
        compare_file(left/name,right/name);copy_file(left/name,out/name)
    v.save(out/'parent-r83-raw-replay.json',rec['raw_theorems'])
    return d,mp,rec

def historical_raw(out):
    raw={}
    for name in history:
        x=load(out/name);need(set(raw).isdisjoint(x),'duplicate historical proof');raw.update(x)
    need(len(raw)==340,'R83 full proof count');return raw

def module_files(folder):
    expected={MODULE+'.olean',MODULE+'.olean.server',MODULE+'.olean.private'}
    actual={p.name for p in folder.iterdir()}
    need(actual in ({MODULE+'.olean'},expected),'R84 exact isolated module parts')
    need(all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),'R84 module regular files')
    return [{'name':n,'sha256':file_hash(folder/n),'bytes':(folder/n).stat().st_size} for n in (MODULE+'.olean',MODULE+'.olean.server',MODULE+'.olean.private') if n in actual]

def installed_matches(fs):
    r83.installed_matches([{'name':'CheckedChunksR83.olean','sha256':pin['olean_sha256'],'bytes':pin['olean_bytes']}])
    dest=root/'.lake/build/lib/lean'/IMPORT_DIR
    need(module_files(dest)==fs,'R84 installed module identity')

def direct(a,out):
    scope=r81.r66.observe_historical_scope();bridge=r81.r68.script_bridge(scope);extension=r81.r69.additive_bridge(scope,bridge);before=r81.r69.observe_live_r3(scope)
    for n,x in (('historical-scope.json',scope),('script-bridge.json',bridge),('script-observation-bridge-r69.json',extension)):v.save(out/n,x)
    pd,pm,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding='utf-8'); tests=TESTS.read_text(encoding='utf-8');need(tests.startswith(VIEW_TEXT),'R84 test import boundary')
    for n,p in (('formal-source.lean',FORMAL),('stream-cache-computation.lean',TESTS),('candidate-manifest.json',CONFIG)):copy_file(p,out/n)
    names=sorted(cfg['new_theorem_candidates']);expected=cfg['required_direct_references']
    selected=[{'name':n,'expected_direct_refs':expected.get(n,[])} for n in names]
    # Strip only the test file's self-import, since both files are compiled into a single new module.
    source=formal+'\n'+tests[len(VIEW_TEXT):]+'\n'+r76.observer(out,names)+v.suffix(names)
    cap=out/CAP;cap.mkdir();p=out/SOURCE
    log=r81.run_lean_with_diagnostics(['--root='+str(root),'-o',str(cap/(MODULE+'.olean'))],p,source)
    audit=r81.read_direct_with_dependency_diagnostics(log,selected)
    newraw=r76.raw_audit(log,{x['name']:x for x in audit},names)
    marker='KUUOS_R84_COMPUTE '; values=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    need(len(values)==1 and set(values[0])==CHECKS and all(x is True for x in values[0].values()),'R84 exact 16 comparisons')
    v.save(out/'stream-cache-computation.json',values)
    fs=module_files(cap);dest=root/'.lake/build/lib/lean'/IMPORT_DIR;dest.mkdir(parents=True,exist_ok=False)
    for item in fs:copy_file(cap/item['name'],dest/item['name'])
    installed_matches(fs)
    prior=pd['fresh_application']['observations'];rows=sorted(prior+audit,key=lambda x:x['name']);need(len(rows)==len({x['name'] for x in rows})==453,'R84 accumulated declaration inventory')
    raw=historical_raw(out);need(set(raw).isdisjoint(newraw),'R84 overwrite forbidden');raw.update(newraw);need(len(raw)==354,'R84 complete proof inventory')
    imported=VIEW_TEXT+'\n'+r76.observer(out,sorted(raw))+v.suffix([x['name'] for x in rows])
    ilog=r81.run_lean_with_diagnostics([],out/'CapsuleObservation.lean',imported)
    obs=r81.read_direct_with_dependency_diagnostics(ilog,[{'name':x['name'],'expected_direct_refs':x['expected_direct_refs']} for x in rows]);need(len(obs)==453 and [x['name'] for x in obs]==[x['name'] for x in rows],'R84 imported inventory')
    for x,y in zip(obs,rows,strict=True):need(all(x[k]==y[k] for k in fields),'R84 imported kernel mismatch '+y['name'])
    iraw=r76.raw_audit(ilog,{x['name']:x for x in obs},raw)
    need({n:r81.canonical_raw(x) for n,x in iraw.items()}=={n:r81.canonical_raw(x) for n,x in raw.items()},'R84 imported complete proof mismatch')
    replay={'observations':[{'name':x['name'],**{k:x[k] for k in fields}} for x in obs],'raw_proof_digests':{n:digest(r81.canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay);(out/VIEW).write_text(VIEW_TEXT,encoding='utf-8')
    manifest={'schema':'kuuos.codeai.r84.incremental-compiled-proof.v1','module':IMPORT_MODULE,'module_path':str(IMPORT_DIR/(MODULE+'.olean')),'files':fs,'parent_module':pin['module'],'parent_olean_sha256':pin['olean_sha256'],'parent_independent_run':pin['run_id'],'parent_imported_replay_digest':pin['replay_digest'],'source_sha256':file_hash(p),'view_sha256':file_hash(out/VIEW),'imported_replay_digest':digest(replay),'imported_audits':453,'imported_complete_proofs':354,'parent_source_recompiled':False,'delta_compilation_count':1,'proof_authority':False,'action_authority':False}
    v.save(out/MANIFEST,manifest)
    after=r81.r69.observe_live_r3(scope);r81.r69.observation_pair_valid(scope,before,after);v.save(out/'main-observations.json',{'before':before,'after':after})
    boundary={k:False for k in BOUNDARY}
    inherited={k:True for k in ('minimal_batch_constructor_proved','candidate_inclusion_minimality_proved','conflict_no_extension_proved','finite_frontier_coverage_proved','equal_binding_set_distinct_route_retained','append_only_residual_exactness_proved','impossible_route_persistence_proved','old_frontier_pruning_counterexample_proved','cached_plan_set_refresh_proved','cached_inventory_order_and_ids_retained','cached_frontier_set_refresh_proved','closed_set_cache_refresh_proved','two_stage_set_cache_composition_proved','two_stage_frontier_composition_proved','finite_chain_endpoint_extension_proved','finite_chain_cache_exactness_proved','finite_chain_chunk_composition_proved','finite_chain_frontier_exactness_proved','all_routes_retained','raw_positive_hold','raw_negative_retained','historical_hold_retained','external_approval_required','historical_research_only','future_additions_observation_only','deletion_basis_only_no_inverse_retained','net_history_collision_retained','original_patch_history_retained')}
    need(all(parent.get(k) is True and pd.get(k) is True for k in inherited),'R83 inherited positive claims')
    record=r63.r62.gate.base.portable.seal({'schema':'kuuos.codeai.registry-stream-cache.v1','parent_key':pin['key'],'parent_direct_digest':pin['direct_digest'],'parent_mcp_digest':pin['mcp_digest'],'parent_manifest_digest':pin['manifest_digest'],'historical_scope_digest':digest(scope),'script_bridge_digest':digest(bridge),'r69_additive_observation_digest':digest(extension),'source_head':cfg['fixed_scope']['canonical_head'],'source_tree':cfg['fixed_scope']['canonical_tree'],'original_routes':parent['original_routes'],'empty_inventory_holds':parent['empty_inventory_holds'],'raw_theorems':newraw,'formal_observations':{x['name']:x for x in audit},'actual_computations':values,'candidate_manifest_sha256':file_hash(CONFIG),'r82_r1_failure_evidence_digest':pin['r1_failure_evidence_digest'],'formal_source_sha256':file_hash(FORMAL),'computation_source_sha256':file_hash(TESTS),**inherited,**boundary})
    v.save(out/RECORD,record)
    d={'status':'R84_DIRECT_STREAM_CACHE','r82_r1_failure_evidence_digest':pin['r1_failure_evidence_digest'],'parent_direct_digest':pin['direct_digest'],'parent_mcp_digest':pin['mcp_digest'],'stream_cache_key':record['key'],'audit_capsule_digest':digest(manifest),'imported_replay_digest':digest(replay),'delta_source_sha256':file_hash(p),'new_theorem_names':names,'general_theorems':12,'actual_theorems':2,'actual_computations':values,'raw_theorem_digests':{n:digest(x) for n,x in newraw.items()},'parent_source_recompiled':False,'delta_compilation_count':1,'imported_complete_proofs':354,'historical_hold_retained':True,'empty_inventory_hold_count':5,'unobserved_module_count':695,'fresh_application':{'observations':rows,'mcp_source':source},**inherited,**boundary}
    v.save(out/'direct.json',d);print('KUUOS_R84_DIRECT',json.dumps({'direct_digest':digest(d),'audits':453,'complete_proofs':354,'comparisons':values,'manifest':manifest},sort_keys=True),flush=True);return d

def check_capsule(out,d):
    m,r,rec=load(out/MANIFEST),load(out/REPLAY),load(out/RECORD)
    evidence=load(out/'r82-r1-failure'/'repair-evidence.json')
    need(digest(evidence)==d['r82_r1_failure_evidence_digest']==rec['r82_r1_failure_evidence_digest']==pin['r1_failure_evidence_digest'] and evidence['r1_admitted'] is False and evidence['r1_source_recompiled'] is False and all(file_hash(out/'r82-r1-failure'/name)==h for name,h in evidence['retained_file_sha256'].items()),'R84 retained R82 failure evidence')
    need(d['status']=='R84_DIRECT_STREAM_CACHE' and m['schema']=='kuuos.codeai.r84.incremental-compiled-proof.v1' and m['module']==IMPORT_MODULE and m['module_path']==str(IMPORT_DIR/(MODULE+'.olean')) and m['files']==module_files(out/CAP),'R84 compiled manifest')
    need(m['parent_olean_sha256']==pin['olean_sha256'] and m['parent_module']==pin['module'] and m['parent_imported_replay_digest']==pin['replay_digest'] and m['parent_independent_run']==pin['run_id'],'R84 manifest parent')
    need(m['source_sha256']==file_hash(out/SOURCE)==d['delta_source_sha256'] and (out/SOURCE).read_bytes()==d['fresh_application']['mcp_source'].encode() and (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m['view_sha256']==file_hash(out/VIEW),'R84 exact source and view')
    need(digest(m)==d['audit_capsule_digest'] and digest(r)==m['imported_replay_digest']==d['imported_replay_digest'] and m['imported_audits']==453 and m['imported_complete_proofs']==354 and m['parent_source_recompiled'] is False and m['delta_compilation_count']==1 and m['proof_authority'] is False and m['action_authority'] is False,'R84 replay scope')
    need(r['observations']==[{'name':x['name'],**{k:x[k] for k in fields}} for x in d['fresh_application']['observations']],'R84 replay rows')
    raw=historical_raw(out);need(set(raw).isdisjoint(rec['raw_theorems']),'R84 raw replacement');raw.update(rec['raw_theorems'])
    need(len(raw)==354 and r['raw_proof_digests']=={n:digest(r81.canonical_raw(x)) for n,x in raw.items()},'R84 raw replay')
    need(rec['key']==d['stream_cache_key']==r63.r62.gate.base.portable.seal(rec)['key'] and {n:digest(x) for n,x in rec['raw_theorems'].items()}==d['raw_theorem_digests'] and all(rec[k] is False and d[k] is False for k in BOUNDARY),'R84 research record binding')
    return m,r

DIAG_FILES=(('error','mcp-diagnostics.json'),('warning','mcp-diagnostics-warning.json'))
DIAG_SOURCE=str(IMPORT_DIR/SOURCE)
VIEW_PATH=str(IMPORT_DIR/VIEW)

def diagnostics(client,out,d):
    p=out/SOURCE;need(p.read_bytes()==d['fresh_application']['mcp_source'].encode(),'R84 diagnostic source')
    receipts=[]
    for severity,name in DIAG_FILES:
        args={'file_path':DIAG_SOURCE,'timeout_s':r81.DIAG_TIMEOUT,'severity':severity}
        raw=v.call_tool(client,'lean_diagnostic_messages',args);v.save(out/name,raw)
        diag=v.structured(raw);print('KUUOS_R84_DIAGNOSTIC',json.dumps({'severity':severity,'result':diag},sort_keys=True),flush=True)
        need(r81.complete_diagnostic(raw),'R84 full-source '+severity+' incomplete or non-clean')
        receipts.append({'severity':severity,'file':name,'request':args,'raw_sha256':file_hash(out/name)})
    manifest={'schema':'kuuos.codeai.r84.complete-severity-diagnostics.v1','source_sha256':file_hash(p),'mcp_version':v.EXPECTED_SERVER_VERSION,'full_source':True,'no_line_or_declaration_filter':True,'all_error_and_warning_severities':True,'info_and_hint_not_transferred':True,'timeout_s_per_call':r81.DIAG_TIMEOUT,'client_timeout_s':r81.DIAG_CLIENT_TIMEOUT,'pinned_diagnostics_api_blob':r81.DIAG_API_BLOB,'pinned_diagnostics_processor_blob':r81.DIAG_PROCESS_BLOB,'receipts':receipts}
    v.save(out/'mcp-diagnostic-coverage.json',manifest);return manifest

def verify_diagnostics(first,d,mp):
    m=load(first/'mcp-diagnostic-coverage.json');need(m['schema']=='kuuos.codeai.r84.complete-severity-diagnostics.v1' and m['source_sha256']==file_hash(first/SOURCE)==d['delta_source_sha256'] and digest(m)==mp['diagnostic_coverage_digest'] and m['mcp_version']==v.EXPECTED_SERVER_VERSION and m['pinned_diagnostics_api_blob']==r81.DIAG_API_BLOB and m['pinned_diagnostics_processor_blob']==r81.DIAG_PROCESS_BLOB and m['timeout_s_per_call']==r81.DIAG_TIMEOUT and m['client_timeout_s']==r81.DIAG_CLIENT_TIMEOUT and all(m[k] is True for k in ('full_source','no_line_or_declaration_filter','all_error_and_warning_severities','info_and_hint_not_transferred')) and len(m['receipts'])==2,'R84 diagnostic manifest')
    for item,(severity,name) in zip(m['receipts'],DIAG_FILES,strict=True):
        need(item=={'severity':severity,'file':name,'request':{'file_path':DIAG_SOURCE,'timeout_s':r81.DIAG_TIMEOUT,'severity':severity},'raw_sha256':file_hash(first/name)} and r81.complete_diagnostic(load(first/name)),'R84 complete diagnostic receipt')
    return m

def mcp(out):
    d=load(out/'direct.json');mf,replay=check_capsule(out,d);installed_matches(mf['files'])
    parent=out/PARENT;pd,pm=load(parent/'direct.json'),load(parent/'mcp.json')
    need(digest(pd)==pin['direct_digest'] and digest(pm)==pin['mcp_digest'] and pm['direct_digest']==pin['direct_digest'] and pm['mcp_version']==v.EXPECTED_SERVER_VERSION,'R84 MCP parent')
    prev={x['name']:(j,x) for j,x in enumerate(pd['fresh_application']['observations'])};need(len(prev)==439 and set(prev).isdisjoint(d['new_theorem_names']),'R84 disjoint MCP inventory')
    version=v.server_version(['uvx','--from','lean-lsp-mcp=='+v.EXPECTED_SERVER_VERSION,'lean-lsp-mcp'],root)
    client=r81.transport.new_client('KuuOS R84 delta source diagnostics')
    try: coverage=diagnostics(client,out,d)
    finally: client.close()
    client=r81.transport.new_client('KuuOS R84 new compiled theorem audits');rows=[];origins=[]
    try:
        for j,row in enumerate(d['fresh_application']['observations']):
            name=row['name'];dest=out/f'mcp-verify-{j}.json'
            if name in prev:
                k,prior=prev[name];need(prior==row,'R84 exact prior row')
                copy_file(parent/f'mcp-verify-{k}.json',dest);raw=load(dest)
                origin={'name':name,'mode':'exact_reused','origin_run':pin['run_id'],'origin_job':pin['sandbox_job_id'],'parent_audit_index':k,'prior_origin':pm['audit_origins'][k],'receipt_sha256':file_hash(dest)}
            else:
                need(name in d['new_theorem_names'],'R84 new audit identity');installed_matches(mf['files'])
                args={'file_path':VIEW_PATH,'theorem_name':name,'scan_source':False}
                print('KUUOS_R84_VERIFY_START',json.dumps(args,sort_keys=True),flush=True)
                raw=client.request('tools/call',{'name':'lean_verify','arguments':args});v.save(dest,raw)
                origin={'name':name,'mode':'fresh_actual_mcp','receipt_sha256':file_hash(dest),'request':args,'audit_capsule_digest':digest(mf),'audit_view_sha256':mf['view_sha256']}
            val=v.structured(raw);ax=normalize(val['axioms']);need(raw['result']['isError'] is False and val['warnings']==[] and ax==row['axioms'] and set(ax)<=set(cfg['fixed_scope']['standard_axioms']),'R84 MCP axiom audit '+name)
            rows.append({'name':name,'axioms':ax});origins.append(origin)
    finally: client.close()
    reused=sum(x['mode']=='exact_reused' for x in origins);fresh=len(origins)-reused;need((reused,fresh,len(rows))==(439,14,453),'R84 exact MCP count');installed_matches(mf['files'])
    result={'status':'R84_REAL_MCP_GREEN','direct_digest':digest(d),'audits':rows,'audit_origins':origins,'parent_mcp_digest':pin['mcp_digest'],'reused_audit_count':reused,'new_audit_count':fresh,'fresh_full_source_diagnostics':True,'diagnostic_scope':'full_source_error_and_warning','diagnostic_source_scope':'new_delta_module_with_certified_parent_import','diagnostic_coverage_digest':digest(coverage),'mcp_version':v.EXPECTED_SERVER_VERSION,'version_output':version,'audit_transport':'incremental_compiled_import_exact_replay','audit_capsule_digest':digest(mf),'audit_view_sha256':mf['view_sha256'],'imported_replay_digest':digest(replay)}
    v.save(out/'mcp.json',result);print('KUUOS_R84_MCP',json.dumps({'mcp_digest':digest(result),'audited':453,'new_actual_mcp_audits':14,'reused_actual_mcp_audits':439},sort_keys=True),flush=True)

def independent(d,first,out):
    a,mp=load(first/'direct.json'),load(first/'mcp.json');mf,replay=check_capsule(out,d);prior,preplay=check_capsule(first,a)
    need(a==d and prior==mf and preplay==replay and mp['status']=='R84_REAL_MCP_GREEN' and mp['direct_digest']==digest(d) and mp['parent_mcp_digest']==pin['mcp_digest'] and mp['reused_audit_count']==439 and mp['new_audit_count']==14 and mp['fresh_full_source_diagnostics'] is True and mp['diagnostic_scope']=='full_source_error_and_warning' and mp['diagnostic_source_scope']=='new_delta_module_with_certified_parent_import' and mp['audit_transport']=='incremental_compiled_import_exact_replay' and mp['audit_capsule_digest']==digest(prior) and mp['audit_view_sha256']==prior['view_sha256'] and mp['imported_replay_digest']==digest(replay) and mp['mcp_version']==v.EXPECTED_SERVER_VERSION,'R84 independent receipt binding')
    coverage=verify_diagnostics(first,d,mp)
    for name in ('mcp-diagnostic-coverage.json','mcp-diagnostics.json','mcp-diagnostics-warning.json'):copy_file(first/name,out/name)
    parent=out/PARENT;pd,pm=load(parent/'direct.json'),load(parent/'mcp.json');rows=d['fresh_application']['observations'];origins=mp['audit_origins']
    need(len(mp['audits'])==len(origins)==len(rows)==453,'R84 independent MCP inventory')
    reused=fresh=0
    for j,row in enumerate(rows):
        p=first/f'mcp-verify-{j}.json';raw=load(p);val=v.structured(raw);origin=origins[j]
        need(raw['result']['isError'] is False and val['warnings']==[] and normalize(val['axioms'])==row['axioms']==mp['audits'][j]['axioms'] and row['name']==mp['audits'][j]['name']==origin['name'] and origin['receipt_sha256']==file_hash(p),'R84 independent MCP receipt')
        if origin['mode']=='exact_reused':
            k=origin['parent_audit_index'];need(0<=k<439 and origin['origin_run']==pin['run_id'] and origin['origin_job']==pin['sandbox_job_id'] and pd['fresh_application']['observations'][k]==row and origin['prior_origin']==pm['audit_origins'][k],'R84 prior origin');compare_file(parent/f'mcp-verify-{k}.json',p);reused+=1
        else:
            need(origin['mode']=='fresh_actual_mcp' and row['name'] in d['new_theorem_names'] and origin['request']=={'file_path':VIEW_PATH,'theorem_name':row['name'],'scan_source':False} and origin['audit_capsule_digest']==digest(prior) and origin['audit_view_sha256']==prior['view_sha256'],'R84 fresh origin');fresh+=1
    need((reused,fresh)==(439,14),'R84 exact independent MCP count')
    scope=load(out/'historical-scope.json')
    for folder in (out,first):
        ob=load(folder/'main-observations.json');r81.r69.observation_pair_valid(scope,ob['before'],ob['after'])
    for n in files+(RECORD,'direct.json','historical-scope.json','script-bridge.json','script-observation-bridge-r69.json','formal-source.lean','stream-cache-computation.lean','stream-cache-computation.json','candidate-manifest.json',SOURCE,VIEW,MANIFEST,REPLAY,'CapsuleObservation.lean',*history):compare_file(out/n,first/n)
    for folder in (CAP,*parents,*('parent-r'+str(i)+'-receipts' for i in range(54,84))):tree_equal(out/folder,first/folder)
    tree_equal(out/'r82-r1-failure',first/'r82-r1-failure')
    installed_matches(mf['files'])
    result={k:x for k,x in d.items() if k!='fresh_application'}
    result.update({'status':'R84_INDEPENDENT_STREAM_CACHE_GREEN','direct_digest':digest(d),'mcp_digest':digest(mp),'mcp_audits':453,'mcp_new_audits':14,'mcp_reused_audits':439,'diagnostic_coverage_digest':digest(coverage),'fresh_full_source_mcp_diagnostics':True,'parent_bytes_preserved':True,'raw_new_proofs_equal':True,'raw_type_and_proof_equal':True,'compiled_file_bytes_equal':True,'imported_replay_equal':True,'actual_computation_bytes_equal':True,'parent_source_recompiled':False,'independent_delta_compilation_count':1})
    v.save(out/'independent.json',result);print('KUUOS_R84_INDEPENDENT',json.dumps(result,sort_keys=True),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('preflight','direct','mcp','independent'),required=True);parser.add_argument('--out',type=Path)
    for x in ('r83-local','r83-independent','first'):parser.add_argument('--'+x,type=Path)
    a=parser.parse_args()
    if a.phase=='preflight':
        c=config_check();print(json.dumps({'status':'STATIC_SOURCE_HASH_MATCH_ONLY','theorem_candidates':len(c['new_theorem_candidates']),'comparison_candidates':len(CHECKS),'lean_executed':False},sort_keys=True));return
    activate();need(a.out is not None,'required --out');out=a.out.resolve();need(out==root/IMPORT_DIR,'R84 exact isolated runner path')
    if a.phase=='mcp':mcp(out);return
    need(a.r83_local is not None and a.r83_independent is not None,'required certified parent pair')
    if a.phase=='independent':need(a.first is not None,'required sandbox output')
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=='independent':independent(d,a.first,out)
if __name__=='__main__':main()
