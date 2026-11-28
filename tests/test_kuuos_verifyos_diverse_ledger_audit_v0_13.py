"""Frozen-profile fixtures, actual signed subprocess pairs, common-mode falsification."""
import copy
from pathlib import Path
import shutil
import tempfile
import unittest
from runtime import kuuos_verifyos_diverse_ledger_audit_v0_13 as g
from runtime import kuuos_verifyos_execution_witness_v0_12 as w

u=w.g; b,p=u.b,u.p


def build(root, mode='correct'):
    for name in ('base','gates','ledger'): (root/name).mkdir(parents=True,exist_ok=True)
    rules=[dict(identity=f'r{i}',tier='A',source=dict(source_head='1'*40,blob='2'*40),scope='fixed scope',premises=['premise']) for i in range(10)]
    marks=dict(main_observed='3'*40,main_reported_substantive='4'*40,research_observed_head='5'*40)
    base=dict(schema='kuuos.native-gpt.continuity.v15',repository=g.REPO,pins=g.PINS,rules=rules,checkpoints={**marks,'research_scoped_verified':['6'*40,'7'*40]})
    for name in g.BASE: (root/name).write_bytes(g.canonical(base) if name==g.REGISTRY else b'fixture')
    binding=dict(rule_sha256=g.sha(g.canonical(rules[0])),source_head='1'*40,blob='2'*40,scope='fixed scope',pins=g.PINS)
    observed=dict(source_head='1'*40,blob='2'*40,scope='fixed scope',pins=g.PINS,scope_status='MATCH',source_evidence=['source'],scope_evidence=['scope'],exclusion_status='CLEAR',exclusion_evidence=['exclusion'],premise_checks=[dict(premise='premise',status='SATISFIED',evidence=['premise'])])
    review=dict(schema='kuuos.native-gpt.scope-review.v16.1',review_id='r1',rule_identity='r0',binding=binding,observed=observed,status='CONDITIONAL_REUSE_CANDIDATE_ONLY',disposition='CANDIDATE_ONLY',evidence_kind='LOCAL_FIXTURE',proof_authority=False,action_authority=False)
    events=[]; parent='0'*64
    for i in range(2):
        ev=dict(schema='kuuos.native-gpt.ledger.v16',repository=g.REPO,pins=g.PINS,seq=i,parent_sha256=parent,kind='GENESIS' if i==0 else 'DAILY_RUN',run_id=f'run{i}',observed_at='2026-11-28T10:00:00+09:00',proof_authority=False,action_authority=False,pb16_executed=0,base_registry_sha256=g.sha((root/g.REGISTRY).read_bytes()),transitions=[],new_rules=[],withdrawals=[],research_certificates=[],notification_intents=[],obstructions=[dict(id=f'obs{i}',scope='scope',reason='hold',kind='OPERATIONAL_HOLD')],checks=[],observation={},backlog_notes=[])
        if i:
            ev['checks']=[dict(id=f'T{j}',status='PASS',kind='LOCAL_FIXTURE',actual=True,expected=True) for j in range(1,6)]
            ev['scope_reviews']=[review,dict(review,review_id='r2',observed=None,status='HOLD_CONTEXT_NO_DATA',disposition='HOLD')]
        raw=g.canonical(ev); (root/f'ledger/{i:012d}.json').write_bytes(raw); parent=g.sha(raw); events.append(ev)
    common=dict(seq=1,tip_sha256=parent,proof_authority=False,action_authority=False)
    outputs=[dict(status='PASS_INTEGRITY_ONLY',**common,rule_count=11 if mode=='wrong_count' else 10,withdrawn_count=0,watermarks=marks,notification_intent_count=0,obstruction_count=2,research_certificate_count=2,pb16_executed=0),dict(status='PASS_SCOPE_RECORDS_ONLY',**common,reviews=dict(candidate=1,held=1,no_use=0))]
    for name,output in zip(g.GATES,outputs): (root/name).write_text('import json\nprint(json.dumps('+repr(output)+'))\n')
    inv={str(x.relative_to(root)):g.sha(x.read_bytes()) for x in root.glob('*/*')}
    req=dict(challenge='a'*64,seq=1,tip=parent,expected_hashes={k:inv[k] for k in (g.REGISTRY,*g.GATES)})
    return req,inv,events


class AuditTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); self.root=Path(tmp.name)
        self.req,self.inv,self.events=build(self.root)

    def audit(self): return g.audit(self.root,self.req,self.inv)

    def change(self, fn):
        fn(self.events[1]); path=self.root/'ledger/000000000001.json'; raw=g.canonical(self.events[1]); path.write_bytes(raw); self.inv['ledger/000000000001.json']=g.sha(raw); self.req['tip']=g.sha(raw)

    def test_reconstructed_counts_and_decisions(self):
        out=self.audit(); self.assertEqual(out['status'],'FROZEN_PROFILE_RECONSTRUCTED_ONLY'); self.assertEqual(out['outputs'][0]['rule_count'],10); self.assertEqual(out['outputs'][0]['obstruction_count'],2); self.assertEqual(out['outputs'][1]['reviews'],dict(candidate=1,held=1,no_use=0)); self.assertEqual(len(out['review_decisions']),2)

    def test_no_inherited_gate_calls(self):
        from unittest.mock import patch
        with patch.object(b,'run',side_effect=AssertionError('not independent')),patch.object(b,'verify',side_effect=AssertionError('not independent')):
            self.assertEqual(self.audit()['status'],'FROZEN_PROFILE_RECONSTRUCTED_ONLY')

    def test_wrong_hash(self):
        (self.root/g.BASE[0]).write_text('changed'); self.assertEqual(self.audit()['reason'],'INPUT_HASH_OR_SIZE_MISMATCH')

    def test_wrong_parent(self):
        self.change(lambda e:e.update(parent_sha256='f'*64)); self.assertEqual(self.audit()['reason'],'CHAIN_LINK')

    def test_outside_profile(self):
        for k in ('new_rules','withdrawals','research_certificates','notification_intents'):
            old=copy.deepcopy(self.events[1]); self.change(lambda e:e.update({k:[{}]})); self.assertEqual(self.audit()['reason'],'OUTSIDE_FROZEN_REGISTRY_PROFILE:'+k); self.change(lambda e:e.update(old))

    def test_false_pass_strict_type(self):
        self.change(lambda e:e['checks'][0].update(actual=1)); self.assertEqual(self.audit()['reason'],'FALSE_PASS')

    def test_common_false_review(self):
        self.change(lambda e:e['scope_reviews'][0]['observed'].update(exclusion_status='CHANGED')); out=self.audit(); self.assertEqual(out['reason'],'SCOPE_DECISION_DISAGREEMENT'); self.assertEqual(out['review_decisions'][-1]['recomputed'],'HOLD_EXCLUSION_CHANGED_OR_UNCONFIRMED')

    def test_duplicate_review(self):
        self.change(lambda e:e['scope_reviews'].append(e['scope_reviews'][0])); self.assertEqual(self.audit()['reason'],'REVIEW_ID')

    def test_missing_review_reason(self):
        self.change(lambda e:e.update(scope_reviews=[])); self.assertEqual(self.audit()['reason'],'NO_USE_REASON')

    def test_no_use(self):
        self.change(lambda e:e.update(scope_reviews=[],scope_no_use_reason='no use')); self.assertEqual(self.audit()['outputs'][1]['reviews'],dict(candidate=0,held=0,no_use=1))

    def test_unanchored_extra(self):
        (self.root/'ledger/000000000002.json').write_text('{}'); self.assertEqual(self.audit()['reason'],'FILE_SET_MISMATCH')

    def test_duplicate_json(self):
        path=self.root/'ledger/000000000001.json'; raw=path.read_bytes().replace(b'"seq":1',b'"seq":1,"seq":1'); path.write_bytes(raw); self.inv['ledger/000000000001.json']=g.sha(raw); self.req['tip']=g.sha(raw); self.assertEqual(self.audit()['reason'],'DUPLICATE_KEY')


class PairTests(unittest.TestCase):
    def pair(self,mode):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root=Path(tmp.name); snap=root/'primary'; req,inv,_=build(snap,mode)
        question='取得済み台帳について、検査結果を教えて。'.encode(); family=u.f.analyze(question)['family']; ctx=dict(turn_id='b'*64,question_sha256=b.sha(question),challenge=req['challenge'],request_sha256=u.v.digest(req),audience=p.AUDIENCE)
        base=b.canonical(u.v.r.empty_log(family,ctx)); seed=dict(question=question,candidate=b.canonical(family),base_request=req,base_context=ctx,base_log=base,base_anchor=b.sha(base))
        store=root/'store.sqlite'; anchor=root/'anchor.sqlite'; genesis=u.s.initialize(store,seed)['tip']; tip=u.a.initialize(store,anchor,seed,genesis)['anchor_tip']
        host=bytes(range(32)); raw,adm=p.execute_and_admit(snap,req,ctx,host); self.assertIsNotNone(adm)
        private=root/'primary.pem'; private.write_bytes(u.openssl('genpkey','-algorithm','ED25519')); pub=u.public_key(private)
        primary=u.issue(store,anchor,seed,tip,raw,adm,host,p.publish(raw,adm,req,ctx,host),private,pub,req,ctx); self.assertEqual(primary['status'],'SIGNED_SNAPSHOT_ONLY')
        other=root/'witness'; shutil.copytree(snap,other); secret=root/'witness.pem'; secret.write_bytes(u.openssl('genpkey','-algorithm','ED25519')); key=u.public_key(secret)
        policy=dict(nonce='c'*64,primary_packet_sha256=b.sha(primary['packet']),inventory=inv)
        witness=w.execute_and_issue(other,policy,req,ctx,tip,pub,key,secret); self.assertEqual(witness['status'],'SIGNED_EXECUTION_WITNESS_ONLY')
        args=dict(primary_packet=primary['packet'],primary_raw=raw,revision_log=primary['revision_log'],seed=seed,witness_packet=witness['packet'],witness_raw=witness['raw'],policy=policy,request=req,context=ctx,anchor=tip,primary_key=pub,witness_key=key)
        third=root/'independent'; shutil.copytree(snap,third); return third,args

    def test_real_pair_and_diverse_match(self):
        root,args=self.pair('correct'); out=g.verify_diverse(root,**args); self.assertEqual(out['status'],'DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY'); self.assertEqual(out['answer_status'],'AMBIGUOUS_PARTIAL'); self.assertTrue(all(out[k] is False for k in g.BOUNDARY))

    def test_real_common_mode_error_detected(self):
        root,args=self.pair('wrong_count'); out=g.verify_diverse(root,**args); self.assertEqual(out['pair']['status'],'SEPARATE_KEY_EXECUTION_REPORTS_AGREE_ONLY'); self.assertEqual(out['reason'],'COMMON_OR_LOCAL_OUTPUT_DISAGREEMENT'); self.assertEqual(len(out['differences']),2); self.assertTrue(all(x['expected']['rule_count']==10 and x['observed']['rule_count']==11 for x in out['differences']))

    def test_missing_third_snapshot(self):
        root,args=self.pair('correct'); shutil.rmtree(root); self.assertEqual(g.verify_diverse(root,**args)['reason'],'DIVERSE_AUDIT_NOT_ADMITTED')


if __name__=='__main__': unittest.main()
