"""Transport tests. Positive protocol fixture explicitly mocks Lean; no production."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import kuuos_verifyos_local_host_v0_25 as v
import test_kuuos_verifyos_mcp_bridge_v0_24 as f

m=v.m

class HostTests(unittest.TestCase):
    def setUp(self):
        self.fixture=f.BridgeTests('test_production_class_not_authorized')
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        t=self.fixture
        self.gate=v.LocalGate(t.bridge,t.policy,t.receipt.public_key())
        self.addCleanup(self.gate.close)
        self.socket_dir=t.root/'ipc'; self.socket_dir.mkdir(mode=0o700)
        self.path=self.socket_dir/'gate.sock'
    def arm(self,n=1,missing=False):
        t=self.fixture;q,req,ctx=f.fixture(n)
        t.args={'request':req,'context':ctx,'seed':{'question':q},'primary_raw':b'synthetic input'}
        self.assertIsNotNone(t.client.select_turn(q,f.v01(req),f.v01(ctx)))
        result=self.gate.arm(q,snapshot=t.root,lean=t.root/'absent' if missing else t.binary,pair_inputs=t.args)
        self.assertIsNotNone(result);t.binding,event=result;t.client.notify(event)
        self.request={'challenge':t.binding.challenge.nonce}
        return json.dumps(self.request).encode()
    def assert_hold(self,res):
        self.assertEqual((res['status'],res['production_status'],res['claims'],res['receipt']),('HOLD','HOLD',[],None))
    def positive(self,func):
        obj,view=self.fixture.projection()
        with patch.object(m.g,'_run_v017',return_value=(f.v01(obj),view)) as mock:
            result=func();self.assertEqual(mock.call_count,1)
        self.assertEqual(result['status'],'SYNTHETIC_RECEIPT_MATCHED_ONLY',result)
        self.assertEqual(result['production_status'],'HOLD');self.assertEqual(result['claims'],[])
        self.assertEqual(m.inspect_receipt(result['receipt'],self.fixture.receipt.public_key(),self.fixture.binding,self.fixture.policy)['status'],'SYNTHETIC_RECEIPT_SIGNATURE_MATCHED_ONLY')
        return result
    def rpc(self,request):
        with v.UnixGateServer(self.path,self.gate) as server,ThreadPoolExecutor(max_workers=1) as pool:
            job=pool.submit(server.serve_once);result=v.invoke_local(self.path,request);job.result(4);return result
    def test_no_armed_request(self): self.assert_hold(self.gate.dispatch(b'{"challenge":"'+b'a'*64+b'"}'))
    def test_real_missing_lean_through_socket(self):
        self.arm(missing=True);self.assert_hold(self.rpc(self.request));self.assert_hold(self.gate.dispatch(json.dumps(self.request).encode()))
    def test_signed_synthetic_protocol_through_socket(self):
        raw=self.arm();self.positive(lambda:self.rpc(self.request));self.assert_hold(self.gate.dispatch(raw))
    def test_wrong_challenge_does_not_consume(self):
        raw=self.arm();self.assert_hold(self.gate.dispatch(b'{"challenge":"'+b'f'*64+b'"}'));self.positive(lambda:self.gate.dispatch(raw))
    def test_invalid_fields_duplicate_nonfinite_and_type(self):
        raw=self.arm()
        for obj in ({**self.request,'path':'/tmp'},{**self.request,'question_id':'production_inventory'},{**self.request,'status':'PASS'},{'challenge':True}):
            self.assert_hold(self.gate.dispatch(json.dumps(obj).encode()))
        for invalid in (b'{"challenge":"x","challenge":"y"}',b'{"challenge":NaN}',b'\xff',b' '*1025):self.assert_hold(self.gate.dispatch(invalid))
        self.positive(lambda:self.gate.dispatch(raw))
    def test_production_policy_unavailable(self):
        t=self.fixture
        with self.assertRaisesRegex(ValueError,'PRODUCTION_AUTHORITY_UNAVAILABLE'):v.LocalGate(t.bridge,replace(t.policy,classification='PRODUCTION'),t.receipt.public_key())
    def test_wrong_receipt_key_holds(self):
        t=self.fixture;self.gate=v.LocalGate(t.bridge,t.policy,Ed25519PrivateKey.generate().public_key());self.addCleanup(self.gate.close)
        raw=self.arm();obj,view=t.projection()
        with patch.object(m.g,'_run_v017',return_value=(f.v01(obj),view)):self.assert_hold(self.gate.dispatch(raw))
        self.assert_hold(self.gate.dispatch(raw));self.assertEqual(t.display().status,m.g.HOLD)
    def test_new_turn_rejects_previous(self):
        old=self.arm();new=self.arm(2);self.assert_hold(self.gate.dispatch(old));self.positive(lambda:self.gate.dispatch(new))
    def test_invalidation(self):
        raw=self.arm();self.gate.invalidate();self.assert_hold(self.gate.dispatch(raw))
    def test_closed_terminal(self):
        raw=self.arm();self.gate.close();self.assert_hold(self.gate.dispatch(raw));t=self.fixture;q,req,ctx=f.fixture(2)
        self.assertIsNone(self.gate.arm(q,snapshot=t.root,lean=t.binary,pair_inputs={'request':req,'context':ctx,'seed':{'question':q}}))
    def test_concurrent_one_shot(self):
        raw=self.arm();obj,view=self.fixture.projection()
        with patch.object(m.g,'_run_v017',return_value=(f.v01(obj),view)) as mock,ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:self.gate.dispatch(raw),range(8)))
        self.assertEqual(mock.call_count,1);self.assertEqual(sum(x['status']=='SYNTHETIC_RECEIPT_MATCHED_ONLY' for x in results),1)
        self.assertTrue(all(x['production_status']=='HOLD' for x in results))
    def test_turn_change_during_execution(self):
        raw=self.arm();obj,view=self.fixture.projection();started=threading.Event();resume=threading.Event()
        def delayed(*a,**kw):
            started.set();self.assertTrue(resume.wait(3));return f.v01(obj),view
        with patch.object(m.g,'_run_v017',side_effect=delayed),ThreadPoolExecutor(max_workers=1) as pool:
            job=pool.submit(self.gate.dispatch,raw)
            try:self.assertTrue(started.wait(3));new=self.arm(2)
            finally:resume.set()
            self.assert_hold(job.result(4))
        self.positive(lambda:self.gate.dispatch(new))
    def test_actual_separate_process_transport(self):
        self.arm();obj,view=self.fixture.projection()
        script='import json,socket,sys\nwith socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:\n s.connect(sys.argv[1]); s.sendall(sys.argv[2].encode()+b"\\n"); print(s.makefile("rb").readline().decode(),end="")\n'
        with patch.object(m.g,'_run_v017',return_value=(f.v01(obj),view)) as mock,v.UnixGateServer(self.path,self.gate) as server,ThreadPoolExecutor(max_workers=1) as pool:
            job=pool.submit(server.serve_once)
            child=subprocess.run([sys.executable,'-c',script,str(self.path),json.dumps(self.request)],capture_output=True,timeout=10,check=True);job.result(4)
            self.assertEqual(mock.call_count,1);self.assertEqual(json.loads(child.stdout)['status'],'SYNTHETIC_RECEIPT_MATCHED_ONLY')
        self.assertFalse(self.path.exists())
    def test_existing_socket_path_not_removed(self):
        self.path.write_bytes(b'existing')
        with self.assertRaisesRegex(ValueError,'SOCKET_EXISTS'):v.UnixGateServer(self.path,self.gate)
        self.assertEqual(self.path.read_bytes(),b'existing')
    def test_public_directory_refused(self):
        self.socket_dir.chmod(0o755)
        with self.assertRaisesRegex(ValueError,'PRIVATE_SOCKET_DIRECTORY_REQUIRED'):v.UnixGateServer(self.path,self.gate)
    def test_socket_mode(self):
        with v.UnixGateServer(self.path,self.gate):self.assertEqual(self.path.stat().st_mode&0o777,0o600)
        self.assertFalse(self.path.exists())
    def test_multiple_frames_same_read(self):
        a,b=socket.socketpair()
        with a,b:
            a.sendall(b'{}\n{}\n')
            with self.assertRaisesRegex(ValueError,'EXTRA_FRAME'):v.read_line(b,1024)
    def test_incomplete_frame(self):
        a,b=socket.socketpair()
        with a,b:
            a.sendall(b'{}');a.shutdown(socket.SHUT_WR)
            with self.assertRaisesRegex(ValueError,'INCOMPLETE_LINE'):v.read_line(b,1024)
    def test_absolute_deadline(self):
        a,b=socket.socketpair()
        with a,b:
            with self.assertRaises(TimeoutError):v.read_line(b,1024,0.03)

if __name__=='__main__':unittest.main()
