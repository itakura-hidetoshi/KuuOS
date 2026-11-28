#!/usr/bin/env python3
"""R82 R2 candidate verifier; retain R1 failure and repair only trace_length. No claim of successful execution.
Run only in the pinned research runner with R81 verified artifacts.
Preserve parent bytes; compile exactly one new module per direct runner.
"""
from __future__ import annotations
import argparse, json, shutil, hashlib, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
FORMAL=HERE/'lean_probes'/'codeai_registry_checked_chain_v1_r2.lean'
TESTS=HERE/'lean_probes'/'codeai_registry_checked_chain_v1_tests.lean'
CONFIG=HERE/'lean_probes'/'R82_R2_candidate_manifest.json'
MODULE='CheckedChainR82'
IMPORT_DIR=Path('artifacts/olean-r82')
IMPORT_MODULE='artifacts.«olean-r82».CheckedChainR82'
SOURCE=MODULE+'.lean'
VIEW='McpCapsuleApplication.lean'
VIEW_TEXT='import '+IMPORT_MODULE+'\n'
CAP='audit-capsule'
MANIFEST='r82-audit-capsule.json'
REPLAY='r82-imported-replay.json'
RECORD='registry-checked-chain-v1.json'
PARENT='parent-r81-receipts'
PARENT_CAP='parent-r81-audit-capsule'
CHECKS={'empty_input','all_batches_accepted_including_empty','exact_terminal_bindings','exact_suffix_and_position','atomic_failure_and_no_later_application','existing_key_reason','duplicate_reason_and_no_progress','both_failure_flags','full_cache_exact','prefix_cache_exact','frontier_exact','none_is_not_empty','actual_good_and_bad_prefixes','actual_required_binding_preserved','actual_cache_exact','actual_hold_prefix_exact','actual_frontier_exact'}
BOUNDARY=('proof_authority','action_authority','release_authorized','active_policy_changed','semantic_search_complete','complete_transitive_closure','all_repository_dependencies_observed','python_general_correctness_proved','policy_is_refutation','live_main_admission','current_main_certification_transferred','identity_authentication_proved','registry_authentication_proved','unknown_registration_is_refutation','registry_updated','automatic_registration_authority','batch_applied_to_live_registry','registration_correctness_implied_by_readiness','execution_history_order_independent','automatic_recovery_authority','cross_route_replacement_proved','search_of_unlisted_routes_complete','ordered_binding_list_refresh_proved','arbitrary_cache_refresh_proved','general_r77_projection_equality_proved')

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def file_hash(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def config_check():
    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    need(file_hash(CONFIG)=='20d3ee3e3fc2eef42e35bc66af00238617bdf4cc681c097600cf03e2d1ffc8a3','fixed R82 candidate manifest')
    for item,p in zip(cfg['files'],(FORMAL,TESTS),strict=True):
        need(item['name']==p.name and item['sha256']==file_hash(p) and item['bytes']==p.stat().st_size,'R82 exact source '+p.name)
    import re
    names=cfg['new_theorem_candidates']; refs=cfg['required_direct_references']
    declared=['KuuOSR82.'+n for n in re.findall(r'^theorem ([A-Za-z0-9_]+)',FORMAL.read_text(encoding='utf-8'),re.M)]
    declared_checks=re.findall(r'^\s*\("([a-z0-9_]+)",',TESTS.read_text(encoding='utf-8'),re.M)
    need(declared==names,'R82 source declaration list matches manifest')
    need(len(declared_checks)==len(set(declared_checks))==17 and set(declared_checks)==CHECKS,'R82 source comparison list matches verifier')
    need(len(names)==len(set(names))==16 and set(refs)<=set(names),'R82 declaration inventory')
    need(cfg['expected_comparison_count']==len(CHECKS)==17,'R82 comparison inventory')
    return cfg

def activate():
    global r81,r80,r76,r75,r63,v,root,load,sha,digest,normalize,pin,cfg,fields,files,history,parents
    import check_codeai_olean_registry_finite_chain_v1_r81 as r81
    r80,r76,r75,r63,v=r81.r80,r81.r76,r81.r75,r81.r63,r81.v
    root,load,sha,digest,normalize,fields=r81.ROOT,r81.load,r81.sha,r81.digest,r81.normalize,r81.FIELDS
    cfg=config_check(); pin=cfg['parent']
    files=r81.FILES+(r81.NEW,)
    history=r81.HIST_RAW+('parent-r81-raw-replay.json',)
    parents=(r81.BASE_CAP,r81.R75_CAP,r81.R76_CAP,r81.R77_CAP,r81.R78_CAP,r81.R79_CAP,r81.PARENT_CAP,PARENT_CAP,'capsule','joint-capsule')
    need(str(r81.r66.PINNED_HEAD)==cfg['fixed_scope']['canonical_head'] and str(r81.r66.PINNED_TREE)==cfg['fixed_scope']['canonical_tree'],'R82 historical root')

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
    need(run['id']==pin['run_id'] and run['head_sha']==pin['head'] and run['head_commit']['tree_id']==pin['tree'] and run['run_attempt']==1 and run['status']=='completed' and run['conclusion']=='success','R81 run identity')
    for jid,steps in ((pin['sandbox_job_id'],('Verify R81 registry finite chain','Actual Lean MCP R81 new declarations and exact prior receipt reuse')),(pin['independent_job_id'],('Independently verify R81 registry finite chain',))):
        j=api('actions/jobs/'+str(jid));need(j['id']==jid and j['run_id']==pin['run_id'] and j['head_sha']==pin['head'] and j['status']=='completed' and j['conclusion']=='success' and all(any(s['name']==name and s['status']=='completed' and s['conclusion']=='success' for s in j['steps']) for name in steps),'R81 job identity')
    for tag in ('local','independent'):
        aid=pin['artifact_'+tag+'_id']; x=api('actions/artifacts/'+str(aid))
        need(x['id']==aid and x['name']==pin['artifact_'+tag+'_name'] and x['digest']=='sha256:'+pin['artifact_'+tag+'_sha256'] and not x['expired'] and x['workflow_run']['id']==pin['run_id'] and x['workflow_run']['head_sha']==pin['head'],'R81 artifact identity')

def admit(a,out,scope,bridge,extension):
    parent_api(); left,right=a.r81_local,a.r81_independent
    # Audit all matching files, but preserve distinct main observations separately.
    d,mp,ind=load(left/'direct.json'),load(left/'mcp.json'),load(right/'independent.json')
    need(d==load(right/'direct.json') and digest(d)==pin['direct_digest'] and digest(mp)==pin['mcp_digest'],'R81 fixed direct and MCP digests')
    need(mp['status']=='R81_REAL_MCP_GREEN' and mp['direct_digest']==pin['direct_digest'] and ind['status']=='R81_INDEPENDENT_FINITE_CHAIN_GREEN' and ind['direct_digest']==pin['direct_digest'] and ind['mcp_digest']==pin['mcp_digest'],'R81 independent binding')
    need(ind['mcp_audits']==411 and ind['mcp_new_audits']==8 and ind['mcp_reused_audits']==403 and ind['imported_complete_proofs']==312 and all(ind[k] is True for k in ('parent_bytes_preserved','raw_new_proofs_equal','finite_chain_bytes_equal','actual_computation_bytes_equal','raw_type_and_proof_equal','compiled_file_bytes_equal','imported_replay_equal')),'R81 certified counters and byte checks')
    need(d['parent_source_recompiled'] is False and ind['parent_source_recompiled'] is False and d['delta_compilation_count']==ind['independent_delta_compilation_count']==1,'R81 compilation history')
    rows=d['fresh_application']['observations'];need(len(rows)==len({x['name'] for x in rows})==411 and [{'name':x['name'],'axioms':x['axioms']} for x in rows]==mp['audits'],'R81 audit inventory')
    for name in files:
        compare_file(left/name,right/name);copy_file(left/name,out/name)
    rec=load(out/r81.NEW)
    need(rec['key']==pin['key']==r63.r62.gate.base.portable.seal(rec)['key'] and len(rec['original_routes'])==2 and len(rec['empty_inventory_holds'])==5,'R81 sealed research record')
    need(rec['historical_scope_digest']==d['historical_scope_digest']==r81.SCOPE==digest(scope) and rec['script_bridge_digest']==d['script_bridge_digest']==r81.BRIDGE==digest(bridge) and rec['r69_additive_observation_digest']==d['r69_additive_observation_digest']==r81.EXTENSION==digest(extension),'R81 historical scope')
    need({n:digest(x) for n,x in rec['raw_theorems'].items()}==d['raw_theorem_digests'] and all(d.get(k) is False and rec.get(k) is False for k in BOUNDARY),'R81 raw proofs and authority limits')
    m1,replay1=r81.check_capsule(left,d);m2,replay2=r81.check_capsule(right,d)
    pfiles=[{'name':'FiniteChainR81.olean','sha256':pin['olean_sha256'],'bytes':pin['olean_bytes']}]
    need(m1==m2 and digest(m1)==pin['manifest_digest'] and replay1==replay2 and digest(replay1)==pin['replay_digest'] and m1['files']==pfiles,'R81 compiled certificate')
    coverage=r81.verify_complete_diagnostics(left,d,mp)
    need(digest(coverage)==pin['diagnostics_digest']==ind['diagnostic_coverage_digest'] and mp['reused_audit_count']==403 and mp['new_audit_count']==8 and len(mp['audit_origins'])==411 and mp['audit_capsule_digest']==pin['manifest_digest'] and mp['imported_replay_digest']==pin['replay_digest'] and mp['fresh_full_source_diagnostics'] is True,'R81 diagnostic receipt')
    receipts=out/PARENT;receipts.mkdir()
    for name,src in (('direct.json',left),('mcp.json',left),('independent.json',right)):
        copy_file(src/name,receipts/name)
    for name in ('formal-source.lean','finite-application.lean','finite-computation.lean','finite-computation.json','historical-scope.json','script-bridge.json','script-observation-bridge-r69.json',r81.SOURCE,r81.VIEW,r81.MANIFEST,r81.REPLAY,'CapsuleObservation.lean','mcp-diagnostic-coverage.json','mcp-diagnostics.json','mcp-diagnostics-warning.json',*r81.HIST_RAW):
        compare_file(left/name,right/name);copy_file(left/name,receipts/name)
    for name,field in (('formal-source.lean','formal_source_sha256'),('finite-application.lean','application_source_sha256'),('finite-computation.lean','computation_source_sha256')):
        need(file_hash(receipts/name)==rec[field],'R81 source lineage')
    need(load(receipts/'finite-computation.json')==rec['actual_computations'],'R81 comparison lineage')
    for label,src in (('sandbox',left),('independent',right)):
        obs=load(src/'main-observations.json');r81.r69.observation_pair_valid(scope,obs['before'],obs['after']);copy_file(src/'main-observations.json',receipts/(label+'-main-observations.json'))
    for j,row in enumerate(rows):
        name=f'mcp-verify-{j}.json';raw=load(left/name);val=v.structured(raw);origin=mp['audit_origins'][j]
        need(raw['result']['isError'] is False and val['warnings']==[] and normalize(val['axioms'])==row['axioms']==mp['audits'][j]['axioms'] and row['name']==mp['audits'][j]['name']==origin['name'] and origin['receipt_sha256']==file_hash(left/name),'R81 exact prior MCP '+row['name'])
        copy_file(left/name,receipts/name)
    for folder in ('capsule','joint-capsule'):
        mf=d['capsule_manifest' if folder=='capsule' else 'joint_capsule_manifest'];tool=r63.r62.r39 if folder=='capsule' else r63.r62.r45
        need(tool.capsule_files(left/folder)==tool.capsule_files(right/folder)==mf['files'],'R81 base capsule')
        copy_tree(left/folder,right/folder,out/folder);need(file_hash(out/folder/(mf['module']+'.lean'))==mf['source_sha256'],'R81 base source');tool.install(out/folder,mf)
    for folder in parents[:-3]: copy_tree(left/folder,right/folder,out/folder)
    base=[{'name':'RecoveryDualityR62.olean','sha256':r75.PARENT_OLEAN,'bytes':5972832}]
    need(r81.transport.capsule_files(out/r81.BASE_CAP)==base,'R81 recovery base');r81.transport.install(out/r81.BASE_CAP,base)
    for tool,folder,fs in ((r75,r81.R75_CAP,[{'name':'RegistryRecoveryR75.olean','sha256':r76.PARENT_OLEAN,'bytes':236464}]),(r76,r81.R76_CAP,r81.r77.PARENT_FILES),(r81.r77,r81.R77_CAP,r81.r78.PARENT_FILES),(r81.r78,r81.R78_CAP,r81.r79.PARENT_FILES),(r81.r79,r81.R79_CAP,r80.PARENT_FILES),(r80,r81.PARENT_CAP,r81.PARENT_FILES)):
        need(tool.module_files(out/folder)==fs,'R81 dependency module identity '+folder);tool.install_module(out/folder,fs)
    copy_tree(left/r81.CAP,right/r81.CAP,out/PARENT_CAP);r81.install_module(out/PARENT_CAP,pfiles);r81.installed_matches(pfiles)
    for i in range(54,81):
        folder='parent-r'+str(i)+'-receipts';copy_tree(left/folder,right/folder,out/folder)
    for name in r81.HIST_RAW:
        compare_file(left/name,right/name);copy_file(left/name,out/name)
    v.save(out/'parent-r81-raw-replay.json',rec['raw_theorems'])
    return d,mp,rec

def historical_raw(out):
    raw={}
    for name in history:
        x=load(out/name);need(set(raw).isdisjoint(x),'duplicate historical proof');raw.update(x)
    need(len(raw)==312,'R81 full proof count');return raw

def module_files(folder):
    expected={MODULE+'.olean',MODULE+'.olean.server',MODULE+'.olean.private'}
    actual={p.name for p in folder.iterdir()}
    need(actual in ({MODULE+'.olean'},expected),'R82 exact isolated module parts')
    need(all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),'R82 module regular files')
    return [{'name':n,'sha256':file_hash(folder/n),'bytes':(folder/n).stat().st_size} for n in (MODULE+'.olean',MODULE+'.olean.server',MODULE+'.olean.private') if n in actual]

