from __future__ import annotations
import hashlib,re
from dataclasses import dataclass
from typing import Any,Mapping
from runtime.kuuos_codeai_typed_structured_edit_ir_v0_1 import (
 IR_DIGEST_FIELD,RECEIPT_DIGEST_FIELD as TYPED_IR_RECEIPT_DIGEST_FIELD,
 OP_CREATE_FILE,OP_REPLACE_SYMBOL,OP_INSERT_BEFORE_SYMBOL,OP_INSERT_AFTER_SYMBOL,OP_DELETE_SYMBOL,
 canonical_digest,canonical_json,digest_without,seal)
VERSION='kuuos_codeai_candidate_static_admissibility_preflight_v0_1'; SCHEMA_VERSION='v0.1'; PROFILE_VERSION='CodeAI Candidate Static Admissibility Preflight v0.1'
STATUS_READY='ready'; STATUS_BLOCKED='blocked'; MODE_PREFLIGHT_ONLY='static_preflight_only'
DISPOSITION_ADMISSIBLE='candidate_static_admissibility_confirmed'; DISPOSITION_REPAIRABLE='candidate_static_preflight_repair_required'; DISPOSITION_HOLD='candidate_static_preflight_held'; DISPOSITION_REJECTED='candidate_static_preflight_rejected'
REQUEST_DIGEST_FIELD='codeai_candidate_static_admissibility_preflight_request_digest'; POLICY_DIGEST_FIELD='codeai_candidate_static_admissibility_preflight_policy_digest'; DEPENDENCY_INVENTORY_DIGEST_FIELD='codeai_candidate_dependency_inventory_digest'; TEST_PLAN_CATALOG_DIGEST_FIELD='codeai_candidate_test_plan_catalog_digest'; REPORT_DIGEST_FIELD='codeai_candidate_static_admissibility_report_digest'; RECEIPT_DIGEST_FIELD='codeai_candidate_static_admissibility_preflight_receipt_digest'
SEVERITY_REPAIRABLE='repairable'; SEVERITY_HOLD='hold'; SEVERITY_REJECT='reject'
OPS={OP_CREATE_FILE,OP_REPLACE_SYMBOL,OP_INSERT_BEFORE_SYMBOL,OP_INSERT_AFTER_SYMBOL,OP_DELETE_SYMBOL}; LANGS={'python','lean'}
SHA40=re.compile(r'^[0-9a-f]{40}$'); SHA256=re.compile(r'^[0-9a-f]{64}$')
@dataclass(frozen=True)
class CodeAICandidateStaticAdmissibilityPreflightResult:
 status:str; issues:tuple[str,...]; report:dict[str,Any]|None; receipt:dict[str,Any]|None

def mapping(x): return x if isinstance(x,Mapping) else None
def canonical_path(p): return isinstance(p,str) and p and not p.startswith('/') and not p.endswith('/') and not any(c in p for c in ('\\','\0','\n','\r')) and all(x not in ('','.','..') for x in p.split('/'))
def canonical_text(x): return isinstance(x,str) and '\0' not in x and '\r' not in x and (not x or x.endswith('\n'))
def strings(x,nonempty=False): return isinstance(x,list) and all(isinstance(v,str) and v for v in x) and len(x)==len(set(x)) and (bool(x) or not nonempty)
def digest_ok(x,f): return isinstance(x.get(f),str) and SHA256.fullmatch(x[f]) and x[f]==digest_without(x,f)
def has_prefix(p,q): q=q.rstrip('/'); return p==q or p.startswith(q+'/')
def path_allowed(p,pol): return any(has_prefix(p,q) for q in pol['allowed_repository_path_prefixes']) and not any(has_prefix(p,q) for q in pol['forbidden_repository_path_prefixes'])
def snapshot_size(repo): return len(canonical_json(repo).encode())
def file_digest(s): return hashlib.sha256(s.encode()).hexdigest()
def finding(code,severity,path='',operation_id='',detail=''): return {'code':code,'severity':severity,'path':path,'operation_id':operation_id,'detail':detail}

