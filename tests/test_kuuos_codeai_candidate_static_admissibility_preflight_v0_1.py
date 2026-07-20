from __future__ import annotations
import copy, hashlib, json, unittest
from pathlib import Path
from runtime.kuuos_codeai_candidate_static_admissibility_preflight_v0_1 import *

EXAMPLE=Path(__file__).resolve().parents[1]/'examples/codeai_candidate_static_admissibility_preflight_v0_1.json'

def fixture():
    data=json.loads(EXAMPLE.read_text())
    data.pop('expected_report',None); data.pop('expected_receipt',None)
    data.pop('profile_version',None); data.pop('schema_version',None)
    return data

def reseal(data):
    repo=data['repository_files']; rd=canonical_digest(repo)
    ir=data['typed_edit_ir']
    for op in ir['operations']:
        op['new_text_digest']=hashlib.sha256(op['new_text'].encode()).hexdigest(); op['new_text_bytes']=len(op['new_text'].encode())
    ir['operation_count']=len(ir['operations']); ir['total_new_text_bytes']=sum(x['new_text_bytes'] for x in ir['operations']); ir['repository_snapshot_digest']=rd
    data['typed_edit_ir']=seal(ir,IR_DIGEST_FIELD); ir=data['typed_edit_ir']
    rr=data['typed_edit_ir_receipt']; rr['typed_edit_ir_digest']=ir[IR_DIGEST_FIELD]; rr['repository_snapshot_digest']=rd; rr['operation_count']=len(ir['operations']); rr['operation_ids']=[x['operation_id'] for x in ir['operations']]; rr['target_paths']=sorted({x['path'] for x in ir['operations']}); rr['total_new_text_bytes']=ir['total_new_text_bytes']
    data['typed_edit_ir_receipt']=seal(rr,TYPED_IR_RECEIPT_DIGEST_FIELD); rr=data['typed_edit_ir_receipt']
    inv=data['dependency_inventory']; inv['repository_snapshot_digest']=rd; data['dependency_inventory']=seal(inv,DEPENDENCY_INVENTORY_DIGEST_FIELD)
    cat=data['test_plan_catalog']; cat['repository_snapshot_digest']=rd; data['test_plan_catalog']=seal(cat,TEST_PLAN_CATALOG_DIGEST_FIELD)
    req=data['preflight_request']; req['expected_typed_edit_ir_digest']=ir[IR_DIGEST_FIELD]; req['expected_typed_edit_ir_receipt_digest']=rr[TYPED_IR_RECEIPT_DIGEST_FIELD]; req['expected_repository_snapshot_digest']=rd; req['dependency_inventory_digest']=data['dependency_inventory'][DEPENDENCY_INVENTORY_DIGEST_FIELD]; req['test_plan_catalog_digest']=data['test_plan_catalog'][TEST_PLAN_CATALOG_DIGEST_FIELD]
    data['preflight_request']=seal(req,REQUEST_DIGEST_FIELD)
    data['preflight_policy']=seal(data['preflight_policy'],POLICY_DIGEST_FIELD)

def run(data):
    return build_codeai_candidate_static_admissibility_preflight(
        typed_edit_ir=data['typed_edit_ir'],typed_edit_ir_receipt=data['typed_edit_ir_receipt'],repository_files=data['repository_files'],preflight_request=data['preflight_request'],preflight_policy=data['preflight_policy'],dependency_inventory=data['dependency_inventory'],test_plan_catalog=data['test_plan_catalog'])

def set_text(data,text): data['typed_edit_ir']['operations'][0]['new_text']=text; reseal(data)
def create_op(path,text,lang='python',oid='create'):
    return {'operation_id':oid,'operation':'create_file','path':path,'language':lang,'precondition_kind':'path_absent','anchor_kind':'','anchor_symbol':'','resolved_start_line':0,'resolved_end_line':0,'application_start_line':0,'application_end_line':0,'file_digest':'','anchor_digest':'','context_entry_content_digest':'','new_text':text,'new_text_digest':'','new_text_bytes':0,'requirement_trace_ids':['REQ-new'],'test_plan_ids':['test:greet'],'risk_labels':['low'],'application_sequence':1}