def installed_matches(fs):
    r81.installed_matches([{'name':'FiniteChainR81.olean','sha256':pin['olean_sha256'],'bytes':pin['olean_bytes']}])
    dest=root/'.lake/build/lib/lean'/IMPORT_DIR
    need(module_files(dest)==fs,'R82 installed module identity')


def bind_r1_failure(a,out):
    repair=cfg['repair']; api=v.cache.api
    run=api('actions/runs/'+str(repair['r1_run']))
    need(run['id']==repair['r1_run'] and run['head_sha']==repair['r1_head'] and run['head_commit']['tree_id']==repair['r1_tree'] and run['run_attempt']==1 and run['status']=='completed' and run['conclusion']=='failure','R82 R1 exact failed run')
    job=api('actions/jobs/'+str(repair['r1_sandbox_job']))
    need(job['id']==repair['r1_sandbox_job'] and job['run_id']==repair['r1_run'] and job['head_sha']==repair['r1_head'] and job['status']=='completed' and job['conclusion']=='failure','R82 R1 failed job')
    need(all(any(s['name']==name and s['status']=='completed' and s['conclusion']==conclusion for s in job['steps']) for name,conclusion in [('Verify fixed R82 candidate source hashes','success'),('Verify R82 checked registry extension chain','failure'),('Actual Lean MCP R82 new declarations and exact prior receipt reuse','skipped'),('Run actions/upload-artifact@v4','success')]),'R82 R1 exact failure steps')
    independent=api('actions/jobs/'+str(repair['r1_independent_job']))
    need(independent['run_id']==repair['r1_run'] and independent['head_sha']==repair['r1_head'] and independent['status']=='completed' and independent['conclusion']=='skipped','R82 R1 independent not admitted')
    art=api('actions/artifacts/'+str(repair['r1_artifact_id']))
    need(art['id']==repair['r1_artifact_id'] and art['name']==repair['r1_artifact_name'] and art['digest']=='sha256:'+repair['r1_artifact_sha256'] and not art['expired'] and art['workflow_run']['id']==repair['r1_run'] and art['workflow_run']['head_sha']==repair['r1_head'],'R82 R1 exact failed artifact')
    original=HERE/'lean_probes'/'codeai_registry_checked_chain_v1.lean'
    original_manifest=HERE/'lean_probes'/'R82_candidate_manifest.json'
    original_verifier=HERE/'check_codeai_olean_registry_checked_chain_v1_r82.py'
    original_workflow=HERE.parent/'.github/workflows/codeai-olean-registry-checked-chain-v1-r82.yml'
    need(file_hash(original)==repair['r1_formal_sha256'] and file_hash(original_manifest)==repair['r1_manifest_sha256'] and file_hash(original_verifier)==repair['r1_verifier_sha256'] and file_hash(original_workflow)==repair['r1_workflow_sha256'],'R82 R1 immutable source lineage')
    previous=original.read_text(encoding='utf-8')
    old="  | hold reg b bs bad => rfl\n  | step reg next b bs updates pending ok tail ih =>\n      simp only [List.length_cons]"
    new="  | hold reg b bs bad => exact Nat.zero_add _\n  | step reg next b bs updates pending ok tail ih =>\n      simp only [List.length_cons]"
    need(previous.count(old)==1 and FORMAL.read_text(encoding='utf-8')==previous.replace(old,new,1),'R82 R2 exact one-line repair')
    oldcfg=json.loads(original_manifest.read_text(encoding='utf-8'))
    for field in ('parent','fixed_scope','new_theorem_candidates','required_direct_references','expected_comparison_count','expected_after_all_gates_pass','authority'):
        need(oldcfg[field]==cfg[field],'R82 no weakened condition '+field)
    need(oldcfg['files'][1]==cfg['files'][1],'R82 identical comparison source')
    failure=a.r82_r1_failure
    need(failure is not None and failure.is_dir(),'R82 required R1 failure evidence')
    compare_file(failure/'formal-source.lean',original)
    compare_file(failure/'candidate-manifest.json',original_manifest)
    compare_file(failure/'checked-chain-computation.lean',TESTS)
    failed_source=(failure/SOURCE).read_text(encoding='utf-8')
    need(failed_source.startswith(previous+'\n'+TESTS.read_text(encoding='utf-8')[len(VIEW_TEXT):]+'\n'),'R82 failed assembled source lineage')
    failed_log=(failure/(MODULE+'.log')).read_text(encoding='utf-8')
    need('Tactic `rfl` failed' in failed_log and repair['diagnostic'] in failed_log and 'case hold' in failed_log,'R82 R1 retained Lean diagnostic')
    need(not any((failure/name).exists() for name in ('direct.json','mcp.json','independent.json')),'R82 R1 cannot be an admitted result')
    retained=out/'r82-r1-failure';retained.mkdir()
    for name in ('formal-source.lean','candidate-manifest.json','checked-chain-computation.lean',SOURCE,MODULE+'.log'):
        copy_file(failure/name,retained/name)
    evidence={**repair,'retained_file_sha256':{p.name:file_hash(p) for p in sorted(retained.iterdir())},'r1_source_recompiled':False,'r1_admitted':False}
    v.save(retained/'repair-evidence.json',evidence)
    print('KUUOS_R82_R2_FAILURE_BOUND',json.dumps(evidence,sort_keys=True),flush=True)
    return evidence