def validate_inputs(ir,rr,repo,req,pol,inv,cat):
 issues=[]
 try:
  for obj,f,n in ((ir,IR_DIGEST_FIELD,'typed_ir'),(rr,TYPED_IR_RECEIPT_DIGEST_FIELD,'typed_ir_receipt'),(req,REQUEST_DIGEST_FIELD,'preflight_request'),(pol,POLICY_DIGEST_FIELD,'preflight_policy'),(inv,DEPENDENCY_INVENTORY_DIGEST_FIELD,'dependency_inventory'),(cat,TEST_PLAN_CATALOG_DIGEST_FIELD,'test_plan_catalog')):
   if not digest_ok(obj,f): issues.append(n+'_digest_mismatch')
  if ir['codeai_disposition']!='typed_structured_edit_ir_normalized' or ir['operating_mode']!='typed_ir_only': issues.append('typed_ir_state_invalid')
  for f in ('typed_operations_only','symbol_preconditions_verified','context_lineage_verified','repository_snapshot_read_only'):
   if ir[f] is not True: issues.append('typed_ir_required_true:'+f)
  for f in ('whole_file_modify_allowed','provider_invoked','verification_runner_invoked','repository_mutation_performed','git_effect_performed','candidate_selection_authority_granted','execution_authority_granted'):
   if ir[f] is not False: issues.append('typed_ir_required_false:'+f)
  if not SHA40.fullmatch(ir['source_commit_sha']) or not SHA256.fullmatch(ir['repository_snapshot_digest']): issues.append('typed_ir_identity_invalid')
  ops=ir['operations']
  if not isinstance(ops,list) or not ops or ir['operation_count']!=len(ops): issues.append('typed_ir_operations_invalid')
  else:
   ids=[]; seq=[]
   for i,o in enumerate(ops):
    if not isinstance(o,Mapping): issues.append(f'typed_ir_operation[{i}]_not_mapping'); continue
    ids.append(o['operation_id']); seq.append(o['application_sequence'])
    if o['operation'] not in OPS or o['language'] not in LANGS or not canonical_path(o['path']) or not canonical_text(o['new_text']): issues.append(f'typed_ir_operation[{i}]_invalid')
    if o['new_text_digest']!=file_digest(o['new_text']) or o['new_text_bytes']!=len(o['new_text'].encode()): issues.append(f'typed_ir_operation[{i}]_new_text_mismatch')
    for f in ('requirement_trace_ids','test_plan_ids','risk_labels'):
     if not strings(o[f]): issues.append(f'typed_ir_operation[{i}]_{f}_invalid')
   if len(ids)!=len(set(ids)): issues.append('typed_ir_duplicate_operation_id')
   if sorted(seq)!=list(range(1,len(ops)+1)): issues.append('typed_ir_application_sequence_not_contiguous')
  if rr['codeai_disposition']!='typed_structured_edit_ir_normalized' or rr['operating_mode']!='typed_ir_only': issues.append('typed_ir_receipt_state_invalid')
  for f in ('route_receipt_recorded','typed_structured_edit_ir_emitted','repository_snapshot_read_only'):
   if rr[f] is not True: issues.append('typed_ir_receipt_required_true:'+f)
  for f in ('provider_invoked','verification_runner_invoked','repository_mutation_performed','git_effect_performed','candidate_selection_authority_granted','execution_authority_granted'):
   if rr[f] is not False: issues.append('typed_ir_receipt_required_false:'+f)
  if not strings(rr['operation_ids'],True) or not strings(rr['target_paths'],True): issues.append('typed_ir_receipt_accounting_invalid')
  for p,c in repo.items():
   if not canonical_path(p) or not canonical_text(c): issues.append('repository_invalid:'+str(p))
  for f in ('expected_typed_edit_ir_digest','expected_typed_edit_ir_receipt_digest','expected_repository_snapshot_digest','dependency_inventory_digest','test_plan_catalog_digest'):
   if not SHA256.fullmatch(req[f]): issues.append('preflight_request_digest_invalid:'+f)
  if not SHA40.fullmatch(req['source_commit_sha']) or not isinstance(req['claims_authority'],bool) or not isinstance(req['request_created_epoch'],int): issues.append('preflight_request_invalid')
  for f in ('required_test_plan_ids','prior_preflight_receipt_digests','unresolved_preflight_questions'):
   if not strings(req[f]): issues.append('preflight_request_'+f+'_invalid')
  if not SHA40.fullmatch(pol['expected_source_commit_sha']): issues.append('preflight_policy_source_commit_invalid')
  for f in ('allowed_repository_path_prefixes','allowed_languages'):
   if not strings(pol[f],True): issues.append('preflight_policy_'+f+'_invalid')
  for f in ('forbidden_repository_path_prefixes','allowed_external_python_modules','allowed_external_lean_import_prefixes','forbidden_new_text_markers'):
   if not strings(pol[f]): issues.append('preflight_policy_'+f+'_invalid')
  for f in ('maximum_operations','maximum_changed_paths','maximum_source_snapshot_bytes','maximum_result_snapshot_bytes','maximum_findings','maximum_request_age'):
   if not isinstance(pol[f],int) or isinstance(pol[f],bool) or pol[f]<=0: issues.append('preflight_policy_'+f+'_invalid')
  if any(x not in LANGS for x in pol['allowed_languages']): issues.append('preflight_policy_language_invalid')
  for f in ('require_exact_ir_lineage','require_materialized_parse','require_internal_python_import_resolution','require_internal_lean_import_resolution','require_test_plan_correspondence','allow_repository_mutation','allow_provider_invocation','allow_verification_runner_invocation','allow_candidate_selection_authority','allow_execution_authority'):
   if not isinstance(pol[f],bool): issues.append('preflight_policy_'+f+'_invalid')
  if inv['schema_version']!=SCHEMA_VERSION or not SHA256.fullmatch(inv['repository_snapshot_digest']) or not strings(inv['python_external_modules']) or not strings(inv['lean_external_import_prefixes']): issues.append('dependency_inventory_invalid')
  if cat['schema_version']!=SCHEMA_VERSION or not SHA256.fullmatch(cat['repository_snapshot_digest']) or not isinstance(cat['plans'],list): issues.append('test_plan_catalog_invalid')
  else:
   seen=set()
   for i,p in enumerate(cat['plans']):
    if not isinstance(p,Mapping) or not isinstance(p.get('test_plan_id'),str) or not p.get('test_plan_id') or p.get('test_plan_id') in seen or not strings(p.get('covered_path_prefixes'),True) or not strings(p.get('languages'),True) or not isinstance(p.get('evidence_kind'),str) or not p.get('evidence_kind'): issues.append(f'test_plan_catalog_plan[{i}]_invalid')
    else: seen.add(p['test_plan_id'])
 except (KeyError,TypeError,AttributeError): issues.append('required_field_missing_or_invalid')
 return sorted(set(issues))