class StaticPreflightTests(unittest.TestCase):
    def test_01_example_admissible(self): self.assertEqual(run(fixture()).report['codeai_disposition'],DISPOSITION_ADMISSIBLE)
    def test_02_receipt_effect_free(self):
        r=run(fixture()).receipt
        for f in ('provider_invoked','verification_runner_invoked','repository_mutation_performed','git_effect_performed','candidate_selected','execution_authority_granted'): self.assertFalse(r[f])
    def test_03_ephemeral_result(self): self.assertTrue(run(fixture()).report['result_snapshot_ephemeral'])
    def test_04_report_receipt_digests(self):
        x=run(fixture()); self.assertEqual(x.report[REPORT_DIGEST_FIELD],digest_without(x.report,REPORT_DIGEST_FIELD)); self.assertEqual(x.receipt[RECEIPT_DIGEST_FIELD],digest_without(x.receipt,RECEIPT_DIGEST_FIELD))
    def test_05_syntax_repairable(self):
        d=fixture(); set_text(d,'def greet(:\n'); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_06_external_dependency_hold(self):
        d=fixture(); set_text(d,"import requests\n\ndef greet(name: str) -> str:\n    return name\n"); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_HOLD)
    def test_07_collision_rejected(self):
        d=fixture(); op=copy.deepcopy(d['typed_edit_ir']['operations'][0]); op['operation_id']='second'; op['application_sequence']=2; d['typed_edit_ir']['operations'].append(op); reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REJECTED)
    def test_08_forbidden_marker_repairable(self):
        d=fixture(); set_text(d,"def greet(name: str) -> str:\n    # TODO\n    return name\n"); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_09_missing_test_repairable(self):
        d=fixture(); d['test_plan_catalog']['plans']=[]; reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_10_no_effect_repairable(self):
        d=fixture(); set_text(d,"def greet(name: str) -> str:\n    return 'hello ' + name\n"); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_11_create_admissible(self):
        d=fixture(); d['typed_edit_ir']['operations']=[create_op('runtime/new.py','def created() -> int:\n    return 1\n')]; reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_ADMISSIBLE)
    def test_12_internal_import_repairable(self):
        d=fixture(); set_text(d,"from runtime.missing import x\n\ndef greet(name: str) -> str:\n    return str(x)+name\n"); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_13_lean_external_hold(self):
        d=fixture(); op=create_op('formal/KUOS/New.lean','import Foo.Bar\n\ndef x : Nat := 1\n','lean'); d['typed_edit_ir']['operations']=[op]; d['test_plan_catalog']['plans'].append({'test_plan_id':'test:lean','covered_path_prefixes':['formal'],'languages':['lean'],'evidence_kind':'formal'}); d['preflight_request']['required_test_plan_ids']=['test:lean']; op['test_plan_ids']=['test:lean']; reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_HOLD)
    def test_14_lean_balance_repairable(self):
        d=fixture(); op=create_op('formal/KUOS/New.lean','import Mathlib\n\ndef x : Nat := (\n  1\n','lean'); d['typed_edit_ir']['operations']=[op]; d['test_plan_catalog']['plans'].append({'test_plan_id':'test:lean','covered_path_prefixes':['formal'],'languages':['lean'],'evidence_kind':'formal'}); d['preflight_request']['required_test_plan_ids']=['test:lean']; op['test_plan_ids']=['test:lean']; reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_REPAIRABLE)
    def test_15_test_check_disabled(self):
        d=fixture(); d['test_plan_catalog']['plans']=[]; d['preflight_policy']['require_test_plan_correspondence']=False; reseal(d); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_ADMISSIBLE)
    def test_16_external_policy_allows(self):
        d=fixture(); d['preflight_policy']['allowed_external_python_modules']=['requests']; set_text(d,"import requests\n\ndef greet(name: str) -> str:\n    return name\n"); self.assertEqual(run(d).report['codeai_disposition'],DISPOSITION_ADMISSIBLE)
    def test_17_invalid_repository_path_blocks(self):
        d=fixture(); d['repository_files']['../bad.py']='x=1\n'; self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_18_noncontiguous_sequence_blocks(self):
        d=fixture(); d['typed_edit_ir']['operations'][0]['application_sequence']=2; reseal(d); self.assertEqual(run(d).status,STATUS_BLOCKED)

def corrupt(field):
    def test(self):
        d=fixture(); obj,key=field; d[obj][key]='0'*64; self.assertEqual(run(d).status,STATUS_BLOCKED)
    return test
for i,(obj,key) in enumerate((('typed_edit_ir',IR_DIGEST_FIELD),('typed_edit_ir_receipt',TYPED_IR_RECEIPT_DIGEST_FIELD),('preflight_request',REQUEST_DIGEST_FIELD),('preflight_policy',POLICY_DIGEST_FIELD),('dependency_inventory',DEPENDENCY_INVENTORY_DIGEST_FIELD),('test_plan_catalog',TEST_PLAN_CATALOG_DIGEST_FIELD)),19): setattr(StaticPreflightTests,f'test_{i:02d}_digest_block',corrupt((obj,key)))

def effect(field):
    def test(self):
        d=fixture(); d['preflight_policy'][field]=True; d['preflight_policy']=seal(d['preflight_policy'],POLICY_DIGEST_FIELD); self.assertEqual(run(d).status,STATUS_BLOCKED)
    return test
for i,f in enumerate(('allow_repository_mutation','allow_provider_invocation','allow_verification_runner_invocation','allow_candidate_selection_authority','allow_execution_authority'),25): setattr(StaticPreflightTests,f'test_{i:02d}_effect_block',effect(f))

def simple(case):
    def test(self):
        d=fixture()
        if case=='authority': d['preflight_request']['claims_authority']=True; d['preflight_request']=seal(d['preflight_request'],REQUEST_DIGEST_FIELD)
        elif case=='question': d['preflight_request']['unresolved_preflight_questions']=['q']; d['preflight_request']=seal(d['preflight_request'],REQUEST_DIGEST_FIELD)
        elif case=='stale': d['preflight_request']['request_created_epoch']=1; d['preflight_request']=seal(d['preflight_request'],REQUEST_DIGEST_FIELD)
        elif case=='forbid': d['preflight_policy']['forbidden_repository_path_prefixes']=['runtime']; d['preflight_policy']=seal(d['preflight_policy'],POLICY_DIGEST_FIELD)
        elif case=='language': d['preflight_policy']['allowed_languages']=['lean']; d['preflight_policy']=seal(d['preflight_policy'],POLICY_DIGEST_FIELD)
        elif case=='source_budget': d['preflight_policy']['maximum_source_snapshot_bytes']=1; d['preflight_policy']=seal(d['preflight_policy'],POLICY_DIGEST_FIELD)
        elif case=='result_budget': d['preflight_policy']['maximum_result_snapshot_bytes']=1; d['preflight_policy']=seal(d['preflight_policy'],POLICY_DIGEST_FIELD)
        self.assertEqual(run(d).status,STATUS_BLOCKED)
    return test
for i,c in enumerate(('authority','question','stale','forbid','language','source_budget','result_budget'),30): setattr(StaticPreflightTests,f'test_{i:02d}_{c}_block',simple(c))

if __name__=='__main__': unittest.main()