def direct(a,out):
    repair_evidence=bind_r1_failure(a,out)
    scope=r81.r66.observe_historical_scope();bridge=r81.r68.script_bridge(scope);extension=r81.r69.additive_bridge(scope,bridge);before=r81.r69.observe_live_r3(scope)
    for n,x in (('historical-scope.json',scope),('script-bridge.json',bridge),('script-observation-bridge-r69.json',extension)):v.save(out/n,x)
    pd,pm,parent=admit(a,out,scope,bridge,extension)
    formal=FORMAL.read_text(encoding='utf-8'); tests=TESTS.read_text(encoding='utf-8');need(tests.startswith(VIEW_TEXT),'R82 test import boundary')
    for n,p in (('formal-source.lean',FORMAL),('checked-chain-computation.lean',TESTS),('candidate-manifest.json',CONFIG)):copy_file(p,out/n)
    names=sorted(cfg['new_theorem_candidates']);expected=cfg['required_direct_references']
    selected=[{'name':n,'expected_direct_refs':expected.get(n,[])} for n in names]
    # Strip only the test file's self-import, since both files are compiled into a single new module.
    source=formal+'\n'+tests[len(VIEW_TEXT):]+'\n'+r76.observer(out,names)+v.suffix(names)
    cap=out/CAP;cap.mkdir();p=out/SOURCE
    log=r81.run_lean_with_diagnostics(['--root='+str(root),'-o',str(cap/(MODULE+'.olean'))],p,source)
    audit=r81.read_direct_with_dependency_diagnostics(log,selected)
    newraw=r76.raw_audit(log,{x['name']:x for x in audit},names)
    marker='KUUOS_R82_COMPUTE '; values=[json.loads(l[len(marker):]) for l in log.splitlines() if l.startswith(marker)]
    need(len(values)==1 and set(values[0])==CHECKS and all(x is True for x in values[0].values()),'R82 exact 17 comparisons')
    v.save(out/'checked-chain-computation.json',values)
    fs=module_files(cap);dest=root/'.lake/build/lib/lean'/IMPORT_DIR;dest.mkdir(parents=True,exist_ok=False)
    for item in fs:copy_file(cap/item['name'],dest/item['name'])
    installed_matches(fs)
    prior=pd['fresh_application']['observations'];rows=sorted(prior+audit,key=lambda x:x['name']);need(len(rows)==len({x['name'] for x in rows})==427,'R82 accumulated declaration inventory')
    raw=historical_raw(out);need(set(raw).isdisjoint(newraw),'R82 overwrite forbidden');raw.update(newraw);need(len(raw)==328,'R82 complete proof inventory')
    imported=VIEW_TEXT+'\n'+r76.observer(out,sorted(raw))+v.suffix([x['name'] for x in rows])
    ilog=r81.run_lean_with_diagnostics([],out/'CapsuleObservation.lean',imported)
    obs=r81.read_direct_with_dependency_diagnostics(ilog,[{'name':x['name'],'expected_direct_refs':x['expected_direct_refs']} for x in rows]);need(len(obs)==427 and [x['name'] for x in obs]==[x['name'] for x in rows],'R82 imported inventory')
    for x,y in zip(obs,rows,strict=True):need(all(x[k]==y[k] for k in fields),'R82 imported kernel mismatch '+y['name'])
    iraw=r76.raw_audit(ilog,{x['name']:x for x in obs},raw)
    need({n:r81.canonical_raw(x) for n,x in iraw.items()}=={n:r81.canonical_raw(x) for n,x in raw.items()},'R82 imported complete proof mismatch')
    replay={'observations':[{'name':x['name'],**{k:x[k] for k in fields}} for x in obs],'raw_proof_digests':{n:digest(r81.canonical_raw(x)) for n,x in iraw.items()}}
    v.save(out/REPLAY,replay);(out/VIEW).write_text(VIEW_TEXT,encoding='utf-8')
    manifest={'schema':'kuuos.codeai.r82.incremental-compiled-proof.v1','module':IMPORT_MODULE,'module_path':str(IMPORT_DIR/(MODULE+'.olean')),'files':fs,'parent_module':pin['module'],'parent_olean_sha256':pin['olean_sha256'],'parent_independent_run':pin['run_id'],'parent_imported_replay_digest':pin['replay_digest'],'source_sha256':file_hash(p),'view_sha256':file_hash(out/VIEW),'imported_replay_digest':digest(replay),'imported_audits':427,'imported_complete_proofs':328,'parent_source_recompiled':False,'delta_compilation_count':1,'proof_authority':False,'action_authority':False}
    v.save(out/MANIFEST,manifest)
    after=r81.r69.observe_live_r3(scope);r81.r69.observation_pair_valid(scope,before,after);v.save(out/'main-observations.json',{'before':before,'after':after})
    boundary={k:False for k in BOUNDARY}
    inherited={k:True for k in ('minimal_batch_constructor_proved','candidate_inclusion_minimality_proved','conflict_no_extension_proved','finite_frontier_coverage_proved','equal_binding_set_distinct_route_retained','append_only_residual_exactness_proved','impossible_route_persistence_proved','old_frontier_pruning_counterexample_proved','cached_plan_set_refresh_proved','cached_inventory_order_and_ids_retained','cached_frontier_set_refresh_proved','closed_set_cache_refresh_proved','two_stage_set_cache_composition_proved','two_stage_frontier_composition_proved','finite_chain_endpoint_extension_proved','finite_chain_cache_exactness_proved','finite_chain_chunk_composition_proved','finite_chain_frontier_exactness_proved','all_routes_retained','raw_positive_hold','raw_negative_retained','historical_hold_retained','external_approval_required','historical_research_only','future_additions_observation_only','deletion_basis_only_no_inverse_retained','net_history_collision_retained','original_patch_history_retained')}
    need(all(parent.get(k) is True and pd.get(k) is True for k in inherited),'R81 inherited positive claims')
    record=r63.r62.gate.base.portable.seal({'schema':'kuuos.codeai.registry-checked-chain.v1','parent_key':pin['key'],'parent_direct_digest':pin['direct_digest'],'parent_mcp_digest':pin['mcp_digest'],'parent_manifest_digest':pin['manifest_digest'],'historical_scope_digest':digest(scope),'script_bridge_digest':digest(bridge),'r69_additive_observation_digest':digest(extension),'source_head':cfg['fixed_scope']['canonical_head'],'source_tree':cfg['fixed_scope']['canonical_tree'],'original_routes':parent['original_routes'],'empty_inventory_holds':parent['empty_inventory_holds'],'raw_theorems':newraw,'formal_observations':{x['name']:x for x in audit},'actual_computations':values,'candidate_manifest_sha256':file_hash(CONFIG),'r1_failure_evidence_digest':digest(repair_evidence),'formal_source_sha256':file_hash(FORMAL),'computation_source_sha256':file_hash(TESTS),**inherited,**boundary})
    v.save(out/RECORD,record)
    d={'status':'R82_DIRECT_CHECKED_CHAIN','r1_failure_evidence_digest':digest(repair_evidence),'parent_direct_digest':pin['direct_digest'],'parent_mcp_digest':pin['mcp_digest'],'checked_chain_key':record['key'],'audit_capsule_digest':digest(manifest),'imported_replay_digest':digest(replay),'delta_source_sha256':file_hash(p),'new_theorem_names':names,'general_theorems':14,'actual_theorems':2,'actual_computations':values,'raw_theorem_digests':{n:digest(x) for n,x in newraw.items()},'parent_source_recompiled':False,'delta_compilation_count':1,'imported_complete_proofs':328,'historical_hold_retained':True,'empty_inventory_hold_count':5,'unobserved_module_count':695,'fresh_application':{'observations':rows,'mcp_source':source},**inherited,**boundary}
    v.save(out/'direct.json',d);print('KUUOS_R82_DIRECT',json.dumps({'direct_digest':digest(d),'audits':427,'complete_proofs':328,'comparisons':values,'manifest':manifest},sort_keys=True),flush=True);return d

