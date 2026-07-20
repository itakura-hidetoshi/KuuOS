from __future__ import annotations

import copy, json, unittest
from pathlib import Path
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import DECISION_ABSTAINED, DECISION_DIGEST_FIELD as SD, REASON_NO_ELIGIBLE, RECEIPT_DIGEST_FIELD as SR
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import MEMORY_SNAPSHOT_DIGEST_FIELD as MD, RECEIPT_DIGEST_FIELD as MR
from runtime.kuuos_codeai_maintainability_trajectory_gate_schema_v0_1 import DECISION_DIGEST_FIELD, EVIDENCE_PACKET_DIGEST_FIELD as PD, EVIDENCE_RECORD_DIGEST_FIELD as RD, GATE_ADMITTED, GATE_HELD, POLICY_DIGEST_FIELD, REASON_AXIS_LIMIT, REASON_INSUFFICIENT_IMPROVEMENT, REASON_TOTAL_REGRESSION, RECEIPT_DIGEST_FIELD, REQUEST_DIGEST_FIELD, STATUS_BLOCKED, STATUS_READY, canonical_digest, seal
from runtime.kuuos_codeai_maintainability_trajectory_gate_v0_1 import build_codeai_maintainability_trajectory_gate as build
from scripts.build_codeai_maintainability_trajectory_gate_fixture_v0_1 import build_fixture

ROOT=Path(__file__).resolve().parents[1]
def fixture():
    load=lambda p: json.loads((ROOT/p).read_text(encoding='utf-8'))
    return build_fixture(load('examples/codeai_maintainability_trajectory_gate_v0_1.json'),load('examples/codeai_evidence_weighted_selection_abstention_v0_1.json'),load('examples/codeai_independent_test_strengthening_v0_1.json'),load('examples/codeai_version_bound_repair_memory_v0_1.json'),load('examples/codeai_typed_error_classification_v0_1.json'),load('examples/codeai_evidence_bearing_candidate_portfolio_v0_1.json'),load('examples/codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json'))
def run(d): return build(**d)
def rq(d): d['gate_request']=seal(d['gate_request'],REQUEST_DIGEST_FIELD)
def rp(d): d['gate_policy']=seal(d['gate_policy'],POLICY_DIGEST_FIELD)
def pk(d):
    p=seal(d['trajectory_evidence_packet'],PD); d['trajectory_evidence_packet']=p; x=p[PD]
    d['gate_request']['trajectory_evidence_packet_digest']=x; d['gate_policy']['expected_trajectory_evidence_packet_digest']=x; rq(d); rp(d)
def rr(d,i=0): d['trajectory_evidence_packet']['records'][i]=seal(d['trajectory_evidence_packet']['records'][i],RD); pk(d)
def memory(d):
    m=seal(d['memory_snapshot'],MD); d['memory_snapshot']=m; r=d['memory_receipt']; r['version_bound_repair_memory_snapshot_digest']=m[MD]
    for f in ('repository_full_name','source_commit_sha','memory_entry_count','matched_entry_count','excluded_entry_count','recommendation'): r[f]=m[f]
    r=seal(r,MR); d['memory_receipt']=r; p=d['trajectory_evidence_packet']; p['memory_snapshot_digest']=m[MD]; p['memory_receipt_digest']=r[MR]
    d['gate_request']['memory_snapshot_digest']=m[MD]; d['gate_request']['memory_receipt_digest']=r[MR]; d['gate_policy']['expected_memory_snapshot_digest']=m[MD]; d['gate_policy']['expected_memory_receipt_digest']=r[MR]; pk(d)
def abstain(d):
    x=d['selection_decision']; x.update(decision=DECISION_ABSTAINED,decision_reason=REASON_NO_ELIGIBLE,selected_candidate_id='',selected_candidate_digest='',candidate_selected=False,abstention_recorded=True,selection_authority_exercised=False); x=seal(x,SD); d['selection_decision']=x
    r=d['selection_receipt']; r.update(decision_digest=x[SD],decision=DECISION_ABSTAINED,decision_reason=REASON_NO_ELIGIBLE,selected_candidate_id='',candidate_selected=False,abstention_recorded=True,selection_authority_exercised=False); r=seal(r,SR); d['selection_receipt']=r
    p=d['trajectory_evidence_packet']; p['selection_decision_digest']=x[SD]; p['selection_receipt_digest']=r[SR]
    d['gate_request']['selection_decision_digest']=x[SD]; d['gate_request']['selection_receipt_digest']=r[SR]; d['gate_policy']['expected_selection_decision_digest']=x[SD]; d['gate_policy']['expected_selection_receipt_digest']=r[SR]; pk(d)

