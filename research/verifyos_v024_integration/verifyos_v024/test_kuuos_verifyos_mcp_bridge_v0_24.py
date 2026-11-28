"""v0.24 local protocol tests. Positive egress fixture mocks Lean; never production.
Actual v0.1 encoding reproduction, Ed25519, SQLite, host/client anchor checks.
Missing-runtime negative uses the unpatched real host execution entry point.
"""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
import copy, json, tempfile, threading, unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_mcp_bridge_v0_24 as m
from test_kuuos_verifyos_closed_surface_v0_18_r2 import view
x,d,e,p,g=m.x,m.d,m.e,m.p,m.g

# Independent reproduction of the fetched v0.1 canonical function.
def v01(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def fixture(n=1):
    question='取得済み台帳について、検査結果を教えて。'.encode()
    req={'challenge':'a'*64,'seq':1,'tip':'b'*64,
         'expected_hashes':{k:f'{i:064x}' for i,k in enumerate(sorted(m.HASH_KEYS),1)}}
    ctx={'turn_id':f'{n:064x}','question_sha256':g.sha(question),'challenge':req['challenge'],
         'request_sha256':g.sha(v01(req)),'audience':'private_verification_channel'}
    return question,req,ctx


def ingress(n=1):
    question,req,ctx=fixture(n); return question,v01(req),v01(ctx)


class EncodingTests(unittest.TestCase):
    def test_old_actual_ingress_failure(self):
        with self.assertRaisesRegex(ValueError,'NONCANONICAL'): p.exact_turn(*ingress())
    def test_upstream_exact_bytes_preserved(self):
        q,req,ctx=ingress(); t=m.exact_turn(q,req,ctx)
        self.assertEqual(t.request_sha256,g.sha(req)); self.assertEqual(t.context_sha256,g.sha(ctx))
        self.assertEqual(t.question_sha256,g.sha(q)); self.assertEqual(m.upstream_canonical(m.upstream_strict(req)),req)
        self.assertNotEqual(g.sha(req),g.sha(g.canonical(m.upstream_strict(req))))
    def test_unicode_canonical(self):
        obj={'質問':'台帳の検査','nested':{'漢字':'空'}}; self.assertEqual(v01(obj),m.upstream_canonical(obj))
        self.assertEqual(m.upstream_strict(v01(obj)),obj)
    def test_transport_encoding_unchanged(self):
        raw=g.canonical({'日本語':'質問'}); self.assertEqual(g.strict(raw),{'日本語':'質問'})
        with self.assertRaises(ValueError): m.upstream_strict(raw)
        with self.assertRaises(ValueError): g.strict(v01({'日本語':'質問'}))
    def test_missing_lf_rejected(self):
        q,req,ctx=ingress();
        with self.assertRaisesRegex(ValueError,'UPSTREAM_NONCANONICAL'): m.exact_turn(q,req,ctx[:-1])
    def test_duplicate_and_nonfinite_rejected(self):
        for raw in (b'{"a":1,"a":1}\n',b'{"a":NaN}\n'):
            with self.subTest(raw=raw),self.assertRaises(ValueError): m.upstream_strict(raw)
    def test_changed_question_rejected(self):
        q,req,ctx=ingress();
        with self.assertRaisesRegex(ValueError,'INGRESS_CONTEXT_BINDING'): m.exact_turn(q+b'!',req,ctx)
    def test_changed_request_rejected(self):
        q,req,ctx=fixture(); req['seq']=2
        with self.assertRaisesRegex(ValueError,'INGRESS_CONTEXT_BINDING'): m.exact_turn(q,v01(req),v01(ctx))
    def test_wrong_audience_rejected(self):
        q,req,ctx=fixture();ctx['audience']='public'
        with self.assertRaisesRegex(ValueError,'CONTEXT_AUDIENCE_CHALLENGE'): m.exact_turn(q,v01(req),v01(ctx))
    def test_wrong_request_challenge_rejected(self):
        q,req,ctx=fixture();ctx['challenge']='f'*64
        with self.assertRaisesRegex(ValueError,'CONTEXT_AUDIENCE_CHALLENGE'): m.exact_turn(q,v01(req),v01(ctx))
    def test_bool_sequence_rejected(self):
        q,req,ctx=fixture(); req['seq']=True;ctx['request_sha256']=g.sha(v01(req))
        with self.assertRaisesRegex(ValueError,'REQUEST_SEQ'): m.exact_turn(q,v01(req),v01(ctx))
    def test_missing_or_extra_pin_rejected(self):
        for pins in ({},dict(fixture()[1]['expected_hashes'],extra='a'*64)):
            q,req,ctx=fixture();req['expected_hashes']=pins;ctx['request_sha256']=g.sha(v01(req))
            with self.assertRaisesRegex(ValueError,'EXPECTED_HASHES'):m.exact_turn(q,v01(req),v01(ctx))


class BridgeTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
        self.v,self.presenter,self.event,self.anchor,self.writer,self.receipt=(Ed25519PrivateKey.generate() for _ in range(6))
        def provider(ident):
            self.hs=x.AnchorService.provision(self.root/'host-external.db',ident,self.anchor,self.writer.public_key())
            self.hl=x.AnchorLink(ident,self.anchor.public_key(),self.writer,self.hs.handle); return self.hl
        self.host=m.CanonicalExternalHost(self.root/'host.db',self.root/'host-anchor.db',self.v.public_key(),self.presenter,self.event,
            authority_key=self.anchor.public_key(),writer_key=self.writer.public_key(),link_provider=provider)
        self.assertFalse(self.host._failed)
        ca,cw=Ed25519PrivateKey.generate(),Ed25519PrivateKey.generate()
        ident=d.identity('client',self.host.session_id,self.host.client_id,self.event.public_key(),self.presenter.public_key(),self.v.public_key())
        ih=g.sha(g.canonical(ident));self.cs=x.AnchorService.provision(self.root/'client-external.db',ih,ca,cw.public_key())
        self.cl=x.AnchorLink(ih,ca.public_key(),cw,self.cs.handle)
        self.client=m.CanonicalExternalClient(self.root/'client.db',self.root/'client-anchor.db',self.host.session_id,self.host.client_id,
            self.event.public_key(),self.presenter.public_key(),self.v.public_key(),self.cl,create=True)
        self.assertTrue(self.client.reconnect())
        # Byte fixture only, never executed; positive tests explicitly patch _run_v017.
        self.binary=self.root/'synthetic-binary-not-executable'; self.binary.write_bytes(b'NOT A LEAN EXECUTABLE')
        _,req,_=fixture();self.policy=m.HostPolicy('d'*64,req['seq'],req['tip'],tuple(sorted(req['expected_hashes'].items())),g.sha(self.binary.read_bytes()))
        self.bridge=m.McpBridge(self.host,self.policy,self.v,self.receipt)

    def arm(self,n=1,lean=None):
        q,req,ctx=fixture(n); self.args={'request':req,'context':ctx,'seed':{'question':q},'primary_raw':b'synthetic input'}
        self.assertIsNotNone(self.client.select_turn(q,v01(req),v01(ctx)))
        result=self.bridge.arm(q,snapshot=self.root,lean=self.binary if lean is None else lean,pair_inputs=self.args)
        self.assertIsNotNone(result);self.binding,event=result;self.client.notify(event)
        self.wire={'challenge':self.binding.challenge.nonce};return self.binding

    def projection(self,binding=None):
        b=binding or self.binding; v=view();
        values={k:None for k in m.r.LABELS};values['rule_count']=7
        ex={'lean_version':m.LEAN_VERSION,'lean_binary_sha256':self.policy.lean_binary_sha256,'exit_code':0,
            'stages':[{'module':module,'exit_code':0,'source_sha256':digest,'stdout_sha256':'4'*64} for module,digest in m.LEAN_SOURCES.items()],
            'stdout_sha256':'5'*64,'input_sha256':g.sha(self.args['primary_raw']),'request_sha256':b.challenge.request_sha256,'context_sha256':b.challenge.context_sha256,
            'result':{'status':'TYPED_JSON_PROJECTION_ONLY','reason':'','proof_authority':False,'action_authority':False,
                      'complete_python_refinement_proved':False,'claims':[{'claim_id':k,'value':val} for k,val in values.items()]}}
        obj={'schema':'kuuos.verifyos.lean-egress.v0.17','status':g.MATCH,'context_sha256':b.challenge.context_sha256,'execution':ex,**v}
        return obj,v

    def execute_fixture(self,mutate=lambda x:None):
        obj,v=self.projection();mutate(obj)
        # Protocol-only test double, never a production/actual Lean execution claim.
        with patch.object(g,'_run_v017',return_value=(v01(obj),v)) as mocked:
            response=self.bridge.handle(self.wire);self.assertEqual(mocked.call_count,1)
        return response

    def display(self):
        nonce=self.client.request_checkpoint();self.assertIsNotNone(nonce)
        self.client.accept_checkpoint(nonce,self.host.checkpoint(nonce))
        req=self.client.request()
        if req is None:return self.client.current()
        request,wire=req;return self.client.accept(request,self.host.present(wire))

    def test_real_anchored_ingress_without_lean(self):
        b=self.arm(lean=self.root/'absent');self.assertEqual(b.challenge.request_sha256,g.sha(v01(self.args['request'])))
        self.assertEqual(self.bridge.handle(self.wire)['status'],'HOLD');self.assertEqual(self.display().status,g.HOLD)
        self.assertEqual(self.host._tip,self.hl.read());self.assertEqual(self.client._tip,self.cl.read())
    def test_real_runtime_unavailable_no_positive(self):
        self.arm()  # actual wrapper, no patch, missing runtime or invalid executable
        self.assertEqual(self.bridge.handle(self.wire)['status'],'HOLD');self.assertEqual(self.display().status,g.HOLD)
    def test_positive_synthetic_protocol_and_closed_view(self):
        self.arm();response=self.execute_fixture();self.assertEqual(response['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY')
        self.assertEqual(m.inspect_receipt(response,self.receipt.public_key(),self.binding,self.policy)['status'],'SYNTHETIC_RECEIPT_SIGNATURE_MATCHED_ONLY')
        self.assertEqual(m.inspect_receipt(response,self.receipt.public_key(),self.binding,self.policy)['production_status'],'HOLD')
        payload=response['signed_receipt']['payload'];self.assertEqual(payload['classification'],'SYNTHETIC_ONLY')
        self.assertEqual(self.display().status,g.ALL); self.assertNotIn(self.args['seed']['question'],g.canonical(response));self.assertNotIn(b'synthetic input',g.canonical(response));self.assertNotIn(b'"view"',g.canonical(response))
    def test_synthetic_render_is_explicitly_labeled(self):
        self.assertIn(b'SYNTHETIC ONLY - NOT PRODUCTION',self.client.render())
        self.arm(); self.assertEqual(self.execute_fixture()['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY')
        self.assertEqual(self.display().status,g.ALL)
        self.assertIn(b'SYNTHETIC ONLY - NOT PRODUCTION',self.client.render())
    def test_tool_schema_no_caller_selected_inputs(self):
        self.arm()
        for extra in ({'tip':'f'*64},{'approved':True},{'lean_output':{}},{'path':'/tmp'},{'classification':'PRODUCTION'}):
            self.assertEqual(self.bridge.handle({**self.wire,**extra})['status'],'HOLD')
        self.assertEqual(self.execute_fixture()['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY')
    def test_wrong_challenge_does_not_consume(self):
        self.arm();self.assertEqual(self.bridge.handle({'challenge':'f'*64})['status'],'HOLD')
        self.assertEqual(self.execute_fixture()['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY')
    def test_replay_rejected(self):
        self.arm();self.assertEqual(self.execute_fixture()['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY');self.assertEqual(self.bridge.handle(self.wire)['status'],'HOLD')
    def test_receipt_tampering_rejected(self):
        self.arm();out=self.execute_fixture();out['signed_receipt']['payload']['seq']=2
        out['receipt_sha256']=g.sha(g.canonical(out['signed_receipt']))
        self.assertEqual(m.inspect_receipt(out,self.receipt.public_key(),self.binding,self.policy)['status'],'HOLD')
    def test_wrong_public_key_rejected(self):
        self.arm();out=self.execute_fixture();self.assertEqual(m.inspect_receipt(out,Ed25519PrivateKey.generate().public_key(),self.binding,self.policy)['status'],'HOLD')
    def test_wrong_binding_rejected(self):
        self.arm();out=self.execute_fixture();old=self.binding;self.arm(2)
        self.assertNotEqual(old,self.binding);self.assertEqual(m.inspect_receipt(out,self.receipt.public_key(),self.binding,self.policy)['status'],'HOLD')
        self.assertEqual(self.display().status,g.HOLD)
    def test_production_class_not_authorized(self):
        with self.assertRaisesRegex(ValueError,'PRODUCTION_AUTHORITY_UNAVAILABLE'):replace(self.policy,classification='PRODUCTION').validate()
    def test_policy_drift_rejected_before_execution(self):
        q,req,ctx=fixture();req['tip']='f'*64;ctx['request_sha256']=g.sha(v01(req))
        self.assertIsNone(self.bridge.arm(q,snapshot=self.root,lean=self.binary,pair_inputs={'request':req,'context':ctx,'seed':{'question':q}}))
    def test_missing_pins_do_not_create_policy(self):
        with self.assertRaises(ValueError):replace(self.policy,expected_hashes=()).validate()
    def test_lean_pin_mismatch_holds(self):
        self.arm();self.binary.write_bytes(b'changed')
        with patch.object(g,'_run_v017',side_effect=AssertionError('must not run')) as call:
            self.assertEqual(self.bridge.handle(self.wire)['status'],'HOLD');call.assert_not_called()
    def test_execution_fields_disagree(self):
        mutations=(lambda o:o['execution'].update(exit_code=1),lambda o:o['execution'].update(exit_code=False),
                   lambda o:o['execution'].update(lean_binary_sha256='6'*64),lambda o:o['execution'].update(input_sha256='7'*64),
                   lambda o:o['execution'].update(context_sha256='8'*64),lambda o:o['execution']['stages'][0].update(source_sha256='9'*64),
                   lambda o:o['execution']['result']['claims'].pop(),lambda o:o['execution']['result']['claims'][6].update(claim_id='unknown'),
                   lambda o:next(row for row in o['execution']['result']['claims'] if row['claim_id']=='rule_count').update(value=8))
        for i,mut in enumerate(mutations,1):
            with self.subTest(i=i):self.arm(i);self.assertEqual(self.execute_fixture(mut)['status'],'HOLD')
    def test_old_execution_after_new_turn_holds(self):
        self.arm();old_wire=dict(self.wire);obj,v=self.projection();started,finish=threading.Event(),threading.Event()
        def delayed(*a,**kw):
            started.set();self.assertTrue(finish.wait(4));return v01(obj),v
        with patch.object(g,'_run_v017',side_effect=delayed):
            with ThreadPoolExecutor(max_workers=1) as pool:
                f=pool.submit(self.bridge.handle,old_wire);self.assertTrue(started.wait(3));self.arm(2);finish.set();self.assertEqual(f.result(4)['status'],'HOLD')
        self.assertEqual(self.execute_fixture()['status'],'SYNTHETIC_EXECUTION_RECEIPT_ONLY')
    def test_concurrent_tool_invocations_one_shot(self):
        self.arm();obj,v=self.projection()
        with patch.object(g,'_run_v017',return_value=(v01(obj),v)) as call:
            with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(lambda _:self.bridge.handle(self.wire),range(8)))
            self.assertEqual(call.call_count,1)
        self.assertEqual(sum(r['status']=='SYNTHETIC_EXECUTION_RECEIPT_ONLY' for r in results),1)
    def test_anchor_unavailable_after_execution_holds(self):
        self.arm();obj,v=self.projection();original=self.hl.transport
        def fail(*a,**kw):self.hl.transport=lambda _:(_ for _ in ()).throw(TimeoutError('offline'));return v01(obj),v
        try:
            with patch.object(g,'_run_v017',side_effect=fail):self.assertEqual(self.bridge.handle(self.wire)['status'],'HOLD')
        finally:self.hl.transport=original
        self.assertTrue(self.host._failed);self.assertEqual(self.display().status,g.HOLD)
    def test_pilot_receipt_rejected(self):
        self.arm();raw=Path(__file__).parent.parent/'verifyos_v023/mcp_pilot_observation.json';pilot=json.loads(raw.read_bytes())
        self.assertEqual(m.inspect_receipt(pilot,self.receipt.public_key(),self.binding,self.policy)['status'],'HOLD')
    def test_signed_classification_change_still_rejected(self):
        self.arm();response=self.execute_fixture();payload=response['signed_receipt']['payload'];payload['classification']='PRODUCTION'
        wire=m._seal(self.receipt,payload);response['signed_receipt']=g.strict(wire);response['receipt_sha256']=g.sha(wire)
        self.assertEqual(m.inspect_receipt(response,self.receipt.public_key(),self.binding,self.policy)['status'],'HOLD')

if __name__=='__main__':unittest.main()