def check_capsule(out,d):
    m,r,rec=load(out/MANIFEST),load(out/REPLAY),load(out/RECORD)
    retained=out/'r82-r1-failure'; evidence=load(retained/'repair-evidence.json')
    need(digest(evidence)==d['r1_failure_evidence_digest']==rec['r1_failure_evidence_digest'] and evidence['r1_admitted'] is False and evidence['r1_source_recompiled'] is False and all(file_hash(retained/name)==h for name,h in evidence['retained_file_sha256'].items()),'R82 R2 retained failure evidence')
    need(d['status']=='R82_DIRECT_CHECKED_CHAIN' and m['schema']=='kuuos.codeai.r82.incremental-compiled-proof.v1' and m['module']==IMPORT_MODULE and m['module_path']==str(IMPORT_DIR/(MODULE+'.olean')) and m['files']==module_files(out/CAP),'R82 compiled manifest')
    need(m['parent_olean_sha256']==pin['olean_sha256'] and m['parent_module']==pin['module'] and m['parent_imported_replay_digest']==pin['replay_digest'] and m['parent_independent_run']==pin['run_id'],'R82 manifest parent')
    need(m['source_sha256']==file_hash(out/SOURCE)==d['delta_source_sha256'] and (out/SOURCE).read_bytes()==d['fresh_application']['mcp_source'].encode() and (out/VIEW).read_bytes()==VIEW_TEXT.encode() and m['view_sha256']==file_hash(out/VIEW),'R82 exact source and view')
    need(digest(m)==d['audit_capsule_digest'] and digest(r)==m['imported_replay_digest']==d['imported_replay_digest'] and m['imported_audits']==427 and m['imported_complete_proofs']==328 and m['parent_source_recompiled'] is False and m['delta_compilation_count']==1 and m['proof_authority'] is False and m['action_authority'] is False,'R82 replay scope')
    need(r['observations']==[{'name':x['name'],**{k:x[k] for k in fields}} for x in d['fresh_application']['observations']],'R82 replay rows')
    raw=historical_raw(out);need(set(raw).isdisjoint(rec['raw_theorems']),'R82 raw replacement');raw.update(rec['raw_theorems'])
    need(len(raw)==328 and r['raw_proof_digests']=={n:digest(r81.canonical_raw(x)) for n,x in raw.items()},'R82 raw replay')
    need(rec['key']==d['checked_chain_key']==r63.r62.gate.base.portable.seal(rec)['key'] and {n:digest(x) for n,x in rec['raw_theorems'].items()}==d['raw_theorem_digests'] and all(rec[k] is False and d[k] is False for k in BOUNDARY),'R82 research record binding')
    return m,r