class Tests(unittest.TestCase):
    def test_reference(self):
        r=run(fixture()); self.assertEqual((r.status,r.decision['gate_decision'],r.decision['axis_count'],r.decision['improved_axis_count'],r.decision['total_regression'],r.decision['exceeded_axis_count'],r.decision['memory_hint_available']),(STATUS_READY,GATE_ADMITTED,6,3,3,0,False))
    def test_deterministic(self):
        d=fixture(); a,b=run(d),run(copy.deepcopy(d)); self.assertEqual((a.decision,a.receipt),(b.decision,b.receipt)); self.assertEqual(a.decision[DECISION_DIGEST_FIELD],seal(a.decision,DECISION_DIGEST_FIELD)[DECISION_DIGEST_FIELD]); self.assertEqual(a.receipt[RECEIPT_DIGEST_FIELD],seal(a.receipt,RECEIPT_DIGEST_FIELD)[RECEIPT_DIGEST_FIELD])
    def test_axes(self):
        a={x['axis']:x for x in run(fixture()).decision['axis_assessments']}; self.assertEqual((a['dependency_surface']['regression_amount'],a['test_burden']['regression_amount']),(1,2)); self.assertTrue(all(a[x]['improved'] for x in ('structural_complexity','duplication','repair_recurrence')))
    def test_memory_no_waiver(self):
        d=fixture(); x=d['trajectory_evidence_packet']['records'][0]; x['candidate_value']=x['baseline_value']+1; x['observed_delta']=1; rr(d); r=run(d); self.assertEqual(r.decision['gate_decision'],GATE_HELD); self.assertIn(REASON_AXIS_LIMIT,r.decision['decision_reasons']); self.assertFalse(r.decision['memory_hint_available']); self.assertFalse(r.decision['memory_hint_used_as_threshold_waiver'])
    def test_axis_hold(self):
        d=fixture(); x=d['trajectory_evidence_packet']['records'][2]; x['candidate_value']=x['baseline_value']+1; x['observed_delta']=1; rr(d,2); r=run(d); self.assertEqual(r.decision['gate_decision'],GATE_HELD); self.assertIn('duplication',r.decision['exceeded_axes'])
    def test_total_hold(self):
        d=fixture(); d['gate_policy']['maximum_total_regression']=2; rp(d); r=run(d); self.assertEqual(r.decision['gate_decision'],GATE_HELD); self.assertIn(REASON_TOTAL_REGRESSION,r.decision['decision_reasons'])
    def test_improvement_hold(self):
        d=fixture()
        for i in (0,2,5):
            x=d['trajectory_evidence_packet']['records'][i]; x['candidate_value']=x['baseline_value']; x['observed_delta']=0; d['trajectory_evidence_packet']['records'][i]=seal(x,RD)
        pk(d); r=run(d); self.assertEqual(r.decision['gate_decision'],GATE_HELD); self.assertIn(REASON_INSUFFICIENT_IMPROVEMENT,r.decision['decision_reasons'])
    def test_boundaries(self):
        r=run(fixture()).decision
        for f in ('memory_hint_used_as_threshold_waiver','historical_repair_outcome_used_as_probability','test_execution_performed_by_kernel','repair_executed','repository_mutation_performed','git_effect_performed','selection_authority_granted','verification_authority_granted','repair_authority_granted','execution_authority_granted','git_authority_granted','bounded_measurement_treated_as_future_proof','maintainability_gate_treated_as_correctness_proof','maintainability_gate_treated_as_probability','held_treated_as_rejection'): self.assertFalse(r[f],f)
    def test_windows(self):
        for c,f,s in (('gate_request','request_created_epoch',rq),('trajectory_evidence_packet','evidence_created_epoch',pk)):
            for v in (1,fixture()['gate_policy']['evaluation_epoch']+1):
                d=fixture(); d[c][f]=v; s(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_roles(self):
        for t,s in (('independent_assessor_id','candidate_producer_id'),('independent_reviewer_id','candidate_producer_id'),('independent_reviewer_id','independent_assessor_id')):
            d=fixture(); d['trajectory_evidence_packet'][t]=d['trajectory_evidence_packet'][s]; pk(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_delta(self):
        d=fixture(); d['trajectory_evidence_packet']['records'][0]['observed_delta']+=1; rr(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_memory_binding(self):
        d=fixture(); d['memory_snapshot']['query_version_binding']['source_candidate_digest']=canonical_digest({'different':'candidate'}); memory(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_abstained(self):
        d=fixture(); abstain(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    def test_axis_order(self):
        d=fixture(); a=d['trajectory_evidence_packet']['records']; a[0],a[1]=a[1],a[0]; pk(d); self.assertEqual(run(d).status,STATUS_BLOCKED)

def install():
    def add(name,fn): setattr(Tests,name,fn)
    for f in ('selection_decision','selection_receipt','memory_snapshot','memory_receipt','trajectory_evidence_packet','gate_request','gate_policy'):
        add('test_non_mapping_'+f,lambda self,f=f: self.assertEqual(run({**fixture(),f:[]}).status,STATUS_BLOCKED))
    for c,f,v in (('gate_request','gate_request_id','x'),('gate_policy','maximum_trajectory_records',999),('trajectory_evidence_packet','record_count',999),('selection_decision','candidate_count',999),('selection_receipt','candidate_count',999),('memory_snapshot','matched_entry_count',999),('memory_receipt','matched_entry_count',999)):
        def t(self,c=c,f=f,v=v): d=fixture(); d[c][f]=v; self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_tampered_'+c+'_'+f,t)
    for f in ('require_source_selection_selected','require_exact_lineage','require_complete_axis_coverage','require_independent_assessor','require_independent_reviewer','require_isolated_candidate_evaluation','require_source_correspondence','require_exact_memory_binding','require_live_repository_unchanged','allow_maintainability_gate_decision'):
        def t(self,f=f): d=fixture(); d['gate_policy'][f]=False; rp(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_required_'+f,t)
    for f in ('allow_memory_threshold_waiver','allow_test_execution','allow_repair_execution','allow_repository_mutation','allow_selection_authority','allow_verification_authority','allow_repair_authority','allow_execution_authority','allow_git_authority'):
        def t(self,f=f): d=fixture(); d['gate_policy'][f]=True; rp(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_forbidden_'+f,t)
    for f in ('external_measurement_reported','independent_assessor_verified','independent_reviewer_verified','isolated_candidate_evaluation_verified','source_correspondence_verified','live_repository_unchanged'):
        def t(self,f=f): d=fixture(); d['trajectory_evidence_packet'][f]=False; pk(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_packet_false_'+f,t)
    for f in ('completed','external_measurement','independent_assessor','independent_reviewer','isolated_candidate_evaluation','source_correspondence'):
        def t(self,f=f): d=fixture(); d['trajectory_evidence_packet']['records'][0][f]=False; rr(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_record_false_'+f,t)
    for f in ('claims_selection_authority','claims_verification_authority','claims_repair_authority','claims_execution_authority','claims_git_authority'):
        def t(self,f=f): d=fixture(); d['gate_request'][f]=True; rq(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_claim_'+f,t)
    for f in ('expected_selection_decision_digest','expected_selection_receipt_digest','expected_memory_snapshot_digest','expected_memory_receipt_digest','expected_trajectory_evidence_packet_digest','expected_repository_full_name','expected_source_commit_sha','expected_source_repository_snapshot_digest','expected_selected_candidate_id','expected_selected_candidate_digest'):
        def t(self,f=f):
            d=fixture(); cur=d['gate_policy'][f]
            d['gate_policy'][f]=('f'*40 if f=='expected_source_commit_sha' else str(cur)+'-x' if f in ('expected_repository_full_name','expected_selected_candidate_id') else canonical_digest({'mismatch':f})); rp(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_policy_mismatch_'+f,t)
    for f in ('candidate_producer_involved_in_measurement','repository_mutation_performed','git_effect_performed'):
        def t(self,f=f): d=fixture(); d['trajectory_evidence_packet'][f]=True; pk(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_packet_forbidden_'+f,t)
    for f in ('candidate_producer_involved','repository_mutation_performed','git_effect_performed'):
        def t(self,f=f): d=fixture(); d['trajectory_evidence_packet']['records'][0][f]=True; rr(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
        add('test_record_forbidden_'+f,t)
    def budget(self): d=fixture(); d['gate_policy']['maximum_trajectory_records']=1; rp(d); self.assertEqual(run(d).status,STATUS_BLOCKED)
    add('test_record_budget',budget)
install()
if __name__=='__main__': unittest.main()