DIAG_FILES=(('error','mcp-diagnostics.json'),('warning','mcp-diagnostics-warning.json'))
DIAG_SOURCE=str(IMPORT_DIR/SOURCE)
VIEW_PATH=str(IMPORT_DIR/VIEW)

def diagnostics(client,out,d):
    p=out/SOURCE;need(p.read_bytes()==d['fresh_application']['mcp_source'].encode(),'R82 diagnostic source')
    receipts=[]
    for severity,name in DIAG_FILES:
        args={'file_path':DIAG_SOURCE,'timeout_s':r81.DIAG_TIMEOUT,'severity':severity}
        raw=v.call_tool(client,'lean_diagnostic_messages',args);v.save(out/name,raw)
        diag=v.structured(raw);print('KUUOS_R82_DIAGNOSTIC',json.dumps({'severity':severity,'result':diag},sort_keys=True),flush=True)
        need(r81.complete_diagnostic(raw),'R82 full-source '+severity+' incomplete or non-clean')
        receipts.append({'severity':severity,'file':name,'request':args,'raw_sha256':file_hash(out/name)})
    manifest={'schema':'kuuos.codeai.r82.complete-severity-diagnostics.v1','source_sha256':file_hash(p),'mcp_version':v.EXPECTED_SERVER_VERSION,'full_source':True,'no_line_or_declaration_filter':True,'all_error_and_warning_severities':True,'info_and_hint_not_transferred':True,'timeout_s_per_call':r81.DIAG_TIMEOUT,'client_timeout_s':r81.DIAG_CLIENT_TIMEOUT,'pinned_diagnostics_api_blob':r81.DIAG_API_BLOB,'pinned_diagnostics_processor_blob':r81.DIAG_PROCESS_BLOB,'receipts':receipts}
    v.save(out/'mcp-diagnostic-coverage.json',manifest);return manifest

def verify_diagnostics(first,d,mp):
    m=load(first/'mcp-diagnostic-coverage.json');need(m['schema']=='kuuos.codeai.r82.complete-severity-diagnostics.v1' and m['source_sha256']==file_hash(first/SOURCE)==d['delta_source_sha256'] and digest(m)==mp['diagnostic_coverage_digest'] and m['mcp_version']==v.EXPECTED_SERVER_VERSION and m['pinned_diagnostics_api_blob']==r81.DIAG_API_BLOB and m['pinned_diagnostics_processor_blob']==r81.DIAG_PROCESS_BLOB and m['timeout_s_per_call']==r81.DIAG_TIMEOUT and m['client_timeout_s']==r81.DIAG_CLIENT_TIMEOUT and all(m[k] is True for k in ('full_source','no_line_or_declaration_filter','all_error_and_warning_severities','info_and_hint_not_transferred')) and len(m['receipts'])==2,'R82 diagnostic manifest')
    for item,(severity,name) in zip(m['receipts'],DIAG_FILES,strict=True):
        need(item=={'severity':severity,'file':name,'request':{'file_path':DIAG_SOURCE,'timeout_s':r81.DIAG_TIMEOUT,'severity':severity},'raw_sha256':file_hash(first/name)} and r81.complete_diagnostic(load(first/name)),'R82 complete diagnostic receipt')
    return m

def mcp(out):
    d=load(out/'direct.json');mf,replay=check_capsule(out,d);installed_matches(mf['files'])
    parent=out/PARENT;pd,pm=load(parent/'direct.json'),load(parent/'mcp.json')
    need(digest(pd)==pin['direct_digest'] and digest(pm)==pin['mcp_digest'] and pm['direct_digest']==pin['direct_digest'] and pm['mcp_version']==v.EXPECTED_SERVER_VERSION,'R82 MCP parent')
    prev={x['name']:(j,x) for j,x in enumerate(pd['fresh_application']['observations'])};need(len(prev)==411 and set(prev).isdisjoint(d['new_theorem_names']),'R82 disjoint MCP inventory')
    version=v.server_version(['uvx','--from','lean-lsp-mcp=='+v.EXPECTED_SERVER_VERSION,'lean-lsp-mcp'],root)
    client=r81.transport.new_client('KuuOS R82 delta source diagnostics')
    try: coverage=diagnostics(client,out,d)
    finally: client.close()
    client=r81.transport.new_client('KuuOS R82 new compiled theorem audits');rows=[];origins=[]
    try:
        for j,row in enumerate(d['fresh_application']['observations']):
            name=row['name'];dest=out/f'mcp-verify-{j}.json'
            if name in prev:
                k,prior=prev[name];need(prior==row,'R82 exact prior row')
                copy_file(parent/f'mcp-verify-{k}.json',dest);raw=load(dest)
                origin={'name':name,'mode':'exact_reused','origin_run':pin['run_id'],'origin_job':pin['sandbox_job_id'],'parent_audit_index':k,'prior_origin':pm['audit_origins'][k],'receipt_sha256':file_hash(dest)}
            else:
                need(name in d['new_theorem_names'],'R82 new audit identity');installed_matches(mf['files'])
                args={'file_path':VIEW_PATH,'theorem_name':name,'scan_source':False}
                print('KUUOS_R82_VERIFY_START',json.dumps(args,sort_keys=True),flush=True)
                raw=client.request('tools/call',{'name':'lean_verify','arguments':args});v.save(dest,raw)
                origin={'name':name,'mode':'fresh_actual_mcp','receipt_sha256':file_hash(dest),'request':args,'audit_capsule_digest':digest(mf),'audit_view_sha256':mf['view_sha256']}
            val=v.structured(raw);ax=normalize(val['axioms']);need(raw['result']['isError'] is False and val['warnings']==[] and ax==row['axioms'] and set(ax)<=set(cfg['fixed_scope']['standard_axioms']),'R82 MCP axiom audit '+name)
            rows.append({'name':name,'axioms':ax});origins.append(origin)
    finally: client.close()
    reused=sum(x['mode']=='exact_reused' for x in origins);fresh=len(origins)-reused;need((reused,fresh,len(rows))==(411,16,427),'R82 exact MCP count');installed_matches(mf['files'])
    result={'status':'R82_REAL_MCP_GREEN','direct_digest':digest(d),'audits':rows,'audit_origins':origins,'parent_mcp_digest':pin['mcp_digest'],'reused_audit_count':reused,'new_audit_count':fresh,'fresh_full_source_diagnostics':True,'diagnostic_scope':'full_source_error_and_warning','diagnostic_source_scope':'new_delta_module_with_certified_parent_import','diagnostic_coverage_digest':digest(coverage),'mcp_version':v.EXPECTED_SERVER_VERSION,'version_output':version,'audit_transport':'incremental_compiled_import_exact_replay','audit_capsule_digest':digest(mf),'audit_view_sha256':mf['view_sha256'],'imported_replay_digest':digest(replay)}
    v.save(out/'mcp.json',result);print('KUUOS_R82_MCP',json.dumps({'mcp_digest':digest(result),'audited':427,'new_actual_mcp_audits':16,'reused_actual_mcp_audits':411},sort_keys=True),flush=True)

def independent(d,first,out):
    a,mp=load(first/'direct.json'),load(first/'mcp.json');mf,replay=check_capsule(out,d);prior,preplay=check_capsule(first,a)
    need(a==d and prior==mf and preplay==replay and mp['status']=='R82_REAL_MCP_GREEN' and mp['direct_digest']==digest(d) and mp['parent_mcp_digest']==pin['mcp_digest'] and mp['reused_audit_count']==411 and mp['new_audit_count']==16 and mp['fresh_full_source_diagnostics'] is True and mp['diagnostic_scope']=='full_source_error_and_warning' and mp['diagnostic_source_scope']=='new_delta_module_with_certified_parent_import' and mp['audit_transport']=='incremental_compiled_import_exact_replay' and mp['audit_capsule_digest']==digest(prior) and mp['audit_view_sha256']==prior['view_sha256'] and mp['imported_replay_digest']==digest(replay) and mp['mcp_version']==v.EXPECTED_SERVER_VERSION,'R82 independent receipt binding')
    coverage=verify_diagnostics(first,d,mp)
    for name in ('mcp-diagnostic-coverage.json','mcp-diagnostics.json','mcp-diagnostics-warning.json'):copy_file(first/name,out/name)
    parent=out/PARENT;pd,pm=load(parent/'direct.json'),load(parent/'mcp.json');rows=d['fresh_application']['observations'];origins=mp['audit_origins']
    need(len(mp['audits'])==len(origins)==len(rows)==427,'R82 independent MCP inventory')
    reused=fresh=0
    for j,row in enumerate(rows):
        p=first/f'mcp-verify-{j}.json';raw=load(p);val=v.structured(raw);origin=origins[j]
        need(raw['result']['isError'] is False and val['warnings']==[] and normalize(val['axioms'])==row['axioms']==mp['audits'][j]['axioms'] and row['name']==mp['audits'][j]['name']==origin['name'] and origin['receipt_sha256']==file_hash(p),'R82 independent MCP receipt')
        if origin['mode']=='exact_reused':
            k=origin['parent_audit_index'];need(0<=k<411 and origin['origin_run']==pin['run_id'] and origin['origin_job']==pin['sandbox_job_id'] and pd['fresh_application']['observations'][k]==row and origin['prior_origin']==pm['audit_origins'][k],'R82 prior origin');compare_file(parent/f'mcp-verify-{k}.json',p);reused+=1
        else:
            need(origin['mode']=='fresh_actual_mcp' and row['name'] in d['new_theorem_names'] and origin['request']=={'file_path':VIEW_PATH,'theorem_name':row['name'],'scan_source':False} and origin['audit_capsule_digest']==digest(prior) and origin['audit_view_sha256']==prior['view_sha256'],'R82 fresh origin');fresh+=1
    need((reused,fresh)==(411,16),'R82 exact independent MCP count')
    scope=load(out/'historical-scope.json')
    for folder in (out,first):
        ob=load(folder/'main-observations.json');r81.r69.observation_pair_valid(scope,ob['before'],ob['after'])
    for n in files+(RECORD,'direct.json','historical-scope.json','script-bridge.json','script-observation-bridge-r69.json','formal-source.lean','checked-chain-computation.lean','checked-chain-computation.json','candidate-manifest.json',SOURCE,VIEW,MANIFEST,REPLAY,'CapsuleObservation.lean',*history):compare_file(out/n,first/n)
    for folder in (CAP,*parents,*('parent-r'+str(i)+'-receipts' for i in range(54,82))):tree_equal(out/folder,first/folder)
    tree_equal(out/'r82-r1-failure',first/'r82-r1-failure')
    installed_matches(mf['files'])
    result={k:x for k,x in d.items() if k!='fresh_application'}
    result.update({'status':'R82_INDEPENDENT_CHECKED_CHAIN_GREEN','direct_digest':digest(d),'mcp_digest':digest(mp),'mcp_audits':427,'mcp_new_audits':16,'mcp_reused_audits':411,'diagnostic_coverage_digest':digest(coverage),'fresh_full_source_mcp_diagnostics':True,'parent_bytes_preserved':True,'raw_new_proofs_equal':True,'raw_type_and_proof_equal':True,'compiled_file_bytes_equal':True,'imported_replay_equal':True,'actual_computation_bytes_equal':True,'parent_source_recompiled':False,'independent_delta_compilation_count':1})
    v.save(out/'independent.json',result);print('KUUOS_R82_INDEPENDENT',json.dumps(result,sort_keys=True),flush=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('preflight','direct','mcp','independent'),required=True);parser.add_argument('--out',type=Path)
    for x in ('r81-local','r81-independent','r82-r1-failure','first'):parser.add_argument('--'+x,type=Path)
    a=parser.parse_args()
    if a.phase=='preflight':
        c=config_check();print(json.dumps({'status':'STATIC_SOURCE_HASH_MATCH_ONLY','theorem_candidates':len(c['new_theorem_candidates']),'comparison_candidates':len(CHECKS),'lean_executed':False},sort_keys=True));return
    activate();need(a.out is not None,'required --out');out=a.out.resolve();need(out==root/IMPORT_DIR,'R82 exact isolated runner path')
    if a.phase=='mcp':mcp(out);return
    need(a.r81_local is not None and a.r81_independent is not None,'required certified parent pair')
    if a.phase=='independent':need(a.first is not None,'required sandbox output')
    out.mkdir(parents=True,exist_ok=False);d=direct(a,out)
    if a.phase=='independent':independent(d,a.first,out)
if __name__=='__main__':main()
